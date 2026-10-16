#!/usr/bin/env python3
"""Independent exact algebra checks. This file does not import the original checker."""
import ast
from fractions import Fraction as Q
from itertools import product
import json
from math import factorial
import os
from pathlib import Path
import sys
sys.dont_write_bytecode = True

def require(ok, label):
    if not ok:
        raise RuntimeError(label)

def rejected_false_claim(label, claim):
    try:
        require(claim, label)
    except RuntimeError as exc:
        require(str(exc) == label, 'unexpected rejection')
        return label
    raise RuntimeError('semantic negative control unexpectedly accepted: ' + label)

def r(m, v):
    if m <= 0 or v < -m:
        raise ValueError('outside dissipation domain')
    return v*v/(2*m) + v*v*v/(6*m*m)

def graph_checks():
    n = 0
    for m01,m12,m02 in product([Q(1,8),Q(2,3),Q(1),Q(7,2)], repeat=3):
        m = (m01,m12,m02)
        u0 = 1/(m02+m01*m12/(m01+m12))
        u1 = m01*u0/(m01+m12)
        d = (u0-u1,u1,u0)
        flux = tuple(x*y for x,y in zip(m,d))
        require(flux[0]+flux[2] == 1 and flux[1] == flux[0], 'graph feasibility')
        A = sum(x*y*y for x,y in zip(m,d));M=sum(m);P=sum(flux)
        S=(A+M)/2;R=S-P;C=Q(1)
        require(A == u0 and P >= C and R >= 0, 'graph energy and optimal cost')
        hp = P-M-d[2]+C
        require(hp == C-S-R, 'multiedge entropy chain rule')
        require((M-C)**2 <= 2*M*(S-C), 'multiedge mass estimate')
        mismatch=sum(abs(x-y) for x,y in zip(m,flux))
        require(mismatch*mismatch <= 2*M*(S-C), 'multiedge density-flux estimate')
        for mid in [Q(0),Q(1,4),Q(1,2),Q(1)]:
            opt=(1-mid,mid,Q(1))
            D=sum(x*(y-z)**2 for x,y,z in zip(m,d,opt))/2
            K=sum(x*(1-z*z) for x,z in zip(m,opt))/2
            require(S-C == D+K and D >= 0 and K >= 0, 'weighted decomposition')
        vel=tuple(x*(y-1) for x,y in zip(m,d))
        sprime=sum(v*(1-y*y)/2 for v,y in zip(vel,d))
        require(sprime == -sum(x*(y+1)*(y-1)**2/2 for x,y in zip(m,d)), 'graph Lyapunov identity')
        n += 1
    return {'exact_triangle_network_states':n,'weighted_comparators_per_state':4,'role':'Algebraic non-scalar regression, not a continuum approximation theorem.'}

def dissipation_checks():
    n=supports=0
    for m,g in product([Q(1,11),Q(1),Q(7,3),Q(12)], [Q(0),Q(1,9),Q(1,2),Q(1),Q(5,2),Q(8)]):
        v=m*(g-1);xi=(g*g-1)/2
        primal=r(m,v);dual=xi*v-primal
        require(primal==m*(g-1)**2*(g+2)/6, 'primal formula')
        require(dual==m*(g-1)**2*(2*g+1)/6, 'dual formula')
        require(primal+dual==m*(g-1)**2*(g+1)/2, 'Fenchel dissipation')
        require(primal-v*v/(3*m)==v*v*(m+v)/(6*m*m), 'global coercivity factor')
        for z in [Q(-1),Q(-3,4),Q(0),Q(2),Q(15)]:
            w=m*z
            require(r(m,w)>=primal+xi*(w-v),'supporting hyperplane')
            supports+=1
        n+=1
    for xi in [Q(-1,2),Q(-2),Q(-11)]:
        m=Q(3,2);v=-m
        for z in [Q(-1),Q(-1,2),Q(0),Q(4)]:
            require(r(m,m*z)>=r(m,v)+xi*(m*z-v),'endpoint subgradient')
    return {'reaction_states':n,'supporting_hyperplane_checks':supports,'endpoint_subgradient_checks':12}

def explicit_checks():
    n=0
    for mu0,F,e in product([Q(1,13),Q(1),Q(9,2)],[Q(-7),Q(-1,2),Q(0),Q(1,2),Q(7)],[Q(1),Q(4,5),Q(1,2),Q(1,10000)]):
        rho=abs(F);mu=e*mu0+(1-e)*rho;gx=F/mu
        require(mu>0 and mu>=e*mu0,'finite-time strict positivity')
        require(-e*(mu0-rho)==mu*(abs(gx)-1),'fixed flux reaction')
        require(mu-rho==e*(mu0-rho),'density error')
        if e<=Q(1,2):require(abs(gx)<=2,'large-time gradient bound')
        n+=1
    radial=0
    for d in range(2,13):
        for rr in [Q(j,31) for j in range(1,32)]:
            q=(rr**3-rr)/d; qp=(3*rr*rr-1)/d
            h=1-Q(d+2,d)*rr*rr
            require(qp+(d-1)*q/rr==-h,'radial divergence')
            require(abs(q)<=rr/d,'radial flux estimate')
            radial+=1
        require(Q(1,d)-Q(d+2,d)/Q(d+2)==0,'zero radial forcing mass')
    L=Q(1,4)
    mean=L**5*Q(factorial(2)**2,factorial(5))
    second=L**9*Q(factorial(4)**2,factorial(9))
    var=second-mean*mean
    require(mean==Q(1,30720) and var==Q(11,2202009600),'independent beta-integral moments')
    for j in range(65):
        s=L*Q(j,64);wp=2*s*(L-s)*(L-2*s)
        require(abs(wp)<=Q(1,128),'inactive perturbation bound')
    return {'fixed_flux_states':n,'radial_states':radial,'dimensions':list(range(2,13)),'perturbation_mean':str(mean),'perturbation_mean_zero_L2_squared':str(var),'strict_positivity_of_degenerate_example':False}

def semantic_controls():
    out=[]
    m=Q(1);g=Q(2);v=m*(g-1)
    out.append(rejected_false_claim('wrong cubic sign',v*v/(2*m)-v**3/(6*m*m)==m*(g-1)**2*(g+2)/6))
    out.append(rejected_false_claim('wrong square-root branch',-m*(g+1)>=-m))
    out.append(rejected_false_claim('nonzero gradient at active obstacle',-Q(1,2)>=0))
    F=Q(-2);mu0=Q(1);e=Q(1,4)
    wrong=e*mu0+(1-e)*F
    out.append(rejected_false_claim('signed flux substituted for its magnitude',wrong>0))
    out.append(rejected_false_claim('zero density called strictly positive',Q(0)>0))
    N=64;eps=Q(1,N*N)
    a0=Q(0);b0=eps;am=-eps;bm=Q(0)
    holder_ratio=abs((abs(a0)-abs(b0))-(abs(am)-abs(bm)))/Q(1,N)
    out.append(rejected_false_claim('absolute-value Holder contraction',holder_ratio<=eps))
    out.append(rejected_false_claim('weighted control implies same unweighted control',Q(N*N)<=Q(1)))
    out.append(rejected_false_claim('weak elliptic product uses arithmetic conductivity',Q(4,3)==Q(1)))
    # Two equiprobable conductivities 1 and 3: mean reciprocal 2/3, mean 2.
    out.append(rejected_false_claim('reciprocal commutes with averaging',(Q(1)+Q(1,3))/2==Q(1,2)))
    return {'rejected_semantic_overclaims':out,'Holder_counterexample':{'delta':'1/2','epsilon':str(eps),'input_difference_Cdelta_norm':str(eps),'output_difference_Cdelta_seminorm_lower_bound':str(holder_ratio),'ratio_lower_bound':str(holder_ratio/eps)},'limits':'The Holder example refutes a generic composition inequality, not by itself the specialized fixed-forcing elliptic-map theorem.'}

def readonly_probes():
    base=Path(__file__).resolve().parent
    require(os.geteuid()==1000,'UID 1000 required')
    require(not os.access(base,os.W_OK),'audit directory must be read-only')
    probe=base/('.probe_'+str(os.getpid()))
    try:fd=os.open(probe,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    except PermissionError:pass
    else:
        os.close(fd);probe.unlink();raise RuntimeError('directory write unexpectedly permitted')
    n=0
    for p in sorted(base.rglob('*')):
        if p.is_file():
            require(not p.is_symlink() and not os.access(p,os.W_OK),'file unexpectedly writable')
            try:fd=os.open(p,os.O_WRONLY)
            except PermissionError:n+=1
            else:
                os.close(fd);raise RuntimeError('file write-open unexpectedly permitted')
    return {'actual_directory_create_denied':True,'actual_file_write_open_denials':n}

if __name__=='__main__':
    try:
        require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(Path(__file__).read_text()))),'assert forbidden')
        result={'status':'passed','uid':os.geteuid(),'optimization':sys.flags.optimize,'graph':graph_checks(),'dissipation':dissipation_checks(),'explicit_cases':explicit_checks(),'semantic_controls':semantic_controls(),'limits':'Exact bounded regressions and written proof audit; no general PDE existence or convergence certification.'}
        if '--require-readonly' in sys.argv:result['readonly']=readonly_probes()
        print(json.dumps(result,indent=2,sort_keys=True))
    except Exception as exc:
        sys.stderr.write(type(exc).__name__+': '+str(exc)+'\n');sys.exit(1)
