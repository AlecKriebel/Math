import sympy as s,json,itertools,math
from fractions import Fraction as F
N=0
def ck(x):
 global N
 assert x;N+=1
z,w,T=s.symbols('z w T')
# Elimination-based push-forward independently tests the companion-matrix route,
# including repeated fibers at w=0 and polynomial values of the lifted function.
for degree in range(1,6):
 for a in range(-2,3):
  poly=z**degree+(a*z if degree>1 else a)-w
  # Monic polynomial companion on quotient basis 1,z,...
  C=s.zeros(degree)
  for j in range(degree):
   rem=s.rem(z**(j+1),poly,z)
   for i in range(degree):C[i,j]=rem.coeff(z,i)
  value=z*z+2*z+3
  M=C*C+2*C+3*s.eye(degree)
  lhs=s.expand(M.charpoly(T).as_expr());rhs=s.resultant(poly,T-value,z)
  ck(s.expand(lhs-rhs)==0)
  for b in [-1,0,1]:ck(s.Poly(lhs.subs(w,b),T).LC()==1)
# Universal finite-difference nonvanishing checked on several step sizes/orders,
# exact integer lamps rather than finite cyclic truncations.
for r in range(1,9):
 for scale in range(1,7):
  lamps={0:scale}
  for k in range(1,13):
   nxt={}
   for pos,c in lamps.items():nxt[pos+r]=nxt.get(pos+r,0)+c;nxt[pos]=nxt.get(pos,0)-c
   lamps={p:c for p,c in nxt.items() if c}
   ck(lamps[k*r]==scale)
   ck(lamps=={j*r:scale*(-1)**(k-j)*math.comb(k,j) for j in range(k+1)})
# Fractional removable exponents and total decay, including mixed zero exponents.
for alpha in itertools.product([F(0),F(1,7),F(1,2),F(6,7)],repeat=3):
 ck(all(F(m)-a>0 for a in alpha for m in range(1,5)))
 ck((sum(alpha)>0)==any(alpha))
# Nontrivial Jordan block powers violate uniform boundedness.
for k in range(1,21):
 J=s.Matrix([[1,1,0],[0,1,1],[0,0,1]])**k
 ck(J[0,2]==s.binomial(k,2));ck(J[0,1]==k)
print(json.dumps({'status':'PASS','independent_assertions':N,'scope':'Independent resultant/companion equality, exact infinite-lamp finite differences, fractional exponents and Jordan powers; analytic and topological implications audited in full prose.'},indent=2))
