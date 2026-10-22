from fractions import Fraction as F
import json, math, sys
from pathlib import Path
R=Path(__file__).resolve().parent
def need(v,msg):
    if not v:raise RuntimeError(msg)
def transpose(a):return list(map(list,zip(*a)))
def mul(a,b):return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in transpose(b)] for row in a]
def sub(a,b):return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]
def eye(n):return [[F(i==j) for j in range(n)]for i in range(n)]
def trace(a):return sum((a[i][i]for i in range(len(a))),F(0))
# Independent exact Gaussian tensor-projection family. Brownian increment
# covariance is T/m I, observation operator aggregates each block of k cells.
# For independent x,y, Var(x^t K y)=tr(K^t C K C); conditioning both block sums
# projects each tensor leg by the block-averaging orthogonal projector.
rows=[]
for n,k,T in [(1,2,F(1)),(1,5,F(3,2)),(2,3,F(5,7)),(3,4,F(2)),(5,2,F(7,3))]:
    m=n*k;K=[[F(1)if i<j else F(1,2)if i==j else F(0)for j in range(m)]for i in range(m)]
    Q=[[F(1,k)if i//k==j//k else F(0)for j in range(m)]for i in range(m)]
    projected=mul(mul(Q,K),Q);res=sub(K,projected)
    residual=sum((x*x for row in res for x in row),F(0))*(T/m)**2
    expected=T*T*F(k-1,4*n*k)
    need(residual==expected,'Brownian finite polygon tensor residual')
    need(mul(Q,Q)==Q,'Observation projector idempotence')
    # The full tensor conditional expectation reduces to the coarse trapezoid.
    coarse=[[F(1)if i//k<j//k else F(1,2)if i//k==j//k else F(0)for j in range(m)]for i in range(m)]
    need(projected==coarse,'Bilinear conditional estimator/coarse trapezoid')
    # Removing the half-increment diagonal changes the observable expectation.
    wrong=[[F(i<j)for j in range(m)]for i in range(m)]
    need(mul(mul(Q,wrong),Q)!=projected,'Half-correction adversary')
    rows.append({'n':n,'refinement':k,'T':str(T),'exact_residual_variance':str(residual),'canonical_limit_variance':str(T*T/F(4*n)),'conditional_projection_exact':True})
# Second new family: exact nonnested finite pairing, with Delta=1 so no
# irrational scaling enters. Fixed n deterministic sums are evaluated without
# assuming m shares any observation times other than the endpoints.
phi=[F(0)]*4+[F(1),F(-4),F(6),F(-4),F(1)]
def deriv(p):return [i*p[i]for i in range(1,len(p))]
f=deriv(phi)
def val(p,x):
    if x<0 or x>1:return F(0)
    return sum((a*x**i for i,a in enumerate(p)),F(0))
pairings=[]
for n in [1,2,3]:
    for m in [5,11,23,47,95]:
        total=F(0)
        for j in range(n):
            total+=sum((val(f,F(k*n,m)-j)*(val(phi,F((k+1)*n,m)-j)-val(phi,F(k*n,m)-j))for k in range(m)),F(0))
        target=n*F(4,45045)
        pairings.append({'n':n,'m':m,'sum':str(total),'target':str(target),'absolute_error':float(abs(total-target))})
    need(pairings[-1]['absolute_error']<pairings[-5]['absolute_error'],'Nonnested deterministic pairing convergence diagnostic')
out={'status':'PASS','family_1':'Exact independent Gaussian tensor conditional projection of finite Brownian polygons; no rough increment coercivity','tensor_controls':rows,'family_2':'Exact rational nonnested left-pairing grids for fixed n, independent from supplied checker','pairing_controls':pairings,'deduced_Brownian_limit':'T²/(4n) residual variance, RMS=T/(2 sqrt(n)); this agrees with attributed prior optimum','universal_proof':'Independent analytic reconstruction, not these finite tests','not_interval_bounds':True}
(R/'NEW_MATH_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','tensor_cases':len(rows),'nonnested_pairings':len(pairings)}))
