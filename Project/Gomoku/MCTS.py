import math
import random
import copy
from Controller import get_keys,is_terminal,winner

class State(object):
    def __init__(self):
        self.current_round_index = 0
        self.cumulative_choices = []
        self.max_depth = 20

    def set_player(self,player):
        self.player = player

    def get_pieces(self):
        return self.pieces

    def set_pieces(self,pieces):
        self.pieces = pieces

    def get_board_avaiable(self):
        return self.board_avaiable

    def set_board_avaiable(self,board_avaiable):
        self.board_avaiable = board_avaiable

    def get_current_round_index(self):
        return self.current_round_index

    def set_current_round_index(self, turn):
        self.current_round_index = turn

    def get_cumulative_choices(self):
        return self.cumulative_choices

    def set_cumulative_choices(self, choices):
        self.cumulative_choices = choices

    def compute_reward(self):
        who_wins = winner(self.pieces)
        return who_wins


    def get_next_state_with_random_choice(self):
        random_choice = random.choice([choice for choice in self.board_avaiable])

        next_state = State()
        next_state.set_player(self.player[::-1])
        next_piece = copy.deepcopy(self.pieces)
        next_piece[random_choice] = next_state.player[0]

        next_state.set_pieces(next_piece)
        next_state.set_board_avaiable([i for i in self.board_avaiable if i != random_choice])
        next_state.set_current_round_index(self.current_round_index + 1)
        next_state.set_cumulative_choices(self.cumulative_choices +
                                          [random_choice])
        return next_state

class Node(object):

    def __init__(self):
        self.parent = None
        self.children = []

        self.visit_times = 0
        self.quality_value = 0.0

        self.state = None

    def set_avaiable_choice_number(self,board_avaiable_number):
        self.board_avaiable_number = board_avaiable_number

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def get_children(self):
        return self.children

    def get_visit_times(self):
        return self.visit_times

    def set_visit_times(self, times):
        self.visit_times = times

    def visit_times_add_one(self):
        self.visit_times += 1

    def get_quality_value(self):
        return self.quality_value

    def set_quality_value(self, value):
        self.quality_value = value

    def quality_value_add_n(self, n):
        self.quality_value += n

    def is_all_expand(self):
        return len(self.children) == self.board_avaiable_number

    def add_child(self, sub_node):
        sub_node.set_parent(self)
        self.children.append(sub_node)


def tree_policy(node):

  # Check if the current node is the leaf node
    while (is_terminal(node.get_state().get_pieces()) == False):
        if node.is_all_expand():
            node = best_child(node, True)
        else:
      # Return the new sub node
            sub_node = expand(node)
            return sub_node

  # Return the leaf node
    return node


def default_policy(node):

  # Get the state of the game
    current_state = node.get_state()

  # Run until the game over
    while (is_terminal(current_state.get_pieces()) == False):
    # Pick one random action to play and get next state
        current_state = current_state.get_next_state_with_random_choice()

    final_state_reward = current_state.compute_reward()
    return final_state_reward

def expand(node):
    tried_sub_node_states = [
      sub_node.get_state() for sub_node in node.get_children()
  ]

    new_state = node.get_state().get_next_state_with_random_choice()


  # Check until get the new state which has the different action from others
    while new_state in tried_sub_node_states:
        new_state = node.get_state().get_next_state_with_random_choice()

    sub_node = Node()
    sub_node.set_state(new_state)
    sub_node.set_avaiable_choice_number(node.board_avaiable_number-1)
    node.add_child(sub_node)
    return sub_node

def best_child(node, is_exploration):
  # TODO: Use the min float value
    best_score = -100
    best_sub_node = None

  # Travel all sub nodes to find the best one
    for sub_node in node.get_children():

    # Ignore exploration for inference
        if is_exploration:
            C = 1 / math.sqrt(2.0)
        else:
            C = 0.0

    # UCB = quality / times + C * sqrt(2 * ln(total_times) / times)
        left = sub_node.get_quality_value() / sub_node.get_visit_times()
        right = 2.0 * math.log(node.get_visit_times()) / sub_node.get_visit_times()
        score = left + C * math.sqrt(right)
        if score > best_score:
            best_sub_node = sub_node
            best_score = score
    return best_sub_node


def backup(node, reward):


  # Update util the root node
    while node != None:
    # Update the visit times
        node.visit_times_add_one()

    # Update the quality value
        node.quality_value_add_n(reward)

    # Change the node to the parent node
        node = node.parent



def monte_carlo_tree_search(node):


    computation_budget = 1

  # Run as much as possible under the computation budget
    for i in range(computation_budget):

    # 1. Find the best node to expand
        expand_node = tree_policy(node)
    # 2. Random run to add node and get reward
        reward = default_policy(expand_node)
        #print("Reward: ",reward)
    # 3. Update all passing nodes with reward
        backup(expand_node, reward)


  # N. Get the best next node
    best_next_node = best_child(node, False)

    return best_next_node


def run_MCTS(state):
    board_avaiable = get_keys(state,-1)
    init_state = State()
    init_state.set_player([1,0])
    init_state.set_pieces(state)
    init_state.set_board_avaiable(board_avaiable)

    init_node = Node()
    init_node.set_avaiable_choice_number(len(board_avaiable))
    init_node.set_state(init_state)
    current_node = init_node

  # Set the rounds to play
    for i in range(10):
        current_node = monte_carlo_tree_search(init_node)
    selected = list(set(init_node.state.board_avaiable) - set(current_node.state.board_avaiable))[0]
    return selected
