"""Own exact controls for the determinant-one contraction and flow-word reduction."""
import sympy as s
from collections import Counter
import json
C=Counter()
def eq(a,b,key):
 assert s.cancel(s.expand(a-b))==0,key
 C[key]+=1
x,y,z,t=s.symbols('x y z t')
lam,a=s.symbols('lam a',nonzero=True)
vars=(x,y,z);D=x*x*y+z*z

def family(t):
 return {x:x,z:z+t*x*D,y:y-2*t*x*y*z-t*t*D**2+6*t*t*z*z*D+6*t**3*x*z*D**2+2*t**4*x*x*D**3}

def inverse(t):
 T=D-2*t*x*z**3
 return {x:x,z:z-t*x*T,y:y+2*t*x*y*z-4*t*t*z**4-t*t*T**2}
G=family(1);H=inverse(1);Ft=family(t);Ht=inverse(t)
for v in vars:
 eq(Ft[v].xreplace(Ht),v,'polynomial_family_inverse')
 eq(Ht[v].xreplace(Ft),v,'polynomial_family_inverse')
 eq(Ft[v].subs(t,0),v,'family_at_zero')
scale={x:lam**3*x,y:lam**-4*y,z:lam*z}
invscale={x:lam**-3*x,y:lam**4*y,z:lam**-1*z}
for v in vars:
 got=invscale[v].xreplace(G).xreplace(scale)
 eq(got,family(lam**4)[v],'SL3_contraction_identity')
eq(lam**3*lam**-4*lam,1,'scaling_determinant')
# Ring composition sigma_M sigma_N has the reversed coordinate-matrix product.
U=lambda c:s.Matrix([[1,c],[0,1]])
L=lambda c:s.Matrix([[1,0],[c,1]])
word=[L(-a),U(1/a-1),L(1),U(a-1)]
M=s.eye(2)
for factor in word:M=factor*M
for i in range(2):
 for j in range(2):eq(M[i,j],s.diag(a,1/a)[i,j],'four_transvection_block')
# Explicit polynomial LND conjugates may move x. For B=y*d/dx,
# gamma B gamma^-1 is polynomial, and nilpotence follows before substitution.
B=lambda f:s.expand(y*s.diff(f,x))
eq(B(H[x]).xreplace(G),G[y],'conjugated_LND_moves_x')
for v,bound in [(x,2),(y,5),(z,4)]:
 f=H[v]
 for _ in range(bound):f=B(f)
 eq(f,0,'conjugated_LND_coordinate_nilpotence')
# eta_t=gamma_t gamma^-1 is a polynomial family; at t=0 it is gamma^-1.
for v in vars:
 eta=H[v].xreplace(Ft)
 eq(eta.subs(t,0),H[v],'relative_family_limit')
 eq(eta.subs(t,1),v,'relative_family_identity_at_one')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'scope':'Contraction family, finite elementary/conjugated-LND word for nonzero parameters, and polynomial limit identities. Membership of the limiting gamma in the generated subgroup is not proved.'},indent=2,sort_keys=True))
