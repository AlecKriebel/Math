import mpmath as mp,json,math
from pathlib import Path
mp.mp.dps=80;N=11

def mul(a,b):return [sum(a[j]*b[k-j] for j in range(k+1)) for k in range(N+1)]
def compose(a,b):
 r=[mp.mpc(0)]*(N+1)
 for j in range(N,-1,-1):r=mul(r,b);r[0]+=a[j]
 return r

def slit(q,u):
 y=[mp.mpc(0)]+[q*j*u**(j-1) for j in range(1,N+1)]
 a=[mp.mpc(0)]+[(-u)**(j-1)*mp.mpf(math.comb(2*j,j))/(j+1) for j in range(1,N+1)]
 return compose(a,y)

out=[]
for file in ['loewner_search.json','two_switch_search.json']:
 for r in json.loads(Path(__file__).with_name(file).read_text()):
  x=[mp.mpf(str(v)) for v in r['x']];n=r['n']
  if len(x)==2:q=x[0];w=slit(q,mp.exp(mp.j*x[1]))
  else:
   q=x[0]*x[1];w=compose(slit(x[1],mp.exp(mp.j*x[3])),slit(x[0],mp.exp(mp.j*x[2])))
  aa=[v/q for v in compose([mp.mpc(0)]+[mp.mpf(j) for j in range(1,N+1)],w)]
  delta=sum(abs(aa[j]) for j in range(1,2*n,2))-abs(aa[n])**2
  out.append({'source':file,'n':n,'double_minimum':r['minimum'],'80dps_delta':mp.nstr(delta,60),'sign':int(mp.sign(delta))})
print(json.dumps(out,indent=2));Path(__file__).with_name('rechecked_minima.json').write_text(json.dumps(out,indent=2)+'\n')
