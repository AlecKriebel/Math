#!/usr/bin/env python3
"""Bounded rejection controls for verify_packet.py; no mathematical assertions."""
import hashlib,json,pathlib,shutil,subprocess,sys,tempfile
root=pathlib.Path(__file__).resolve().parent
pin=hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest()
cases=['missing','extra_file','extra_dir','altered_proof','symlink','manifest_rebind','duplicate_json','unsafe_name','wrong_size_type']
positive=negative=0
with tempfile.TemporaryDirectory(prefix='knot-integrity-controls-') as td:
    base=pathlib.Path(td)
    for optimized in (False,True):
        for case in ['baseline']+cases:
            loc=base/('opt_' if optimized else 'normal_')/case
            shutil.copytree(root,loc)
            chosen_pin=pin
            if case=='missing':(loc/'PROOF.md').unlink()
            elif case=='extra_file':(loc/'unlisted.txt').write_text('extra')
            elif case=='extra_dir':(loc/'unlisted').mkdir()
            elif case=='altered_proof':(loc/'PROOF.md').write_bytes((loc/'PROOF.md').read_bytes()+b'\nchanged')
            elif case=='symlink':
                (loc/'PROOF.md').unlink();(loc/'PROOF.md').symlink_to(root/'PROOF.md')
            elif case=='manifest_rebind':
                d=json.loads((loc/'MANIFEST.json').read_text());b=(loc/'PROOF.md').read_bytes()+b'\nchanged';(loc/'PROOF.md').write_bytes(b)
                d['files']['PROOF.md']={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()};(loc/'MANIFEST.json').write_text(json.dumps(d))
            elif case in ('duplicate_json','unsafe_name','wrong_size_type'):
                d=json.loads((loc/'MANIFEST.json').read_text())
                if case=='duplicate_json':raw=json.dumps(d)[:-1]+',"schema":1}'
                elif case=='unsafe_name':d['files']['../escape']=d['files']['PROOF.md'];raw=json.dumps(d)
                else:d['files']['PROOF.md']['bytes']=True;raw=json.dumps(d)
                (loc/'MANIFEST.json').write_text(raw)
                # These test schema validation after a caller intentionally pins
                # the malformed inventory, separately from external-pin controls.
                chosen_pin=hashlib.sha256((loc/'MANIFEST.json').read_bytes()).hexdigest()
            args=[sys.executable,'-I','-S','-B']+(['-O'] if optimized else [])+[str(loc/'verify_packet.py'),'--manifest-sha256',chosen_pin]
            out=subprocess.run(args,cwd=base,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
            if case=='baseline':
                if out.returncode:raise RuntimeError('baseline rejected: '+out.stderr.decode())
                positive+=1
            else:
                if out.returncode==0:raise RuntimeError('mutation accepted: '+case)
                negative+=1
print(json.dumps({'positive_runs':positive,'rejected_runs':negative,'cases':cases,'scope':'closed-inventory/hash/schema/replay controls only'},sort_keys=True))
