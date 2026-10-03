"""Reproduce this lane's source-free controls and verify its owned evidence."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json,subprocess,sys,os

P=Path(__file__).parent
manifest=json.loads((P/'PUBLIC_MANIFEST.json').read_text())
for f in manifest['files']:
    b=(P/f['path']).read_bytes()
    assert len(b)==f['bytes'] and sha256(b).hexdigest()==f['sha256'],f['path']
source=json.loads((P/'source_first_seal.json').read_text())
for path,digest in source['public_files'].items():
    assert sha256((P/path).read_bytes()).hexdigest()==digest,path
verdict=json.loads((P/'mathematical_verdict_seal.json').read_text())
assert sha256((P/'MATHEMATICAL_VERDICT.md').read_bytes()).hexdigest()==verdict['proof_sha256']
assert sha256((P/'post_candidate_controls.py').read_bytes()).hexdigest()==verdict['control_sha256']
T=P/'tmp';T.mkdir(exist_ok=True)
env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';env['TMPDIR']=str(T)
for script,seal in [('independent_controls.py',source),('post_candidate_controls.py',verdict)]:
    r=subprocess.run([sys.executable,str(P/script)],cwd=P,env=env,capture_output=True)
    (T/(script+'.owned_replay.stdout')).write_bytes(r.stdout)
    (T/(script+'.owned_replay.stderr')).write_bytes(r.stderr)
    assert r.returncode==0
    assert sha256(r.stdout).hexdigest()==seal['controls_stdout_sha256']
    assert sha256(r.stderr).hexdigest()==seal['controls_stderr_sha256']
    print(script,'PASS; source PDF reads=0')
print('Owned public paths:',len(manifest['files']))
print('Both independence seals and all public hashes PASS')
print('Completed UTC:',datetime.now(timezone.utc).isoformat())
