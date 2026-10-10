"""Optional, non-certifying two-parameter exploration; not a global optimum search."""
import json
import numpy as np
from scipy.optimize import minimize

def data(n, xy):
    u=complex(*xy); alpha=1-u; b=[1+0j]
    for j in range(1,n+1): b.append(b[-1]*(alpha+j-1)/j)
    v=np.array([b[n-k]/k for k in range(n//2+1,n+1)])
    W=b[n]+u*sum(v)
    q=abs(W)/sum(abs(v))
    return max(abs(u),q),u,b,v,W

def main():
    out=[]
    for n in [2,3,4,8,16,32,64,128]:
        r=minimize(lambda x:data(n,x)[0],[.43246,-.54237],method='Nelder-Mead',options={'maxiter':400,'xatol':1e-12,'fatol':1e-12})
        q,u,_,_,_=data(n,r.x)
        out.append({'n':n,'u_real':u.real,'u_imag':u.imag,'constructed_radius_float':q,'iterations':int(r.nit),'globally_optimal':False})
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
