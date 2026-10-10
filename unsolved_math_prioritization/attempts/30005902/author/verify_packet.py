#!/usr/bin/env python3
"""Check exact packet inventory, optional external manifest pin, and math replay."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

FILES = {
    'DATASET_IDENTITY.json','PROOF.md','README.md','REPOSITORY_CHECKS.json',
    'RESEARCH_LOG.md','RESEARCH_RESULT.json','SOURCES.json','SOURCE_AUDIT.md',
    'readiness.json','results.json','verify_counterexample.py','verify_packet.py',
}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def sha(b):
    return hashlib.sha256(b).hexdigest()

def check(root, pin=None, replay=True):
    root = Path(root)
    require(root.is_dir() and not root.is_symlink(), 'Invalid root')
    paths = list(root.rglob('*'))
    require(all(p.is_file() and not p.is_symlink() for p in paths), 'Unexpected directory or symlink')
    require({p.relative_to(root).as_posix() for p in paths} == FILES | {'MANIFEST.json'}, 'Inventory mismatch')
    raw = (root/'MANIFEST.json').read_bytes()
    digest = sha(raw)
    if pin is not None:
        require(digest == pin, 'External manifest pin mismatch')
    m = json.loads(raw)
    require(set(m) == {'format','problem_id','files'}, 'Manifest schema')
    require(m['format'] == 1 and m['problem_id'] == '30005902', 'Manifest identity')
    require(set(m['files']) == FILES, 'Manifest file inventory')
    for name in sorted(FILES):
        require('/' not in name and '\\' not in name and name not in {'.','..'}, 'Unsafe filename')
        data = (root/name).read_bytes()
        require(m['files'][name] == {'bytes':len(data),'sha256':sha(data)}, 'File mismatch: '+name)
    disposition = json.loads((root/'RESEARCH_RESULT.json').read_bytes())
    require(disposition['review_status'] == 'independent_audit_pending', 'Historical author disposition altered')
    require(disposition['substantive_approaches_used'] == 1 and disposition['novelty_claim'] is False, 'Scope altered')
    if replay:
        p = subprocess.run([sys.executable,'-B',str(root/'verify_counterexample.py')],capture_output=True,check=True)
        require(p.stdout == (root/'results.json').read_bytes(), 'Result replay differs')
    return {'status':'PASS','packet_file_count':len(FILES)+1,'manifest_sha256':digest,
            'external_pin_checked':pin is not None,'mathematical_result_replayed':replay}

def negative_controls(root, pin):
    names=[]
    def trial(name, mutation):
        with tempfile.TemporaryDirectory(prefix='hopf-packet-control-') as d:
            copy=Path(d)/'packet';shutil.copytree(root,copy)
            mutation(copy)
            try: check(copy,pin,replay=False)
            except (ValueError,FileNotFoundError,json.JSONDecodeError): names.append(name)
            else: raise RuntimeError('False packet accepted: '+name)
    trial('changed_proof', lambda p:(p/'PROOF.md').write_bytes((p/'PROOF.md').read_bytes()+b'\nchanged'))
    trial('changed_math_result', lambda p:(p/'results.json').write_text('{}\n'))
    trial('changed_code', lambda p:(p/'verify_counterexample.py').write_text('pass\n'))
    trial('missing_file', lambda p:(p/'SOURCES.json').unlink())
    trial('extra_file', lambda p:(p/'extra.txt').write_text('extra'))
    trial('extra_directory', lambda p:(p/'extra').mkdir())
    def symlink(p):
        (p/'SOURCES.json').unlink();(p/'SOURCES.json').symlink_to('README.md')
    trial('symlink', symlink)
    def rebound(p):
        f=p/'PROOF.md';f.write_bytes(f.read_bytes()+b'\nchanged')
        m=json.loads((p/'MANIFEST.json').read_bytes())
        m['files']['PROOF.md']={'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())}
        (p/'MANIFEST.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
    trial('rebound_manifest_external_pin', rebound)
    return names

if __name__ == '__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--manifest-sha256');ap.add_argument('--negative-controls',action='store_true')
    args=ap.parse_args();root=Path(__file__).resolve().parent
    out=check(root,args.manifest_sha256)
    if args.negative_controls:
        out['rejected_negative_controls']=negative_controls(root,args.manifest_sha256 or out['manifest_sha256'])
    if args.manifest_sha256 is None:
        out['qualification']='Internal consistency only; compare the manifest digest with the separately supplied freeze receipt to authenticate frozen bytes.'
    print(json.dumps(out,indent=2,sort_keys=True))
