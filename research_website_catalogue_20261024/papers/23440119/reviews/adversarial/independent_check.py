#!/usr/bin/env python3
"""Independent pre-support adversarial checks. Python standard library only.

This file was written without consulting submitted checkers, proof supplements,
or previous reviews. Polynomial checks use a small sparse ring Z[s,t]. Numerical
attacks use Fraction, direct derivatives of p=x*y*y-z*z*z, and no printed matrix.
"""
from fractions import Fraction as Q
from itertools import combinations
import hashlib, json, math, random
from pathlib import Path

class Poly:
    def __init__(self, x=0):
        self.d = {k:v for k,v in x.items() if v} if isinstance(x,dict) else ({(0,0):x} if x else {})
    def __add__(self,o):
        o=poly(o); d=self.d.copy()
        for k,v in o.d.items(): d[k]=d.get(k,0)+v
        return Poly(d)
    __radd__=__add__
    def __neg__(self): return Poly({k:-v for k,v in self.d.items()})
    def __sub__(self,o): return self+-poly(o)
    def __rsub__(self,o): return poly(o)+-self
    def __mul__(self,o):
        o=poly(o); d={}
        for (i,j),v in self.d.items():
            for (k,l),w in o.d.items(): d[i+k,j+l]=d.get((i+k,j+l),0)+v*w
        return Poly(d)
    __rmul__=__mul__
    def __pow__(self,n):
        out=Poly(1)
        for _ in range(n): out=out*self
        return out
    def __eq__(self,o): return self.d==poly(o).d
    def at(self,s,t): return sum(v*s**i*t**j for (i,j),v in self.d.items())
def poly(x): return x if isinstance(x,Poly) else Poly(x)

def det(A):
    if len(A)==1: return A[0][0]
    return sum((-1)**j*A[0][j]*det([row[:j]+row[j+1:] for row in A[1:]]) for j in range(len(A)))

def p_derivatives(q):
    x,y,z=q
    p=x*y*y-z*z*z
    dp=[y*y,2*x*y,-3*z*z]
    dd=[[0,2*y,0],[2*y,2*x,0],[0,0,-6*z]]
    ddd=[[[0 for k in range(3)] for j in range(3)] for i in range(3)]
    for i,j,k in [(0,1,1),(1,0,1),(1,1,0)]: ddd[i][j][k]=2
    ddd[2][2][2]=-6
    return p,dp,dd,ddd

def curvature_numerator(q,h,include_z=True):
    """Exactly -p(q)^3 D^3(-log(p)-log(z))[h], from raw p derivatives."""
    p,dp,dd,ddd=p_derivatives(q)
    dh=sum(dp[k]*h[k] for k in range(3))
    dhi=[sum(dd[i][k]*h[k] for k in range(3)) for i in range(3)]
    out=[]
    for i in range(3):
        row=[]
        for j in range(3):
            dhij=sum(ddd[i][j][k]*h[k] for k in range(3))
            v=2*dh*dp[i]*dp[j]-p*(dhi[i]*dp[j]+dhi[j]*dp[i]+dd[i][j]*dh)+p*p*dhij
            if include_z and i==j==2: v+=2*p**3*h[2]/q[2]**3 if not isinstance(p,Poly) else 2*p**3*h[2]
            row.append(v)
        out.append(row)
    return out

def hessian(q):
    p,dp,dd,_=p_derivatives(q)
    return [[dp[i]*dp[j]/p**2-dd[i][j]/p+(Q(1,q[2]**2) if i==j==2 else 0) for j in range(3)] for i in range(3)]
def bilinear(A,u,v): return sum(u[i]*A[i][j]*v[j] for i in range(3) for j in range(3))
def psd(A): return all(det([[A[i][j] for j in ix] for i in ix])>=0 for n in range(1,4) for ix in combinations(range(3),n))
def pd(A): return all(det([row[:n] for row in A[:n]])>0 for n in range(1,4))

def main():
    checks={}
    def check(name,b):
        checks[name]=bool(b)
        assert b,name
    s,t=Poly({(1,0):1}),Poly({(0,1):1}); r=s+1
    M=curvature_numerator([r,1,1],[t**3,1,t])
    displayed=[
        [2*(t-1)**2*(t+2),2*(t-1)*(2*t*t+2*t-1-3*r),6*(t-1)*(r-t*t-t+1)],
        [0,4*r**3+12*r*r-18*r*r*t+6*r*t**3-6*r*t+2*t**3,12*r*r*t-18*r*r-6*r*t**3+24*r*t-6*r-6*t**3],
        [0,0,6*(r+2)*t**3+2*(r**3-6*r*r-18*r-4)*t+12*r*(r+2)]]
    check('all_six_printed_matrix_entries_from_raw_tensor',all(M[i][j]==displayed[i][j] for i in range(3) for j in range(i,3)))
    P=2*(t+2)*s*s-3*(t-1)*(3*t+5)*s+3*(t-1)**2*(t+2)**2
    R=(t+2)*(2*t*s*s-3*(t-1)*(3*t+1)*s+3*(t-1)**2*(t*t+4*t+1))
    check('minor2',det([row[:2] for row in M[:2]])==4*s*(t-1)**2*P)
    check('minor3',det(M)==8*s**4*(t-1)**2*R)
    discP=(3*(t-1)*(3*t+5))**2-4*2*(t+2)*3*(t-1)**2*(t+2)**2
    discR=(3*(t-1)*(3*t+1))**2-4*2*t*3*(t-1)**2*(t*t+4*t+1)
    check('alternative_discriminant_P',discP==-3*(t-1)**2*(8*t**3+21*t*t+6*t-11))
    check('alternative_discriminant_R',discR==-3*(t-1)**3*(8*t*t+13*t+3))
    check('P_remainder_at_1_plus_v',all((8*t**3+21*t*t+6*t-11).at(0,Q(1)+Q(k,7))>0 for k in range(100)))
    a=[1,2,-3]; b=[0,1,-1]
    E=curvature_numerator([r,1,1],[1,0,0])
    check('endpoint_Gram',all(E[i][j]==2*a[i]*a[j]+6*s*b[i]*b[j] for i in range(3) for j in range(3)))
    special=[[0,0,0],[0,2*s*s*(2*r+1),-6*s*s],[0,-6*s*s,2*s*s*(r+2)]]
    check('t1_degeneracy',all(M[i][j].at(0,1)==poly(special[i][j]).at(0,1) for i in range(3) for j in range(3)))
    # Stronger direct identity at t=1 as a polynomial in s.
    check('t1_all_s_coefficients',all(Poly({(i,0):sum(v for (k,j),v in M[a0][b0].d.items() if k==i) for i in range(8)})==special[a0][b0] for a0 in range(3) for b0 in range(3)))
    grid=[Q(0),Q(1,10**6),Q(1,100),Q(1,2),Q(999999,10**6),Q(1),Q(1000001,10**6),Q(2),Q(100),Q(10**6)]
    sgrid=[Q(1,10**12),Q(1,10**6),Q(1,100),Q(1),Q(4),Q(100),Q(10**6),Q(10**12)]
    curvature_cases=0
    for ss in sgrid:
        for tt in grid:
            A=curvature_numerator([1+ss,Q(1),Q(1)],[tt**3,Q(1),tt])
            check(f'curvature_grid_{curvature_cases}',psd(A) and (tt==1 or pd(A)))
            curvature_cases+=1
    rng=random.Random(23440119)
    mixed_cases=0; rational_max_ratio=Q(0)
    for k in range(500):
        # Generic coordinates and arbitrary cone directions, not only normalized rays.
        y=Q(rng.randint(1,20),rng.randint(1,9)); z=Q(rng.randint(1,20),rng.randint(1,9))
        delta=Q(1,rng.choice([1,10,100,10000]))*rng.randint(1,10)
        q=[z**3/y**2+delta,y,z]
        hy=Q(rng.randint(1,10),rng.randint(1,7)); hz=Q(rng.randint(0,10),rng.randint(1,7))
        h=[hz**3/hy**2+Q(rng.randint(0,10),rng.randint(1,7)),hy,hz]
        A=curvature_numerator(q,h)
        check(f'generic_cone_curvature_{k}',psd(A))
        u=[Q(rng.randint(-30,30),rng.randint(1,11)) for _ in range(3)]
        v=[Q(rng.randint(-30,30),rng.randint(1,11)) for _ in range(3)]
        H=hessian(q); p=q[0]*q[1]**2-q[2]**3
        check(f'generic_hessian_pd_{k}',pd(H))
        d3=-bilinear(curvature_numerator(q,v),u,u)/p**3
        denom=bilinear(H,v,v)*bilinear(H,u,u)**2
        check(f'mixed_self_concordance_25_scale_{k}',d3*d3<=100*denom)
        if denom: rational_max_ratio=max(rational_max_ratio,d3*d3/denom)
        mixed_cases+=1
    f0=curvature_numerator([Q(5),Q(1),Q(1)],[Q(8),Q(1),Q(2)],False)
    check('omitted_log_z_is_detected',det(f0)==-24576)
    # A concrete negative-curvature failure after omitting the claimed repair term.
    u=[Q(9),Q(-3),Q(-2)]
    witness=bilinear(f0,u,u)
    # Search finite integral directions if this first independently chosen one misses.
    if witness>=0:
        for aa in range(-10,11):
            for bb in range(-10,11):
                for cc in range(-10,11):
                    vv=[Q(aa),Q(bb),Q(cc)]; w=bilinear(f0,vv,vv)
                    if w<0: u,witness=vv,w;break
                if witness<0: break
            if witness<0: break
    check('negative_control_has_exact_direction',witness<0)
    out={
        'status':'PASS independent finite and polynomial checks; not a substitute for the proof',
        'check_count':len(checks),'failed':[k for k,v in checks.items() if not v],
        'curvature_normalized_exact_cases':curvature_cases,'generic_exact_cases':mixed_cases,
        'mixed_ratio_max_float':float(rational_max_ratio),
        'omitted_log_z':{'matrix':[[str(v) for v in row] for row in f0],'determinant':str(det(f0)),
                         'u':[str(v) for v in u],'uT_M_u':str(witness),'D3f0_huu':str(-witness/Q(4)**3)},
        'all_checks':checks,
    }
    target=Path(__file__).with_name('independent-check-results.json')
    target.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='all_checks'},indent=2))
if __name__=='__main__': main()
