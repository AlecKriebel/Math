import numpy as np, math, json
from scipy.optimize import differential_evolution
from pathlib import Path
N=9

def mul(a,b): return np.convolve(a,b)[:N+1]
def compose(a,b):
 r=np.zeros(N+1,complex)
 for j in range(N,-1,-1):
  r=mul(r,b); r[0]+=a[j]
 return r

def slit(q,u):
 # k_u(w)=q k_u(z), w(0)=0; use Catalan inverse series.
 y=np.zeros(N+1,complex)
 for j in range(1,N+1): y[j]=q*j*u**(j-1)
 a=np.zeros(N+1,complex)
 for j in range(1,N+1): a[j]=(-u)**(j-1)*math.comb(2*j,j)/(j+1)
 return compose(a,y)

def coeff(x):
 q=x[0];u=np.exp(1j*x[1]); v=1
 w=slit(q,u)
 a=np.array([0]+[j*v**(j-1) for j in range(1,N+1)],complex)
 return compose(a,w)/q

def obj(x,n):
 a=coeff(x); return float(sum(abs(a[j]) for j in range(1,2*n,2))-abs(a[n])**2)

out=[]
for n in range(3,6):
 r=differential_evolution(lambda x:obj(x,n),[(.001,.999),(0,2*np.pi)],seed=583+ n,popsize=20,maxiter=100,tol=1e-9,polish=True)
 out.append({'n':n,'minimum':float(r.fun),'x':r.x.tolist(),'coeff':[[float(z.real),float(z.imag)] for z in coeff(r.x)]}); print(out[-1],flush=True)
Path(__file__).with_name('loewner_search.json').write_text(json.dumps(out,indent=2))
