# utils.py

import math

def square(x):
    return x * x

class vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return vector(self.x - other.x, self.y - other.y)

    def move(self, other):  # move 메서드 추가
        self.x += other.x
        self.y += other.y

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5  # 벡터 크기 계산



def floor(value, size):
    return value // size * size