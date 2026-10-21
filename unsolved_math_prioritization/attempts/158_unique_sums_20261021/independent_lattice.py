import json, itertools
from pathlib import Path
from sympy import Matrix
from sympy.matrices.normalforms import hermite_normal_form
b=Path(__file__).parent
out=[]
for item in json.loads((b/'exact_results.json').read_text()):
 p=item['p']; A=item['witness'];n=len(A)
 pairs=list(itertools.combinations_with_replacement(range(n),2))
 # All pairwise differences, not a star basis; eliminate FIRST column.
 columns=[]
 for u,v in itertools.combinations(pairs,2):
  if sum(A[i] for i in u)%p!=sum(A[i] for i in v)%p:continue
  col=[u.count(i)-v.count(i) for i in range(1,n)]
  columns.append(col)
 H=hermite_normal_form(Matrix(columns).T)
 determinant=abs(int(H.det()))
 assert H.shape==(n-1,n-1) and determinant==p
 out.append(dict(p=p,all_difference_columns=len(columns),hnf_shape=list(H.shape),hnf_determinant=determinant,implied_smith_diagonal=[1]*(n-2)+[p]))
C=(0,1,4);p=13
quad={x:[list(q) for q in itertools.combinations_with_replacement(C,4) if sum(q)%p==4*x%p and q!=(x,)*4] for x in C}
B=sorted({(x+y)%p for x in C for y in C})
reps={s:[list(q) for q in itertools.combinations_with_replacement(B,2) if sum(q)%p==s] for s in range(p)}
unique={s:q for s,q in reps.items() if len(q)==1}
assert all(quad.values()) and unique
result=dict(lattices=out,counterexample=dict(p=p,C=C,nontrivial_quads=quad,B=B,unique_sum_pairs=unique))
(b/'independent_lattice_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
