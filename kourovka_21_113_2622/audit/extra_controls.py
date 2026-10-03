#!/usr/bin/env python3
"""Additional exact audit controls: composite Mobius order and modular quotient vector."""
import contextlib,io,json
from pathlib import Path
with contextlib.redirect_stdout(io.StringIO()):
 import independent_controls as C
from fractions import Fraction
import sympy as S
G=C.groups[0][1] # S3
# S3 characteristic 2 Brauer irreducibles: trivial and the natural degree-2 simple.
B=[]
for i in range(G.n):
 if G.orders[i]%2: B.append((i,1,2 if i==G.identity else -1))
c=[sum(Fraction(G.psi(2)[i]*row,G.n) for i,a,b in B for row in [a if k==0 else b]) for k in [0,1]]
assert c==[1,1]
# S4/V4, with the same two Brauer irreducibles inflated: all simples factor through normal V4.
S4=C.groups[1][1]
V={i for i,g in enumerate(S4.elements) if i==S4.identity or g.cycle_structure=={2:2}}
Q,pi=S4.quotient(V)
co=[]
for k in [0,1]:
 f={i:1 if k==0 else (2 if i==Q.identity else -1) for i in range(Q.n) if Q.orders[i]%2}
 co.append(sum(Fraction(S4.psi(2)[i]*f[pi[i]],S4.n) for i in range(S4.n) if S4.orders[i]%2))
assert co==c

# Composite m=15. Independent group S3 x C10, H=C3 x C10, p=2.
# Additive lambda exponent is 5*j + 3*k modulo 15, where j labels the order-3 factor
# and k is the C10 coordinate modulo 5. This includes p-elements in H.
H3=next(G.cyclic(i) for i in range(G.n) if G.orders[i]==3)
t=next(i for i in H3 if G.orders[i]==3)
labels={x:j for j,x in enumerate(G.powers[t])}
H10=C.cyclic(10);D=C.direct(G,H10)
H={i for i,(x,y) in enumerate(D.elements) if x in H3}
lab={i:(5*labels[x]+3*(y%5))%15 for i,(x,y) in enumerate(D.elements) if i in H}
T=[0]*15
for x in range(D.n):
 y=D.regular(x,2)
 if y in H:T[lab[y]]+=1
assert all(lab[D.table[x][y]]==(lab[x]+lab[y])%15 for x in H for y in H)
divisors=[1,3,5,15]
ts={d:T[(15//d)%15] for d in divisors}
assert ts=={1:8,3:2,5:8,15:2}
msum=sum(int(S.mobius(d))*ts[d] for d in divisors)
assert msum==0
# Compute exact Fourier polynomial remainder in Q[z]/Phi_15, independently of Mobius grouping.
z=S.Symbol('z')
rem=S.rem(sum(T[j]*z**((-j)%15) for j in range(15)),S.cyclotomic_poly(15,z),z)
assert rem==0
# Direct induced character calculation coordinatewise in the same cyclotomic field.
polys={h:S.Poly(S.rem(z**lab[h],S.cyclotomic_poly(15,z),z),z) for h in H}
for k in range(8):
 vals={h:int(poly.nth(k)) for h,poly in polys.items()}
 induced=D.induced(H,vals)
 assert sum(induced[D.regular(x,2)] for x in range(D.n))==0
out={'S3_p2_projective_coefficients':list(map(str,c)),
 'S4_mod_V4_p2_projective_coefficients':list(map(str,co)),
 'composite_mobius_control':{'group':'S3 x C10','H':'C3 x C10','p':2,'m':15,'fiber_counts':T,
 'primitive_root_per_root_counts':ts,'signed_numerator':msum,'direct_cyclotomic_induction_average':0}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
