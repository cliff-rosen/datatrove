

class X():
    def hello(self):
        print("hello")


def hello2():
    print("hello2")


x = X()
x.hello = hello2
x.hello()