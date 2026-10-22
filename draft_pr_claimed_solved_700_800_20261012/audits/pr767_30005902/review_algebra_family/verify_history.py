#!/usr/bin/env python3
"""Read-only closure of this family's authored history; no adjacent inputs."""
import hashlib,json,os,stat,subprocess,sys
from pathlib import Path
def need(ok,msg):
    if not ok: raise RuntimeError(msg)
def digest(data): return hashlib.sha256(data).hexdigest()
def main():
    root=Path(__file__).resolve().parent
    mpath=root/'MANIFEST.json'; raw=mpath.read_bytes(); m=json.loads(raw)
    got={}
    for parent,dirs,files in os.walk(root,followlinks=False):
        need(bool(dirs or files),'empty directory: '+parent)
        for name in dirs+files:
            p=Path(parent)/name; mode=p.lstat().st_mode
            need(stat.S_ISDIR(mode) or stat.S_ISREG(mode),'symlink or special node: '+str(p))
        for name in files:
            p=Path(parent)/name; rel=p.relative_to(root).as_posix()
            if rel!='MANIFEST.json':
                data=p.read_bytes();got[rel]={'bytes':len(data),'sha256':digest(data)}
    need(got==m['files'],'recursive exact authored inventory/digests differ')
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    expected=(root/'independent_results.json').read_bytes()
    modes=[]
    for optimized in (False,True):
        args=[sys.executable]+(['-O'] if optimized else [])+[str(root/'verify_algebra.py')]
        p=subprocess.run(args,capture_output=True,env=env)
        need(p.returncode==0,'finite replay failed: '+p.stderr.decode())
        need(p.stdout==expected,'finite replay bytes differ')
        modes.append('optimized' if optimized else 'normal')
    for name,sha in json.loads((root/'INDEPENDENT_CHECKPOINT.json').read_bytes())['files'].items():
        need(digest((root/name).read_bytes())==sha,'independent pre-history checkpoint changed: '+name)
    verdict=json.loads((root/'VERDICT.json').read_bytes())
    need(verdict['issue_count']==0 and not verdict['required_repairs'] and not verdict['remaining_central_gaps'],'verdict inconsistency')
    return {'status':'PASS','scope':'authored history only; current adjacent inputs checked separately',
      'regular_authored_files_excluding_manifest':len(got),'total_bytes_excluding_manifest':sum(v['bytes'] for v in got.values()),
      'finite_replay_modes':modes,'replay_sha256':digest(expected),'manifest_sha256':digest(raw)}
if __name__=='__main__': print(json.dumps(main(),sort_keys=True,indent=2))
