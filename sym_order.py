from sym_struct import *
from sym_functions import *
from sym_evaluate import *

# Compre (u ,v)
# -1 if u < v
# 0 if u == v
# 1 if u > v
# The ✁ order relation defines the actions of the basic commutative trans-
# formations, and, in a simplified sum or product, the operands are ordered
# according to this relation. Since the operands of these expressions are sim-
# plified recursively, it is sufficient to define the order relation for expressions
# that are automatically simplified. [page 84]
def compare(u, v):
	# O-1. Suppose that u and v are both constants (integers or fractions). Then,
	# u✁v → u < v
	if((kind(u) == NODE.INT or is_fraction(u)) and (kind(v) == NODE.INT or is_fraction(v))):
		u_value = u.children[0].value / u.children[1].value if is_fraction(u) else u.value
		v_value = v.children[0].value / v.children[1].value if is_fraction(v) else v.value
		if(u_value == v_value):
			return 0
		elif(u_value < v_value):
			return -1
		else:
			return 1
	# O-2. Suppose that u and v are both symbols. Then, u✁v is defined by
	# the lexicographical order of the symbols.
	elif(kind(u) == NODE.SYM and kind(v) == NODE.SYM):
		if(u.value == v.value):
			return 0
		elif(u.value < v.value):
			return -1
		else:
			return 1
	# 	O-3. Suppose that u and v are either both products or both sums with
	# operands
	elif(kind(u) == OP.ADD and kind(v) == OP.ADD or kind(u) == OP.MUL and kind(v) == OP.MUL):
		size_u = len(u.children)
		size_v = len(v.children)
		size = max(size_u, size_v)
		for i in range(size):
			if(v.children[size_v-i-1] is None):
				# op 3
				return 1
			elif(u.children[size_u-i-1] is None):
				return -1
			else:
				# op 2 and 1
				comp = compare(u.children[size_u-i-1], v.children[size_v-i-1])
				if(comp != 0):
					return comp
		return 0
	# O-4. In other words, if the bases are different, the order is determined by the
	# order of bases, and if the bases are the same, the order is determined by
	# the order of the exponents.
	elif(kind(u) == OP.POW and kind(v) == OP.POW):
		comp = compare(u.children[0], v.children[0])
		if(comp != 0):
			return comp
		else:
			return compare(u.children[1], v.children[1])
	# O-6. Suppose that u and v are defs
	elif(u.type == NODE.FUNC and v.type == NODE.FUNC):
		if(kind(u) != kind(v)):
			if(kind(u) < kind(v)):
				return -1
			else:
				return 1
		else:
			size_u = len(u.children)
			size_v = len(v.children)
			size = max(size_u, size_v)
			for i in range(size):
				if(v.children[i] is None):
					# op 3
					return 1
				elif(u.children[i] is None):
					return -1
				else:
					# op 2 and 1
					comp = compare(u.children[i], v.children[i])
					if(comp != 0):
						return comp
			return 0
	# O-7. If u is an integer or fraction and v is any other type, then u✁v.
	elif((kind(u) == NODE.INT or is_fraction(u)) and kind(v) != NODE.INT and not(is_fraction(v))):
		return -1
	# O-8. Suppose that u is a product. If v is a power, sum, factorial, def,
	# or symbol, then 9
	# u✁v → u✁ · v.
	elif(kind(u) == OP.MUL and (kind(v) == OP.POW or kind(v) == OP.ADD or kind(v) == NODE.SYM or v.type == NODE.FUNC)):
		return compare(u, construct(OP.MUL, [v]))
	# O-9. Suppose that u is a power. If v is a sum, factorial, def, or
	# symbol, then
	# u✁v → u✁v 1 .
	elif(kind(u) == OP.POW and (kind(v) == OP.ADD or kind(v) == NODE.SYM or v.type == NODE.FUNC)):
		return compare(u, construct(OP.POW, [v, createInteger(1)]))
	# O-10. Suppose that u is a sum. If v is a factorial, def, or symbol,
	# then
	# u✁v → u✁ + v.
	elif(kind(u) == OP.ADD and (kind(v) == NODE.SYM or v.type == NODE.FUNC)):
		return compare(u, construct(OP.ADD, [v]))
	# O-11. Suppose that u is a factorial. If v is a def or symbol
	# -----------------------------------------------------------------
	# Not implemented yet. No factorial def was used yet. When implement, also include
	# the factorial cases in the other rules

	# O-12. Suppose that u is a def, and v is a symbol.
	# -----------------------------------------------------------------
	# It is not possible to use non predetermined defs. Because of this, a symbol is always
	# before a def.
	elif(u.type == NODE.FUNC and kind(v) == NODE.SYM):
		return 1
	# O-13. If u and v do not satisfy the conditions in any of the above rules,
	else:
		return -compare(v, u)