#!/usr/bin/env python3
"""Exact matrix/word controls; not a verifier for the full current problem."""
import sympy as s
from collections import Counter
import json

counts=Counter()
def check(ok,name):
    assert bool(ok), name
    counts[name]+=1
A=s.Matrix([[1,2],[0,1]]);B=s.Matrix([[1,0],[2,1]])
for M in [A,B,A*B,A*B.inv()]:
    check(M.det()==1,'SL2_determinants')
    check(all((M[i,j]-(1 if i==j else 0))%2==0 for i in range(2) for j in range(2)),
          'principal_level_two_congruences')
check(A.trace()==2 and B.trace()==2,'cusp_generators')
check((A*B.inv()).trace()==-2,'third_cusp_trace')
check((A*B).trace()==6,'hyperbolic_closed_word_trace')
check((A*B).charpoly().as_expr().subs(s.Symbol('lambda'),s.Symbol('t'))==s.Symbol('t')**2-6*s.Symbol('t')+1,
      'hyperbolic_characteristic_polynomial')
check(3+2*s.sqrt(2)>1,'positive_translation_length')

# A classical trace-reversal control in the rank-two free group.
word='aababb'; reverse="aaabbb"
def rotations(w):return {w[k:]+w[:k] for k in range(len(w))}
inverse=''.join(c.swapcase() for c in word[::-1])
check(reverse not in rotations(word),'different_cyclic_words')
check(reverse not in rotations(inverse),'different_unoriented_cyclic_words')
for w in [word,reverse]:
    for period in [1,2,3]:
        check(w!=w[:period]*(len(w)//period),'not_proper_powers')

z,p,q,r=s.symbols('z p q r',nonzero=True)
M=s.diag(z,1/z);N=s.Matrix([[p,q],[r,(1+q*r)/p]])
check(s.cancel(M.det())==1 and s.cancel(N.det())==1,'generic_SL2_pair')
def evaluate(w,A,B):
    out=s.eye(2)
    for letter in w: out=out*({'a':A,'b':B}[letter])
    return out
check(s.cancel(s.trace(evaluate(word,M,N))-s.trace(evaluate(reverse,M,N)))==0,
      'generic_trace_reversal_identity')
for k in range(1,8):
    Ap=s.Matrix([[1,k],[0,1]]);Bp=s.Matrix([[1,0],[k+1,1]])
    check(s.trace(evaluate(word,Ap,Bp))==s.trace(evaluate(reverse,Ap,Bp)),
          'integer_trace_controls')

print(json.dumps({'status':'PASS','sympy_version':s.__version__,
 'checks':dict(counts),'assertions':sum(counts.values()),
 'trace_control_words':[word,reverse],
 'scope':'Exact matrix and free-word controls only. The one-point Teichmuller scope, nonatomic current, compactness, and simple-reference theorem require the written argument and source audit; no finite all-metric test is claimed.'},indent=2))
