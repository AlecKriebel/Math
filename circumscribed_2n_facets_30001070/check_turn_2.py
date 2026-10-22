import sympy as S
from itertools import combinations
import json
n=3
Q=S.ones(n)*S.Rational(2,3)-S.eye(n)
U=S.eye(n).col_join(-Q)
assert Q.T*Q==S.eye(n) and Q*S.ones(n,1)==S.ones(n,1)
assert U.T*S.ones(2*n,1)==S.zeros(n,1) and U.T*U==2*S.eye(n)
vertices=set()
for ids in combinations(range(2*n),n):
 A=U[list(ids),:]
 if A.det()==0:continue
 x=A.inv()*S.ones(n,1)
 if all(v<=1 for v in U*x):vertices.add(tuple(x))
assert (-2,1,1) in vertices
assert not any(U[i,:]==-U[j,:] for i in range(2*n) for j in range(i))
norms=sorted(set(str(sum(x*x for x in v)) for v in vertices))
assert min(sum(x*x for x in v) for v in vertices)>=n
print(json.dumps({'Q':str(Q),'normal_count':2*n,'centered':True,'frame_operator':'2I','antipodal_pairs':0,'vertices':[list(map(str,v)) for v in sorted(vertices)],'squared_norm_values':norms,'all_exact_checks_passed':True},indent=2))
