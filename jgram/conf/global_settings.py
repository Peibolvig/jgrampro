import sys 
import os 

def use_globalconf():
    # jgram parent dir
    curdir = os.path.dirname(os.path.abspath(__file__)) 
    PROJECT_DIR = os.path.dirname(curdir) 

    sys.path.insert(0, PROJECT_DIR) 

    return PROJECT_DIR
