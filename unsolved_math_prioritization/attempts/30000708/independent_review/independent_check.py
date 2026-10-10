"""Independent exact controls for the classical punctured-measure counterexample.

These verify finite algebra, antiderivatives and cone inequalities. They do
not reprove the imported exterior Radon support theorems.
"""
import sympy as S
from fractions import Fraction as Q
from collections import Counter
import json
C=Counter()
def ck(v,k):
 assert v,k
 C[k]+=1
def eq(v,k):ck(S.simplify(v)==0,k)
t,p,x,y=S.symbols('t p x y',real=True);I=S.I
# Every line at nonzero signed distance p is a unit rotation of p+it.
for k in range(3,10):
 primitive=(p+I*t)**(1-k)/(I*(1-k))
 eq(S.diff(primitive,t)-(p+I*t)**(-k),'line_primitive')
 for pv in [-7,-2,-1,1,3,8]:
  ck(S.limit(primitive.subs(p,pv),t,S.oo)==0,'line_positive_endpoint')
  ck(S.limit(primitive.subs(p,pv),t,-S.oo)==0,'line_negative_endpoint')
# Explicit real power3 density and its nonzero values.
f=S.re((x+I*y)**(-3)).expand(complex=True)
eq(f-(x**3-3*x*y*y)/(x*x+y*y)**3,'real_cubic_density')
a=S.symbols('a',positive=True)
eq(f.subs({x:a*x,y:a*y})-a**(-3)*f,'density_homogeneity_minus3')
for xv,yv in [(1,0),(-1,0),(2,1),(3,1),(-3,1)]:
 ck(f.subs({x:xv,y:yv})!=0,'nontrivial_density_samples')
# Polar absolute-tail upper bound r^-3 in dimension2: finite outside epsilon,
# while both angular sign sectors have infinite mass near zero.
r,e=S.symbols('r e',positive=True)
eq(S.integrate(r**(-2),(r,e,S.oo))-1/e,'absolute_tail_radial_bound')
eq(S.integrate(r**0,(r,0,1))+S.integrate(r**(-2),(r,1,S.oo))-2,'Levy_weighted_radial_bound')
ck(S.integrate(r**(-2),(r,0,1))==S.oo,'origin_radial_infinite_mass')
# An enclosing cone in x_d >= delta*||x'|| is uniformly inside a hemisphere.
# Finite rational controls of the projective map used in the credited theorem.
for d in range(2,6):
 for n in range(1,21):
  xp=[Q((j+1)*n,7) for j in range(d-1)];xd=Q(1)+sum(abs(v) for v in xp)
  image=[v/(1+xd) for v in xp];yd=xd/(1+xd)
  ck(0<yd<1,'projective_cone_height')
  ck(sum(abs(v) for v in image)<yd,'projective_cone_bounded_slice')
  ck([v/(1-yd) for v in image]==xp and yd/(1-yd)==xd,'projective_inverse')
# Avoiding-origin halfspace restriction under an isometric embedding of R2.
for pval in [-5,-2,-1]:
 for w1,w2 in [(Q(1),Q(0)),(Q(0),Q(1)),(Q(3,5),Q(4,5))]:
  ck(w1*w1+w2*w2==1 and pval<0,'halfspace_closure_avoids_origin')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(sorted(C.items())),'sympy_version':S.__version__,'scope':'Independent exact inverse-power kernel, radial-integrability and projective-cone algebra. Classical support and uniqueness theorems remain credited source inputs.'},indent=2,sort_keys=True))
