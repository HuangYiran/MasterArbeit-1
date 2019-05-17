import sys
from PyQt5.QtWidgets import QApplication,QWidget,QMessageBox
from PyQt5.QtGui import QPainter,QPen,QColor
from PyQt5.QtCore import Qt,QPoint
from Controller import has_a_winner,get_player_and_avaiable,is_terminal
from MCTS import run_MCTS,State,Node
from Model import Model


class View(QWidget):
    def __init__(self):
        super().__init__(parent=None)
        self.initUI()

    def initUI(self):
        self.grid = 7
        self.line =  50
        self.model = Model()
        self.color = {0:"Player",1:"AI"}
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
        player_state,ai_state = get_player_and_avaiable(self.model.state)

        for i,piece_center in enumerate(player_state):
            piece_center = QPoint(piece_center[0], piece_center[1])
            qp.setBrush(QColor(Qt.black))
            qp.drawEllipse(piece_center, 20, 20)
        for i,piece_center in enumerate(ai_state):
            piece_center = QPoint(piece_center[0], piece_center[1])
            qp.setBrush(QColor(Qt.white))
            qp.drawEllipse(piece_center, 20, 20)

    # 鼠标点击，触发player下子和ai下子
    def mousePressEvent(self,event):
        click_location = (event.x(),event.y())
        player_select = self.model.player_move(click_location)

        if player_select is None:
            print("Pleace Reselect Location")
        else:
            # Player 走子
            if self.run_process(player_select):
                self.game_end()
                return
            self.player = self.player[::-1]

            # AI 走子
            player_select = self.model.AI_move()
            if self.run_process(player_select):
                self.game_end()
            self.player = self.player[::-1]
        self.update()

    #更新棋盘，判断赢家
    def run_process(self,player_select):
        self.model.board_update(player_select,self.player[0])
        terminal = is_terminal(self.model.state)
        return terminal

    # 游戏结束
    def game_end(self):
        buttonReply = QMessageBox.question(self, 'PyQt5 message', "{} is the winner.Play Again?".format(self.color[self.player[0]]),
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.close()
            self.initUI()
        else:
            self.close()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = View()
    app.exec_()