#!/usr/bin/env python3
"""Independent exact audit controls. Python >=3.10; standard library only.

These deterministic finite tests discriminate hypotheses and algebraic mistakes.
They do not prove any infinite-orbit, Fatou-boundary, or general Baker theorem.
Run: python3 audit_controls.py > audit-controls.json
"""
from fractions import Fraction as Q
from math import factorial
import json

# Gaussian rational arithmetic, independent of the packet's polynomial approach.
class G:
    def __init__(self, re=0, im=0):
        self.re, self.im = Q(re), Q(im)
    @staticmethod
    def as_g(z):
        return z if isinstance(z, G) else G(z)
    def __add__(self, z):
        z=self.as_g(z); return G(self.re+z.re,self.im+z.im)
    __radd__=__add__
    def __neg__(self): return G(-self.re,-self.im)
    def __sub__(self,z): return self+-self.as_g(z)
    def __rsub__(self,z): return self.as_g(z)+-self
    def __mul__(self,z):
        z=self.as_g(z)
        return G(self.re*z.re-self.im*z.im,self.re*z.im+self.im*z.re)
    __rmul__=__mul__
    def __truediv__(self,z):
        z=self.as_g(z); d=z.norm2()
        if not d: raise ZeroDivisionError
        return self*G(z.re/d,-z.im/d)
    def __rtruediv__(self,z): return self.as_g(z)/self
    def __pow__(self,n):
        assert isinstance(n,int) and n>=0
        out=G(1)
        for _ in range(n): out=out*self
        return out
    def __eq__(self,z):
        z=self.as_g(z); return self.re==z.re and self.im==z.im
    def norm2(self): return self.re*self.re+self.im*self.im

I=G(0,1)
def T(w): return w-1/w
def C(w): return (w-I)/(w+I)
def Ci(z): return I*(1+z)/(1-z)
def g(z): return (3*z*z+1)/(z*z+3)

conjugacy_count=0
for a in range(-6,7):
    for b in range(-6,7):
        z=G(Q(a,7),Q(b,7))
        if z.norm2()>=1: continue
        w=Ci(z)
        assert w.im>0
        assert C(T(w))==g(z)
        assert (z*z+3).norm2()-(3*z*z+1).norm2()==8*(1-z.norm2()**2)
        assert g(z).norm2()<1
        assert (g(z)-z)*(z*z+3)==(1-z)**3
        conjugacy_count+=1
# The sign-reversed Boole map is detectably a different model.
assert C(I+1/I)==G(-1)
assert g(G(0))==G(Q(1,3))

circle_count=0
for k in range(-40,41):
    x=Q(k,8); z=C(G(x))
    assert z.norm2()==1 and g(z).norm2()==1
    if x: assert g(z)==C(G(x-1/x))
    circle_count+=1
# Sphere extension: a finite prepole DOES converge to infinity eventually.
assert C(G(0))==G(-1)
assert g(G(-1))==G(1) and g(G(1))==G(1)
assert g(C(G(1)))==G(-1)  # 1 -> 0 -> infinity, on the sphere.

# Independent real recurrence stress test and compact-anchor contrast.
def real_t(x): return x-1/x
contractions=0
for den in range(1,12):
    for num in range(-35,36):
        x=Q(num,den)
        if abs(x)>1:
            y=real_t(x)
            assert abs(y)==abs(x)-1/abs(x)
            assert x*x-y*y==2-1/(x*x)>1
            contractions+=1
anchor_exits=[]
for k in range(1,65):
    x=1+Q(k,64); steps=0
    while x>1:
        x=real_t(x); steps+=1
        assert steps<=4
    anchor_exits.append(steps)
# Long excursions can start in a bounded, noncompact set next to the pole.
# First iterate is large, whereas x0 -> 0 where T is not continuous.
bounded_start_prefixes=[]
for R in [1,3,11]:
    for N in [1,3,6,10]:
        m=R+N+3; x0=-Q(1,m); x=real_t(x0)
        assert -1<x0<0 and x>R+N+2
        for j in range(N+1):
            assert x>R
            if j<N: x=real_t(x)
        bounded_start_prefixes.append({'R':R,'N':N,'start':str(x0),'all_postfirst_prefix_terms_above_R':True})

# Exact upper/lower exponential enclosures; unlike the original controls,
# these check the actual e-1 chord coefficient at all interior sample points.
def exp_bounds(t,d=40):
    assert 0<=t<d+2
    lo=sum((t**j/factorial(j) for j in range(d+1)),Q(0))
    tail=t**(d+1)/factorial(d+1)
    hi=lo+tail/(1-t/Q(d+2))
    return lo,hi
elo,ehi=exp_bounds(Q(1))
chord_samples=[]
for k in range(1,64):
    t=Q(k,64); lo,hi=exp_bounds(t)
    assert lo>=1+t
    assert hi<1+(elo-1)*t
    chord_samples.append(str(t))
# t=0 and t=1 satisfy the chord inequality as identities.
assert exp_bounds(Q(0))==(Q(1),Q(1))
# Extending the chord inequality to t=2 would be false.
assert exp_bounds(Q(2))[0]>1+2*(ehi-1)
# Deformed invariant-line displacement is a*(1-exp(delta)) below threshold.
for a in [Q(1,10),Q(1),Q(2),Q(7)]:
    for delta in [Q(1,100),Q(1,2),Q(1),Q(3)]:
        assert a*(1-exp_bounds(delta)[0])<0

# Adversarial compact-selection controls, not Baker-domain examples.
# Weakening covering to adjacent intersection fails even for continuous entire F.
# F(x)=x/2 and K_n={2^n,2^(n+2)} have escaping minima and adjacent
# intersections, but no forward orbit through all K_n.
def K(n): return {Q(2)**n,Q(2)**(n+2)}
for n in range(20):
    image={x/2 for x in K(n)}
    assert image & K(n+1)
    assert not image>=K(n+1)
viable=[]
for n in range(5):
    ens={x for x in K(0) if all(x/(Q(2)**j) in K(j) for j in range(n+1))}
    viable.append(len(ens))
assert viable==[2,1,0,0,0]
# Reverse coverings alone also fail: F({2^(n+1)})={2^n}.
for n in range(20): assert Q(2)**(n+1)/2==Q(2)**n

# Residue constant +1, with a sharpness witness h(z)=z:
# (h-T)(z)=1/z, so on |z|=r the lower bound 1/r is attained.
residue_sharpness=0
for r in [Q(1,10),Q(1,2),Q(1),Q(2),Q(13)]:
    for a,b in [(Q(1),Q(0)),(Q(0),Q(1)),(Q(3,5),Q(4,5)),(Q(-5,13),Q(12,13))]:
        z=G(r*a,r*b)
        assert z.norm2()==r*r
        assert (z-T(z)).norm2()==1/(r*r)
        residue_sharpness+=1

print(json.dumps({
    'target_id':30001388,
    'status':'passed',
    'arithmetic':'fractions.Fraction including Gaussian rationals; no floating-point arithmetic',
    'exact_disk_conjugacy_samples':conjugacy_count,
    'exact_circle_samples':circle_count,
    'wrong_sign_model_rejected':True,
    'finite_prepole_sphere_exception_verified':True,
    'real_contraction_samples':contractions,
    'compact_positive_anchor_samples':len(anchor_exits),
    'max_observed_anchor_exit_steps':max(anchor_exits),
    'bounded_near_pole_prefixes':bounded_start_prefixes,
    'actual_e_minus_1_chord_interior_samples':len(chord_samples),
    'chord_endpoints_checked_as_identities':True,
    'chord_extension_to_t_2_rejected':True,
    'deformation_negative_displacement_samples':16,
    'weak_covering_viable_prefix_counts':viable,
    'reverse_covering_counterexample_checked':True,
    'sharp_residue_lower_bound_samples':residue_sharpness,
    'scope':'Finite controls and exact countermodels only. No general Baker-domain theorem, boundary membership, or infinite orbit is established by executing this script.'
},indent=2,sort_keys=True))
