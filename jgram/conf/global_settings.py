import sys
import os

curdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(curdir)
print(parentdir)
sys.path.insert(0, parentdir)
