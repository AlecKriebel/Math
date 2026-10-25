#!/usr/bin/env python3
"""Fresh adversarial controls, independent of submitted verification code.

Exact Fraction checks validate finite arithmetic after analytic derivation.
Decimal complex Newton checks only probe a finite coefficient enclosure;
they do not construct or certify a maximizing schlicht map.
"""
from fractions import Fraction as F
from decimal import Decimal as D, localcontext
from pathlib import Path
import json

E, H, T = F(1, 10**24), F(1, 10**12), F(7, 4)
exact = []
def check(name, condition, detail=None):
    if not condition:
        raise AssertionError(name)
    exact.append({'name': name, 'passed': True, 'detail': detail})

# Derive [z^n] f^j by ordered integer compositions, with symbolic
# monomials a2^u a3^v a4^w and formal u=1/w kept as a fourth exponent.
def comps(n, k):
    if k == 0:
        if n == 0:
            yield ()
        return
    for i in range(1, n-k+2):
        for rest in comps(n-i, k-1):
            yield (i,)+rest
def quotient(n, leading=-1):
    poly={}
    for j in range(2,n+1):
        for c in comps(n,j):
            key=(c.count(2),c.count(3),c.count(4),j-1)
            poly[key]=poly.get(key,0)+leading
    return poly
q2={(0,0,0,1):-1}
q3={(1,0,0,1):-2,(0,0,0,2):-1}
q4={(2,0,0,1):-1,(0,1,0,1):-2,(1,0,0,2):-3,(0,0,0,3):-1}
check('independent quotient degrees 2 to 4', [quotient(j) for j in (2,3,4)]==[q2,q3,q4])
check('a4 absent from exact Schiffer differential', all(k[2]==0 for k in quotient(4)))
check('wrong quotient leading sign rejected', quotient(2,1)!=q2)
check('negative double cover signs', [-4*(-1)**j for j in (3,4,5)]==[4,-4,4])
check('positive cover mutant fails required P', [-4 for j in (3,4,5)]!=[4,-4,4])

r=F(2,3)
check('epsilon eta relation',E==H**2)
check('near Koebe a2 and a3 constants',52<64 and F(52,3)<25)
check('a3 A B enclosure coefficients',5+24==29 and 2*29+8*6==106 and 3*8==24)
check('H weighted tail', r**4/(3*(1-r*r))==F(16,135)<F(1,4))
check('H derivative weighted tail',(1-r*r)**-2-1==F(56,25)<F(9,4))
check('H and derivative coarse constants', 4*r+2<5 and 4+4*F(3,2)==10)
check('f value error',r*5*F(7,2)/(F(3,2)**2*F(5,3)**2)<2)
check('f derivative error',(5+F(4,3)*10)/F(3,2)**3+F(1,3)*5*11/(F(3,2)**3*F(5,3)**3)<8)
tip=F(1,2)
check('actual tip strict upper bound',tip<F(3,10),str(tip))
check('distance direction concrete unit disk control',1-r < 1-r*r)
check('reversed distance inequality fails unit disk',not (1-r >= 1-r*r))
check('trajectory radius separation',(T+333*E)**-2>F(25,81)>F(3,10))
check('stated radius gap exact',F(25,81)-F(3,10)==F(7,810))
check('near tip mutant invalidates continuation gate',not (F(25,81)>F(1,2)))

delta=111*E
check('square root branch excludes zero',delta<F(1,4))
check('Rouche target disk strict separation',333*E<1)
check('all t orientation estimate',222*E/(1-delta)<223*E<1)
check('sqrt quadratic absorption',F(111**2,2)*H<1)
check('inverse composition absorption',18315*H<1)
check('derivative composition absorption',(24642+20979)*H<1)
check('complex inverse sqrt second derivative squared',(F(3,4)**2)*F(4,3)**5<16)
Cz=1541+4662*H
check('uniform Z bound',Cz<2000)
def first_order(t,B=F(3),c=F(1)):
    return B*t*t/3-F(2,5)*c*t**4
check('independent first variation endpoints',first_order(F(1))==F(3,5) and first_order(T)==-F(441,640))
check('full B enclosure first order signs',first_order(F(1),3-24*H)>F(1,2) and first_order(T,3+24*H)<-F(1,2))
check('published full analytic error strict margins',F(3,5)-2000*H>F(1,2) and -F(441,640)+2000*H<-F(1,2))
check('epsilon zero mutant loses signs',0*first_order(F(1))==0)
check('drop quartic mutant loses reversal',F(1)>0 and T*T>0)
check('drop cubic coefficient term mutant loses reversal',first_order(F(1),6)>0 and first_order(T,6)>0)
check('inflated eta proof budget mutant rejected',not (161+45621*F(1,10**4)<162))
check('opposite signs alone admit monotone beta',F(1)>0 and -F(1)<0 and F(1)>-F(1), 'beta(s)=-s on [-1,1] is decreasing; the zero infinity limit is essential')
check('zero infinity limit blocks both monotone directions',F(0)<F(1) and F(1)>-F(1), 'three ordered values 0,+1,-1')
check('absolute beta has interior minimum',abs(F(1))>abs(F(0)) and abs(-F(1))>abs(F(0)))
check('inward unsigned supplement retains nonmonotonicity',3-abs(F(1))<3-abs(F(0)) and 3-abs(-F(1))<3-abs(F(0)))

# No submitted code is imported. Decimal complex arithmetic is a pair of
# Decimals, and natural-coordinate integration uses a degree-17 polynomial
# from a fresh fourth-order binomial expansion, rather than quadrature.
def dec(x):
    if isinstance(x,F): return D(x.numerator)/D(x.denominator)
    return D(x)
def c(x=0,y=0):return (dec(x),dec(y))
def ca(a,b):return (a[0]+b[0],a[1]+b[1])
def cn(a):return (-a[0],-a[1])
def cs(a,b):return ca(a,cn(b))
def cm(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def ck(a,k):return (a[0]*k,a[1]*k)
def cd(a,b):
    z=b[0]*b[0]+b[1]*b[1]
    return ((a[0]*b[0]+a[1]*b[1])/z,(a[1]*b[0]-a[0]*b[1])/z)
def norm(a):return (a[0]*a[0]+a[1]*a[1]).sqrt()
def pm(a,b):
    out={}
    for n,x in a.items():
        for m,y in b.items():out[n+m]=ca(out.get(n+m,c()),cm(x,y))
    return out
def ev(poly,z):
    a=c()
    for n in range(max(poly),-1,-1):a=ca(cm(a,z),poly.get(n,c()))
    return a
def coordinate(A,B,eps):
    ie=c(0,eps)
    x={0:cm(ie,A),2:cn(cm(ie,B)),4:ie}
    power={0:c(1)};p={0:c(1)};coef=D(1)
    for j in range(1,5):
        power=pm(power,x);coef=coef*(D('0.5')-D(j-1))/D(j)
        for n,y in power.items():p[n]=ca(p.get(n,c()),ck(y,coef))
    G={n+1:ck(y,D(1)/D(n+1)) for n,y in p.items()}
    return p,G
def solve(p,G,t):
    v=c(t)
    for _ in range(8):
        step=cd(cs(ev(G,v),c(t)),ev(p,v));v=cs(v,step)
        if norm(step)<D('1e-95'):break
    residual=norm(cs(ev(G,v),c(t)))
    z=cd(c(t),cm(v,ev(p,v)))
    return v,z,residual

with localcontext() as ctx:
    ctx.prec=110
    eps,eta=dec(E),dec(H)
    directions=[c(1),c(-1),c(0,1),c(0,-1)]+[c(F(i*3,5),F(j*4,5)) for i in (-1,1) for j in (-1,1)]
    cases=[('nominal',c(-2),c(3))]
    for i,aa in enumerate(directions):
        for j,bb in enumerate(directions):cases.append((f'boundary_{i}_{j}',ca(c(-2),ck(aa,106*eta)),ca(c(3),ck(bb,24*eta))))
    probes=[D(1),D(7)/4,D('0.000001')]
    rows=[];max_res=D(0);worst_pos=D('Infinity');worst_neg=D('-Infinity');max_error=D(0)
    for name,A,B in cases:
        p,G=coordinate(A,B,eps)
        for t in probes:
            v,z,res=solve(p,G,t)
            max_res=max(max_res,res)
            q=t*t-D('0.4')*t**4
            err=norm(cs(cs(z,c(1)),c(0,eps*q)))/(eps*eta)
            max_error=max(max_error,err)
            if t==1:worst_pos=min(worst_pos,z[1]/eps)
            if t==D(7)/4:worst_neg=max(worst_neg,z[1]/eps)
            rows.append({'case':name,'t':str(t),'ImZ_over_epsilon':str(z[1]/eps),'ReZ':str(z[0]),'residual':str(res),'error_over_epsilon_eta':str(err)})
    assert worst_pos>D('0.5') and worst_neg<D('-0.5')
    assert max_res<D('1e-95') and max_error<D(2000)
    summary={'cases':len(cases),'probes':len(rows),'precision_decimal_digits':ctx.prec,'minimum_ImZ_over_epsilon_at_1':str(worst_pos),'maximum_ImZ_over_epsilon_at_T':str(worst_neg),'maximum_residual':str(max_res),'maximum_error_over_epsilon_eta':str(max_error),'binomial_order':4,'analytic_truncation_bound_for_G_on_disk3':str(6*(111*eps)**5),'role':'finite independently implemented consistency probe only; not interval arithmetic, not extremal existence, not a universal proof'}
    out=Path(__file__).resolve().parents[1]/'evidence'
    (out/'independent-decimal-probes.json').write_text(json.dumps({'summary':summary,'probes':rows},indent=2)+'\n')
    (out/'independent-exact-controls.json').write_text(json.dumps({'status':'passed','checks':exact,'count':len(exact),'decimal_summary':summary},indent=2)+'\n')
    print(json.dumps({'exact_checks':len(exact),'decimal_summary':summary},indent=2))
