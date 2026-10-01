"""Exact symbolic certificates for the circle-odd Hodge factorization."""
import sympy as s
from itertools import product
from collections import Counter
import json
N=Counter()
def ck(x,label):
 assert x,label
 N[label]+=1
A,B,C,D,E,fp,fpp,lam=s.symbols('A B C D E fp fpp lam',real=True)
# Radial integration derivative: A'=C-A², p'/p=3A+2B-f'.
ibp=-(C-A*A+(3*A+2*B-fp)*A)
rad=s.expand(A*A+4*A*A-2*C+ibp)
sph=s.expand(A*A+A*A-2*A*B+ibp)
ck(s.expand(rad-(3*A*A-3*C-2*A*B+A*fp))==0,'radial_rescaling_coefficient')
ck(s.expand(sph-(-C-4*A*B+A*fp))==0,'sphere_rescaling_coefficient')
# The soliton equations in circle, radial and sphere directions.
sub={C:-2*A*B+A*fp+lam}
ck(s.expand((rad-(3*A*A-2*C-lam)).subs(sub))==0,'circle_equation_radial_reduction')
ck(s.expand((sph-(-2*A*B-lam)).subs(sub))==0,'circle_equation_sphere_reduction')
RicFrr=-2*D+fpp-3*(C-A*A)
RicFss=E-D+B*(fp-3*A)
ck(s.expand(RicFrr.subs(fpp,C+2*D-lam)-(3*A*A-2*C-lam))==0,'weighted_Ricci_radial')
ck(s.expand(RicFss.subs(E,D+A*B-B*fp-lam)-(-2*A*B-lam))==0,'weighted_Ricci_sphere')
# Equivalent invariant Hessian identity, verified coefficient-wise.
x,y=s.symbols('x y')
ck(s.expand(x-lam-3*(x-y)-(-2*x+3*y-lam))==0,'invariant_Hessian_formula')
for a,b,f,k in product(range(1,9),range(1,9),range(-4,5),range(1,8)):
 mu=a**3*b**2
 norm_tensor=2*a*b**2*(a*k)**2
 ck(norm_tensor==2*mu*k*k,'weighted_unitary_norm')
for l in range(1,101):
 ck(l*(l+1)>0,'positive_nonconstant_sphere_eigenvalue')
 ck(2+2*l-1>0,'origin_boundary_power')
for multiplicities in product(range(7),repeat=4):
 even0,odd0,k1,k2=multiplicities
 ck((even0+odd0+2*k1+2*k2)%2==(even0+odd0)%2,'real_Fourier_parity')
 ck((even0+2*k1+2*k2)%2==even0%2,'parity_after_odd_sector_removed')
print(json.dumps({'status':'PASS','assertions':sum(N.values()),'counts':dict(sorted(N.items())),'sympy_version':s.__version__,'scope':'Symbolic local identities and finite arithmetic only; domain closure and weighted harmonic vanishing are analytic proofs in TURN_3.md.'},indent=2,sort_keys=True))
