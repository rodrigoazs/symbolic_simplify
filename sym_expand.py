# Algebraic Expand (u)
# u : an algebraic expression where all exponents of powers are integers
def algebraic_expand(u):
  if(kind(u) == OP.ADD):
    v = operand(u, 0)
    p = u.children[1:]
    r = p[0] if len(p) == 1 else construct(OP.ADD, [p])
    return construct(OP.ADD, [algebraic_expand(v), algebraic_expand(r)])
  elif(kind(u) == OP.MUL):
    v = operand(u, 0)
    p = u.children[1:]
    r = p[0] if len(p) == 1 else construct(OP.MUL, [p])
    return expand_product(algebraic_expand(v), algebraic_expand(r))
  elif(kind(u) == OP.POW):
    base = operand(u, 0)
    exponent = operand(u, 1)
    if(kind(exponent) == NODE.INT and exponent.value >= 2):
      return expand_power(algebraic_expand(base), exponent.value)
  for i in range(len(u.children)):
      u.children[i] = algebraic_expand(u.children[i])
  return u

# Expand Product (r, s)
# r,s : expanded algebraic expressions, where all exponents of powers are
# integers
def expand_product(r, s):
  if(kind(r) == OP.ADD):
    f = operand(r, 0)
    p = r.children[1:]
    t = p[0] if len(p) == 1 else construct(OP.ADD, [p])
    return construct(OP.ADD, [expand_product(f, s), expand_product(t, s)])
  elif(kind(s) == OP.ADD):
    return expand_product(s, r)
  else:
    return construct(OP.MUL, r, s)

# Expand Power (u)
# u : an expanded algebraic expression where all exponents of powers are
# integers
# n : a non-negative integer
def expand_power(u, n):
  if(kind(u) == OP.ADD):
    f = operand(u, 0)
    p = u.children[1:]
    r = p[0] if len(p) == 1 else construct(OP.ADD, [p])
    s = createInteger(0)
    for i in range(n+1):
      #fat=n=>(n<2)?1:fat(n-1)*n
      c = combination(n, i) #fat(n) / (fat(i) * fat(n-i))
      s = construct(OP.ADD, s, expand_product(construct(OP.MUL, [c, construct(OP.POW, [f, createInteger(n-i)])]), expand_power(r, i)))
    return s
  else:
    return construct(OP.POW, [u, createInteger(n)])