#!/usr/bin/env python3
"""Exact algebra controls for the continuous C*-dilation counterexample.

Standard library only. Scalars are in Q(sqrt(2),sqrt(3),sqrt(5)); no float
arithmetic is used. The program verifies the finite witness and compression
identities, not the analytic continuity proof or a literature-priority claim.
"""
from fractions import Fraction as F
import json
from pathlib import Path

class K:
    def __init__(self, value=0):
        if isinstance(value,K): self.c=value.c
        elif isinstance(value,(list,tuple)):
            assert len(value)==8
            self.c=tuple(F(x) for x in value)
        else: self.c=(F(value),)+(F(0),)*7
    def __add__(a,b):
        b=K(b);return K([x+y for x,y in zip(a.c,b.c)])
    __radd__=__add__
    def __neg__(a):return K([-x for x in a.c])
    def __sub__(a,b):return a+-K(b)
    def __rsub__(a,b):return K(b)+-a
    def __mul__(a,b):
        b=K(b);out=[F(0)]*8
        for i,x in enumerate(a.c):
            for j,y in enumerate(b.c):
                m=1
                for bit,p in enumerate((2,3,5)):
                    if (i&j)&(1<<bit):m*=p
                out[i^j]+=x*y*m
        return K(out)
    __rmul__=__mul__
    def __truediv__(a,b):return K([x/F(b) for x in a.c])
    def __eq__(a,b):return a.c==K(b).c
    def __repr__(a):return repr(a.c)

def radical(mask):
    c=[0]*8;c[mask]=1;return K(c)
r2,r3,r5=map(radical,(1,2,4))
def mat(rows):return tuple(tuple(K(v) for v in row) for row in rows)
def add(a,b):return tuple(tuple(x+y for x,y in zip(ar,br)) for ar,br in zip(a,b))
def neg(a):return tuple(tuple(-x for x in ar) for ar in a)
def sub(a,b):return add(a,neg(b))
def mul(a,b):return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def scale(c,a):return tuple(tuple(K(c)*x for x in ar) for ar in a)
def star(a):return tuple(tuple(a[j][i] for j in range(2)) for i in range(2))
def conj(u,a):return mul(mul(u,a),star(u))
def diag(a):return mat([[a[0][0],0],[0,a[1][1]]])
I=mat([[1,0],[0,1]]);Z=mat([[0,0],[0,0]]);q=mat([[1,0],[0,0]])
checks=[]
def check(name,condition):
    if not condition:raise AssertionError(name)
    checks.append(name)

for mask in range(8):
    p=1
    for bit,v in enumerate((2,3,5)):
        if mask&(1<<bit):p*=v
    check('field_square_'+str(mask),radical(mask)*radical(mask)==p)

# V(s) for s=log 2, and V(2s), from the half-angle formula.
R1=mat([[r3/2,F(-1,2)],[F(1,2),r3/2]])
R2=mat([[r2*r5/4,-r2*r3/4],[r2*r3/4,r2*r5/4]])
U=mul(star(R1),R2)
for name,u in [('V(s)',R1),('V(2s)',R2),('u_s(s)',U)]:
    check(name+'_unitary_left',mul(star(u),u)==I)
    check(name+'_unitary_right',mul(u,star(u))==I)
check('cocycle_at_0_s_s',mul(R1,U)==R2)
Q0=conj(R1,q);Qs=conj(U,q)
check('Q0_exact',Q0==mat([[F(3,4),r3/4],[r3/4,F(1,4)]]))
for name,a in [('q',q),('Q0',Q0),('Qs',Qs)]:
    check(name+'_projection',mul(a,a)==a)
    check(name+'_selfadjoint',star(a)==a)

A0=sub(mul(mul(q,Q0),q),scale(F(3,4),q))
As=sub(mul(mul(q,Qs),q),scale(F(3,4),q))
d=(3*r5-3)/16
check('witness_at_zero_is_zero',A0==Z)
check('witness_at_s_exact',As==scale(d,q))
check('radical_positive_lower_bound',F(2)**2<5 and F(2)>1)
check('d_nonzero',d!=0)
shifted=conj(R1,As)
check('translated_witness_exact',shifted==scale(d,Q0))
check('translated_witness_nonzero',shifted!=Z)
check('expectation_of_translated_witness',diag(shifted)==scale(d,mat([[F(3,4),0],[0,F(1,4)]])))
check('expectation_of_translated_square',diag(mul(shifted,shifted))==scale(d*d,mat([[F(3,4),0],[0,F(1,4)]])))
check('original_expectation_zero',diag(A0)==Z)
check('strongness_equation_fails',diag(shifted)!=Z)

# Cyclicity / faithfulness of the evaluated M2 left action.
e12=mat([[0,1],[0,0]]);e21=star(e12)
check('evaluated_generators_produce_e12',scale(4*r3/3,mul(mul(q,Q0),sub(I,q)))==e12)
check('matrix_units_product_11',mul(e12,e21)==q)
check('matrix_units_product_22',mul(e21,e12)==sub(I,q))
check('cyclic_vector_has_unit_inner_product',diag(mul(star(I),I))==I)

# P(r)=J+rK, where r=exp(-t). Exact controls of the semigroup formula.
J=mat([[F(1,2),F(1,2)],[F(1,2),F(1,2)]])
H=mat([[F(1,2),F(-1,2)],[F(-1,2),F(1,2)]])
check('J_idempotent',mul(J,J)==J)
check('H_idempotent',mul(H,H)==H)
check('JH_zero',mul(J,H)==Z)
check('HJ_zero',mul(H,J)==Z)
check('J_plus_H_identity',add(J,H)==I)
def P(r):return add(J,scale(r,H))
for r in (F(0),F(1,7),F(1,3),F(1,2),F(3,4),F(1)):
    for v in (F(0),F(1,9),F(2,5),F(1)):
        check('semigroup_'+str(r)+'_'+str(v),mul(P(r),P(v))==P(r*v))
    check('row_sums_'+str(r),all(sum(row)==1 for row in P(r)))
for j,b in enumerate([q,sub(I,q),I,mat([[2,0],[0,-3]])]):
    expected=mat([[F(3,4)*b[0][0]+F(1,4)*b[1][1],0],[0,F(1,4)*b[0][0]+F(3,4)*b[1][1]]])
    check('compressed_diagonal_basis_'+str(j),diag(conj(R1,b))==expected)

# A cocycle chosen with a linear angle would give x-independent translates.
# Its putative q q_s q - coefficient*q witness is identically zero.
check('linear_angle_negative_control',sub(mul(mul(q,Q0),q),scale(F(3,4),q))==Z)
result={
  'result':'PASS',
  'exact_assertions':len(checks),
  'arithmetic':'fractions.Fraction in Q(sqrt(2),sqrt(3),sqrt(5)); no floating point',
  'witness_time':'s=log(2)',
  'witness_coefficient':'(3*sqrt(5)-3)/16',
  'translated_compression':'((3*sqrt(5)-3)/16)*diag(3/4,1/4)',
  'checked':checks,
  'limits':['Finite exact algebra does not replace the all-time analytic proof.','No novelty or source-status decision is made by this program.']
}
print(json.dumps(result,indent=2))
