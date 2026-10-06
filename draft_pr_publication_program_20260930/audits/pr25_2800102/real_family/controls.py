#!/usr/bin/env python3
"""Exact direct de Bruijn/joint-law controls, independent of submitted scripts.
All matrix entries and moment coordinates are Fraction; decimals are illustrative.
"""
from fractions import Fraction as F
from math import factorial, comb, sqrt, pi, isqrt
from pathlib import Path
import json, hashlib, subprocess, sys
checks=[]
def ck(name, test):
    assert test, name
    checks.append(name)
def hg(k): # Gamma(k+1/2)/sqrt(pi)
    return F(factorial(2*k),4**k*factorial(k))
def partial_even(p,q): # integral 0 to pi/4 = a+b*pi
    if q:
        a,b=partial_even(p,q-2)
        return F(q-1,p+q)*a-F(1,2**((p+q)//2)*(p+q)),F(q-1,p+q)*b
    if p:
        a,b=partial_even(p-2,0)
        return F(p-1,p)*a+F(1,p*2**(p//2)),F(p-1,p)*b
    return F(0),F(1,4)
def angular_even(p,q):
    a,b=partial_even(p,q)
    total_pi=hg(p//2)*hg(q//2)/(2*factorial((p+q)//2))
    ck(f'angular_pi_cancels_{p}_{q}',total_pi==2*b)
    return -2*a
def angular_mixed(p,q): # D = a+b*sqrt(2), odd p, even q or opposite
    if p%2==0:
        a,b=angular_mixed(q,p); return -a,-b
    k=(p-1)//2
    total=F(0); partial=F(0)
    for l in range(k+1):
        v=F((-1)**l*comb(k,l),q+2*l+1)
        total+=v
        # integral at sin(pi/4): (1/sqrt2)^(q+2l+1)
        partial+=v/F(2**((q+2*l)//2))
    return total,-partial # 2*Ipartial= sqrt2*partial

def matrix_inverse(m):
    n=len(m); a=[row[:]+[F(i==j) for j in range(n)] for i,row in enumerate(m)]
    for j in range(n):
        k=next(k for k in range(j,n) if a[k][j]);a[j],a[k]=a[k],a[j]
        d=a[j][j];a[j]=[x/d for x in a[j]]
        for k in range(n):
            if k!=j:
                d=a[k][j];a[k]=[x-d*y for x,y in zip(a[k],a[j])]
    return [r[n:] for r in a]
def direct_real(n):
    # joint weight x^(-1/2)e^(-x/2), Vandermonde monomial determinant.
    size=n+n%2;m=[[F(0) for j in range(size)] for i in range(size)]
    dm=[[(F(0),)*4 for j in range(size)] for i in range(size)]
    for i in range(n):
        for j in range(n):
            m[i][j]=4*2**(i+j)*factorial(i+j)*angular_even(2*i,2*j)
            a,b=angular_mixed(2*i+1,2*j);c,d=angular_mixed(2*i,2*j+1)
            scale=4*2**(i+j)*hg(i+j+1)
            # radial sqrt2*sqrt(pi): sqrtpi coordinates (2*b,a)
            dm[i][j]=(scale*2*(b+d),scale*(a+c),F(0),F(0))
        if n%2:
            # rescale de Bruijn border by 1/sqrt(2pi), giving rational M.
            m[i][n]=2**i*hg(i);m[n][i]=-m[i][n]
            dm[i][n]=(F(0),F(0),F(0),F(2**i*factorial(i)))
            dm[n][i]=tuple(-x for x in dm[i][n])
    inv=matrix_inverse(m)
    return tuple(sum((inv[i][j]*dm[j][i][k]/2 for i in range(size) for j in range(size)),F(0)) for k in range(4))
def lagpoly(n):return [F((-1)**k*comb(n,k),factorial(k)) for k in range(n+1)]
def mixed_half(r,s):
    return sum((a*b*hg(i+j+1) for i,a in enumerate(lagpoly(r)) for j,b in enumerate(lagpoly(s))),F(0))
def cx(n):return sum((mixed_half(k,k) for k in range(n)),F(0))
def phi_real(n):
    # Independently integrate printed density formula, exact even gamma integrals.
    eps=n%2; poly=lagpoly(n-1); jp=F(0)
    for m in range((n+eps-2)//2+1):
        s=2*m+1-eps
        if eps: w=2*hg(m)/factorial(m) # w/sqrtpi
        else: w=F(2*factorial(m),1)/hg(m+1) # w*sqrtpi
        jp+=w*mixed_half(n-1,s)
    if eps:
        j2=sum((a*2**(j+1)*factorial(j) for j,a in enumerate(poly)),F(0))
        ratio=F(factorial((n-1)//2),1)/hg((n-1)//2)/2
        # Phi1 integral pi*jp, Phi2 integral sqrt2*j2; ratio /sqrtpi
        return (cx(n)-ratio*jp,F(0),F(0),ratio*j2)
    # I_j = integral x^j e^(-x/2)erfc(sqrt(x/2)) = a+b sqrt2.
    ints=[];a,b=F(2),F(-1)
    for j in range(n):
        if j:
            a*=2*j;b=2*j*b-hg(j) # gamma(j+1/2)/sqrtpi factor sqrt2
        ints.append((a,b))
    a=sum((co*(2*ints[j][0]-2**(j+1)*factorial(j)) for j,co in enumerate(poly)),F(0))
    b=sum((co*2*ints[j][1] for j,co in enumerate(poly)),F(0))
    ratio=hg(n//2)/(2*factorial(n//2-1)) # density gamma_ratio /sqrtpi
    # J=jp - sqrt2*(a+b sqrt2)
    return (cx(n)-ratio*(jp-2*b),ratio*a,F(0),F(0))
def coordinates_value(c):return sqrt(pi)*(float(c[0])+float(c[1])*sqrt(2))+(float(c[2])+float(c[3])*sqrt(2))/sqrt(pi)
rows=[]
for n in range(1,9):
    direct=direct_real(n);printed=phi_real(n)
    ck(f'LOE_direct_joint_vs_printed_density_N{n}',direct==printed)
    rows.append({'N':n,'raw_Y_coordinates':[str(x) for x in direct],'basis':['sqrt(pi)','sqrt(2pi)','1/sqrt(pi)','sqrt(2/pi)'],'alpha_illustrative':coordinates_value(direct)/n**1.5})
ck('raw_Y_1',direct_real(1)==(F(0),F(0),F(0),F(1)))
ck('raw_Y_2',direct_real(2)==(F(2),F(-1,2),F(0),F(0)))
# AP ODE/recurrence reconstructed coefficientwise from positive convolution.
b=[F(1)]
for j in range(1,41):b.append(b[-1]*F(2*j-3,2*j)) # sigma_j
h=[hg(j+1)/factorial(j) for j in range(41)]
y=[F(0)]
for n in range(1,42):y.append(y[-1]+sum((b[n-1-k]**2*h[k] for k in range(n)),F(0)))
for n in range(1,41):ck(f'AP_positive_convolution_recurrence_{n}',n*n*(y[n+1]-2*y[n]+y[n-1])==F(3,4)*y[n])
# Coefficient inequalities driving AP Lemma6; exact tested margins supplement general proof.
for j in range(3,80):
    lam=F(128,3)
    k=2*j+4
    for i in range(k):lam*=F(3,2)-i
    lam/=factorial(k)
    ck(f'AP_lambda_bound_{j}',0<lam<F(1,3*(j+1)))
# Universal coefficient ratio polynomial proof via shifted coefficient expansion.
ck('ratio_polynomial_shift_coefficients',[4,32,71,37]==[4,4*9-4,4*27-8*3-13,4*27-4*9-39+4])
ck('uniform_reserve_rational',F(4,5)**3>F(7,10)**2 and F(7,10)/(32*F(22,7))>F(1,160))
# Rational interval controls for exact real increments; no float in certification.
def iadd(x,y):return (x[0]+y[0],x[1]+y[1])
def imul(x,y):
    z=[a*b for a in x for b in y];return min(z),max(z)
def idiv(x,y):
    assert y[0]>0;return imul(x,(1/y[1],1/y[0]))
def iscale(x,c):return imul(x,(c,c))
def isub(x,y):return (x[0]-y[1],x[1]-y[0])
def sroot(q):
    scale=10**35;k=isqrt(q.numerator*scale*scale//q.denominator)
    return F(k,scale),F(k+1,scale)
def iroot(x):return sroot(x[0])[0],sroot(x[1])[1]
def atan_inv(q, terms=55):
    z=sum((F((-1)**k,(2*k+1)*q**(2*k+1)) for k in range(terms)),F(0))
    nxt=F((-1)**terms,(2*terms+1)*q**(2*terms+1))
    return min(z,z+nxt),max(z,z+nxt)
pi_i=isub(iscale(atan_inv(5),F(16)),iscale(atan_inv(239),F(4)))
ck('Machin_pi_range',pi_i[0]>F(157,50) and pi_i[1]<F(22,7))
s2=sroot(F(2));sp=iroot(pi_i);invsp=idiv((F(1),F(1)),sp)
def alpha_interval(c,n):
    t=iadd(iscale(sp,c[0]),iscale(imul(sp,s2),c[1]))
    t=iadd(t,iadd(iscale(invsp,c[2]),iscale(imul(invsp,s2),c[3])))
    return idiv(t,iscale(sroot(F(n)),F(n)))
bounded=[]
for n in range(1,8):
    inc=isub(alpha_interval(direct_real(n+1),n+1),alpha_interval(direct_real(n),n))
    ck(f'validated_real_increment_reserve_N{n}',inc[0]>F(1,160*n*n))
    bounded.append({'N':n,'increment_lower':str(inc[0]),'increment_upper':str(inc[1]),'target':str(F(1,160*n*n))})
# replay original controls in ignored workspace, compare exact receipts
p=Path(__file__).resolve().parent; snap=p.parent/'source_snapshot'
replay=[]
for f in ['verify.py','review/submitted_verify.py','review/independent_checks.py']:
    dest=p/'tmp'/f.replace('/','_');dest.write_bytes((snap/f).read_bytes())
    run=subprocess.run([sys.executable,str(dest)],capture_output=True,text=True,check=True)
    replay.append({'file':f,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'stdout':run.stdout.strip(),'returncode':run.returncode})
(p/'CONTROL_RESULTS.json').write_text(json.dumps({'status':'passed','total_exact_assertions':len(checks),'new_control_scope':'direct joint-law half-moments N1..8; independently integrated density; AP convolution recurrence N1..40; bounded AP coefficients and universal scalar polynomial proof controls; finite controls do not extrapolate','direct_real':rows,'validated_real_increments':bounded,'pi_interval':[str(x) for x in pi_i],'original_replays':replay,'checks':checks},indent=2)+'\n')
print(json.dumps({'status':'passed','assertions':len(checks),'rows':rows,'original_replays':replay},indent=2))
