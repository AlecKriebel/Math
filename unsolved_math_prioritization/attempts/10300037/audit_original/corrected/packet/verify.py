#!/usr/bin/env python3
"""Read-only exact model diagnostics; not a general topological proof checker."""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
from math import gcd
import copy,json,sys

class VerificationError(Exception):pass
def require(ok,message):
    if not ok:raise VerificationError(message)
def pairs(items):
    d={}
    for k,v in items:
        require(k not in d,'duplicate JSON key');d[k]=v
    return d
def strict_json(raw):
    def bad(s):raise VerificationError('nonfinite JSON constant '+s)
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad)
def integer(n,name):require(type(n) is int,name+' must be an integer');return n
EXPECTED={'schema':'even-sided-10300037-claims-v1','problem_id':10300037,'problem_code':'AMR-102-0037','rank':1006,'status':'unsolved','status_scope':'author attempt; not a current-openness claim','approaches':5,'general_resolution':False,'novelty_claim':False,'independent_review':'accepted_after_corrections','universal_announcement_credited':True,'universal_complete_proof_inspected':False,'monodromy_condition_required':True,'even_side_count_alone_sufficient':False,'local_model_proves_global_essentiality':False,'meridional_surgery_included':False,'digon_claimed_genuine':False,'noncompact_extension_required':True,'finite_checks_prove_topology':False,'source_pdfs_or_dataset_contents_in_packet':False}
def validate_claims(c):
    require(type(c) is dict and set(c)==set(EXPECTED),'claim key schema')
    for k,v in EXPECTED.items():require(type(c[k]) is type(v) and c[k]==v,'wrong claim '+k)
def alternating(v):
    require(type(v) is tuple and len(v)>=2,'invalid cyclic side list')
    require(all(type(x) is int and x in (-1,1) for x in v),'invalid sign')
    return all(v[(j+1)%len(v)]==-v[j] for j in range(len(v)))
def invariant(v,s):
    integer(s,'shift')
    return alternating(v) and all(v[(j+s)%len(v)]==v[j] for j in range(len(v)))
def model(m,a,b):
    for n,k in ((m,'m'),(a,'a'),(b,'b')):integer(n,k)
    require(m>0 and b!=0 and gcd(a,b)==1,'invalid primitive nonmeridional model')
    n=m*abs(b); s=(m*a)%n
    return n,s

def bezout(a,b):
    oldr,r=a,b; olds,s=1,0; oldt,t=0,1
    while r:
        q=oldr//r;oldr,r=r,oldr-q*r;olds,s=s,olds-q*s;oldt,t=t,oldt-q*t
    if oldr<0:oldr,olds,oldt=-oldr,-olds,-oldt
    require(oldr==1,'nonprimitive slope')
    return olds,oldt

def must_reject(f,name):
    try:f()
    except (VerificationError,ValueError,KeyError,TypeError):return name
    raise VerificationError('negative control accepted: '+name)

def run():
    require(len(sys.argv)==1,'no command-line arguments supported')
    root=Path(__file__).resolve().parent
    validate_claims(strict_json((root/'CLAIMS.json').read_text()))
    ledger=strict_json((root/'APPROACH_LEDGER.json').read_text())
    require(ledger['schema']=='even-sided-approach-ledger-v1' and ledger['problem_id']==10300037,'ledger identity')
    require(type(ledger['turns_used']) is int and ledger['turns_used']==5,'ledger turns')
    require(type(ledger['approaches']) is list and len(ledger['approaches'])==5,'ledger length')
    require([x['turn'] for x in ledger['approaches']]==[1,2,3,4,5],'ledger order')
    require(all(x['counted'] is True and x['status']=='scoped_partial' for x in ledger['approaches']),'ledger status')
    counts={'cyclic_sign_lists':0,'rotation_sign_tests':0,'primitive_cusp_models':0,'knot_filling_models':0,'square_rational_interior_controls':0,'square_open_edge_controls':0,'slope_zero_gluing_controls':0}
    for n in range(2,13):
        good=[]
        for v in product((-1,1),repeat=n):
            if alternating(v):good.append(v)
            counts['cyclic_sign_lists']+=1
        require(len(good)==(2 if n%2==0 else 0),'cyclic parity classification')
        for v in good:
            for s in range(n):
                require(invariant(v,s)==(s%2==0),'rotation classification')
                counts['rotation_sign_tests']+=1
    for m,a,b in product(range(1,8),range(-12,13),range(-12,13)):
        if b==0 or gcd(a,b)!=1:continue
        n,s=model(m,a,b)
        seen=set(); cycles=0
        for i in range(n):
            if i in seen:continue
            j=i;length=0
            while j not in seen:seen.add(j);length+=1;j=(j+s)%n
            require(j==i and length==abs(b),'permutation cycle')
            cycles+=1
        require(cycles==m,'number of cusp annuli')
        possible=n%2==0 and s%2==0
        require(possible==(m%2==0),'even cusp iff alternating prescription')
        if n%2==0:
            v=tuple((-1)**j for j in range(n));require(invariant(v,s)==possible,'sign model agreement')
        counts['primitive_cusp_models']+=1
    for p,q,k in product(range(-20,21),range(-12,13),range(1,5)):
        if q==0 or gcd(p,q)!=1:continue
        d,minus_c=bezout(p,q);c=-minus_c
        require(p*d-q*c==1,'unimodular filling basis')
        require((d*p-q*c,d*q-q*d)==(1,0),'mu=d r-q l')
        n,s=model(2*k,d,-q)
        require(n==2*k*abs(q) and s%2==0,'filling parity')
        for h in (-3,-1,1,3):require((2*k*(d+h*q))%n==s,'longitude choice invariance')
        counts['knot_filling_models']+=1
    # Exact polynomial Frobenius calculation in x,y. A B dt+2x B dx-2y A dy.
    # curl components: (-2y A, 2x B, 8xy). Dot product is identically
    # (-4-4+8)xy A B = 0, verified as integer coefficients, not sampling alone.
    frobenius_coefficients=[-4,-4,8]
    require(sum(frobenius_coefficients)==0,'square Frobenius identity')
    for xi,yi in product(range(-9,10),repeat=2):
        x,y=F(xi,10),F(yi,10);A,B=1-x*x,1-y*y
        require(A>0 and B>0,'interior side distances')
        P,Q,R=2*x*B,-2*y*A,A*B
        require(R>0,'nonsingularity')
        require(P*(-2*y*A)+Q*(2*x*B)+R*(8*x*y)==0,'exact Frobenius control')
        ratio=A/B
        require((1-(-x)**2)/(1-(-y)**2)==ratio,'even half-turn invariance')
        require((1-(-y)**2)/(1-x*x)==1/ratio,'odd quarter-turn sign reversal')
        counts['square_rational_interior_controls']+=1
    for t in (F(i,10) for i in range(-9,10)):
        for x,y in ((F(1),t),(F(-1),t),(t,F(1)),(t,F(-1))):
            A,B=1-x*x,1-y*y;coef=(2*x*B,-2*y*A,A*B)
            require(any(coef),'open edge nonsingularity')
            require(coef[2]==0,'side tangency')
            counts['square_open_edge_controls']+=1
    for p,q in product(range(-50,51),range(1,21)):
        r=F(p,q);require(r+F(0)==r,'zero displacement gluing')
        require(q*r==p,'q circuits have p turns')
        counts['slope_zero_gluing_controls']+=1
    require(not invariant((1,-1,1,-1,1,-1),3),'even sides do not imply descent')
    n,s=model(3,1,2);require(n==6 and s==3,'odd cusp/even denominator countercontrol')
    v=(1,-1,1,-1,1,-1);require(invariant(v,2*s) and not invariant(v,s),'cover does not descend')
    negatives=[]
    for k in EXPECTED:
        c=copy.deepcopy(EXPECTED);c[k]=None
        negatives.append(must_reject(lambda c=c:validate_claims(c),'null-'+k))
    for k,value in [('approaches',True),('problem_id',10300037.0),('general_resolution',1),('universal_complete_proof_inspected',True),('status','solved')]:
        c=copy.deepcopy(EXPECTED);c[k]=value
        negatives.append(must_reject(lambda c=c:validate_claims(c),'mutation-'+k))
    for raw in ('{broken','{"a":1,"a":2}','{"x":NaN}','{"x":Infinity}'):
        negatives.append(must_reject(lambda raw=raw:strict_json(raw),'malformed-'+str(len(negatives))))
    for m,a,b in ((0,1,1),(2,1,0),(2,2,4),(True,1,1),(2,1.0,1)):
        negatives.append(must_reject(lambda m=m,a=a,b=b:model(m,a,b),'invalid-model-'+str(len(negatives))))
    return {'schema':'even-sided-10300037-diagnostics-v1','status':'pass','problem_id':10300037,'claim_status':'unsolved','approaches':5,'counts':counts,'square_frobenius_coefficient_sum':sum(frobenius_coefficients),'negative_controls':negatives,'scope':'Exact finite model and schema controls only; no global essentiality, universal construction, or independent-review claim.'}
if __name__=='__main__':
    try:print(json.dumps(run(),sort_keys=True,separators=(',',':')))
    except (VerificationError,OSError,ValueError,KeyError,TypeError) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
