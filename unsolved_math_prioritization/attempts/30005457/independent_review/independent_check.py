#!/usr/bin/env python3
"""Independent exact rational controls of lattice-WARM partials; no simulation."""
from fractions import Fraction as F
from pathlib import Path
import json,random
R=random.Random(30005457);counts={};q=F(1,16);C=(1+q*q)/(1+q);eta=F(1,100)
def ck(name,v):
 assert v,name;counts[name]=counts.get(name,0)+1
def p(v):
 n,y=v
 return q**(abs(n)+abs(y)) if y else (C*q**(abs(n)-1) if n else 2*q/(1+q))
def norm(e):return tuple(sorted(e))
def inc(v):
 a,b=v;return [norm([v,z]) for z in [(a-1,b),(a+1,b),(a,b-1),(a,b+1)]]
def x(e):
 (a,y),(b,z)=norm(e)
 if y==z==0:return q**min(abs(a),abs(b))
 if y==z and y!=0 and a%2==0:return p((a,y))+p((b,z))
 return F(0)
for n in range(-9,10):
 for y in range(-4,5):
  v=(n,y);star=inc(v);ss=sum(x(e)**2 for e in star)
  ck('positive_bounded_rate',0<p(v)<=1);ck('nonzero_star',ss>0)
  for e in star:
   val=sum(p(w)*x(e)**2/sum(x(b)**2 for b in inc(w)) for w in e)
   ck('full_lattice_equilibrium',val==x(e))
   ck('edge_rate_envelope',x(e)<=sum(p(w) for w in e))
  ck('local_K_lower_bound',sum(x(e) for e in star)>=p(v))
# Assemble an ordinary finite-graph drift Jacobian independently by differentiating
# each local selection fraction, before testing row/column logarithmic norms.
def field_jac(edges,w,rate):
 incident={v:[i for i,e in enumerate(edges) if v in e] for v in rate}
 m=len(edges);f=[-z for z in w];J=[[F(-int(i==j)) for j in range(m)] for i in range(m)]
 for v,ids in incident.items():
  ss=sum(w[i]**2 for i in ids)
  for i in ids:
   f[i]+=rate[v]*w[i]**2/ss
   for j in ids:
    J[i][j]+=rate[v]*(2*w[i]*int(i==j)/ss-2*w[i]**2*w[j]/ss**2)
 return f,J
rho=2*F(32,257)/(1-eta)*((1+eta)/(1-eta))**4
ck('exact_nonlinear_bound',rho==F(665986566400,2444044428243));ck('nonlinear_gap',rho<F(1,3));ck('linear_gap',1-2*F(32,257)==F(193,257))
for M in range(2,9):
 edges=[(n,n+1) for n in range(-M,M)];base=[q**min(abs(a),abs(b)) for a,b in edges];rate={v:p((v,0)) for v in range(-M,M+1)}
 f,J=field_jac(edges,base,rate);r=q**(M+1)/(1+q)
 ck('endpoint_residual',f[0]==f[-1]==r and all(z==0 for z in f[1:-1]));ck('relative_endpoint_residual',r/base[0]==F(1,272));ck('invariant_box_forcing',F(1,272)<F(2,3)*eta)
 for trial in range(32):
  perturb=[R.choice([-eta,F(0),eta]) for _ in base];w=[z*(1+h) for z,h in zip(base,perturb)];_,J=field_jac(edges,w,rate);m=len(w)
  for i in range(m):
   ck('nonpositive_off_diagonal',all(J[i][j]<=0 for j in range(m) if i!=j))
   row=J[i][i]+sum(abs(J[i][j])*base[j]/base[i] for j in range(m) if j!=i)
   ck('relative_row_contraction',row<=-F(2,3))
   col=J[i][i]+sum(abs(J[j][i]) for j in range(m) if j!=i)
   ck('ordinary_column_contraction',col<=-F(2,3));ck('conserved_rate_column_sum',sum(J[j][i] for j in range(m))==-1)
 for n in [M,M+1]:
  b=3*q**(n+1)/(1+q)+2*(1+C)*q**n/(1-q)
  ck('tail_bound',0<b<5*q**n)
# Uniform l1 Lipschitz estimate on finite analogues of K; no rate lower bound used.
graphs=[[(0,1)],[(0,1),(1,2)],[(0,1),(1,2),(2,0)],[(0,1),(0,2),(0,3),(1,2)]]
for edges in graphs:
 for trial in range(30):
  w=[F(R.randrange(1,9),R.randrange(1,11)) for e in edges];vs=set(sum(([a,b] for a,b in edges),[]));rate={v:sum(w[i] for i,e in enumerate(edges) if v in e)/2 for v in vs};D=max(sum(v in e for e in edges) for v in vs);f,J=field_jac(edges,w,rate)
  ck('K_total_mass',sum(w)==sum(rate.values()));ck('K_edge_envelope',all(w[i]<=rate[a]+rate[b] for i,(a,b) in enumerate(edges)))
  # F+x=f_intensity. Its Jacobian is J+I.
  for j in range(len(w)):
   ck('l1_intensity_Lipschitz',sum(abs(J[i][j]+int(i==j)) for i in range(len(w)))<=8*D)
  ss={v:sum(w[i]**2 for i,e in enumerate(edges) if v in e) for v in vs}
  g=[-1+sum(rate[v]*w[i]/ss[v] for v in e) for i,e in enumerate(edges)]
  ck('weighted_gradient_identity',all(f[i]==w[i]*g[i] for i in range(len(w))))
  ck('nonnegative_Lyapunov_dissipation',sum(f[i]*g[i] for i in range(len(w)))==sum(w[i]*g[i]**2 for i in range(len(w))))
  ck('uniform_gradient_bound',all(abs(z)<=1+2*D for z in g))
ck('line_rate_mass',2*q/(1+q)+2*C/(1-q)==2/(1-q))
ck('total_rate',2/(1-q)+2*q*(1+q)/(1-q)**2==F(514,225))
ck('square_root_rate_majorant',F(1)+2/(1-F(1,4))+2*F(1,4)*(1+F(1,4))/(1-F(1,4))**2==F(43,9))
out={'status':'PASS','exact_assertions':sum(counts.values()),'categories':counts,'q':str(q),'nonlinear_correction':str(rho),'total_rate':'514/225','method':'Independent rational reconstruction of full local rates, finite-path Jacobians, logarithmic norms, K-domain and weighted-gradient identities','limits':'Finite controls do not certify stochastic percolation or replace the separately audited infinite-volume arguments.'}
Path(__file__).with_name('INDEPENDENT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
