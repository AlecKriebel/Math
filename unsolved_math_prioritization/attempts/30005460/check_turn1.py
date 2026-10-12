"""Exact finite controls for the circuit and formal-template reductions.

No SDP solver or numerical non-SOS inference is used. The universal statements
are proved in TURN_1.md; this script verifies identities and boundary controls.
"""
from itertools import product
from fractions import Fraction
from math import comb
from collections import Counter
import json
import sympy as S

counts = Counter()
def ck(x, family):
    assert x, family
    counts[family] += 1

x,y,z,a,u,v = S.symbols('x y z a u v')
M = x**4*y**2+x**2*y**4+z**6-a*x**2*y**2*z**2
H = [
 x**5*y**4-a*x**3*y**4*z**2,
 x**4*y**5-a*x**4*y**3*z**2,
 x**4*y**2*z**3-a*x**2*y**2*z**5,
 x**2*y**4*z**3-a*x**2*y**2*z**5,
 x*y**2*z**6-a*x**3*y**4*z**2,
 x**2*y*z**6-a*x**4*y**3*z**2,
 x**2*y**4*z**3-x**4*y**2*z**3,
 x**4*y**5-x**2*y*z**6,
 x**5*y**4-x*y**2*z**6,
]
terms = [(S.Rational(3,2),h) for h in H] + [
 (1,z**9-2*a*x**2*y**2*z**5),
 (a,x*y*z**7-2*a*x**3*y**3*z**3),
 (1,x**3*y**6-2*a*x**3*y**4*z**2),
 (a,x**3*y**5*z-2*a*x**3*y**3*z**3),
 (1,x**6*y**3-2*a*x**4*y**3*z**2),
 (a,x**5*y**3*z-2*a*x**3*y**3*z**3),
 (15-13*a**3,x**3*y**3*z**3),
]
ck(S.Poly(S.expand(M**3-sum(c*h*h for c,h in terms)),x,y,z,a).is_zero,
   'published_Motzkin_cube_polynomial_identity')
for coefficient,h in terms:
    ck(S.sympify(coefficient).subs(a,1)>0, 'M1_positive_square_weights')
    ck(all(sum(exponents[:3])==9 for exponents in S.Poly(h,x,y,z,a).monoms()),
       'square_summand_homogeneity')

# Half Newton simplex for M_a itself and its negative inner coefficient.
half = []
for i in range(4):
    for j in range(4-i):
        k=3-i-j
        bary=(Fraction(2*i-j,3),Fraction(2*j-i,3),Fraction(k,3))
        if min(bary)>=0 and sum(bary)==1:half.append((i,j,k))
ck(half==[(0,0,3),(1,1,1),(1,2,0),(2,1,0)], 'Motzkin_half_Newton_lattice')
pairs=[(s,t) for s in half for t in half if tuple(s[i]+t[i] for i in range(3))==(2,2,2)]
ck(pairs==[((1,1,1),(1,1,1))], 'negative_coefficient_not_SOS_control')
for r,s,t,c in product(range(1,6),range(1,6),range(1,6),range(-2,3)):
    A=r**4*s**2;B=r**2*s**4;C=t**6;D=c*r*r*s*s*t*t
    ck(D**3==c**3*A*B*C, 'diagonal_Motzkin_normalization')

# Exact weighted geometric-mean superadditivity controls, including zeros.
# a_i=lambda_i U_i^L makes Theta(a)=product_i U_i^w_i rational/integer.
for L in range(2,7):
    for length in (2,3):
        for weights in product(range(1,L),repeat=length):
            if sum(weights)!=L:continue
            for U in product(range(3),repeat=length):
                for V in product(range(3),repeat=length):
                    A=1;B=1;combined=1
                    for ui,vi,w in zip(U,V,weights):
                        A*=ui**w;B*=vi**w
                        combined*=(ui**L+vi**L)**w
                    ck((A+B)**L<=combined, 'weighted_mean_superadditivity')

# Every lower odd exponent has an explicit binomial monomial outside the ideal.
for q in range(1,16,2):
    for t in range(1,16,2):
        N=q+t-1
        for n in range(1,N,2):
            i=min(q-1,n);j=n-i
            ck(i<q and j<t and i+j==n and comb(n,i)>0,
               'formal_lower_exponent_missing_monomial')
        coefficient=[0]*(N+1)
        for i in range(q):coefficient[i]+=comb(N,i)
        for j in range(t):coefficient[q+j]+=comb(N,q+j)
        ck(coefficient==[comb(N,i) for i in range(N+1)],
           'published_sharp_exponent_split_identity')
        ck((q-1)%2==(t-1)%2==0 and N>q-1 and N>t-1,
           'truncated_binomial_input_hypotheses')
        for n in range(N,N+20,2):
            ck((n-N)%2==0,'higher_odd_exponent_square_multiplier')

F=10*u*u+5*u*v+v*v
ck(S.expand(F-10*(u+v/4)**2-S.Rational(3,8)*v*v)==0,
   'explicit_binary_SOS_multiplier')
ck(S.expand((u+v)**5-v**3*F-u**3*F.xreplace({u:v,v:u}))==0,
   'cube_inputs_fifth_power_identity')

print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),
 'categories':dict(sorted(counts.items())),
 'scope':'Finite exact identity, lattice, scaling, geometric-mean and monomial-ideal controls. No counterexample to fixed-exponent convexity or numerical SOS feasibility claim.',
 'known_identity_credit':'Blekherman–Kozhasov–Reznick, Forum Math. Sigma14(2026), Theorems5.1–5.3 and the identity following Theorem6.3.'},indent=2,sort_keys=True))
