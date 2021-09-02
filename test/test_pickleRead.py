
import pickle
import os
import time

if __name__ == "__main__":
    fileName = "abc.pkl"
    while True:
        print(os.path.getsize(fileName))
        with open(fileName, "rb") as file:
            a = pickle.load(file)
        print(a)
        time.sleep(2)
