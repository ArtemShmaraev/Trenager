import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QWidget, QTableWidgetItem, QPushButton, QLabel, \
    QMessageBox
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from random import randint
from PyQt5 import QtCore, QtGui, QtWidgets


class Game:
    def __init__(self):
        self.levels = []
        self.star = []
        f = open("main.txt")
        data = f.read().split("\n")
        for i in range(4):
            s = []
            for j in range(18):
                s.append(int(data[i][j]))
            self.levels.append(s)

        for i in range(4):
            s = []
            for j in range(18):
                s.append(int(data[i + 4][j]))
            self.star.append(s)
        f.close()


class Level:
    def __init__(self, n, bad, k, ok, i, znak):
        self.n_primer = n
        self.bad = bad
        self.k = k
        self.i = i
        self.ok = ok
        self.znak = znak
        if self.znak == "*":
            self.games = 0
        if self.znak == "+":
            self.games = 1
        if self.znak == "-":
            self.games = 2
        if self.znak == "/":
            self.games = 3

    def next(self, star):
        if game.levels[self.games][self.i] == 1 or (
                game.levels[self.games][self.i] == 2 and game.star[self.games][self.i] < star):
            game.levels[self.games][self.i] = 2
            game.star[self.games][self.i] = star
            if len(game.levels[self.games]) != self.i + 1:
                game.levels[self.games][self.i + 1] = 1

            f = open("main.txt", "w")

            for i in range(4):
                result = "".join([str(item) for item in game.levels[i]]) + "\n"
                f.write(result)
            for i in range(4):
                result = "".join([str(item) for item in game.star[i]]) + "\n"
                f.write(result)
            f.close()


game = Game()


class Show_levels(QWidget):
    def __init__(self, znak):
        super().__init__()
        self.btn = {}
        self.znak = znak
        if self.znak == "*":
            self.games = 0
        if self.znak == "+":
            self.games = 1
        if self.znak == "-":
            self.games = 2
        if self.znak == "/":
            self.games = 3
        self.initUI()

    def initUI(self):
        self.resize(1920, 1080)
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowTitle("Уровни")
        self.setStyleSheet("background-color: #69BE94")
        self.exitbtn = QPushButton("Выход", self)
        self.exitbtn.resize(150, 75)
        self.exitbtn.move(30, 30)
        self.exitbtn.setStyleSheet(
            "background-color: rgb(85, 150, 127); border-radius: 15px; font-size: 20pt; color: rgb(255, 255, "
            "255); font-weight: bold")
        self.exitbtn.clicked.connect(self.exit)

        self.label = QLabel(self)
        self.label.move(800, 30)
        self.label.setStyleSheet(
            "font-size: 36pt; color: rgb(255, 255, 255); font-weight: bold")
        if self.games == 0:
            self.label.setText("Умножение")
        if self.games == 1:
            self.label.setText("Сложение")
        if self.games == 2:
            self.label.setText("Вычитание")
        if self.games == 3:
            self.label.setText("Деление")



        x = 120
        y = 135
        k = 0
        for i in range(3):
            for j in range(6):
                k += 1
                self.btn[(i, j)] = QPushButton(str(k), self)
                self.btn[(i, j)].resize(225, 225)
                self.btn[(i, j)].move(x, y)
                if game.levels[self.games][k - 1] == 0:
                    self.btn[(i, j)].setStyleSheet(
                        "color: rgb(255, 255, 255); background-color: #ca3120; border-radius: 55px; font-size: 32pt; "
                        "font-weight: bold")
                    self.btn[(i, j)].setEnabled(False)
                if game.levels[self.games][k - 1] == 1:
                    self.btn[(i, j)].setStyleSheet(
                        "color: rgb(255, 255, 255); background-color:rgb(85, 0, 255); border-radius: 55px; font-size: "
                        "32pt; font-weight: bold")
                if game.levels[self.games][k - 1] == 2:
                    self.btn[(i, j)].setStyleSheet(
                        "color: rgb(255, 255, 255); background-color:rgb(52, 162, 35); border-radius: 55px; "
                        "font-size: 32pt; font-weight: bold")
                    self.btn[(i, j)].setText(f"{str(k)} ({str(game.star[self.games][k - 1])})")
                    if game.star[self.games][k - 1] == 5:
                        self.btn[(i, j)].setStyleSheet(
                            """background-color:
                               rgb(255, 220, 90); 
                               border: 6px solid rgb(255, 176, 16);
                               border-radius: 35px; 
                               color: rgb(100, 100, 100); font-size: 36pt; font-weight: bold""")
                        self.btn[(i, j)].setText(str(k))
                self.btn[(i, j)].clicked.connect(self.select)

                x += 300
            y += 300
            x = 120

    def select(self):
        text = self.sender().text()
        c = text.find(" ")
        if c == -1:
            k = int(text)
        else:
            text1 = text[:c]
            k = int(text1)
        i = k - 1
        n = k * 2
        if k % 2 != 0:
            k += 1
        k += 2
        do_k = k / 2
        bad = 5
        ok = 0
        if i > 2:
            ok = 1

        level = Level(n, bad, do_k, ok, i, self.znak)
        self.play = Play_level(level)
        self.play.showFullScreen()
        self.close()

    def exit(self):
        self.close()
        self.ex = Menu()
        self.ex.showFullScreen()


class Result(QMainWindow):
    def __init__(self, bad, level):
        super().__init__()
        uic.loadUi('result.ui', self)  # Загружаем дизайн
        self.pushButton_6.clicked.connect(self.menu)
        self.pushButton_2.clicked.connect(self.next)
        self.pushButton.clicked.connect(self.repeat)
        self.lvl = level
        self.bad = bad
        if self.bad >= self.lvl.bad:
            self.label.setText(f"{self.lvl.i + 1} Уровень не пройден")
            self.pushButton_2.hide()
            self.pushButton_3.hide()
            self.pushButton_4.hide()
            self.pushButton_5.hide()
            self.pushButton_7.hide()
            self.pushButton_8.hide()
        else:
            self.label.setText(f"{self.lvl.i + 1} Уровень пройден")
            if self.bad == 4:
                self.pushButton_4.hide()
            if self.bad >= 3:
                self.pushButton_5.hide()
            if self.bad >= 2:
                self.pushButton_7.hide()
            if self.bad >= 1:
                self.pushButton_8.hide()
            self.lvl.next(5 - self.bad)
            if len(game.levels[self.lvl.games]) == self.lvl.i + 1:
                self.pushButton_2.hide()

    def repeat(self):
        k = self.lvl.i + 1
        i = k - 1
        n = k * 2
        if k % 2 != 0:
            k += 1
        k += 2
        do_k = k / 2
        bad = 5
        ok = 0
        if i > 2:
            ok = 1
        level = Level(n, bad, do_k, ok, i, self.lvl.znak)
        self.play = Play_level(level)
        self.play.showFullScreen()
        self.close()

    def menu(self):
        self.close()
        self.show_l = Show_levels(self.lvl.znak)
        self.show_l.showFullScreen()

    def next(self):
        k = self.lvl.i + 2
        i = k - 1
        n = k * 2
        if k % 2 != 0:
            k += 1
        k += 2
        do_k = k / 2
        bad = 5
        ok = 0
        if i > 2:
            ok = 1
        level = Level(n, bad, do_k, ok, i, self.lvl.znak)
        self.play = Play_level(level)
        self.play.showFullScreen()
        self.close()


class Play_level(QMainWindow):
    def __init__(self, level):
        super().__init__()
        uic.loadUi('level.ui', self)  # Загружаем дизайн
        self.lvl = level
        self.pushButton.clicked.connect(self.next_primer)
        self.pushButton_2.clicked.connect(self.exit)
        if self.lvl.znak == "-":
            self.a = randint(self.lvl.ok + 1, self.lvl.k * 3)
            self.b = randint(self.lvl.ok, self.a)
        elif self.lvl.znak == "+":
            self.a = randint(self.lvl.ok + 1, self.lvl.k * 3)
            self.b = randint(self.lvl.ok, self.lvl.k * 3)
        elif self.lvl.znak == "/":
            c = randint(self.lvl.ok + 1, self.lvl.k)
            self.a = randint(self.lvl.ok + 1, self.lvl.k) * c
            self.b = c
        else:
            self.a = randint(self.lvl.ok, self.lvl.k)
            self.b = randint(self.lvl.ok + 1, self.lvl.k)
        self.n = 0
        self.bad = 0
        self.label_2.setText(f"{self.a} {self.lvl.znak} {self.b} = ")
        self.label.setText(f"{self.lvl.i + 1} Уровень | Пример {self.n + 1} из {self.lvl.n_primer}   ")
        self.label_3.setText("")

    def exit(self):
        self.close()
        self.show_l = Show_levels(self.lvl.znak)
        self.show_l.showFullScreen()

    def next_primer(self):
        self.label_3.setText("")
        if self.lineEdit.text() == "":
            pass
        else:
            try:
                if int(self.lineEdit.text()) == eval(str(self.a) + self.lvl.znak + str(self.b)):
                    self.n += 1
                    if self.n + 1 == self.lvl.n_primer:
                        self.pushButton.setText("Закончить уровень!")
                    if self.n == self.lvl.n_primer:
                        self.res = Result(self.bad, self.lvl)
                        self.res.show()
                        self.close()

                    if self.lvl.znak == "-":
                        self.a = randint(self.lvl.ok + 1, self.lvl.k * 2)
                        self.b = randint(self.lvl.ok, self.a)
                    elif self.lvl.znak == "+":
                        self.a = randint(self.lvl.ok + 1, self.lvl.k * 2)
                        self.b = randint(self.lvl.ok, self.lvl.k * 2)
                    elif self.lvl.znak == "/":
                        c = randint(self.lvl.ok + 1, self.lvl.k)
                        self.a = randint(self.lvl.ok + 1, self.lvl.k) * c
                        self.b = c
                    else:
                        self.a = randint(self.lvl.ok, self.lvl.k)
                        self.b = randint(self.lvl.ok + 1, self.lvl.k)

                    self.label_2.setText(f"{self.a} {self.lvl.znak} {self.b} = ")
                    self.label.setText(f"{self.lvl.i + 1} Уровень | Пример {self.n + 1} из {self.lvl.n_primer}   ")
                    self.lineEdit.setText("")

                else:
                    self.label_3.setText("Неверно, попробуй еще раз")
                    self.bad += 1
                    self.lineEdit.setText("")
            except ValueError:
                self.lineEdit.setText("")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.next_primer()


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('menu.ui', self)  # Загружаем дизайн
        self.pushButton.clicked.connect(self.show_levels_u)
        self.pushButton_2.clicked.connect(self.show_levels_p)
        self.pushButton_3.clicked.connect(self.show_levels_m)
        self.pushButton_4.clicked.connect(self.show_levels_d)
        self.label_2.setText(str(sum(game.star[0])) + " / 90 ")
        self.label_3.setText(str(sum(game.star[1])) + " / 90 ")
        self.label_4.setText(str(sum(game.star[2])) + " / 90 ")
        self.label_5.setText(str(sum(game.star[3])) + " / 90 ")

        p1 = int((sum(game.star[0]) / 90) * 100)
        if p1 == 100:
            self.pushButton.setStyleSheet(f"""background-color:
                                   rgb({str(int(85 + (1.7 * p1)))}, {str(int(150 + (0.7 * p1)))}, {str(int(127 - (0.63 * p1)))}); 
                                   border-radius: 15px; 
                                   color: rgb({str(int(255 - (1.55 * p1)))}, {str(int(255 - (1.55 * p1)))}, {str(int(255 - (1.55 * p1)))});
                                   border: 4px solid rgb(255, 176, 16)""")
        else:
            self.pushButton.setStyleSheet(f"""background-color:
                       rgb({str(int(85 + (1.7 * p1)))}, {str(int(150 + (0.7 * p1)))}, {str(int(127 - (0.63 * p1)))}); 
                       border-radius: 15px; 
                       color: rgb(255, 255, 255)""")

        p2 = int((sum(game.star[1]) / 90) * 100)
        if p2 == 100:
            self.pushButton_2.setStyleSheet(f"""background-color:
                                   rgb({str(int(85 + (1.7 * p2)))}, {str(int(150 + (0.7 * p2)))}, {str(int(127 - (0.63 * p2)))}); 
                                   border-radius: 15px; 
                                   color: rgb({str(int(255 - (1.55 * p1)))}, {str(int(255 - (1.55 * p2)))}, {str(int(255 - (1.55 * p2)))});
                                   border: 4px solid rgb(255, 176, 16)""")
        else:
            self.pushButton_2.setStyleSheet(f"""background-color:
                       rgb({str(int(85 + (1.7 * p2)))}, {str(int(150 + (0.7 * p2)))}, {str(int(127 - (0.63 * p2)))}); 
                       border-radius: 15px; 
                       color: rgb(255, 255, 255)""")

        p3 = int((sum(game.star[2]) / 90) * 100)
        if p3 == 100:
            self.pushButton_3.setStyleSheet(f"""background-color:
                                   rgb({str(int(85 + (1.7 * p3)))}, {str(int(150 + (0.7 * p3)))}, {str(int(127 - (0.63 * p3)))}); 
                                   border-radius: 15px; 
                                   color: rgb({str(int(255 - (1.55 * p3)))}, {str(int(255 - (1.55 * p3)))}, {str(int(255 - (1.55 * p3)))});
                                   border: 4px solid rgb(255, 176, 16)""")
        else:
            self.pushButton_3.setStyleSheet(f"""background-color:
                       rgb({str(int(85 + (1.7 * p3)))}, {str(int(150 + (0.7 * p3)))}, {str(int(127 - (0.63 * p3)))}); 
                       border-radius: 15px; 
                       color: rgb(255, 255, 255)""")

        p4 = int((sum(game.star[3]) / 90) * 100)
        if p4 == 100:
            self.pushButton_4.setStyleSheet(f"""background-color:
                                   rgb({str(int(85 + (1.7 * p4)))}, {str(int(150 + (0.7 * p4)))}, {str(int(127 - (0.63 * p4)))}); 
                                   border-radius: 15px; 
                                   color: rgb({str(int(255 - (1.55 * p4)))}, {str(int(255 - (1.55 * p4)))}, {str(int(255 - (1.55 * p4)))});
                                   border: 4px solid rgb(255, 176, 16)""")
        else:
            self.pushButton_4.setStyleSheet(f"""background-color:
                       rgb({str(int(85 + (1.7 * p4)))}, {str(int(150 + (0.7 * p4)))}, {str(int(127 - (0.63 * p4)))}); 
                       border-radius: 15px; 
                       color: rgb(255, 255, 255)""")

        progres = int(
            (((sum(game.star[3])) + (sum(game.star[2])) + (sum(game.star[1])) + (sum(game.star[0]))) / (90 * 4)) * 100)
        self.par.setValue(progres)

    def show_levels_u(self):
        self.show_l = Show_levels("*")
        self.show_l.showFullScreen()
        self.close()

    def show_levels_d(self):
        self.show_l = Show_levels("/")
        self.show_l.showFullScreen()
        self.close()

    def show_levels_p(self):
        self.show_l = Show_levels("+")
        self.show_l.showFullScreen()
        self.close()

    def show_levels_m(self):
        self.show_l = Show_levels("-")
        self.show_l.showFullScreen()
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.showFullScreen()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
