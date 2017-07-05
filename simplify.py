import struct
import functions

# Automatic Simplifiy (u)
# To begin, since integers and symbols are in simplified form, the pro-
# cedure simply returns the input expression simplified [page 91]
def automatic_simplify(node):
    ret = 0
    
    if node.type == NODE.INT or node.type == NODE.SYM:
        ret = node
    elif node.type == NODE.OP:
        children = []
        for i in range(len(node.children)):
            children.append(automatic_simplify(node.children[i]))
        if node.value == OP.DIV:
            if(children[0].type == NODE.INT and children[1].type == NODE.INT):
                ret = simplify_rational_number(construct(OP.DIV, [children[0], children[1]]))
            else:
                ret = simplify_quotient(construct(OP.DIV, [children[0], children[1]]))
        elif node.value == OP.MUL:
            ret = simplify_product(construct(OP.MUL, children))
        elif node.value == OP.ADD:
            ret = simplify_sum(construct(OP.ADD, children))
        elif node.value == OP.SUB:
            ret = simplify_sum(construct(OP.ADD, [children[0], simplify_difference(children[1])]))
        elif node.value == OP.NEG:
            ret = simplify_difference(children[0])
        elif node.value == OP.POW:
            simplify_power(construct(OP.POW, [children[0], children[1]]))
    elif node.type == NODE.FUNC:
        # not implemented yet
        children = []
        for i in range(len(node.childre)):
            children[i] = automatic_simplify(node.children[i])
        ret = simplify_def(createNode(node.type, node.value, children))
    return ret

# Simplify Rational Number (u)
# Let u be an integer or a fraction with non-zero denominator. The operator
# Simplify rational number(u) transforms u to a rational number in standard form [page 37]
def simplify_rational_number(node):
    if(kind(node) == NODE.INT):
        return node
    elif(is_fraction(node)):
        n = operand(node, 0).value
        d = operand(node, 1).value
        if(not(not((n % 1))) or not(not((d % 1)))):
            return createNode(NODE.INT, n/d) # verify if one of them is a float number then divides
        if(d == 0):
            return node
        if(n % d == 0):
            return createNode(NODE.INT, (n / d) >> 0) # compare remainder and return integer quotient
        else:
            g = gcd(n, d)
            if(d > 0):
                return createNode(NODE.OP, OP.DIV, [createNode(NODE.INT, (n / g) >> 0), createNode(NODE.INT, (d / g) >> 0)])
            else:
                return createNode(NODE.OP, OP.DIV, [createNode(NODE.INT, (-n / g) >> 0), createNode(NODE.INT, (-d / g) >> 0)])

# Simplify Power (u)
# Definition 3.33. Let u = v^w where the base v = Operand(u, 1) and the
# exponent w = Operand(u, 2) are either ASAEs or the symbol Undefined.
# The operator Simplify power(u) is defined by the following transformation
# rules. [page 94]
def simplify_power(node):
	v = operand(node, 0)
	w = operand(node, 1)

	if(kind(v) == NODE.INT and v.value == 0):
		if((kind(w) == NODE.INT and w.value > 0) or (is_fraction(w) and operand(w, 0).value > 0)):
			return createInteger(0)
		else:
			return node
	elif(kind(v) == NODE.INT and v.value == 1):
		return createInteger(1)
	elif(kind(w) == NODE.INT):
		return simplify_integer_power(v, w)
	# added - verify if it is a square root of integer
	elif(kind(v) == NODE.INT and is_fraction(w)):
		return simplify_square_root_power(v, w)
	else:
		return node

# Simplify Square Root Power (v, w)
# (Should it be implemented here?)
def simplify_square_root_power(v, w):
    if(operand(w, 0).value == 1 and operand(w, 1).value == 2):
        positive = v.value > 0
        s = math.sqrt(abs(v.value))
        s2 = (s*s)%10
        lsd = ((s%10)*(s%10))%10 #javascript accuracy is not good
        if(not(s % 1) and s2 == lsd):
            if(positive):
                return createInteger(s)
            else:
                return simplify_product(construct(OP.MUL, [createInteger(s), createSymbol(SYM_IMAGINARY)]))
        elif(not positive):
            return simplify_product(construct(OP.MUL, [construct(OP.POW, [createInteger(math.abs(v.value)), w]), createSymbol(SYM.IMAGINARY)]))
    return construct(OP.POW, [v, w])

# Simplify Integer Power (v, n)
# Definition 3.34. Consider the expression v^n where v != 0 is an ASAE and
# n is an integer. The operator Simplify integer power(v, n) is defined by the
# following transformation rules. [page 95]
def simplify_integer_power(v, n):
    if(kind(v) == NODE.INT or is_fraction(v)): #not implemented yet
          return simplify_RNE(construct(OP.POW, [v, n]))
          #return construct(OP.POW, v, n)
    elif(kind(n) == NODE.INT and n.value == 0):
           return createInteger(1)
    elif(kind(n) == NODE.INT and n.value == 1):
            return v
	# the def exp was transformed into e^n
	# elif(kind(v) == FUNC.EXP) # exp def to the integer power
	# {
	# 	return simplify_def(createNode(NODE.FUNC, FUNC.EXP, simplify_product(construct(OP.MUL, n, operand(v, 0)))))
	# }
    elif(kind(v) == OP.POW):
        r = operand(v, 0)
        s = operand(v, 1)

        p = simplify_product(construct(OP.MUL, [s, n]))

        if(kind(p) == NODE.INT):
                return simplify_integer_power(r, p)
        else:
                return construct(OP.POW, r, p)
    elif(kind(v) == OP.MUL and kind(n) == NODE.INT and not(n.value % 1)): # only exact integers
        ret = []
        r = v.children[:]
        for i in range(len(r)):
                r[i] = simplify_integer_power(r[i], n)
                ret[i] = simplify_product(r[i])
        return construct(OP.MUL, ret)
    # added - transforming i^2 to -1
    # (Should it be implemented here?)
    elif(is_symbol(v, SYM_IMAGINARY) and kind(n) == NODE.INT):
        if(n.value == 2):
            return createInteger(-1)
        else:
            if(n.value % 2):
                return construct(OP.MUL, [createInteger(math.pow(-1, (n.value-1)/2)), createSymbol(SYM_IMAGINARY)])
            else:
                return createInteger(math.pow(-1, n.value/2))
    else:
        return construct(OP.POW, [v, n])

# Simplify Sum (u)
# The operator Simplify sum(u)
# In development
def simplify_sum(node):
	if(kind(node) == OP.ADD):
		if(len(node.children) == 1):
			return node.children[0]
		else:
			v = simplify_sum_rec(node.children)
			if(len(v) == 1):
				return v[0]
			elif(len(v) >= 2):
				if(v[0].type == NODE.INT and v[0].value == 0):
					return construct(OP.ADD, v[1:])
				else:
					return construct(OP.ADD, v)
			elif(len(v) == 0):
				return createInteger(0)
	else:
		return node

# Simplify Sum Recursive (u)
# def responsible to bring children up if the node is a sum
# Also calls the def group_all_sum_terms that groups terms in the sum
def simplify_sum_rec(children):
    ret = 0
    new_children = []
    for i in range(len(children)):
        simplified =  simplify_sum_rec(children[i].children) if kind(children[i]) == OP.ADD else children[i]
        if(isinstance(simplified, list)):
            new_children.extend(simplified)
        else:
            new_children.append(simplified)
    ret = group_all_sum_terms(new_children)
    ret.sort(compare)
    #ret.reverse()
    return ret

# Group Sum Terms (l, r)
# If possible, group the terms transforming them into multiples, adding integers and so on
def group_sum_terms(left, right):
	if(kind(left) == NODE.INT and left.value == 0):
		return right
	elif(kind(right) == NODE.INT and right.value == 0):
		return left
	elif((kind(left) == NODE.INT and kind(right) == NODE.INT) or (is_fraction(left) and is_fraction(right)) or (kind(left) == NODE.INT and is_fraction(right)) or (is_fraction(left) and kind(right) == NODE.INT)):
		return simplify_rational_number(evaluate_sum(left, right))
	else:
		l = term(left)
		r = term(right)
		if(l is not None and r is not None and compare(term(left), term(right)) == 0):
			return simplify_product(construct(OP.MUL, simplify_sum(construct(OP.ADD, constant(left), constant(right))), term(left)))

# Group All Sum Terms (u)
# Responsible for grouping all the children of a sum
def group_all_sum_terms(arg):
    children = arg[:] # copy array
    i = 0
    while(i < len(children) - 1):
        new_children = [children[i]]
        for j in range(i+1, len(children)):
            n = group_sum_terms(new_children[0], children[j])
            if(n is None):
                new_children.append(children[j])
            else:
                new_children[0] = n
        left = children[0:i]
        right = new_children[:]
        total = left.expand(right)
        children = total[:]
        i = i + 1
    return children

# Simplify Product (u)
# The operator Simplify product(u)
# Let u be a product with one or more operands that
# are ASAEs, and let L = [u 1 , . . . , u n ] be the list of the operands of u.
# The Simplify product (u) operator is defined by the following transforma-
# tion rules. [page 98]
def simplify_product(node):
	if(kind(node) == OP.MUL):
		for i in range(len(node.children)):
			if(kind(node.children[i]) == NODE.INT and node.children[i].value == 0):
					return createInteger(0)
		if(len(node.children) == 1):
			return node.children[0]
		else:
			v = simplify_product_rec(node.children)
			if(len(v) == 1):
				return v[0]
			elif(len(v) >= 2):
				if(v[0].type == NODE.INT and v[0].value == 1):
					return construct(OP.MUL, v[1:])
				else:
					return construct(OP.MUL, v)
			elif(len(v) == 0):
				return createInteger(1)
	else:
		return node

# Simplify Product Recursive (u)
# def responsible to bring children up if the node is a product
# Also calls the def group_all_product_terms that groups terms in the product
def simplify_product_rec(children):
    ret = 0
    new_children = []
    for i in range(len(children)):
        simplified = simplify_product_rec(children[i].children) if kind(children[i]) == OP.MUL else children[i]
        if isinstance(simplified, list):
            new_children.expand(simplified)
        else:
            new_children.append(simplified)
    ret = group_all_product_terms(new_children)
    ret.sort(compare)
    return ret

# Group Product Terms (l, r)
# If possible, group the terms transforming them into a power, multiplying integers and so on
def group_product_terms(left, right):
	# if(kind(left) == NODE.INT and kind(right) == NODE.INT)
	# {
	# 	return createNode(NODE.INT, left.value * right.value)
	# }
	#elif(kind(left) == NODE.INT and left.value == 1)
	if(kind(left) == NODE.INT and left.value == 1):
		return right
	elif(kind(right) == NODE.INT and right.value == 1):
		return left
	#elif((is_fraction(left) and is_fraction(right)) or (kind(left) == NODE.INT and is_fraction(right)) or  (is_fraction(left) and kind(right) == NODE.INT))
	elif((kind(left) == NODE.INT and kind(right) == NODE.INT) or (is_fraction(left) and is_fraction(right)) or (kind(left) == NODE.INT and is_fraction(right)) or  (is_fraction(left) and kind(right) == NODE.INT)):
		# left_num = is_fraction(left) ? left.children[0].value : left.value
		# left_den = is_fraction(left) ? left.children[1].value : 1
		# right_num = is_fraction(right) ? right.children[0].value : right.value
		# right_den = is_fraction(right) ? right.children[1].value : 1
		# num = left_num * right_num
		# den = left_den * right_den
		return simplify_rational_number(evaluate_product(left, right))
		#return simplify_rational_number(construct(OP.DIV, createNode(NODE.INT, num), createNode(NODE.INT, den)))
	# the def exp was transformed into e^n
	# elif(kind(left) == FUNC.EXP and kind(right) == FUNC.EXP) # groupind exp defs
	# {
	# 	return simplify_def(createNode(NODE.FUNC, FUNC.EXP, simplify_sum(construct(OP.ADD, operand(left, 0), operand(right, 0)))))
	# }
	elif(compare(base(left), base(right)) == 0):
		return simplify_power(construct(OP.POW, base(left), simplify_sum(construct(OP.ADD, exponent(left), exponent(right)))))

# Group All Product Terms (u)
# Responsible for grouping all the children of a product
def group_all_product_terms(arg):
    children = arg[:] # copy array
    i = 0
    while(i < len(children) - 1):
        new_children = [children[i]]
        for j in range(i+1, len(children)):
            n = group_product_terms(new_children[0], children[j])
            if(n is None):
                new_children.append(children[j])
            else:
                new_children[0] = n
        left = children[:i]
        right = new_children[:]
        left.extend(right)
        children = left[:]
        i = i + 1
    return children

# Simplify Difference (u)
# The operator Simplify difference(u) is based on the basic difference
# transformations −u = (−1) · u and u − v = u + (−1) · v. [page 106]
def simplify_difference(node):
	if(node.type == NODE.INT):
		return createInteger(-node.value)
	else:
		return simplify_product(construct(OP.MUL, [createInteger(-1), node]))

# Simplify Quotient (u)
# The operator Simplify quotient, which simplifies quotients, is based on the
# basic quotient transformation u/v = u · v −1 [page 106]
def simplify_quotient(node):
	return simplify_product(construct(OP.MUL, [node.children[0], simplify_power(construct(OP.POW, [node.children[1], createInteger(-1)]))]))

# Simplify RNE (u)
# [page 40]
def simplify_RNE(node):
	v = simplify_RNE_rec(node)
	if(v is not None):
		return simplify_rational_number(v)

# Simplify RNE rec(u)
# [page 41]
def simplify_RNE_rec(node):
    if(kind(node) == NODE.INT):
        return node
    elif(is_fraction(node)):
        #if Denominator fun(u) = 0 then Return(Undefined)
        return node
    elif(number_of_operands(node) == 1):
        v = simplify_RNE_rec(operand(node, 0))
        return v
    elif(number_of_operands(node) == 2):
        if(kind(node) == OP.POW):
            v = simplify_RNE_rec(operand(node, 0))
            return evaluate_power(v, operand(node, 1))
        else:
            v = simplify_RNE_rec(operand(node, 0))
            w = simplify_RNE_rec(operand(node, 1))
            if(kind(node) == OP.ADD):
                return evaluate_sum(v, w)
            elif(kind(node) == OP.MUL):
                return evaluate_product(v, w)
            elif(kind(node) == OP.DIV):
                return evaluate_quotient(v, w)

# Simplify def (u)
#def simplify_def(node):
#	if(kind(node) == FUNC.SQRT):
#		return simplify_power(construct(OP.POW, operand(node, 0), construct(OP.DIV, createNode(NODE.INT, 1), createNode(NODE.INT, 2))))
#	elif(kind(node) == FUNC.SIN and kind(operand(node, 0)) == NODE.INT and operand(node, 0).value == 0):
#		return createInteger(0)
#	elif(kind(node) == FUNC.TAN and kind(operand(node, 0)) == NODE.INT and operand(node, 0).value == 0):
#		return createInteger(0)
#	elif(kind(node) == FUNC.COS and kind(operand(node, 0)) == NODE.INT and operand(node, 0).value == 0):
#		return createInteger(1)
#	elif(kind(node) == FUNC.SEC and kind(operand(node, 0)) == NODE.INT and operand(node, 0).value == 0):
#		return createInteger(1)
#	# the def exp was transformed into e^n
#	# elif(kind(node) == FUNC.EXP and kind(operand(node, 0)) == NODE.INT and operand(node, 0).value == 0)
#	# {
#	# 	return createNode(NODE.INT, 1)
#	# }
#	elif(kind(node) == FUNC.NLOG and kind(operand(node, 0)) == NODE.INT and operand(node, 0).value == 1):
#		return createInteger(0)
#	elif(kind(node) == FUNC.BLOG and kind(operand(node, 1)) == NODE.INT and operand(node, 1).value == 1):
#		return createInteger(0)
#	elif(kind(node) == FUNC.NLOG and kind(operand(node, 0)) == NODE.SYM and operand(node, 0).value == SYM.EULER):
#		return createInteger(1)
#	elif(kind(node) == FUNC.BLOG and kind(operand(node, 1)) == NODE.INT and operand(node, 1).value == operand(node, 0).value):
#		return createInteger(1)
#	elif(kind(node) == FUNC.NLOG and kind(operand(node, 0)) == OP.POW and kind(operand(operand(node, 0), 0)) == NODE.SYM and operand(operand(node, 0), 0).value == SYM.EULER):
#		return operand(operand(node, 0), 1)
#	elif(kind(node) == FUNC.BLOG and kind(operand(node, 1)) == OP.POW and kind(operand(operand(node, 1), 0)) == NODE.INT and operand(operand(node, 1), 0).value == operand(node, 0).value):
#		return operand(operand(node, 1), 1)
#	else:
#		return node