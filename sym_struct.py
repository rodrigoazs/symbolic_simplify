from enum import Enum

class Node:
    def __init__(self, type, value, children):
        self.type = type
        self.value = value
        self.children = children

class NODE(Enum):
    OP = 0    # Operator
    SYM = 1   # Symbol
    INT = 2   # Integer
    FUNC = 3  # Function

class OP(Enum):
    ADD = 10    # Addition
    SUB = 11    # Subtraction
    DIV = 12    # Division (used for interpreting "/" and for fractions after automatic simplification)
    MUL = 13    # Multiplication
    NEG = 14    # Negation
    POW = 15    # Power

class FUNC(Enum):
    SQRT = 20
    EXP = 21
    NLOG = 22
    BLOG = 23
    SIN = 24
    COS = 25
    TAN = 26
    SINH = 27
    COSH = 28
    TANH = 29
    ASIN = 30
    ACOS = 31
    ATAN = 32
    ASINH = 33
    ACOSH = 34
    ATANH = 35
    SEC = 36
    SECH = 37
    ASEC = 38
    ASECH = 39
    CSC = 40
    CSCH = 41
    ACSC = 42
    ACSCH = 43
    COT = 44
    COTH = 45
    ACOT = 46
    ACOTH = 47

class SYM(Enum):
    SYM_EULER = "e"
    SYM_PI = "pi"
    SYM_INFINITY = "infinity"
    SYM_IMAGINARY = "i"
    
def createNode(type, value, childs):
    return Node(type, value, childs)