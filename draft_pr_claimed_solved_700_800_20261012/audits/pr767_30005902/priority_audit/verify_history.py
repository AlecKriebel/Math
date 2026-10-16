#!/usr/bin/env python3
"""Read-only exact recursive authored-history and arithmetic replay verification."""
import hashlib,json,os,stat,subprocess,sys
from pathlib import Path
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def inventory(root):
    files={}
    for parent,dirs,names in os.walk(root,followlinks=False):
        need(bool(dirs or names),'empty directory: '+str(parent))
        for name in dirs+names:
            q=Path(parent)/name;s=q.lstat().st_mode
            need(stat.S_ISREG(s) or stat.S_ISDIR(s),'symlink or special node: '+str(q))
        for name in names:
            q=Path(parent)/name;rel=q.relative_to(root).as_posix()
            if rel=='MANIFEST.json':continue
            b=q.read_bytes();files[rel]={'bytes':len(b),'sha256':sha(b)}
    return files
def main():
    root=Path(__file__).resolve().parent;raw=(root/'MANIFEST.json').read_bytes();m=json.loads(raw)
    got=inventory(root);need(got==m['files'],'exact authored inventory/digest mismatch')
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');replays=[]
    for script,expected in [('verify_implications.py','implication_results.json'),('adversary/check_heisenberg.py','adversary/CHECK_RESULTS.json')]:
        target=(root/expected).read_bytes()
        for optimized in (False,True):
            args=[sys.executable]+(['-O'] if optimized else [])+[str(root/script)]
            r=subprocess.run(args,capture_output=True,env=env)
            need(r.returncode==0,'replay failed: '+r.stderr.decode())
            need(r.stdout==target,'replay bytes differ: '+script)
            replays.append({'script':script,'mode':'optimized' if optimized else 'normal','sha256':sha(target)})
    for rel,h in json.loads((root/'INDEPENDENT_CHECKPOINT.json').read_bytes())['files'].items():
        need(sha((root/rel).read_bytes())==h,'independent checkpoint changed: '+rel)
    v=json.loads((root/'VERDICT.json').read_bytes())
    need(v['status']=='FAIL_NEW_RESOLUTION_PRIORITY_FOR_ORIGINAL_UNRESTRICTED_QUESTION','unexpected verdict')
    need(bool(v['blocking_priority_issues']) and bool(v['known_full_predecessors']),'missing supported priority issue')
    need(v['decision_action_executed'] is False,'unauthorized action state')
    return {'status':'PASS','scope':'authored history only; adjacent current inputs separate',
      'regular_authored_files_excluding_manifest':len(got),'total_bytes_excluding_manifest':sum(x['bytes'] for x in got.values()),
      'manifest_sha256':sha(raw),'replays':replays}
if __name__=='__main__':print(json.dumps(main(),sort_keys=True,indent=2))
