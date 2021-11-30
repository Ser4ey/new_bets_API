# нет self
def decorator1(f):
    def wrapper(text):
        return f(text+'$$$$')

    return wrapper

# есть self
def decorator2(f):
    def wrapper(self, text):
        return f(self, text+'LLLL')

    return wrapper


class A:
    # работает только с self
    @decorator2
    def say_text(self, text):
        print(text)

    # работает без self
    def activate(self):
        self.say_text = decorator1(self.say_text)

A1 = A()
A1.say_text('123abs')

# работает только без self
A1.say_text = decorator1(A1.say_text)
A1.say_text('123abs')

# Почему в даном случае декоратору не нужно передовать self?
#    @decorator2
#    def say_text(self, text)   ==    A1.say_text = decorator1(A1.say_text)
