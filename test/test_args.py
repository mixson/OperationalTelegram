

def logUserRecord(func):
    def inner_function(*args, **kwargs):
        func(*args, **kwargs)
        bot = args[0]
        update = args[1]
        print(bot, update)

    return inner_function

@logUserRecord
def afun(a,b):
    print(a+b)


afun(1,2)