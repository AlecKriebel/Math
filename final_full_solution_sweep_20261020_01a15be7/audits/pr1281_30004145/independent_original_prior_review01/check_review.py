#!/usr/bin/env python3
"""Offline exact diagnostics supporting the written genus-one proof; no services.

These rational calculations do not prove topology by sampling. All guards use
explicit exceptions so optimization cannot remove them. No source-author code.
"""
import argparse
import hashlib
import itertools
import json
import sys
from fractions import Fraction as F
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
COUNTS={}


def require(v,message):
    if not v:raise RuntimeError(message)


def count(label):COUNTS[label]=COUNTS.get(label,0)+1


def readj(name):return json.loads((BASE/name).read_text())


def sha(raw):return hashlib.sha256(raw).hexdigest()


def in_u(x):return bool(x) and all(a<b for a,b in zip(x,x[1:])) and x[-1]<x[0]+1


def residues(x):return tuple(sorted(t%1 for t in x))


def turn(x,n):
    m=len(x)
    return tuple(x[(j+n)%m]+(j+n)//m for j in range(m))


def iterative_turn(x,n):
    y=x
    for _ in range(abs(n)):
        y=(y[1:]+(y[0]+1,)) if n>0 else ((y[-1]-1,)+y[:-1])
    return y


def equal_space(x):
    m=len(x);mu=sum(x)/m
    return tuple(mu+F(2*j-m-1,2*m) for j in range(1,m+1))


def homotopy(x,t):return tuple((1-t)*a+t*b for a,b in zip(x,equal_space(x)))


def complex_mul(x,y):return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])


def conjugate(x):return x[0],-x[1]


def group_add(x,y,beta):
    # Rational sample of a circle-by-Z/2 coset chart with 2b=phi(beta).
    return (x[0]+y[0])%2,(x[1]+y[1]+((x[0]+y[0])//2)*beta)%1


def group_sum(xs,beta):
    out=(0,F(0))
    for x in xs:out=group_add(out,x,beta)
    return out


def wrong(call,label):
    try:call()
    except RuntimeError:count('rejected_wrong_science')
    else:raise RuntimeError('wrong control escaped: '+label)


def anchors():
    binding=readj('INPUT_BINDING.json')
    require(binding['head']=='f76be6cc96afc990dfe894b117681cdac95ff10f','head')
    require(len(binding['files'])==7,'seven actual PR blobs')
    for e in binding['files']:
        raw=(BASE/e['local']).read_bytes()
        require(len(raw)==e['bytes'] and sha(raw)==e['sha256'],'PR bytes '+e['local'])
        require(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==e['git_blob_sha1'],'immutable blob')
        count('authenticated_PR_blobs')
    for e in readj('AUTHENTICATED_INPUTS.json')['files']:
        raw=(BASE/e['path']).read_bytes()
        require(len(raw)==e['bytes'] and sha(raw)==e['sha256'],'local pin '+e['path'])
        count('authenticated_local_inputs')
    for e in readj('ROOT_ANCHORS.json')['files']:
        raw=(ROOT/e['path']).read_bytes()
        require(len(raw)==e['bytes'] and sha(raw)==e['sha256'],'root pin '+e['path'])
        count('authenticated_root_anchors')
    for e in readj('private/pr_source/PUBLICATION_MANIFEST.json')['files']:
        raw=(BASE/'private/pr_source'/e['file']).read_bytes()
        require(len(raw)==e['bytes'] and sha(raw)==e['sha256'],'submitted manifest')
    require(sha((BASE/'private/primary/original.pdf').read_bytes())=='bc813c4ac357dda41371e3309349b8cb07b01879994657cff3d9f0680647b90d','fresh exact EMS source')
    meta=readj('private/primary/crossref.json')['message']
    require(meta['DOI']=='10.4171/owr/2019/21' and meta['title']==['Tropical Geometry: new directions'],'report DOI identity')
    require([a['family'] for a in meta['author']]==['Itenberg','Markwig','Mikhalkin','Shustin'],'container byline; do not invent separate paper')


def diagnostic():
    inputs=readj('CONTROL_INPUTS.json')
    blocks=[tuple(F(t) for t in row) for row in inputs['circle_lifts']]
    times=[F(t) for t in inputs['homotopy_times']]
    for x in blocks:
        m=len(x);require(in_u(x),'valid increasing lifts')
        require(len(set(residues(x)))==m,'distinct residues')
        require(turn(x,m)==tuple(t+1 for t in x),'m cyclic turns one full rotation')
        r=equal_space(x)
        require(in_u(r) and sum(r)==sum(x) and equal_space(r)==r,'sum-preserving retraction and fixed locus')
        for n in range(-2*m,2*m+1):
            y=turn(x,n)
            require(y==iterative_turn(x,n),'independent signed turn implementation')
            require(in_u(y) and residues(y)==residues(x),'unordered circle configuration')
            require(sum(y)==sum(x)+n,'UNWEIGHTED exponent increment')
            require((y==x)==(n==0),'no isotropy at symmetric configurations')
            require(equal_space(y)==turn(r,n),'retraction equivariance')
            for t in times:
                h=homotopy(x,t)
                require(in_u(h) and sum(h)==sum(x),'convex sum-preserving homotopy')
                require(homotopy(y,t)==turn(h,n),'full homotopy affine deck equivariance')
                require(homotopy(r,t)==r,'strong retraction fixes target at every time')
                count('exact_homotopy_equivariance')
            count('signed_cyclic_deck_cases')
        if m<=4:
            # Independently enumerate integer lifts of residues and recognize every
            # admissible cyclic window by its INTEGER SUM increment.
            rr=residues(x)
            for shifts in itertools.product(range(-1,2),repeat=m):
                y=tuple(sorted(t+n for t,n in zip(rr,shifts)))
                if not in_u(y):continue
                n=sum(y)-sum(x)
                require(n.denominator==1 and turn(x,int(n))==y,'complete small fiber windows')
                count('exhaustive_small_fiber_windows')
        # Local order chart remains inside strict cyclic inequalities under
        # independent perturbations smaller than one quarter of minimum gap.
        gaps=[b-a for a,b in zip(x,x[1:])]+[x[0]+1-x[-1]]
        eps=min(gaps)/4
        for signs in itertools.product([-1,1],repeat=min(m,4)):
            delta=tuple(eps*signs[j%len(signs)] for j in range(m))
            require(in_u(tuple(a+d for a,d in zip(x,delta))),'disjoint-arc local chart perturbation')
            count('local_order_chart_perturbations')
    for c0 in inputs['unit_complex_constants']:
        c=tuple(F(t) for t in c0)
        require(complex_mul(c,conjugate(c))==(1,0),'descent constant unit norm')
        lam=(F(0),F(1)) if c==(-1,0) else (1+c[0],c[1])
        require(lam!=(0,0) and complex_mul(conjugate(lam),c)==lam,'real-descent scalar rescaling')
        count('exact_real_descent_scalars')
    # Fixed-distribution product slices; these test the configuration model only,
    # not realizability of every sampled distribution by plane cubic intersections.
    for counts in inputs['occupied_counts']:
        require(1<=len(counts)<=2 and min(counts)>0,'genus-one occupied count range')
        raw=tuple(tuple(F(j*j,2*m*m) for j in range(m)) for m in counts)
        require(all(in_u(x) for x in raw),'product lifts')
        k=len(raw)
        for target0 in inputs['slice_targets']:
            target=F(target0);delta=(target-sum(map(sum,raw)))/counts[0]
            x=(tuple(t+delta for t in raw[0]),)+raw[1:]
            require(sum(map(sum,x))==target and all(in_u(a) for a in x),'every real slice nonempty')
            for z in itertools.product(range(-3,4),repeat=k):
                y=tuple(turn(a,n) for a,n in zip(x,z));zsum=sum(z)
                require(tuple(sum(a) for a in y)==tuple(sum(a)+n for a,n in zip(x,z)),'block sums detect every exponent')
                require(sum(map(sum,y))==target+zsum,'slice index is exponent sum')
                require((y==x)==all(n==0 for n in z),'free product action')
                if zsum==0:
                    # e_i-e_k basis reconstructs the integral kernel exactly.
                    reconstruction=tuple(z[i] if i<k-1 else -sum(z[:-1]) for i in range(k))
                    require(reconstruction==z,'primitive sum-kernel basis')
                    for t in times:
                        h=tuple(homotopy(a,t) for a in x)
                        require(sum(map(sum,h))==target,'retraction stays in H')
                        require(tuple(homotopy(a,t) for a in y)==tuple(turn(a,n) for a,n in zip(h,z)),'K-equivariant homotopy')
                    count('exact_kernel_deck_elements')
                # A compact set with block-sum intervals [ai-M,ai+M] can meet
                # its z-translate only if |zi|<=2M. Finite arithmetic check.
                for radius0 in inputs['compact_sum_radii']:
                    radius=F(radius0)
                    overlaps=all(abs(n)<=2*radius for n in z)
                    if overlaps:require(all(abs(n)<=int(2*radius) for n in z),'integer translate bound')
                    count('proper_action_integer_bounds')
                count('product_slice_deck_cases')
        for beta0 in inputs['coset_twists']:
            beta=F(beta0);bpoints=[(i,F(i+1,7)) for i in range(k)]
            offset=group_sum([b for b,m in zip(bpoints,counts) for _ in range(m)],beta)
            points=[group_add(b,(0,t%1),beta) for b,a in zip(bpoints,raw) for t in a]
            actual=group_sum(points,beta)
            expected=group_add(offset,(0,sum(map(sum,raw))%1),beta)
            require(actual==expected,'nonidentity coset offsets exactly retained')
            for z in itertools.product([-1,0,1],repeat=k):
                lifted=tuple(turn(a,n) for a,n in zip(raw,z))
                moved=[group_add(b,(0,t%1),beta) for b,a in zip(bpoints,lifted) for t in a]
                require(group_sum(moved,beta)==actual,'fixed coset offset and residues under all turns')
                count('fixed_coset_offset_deck_checks')
            count('nonidentity_offset_models')
    wrong(lambda:require(sum(turn((F(0),F(1,3)),1))==F(1,3)+2,'weighted one-block sum is false'),'count weighted generator')
    wrong(lambda:require(2*1+3*(-1)==0,'legitimate kernel generator must not be weighted'),'wrong weighted kernel excludes valid loop')
    wrong(lambda:require(sum((3,-2))==0,'weighted-zero vector leaves correct slice'),'weighted kernel admits invalid loop')
    wrong(lambda:require(turn((F(0),F(1,2)),1)==(F(0),F(1,2)),'symmetric configuration has no stabilizer upstairs'),'artificial rotational isotropy')
    wrong(lambda:require(complex_mul((1,0),(F(3,5),F(4,5)))==(1,0),'unrescaled nonreal descent constant'),'forgot real rescaling')
    wrong(lambda:require(in_u((F(0),F(0))),'colliding points forbidden'),'collision extension')
    wrong(lambda:require(homotopy((F(0),F(1,3)),F(1))==(F(0),F(1,2)),'anchoring spacing at x1 breaks sum'),'wrong anchored retraction')


def accounting():
    ledger=json.loads((ROOT/'raw/pr1281/ledger_live.json').read_text())
    rows=ledger['response']['values'];aliases=readj('ALIASES.json')
    require(len(rows)==191 and ledger['response']['range'].endswith('A1:AQ1178'),'root observed ledger snapshot')
    hits=[(n,a) for n,row in enumerate(rows,1) for a in aliases['direct'] if any(a.casefold() in str(c).casefold() for c in row)]
    require(hits==[(171,'Viro')],'exact exposed raw-substring leads; no hidden target hit')
    scan=readj('ALIAS_SCAN.json')
    require(scan['semantic_target_matches']==0 and scan['raw_substring_direct_hits']==[{'row':171,'alias':'Viro','occurs_in':'environmental','same_author_or_target':False}],'reasoned substring adjudication retained for root adoption')
    row=readj('LITERAL_FOUR_CELL_PROPOSAL.json')
    require(type(row)is list and len(row)==4 and all(type(x)is str for x in row) and row[1]=='','literal four strings blank B')
    require(row[2]=='https://doi.org/10.4171/OWR/2019/21','actual source report DOI identifies prior cubic statement')
    require('Viro' in row[3] and 'Öztürkalan' in row[3] and 'statement' in row[3],'qualified prior-statement attribution')
    disposition=readj('ACCOUNTING_DISPOSITION.json')
    require(disposition['publication_ready'] is False and disposition['root_adopted'] is False and disposition['new_publication'] is False,'no service readiness')
    count('literal_prior_statement_row_checked')


def package():
    manifest=readj('MANIFEST.json');expected={e['path'] for e in manifest['files']}
    actual={str(p.relative_to(BASE)) for p in BASE.rglob('*') if p.is_file()}-set(manifest['self_exclusions'])
    require(expected==actual,'closed package membership')
    for p in BASE.rglob('*'):require(not p.is_symlink(),'no package symlinks')
    for e in manifest['files']:
        raw=(BASE/e['path']).read_bytes()
        require(len(raw)==e['bytes'] and sha(raw)==e['sha256'],'payload '+e['path'])
    require(sum(p.stat().st_blocks*512 for p in BASE.rglob('*') if p.is_file())<=25*1024**2,'25MiB allocation cap')
    count('complete_closed_package_readback')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verify-package',action='store_true');parser.add_argument('--deliberate-bad-guard',action='store_true');args=parser.parse_args()
    anchors();diagnostic();accounting()
    if args.deliberate_bad_guard:require(False,'deliberate optimization-safe failure')
    if args.verify_package:package()
    print(json.dumps({'status':'PASS','optimize':sys.flags.optimize,'checker_sha256':sha(Path(__file__).read_bytes()),'counts':COUNTS,'role':'finite rational diagnostics supplement written topology/descent proof; no services'},sort_keys=True))


if __name__=='__main__':main()
