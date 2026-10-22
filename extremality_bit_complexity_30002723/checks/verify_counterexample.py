from fractions import Fraction as F
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).parent))
from find_grid_counterexample import rank_at
v=list(map(F,['0','1','1/3','1/2','2/3']))
rank,N,A,w=rank_at(v,3)
h=list(map(F,['0']*8+['-1','0','1']+['0']*4))
sl=[]
for i in range(N):
 for j in range(N):
  a=w[i]+w[j]-w[(i+j)%N];b=h[i]+h[j]-h[(i+j)%N]
  assert a>=0
  if a==0:assert b==0
  if b:sl.append(a/abs(b))
eps=min(sl)
assert eps>0
for sign in [-1,1]:
 z=[w[i]+sign*eps*h[i] for i in range(N)]
 assert z[0]==0 and z[3]==1
 assert all(0<=x<=1 for x in z)
 assert all(z[i]+z[(3-i)%N]==1 for i in range(N))
 assert all(z[i]+z[j]>=z[(i+j)%N] for i in range(N) for j in range(N))
out={'q':5,'f':'1/5','sparse_breakpoints':['0','1/5','2/5','4/5','1'],'sparse_values':['0','1','1/3','2/3','0'],'coarse_rank':rank_at(v)[0],'refined_N':N,'refined_rank':rank,'epsilon':str(eps),'h_grid':[str(x) for x in h],'all_checks':'PASS'}
print(json.dumps(out,indent=2))
Path(__file__).with_name('counterexample_verified.json').write_text(json.dumps(out,indent=2)+'\n')
