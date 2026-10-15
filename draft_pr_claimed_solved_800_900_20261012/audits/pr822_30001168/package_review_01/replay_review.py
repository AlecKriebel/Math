#!/usr/bin/env python3
"""Independent relocated replays and archive inspection; original inputs are read-only."""
from pathlib import Path, PurePosixPath
import datetime
import hashlib
import json
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import zipfile

A = Path(__file__).resolve().parents[1]
R = A / 'package_review_01'
T = A.parents[1] / 'work/pr822_revision_r1'
def sha(b): return hashlib.sha256(b).hexdigest()
def need(c, m):
    if not c: raise RuntimeError(m)
def read(p): return json.loads(p.read_bytes())

receipt = {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'runs': [], 'read_only_inputs': True}
with zipfile.ZipFile(A/'preprint/verification.zip') as z:
    members = z.infolist()
    names = [i.filename for i in members]
    need(len(names) == len(set(names)) == 110, 'portable member count')
    need(not z.comment and z.testzip() is None, 'ZIP comment/CRC')
    for i in members:
        n=PurePosixPath(i.filename)
        need(not i.is_dir() and not n.is_absolute() and '..' not in n.parts
             and '\\' not in i.filename and str(n)==i.filename
             and stat.S_ISREG(i.external_attr>>16), 'unsafe ZIP member')
        need(not i.extra and not i.comment and not i.flag_bits & 1, 'ZIP extra/comment/encryption')
        need(i.date_time == (2026,10,13,0,0,0), 'nonfixed member timestamp')
        need(z.read(i)==(T/'publication_20261013/verification_package'/i.filename).read_bytes(),
             'ZIP/assembly mismatch')
    receipt['portable_archive']={'members':len(members),'safe_regular_members':True,
        'CRC_verified':True,'fixed_timestamps':True,'extracted_assembly_byte_identity':True,
        'sha256':sha((A/'preprint/verification.zip').read_bytes())}
index_pin=sha((A/'preprint/package_index.json').read_bytes())
outer_pin=sha((T/'PUBLICATION_MANIFEST.json').read_bytes())
for family in ('portable','outer'):
    for optimized in (False, True):
        with tempfile.TemporaryDirectory(prefix='independent R1 review with spaces ') as td:
            root=Path(td)/('portable package with spaces' if family=='portable' else 'outer repository with spaces')
            if family=='portable':
                root.mkdir()
                with zipfile.ZipFile(A/'preprint/verification.zip') as z:z.extractall(root)
                script=root/'verify_package.py';pin=index_pin
            else:
                shutil.copytree(T,root)
                script=root/'verify_publication.py';pin=outer_pin
            command=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(script),pin,'--full']
            started=time.monotonic()
            result=subprocess.run(command,cwd='/',capture_output=True,text=True,timeout=900)
            record={'family':family,'optimized':optimized,'relocated_path_has_spaces':True,
                    'foreign_cwd':'/','exit_code':result.returncode,'elapsed_seconds':time.monotonic()-started,
                    'stdout_sha256':sha(result.stdout.encode()),'stderr':result.stderr}
            if result.returncode==0:record['output']=json.loads(result.stdout)
            else:record['stdout']=result.stdout
            receipt['runs'].append(record)
            (R/'REPLAY_RECEIPTS.json').write_text(json.dumps(receipt,indent=2)+'\n')
            print(json.dumps({k:v for k,v in record.items() if k not in ('output','stdout')}),flush=True)
            need(result.returncode==0 and not result.stderr, family+' replay failed')

# Rebuild in the audit-layout expected by the dated builder, entirely in a temp copy.
with tempfile.TemporaryDirectory(prefix='independent deterministic R1 rebuild ') as td:
    audit=Path(td)/'audit with spaces';pre=audit/'preprint';pre.mkdir(parents=True)
    for p in (A/'preprint').iterdir():
        if p.is_file():shutil.copyfile(p,pre/p.name)
    (pre/'output/pdf').mkdir(parents=True)
    shutil.copyfile(A/'preprint/output/pdf/note.pdf',pre/'output/pdf/note.pdf')
    shutil.copytree(A/'source',audit/'source')
    for folder in ('geometry_audit_01','trace_audit_01'):
        target=audit/folder;target.mkdir()
        for p in (A/folder).iterdir():
            if p.is_file() and p.suffix in {'.md','.json','.jsonl','.py'}:shutil.copyfile(p,target/p.name)
    priority=audit/'priority_audit_01';priority.mkdir()
    manifest=read(A/'priority_audit_01/PUBLIC_MANIFEST.json')
    for row in manifest['files']:
        target=priority/row['relative_public_path'];target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(A/'priority_audit_01'/row['relative_public_path'],target)
    shutil.copyfile(A/'priority_audit_01/PUBLIC_MANIFEST.json',priority/'PUBLIC_MANIFEST.json')
    for p in A.iterdir():
        if p.is_file() and p.suffix in {'.md','.json','.py'}:shutil.copyfile(p,audit/p.name)
    result=subprocess.run([sys.executable,'-I','-B',str(pre/'build_verification.py')],
                          cwd='/',capture_output=True,text=True,timeout=60)
    need(result.returncode==0 and not result.stderr,'rebuild failed '+result.stderr)
    need((pre/'package_index.json').read_bytes()==(A/'preprint/package_index.json').read_bytes(),'index nondeterminism')
    need((pre/'verification.zip').read_bytes()==(A/'preprint/verification.zip').read_bytes(),'archive nondeterminism')
    receipt['deterministic_rebuild']={'layout':'disposable audit layout with spaces',
        'exit_code':result.returncode,'index_byte_identical':True,'zip_byte_identical':True,
        'output':json.loads(result.stdout)}
(R/'REPLAY_RECEIPTS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'deterministic_rebuild':receipt['deterministic_rebuild']},indent=2))
