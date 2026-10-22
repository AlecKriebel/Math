#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

SAFE = Path(__file__).resolve().parent

def require(test, text):
    if not test:
        raise RuntimeError(text)

def h(b):
    return hashlib.sha256(b).hexdigest()

def manifest(p):
    files = {q.name: {'bytes': len(q.read_bytes()), 'sha256': h(q.read_bytes())}
             for q in sorted(p.iterdir()) if q.name != 'MANIFEST.json'}
    (p/'MANIFEST.json').write_text(json.dumps({'schema':'strict-flat-sha256-v1','files':files},indent=2,sort_keys=True)+'\n')
    return h((p/'MANIFEST.json').read_bytes())

def run(p, pin, optimized=False):
    args = [sys.executable, '-B'] + (['-O'] if optimized else [])
    return subprocess.run(args + [str(p/'verify.py'),'--manifest-sha256',pin],capture_output=True,text=True,cwd='/tmp',timeout=30)

parser = argparse.ArgumentParser(description="Replay package and semantic negative controls; does not prove the cited theorem.")
parser.add_argument('--manifest-sha256', required=True)
args = parser.parse_args()
require(h((SAFE/'MANIFEST.json').read_bytes()) == args.manifest_sha256, 'External manifest pin mismatch')
manifest_data=json.loads((SAFE/'MANIFEST.json').read_text())
for name in ['verify.py','audit_checks.py']:
    raw=(SAFE/name).read_bytes()
    require({'bytes':len(raw),'sha256':h(raw)} == manifest_data['files'][name], 'Code pin mismatch '+name)
results = {'schema':'dominating-digraph-package-checks-v1','date_utc':'2026-10-06',
           'scope':'Package integrity, exact metadata semantics and integer arithmetic only. The published theorem is externally cited, not computationally proved.',
           'pre_execution_code_pins':{n:manifest_data['files'][n] for n in ['verify.py','audit_checks.py']},
           'replays':[], 'semantic_controls':[], 'integrity_controls':[]}
for optimized in [False,True]:
    p=run(SAFE,h((SAFE/'MANIFEST.json').read_bytes()),optimized)
    require(p.returncode==0,p.stderr)
    results['replays'].append({'location':'original','optimized':optimized,'result':json.loads(p.stdout)})
with tempfile.TemporaryDirectory(prefix='dominating-digraph-replay-') as td:
    t = Path(td)
    moved = t/'relocated';shutil.copytree(SAFE,moved)
    for optimized in [False,True]:
        p=run(moved,h((moved/'MANIFEST.json').read_bytes()),optimized)
        require(p.returncode==0,p.stderr)
        results['replays'].append({'location':'relocated','optimized':optimized,'result':json.loads(p.stdout)})
    changes=[('girth_100','girth_lower_bound',100),('subset_limit_99','dominated_subset_limit',99),
             ('wrong_orientation','witness_orientation','u_to_v'),('exact_size_only','subset_quantifier','exactly'),
             ('infinite_only','finite',False),('tournament_only','graph_class','tournaments'),
             ('zero_length_power','power_minimum_walk_length',0),('off_by_one_base','base_girth_lower_bound',9900)]
    for label,key,value in changes:
        pth=t/label;shutil.copytree(SAFE,pth)
        m=json.loads((pth/'PUBLIC_METADATA.json').read_text());m['theorem_specialization'][key]=value
        (pth/'PUBLIC_METADATA.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
        pin=manifest(pth)
        for opt in [False,True]:
            p=run(pth,pin,opt);require(p.returncode!=0,'Semantic mutation accepted '+label)
        results['semantic_controls'].append({'name':label,'normal_rejected':True,'optimized_rejected':True,'manifest_recomputed':True})
    for label in ['extra_file','cache_directory','symlink','fifo','missing_file','corrupt_payload','corrupt_manifest','hard_link']:
        pth=t/label;shutil.copytree(SAFE,pth);pin=h((pth/'MANIFEST.json').read_bytes())
        if label=='extra_file':(pth/'unexpected.txt').write_text('unlisted')
        elif label=='cache_directory':(pth/'__pycache__').mkdir()
        elif label=='symlink':
            (pth/'REPORT.md').unlink();(pth/'REPORT.md').symlink_to(SAFE/'REPORT.md')
        elif label=='fifo':
            (pth/'REPORT.md').unlink();os.mkfifo(pth/'REPORT.md')
        elif label=='missing_file':(pth/'REPORT.md').unlink()
        elif label=='corrupt_payload':(pth/'REPORT.md').write_text('changed')
        elif label=='corrupt_manifest':(pth/'MANIFEST.json').write_text('{}\n')
        elif label=='hard_link':
            source=t/'extra-hardlink-source';source.write_bytes((pth/'REPORT.md').read_bytes())
            (pth/'REPORT.md').unlink();os.link(source,pth/'REPORT.md')
        for opt in [False,True]:
            p=run(pth,pin,opt);require(p.returncode!=0,'Integrity mutation accepted '+label)
        results['integrity_controls'].append({'name':label,'normal_rejected':True,'optimized_rejected':True})
print(json.dumps(results,indent=2,sort_keys=True))
