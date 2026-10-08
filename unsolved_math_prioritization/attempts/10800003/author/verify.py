#!/usr/bin/env python3
"""Exact finite controls and scope checks. No theorem-proof or novelty certification."""
from pathlib import Path
from fractions import Fraction as Q
import argparse, hashlib, itertools, json, math, re, stat, sys
class Rejected(Exception): pass
COUNTS={}
def require(ok,msg):
    if not ok: raise Rejected(msg)
def check(ok,group,msg):
    require(ok,msg);COUNTS[group]=COUNTS.get(group,0)+1
def pairs(items):
    d={}
    for k,v in items:
        require(k not in d,'duplicate JSON key'); d[k]=v
    return d
def bad_constant(x): raise Rejected('nonfinite JSON constant')
def strict_float(s):
    x=float(s);require(math.isfinite(x),'nonfinite JSON number');return x
def read_json(p):
    require(not p.is_symlink() and stat.S_ISREG(p.stat().st_mode),'not a regular input')
    b=p.read_bytes();require(len(b)<1000000,'input too large')
    return json.loads(b,object_pairs_hook=pairs,parse_constant=bad_constant,parse_float=strict_float)
def exact_keys(v,keys):require(type(v) is dict and set(v)==set(keys),'wrong object keys')
def integer(x,lo=-10000,hi=10000):require(type(x) is int and lo<=x<=hi,'integer type/range');return x
def integer_list(xs,n=None):
    require(type(xs) is list and (n is None or len(xs)==n),'list shape')
    return [integer(x) for x in xs]
def mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def tr(a):return [list(x) for x in zip(*a)]
def ident(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def mpow(a,k):
    r=ident(len(a))
    for _ in range(k):r=mm(r,a)
    return r
def rank(a):
    a=[[Q(x) for x in row] for row in a];i=0
    for j in range(len(a[0]) if a else 0):
        k=next((k for k in range(i,len(a)) if a[k][j]),None)
        if k is None:continue
        a[i],a[k]=a[k],a[i];z=a[i][j];a[i]=[x/z for x in a[i]]
        for k in range(len(a)):
            if k!=i:
                z=a[k][j];a[k]=[x-z*y for x,y in zip(a[k],a[i])]
        i+=1
        if i==len(a):break
    return i
def det(a):
    a=[[Q(x) for x in row] for row in a];r=Q(1);n=len(a)
    for j in range(n):
        k=next((k for k in range(j,n) if a[k][j]),None)
        if k is None:return Q(0)
        if k!=j:a[j],a[k]=a[k],a[j];r=-r
        z=a[j][j];r*=z
        for k in range(j+1,n):
            f=a[k][j]/z;a[k]=[x-f*y for x,y in zip(a[k],a[j])]
    return r
def pmul(a,b):
    r=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):r[i+j]+=x*y
    return r
def peval(a,x):
    r=Q(0)
    for c in reversed(a):r=r*x+c
    return r
def deriv(a):return [i*a[i] for i in range(1,len(a))]
def from_roots(xs):
    r=[Q(1)]
    for x in xs:r=pmul(r,[-x,1])
    return r
def primitive(a):return [Q(0)]+[Q(c,i+1) for i,c in enumerate(a)]
def lagrange(xs,i):
    p=from_roots([x for k,x in enumerate(xs) if i!=k]);v=peval(p,xs[i]);return [x/v for x in p]
def main():
    pa=argparse.ArgumentParser();pa.add_argument('--source-dir');args=pa.parse_args()
    root=Path(__file__).resolve().parent
    claims=read_json(root/'CLAIMS.json')
    exact_keys(claims,['schema','problem_id','catalog_id','rank','status','approaches_used','complete_original_resolution','target_counterexample','novelty_claim','formal_verification_claim','human_peer_review_claim','results','remaining_gap','foundational_inputs','literature_scope'])
    check(claims['schema']=='critical-value-collisions-claims-v1' and claims['catalog_id']=='AMR-107-0003','scope','identity')
    check(integer(claims['problem_id'],10800003,10800003)==10800003 and integer(claims['rank'])==1011,'scope','catalog target')
    check(claims['status']=='unsolved' and integer(claims['approaches_used'])==5,'scope','status or turns overstated')
    for key in ['complete_original_resolution','target_counterexample','novelty_claim','formal_verification_claim','human_peer_review_claim']:
        check(type(claims[key]) is bool and claims[key] is False,'scope','unjustified claim flag: '+key)
    for key in ['results','foundational_inputs']:
        require(type(claims[key]) is list and all(type(x) is str and x for x in claims[key]),'claim list')
    for key in ['remaining_gap','literature_scope']:require(type(claims[key]) is str and claims[key],'claim text')
    ledger=read_json(root/'APPROACH_LEDGER.json')
    exact_keys(ledger,['schema','problem_id','turns','nonturn_work'])
    require(ledger['schema']=='critical-value-collisions-ledger-v1' and type(ledger['problem_id']) is int and ledger['problem_id']==10800003,'ledger identity')
    ts=ledger['turns'];require(type(ts) is list and len(ts)==5,'five turns required')
    mechanisms=['local_algebra','rank_two_reflections','geometric_cycles','inverse_flow','separable_x9']
    for i,t in enumerate(ts):
        exact_keys(t,['turn','mechanism','mathematical_attempt','outcome','proof_location'])
        check(type(t['turn']) is int and t['turn']==i+1 and t['mechanism']==mechanisms[i],'scope','ledger mechanism')
        require(all(type(t[k]) is str and t[k] for k in ['mathematical_attempt','outcome','proof_location']),'ledger text')
    cert=read_json(root/'CERTIFICATE.json')
    exact_keys(cert,['schema','reflection_m','cusp_s','grid_alpha','grid_beta','scaling'])
    require(cert['schema']=='critical-value-collisions-certificate-v1','certificate schema')
    ms=integer_list(cert['reflection_m']);require(ms==list(range(-8,9)),'reflection test domain changed')
    I=ident(2)
    for m in ms:
        G=[[-2,m],[m,-2]];Ra=[[-1,m],[0,1]];Rb=[[1,0],[m,-1]];P=mm(Ra,Rb)
        check(mpow(Ra,2)==I and mpow(Rb,2)==I,'rank_two','reflection involutions')
        check(mm(mm(tr(Ra),G),Ra)==G and mm(mm(tr(Rb),G),Rb)==G,'rank_two','Gram preservation')
        check(P==[[m*m-1,-m],[m,-1]],'rank_two','product formula')
        check(det(P)==1 and P[0][0]+P[1][1]==m*m-2 and det(G)==4-m*m,'rank_two','trace determinant')
        if m==0:check(P==[[-1,0],[0,-1]] and mpow(P,2)==I,'rank_two','m0 order')
        elif abs(m)==1:check(mpow(P,3)==I and P!=I,'rank_two','m1 order')
        elif abs(m)==2:
            N=[[P[i][j]-I[i][j] for j in range(2)] for i in range(2)]
            check(N!=[[0,0],[0,0]] and mm(N,N)==[[0,0],[0,0]],'rank_two','m2 nilpotent')
            for k in range(1,7):check(mpow(P,k)==[[I[i][j]+k*N[i][j] for j in range(2)] for i in range(2)],'rank_two','unipotent power')
        else:check(P[0][0]+P[1][1]>2,'rank_two','hyperbolic trace')
    require(type(cert['cusp_s']) is list and len(cert['cusp_s'])==32,'cusp list')
    ss=[]
    for pq in cert['cusp_s']:
        p,q=integer_list(pq,2);require(q>0 and p!=0,'cusp rational');ss.append(Q(p,q))
    require(len(set(ss))==32,'duplicate cusp cases')
    for s in ss:
        a=s*s;b=Q(7,5);h=lambda z:z**3-3*a*z+b
        check(3*s*s-3*a==0 and 3*(-s)**2-3*a==0,'cusp','critical equations')
        check(h(s)==b-2*s**3 and h(-s)==b+2*s**3,'cusp','critical values')
        d=h(-s)-h(s)
        check(d*d==16*a**3,'cusp','discriminant relation')
        check((2*s)/(12*s*s)==1/(6*s),'cusp','inverse derivative')
    alpha=integer_list(cert['grid_alpha'],3);beta=integer_list(cert['grid_beta'],3)
    require(alpha==[-2,-1,3] and beta==[-5,1,4],'grid fixture')
    p=primitive(from_roots(alpha));q=primitive(from_roots(beta))
    check(p==[0,-6,Q(-7,2),0,Q(1,4)] and q==[0,20,Q(-21,2),0,Q(1,4)],'grid','quartic coefficients')
    pts=list(itertools.product(alpha,beta));vals=[]
    for x,y in pts:
        check(peval(deriv(p),x)==0 and peval(deriv(q),y)==0,'grid','grid critical equations')
        check(peval(deriv(deriv(p)),x)!=0 and peval(deriv(deriv(q)),y)!=0,'grid','Morse Hessian')
        vals.append(peval(p,x)+peval(q,y))
    check(len(set(vals))==9,'grid','distinct critical values')
    mon=list(itertools.product(range(3),repeat=2))
    E=[[x**i*y**j for i,j in mon] for x,y in pts]
    va=[[x**i for i in range(3)] for x in alpha];vb=[[y**j for j in range(3)] for y in beta]
    check(det(E)==det(va)**3*det(vb)**3 and det(E)!=0,'grid','tensor Vandermonde determinant')
    check(rank(E)==9,'grid','full tangent rank')
    for i,j in itertools.product(range(3),repeat=2):
        li=lagrange(alpha,i);mj=lagrange(beta,j)
        for k,l in itertools.product(range(3),repeat=2):
            check(peval(li,alpha[k])*peval(mj,beta[l])==int((i,j)==(k,l)),'grid','tensor Lagrange indicator')
    rectangles=[]
    for i,k in itertools.combinations(range(3),2):
        for j,l in itertools.combinations(range(3),2):
            r=[0]*9
            for a,b,z in [(i,j,1),(i,l,-1),(k,j,-1),(k,l,1)]:r[3*a+b]=z
            rectangles.append(r)
            check(sum(x*y for x,y in zip(r,vals))==0,'grid','value rectangle')
    for u,v in itertools.combinations(range(9),2):
        check(rank([[r[u],r[v]] for r in rectangles])==2,'grid','two-supported additive matrix kernel')
    scaling=cert['scaling'];exact_keys(scaling,['x9','j10'])
    for name,d,w,e in [('x9',4,[1,1],[2,2]),('j10',6,[2,1],[1,4])]:
        z=scaling[name];exact_keys(z,['weights','degree','marginal_exponents'])
        ww=integer_list(z['weights'],2);ee=integer_list(z['marginal_exponents'],2);dd=integer(z['degree'])
        check(ww==w and ee==e and dd==d,'scaling','weights')
        check(dd-sum(x*y for x,y in zip(ww,ee))==0,'scaling','modulus is invariant under scaling')
    sources=read_json(root/'SOURCE_METADATA.json')
    exact_keys(sources,['schema','sources','source_bytes_in_packet','primary_statement_verified','uninspected_original_dependency','search_scope','stale_versions_not_controlling'])
    require(sources['schema']=='critical-value-collisions-sources-v1','source schema')
    require(type(sources['source_bytes_in_packet']) is bool and sources['source_bytes_in_packet'] is False,'source contents flag')
    require(type(sources['primary_statement_verified']) is bool and sources['primary_statement_verified'] is True,'statement flag')
    require(type(sources['sources']) is list and len(sources['sources'])==6,'source list')
    aliases=set()
    for e in sources['sources']:
        exact_keys(e,['alias','title','url','bytes','sha256','public_status','retrieved_utc_date','inspection'])
        require(all(type(e[k]) is str and e[k] for k in ['alias','title','url','sha256','public_status','retrieved_utc_date','inspection']),'source text')
        require(e['alias'] not in aliases and re.fullmatch('[a-z0-9_]+',e['alias']) is not None,'source alias');aliases.add(e['alias'])
        integer(e['bytes'],1,10000000);require(re.fullmatch('[a-f0-9]{64}',e['sha256']) is not None,'source sha')
    source_state='NOT_RUN: source bytes are intentionally external'
    if args.source_dir:
        sd=Path(args.source_dir);require(not sd.is_symlink() and sd.is_dir(),'external source directory')
        names={'problem_published':'vassiliev2015-published.pdf','problem_preprint':'vassiliev2015.pdf','quartic_current':'quartic-v12.pdf','j10_current':'j10v5.pdf','parabolic_current':'parabolic-v6.pdf','problem_html':'vassiliev2015.html'}
        require(aliases==set(names),'source alias set')
        for e in sources['sources']:
            p=sd/names[e['alias']];require(not p.is_symlink() and stat.S_ISREG(p.stat().st_mode),'external source type')
            raw=p.read_bytes();check(len(raw)==e['bytes'] and hashlib.sha256(raw).hexdigest()==e['sha256'],'external_sources','source byte mismatch')
        source_state='PASS: all six actual external source files matched'
    return {'schema':'critical-value-collisions-diagnostics-v1','status':'PASS','problem_id':10800003,'original_problem_status':'unsolved','approaches_used':5,'checks':COUNTS,'total_exact_checks':sum(COUNTS.values()),'source_byte_reverification':source_state,'limitations':['Finite algebra controls do not formally verify the analytic or geometric proofs.','No original-problem solution, counterexample, novelty or human-peer-review certification.']}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True,separators=(',',':')))
    except (Rejected,OSError,ValueError,TypeError,KeyError,IndexError,ZeroDivisionError) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
