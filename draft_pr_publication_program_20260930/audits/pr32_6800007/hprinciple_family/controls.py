#!/usr/bin/env python3
"""Exact adversarial geometric controls. Does not certify convex integration.

Run with the existing workspace .venv/bin/python. No network, input writes,
legacy imports, or calls to either frozen checker.
"""
import json
import sympy as s
from sympy.matrices.normalforms import smith_normal_form

checks = []
def check(ok, label, **evidence):
    assert ok, label
    checks.append(dict(label=label, evidence=evidence))

I = s.I
e = [s.eye(3)[:,i] for i in range(3)]
def real_columns(cols):
    return s.Matrix.vstack(s.Matrix.hstack(*cols).applyfunc(s.re),
                           s.Matrix.hstack(*cols).applyfunc(s.im))

# Two real-independent fixed columns need not be complex independent.
bad = [e[0], I*e[0]]
check(real_columns(bad).rank() == 2 and s.Matrix.hstack(*bad).rank() == 1,
      'real-independent, complex-dependent fixed columns',
      real_rank=2, complex_rank=1)
z0,z1,z2 = s.symbols('z0 z1 z2')
check(s.Matrix.hstack(*bad,s.Matrix([z0,z1,z2])).det() == 0,
      'that entire principal slice is empty')

# Exact direct-sum criterion W intersect iW = 0 for valid total-real frames.
frames = [s.eye(3), s.Matrix([[1,I,0],[0,1,I],[I,0,2]]),
          s.Matrix([[1,0,0],[I,1,0],[0,I,1]])]
for j,A in enumerate(frames):
    real = real_columns([A[:,i] for i in range(3)])
    imag = real_columns([I*A[:,i] for i in range(3)])
    check(A.det() != 0 and real.rank() == 3 and real.row_join(imag).rank() == 6,
          'complexification and real direct-sum criterion agree', frame=j,
          determinant=str(A.det()))

# Principal direction may be changed by any real source basis change.
P = s.Matrix([[1,0,1],[1,1,0],[0,1,1]])
check(P.det() == 2, 'non-coordinate principal direction change is invertible')
check((frames[1]*P).det() == frames[1].det()*P.det(),
      'total reality survives arbitrary real change of source basis')

# Complement of C e1 + C e2. Any forbidden z is midpoint of z +/- e3;
# for a general z choose a real N with z3 +/- N both nonzero.
points = [s.Matrix([2,I,0]),s.Matrix([0,0,1]),s.Matrix([I,3,2]),
          s.Matrix([0,0,I])]
for j,z in enumerate(points):
    N = next(n for n in (1,2,3) if z[2]+n != 0 and z[2]-n != 0)
    u,v = z+N*e[2], z-N*e[2]
    check(u[2] != 0 and v[2] != 0 and (u+v)/2 == z,
          'slice complement realizes an arbitrary midpoint', point=j, N=N)
# The straight segment from -1 to 1 is forbidden; the path through i is valid.
t = s.symbols('t',real=True)
check(s.solve(s.re(-1+t*(1+I)),t) == [1] and
      s.im((-1+t*(1+I)).subs(t,1)) == 1,
      'first polygonal quotient path segment avoids the origin')
check(s.solve(s.re(I+t*(1-I)),t) == [0] and
      s.im((I+t*(1-I)).subs(t,0)) == 1,
      'second polygonal quotient path segment avoids the origin')

# Actual adjoint weights at the upper-Borel flag; no nearly-Kaehler substitution.
u,v = s.symbols('u v',nonzero=True)
diag = s.diag(u,v,1/(u*v))
weights = []
for j,i in ((1,0),(2,0),(2,1)):
    E = s.zeros(3); E[j,i] = 1
    w = s.cancel(diag[j,j]/diag[i,i]); weights.append(str(w))
    check(diag*E*diag.inv() == w*E,
          'holomorphic lower-matrix isotropy weight', entry=[j+1,i+1], weight=str(w))
x,y = s.symbols('x y')
xs = [x,y,-x-y]
root_classes = [xs[j]-xs[i] for j,i in ((1,0),(2,0),(2,1))]
check(s.expand(sum(root_classes)) == -4*x-2*y,
      'integrable tangent determinant class')
check(s.expand((xs[1]-xs[0])+(xs[2]-xs[1])+(xs[0]-xs[2])) == 0,
      'wrong cyclic-root structure is detected by determinant',
      warning='These cyclic roots do not give the integrable tangent representation.')

# New genuine closed nonorientable boundary control: mapping torus of a
# concrete Klein-bottle diffeomorphism. Affine deck transformations are exact.
X,Y = s.symbols('X Y')
pt = s.Matrix([X,Y])
def a(p):return s.Matrix([p[0]+1,-p[1]])
def ai(p):return s.Matrix([p[0]-1,-p[1]])
def b(p):return s.Matrix([p[0],p[1]+1])
def bi(p):return s.Matrix([p[0],p[1]-1])
def h(p):return s.Matrix([-p[0],p[1]-s.Rational(1,2)])
check(h(a(pt)) == ai(b(h(pt))), 'h a = (a^-1 b) h on the cover')
check(h(b(pt)) == b(h(pt)), 'h b = b h on the cover')
check(h(h(pt)) == bi(pt), 'h squared is a deck transformation')
check(s.Matrix([h(pt)]).jacobian([X,Y]).det() == -1,
      'h is a smooth affine diffeomorphism')
# H1 presentation for mapping torus: a,b,t with 2b=0, 2a-b=0.
rels = s.Matrix([[0,2],[2,-1],[0,0]])
snf = smith_normal_form(rels,domain=s.ZZ)
check([abs(snf[i,i]) for i in range(2)] == [1,4],
      'mapping-torus integral H1 = Z + Z/4', smith_diagonal=[1,4,0])
check((rels.T*s.Matrix([1,2,0])).applyfunc(lambda z:z%4) == s.zeros(2,1),
      'orientation character on a lifts to Z/4')
check(rels.T.nullspace() == [s.Matrix([0,0,1])],
      'all integral characters vanish on a; w1 has no integral lift')
labels = [(a0,b0) for a0 in range(4) for b0 in range(4)
          if (-4*a0-2*b0-2)%4 == 0]
check(len(labels) == 8 and all(b0%2 == 1 for a0,b0 in labels),
      'nonzero divisible determinant index control', delta=2, B='Z/4', labels=labels)
check(not any((-4*a0-2*b0-1)%2 == 0 for a0 in range(2) for b0 in range(2)),
      'RP2 x R nonorientable obstruction control')

print(json.dumps({'pass':True,'sympy_version':s.__version__,'controls':checks,
                  'count':len(checks),
                  'scope':'Exact geometric/presentation controls only. Universal proofs, standard h-principle and dimension arguments are in AUDIT.md; these controls do not turn those theorems into computed evidence.'},indent=2))
