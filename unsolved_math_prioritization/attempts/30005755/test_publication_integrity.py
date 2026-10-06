#!/usr/bin/env python3
"""Mutation controls without publishing queue snapshots or external inputs."""
from pathlib import Path
import importlib.util,json,shutil,subprocess,sys,tempfile
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('publication_verifier',ROOT/'verify_publication.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
def rejected(action,label):
    try:action()
    except (RuntimeError,FileNotFoundError,ValueError):return
    raise RuntimeError('Negative control accepted: '+label)
v.verify(ROOT)
with tempfile.TemporaryDirectory(prefix='tf-cones-integrity-') as td:
    temp=Path(td)
    for label in ['changed_file','missing_file','extra_file','changed_archive','symlink']:
        root=temp/label;shutil.copytree(ROOT,root)
        if label=='changed_file':
            p=root/'author/PROOF.md';p.write_bytes(p.read_bytes()+b'\nmutation\n')
        elif label=='missing_file':(root/'audit/CLARIFICATIONS.md').unlink()
        elif label=='extra_file':(root/'unexpected.txt').write_text('extra')
        elif label=='symlink':(root/'link').symlink_to(root/'README.md')
        else:
            p=next((root/'frozen_archives').glob('*AUTHOR*.zip'));b=bytearray(p.read_bytes());b[100]^=1;p.write_bytes(b)
        rejected(lambda:v.verify(root),label)
    # Check that the frozen assertion-based arithmetic checkers reject mutations.
    for label,script,result in [('author','author/verification.py','author/expected_results.json'),('audit','audit/audit_checks.py','audit/AUDIT_RESULTS.json')]:
        p=temp/(label+'_invalid.json');data=json.loads((ROOT/result).read_text());data['mutation']=True;p.write_text(json.dumps(data))
        r=subprocess.run([sys.executable,'-E','-B',str(ROOT/script),'--check',str(p)],capture_output=True)
        v.require(r.returncode!=0,'Arithmetic checker accepted changed expectations')
    qroot=temp/'synthetic';qroot.mkdir()
    old=b'| 801 | 30005755 / OWR-14298157-005 | title | 0.1 | 5.5 | 3 | 2024 | queued | 0/5 |  |  |  |\n'
    c=old.split(b'|');c[8]=b' unsolved ';c[9]=b' 5/5 ';new=b'|'.join(c)
    base=b'stale header\n'+old+b'untouched tail\n';updated=b'stale header\n'+new+b'untouched tail\n'
    d={'base':v.identity(base),'updated':v.identity(updated),'row_line_1_based':2};bp=temp/'base';up=temp/'updated';bp.write_bytes(base);up.write_bytes(updated);(qroot/'QUEUE_DELTA.json').write_text(json.dumps(d));v.verify_queue(qroot,bp,up)
    changed=updated.replace(b'untouched tail',b'edited tail');up.write_bytes(changed);d['updated']=v.identity(changed);(qroot/'QUEUE_DELTA.json').write_text(json.dumps(d));rejected(lambda:v.verify_queue(qroot,bp,up),'unrelated queue edit with recomputed hash')
    r=subprocess.run([sys.executable,'-E','-B','-O',str(ROOT/'verify_publication.py')],capture_output=True);v.require(r.returncode!=0,'Optimized-mode guard failed')
print(json.dumps({'status':'PASS','negative_controls':9,'payload_mutations_rejected':5,'arithmetic_expectation_mutations_rejected':2,'unrelated_queue_edit_rejected':True,'optimized_mode_rejected':True},sort_keys=True))
