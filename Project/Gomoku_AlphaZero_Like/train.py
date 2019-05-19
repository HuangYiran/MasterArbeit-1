# 实现自我对弈

# Step1: Data Collcection

from __future__ import print_function
import random
import numpy as np
from collections import defaultdict, deque
from game import Board, Game
from mcts_prue import MCTSPlayer as MCTS_Pure
from mcts_NN import MCTSPlayer
from collections import deque
from policy_value_net_pytorch import PolicyValueNet



class TrainPipeline():
    def __init__(self, init_model=None):
        # params of the board and the game
        self.board_width = 6
        self.board_height = 6
        self.n_in_row = 4
        self.board = Board(width=self.board_width,
                           height=self.board_height,
                           n_in_row=self.n_in_row)
        self.game = Game(self.board)
        # training params
        self.learn_rate = 2e-3
        self.data_buffer = deque(maxlen=1000)
        self.batch_size = 10
        self.temp = 1.0  # the temperature param
        self.n_playout = 40 # num of simulations for each move
        self.c_puct = 5
        self.epochs = 50

        self.pure_mcts_playout_num = 2
        self.best_win_ratio = 0.0

        self.policy_value_net = PolicyValueNet(self.board_width,self.board_height)
        self.mcts_player = MCTSPlayer(self.policy_value_net.policy_value_fn,c_puct=self.c_puct,n_playout=self.n_playout,is_selfplay=1)


    def collect_selfplay_data(self,n_games=1):
        """collect self-play data for training"""
        print("Phase 1: Collecting Data")
        for i in range(n_games):
            winner, play_data = self.game.start_self_play(self.mcts_player,temp=self.temp)
            play_data = list(play_data)[:]
            self.data_buffer.extend(play_data)

    def policy_update(self):

        """update the policy-value net"""
        print("Phase 2: Updating the Network")
        mini_batch = random.sample(self.data_buffer, self.batch_size)

        state_batch = [data[0] for data in mini_batch]
        mcts_probs_batch = [data[1] for data in mini_batch]
        winner_batch = [data[2] for data in mini_batch]

        for i in range(self.epochs):
            loss, entropy = self.policy_value_net.train_step(
                    state_batch,
                    mcts_probs_batch,
                    winner_batch,
                    self.learn_rate)
            #print("Loss is {}, Entropy is {}".format(loss,entropy))
        return loss, entropy

    def policy_evaluate(self, n_games=10):
        """
        Evaluate the trained policy by playing against the pure MCTS player
        Note: this is only for monitoring the progress of training
        """

        print("Phase 3: Evaluatiing the Network")
        current_mcts_player = MCTSPlayer(self.policy_value_net.policy_value_fn,
                                         c_puct=self.c_puct,
                                         n_playout=self.n_playout)
        pure_mcts_player = MCTS_Pure(c_puct=5,
                                     n_playout=self.pure_mcts_playout_num)
        win_cnt = defaultdict(int)
        for i in range(n_games):
            winner = self.game.start_play(current_mcts_player,
                                          pure_mcts_player,
                                          start_player=i % 2,is_shown=0)
            win_cnt[winner] += 1
        win_ratio = 1.0*(win_cnt[1] + 0.5*win_cnt[-1]) / n_games
        print("num_playouts:{}, win: {}, lose: {}, tie:{}".format(
                self.pure_mcts_playout_num,
                win_cnt[1], win_cnt[2],
                win_cnt[-1]))
        return win_ratio

    def run(self):
        """run the training pipeline"""
        try:
            for i in range(5):
                print("Then {} / {} Training".format(i,5))
                self.collect_selfplay_data(5)
                if len(self.data_buffer) > self.batch_size:
                    loss, entropy = self.policy_update()
                    print("Final Loss : {} , Final Entropy: {}".format(loss,entropy))

                win_ratio = self.policy_evaluate(7)
                print("Win-Ratio: ",win_ratio)
                #self.policy_value_net.save_model('./current_policy.model')
                if win_ratio > self.best_win_ratio:
                    print("New best policy!!!!!!!!")
                    self.best_win_ratio = win_ratio
            self.policy_value_net.save_model('./best_policy.model')
        except KeyboardInterrupt:
            print('\n\rquit')

if __name__ == '__main__':
    pipe = TrainPipeline()
    pipe.run()
