from tkinter import *
from tkinter import messagebox as tkMessageBox
import random

ROW = 9
COL = 9
MINE_COUNT = 10

root = Tk()
root.title('天天扫雷')

TYPE_0 = 0  # 普通格子
TYPE_1 = 1  # 数字格子
TYPE_2 = 2  # 雷格子


class App:
    """
    扫雷
    """

    def __init__(self, master):
        self.level = 1
        self.master = master
        self.frame = Frame(master)  # 主区块
        self.label_frame = Frame(master)  # 标签区块
        self.images = {
            "plain": PhotoImage(file="images/tile_plain.gif"),
            "clicked": PhotoImage(file="images/tile_clicked.gif"),
            "mine": PhotoImage(file="images/tile_mine.gif"),
            "flag": PhotoImage(file="images/tile_flag.gif"),
            "wrong": PhotoImage(file="images/tile_wrong.gif"),
            "numbers": []
        }
        for i in range(1, 9):
            self.images["numbers"].append(
                PhotoImage(file="images/tile_"+str(i)+".gif"))
        # 等级制度
        self.levels = {
            1: {'row': 9, 'col': 9, 'mine_count': 10},
            2: {'row': 16, 'col': 16, 'mine_count': 40},
            3: {'row': 16, 'col': 30, 'mine_count': 99},
        }
        # 类型点击事件
        self.type_events = {
            TYPE_0: self.clickEmpty,
            TYPE_1: self.clickNumber,
            TYPE_2: self.clickMine
        }
        # 开始游戏
        self.frame.pack()
        self.label_frame.pack()
        self.startGame()

    def setup(self):
        """
        安装游戏 初始化地图和雷数等信息
        """
        if self.level <= 0:
            self.level = 1

        level = self.levels[self.level]
        self.row = level['row']
        self.col = level['col']
        self.mine_count = level['mine_count']

        # 初始化地图
        self.map = [[{
            'x': i,  # x轴坐标
            'y': j,  # y轴坐标
            'type': TYPE_0,  # 类型 0 空格 1 数量 2 雷
            'num': 0,  # 周围雷的数量
            'show': 0,  # 是否已点击显示
            'flag': 0  # 是否立了旗子
        } for j in range(self.col)]
            for i in range(self.row)]

        # 初始化雷和数字
        self.mines = random.sample(sum(self.map, []), self.mine_count)
        for mine in self.mines:
            self.map[mine['x']][mine['y']]['type'] = TYPE_2
            neighbors = self.getNeighbors(mine['x'], mine['y'])
            for n in neighbors:
                if self.map[n[0]][n[1]]['type'] != TYPE_2:
                    self.map[n[0]][n[1]]['type'] = TYPE_1
                    self.map[n[0]][n[1]]['num'] += 1

        # 显示和绑定点击事件
        for x in range(self.row):
            for y in range(self.col):
                btn = Button(self.frame, image=self.images['plain'])
                btn.bind('<Button-1>', self.leftClick(x, y))
                btn.bind('<Button-3>', self.rightClick(x, y))
                btn.grid(row=x, column=y)
                self.map[x][y]['btn'] = btn

        # 其他标签
        self.labels = {
            'time': Label(self.label_frame, text='计时: 0'),
            'flag': Label(self.label_frame, text='剩余: ' + str(self.mine_count))
        }
        self.labels['time'].grid(row=self.row + 1, column=0)
        self.labels['flag'].grid(row=self.row + 1, column=self.col // 2)
    
    def timer(self):
        """
        计时
        """
        if self.clicked_count == 0:
            return False
        self.time += 1
        self.labels['time'].config(text='计时: ' + str(self.time))
        self.master.after(1000, self.timer)

    def getNeighbors(self, x, y):
        """
        获取周围格子坐标列表
        :param x: x坐标
        :param y: y坐标
        :return list((x, y))
        """
        return [(i, j) for i in range(max(0, x - 1), min(self.col - 1, x + 1) + 1)
                for j in range(max(0, y - 1), min(self.row - 1, y + 1) + 1) if i != x or j != y]

    def leftClick(self, x, y):
        return lambda Click: self._leftClick(x, y)

    def _leftClick(self, x, y):
        """
        鼠标左键点击事件
        """
        block = self.map[x][y]
        self.type_events[block['type']](x, y)
        if (self.clicked_count == self.row * self.col - self.mine_count):
            self.gameOver(True)

        if self.clicked_count == 1:
            self.timer()

    def rightClick(self, x, y):
        return lambda Click: self._rightClick(x, y)

    def _rightClick(self, x, y):
        """
        鼠标右键点击事件
        """
        block = self.map[x][y]
        if not block['show']:
            if block['flag']:
                block['btn'].config(image=self.images['plain'])
                block['flag'] = 0
                self.flag_count -= 1
            else:
                block['btn'].config(image=self.images['flag'])
                block['flag'] = 1
                self.flag_count += 1
            self.map[x][y] = block
            self.labels['flag'].config(text='剩余: ' + str(self.mine_count - self.flag_count))

    def clickEmpty(self, x, y):
        """
        点击空处
        """
        block = self.map[x][y]
        if not block['show']:
            block['btn'].config(image=self.images['clicked'])
            self.map[x][y]['show'] = 1
            self.clicked_count += 1
            neighbors = self.getNeighbors(x, y)
            for n in neighbors:
                if self.map[n[0]][n[1]]['show'] == 0:
                    self.type_events[self.map[n[0]][n[1]]['type']](n[0], n[1])

    def clickNumber(self, x, y):
        """
        点击数量
        """
        block = self.map[x][y]
        if block['show'] == 0:
            block['btn'].config(image=self.images['numbers'][block['num'] - 1])
            block['show'] = 1
            self.clicked_count += 1
            self.map[x][y] = block

    def clickMine(self, x, y):
        """
        点击雷
        """
        block = self.map[x][y]
        block['btn'].config(image=self.images['mine'])
        self.gameOver()

    def startGame(self, level=None):
        """
        开始或重新开始游戏
        """
        if not level is None:
            self.level = level
        self.clicked_count = 0  # 已点击数量
        self.flag_count = 0 # 已放置旗帜数量
        self.time = 0 # 清空计时
        self.setup()

    def gameOver(self, win=False):
        """
        游戏结束
        """
        if not win:
            for x in range(self.row):
                for y in range(self.col):
                    block = self.map[x][y]
                    if block['show'] == 0:
                        if block['flag'] == 1 and block['type'] != TYPE_2:  # 错误
                            block['btn'].config(image=self.images['wrong'])

                        if block['flag'] == 0 and block['type'] == TYPE_2:  # 显示所有雷
                            block['btn'].config(image=self.images['mine'])

        msg = '你赢了, 用时' + str(self.time) + ' 是否继续' if win else '你输了, 是否继续'
        rs = tkMessageBox.askyesno('游戏结束', msg)
        if rs:
            self.startGame()
        else:
            self.master.quit()


app = App(root)
mainmenu = Menu(root)
startmenu = Menu(mainmenu)
startmenu.add_command(label="简单", command=lambda: app.startGame(1))
startmenu.add_command(label="困难", command=lambda: app.startGame(2))
startmenu.add_command(label="地域", command=lambda: app.startGame(3))
mainmenu.add_cascade(label="游戏难度", menu=startmenu)
root['menu'] = mainmenu

root.mainloop()
