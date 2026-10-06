#!/usr/bin/env python3
"""Adversarial independent controls; mutations only occur in temporary copies."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile


def require(condition,message):
    if not condition:
        raise ValueError(message)


def rehash(root,name):
    p=root/name
    doc=json.loads(p.read_bytes())
    for row in doc['files']:
        b=(root/row['path']).read_bytes()
        row['bytes']=len(b)
        row['sha256']=hashlib.sha256(b).hexdigest()
    p.write_text(json.dumps(doc,indent=2,sort_keys=True)+'\n')


def replace(path,old,new):
    data=path.read_text()
    require(data.count(old)==1,'Expected unique mutation anchor')
    path.write_text(data.replace(old,new))


def main():
    source=Path(__file__).absolute().parent
    records=[]
    with tempfile.TemporaryDirectory(prefix='yamabe audit controls ') as td:
        temp=Path(td)
        counter=0
        def run(label,kind,mutate=None,diagnostic=None,accept=False):
            nonlocal counter
            for optimize in (False,True):
                counter+=1
                target=temp/f'case {counter}'
                shutil.copytree(source,target)
                root=target/'author' if kind=='author' else target
                if mutate:
                    mutate(root)
                # Always run the pristine trusted verifier, not a modified copy.
                verifier=source/('author/verify_bundle.py' if kind=='author' else 'verify_audit.py')
                command=[sys.executable,'-I','-B']+(['-O'] if optimize else [])+[str(verifier),'--root',str(root)]
                p=subprocess.run(command,cwd=temp,capture_output=True,text=True,timeout=60)
                require((p.returncode==0)==accept,'Wrong acceptance: '+label+' '+p.stderr)
                if diagnostic:
                    require(diagnostic in p.stderr,'Wrong rejection diagnostic: '+label+' '+p.stderr)
                records.append({'case':label,'verifier':kind,'optimized':optimize,
                  'accepted':p.returncode==0,'expected_acceptance':accept,
                  'diagnostic':'verified' if accept else diagnostic})
        run('relocation with spaces and foreign cwd','author',accept=True)
        run('relocation with spaces and foreign cwd','audit',accept=True)
        run('missing author proof','author',lambda r:(r/'PROOF.md').unlink(),'Strict inventory mismatch')
        run('extra regular file','author',lambda r:(r/'EXTRA').write_text('x'),'Strict inventory mismatch')
        run('injected bytecode directory','author',lambda r:(r/'__pycache__').mkdir(),'Strict inventory mismatch')
        def symlink(r):
            (r/'PROOF.md').unlink(); (r/'PROOF.md').symlink_to(source/'author/PROOF.md')
        run('symlink instead of proof','author',symlink,'Nonregular entry')
        def fifo(r):
            (r/'PROOF.md').unlink(); os.mkfifo(r/'PROOF.md')
        run('FIFO instead of proof','author',fifo,'Nonregular entry')
        def same_size(r):
            p=r/'PROOF.md'; data=p.read_bytes(); p.write_bytes(b'!'+data[1:])
        run('same-size authored proof corruption','author',same_size,'Hash mismatch')
        def short(r):
            replace(r/'certificate.py','L = 10000','L = 100'); rehash(r,'MANIFEST.json')
        run('short cylinder after rehash','author',short,'finite-cylinder strict separation')
        def tight(r):
            replace(r/'certificate.py','ROUND_BOUND = Q(129, 200)','ROUND_BOUND = Q(3, 5)'); rehash(r,'MANIFEST.json')
        run('false round threshold after rehash','author',tight,'round interval')
        def bad_result(r):
            doc=json.loads((r/'RESULTS.json').read_text()); doc['checks']=612
            (r/'RESULTS.json').write_text(json.dumps(doc,indent=2,sort_keys=True)+'\n'); rehash(r,'MANIFEST.json')
        run('wrong author output after rehash','author',bad_result,'Reproduced result differs')
        run('audit cache rejected','audit',lambda r:(r/'__pycache__').mkdir(),'Root strict inventory mismatch')
        def afifo(r):
            (r/'AUDIT.md').unlink(); os.mkfifo(r/'AUDIT.md')
        run('audit FIFO rejected before reads','audit',afifo,'Root nonregular entry')
        def out(r):
            doc=json.loads((r/'INDEPENDENT_RESULTS.json').read_text()); doc['grid_cells']=199
            (r/'INDEPENDENT_RESULTS.json').write_text(json.dumps(doc,indent=2,sort_keys=True)+'\n'); rehash(r,'AUDIT_MANIFEST.json')
        run('wrong independent output after rehash','audit',out,'Independent output mismatch')
        def semantic(r):
            replace(r/'independent_certificate.py','LENGTH = 10000','LENGTH = 100'); rehash(r,'AUDIT_MANIFEST.json')
        run('independent short-cylinder rejection after rehash','audit',semantic,'strict cylinder separation')
        def tighter(r):
            replace(r/'independent_certificate.py','ROUND_LIMIT = F(129, 200)','ROUND_LIMIT = F(3, 5)'); rehash(r,'AUDIT_MANIFEST.json')
        run('independent false round bound after rehash','audit',tighter,'round interval bound')
        def frozen(r):
            p=r/'author/MANIFEST.json'; p.write_bytes(p.read_bytes()+b' '); rehash(r,'AUDIT_MANIFEST.json')
        run('changed frozen author manifest after outer rehash','audit',frozen,'Frozen author manifest mismatch')
    return {'controls':records,'total':len(records),'passes':len(records),
      'accepted_baselines':sum(x['accepted'] for x in records),
      'expected_rejections':sum(not x['accepted'] for x in records),
      'all_optimization_modes_checked':True,'mutations_confined_to_temporary_copies':True}


if __name__=='__main__':
    require(len(sys.argv)==1,'No arguments accepted')
    print(json.dumps(main(),indent=2,sort_keys=True))
