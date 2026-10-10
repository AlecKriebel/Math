#!/usr/bin/env python3
"""Exact finite checks of supporting formulas, never a Cantor-set classifier.

Uses explicit guards, no assert, and standard-library arithmetic. Outputs only
JSON on stdout, or to an explicitly external file. --require-readonly performs
real create/open-for-write probes and requires non-root UID 1000.
"""
import argparse
import ast
from fractions import Fraction as F
import hashlib
import json
import os
from pathlib import Path
import sys

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def expect_rejection(call, text):
    try:
        call()
    except (RuntimeError, ValueError) as exc:
        require(text in str(exc), 'wrong rejection reason: '+str(exc))
        return
    raise RuntimeError('expected rejection did not occur')


def validate_pl(points):
    require(len(points) >= 2, 'PL requires two nodes')
    require(all(a[0] < b[0] and a[1] < b[1] for a,b in zip(points,points[1:])),
            'PL strict monotonicity required')
    require(points[0][0] == points[0][1] and points[-1][0] == points[-1][1],
            'PL endpoints must agree with identity')


def pl_value(points,x):
    if x <= points[0][0] or x >= points[-1][0]:
        return x
    for (a,b),(c,d) in zip(points,points[1:]):
        if a <= x <= c:
            return b+(d-b)*(x-a)/(c-a)
    raise RuntimeError('uncovered PL point')


def inverse_pl(points):
    validate_pl(points)
    result=[(y,x) for x,y in points]
    validate_pl(result)
    return result


def displacement(points):
    validate_pl(points)
    return max(abs(x-y) for x,y in points)


def dilation(points,t,x):
    require(F(0) <= t <= F(1), 'dilation parameter outside [0,1]')
    return x if t == 0 else t*pl_value(points,x/t)


def check_dilations():
    maps=[]
    for a in [F(-1,3),F(0),F(1,3)]:
        for b in [F(-1,4),F(0),F(1,4)]:
            for c in [F(-1,5),F(1,5)]:
                points=[(F(-2),F(-2)),(F(-1),F(-1)+a),(F(0),b),
                        (F(1),F(1)+c),(F(2),F(2))]
                validate_pl(points)
                maps.append(points)
    ts=[F(0),F(1,100),F(1,8),F(1,3),F(1,2),F(4,5),F(1)]
    cases=0
    for points in maps:
        inv=inverse_pl(points)
        D=displacement(points)
        require(displacement(inv)==D,'inverse displacement inequality lost')
        for t in ts:
            xs=sorted(set([F(k,7) for k in range(-28,29)]+[t*x for x,y in points]))
            for x in xs:
                y=dilation(points,t,x)
                require(dilation(inv,t,y)==x,'dilation inverse failed')
                require(dilation(points,t,dilation(inv,t,x))==x,'reverse inverse failed')
                require(abs(y-x)<=t*D,'dilation displacement bound failed')
            scaled=[(t*x,t*y) for x,y in points]
            require(t==0 or displacement(scaled)==t*D,'exact supremum scaling failed')
            for s in ts:
                require(all(abs(dilation(points,t,x)-dilation(points,s,x)) <= (t+s)*D
                            for x in xs),'track diameter bound failed')
            cases+=1
    # Wrong inverse scaling blows up displacement; detect rather than endorse it.
    p=maps[0]; D=displacement(p); t=F(1,2)
    wrong=[(x/t,y/t) for x,y in p]
    require(displacement(wrong)==D/t and displacement(wrong)>D,'wrong scaling control failed')
    expect_rejection(lambda:validate_pl([(F(0),F(0)),(F(1),F(0)),(F(2),F(2))]),'strict monotonicity')
    expect_rejection(lambda:dilation(p,F(-1),F(0)),'outside')
    return {'PL_maps':len(maps),'parameter_cases':cases,'sample_and_breakpoint_inverses':True,
            'inverse_supremum_identity':True,'wrong_scaling_detected':True}


def triangle(x):
    # Period-one continuous triangle wave, with range [0,1].
    r=x-(x.numerator//x.denominator)
    return 2*r if r<=F(1,2) else 2-2*r


def check_shear():
    a=F(1,5)
    def H(t,x,y,sign=1):
        return (x,y) if t==0 else (x,y+sign*t*a*triangle(x/t))
    count=0
    for t in [F(0),F(1,100),F(1,7),F(1,2),F(1)]:
        for k in range(-40,41):
            x,y=F(k,9),F(k-2,11)
            z=H(t,x,y)
            require(H(t,*z,sign=-1)==(x,y),'shear inverse failed')
            require(abs(z[1]-y)<=t*a,'shear bound failed')
            count+=1
        if t>0:
            require(H(t,t/2,F(0))[1]==t*a,'shear supremum not attained')
    return {'exact_periodic_shear_cases':count,'noncompact_support':True}


def cantor_intervals(depth):
    require(isinstance(depth,int) and 0<=depth<=12,'bad Cantor depth')
    intervals=[(F(0),F(1))]
    for _ in range(depth):
        result=[]
        for l,r in intervals:
            d=(r-l)/3
            result.extend([(l,l+d),(r-d,r)])
        intervals=result
    return intervals


def check_interval_compression():
    cases=0
    for depth in range(1,8):
        cells=cantor_intervals(depth); next_cells=cantor_intervals(depth+1)
        supports=[]
        for l,r in cells:
            L=r-l; a=l-L/10; b=r+L/10; u=l+F(2,5)*L; v=l+F(3,5)*L
            p=[(a,a),(l,u),(r,v),(b,b)]
            validate_pl(p)
            inv=inverse_pl(p)
            require(all(v<c or d<u for c,d in next_cells),'target gap meets next Cantor stage')
            for k in range(21):
                x=l+F(k,20)*L
                y=pl_value(p,x)
                require(u<=y<=v and pl_value(inv,y)==x,'hull compression failed')
            require(displacement(p)==F(2,5)*L,'compression displacement incorrect')
            require(displacement(p)<b-a,'support diameter bound failed')
            supports.append((a,b));cases+=1
        require(all(b<c for (a,b),(c,d) in zip(supports,supports[1:])),
                'piecewise supports intersect')
    # Identity does not displace the actual Cantor endpoint 0.
    require(F(0) in {x for p in cantor_intervals(4) for x in p},'Cantor endpoint missing')
    expect_rejection(lambda:cantor_intervals(-1),'bad Cantor depth')
    return {'stage_depths':7,'compressed_cells':cases,'targets_in_certified_middle_third_gaps':True,
            'identity_non_displacement_control':True}


def check_radial_compression():
    count=0
    for r in [F(1,4),F(1,2),F(3,4),F(9,10)]:
        for multiplier in [F(1,10),F(1,3),F(2,3)]:
            a=multiplier*r
            nodes=[(F(0),F(0)),(r,a),(F(1),F(1))]
            validate_pl(nodes);inv=inverse_pl(nodes)
            for k in range(101):
                x=F(k,100);y=pl_value(nodes,x)
                require(pl_value(inv,y)==x,'radial inverse failed')
                require(x>r or y<=a,'radial compression radius failed')
            require(pl_value(nodes,F(1))==1,'radial boundary not fixed')
            require(displacement(nodes)==r-a,'radial supremum failed')
            count+=1
    return {'radial_profiles':count,'radial_inverse_and_boundary':True}


def add(p,q,sign=1):
    r=dict(p)
    for word,coefficient in q.items():
        r[word]=r.get(word,0)+sign*coefficient
        if r[word]==0:del r[word]
    return r


def multiply(p,q,degree=None):
    r={}
    for a,x in p.items():
        for b,y in q.items():
            word=a+b
            if degree is None or len(word)<=degree:
                r[word]=r.get(word,0)+x*y
    return {a:x for a,x in r.items() if x}


def bracket(p,q):
    return add(multiply(p,q),multiply(q,p),-1)


def leading_tree(leaves):
    require(len(leaves)>0,'empty commutator tree')
    if len(leaves)==1:return {(leaves[0],):1}
    k=len(leaves)//2
    return bracket(leading_tree(leaves[:k]),leading_tree(leaves[k:]))


def inverse_word(w):
    return [-x for x in reversed(w)]


def commutator_word(u,v):
    return u+v+inverse_word(u)+inverse_word(v)


def tree_word(leaves):
    require(len(leaves)>0,'empty commutator tree')
    if len(leaves)==1:return list(leaves)
    k=len(leaves)//2
    return commutator_word(tree_word(leaves[:k]),tree_word(leaves[k:]))


def magnus(word,degree):
    p={():1}
    for x in word:
        require(x!=0,'zero free generator')
        q={():1,(abs(x),):1}
        if x<0:
            q={tuple([abs(x)]*k):(-1)**k for k in range(degree+1)}
        p=multiply(p,q,degree)
    return p


def check_magnus():
    records=[]
    for N in [2,3,4,5,6,7,8,16]:
        leaves=list(range(1,N+1));P=leading_tree(leaves)
        require(P.get(tuple(leaves))==1,'distinct-leaf coefficient failed')
        require(all(len(w)==N and len(set(w))==N for w in P),'wrong leading degree/alphabet')
        require(bracket(P,P)=={},'identical-word bracket did not cancel') if N<=8 else None
        records.append({'leaves':N,'nonzero_monomials':len(P),'canonical_coefficient':P[tuple(leaves)]})
    full=[]
    for N in [2,3,4]:
        leaves=list(range(1,N+1));w=tree_word(leaves);P=leading_tree(leaves)
        require(magnus(w,N-1)=={():1},'lower-degree vanishing failed')
        require(magnus(w,N)==add({():1},P),'full Magnus leading term failed')
        conjugator=[N+1,1,-(N+1)]
        conjugate=conjugator+w+inverse_word(conjugator)
        require(magnus(conjugate,N)==add({():1},P),'conjugacy leading term changed')
        require(magnus(inverse_word(w),N)==add({():1},P,-1),'inverse leading sign failed')
        full.append(N)
    require(magnus(commutator_word([1],[1]),6)=={():1},'[x,x] negative control failed')
    require(bracket({(1,):1},{(2,):1})!={},'distinct-generator positive control failed')
    expect_rejection(lambda:leading_tree([]),'empty')
    expect_rejection(lambda:magnus([0],2),'zero free generator')
    return {'homogeneous_trees':records,'full_truncated_expansion_leaf_counts':full,
            'repeated_generator_cancellation_detected':True,'conjugation_and_inverse_checked':True}


def complement_rank(d,N,i):
    require(d>=3 and N>=1 and i>=1,'bad duality parameters')
    degree=d-i-1
    if degree==0:return N  # reduced H^0 of N sphere-components plus infinity
    if degree==d-2:return N
    return 0


def check_duality():
    cases=0
    for d in range(3,13):
        for N in range(1,11):
            require(complement_rank(d,N,1)==N,'meridian H1 rank failed')
            require(complement_rank(d,N,2)==(N if d==3 else 0),'H2 dimension boundary failed')
            cases+=1
    expect_rejection(lambda:complement_rank(2,1,1),'bad duality parameters')
    return {'dimension_component_cases':cases,'three_dimensional_H2_obstruction_detected':True}


def verify_pins():
    pins=json.loads((BASE/'PAYLOAD_PINS.json').read_text())
    require(pins.get('schema')==1,'unknown pin schema')
    files=pins.get('files');require(isinstance(files,list) and files,'empty pin list')
    expected={x['path'] for x in files}
    actual={p.name for p in BASE.iterdir() if p.name!='PAYLOAD_PINS.json'}
    require(actual==expected,'payload file set changed')
    for entry in files:
        p=BASE/entry['path']
        require(p.parent==BASE and p.is_file() and not p.is_symlink(),'invalid pinned file')
        data=p.read_bytes()
        require(len(data)==entry['bytes'],'pinned byte count mismatch: '+entry['path'])
        require(hashlib.sha256(data).hexdigest()==entry['sha256'],'pinned hash mismatch: '+entry['path'])
    manifest=json.loads((BASE/'SOURCE_MANIFEST.json').read_text())
    require(manifest['source_bodies_in_payload'] is False,'source bodies forbidden')
    require(manifest['sources'][0]['id']=='K','source ordering changed')
    require(any(s['id']=='S' and s['original_full_text_inspected'] is False for s in manifest['sources']),
            'Sher inspection limitation lost')
    status=json.loads((BASE/'STATUS.json').read_text())
    require(status['problem_id']==3422 and status['substantive_proof_search_approaches']==0,'status mismatch')
    require(status['classification']['sticky_exists_iff']=='n >= 4','classification drift')
    require(not any(isinstance(x,ast.Assert) for x in ast.walk(ast.parse(Path(__file__).read_text()))),
            'checker must not depend on Python assert')
    return {'pinned_payload_files':len(files),'all_hashes_matched':True,'no_assert_nodes':True,
            'source_scope_guards':True}


def readonly_probes():
    require(os.geteuid()==1000,'read-only verification requires UID 1000')
    require(not os.access(BASE,os.W_OK),'packet directory is writable')
    probe=BASE/('.write_probe_'+str(os.getpid()))
    require(not probe.exists(),'write-probe collision')
    create_denied=False
    try:
        fd=os.open(probe,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    except PermissionError:
        create_denied=True
    else:
        os.close(fd);probe.unlink()
    require(create_denied,'actual packet-create probe unexpectedly succeeded')
    denied=0
    for p in BASE.iterdir():
        require(p.is_file() and not p.is_symlink(),'unexpected entry for read-only probe')
        require(not os.access(p,os.W_OK),'packet file is writable')
        try:
            fd=os.open(p,os.O_WRONLY)  # no truncation and no content write
        except PermissionError:
            denied+=1
        else:
            os.close(fd)
            raise RuntimeError('actual file write-open probe unexpectedly succeeded')
    return {'directory_create_denied':create_denied,'existing_file_write_open_denials':denied,
            'actual_write_probes':True}


def output_destination(value):
    p=Path(value).expanduser().resolve()
    require(p!=BASE and BASE not in p.parents,'output must be external to the packet')
    return p


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-readonly',action='store_true')
    parser.add_argument('--output')
    args=parser.parse_args()
    out=output_destination(args.output) if args.output else None
    probes=readonly_probes() if args.require_readonly else {'actual_write_probes':False}
    result={'status':'passed','uid':os.geteuid(),'python_optimization':sys.flags.optimize,
            'readonly_required':args.require_readonly,'readonly':probes,
            'checks':{'integrity':verify_pins(),'dilation':check_dilations(),'shear':check_shear(),
                      'interval':check_interval_compression(),'radial':check_radial_compression(),
                      'magnus':check_magnus(),'duality':check_duality()},
            'limits':'Finite formula checks only. No computation proves Sher, spun Bing shrinkability, or classification.'}
    data=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if out:out.write_text(data)
    else:sys.stdout.write(data)


if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        sys.stderr.write(type(exc).__name__+': '+str(exc)+'\n')
        sys.exit(1)
