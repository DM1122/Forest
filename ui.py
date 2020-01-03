import tkinter as tk
from forest import *


def createNode():
    print('Creating Node')


    e = tk.Entry(root)
    e.pack()

def deleteNode():
    print('Deleting Node')



def callback(event):
    draw(event.x, event.y)

def draw(x, y):
    canvas.coords(circle, x-20, y-20, x+20, y+20)



if __name__ == '__main__':
    root = tk.Tk()
    title = tk.Label(root, text='Visual Tree Creator').pack()

    frame = tk.LabelFrame(root, text='Tools', padx=0, pady=0)
    frame.pack(padx=0, pady=0)

    createNodeButton = tk.Button(frame, text='Create Node', padx=5, pady=5, command=createNode)
    createNodeButton.pack()

    deleteNodeButton = tk.Button(frame, text='Delete Node', padx=5, pady=5, command=deleteNode)
    createNodeButton.pack()





    canvas = tk.Canvas(root, width=100, height=100)
    canvas.bind('<Motion>', callback)
    canvas.pack()

    circle = canvas.create_oval(0, 0, 0, 0)
    root.mainloop()

    

    root.mainloop()

