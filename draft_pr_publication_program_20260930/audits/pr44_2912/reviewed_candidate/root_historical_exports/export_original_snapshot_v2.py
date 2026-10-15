"""ROOT read-only original PR44 export; execute no scientific helper."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import subprocess
import os

A = Path(__file__).resolve().parent
R = A.parents[2]
HEAD = 'c772dc5b851ec91da9d46d534577609e5d3ca389'
PREFIX = 'unsolved_math_prioritization/attempts/2912/'
commands = []


def run(*args):
    assert args[0] in ['branch','rev-parse','merge-base','ls-tree','show','diff']
    rec = {'argv':['git',*args], 'cwd':str(R), 'started_utc':dt.datetime.now(dt.timezone.utc).isoformat(), 'stdin_supplied':False}
    p = subprocess.Popen(rec['argv'],cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
    out,err = p.communicate(); index = len(commands)
    rec.update(pid=p.pid,actual_execution=True,completed=True,exit_code=p.returncode,finished_utc=dt.datetime.now(dt.timezone.utc).isoformat())
    for channel,raw in [('stdout',out),('stderr',err)]:
        name=str(index)+'.'+channel
        (A/'original_git_commands_v2'/name).write_bytes(raw)
        rec[channel]={'path':name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
    commands.append(rec)
    assert p.returncode == 0 and not err
    return out


def main():
    assert __debug__
    (A/'original_git_commands_v2').mkdir(); (A/'source_snapshot_v2').mkdir()
    source=Path(__file__).read_bytes()
    (A/'PRELAUNCH_EXPORT_SOURCE_V2.py').write_bytes(source)
    try:
        assert run('branch','--show-current').strip()==b'main'
        current=run('rev-parse','HEAD').decode().strip()
        assert run('rev-parse',HEAD).decode().strip()==HEAD
        base=run('merge-base',current,HEAD).decode().strip()
        tree=run('ls-tree','-r','-z',HEAD,'--',PREFIX).decode().split('\0')
        rows=[]
        for entry in filter(None,tree):
            fields,name=entry.split('\t');mode,kind,oid=fields.split()
            assert mode=='100644' and kind=='blob' and name.startswith(PREFIX)
            relative=name[len(PREFIX):]; path=A/'source_snapshot_v2'/relative
            path.parent.mkdir(parents=True,exist_ok=True)
            raw=run('show',HEAD+':'+name);path.write_bytes(raw);path.chmod(0o444)
            rows.append({'path':relative,'size':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'mode':mode,'git_blob':oid})
        assert rows and {'OBSTRUCTION.md','source_record.json','turns.jsonl'}.issubset({row['path']for row in rows})
        changed=run('diff','--name-only',base,HEAD).decode().splitlines()
        assert set(changed)=={PREFIX+row['path']for row in rows}|{'unsolved_math_prioritization/QUEUE.md'}
        diff=run('diff',base,HEAD);(A/'original_diff_v2.patch').write_bytes(diff);(A/'original_diff_v2.patch').chmod(0o444)
        manifest={'schema':'pr44-root-readonly-original-snapshot/v1','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'pr':44,'id':2912,'head':HEAD,'base':base,'main_at_export':current,'files':rows,'changed_paths':changed,'diff_bytes':len(diff),'diff_sha256':hashlib.sha256(diff).hexdigest(),'scientific_helpers_executed':False,'mathematical_review':'PENDING','new_substantive_attempts':0,'audit_turns':0}
        with (A/'snapshot_manifest_v2.json').open('x')as f:json.dump(manifest,f,indent=2);f.write('\n')
        (A/'snapshot_manifest_v2.json').chmod(0o444)
        assert run('rev-parse','HEAD').decode().strip()==current
        print(json.dumps({'status':'PASS_ORIGINAL_EXPORT_ONLY','members':len(rows),'changed':len(changed),'base':base,'diff_bytes':len(diff),'manifest_sha256':hashlib.sha256((A/'snapshot_manifest_v2.json').read_bytes()).hexdigest()}))
    finally:
        with (A/'ORIGINAL_GIT_COMMANDS_V2.json').open('x')as f:json.dump(commands,f,indent=2);f.write('\n')


if __name__=='__main__':
    main()
