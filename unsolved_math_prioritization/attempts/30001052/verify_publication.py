#!/usr/bin/env python3
"""Source-free, closed-inventory replay; never edits frozen files."""
from pathlib import Path, PurePosixPath
import argparse,hashlib,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parent
ANCHORS={'packet/AUTHOR_MANIFEST.json':'cfa02b87b3cd03463d68912a12b621c7603cd00b86143edf3562055c1a933407','independent_audit/AUDIT_MANIFEST.json':'865530552768ab8b0336fde8e82ac9e00739ac979bc445d4a0f1a9ffaaf31845'}
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def digest(path):
    b=path.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def inventory(root):
    names=set()
    for p in root.rglob('*'):
        need(not p.is_symlink(),'symlink member: '+str(p.relative_to(root)))
        if p.is_file():names.add(p.relative_to(root).as_posix())
    return names
def validate(root,manifest_name):
    m=json.loads((root/manifest_name).read_text());need(isinstance(m['files'],dict),'manifest mapping')
    expected=set(m['files'])|{manifest_name}
    for n in expected:
        q=PurePosixPath(n)
        need(not q.is_absolute() and '..' not in q.parts and str(q)==n and '\\' not in n,'unsafe manifest path')
    need(inventory(root)==expected,'inventory differs: '+repr(sorted(inventory(root)^expected)))
    for n,d in m['files'].items():need(digest(root/n)==d,'hash/size mismatch: '+n)
    return len(expected)
def command(script):
    level=sys.flags.optimize;flags=['-O']*level
    return [sys.executable,*flags,'-B',str(script)]
def run(script):
    env=dict(os.environ);env['PYTHONOPTIMIZE']=str(sys.flags.optimize);env['PYTHONDONTWRITEBYTECODE']='1'
    r=subprocess.run(command(script),env=env,cwd=ROOT,capture_output=True)
    need(r.returncode==0,'checker failed: '+script.name+'\n'+r.stderr.decode())
    return r.stdout

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--manifest-sha256');args=ap.parse_args()
    if args.manifest_sha256:need(digest(ROOT/'PUBLIC_MANIFEST.json')['sha256']==args.manifest_sha256,'external manifest anchor mismatch')
    count=validate(ROOT,'PUBLIC_MANIFEST.json')
    for name,h in ANCHORS.items():need(digest(ROOT/name)['sha256']==h,'frozen manifest anchor: '+name)
    need(validate(ROOT/'packet','AUTHOR_MANIFEST.json')==14,'author count')
    need(validate(ROOT/'independent_audit','AUDIT_MANIFEST.json')==11,'audit count')
    import sympy
    need(sympy.__version__=='1.14.0','exact replay requires SymPy 1.14.0')
    jobs=[('packet/check_fusion.py','packet/FUSION_CHECKS.json'),('packet/check_obstructions.py','packet/OBSTRUCTION_CHECKS.json'),('independent_audit/independent_fusion_check.py','independent_audit/INDEPENDENT_FUSION_CHECKS.json'),('independent_audit/independent_obstruction_check.py','independent_audit/INDEPENDENT_OBSTRUCTION_CHECKS.json')]
    outputs=[]
    for script,result in jobs:
        out=run(ROOT/script);need(out==(ROOT/result).read_bytes(),'checker output differs: '+script)
        outputs.append({'script':script,'optimize':sys.flags.optimize,'sha256':hashlib.sha256(out).hexdigest(),'byte_exact':True})
    author=json.loads(run(ROOT/'packet/verify.py'));need(author['status']=='PASS','author verifier status')
    print(json.dumps({'status':'PASS','problem_id':30001052,'problem_status':'unsolved','turns':'5/5','public_files':count,'frozen_files':25,'optimize':sys.flags.optimize,'explicit_child_optimization':True,'replays':outputs,'full_source_audit_repeated':False,'general_homotopy_theory_formalized':False},indent=2,sort_keys=True))
if __name__=='__main__':main()
