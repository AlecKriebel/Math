#!/usr/bin/env python3
"""Reject adversarial manifest fixtures without changing either real freeze."""
from pathlib import Path
import contextlib,hashlib,io,json,runpy,tempfile
with contextlib.redirect_stdout(io.StringIO()):
    check=runpy.run_path(str(Path(__file__).with_name('verify_integrity.py')))['check']
results=[]
with tempfile.TemporaryDirectory() as d:
    root=Path(d)
    def reset():
        for p in sorted(root.rglob('*'),reverse=True):
            if p.is_symlink() or p.is_file():p.unlink()
            else:p.rmdir()
        b=b'harmless fixture\n';(root/'payload.txt').write_bytes(b)
        (root/'MANIFEST.json').write_text(json.dumps({'files':[{'path':'payload.txt','bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}]}))
    def rejected(label,mutate):
        reset();mutate()
        try:check(root)
        except (ValueError,FileNotFoundError):results.append({'mutation':label,'rejected':True})
        else:raise RuntimeError('Accepted mutation: '+label)
    reset();check(root)
    rejected('modified payload',lambda:(root/'payload.txt').write_text('changed'))
    rejected('missing payload',lambda:(root/'payload.txt').unlink())
    def nested():
        (root/'nested').mkdir();(root/'nested'/'MANIFEST.json').write_text('{}')
    rejected('unlisted nested manifest',nested)
    def duplicate():
        p=root/'MANIFEST.json';m=json.loads(p.read_text());m['files']*=2;p.write_text(json.dumps(m))
    rejected('duplicate manifest path',duplicate)
    def link():
        (root/'copy.txt').write_bytes((root/'payload.txt').read_bytes())
        (root/'payload.txt').unlink();(root/'payload.txt').symlink_to('copy.txt')
    rejected('payload symlink',link)
    def escape():
        p=root/'MANIFEST.json';m=json.loads(p.read_text());m['files'][0]['path']='../payload.txt';p.write_text(json.dumps(m))
    rejected('parent traversal',escape)
print(json.dumps({'status':'PASS','valid_fixture_accepted':True,'controls':results},indent=2,sort_keys=True))
