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
AUTHOR_PIN = '6e85d6ff39d8c353145140f1122f00861c95ed200f0f35a5445a007dfda2c825'
AUDIT_PIN = 'fc5d45f84f3222c03392924f4fc8aba94e8af59d0567f89d047c7392cc6b54fb'
SPECS = [
 ('FINITE_MEAN_CODING_30005024_AUTHOR_SAFE_FREEZE.zip','author',19304,
  '0f5e6dfb82fa255889d917eba93535e1912785787276f5a3f63e85a9abddc144',AUTHOR_PIN,10,'MANIFEST.json'),
 ('FINITE_MEAN_CODING_30005024_INDEPENDENT_AUDIT.zip','audit',44955,
  'b14db896d3572e668e6139aaf677ac06d16df90b083aae7b487604bde8358d54',AUDIT_PIN,22,'AUDIT_MANIFEST.json')]

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
    for name,folder,size,digest,mpin,count,manifest_name in SPECS:
        frozen=root/folder
        m=(frozen/manifest_name).read_bytes()
        require(meta(m)['sha256']==mpin,'Frozen manifest pin')
        rows=json.loads(m)['files']
        names={r['path'] for r in rows}|{manifest_name}
        require(len(names)==count,'Frozen file count')
        require(inventory(frozen)==(names,expected_dirs(names)),'Frozen recursive inventory')
        rows_check(frozen,rows,names-{manifest_name})
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
    source=json.loads((root/'audit/SOURCE_AUDIT.json').read_bytes())
    require(source['review_hash']=='fb5ee42c259cebb1c28137995be1214779f6c5a20c8e56a417fe7429b3b463fc','Review hash addendum')
    require(source['review_hash_independently_recomputed'] is True,'Review hash history')
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
    matches=[i for i,l in enumerate(lines) if b'| 30005024 / OWR-9790359-005 |' in l]
    require(len(matches)==1,'Exact queue target match')
    i=matches[0];fields=lines[i].split(b'|')
    require(fields[8:10]==[b' queued ',b' 0/5 '],'Queue old fields')
    fields[8:10]=[b' unsolved ',b' 5/5 ']
    lines[i]=b'|'.join(fields)
    require(b''.join(lines)==a,'Only Status and Turns may change; preserve every other byte')
    return 'PASS_EXACT_FULL_BYTES'

def verify(root=ROOT,expected_manifest=None,before=None,after=None):
    root=Path(root).resolve()
    result=integrity(root,expected_manifest)
    manifest=json.loads(run(root/'author/verify_manifest.py'))
    audit_manifest=json.loads(run(root/'audit/verify_audit_manifest.py'))
    require(manifest=={'status':'PASS_MANIFEST','files':9},'Author manifest replay')
    require(audit_manifest=={'status':'PASS_AUDIT_MANIFEST','files':21,'source_payload_included':False},'Audit manifest replay')
    author=json.loads(run(root/'author/verify.py'))
    duplicate=json.loads(run(root/'audit/author/verify.py'))
    require(author==duplicate=={'status':'PASS_FINITE_DIAGNOSTICS','assertions':9093,'recorded_results_match':True},'Author deterministic results replay')
    independent=json.loads(run(root/'audit/verify_independent.py'))
    require(independent=={'status':'PASS_INDEPENDENT_REBUILD','original_cases_rebuilt':9093,'additional_exact_checks':3787,'primitive_three_state_supports_checked':139,'recorded_author_results_match':True},'Independent deterministic results replay')
    status=json.loads((root/'audit/AUDIT_RESULT.json').read_bytes())
    require(status['audit_result']=='PASS_SCOPED_AUXILIARY_RESULTS' and status['general_problem_status']=='unsolved','Scoped disposition')
    require(status['substantive_approaches_used']==5 and status['limit']==5,'Approach count')
    require(not status['full_solution'] and not status['mathematical_corrections_required'],'No full solution or mathematical correction')
    require((before is None)==(after is None),'Supply both queue inputs or neither')
    queue=queue_check(root,before,after) if before else 'NOT_RUN_EXTERNAL_QUEUE_INPUTS_REQUIRED'
    require(integrity(root,expected_manifest)==result,'Replay altered packet')
    result.update(status='PASS',problem_id='30005024',assertions_enabled=True,
        author_assertions=9093,independent_original_cases_rebuilt=9093,independent_additional_checks=3787,
        primitive_three_state_supports=139,recorded_results_recomputed_and_matched=True,
        both_frozen_archives_verified=True,review_hash_addendum_verified=True,
        disposition='unsolved',substantive_approaches='5/5',queue_delta=queue,
        external_source_provenance='NOT_RUN_EXTERNAL_INPUTS_REQUIRED',
        new_source_retrieval_or_inspection='NOT_RUN',
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
