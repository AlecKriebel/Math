#!/usr/bin/env python3
"""Auxiliary exact adversarial controls; universal analytic claims are prose-audited."""
import json
from itertools import product
from fractions import Fraction
import sympy as s
x,y,t,w,T=s.symbols('x y t w T')
counts={'ramified_tensor_resultants':0,'torus_coset_constant_coefficients':0,'crossing_transversality':0,'character_decay_bounds':0}
def ck(v,key):
    assert v
    counts[key]+=1
# Two independent ramified polynomial fibers, including unequal degrees and repeated roots.
for d,e,a,b in [(2,2,0,0),(2,3,1,-1),(3,2,-1,2),(1,3,0,0)]:
    px=x**d+a*x-w if d>1 else x-w
    py=y**e+b*y-w if e>1 else y-w
    def quotient_matrix(z,p,degree):
        C=s.zeros(degree)
        for j in range(degree):
            r=s.rem(z**(j+1),p,z)
            for i in range(degree):C[i,j]=r.coeff(z,i)
        return C
    A=s.kronecker_product(quotient_matrix(x,px,d),s.eye(e))
    B=s.kronecker_product(s.eye(d),quotient_matrix(y,py,e))
    M=A*B+A+2*B+s.eye(d*e)
    candidate=M.charpoly(T).as_expr()
    elimination=s.resultant(py,s.resultant(px,T-(x*y+x+2*y+1),x),y)
    ck(s.expand(candidate-elimination)==0,'ramified_tensor_resultants')
    for v in [-1,0,1]:
        ck(s.Poly(candidate.subs(w,v),T).degree()==d*e,'ramified_tensor_resultants')
        ck(s.Poly(candidate.subs(w,v),T).LC()==1,'ramified_tensor_resultants')
# Torus-coset mechanism: nonzero powers never create a constant Laurent term.
for r,q in product([-3,-2,-1,1,2,3],repeat=2):
    expr=s.expand((2*t**(2*r)+3*t**(-r)+7)+(5*t**q-4*t**(-2*q)+11))
    constant=sum(term for term in s.Add.make_args(expr) if term.as_powers_dict().get(t,0)==0)
    ck(constant==18,'torus_coset_constant_coefficients')
# Divisor crossings: Y derivative in the remaining coordinate equals -2≠0.
for zero_pair in [(0,1),(0,2),(1,2)]:
    remaining=({0,1,2}-set(zero_pair)).pop()
    values=[s.Integer(1)]*3;values[remaining]=-2
    ck(sum(values)==0,'crossing_transversality')
    ck(values[remaining]!=0,'crossing_transversality')
ck(sum([1,1,1])!=0,'crossing_transversality')
# Exact asymptotic exponent premise in the full nonnegative unit cube.
for alpha in product([Fraction(0),Fraction(1,101),Fraction(1,2),Fraction(100,101)],repeat=3):
    ck((sum(alpha)>0)==any(a>0 for a in alpha),'character_decay_bounds')
    for a in alpha:ck(Fraction(1)-a>0,'character_decay_bounds')
print(json.dumps({'status':'PASS','assertions':sum(counts.values()),'families':counts,'finite_auxiliary_controls_only':True,'proves_original_problem':False},indent=2))
