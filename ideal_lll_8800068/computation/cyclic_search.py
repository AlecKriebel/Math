from pathlib import Path
#!/usr/bin/env python3
import argparse,json,random,time
import sympy as S
from fractions import Fraction

def basis(n,m):
 B=S.eye(n)*m; B[n-1,:]=S.ones(1,n);return B

def audit(B,m):
 n=B.rows; gs=[]; norms=[];mus=[]
 for i in range(n):
  v=list(map(Fraction,B.row(i)));row=[]
  for j in range(i):
   mu=sum(Fraction(B[i,k])*gs[j][k] for k in range(n))/norms[j];row.append(mu)
   v=[x-mu*y for x,y in zip(v,gs[j])]
  gs.append(v);norms.append(sum(x*x for x in v));mus.append(row)
 ok=all(abs(mu)<=Fraction(1,2) for row in mus for mu in row) and all(norms[i]+mus[i][i-1]**2*norms[i-1]>=Fraction(3,4)*norms[i-1] for i in range(1,n))
 return {'reduced':ok,'size_reduced':all(abs(mu)<=Fraction(1,2) for row in mus for mu in row),'failing_lovasz_indices':[i+1 for i in range(1,n) if norms[i]+mus[i][i-1]**2*norms[i-1]<Fraction(3,4)*norms[i-1]],'determinant_abs':str(abs(B.det())),'membership':all(all((B[i,j]-B[i,0])%m==0 for j in range(n)) for i in range(n)),'gs_squared':[str(x) for x in norms]}

def run(n,m,trials,seed):
 rng=random.Random(seed);base=basis(n,m);best=-1;output={};fails=0; hist={}
 for t in range(trials):
  B=base.copy()
  # Half exploratory fresh scrambles, half mutate the best reduced state.
  if t%2 and output:B=S.Matrix(output['basis'])
  p=list(range(n));rng.shuffle(p);B=B[p,:]
  for _ in range(3*n if not t%2 else n):
   i,j=rng.sample(range(n),2);a=rng.choice([-2,-1,1,2]);B[i,:]=B[i,:]+a*B[j,:]
  try:R=B.lll(delta=S.Rational(3,4))
  except Exception as e:fails+=1;continue
  score=int(sum(x*x for x in R.row(0)));hist[score]=hist.get(score,0)+1
  if score>best:
   best=score;output={'n':n,'m':m,'trial':t,'seed':seed,'first_squared':score,'ratio_squared':str(Fraction(score,n)),'basis':[[int(x) for x in R.row(i)] for i in range(n)]}
 output.update({'trials':trials,'failures':fails,'histogram':hist,'audit':audit(S.Matrix(output['basis']),m)})
 return output
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--trials',type=int,default=30);p.add_argument('--output',default=str(Path(__file__).with_name('cyclic_results.json')));a=p.parse_args()
 out=[]
 for n,m in [(6,4),(8,5),(8,8),(12,6),(12,12),(16,8),(16,16),(20,10),(20,20)]:
  r=run(n,m,a.trials,8800068+n*100+m);out.append(r);print(n,m,r['first_squared'],r['histogram'],flush=True)
  with open(a.output,'w') as f:json.dump(out,f,indent=2)
