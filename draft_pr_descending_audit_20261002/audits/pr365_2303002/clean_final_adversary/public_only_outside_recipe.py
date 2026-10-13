#!/usr/bin/env python3
"""Create a public-only scratch OUTSIDE this immutable review namespace.

This is a writing fixture driver, never a read-only command. Only new ROOT
scratch/receipt paths are written; no source, index/ref or family is modified.
"""
import datetime,gzip,hashlib,json,os,pathlib,shutil,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parent;A=ROOT.parent
dest=A/'root_replay_private/public_only_whole';dest.mkdir(exist_ok=False)
audit=dest/'audit';audit.mkdir();mine=audit/ROOT.name;mine.mkdir()
m=json.loads((ROOT/'PUBLIC_MANIFEST.json').read_bytes())
for p in list(m['public_files'])+['PUBLIC_MANIFEST.json']:
    q=mine/p;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/p,q)
for b in json.loads((ROOT/'03_reproduction_bindings.json').read_bytes())['original_bindings']:
    q=audit/'snapshot'/b['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(A/'snapshot'/b['path'],q)
for f in m['family_closures']:
    source=A/f['directory'];d=audit/f['directory'];d.mkdir()
    fm=json.loads((source/f['manifest']).read_bytes());ps=fm['files']
    ps=[r['path'] for r in ps] if isinstance(ps,list) else list(ps)
    for p in ps+[f['manifest'],'FINAL_SEAL.json']:
        q=d/p;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source/p,q)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
argv=[sys.executable,str(mine/'verify_public.py'),'--preseal','--replay']
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
run=subprocess.run(argv,env=env,capture_output=True)
rec=dict(argv=argv,started_utc=start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_code=run.returncode,streams={})
for name,data in [('stdout',run.stdout),('stderr',run.stderr)]:
    stored=gzip.compress(data,mtime=0);p=A/'root_replay_private'/('public_only_whole.'+name+'.gz');p.write_bytes(stored)
    rec['streams'][name]=dict(path=p.relative_to(A).as_posix(),logical_bytes=len(data),logical_sha256=hashlib.sha256(data).hexdigest(),stored_bytes=len(stored),stored_sha256=hashlib.sha256(stored).hexdigest())
(A/'root_replay_private/public_only_whole.receipt.json').write_text(json.dumps(rec,indent=2)+'\n')
sys.stdout.buffer.write(run.stdout);sys.stderr.buffer.write(run.stderr)
assert run.returncode==0
o=json.loads(run.stdout);assert o['private_evidence'].startswith('absent;')
assert all(s.startswith('public integrity only') for s in o['family_evidence'].values())
