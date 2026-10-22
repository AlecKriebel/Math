#!/usr/bin/env python3
"""Replay and adversarial controls for this package, with no -O-disabled assertions."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit("Use a reviewed external bootstrap with python -I -S -B; startup is not isolated")
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parent
PAYLOAD={'REPORT.md','PUBLIC_METADATA.json','SOURCES.json','math_checks.py','verify.py','verify_corpora.py','audit_checks.py','VERIFICATION.json'}
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def manifest(path):
    files={p.name:{'bytes':len(p.read_bytes()),'sha256':sha(p.read_bytes())} for p in sorted(path.iterdir()) if p.name!='MANIFEST.json'}
    (path/'MANIFEST.json').write_text(json.dumps({'schema':'strict-flat-sha256-v1','files':files},sort_keys=True,indent=2)+'\n')
    return sha((path/'MANIFEST.json').read_bytes())
def run(path,pin,opt):
    return subprocess.run([sys.executable,'-I','-S','-B']+(['-O'] if opt else [])+[str(path/'verify.py'),'--root',str(path),'--manifest-sha256',pin],cwd='/tmp',capture_output=True,text=True,timeout=30)
def writable_copy(src,dst):
    shutil.copytree(src,dst)
    for p in dst.iterdir():p.chmod(0o644)
    return dst
p=argparse.ArgumentParser();p.add_argument('--manifest-sha256',required=True);a=p.parse_args()
need(sha((ROOT/'MANIFEST.json').read_bytes())==a.manifest_sha256,'External bootstrap manifest pin mismatch')
need({p.name for p in ROOT.iterdir()}==PAYLOAD|{'MANIFEST.json'},'Bootstrap inventory mismatch')
meta=json.loads((ROOT/'MANIFEST.json').read_text())
need(set(meta['files'])==PAYLOAD,'Bootstrap manifest inventory mismatch')
for p in ROOT.iterdir():
    st=p.lstat();need(stat.S_ISREG(st.st_mode) and st.st_nlink==1,'Bootstrap entry type')
for name in PAYLOAD:
    b=(ROOT/name).read_bytes();need(meta['files'][name]=={'bytes':len(b),'sha256':sha(b)},'Bootstrap payload pin mismatch '+name)
result={'schema':'unitary-package-replay-v1','pre_execution_code_pins':{k:meta['files'][k] for k in ['verify.py','audit_checks.py','math_checks.py','verify_corpora.py']},'replays':[],'semantic_controls':[],'integrity_controls':[],'scope':'Package and finite arithmetic controls; no analytic distinction theorem is proved.'}
for opt in [False,True]:
    r=run(ROOT,a.manifest_sha256,opt);need(r.returncode==0,r.stderr);result['replays'].append({'location':'original','optimized':opt,'result':json.loads(r.stdout)})
with tempfile.TemporaryDirectory(prefix='unitary distinction audit ') as td:
    t=Path(td);moved=writable_copy(ROOT,t/'relocated package')
    for opt in [False,True]:
        r=run(moved,a.manifest_sha256,opt);need(r.returncode==0,r.stderr);result['replays'].append({'location':'relocated','optimized':opt,'result':json.loads(r.stdout)})
    changes=[('wrong_local_field',['exact_target','extension_field'],'p_adic'),('wrong_subgroup',['exact_target','subgroup'],'GL_n(R)'),('conjugate_dual',['exact_target','symmetry'],'pi_tau_isomorphic_pi_dual'),('conjugate_exponent',['exact_target','parameter_conjugation'],'(k,s)->(-k,conjugate(s))'),('distinct_orbits_only',['exact_target','orbit_count'],'distinct_pairs_only'),('parity_added',['exact_target','extra_parity_restriction'],True),('full_solution',['full_resolution_claim'],True),('dimension_equality',['partial_results','formula_is_period_dimension'],True),('positive_bound_existence',['partial_results','positive_upper_bound_proves_distinction'],True),('toy_as_target_counterexample',['partial_results','quotient_example_is_target_counterexample'],True),('review_hash_wrong',['full_record_review','sha256'],'0'*64),('review_bytes_wrong',['full_record_review','bytes'],4194),('approach_count_wrong',['actual_substantive_approaches'],5)]
    for label,path,value in changes:
        dest=writable_copy(ROOT,t/label);j=json.loads((dest/'PUBLIC_METADATA.json').read_text());parent=j
        for key in path[:-1]:parent=parent[key]
        parent[path[-1]]=value;(dest/'PUBLIC_METADATA.json').write_text(json.dumps(j,indent=2,sort_keys=True)+'\n');pin=manifest(dest)
        for opt in [False,True]:
            r=run(dest,pin,opt);need(r.returncode!=0,'Semantic mutation accepted '+label)
        result['semantic_controls'].append({'name':label,'normal_rejected':True,'optimized_rejected':True,'manifest_recomputed':True})
    for label in ['extra_file','cache_directory','missing_file','symlink','fifo','hardlink','corrupt_payload','corrupt_manifest','duplicate_manifest_key','root_symlink']:
        dest=writable_copy(ROOT,t/label);pin=a.manifest_sha256
        if label=='extra_file':(dest/'unlisted').write_text('extra')
        elif label=='cache_directory':(dest/'__pycache__').mkdir()
        elif label=='missing_file':(dest/'REPORT.md').unlink()
        elif label=='symlink':(dest/'REPORT.md').unlink();(dest/'REPORT.md').symlink_to(ROOT/'REPORT.md')
        elif label=='fifo':(dest/'REPORT.md').unlink();os.mkfifo(dest/'REPORT.md')
        elif label=='hardlink':
            source=t/'hardlink_source';source.write_bytes((dest/'REPORT.md').read_bytes());(dest/'REPORT.md').unlink();os.link(source,dest/'REPORT.md')
        elif label=='corrupt_payload':(dest/'REPORT.md').write_text('changed')
        elif label=='corrupt_manifest':(dest/'MANIFEST.json').write_text('{}')
        elif label=='duplicate_manifest_key':
            raw=(dest/'MANIFEST.json').read_text();raw=raw.replace('{','{"schema":"strict-flat-sha256-v1",',1);(dest/'MANIFEST.json').write_text(raw);pin=sha(raw.encode())
        elif label=='root_symlink':
            link=t/'linked_root';link.symlink_to(dest,target_is_directory=True);dest=link
        for opt in [False,True]:
            r=run(dest,pin,opt);need(r.returncode!=0,'Integrity mutation accepted '+label)
        result['integrity_controls'].append({'name':label,'normal_rejected':True,'optimized_rejected':True})
print(json.dumps(result,indent=2,sort_keys=True))
