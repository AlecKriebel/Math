"""Minimal preserved reproducer for the two abandoned double-tuned families.

Reconstructed from the original generator/diagnostic functions and cases.
The original full first-run source snapshot was not retained before editing.
This does not conduct a new broad numeric run.
"""
import math, json
import mpmath as mp
from pathlib import Path
from datetime import datetime, timezone

def det(p,q): return p[0]*q[1]-p[1]*q[0]
def next_point(P,a,b,lam,sqrt):
    ac,bc=sqrt(a*a-lam),sqrt(b*b-lam)
    Y=(P[0]/ac,P[1]/bc); r2=Y[0]*Y[0]+Y[1]*Y[1]; root=sqrt(r2-1)
    for sign in (-1,1):
        U=((Y[0]-sign*Y[1]*root)/r2,(Y[1]+sign*Y[0]*root)/r2)
        direction=(ac*U[0]-P[0],bc*U[1]-P[1])
        if det(P,direction)>0:
            den=direction[0]**2/(a*a)+direction[1]**2/(b*b)
            distance=-2*(P[0]*direction[0]/(a*a)+P[1]*direction[1]/(b*b))/den
            return (P[0]+distance*direction[0],P[1]+distance*direction[1])
    raise AssertionError('no ccw tangent')
def trajectory(a,b,lam,N,phase,ctx):
    points=[(a*ctx.cos(phase),b*ctx.sin(phase))]
    for _ in range(N): points.append(next_point(points[-1],a,b,lam,ctx.sqrt))
    return points
def tune(a,b,N,k,ctx,iterations,small):
    lower=small*b*b; upper=(1-small)*b*b
    for _ in range(iterations):
        mid=(lower+upper)/2; P=trajectory(a,b,mid,N,ctx.mpf(0) if ctx is mp else 0.,ctx)
        angle=ctx.fsum(ctx.atan2(det(p,q),p[0]*q[0]+p[1]*q[1]) for p,q in zip(P,P[1:]))
        if angle<2*ctx.pi*k: lower=mid
        else: upper=mid
    return (lower+upper)/2
def am(Q):
    cr=[det(p,Q[(i+1)%len(Q)]) for i,p in enumerate(Q)]
    return math.fsum(cr)/2,complex(*(math.fsum(cr[i]*(Q[i][j]+Q[(i+1)%len(Q)][j]) for i in range(len(Q))) for j in (0,1)))
def moment_residuals(P,a,b,lam):
    def feet(M):
        Q=[]
        for p in P:
            n=(p[0]/(a*a),p[1]/(b*b)); n2=n[0]**2+n[1]**2
            factor=(1-n[0]*M[0]-n[1]*M[1])/n2
            Q.append((M[0]+factor*n[0],M[1]+factor*n[1]))
        return Q
    H=(a*a+b*b)/2; e=(a*a-b*b)/2; d=1-lam/a**2-lam/b**2; F=H*d+2*lam; v=-4*e*lam*d/(F*F-e*e*d*d)
    S0,_=am(feet((0.,0.))); Ms=[(0.,0.),(.71,-.43),(2.3,1.7),(-5.,3.)]
    if d<0: Ms.append((math.sqrt(-2*F/d),0.))
    residuals=[]
    for M in Ms:
        z=complex(*M); r2=abs(z)**2; G=2*F+d*r2
        _,actual=am(feet(M))
        numerator=z*(F+2*H*d+e*v*d)+z.conjugate()*(2*F*v+3*e*d+v*d*r2/2)
        expected=S0/F*(3*G*z/2-numerator)
        residuals.append({'M':M,'normalized_moment_residual':abs(actual-expected)/(1+abs(actual)+abs(expected))})
    return residuals

mp.mp.dps=90
cases=[]
for a,N,k,phase in [(1.7,20,9,0.),(4.3,28,11,.317)]:
    lam=tune(a,1.,N,k,math,60,1e-10)
    doubleP=trajectory(a,1.,lam,N,phase,math)[:-1]
    aa=mp.mpf(str(a)); mp_lam=tune(aa,mp.mpf(1),N,k,mp,160,mp.mpf('1e-60'))
    preciseP=[tuple(map(float,p)) for p in trajectory(aa,mp.mpf(1),mp_lam,N,mp.mpf(str(phase)),mp)[:-1]]
    bad=moment_residuals(doubleP,a,1.,lam)
    repaired=moment_residuals(preciseP,a,1.,float(mp_lam))
    assert max(c['normalized_moment_residual'] for c in bad)>2e-8
    assert max(c['normalized_moment_residual'] for c in repaired)<2e-8
    cases.append({'case':[a,N,k,phase],'double_lambda':repr(lam),
                  'high_precision_caustic_gap':str(1-mp_lam),
                  'original_diagnostic':bad,'repaired_diagnostic':repaired})
result={'status':'EXPECTED_DOUBLE_PRECISION_FAILURES_REPRODUCED_AND_REPAIRED',
        'timestamp_utc':datetime.now(timezone.utc).isoformat(),'original_failure_exit_code':1,
        'normalized_threshold':2e-8,'cases':cases,
        'limitation':'Minimal generator reproducer reconstructed from original functions; original entire first-run source snapshot was not preserved.'}
Path(__file__).with_name('DOUBLE_PRECISION_FAILURE_REPRODUCTION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
