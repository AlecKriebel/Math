"""Read-only verification of this closed review and its six frozen inputs."""
from pathlib import Path
import hashlib,json,stat
ROOT=Path(__file__).resolve().parent
def require(v,m):
    if not v:raise ValueError(m)
def identity(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
    m=json.loads((ROOT/'MANIFEST.json').read_bytes());listed={}
    for row in m['authored_files']:
        name=row['path'];parts=name.split('/')
        require(name and not name.startswith('/') and '\\' not in name and all(x not in ('','.','..') for x in parts),'unsafe review name')
        require(name not in listed and name!='MANIFEST.json','duplicate/self review name')
        listed[name]={k:row[k] for k in ('bytes','sha256')}
    actual={};dirs=set()
    for p in ROOT.rglob('*'):
        require(not p.is_symlink(),'symlink review')
        if p.is_dir():dirs.add(p.relative_to(ROOT).as_posix());continue
        require(stat.S_ISREG(p.stat().st_mode),'special review')
        actual[p.relative_to(ROOT).as_posix()]=identity(p)
    require(set(actual)==set(listed)|{'MANIFEST.json'},'review set')
    require(all(actual[n]==e for n,e in listed.items()),'review bytes')
    expected_dirs={x.as_posix() for name in actual for x in Path(name).parents if x.as_posix()!='.'}
    require(dirs==expected_dirs,'empty or unlisted review directory')
    checked=json.loads((ROOT/'CHECKED_INPUTS.json').read_bytes());inputs=Path(checked['root'])
    for row in checked['files']:
        require(identity(inputs/row['path'])=={k:row[k] for k in ('bytes','sha256')},'frozen input changed '+row['path'])
    print(json.dumps({'status':'PASS','review_files_excluding_manifest':len(listed),'six_frozen_inputs_match':True,'closed_at_utc':m['closed_at_utc']},indent=2))
if __name__=='__main__':main()
