from itertools import combinations,product
from fractions import Fraction as F
from pathlib import Path
import json,hashlib,random
checks=0
def ck(x):
 global checks
 assert x;checks+=1
D=[[0,1050,1998,1954,1006,1934,1966,1063],[1050,0,1052,1939,1962,1046,1975,1928],[1998,1052,0,1065,1918,1937,1018,1997],[1954,1939,1065,0,1013,1980,1933,1069],[1006,1962,1918,1013,0,1091,1978,1919],[1934,1046,1937,1980,1091,0,1040,1913],[1966,1975,1018,1933,1978,1040,0,1094],[1063,1928,1997,1069,1919,1913,1094,0]]
for i,j,k in product(range(8),repeat=3):ck(D[i][j]<=D[i][k]+D[k][j])
sols=[]
for centers in combinations(range(8),2):
 for labels in product(range(2),repeat=8):
  assign=tuple(centers[a] for a in labels);cost=sum(D[assign[j]][j] for j in range(8));sols.append((cost,centers,assign));ck(cost>=7099)
sols.sort();ck(sols[0]==(7099,(2,4),(4,2,2,4,4,4,2,4)));ck(sols[1][0]==7110);ck(F(1001,1000)*7099<7110)
E={tuple(sorted((i,(i+1)%8))) for i in range(8)}|{(i,i+4) for i in range(4)}
y=[F(1,4)]*8;x=[[F(1,4) if i==j or tuple(sorted((i,j))) in E else F(0) for j in range(8)] for i in range(8)]
ck(sum(y)==2)
for j in range(8):ck(sum(x[i][j] for i in range(8))==1)
for i,j in product(range(8),repeat=2):ck(0<=x[i][j]<=y[i]<=1)
fcost=sum(D[i][j]*x[i][j] for i,j in product(range(8),repeat=2));ck(fcost==F(12607,2));ck(fcost<7099)
for k,expected in [(1,10887),(2,7099),(3,5171)]:ck(min(sum(min(D[i][j] for j in c) for i in range(8)) for c in combinations(range(8),k))==expected)
# A separate positive control for strict dual margins and robustness.
points=[0,1,2,100,101,102];C=[1,1,1,4,4,4];S={1,4};base=[[F(abs(i-j)) for j in points] for i in points];t=F(3)
def cert(d):
 alpha=[d[C[j]][j]+1 for j in range(6)];beta=[[max(alpha[j]-d[i][j],0) for j in range(6)] for i in range(6)]
 for c in S:ck(sum(beta[c])==t)
 gamma=min(d[c][j]-alpha[j] for c in S for j in range(6) if c!=C[j]);eta=min(t-sum(beta[i]) for i in range(6) if i not in S)
 ck(gamma>0);ck(eta>0);ck(sum(alpha)-2*t==sum(d[C[j]][j] for j in range(6)))
 return gamma,eta
ck(cert(base)==(F(97),F(1)))
rng=random.Random(2800904)
for _ in range(100):
 pert=[[base[i][j]+F(rng.randrange(-1,2),100) for j in range(6)] for i in range(6)]
 cert(pert)
here=Path(__file__).resolve().parent
r={'status':'PASS','exact_assertions':checks,'integer_center_assignment_pairs':len(sols),'integer_optimum':7099,'next_solution_cost':7110,'fractional_feasible_cost':str(fcost),'perturbation_resilience_factor':'1001/1000','positive_control_gamma':97,'positive_control_eta':1,'artifact_sha256':hashlib.sha256((here/'PARTIAL_RESULT.md').read_bytes()).hexdigest(),'scope':'Finite-metric LP counterexample and strict-dual-margin controls only; no general gap-stability or k-means SDP theorem.'}
(here/'verification.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
