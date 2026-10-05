#!/usr/bin/env python3
"""Relocated clean replay and negative package controls, normal and optimized."""
import hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def need(v,m):
    if not v:raise RuntimeError('PUBLICATION CONTROL FAILURE: '+m)
def run(root,opt):
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env.pop('PYTHONPATH',None);env['PYTHONDONTWRITEBYTECODE']='1'
    return subprocess.run([sys.executable]+(['-O'] if opt else [])+[str(root/'verify_package.py')],cwd=root.parent,env=env,capture_output=True)
rows=[]
with tempfile.TemporaryDirectory(prefix='positive-braid-publication-') as d:
    base=Path(d);clean=base/'relocated';shutil.copytree(ROOT,clean,ignore=shutil.ignore_patterns('__pycache__'))
    outputs=[]
    for label,root in [('packet',ROOT),('relocated',clean)]:
        for opt in [False,True]:
            p=run(root,opt);need(p.returncode==0,label+' replay: '+p.stderr.decode(errors='replace'));outputs.append(p.stdout)
            rows.append({'test':label+'_replay','optimized':opt,'exit_code':0})
    need(all(x==outputs[0] for x in outputs),'normal optimized relocated bytes')
    for mutation in ['changed_proof','missing_result','unexpected_file','damaged_zip','unsafe_manifest']:
        target=base/mutation;shutil.copytree(clean,target)
        if mutation=='changed_proof':(target/'author/PROOF.md').write_bytes((target/'author/PROOF.md').read_bytes()+b'corruption\n')
        elif mutation=='missing_result':(target/'audit/independent_results.json').unlink()
        elif mutation=='unexpected_file':(target/'unlisted.txt').write_text('unexpected\n')
        elif mutation=='damaged_zip':
            z=next((target/'archives').glob('*.zip'));b=z.read_bytes();z.write_bytes(b[:15]+bytes([b[15]^1])+b[16:])
        else:
            m=target/'PUBLICATION_MANIFEST.json';j=json.loads(m.read_text());j['files'][0]['path']='../escape';m.write_text(json.dumps(j))
        for opt in [False,True]:
            p=run(target,opt);need(p.returncode!=0,'mutation accepted: '+mutation)
            rows.append({'test':mutation,'optimized':opt,'rejected':True})
print(json.dumps({'status':'pass','control_count':len(rows),'clean_outputs_byte_identical':True,'controls':rows},sort_keys=True,indent=2))
