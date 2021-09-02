
import pickle

if __name__ == "__main__":
    fileName = "abc.pkl"
    b = [1,2,3,4]
    with open(fileName, "wb") as file:
        pickle.dump(b, file)

