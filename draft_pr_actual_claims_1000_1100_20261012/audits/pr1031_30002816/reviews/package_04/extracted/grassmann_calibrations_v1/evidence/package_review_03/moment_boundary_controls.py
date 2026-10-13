from pathlib import Path
from fractions import Fraction as F
import json,datetime
R=Path(__file__).resolve().parent
req=lambda c,m: None if c else (_ for _ in ()).throw(RuntimeError(m))
def rank(a):
 a=[list(r) for r in a];n=0
 for j in range(len(a[0])):
  k=next((i for i in range(n,len(a)) if a[i][j]),None)
  if k is None:continue
  a[n],a[k]=a[k],a[n];v=a[n][j];a[n]=[x/v for x in a[n]]
  for i in range(len(a)):
   if i!=n:
    v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[n])]
  n+=1
 return n
X=[(F(1),F(0)),(F(3,5),F(4,5)),(F(3,5),F(-4,5)),(F(-1),F(0)),(F(-3,5),F(4,5)),(F(-3,5),F(-4,5))]
evalrows=[[F(1),x,y,x*x,x*y,y*y] for x,y in X]
req(rank(evalrows)==5,'degree2 evaluation rank');req(all(1-x*x-y*y==0 for x,y in X),'sphere relation')
# Thus full J_2 is exactly the sphere relation on this six-point variety.
# Its first moment projection is the disk (construct covariance), unlike its polyhedral hull.
for x,y in X:
 h1=1-F(25,16)*y*y;h2=F(25,32)*y*y-F(5,8)*y
 req(F(4,5)-y==F(4,5)*h1*h1+F(8,5)*h2*h2,'higher-degree SOS')
c=(F(1,100),F(1));delta=max(c[0]*x+c[1]*y for x,y in X);gap=1-delta;req(gap==F(97,500) and gap>0,'strict rational perturbation')
# Missing full-ideal linear relation for X={(1,0),(-1,0)} permits false sphere moment.
M=[[1,0,1],[0,0,0],[1,0,1]];req(sum(M[i][i] for i in range(3))==2,'trace2');req(M[0][2]==1,'omitted p2=0');req(-M[0][2]==-1,'violated supporting function')
# Standard nonclosed shadow boundary, prevented by compact trace slice in the target.
seq=[]
for k in (1,2,10,100):
 x,y=F(1,k),F(k);req(x>0 and y>0 and x*y-1==0,'nonclosed PSD sequence');seq.append({'x':str(x),'y':str(y),'determinant':'0','trace':str(x+y)})
req(F(0)*F(1)-1<0,'excluded x=0')
d={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'arithmetic':'fractions.Fraction; no candidate implementation imported','six_point_full_J2_evaluation_rank':5,'polynomial_space_dimension':6,'full_J2_dimension':1,'full_J2_basis':'1-p1^2-p2^2','six_point_support_gap_at_disk_point':'1/5','higher_root_degree_SOS_identity_on_all_six_points':True,'rational_perturbation_coefficients':['1/100','1'],'perturbed_support_value':str(delta),'perturbed_strict_gap':str(gap),'missing_full_ideal_relation':'p2=0 on the two-point axis variety','sphere_only_rank_one_matrix':M,'invalid_support_value':-1,'nonclosed_shadow_sequence':seq,'target_witness_or_explicit_calibration_constructed':False,'boundary':'Small falsification controls validate hypotheses and distinguish degree truncation, full ideal, compactness and rational strictness. They are not a C(4,12) witness.'}
(R/'MOMENT_BOUNDARY_CONTROLS.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2))
