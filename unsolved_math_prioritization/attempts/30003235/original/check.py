#!/usr/bin/env python3
"""Exact finite controls, metadata checks, and byte integrity; not a proof assistant."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from math import lcm
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parent
COUNTS = {}

class VerificationError(Exception):
    pass

def need(condition, family, message):
    if not condition:
        raise VerificationError(f'{family}: {message}')
    COUNTS[family] = COUNTS.get(family, 0) + 1

def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        raise VerificationError(f'JSON input rejected: {exc}') from exc

def norm(x):
    x = F(x)
    r = x - (x.numerator // x.denominator)
    return min(r, 1-r)

def det(v):
    a,b,c = v
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])

def rank(rows):
    a = [[F(x) for x in row] for row in rows]
    r = 0
    for col in range(3):
        p = next((k for k in range(r,len(a)) if a[k][col]), None)
        if p is None:
            continue
        a[r],a[p] = a[p],a[r]
        z = a[r][col]
        a[r] = [t/z for t in a[r]]
        for k in range(len(a)):
            if k != r:
                z = a[k][col]
                a[k] = [a[k][j]-z*a[r][j] for j in range(3)]
        r += 1
        if r == len(a):
            break
    return r

def height_power(A,B,i,j,k):
    need(i>0 and j>0 and i+j==1, 'height_domain', 'invalid weights')
    ei,ej = F(k)/i,F(k)/j
    need(ei.denominator==1 and ej.denominator==1, 'height_domain', 'noninteger power')
    return max(abs(F(A))**int(ei),abs(F(B))**int(ej))

def check_claims(path):
    d=read_json(path)
    expected={
        'schema':1,'problem_id':30003235,'author_approaches':5,'status':'unsolved',
        'positive_weights_required':True,'nonzero_slope_required':True,
        'global_endpoint_proved':False,
        'rational_point_line_endpoint_proved_relative_to_fiber_theorem':True,
        'arbitrary_real_projective_invariance_claimed':False,
        'finite_checks_are_proof':False,'historical_novelty_claimed':False}
    need(type(d) is dict and set(d)==set(expected),'claim_schema','fields differ')
    for k,v in expected.items():
        need(type(d[k]) is type(v) and d[k]==v,'claim_scope',f'unsupported {k}')

def check_probes(path):
    probes=read_json(path)
    need(type(probes) is list and len(probes)==3,'probe_schema','expected three probes')
    for p in probes:
        need(type(p) is dict and 'kind' in p,'probe_schema','malformed probe')
        if p['kind']=='rank_bound':
            need(set(p)=={'kind','vectors','claimed_max_rank'},'probe_schema','rank fields')
            v=p['vectors']
            need(type(v) is list and len(v)>0 and all(type(r) is list and len(r)==3 and all(type(x) is int for x in r) for r in v),'probe_schema','integer triples required')
            need(type(p['claimed_max_rank']) is int and 0<=p['claimed_max_rank']<=3,'probe_schema','rank bound type')
            need(rank(v)<=p['claimed_max_rank'],'rank_probe','false rank claim')
        elif p['kind']=='projective_identity':
            need(set(p)=={'kind','x','y','u','v'},'probe_schema','projective fields')
            try:
                x,y,u,v=[F(p[k]) for k in ('x','y','u','v')]
            except (ValueError,TypeError,ZeroDivisionError) as exc:
                raise VerificationError('malformed projective rational') from exc
            need(x!=0,'projective_probe','zero denominator')
            need(x*u==1 and x*v==y,'projective_probe','false inversion identity')
        elif p['kind']=='cf_step':
            need(set(p)=={'kind','t','q_prev','q','q_next'},'probe_schema','CF fields')
            need(all(type(p[k]) is int for k in ('t','q_prev','q','q_next')),'probe_schema','CF integers required')
            t,prev,q,qn=[p[k] for k in ('t','q_prev','q','q_next')]
            need(t>=2 and 0<prev<q,'cf_probe','invalid recurrence domain')
            need(qn==q**t+prev,'cf_probe','false denominator recurrence')
        else:
            raise VerificationError('unknown probe kind')

def check_math():
    # Rational truncations and exact recurrences. Infinite tails are proved in PROOF.md.
    for t in (2,3,4):
        pprev,p,qprev,q=0,1,1,2
        conv=[(p,q)]
        for n in range(5):
            digit=q**(t-1)
            pn,qn=digit*p+pprev,digit*q+qprev
            need(q**t<=qn<=3*q**t,'cf_recurrence','growth sandwich')
            need(abs(pn*q-p*qn)==1,'cf_recurrence','unimodular convergents')
            conv.append((pn,qn))
            pprev,p,qprev,q=p,pn,q,qn
        approx=F(p,q)
        for qtest in range(1,301):
            need(qtest**t*norm(qtest*approx)>F(1,5),'cf_finite_errors','finite truncation lower control')
        for pn,qn in conv[:-2]:
            need(F(1,5)<qn**t*abs(qn*approx-pn)<=1,'cf_finite_errors','convergent critical normalization')
    # Exponent bookkeeping for the true nearby-weight consequence.
    for d in range(3,40):
        s0=F(1,2)
        s=F(1,d)
        tau0,tau=1/s0,1/s
        eps=(tau-tau0)/2
        need(eps>0 and tau-eps-tau0==eps,'weight_perturbation','positive excess')
    # Scalar diagnostic only, not a constructed real vector.
    for n in range(1,21):
        for delta in (F(1,12),F(1,6),F(1,4)):
            exponent=120*n*n*delta
            need(exponent.denominator==1,'scalar_limit_control','integer test exponent')
            off=F(2**int(exponent),n)
            need(off>=F(1,n) and off>=n,'scalar_limit_control','separated scalar growth')
    # Exact rational projective identities and weighted height estimates.
    rng=random.Random(30003235)
    weights=[(F(1,2),F(1,2)),(F(2,3),F(1,3)),(F(3,4),F(1,4))]
    for z in range(1600):
        x=F(rng.choice([k for k in range(-7,8) if k]),rng.randint(1,7))
        y=F(rng.randint(-9,9),rng.randint(1,7))
        u,v=1/x,y/x
        A,B,C=[rng.randint(-12,12) for _ in range(3)]
        if A==B==0:
            continue
        form=A*u+B*v+C
        need(x*form==C*x+B*y+A,'projective_identity','coefficient permutation')
        need(1/u==x and v/u==y,'projective_identity','involution')
        if abs(form)<1:
            K=1+abs(u)+abs(v)
            need(abs(C)<=K*max(abs(A),abs(B)),'projective_height','linear coefficient bound')
            for i,j in weights:
                k=lcm(i.numerator,j.numerator)
                lhs=height_power(C,B,i,j,k)
                rhs=K**int(F(k)/i)*height_power(A,B,i,j,k)
                need(lhs<=rhs,'projective_height','heavier-coordinate height bound')
    # A diagnostic showing the same height proof cannot ignore the weight order.
    i,j,k=F(1,3),F(2,3),2
    need(height_power(100,100,i,j,k)>3**6*height_power(0,100,i,j,k),'weight_order_negative','missing order would pass')
    # Rational-point coefficient identities, valid independently of a global hypothesis.
    for a in (F(2,7),F(-5,9),F(13,4)):
        for r,s in ((F(1,2),F(2,3)),(F(-3,5),F(4,7)),(F(0),F(1))):
            d=lcm(r.denominator,s.denominator)
            b=s-a*r
            K=max(d,abs(d*r))
            for q in range(1,101):
                need(max(norm(d*q*a),norm(d*q*b))<=K*norm(q*a),'rational_point_coefficients','dilation reduction')
    # Local resonance bounds: kappa here is a one-Q control, not a global claim.
    for n in range(2,6):
        for a in (F(2,7),F(3,5),F(5,8)):
            for B in range(3,70):
                A=-((a*B+F(1,2)).numerator//(a*B+F(1,2)).denominator)
                alpha=A+a*B
                if not alpha or abs(alpha)>abs(a)*B/2:
                    continue
                b=F(7,11); C=-(b*B).numerator//(b*B).denominator
                beta=C+b*B
                h=F(B**n)
                hlow=(abs(a)/2)**n
                kappa=B**n*max(norm(B*a),norm(B*b))
                if not kappa:
                    continue
                eta=kappa*hlow/4
                center=-beta/alpha
                X=abs(center)+1
                need(abs(alpha)>=kappa/(2*(X+1)*B**n),'resonance_local','slope elimination')
                need(2*eta/(h*abs(alpha))<=4*(X+1)*eta/(kappa*hlow),'resonance_local','interval bound')
    # Exact determinant column identity on arbitrary triples.
    for n in range(800):
        rows=[[rng.randint(-20,20) for _ in range(3)] for _ in range(3)]
        x0,a,b=F(2,3),F(5,7),F(-4,9)
        transformed=[[A,B,A*x0+B*(a*x0+b)+C] for A,B,C in rows]
        need(det(rows)==det(transformed),'determinant_identity','column operation')
        HA=max(abs(z[0]) for z in transformed)
        HB=max(abs(z[1]) for z in transformed)
        E=max(abs(z[2]) for z in transformed)
        need(abs(det(rows))<=6*HA*HB*E,'determinant_bound','six-term estimate')
    # Actual height-window families with rational concurrency, and the rank-two boundary.
    for N in range(2,32):
        H=N**4; R=H; eta=F(1,24*R); a=F(1); Ca=2
        radius=F(1,24*Ca*N**6)
        need(6*Ca*N**6*radius+6*eta*R==F(1,2),'determinant_scale','strict integer bound')
        rows=[[1,0,0],[0,1,0],[N,N,0]]
        need(rank(rows)==2 and det(rows)==0,'determinant_rank','rank-two pencil')
    need(rank([[1,0,0],[0,1,0],[0,0,1]])==3,'determinant_rank','rank-three negative boundary')

def check_integrity():
    manifest=read_json(ROOT/'MANIFEST.json')
    need(type(manifest) is dict and set(manifest)=={'schema','files'} and manifest['schema']==1,'manifest_schema','invalid manifest')
    entries=manifest['files']
    need(type(entries) is list and len(entries)>0,'manifest_schema','empty manifest')
    expected=[]
    for e in entries:
        need(type(e) is dict and set(e)=={'path','bytes','sha256'},'manifest_schema','file entry schema')
        name=e['path']; rel=Path(name)
        need(type(name) is str and not rel.is_absolute() and '..' not in rel.parts and name!='MANIFEST.json','manifest_schema','unsafe path')
        p=ROOT/rel
        need(p.is_file() and not p.is_symlink(),'manifest_integrity','missing or symlinked file')
        b=p.read_bytes()
        need(type(e['bytes']) is int and len(b)==e['bytes'],'manifest_integrity',f'size {name}')
        need(hashlib.sha256(b).hexdigest()==e['sha256'],'manifest_integrity',f'hash {name}')
        expected.append(name)
    actual=sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p.name!='MANIFEST.json')
    need(sorted(expected)==actual and len(set(expected))==len(expected),'manifest_integrity','file set drift')
    ledger=read_json(ROOT/'APPROACH_LEDGER.json')
    author=[x for x in ledger if x.get('counts_as_author_approach') is True]
    need([x['sequence'] for x in author]==list(range(1,6)),'author_history','approach sequence')
    need([x['time_utc'] for x in author]==sorted(x['time_utc'] for x in author),'author_history','chronology')
    for x in author:
        data=(ROOT/x['checkpoint']).read_bytes()
        need(hashlib.sha256(data).hexdigest()==x['proof_sha256_at_checkpoint'],'author_history','historical proof bytes')
    need((ROOT/'PROOF.md').read_bytes()==(ROOT/'checkpoints/05_PROOF.md').read_bytes(),'author_history','final checkpoint drift')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--claims',type=Path,default=ROOT/'claims.json')
    parser.add_argument('--probes',type=Path,default=ROOT/'probes.json')
    args=parser.parse_args()
    try:
        check_claims(args.claims)
        check_probes(args.probes)
        check_math()
        check_integrity()
    except (VerificationError,OSError,ValueError,TypeError,KeyError,ZeroDivisionError) as exc:
        print(json.dumps({'status':'FAIL','reason':str(exc)},sort_keys=True))
        return 1
    print(json.dumps({'status':'PASS','scope':'finite_controls_and_integrity_only','counts':COUNTS,'total_checks':sum(COUNTS.values())},sort_keys=True))
    return 0

if __name__=='__main__':
    sys.exit(main())
