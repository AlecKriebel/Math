import sympy as S
from itertools import combinations
import json
n=4
V=[S.zeros(n,1)]+[S.eye(n)[:,i] for i in range(n)]
for i in range(3):V.append(S.Matrix([S.Rational(-1,100) if j==i else S.Rational(1,4) for j in range(n)]))
w=[S.Rational(1,5)]*5+[S.Integer(1)]*3
facets=[]
for F in combinations(range(8),n):
 A=S.Matrix([[*V[i],1] for i in F]);null=A.nullspace()
 if len(null)!=1:continue
 z=null[0]; vals=[(S.Matrix([*v,1]).T*z)[0] for v in V]
 if all(x>=0 for x in vals) or all(x<=0 for x in vals):
  ids=tuple(i for i,x in enumerate(vals) if x==0)
  if ids not in facets:facets.append(ids)
assert all(sum(i>=5 for i in F)<=1 for F in facets)
maxmass=max(sum(w[i] for i in F) for F in facets)
assert maxmass==S.Rational(8,5)<sum(w)/2
print(json.dumps({'dimension':4,'vertex_count':8,'facet_count':len(facets),'facets':facets,'total_weight':str(sum(w)),'maximum_facet_weight':str(maxmass),'sphere_or_isotropy_claimed':False,'combinatorial_shortcut_refuted':True},indent=2))
