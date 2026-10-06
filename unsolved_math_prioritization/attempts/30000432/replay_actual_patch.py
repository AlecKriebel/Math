#!/usr/bin/env python3
"""Apply the distributed patch itself, then reproduce both defects and fixes."""
import difflib, hashlib, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).absolute().parent
def need(ok,why):
    if not ok:raise RuntimeError(why)
def manifest(root):
    files={p.relative_to(root).as_posix():{'bytes':len(p.read_bytes()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(root.rglob('*')) if p.is_file() and p.name!='MANIFEST.json'}
    (root/'MANIFEST.json').write_text(json.dumps({'files':files},indent=2,sort_keys=True)+'\n')
def run(root,opt=False,harness=False):
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env.pop('PYTHONPATH',None);env['PYTHONDONTWRITEBYTECODE']='1'
    return subprocess.run([sys.executable]+(['-O'] if opt else [])+[str(root/('run_checks.py' if harness else 'verify.py'))],cwd=root.parent,env=env,capture_output=True)
def main():
    env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
    gate=subprocess.run([sys.executable,str(ROOT/'verify_package.py'),'--integrity-only'],cwd=ROOT.parent,env=env,capture_output=True)
    need(gate.returncode==0,gate.stderr.decode(errors='replace'))
    expected=json.loads((ROOT/'audit/CHECKS.json').read_text());rows=[]
    with tempfile.TemporaryDirectory(prefix='equal-area-actual-patch-') as td:
        td=Path(td);patched=td/'patched';shutil.copytree(ROOT/'author',patched)
        patch=(ROOT/'audit/AUTHOR_HARDENING.patch').read_bytes()
        r=subprocess.run(['patch','--batch','--fuzz=0','-p1'],input=patch,cwd=patched,capture_output=True)
        need(r.returncode==0,'Actual patch failed: '+r.stderr.decode(errors='replace'))
        source=(ROOT/'author/verify.py').read_text();result=(patched/'verify.py').read_text()
        reconstructed=''.join(difflib.unified_diff(source.splitlines(True),result.splitlines(True),fromfile='a/verify.py',tofile='b/verify.py'))
        need(reconstructed.encode()==patch,'Actual patch bytes differ from resulting edit')
        need(set(p.name for p in patched.iterdir())==set(p.name for p in (ROOT/'author').iterdir()),'Patch left unexpected files')
        manifest(patched)
        for opt in (False,True):
            p=run(patched,opt);need(p.returncode==0,'Patched baseline failed');need(json.loads(p.stdout)==expected['separate_hardened_author_baseline'],'Patched baseline differs')
        harness=run(patched,harness=True);need(harness.returncode==0,'Patched original harness failed')
        need(json.loads(harness.stdout)==expected['separate_hardened_author_original_harness'],'Patched harness differs')
        for hard,base in ((False,ROOT/'author'),(True,patched)):
            for case in ('translated_family','unlisted_FIFO'):
                d=td/(str(hard)+'_'+case);shutil.copytree(base,d)
                if case=='translated_family':
                    p=d/'verify.py';s=p.read_text();anchor='    return points,faces';need(s.count(anchor)==1,'Translation anchor')
                    p.write_text(s.replace(anchor,'    points={v:(x+Q(1,1000),y-Q(1,500)) for v,(x,y) in points.items()}\n'+anchor));manifest(d)
                else:os.mkfifo(d/'unlisted_FIFO')
                for opt in (False,True):
                    p=run(d,opt);need((p.returncode!=0)==hard,'Defect expectation: '+case)
                    rows.append({'case':case,'hardening_applied':hard,'optimized':opt,'accepted':p.returncode==0})
        need(rows==expected['reproduced_original_gaps_and_hardened_rejections'],'Defect history differs')
    print(json.dumps({'status':'PASS','actual_patch_applied':True,'zero_fuzz':True,'patched_verifier_sha256':hashlib.sha256(result.encode()).hexdigest(),'patch_sha256':hashlib.sha256(patch).hexdigest(),'separate_hardened_author_baseline':expected['separate_hardened_author_baseline'],'patched_original_harness_matches_frozen_audit':True,'frozen_author_unchanged':True,'reproduced_original_gaps_and_hardened_rejections':rows},indent=2,sort_keys=True))
if __name__=='__main__':main()
