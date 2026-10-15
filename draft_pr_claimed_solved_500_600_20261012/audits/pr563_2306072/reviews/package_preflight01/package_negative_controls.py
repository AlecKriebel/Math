#!/usr/bin/env python3
"""Exercise package failure boundaries on disposable independent copies only."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import sys

OUT = Path(__file__).resolve().parent
SOURCE = OUT/'.cache/extract/support_slit_verification'
results=[]

def outer_refresh(root, path):
    m=json.loads((root/'MANIFEST.json').read_text())
    data=(root/path).read_bytes()
    m['files'][path]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
    (root/'MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')

def source_refresh(root, path):
    outer_refresh(root,path)
    name='reviews/source01/AUTHORED_MANIFEST.json'
    m=json.loads((root/name).read_text())
    rel=Path(path).name
    data=(root/path).read_bytes()
    m['files'][rel]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
    (root/name).write_text(json.dumps(m,indent=2)+'\n')
    outer_refresh(root,name)

def case(label, change, expect_pass=False, options=None):
    with tempfile.TemporaryDirectory(prefix='negative-',dir=OUT/'.cache') as d:
        root=Path(d)/'package'; shutil.copytree(SOURCE,root)
        change(root)
        options=options or {}
        p=subprocess.run([sys.executable,*options.get('flags',[]),'run_all.py'],cwd=root,
                         env=dict(os.environ,**options.get('env',{})),capture_output=True,text=True)
        accepted=p.returncode==0
        if accepted!=expect_pass:
            raise RuntimeError(label+': unexpected acceptance='+str(accepted)+'\n'+p.stderr)
        results.append({'name':label,'expected':'PASS' if expect_pass else 'REJECT',
                        'actual':'PASS' if accepted else 'REJECT','returncode':p.returncode,
                        'diagnostic':p.stdout.splitlines()[-1] if accepted else p.stderr.splitlines()[-1]})

case('unlisted hidden file',lambda p:(p/'.unlisted').write_text('negative-control'))
case('missing archived gitignore',lambda p:(p/'reviews/priority03/.gitignore').unlink())
case('missing complete JSONL evidence ledger',lambda p:(p/'reviews/priority03/SOURCE_RETRIEVALS.jsonl').unlink())
case('source changed without updating authority',lambda p:(p/'support_slit.tex').write_text((p/'support_slit.tex').read_text()+'\n'))
case('unlisted symlink',lambda p:(p/'unlisted-symlink').symlink_to(p/'README.md'))
case('optimizer flag',lambda p:None,options={'flags':['-O']})
case('optimizer environment',lambda p:None,options={'env':{'PYTHONOPTIMIZE':'1'}})

def nested_disagreement(p):
    path='reviews/priority03/BROWN_SUPPORT_WAVER.md'
    (p/path).write_text((p/path).read_text()+'\nOuter seal alone must not supersede inner seal.\n')
    outer_refresh(p,path)
case('outer-authorized content still disagrees with inner seal',nested_disagreement)

def registry_disagreement(p):
    (p/'SEALS.json').write_text(json.dumps(json.loads((p/'SEALS.json').read_text())[:-1])+'\n')
    outer_refresh(p,'SEALS.json')
case('independently registered seal list disagreement',registry_disagreement)

def excessive_normalization(p):
    jobs=json.loads((p/'JOBS.json').read_text())
    jobs[6]['ignored_dynamic_fields']=['checked_at_utc','q_at_1']
    (p/'JOBS.json').write_text(json.dumps(jobs,indent=2)+'\n'); outer_refresh(p,'JOBS.json')
case('mathematical field cannot be normalized away',excessive_normalization)

def wrong_normalization(p):
    jobs=json.loads((p/'JOBS.json').read_text())
    jobs[0]['ignored_dynamic_fields']=['checked_at_utc']
    (p/'JOBS.json').write_text(json.dumps(jobs,indent=2)+'\n'); outer_refresh(p,'JOBS.json')
case('timestamp exception cannot migrate to different job',wrong_normalization)

def source_value_drift(p):
    path='reviews/source01/SOURCE_BRIDGE_CHECKS.json'
    record=json.loads((p/path).read_text()); record['q_at_1']='3/4'
    (p/path).write_text(json.dumps(record,indent=2)+'\n'); source_refresh(p,path)
case('source bridge mathematical result drift after consistent resealing',source_value_drift)

def missing_timestamp(p):
    path='reviews/source01/SOURCE_BRIDGE_CHECKS.json'
    record=json.loads((p/path).read_text()); record.pop('checked_at_utc')
    (p/path).write_text(json.dumps(record,indent=2)+'\n'); source_refresh(p,path)
case('normalization requires recorded generated timestamp',missing_timestamp)

# Instrument subprocess boundaries in memory, preserving frozen runner bytes.
# The after-inventory safeguard must catch a write into the sealed parent.
with tempfile.TemporaryDirectory(prefix='immutability-',dir=OUT/'.cache') as d:
    root=Path(d)/'package'; shutil.copytree(SOURCE,root)
    harness="""import run_all\nfrom pathlib import Path\noriginal=run_all.subprocess.run\ndef wrapper(*a,**k):\n result=original(*a,**k)\n (run_all.ROOT/'README.md').write_bytes((run_all.ROOT/'README.md').read_bytes()+b'changed')\n return result\nrun_all.subprocess.run=wrapper\nrun_all.main()\n"""
    p=subprocess.run([sys.executable,'-c',harness],cwd=root,capture_output=True,text=True)
    if p.returncode==0 or 'Frozen payload changed during replay' not in p.stderr:
        raise RuntimeError('after-inventory did not catch parent mutation')
    results.append({'name':'write into sealed root during otherwise successful jobs','expected':'REJECT','actual':'REJECT','returncode':p.returncode,'diagnostic':p.stderr.splitlines()[-1]})

# Positive boundary control: every script/cwd is scratch-local; deliberate
# scratch-only writes are allowed, scratch directories are removed afterwards.
with tempfile.TemporaryDirectory(prefix='scratch-',dir=OUT/'.cache') as d:
    root=Path(d)/'package'; shutil.copytree(SOURCE,root)
    harness="""import run_all\nfrom pathlib import Path\noriginal=run_all.subprocess.run\nseen=[]\ndef wrapper(*a,**k):\n script=Path(a[0][1]).resolve(); cwd=Path(k['cwd']).resolve()\n assert script.parent==cwd\n assert any(q.startswith('.verify-') for q in script.parts)\n assert not script.is_relative_to(run_all.ROOT/'original')\n seen.append(str(script.relative_to(run_all.ROOT)))\n result=original(*a,**k)\n scratch=next(q for q in script.parents if q.name.startswith('.verify-'))\n (scratch/'scratch-only-sentinel').write_text('scratch only')\n return result\nrun_all.subprocess.run=wrapper\nrun_all.main()\nprint('SCRATCH_JOBS='+str(len(seen)))\nassert len(seen)==11\nassert not list(run_all.ROOT.glob('.verify-*'))\n"""
    p=subprocess.run([sys.executable,'-c',harness],cwd=root,capture_output=True,text=True)
    if p.returncode: raise RuntimeError(p.stderr)
    results.append({'name':'all 11 execution paths and working directories are disposable scratch','expected':'PASS','actual':'PASS','returncode':0,'diagnostic':p.stdout.splitlines()[-1]})

# Document the runner's explicitly allowed inventory exceptions. The data here
# is a harmless sentinel, not real private or account material.
def cache_exception(p):
    (p/'__pycache__').mkdir(exist_ok=True)
    (p/'__pycache__/arbitrary-sentinel.txt').write_text('unsealed exception sentinel')
case('documented __pycache__ directory is outside sealed inventory',cache_exception,expect_pass=True)

result={'status':'PASS','cases':results,'count':len(results),
        'limits':'Disposable mutations intentionally alter declared authority for selected tests. Seals are consistency controls, not an adversary-proof signature. __pycache__ and .venv are intentional whole-directory exceptions; unchanged means unchanged sealed inventory.'}
(OUT/'PACKAGE_NEGATIVE_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
