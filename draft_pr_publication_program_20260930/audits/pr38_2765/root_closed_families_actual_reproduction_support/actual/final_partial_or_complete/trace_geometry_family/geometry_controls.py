#!/usr/bin/python3
"""Audit controls only; no finite test certifies a current-fiber theorem."""
import json
import sympy as s
from collections import Counter
counts=Counter()
def check(value,label):
    assert bool(value),label
    counts[label]+=1

def rotations(w):return {w[k:]+w[:k] for k in range(len(w))}
def inverse(w):return ''.join(c.swapcase() for c in w[::-1])
def evalword(w,A,B):
    out=s.eye(2)
    for letter in w:out=out*{'a':A,'A':A.inv(),'b':B,'B':B.inv()}[letter]
    return out
p,q,r,u,v,w=s.symbols('p q r u v w',nonzero=True)
A=s.Matrix([[p,q],[r,(1+q*r)/p]])
B=s.Matrix([[u,v],[w,(1+v*w)/u]])
x=A.trace();y=B.trace();z=(A*B).trace()
f=x*x*y*z-x*z*z-x*y*y+x
for word in ['aaBab','aabaB']:
    check(s.cancel(evalword(word,A,B).trace()-f)==0,'six_parameter_exact_trace_formula')
check('aabaB' not in rotations('aaBab'),'distinct_Horowitz_cyclic_words')
check('aabaB' not in rotations(inverse('aaBab')),'distinct_Horowitz_unoriented_words')
AA=s.Matrix([[1,2],[0,1]]);BB=s.Matrix([[1,0],[2,1]])
for word,expected in [('aaBab',[[-27,-10],[-8,-3]]),('aabaB',[[-35,22],[-8,5]]),('aababb',[[97,22],[22,5]]),('bbabaa',[[5,22],[22,97]])]:
    M=evalword(word,AA,BB)
    check(M.tolist()==expected,'actual_Gamma2_word_matrix')
    check(M.det()==1 and abs(M.trace())>2,'actual_Gamma2_word_hyperbolic')
check(evalword('aababb',AA,BB).trace()==102,'original_reversal_trace_102')
check(evalword('aaabbb',AA,BB).trace()==38,'wrong_word_trace_38')
# Jyothis v3 Eq.8, k=2,t=3; count formulas are source-defined geometric data.
triples=[(17,12,3),(19,8,5)]
check(sum(triples[0])==sum(triples[1])==32,'v3_equal_total_half_twists')
a,b,c=triples[0];ap,bp,cp=triples[1]
check((a-ap)+3*(b-bp)+5*(c-cp)==0,'v3_equal_self_intersection_linear_constraint')
values=[]; traces=[]
for a,b,c in triples:
    check(a>=b>=c and a%2==c%2==1 and b%2==0,'v3_parity_and_order')
    count=(a-1)//2+3*(b-2)//2+5*(c-1)//2+6
    arcs=[(a-1)//2+(b-2)//2+(c-1)//2+3,a+b+c,(a-1)//2+(b-2)//2+(c-1)//2+4]
    values.append([count,arcs])
    M=BB*AA*BB**((c+1)//2)*AA.inv()*BB**(b//2)*AA.inv()*BB**((a-1)//2)
    traces.append(int(M.trace()))
check(values[0]==values[1]==[34,[17,32,18]],'v3_matching_source_count_and_arc_formulas')
check(traces==[6270,6654],'v3_actual_word_trace_separation')
# Local self-intersection integral is finite; this does not assert cusped continuity.
theta,phi=s.symbols('theta phi',real=True)
angular=2*s.integrate(s.integrate(s.sin(theta-phi),(phi,0,theta)),(theta,0,s.pi))
check(s.simplify(angular-2*s.pi)==0,'exact_angular_integral')
check(s.simplify(s.Rational(1,4)*angular*2*s.pi-s.pi**2)==0,'standard_unoriented_Liouville_self_length')
# Direct Möbius side pairing for the ideal quadrilateral -1,0,1,infinity.
def mobius(M,z):return s.cancel((M[0,0]*z+M[0,1])/(M[1,0]*z+M[1,1]))
check(mobius(AA,-1)==1,'vertical_side_pairing')
check(mobius(BB,-1)==1 and mobius(BB,0)==0,'semicircle_side_pairing_endpoints')
check(s.simplify(mobius(BB,s.Rational(-1,2)+s.I/2)-(s.Rational(1,2)+s.I/2))==0,'semicircle_side_pairing_midpoint')
print(json.dumps({'status':'PASS','sympy_version':s.__version__,'assertions':sum(counts.values()),'checks':dict(counts),'jyothis_v3_triples':triples,'jyothis_v3_word_traces':traces,'scope':'Exact formula, word, parity, angle and ideal-quadrilateral side-map controls. The six essential arc argument, polygon theorem, surface retraction and positivity support proof remain mathematical arguments; no arbitrary-current classification is tested.'},indent=2))
