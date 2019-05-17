import sys
import random
import time
import copy
from PyQt5.QtWidgets import QMainWindow, QGridLayout,QApplication,QWidget,QLabel,QVBoxLayout,QMessageBox
from PyQt5.QtGui import QPainter,QPen,QColor,QBrush,QPixmap
from PyQt5.QtCore import Qt,QPoint
import numpy as np


from MCTS import run_MCTS,State,Node


class View(QWidget):
    def __init__(self):
        super().__init__(parent=None)
        self.initUI()

    def initUI(self):
        self.grid = 7

        self.line =  50
        # 存储棋盘对应的数据
        self.model = Model()
        self.color = {0:"Player",1:"AI"}
        # 存储当下棋手的信息 1 为 白子，0 为黑子 黑子先下
        self.player = [0,1]
        self.setGeometry(300,300,700,800)
        self.setWindowTitle("五子棋")
        self.show()

    def paintEvent(self,e):
        painter = QPainter()
        painter.begin(self)

        self.drawLines(painter)
        self.drawCircles(painter)
        painter.end()
        QApplication.processEvents()


    # 画棋盘
    def drawLines(self,qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)

        for i in range(self.grid):
            additional_width = self.line * i
            x_cord = 100 + additional_width
            y_cord = 100 + additional_width
            max_length = self.line * (self.grid - 1) + 100
            qp.drawLine(x_cord,100,x_cord,max_length)
            qp.drawLine(100,y_cord,max_length,y_cord)

    # 画棋子
    def drawCircles(self,qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        for i,piece_center in enumerate(self.model.pieces):
            piece_center = QPoint(piece_center[0], piece_center[1])
            if i%2 == 0:
                qp.setBrush(QColor(Qt.black))
            else:
                qp.setBrush(QColor(Qt.white))
            qp.drawEllipse(piece_center,20,20)


    # 更新棋盘和逻辑
    def mousePressEvent(self,event):
        x_coord = event.x()
        y_coord = event.y()
        click_location = (x_coord,y_coord)
        player_select = self.model.player_move(click_location)
        if player_select is None:
            print("Pleace Reselect Location")
        else:
            # Player Move
            self.model.board_update(player_select)
            if self.is_terminal():
                self.game_end()
                return
            self.player = self.player[::-1]

             #AI Move
            AI_select = self.model.AI_move()

            print("AI Select: ",AI_select)
            self.model.board_update(AI_select)
            if self.is_terminal():
                self.game_end()
            self.player = self.player[::-1]
        self.update()


    # 判定有没有结束
    def is_terminal(self):
        if len(self.model.pieces) < self.grid*self.grid and len(self.model.pieces)> 8 :
            all_pieces_location = self.model.pieces
            player = list(all_pieces_location)[::2]
            AI = list(set(all_pieces_location).difference(player))
            if self.who_wins(player):
                return True
            elif self.who_wins(AI):
                return True
            else:
                return False
        elif len(self.model.pieces) >= 49:
            return True
        else:
            return False

    # 判定谁是赢家
    def who_wins(self,black):
        for element in black:
            x = element[0]
            y = element[1]
            x_up = x
            y_up = y
            x_down = x
            y_down = y

            x_paral = [element]
            y_paral = [element]
            upper_right = [element]
            lower_right = [element]
            for i in range(4):
                x_up += 50
                x_down -= 50
                y_up += 50
                y_down -= 50

                x_paral.append((x_up,y))
                y_paral.append((x, y_up))
                upper_right.append((x_up,y_up))
                lower_right.append((x_up,y_down))

            if (set(x_paral).issubset(black)) or (set(y_paral).issubset(black)) or (set(upper_right).issubset(black)) or (set(lower_right).issubset(black)) :
                return True
        return False

    def game_end(self):
        buttonReply = QMessageBox.question(self, 'PyQt5 message', "{} is the winner.Play Again?".format(self.color[self.player[0]]),
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.close()
            self.initUI()
        else:
            self.close()

def has_a_winner(self, board):
    moved = board
    if (len(moved) < self.n_in_row + 2):
        return False, -1
    width = board.width
    height = board.height
    states = board.states
    n = self.n_in_row
    for m in moved:
        h = m // width
        w = m % width
        player = states[m]

        # 横向连城一线
        if (w in range(width - n + 1) and len(set(states[i] for i in range(m, m + n))) == 1):
            return True, player
        # 竖向连城一线
        if (h in range(height - n + 1) and len(set(states[i] for i in range(m, m + n * width, width))) == 1):
            return True, player
        if (w in range(width - n + 1) and h in range(height - n + 1) and len(
                set(states[i] for i in range(m, m + n * (width + 1), width + 1))) == 1):
            return True, player
        if (w in range(width - n + 1) and h in range(height - n + 1) and len(
                set(states[i] for i in range(m, m + n * (width - 1), width - 1))) == 1):
            return True, player
    return False, -1


class Model():
    def __init__(self):
    # ALL Locations
        self.pieces = []
        self.board_array = []
        self.board_avaiable = []

        # List stores 0 , 1 stands for player , 2 stands for AI
        self.moved = [0 for _ in range(49)]

        self.buildBoard()

    # 初始化棋盘的值
    def buildBoard(self):
        for i in range(100,410,50):
            for j in range(100,410,50):
                self.board_array.append((i,j))
        self.board_avaiable = copy.deepcopy(self.board_array)


    # 选择落子位置
    def player_select_location(self,x,y):
        click_location = np.array((x,y))
        distance = [np.linalg.norm(np.array(i) - click_location) for i in self.board_array]
        min_dis = np.argmin(distance)
        selected = self.board_array[int(min_dis)]
        return selected


    # AI Policy : Random
    def AI_move(self):
        selected = random.choice(self.board_avaiable)
        #selected = run_MCTS(self.pieces,self.board_avaiable)
        return selected

    # Player move
    def player_move(self,click_location):
        x_coord = click_location[0]
        y_coord = click_location[1]
        if (x_coord>= 100) and (x_coord<= 410) and (y_coord>=100) and (y_coord<=410):
            selected = self.player_select_location(x_coord,y_coord)
            if selected not in self.pieces:

            # if selected not in self.move:
                return selected
            else:
                return None
        else:
            return None

    # 更新步数和和剩余棋盘位置
    def board_update(self,selected):
        self.pieces.append(selected)
        self.board_avaiable.remove(selected)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = View()
    app.exec_()
