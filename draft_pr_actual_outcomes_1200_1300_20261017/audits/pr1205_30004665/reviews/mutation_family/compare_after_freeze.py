#!/usr/bin/env python3
"""Compare submitted data ONLY AFTER independent reconstruction was frozen."""
import json, hashlib, re
from pathlib import Path
import sympy as s
import reconstruct as r

p=r.HERE/'independent_output.json'
digest=hashlib.sha256(p.read_bytes()).hexdigest()
assert digest in (r.HERE/'INDEPENDENT_FREEZE.txt').read_text()
data=json.loads(p.read_text())
proof=r.HERE.parents[1]/'submitted'/'PROOF.md'
text=proof.read_text()
rows=[];witnesses=[]
for match in re.finditer(r'^\|([0-9]+)\|([012]{12})\|\(([^)]+)\)\|$',text,re.M):
    j,a,z=match.groups();assert int(j)==len(rows)+1
    rows.append(list(map(int,a)));witnesses.append(list(map(int,z.split(','))))
assert len(rows)==22
independent={tuple(-e for e in t['exponents']) for a in data['summands'].values() for t in a['support']}
assert set(map(tuple,rows))==independent
products=[[sum(a*b for a,b in zip(row,z)) for z in witnesses] for row in rows]
assert all(products[i][j]==-1 if i==j else products[i][j]>=0 for i in range(22) for j in range(22))

# Transcription of the submitted displayed factored formula, not used to build
# independent_output.json or to discover any seed/route/support.
y=s.symbols('y1:13');Y={i+1:v for i,v in enumerate(y)}
A=1+Y[3]+Y[2]*Y[3];B=Y[2]*Y[3]*Y[4]*Y[5]
F7=1+Y[6]+Y[6]*Y[8]*A+Y[6]*Y[8]*Y[10]*((1+Y[5])*A+B*(1+Y[6]+Y[1]*Y[6]))
F9=1+Y[8]+Y[8]*Y[10]*(1+Y[5]+Y[4]*Y[5])
W=Y[7]*F7+Y[9]*F9+Y[11]*(1+Y[10])+Y[12]
terms=s.Poly(s.expand(W),*y).terms()
assert {e for e,c in terms}==independent and all(c==1 for e,c in terms)

# Independent chamber-ansatz exponent transformation, KS2022 Definition9.
n=12;w=r.WORD
C=[[2 if a==b else (-1 if r.adjacent(a,b) else 0) for b in range(1,5)] for a in range(1,5)]
K=s.zeros(n)
for k in range(n):
    kp=next((l for l in range(k+1,n) if w[l]==w[k]),n)
    K[k,k]=1
    if kp<n:K[k,kp]=1
    for l in range(k+1,kp):K[k,l]=C[w[k]-1][w[l]-1]
assert abs(K.det())==1
transformed=[list(s.Matrix(1,n,a)*K) for a in rows]
assert max(abs(e) for a in transformed for e in a)==1

report={'independent_output_sha256':digest,'submitted_proof_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),
        'candidate_formula_equal':'passed','candidate_table_equals_independent_support':'passed',
        'all_484_separation_products':'passed','diagonal_products':[-1]*22,
        'minimum_off_diagonal_product':min(products[i][j] for i in range(22) for j in range(22) if i!=j),
        'products':products,'chamber_ansatz_matrix':[[int(K[i,j]) for j in range(n)] for i in range(n)],
        'chamber_ansatz_determinant':int(K.det()),'transformed_rows':[[int(e) for e in a] for a in transformed],
        'max_abs_transformed_exponent':1}
(r.HERE/'postfreeze_comparison.json').write_text(json.dumps(report,indent=2)+'\n')
print({k:v for k,v in report.items() if k not in ('products','chamber_ansatz_matrix','transformed_rows')})
