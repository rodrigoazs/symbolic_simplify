from sym_struct import *
from sym_functions import *

def toDict(node):
    children = []
    for i in range(len(node.children)):
        children.append(toDict(node.children[i]))
    return {'type': node.type, 'value': node.value, 'children': children}

def toTree(node):   
    if node.type == NODE.INT or node.type == NODE.SYM:
        return str(node.value)
    elif node.type == NODE.OP:
        children = []
        for i in range(len(node.children)):
            children.append(toTree(node.children[i]))
        if node.value == OP.DIV:
            return "/("+ ",".join(children) + ")"
        elif node.value == OP.MUL:
            return "*("+ ",".join(children) + ")"
        elif node.value == OP.ADD:
            return "+("+ ",".join(children) + ")"
        elif node.value == OP.POW:
            return "^("+ ",".join(children) + ")"