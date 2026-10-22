import json,itertools
from pathlib import Path
from sympy import Matrix,ZZ
from sympy.matrices.normalforms import smith_normal_form
base=Path(__file__).parent
out=[]
for item in json.loads((base/'exact_results.json').read_text()):
 p=item['p'];A=item['witness'];n=len(A);groups={}
 for i in range(n):
  for j in range(i,n):groups.setdefault((A[i]+A[j])%p,[]).append((i,j))
 rows=[]
 for pairs in groups.values():
  i,j=pairs[0]
  for k,l in pairs[1:]:
   row=[0]*n
   for t,s in [(i,1),(j,1),(k,-1),(l,-1)]:row[t]+=s
   rows.append(row[:-1])
 D=smith_normal_form(Matrix(rows),domain=ZZ)
 diag=[abs(int(D[i,i])) for i in range(min(D.shape))]
 out.append({'p':p,'rows':len(rows),'columns':n-1,'smith_diagonal':diag})
print(json.dumps(out,indent=2))
(base/'lattice_results.json').write_text(json.dumps(out,indent=2)+'\n')
