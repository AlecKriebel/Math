#!/usr/bin/env python3
"""Read-only exact inventory, immutable freeze and finite replay verification."""
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

ROOT = Path(__file__).resolve().parent
AUTHOR_PIN = 'ce591fbb475041f39c5b6df4e4bafb535f534f1a6c7abd2dc8e439c2314ddf52'
AUDIT_PIN = 'c360712a1b0b2e1afa241e755244370ef1f8f954824134b6423a29e3ceefeab9'
SUPPLEMENT_PIN = '0a7982b7a16f8ce2db8747cbb5b7600eddc2d37a12a99dad703d0d3eb5be5c58'
SUPPLEMENT = 'HOPF_30004831_REVIEW_HASH_SUPPLEMENT_RECEIPT.json'
SPECS = [
    ('HOPF_30004831_AUTHOR_SAFE_FREEZE.zip','author',17559,
     '42c545640e66d6ee85dec4d0035ca9b834f733d40baa6f8ec731060586a8aa40',AUTHOR_PIN,11),
    ('HOPF_30004831_INDEPENDENT_AUDIT_PASS.zip','audit',35961,
     '4e9b5ab04a34aeb9eb3396d6a6bf70cab5438f78a53b4f530a374fb193c34e18',AUDIT_PIN,22)]

def require(ok, why):
    if not ok:
        raise ValueError(why)

def meta(b):
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def inventory(root):
    require(not root.is_symlink(),'Symlink root')
    files,dirs=set(),set()
    for p in root.rglob('*'):
        n=p.relative_to(root).as_posix()
        require(not p.is_symlink(),'Symlink entry')
        if p.is_dir(): dirs.add(n)
        else:
            require(p.is_file(),'Nonregular entry')
            files.add(n)
    return files,dirs

def expected_dirs(files):
    return {p.as_posix() for n in files for p in Path(n).parents if p.as_posix()!='.'}

def rows_check(root, rows, files):
    require(len(rows)==len({r['path'] for r in rows}),'Duplicate manifest entries')
    require({r['path'] for r in rows}==files,'Manifest file set')
    for r in rows:
        n=r['path'];p=Path(n)
        require(not p.is_absolute() and '..' not in p.parts and p.as_posix()==n,'Unsafe path')
        require(meta((root/n).read_bytes())=={k:r[k] for k in ('bytes','sha256')},'Changed member: '+n)

def integrity(root, expected_manifest=None):
    root=Path(root)
    require(__debug__ and sys.flags.optimize==0,'Assertions must remain enabled; no -O or PYTHONOPTIMIZE.')
    raw=(root/'PUBLICATION_MANIFEST.json').read_bytes()
    pin=meta(raw)['sha256']
    if expected_manifest: require(pin==expected_manifest,'External publication manifest pin')
    rows=json.loads(raw)['files']
    want={r['path'] for r in rows}|{'PUBLICATION_MANIFEST.json'}
    files,dirs=inventory(root)
    require(files==want and dirs==expected_dirs(want),'Exact recursive inventory')
    rows_check(root,rows,want-{'PUBLICATION_MANIFEST.json'})
    for name,folder,size,digest,mpin,count in SPECS:
        frozen=root/folder
        m=(frozen/'MANIFEST.json').read_bytes()
        require(meta(m)['sha256']==mpin,'Frozen manifest pin')
        rows=json.loads(m)['files']
        names={r['path'] for r in rows}|{'MANIFEST.json'}
        require(len(names)==count,'Frozen file count')
        require(inventory(frozen)==(names,expected_dirs(names)),'Frozen recursive inventory')
        rows_check(frozen,rows,names-{'MANIFEST.json'})
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
    for p in (root/'author').iterdir():
        require(p.read_bytes()==(root/'audit/author'/p.name).read_bytes(),'Audit author copy changed')
    require(meta((root/SUPPLEMENT).read_bytes())['sha256']==SUPPLEMENT_PIN,'Later supplement pin')
    supplement=json.loads((root/SUPPLEMENT).read_bytes())
    require(supplement['review_hash_match'] is True and supplement['original_audit_archive_unchanged'] is True,'Supplement disposition')
    return {'publication_manifest_sha256':pin,'packet_files':len(want)}

def run(script,*args):
    env=dict(os.environ)
    env.pop('PYTHONOPTIMIZE',None)
    env['PYTHONDONTWRITEBYTECODE']='1'
    return subprocess.check_output([sys.executable,'-B',str(script),*map(str,args)],env=env)

def queue_check(root,before,after):
    d=json.loads((root/'QUEUE_DELTA.json').read_bytes())
    b=Path(before).read_bytes();a=Path(after).read_bytes()
    require(meta(b)==d['before'] and meta(a)==d['after'],'Complete queue hashes')
    lines=b.splitlines(keepends=True)
    matches=[i for i,l in enumerate(lines) if b'| 30004831 / OWR-8415347-009 |' in l]
    require(len(matches)==1,'Exact queue target match')
    i=matches[0];fields=lines[i].split(b'|')
    require(fields[8:10]==[b' queued ',b' 0/5 '] and fields[11]==b'  ','Queue old fields')
    fields[8]=b' already_solved '
    fields[11]=b' '+d['changes']['Findings'][1].encode()+b' '
    lines[i]=b'|'.join(fields)
    require(b''.join(lines)==a,'Only Status and Findings may change; preserve every other byte')
    return 'PASS_EXACT_FULL_BYTES'

def verify(root=ROOT,expected_manifest=None,before=None,after=None):
    root=Path(root).resolve()
    result=integrity(root,expected_manifest)
    run(root/'author/verify_manifest.py','--expected-manifest',AUTHOR_PIN)
    author=run(root/'author/verify_algebra.py')
    independent=run(root/'audit/verify_independent.py')
    require(author==(root/'author/CHECK_RESULTS.json').read_bytes(),'Author byte-for-byte replay')
    require(independent==(root/'audit/INDEPENDENT_RESULTS.json').read_bytes(),'Independent byte-for-byte replay')
    require(json.loads(author)['assertions']==4543 and json.loads(independent)['assertions']==2902,'Exact assertion counts')
    audit=json.loads(run(root/'audit/verify_audit.py','--expected-manifest',AUDIT_PIN))
    require(audit['status']=='pass','Audit replay status')
    controls=audit['author_integrity_negative_controls']+audit['audit_integrity_negative_controls']
    require(len(controls)==14 and all(r['rejected'] for r in controls),'Frozen integrity controls')
    status=json.loads((root/'audit/AUDIT_RESULT.json').read_bytes())
    require(status['recommended_status']=='already_solved' and status['new_research_attempts_used']==0,'Credited disposition')
    require(status['credited_resolution']=='Ruipeng Zhu, Example 4.11','Prior-work credit')
    require(status['dimensions']=={'H':1,'L':'infinity'},'Dimensions')
    require(status['independent_false_variants_detected']==313,'False variants')
    require(not status['novelty_claim'] and not status['expert_peer_review_claim'] and not status['formal_proof_claim'],'Scope claims')
    require((before is None)==(after is None),'Supply both queue inputs or neither')
    queue=queue_check(root,before,after) if before else 'NOT_RUN_EXTERNAL_QUEUE_INPUTS_REQUIRED'
    require(integrity(root,expected_manifest)==result,'Replay altered packet')
    result.update(status='PASS',problem_id='30004831',assertions_enabled=True,
        author_assertions=4543,independent_assertions=2902,independent_false_variants=313,
        frozen_integrity_negative_controls=14,both_replays_byte_identical=True,
        both_frozen_archives_verified=True,supplement_pin_verified=True,
        disposition='already_solved',new_research_attempts='0/5',queue_delta=queue,
        full_dataset_and_primary_source_reinspection='NOT_RUN_EXTERNAL_INPUTS_REQUIRED',
        finite_checks_are_formal_proof=False,hosted_ci_pass_claimed=False)
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--root',default=str(ROOT))
    p.add_argument('--expected-manifest')
    p.add_argument('--queue-before')
    p.add_argument('--queue-after')
    a=p.parse_args()
    print(json.dumps(verify(a.root,a.expected_manifest,a.queue_before,a.queue_after),indent=2,sort_keys=True))
