#!/usr/bin/env python3
"""Review-only independent arithmetic, archive and package-rebuild checks."""
from pathlib import Path
from fractions import Fraction
import ast, datetime, hashlib, itertools, json, os, shutil, subprocess, sys, zipfile
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import sympy as sp
import verify_exact as sparse
import verify_concurrent_equivalence as dense
import verify_tensor_words as words
import verify_braid_link as braid
EVIDENCE=Path(__file__).resolve().parent

def require(condition,label):
    if not condition: raise RuntimeError(label)
    print('[ok]',label,flush=True)

def sym(value):
    return sum(coefficient*radical for coefficient,radical in zip(value.re.v,(1,sp.sqrt(2),sp.sqrt(3),sp.sqrt(6))))+sp.I*sum(coefficient*radical for coefficient,radical in zip(value.im.v,(1,sp.sqrt(2),sp.sqrt(3),sp.sqrt(6))))

for module in (sparse,dense):
    real=[module.Q23(*(int(i==j) for i in range(4))) for j in range(4)]
    basis=[module.CQ23(x) for x in real]+[module.CQ23(0,x) for x in real]
    for a,b in itertools.product(basis,repeat=2):
        require(sp.expand(sym(a*b)-sym(a)*sym(b))==0,'field basis product '+module.__name__)
    for a in basis:
        require(sp.expand(sym(a.conjugate())-sp.conjugate(sym(a)))==0,'field conjugation '+module.__name__)
        require(bool(a),'field nonzero basis '+module.__name__)
    require(not module.CQ23(),'field zero '+module.__name__)
    require(all(a!=b for i,a in enumerate(basis) for b in basis[i+1:]),'distinct exact field basis '+module.__name__)
    # A fixed rational combination also tests linear accumulation/cancellation.
    x=sum((Fraction(i-3,7)*a for i,a in enumerate(basis)),module.CQ23())
    y=sum((Fraction(5-i,11)*a for i,a in enumerate(basis)),module.CQ23())
    require(sp.expand(sym(x*y)-sym(x)*sym(y))==0,'rational linear-combination multiplication '+module.__name__)
    require(not (x-x),'cancellation '+module.__name__)

I=sp.eye(2);X=sp.Matrix([[0,1],[1,0]]);Z=sp.diag(1,-1);J=X*Z;Y=sp.I*J
real={'I':I,'X':X,'Z':Z,'J':J}; complex_pauli={'I':I,'X':X,'Y':Y,'Z':Z}
for (a,b),(sign,c) in words.SINGLE_PRODUCT.items():
    require(real[a]*real[b]==sign*real[c],'real Pauli multiplication '+a+b)
for (a,b),(phase,c) in braid.PAULI_PRODUCT.items():
    require(complex_pauli[a]*complex_pauli[b]==sym(phase)*complex_pauli[c],'complex Pauli multiplication '+a+b)
for axis in complex_pauli:
    u=(I+sp.I*complex_pauli[axis])/sp.sqrt(2)
    for word in complex_pauli:
        for inverse in (False,True):
            phase,out=braid.quarter_turn_conjugate_word(word,axis,inverse)
            v=u.conjugate().T if inverse else u
            require(sp.simplify(v*complex_pauli[word]*v.conjugate().T-sym(phase)*complex_pauli[out])==sp.zeros(2),'quarter-turn conjugation '+axis+word+str(inverse))

identity,m,e,h,q,k,ki,r,ri=braid.build_five_word_data()
pr,pri=braid.literal_five_word_pauli_operators(q,k)
require(dense.equal(r,braid.pauli_sum_matrix(pr)),'literal Pauli R agrees with dense five-word R')
require(dense.equal(ri,braid.pauli_sum_matrix(pri)),'literal Pauli R inverse agrees with dense R inverse')

supported=('verify_exact.py','verify_tensor_words.py','verify_supplied.py','verify_concurrent_equivalence.py','verify_braid_link.py')
for name in supported:
    tree=ast.parse((ROOT/name).read_text())
    require(not any(isinstance(node,ast.Constant) and isinstance(node.value,(float,complex)) for node in ast.walk(tree)),name+' has no binary float/complex literals')

manifest={'SHA256SUMS':hashlib.sha256((ROOT/'SHA256SUMS').read_bytes()).hexdigest()}
manifest.update({name:digest for digest,name in (line.split('  ',1) for line in (ROOT/'SHA256SUMS').read_text().splitlines())})
archive=ROOT/'submission/exceptional-ybe-d4-v1.2.0-source.zip'; prefix='exceptional-ybe-d4-v1.2.0/'
with zipfile.ZipFile(archive) as z:
    require(z.testzip() is None,'source ZIP CRC checks')
    require(len(z.namelist())==len(set(z.namelist())),'source ZIP has no duplicate member paths')
    require(set(z.namelist())=={prefix+x for x in manifest},'source ZIP is exactly manifest allowlist plus manifest')
    for name,digest in manifest.items():
        require(hashlib.sha256(z.read(prefix+name)).hexdigest()==digest,'archive member hash '+name)
with zipfile.ZipFile(ROOT/'submission/exceptional-ybe-d4-v1.2.0-arxiv.zip') as z:
    require(z.namelist()==['main.tex'],'arXiv ZIP contains only main.tex')
    require(z.read('main.tex')==(ROOT/'main.tex').read_bytes(),'arXiv main.tex agrees byte-for-byte')
for file in ('SHA256SUMS','ARXIV_SHA256SUMS'):
    for line in (ROOT/'submission'/file).read_text().splitlines():
        digest,name=line.split('  ',1)
        require(hashlib.sha256((ROOT/'submission'/name).read_bytes()).hexdigest()==digest,'submission hash '+name)

copy=ROOT/'submission_review_2026-09-25/tmp/baseline_package_copy'
copy.mkdir(parents=True,exist_ok=True)
for name in manifest:
    destination=copy/name;destination.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,destination)
env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
result=subprocess.run([sys.executable,str(copy/'package_submission.py')],cwd=copy,env=env,capture_output=True,text=True)
(EVIDENCE/'baseline_package_rebuild.log').write_text(result.stdout+result.stderr)
require(result.returncode==0,'isolated unchanged-release package rebuild')
for original in (ROOT/'submission').iterdir():
    require(original.read_bytes()==(copy/'submission'/original.name).read_bytes(),'deterministic rebuilt artifact '+original.name)

print('All review-only reproducibility checks passed at',datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
