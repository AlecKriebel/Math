#!/usr/bin/env python3
"""Exact supplementary controls; no external packages and no numerical rank tests."""
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, tempfile, shutil

ROOT = Path(__file__).resolve().parent
COUNT = 0
NEGATIVE = []

def require(ok, label):
    global COUNT
    COUNT += 1
    if not ok:
        raise ValueError(label)

def determinant(A):
    A = [list(map(Q, r)) for r in A]
    n = len(A)
    if any(len(r) != n for r in A):
        raise ValueError('nonsquare determinant')
    ans = Q(1)
    for j in range(n):
        k = next((k for k in range(j, n) if A[k][j]), None)
        if k is None:
            return Q(0)
        if k != j:
            A[k], A[j] = A[j], A[k]
            ans = -ans
        p = A[j][j]
        ans *= p
        for k in range(j+1, n):
            fac = A[k][j]/p
            for t in range(j+1, n):
                A[k][t] -= fac*A[j][t]
    return ans

def rank(A):
    A = [list(map(Q, r)) for r in A]
    if not A:
        return 0
    r = 0
    for j in range(len(A[0])):
        k = next((k for k in range(r, len(A)) if A[k][j]), None)
        if k is None:
            continue
        A[k], A[r] = A[r], A[k]
        p = A[r][j]
        A[r] = [v/p for v in A[r]]
        for k in range(len(A)):
            if k != r and A[k][j]:
                fac = A[k][j]
                A[k] = [a-fac*b for a,b in zip(A[k], A[r])]
        r += 1
        if r == len(A):
            break
    return r

def dot(a,b):
    return sum((x*y for x,y in zip(a,b)), Q(0))

def det_cols(a,b,c):
    return determinant(list(zip(a,b,c)))

PAIRS = list(combinations(range(4),2))
BASE = list(map(Q, [4,4,4,-4,0,0,0,-4,0,0,0,-4,1,1,0,0,0,0,0,0]))

def incidence(p):
    v=[p[3*i:3*i+3] for i in range(4)]
    a,b,c,d,e,f,g,h=p[12:]
    rays=[(1,a,b),(-1,c,d),(e,-1,f),(g,h,-1)]
    return [det_cols([v[j][k]-v[i][k] for k in range(3)],rays[i],rays[j]) for i,j in PAIRS]

EXPECTED_J=[
[0,1,-1,0,-1,1,0,0,0,0,0,0,-4,4,4,-4,0,0,0,0],
[-1,0,1,0,0,0,1,0,-1,0,0,0,0,-4,0,0,-4,4,0,0],
[1,-1,0,0,0,0,0,0,0,-1,1,0,4,0,0,0,0,0,4,-4],
[0,0,0,0,0,-1,0,0,1,0,0,0,0,0,0,4,0,-4,0,0],
[0,0,0,0,1,0,0,0,0,0,-1,0,0,0,-4,0,0,0,0,4],
[0,0,0,0,0,0,-1,0,0,1,0,0,0,0,0,0,4,0,-4,0]]

def membership(x,y):
    return [x>0 and y>0 and x+y<1,
            y<0 and x>y and x+3*y<1,
            x+y>1 and x+3*y>1 and 2*x+y>1,
            x<0 and x<y and 2*x+y<1]

def reject(check, value, label):
    try:
        check(value)
    except (ValueError, OSError, KeyError, TypeError):
        NEGATIVE.append(label)
        return
    raise ValueError('negative control accepted: '+label)

def validate_status(s):
    require(s['problem_id']=='30001893','target binding')
    require(s['status']=='partial','status not partial')
    require(s['full_source_solved'] is False,'full-source claim inflation')
    require(s['novelty_claimed'] is False,'novelty inflation')
    require(s['current_global_openness_verified'] is False,'openness inflation')
    require(s['approaches_completed']==5,'five approaches')
    require(s['live_target_statement_inspected'] is False,'uninspected live target')
    require(s['raw_upstream_ai_corpora_inspected'] is False,'uninspected AI corpora')
    require(s['independent_audit_status']=='pending','audit has not run')

ALLOWED={'.md','.json','.py'}
def validate_manifest(root):
    m=json.loads((root/'MANIFEST.json').read_text())
    require(m['problem_id']=='30001893','manifest target')
    require(m['schema']=='safe-authored-freeze-v1','manifest schema')
    entries=m['files']
    names=[x['path'] for x in entries]
    require(len(names)==len(set(names)),'duplicate path')
    expected=set(names)|{'MANIFEST.json'}
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() or p.is_symlink()}
    require(actual==expected,'unexpected or missing file')
    for e in entries:
        name=e['path']; rel=PurePosixPath(name)
        require(not rel.is_absolute() and '..' not in rel.parts and '\\' not in name,'unsafe path')
        require(len(rel.parts)==1 and rel.suffix in ALLOWED,'non-authored file type/path')
        p=root/name
        require(not p.is_symlink() and p.is_file(),'regular file required')
        b=p.read_bytes()
        require(len(b)==e['bytes'],'byte mismatch')
        require(hashlib.sha256(b).hexdigest()==e['sha256'],'hash mismatch')
    return len(entries)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--selftest',action='store_true')
    parser.add_argument('--verify-freeze',action='store_true')
    parser.add_argument('--out')
    args=parser.parse_args()
    require(determinant([[1,-1,0],[1,3,-1],[2,1,-1]])==-1,'nonregular determinant')
    require(determinant([[1,-1,0],[1,2,-1],[2,1,-1]])==0,'concurrent control')
    for i,(x,y) in enumerate([(Q(1,4),Q(1,4)),(Q(1,2),Q(-1)),(Q(1),Q(1)),(Q(-1),Q(1,2))]):
        require(membership(x,y)==[j==i for j in range(4)],'interior witness')
    grid=0
    for u,v in product(range(-15,16),repeat=2):
        x,y=Q(u,4),Q(v,4)
        if any(z==0 for z in [x,y,x+y-1,x-y,x+3*y-1,2*x+y-1]):
            continue
        grid+=1
        require(sum(membership(x,y))==1,'supplementary coverage control')
    # Coefficient order constant,x,y,z. These values define an authored example.
    funcs=[[0,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1],[1,Q(1,4),Q(1,4),Q(1,4)]]
    offset=[2,-1,5,7]
    scaled=[[3*z+h for z,h in zip(f,offset)] for f in funcs]
    gauge=0
    for xyz in product(range(-2,3), repeat=3):
        w=[1]+list(xyz)
        for i,j in combinations(range(5),2):
            gauge+=1
            require(dot(scaled[i],w)-dot(scaled[j],w)==3*(dot(funcs[i],w)-dot(funcs[j],w)),'gauge identity')
    for v in [BASE[i:i+3] for i in range(0,12,3)]:
        values=[dot(f,[1]+v) for f in funcs]
        require(sum(x==max(values) for x in values)==4,'simple tetrahedron vertex')
        require(values[-1]==max(values),'bounded cell incident')
    require(incidence(BASE)==[0]*6,'six planarity equations')
    # Every variable occurs with degree <=1 separately. Unit coordinate difference
    # is therefore the exact partial derivative, not a numerical approximation.
    columns=[]
    for k in range(20):
        moved=BASE.copy(); moved[k]+=1
        columns.append([x-y for x,y in zip(incidence(moved),incidence(BASE))])
    J=[list(row) for row in zip(*columns)]
    require(J==EXPECTED_J,'symbolic multiaffine Jacobian')
    require(rank(J)==5,'exact rank five')
    require(all(sum(row[j] for row in J)==0 for j in range(20)),'row dependence')
    minor=determinant([[J[i][j] for j in [0,1,4,5,6]] for i in range(5)])
    require(minor==1,'nonzero five by five minor')
    changed=BASE.copy(); changed[12]+=Q(1,7)
    require(any(incidence(changed)),'perturbed invalid incidence rejected')
    for n in range(4,101):
        V=2*n-4; E=3*n-6
        require(V-E+n==2 and 3*V==2*E,'fan Euler arithmetic')
        require(2*V+3==4*n-5,'moving versus fixed central fan')
        require(2*(2*n-5)+3+2==4*n-5,'cylindrical chart arithmetic')
        require(4*n-5<=3*n*(n-1)//2,'retained interval consistency')
    status=json.loads((ROOT/'STATUS.json').read_text())
    validate_status(status)
    if args.selftest:
        for key,value in [('status','claimed_solved'),('full_source_solved',True),('novelty_claimed',True),('current_global_openness_verified',True),('approaches_completed',4),('live_target_statement_inspected',True),('raw_upstream_ai_corpora_inspected',True),('independent_audit_status','passed')]:
            bad=dict(status); bad[key]=value
            reject(validate_status,bad,'status mutation '+key)
        reject(lambda n: require(n==rank(J),'reject rank-six claim'),6,'independent-six-equation claim')
        reject(lambda n: require(n==2*(2*5-4),'reject fixed-apex plus translations'),15,'fixed-apex overcount')
        reject(lambda n: require(n==4*5-5,'reject old regular count'),19,'old 4n-1 regular count')
        reject(lambda p: require(not any(incidence(p)),'reject failed incidence'),changed,'ray perturbation')
    freeze_count=None
    if args.verify_freeze:
        freeze_count=validate_manifest(ROOT)
        if args.selftest:
            with tempfile.TemporaryDirectory() as td:
                base=Path(td)/'freeze'; shutil.copytree(ROOT,base)
                # Each mutation is reset, so tests are independent.
                manifest=(base/'MANIFEST.json').read_bytes()
                proof=(base/'PROOF.md').read_bytes()
                (base/'PROOF.md').write_bytes(proof+b'\n')
                reject(validate_manifest,base,'modified proof bytes')
                (base/'PROOF.md').write_bytes(proof)
                (base/'source.pdf').write_bytes(b'not publishable')
                reject(validate_manifest,base,'unexpected PDF')
                (base/'source.pdf').unlink()
                m=json.loads(manifest); m['files'].append(dict(m['files'][0]));(base/'MANIFEST.json').write_text(json.dumps(m))
                reject(validate_manifest,base,'duplicate manifest entry')
                (base/'MANIFEST.json').write_bytes(manifest)
                p=base/'PROOF.md';p.unlink();p.symlink_to(ROOT/'PROOF.md')
                reject(validate_manifest,base,'symlink proof')
                p.unlink();p.write_bytes(proof)
                m=json.loads(manifest);m['files'][0]['path']='../outside.md';(base/'MANIFEST.json').write_text(json.dumps(m))
                reject(validate_manifest,base,'unsafe parent path')
                (base/'MANIFEST.json').write_bytes(manifest)
                m=json.loads(manifest);m['files'][0]['bytes']+=1;(base/'MANIFEST.json').write_text(json.dumps(m))
                reject(validate_manifest,base,'wrong byte count')
                (base/'MANIFEST.json').write_bytes(manifest)
                m=json.loads(manifest);m['files'][0]['sha256']='0'*64;(base/'MANIFEST.json').write_text(json.dumps(m))
                reject(validate_manifest,base,'wrong content hash')
                (base/'MANIFEST.json').write_bytes(manifest)
                (base/'README.md').unlink()
                reject(validate_manifest,base,'missing authored file')
    out={'problem_id':'30001893','arithmetic':'fractions.Fraction; exact determinants and elimination','mathematical_checks_and_guards':COUNT,'grid_points':grid,'gauge_pair_checks':gauge,'nonregular_cycle_determinant':-1,'planarity_jacobian_rank':5,'planarity_minor':int(minor),'negative_controls_rejected':NEGATIVE,'freeze_payload_files':freeze_count,'full_source_solved':False,'scope':'Supplementary finite checks, not a universal dimension proof.'}
    text=json.dumps(out,indent=2,sort_keys=True)+'\n'
    if args.out:
        Path(args.out).write_text(text)
    print(text,end='')

if __name__=='__main__':
    main()
