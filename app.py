from tkinter import *

root = Tk()

class App(Frame):
    def startGame(self):
        print('开始游戏')

app = App()
mainmenu = Menu(root)
startmenu = Menu(mainmenu)
startmenu.add_command(label="开始游戏", command=app.startGame)
mainmenu.add_cascade(label="开始", menu=startmenu)
root['menu'] = mainmenu
root.mainloop()