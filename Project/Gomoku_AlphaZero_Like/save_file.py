import pickle
import os


def store_object(file,name):
    with open(str(name), 'wb') as saving:
        pickle.dump(file,saving)


def load_object(name):
    exists = os.path.isfile(str(name))
    if exists:
        with open(str(name),'rb') as saving:
            obj = pickle.load(saving)
        return obj
    else:
        return []

def load_states_and_node(pairs):
    return [x[0] for x in pairs],[x[1] for x in pairs]
