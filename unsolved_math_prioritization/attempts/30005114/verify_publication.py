#!/usr/bin/env python3
"""Read-only exact inventory, immutable freeze, and finite replay checks."""
import argparse
import base64
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import zipfile

ROOT=Path(__file__).resolve().parent
SPECS=[
 ('TRIANGLE_REMOVAL_SPREAD_30005114_AUTHOR_SAFE_FREEZE.zip','author',17977,
  'dd3d6c99dea68a3dab8332574562c4232d14fca288bc1b61515b927a5086b48f',
  'a1d67cd8bb7c3c41f72a22371611096a62dcea021444740d741206200fdac0bf',7),
 ('TRIANGLE_REMOVAL_SPREAD_30005114_INDEPENDENT_AUDIT.zip','audit',39177,
  '7490cbb65128e68bb63a2e04d48ba8e4bc5577d617858d7fd8635a6ddcf10fbe',
  'd2d06d0c737be8a45098401f8304c7d3bb15568bb61601e200a43c2fb2fc7815',19)]

def require(ok,why):
    if not ok: raise ValueError(why)

def meta(b):
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def inventory(root):
    require(not root.is_symlink(),'Symlink root')
    files,dirs=set(),set()
    for p in root.rglob('*'):
        n=p.relative_to(root).as_posix()
        require(not p.is_symlink(),'Symlink entry')
        if p.is_dir():dirs.add(n)
        else:
            require(p.is_file(),'Nonregular entry')
            files.add(n)
    return files,dirs

def expected_dirs(files):
    return {p.as_posix() for n in files for p in Path(n).parents if p.as_posix()!='.'}

def safe_path(n):
    p=Path(n)
    require(not p.is_absolute() and '..' not in p.parts and p.as_posix()==n,'Unsafe path')

def frozen_manifest(root,pin,count):
    raw=(root/'MANIFEST.sha256').read_bytes()
    require(meta(raw)['sha256']==pin,'Frozen manifest pin')
    rows={}
    for line in raw.decode().splitlines():
        digest,name=line.split('  ',1);safe_path(name)
        require(name not in rows,'Duplicate manifest entry')
        rows[name]=digest
    names=set(rows)|{'MANIFEST.sha256'}
    require(len(names)==count and inventory(root)==(names,expected_dirs(names)),'Frozen recursive inventory')
    for n,h in rows.items():
        require(Path(n).suffix in {'.md','.json','.py','.sha256'},'Unsafe frozen file type')
        require(meta((root/n).read_bytes())['sha256']==h,'Frozen payload hash: '+n)
    return names

def integrity(root,expected_manifest=None):
    root=Path(root)
    require(__debug__ and sys.flags.optimize==0,'Assertions must remain enabled; no -O or PYTHONOPTIMIZE.')
    raw=(root/'PUBLICATION_MANIFEST.json').read_bytes();pin=meta(raw)['sha256']
    if expected_manifest:require(pin==expected_manifest,'External publication manifest pin')
    rows=json.loads(raw)['files']
    require(len(rows)==len({r['path'] for r in rows}),'Duplicate publication entries')
    want={r['path'] for r in rows}|{'PUBLICATION_MANIFEST.json'}
    require(inventory(root)==(want,expected_dirs(want)),'Exact recursive inventory')
    for r in rows:
        n=r['path'];safe_path(n)
        require(meta((root/n).read_bytes())=={k:r[k] for k in ('bytes','sha256')},'Changed publication member: '+n)
    for name,folder,size,digest,mpin,count in SPECS:
        frozen=root/folder;names=frozen_manifest(frozen,mpin,count)
        enc=(root/'frozen_archives'/(name+'.b64')).read_bytes()
        data=base64.b64decode(enc.strip(),validate=True)
        require(base64.b64encode(data)+b'\n'==enc,'Canonical archive encoding')
        require(meta(data)=={'bytes':size,'sha256':digest},'Original ZIP identity')
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            entries=z.infolist()
            require(len(entries)==count and {m.filename for m in entries}==names,'ZIP exact member set')
            require(z.testzip() is None,'ZIP CRC')
            for member in entries:
                require(not member.is_dir() and not stat.S_ISLNK(member.external_attr>>16),'Unsafe ZIP member')
                require(not member.flag_bits & 1,'Encrypted ZIP member')
                require(z.read(member)==(frozen/member.filename).read_bytes(),'ZIP/directory byte mismatch')
    frozen_manifest(root/'audit/author_frozen',SPECS[0][4],7)
    for p in (root/'author').rglob('*'):
        if p.is_file():require(p.read_bytes()==(root/'audit/author_frozen'/p.relative_to(root/'author')).read_bytes(),'Audit author copy changed')
    return {'publication_manifest_sha256':pin,'packet_files':len(want)}

def run(script):
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
    return subprocess.check_output([sys.executable,'-B',str(script)],env=env)

def queue_check(root,before,after):
    d=json.loads((root/'QUEUE_DELTA.json').read_bytes());b=Path(before).read_bytes();a=Path(after).read_bytes()
    require(meta(b)==d['before'] and meta(a)==d['after'],'Complete queue hashes')
    lines=b.splitlines(keepends=True)
    matches=[i for i,l in enumerate(lines) if b'| 30005114 / OWR-10252930-024 |' in l]
    require(len(matches)==1,'Exact queue target match')
    i=matches[0];fields=lines[i].split(b'|')
    require(fields[8:10]==[b' queued ',b' 0/5 '],'Queue old fields')
    fields[8]=b' unsolved ';fields[9]=b' 5/5 ';lines[i]=b'|'.join(fields)
    require(b''.join(lines)==a,'Only Status and Turns may change; preserve every other byte')
    return 'PASS_EXACT_FULL_BYTES'

def verify(root=ROOT,expected_manifest=None,before=None,after=None):
    root=Path(root).resolve();result=integrity(root,expected_manifest)
    run(root/'audit/code/verify_manifest.py')
    author=run(root/'author/code/verify_triangle_removal.py')
    independent=run(root/'audit/code/independent_verify.py')
    require(author==(root/'author/results/verification.json').read_bytes(),'Author byte-for-byte replay')
    require(author==(root/'audit/results/author_replayed.json').read_bytes(),'Audit author replay identity')
    require(independent==(root/'audit/results/independent_verification.json').read_bytes(),'Independent byte-for-byte replay')
    require(json.loads(author)['status']=='PASS' and json.loads(independent)['status']=='PASS','Finite verifier status')
    require(json.loads(independent)['hazards']['graph_family_pairs']==141040,'Independent enumeration count')
    require((before is None)==(after is None),'Supply both queue inputs or neither')
    queue=queue_check(root,before,after) if before else 'NOT_RUN_EXTERNAL_QUEUE_INPUTS_REQUIRED'
    require(integrity(root,expected_manifest)==result,'Replay altered packet')
    result.update(status='PASS',problem_id='30005114',assertions_enabled=True,
        both_replays_byte_identical=True,both_frozen_archives_verified=True,independent_graph_family_cases=141040,
        disposition='unsolved',turns='5/5',queue_delta=queue,
        full_dataset_and_primary_source_reinspection='NOT_RUN_EXTERNAL_INPUTS_REQUIRED',
        finite_checks_are_formal_proof=False,hosted_ci_pass_claimed=False)
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',default=str(ROOT));p.add_argument('--expected-manifest')
    p.add_argument('--queue-before');p.add_argument('--queue-after');a=p.parse_args()
    print(json.dumps(verify(a.root,a.expected_manifest,a.queue_before,a.queue_after),indent=2,sort_keys=True))
