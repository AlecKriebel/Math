import datetime,json,pathlib,sys
sys.dont_write_bytecode=True
from fractions import Fraction as F
O=pathlib.Path(__file__).resolve().parent
# Independent exact elimination and six rational points, distinct from archived examples.
def rank(a):
 a=[list(row)for row in a];r=0
 for c in range(len(a[0])):
  k=next((k for k in range(r,len(a)) if a[k][c]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];s=a[r][c];a[r]=[v/s for v in a[r]]
  for k in range(len(a)):
   if k!=r:
    q=a[k][c];a[k]=[v-q*w for v,w in zip(a[k],a[r])]
  r+=1
 return r
points=[(F(1),F(0)),(F(-1),F(0))]+[(s*F(5,13),t*F(12,13))for s,t in ((1,1),(-1,-1),(1,-1),(-1,1))]
evaluation=[[1,x,y,x*x,x*y,y*y]for x,y in points]
assert rank(evaluation)==5 and all(x*x+y*y==1 for x,y in points)
# Unique quadratic relation is sphere; hence rank-one moments at (0,1) satisfy full degree-two ideal.
M=[[F(1),F(0),F(1)],[F(0),F(0),F(0)],[F(1),F(0),F(1)]]
assert sum(M[i][i]for i in range(3))==2
assert all(M[i][i]>=0 for i in range(3))and all(M[i][i]*M[j][j]-M[i][j]**2>=0 for i in range(3)for j in range(i+1,3))
assert rank(M)==1
support=max(y for x,y in points);gap=F(1)-support;assert support==F(12,13) and gap==F(1,13)
# On a different sphere subset, the full ideal p2=0 prevents this same extraneous moment.
assert all(y==0 for x,y in points[:2]) and M[0][2]!=0
# Explicit nonclosed projection: det[[x,1],[1,y]]=0 at x=1/k,y=k, but x=0 cannot be PSD.
for k in (1,3,17,1000):assert F(1,k)*F(k)==1
# Signed rational positive case; sign in optional completion converse checked on all coordinates.
a=[F(1,2),F(1,2)];B=[[-F(1,2),F(1,2)],[-F(1,2),-F(1,2)]];phi=[F(1),F(0)]
assert sum(v*v for v in a)==F(1,2)
assert [sum(a[k]*B[k][j]for k in range(2))for j in range(2)]==[-v/2 for v in phi]
for p in [(F(1),F(0)),(F(-1),F(0)),(F(3,5),F(4,5)),(F(-3,5),F(-4,5))]:
 bp=[sum(v*w for v,w in zip(row,p))for row in B];rhs=sum((v+w)**2 for v,w in zip(a,bp));assert rhs==1-p[0]
 # 2||projection onto a-perp||² = 1-phi².
 dot=sum(v*w for v,w in zip(a,bp));projection=[v-dot*w/F(1,2)for v,w in zip(bp,a)];assert 2*sum(v*v for v in projection)==1-p[0]**2
obj={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','controls':[{'name':'six_rational_circle_points','degree2_evaluation_rank':5,'full_J2':'span(1-x²-y²)','finite_polyhedral_lift_exists':True,'affine_support_SOS_fails':True,'support':'12/13','relaxation_violation_gap':'1/13','target_Grassmann_witness':False},{'name':'full_ideal_relation_material','sphere_only_extraneous_first_moment':'p2=1','full_ideal_requires':'p2=0'},{'name':'projection_closure_without_trace_bound','feasible_sequence':'(1/k,k)','excluded_limit_x':'0'},{'name':'optional_converse_negative_sign_and_projection','B_transpose_a':'-phi/2','a_norm_squared':'1/2','all_four_exact_signed_point_checks':True}],'theorem_scope':'These examples falsify possible generic closure/ideal/converse mistakes. They do not construct the existential Grassmann functional.'}
(O/'MOMENT_BOUNDARY_CONTROLS.json').write_text(json.dumps(obj,indent=2)+'\n');print(json.dumps(obj,indent=2))
