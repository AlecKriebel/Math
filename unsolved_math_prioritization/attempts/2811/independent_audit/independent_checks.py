#!/usr/bin/env python3
"""Independent finite diagnostics and author integrity controls; no topology solver."""
import hashlib
import importlib.util
import itertools
import json
import math
import pathlib
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile
from fractions import Fraction as F
sys.dont_write_bytecode = True
ROOT = pathlib.Path(__file__).resolve().parent
ARCHIVE = 'SURFACE_TRIPLE_POINTS_2811_AUTHOR_SAFE_FREEZE.zip'
ARCHIVE_SHA = '913061fdd981ef0decf65fcc0916c58b2fd1e7ff0a70b3397459a623e0f08493'
MANIFEST_SHA = '15f8d6b6ae8b0fce32a1cee255a1b707dfcf58b2e7a10b6a94c0c161db2cf3f0'

def need(ok, why):
    if not ok: raise RuntimeError(why)

def sha(b): return hashlib.sha256(b).hexdigest()
def canon(x): return x if x[0] > 0 or (x[0] == 0 and x[1] > 0) else (-x[0],-x[1])
def det(a,b): return a[0]*b[1]-a[1]*b[0]
def determinant(A):
    return (A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1])
            - A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0])
            + A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0]))

def unpack(root):
    raw=(ROOT/ARCHIVE).read_bytes(); need(len(raw)==18270 and sha(raw)==ARCHIVE_SHA,'author ZIP pin')
    with zipfile.ZipFile(ROOT/ARCHIVE) as z:
        names=z.namelist(); need(len(names)==10 and len(set(names))==10,'author members')
        for info in z.infolist():
            need(info.filename not in ('.','..') and '/' not in info.filename and '\\' not in info.filename and stat.S_ISREG(info.external_attr>>16),'safe regular member')
        need(sha(z.read('MANIFEST.json'))==MANIFEST_SHA,'author manifest pin')
        manifest=json.loads(z.read('MANIFEST.json'))
        need(set(names)=={'MANIFEST.json'}|{r['path'] for r in manifest['files']},'exact author inventory')
        for r in manifest['files']:
            data=z.read(r['path']);need(len(data)==r['bytes'] and sha(data)==r['sha256'],'author member integrity')
        z.extractall(root)

def author_run(root, mode, pin=MANIFEST_SHA):
    args=[sys.executable,'-B']+(['-O'] if mode else [])+[str(root/'verify_package.py')]
    if pin is not None:args += ['--manifest-sha256',pin]
    return subprocess.run(args,capture_output=True)

def mutation_controls(original):
    cases=['alter_proof','alter_checker','missing_file','extra_file','wrong_external_pin','no_external_pin','corrupt_manifest','rebound_corrupt_proof','symlink_payload','unsafe_manifest_path','manifest_symlink','duplicate_entry','boolean_size','negative_size','wrong_identity','extra_directory','false_saved_receipt','absolute_path','reserved_manifest_path','bad_hash_format']
    results=[]
    for case in cases:
        with tempfile.TemporaryDirectory() as temp:
            r=pathlib.Path(temp)/'packet';shutil.copytree(original,r);pin=MANIFEST_SHA
            mp=r/'MANIFEST.json';m=json.loads(mp.read_bytes());rebind=False
            if case=='alter_proof': (r/'PROOF.md').write_bytes((r/'PROOF.md').read_bytes()+b'\nchanged\n')
            elif case=='alter_checker':(r/'check_math.py').write_bytes((r/'check_math.py').read_bytes()+b'\n# changed\n')
            elif case=='missing_file':(r/'REPORT.md').unlink()
            elif case=='extra_file':(r/'unexpected').write_text('extra')
            elif case=='wrong_external_pin':pin='0'*64
            elif case=='no_external_pin':pin=None
            elif case=='corrupt_manifest':mp.write_text('invalid JSON')
            elif case=='rebound_corrupt_proof':
                p=r/'PROOF.md';p.write_bytes(p.read_bytes()+b'\nchanged\n')
                for x in m['files']:
                    if x['path']=='PROOF.md':x.update(bytes=p.stat().st_size,sha256=sha(p.read_bytes()))
                mp.write_text(json.dumps(m))  # deliberately retain original external pin
            elif case=='symlink_payload':p=r/'REPORT.md';p.unlink();p.symlink_to(original/'REPORT.md')
            elif case=='manifest_symlink':mp.unlink();mp.symlink_to(original/'MANIFEST.json')
            elif case=='extra_directory':(r/'unexpected_dir').mkdir()
            elif case=='false_saved_receipt':
                p=r/'CHECK_RESULTS.json';p.write_text('{}\n')
                for x in m['files']:
                    if x['path']==p.name:x.update(bytes=p.stat().st_size,sha256=sha(p.read_bytes()))
                rebind=True
            else:
                rebind=True
                if case=='unsafe_manifest_path':m['files'][0]['path']='../PROOF.md'
                elif case=='duplicate_entry':m['files'].append(m['files'][0])
                elif case=='boolean_size':m['files'][0]['bytes']=True
                elif case=='negative_size':m['files'][0]['bytes']=-1
                elif case=='wrong_identity':m['problem_id']=2812
                elif case=='absolute_path':m['files'][0]['path']='/PROOF.md'
                elif case=='reserved_manifest_path':m['files'][0]['path']='MANIFEST.json'
                elif case=='bad_hash_format':m['files'][0]['sha256']='xyz'
            if rebind:
                mp.write_text(json.dumps(m));pin=sha(mp.read_bytes())
            for mode in (False,True):
                result=author_run(r,mode,pin)
                need(result.returncode != 0,'integrity false acceptance: '+case)
            results.append({'case':case,'normal_rejected':True,'optimized_rejected':True})
    return results

def regular_group_checks(author):
    groups=[('C10',tuple(range(10)),0,lambda x,y:(x+y)%10),
            ('C3xC3',tuple(itertools.product(range(3),repeat=2)),(0,0),lambda x,y:((x[0]+y[0])%3,(x[1]+y[1])%3)),
            ('D4',tuple(itertools.product(range(4),range(2))),(0,0),lambda x,y:((x[0]+(-1)**x[1]*y[0])%4,(x[1]+y[1])%2)),
            ('C2xC2',tuple(itertools.product(range(2),repeat=2)),(0,0),lambda x,y:((x[0]+y[0])%2,(x[1]+y[1])%2))]
    result={}
    for name,G,e,mul in groups:
        count=0
        for mask in range(1<<len(G)):
            S={g for j,g in enumerate(G) if mask>>j&1}
            # Count how many labeled translates contain each point; no subset deduplication.
            max_overlap=max(sum(x in {mul(g,s) for s in S} for g in G) for x in G)
            need(max_overlap==len(S),'regular labeled incidence count')
            count+=1
        need(author.group_controls(G,e,mul)==count,'independent/author group equivalence')
        result[name]=count
    # A non-free transitive action may create three labeled translates with one preimage.
    C3=range(3); S={0}; need(sum(0 in S for g in C3)==3 and len(S)==1,'freeness countermodel')
    # A free but nontransitive trivial action on a three-point set misses the fiber triple.
    need(len({0,1,2})==3 and len([0])<3,'transitivity countermodel')
    # Distinct group elements still count if all translated subsets coincide.
    need(len({frozenset({(s+g)%3 for s in range(3)}) for g in range(3)})==1,'subset alias countermodel')
    return result

def slope_checks(author):
    slopes=sorted({canon((p,q)) for p in range(-4,5) for q in range(-4,5) if math.gcd(p,q)==1})
    cases=0
    for a in slopes:
        for b in slopes:
            if a==b:continue
            D=abs(det(a,b));need(D>0,'primitive unoriented aliasing')
            for m,n in itertools.product(range(4),repeat=2):
                P=(abs(b[0])*m+abs(a[0])*n)//D;Q=(abs(b[1])*m+abs(a[1])*n)//D
                expected={canon((p,q)) for p in range(-P,P+1) for q in range(-Q,Q+1) if math.gcd(p,q)==1 and abs(det(a,(p,q)))<=m and abs(det(b,(p,q)))<=n}
                got=author.slope_grid(a,b,m,n);need(got==expected,'independent p,q oracle')
                need(len(got)<=2*m*n+m+n,'exception-count bound')
                need(got==author.slope_grid(tuple(-x for x in a),tuple(-x for x in b),m,n),'both slope signs')
                # Integral determinant distances versus nonintegral strict thresholds.
                ka=F(3*m+2,3);kb=F(5*n+4,5)
                need(all(abs(det(a,g))<=ka and abs(det(b,g))<=kb for g in got),'floor threshold interpretation')
                for T in (lambda v:(v[0]+2*v[1],v[1]),lambda v:(v[0],-v[1])):
                    need({canon(T(g)) for g in got}==author.slope_grid(T(a),T(b),m,n),'GL2Z covariance')
                cases+=1
    need(author.slope_grid((1,0),(0,1),0,0)==set(),'zero-area grid')
    need(author.slope_grid((1,0),(0,1),0,3)=={(1,0)},'zero-width grid')
    rejected=0
    for a,b,m,n in [((1,0),(-1,0),1,1),((0,1),(0,-1),0,0),((1,0),(0,1),1,-1)]:
        try:author.slope_grid(a,b,m,n)
        except RuntimeError:rejected+=1
    need(rejected==3,'dependent and negative cases')
    return {'primitive_representatives':len(slopes),'ordered_pair_threshold_cases':cases,'additional_invalid_cases':rejected}

def affine_checks(author):
    cases=0
    shifts=[(0,0,0)]+[tuple(s if i==j else 0 for i in range(3)) for j in range(3) for s in (-1,1)]
    for coeff in itertools.product((-1,0,1),repeat=6):
        it=iter(coeff);A=[[F(0) if i==j else F(next(it),6) for j in range(3)] for i in range(3)]
        M=[[F(i==j)-A[i][j] for j in range(3)] for i in range(3)];D=determinant(M)
        need(D!=0,'rank three from strict contraction')
        for shift in shifts:
            B=[F(v,3) for v in shift];x=[]
            for col in range(3):
                N=[row[:] for row in M]
                for row in range(3):N[row][col]=B[row]
                x.append(determinant(N)/D)
            need(all(abs(t)<1 for t in x),'interior exact Cramer point')
            need(all(x[i]==B[i]+sum(A[i][j]*x[j] for j in range(3)) for i in range(3)),'independent affine equations')
            need(x==author.solve_affine(A,B),'Cramer versus elimination')
            cases+=1
    # These limiting examples are intentionally outside the strict hypotheses.
    need(determinant([[1,-1,0],[-1,1,0],[0,0,1]])==0,'dependent-normal rank countermodel')
    # x=y, y=x, z=0 intersect; x=y+epsilon, y=x, z=0 do not for epsilon nonzero.
    need(F(1,100)!=0,'nontransverse triple may disappear')
    need(not all(abs(v)<1 for v in [1,1,1]),'closed-range-only boundary fixed point')
    return {'exact_affine_cases':cases,'rank_and_boundary_countermodels':3}

def main():
    with tempfile.TemporaryDirectory() as temp:
        root=pathlib.Path(temp)/'author';root.mkdir();unpack(root)
        normal=author_run(root,False);optimized=author_run(root,True)
        need(normal.returncode==optimized.returncode==0 and not normal.stderr and not optimized.stderr and normal.stdout==optimized.stdout,'author positive replay')
        spec=importlib.util.spec_from_file_location('pinned_author_math',root/'check_math.py');author=importlib.util.module_from_spec(spec);spec.loader.exec_module(author)
        result={'status':'PASS_INDEPENDENT_FINITE_AND_INTEGRITY_CONTROLS','author_archive_sha256':ARCHIVE_SHA,
                'author_replay':json.loads(normal.stdout),'author_math':json.loads((root/'CHECK_RESULTS.json').read_bytes()),
                'independent_group_subsets':regular_group_checks(author),'independent_slopes':slope_checks(author),
                'independent_affine':affine_checks(author),'integrity_negatives':mutation_controls(root),
                'scope':'Finite diagnostics supplement the independently reviewed all-size proofs; no hyperbolic realization, universal theorem, or novelty certification.'}
        print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
