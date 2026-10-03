#!/usr/bin/env python3
"""Exact independent character/decomposition checks. Source row is identified
with Sym^n of the binary icosahedral natural character in CHECK_REPORT.md.
Finite algebra below checks consistency, not existence of that representation.
"""
from pathlib import Path
import json
import sympy as s
q=s.sqrt(5); a=(q-1)/2; b=(-q-1)/2
names=['1','z','3','4','5a','5b','6','-5a','-5b']
sizes=[1,1,20,30,12,12,20,12,12]
orders=[1,2,3,4,5,5,6,10,10]
square=[0,0,2,1,5,4,2,5,4]
t=s.Matrix([[2,-2,-1,0,a,b,1,-a,-b]])
tb=t.applyfunc(lambda x:x.subs(q,-q))
poly=lambda f:t.applyfunc(lambda x:s.expand(f(x)))
chars={
 'one':s.ones(1,9),
 'two_a':t,
 'two_b':tb,
 'three_a':poly(lambda x:x*x-1),
 'three_b':tb.applyfunc(lambda x:s.expand(x*x-1)),
 'four_plus':s.Matrix([[4,4,1,0,-1,-1,1,-1,-1]]),
 'four_minus':poly(lambda x:x**3-2*x),
 'five':poly(lambda x:x**4-3*x*x+1),
 'six':poly(lambda x:x**5-4*x**3+3*x),
}
X=s.Matrix.vstack(*chars.values()); W=s.diag(*sizes)
assert (X*W*X.T).applyfunc(s.simplify)==120*s.eye(9)
assert sum(int(X[i,0])**2 for i in range(9))==120
fs={name:s.simplify(sum(sizes[j]*row[square[j]] for j in range(9))/120) for name,row in chars.items()}
assert list(fs.values())==[1,-1,-1,1,1,1,-1,1,-1]
odd=[0,2,4,5]
B=s.Matrix([[1,1,1,1],[2,-1,a,b],[2,-1,b,a],[4,1,-1,-1]])
D=(X[:,odd]*B.inv()).applyfunc(s.simplify)
assert all(x.is_integer and x>=0 for x in D)
C=D.T*D
assert C==s.Matrix([[8,4,4,0],[4,4,2,0],[4,2,4,0],[0,0,0,2]])
# Rows of ordinary PIM characters are columns of D by Brauer reciprocity.
P=D.T*X
assert [P[i,0] for i in range(4)]==[24,16,16,8]
assert all(P[i,j]==0 for i in range(4) for j,o in enumerate(orders) if o%2==0)
assert P[3,:]==chars['four_plus']+chars['four_minus']
# F2 simples: trivial, U(two_a+two_b), S(four_plus).
F2P=[P[0,:],P[1,:]+P[2,:],P[3,:]]
F2vectors=[]
for row in F2P:
 d=(row[:,odd]*B.inv()).applyfunc(s.simplify)
 assert d[1]==d[2]
 F2vectors.append([int(d[0]),int(d[1]),int(d[3])])
assert F2vectors==[[8,4,0],[8,6,0],[0,0,2]]
V1=s.Matrix([[1,0,0]]);V4=s.Matrix([[0,0,1]]);V5=s.Matrix([[1,1,0]])
assert list(4*V1+4*V5)==F2vectors[0]
assert list(2*V1+6*V5)==F2vectors[1]
assert list(2*V4)==F2vectors[2]
# Counts in the regular F2 group algebra: dim simple/end(simple)=1,2,4.
assert 1*24+2*32+4*8==120
# Nontrivial quaternionic multiplicities in F2-projective ordinary characters.
fused_coeffs=[D[:,0],D[:,1]+D[:,2],D[:,3]]
assert [list(c)[6] for c in fused_coeffs]==[0,0,1]
assert [list(c)[1] for c in fused_coeffs]==[0,1,0]
# Hilbert symbol at 2 for odd units a,b: (-1)^(((a-1)/2)((b-1)/2)).
def hs2(a,b):
 assert a%2 and b%2
 return (-1)**(((a-1)//2)*((b-1)//2))
assert hs2(-1,-3)==1 and hs2(-1,-1)==-1
out={
 'class_labels':names,'class_sizes':sizes,'class_orders':orders,'square_class_indices':square,
 'ordinary_labels':list(chars),'ordinary_character_rows':[[str(x) for x in row] for row in X.tolist()],
 'FS_indicators':{k:int(v) for k,v in fs.items()},
 'decomposition_matrix_F4':[[int(x) for x in row] for row in D.tolist()],
 'Cartan_F4':[[int(x) for x in row] for row in C.tolist()],
 'F2_PIM_composition_vectors':F2vectors,
 'F2_PIM_ordinary_multiplicities':[[int(x) for x in c] for c in fused_coeffs],
 'F2_PIM_dimensions':[24,32,8],
 'positive_witnesses':['4 V1 + 4 V5','2 V1 + 6 V5','2 V4'],
 'eight_dim_PIM_character': 'four_plus + four_minus',
 'four_minus_FS_indicator':-1,
 'four_minus_global_Schur_index':2,'four_minus_Q2_Schur_index':1,
 'check':'PASS; theorem-level source and lifting arguments in CHECK_REPORT.md'
}
Path(__file__).with_name('character_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
