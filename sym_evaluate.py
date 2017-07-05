from sym_struct import *
from sym_functions import *

# Evaluate quotient (v,w)
# an integer or a fraction in def notation
def evaluate_quotient(v, w):
		return construct(OP_DIV, [createInteger(numerator_fun(v) * denominator_fun(w)), createInteger(numerator_fun(w) * denominator_fun(v))])

# Evaluate product (v,w)
# an integer or a fraction in def notation
def evaluate_product(v, w):
		if(is_fraction(v) or is_fraction(w)):
			return construct(OP_DIV, [createInteger(numerator_fun(v) * numerator_fun(w)), createInteger(denominator_fun(v) * denominator_fun(w))])
		else:
			return createInteger(numerator_fun(v) * numerator_fun(w))

# Evaluate sum (v,w)
# an integer or a fraction in def notation
def evaluate_sum(v, w):
		if(is_fraction(v) or is_fraction(w)):
			return construct(OP_DIV, [createInteger(numerator_fun(v) * denominator_fun(w) + numerator_fun(w) * denominator_fun(v)), createInteger(denominator_fun(v) * denominator_fun(w))])
		else:
			return createInteger(numerator_fun(v) + numerator_fun(w))

# Evaluate power (v, n)
# v : an integer or a fraction in def notation
# n : an integer
def evaluate_power(v, n):
	if(numerator_fun(v) == 0):
		if(n.value > 0):
			return createInteger(0)
		else:
			return createNode(OP_POW, [v, n])
	else:
		if(n.value > 0):
			s = evaluate_power(v, createInteger(n.value-1))
			return evaluate_product(s, v)
		elif(n.value == 0):
			return createInteger(1)
		elif(n.value == -1):
			# check again in the book [page 42]
			return construct(OP_DIV, [createInteger(denominator_fun(v)), createInteger(numerator_fun(v))])
		elif(n.value < -1):
			s = construct(OP_DIV, [createInteger(denominator_fun(v)), createInteger(numerator_fun(v))])
			return evaluate_power(s, createInteger(-n.value))
