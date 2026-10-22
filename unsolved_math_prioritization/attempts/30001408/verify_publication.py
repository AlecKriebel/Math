#!/usr/bin/env python3
"""Fail-closed integrity, controlling-correction binding, and portable replay.

Does not certify an all-body theorem or authenticate a coordinated rewrite of
this verifier and manifest. Pin the externally recorded manifest digest.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PINS = {
    'author/AUTHOR_MANIFEST.json':'938d14791569ca0c77c9f19b13a71bd33219df81395d778c86e6703300c9bb34',
    'audit/AUDIT_MANIFEST.json':'5500994baaca7f9a25bd5a8510a8aba3ead206f063e23188e12a41a0ace9c991',
    'audit/CORRECTION.md':'c865aab4da0e409cc62ae9c444c3a38d73a4c4ac4d12f88a71eb0895edb85b01',
}
def require(condition, message):
    if not condition:
        raise ValueError(message)
def digest(data):
    return hashlib.sha256(data).hexdigest()
def load(path):
    return json.loads((ROOT/path).read_bytes())
def bound_file(path, row):
    data=(ROOT/path).read_bytes()
    require(len(data)==row['bytes'], 'Byte mismatch: '+path)
    require(digest(data)==row['sha256'], 'Hash mismatch: '+path)
def run(script, *args):
    env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONOPTIMIZE='0')
    return subprocess.check_output([sys.executable,'-B','-I',str(ROOT/script),*map(str,args)],cwd=ROOT,env=env)

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--expected-manifest-sha256')
args=parser.parse_args()
manifest_bytes=(ROOT/'PUBLICATION_MANIFEST.json').read_bytes()
if args.expected_manifest_sha256:
    require(digest(manifest_bytes)==args.expected_manifest_sha256,'Publication manifest trust-anchor mismatch')
manifest=json.loads(manifest_bytes)
require(manifest['problem_id']=='30001408','Wrong problem ID')
require(manifest['mathematical_status']=='unsolved' and manifest['turns']=='5/5','Wrong status')
rows=manifest['files']; names=[r['path'] for r in rows]
require(len(names)==len(set(names)), 'Duplicate manifest path')
for name in names:
    p=Path(name)
    require(not p.is_absolute() and '..' not in p.parts and p.as_posix()==name,'Unsafe path')
expected=set(names)|{'PUBLICATION_MANIFEST.json'}
actual=set()
for p in ROOT.rglob('*'):
    require(not p.is_symlink(),'Symlink forbidden')
    name=p.relative_to(ROOT).as_posix()
    if p.is_dir():
        require(name in {'author','audit'},'Unexpected directory: '+name)
    else:
        require(p.is_file(),'Nonregular file: '+name)
        actual.add(name)
require(actual==expected,'Packet has missing or unlisted files')
for row in rows:
    bound_file(row['path'],row)
for name,pin in PINS.items():
    require(digest((ROOT/name).read_bytes())==pin,'Frozen trust-anchor mismatch: '+name)
author=load('author/AUTHOR_MANIFEST.json'); audit=load('audit/AUDIT_MANIFEST.json')
require(author['status']=='unsolved' and author['approaches_used']==5,'Author status')
require(audit['verdict']=='PASS_WITH_REQUIRED_CORRECTION','Audit verdict')
require(audit['mathematical_status']=='unsolved' and audit['approaches_used']==5,'Audit status')
for prefix,original,manifestname in [('author',author,'AUTHOR_MANIFEST.json'),('audit',audit,'AUDIT_MANIFEST.json')]:
    required={r['path'] for r in original['files']}|{manifestname}
    require({p.name for p in (ROOT/prefix).iterdir()}==required,'Frozen file set: '+prefix)
    for row in original['files']:
        require(Path(row['path']).name==row['path'],'Unsafe frozen path')
        bound_file(prefix+'/'+row['path'],row)
status=load('RELEASE_STATUS.json')
require(status['problem_id']=='30001408' and status['rank']==696,'Release identity')
require(status['mathematical_status']=='unsolved' and status['turns']=='5/5' and status['approaches_used']==5,'Release status')
require(status['audit_verdict']=='PASS_WITH_REQUIRED_CORRECTION' and status['correction_authoritative'] is True,'Correction precedence missing')
require(status['correction_path']=='audit/CORRECTION.md' and status['correction_sha256']==PINS['audit/CORRECTION.md'],'Correction identity')
for name in ['full_higher_dimensional_classification','mixed_infinity_example_constructed','historical_novelty_claim','global_open_status_claim','finite_checks_are_proof']:
    require(status[name] is False,'Unsupported claim: '+name)
binding=load('audit/BINDING.json')
bound_file('author/'+binding['corrected_file']['path'],binding['corrected_file'])
require(binding['author_manifest']['sha256']==PINS['author/AUTHOR_MANIFEST.json'],'Author binding')
text=(ROOT/'author/RESULT.md').read_text()
part=binding['corrected_paragraph']
require(text.count(part['starts_with'])==1,'Correction target is not unique')
start=text.index(part['starts_with']); end=text.index('\n\n',start)
paragraph=text[start:end].encode()
require(len(paragraph)==part['bytes'] and digest(paragraph)==part['sha256'],'Correction target paragraph mismatch')
require(text[:start].count('\n')+1==part['line'] and paragraph.decode().endswith(part['ends_with']),'Correction target location mismatch')
correction=(ROOT/'audit/CORRECTION.md').read_text()
replacement=correction.split('## Complete replacement paragraph\n\n',1)[1].split('\n\n## Exact counterexample',1)[0].encode()
part=binding['replacement_paragraph']
require(len(replacement)==part['bytes'] and digest(replacement)==part['sha256'],'Full replacement mismatch')
require(replacement.decode() in (ROOT/'README.md').read_text(),'Entry-point replacement missing')
before={p:digest((ROOT/p).read_bytes()) for p in expected}
author_out=run('author/check_controls.py')
audit_out=run('audit/audit_controls.py', ROOT/'author')
require(author_out==(ROOT/'author/CONTROL_RESULTS.json').read_bytes(),'Author output mismatch')
require(audit_out==(ROOT/'audit/AUDIT_RESULTS.json').read_bytes(),'Audit output mismatch')
av=json.loads(author_out); iv=json.loads(audit_out)
require(av['total_assertions']==15200 and iv['independent_assertions']==28270,'Unexpected check counts')
require(len(iv['deliberate_negatives'])==10 and all(x['rejected'] is True for x in iv['deliberate_negatives']),'Mathematical negatives')
require(iv['groups']['in_memory_tamper_rejections']==8,'Tamper checks')
run('author/verify_packet.py')
run('audit/verify_audit.py',ROOT/'author')
require(before=={p:digest((ROOT/p).read_bytes()) for p in expected},'Replay modified files')
print(json.dumps({'result':'PASS_CORRECTED_PACKET_BINDINGS_AND_FINITE_REPLAY',
 'problem_id':'30001408','mathematical_status':'unsolved','turns':'5/5',
 'audit_verdict':'PASS_WITH_REQUIRED_CORRECTION','controlling_replacement_bound':True,
 'frozen_author_files':8,'frozen_audit_files':7,'release_files':len(expected),
 'author_assertions':15200,'independent_checks':28270,'mathematical_negatives':10,
 'in_memory_tamper_negatives':8,'outputs_byte_identical':True,
 'limitation':'Integrity and finite controls only; not a complete classification, formal verification, human peer review, novelty claim, or CI result.'},sort_keys=True,indent=2))
