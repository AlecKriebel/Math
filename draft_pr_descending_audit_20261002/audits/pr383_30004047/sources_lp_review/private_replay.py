#!/usr/bin/env python3
"""Replay audited author code solely in an output-local private B copy."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys

p=Path(__file__).resolve().parent
a=p.parent
m=json.loads((a/'snapshot_manifest.json').read_text())
clone=p/'private_B'
clone.mkdir(exist_ok=True)
for row in m['files']:
    src=a/'snapshot'/row['path']
    b=src.read_bytes()
    assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
    dst=clone/row['path']
    dst.parent.mkdir(parents=True,exist_ok=True)
    dst.write_bytes(b)
d=clone/'unsolved_math_prioritization/attempts/30004047'
sd=p/'bound_source_names'
sd.mkdir(exist_ok=True)
for out,original in [('OWR_2019_1.pdf','ems_46780.pdf'),
                     ('Concatenating_published_2022.pdf','ejc_v29i2p47.pdf')]:
    shutil.copyfile(p/'primary_sources'/original,sd/out)
source_rows=[]
for row in json.loads((d/'SOURCE_MANIFEST.json').read_text())['files']:
    b=(sd/row['name']).read_bytes()
    assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
    source_rows.append(dict(name=row['name'],bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),matches=True))
cmd=[sys.executable,str(d/'verify_packet.py'),'--author-dir',str(d),'--source-dir',str(sd)]
proc=subprocess.run(cmd,cwd=d,capture_output=True,check=True)
(p/'PRIVATE_VERIFY_PACKET.stdout').write_bytes(proc.stdout)
(p/'PRIVATE_VERIFY_PACKET.stderr').write_bytes(proc.stderr)
rows=[]
for i in range(1,6):
    proc=subprocess.run([sys.executable,str(d/f'check_turn_{i}.py')],cwd=d,capture_output=True,check=True)
    (p/f'PRIVATE_TURN_{i}.stdout').write_bytes(proc.stdout)
    (p/f'PRIVATE_TURN_{i}.stderr').write_bytes(proc.stderr)
    assert proc.stdout==(d/f'TURN_{i}_CHECKS.json').read_bytes()
    rows.append(dict(turn=i,byte_exact=True,exact_assertions=json.loads(proc.stdout)['exact_assertions']))
for row in m['files']:
    b=(clone/row['path']).read_bytes()
    assert b==(a/'snapshot'/row['path']).read_bytes()
    assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
assert {str(f.relative_to(clone)) for f in clone.rglob('*') if f.is_file()}=={r['path'] for r in m['files']}
result=dict(status='PASS',input_files=49,target_files=48,queue_files=1,private_B_full_bytes_unchanged=True,
            sources=source_rows,packet_verifier=json.loads((p/'PRIVATE_VERIFY_PACKET.stdout').read_text()),
            direct_replays=rows,executed_reviewer_code=False,
            scope='Read all five author checkers and packet/publication verifiers before execution; only author packet verifier and five author checkers executed in private B. No prior review verdict used.')
(p/'PRIVATE_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(status='PASS',input_files=49,author_assertions=sum(r['exact_assertions'] for r in rows),sources_checked=2),indent=2))
