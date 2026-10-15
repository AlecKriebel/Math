#!/usr/bin/env python3
"""Independent deterministic diagnostics; not a finite surrogate for the proof.
All guards use explicit exceptions and run under -O as well as normal Python.
"""
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,math,random,sys

def require(condition,message):
    if not condition: raise RuntimeError(message)

def Tv(v,z,adj,beta):
    return sum((z[v]+z[w])**beta for w in adj[v])

def scalar_response(p,neighbors,beta):
    # Unique solution a sum_w(a+neighbors_w)^beta=p, with an exact sign bracket.
    lo=0.0; hi=(p/len(neighbors))**(1/(beta+1))
    for _ in range(90):
        mid=(lo+hi)/2
        val=mid*sum((mid+x)**beta for x in neighbors)
        if val < p:lo=mid
        else:hi=mid
    return (lo+hi)/2

def finite_volume(beta,radius,rate):
    # Path Z, zero exterior; same scalar equations as energy minimization, solved
    # by cyclic exact one-coordinate minimization. No root/author routine reused.
    vertices=list(range(-radius,radius+1))
    P=max(rate(v) for v in vertices)
    B=P**(1/(beta+1))
    z={v:B/2 for v in vertices}
    for sweeps in range(6000):
        change=0.0
        for v in vertices:
            a=scalar_response(rate(v),[z.get(v-1,0.0),z.get(v+1,0.0)],beta)
            change=max(change,abs(a-z[v]));z[v]=a
        residual=max(abs(z[v]*sum((z[v]+z.get(w,0.0))**beta for w in (v-1,v+1))-rate(v))/rate(v) for v in vertices)
        if residual < 2e-11:break
    require(residual<2e-11,f"finite-volume residual {beta=} {radius=} {residual=}")
    for v in vertices:
        lower=rate(v)/(2*(2*B)**beta)
        upper=(rate(v)/2)**(1/(beta+1))
        require(z[v] >= lower*(1-1e-10),"coordinate lower estimate failed")
        require(z[v] <= upper*(1+1e-10),"coordinate upper estimate failed")
    return z,{'beta':beta,'radius':radius,'sweeps':sweeps+1,'max_relative_residual':residual,'center':z[0],'min_rate':min(rate(v) for v in vertices)}

def modulus(epsilon,K,beta):
    return epsilon**beta if beta<=1 else beta*(2*K)**(beta-1)*epsilon

def strip_controls(rng):
    exact=0; floating=0; min_margin=math.inf
    adj={v:[(v-1)%6,(v+1)%6] for v in range(6)}
    # Every rate is manufactured from a genuine equilibrium; not an assumption
    # that an arbitrary positive array solves unspecified rates.
    for beta in [F(1),F(2),0.25,0.5,4.0,9.0]:
        for sign in [1,-1]:
            for case in range(100):
                z={v:F(rng.randint(2,100),100) if isinstance(beta,F) else 10**rng.uniform(-12,0) for v in range(6)}
                K=max(z.values())+1
                B=max(z.values())
                M=F(1,10) if isinstance(beta,F) else 0.1
                # In lower strip select a site with z_v>M, preserving positivity.
                v=case%6
                z[v]=F(1,2) if isinstance(beta,F) else 0.5
                B=max(z.values());K=B+1
                eps=M/8
                while B*2*modulus(eps,K,beta)/(M/2)**beta >=M/4:eps/=2
                d={w:(F(rng.randint(-100,100),100)*min(M,z[w]/2) if isinstance(beta,F) else rng.uniform(-1,1)*min(M,z[w]/2)) for w in range(6)}
                d[v]=sign*(M-eps/2)
                # Challenge with opposing neighbors at their largest allowed
                # deviation; lower positivity limits the negative choice.
                for w in adj[v]:
                    d[w]=-min(M,z[w]/2) if sign>0 else M
                b={w:z[w]+d[w] for w in range(6)}
                require(all(x>0 for x in b.values()),"invalid test trajectory coordinate")
                p=z[v]*Tv(v,z,adj,beta)
                R=p/Tv(v,b,adj,beta)
                derivative=(R-z[v])-d[v] # actual c multiplier removed
                margin=-M/2-derivative if sign>0 else derivative-M/2
                require(margin>=-1e-12,"backward-strip damping bound failed")
                min_margin=min(min_margin,float(margin))
                if isinstance(beta,F):
                    require(isinstance(p,F) and isinstance(R,F) and isinstance(derivative,F) and isinstance(margin,F),"exact-control arithmetic left rational domain")
                    exact+=1
                else:floating+=1
    return {'exact_fraction_strip_cases':exact,'floating_strip_cases':floating,'min_damping_margin_before_c_factor':min_margin}

def boundary_checks():
    # Infinite alternating path reduces exactly to two parity classes, degree 2.
    rows=[]
    for alpha in [0.01,0.25,0.5,0.75,0.99]:
        for even in [True,False]:
            vals=[2.0 if ((i%2==0)==even) else 0.0 for i in range(4)]
            for i,x in enumerate(vals):
                left=vals[(i-1)%4];right=vals[(i+1)%4]
                rhs=x**alpha*(1/(left**alpha+x**alpha)+1/(x**alpha+right**alpha))
                require(abs(rhs-x)<1e-13,"alternating boundary residual")
            rows.append({'alpha':alpha,'parity':even,'residual_max':max(abs(x**alpha*(1/(vals[(i-1)%4]**alpha+x**alpha)+1/(x**alpha+vals[(i+1)%4]**alpha))-x) for i,x in enumerate(vals))})
        require(abs(1**alpha*(1/2+1/2)-1)<1e-15,"positive path equilibrium")
    # Critical even cycle has strictly positive continuum and must be excluded.
    for a in [0.01,0.3,0.9,1.7]:
        b=2-a
        require(abs(a*(1/(a+b)+1/(a+b))-a)<1e-14,"critical positive equilibrium")
    return {'alternating_path_boundary_cases':rows,'critical_even_cycle_positive_cases':4,'alpha_zero_rate_on_path':1.0}

def disconnected_small_rate_control():
    # Countably many independent one-edge components with p_u=p_v=2^-n.
    # Symmetric ODE solution y=b^(beta+1)=p/2^beta+C exp(-s).
    # Complete positivity and boundedness force C=0 on each component.
    rows=[]
    for beta in [0.25,0.5,1.0,2.0,9.0]:
        for n in [1,20,100,500]:
            p=2.0**(-n)
            z=(p/2**beta)**(1/(beta+1))
            x=(2*z)**(beta+1)
            require(math.isclose(x,2*p,rel_tol=5e-13),"single-edge equilibrium mapping")
            rows.append({'beta':beta,'n':n,'rate':p,'z':z,'x':x})
    return {'exact_formula':'b^(beta+1)=p/2^beta+C exp(-s); C<0 violates backward positivity, C>0 violates backward boundedness','positive_stationary_components':rows}

def main():
    rng=random.Random(76430005453)
    finite=[]
    for beta in [0.25,0.5,1.0,2.0,4.0,9.0]:
        centers=[]
        for radius in [2,4,8,16]:
            z,row=finite_volume(beta,radius,lambda v:2.0**(-abs(v)))
            finite.append(row);centers.append(z[0])
        require(abs(centers[-1]-centers[-2])<0.02,"finite-volume center stabilization diagnostic")
    result={'checked_utc':datetime.now(timezone.utc).isoformat(),'result':'PASS','scope':'Deterministic diagnostics, exact finite strip inequalities for beta=1,2, and elementary limiting controls; analytic infinite-volume and rigidity claims are verified in the independent derivation, not inferred from these tests.','finite_volume':finite,'strip_controls':strip_controls(rng),'boundary_controls':boundary_checks(),'vanishing_rate_complete_trajectory_control':disconnected_small_rate_control()}
    destination=None
    if len(sys.argv)>1:
        require(len(sys.argv)==3 and sys.argv[1]=='--output','Usage: independent_controls.py [--output PATH]')
        destination=Path(sys.argv[2])
        destination.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'result':result['result'],'finite_volume_cases':len(finite),'strip_controls':result['strip_controls'],'output':str(destination) if destination else None}))

if __name__=='__main__':main()
