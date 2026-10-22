#!/usr/bin/env python3
"""Independent reviewer controls. Writes only temporary copies outside author packet."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile

AUTHOR=Path(__file__).resolve().parents[2]/'public'
ANCHOR='f7b959531c352611c5c9b9d0c2cb57bcb865de9399d65dbd66c4fabef3a88e59'
passed=[]
def need(test, value):
    if not value: raise RuntimeError(test)
    passed.append(test)
def sha(b):return hashlib.sha256(b).hexdigest()
def matmul(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def trans(a):return list(map(list,zip(*a)))
def power(a,n):
    p=[[F(1),F(0)],[F(0),F(1)]]
    while n:
        if n&1:p=matmul(p,a)
        a=matmul(a,a);n//=2
    return p
A=[[F(3,5),F(-4,5)],[F(4,5),F(3,5)]]
I=[[F(1),F(0)],[F(0),F(1)]]
need('frozen_manifest_hash',sha((AUTHOR/'MANIFEST.json').read_bytes())==ANCHOR)
need('independent_orthogonal',matmul(trans(A),A)==I)
need('independent_det',A[0][0]*A[1][1]-A[0][1]*A[1][0]==1)
# Independent Gaussian-integer computation, no author recurrence code imported.
a,b=1,0
for n in range(1,1001):
    a,b=3*a-4*b,4*a+3*b
    need(f'gaussian_norm_{n}',a*a+b*b==25**n)
    need(f'gaussian_trace_residue_{n}',(2*a)%5==1)
    need(f'gaussian_nonidentity_{n}',(a,b)!=(5**n,0))
# Independent structural residue certificate: i maps to 2 and -2 in F_5.
need('residue_roots',2*2%5==(-1)%5 and (-2)*(-2)%5==(-1)%5)
need('residue_split_witness', (3+4*2)%5==1 and (3-4*2)%5==0)
for n in [1,2,3,5,11,29,127,511]:
    p=power(A,n)
    need(f'orthogonal_fast_power_{n}',matmul(trans(p),p)==I)
    need(f'inverse_power_{n}',matmul(p,power(trans(A),n))==I)
# Nonorthogonal conjugate preserves a positive-definite quadratic form.
T=[[F(2),F(1)],[F(0),F(1)]]
Ti=[[F(1,2),F(-1,2)],[F(0),F(1)]]
C=matmul(matmul(T,A),Ti)
Q=matmul(trans(Ti),Ti)
need('conjugation_identity',matmul(T,Ti)==I)
need('conjugate_is_not_euclidean_rotation',matmul(trans(C),C)!=I)
need('conjugate_preserves_Q',matmul(matmul(trans(C),Q),C)==Q)
need('Q_positive_definite',Q[0][0]>0 and Q[0][0]*Q[1][1]-Q[0][1]*Q[1][0]>0)
R=[[F(0),F(-1)],[F(1),F(0)]]
H=[[F(2),F(0)],[F(0),F(1,2)]]
need('finite_rotation_negative_control',matmul(trans(R),R)==I and power(R,4)==I)
need('det_one_negative_control',H[0][0]*H[1][1]==1 and matmul(trans(H),H)!=I)
need('two_end_negative_control',2-1<2)
need('three_end_positive_control',3-1>=2)
need('three_point_witness',len({F(0),F(2,3),F(1)})==3)
# Anchor and inventory attack controls in disposable copies.
mutation_results=[]
def run_packet(root,anchor,mode=False):
    return subprocess.run([sys.executable,*(['-O'] if mode else []),'-B',str(root/'VERIFY.py'),anchor],capture_output=True,text=True)
def reanchor(root):
    return sha((root/'MANIFEST.json').read_bytes())
def altered_manifest(root,fn):
    p=root/'MANIFEST.json';m=json.loads(p.read_text());fn(m);p.write_text(json.dumps(m,indent=2)+'\n')
def rebind(root,name):
    def update(m):
        for item in m['files']:
            if item['path']==name:
                b=(root/name).read_bytes();item['bytes']=len(b);item['sha256']=sha(b)
    altered_manifest(root,update)
def exercise(label,mutation,expected,reanchored=False):
    with tempfile.TemporaryDirectory(prefix='veech-review-b-') as td:
        root=Path(td)/'packet';shutil.copytree(AUTHOR,root)
        mutation(root)
        anchor=reanchor(root) if reanchored else ANCHOR
        for mode in (False,True):
            p=run_packet(root,anchor,mode)
            need(label+('_optimized' if mode else '_ordinary'),p.returncode!=0 and expected in p.stderr)
        mutation_results.append({'case':label,'rejected_in':['ordinary','optimized'],'expected_error':expected})
for mode in (False,True):
    p=run_packet(AUTHOR,ANCHOR,mode)
    need('author_packet_baseline_'+str(mode),p.returncode==0 and json.loads(p.stdout)['total_exact_checks_per_mode']==1996)
exercise('wrong_manifest_bytes',lambda p:(p/'MANIFEST.json').write_bytes((p/'MANIFEST.json').read_bytes()+b' '),'Manifest anchor mismatch')
exercise('proof_byte_change',lambda p:(p/'PROOF.md').write_bytes((p/'PROOF.md').read_bytes()+b'x'),'Size mismatch')
exercise('missing_file',lambda p:(p/'README.md').unlink(),'Missing, linked or non-file member')
exercise('extra_file',lambda p:(p/'SURPRISE').write_text('x'),'Exact inventory mismatch')
def member_link(p):
    (p/'README.md').unlink();(p/'README.md').symlink_to(AUTHOR/'README.md')
exercise('member_symlink',member_link,'Missing, linked or non-file member')
def manifest_link(p):
    (p/'MANIFEST.json').unlink();(p/'MANIFEST.json').symlink_to(AUTHOR/'MANIFEST.json')
exercise('manifest_symlink',manifest_link,'Manifest symlink forbidden')
exercise('duplicate_json_key',lambda p:(p/'MANIFEST.json').write_text((p/'MANIFEST.json').read_text().replace('{','{"schema":"veech-ends-author-v1",',1)),'Duplicate JSON key',True)
exercise('unsafe_member_name',lambda p:altered_manifest(p,lambda m:m['files'][0].update(path='../escape')),'Unsafe inventory member',True)
exercise('duplicate_member_name',lambda p:altered_manifest(p,lambda m:m['files'].append(m['files'][0])),'Duplicate inventory member',True)
def receipt_change(p):
    q=p/'CHECK_RESULTS.json';d=json.loads(q.read_text());d['total_exact_checks']=0;q.write_text(json.dumps(d,sort_keys=True,indent=2)+'\n');rebind(p,q.name)
exercise('rebound_false_receipt',receipt_change,'Arithmetic receipt mismatch',True)
def checker_failure(p):
    q=p/'CHECKS.py';q.write_text('raise RuntimeError("review control")\n');rebind(p,q.name)
exercise('rebound_checker_failure',checker_failure,'Arithmetic replay failed',True)
need('author_manifest_unchanged_after_controls',sha((AUTHOR/'MANIFEST.json').read_bytes())==ANCHOR)
print(json.dumps({'status':'PASS','independent_exact_checks':len(passed),'gaussian_power_bound':1000,'verifier_negative_controls':mutation_results,'author_manifest_sha256':ANCHOR,'limits':'Finite controls do not prove topological or analytic lemmas. Gaussian residue argument is proved symbolically in ACCEPTANCE.md. Mutation tests use disposable copies; the author packet is unchanged.'},indent=2,sort_keys=True))
