"""ROOT full immutable current byte/type/reading reconciliation; no imports."""
import datetime as dt
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
A=Path(__file__).resolve().parent;C=A/'reviewed_candidate';R=A.parents[2]
def sha(b):return hashlib.sha256(b).hexdigest()
def parse(b):
 def unique(items):
  o={}
  for k,v in items:assert k not in o;o[k]=v
  return o
 def floating(v):
  n=float(v);assert math.isfinite(n);return n
 return json.loads(b,object_pairs_hook=unique,parse_float=floating,parse_constant=lambda v:(_ for _ in()).throw(ValueError(v)))
def eq(a,b):
 if type(a) is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys() and all(eq(a[k],v) for k,v in b.items())
 if isinstance(a,list):return len(a)==len(b) and all(eq(x,y) for x,y in zip(a,b))
 return a==b
def check(root,row):
 n=row['path'];p=PurePosixPath(n);assert type(n) is str and n and not p.is_absolute() and p.as_posix()==n and '..' not in p.parts and '\\' not in n
 f=root/n;assert f.is_file() and not f.is_symlink();b=f.read_bytes()
 size=row.get('bytes',row.get('size'));assert type(size) is int and len(b)==size and sha(b)==row['sha256']
 return b
manifest_raw=(C/'MANIFEST.json').read_bytes();assert sha(manifest_raw)=='3431ca2dfb332500f3815ea1e61f089744b3bacd9c3659018537016b9396fbfa'
m=parse(manifest_raw);assert m['self_excluded']==['MANIFEST.json'] and type(m['files_count']) is int and m['files_count']==len(m['files'])==547
names=[z['path'] for z in m['files']];assert len(names)==len(set(names)) and 'MANIFEST.json' not in names
expected=set(names)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in PurePosixPath(n).parents if p.as_posix()!='.'}
actual=set();actual_dirs=set();objects={};total=len(manifest_raw)
for p in C.rglob('*'):
 assert not p.is_symlink() and (p.is_file() or p.is_dir())
 (actual_dirs if p.is_dir() else actual).add(p.relative_to(C).as_posix())
assert actual==expected and actual_dirs==dirs
for row in m['files']:
 b=check(C,row);total+=len(b);assert (C/row['path']).stat().st_mode&0o777==0o444 and row['mode']=='0444'
 if PurePosixPath(row['path']).suffix=='.json':objects[row['path']]=parse(b)
assert (C/'MANIFEST.json').stat().st_mode&0o777==0o444
d=objects['CURRENT_PROOF_DEPENDENCIES.json'];assert d['dependency_anchor_repository_relative']==A.relative_to(R).as_posix() and len(d['files'])==469
dn=[z['path'] for z in d['files']];assert len(dn)==len(set(dn));dep_total=0
for row in d['files']:dep_total+=len(check(A,row))
snapshot=parse((A/'snapshot_manifest.json').read_bytes());assert len(snapshot['files'])==16
for row in snapshot['files']:
 b=check(A/'source_snapshot',row);assert (C/'original_archive'/row['path']).read_bytes()==b
for n in ['PROOF.md','verify.py','verification.json','source_record.json','prior_report.json','source_provenance.json','turns.json','review/independent_checks.py','review/independent_results.json','review/review_summary.json']:
 assert (C/n).read_bytes()==(C/'original_archive'/n).read_bytes()
qual=(A/'primary_scope_family/SOURCE_PROOF_QUALIFICATIONS.md').read_bytes();assert sha(qual)=='69196e84de0d627b31b6f2a20a3745ba33048969cb93efba92a886bfedf8bc7e'
for n in ['README.md','SOURCE_AUDIT.md','review/REVIEW.md','pr_body.md']:assert (C/n).read_bytes().endswith(qual)
for n in ['SOURCE_AUDIT.md','review/REVIEW.md']:assert (C/'original_archive'/n).read_bytes() in (C/n).read_bytes()
for n in ['attempt.json','status.json','readiness.json','review/verdict.json']:
 o=objects[n];assert o['full_problem_solved'] is False and o['novelty_claimed'] is False and o['historical_verdict_transferred'] is False
 assert all(o[k] is None for k in ['current_model','current_reasoning_effort','current_deadline_utc','current_verdict'])
 assert type(o['original_substantive_attempts']) is int and o['original_substantive_attempts']==2 and o['substantive_attempt_limit']==5
 assert type(o['new_substantive_attempts']) is int and o['new_substantive_attempts']==0 and type(o['audit_turns']) is int and o['audit_turns']==0
 assert o['current_gate']=='pending_NEW_whole_current_packet_source_first_adversary'
card=objects['root_verification/ROOT_SCIENCE_CARD.json'];assert card['status']=='UNSOLVED' and card['partial_valid'] is True and len(card['root_flags'])==8 and all(v is True for v in card['root_flags'].values())
assert card['new_whole_current_gate']=='PENDING' and card['current_verdict'] is None
before=(C/'queue_proposal/QUEUE_PREIMAGE.md').read_bytes();after=(C/'queue_proposal/QUEUE_PROSPECTIVE.md').read_bytes();patch=objects['CURRENT_QUEUE_PATCH.json']
assert sha(before)==patch['whole_preimage_sha256'] and sha(after)==patch['whole_prospective_sha256']
assert before.count(patch['row_before'].encode())==1 and after.count(patch['row_prospective'].encode())==1
assert before.replace(patch['row_before'].encode(),patch['row_prospective'].encode(),1)==after
fields=[x.split('|') for x in [patch['row_before'],patch['row_prospective']]];assert all(fields[0][i]==fields[1][i] for i in range(14) if i not in {8,9,11})
cap=parse((A/'root_current_freeze_actual_capture/CAPTURE.json').read_bytes());assert cap['pid']==36236 and cap['exit_code']==0 and cap['status']=='PASS' and cap['actual_execution'] is True and cap['completed'] is True
assert cap['native13_and_HEAD_unchanged'] is True and eq(cap['fresh_native13_before'],cap['fresh_native13_after'])
for channel in ['stdout','stderr']:check(A/'root_current_freeze_actual_capture',cap[channel])
assert sha((A/'root_current_freeze_actual_capture/prelaunch_source.py').read_bytes())==cap['source_sha256']==sha((C/'build/prepare_current_packet.py').read_bytes())
receipt=objects['CURRENT_BUILD_RECEIPT.json'];assert receipt['fresh_root_approved_head']==cap['head_before']==cap['head_after'] and receipt['dated_actual_replay_head']=='33a08009b078d43c4e560c144cf75361bd0f4c0a'
result=dict(utc=dt.datetime.now(dt.timezone.utc).isoformat(),status='PASS',current_manifest_sha256=sha(manifest_raw),current_members=547,current_bytes=total,strict_complete_JSON_objects=len(objects)+1,dependency_manifest_sha256=sha((C/'CURRENT_PROOF_DEPENDENCIES.json').read_bytes()),dependencies=469,dependency_bytes=dep_total,
 root_full_current_scientific_read_completed=True,qualified_ancillary_sources_globally_current_and_archives_preserved=True,
 original16_and_immutable_science_exact=True,all_current_files_readonly=True,whole_prospective_queue_named_changes_only=True,
 actual_freeze_PID=36236,actual_freeze_capture_sha256=sha((A/'root_current_freeze_actual_capture/CAPTURE.json').read_bytes()),
 partial_valid=True,full_problem_solved=False,novelty_claimed=False,original_substantive_attempts=2,new_substantive_attempts=0,audit_turns=0,new_whole_current_gate='PENDING',current_verdict=None,paper_or_new_doi_or_tracker=False,
 scope='Root read new current presentation, exact source-qualified proof and complete retained typed bytes. Independent entire-current gate and actual acceptance remain pending; dated freeze inputs do not restrict future independently reviewed main rebases.')
with (A/'ROOT_CURRENT_PACKET_INSPECTION.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result))
