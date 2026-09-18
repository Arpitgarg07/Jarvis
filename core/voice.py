import speech_recognition as sr
import win32com.client as wincl
import threading
import time

# Single SAPI voice instance
_speaker = wincl.Dispatch("SAPI.SpVoice")

# SAPI speaking flags
_SAPI_ASYNC = 1
_SAPI_STOP  = 3

# State
_last_spoken: str = ""
_interrupted: bool = False

# Words that trigger interrupt — checked against recognized speech
_INTERRUPT_WORDS = {
    "ok", "okay", "stop", "wait", "enough", "pause", "hold on",
    "got it", "i understand", "understood", "yes", "yeah",
    "shut up", "quiet", "alright", "fine", "no", "nope",
    "i got it", "ok ok", "wait wait", "stop stop", "no no",
    "that's fine", "i know", "thanks", "thank you"
}


def _is_speaking() -> bool:
    try:
        return _speaker.Status.RunningState == 2
    except Exception:
        return False


def _stop_now():
    """Hard-stop SAPI immediately."""
    try:
        _speaker.Skip("Sentence", 9999)
    except Exception:
        pass
    try:
        _speaker.Speak("", _SAPI_STOP)
    except Exception:
        pass


def Speak(audio: str) -> None:
    """
    Speak text via SAPI async.
    Interrupt detection runs in a background thread using
    speech_recognition.listen_in_background — no PyAudio conflict with SAPI.
    When user says any interrupt word, SAPI is hard-stopped instantly.
    """
    global _last_spoken, _interrupted

    _last_spoken = audio
    _interrupted = False

    print(f"Jarvis: {audio}")

    # Start SAPI speaking in background
    try:
        _speaker.Speak(audio, _SAPI_ASYNC)
    except Exception as e:
        print(f"Speak error: {e}")
        return

    # Event that fires when interrupt is detected
    _stop_event = threading.Event()

    # Recognizer for interrupt — separate instance from TakeCommand
    _r = sr.Recognizer()
    _r.energy_threshold = 1200       # high enough to ignore SAPI bleed
    _r.dynamic_energy_threshold = False
    _r.pause_threshold = 0.8         # must be >= non_speaking_duration (default 0.8)
    _r.non_speaking_duration = 0.4   # must be <= pause_threshold

    def _on_speech(recognizer, audio_data):
        """Called by listen_in_background when audio chunk is ready."""
        if _stop_event.is_set():
            return
        try:
            text = recognizer.recognize_google(
                audio_data, language="en-in").lower()
            print(f"  [heard: '{text}']")
            words = set(text.split())
            if words & _INTERRUPT_WORDS:
                _stop_event.set()
        except sr.UnknownValueError:
            pass
        except Exception:
            pass

    # Start background listener — returns a stop function
    try:
        mic = sr.Microphone()
        with mic as source:
            _r.adjust_for_ambient_noise(source, duration=0.3)

        stop_listening = _r.listen_in_background(mic, _on_speech,
                                                  phrase_time_limit=3)
    except Exception as e:
        print(f"Interrupt listener error: {e}")
        # Fallback: just speak without interrupt support
        while _is_speaking():
            time.sleep(0.05)
        return

    # Wait: either natural finish or interrupt
    while _is_speaking() and not _stop_event.is_set():
        time.sleep(0.05)

    # Stop the background listener
    stop_listening(wait_for_stop=False)

    if _stop_event.is_set():
        # User interrupted — kill SAPI immediately
        _stop_now()
        _interrupted = True
        time.sleep(0.15)
        # Say "Okay" to confirm we heard the user
        _speaker.Speak("Okay.", _SAPI_ASYNC)
        while _is_speaking():
            time.sleep(0.05)
        print("  [Jarvis stopped]")
    else:
        # Natural end — drain any remaining buffer
        while _is_speaking():
            time.sleep(0.05)


def was_interrupted() -> bool:
    return _interrupted


def last_spoken() -> str:
    return _last_spoken


def TakeCommand() -> str:
    """
    Listen until user fully stops speaking.
    pause_threshold=2.5s → waits 2.5s of silence before deciding done.
    phrase_time_limit=None → no cap on speech length.
    """
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.8)
        r.pause_threshold = 2.5
        r.non_speaking_duration = 1.5
        r.dynamic_energy_threshold = True
        r.dynamic_energy_adjustment_damping = 0.15
        r.dynamic_energy_ratio = 1.5

        try:
            audio = r.listen(source, timeout=8, phrase_time_limit=None)
        except sr.WaitTimeoutError:
            return "None"

    try:
        query = r.recognize_google(audio, language="en-in")
        print(f"You said: {query}\n")
        return query
    except sr.UnknownValueError:
        return "None"
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
        return "None"
