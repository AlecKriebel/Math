"""Explicit-guard, exact-inventory verification; works under python -O."""
import hashlib,json,os,stat,subprocess,sys
from pathlib import Path,PurePosixPath
EXPECTED={'README.md','SOURCE_ANALYSIS.md','PROOF_AUDIT.md','PUBLIC_SOURCE_METADATA.json','EDITORIAL_TRANSFORM.md','finite_regression.py','regression_output.json','verify.py'}

def require(ok,msg):
    if not ok:
        raise ValueError(msg)

def unique_pairs(pairs):
    d={}
    for k,v in pairs:
        require(k not in d,'duplicate JSON key')
        d[k]=v
    return d

def read_json(p):
    return json.loads(p.read_text(),object_pairs_hook=unique_pairs)

def main():
    root=Path(__file__).absolute().parent
    require(not root.is_symlink(),'symlink package root')
    found=set()
    for base,dirs,files in os.walk(root,followlinks=False):
        for name in dirs+files:
            path=Path(base)/name
            require(not path.is_symlink(),'symlink inventory entry')
            require(stat.S_ISREG(path.lstat().st_mode),'non-file inventory entry')
            found.add(path.relative_to(root).as_posix())
    require(found==EXPECTED|{'MANIFEST.json'},'unexpected or missing inventory entry')
    manifest=read_json(root/'MANIFEST.json')
    require(set(manifest)=={'schema','files'} and manifest['schema']==1,'manifest schema')
    entries=manifest['files']; require(isinstance(entries,dict),'manifest files type')
    for name,entry in entries.items():
        q=PurePosixPath(name)
        require(not q.is_absolute() and len(q.parts)==1 and '..' not in q.parts and '\\' not in name,'unsafe manifest path')
        require(name in EXPECTED,'manifest path not allowed')
        require(isinstance(entry,dict) and set(entry)=={'bytes','sha256'},'entry schema')
        data=(root/name).read_bytes()
        require(type(entry['bytes']) is int and entry['bytes']==len(data),'byte count mismatch: '+name)
        require(entry['sha256']==hashlib.sha256(data).hexdigest(),'hash mismatch: '+name)
    require(set(entries)==EXPECTED,'manifest inventory mismatch')
    m=read_json(root/'PUBLIC_SOURCE_METADATA.json')
    require(m['id']==20000012 and m['queue_rank']==1857 and m['turns']=='1/5','identity or turns')
    require(m['gate']=='already_solved_original_broad_existence_only','scope gate')
    h=m['sources'][2]
    require(h['inspected_version']=='v3' and h['inspected_version_date']=='2026-09-17','Han version')
    require(h['bytes']==436161 and h['sha256']=='7ce5d9eba6e8693da2c75915f5c2282217869ca830b1c97cf79ad9c8c3ec5555','Han artifact')
    for mode in ([],['-O']):
        proc=subprocess.run([sys.executable,*mode,'-B',str(root/'finite_regression.py')],cwd=root,capture_output=True,timeout=30)
        require(proc.returncode==0,'regression failure')
        require(proc.stderr==b'','unexpected regression stderr')
        require(proc.stdout==(root/'regression_output.json').read_bytes(),'complete regression output mismatch')
    print('PASS: exact inventory, hashes, scoped metadata, full normal/-O finite regression replay; no general-proof computational certification.')

if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print('FAIL: '+str(exc),file=sys.stderr)
        sys.exit(1)
