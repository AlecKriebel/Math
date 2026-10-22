#!/usr/bin/env python3
"""Exact finite algebra checks, not a proof checker for the cited topology."""
from pathlib import Path
import hashlib,json,re,sys
class Reject(Exception): pass
def require(ok,msg):
    if not ok: raise Reject(msg)
def pairs(xs):
    d={}
    for k,v in xs:
        require(k not in d,'duplicate JSON key')
        d[k]=v
    return d
def read(name):
    return json.loads((Path(__file__).resolve().parent/name).read_text(),object_pairs_hook=pairs)
def exact(x,y,msg):require(type(x) is type(y) and x==y,msg)
def integer(x):return type(x) is int
# Sparse polynomials in x,a0,a1,b0,b1,c0,c1, truncated by x^2.
z=(0,)*7
def con(n):return {} if n==0 else {z:n}
def var(i):
    v=list(z);v[i]=1;return {tuple(v):1}
def add(*xs):
    r={}
    for p in xs:
        for m,c in p.items():r[m]=r.get(m,0)+c
    return {m:c for m,c in r.items() if c}
def neg(p):return {m:-c for m,c in p.items()}
def mul(p,q):
    r={}
    for a,c in p.items():
        for b,d in q.items():
            m=tuple(u+v for u,v in zip(a,b))
            if m[0]<2:r[m]=r.get(m,0)+c*d
    return {m:c for m,c in r.items() if c}
def power(p,n):
    require(integer(n) and n>=0,'bad exponent');r=con(1)
    for _ in range(n):r=mul(r,p)
    return r
def main():
    require(len(sys.argv)==1,'no arguments permitted')
    c=read('CERTIFICATE.json')
    require(type(c) is dict and set(c)=={'schema','problem_id','ranks','casson_normalization','first_coefficients','forced_rank_three','second_difference','coefficient_formula','base_ring','quantum_parameter','quotient_level','witness','limitations'},'certificate schema')
    exact(c['schema'],'habiro-rank-certificate-v1','schema');exact(c['problem_id'],10400145,'problem')
    require(type(c['ranks']) is list and all(integer(n) for n in c['ranks']),'ranks types');exact(c['ranks'],[1,2,3],'ranks')
    exact(c['casson_normalization'],-1,'Casson value');exact(c['quotient_level'],3,'level')
    require(type(c['first_coefficients']) is list and all(integer(n) for n in c['first_coefficients']),'coefficient types')
    actual=[n*(n*n-1)*c['casson_normalization'] for n in c['ranks']]
    exact(c['first_coefficients'],actual,'coefficients')
    exact(c['forced_rank_three'],2*actual[1]-actual[0],'forced value')
    residual=actual[2]-2*actual[1]+actual[0];exact(c['second_difference'],residual,'residual');require(residual!=0,'missing obstruction')
    exact(c['coefficient_formula'],'n*(n*n-1)*lambda','formula');exact(c['base_ring'],'Z[x]/(x^2)','base ring');exact(c['quantum_parameter'],'q=1+x','parameter')
    exact(c['witness'],'Poincare sphere: minus-one surgery on the left-handed trefoil','witness')
    exact(c['limitations'],['Finite algebra checks only; primary topological inputs are cited, not computationally proved.'],'limitations')
    x=var(0);q=add(con(1),x)
    coeff=[add(var(i),mul(var(i+1),x)) for i in (1,3,5)]
    evals=[add(*[mul(coeff[j],power(q,j*n)) for j in range(3)]) for n in (1,2,3)]
    require(not add(evals[2],neg(evals[1]),neg(evals[1]),evals[0]),'generic three-node identity')
    # q(1+q)(1-q^3) is the k=1 Poincare summand, with the denominator cancelled.
    term=mul(mul(q,add(con(1),q)),add(con(1),neg(power(q,3))))
    require(term==mul(con(-6),x),'Poincare linear term')
    for k in range(2,10):
        # cancel 1-q from the first factor, leaving the geometric sum.
        geom=add(*[power(q,j) for j in range(k+1)])
        term=mul(power(q,k),geom)
        for j in range(k+2,2*k+2):term=mul(term,add(con(1),neg(power(q,j))))
        require(not term,'sample tail order')
    claims=read('CLAIMS.json');exact(claims['schema'],'habiro-rank-claims-v1','claims schema');exact(claims['problem_id'],10400145,'claims identity');exact(claims['status'],'claimed_solved','claims status');exact(claims['resolution'],'negative_literal_statement','resolution');exact(claims['approaches_used'],1,'turns')
    for key in ('novelty_claim','formal_verification_claim','human_review_claim'):exact(claims[key],False,key)
    exact(claims['full_original_scope'],True,'scope flag')
    ledger=read('APPROACH_LEDGER.json');exact(ledger['schema'],'habiro-rank-ledger-v1','ledger schema');exact(ledger['used'],1,'ledger used');exact(ledger['budget'],5,'ledger budget');require(len(ledger['approaches'])==1,'ledger approaches');exact(ledger['approaches'][0]['number'],1,'approach number')
    sources=read('SOURCE_METADATA.json');exact(sources['schema'],'habiro-rank-sources-v1','source schema');require(type(sources['sources']) is list and {s['id'] for s in sources['sources']}=={'O','L','HL','HL-published','LQ','H','L-preprint','HL-older','BG'},'source inventory')
    for s in sources['sources']:
        require(integer(s['bytes']) and s['bytes']>0,'source byte count');require(type(s['sha256']) is str and re.fullmatch('[0-9a-f]{64}',s['sha256']) is not None,'source digest');require(type(s['url']) is str and s['url'].startswith('https://'),'source URL')
    gate=read('GATE_METADATA.json');exact(gate['schema'],'habiro-rank-gate-v1','gate schema');exact(gate['substantive_prior_attempt_found'],False,'prior attempt');exact(gate['exact_target_pr_matches'],0,'PR count')
    return {'schema':'habiro-rank-diagnostics-v1','status':'PASS','generic_first_jet_identity':True,'ranks':c['ranks'],'observed':actual,'forced_rank_three':c['forced_rank_three'],'second_difference':residual,'poincare_rank_two_first_coefficient':-6,'sample_tail_terms_checked':8,'scope':'Exact finite algebra only; primary topological inputs are not proved by this program.'}
if __name__=='__main__':
    try: print(json.dumps(main(),sort_keys=True,separators=(',',':')))
    except (Reject,OSError,ValueError,KeyError,TypeError,IndexError) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
