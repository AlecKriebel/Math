#!/usr/bin/env python3
"""Independent exact, optimization-safe audit. The frozen packet is read-only.
Only authored math, metadata, and generated checks are written beside this file.
No network access or third-party package is used.
"""
from pathlib import Path
from itertools import product
from math import comb, gcd
from collections import Counter
import ast, hashlib, json, shutil, subprocess, sys, tempfile

ROOT=Path(__file__).resolve().parent
PACKET=ROOT.parent/'packet'
PIN='b1af9079189bd88ba892e682dc848de46448237539e68b5f624cab2aaab253fa'
CHECKS=0

def require(condition, message):
    global CHECKS
    CHECKS+=1
    if not condition:
        raise RuntimeError(message)

def sha(data): return hashlib.sha256(data).hexdigest()

def integrity(path, pin=PIN):
    b=(path/'MANIFEST.json').read_bytes()
    require(sha(b)==pin,'Frozen manifest mismatch')
    manifest=json.loads(b)
    require(len(manifest['files'])==7,'Payload file count')
    require(sum(e['bytes'] for e in manifest['files'])==82741,'Payload byte count')
    for e in manifest['files']:
        content=(path/e['path']).read_bytes()
        require(len(content)==e['bytes'],'Size mismatch: '+e['path'])
        require(sha(content)==e['sha256'],'Hash mismatch: '+e['path'])
    return manifest

manifest=integrity(PACKET)
source_metadata=json.loads((PACKET/'SOURCE_METADATA.json').read_text())
source_checks=[]
for e in source_metadata['primary_sources']:
    source_path=ROOT.parent/'sources'/e['downloaded_file_label']
    if not source_path.exists():
        if '--source-bytes' in sys.argv:
            raise RuntimeError('Requested source-byte check requires: '+e['downloaded_file_label'])
        source_checks.append({'title':e['title'],'public_url':e['public_url'],'bytes':e['bytes'],'sha256':e['sha256'],'verified':False,'reason':'Public PDF absent; mathematical checks do not require copied sources.'})
        continue
    b=source_path.read_bytes()
    require(len(b)==e['bytes'] and sha(b)==e['sha256'],'Source-byte mismatch')
    source_checks.append({'title':e['title'],'public_url':e['public_url'],'bytes':len(b),'sha256':sha(b),'verified':True})

# Independent polynomial model: the differential is constructed from generator
# values by the Leibniz rule, rather than the packet's parity formula.
one=frozenset({(0,0,0)})
x=frozenset({(1,0,0)})
y=frozenset({(0,1,0)})
z=frozenset({(0,0,1)})

def plus(*ps):
    counts=Counter(t for p in ps for t in p)
    return frozenset(t for t,n in counts.items() if n%2)

def times(p,q):
    counts=Counter()
    for a in p:
        for b in q:
            t=tuple(a[i]+b[i] for i in range(3))
            if not(t[0] and t[2]): counts[t]+=1
    return frozenset(t for t,n in counts.items() if n%2)

def power(p,n):
    out=one
    for _ in range(n): out=times(out,p)
    return out

GEN_DIFF=[times(x,x),plus(times(x,y),z),frozenset()]

def derivative(p):
    out=frozenset()
    for t in p:
        for i,exponent in enumerate(t):
            if exponent%2:
                reduced=list(t);reduced[i]-=1
                out=plus(out,times(frozenset({tuple(reduced)}),GEN_DIFF[i]))
    return out

def monomials(d):
    out=[(d-2*b,b,0) for b in range(d//2+1)]
    out += [(0,(d-3*c)//2,c) for c in range(1,d//3+1) if (d-3*c)%2==0]
    return out

def linear_rank(ps):
    # Row elimination in a transposed incidence matrix, using lowest pivots.
    terms=sorted(set().union(*ps)) if ps else []
    rows=[sum(1<<j for j,p in enumerate(ps) if t in p) for t in terms]
    rank=0
    for j in range(len(ps)):
        found=next((i for i in range(rank,len(rows)) if (rows[i]>>j)&1),None)
        if found is None: continue
        rows[rank],rows[found]=rows[found],rows[rank]
        for i in range(rank+1,len(rows)):
            if (rows[i]>>j)&1: rows[i]^=rows[rank]
        rank+=1
    return rank

def qpoly(i,j):
    # Closed integer coefficient formula for u^m+v^m in x=u+v,y=uv.
    m=j-i; out=set()
    for k in range(m//2+1):
        coefficient=comb(m-k,k)+(comb(m-k-1,k-1) if k else 0)
        if coefficient%2: out.add((m-2*k,k+i,0))
    return frozenset(out)

def skies(d):
    out=[(f'Q({i},{d-i})',qpoly(i,d-i)) for i in range((d+1)//2)]
    out += [(f'M({(d-3*c)//2},{c})',frozenset({(0,(d-3*c)//2,c)})) for c in range(d//3+1) if (d-3*c)%2==0]
    return out

stored=json.loads((PACKET/'TEST_RESULTS.json').read_text())
rows=[]
for d in range(101):
    mons=monomials(d)
    images=[derivative({m}) for m in mons]
    incoming=[derivative({m}) for m in monomials(d-1)] if d else []
    require(all(not derivative(p) for p in images),f'd^2 in degree {d}')
    expected=[]
    if d%4==0: expected.append(frozenset({(0,d//2,0)}))
    if d%4==3: expected.append(frozenset({(0,(d-3)//2,1)}))
    e2=len(mons)-linear_rank(images)-linear_rank(incoming)
    require(e2==len(expected),f'E2 dimension {d}')
    require(all(not derivative(p) for p in expected),f'E2 cycles {d}')
    require(linear_rank(incoming+expected)==linear_rank(incoming)+len(expected),f'E2 independence {d}')
    sky=skies(d)
    require(len(sky)==len(mons) and linear_rank([p for _,p in sky])==len(mons),f'Skyline basis {d}')
    selected=[];chosen=[]
    for name,p in skies(d-1) if d else []:
        image=derivative(p)
        if linear_rank(chosen+[image])>len(chosen):
            chosen.append(image);selected.append(name)
    row={'degree':d,'mod2_dimension':len(mons),'first_bockstein_rank':linear_rank(images),
         'E2_dimension':e2,'order2_factors':len(chosen),'order4_factors':int(d>0 and d%4==0),
         'primary_skyline_sources':selected,'secondary_skyline_source':f'M({d//2-2},1)' if d>0 and d%4==0 else None}
    if d<=80:require(row==stored['S4_rows'][d],f'Independent row differs in degree {d}')
    rows.append({k:v for k,v in row.items() if k not in ('primary_skyline_sources',)})

# Exact characteristic class restrictions and cyclic cochains.
cyclic=[]
for m in (2,4,8,16):
    pairs=list(product(range(m),repeat=2))
    carry=lambda i,j:(i+j)//m
    for i,j in pairs:
        dc=j-((i+j)%m)+i
        require(dc==m*carry(i,j),'Integral cyclic lift')
        require((i%2-i)%2==0,'Cyclic lift retains mod2 source')
    for i,j,k in product(range(m),repeat=3):
        dt=carry(j,k)-carry((i+j)%m,k)+carry(i,(j+k)%m)-carry(i,j)
        require(dt==0,'Integral cyclic carry cocycle')
    if m>=4:
        for i,j in pairs:
            dh=(j//2-((i+j)%m)//2+i//2)%2
            require(dh==(i%2)*(j%2),'Exterior square for C_(2^r), r>=2')
        require(any((j%2-((i+j)%m)%2+i%2)%m for i,j in pairs),'Uncorrected parity lift cannot substitute for compatible lift')
    cyclic.append({'order':m,'first_nonzero_Bockstein_page':m.bit_length()-1,'pairs_checked':len(pairs),'triples_checked':m**3})
for i,j in product(range(4),repeat=2):
    require((2*i+2*j)//8==(i+j)//4,'C8 to C4 restriction of t')
require(all((2*i)%2==0 for i in range(4)),'Restriction s8 is zero, not s4')
# Coset reps 0,1 for C4=<2> in C8; transfer maps g to g^2.
transfer_exponent=sum((r+1)-((r+1)%2) for r in (0,1))//2
require(transfer_exponent%2==1,'Degree-one corestriction s4 to s8')

# Independent bit-mask Mackey enumeration and cycle types on both blocks.
def rotate(mask,step):
    return ((mask<<step)|(mask>>(8-step)))&255 if step else mask

def cycles(mask,step):
    remaining={i for i in range(8) if mask&(1<<i)};out=[]
    while remaining:
        seed=min(remaining);orbit=[];a=seed
        while a not in orbit:
            orbit.append(a);a=(a+step)%8
        require(set(orbit)<=remaining,'Invalid stabilizer cycle')
        remaining-=set(orbit);out.append(len(orbit))
    return sorted(out)

unseen={i for i in range(256) if i.bit_count()==4};orbits=[]
while unseen:
    mask=min(unseen);orbit={rotate(mask,k) for k in range(8)};unseen-=orbit
    stabilizer=[k for k in range(8) if rotate(mask,k)==mask]
    order=len(stabilizer);step=8//order if order>1 else 0
    entry={'representative':[i for i in range(8) if mask&(1<<i)],'orbit_size':len(orbit),'stabilizer_order':order,
           'selected_block_cycles':cycles(mask,step),'complement_block_cycles':cycles(mask^255,step)}
    orbits.append(entry)
require(sum(o['orbit_size'] for o in orbits)==70,'Mackey coset coverage')
require(Counter(o['stabilizer_order'] for o in orbits)==Counter({1:8,2:1,4:1}),'Mackey orbit multiplicities')
for o in orbits:
    if o['stabilizer_order']==4:
        require(o['selected_block_cycles']==[4] and o['complement_block_cycles']==[4],'C4 regular actions')
    if o['stabilizer_order']==2:
        require(o['selected_block_cycles']==[2,2] and o['complement_block_cycles']==[2,2],'C2 two-transposition actions')
require(comb(4,2)==6 and comb(4,2)%2==0,'Equal profile transfer cancellation')
require([comb(n,4) for n in (5,6,7)]==[5,15,35],'Odd-index restriction')
require(all(comb(8,a)%2==0 for a in range(1,8)),'Power-of-two barrier')

# Artificial complex and the preferred-basis obstruction.
D0=((2,2),(4,0),(-4,0));D1=(0,2,2)
require(all(sum(D1[k]*D0[k][j] for k in range(3))==0 for j in (0,1)),'Artificial differential square')
minor=abs(2*0-2*4);first=gcd(gcd(2,2),4)
require((first,minor//first)==(2,4),'Smith factors from independent determinant/gcd')
allowed={(a,2*k%4) for a in range(2) for k in range(2)}
require(len(allowed)==4 and (0,1) not in allowed,'Preferred source mixing obstruction')

# Verify the patch retains every assertion's original mathematical expression.
original=(PACKET/'verify.py').read_text()
patched=(ROOT/'patched'/'verify.py').read_text()
asserts=[n for n in ast.walk(ast.parse(original)) if isinstance(n,ast.Assert)]
checks=[n for n in ast.walk(ast.parse(patched)) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='check']
require(len(asserts)==len(checks)>0,'Patch guard count')
require([ast.dump(n.test) for n in asserts]==[ast.dump(n.args[0]) for n in checks],'Patch guard expression semantics')

# Execute actual child processes in isolated temporary directories.
mutations=[
 ('lose_y_contribution','if (a+b)%2 and c==0:toggle(out,(a+1,b,c))','if a%2 and c==0:toggle(out,(a+1,b,c))'),
 ('lose_z_contribution','if b%2 and a==0:toggle(out,(0,b-1,c+1))','if False:toggle(out,(0,b-1,c+1))'),
 ('false_mackey_stabilizers','==[1]*8+[2,4]','==[1]*8+[2,2]'),
 ('incorrect_transfer_coefficient','math.comb(4,2)%2==0','math.comb(4,2)%2==1'),
]
process_results=[]
def run_child(text,mode):
    with tempfile.TemporaryDirectory(prefix='skyline-audit-') as tmp:
        p=Path(tmp)/'verify.py';p.write_text(text)
        completed=subprocess.run([sys.executable]+([mode] if mode else [])+[str(p)],text=True,capture_output=True,timeout=180)
        out=Path(tmp)/'TEST_RESULTS.json'
        return {'returncode':completed.returncode,'stdout':completed.stdout.strip(),
                'last_error_line':completed.stderr.strip().splitlines()[-1] if completed.stderr.strip() else None,
                'result_hash':sha(out.read_bytes()) if out.exists() else None}
expected_result_hash=sha((PACKET/'TEST_RESULTS.json').read_bytes())
for version,script in [('original',original),('patched',patched)]:
    for mode in ('','-O','-OO'):
        r=run_child(script,mode)
        require(r['returncode']==0 and r['result_hash']==expected_result_hash,f'{version} baseline {mode}')
        process_results.append({'version':version,'mode':mode or 'normal','case':'unmodified',**r,
            'interpretation':'Checks active' if version=='patched' or not mode else 'Output reproducible, but assertions disabled; not validation'})
        for name,old,new in mutations:
            require(script.count(old)==1,'Mutation location must be unique: '+name)
            r=run_child(script.replace(old,new),mode)
            expected_rejection=(version=='patched' or not mode)
            require((r['returncode']!=0)==expected_rejection,f'Unexpected mutant behavior: {version} {mode} {name}')
            process_results.append({'version':version,'mode':mode or 'normal','case':name,**r,
                'interpretation':'Rejected' if r['returncode'] else 'False PASS with assertions disabled'})

# Byte-integrity negative controls, including a rewritten self-consistent manifest.
integrity_controls=[]
with tempfile.TemporaryDirectory(prefix='skyline-integrity-') as tmp:
    q=Path(tmp)/'packet';shutil.copytree(PACKET,q)
    (q/'PROOF.md').write_bytes((q/'PROOF.md').read_bytes()+b'\n')
    try:integrity(q)
    except RuntimeError as e:integrity_controls.append({'case':'payload_byte_change','rejected':True,'reason':str(e)})
    else:raise RuntimeError('Corrupt payload passed')
    mm=json.loads((q/'MANIFEST.json').read_text())
    for e in mm['files']:
        if e['path']=='PROOF.md':
            b=(q/e['path']).read_bytes();e.update(bytes=len(b),sha256=sha(b))
    (q/'MANIFEST.json').write_text(json.dumps(mm,indent=2)+'\n')
    try:integrity(q)
    except RuntimeError as e:integrity_controls.append({'case':'payload_and_manifest_rewritten','rejected':True,'reason':str(e)})
    else:raise RuntimeError('Unpinned replacement passed')

integrity(PACKET)
result={'status':'PASS','scope':'Independent finite exact checks and audit harness; all-degree conclusions require the written proof',
        'frozen_manifest_sha256':PIN,'payload_files':7,'payload_bytes':82741,'optimization_safe_check_count':CHECKS,
        'independent_S4_degrees_checked':101,'independent_S4_rows':rows,'source_byte_verification':source_checks,
        'cyclic_cochain_checks':cyclic,'C8_Mackey_orbits':orbits,'assertions_replaced':len(asserts),
        'child_process_tests':process_results,'integrity_negative_controls':integrity_controls,
        'original_preserved':True}
(ROOT/'AUDIT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ('status','optimization_safe_check_count','independent_S4_degrees_checked','assertions_replaced','original_preserved')}))
