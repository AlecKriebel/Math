#!/usr/bin/env python3
"""Independent rational reconstruction and Sturm checks. No author code imported.
Finite checks accompany, and do not replace, the audited universal proof.
"""
import argparse, hashlib, itertools, json, math
from pathlib import Path
import sympy as s

t=s.Symbol('t')
R=s.Rational
class AuditFailure(Exception): pass

def check(test, label):
    if not bool(test): raise AuditFailure(label)

def identity(a,b,label): check(s.expand(a-b)==0,label)

def direct_chi(p,x):
    for v in x: p=s.Poly(p-s.diff(p,v),*x).as_expr()
    return s.Poly(p.subs(dict.fromkeys(x,t)),t,domain=s.QQ)

def admissible_algebra(p,x,d):
    q=s.Poly(p,*x);one=dict.fromkeys(x,1)
    check(all(sum(a)==d for a,c in q.terms()),'homogeneity')
    check(q.as_expr().subs(one)==1,'normalization')
    check(all(c>=0 for c in q.coeffs()),'coefficient positivity')
    check(all(s.diff(p,v).subs(one)==R(d,len(x)) for v in x),'equal gradient')

# A separate exact Sturm implementation; no Poly.intervals / numerical roots.
def chain(f):
    f=f.monic(); seq=[f,f.diff()]
    while not seq[-1].is_zero:
        rem=-seq[-2].rem(seq[-1])
        if rem.is_zero:break
        seq.append(rem)
    return seq

def variations(seq,a):
    signs=[s.sign(g.eval(a)) for g in seq if g.eval(a)!=0]
    return sum(u!=v for u,v in zip(signs,signs[1:]))

def bound(f): return 2+int(s.ceiling(max([abs(c/f.LC()) for c in f.all_coeffs()[1:]]+[0])))

def sturm_data(f):
    check(f.degree()>0,'positive polynomial degree')
    factors=s.sqf_list(f)[1];count=0
    for fac,mul in factors:
        st=chain(fac);B=bound(fac)
        count+=mul*(variations(st,-B)-variations(st,B))
    check(count==f.degree(),'all roots real, with multiplicity')
    sf=f.exquo(s.gcd(f,f.diff())).monic();st=chain(sf);B=bound(sf)
    return sf,st,B

def largest(f,bits=72):
    sf,st,B=sturm_data(f);lo=R(-B);hi=R(B);vend=variations(st,B)
    while hi-lo>R(1,2**bits) or variations(st,lo)-variations(st,hi)!=1:
        mid=(lo+hi)/2;above=variations(st,mid)-vend
        if sf.eval(mid)==0 and above==0:return mid,mid
        if above:lo=mid
        else:hi=mid
    return lo,hi

def interval_taylor(f,lo,hi):
    # Bound each Taylor term around lo; u is in [0, hi-lo].
    low=high=f.eval(lo);der=f;power=R(1);fact=1
    for k in range(1,f.degree()+1):
        der=der.diff();power*=hi-lo;fact*=k
        term=der.eval(lo)*power/fact
        low+=min(0,term);high+=max(0,term)
    return low,high

def reference(m,d):
    # Enumerate subsets of variables; derivative of a power of the average.
    coeff=[R(math.comb(m,k)*math.prod(range(d-k+1,d+1)),m**k) for k in range(min(m,d)+1)]
    return s.Poly(sum((-1)**k*c*t**(d-k) for k,c in enumerate(coeff)),t),coeff

def rook_coefficients(rows):
    # Choose at most one column for each factor and never reuse a column.
    # The coefficient for a used-column mask is its partial matching weight.
    dp={0:R(1)}
    for row in rows:
        nxt=dict(dp)
        for mask,value in dp.items():
            for j,a in enumerate(row):
                if a and not mask>>j&1:
                    dest=mask|1<<j;nxt[dest]=nxt.get(dest,0)+value*a
        dp=nxt
    out=[R(0)]*(min(len(rows),len(rows[0]))+1)
    for mask,v in dp.items():out[mask.bit_count()]+=v
    return out

def cyclic_polynomial(m,d):
    x=s.symbols('x:'+str(m));N=m*math.ceil(d/m)
    p=s.prod((x[i%m]+2*x[(i+1)%m])/3 for i in range(N))
    p=s.expand(p)
    for deg in range(N,d,-1):p=s.expand(sum(s.diff(p,v) for v in x)/deg)
    return p,x

def marginal_moments(p,x,d):
    # Derive Bernoulli power sums from factorial cumulants at z=1.
    z=s.Symbol('z');sum2=sum3=0
    for v in x:
        F=s.Poly(p.subs({w:(z if w==v else 1) for w in x}),z)
        a=F.diff().eval(1);b=F.diff().diff().eval(1);c=F.diff().diff().diff().eval(1)
        sum2+=a*a-b
        sum3+=(c-3*a*b+2*a**3)/2
    m=len(x)
    return s.factor(sum2-R(d,m)),s.factor(sum3-R(d,m*m))

def compare_record(f,m,d,expected,name):
    ref,rc=reference(m,d);lo,hi=largest(f);rl,rh=largest(ref)
    check(hi<rl or f==ref,'largest-root direction: '+name)
    claimed=s.Poly(sum((-1)**k*R(v)*t**(d-k) for k,v in enumerate(expected['coefficients'])),t)
    check(f.as_expr()==claimed.as_expr(),'reconstructed coefficients: '+name)
    for a,b in [expected['largest_root_interval'],expected['reference_interval']]:check(R(a)<=R(b),'author interval ordering')
    # Verify each reported interval contains the appropriate exact largest root.
    for poly,key in [(f,'largest_root_interval'),(ref,'reference_interval')]:
        a,b=map(R,expected[key]);sf,st,B=sturm_data(poly)
        if a==b:
            check(sf.eval(a)==0 and variations(st,a)==variations(st,B),'reported exact largest root')
        else:
            check(variations(st,a)-variations(st,b)==1 and variations(st,b)==variations(st,B),'reported largest-root enclosure')
    rec={'name':name,'m':m,'d':d,'chi_coefficients':[str(c) for c in f.all_coeffs()],
         'largest_interval':[str(lo),str(hi)],'reference_interval':[str(rl),str(rh)],'comparison':'strictly below' if hi<rl else 'equal'}
    if 'flow_check' in expected:
        common=s.gcd(f,f.diff())
        repeated=False
        if common.degree()>0:
            if lo==hi:repeated=common.eval(lo)==0
            else:
                cseq=chain(common.exquo(s.gcd(common,common.diff())))
                repeated=variations(cseq,lo)-variations(cseq,hi)>0 or common.eval(lo)==0 or common.eval(hi)==0
        if repeated:rec['flow']='repeated largest root: no derivative division'
        else:
            h=s.Poly(t*f.diff().diff().as_expr()-(m*t-m+d-1)*f.diff().as_expr(),t)
            low,high=interval_taylor(h,lo,hi)
            check(low>0,'positive sampled corrected-flow derivative')
            rec['flow']='positive';rec['scaled_velocity_numerator_interval']=[str(low),str(high)]
        check(('repeated' in rec['flow'])==('multiple' in expected['flow_check']),'author multiplicity handling')
    return rec

def symbolic_checks():
    m,d,A,B,D2,D3=s.symbols('m d A B D2 D3');mu=d/m
    ex2=m*(mu**2+mu)-A
    ex3=m*(mu**3+3*mu**2+mu)-3*(mu+1)*A+2*B
    c2=(d*d-ex2)/2;c3=(d**3-3*d*ex2+2*ex3)/6
    def excess(v):return s.expand(v.subs({A:d/m+D2,B:d/m**2+D3})-v.subs({A:d/m,B:d/m**2}))
    identity(excess(c2),D2/2,'universal second coefficient identity')
    identity(excess(c3),(d/2-d/m-1)*D2+R(2,3)*D3,'universal third coefficient identity')
    u=s.Symbol('u')
    a=s.Symbol('a');z=s.Symbol('z')
    identity((z-a)**2*(z+2*a),z**3-3*a*a*z+2*a**3,'deviation identity')
    q3=t**3-d*t*t+d*(d-1)*t/3-d*(d-1)*(d-2)/27
    identity(q3.subs(t,d/3+u),u**3-d*u/3-2*d/27,'m=3 cubic')
    qd=t**3-3*t*t+3*(m-1)*t/m-(m-1)*(m-2)/m**2
    identity(qd.subs(t,1+u),u**3-3*u/m-2/m**2,'d=3 cubic')
    identity(q3.subs(t,d/3+R(2,9)),R(8,729)-4*d/27,'first strict witness')
    identity(qd.subs(t,1+2/(3*m)),8/(27*m**3)-4/m**2,'second strict witness')
    # Coefficient recurrence verifies the intertwining formula for arbitrary C_k.
    k=s.Symbol('k',integer=True)
    identity(m*(d-k)/(m*d),(d-k)/d,'same-degree T coefficient')
    identity(-(m-k)*(d-k)/(m*d),-((m-d+1)*(d-k)+(d-k)*(d-k-1))/(m*d),'lower-degree T coefficient')
    return 9

def operator_checks():
    cases=[]
    for m,d in [(2,3),(3,2),(3,3),(4,3)]:
        p,x=cyclic_polynomial(m,d);f=direct_chi(p,x)
        tp=s.expand(sum(x)*sum(s.diff(p,v) for v in x)/(m*d))
        actual=direct_chi(tp,x)
        predicted=s.Poly(((m*t-m+d-1)*f.diff().as_expr()-t*f.diff().diff().as_expr())/(m*d),t)
        check(actual.as_expr()==predicted.as_expr(),'operator intertwining')
        r,u=s.symbols('r u');bar=sum(x)/m
        flow=s.expand(p.xreplace({v:r*v+(1-r)*bar for v in x}))
        identity(-s.diff(flow,r).subs(r,1)/d,tp-p,'corrected flow generator')
        identity(flow.subs(r,0),bar**d,'corrected flow endpoint')
        composed=flow.xreplace({v:u*v+(1-u)*bar for v in x})
        identity(composed,flow.subs(r,r*u),'corrected flow composition')
        cases.append({'m':m,'d':d,'intertwining':'pass','generator':'pass','limit':'pass','composition':'pass'})
    return cases

def negative_controls():
    x,y,z,w=s.symbols('x y z w');P=(x+y)**2*(z+w)**2/16
    Q=sum(P.xreplace(dict(zip((x,y,z,w),p))) for p in itertools.permutations((x,y,z,w)))/24
    identity(Q.subs({x:t,y:-1,z:0,w:1}),(t*t+1)/24,'actual full average specialization')
    identity(direct_chi(P,(x,y,z,w)).as_expr(),direct_chi(Q,(x,y,z,w)).as_expr(),'same mixed characteristic')
    identity(direct_chi(P,(x,y,z,w)).as_expr(),(t*t-2*t+R(1,2))**2,'square mixed characteristic')
    pinf=(x+y)**2/4;bad=direct_chi(2*x*y-pinf,(x,y));good=direct_chi((x*y+pinf)/2,(x,y))
    identity(bad.as_expr(),t*t-2*t+R(3,2),'wrong flow')
    identity(good.as_expr(),t*t-2*t+R(3,4),'corrected flow')
    rejects=[]
    def rejection(name,fn):
        try:fn()
        except AuditFailure:rejects.append(name);return
        raise AuditFailure('negative control accepted: '+name)
    rejection('permutation averaging preserves stability',lambda:sturm_data(s.Poly(Q.subs({x:t,y:-1,z:0,w:1}),t)))
    rejection('printed flow keeps chi real-rooted',lambda:sturm_data(bad))
    rejection('corrected flow decreases maxroot',lambda:check(largest(good)[1]<=1,'wrong direction'))
    rejection('wrong normalization',lambda:admissible_algebra(2*x*y,(x,y),2))
    rejection('wrong gradient',lambda:admissible_algebra((x+2*y)**2/9,(x,y),2))
    rejection('nonhomogeneous input',lambda:admissible_algebra((x+y+1)/3,(x,y),1))
    rejection('negative coefficient input',lambda:admissible_algebra(2*x*y-pinf,(x,y),2))
    rejection('stability can be dropped',lambda:check(largest(direct_chi((x*x+y*y)/2,(x,y)))[1]<largest(reference(2,2)[0])[0],'unstable largest root too large'))
    rejection('replace product of operators by one minus sum',lambda:identity(direct_chi(x*y,(x,y)).as_expr(),t*t-2*t,'missing cross derivative'))
    rejection('evaluate diagonal before derivatives',lambda:identity(direct_chi(x*y,(x,y)).as_expr(),t*t-4*t+2,'wrong diagonal order'))
    rejection('wrong second moment sign',lambda:check(1-R(1,2)==-R(1,2),'coefficient sign'))
    rejection('reference largest root wrongly set to one',lambda:check(largest(reference(2,2)[0])[1]<=1,'reference top root'))
    rejection('cubic witness has wrong sign',lambda:check(R(8,729)-R(4,9)>0,'strict witness'))
    repeated=s.Poly((t-1)**3*t**2,t)
    a,b=largest(repeated);check(a<=1<=b,'repeated largest root')
    rejection('distinct real root count equals degree',lambda:check(repeated.degree()==repeated.sqf_part().degree(),'multiplicity omitted'))
    return {'rejected':rejects,'count':len(rejects),'full_average_specialization':str(s.factor(Q.subs({x:t,y:-1,z:0,w:1}))),
            'printed_flow':str(bad.as_expr()),'corrected_flow':str(good.as_expr()),'repeated_root_control':'pass'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--author',type=Path,required=True);ap.add_argument('--output',type=Path);args=ap.parse_args()
    raw=(args.author/'verification.json').read_bytes();j=json.loads(raw)
    check(j['unrestricted_target']=='unresolved','scope retained')
    output={'problem_id':'30003442','status':'PASS','scope':'finite independent reconstructions; universal proof assessed separately',
        'symbolic_checks':symbolic_checks(),'operator_checks':operator_checks(),'negative_controls':negative_controls(),'author_verification_sha256':hashlib.sha256(raw).hexdigest(),'examples':[]}
    for rec in j['exact_examples']:
        m,d=rec['m'],rec['d'];name=rec['name']
        if 'permutations' in rec:
            perms=rec['permutations'];rows=[[R(sum(p[i]==k for p in perms),len(perms)) for k in range(m)] for i in range(d)]
            check(all(sum(row)==1 for row in rows),'product row sums')
            check(all(sum(row[k] for row in rows)==R(d,m) for k in range(m)),'product column sums')
            cs=rook_coefficients(rows);f=s.Poly(sum((-1)**k*c*t**(d-k) for k,c in enumerate(cs)),t)
            # Independent factorization makes theta_i,j exactly the row coefficients.
            D2=sum((a-R(1,m))**2 for row in rows for a in row)
            D3=sum(a**3 for row in rows for a in row)-R(d,m*m)
        else:
            p,x=cyclic_polynomial(m,d);admissible_algebra(p,x,d);f=direct_chi(p,x);D2,D3=marginal_moments(p,x,d)
        check(D2==R(rec['delta2']) and D3==R(rec['delta3']),'author moment values')
        check(D2>=0 and 0<=D3<=(min(1,R(d,m))+R(2,m))*D2,'marginal moment bounds')
        _,rc=reference(m,d)
        if min(m,d)>=2:check(f.nth(d-2)-rc[2]==D2/2,'second coefficient reconstructed')
        if min(m,d)>=3:check(-f.nth(d-3)-rc[3]==(R(d,2)-R(d,m)-1)*D2+R(2,3)*D3,'third coefficient reconstructed')
        output['examples'].append(compare_record(f,m,d,rec,name))
    check(len(output['examples'])==58,'all author examples independently reconstructed')
    boundary=[]
    for m,d in [(1,n) for n in range(1,10)]+[(n,1) for n in range(2,10)]+[(2,12),(3,12),(12,2),(12,3)]:
        x=s.symbols('x:'+str(m));ref,_=reference(m,d)
        if m==1:identity(ref.as_expr(),t**(d-1)*(t-d),'one variable')
        elif d==1:identity(ref.as_expr(),t-1,'degree one')
        else:sturm_data(ref)
        boundary.append([m,d])
    output['boundary_checks']=boundary
    output['example_count']=len(output['examples']);output['product_examples']=sum('permutations' in r for r in j['exact_examples'])
    output['flow_positive']=sum(r.get('flow')=='positive' for r in output['examples'])
    output['flow_repeated_omitted']=sum('repeated' in r.get('flow','') for r in output['examples'])
    content=json.dumps(output,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(content)
    else:print(content,end='')
if __name__=='__main__':main()
