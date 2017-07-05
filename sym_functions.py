from sym_struct import *

# Numerator Fun (v)
# return an integer
def numerator_fun(v):
	if(kind(v) == NODE.INT):
		return v.value
	elif(is_fraction(v)):
		return operand(v, 0).value

# Denominator Fun (v)
# return an integer
def denominator_fun(v):
	if(kind(v) == NODE.INT):
		return 1
	elif(is_fraction(v)):
		return operand(v, 1).value
    
# Kind (u)
# This operator returns the type of expression (e.g., symbol,
# integer, fraction, +, ∗, ^, and def names). For example, Kind (m ∗ x + b) → +. [page 8]
def kind(node):
	if(node.type == NODE.INT or node.type == NODE.SYM):
		return node.type;
	else:
		return node.value;
    
# Number_of_operands(u)
# This operator returns the number of operands
# of the main operator of u. For example,
# Number of operands(a ∗ x + b ∗ x + c) → 3 [page 8]
def number_of_operands(node):
	return len(node.children);

# Operand (u, i)
# This operator returns the ith operand of the main
# operator of u. For example, Operand (m ∗ x + b, 2) → b [page 9]
def operand(node, pos):
	return node.children[pos];

# Operands (u)
# This operator returns all the operands of the main
def operands(node):
	if(node.type == NODE.INT or node.type == NODE.SYM):
		return node
	else:
		return node.children

# Base (u)
# This operator returns the base of an ASAE
def base(node):
	if(kind(node) == OP.POW):
		return operand(node, 0)
	else:
		return node

# Term (u)
# [page 83]
def term(node):
	if(kind(node) == NODE.SYM or kind(node) == OP.ADD or kind(node) == OP.POW or node.type == NODE.FUNC):
		return construct(OP.MUL, node)
	elif(kind(node) == OP.MUL):
		if(kind(operand(node, 0)) == NODE.INT or is_fraction(kind(operand(node, 0)))):
			return construct(OP.MUL, node.children[1:])
		else:
			return node

# Constant (u)
# [page 83]
def constant(node):
	if(kind(node) == NODE.SYM or kind(node) == OP.ADD or kind(node) == OP.POW or node.type == NODE.FUNC):
		return createInteger(1)
	elif(kind(node) == OP.MUL):
		if(kind(operand(node, 0)) == NODE.INT or is_fraction(kind(operand(node, 0)))):
			return operand(node, 0)
		else:
			return createInteger(1)

# Exponent (u)
# This operator returns the exponent of an ASAE
def exponent(node):
	if(kind(node) == OP.POW):
		return operand(node, 1)
	else:
		return createInteger(1)

# Construct(f, L)
# Let f be an operator (+, ∗, =, etc.) or a symbol,
# and let L = [a, b, . . . , c] be a list of expressions. This operator returns
# an expression with main operator f and operands a, b, . . . , c. For
# example, Construct (” + ”, [a, b, c]) → a + b + c. [page 9]
def construct(operator, expressions):
    if(isinstance(expressions, list)):
        return Node(NODE.OP, operator, expressions)
    else:
        return Node(NODE.OP, operator, [expressions])

# Short def to construct sub as ASAE
def construct_neg(a):
	return construct(OP.MUL, [createInteger(-1), a])


# Short def to construct sub as ASAE
def construct_sub(a, b):
	return construct(OP.ADD, [a, construct(OP.MUL, [createInteger(-1), b])])

# Short def to construct div as ASAE
def construct_div(a, b):
	return construct(OP.MUL, [a, construct(OP.POW, [b, createInteger(-1)])])

# Short def to create Node Int
def createInteger(u):
	return createNode(NODE.INT, u, [])

# Short def to create Node Sym
def createSymbol(u):
	return createNode(NODE.SYM, u, [])

# Returns the GCD of the given integers. Each input will be transformer into non-negative.
def gcd(a, b):
    a = abs(a)
    b = abs(b)
    if (not a):
        return b
    if (not b):
        return a

    while (1):
        a %= b
        if (not a):
            return b
        b %= a
        if (notb):
            return a

# Returns the signal of a term. The node needs to be simplified.
# False: < 0
# True: >= 0
def signal(term):
    if(kind(term) == NODE.INT):
        return term.value >= 0
    elif(is_fraction(term)):
        return term.children[0].value >= 0
    elif(kind(term) == OP.MUL):
        if(kind(term.children[0]) == NODE.INT):
            return term.children[0].value >= 0
        else:
            return True
    else:
        return True

# Is Fraction (u)
# Return if the node is a fraction or not
def is_fraction(u):
	return u.type == NODE.OP and u.value == OP.DIV and u.children[0].type == NODE.INT and u.children[1].type == NODE.INT

# Is Symbol (u ,s)
# Return True if the node u is a symbol s
def is_symbol(node, symbol):
	if(kind(node) == NODE.SYM and node.value == symbol):
		return True
	else:
		return False;

# Free of Symbol (u, s)
# Return True if the node u does not contain a certain symbol s, otherwise returns False
def free_of_symbol(node, symbol):
    if(kind(node) == NODE.SYM and node.value == symbol):
        return False
    elif(kind(node) == NODE.SYM and node.value != symbol):
        return True
    else:
        ret = True
        for i in range(len(node.children)):
            ret = ret and free_of_symbol(node.children[i], symbol);
            if(not ret):
                return ret
        return ret