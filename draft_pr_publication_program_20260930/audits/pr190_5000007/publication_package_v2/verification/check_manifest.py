"""Validate exact package membership and byte hashes; no mathematical proof claim."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
def require(ok,msg):
    if not ok:raise ValueError(msg)
def main():
    m=json.loads((ROOT/'MANIFEST.json').read_text());files=m['files']
    require(isinstance(files,dict) and files,'Empty manifest')
    observed=set()
    for p in ROOT.rglob('*'):
        require(not p.is_symlink(),'Symlink in package')
        if p.is_file():observed.add(p.relative_to(ROOT).as_posix())
    require(observed==set(files)|{'MANIFEST.json'},'Missing or unexpected package file')
    for name,x in files.items():
        q=Path(name);require(not q.is_absolute() and '..' not in q.parts,'Unsafe manifest path')
        b=(ROOT/q).read_bytes();require(len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],'Package bytes changed: '+name)
    return {'status':'PASS','verified_payloads':len(files),'limits':'Exact artifact identity is not proof of mathematical truth, priority or peer review.'}
if __name__=='__main__':print(json.dumps(main(),indent=2))
