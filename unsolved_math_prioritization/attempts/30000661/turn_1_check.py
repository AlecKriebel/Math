"""Own exact normalization controls; no generalized-tame conclusion follows."""
import sympy as s
from collections import Counter
import json
C=Counter()
def eq(a,b,label):
 assert s.cancel(s.expand(a-b))==0,label
 C[label]+=1
x,y,z,u,v,w,t=s.symbols('x y z u v w t')
D=x*x*y+z*z
T=D-2*x*z**3
G={x:x,z:z+x*D,y:y-2*x*y*z-D**2+2*(3*z*z*D+3*x*z*D**2+x*x*D**3)}
H={x:x,z:z-x*T,y:y+2*x*y*z-4*z**4-T**2}
for q in (x,y,z):
 eq(G[q].xreplace(H),q,'polynomial_inverse_left')
 eq(H[q].xreplace(G),q,'polynomial_inverse_right')
eq(s.det(s.Matrix([G[x],G[y],G[z]]).jacobian((x,y,z))),1,'Jacobian_one')
eq(D.xreplace(G),D+2*x*G[z]**3,'Delta_transform')
eq(T.xreplace(G),D,'Theta_transform')
D0=lambda f:s.expand(x*x*s.diff(f,z)-2*z*s.diff(f,y))
D1=lambda f:s.cancel(D*D0(f)/x)
eq(D0(D),0,'localized_LND_kernel')
eq(D1(z),x*D,'localized_LND_z')
eq(D1(D1(z)),0,'localized_LND_z_nilpotence')
eq(D1(D1(y)),-2*D**2,'localized_LND_y_second')
eq(D1(D1(D1(y))),0,'localized_LND_y_nilpotence')
Nz=z+x*D;Ny=y-2*z*D/x-D**2
for got,expect in [(Nz,G[z]),(Ny+2*Nz**3/x,G[y])]:eq(got,expect,'rational_factorization')
eq(s.cancel(x*(y+2*z**3/x)).subs(x,0),2*z**3,'E_actual_pole')
eq(s.cancel(x*Ny).subs(x,0),-2*z**3,'N_actual_pole')
eq(G[y].subs(x,0),y+5*z**4,'special_fiber')
eq(G[z].subs(x,0),z,'special_fiber')
# The (v,w) coordinate change is singular as a polynomial change at x=0.
eq(s.det(s.Matrix([z,z+x*D]).jacobian((y,z))),-x**3,'coordinate_change_determinant')
eq((z+x*D).xreplace(G),2*G[z]-z+2*x*x*G[z]**3,'Henon_second_coordinate')
# Iteration in formal Henon coordinates controls all iterates by recurrence.
F0=v;F1=w
for n in range(1,6):
 F2=s.Poly(2*F1-F0+2*x*x*F1**3,w,v)
 # Use leading w-degree; the leading coefficient never cancels in characteristic zero.
 expected=3**n
 assert F2.degree(w)==expected;C['Henon_iteration_degree']+=1
 eq(F2.coeff_monomial(w**expected), (2*x*x)**((3**n-1)//2),'Henon_leading_coefficient')
 # Avoid exponentially expanding the next full polynomial: a few exact iterates
 # suffice as controls; the general induction is in the written proof.
 if n==2:break
 F0,F1=F1,F2.as_expr()
# Direct z_1,z_2,z_3 degrees over C(x), matching the general induction formula.
Z0=z;Z1=G[z]
for n in range(1,4):
 P=s.Poly(s.expand(Z1),y,z)
 assert P.total_degree()==2*3**(n-1);C['original_z_degree']+=1
 eq(P.coeff_monomial(z**(2*3**(n-1))),2**((3**(n-1)-1)//2)*x**(2*3**(n-1)-1),'original_z_leading_term')
 if n<3:Z0,Z1=Z1,s.expand(2*Z1-Z0+2*x*x*Z1**3)
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'limitations':'Inverse, localized factorization and degree-growth identities only. They do not produce a finite product of polynomial LND exponentials or prove nonmembership in that generated subgroup.'},indent=2,sort_keys=True))
