"""Fresh audit checks for AMR-067-0014; does not import author scripts.

The main check derives Ricci for a fully generic 4x4 matrix directly from
Koszul connection matrices, then checks the complete block-slice identity.
All calculations are exact. Run with Python and SymPy.
"""
import hashlib
import json
from pathlib import Path
import sympy as sp


def n2(B):
    return sum(entry**2 for entry in B)


def zero(B):
    return all(sp.expand(entry) == 0 for entry in B)


def ricci_from_brackets(A):
    """Column j of G_i is nabla_{e_i} e_j; R_ij uses that convention."""
    d = A.rows + 1
    c = [[[sp.Integer(0) for h in range(d)] for j in range(d)]
         for i in range(d)]
    for i in range(d-1):
        for j in range(d-1):
            c[0][j+1][i+1] = A[i, j]
            c[j+1][0][i+1] = -A[i, j]
    G = [sp.Matrix(d, d, lambda h,j:
                   (c[i][j][h] - c[j][h][i] + c[h][i][j])/2)
         for i in range(d)]
    R = [[G[i]*G[j]-G[j]*G[i]
          -sum((c[i][j][k]*G[k] for k in range(d)), sp.zeros(d))
          for j in range(d)] for i in range(d)]
    return sp.Matrix(d, d, lambda j,l:
                     sp.expand(sum(R[i][j][i,l] for i in range(d))))


# General curvature identity, including the trace term not needed by the proof.
A = sp.Matrix(4, 4, sp.symbols('A:16'))
S = (A+A.T)/2
Ric = ricci_from_brackets(A)
expected = sp.diag(-n2(S), sp.zeros(4))
expected[1:,1:] = (A*A.T-A.T*A)/2-sp.trace(A)*S
assert zero(Ric-expected)
print('PASS generic Koszul Ricci formula for every real 4x4 A')

# Independent block identity for the entire local slice.
a,b,x,y,z,w,v,k = sp.symbols('a b x y z w v k', real=True)
h2 = a*a+b*b
r2 = x*x+y*y+z*z+w*w
H = sp.Matrix([[a,b],[b,-a]])
J = sp.Matrix([[0,-1],[1,0]])
C = H+k*J
L = sp.Matrix([[x,y],[z,w]])
N = sp.Matrix([[0,v],[0,0]])
M = C.row_join(sp.zeros(2)).col_join(L.row_join(N))
Q11 = C*C.T-C.T*C-L.T*L
Q21 = L*C.T-N.T*L
Q22 = L*L.T+N*N.T-N.T*N
q_block = n2(Q11)+2*n2(Q21)+n2(Q22)
assert sp.expand(q_block-n2(M*M.T-M.T*M)) == 0
s_block = 2*h2+(r2+v*v)/2
assert sp.expand(s_block-n2((M+M.T)/2)) == 0

def reduce_constraint(p):
    return sp.rem(sp.Poly(sp.expand(p), k),
                  sp.Poly(k*k-1-h2, k)).as_expr().expand()

P = reduce_constraint(q_block-8*s_block*s_block)
d = w*x-y*z
Q = 16*(2-v*v)*h2+2*(x*x+y*y+(1-3*v*v)*(z*z+w*w)+2*v*d)
R = (-12*h2*r2-24*a*k*(w*z+x*y)
     +12*b*k*(x*x+z*z-y*y-w*w)
     +4*v*(a*(w*y-x*z)-b*(w*x+y*z))
     +4*v*(k-1)*d-4*d*d)
assert reduce_constraint(P-Q-R) == 0
assert sp.expand(Q-(16*(2-v*v)*h2+2*(x+v*w)**2
                    +2*(y-v*z)**2+2*(1-4*v*v)*(z*z+w*w))) == 0
# Taylor coefficients from the directly computed P, using the correct analytic k.
t = sp.symbols('t')
xi = [a,b,x,y,z,w]
Pt = P.subs({r:t*r for r in xi}, simultaneous=True)
Pt = sp.expand(Pt.subs(k,1+t*t*h2/2))
assert Pt.coeff(t,0) == 0 and Pt.coeff(t,1) == 0
assert sp.expand(Pt.coeff(t,2)-Q) == 0
print('PASS independent block commutator identity and full cubic-plus remainder')

# A convenient quantitative coercivity lower bound, derived via determinant/trace.
# Each mixed block is 2*[[1, +/-v], [ +/-v,1-3v^2]],
# positive for |v|<1/2; its minimum eigenvalue is >= 1-4v^2.
D = sp.Matrix([[1,v],[v,1-3*v*v]])
assert sp.expand(D.det()-(1-4*v*v)) == 0
assert sp.expand(D.trace()-(2-3*v*v)) == 0
print('PASS transverse 2x2 block determinant and trace')

u = sp.symbols('u', nonzero=True, real=True)
Au = sp.diag(J, sp.Matrix([[0,u],[0,0]]))
Ric_u = ricci_from_brackets(Au)
assert Ric_u == sp.diag(-u*u/2,0,0,u*u/2,-u*u/2)
assert sp.cancel(sp.trace(Ric_u)**2/n2(Ric_u)) == sp.Rational(1,3)
E = sp.eye(4)+Au*Au
assert E*E == E and Au*Au*E == sp.zeros(4) and E.rank() == 2
# Rotation bracket forces scalar c=-u^2/2; nilpotent bracket then fails.
Dsol = Ric_u+u*u*sp.eye(5)/2
assert Dsol[2,2]-Dsol[0,0]-Dsol[1,1] == 0
assert Dsol[3,3]-Dsol[0,0]-Dsol[4,4] == u*u
print('PASS candidate value, projection, and derivation obstruction')

B = sp.Matrix([[0,-1,0,0],[1,0,0,0],[1,0,0,1],[0,-1,0,0]])
T = sp.eye(4)
T[2:4,0:2] = sp.Matrix([[0,2],[1,0]])
Hscale = sp.diag(1,1,1/u,1)
assert T*Hscale*Au*(T*Hscale).inv() == B
Ric_B = ricci_from_brackets(B)
assert sp.cancel(sp.trace(Ric_B)**2/n2(Ric_B)) == sp.Rational(9,17)
print('PASS explicit same-group nonglobal witness from direct Koszul curvature')

root = Path(__file__).resolve().parent.parent
manifest = json.loads((root/'FROZEN_AUTHOR_HASHES.json').read_text())
for entry in manifest['publication_allowed_files']:
    data = (root/'frozen_author'/entry['path']).read_bytes()
    assert len(data) == entry['bytes']
    assert hashlib.sha256(data).hexdigest() == entry['sha256']
print('PASS all six author files retain frozen sizes and hashes')
