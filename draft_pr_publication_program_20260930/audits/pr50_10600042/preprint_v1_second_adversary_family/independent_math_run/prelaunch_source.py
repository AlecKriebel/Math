#!/usr/bin/env python3
"""Independent bounded falsification tests; no author helper is imported.
Letters are (index, sign), with sign zero for a virtual crossing.
"""
from itertools import product, permutations
from functools import lru_cache
from collections import Counter
from pathlib import Path
import hashlib, json, stat

COUNTS=Counter()
def check(test, kind):
    if not test: raise RuntimeError(kind)
    COUNTS[kind]+=1
def letter(i,e=1): return ((i,e),)
def backwards(w): return tuple((i,-e) for i,e in w[::-1])
def slide(w): return tuple((i+1,e) for i,e in w)
def words(k,virtual):
    letters=tuple((i,e) for i in range(1,k+1) for e in ((-1,0,1) if virtual else (-1,1)))
    return ((),)+tuple((x,) for x in letters)+tuple(product(letters,repeat=2))
def P(state):
    n,w=state
    return (n,w) if n%2==0 else (n+1,w+letter(n))
def supported(state,virtual):
    n,w=state
    return type(n) is int and n>=1 and all(1<=i<n and e in ((-1,0,1) if virtual else (-1,1)) for i,e in w)

@lru_cache(None)
def cycle_ids(state):
    n,w=state
    pos=list(range(n))
    for i,e in w: pos[i-1],pos[i]=pos[i],pos[i-1]
    out=[-1]*n; count=0
    for i in range(n):
        if out[i]>=0: continue
        j=i
        while out[j]<0: out[j]=count; j=pos[j]
        count+=1
    return count,tuple(out)

@lru_cache(None)
def signed_matrix(state):
    n,w=state; count,ids=cycle_ids(state)
    labels=list(range(n)); mat=[[0]*count for _ in range(count)]
    for i,e in w:
        u,z=labels[i-1],labels[i]
        if e:
            over,under=(u,z) if e>0 else (z,u)
            if ids[over]!=ids[under]: mat[ids[over]][ids[under]]+=e
        labels[i-1],labels[i]=z,u
    return tuple(tuple(row) for row in mat)

@lru_cache(None)
def canonical(mat):
    return min(tuple(mat[i][j] for i in perm for j in perm) for perm in permutations(range(len(mat))))

@lru_cache(None)
def color_count(state):
    n,w=state
    a=[[int(i==j) for j in range(n)] for i in range(n)]
    for i,e in w:
        u,z=a[i-1],a[i]
        a[i-1],a[i]=([ (2*x-y)%3 for x,y in zip(u,z)],u[:]) if e>0 else (z[:],[ (2*y-x)%3 for x,y in zip(u,z)])
    a=[[(a[i][j]-int(i==j))%3 for j in range(n)] for i in range(n)]
    rank=0
    for col in range(n):
        pivot=next((j for j in range(rank,n) if a[j][col]),None)
        if pivot is None: continue
        a[rank],a[pivot]=a[pivot],a[rank]
        scale=a[rank][col]; a[rank]=[(x*scale)%3 for x in a[rank]]
        for j in range(n):
            if j!=rank:
                factor=a[j][col]; a[j]=[(x-factor*y)%3 for x,y in zip(a[j],a[rank])]
        rank+=1
    return 3**(n-rank)

def invariant_pair(pair,virtual,label):
    check(all(supported(x,virtual) and x[0]%2==0 for x in pair),'valid_even_'+label)
    check(cycle_ids(pair[0])[0]==cycle_ids(pair[1])[0],'components_'+label)
    if virtual: check(canonical(signed_matrix(pair[0]))==canonical(signed_matrix(pair[1])),'ordered_crossings_'+label)
    else: check(color_count(pair[0])==color_count(pair[1]),'Fox3_'+label)

def lifted_checks():
    # Independent construction directly from the manuscript, not its constructors.
    for virtual in (False,True):
        for m in range(1,5):
            n=m+m%2; allwords=words(m-1,virtual)
            for a,b in product(allwords,repeat=2):
                old=((m,b),(m,a+b+backwards(a)))
                expected=((n,b),(n,a+b+backwards(a))) if m%2==0 else ((n,b+letter(n-1)),(n,a+b+backwards(a)+letter(n-1)))
                check(tuple(map(P,old))==expected,'conjugation_lift')
                invariant_pair(expected,virtual,'C' if m%2==0 else 'BC')
            for b in allwords:
                for e in ((-1,0,1) if virtual else (-1,1)):
                    old=((m,b),(m+1,b+letter(m,e)))
                    expected=((m,b),(m+2,b+letter(m,e)+letter(m+1))) if m%2==0 else ((n,b+letter(n-1)),(n,b+letter(n-1,e)))
                    check(tuple(map(P,old))==expected,'stabilization_lift')
                    invariant_pair(expected,virtual,'D' if m%2==0 else 'T')
                    check(max(x[0] for x in expected)==2*((max(x[0] for x in old)+1)//2),'supplied_height')
            if not virtual or m<2: continue
            for a,b in product(words(m-2,True),repeat=2):
                tail=letter(n-1) if m%2 else ()
                for left in (False,True):
                    old_a,old_b=(slide(a),slide(b)) if left else (a,b)
                    index=1 if left else m-1
                    old=((m,old_a+letter(index,-1)+old_b+letter(index)),(m,old_a+letter(index,0)+old_b+letter(index,0)))
                    expected=((n,old[0][1]+tail),(n,old[1][1]+tail))
                    label=('BL' if left else 'BR') if m%2 else ('L' if left else 'R')
                    check(tuple(map(P,old))==expected,'exchange_lift_'+label)
                    invariant_pair(expected,True,label)
                    check(not m%2 or n>=4,'buffered_minimum')
    # More strands and boundary support, but only four short blocks per pair.
    for n in (6,8):
        for a,b in product(((),letter(n-3),letter(n-3,-1),letter(n-3,0)),repeat=2):
            for left in (False,True):
                aa,bb=(slide(a),slide(b)) if left else (a,b); i=1 if left else n-2
                pair=((n,aa+letter(i,-1)+bb+letter(i)+letter(n-1)),(n,aa+letter(i,0)+bb+letter(i,0)+letter(n-1)))
                invariant_pair(pair,True,'BL_boundary' if left else 'BR_boundary')

def controls():
    check(color_count((2,letter(1)*3))==9 and color_count((2,letter(1)))==3,'illicit_T_witness')
    first=signed_matrix((2,letter(1)*2)); second=signed_matrix((2,letter(1)+letter(1,0)+letter(1)+letter(1,0)))
    check(first==((0,1),(1,0)) and second==((0,2),(0,0)) and canonical(first)!=canonical(second),'illicit_R_witness')
    check(cycle_ids((2,()))[0]==2 and cycle_ids((4,()))[0]==4,'tag_witness')
    check(P((1,()))==(2,letter(1)) and color_count(P((1,())))==3,'one_strand_boundary')
    check(cycle_ids((1,()))[0]!=cycle_ids((2,()))[0],'idle_padding_witness')
    # Fixed-vector rank is cross-checked by literal enumeration for short classical words.
    for w in words(2,False):
        direct=0
        for top in product(range(3),repeat=3):
            y=list(top)
            for i,e in w:
                u,z=y[i-1],y[i]; y[i-1:i+1]=[(2*u-z)%3,u] if e>0 else [z,(2*z-u)%3]
            direct+=tuple(y)==top
        check(direct==color_count((3,w)),'rank_vs_literal_coloring')

def package_checks():
    root=Path(__file__).resolve().parent.parent/'preprint_v1'
    data=(root/'PACKAGE_MANIFEST.json').read_bytes(); manifest=json.loads(data)
    check(hashlib.sha256(data).hexdigest()=='2be2e6795505f3acf54bc02203a5df0d5b51885515c72ddd7c0bf85056ced2b3','supplied_manifest_pin')
    listed=set()
    for row in manifest['files']:
        q=root/row['path']; raw=q.read_bytes(); listed.add(row['path'])
        check(stat.S_ISREG(q.lstat().st_mode) and not q.is_symlink(),'package_regular')
        check(format(stat.S_IMODE(q.stat().st_mode),'04o')==row['mode'] and len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'package_row')
    actual={str(q.relative_to(root)) for q in root.rglob('*') if q.is_file()}
    check(actual==listed|{'PACKAGE_MANIFEST.json'} and len(listed)==18,'exact_package_inventory')
    check(sum(row['bytes'] for row in manifest['files'])==manifest['payload_bytes'],'package_payload_bytes')
    cap=json.loads((root/'verification_run/CAPTURE.json').read_bytes()); pre=json.loads((root/'verification_run/PRELAUNCH.json').read_bytes())
    check(cap['argv']==pre['argv'] and cap['cwd']==pre['cwd'] and cap['operator_pid']==pre['operator_pid'] and type(cap['child_pid']) is int and cap['child_pid']>0,'actual_capture_identity')
    check(cap['actual_execution'] is True and cap['completed'] is True and type(cap['exit_code']) is int and cap['exit_code']==0 and cap['source_unchanged'] is True and cap['operator_unchanged'] is True,'actual_capture_status')
    for name in ('checker','runner'):
        source=root/('verify_even_calculus.py' if name=='checker' else 'run_diagnostics.py')
        check(source.read_bytes()==(root/'verification_run'/('prelaunch_'+name+'.py')).read_bytes(),'full_prelaunch_'+name)
    for name in ('stdout','stderr'):
        raw=(root/'verification_run'/(name+'.bin')).read_bytes()
        check(len(raw)==cap[name]['bytes'] and hashlib.sha256(raw).hexdigest()==cap[name]['sha256'],'capture_'+name)
    output=json.loads((root/'verification_run/stdout.bin').read_bytes()); metadata=json.loads((root/'metadata.json').read_bytes())
    for field in ('checks','edge_cases','relation_context_cases'):
        check(output[field]==metadata['support'][field],'metadata_count_'+field)

if __name__=='__main__':
    lifted_checks(); controls(); package_checks()
    print(json.dumps({'status':'PASS_INDEPENDENT_BOUNDED_FALSIFICATION','checks':sum(COUNTS.values()),'families':dict(sorted(COUNTS.items())),'limits':['Finite invariant checks are not link-equivalence tests','Universal proof and imported theorem hypotheses reviewed separately','No novelty, current-openness or publication certificate']},indent=2,sort_keys=True))
