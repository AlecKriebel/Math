#!/usr/bin/env python3
"""Private public-checkout fixture; never removes or changes source namespaces."""
import json,os,pathlib,shutil,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parent;A=ROOT.parent
dest=ROOT/'private/public_only_fixture_v2';dest.mkdir(exist_ok=False)
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
run=subprocess.run([sys.executable,str(mine/'verify_public.py'),'--preseal','--replay'],env=env,capture_output=True)
sys.stdout.buffer.write(run.stdout);sys.stderr.buffer.write(run.stderr)
assert run.returncode==0
o=json.loads(run.stdout);assert o['private_evidence'].startswith('absent;')
assert all(s.startswith('public integrity only') for s in o['family_evidence'].values())
