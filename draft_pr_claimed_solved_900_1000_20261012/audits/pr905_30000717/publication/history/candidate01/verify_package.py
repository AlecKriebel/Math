#!/usr/bin/env python3
"""Check release bytes, then replay mathematical controls in disposable copies."""
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parent
ORIGINAL_PROOF='a2e2109d45f7776103fc43cff554c7f49de1b9290b92dc62b3d3db5ad23050c1'
ORIGINAL_MANIFEST='1492167c7a7cfeb168976aa4d91b32c0be56c3b58de4090c417785a9d324a765'
def require(ok,message):
    if not ok: raise ValueError(message)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def integrity(pdf,anchor):
    mp=ROOT/'PACKAGE_MANIFEST.json'; raw=mp.read_bytes()
    if anchor: require(hashlib.sha256(raw).hexdigest()==anchor,'Outer manifest anchor mismatch')
    m=json.loads(raw); require(m['problem_id']==30000717 and m['pr_number']==905 and m['version']=='1.0','Wrong release identity')
    expected=m['files']; require(isinstance(expected,dict) and expected,'Empty manifest')
    actual=set()
    for p in ROOT.rglob('*'):
        require(not p.is_symlink(),'Symlink forbidden: '+str(p))
        require(p.is_dir() or p.is_file(),'Special filesystem entry forbidden: '+str(p))
        if p.is_file(): actual.add(p.relative_to(ROOT).as_posix())
    require(actual==set(expected)|{'PACKAGE_MANIFEST.json'},'Payload file-set mismatch')
    for name,item in expected.items():
        n=PurePosixPath(name); require(not n.is_absolute() and '..' not in n.parts and n.as_posix()==name,'Unsafe manifest path')
        p=ROOT.joinpath(*n.parts); require(p.is_file() and not p.is_symlink(),'Nonregular payload')
        require(type(item['bytes']) is int and p.stat().st_size==item['bytes'],'Byte-count mismatch: '+name)
        require(digest(p)==item['sha256'],'Payload digest mismatch: '+name)
    require(digest(ROOT/'original_packet/author/PROOF.md')==ORIGINAL_PROOF,'Original proof anchor mismatch')
    require(digest(ROOT/'original_packet/PUBLIC_MANIFEST.json')==ORIGINAL_MANIFEST,'Original manifest anchor mismatch')
    if pdf:
        require(pdf.is_file() and not pdf.is_symlink(),'Missing/nonregular PDF')
        require(pdf.stat().st_size==m['separate_pdf']['bytes'] and digest(pdf)==m['separate_pdf']['sha256'],'PDF mismatch')
    return m

def run(script,extra):
    env=dict(os.environ); env.pop('PYTHONOPTIMIZE',None); env['PYTHONDONTWRITEBYTECODE']='1'
    p=subprocess.run([sys.executable,'-I','-B',str(script),*extra],cwd=script.parent,env=env,text=True,capture_output=True,timeout=300)
    require(p.returncode==0,'Replay failed: '+script.name+'\n'+p.stderr)
    data=json.loads(p.stdout)
    verdict=data.get('verdict',data.get('status',data.get('result','')))
    require(isinstance(verdict,str) and verdict.startswith('PASS'),'Missing explicit PASS: '+script.name)
    return data

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--integrity-only',action='store_true'); ap.add_argument('--pdf',type=Path); ap.add_argument('--expected-manifest'); args=ap.parse_args()
    m=integrity(args.pdf,args.expected_manifest); jobs=[]
    if not args.integrity_only:
        import sympy
        require(sympy.__version__=='1.14.0','Requires SymPy1.14.0 in this interpreter')
        with tempfile.TemporaryDirectory(prefix='robinson-publication-') as d:
            work=Path(d)/'package'; shutil.copytree(ROOT,work)
            commands=[('original_packet/verify_publication.py',['--expected-manifest',ORIGINAL_MANIFEST]),('original_packet/mutation_tests.py',['--expected-manifest',ORIGINAL_MANIFEST]),('reviews/proof_family/check_exact.py',[]),('reviews/computation_family/checks/exact_controls.py',[])]
            for name,extra in commands:
                data=run(work/name,extra)
                if name.endswith('mutation_tests.py'): require(data['rejected_mutations']==61,'Original mutation count changed')
                if name.endswith('verify_publication.py'): require(data['author_assertions']==185 and data['audit_b_assertions']==51,'Original replay scope changed')
                jobs.append({'script':name,'verdict':data.get('verdict',data.get('status',data.get('result'))),'returncode':0})
    integrity(args.pdf,args.expected_manifest)
    print(json.dumps({'status':'PASS','problem_id':30000717,'payload_files':len(m['files']),'pdf_verified':bool(args.pdf),'replayed_suites':jobs,'distributed_files_unchanged':True,'scope':'Supporting exact controls and byte consistency; universal nonexistence proved in note.'},indent=2))
if __name__=='__main__':
    try: main()
    except Exception as e: print('FAIL: '+str(e),file=sys.stderr); sys.exit(1)
