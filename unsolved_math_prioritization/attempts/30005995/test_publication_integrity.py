#!/usr/bin/env python3
"""Negative controls on disposable copies only; frozen publication bytes remain unchanged."""
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
with tempfile.TemporaryDirectory(prefix='monotone-gradient-integrity-') as td:
    temp=Path(td)
    for label in ['changed_file','missing_file','extra_file','changed_archive','symlink']:
        root=temp/label;shutil.copytree(ROOT,root)
        if label=='changed_file':
            p=root/'author/CHECK_RESULTS.json';p.write_bytes(p.read_bytes()+b' ')
        elif label=='missing_file':(root/'audit/MATHEMATICAL_ADDENDUM.md').unlink()
        elif label=='extra_file':(root/'unexpected.txt').write_text('extra')
        elif label=='symlink':(root/'link').symlink_to(root/'README.md')
        else:
            p=next((root/'frozen_archives').glob('*AUTHOR*.zip'));b=bytearray(p.read_bytes());b[100]^=1;p.write_bytes(b)
        rejected(lambda:v.verify(root),label)
    for label,script,old,new in [('author','author/checks.py','value == formula','value != formula'),('audit','audit/independent_checks.py','actual==expected','actual!=expected')]:
        s=(ROOT/script).read_text();v.require(s.count(old)==1,'Mutation target not unique');p=temp/(label+'_mutant.py');p.write_text(s.replace(old,new))
        for optimized in (False,True):
            args=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(p)]
            r=subprocess.run(args,capture_output=True)
            v.require(r.returncode!=0 and b'AssertionError' in r.stderr,'Arithmetic mutation accepted')
    qroot=temp/'synthetic';qroot.mkdir()
    old=b'| 803 | 30005995 / OWR-14298587-010 | title | 0.1 | 5.5 | 3 | 2024 | queued | 0/5 |  |  |  |\r\n'
    c=old.split(b'|');c[8]=b' unsolved ';c[9]=b' 5/5 ';new=b'|'.join(c)
    base=b'stale header\r\n'+old+b'untouched tail\n';updated=b'stale header\r\n'+new+b'untouched tail\n'
    d={'base':v.identity(base),'updated':v.identity(updated),'row_line_1_based':2};bp=temp/'base';up=temp/'updated';bp.write_bytes(base);up.write_bytes(updated);(qroot/'QUEUE_DELTA.json').write_text(json.dumps(d));v.verify_queue(qroot,bp,up)
    changed=updated.replace(b'untouched tail',b'edited tail');up.write_bytes(changed);d['updated']=v.identity(changed);(qroot/'QUEUE_DELTA.json').write_text(json.dumps(d));rejected(lambda:v.verify_queue(qroot,bp,up),'unrelated queue edit with recomputed hash')
print(json.dumps({'status':'PASS','negative_controls':10,'payload_mutations_rejected':5,'arithmetic_mutations_rejected':4,'arithmetic_optimized_mode_covered':True,'unrelated_queue_edit_rejected':True},sort_keys=True))
