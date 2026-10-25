#!/usr/bin/env python3
"""Independent controls; does not import the paper's implementation.
Finite floating/high-precision calculations support but do not prove universal claims.
"""
import json
import platform
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import scipy
from scipy.linalg import expm, logm
import mpmath as mp

rng=np.random.default_rng(22729537)
results={"scope":"Independent finite controls, no universal proof or novelty certification","timestamp_utc":datetime.now(timezone.utc).isoformat(),"environment":{"python":platform.python_version(),"numpy":np.__version__,"scipy":scipy.__version__,"mpmath":mp.__version__}}

def reversible_case(pi,w,name):
    Q=w/pi[:,None]
    np.fill_diagonal(Q,0)
    Q-=np.diag(Q.sum(axis=1))
    Q0=Q/(-np.trace(Q)); D=np.diag(pi)
    errs=[]
    for age in [.003,.2,.7,1.9]:
        P=expm(Q0*age)
        J=P.T@D@P
        A=np.linalg.solve(D,J)
        sign,logdet=np.linalg.slogdet(A)
        assert sign>0
        s=-logdet
        recovered=np.real_if_close(logm(A))/s
        errs.append({"age":age,"determinant_distance_error":abs(s-2*age),"generator_error":float(np.max(np.abs(recovered-Q0)))})
    assert max(x["determinant_distance_error"] for x in errs)<1e-10
    assert max(x["generator_error"] for x in errs)<1e-10
    return {"name":name,"checks":errs}

pi=rng.uniform(.1,1,4); pi/=pi.sum()
w=rng.uniform(.2,.9,(4,4));w=(w+w.T)/2;np.fill_diagonal(w,0)
connected_path=np.zeros((4,4))
for i in range(3):connected_path[i,i+1]=connected_path[i+1,i]=.2+i*.11
jc=np.ones((4,4)); np.fill_diagonal(jc,0)
results["reversible_generator"]=[reversible_case(pi,w,"generic unequal stationary"),reversible_case(pi,connected_path,"irreducible zero-conductance face"),reversible_case(np.ones(4)/4,jc,"JC repeated eigenvalues")]
Q=(np.roll(np.eye(3),1,axis=1)-np.eye(3))/3
D=np.eye(3)/3;age=.7;P=expm(Q*age);J=P.T@D@P;A=np.linalg.solve(D,J);s=-np.linalg.slogdet(A)[1]
wrong=logm(A)/s
results["nonreversible_negative_control"]={"determinant_distance_error":float(abs(s-2*age)),"generator_recovery_error":float(np.max(abs(wrong-Q))),"expected":"determinant identity survives; reversible generator inversion need not"}
assert abs(s-2*age)<1e-12 and np.max(abs(wrong-Q))>.1

# Full sequence pattern words are affine moment polynomials; check representative
# words by independent expansion, including all off-diagonal and all diagonal.
mp.mp.dps=90
beta=mp.mpf(2)/3; tau=mp.mpf('0.6');lam0=mp.mpf('0.9')
def laplace(theta,s,knots):
    starts=[mp.mpf(0)]+knots
    rate=lam0;survival=mp.mpf(1);total=mp.mpf(0)
    for i,left in enumerate(starts):
        if i: rate+=theta[i-1]
        factor=survival*mp.exp(-s*left)*rate/(rate+s)
        if i==len(knots):total+=factor
        else:
            width=starts[i+1]-left
            total+=factor*(-mp.expm1(-(rate+s)*width))
            survival*=mp.exp(-rate*width)
    return total

def moment(theta,k,knots):
    return mp.exp(-beta*k*tau)*laplace(theta,beta*k,knots)

def word(theta,kinds,knots):
    coeff=[mp.mpf(1)]
    for kind in kinds:
        c0=mp.mpf(1)/16;c1=mp.mpf(3 if kind=='d' else -1)/16
        new=[mp.mpf(0)]*(len(coeff)+1)
        for i,c in enumerate(coeff):new[i]+=c*c0;new[i+1]+=c*c1
        coeff=new
    return sum(c*(1 if k==0 else moment(theta,k,knots)) for k,c in enumerate(coeff))
collisions=[]
for L in range(1,7):
    m=L+1;knots=[mp.mpf(j)*mp.mpf('0.15') for j in range(1,m+1)];zero=[mp.mpf(0)]*m
    targets=[moment(zero,k,knots) for k in range(1,m+1)]
    J=mp.matrix([[mp.exp(-k*beta*tau)*(k*beta)/(k*beta+lam0)**2*mp.exp(-(k*beta+lam0)*a) for a in knots] for k in range(1,m+1)])
    derivative_error=max(abs(mp.diff(lambda x:moment([x if j==col else mp.mpf(0) for j in range(m)],row+1,knots),0)-J[row,col]) for row in range(m) for col in range(m))
    curves=[]
    for last in [mp.mpf('0.001'),mp.mpf('-0.001')]:
        def eq(*args):return tuple(moment(list(args)+[last],k,knots)-targets[k-1] for k in range(1,L+1))
        x=mp.findroot(eq,tuple(mp.mpf(0) for _ in range(L)),tol=mp.mpf('1e-80'),maxsteps=80)
        theta=list(x)+[last]
        assert all(lam0+sum(theta[:i])>0 for i in range(m+1)) and all(t!=0 for t in theta)
        curves.append(theta)
    lo,hi=curves
    matched=max(abs(moment(lo,k,knots)-moment(hi,k,knots)) for k in range(1,L+1))
    nextdiff=abs(moment(lo,L+1,knots)-moment(hi,L+1,knots))
    lowerwords=max(abs(word(lo,kinds,knots)-word(hi,kinds,knots)) for kinds in ['d'*L,'o'*L,'do'*(L//2)+'d'*(L%2)])
    sepword=abs(word(lo,'d'*(L+1),knots)-word(hi,'d'*(L+1),knots))
    assert matched<mp.mpf('1e-70') and derivative_error<mp.mpf('1e-80') and nextdiff>mp.mpf('1e-30')
    assert lowerwords<mp.mpf('1e-70') and sepword>mp.mpf('1e-30')
    collisions.append({"L":L,"jacobian_determinant":str(mp.det(J)),"jacobian_double_condition":float(np.linalg.cond(np.array(J.tolist(),dtype=float))),"derivative_error":str(derivative_error),"lower_moment_difference":str(matched),"next_moment_difference":str(nextdiff),"lower_word_probability_difference":str(lowerwords),"next_diagonal_word_difference":str(sepword),"theta_plus":[str(x) for x in lo],"theta_minus":[str(x) for x in hi]})
results['demographic_collision_controls']=collisions

# Shifted-Hankel co-occupancy formula on repeated, distinct and nearly repeated rates.
decoder=[]
for rates,weights,label in [([1,1],[.13,.29],'equal rates combined'),([.2,1.1,2.6],[.13,.29,.07],'three distinct rates'),([1,1+1e-7],[.13,.29],'nearly coincident rates')]:
    # Mpmath uses supplied decimal strings, keeping tiny gaps meaningful.
    atoms={}
    for r,w in zip(rates,weights):atoms[mp.mpf(str(r))]=atoms.get(mp.mpf(str(r)),mp.mpf(0))+mp.mpf(str(w))
    n=len(atoms);mom=lambda k:sum(w*r**k for r,w in atoms.items())
    H=mp.matrix([[mom(a+b+2) for b in range(n)] for a in range(n)])
    v=mp.matrix([mom(a+1) for a in range(n)])
    recovered=(v.T*mp.lu_solve(H,v))[0]
    error=abs(recovered-sum(atoms.values()))
    assert error<mp.mpf('1e-70')
    decoder.append({"case":label,"cooccupancy_error":str(error),"double_condition":float(np.linalg.cond(np.array(H.tolist(),dtype=float))),"cooccupancy":str(recovered)})
results['child_decoder']=decoder

# Stationary-model determinant conditioning: saturation causes lost precision,
# an expected limitation rather than a counterexample to population identifiability.
Q=(np.ones((4,4))-4*np.eye(4))/12;D=np.eye(4)/4
sat=[]
for s in [.001,1,10,50,100,150]:
    A=expm(Q*s);sign,ld=np.linalg.slogdet(A)
    sat.append({"distance":s,"sign":float(sign),"logdet_error":float(abs(-ld-s)),"condition":float(np.linalg.cond(A))})
results['saturation_conditioning']=sat
results['status']='PASS'
Path('independent-controls.json').write_text(json.dumps(results,indent=2)+'\n')
print('INDEPENDENT_CONTROLS_PASS',json.dumps({"generator_cases":3,"collision_orders":list(range(1,7)),"decoder_cases":3,"negative_control":"nonreversible inversion rejected","max_collision_condition":collisions[-1]['jacobian_double_condition']}))
