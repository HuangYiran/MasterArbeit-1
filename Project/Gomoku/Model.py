import random
import numpy as np
from Controller import get_keys
from MCTS import run_MCTS

class Model():
    def __init__(self):
    # ALL Locations
        self.state = {}
        self.buildBoard()

    # 初始化棋盘的值
    def buildBoard(self):
        for i in range(100,410,50):
            for j in range(100,410,50):
                self.state[(i,j)] = -1
        #self.board_avaiable = list(self.state.keys())
        self.board_avaiable = get_keys(self.state, -1)
        self.board_array = list(self.state.keys())

    # 选择落子位置
    def player_select_location(self,x,y):
        click_location = np.array((x,y))
        distance = [np.linalg.norm(np.array(i) - click_location) for i in self.board_array]
        min_dis = np.argmin(distance)
        selected = self.board_array[int(min_dis)]
        return selected


    # AI Policy : Random
    def AI_move(self):
        #selected = random.choice(self.board_avaiable)
        selected = run_MCTS(self.state)
        #selected = run_MCTS(self.pieces,self.board_avaiable)
        return selected

    # Player move
    def player_move(self,click_location):
        x_coord = click_location[0]
        y_coord = click_location[1]
        if (x_coord>= 100) and (x_coord<= 410) and (y_coord>=100) and (y_coord<=410):
            selected = self.player_select_location(x_coord,y_coord)
            if selected in self.board_avaiable:
                return selected
            else:
                return None
        else:
            return None

    # 更新步数和和剩余棋盘位置
    def board_update(self,selected,player):
        self.board_avaiable.remove(selected)
        self.state[selected] = player