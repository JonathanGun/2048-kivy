from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from random import randint, choice


class Cell(Button):
    colors = {
        "0": (0.9, 0.9, 0.9, 0.6),
        "2": (0.99, 0.99, 0.99, 1),
        "4": (1, 1, 0.9, 1),
        "8": (0.9, 0.7, 0.4, 1),
        "16": (0.95, 0.5, 0.2, 1),
        "32": (0.85, 0.4, 0.3, 1),
        "64": (0.8, 0.2, 0.1, 1),
        "128": (0.8, 0.8, 0.3, 1),
        "256": (0.82, 0.78, 0.2, 1),
    }
    default_color = (0.84, 0.76, 0.16, 1)

    def __init__(self, **kwargs):
        super(Button, self).__init__(**kwargs)
        self.num = 0
        self.font_size = 40
        self.background_color = self.colors.get(str(self.num), self.default_color)

    def setNum(self, num):
        self.num = num
        if(self.num != 0):
            self.text = str(self.num)
        else:
            self.text = ""
        self.background_color = self.colors.get(str(self.num), self.default_color)


class Board(GridLayout):
    full = False

    def __init__(self, size, **kwargs):
        super(Board, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        Window.size = (500, 500)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.cols = size
        self.cols = size
        self.buildBoard()

    def validCell(self, i, j):
        return 0 <= i < self.cols and 0 <= j < self.cols

    def reset(self):
        self.clear_widgets()
        self.buildBoard()

    def buildBoard(self):
        self.resetBoard()
        self.assignBoard()

    def resetBoard(self):
        self.board = [[Cell() for x in range(self.cols)] for y in range(self.cols)]
        self.generateNewNums(3)

    def assignBoard(self):
        for bs in self.board:
            for b in bs:
                self.add_widget(b)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if self.push(keycode[1]):
            self.generateNewNums(1)
        return True

    def push(self, direction):
        if(direction == "up"):
            for j in range(self.cols):
                tmp = []
                for i in range(self.cols):
                    num = self.board[i][j].num
                    if(num != 0):
                        tmp.append(num)
                self.condense(tmp)
                self.setNums(direction, j, tmp)
        elif(direction == "down"):
            for j in range(self.cols):
                tmp = []
                for i in range(self.cols):
                    num = self.board[self.cols - 1 - i][self.cols - 1 - j].num
                    if(num != 0):
                        tmp.append(num)
                self.condense(tmp)
                self.setNums(direction, self.cols - 1 - j, tmp)
        elif(direction == "left"):
            for i in range(self.cols):
                tmp = []
                for j in range(self.cols):
                    num = self.board[self.cols - 1 - i][j].num
                    if(num != 0):
                        tmp.append(num)
                self.condense(tmp)
                self.setNums(direction, self.cols - 1 - i, tmp)
        elif(direction == "right"):
            for i in range(self.cols):
                tmp = []
                for j in range(self.cols):
                    num = self.board[i][self.cols - 1 - j].num
                    if(num != 0):
                        tmp.append(num)
                self.condense(tmp)
                self.setNums(direction, i, tmp)
        else:
            return False
        return True

    def condense(self, tmp):
        i = 0
        while True:
            if i + 1 >= len(tmp):
                break
            if(tmp[i + 1] == tmp[i]):
                del tmp[i]
                tmp[i] *= 2
            else:
                i += 1

    def setNums(self, direction, idx, tmp):
        for i in range(self.cols):
            try:
                num = tmp[i]
            except IndexError:
                num = 0
            if(direction == "up"):
                self.board[i][idx].setNum(num)
            elif (direction == "down"):
                self.board[self.cols - 1 - i][idx].setNum(num)
            elif (direction == "left"):
                self.board[idx][i].setNum(num)
            elif (direction == "right"):
                self.board[idx][self.cols - 1 - i].setNum(num)

    def generateNewNums(self, n):
        self.full = True
        for i in range(self.cols):
            for j in range(self.cols):
                if(self.board[i][j].num == 0):
                    self.full = False
                if not self.full:
                    break
            if not self.full:
                break
        if self.full:
            print("Board is full!")
        else:
            for _ in range(n):
                c = None
                while(not c or c.num != 0):
                    i = randint(0, self.cols - 1)
                    j = randint(0, self.cols - 1)
                    c = self.board[i][j]
                c.setNum(choice([2, 4]))


class Game(App):
    def build(self):
        return Board(size=4)


if __name__ == "__main__":
    Game().run()
