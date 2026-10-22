#!/usr/bin/env python3
"""Publisher KS2022 section 7 regression; no candidate artifact is used."""
import hashlib,json
import sympy as s
import verify_blind as v
word=(2,1,3,4,2,1,3,4,2,1,3,4)
sequence=[6,3,5,4,3,1,2,7,6,8]
b,f,_=v.seed(word); history=[]; z=s.symbols('X1:13')
for one in sequence:
 k=one-1; history.append((b,k)); b=v.mutate(b,k,f)
assert all(b[8][j]<=0 for j in range(12) if j not in f)
p=1/z[8]
for b,k in reversed(history):
 r={z[i]:(1/z[k] if i==k else z[i]*(1+z[k]**(-s.sign(b[i][k])))**(-b[i][k])) for i in range(12)}
 p=s.cancel(p.xreplace(r))
terms=v.laurent_terms(s.expand(p),z)
assert len(terms)==27 and sum(t['coefficient']==2 for t in terms)==1
assert all(t['exponents'][8]==-1 for t in terms)
assert next(t['exponents'] for t in terms if t['coefficient']==2)==[0,0,0,0,-1,-1,-1,-1,-1,0,0,0]
data={'source':'KS2022 publisher section 7, pp.1050-1051','word':word,'sequence':sequence,'support':terms}
raw=(json.dumps(data,indent=2,sort_keys=True)+'\n').encode(); path=v.BASE/'source_regression.json'
if path.exists(): assert path.read_bytes()==raw
else: path.write_bytes(raw)
print(json.dumps({'terms':27,'unique_coefficient_2':True,'sha256':hashlib.sha256(raw).hexdigest()}))
