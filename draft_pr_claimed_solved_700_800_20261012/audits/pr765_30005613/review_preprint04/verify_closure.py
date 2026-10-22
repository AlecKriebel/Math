"""Read-only authored closure; --current-inputs optionally checks live six bindings."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, stat

def need(c,m):
    if not c:raise SystemExit('FAIL: '+m)
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--current-inputs',action='store_true');args=ap.parse_args()
    root=Path(__file__).resolve().parent;mp=root/'MANIFEST.json';m=json.loads(mp.read_bytes());rows=m['files']
    names=[r['path'] for r in rows]
    need(len(names)==len(set(names))==m['file_count'],'manifest unique count')
    for n in names:
        need(isinstance(n,str) and n!='MANIFEST.json' and not PurePosixPath(n).is_absolute() and '\\' not in n and all(p not in ['', '.', '..'] for p in n.split('/')) and str(PurePosixPath(n))==n,'unsafe/self authored path')
    actual={};dirs=set()
    for p in root.rglob('*'):
        s=p.lstat();need(not stat.S_ISLNK(s.st_mode),'symlink '+str(p))
        if stat.S_ISDIR(s.st_mode):dirs.add(p.relative_to(root).as_posix())
        else:
            need(stat.S_ISREG(s.st_mode),'special '+str(p))
            if p!=mp:actual[p.relative_to(root).as_posix()]=identity(p.read_bytes())
    need(set(actual)==set(names),'exact recursive authored inventory, including hidden')
    need(dirs=={p.as_posix() for n in names for p in Path(n).parents if p.as_posix()!='.'},'unexpected empty directory')
    for row in rows:need(actual[row['path']]=={k:row[k] for k in ['bytes','sha256']},'bytes/hash '+row['path'])
    v=json.loads((root/'VERDICT.json').read_bytes());need(v['closed'] and v['audit_complete'],'verdict not closed')
    if args.current_inputs:
        before=json.loads((root/'CHECKED_INPUTS_BEFORE.json').read_bytes())['publication_six'];after=json.loads((root/'CHECKED_INPUTS_AFTER.json').read_bytes())['publication_six'];need(before==after,'before/after bindings differ')
        for n,item in before.items():need(identity((root.parent/'preprint'/n).read_bytes())==item,'current publication '+n)
    print(json.dumps({'status':'PASS','authored_files':len(rows),'current_inputs_checked':args.current_inputs,'manifest_sha256':identity(mp.read_bytes())['sha256'],'report_sha256':actual['REPORT.md']['sha256'],'verdict_sha256':actual['VERDICT.json']['sha256']},indent=2,sort_keys=True))

if __name__=='__main__':main()
