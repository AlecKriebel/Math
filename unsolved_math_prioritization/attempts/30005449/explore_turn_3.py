"""Finite drift diagnostics only: these cannot prove deterministic convergence."""
import json
import numpy as np
import sympy as sy
from scipy.integrate import solve_ivp
from itertools import combinations
rng=np.random.default_rng(5449)
a,b,c=sy.symbols('a b c',positive=True);D=a*b+a*c+b*c
p=sy.Matrix([a*(b+c)/D,b/(a+b),b*c/D]);q=sy.Matrix([p[0]/a,p[1]/b,p[2]/c])
curl=sy.factor(sy.diff(q[0],b)-sy.diff(q[1],a))
assert curl.subs({a:1,b:1,c:1})==sy.Rational(5,36)

def probs(w,edges,n):
 w=np.maximum(w,1e-12)
 L=np.zeros((n-1,n-1))
 for t,(u,v) in zip(w,edges):
  if u<n-1:L[u,u]+=t
  if v<n-1:L[v,v]+=t
  if u<n-1 and v<n-1:L[u,v]-=t;L[v,u]-=t
 out=[]
 for t,(u,v) in zip(w,edges):
  A=L.copy();rhs=np.zeros(n-1)
  if v==n-1:rhs[u]=t
  else:A[u,v]+=t;A[v,u]+=t;rhs[u]=t;rhs[v]=t
  out.append(np.linalg.solve(A,rhs)[0])
 return np.array(out)

# Genuine stopped-walk traces produce admissible convex-combination initial states.
def init(edges,n):
 adj=[[] for _ in range(n)]
 for j,(u,v) in enumerate(edges):adj[u].append((v,j));adj[v].append((u,j))
 frozen=np.exp(rng.uniform(-2,2,len(edges)));total=np.ones(len(edges))
 for _ in range(70):
  v=0;trace=set();steps=0
  while v!=n-1:
   choices=adj[v];ww=np.array([frozen[j] for _,j in choices]);v,j=choices[rng.choice(len(choices),p=ww/ww.sum())];trace.add(j);steps+=1
   if steps>100000:raise RuntimeError('walk cap')
  total[list(trace)]+=1
 return total/71

chosen=[]
for n in (5,6):
 possible=[e for e in combinations(range(n),2) if e!=(0,n-1)]
 seen=set()
 while len(seen)<10:
  mask=int(rng.integers(0,2**len(possible)))
  edges=[e for j,e in enumerate(possible) if mask>>j&1]
  if len(edges)<n or mask in seen:continue
  reached={0}
  for _ in range(n):
   for u,v in edges:
    if u in reached or v in reached:reached.update((u,v))
  if len(reached)!=n:continue
  seen.add(mask);chosen.append((n,edges))
records=[]
for n,edges in chosen:
 finals=[];residual=[]
 for _ in range(3):
  x=init(edges,n)
  sol=solve_ivp(lambda t,w:probs(w,edges,n)-w,(0,50),x,rtol=2e-8,atol=1e-10,max_step=.5)
  assert sol.success
  f=sol.y[:,-1];finals.append(f);residual.append(float(np.max(abs(probs(f,edges,n)-f))))
 records.append({'vertices':n,'edges':edges,'max_final_spread':float(np.max(np.ptp(finals,axis=0))),'max_final_drift':max(residual),'minimum_final_weight':float(np.min(finals))})
print(json.dumps({'status':'completed','exact_gradient_obstruction_at_unit_weights':'5/36','q_a_derivative_b':'-c^2/(ab+ac+bc)^2','q_b_derivative_a':'-1/(a+b)^2','graphs':records,'total_ode_runs':60,'ode_time':50,'floor':1e-12,'largest_final_spread':max(r['max_final_spread'] for r in records),'largest_final_drift':max(r['max_final_drift'] for r in records),'limits':'Finite floating-point diagnostic search; fixed-seed graph sample is not exhaustive, floor changes near-boundary drift, and terminal closeness is not a proof of convergence or uniqueness.'},indent=2))
