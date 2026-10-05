#!/usr/bin/env python3
"""Offline exact checks for the bounded largest-root note. Not a proof assistant."""
import argparse
import hashlib
import itertools
import json
import math
import random
from fractions import Fraction as F
from pathlib import Path
import sympy as S

T = S.Symbol('t')

def require(ok, message):
    if not ok:
        raise AssertionError(message)

def sf(x):
    return S.Rational(x.numerator, x.denominator) if isinstance(x, F) else S.Rational(x)

def product(rows):
    m = len(rows[0]); p = {(0,)*m:F(1)}
    for row in rows:
        q = {}
        for a,c in p.items():
            for i,v in enumerate(row):
                if v:
                    b=list(a);b[i]+=1;b=tuple(b)
                    q[b]=q.get(b,F(0))+c*v
        p=q
    return p

def directional(p):
    d=sum(next(iter(p))); q={}
    for a,c in p.items():
        for i,v in enumerate(a):
            if v:
                b=list(a);b[i]-=1;b=tuple(b)
                q[b]=q.get(b,F(0))+c*v/d
    return q

def cyclic_example(m,d):
    total=m*math.ceil(d/m)
    base=[F(0)]*m;base[0]=F(1,3);base[1]=F(2,3)
    rows=[[base[(j-i)%m] for j in range(m)] for i in range(total)]
    p=product(rows)
    for _ in range(total-d):p=directional(p)
    return p

def coefficients(p):
    m=len(next(iter(p)));d=sum(next(iter(p)));cs=[F(0)]*(min(m,d)+1)
    for a,c in p.items():
        es=[1]+[0]*min(m,d)
        for v in a:
            for k in range(len(es)-1,0,-1):es[k]+=v*es[k-1]
        for k,v in enumerate(es):cs[k]+=c*v
    return cs

def poly_from_coeffs(cs,d):
    return S.Poly(sum((-1)**k*sf(c)*T**(d-k) for k,c in enumerate(cs)),T)

def reference(m,d):
    return poly_from_coeffs([F(math.comb(m,k)*math.factorial(d)//math.factorial(d-k),m**k) for k in range(min(m,d)+1)],d)

def verify_margins(p):
    m=len(next(iter(p)));d=sum(next(iter(p)))
    require(sum(p.values())==1,'normalization')
    require(all(c>=0 for c in p.values()),'nonnegative coefficients')
    require(all(sum(c*a[i] for a,c in p.items())==F(d,m) for i in range(m)),'doubly stochastic gradient')
    require(all(sum(a)==d for a in p),'homogeneity')
    return m,d

def moment_check(p,cs):
    m,d=verify_margins(p);mu=F(d,m)
    mom2=sum(c*sum(v*v for v in a) for a,c in p.items())
    mom3=sum(c*sum(v*v*v for v in a) for a,c in p.items())
    theta2=m*(mu*mu+mu)-mom2
    theta3=(mom3-m*(mu**3+3*mu**2+mu)+3*(mu+1)*theta2)/2
    delta2=theta2-F(d,m);delta3=theta3-F(d,m*m)
    require(delta2>=0,'Delta2 nonnegative')
    require(0<=delta3<=(min(F(1),mu)+F(2,m))*delta2,'Delta3 bound')
    ref=coefficients_reference(m,d)
    if min(m,d)>=2:require(cs[2]-ref[2]==delta2/2,'second coefficient identity')
    if min(m,d)>=3:require(cs[3]-ref[3]==(F(d,2)-mu-1)*delta2+F(2,3)*delta3,'third coefficient identity')
    return {'delta2':str(delta2),'delta3':str(delta3)}

def coefficients_reference(m,d):
    return [F(math.comb(m,k)*math.factorial(d)//math.factorial(d-k),m**k) for k in range(min(m,d)+1)]

def isolated(f):
    intervals=f.intervals(eps=S.Rational(1,10**14))
    require(sum(k for _,k in intervals)==f.degree(),'all roots are real, exactly counted')
    return intervals

def interval_horner(f,lo,hi):
    a=b=S.Rational(0)
    for c in f.all_coeffs():
        choices=[a*lo,a*hi,b*lo,b*hi]
        a=min(choices)+c;b=max(choices)+c
    return a,b

def compare(p,name,flow=False):
    m,d=verify_margins(p);cs=coefficients(p);f=poly_from_coeffs(cs,d);q=reference(m,d)
    bounds=isolated(f);refbounds=isolated(q);(l,u),mult=bounds[-1];(rl,ru),_=refbounds[-1]
    eq=f==q
    require(eq or u<rl,'largest-root comparison separated exactly')
    out={'name':name,'m':m,'d':d,'coefficients':[str(c) for c in cs],
         'largest_root_interval':[str(l),str(u)],'reference_interval':[str(rl),str(ru)],
         'comparison':'equal polynomials' if eq else 'strictly below',**moment_check(p,cs)}
    if flow:
        if mult!=1:out['flow_check']='not evaluated: multiple largest root'
        else:
            h=S.Poly((m*T-m+d-1)*f.diff().as_expr()-T*f.diff().diff().as_expr(),T)
            if h.rem(f).is_zero:out['flow_check']='zero velocity by exact polynomial identity'
            else:
                hl,hu=interval_horner(h,l,u)
                out['flow_numerator_interval']=[str(-hu),str(-hl)]
                out['flow_check']='strictly positive velocity' if hu<0 else 'not certified positive'
    return out

def symbolics():
    d,m,u=S.symbols('d m u',positive=True)
    q3=T**3-d*T*T+d*(d-1)*T/3-d*(d-1)*(d-2)/27
    require(S.expand(q3.subs(T,d/3+u)-(u**3-d*u/3-2*d/27))==0,'m=3 centered cubic')
    qd=T**3-3*T*T+3*(m-1)*T/m-(m-1)*(m-2)/m**2
    require(S.factor(qd.subs(T,1+u)-(u**3-3*u/m-2/m**2))==0,'d=3 centered cubic')
    require(S.factor(q3.subs(T,d/3+S.Rational(2,9))-(S.Rational(8,729)-4*d/27))==0,'m=3 witness sign expression')
    require(S.factor(qd.subs(T,1+2/(3*m))-(8/(27*m**3)-4/m**2))==0,'d=3 witness sign expression')
    theta,a=S.symbols('theta a')
    require(S.expand((theta-a)**2*(theta+2*a)-(theta**3-3*a*a*theta+2*a**3))==0,'cubic deviation identity')
    # Independent subset differentiation for non-product and product examples.
    for mm,dd in [(2,5),(3,3),(5,3),(4,4)]:
        p=cyclic_example(mm,dd);x=S.symbols('x:'+str(mm))
        poly=sum(sf(c)*S.prod(v**e for v,e in zip(x,alpha)) for alpha,c in p.items())
        direct=poly
        for v in x:direct=S.expand(direct-S.diff(direct,v))
        direct=S.Poly(direct.subs(dict.fromkeys(x,T)),T)
        f=poly_from_coeffs(coefficients(p),dd)
        require(direct==f,'independent differential operator check')
        tp=S.expand(sum(x)*sum(S.diff(poly,v) for v in x)/(mm*dd))
        direct_t=tp
        for v in x:direct_t=S.expand(direct_t-S.diff(direct_t,v))
        direct_t=S.Poly(direct_t.subs(dict.fromkeys(x,T)),T)
        formula=S.Poly(((mm*T-mm+dd-1)*f.diff().as_expr()-T*f.diff().diff().as_expr())/(mm*dd),T)
        require(direct_t==formula,'exact resampling-operator identity')
    for n in range(1,7):
        require(reference(1,n).as_expr()==T**n-n*T**(n-1),'one-variable boundary')
        require(reference(n,1).as_expr()==T-1,'degree-one boundary')
    return {'centered_cubics':'pass','moment_deviation_identity':'pass','direct_operator_crosschecks':4,'boundary_checks':12}

def negative_controls():
    x,y,z,w=S.symbols('x y z w')
    p=(x+y)**2*(z+w)**2/16
    q=((x+y)**2*(z+w)**2+(x+z)**2*(y+w)**2+(x+w)**2*(y+z)**2)/48
    badspecial=S.factor(q.subs({x:T,y:-1,z:0,w:1}))
    require(S.expand(badspecial-(T*T+1)/24)==0,'averaging specialization')
    require(S.Poly(badspecial,T).count_roots(-S.oo,S.oo)==0,'average has nonreal specialization roots')
    cp=p;cq=q
    for v in [x,y,z,w]:cp=S.expand(cp-S.diff(cp,v));cq=S.expand(cq-S.diff(cq,v))
    cp=S.factor(cp.subs({x:T,y:T,z:T,w:T}));cq=S.factor(cq.subs({x:T,y:T,z:T,w:T}))
    require(cp==cq and S.expand(cp-(T*T-2*T+S.Rational(1,2))**2)==0,'unchanged chi under averaging')
    pinf=(x+y)**2/4
    def chi2(expr):
        for v in [x,y]:expr=S.expand(expr-S.diff(expr,v))
        return S.Poly(expr.subs({x:T,y:T}),T)
    bad=chi2(2*x*y-pinf);good=chi2((x*y+pinf)/2)
    require(bad.as_expr()==T*T-2*T+S.Rational(3,2),'printed flow control')
    require(bad.count_roots(-S.oo,S.oo)==0,'printed flow loses real-rootedness')
    require(good.as_expr()==T*T-2*T+S.Rational(3,4),'corrected flow control')
    require(good.eval(S.Rational(3,2))==0 and good.eval(S.Rational(1,2))==0,'corrected flow largest root 3/2')
    # Reject wrong normalizations and changed formula signs; these are intentional tests.
    rejections=0
    for condition in [S.discriminant(bad.as_expr(),T)>=0,
                      S.Poly(badspecial,T).count_roots(-S.oo,S.oo)==2,
                      good.eval(1)==0,
                      S.Rational(8,729)-S.Rational(4,9)>0]:
        try:require(condition,'deliberately false claim')
        except AssertionError:rejections+=1
    require(rejections==4,'all deliberate false claims rejected')
    return {'permutation_average_specialization':str(badspecial),'same_chi':str(cp),
            'wrong_flow_chi':str(bad.as_expr()),'corrected_flow_chi':str(good.as_expr()),'false_claims_rejected':rejections}

def run():
    checks=[]
    for m,d in [(2,d) for d in range(2,9)]+[(3,d) for d in range(3,10)]+[(m,d) for m in range(4,8) for d in [2,3]]:
        checks.append(compare(cyclic_example(m,d),f'cyclic-derived-{m}-{d}'))
    rng=random.Random(30003442)
    for n in [4,5,6]:
        for sample in range(12):
            k=2+sample%5;rows=[[F(0) for _ in range(n)] for _ in range(n)]
            perms=[]
            for _ in range(k):
                perm=list(range(n));rng.shuffle(perm);perms.append(perm)
                for i,j in enumerate(perm):rows[i][j]+=F(1,k)
            rec=compare(product(rows),f'permutation-average-{n}-{sample}',flow=True)
            rec['permutations']=perms;checks.append(rec)
    return {'problem_id':'30003442','scope':'partial theorem min(m,d)<=3; finite tests are not a general proof',
            'symbolic':symbolics(),'negative_controls':negative_controls(),
            'exact_examples':checks,'exact_example_count':len(checks),
            'product_search_count':36,'all_exact_largest_root_comparisons':'pass',
            'unrestricted_target':'unresolved','novelty':'not claimed'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--self-test',action='store_true');ap.add_argument('--output');args=ap.parse_args()
    value={'negative_controls':negative_controls(),'status':'pass'} if args.self_test else run()
    text=json.dumps(value,indent=2,sort_keys=True)+'\n'
    if args.output:Path(args.output).write_text(text)
    else:print(text,end='')

if __name__=='__main__':main()
