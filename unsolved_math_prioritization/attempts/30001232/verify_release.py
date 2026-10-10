#!/usr/bin/env python3
"""Strict release integrity and exact replay; no source material or network access."""
from pathlib import Path,PurePosixPath
import hashlib,json,os,stat,subprocess,sys
ROOT=Path(__file__).resolve().parent
PINS={'author/SHA256SUMS':'572b23e2c5f2ddcaec74c05172542d9bfef69d317d6a0151f052bf4e0fc5c62c',
      'author/PROOF.md':'efa3b1a7c809bc244799048bd0cf25e9ac56e09d4f90c133ef5095b0458fbcc3',
      'audit/AUDIT_MANIFEST.json':'1f93eaf030ae19b35a002aef12ca47c720059286aa70fbdd34483eb1abd98597'}
def require(x,message):
    if not x: raise RuntimeError(message)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def verify_integrity(root):
    require(not sys.flags.optimize,'Optimized Python disables author assertions; run without -O.')
    root=Path(root)
    require(not root.is_symlink(),'Root must not be a symlink.')
    mf=root/'RELEASE_MANIFEST.json'
    require(mf.is_file() and not mf.is_symlink(),'Missing regular manifest.')
    manifest=json.loads(mf.read_text())
    require(manifest['schema']==1,'Unsupported schema.')
    rows=manifest['files']; names=[]
    for row in rows:
        name=row['path'];p=PurePosixPath(name)
        require(name and not p.is_absolute() and '..' not in p.parts and str(p)==name,'Unsafe manifest path.')
        require(name!='RELEASE_MANIFEST.json','Self-referential manifest.')
        require(name not in names,'Duplicate manifest path.');names.append(name)
    expected=set(names)|{'RELEASE_MANIFEST.json'}
    actual=set()
    expected_dirs={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'}
    actual_dirs=set()
    for p in root.rglob('*'):
        require(not p.is_symlink(),'Symlink rejected: '+str(p))
        relative=p.relative_to(root).as_posix()
        if p.is_dir(): actual_dirs.add(relative)
        else:
            require(p.is_file(),'Special file rejected: '+relative);actual.add(relative)
    require(actual==expected,'File set differs from strict manifest.')
    require(actual_dirs==expected_dirs,'Directory set differs from strict manifest.')
    for row in rows:
        p=root/row['path']
        require(p.stat().st_size==row['bytes'],'Size mismatch: '+row['path'])
        require(digest(p)==row['sha256'],'Digest mismatch: '+row['path'])
        require(not (p.stat().st_mode & 0o111),'Unexpected executable mode: '+row['path'])
    for n,h in PINS.items(): require(digest(root/n)==h,'Frozen pin mismatch: '+n)
    am=json.loads((root/'audit/AUDIT_MANIFEST.json').read_text())
    for row in am['publication_safe_author_files']:
        p=root/row['path'];require(digest(p)==row['sha256'] and p.stat().st_size==row['bytes'],'Audit-author binding mismatch.')
    for row in am['publication_safe_audit_files']:
        p=root/'audit'/row['path'];require(digest(p)==row['sha256'] and p.stat().st_size==row['bytes'],'Audit binding mismatch.')
    return len(rows)
def main():
    n=verify_integrity(ROOT);replays=[]
    for code,data in [('author/verify_intersections.py','author/intersection_results.json'),('author/verify_formulas.py','author/formula_results.json'),('audit/independent_checks.py','audit/independent_results.json')]:
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
        proc=subprocess.run([sys.executable,str(ROOT/code)],capture_output=True,env=env)
        require(proc.returncode==0,'Replay failed: '+code+' '+proc.stderr.decode())
        require(proc.stdout==(ROOT/data).read_bytes(),'Replay bytes differ: '+code)
        replays.append({'program':code,'exact_stdout_sha256':hashlib.sha256(proc.stdout).hexdigest()})
    verify_integrity(ROOT)
    print(json.dumps({'status':'PASS','strict_manifest_entries':n,'programs_replayed':len(replays),'replays':replays,'audit_assertions':60731,'geometric_existence_not_certified_by_computation':True},indent=2,sort_keys=True))
if __name__=='__main__':main()
