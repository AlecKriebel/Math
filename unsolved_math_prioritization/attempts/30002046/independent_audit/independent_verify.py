#!/usr/bin/env python3
"""Independent exact auditor. Standard library only. Never imports the target code.
Usage: python3 independent_verify.py /path/to/frozen/safe [--check]
Writes only this audit's INDEPENDENT_RESULTS.json unless --check is given.
"""
from fractions import Fraction as R
from pathlib import Path
from math import gcd
from collections import deque, Counter
from copy import deepcopy
import hashlib, json, sys

EXPECTED_MANIFEST = 'faf4f5f3d6069420dd4a975a6320e704bdb6f190f64a1626863c5ff1e08bd045'
class AuditFailure(Exception): pass
def need(condition, message):
    if not condition: raise AuditFailure(message)
def pair(x): return [x.numerator, x.denominator]
def rational(p): return R(*p)
def digest(b): return hashlib.sha256(b).hexdigest()

def question(x):
    """Binary Stern-Brocot address via accelerated subtractive Euclid.
    No continued-fraction summation and no dependency on the target verifier.
    (u,v)=(p,q-p); L replaces v by v-u, R replaces u by u-v.
    An address bit selects the lower/upper half of the dyadic image interval.
    """
    need(0 <= x <= 1, 'domain')
    if x in (0,1): return x
    u,v=x.numerator,x.denominator-x.numerator
    lower,scale=0,1
    while u != v:
        if u < v:
            run=(v-1)//u; v-=run*u
            lower <<= run; scale <<= run
        else:
            run=(u-1)//v; u-=run*v
            lower=(lower<<run)+(1<<run)-1; scale <<= run
    need(u == v == 1, 'Euclidean termination')
    return R(2*lower+1,2*scale)

def cf_digits(x):
    p,q=x.numerator,x.denominator; digits=[]
    while p:
        a,r=divmod(q,p); digits.append(a); q,p=p,r
    return digits

def cf_horner(digits):
    y=R(0)
    for a in reversed(digits): y=(1-y)/(1<<a)
    return 2*y

def classify(a,b,qa,qb):
    if qb < a: return 'negative'
    if qa > b: return 'positive'
    return 'retained'

def make_certificate(depth):
    todo=deque([(R(2,5),R(3,7),0)]); leaves=[]; visited=0; levels=Counter()
    while todo:
        a,b,d=todo.popleft();visited+=1;levels[d]+=1
        qa,qb=question(a),question(b)
        need(b.numerator*a.denominator-a.numerator*b.denominator==1,'neighbor determinant')
        reason=classify(a,b,qa,qb)
        if reason=='retained' and d<depth:
            m=R(a.numerator+b.numerator,a.denominator+b.denominator)
            need(question(m)==(qa+qb)/2,'mediant identity')
            todo.extend([(a,m,d+1),(m,b,d+1)])
        else:
            leaves.append(dict(a=pair(a),b=pair(b),qa=pair(qa),qb=pair(qb),depth=d,reason=reason))
    leaves.sort(key=lambda z:rational(z['a']))
    live=[z for z in leaves if z['reason']=='retained']
    a=rational(live[0]['a']);b=rational(live[-1]['b'])
    return dict(depth=depth,visited=visited,leaf_count=len(leaves),retained_count=len(live),hull=[pair(a),pair(b)],width=pair(b-a),leaves=leaves),dict(sorted(levels.items()))

def validate_certificate(c):
    leaves=c['leaves'];need(bool(leaves),'empty partition')
    need(rational(leaves[0]['a'])==R(2,5),'left coverage')
    need(rational(leaves[-1]['b'])==R(3,7),'right coverage')
    for i,z in enumerate(leaves):
        a,b,qa,qb=(rational(z[k]) for k in ('a','b','qa','qb'))
        need(a<b,'positive length')
        need(question(a)==qa and question(b)==qb,'false endpoint image')
        need(b.numerator*a.denominator-a.numerator*b.denominator==1,'false neighbors')
        need(classify(a,b,qa,qb)==z['reason'],'false exclusion')
        if z['reason']=='retained':need(z['depth']==c['depth'],'false retained depth')
        need(0<=z['depth']<=c['depth'],'invalid depth')
        if i:need(rational(leaves[i-1]['b'])==a,'coverage gap/overlap')
    live=[z for z in leaves if z['reason']=='retained']
    need(bool(live),'no root-containing leaf')
    a=rational(live[0]['a']);b=rational(live[-1]['b'])
    need(c['hull']==[pair(a),pair(b)],'false hull')
    need(c['width']==pair(b-a),'false width')
    need(c['leaf_count']==len(leaves),'false leaf count')
    need(c['visited']==2*len(leaves)-1,'false full-binary node count')
    need(c['retained_count']==len(live),'false retained count')
    need(question(a)<a and question(b)>b,'missing sign bracket')
    # Replay independently, so false depths or omitted subdivisions cannot pass.
    rebuilt,_=make_certificate(c['depth'])
    need(rebuilt==c,'certificate differs from independent complete subdivision')

def bisect(n):
    a,b=R(2,5),R(3,7); trace=[]
    for k in range(n):
        m=(a+b)/2; y=question(m);d=y-m
        need(d!=0,'unexpected rational fixed point')
        if d<0:a=m
        else:b=m
        need(question(a)<a and question(b)>b,'bisection bracket')
        need(b-a==R(1,35*(1<<(k+1))),'bisection width')
        trace.append(dict(step=k+1,midpoint=pair(m),image=pair(y),sign=-1 if d<0 else 1))
    return dict(steps=n,a=pair(a),b=pair(b),width=pair(b-a)),trace

def scan(maxq):
    half=[];one=[];tested=0;best=None;at=None;equivalent=0
    for q in range(3,maxq+1):
        for p in range(1,(q+1)//2):
            if gcd(p,q)!=1:continue
            x=R(p,q);y=question(x);digits=cf_digits(x)
            need(y==cf_horner(digits),'CF versus binary-address disagreement')
            need(digits[-1]>=2,'noncanonical final digit')
            alternative=digits[:-1]+[digits[-1]-1,1]
            need(y==cf_horner(alternative),'finite CF ambiguity');equivalent+=1
            den=1<<(sum(digits)-1)
            need(y.denominator==den,'exact denominator')
            d=abs(y-x);need(d>0,'nontrivial rational fixed point')
            need(d>=R(gcd(q,den),q*den),'integer separation')
            ratio=q*q*d;tested+=1
            if best is None or ratio<best:best,at=ratio,x
            row=dict(x=pair(x),q2_displacement=pair(ratio))
            if ratio<=R(1,2):half.append(row)
            if ratio<1:one.append(row)
    return dict(max_denominator=maxq,tested=tested,at_most_half=half,less_than_one=one,minimum_ratio=pair(best),argmin=pair(at)),equivalent

def positive_controls():
    expected=[(0,0),(R(1,2),R(1,2)),(1,1),(R(1,3),R(1,4)),(R(3,8),R(5,16)),(R(2,5),R(3,8)),(R(3,7),R(7,16)),(R(7,16),R(29,64)),(R(4,9),R(15,32))]
    for x,y in expected:need(question(R(x))==y,'base image')
    count=0
    for q in range(2,151):
        for p in range(1,q):
            if gcd(p,q)!=1:continue
            x=R(p,q);y=question(x);count+=1
            need(question(1-x)==1-y,'reflection')
            need(question(x/(1+x))==y/2,'left equation')
            need((x==y)==(x==R(1,2)),'rational fixed-point control')
    for n in range(3,1001):
        need(question(R(1,n))==R(1,1<<(n-1)),'negative tail image')
        need((1<<(n-1))>=n+1,'negative tail bound')
    for n in range(4,1001):
        need(question(R(n,2*n+1))==R(1,2)-R(1,1<<(n+1)),'positive tail image')
        need((1<<(n+1))>4*n+6,'positive tail bound')
    return dict(base_values=9,symmetry_and_branch_inputs=count,tail_instances_checked=1995,
                warning='Finite tail checks supplement the analytic induction; they do not replace it.')

def negative_controls(cert):
    rejected=[]
    def reject(name,change):
        c=deepcopy(cert);change(c)
        try:validate_certificate(c)
        except AuditFailure as e:rejected.append(dict(name=name,detection=str(e)))
        else:raise AuditFailure('mutation escaped: '+name)
    reject('omitted_terminal_interval',lambda c:c['leaves'].pop(len(c['leaves'])//2))
    reject('tampered_endpoint_image',lambda c:c['leaves'][0]['qa'].__setitem__(0,c['leaves'][0]['qa'][0]+1))
    reject('retained_root_interval_falsely_excluded',lambda c:next(z for z in c['leaves'] if z['reason']=='retained').__setitem__('reason','negative'))
    reject('incorrect_width',lambda c:c['width'].__setitem__(1,c['width'][1]+1))
    reject('incorrect_partition_depth',lambda c:c['leaves'][0].__setitem__('depth',-1))
    reject('incorrect_visited_count',lambda c:c.__setitem__('visited',c['visited']+1))
    a,b=R(2,5),R(4,7)
    need(question(a)<a and question(b)<b,'same-sign example')
    need(a<R(1,2)<b and question(R(1,2))==R(1,2),'interior fixed point')
    need(classify(a,b,question(a),question(b))=='retained','same-sign incorrect pruning')
    # Synthetic normalized strictly increasing polynomial with an even-order contact.
    # Its derivative is >= 7/8 on [0,1], since |(x(1-x)(x-1/2)^2)'| <= 1/2.
    def tangent(x):return x+R(1,4)*x*(1-x)*(x-R(1,2))**2
    a,b=R(1,4),R(3,4)
    need(tangent(a)>a and tangent(b)>b and tangent(R(1,2))==R(1,2),'tangency construction')
    need(classify(a,b,tangent(a),tangent(b))=='retained','tangency discarded')
    # Three roots fit inside exactly the tiny audited interval, with opposite endpoint signs.
    a,b=map(rational,cert['hull']);w=b-a
    def multiple(x):
        t=(x-a)/w
        return x+w*R(1,4)*(t-R(1,4))*(t-R(1,2))*(t-R(3,4))
    roots=[a+w*t for t in (R(1,4),R(1,2),R(3,4))]
    need(all(multiple(x)==x for x in roots),'three-root construction')
    need(multiple(a)<a and multiple(b)>b,'three-root signs')
    need(classify(a,b,multiple(a),multiple(b))=='retained','three-root pruning')
    # Here the derivative >= 1/4 on [a,b]; strictly increasing extensions connect to (0,0),(1,1).
    need(0<multiple(a)<multiple(b)<1,'normalized extension possible')
    for k in [2,20,2000]:
        need(question(R(k,2*k))==R(k,2*k),'unreduced trivial exception')
    a,b=R(5,12),R(53,127)
    need(R(2,5)<a<b<R(3,7),'local decrease placement')
    need(question(b)-b<question(a)-a,'local decrease')
    for t in [R(1,4),R(2,5),R(3,7),R(1,2),R(3,4)]:
        need(question(t/(1+t))-t/(1+t)==(question(t)-t)/2+t*(t-1)/(2*(1+t)),'noninvariant diagonal')
    need(abs(question(R(3,7))-R(3,7))*49==R(7,16),'exception 3/7')
    need(abs(question(R(8,19))-R(8,19))*361==R(19,64),'exception 8/19')
    return dict(rejected_certificate_mutations=rejected,same_sign_endpoints='PASS',even_order_contact_preserved='PASS',three_roots_in_tiny_interval='PASS',unreduced_trivial_exceptions='PASS',local_nonmonotonicity='PASS',noninvariant_diagonal='PASS',small_denominator_exceptions='PASS')

def bind(root):
    raw=(root/'MANIFEST.json').read_bytes()
    need(len(raw)==1493 and digest(raw)==EXPECTED_MANIFEST,'frozen manifest mismatch')
    manifest=json.loads(raw);rows=[]
    need(len(manifest['files'])==8,'payload count')
    need({p.name for p in root.iterdir()}=={'MANIFEST.json'}|{r['path'] for r in manifest['files']},'unexpected packet entries')
    for row in manifest['files']:
        b=(root/row['path']).read_bytes()
        need(len(b)==row['bytes'] and digest(b)==row['sha256'],'payload mismatch: '+row['path'])
        rows.append(dict(path=row['path'],bytes=len(b),sha256=digest(b),matched=True))
    return dict(manifest_bytes=len(raw),manifest_sha256=digest(raw),payload_files=rows)

def main():
    root=Path(sys.argv[1]).resolve();binding=bind(root)
    original=json.loads((root/'EXACT_RESULTS.json').read_text())
    controls=positive_controls();cert,levels=make_certificate(128);validate_certificate(cert)
    need(cert==original['cylinder_exhaustion'],'original enclosure mismatch')
    a,b=map(rational,cert['hull']);scale=10**44
    digits=(a*scale).numerator//(a*scale).denominator
    need(digits==(b*scale).numerator//(b*scale).denominator,'decimal floor disagreement')
    need(str(digits)=='42037233942322307564099300664622187394918986','decimal prefix mismatch')
    bis,trace=bisect(160);need(bis==original['bisection'],'original bisection mismatch')
    need(a<=rational(bis['a'])<rational(bis['b'])<=b,'bisection not in enclosure')
    spacing,equivalent=scan(1500);need(spacing==original['rational_spacing'],'original scan mismatch')
    negatives=negative_controls(cert)
    need(bind(root)==binding,'packet changed during audit')
    results=dict(schema='independent-question-mark-audit-v1',verdict='PASS_WITH_SCOPE_LIMITS',binding=binding,
                 controls=controls,independent_cf_expansion_comparisons=equivalent,cylinder_exhaustion=cert,
                 nodes_by_depth=levels,decimal_prefix_44=str(digits),bisection=bis,bisection_trace=trace,
                 rational_spacing=spacing,negative_controls=negatives,
                 original_exact_sections_matched=['cylinder_exhaustion','bisection','rational_spacing'],
                 limits=['No exact fixed-point count or uniqueness proved.','No transcendence conclusion.','No unbounded rational-displacement bound proved.','No raw-corpus or exact aggregator wording verification.','No novelty or present global-openness conclusion.'])
    data=(json.dumps(results,indent=2,sort_keys=True)+'\n').encode();out=Path(__file__).with_name('INDEPENDENT_RESULTS.json')
    if '--check' in sys.argv:need(out.read_bytes()==data,'independent results changed')
    else:out.write_bytes(data)
    print('PASS: independent Euclidean/Stern-Brocot calculations agree with frozen packet')
    print('manifest',EXPECTED_MANIFEST)
    print('rational inputs',spacing['tested'],'CF expansion comparisons',equivalent)
    print('cylinder nodes',cert['visited'],'leaves',cert['leaf_count'],'retained',cert['retained_count'])
    print('width',str(b-a));print('bisection',bis['steps'],'steps')
    print('mutation rejections',len(negatives['rejected_certificate_mutations']))
    print('output bytes',len(data),'sha256',digest(data))
if __name__=='__main__':main()
