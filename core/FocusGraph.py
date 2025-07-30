#pip install matplotlib
import matplotlib.pyplot as pt

def focus_graph():
    file = open("focus.txt","r")
    content = file.read()
    file.close()

    content = content.split(",")
    x1 = []
    for i in range(0,len(content)):
        content[i] = float(content[i])
        x1.append(i)

    print(content)
    y1 = content

    pt.plot(x1,y1,color = "red",marker = "o")
    pt.title("YOUR FOCUSED TIME",fontsize = 16)
    pt.xlabel("Times",fontsize = 14)
    pt.ylabel("Focus Time", fontsize = 14)
    pt.grid()
    pt.show()