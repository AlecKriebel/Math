import numpy as np, math, json
from scipy.optimize import differential_evolution
from pathlib import Path
N=11

def mul(a,b): return np.convolve(a,b)[:N+1]
def compose(a,b):
 r=np.zeros(N+1,complex)
 for j in range(N,-1,-1):
  r=mul(r,b); r[0]+=a[j]
 return r

def slit(q,u):
 y=np.array([0]+[q*j*u**(j-1) for j in range(1,N+1)],complex)
 a=np.array([0]+[(-u)**(j-1)*math.comb(2*j,j)/(j+1) for j in range(1,N+1)],complex)
 return compose(a,y)

def coeff(x):
 q1,q2=x[:2];u1,u2=np.exp(1j*np.array(x[2:])); w=compose(slit(q2,u2),slit(q1,u1))
 a=np.array([0]+list(range(1,N+1)),complex)
 return compose(a,w)/(q1*q2)

def obj(x,n):
 a=coeff(x); return float(sum(abs(a[j]) for j in range(1,2*n,2))-abs(a[n])**2)

out=[]
for n in range(3,7):
 r=differential_evolution(lambda x:obj(x,n),[(.02,.95),(.02,.95),(0,2*np.pi),(0,2*np.pi)],seed=683+n,popsize=18,maxiter=150,tol=1e-8,polish=True)
 out.append({'n':n,'minimum':float(r.fun),'x':r.x.tolist(),'coeff':[[float(z.real),float(z.imag)] for z in coeff(r.x)]});print(out[-1],flush=True)
Path(__file__).with_name('two_switch_search.json').write_text(json.dumps(out,indent=2))
