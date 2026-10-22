#!/usr/bin/env python3
"""Exact finite controls and fail-closed integrity checks; not a geometry prover."""
import argparse
import hashlib
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path
import shutil
import tempfile

FILES = {'README.md', 'REPORT.md', 'SOURCE_METADATA.json',
         'TARGET_VERIFICATION.json', 'APPROACHES.json', 'RESULTS.json', 'verify.py'}

def need(condition, message):
    if not condition:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def integrity(root, expected):
    root = Path(root)
    need(len(expected) == 64 and all(c in '0123456789abcdef' for c in expected), 'invalid manifest pin')
    actual = {p.name for p in root.iterdir()}
    need(actual == FILES | {'MANIFEST.json'}, 'unexpected or missing package file')
    for p in root.iterdir():
        need(p.is_file() and not p.is_symlink(), 'nonregular package entry')
    raw = (root/'MANIFEST.json').read_bytes()
    need(sha(raw) == expected, 'manifest hash mismatch')
    manifest = json.loads(raw)
    need(set(manifest) == {'schema', 'problem_id', 'status', 'files'}, 'invalid manifest keys')
    need(manifest['schema'] == 1 and manifest['problem_id'] == 30000120 and
         manifest['status'] == 'UNSOLVED_SCOPED_PARTIAL', 'invalid manifest identity')
    need(set(manifest['files']) == FILES, 'invalid manifest inventory')
    for name in sorted(FILES):
        entry = manifest['files'][name]
        need(set(entry) == {'sha256', 'bytes'}, 'invalid file metadata')
        data = (root/name).read_bytes()
        need(type(entry['bytes']) is int and entry['bytes'] == len(data), 'file byte count mismatch: '+name)
        need(entry['sha256'] == sha(data), 'file hash mismatch: '+name)

def clean(p):
    return {k: Q(v) for k, v in p.items() if v}

def add(*polys):
    out = {}
    for p in polys:
        for k, v in p.items():
            out[k] = out.get(k, Q(0)) + v
    return clean(out)

def scale(p, v):
    return clean({k: Q(v)*c for k, c in p.items()})

def rawmul(p, q):
    out = {}
    for (a,b), u in p.items():
        for (c,d), v in q.items():
            k = (a+c,b+d)
            out[k] = out.get(k,Q(0)) + u*v
    return clean(out)

def mon(a,b):
    return {(a,b): Q(1)}

ONE, H, E = mon(0,0), mon(1,0), mon(0,1)

def reduce_poly(p):
    pending = dict(p)
    out = {}
    while pending:
        (a,b), v = pending.popitem()
        if not v or a >= 6 or (a >= 3 and b >= 1):
            continue
        if b >= 3:
            for k,c in [((a+1,b-1),Q(9,2)), ((a+2,b-2),Q(-15,2)), ((a+3,b-3),Q(4))]:
                pending[k] = pending.get(k,Q(0)) + c*v
        else:
            out[(a,b)] = out.get((a,b),Q(0)) + v
    return clean(out)

def mul(p,q):
    return reduce_poly(rawmul(p,q))

def power(p,n):
    need(type(n) is int and n >= 0, 'invalid polynomial exponent')
    out = ONE
    for _ in range(n):
        out = mul(out,p)
    return out

def rank(rows):
    if not rows:
        return 0
    m = [list(map(Q,r)) for r in rows]
    n = len(m[0])
    need(all(len(r)==n for r in m), 'ragged matrix')
    r=0
    for c in range(n):
        piv = next((j for j in range(r,len(m)) if m[j][c]),None)
        if piv is None:
            continue
        m[r],m[piv]=m[piv],m[r]
        t=m[r][c]
        m[r]=[v/t for v in m[r]]
        for j in range(len(m)):
            if j!=r:
                t=m[j][c]
                m[j]=[v-t*w for v,w in zip(m[j],m[r])]
        r+=1
        if r==len(m):
            break
    return r

def convolution(p,q):
    out=[0]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):
            out[i+j]+=a*b
    return out

def compute():
    basis=[(a,0) for a in range(6)]+[(a,b) for b in (1,2) for a in range(3)]
    bs=[mon(*k) for k in basis]
    f=add(scale(H,3),scale(E,-2))
    # Defining relation and two elementary Groebner consequences.
    rel=add(mon(0,3),scale(mon(1,2),Q(-9,2)),scale(mon(2,1),Q(15,2)),scale(mon(3,0),-4))
    g=[rel,mon(3,1),mon(6,0)]
    lms=[(0,3),(3,1),(6,0)]
    for i,j in itertools.combinations(range(3),2):
        l=(max(lms[i][0],lms[j][0]),max(lms[i][1],lms[j][1]))
        s=add(rawmul(mon(l[0]-lms[i][0],l[1]-lms[i][1]),g[i]),
              scale(rawmul(mon(l[0]-lms[j][0],l[1]-lms[j][1]),g[j]),-1))
        need(not reduce_poly(s), 'nonzero S-polynomial')
    # H^6 is genuinely in the two-generator ideal, not an extra geometric relation.
    certificate=add(rawmul(mon(3,0),rel),
        scale(rawmul(mon(0,2),mon(3,1)),-1),
        scale(rawmul(mon(1,1),mon(3,1)),Q(9,2)),
        scale(rawmul(mon(2,0),mon(3,1)),Q(-15,2)))
    need(certificate==scale(mon(6,0),-4),'invalid H^6 ideal certificate')
    need(not reduce_poly(rel), 'defining relation failed')
    need(not mul(power(H,3),E), 'kernel relation failed')
    need(scale(add(f,scale(E,2)),Q(1,3))==H,'boundary inverse failed')
    need(not mul(E,power(add(scale(E,2),f),3)), 'boundary quartic failed')
    cubic=add(scale(power(E,3),8),scale(mul(power(E,2),f),3),
              scale(mul(E,power(f,2)),-3),scale(power(f,3),-8))
    need(not cubic,'boundary cubic failed')
    # Reconstruct the normal Chern polynomial by truncated rational multiplication.
    normal=[Q(1),Q(9),Q(30)]
    tangent_z=[Q(1),Q(3),Q(3)]
    need(convolution(normal,tangent_z)[:3]==[1,12,60], 'normal Chern coefficients failed')
    dims=[]
    generator_ranks=[]
    for degree in range(6):
        keys=[k for k in basis if sum(k)==degree]
        dims.append(len(keys))
        rows=[]
        for j in range(degree+1):
            p=mul(power(E,j),power(f,degree-j))
            rows.append([p.get(k,Q(0)) for k in keys])
        generator_ranks.append(rank(rows))
    need(dims==[1,2,3,3,2,1] and generator_ranks==dims,'generation ranks failed')
    count=0
    for x,y,z in itertools.product(bs,repeat=3):
        need(mul(mul(x,y),z)==mul(x,mul(y,z)), 'associativity failed')
        count+=1
    for x,y in itertools.product(bs,repeat=2):
        need(mul(x,y)==mul(y,x), 'commutativity failed')
    for x in bs:
        need(mul(ONE,x)==x,'unit failed')
    intersection=[]
    for j in range(6):
        p=mul(power(H,5-j),power(E,j))
        need(set(p)<= {(5,0)},'non-top intersection remainder')
        val=p.get((5,0),Q(0))
        need(val.denominator==1,'nonintegral top control')
        intersection.append(int(val))
    need(intersection==[1,0,0,4,18,51],'top intersections failed')
    need(power(add(scale(H,2),scale(E,-1)),5)==mon(5,0),'dual-conic degree failed')
    tangent=add(scale(H,6),scale(E,-2))
    log=add(tangent,scale(add(E,f),-1))
    need(tangent==scale(add(E,f),2) and log==add(E,f),'first Chern formulas failed')
    degree_two_rank=rank([[p.get(k,0) for k in [(1,0),(0,1)]] for p in [tangent,log]])
    need(degree_two_rank==1,'tangent/log obstruction failed')
    # Exact product controls supplement the all-b,c Kunneth proof.
    products=[]
    for b,c in [(1,0),(0,1),(1,1),(0,2),(3,2)]:
        p=[1]
        for _ in range(b): p=convolution(p,[1,1,1])
        for _ in range(c): p=convolution(p,dims)
        need(p==p[::-1] and sum(p)==3**b*12**c,'product Poincare control failed')
        need(p[1]==b+2*c,'product Picard control failed')
        products.append({'b':b,'c':c,'symmetric_rank':b+2*c,'rank_difference':c,'poincare_half_degree':p,'euler':sum(p)})
    # Negative algebra control: E alone misses degree one.
    need(rank([[E.get(k,0) for k in [(1,0),(0,1)]]])==1,'negative rank control failed')
    return {'status':'PASS_EXACT_SCOPED_CONTROLS','problem_id':30000120,
        'geometric_proof_machine_certified':False,'general_problem_solved':False,
        'basis_size':len(basis),'even_betti':dims,'boundary_monomial_ranks':generator_ranks,
        'groebner_pairs_checked':3,'basis_associativity_cases':count,
        'basis_commutativity_cases':144,'basis_unit_cases':12,
        'H_to_E_top_intersections':intersection,'tangent_log_H2_rank':degree_two_rank,
        'H2_dimension':2,'product_controls':products}

def selftest(root,pin):
    mutations=['changed_payload','missing_payload','unexpected_payload','changed_manifest','symlink']
    for name in mutations:
        with tempfile.TemporaryDirectory() as td:
            copy=Path(td)/'pkg'
            shutil.copytree(root,copy)
            if name=='changed_payload':
                with (copy/'REPORT.md').open('ab') as f: f.write(b'\nchanged\n')
            elif name=='missing_payload': (copy/'REPORT.md').unlink()
            elif name=='unexpected_payload': (copy/'unexpected.txt').write_text('unexpected')
            elif name=='changed_manifest':
                with (copy/'MANIFEST.json').open('ab') as f: f.write(b'\n')
            else:
                (copy/'REPORT.md').unlink()
                (copy/'REPORT.md').symlink_to('README.md')
            failed=False
            try: integrity(copy,pin)
            except (ValueError,OSError): failed=True
            need(failed,'accepted tamper: '+name)
    return len(mutations)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--expected-manifest',required=True)
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    integrity(root,args.expected_manifest)
    result=compute()
    expected=(root/'RESULTS.json').read_bytes()
    actual=(json.dumps(result,sort_keys=True,indent=2)+'\n').encode()
    need(actual==expected,'results do not match frozen expected bytes')
    if args.self_test:
        need(selftest(root,args.expected_manifest)==5,'self-test inventory failed')
    print(actual.decode(),end='')

if __name__=='__main__':
    main()
