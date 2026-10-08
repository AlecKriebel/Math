#!/usr/bin/env python3
"""Finite exploratory search only; no universal or interval certificate."""
import argparse,json,sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize

def coefficients(phases, durations, degree):
    a=np.zeros(degree+1,dtype=complex);a[1]=1
    start=0.0
    for phase,duration in zip(phases,durations):
        u=np.exp(1j*phase)
        def rhs(t,a):
            out=np.zeros_like(a);power=a.copy()
            for k in range(2,degree+1):
                power=np.convolve(power,a)[:degree+1]
                out-=2*(u*np.exp(-t))**(k-1)*power
            return out
        sol=solve_ivp(rhs,(start,start+duration),a,rtol=2e-11,atol=2e-12)
        if not sol.success:raise RuntimeError(sol.message)
        a=sol.y[:,-1];start+=duration
    # Finish with an exact Koebe map applied to the disk self-map w_T.
    # e^T k_{-u}(w_T) is normalized and univalent.
    terminal=np.zeros_like(a);power=a.copy()
    for k in range(1,degree+1):
        terminal+=k*(-u*np.exp(-start))**(k-1)*power
        power=np.convolve(power,a)[:degree+1]
    return terminal

def optimize(a,grid):
    n=np.arange(2,len(a));m=len(n)
    theta=np.arange(grid)*2*np.pi/grid
    mat=np.exp(1j*np.outer(theta,n-1))
    plus=mat*(n+1);minus=mat*(n-1)
    def unpack(y):return y[:m]+1j*y[m:]
    def norms(y):
        c=unpack(y);return (abs(plus@c)+abs(minus@c))/2
    obj=np.r_[-a[2:].real,a[2:].imag]
    init=np.zeros(2*m);j=int(np.argmax(abs(a[2:])/n));q=np.conj(a[j+2])/abs(a[j+2])/n[j]
    init[j]=q.real;init[m+j]=q.imag
    res=minimize(lambda y:obj@y,init,jac=lambda y:obj,method='SLSQP',constraints=[{'type':'ineq','fun':lambda y:1-norms(y)}],options={'maxiter':600,'ftol':1e-11})
    c=unpack(res.x)
    fine=np.exp(1j*np.outer(np.arange(32768)*2*np.pi/32768,n-1))
    fine_norm=float(np.max((abs(fine@((n+1)*c))+abs(fine@((n-1)*c)))/2))
    # A rigorous real-arithmetic Lipschitz estimate formula, but float evaluation is not a certificate.
    lipschitz=float(np.sum(n*(n-1)*abs(c)))
    upper=fine_norm+np.pi/32768*lipschitz
    return {'optimizer_success':bool(res.success),'optimizer_message':res.message,'sampled_objective':float(-res.fun),'fine_sampled_norm':fine_norm,'float_lipschitz_upper':upper,'ratio_to_fine_norm':float(-res.fun/fine_norm),'ratio_to_float_upper':float(-res.fun/upper),'perturbation_coefficients':[[float(v.real),float(v.imag)] for v in c]}

def main():
    p=argparse.ArgumentParser();p.add_argument('--cases',type=int,default=24);p.add_argument('--degree',type=int,default=8);p.add_argument('--grid',type=int,default=192);args=p.parse_args()
    if not 1<=args.cases<=100 or not 3<=args.degree<=20 or not 64<=args.grid<=2048:p.error('bounded search ranges exceeded')
    rng=np.random.default_rng(2306113);results=[]
    for j in range(args.cases):
        phases=[float(np.pi)]*3 if j==0 else list(map(float,rng.uniform(-np.pi,np.pi,3)))
        durations=[1.0]*3 if j==0 else list(map(float,3*rng.dirichlet(np.ones(3))))
        a=coefficients(phases,durations,args.degree)
        result={'case':j,'phases':phases,'durations':durations,'univalent_coefficients':[[float(v.real),float(v.imag)] for v in a[1:]]};result.update(optimize(a,args.grid));results.append(result)
        print(json.dumps({'case':j,'success':result['optimizer_success'],'ratio':result['ratio_to_float_upper']}),file=sys.stderr,flush=True)
    json.dump({'claim':'Finite floating-point exploration, not a proof or counterexample certificate.','seed':2306113,'degree':args.degree,'optimization_grid':args.grid,'validation_grid':32768,'cases':results},sys.stdout,indent=2);print()
if __name__=='__main__':main()
