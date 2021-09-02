import time
import importlib
from values import CONSTANT
import pickle

if __name__ == "__main__":
    while True:
        importlib.reload(CONSTANT)
        print(CONSTANT.a)
        time.sleep(1)
