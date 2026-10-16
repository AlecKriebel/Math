#!/usr/bin/env python3
"""ROOT actual prerequisite authoring after complete personal source/math reading.

This approves only corrected unresolved science and current administrative
freezing. Neither a future whole-current verdict nor acceptance is asserted.
Native bodies are read in place. Outputs and real Git captures are exclusive.
"""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

A=Path(__file__).absolute().parent
R=A.parents[2]
F=A/'current_preparation_family_v2'
S=A/'current_source_adversary_family_v2'
T=dt.datetime.now(dt.timezone.utc).isoformat()
assert __debug__ and not os.environ.get('PYTHONOPTIMIZE')
assert R==Path('/Users/alec/Documents/Math') and A.name=='pr47_2849'
assert not (A/'reviewed_candidate').exists()

def sha(b): return hashlib.sha256(b).hexdigest()
def read(p):
    assert not p.is_symlink() and not any(q.is_symlink() for q in p.parents)
    assert stat.S_ISREG(p.stat().st_mode)
    return p.read_bytes()
def obj(p): return json.loads(read(p))
def row(n):
    b=read(A/n)
    return {'path':n,'bytes':len(b),'sha256':sha(b)}
def save(n,v):
    b=v.encode() if type(v) is str else (json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
    with (A/n).open('xb') as h: h.write(b);h.flush();os.fsync(h.fileno())
    return sha(b)

assert sha(read(F/'PREPARATION_MANIFEST.json'))=='da314f40d628606f8e80cc198c3ab4a94b71554e929f70c63fce31cc195def10'
assert sha(read(F/'prepare_current_packet.py'))=='5d0f9c7206043e0503acf1212832ae05d85d670f2d37d9894ab3af3b1071c6c3'
assert sha(read(F/'capture_root_builder_operation.py'))=='d27aff28ae71be91e2e5774dcc884f99394e747b46ee22558102701660387af0'
assert sha(read(S/'SELF_MANIFEST.json'))=='3312457f63a076a55974e94fc8cd6a93e860007e33b992dd3546a418f1170524'
assert sha(read(S/'REPORT.md'))=='3ef1efc066823072128f7cc206400af0800fe98d72524dc3b38c787468e19c08'
sm=obj(S/'SELF_MANIFEST.json')
assert sm['files_count']==len(sm['files'])==263 and sm['actual_closing_child_pid']==48213
assert sm['self_excluded']==['SELF_MANIFEST.json'] and sm['closed_clean'] is True
assert sm['future_acceptance_approved'] is False and sm['current_freeze_or_merge_approved'] is False
actual_files=set();actual_dirs=set()
for p in S.rglob('*'):
    assert not p.is_symlink()
    n=p.relative_to(S).as_posix()
    if p.is_file():actual_files.add(n)
    else:assert stat.S_ISDIR(p.stat().st_mode);actual_dirs.add(n)
assert actual_files=={r['path'] for r in sm['files']}|{'SELF_MANIFEST.json'}
assert actual_dirs==set(sm['directories']) and len(actual_dirs)==93
for r in sm['files']:
    b=read(S/r['path'])
    assert len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE((S/r['path']).stat().st_mode)==r['full_mode']==0o444
assert stat.S_IMODE((S/'SELF_MANIFEST.json').stat().st_mode)==0o444
verdict=obj(S/'VERDICT.json')
assert verdict['mandatory_corrections']==[] and verdict['review_scope']=='SOURCE_ONLY'
assert verdict['future_acceptance_approved'] is False
external=[]
for name,pid in [('root_pr47_source_v2_closure_actual_capture',32176),('root_pr47_source_v2_closed_readback_actual_capture',32684),('root_pr47_source_v2_adversary_closure_actual_capture',48213),('root_pr47_source_v2_adversary_closed_readback_actual_capture',48451)]:
    d=A.parent/'pr45_9900007'/name;c=obj(d/'CAPTURE.json')
    assert set(q.name for q in d.iterdir())=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'}
    assert c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']==pid
    assert type(c['exit_code']) is int and c['exit_code']==0 and c['stdin_supplied'] is False and c['operator_unchanged'] is True
    start=dt.datetime.fromisoformat(c['started_utc']);end=dt.datetime.fromisoformat(c['finished_utc'])
    assert start.utcoffset()==end.utcoffset()==dt.timedelta(0) and start<end<=dt.datetime.fromisoformat(T)
    assert sha(read(d/'prelaunch_operator.py'))==c['operator_sha256']
    for ch in ['stdout','stderr']:
        b=read(d/c[ch]['path']);assert len(b)==c[ch]['bytes'] and sha(b)==c[ch]['sha256']
    assert not read(d/'stderr.bin')
    value=json.loads(read(d/'stdout.bin'))
    expected='3312457f63a076a55974e94fc8cd6a93e860007e33b992dd3546a418f1170524' if 'adversary' in name else 'da314f40d628606f8e80cc198c3ab4a94b71554e929f70c63fce31cc195def10'
    assert value['manifest_sha256']==expected
    external.append({'directory':d.relative_to(R).as_posix(),'entire_actual_capture':c,'entire_stdout_value':value,'members':[{'path':q.relative_to(R).as_posix(),'bytes':len(read(q)),'sha256':sha(read(q)),'full_mode':stat.S_IMODE(q.stat().st_mode)} for q in sorted(d.iterdir())]})
assert dt.datetime.fromisoformat(external[2]['entire_actual_capture']['started_utc'])<=dt.datetime.fromisoformat(sm['created_utc'])<=dt.datetime.fromisoformat(external[2]['entire_actual_capture']['finished_utc'])<dt.datetime.fromisoformat(external[3]['entire_actual_capture']['started_utc'])
for r in obj(S/'INPUT_BINDINGS.json')['files']:
    p=R/r['path'];b=read(p)
    assert len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==r['full_mode']
source_record=obj(F/'DRAFT_ROOT_NEW_SOURCE_ADVERSARY_RECORD.json')
source_record.update(approved_by_root=True,created_utc=T,complete_report_personally_read=True,new_different_source_adversary=True,closed_clean=True,mandatory_corrections=[],preparation_manifest_sha256=sha(read(F/'PREPARATION_MANIFEST.json')),builder_sha256=sha(read(F/'prepare_current_packet.py')),operator_sha256=sha(read(F/'capture_root_builder_operation.py')),manifest=row('current_source_adversary_family_v2/SELF_MANIFEST.json'),report=row('current_source_adversary_family_v2/REPORT.md'),members=[{k:(('current_source_adversary_family_v2/'+r[k]) if k=='path' else r[k]) for k in ['path','bytes','sha256']} for r in sm['files']],entire_source_verdict=verdict,complete_external_closing_and_readback_evidence=external,production_executed=False,current_whole_verdict=None,future_acceptance_approved=False,reconciled_limits=['Dot spelling is lexically admitted but actual topology/regular file guards reject its operative use.','Consumed read/science fields are constrained; ROOT supplies exact drafts and no invented extra approval.','149840 assertions include receipt traversal; no production execution or new mathematics is inferred.','SOURCE reviewer did not freshly rerun foreign raw/SQL or authenticate PDF bytes; ROOT genuine prior audit remains the evidence.','Actual final original inner commands/full streams and outer completion remain later ROOT work.'])
save('ROOT_NEW_SOURCE_ADVERSARY_RECORD.json',source_record)
scope='''# ROOT PR47 corrected unresolved scope acceptance

ROOT_SCOPE_ACCEPTED_CORRECTED_UNRESOLVED_ONLY

PR47 / 2849 / KP-3.51
Original head: 487327b2412c436ae69e8c52bf353a9a1fb7594e
Original GitHub base and merge base: c6975ca76f9f667f1250ba403d0e6da2aafe14d0
Status: unsolved
Original turns: 1/5; new: 0; audit: 0
Universal normal vanishing: false
Realized example instanton rank: unknown
Full problem solved: false
Novelty: false
NEW whole-current review: PENDING
Paper/new DOI/tracker: false

The known Sivek–Zentner menagerie Proposition6.1 example
Y=S²((3,1),(3,1),(3,2)) has H1=C3⊕C12, all SU2 images abelian,
complex normal H1 dimension1, real adjoint dimension2, and a regular
three-cover with b1=2. This blocks universal normal vanishing, not KP3.51.
Its framed instanton rank is not computed. Actual degenerate Floer
contributions/differentials or a sufficient bypass remain the exact gap.
The finite-character orbit count, square weights, unrealized quartic and
credited trefoil6 rank calculation remain valid in their limited scopes.
The auxiliary torus-knot diagnosis concerns only arXiv2608.20551v1.

ROOT has personally read all16 scientific originals, full17-path diff,
helpers/results/metadata, exact K3 and credited primary theorem statements,
both closed independent mathematical reports and constructions, complete
genuine raw/SQL audit and114/114/100 reproductions, scoped original custody,
V1 adverse source evidence, corrected269-line V2 builder/operator/contract,
global qualifications and the entire new different clean SOURCE report.
All263 closed source-review members,1158 fixed bindings, actual source
closure/readback streams and chronology have now been fully checked.
Saved null is an absence marker; upstream key ABSENT and SQLite {} differ.
Legacy primary-byte/pixel claims are attributed; ROOT does not invent fresh
PDF authentication. Identical114 is duplicate, not independent evidence.
SOURCE dot/extra-key limits remain explicitly qualified. This certificate
approves only corrected unresolved science and administrative prerequisites;
actual final inner/outer evidence, new whole-current review and fresh final
integration authority remain separate pending gates. Extensive AI use;
unrefereed, no human peer review or formal certification claim.
'''
scope_sha=save('ROOT_CURRENT_SCOPE_CERTIFICATE.md',scope)
evidence=obj(F/'DRAFT_ROOT_EVIDENCE_BINDINGS.json')
evidence.update(approved_by_root=True,created_utc=T,notes='ROOT personally completed original mathematical and primary-text reconstruction, full raw/SQL and unchanged reproduction review, two independent mathematical families and the entire newly closed different clean V2 SOURCE report; actual current freeze and whole-current acceptance remain pending.',manifest=row('root_original_actual_reproduction/MANIFEST.json'),proof_notes=row('ROOT_MATHEMATICAL_REVIEW.md'),summary=row('root_original_actual_reproduction/ROOT_CURRENT_REPRODUCTION_SUMMARY.json'),raw_audit=row('ROOT_COMPLETE_RAW_SQL_AUDIT.json'),source_adversary=row('ROOT_NEW_SOURCE_ADVERSARY_RECORD.json'))
evidence_sha=save('ROOT_EVIDENCE_BINDINGS.json',evidence)
C=A/'root_current_prerequisite_Git_actual_captures';C.mkdir(exist_ok=False)
git_records=[]
def git(*args):
    d=C/str(len(git_records));d.mkdir(exist_ok=False)
    c={'argv':['git',*args],'cwd':str(R),'started_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_execution':False,'completed':False,'stdin_supplied':False,'pid':None,'exit_code':None,'source':None,'source_unchanged':None}
    with (d/'stdout.bin').open('xb') as out,(d/'stderr.bin').open('xb') as err:
        child=subprocess.Popen(c['argv'],cwd=R,stdin=subprocess.DEVNULL,stdout=out,stderr=err,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'));c.update(actual_execution=True,pid=child.pid)
        c['exit_code']=child.wait(timeout=60);c['completed']=True
    c['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
    for ch in ['stdout','stderr']:
        b=read(d/(ch+'.bin'));c[ch]={'path':ch+'.bin','bytes':len(b),'sha256':sha(b)}
    (d/'CAPTURE.json').write_text(json.dumps(c,indent=2)+'\n');git_records.append(c)
    assert c['exit_code']==0 and not read(d/'stderr.bin')
    return read(d/'stdout.bin')
assert git('branch','--show-current').strip()==b'main'
head=git('rev-parse','HEAD').decode().strip()
native=['unsolved_math_prioritization/'+n for n in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']]+['draft_pr_publication_program_20260930/inventory.json']
native_rows=[]
for n in sorted(native):
    b=read(R/n);native_rows.append({'path':n,'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE((R/n).stat().st_mode)})
for n in ['unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl','draft_pr_publication_program_20260930/inventory.json']:
    assert git('show',head+':'+n)==read(R/n)
assert git('rev-parse','HEAD').decode().strip()==head
fresh=obj(F/'DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json')
fresh.update(approved_by_root=True,created_utc=T,reason='Actual complete live13 bodies/full modes and committed native4 match this dated main HEAD; this authorizes only corrected V2 administrative freezing, with new whole-current review and fresh final acceptance authority still required.',current_head=head,files=native_rows)
fresh_sha=save('ROOT_CURRENT_INPUT_PREIMAGES.json',fresh)
reading=obj(F/'DRAFT_ROOT_READ_LEDGER.json')
reading.update(reading_completed=True,root_flags={k:True for k in reading['root_flags']},created_utc=T,reading_notes='ROOT completed each exact reading flag across its genuine mathematical notes, complete prior primary-text/whole raw SQL and actual original reproduction, both independent constructions, scoped closure history, V1 adverse and V2 corrected source, global qualifications, and the full newly closed different SOURCE report with actual completed closure/readback evidence. No future current or merge verdict is asserted.',scope_certificate_sha256=scope_sha,preparation_manifest_sha256=sha(read(F/'PREPARATION_MANIFEST.json')),source_qualification_sha256=sha(read(F/'SOURCE_PRECISION_QUALIFICATIONS.md')),evidence_bindings_sha256=evidence_sha,family_manifest_sha256={k:v['manifest']['sha256'] for k,v in obj(F/'STATIC_INPUT_BINDINGS.json')['groups'].items() if k!='original'})
ledger_sha=save('ROOT_PRIMARY_READ_LEDGER.json',reading)
science=obj(F/'DRAFT_ROOT_SCIENCE_CARD.json')
science.update({k:v for k,v in reading.items() if k!='schema'})
science.update(current_input_manifest_sha256=fresh_sha,read_ledger_sha256=ledger_sha)
save('ROOT_SCIENCE_CARD.json',science)
for r in native_rows:
    assert sha(read(R/r['path']))==r['sha256'] and stat.S_IMODE((R/r['path']).stat().st_mode)==r['full_mode']
assert git('rev-parse','HEAD').decode().strip()==head
print(json.dumps({'status':'PASS_ROOT_GENUINE_PR47_V2_PREREQUISITES_AUTHORED','created_utc':T,'current_head':head,'five_prerequisites':[row(n) for n in ['ROOT_CURRENT_SCOPE_CERTIFICATE.md','ROOT_PRIMARY_READ_LEDGER.json','ROOT_SCIENCE_CARD.json','ROOT_CURRENT_INPUT_PREIMAGES.json','ROOT_EVIDENCE_BINDINGS.json']],'source_record':row('ROOT_NEW_SOURCE_ADVERSARY_RECORD.json'),'new_whole_current_review':'PENDING','future_acceptance_approved':False},indent=2))
