"""ROOT original-head readonly export; no scientific-helper execution."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import subprocess
A=Path(__file__).resolve().parent;R=A.parents[2]
HEAD='86be0f85c7a37a5cad8d24abd16a32d8d1f27e62';PREFIX='unsolved_math_prioritization/attempts/30004386/'
commands=[]
def run(argv):
    rec=dict(argv=argv,cwd=str(R),started_utc=dt.datetime.now(dt.timezone.utc).isoformat(),stdin_supplied=False)
    p=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate();i=len(commands)
    rec.update(pid=p.pid,actual_execution=True,completed=True,exit_code=p.returncode,finished_utc=dt.datetime.now(dt.timezone.utc).isoformat())
    for name,raw in [('stdout',out),('stderr',err)]:
        (A/'original_git_commands'/f'{i}.{name}').write_bytes(raw)
        rec[name]=dict(path=f'{i}.{name}',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
    commands.append(rec);assert p.returncode==0
    return out
def main():
    (A/'original_git_commands').mkdir();(A/'source_snapshot').mkdir()
    try:
        assert run(['git','branch','--show-current']).strip()==b'main'
        current=run(['git','rev-parse','HEAD']).decode().strip()
        assert run(['git','rev-parse','origin/pr43-review']).decode().strip()==HEAD
        base=run(['git','merge-base',current,HEAD]).decode().strip()
        tree=run(['git','ls-tree','-r','-z',HEAD,'--',PREFIX]).decode().split('\0');rows=[]
        for entry in filter(None,tree):
            fields,name=entry.split('\t');mode,kind,oid=fields.split();assert mode=='100644' and kind=='blob' and name.startswith(PREFIX)
            relative=name[len(PREFIX):];p=A/'source_snapshot'/relative;p.parent.mkdir(parents=True,exist_ok=True);raw=run(['git','show',HEAD+':'+name]);p.write_bytes(raw);p.chmod(0o444)
            rows.append(dict(path=relative,size=len(raw),sha256=hashlib.sha256(raw).hexdigest(),mode=mode,git_blob=oid))
        assert len(rows)==16
        changed=run(['git','diff','--name-only',base,HEAD]).decode().splitlines()
        assert set(changed)=={PREFIX+z['path'] for z in rows}|{'unsolved_math_prioritization/QUEUE.md'}
        patch=run(['git','diff',base,HEAD]);(A/'original_diff.patch').write_bytes(patch);(A/'original_diff.patch').chmod(0o444)
        record=dict(schema='pr43-root-readonly-original-snapshot/v1',utc=dt.datetime.now(dt.timezone.utc).isoformat(),pr=43,id=30004386,head=HEAD,base=base,main_at_export=current,files=rows,changed_paths=changed,diff_bytes=len(patch),diff_sha256=hashlib.sha256(patch).hexdigest(),scientific_helpers_executed=False,mathematical_review='PENDING',new_substantive_attempts=0,audit_turns=0)
        with (A/'snapshot_manifest.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
        (A/'snapshot_manifest.json').chmod(0o444)
        assert run(['git','rev-parse','HEAD']).decode().strip()==current
        print(json.dumps(dict(status='PASS_ORIGINAL_EXPORT_ONLY',members=len(rows),changed=len(changed),base=base,diff_bytes=len(patch),manifest_sha256=hashlib.sha256((A/'snapshot_manifest.json').read_bytes()).hexdigest())))
    finally:
        with (A/'ORIGINAL_GIT_COMMANDS.json').open('x') as f:json.dump(commands,f,indent=2);f.write('\n')
if __name__=='__main__':main()
