"""Exact checks for the local Ricci-pinching counterexample.

Run: python verify.py
Requires SymPy. No floating-point calculations or downloaded data are used.
The normal-form coverage and uniform Taylor estimate are proved in the text.
"""
import sympy as s


def norm2(M):
    return s.trace(M * M.T)


def comm(A, B):
    return A * B - B * A


def S(A):
    return (A + A.T) / 2


u = s.symbols("u", positive=True)
a, b, x, y, z, w, v, k, t = s.symbols("a b x y z w v k t", real=True)
J = s.Matrix([[0, -1], [1, 0]])
N = s.Matrix([[0, u], [0, 0]])
A = s.diag(J, N)
assert norm2(S(A)) == u**2 / 2
assert norm2(comm(A, A.T)) == 2*u**4

# Verify Ricci directly from the Koszul connection, independently of the
# almost-abelian curvature formula cited in the proof.
n = 5
c = s.MutableDenseNDimArray.zeros(n, n, n)
for i in range(4):
    for j in range(4):
        c[0, j+1, i+1] = A[i, j]
        c[j+1, 0, i+1] = -A[i, j]
G = s.MutableDenseNDimArray.zeros(n, n, n)
for i in range(n):
    for j in range(n):
        for h in range(n):
            G[i, j, h] = (c[i,j,h] - c[j,h,i] + c[h,i,j])/2
Ric = s.zeros(n)
for j in range(n):
    for h in range(n):
        Ric[j,h] = s.simplify(sum(
            G[j,h,l]*G[i,l,i] - G[i,h,l]*G[j,l,i] - c[i,j,l]*G[l,h,i]
            for i in range(n) for l in range(n)))
assert Ric == s.diag(-u**2/2, 0, 0, u**2/2, -u**2/2)
assert s.factor(s.trace(Ric)**2/norm2(Ric)) == s.Rational(1,3)
print("PASS: direct Koszul Ricci calculation and F(A_u)=1/3")

# Full slice polynomial, using the determinant-one constraint on the
# rotation block. All expressions below are polynomial identities modulo
# k^2 = 1+a^2+b^2.
M = s.Matrix([[a,b-k,0,0], [b+k,-a,0,0], [x,y,0,v], [z,w,0,0]])
P = s.expand(norm2(comm(M,M.T)) - 8*norm2(S(M))**2)
constraint = k*k - 1 - a*a - b*b
reduce_k = lambda f: s.expand(s.rem(s.Poly(s.expand(f),k),s.Poly(constraint,k)).as_expr())
P = reduce_k(P)
Q = 16*(2-v*v)*(a*a+b*b) + 2*(x*x+y*y+(1-3*v*v)*(z*z+w*w)+2*v*(w*x-y*z))
Q_squares = 16*(2-v*v)*(a*a+b*b) + 2*(x+v*w)**2 + 2*(y-v*z)**2 + 2*(1-4*v*v)*(z*z+w*w)
assert s.expand(Q-Q_squares) == 0
r2 = x*x+y*y+z*z+w*w
rem = (-12*(a*a+b*b)*r2 - 24*a*k*(w*z+x*y)
       +12*b*k*(x*x+z*z-y*y-w*w)
       +4*v*(a*(w*y-x*z)-b*(w*x+y*z))
       +4*v*(k-1)*(w*x-y*z)-4*(w*x-y*z)**2)
assert reduce_k(P-Q-rem) == 0
assert P.subs({a:0,b:0,x:0,y:0,z:0,w:0}) == 0
xi = [a,b,x,y,z,w]
for variable in xi:
    assert s.diff(P,variable).subs({a:0,b:0,x:0,y:0,z:0,w:0,k:1}) == 0
# An independent extraction of the quadratic term after replacing k by its
# analytic square root to sufficient order.
Pt = P.subs({r:t*r for r in xi},simultaneous=True)
Pt = s.expand(Pt.subs(k, 1+t*t*(a*a+b*b)/2))
assert s.expand(Pt.coeff(t,2)-Q) == 0
print("PASS: full slice expansion, vanishing linear term, positive-square decomposition")

# All zero-eigenspace claims use the explicit spectral projection I+A^2.
E = s.eye(4)+A*A
assert E*E == E
assert A*A*E == s.zeros(4)
assert E.rank() == 2
print("PASS: polynomial projection onto the generalized zero eigenspace")

# Explicit greater-value conjugate on the same fixed Lie algebra.
A1 = A.subs(u,1)
Y = s.Matrix([[0,2],[1,0]])
T = s.eye(4)
T[2:4,0:2] = Y
B = s.Matrix([[0,-1,0,0],[1,0,0,0],[1,0,0,1],[0,-1,0,0]])
assert T*A1*T.inv() == B
H = s.diag(1,1,1/u,1)
assert H*A*H.inv() == A1
sB = norm2(S(B)); qB = norm2(comm(B,B.T))
assert sB == s.Rational(3,2)
assert qB == 8
assert s.factor(sB*sB/(sB*sB+qB/4)) == s.Rational(9,17)
print("PASS: same-orbit comparison with F(B)=9/17 > 1/3")

# Direct solvsoliton obstruction: c must be -u^2/2 from the rotation
# bracket, but then D fails the nonzero nilpotent bracket.
D = Ric + u*u*s.eye(5)/2
assert D[0,0] == 0
assert s.simplify(D[3,3] - D[0,0] - D[4,4]) == u*u
print("PASS: direct derivation obstruction")
print("All exact algebraic checks passed. The analytic coverage argument remains a textual proof obligation.")
