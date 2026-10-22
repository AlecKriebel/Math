#!/usr/bin/env python3
"""Authenticate this source package; run exact finite controls in a disposable copy.
This is not a proof assistant or a priority certificate. No network or source writes.
"""
import argparse, hashlib, json, os, shutil, stat, subprocess, sys, tempfile
from pathlib import Path, PurePosixPath

def need(ok, why):
    if not ok: raise ValueError(why)

def pairs(items):
    out={}
    for k,v in items:
        need(k not in out,'duplicate JSON key');out[k]=v
    return out

def loads(b):
    return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON')))

def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def safe(n):
    need(type(n) is str and n and not n.startswith('/') and '\\' not in n and ':' not in n,'unsafe name')
    need(all(v not in ('','.','..') for v in n.split('/')) and str(PurePosixPath(n))==n,'noncanonical name')

def same(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return set(a)==set(b) and all(same(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b

def inventory(root):
    out={}
    for p in root.rglob('*'):
        need(not p.is_symlink(),'symlink')
        if p.is_file():out[str(p.relative_to(root))]=pin(p.read_bytes())
        else:need(p.is_dir(),'special file')
    return out

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--manifest-sha256');args=ap.parse_args()
    root=Path(__file__).resolve().parents[1];mb=(root/'SOURCE_MANIFEST.json').read_bytes()
    if args.manifest_sha256:need(hashlib.sha256(mb).hexdigest()==args.manifest_sha256,'external manifest anchor')
    manifest=loads(mb);need(type(manifest) is dict and bool(manifest),'manifest schema')
    expected_names=set(manifest)|{'SOURCE_MANIFEST.json'}
    generated={'output/finite-warm-thresholds-source-and-verification.zip','output/zenodo-upload-kit.zip'}
    before=inventory(root);need(set(before)-expected_names<=generated and expected_names<=set(before),'source not closed')
    for n,p in manifest.items():
        safe(n);need(type(p) is dict and set(p)=={'bytes','sha256'} and type(p['bytes']) is int and p['bytes']>=0,'bad pin')
        need(before[n]==p,'source fingerprint '+n)
    plan=loads((root/'verification/CONTROL_PLAN.json').read_bytes());expected=loads((root/'verification/EXPECTED.json').read_bytes())
    need(plan['modes']==[[],['-O'],['-OO']],'three modes required')
    need([s['name'] for s in plan['suites']]==['forest','whisker','prior24'] and set(expected)=={'forest','whisker','prior24'},'suite identity')
    runs=[]
    with tempfile.TemporaryDirectory(prefix='finite-warm-controls-') as temp:
        mirror=Path(temp)/'source';mirror.mkdir()
        for n in expected_names:
            safe(n);p=mirror/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((root/n).read_bytes())
        copied=inventory(mirror)
        for p in mirror.rglob('*'):p.chmod(0o555 if p.is_dir() else 0o444)
        mirror.chmod(0o555)
        try:
            for flags in plan['modes']:
                for s in plan['suites']:
                    safe(s['program']);need(s['program'] in manifest,'unbound program')
                    cmd=[sys.executable,*flags,'-B',str(mirror/s['program']),*s['args']]
                    z=subprocess.run(cmd,cwd=mirror,capture_output=True,text=True,timeout=60,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
                    need(z.returncode==0,'control process failed '+s['name']+': '+z.stderr[-1000:])
                    value=loads(z.stdout);need(same(value,expected[s['name']]),'complete exact result/type mismatch '+s['name'])
                    runs.append({'suite':s['name'],'flags':flags,'complete_result':value})
            need(inventory(mirror)==copied,'control modified copied inputs')
        finally:
            for p in mirror.rglob('*'):
                if p.is_dir():p.chmod(0o755)
            mirror.chmod(0o755)
    need(inventory(root)==before,'source changed during run')
    print(json.dumps({'status':'PASS','scope':'Exact finite mathematical controls and integrity only, not universal proof/priority certification','source_payloads':len(manifest),'all_source_and_copy_bytes_unchanged':True,'runs':runs},sort_keys=True))

if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,TypeError,OSError,subprocess.TimeoutExpired) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
