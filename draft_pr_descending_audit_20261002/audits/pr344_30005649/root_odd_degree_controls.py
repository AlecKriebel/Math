"""Independent degree-three scalar-twist and change-of-basis controls.

Finite controls supplement, and do not replace, the all-perfect-field proof.
F_343 = F_7[t]/(t^3+2); irreducibility follows from the no-root cubic check.
"""
import itertools, json

Z = (0, 0, 0)
O = (1, 0, 0)
T = (0, 1, 0)
def add(x, y): return tuple((a+b) % 7 for a, b in zip(x, y))
def neg(x): return tuple(-a % 7 for a in x)
def mul(x, y):
    c = [0]*5
    for i, a in enumerate(x):
        for j, b in enumerate(y): c[i+j] += a*b
    for d in [4, 3]: c[d-3] -= 2*c[d]
    return tuple(a % 7 for a in c[:3])
def power(x, n):
    y = O
    while n:
        if n & 1: y = mul(y, x)
        x = mul(x, x); n >>= 1
    return y
sig = lambda x: power(x, 7)
si = lambda x: power(x, 49)
def sumf(xs):
    y = Z
    for x in xs: y = add(y, x)
    return y
def matrix(entries):
    a = [[Z]*6 for _ in range(6)]
    for i, j in entries: a[i][j] = O
    return a
F = matrix([(1,0), (2,1), (4,3)])
V = matrix([(5,0), (2,3), (4,5)])
def transpose(a): return [list(x) for x in zip(*a)]
def twist(a, s): return [[s(x) for x in row] for row in a]
def act(a, x, s): return [sumf(mul(c, s(z)) for c, z in zip(row, x)) for row in a]
def dot(x, y): return sumf(mul(a,b) for a,b in zip(x,y))
def mm(a, b):
    return [[sumf(mul(x,y) for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def rank(a):
    a = [list(r) for r in a]; i = 0
    for j in range(len(a[0])):
        q = next((q for q in range(i,len(a)) if a[q][j] != Z), None)
        if q is None: continue
        a[i], a[q] = a[q], a[i]
        v = power(a[i][j], 341); a[i] = [mul(v,x) for x in a[i]]
        for q in range(len(a)):
            if q != i:
                v = a[q][j]; a[q] = [add(x,neg(mul(v,y))) for x,y in zip(a[q],a[i])]
        i += 1
        if i == len(a): break
    return i
def delta(a, b):
    aa = mm(a,twist(a,sig)); bb = mm(b,twist(b,si))
    return rank(aa)+rank(bb)-rank([x+y for x,y in zip(aa,bb)])
assert all((x*x*x+2) % 7 != 0 for x in range(7))
for x in itertools.product(range(7), repeat=3):
    assert sig(si(x)) == si(sig(x)) == x
    assert sig(sig(sig(x))) == x
assert sig(T) == (0,4,0) and si(T) == (0,2,0) and sig(T) != si(T)
fd, vd = twist(transpose(V), sig), twist(transpose(F), si)
assert delta(F,V) == 0 and delta(fd,vd) == 1
# A non-prime diagonal basis change forces non-prime operator coefficients.
ds = [power(T,i) for i in range(6)]
P = [[ds[i] if i==j else Z for j in range(6)] for i in range(6)]
Pi = [[power(ds[i],341) if i==j else Z for j in range(6)] for i in range(6)]
FF, VV = mm(mm(P,F),twist(Pi,sig)), mm(mm(P,V),twist(Pi,si))
FFD, VVD = twist(transpose(VV),sig), twist(transpose(FF),si)
assert delta(FF,VV) == 0 and delta(FFD,VVD) == 1
assert FFD != transpose(VV) and VVD != transpose(FF)
state = 246813579
def vector():
    global state
    v = []
    for _ in range(6):
        c=[]
        for _ in range(3):
            state=(1103515245*state+12345) % (2**31); c.append(state % 7)
        v.append(tuple(c))
    return v
bad_plain = bad_inverse = False
for _ in range(64):
    x, phi = vector(), vector()
    assert dot(act(fd,phi,sig),x) == sig(dot(phi,act(V,x,si)))
    assert dot(act(vd,phi,si),x) == si(dot(phi,act(F,x,sig)))
    assert act(F,act(V,x,si),sig) == act(V,act(F,x,sig),si) == [Z]*6
    assert dot(act(FFD,phi,sig),x) == sig(dot(phi,act(VV,x,si)))
    assert dot(act(VVD,phi,si),x) == si(dot(phi,act(FF,x,sig)))
    bad_plain |= dot(act(transpose(V),phi,lambda z:z),x) != sig(dot(phi,act(V,x,si)))
    bad_inverse |= dot(act(transpose(V),phi,si),x) != sig(dot(phi,act(V,x,si)))
assert bad_plain and bad_inverse
print(json.dumps({'status':'PASS', 'field_order':343, 'extension_degree':3,
                  'field_elements_checked':343, 'vector_pairs':64,
                  'frobenius_differs_from_inverse':True,
                  'original_delta':0, 'dual_delta':1,
                  'nonprime_basis_change_verified':True,
                  'wrong_scalar_twist_mutants_rejected':2,
                  'scope':'Finite scalar-twist controls; no universal theorem inferred from sampling.'}, indent=2))
