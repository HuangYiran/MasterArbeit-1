

def get_keys(state,value):
    l = []
    for k,v in state.items():
        if v == value:
            l.append(k)
    return l

def get_player_and_avaiable(state):
    player_state = get_keys(state,0)
    ai_state = get_keys(state,1)
    #board_avaiable = get_keys(state,-1)
    return player_state,ai_state

def who_wins(black):
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

def has_a_winner(state):
    player_state,ai_state = get_player_and_avaiable(state)
    if who_wins(player_state):
        return True,0
    elif who_wins(ai_state):
        return True,1
    elif len(ai_state)+len(player_state)==49:
        return True,-1
    else:
        return False,-1

def is_terminal(state):
    player_state, ai_state = get_player_and_avaiable(state)
    if who_wins(player_state) or who_wins(ai_state):
        return True
    elif len(ai_state)+len(player_state)>=49:
        return True
    else:
        return False

def winner(state):
    player_state, ai_state = get_player_and_avaiable(state)
    if who_wins(player_state):
        return 0
    elif who_wins(ai_state):
        return 1
    else:
        return -1

