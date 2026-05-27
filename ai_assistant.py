"""Text test loop for the new Jarvis AI layer."""

from jarvis_ai import JarvisAI


def main() -> None:
    assistant = JarvisAI()
    print("Jarvis AI test loop. Type 'exit' to stop.")
    while True:
        user_text = input("You: ").strip()
        if user_text.lower() in {"exit", "quit"}:
            break
        print(f"Jarvis: {assistant.answer(user_text)}")


if __name__ == "__main__":
    main()
