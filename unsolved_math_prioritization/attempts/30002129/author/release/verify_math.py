#!/usr/bin/env python3
"""Exact finite controls for a partial investigation; never a universal proof."""
from fractions import Fraction as F
from itertools import combinations, product
from math import gcd, lcm
import json

CHECKS=0
def check(ok, message):
    global CHECKS
    CHECKS += 1
    if not ok: raise RuntimeError(message)

def configurations(nx,ny):
    n=nx+ny
    for rest in combinations(range(1,n),nx-1):
        xs={0,*rest}
        yield ''.join('X' if i in xs else 'Y' for i in range(n))

def tables(W,p,u):
    n=len(W)
    pos={c:[i for i,x in enumerate(W) if x==c] for c in 'XY'}
    out=[]
    for c,shift in [('X',p),('Y',u)]:
        cc=pos[c];d=len(cc);tab=[]
        for i in range(n):
            j=next((k for k,v in enumerate(cc) if v>=i),d)
            q,z=divmod(j+shift,d)
            tab.append(q*n+cc[z])
        out.append(tab)
    return out

def rot(W,word,p,u):
    n=len(W);a,b=tables(W,p,u)
    seq=[a if c=='a' else b for c in word[::-1]]
    def step(x):
        for t in seq:
            q,z=divmod(x,n);x=q*n+t[z]
        return x
    seen={};x=k=0
    while x%n not in seen:
        seen[x%n]=(k,x);x=step(x);k+=1
    j,y=seen[x%n]
    return F(x-y,(k-j)*n)

def upper(word,r,s, all_values=False):
    vals=[(rot(W,word,r.numerator,s.numerator),W) for W in configurations(r.denominator,s.denominator)]
    return vals if all_values else max(x for x,_ in vals)

def jn(r,s):
    # L=lcm denominators gives candidate r+s+1/L. For k>L, any
    # floor-sum candidate <=r+s+1/k<that candidate. Thus k<=L suffices.
    L=lcm(r.denominator,s.denominator)
    return max(F((r*k).__floor__()+(s*k).__floor__()+1,k) for k in range(1,L+1))

def pairs(word):
    return sum(word[i]=='a' and word[(i+1)%len(word)]=='b' for i in range(len(word)))

def main():
    rats=sorted({F(p,q) for q in range(1,6) for p in range(q)})
    words=['ab','aab','abb','aabb','abab','abaab','abbab','aaabbb','abaabb','aababab','abaababb','abaabbabbbababaab']
    trials=0;tested_configs=0;max_defect=F(0);witness=None;nonextreme=None
    for r,s in product(rats,repeat=2):
        ab=upper('ab',r,s)
        check(ab==jn(r,s),f'JN mismatch {r},{s}')
        for w in words:
            vals=upper(w,r,s,True);R=max(x for x,_ in vals);A=w.count('a');B=w.count('b');m=pairs(w);d=R-A*r-B*s;q=R.denominator
            check(d>=0,'linear lower bound')
            check(q<=min(r.denominator,s.denominator),'rationality denominator')
            check(d<=F(m,q),'finite refined bound')
            if q in (r.denominator,s.denominator):check(d<=F(m,q),'full-period special case')
            check(R==upper(w[::-1],r,s),'word reversal')
            if w=='abab':check(R==2*ab,'power identity')
            trials+=1;tested_configs+=len(vals)
            if d*q>max_defect:max_defect=d*q;witness={'word':w,'r':str(r),'s':str(s),'R':str(R),'q_times_defect':str(d*q),'m':m}
            if nonextreme is None:
                for val,W in vals:
                    if val<R and val-A*r-B*s>F(m,val.denominator):
                        nonextreme={'word':w,'r':str(r),'s':str(s),'value':str(val),'R':str(R),'configuration':W,'defect':str(val-A*r-B*s),'bound':str(F(m,val.denominator))};break
    # Full-period averaging applies to a model with that output period,
    # even if it is not the maximizing cyclic order.
    for r,s in product(rats,repeat=2):
        for w in words:
            for val,W in upper(w,r,s,True):
                if val.denominator in (r.denominator,s.denominator):
                    check(val-w.count('a')*r-w.count('b')*s<=F(pairs(w),val.denominator),'individual full-period model')
    # An explicit nonextremal HOMEOMORPHISM pair: f fixes 0,
    # g=f^-1 R_(2/3) fixes 1/6, and f g=R_(2/3).
    def f(x):
        k=x.__floor__(); z=x-k
        return k+(5*z if z<=F(1,6) else F(5,6)+(z-F(1,6))/5)
    def fi(x):
        k=x.__floor__(); z=x-k
        return k+(z/5 if z<=F(5,6) else F(1,6)+5*(z-F(5,6)))
    def g(x):return fi(x+F(2,3))
    check(f(F(0))==0 and g(F(1,6))==F(1,6),'fixed-point lifts')
    for i in range(-120,121):
        x=F(i,60)
        check(fi(f(x))==x and f(fi(x))==x,'PL inversion')
        check(f(g(x))==x+F(2,3),'nonextremal product')
        check(f(x+1)==f(x)+1 and g(x+1)==g(x)+1,'degree-one lifts')
    check(F(2,3)>F(1,3),'arbitrary-representation shortcut fails')
    # Deliberately false denominator substitution: using input q rather than output q.
    R=upper('ab',F(1,5),F(1,5))
    check(R==1,'input-denominator control exact R')
    check(R-F(2,5)>F(1,5),'input-denominator shortcut must fail')
    # Deliberately false independent-phase estimate. Four selected X starts in
    # a 5-X,100-Y order. b has translation 1/100. All four b outputs occupy
    # distinct X gaps, but sum skipped full X gaps is 4>6/5.
    W='XYXYXYXYX'+'Y'*96
    check(W.count('X')==5 and W.count('Y')==100,'phase counts')
    _,bt=tables(W,1,1);xs=[i for i,c in enumerate(W) if c=='X']
    skips=[];dest=[]
    for i in range(4):
        y=bt[xs[i]];j=max(k for k,x in enumerate(xs) if x<y)
        skips.append(j-i);dest.append(j)
    check(skips==[1,1,1,1] and len(set(dest))==4,'phase geometry')
    check(sum(skips)>4*5*F(1,100)+5-4,'phase inequality is false')
    # The subsequent a-hop with p=1 fails to preserve this four-point set.
    image_set={(j+2)%5 for j in dest}
    check(image_set!=set(range(4)),'missing global cyclic orbit condition')
    # Arithmetic in reduction of powers of ab.
    for d,m,c in product(range(1,31),range(1,15),range(1,31)):
        if gcd(c,d)!=1:continue
        q=F(m*c,d).denominator
        check(q==d//gcd(m,d),'power denominator reduction')
        check(F(m,d)<=F(m,q),'power family bound')
    result={'status':'PASS_BOUNDED_EXACT_CONTROLS_ONLY','assertions':CHECKS,'rational_inputs':len(rats),'maximum_input_denominator':5,'words':words,'parameter_word_cases':trials,'configurations_scored':tested_configs,'largest_q_times_defect':witness,'nonextremal_step_model_control_found':nonextreme,'nonextremal_homeomorphism_control':{'r':'0','s':'0','tau_ab':'2/3','R_ab':'1','false_bound':'1/3'},'wrong_input_denominator_control':{'word':'ab','r':'1/5','s':'1/5','R':'1','defect':'3/5','false_bound':'1/5'},'false_phase_bound':{'N':5,'q_selected':4,'V':100,'U':1,'sum_l':4,'claimed_upper':'6/5'},'scope':'Finite orbit enumeration supports, but does not prove, the universal conjecture. Negative controls refute shortcuts only.'}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__': main()
