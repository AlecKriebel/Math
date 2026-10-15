"""Finite controls for source-transfer obstructions; not evidence for asymptotic theorem."""
from fractions import Fraction as F
from math import comb,sqrt,log,lgamma,exp
from itertools import combinations
from pathlib import Path
import json,datetime
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'finite mapping and exponent controls only'}
# Exact arithmetic in a highly nonuniform deterministic test environment.
N=12
values=[F(1,10000),F(1,5),F(37,100),F(1,2),F(4,5),F(9999,10000)]
def env(s,x):return values[((s+3)*(x+17)+s*s)%len(values)]
mu={0:F(1)};directed={(0,0):F(1)}
for s in range(N):
 new={};newd={}
 for x,mass in mu.items():
  for y,pr in [(x+1,env(s,x)),(x-1,1-env(s,x))]:new[y]=new.get(y,F(0))+mass*pr
 for (a,b),mass in directed.items():
  x=a-b
  for y,pr in [((a+1,b),env(s,x)),((a,b+1),1-env(s,x))]:newd[y]=newd.get(y,F(0))+mass*pr
 mu,directed=new,newd
assert all(mu[x]==directed[((N+x)//2,(N-x)//2)] for x in mu)
assert sum(mu.values())==1
out['exact_shear']={'N':N,'laws_equal':True,'reachable_endpoints':len(mu),'transition_values':[str(x) for x in values],'max_exact_error':'0'}
# BBDS one-site backbone kernel: uniform on a nonempty subset of three successors.
kernels=[]
for k in (1,2,3):
 for S in combinations((-1,0,1),k):kernels.append({j:(F(1,k) if j in S else F(0)) for j in (-1,0,1)})
compatible=[]
for ker in kernels:
 if ker[0]==0 and ker[-1]>0 and ker[1]>0:compatible.append(str(ker[1]))
assert compatible==['1/2']
out['bbds_kernel_control']={'nonempty_uniform_successor_kernels':len(kernels),'strictly_positive_no_hold_scalar_probabilities':compatible,'generic_values_1_5_and_37_100_match':False}
# Adjacent-site derivative cannot be imported unchanged for the parity-two law.
rows=[]
for n in (100,400,1600):
 q=.37
 ps={2*j-n:exp(lgamma(n+1)-lgamma(j+1)-lgamma(n-j+1)+j*log(q)+(n-j)*log(1-q)) for j in range(n+1)}
 adj=max(abs(ps.get(k+1,0)-ps.get(k,0)) for k in range(-n-1,n+1))
 same=max(abs(ps.get(k+2,0)-ps.get(k,0)) for k in range(-n-2,n+1))
 rows.append({'n':n,'sqrt_n_adjacent_gradient':sqrt(n)*adj,'n_same_parity_gradient':n*same})
out['parity_gradient_control']=rows
# Quantitative TURN2 and adapted-bootstrap margins.
gamma=F(5,16);rho=F(7,8);beta=F(9,32);eta=F(1,64);b=F(1,128)
margins={'nu_exponent':beta-eta-2*b,'sign_entropy_exponent':F(1,2)-gamma,'nu_minus_entropy':beta-eta-2*b-(F(1,2)-gamma),'boundary_concentration_exponent':2*beta-F(1,2)-eta-2*b,'boundary_mean_exponent':gamma-beta,'old_cell_smoothing_exponent':F(1,2)-gamma/rho,'rho_minus_2gamma':rho-2*gamma}
assert all(v>0 for v in margins.values())
out['rational_exponent_margins']={k:str(v) for k,v in margins.items()}
# Union bound at tiny terminal scales cannot establish N-superpolynomial failure.
rows=[]
for logN in (100,1000,10000,100000):
 M=log(logN);theta=.3;nmin=M**(1/theta)
 rows.append({'log_N':logN,'M_loglogN':M,'neg_log_terminal_bad_prob_c_eq_1':log(nmin)**2,'effective_N_power':log(nmin)**2/logN})
out['slow_scale_union_bound_trap']=rows
Path('FINITE_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
