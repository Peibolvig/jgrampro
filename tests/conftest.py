import sys 
import os 

# Make project root folder visible to the tests
curdir = os.path.dirname(os.path.abspath(__file__)) 
parentdir = os.path.dirname(curdir) 
sys.path.insert(0, parentdir) 

