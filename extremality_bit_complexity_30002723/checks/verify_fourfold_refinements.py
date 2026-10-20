"""Validate structured versus BHK full active matrices on genuine 4q grids."""
from verify_discontinuous_reduction import *

def refine(v,m=4):
 q=len(v)//3;N=m*q;w=[F(0)]*(3*N)
 for k in range(N):
  i,a=divmod(k,m)
  if a==0:
   for st in range(3):w[st*N+k]=v[st*q+i]
  else:
   val=((m-a)*v[q+i]+a*v[2*q+(i+1)%q])/m
   for st in range(3):w[st*N+k]=val
 return w

def rank(A):
 A=sorted(set(tuple(a) for a in A))
 return int(Matrix(A).to_DM().rank())
def run():
 old=json.loads(Path(__file__).with_name('discontinuous_reduction_results.json').read_text())['cases']
 cv=list(map(F,['0','1','1/3','1/2','2/3']))
 cases=[('continuous_coarse_rigid_counterexample',5,1,cv*3,[0,1,2,4,5]),('two_sided_constant_half',2,1,[F(0),F(1),F(1,2),F(1,2),F(1,2),F(1,2)],[0,1,2])]
 for q,t in [(5,0),(9,1),(9,2)]:
  c=next(r for r in old if r['q']==q and r['trial']==t)
  cases.append((f'sparse_LP_q{q}_trial{t}',q,c['f_index'],list(map(F,c['values'])),c['breakpoint_indices']))
 out=[]
 for name,q,f,v,ints in cases:
  N=4*q;w=refine(v);B=[F(i,q) for i in ints]
  A=full_tight(N,4*f,w);C,stats=structured(N,4*f,w,B)
  ra=rank(A);rc=rank(C);ru=rank(A+C)
  assert ra==rc==ru,(name,ra,rc,ru)
  r={'name':name,'q':q,'refined_N':N,'variable_count':3*N,'rank':ra,'structured_rank':rc,'joint_rank':ru,'nullity':3*N-ra,'two_sided_discontinuous_at_0':bool(v[q]>0 and v[2*q]>0),'stats':stats}
  out.append(r);print(json.dumps(r),flush=True)
 final={'all_checks':'PASS','case_count':len(out),'checks':out}
 Path(__file__).with_name('fourfold_refinement_results.json').write_text(json.dumps(final,indent=2)+'\n')
if __name__=='__main__':run()
