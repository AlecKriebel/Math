"""Root typed closure inspection, independent of reviewed helper execution."""
import datetime as dt
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import stat

R=Path('/Users/alec/Documents/Math')
A=R/'draft_pr_publication_program_20260930/audits/pr41_9700035'
F=A/'whole_current_source_first_family'
C=A/'reviewed_candidate'
def H(b): return hashlib.sha256(b).hexdigest()
def pairs(xs):
    d={}
    for k,v in xs:
        assert k not in d, k
        d[k]=v
    return d
def number(s):
    v=float(s); assert math.isfinite(v); return v
def constant(s): raise ValueError(s)
def J(b): return json.loads(b,object_pairs_hook=pairs,parse_float=number,parse_constant=constant)
def safe(n):
    p=PurePosixPath(n)
    assert type(n) is str and n and p.as_posix()==n and not p.is_absolute() and '\\' not in n and not set(p.parts)&{'.','..','.git','__pycache__'}
    return n
def member(root,z):
    p=root/safe(z['path']); assert p.is_file() and not p.is_symlink()
    b=p.read_bytes(); size=z.get('bytes',z.get('size'))
    assert type(size) is int and size>=0 and len(b)==size and H(b)==z['sha256'], str(p)
    return b
def closure(root,rows,self_name,foreign=()):
    names=[]; objects={}
    for z in list(rows)+list(foreign):
        n=safe(z['path']); assert n not in names; names.append(n)
        b=member(root,z); assert stat.S_IMODE((root/n).stat().st_mode)==0o444
        if n.endswith('.json'): objects[n]=J(b)
    expected=set(names)|{self_name}; actual=set(); dirs=set()
    for p in root.rglob('*'):
        assert not p.is_symlink()
        n=p.relative_to(root).as_posix()
        if p.is_file(): actual.add(n)
        else: assert p.is_dir(); dirs.add(n)
    assert actual==expected
    assert dirs=={p.as_posix() for n in expected for p in PurePosixPath(n).parents if p.as_posix()!='.'}
    assert stat.S_IMODE((root/self_name).stat().st_mode)==0o444
    return objects

raw=(F/'FIRST_PARTY_MANIFEST.json').read_bytes()
pin='233867cfb7e18b910f1ec17c9a57a386eadd1793ff3a44328260e204d8304130'
assert H(raw)==pin
m=J(raw); assert m['files_count']==len(m['files'])==143 and m['foreign_count']==len(m['foreign_files'])==17
assert m['excluded']==['FIRST_PARTY_MANIFEST.json'] and m['all_members_0444'] is True
objects=closure(F,m['files'],'FIRST_PARTY_MANIFEST.json',m['foreign_files'])
v=objects['RESULT.json']; assert H((F/'RESULT.json').read_bytes())==m['result_sha256']
assert H((F/'WHOLE_CURRENT_ADVERSARIAL_REVIEW.md').read_bytes())==m['report_sha256']
assert v['verdict']=='PASS_QUALIFIED_UNSOLVED_PARTIAL_NEW_WHOLE_CURRENT'
assert v['mandatory_repairs']==[] and v['partial_valid'] is True and v['review_completed'] is True
assert v['full_problem_solved'] is v['novelty_claimed'] is False
assert v['original_substantive_attempts']==2 and v['substantive_attempt_limit']==5 and v['new_substantive_attempts']==v['audit_turns']==0
capobjects=[]
for z in v['own_actual_capture_receipts']:
    cap=objects[z['path']]; assert H((F/z['path']).read_bytes())==z['sha256']
    assert cap['actual_execution'] is cap['completed'] is True and cap['stdin_supplied'] is False
    assert type(cap['pid']) is int and cap['pid']==z['pid']>0 and type(cap['returncode']) is int and cap['returncode']==z['exit_code']==0
    start,end=[dt.datetime.fromisoformat(cap[k]) for k in ['started_utc','finished_utc']]
    assert all(t.tzinfo and t.utcoffset()==dt.timedelta(0) for t in (start,end)) and start<=end
    src=member(F,cap['source']); assert src==Path(cap['argv'][2]).read_bytes()
    for field in ['stdout','stderr']: member(F,cap[field])
    assert cap['stdout']['path']!=cap['stderr']['path'] and cap['stderr'].get('bytes',cap['stderr'].get('size'))==0
    capobjects.append(cap)
assert len(capobjects)==5
mathresult=objects['INDEPENDENT_MATH_BOUNDARY_RESULTS.json']
assert mathresult['passed']==len(mathresult['checks'])==144 and mathresult['failed']==0
assert all(x['result']=='PASS' for x in mathresult['checks'])
currentraw=(C/'MANIFEST.json').read_bytes()
assert H(currentraw)==v['reviewed_current']['manifest_sha256']=='3431ca2dfb332500f3815ea1e61f089744b3bacd9c3659018537016b9396fbfa'
cm=J(currentraw); assert cm['files_count']==len(cm['files'])==547 and cm['self_excluded']==['MANIFEST.json']
co=closure(C,cm['files'],'MANIFEST.json'); assert len(co)==135
deps=co['CURRENT_PROOF_DEPENDENCIES.json']; assert deps['dependency_anchor_repository_relative']==A.relative_to(R).as_posix()
seen=set()
for z in deps['files']:
    assert z['path'] not in seen; seen.add(z['path']); member(A,z)
assert len(seen)==469
card=co['root_verification/ROOT_SCIENCE_CARD.json']; ledger=co['primary_evidence/ROOT_PRIMARY_READ_LEDGER.json']
assert card['root_flags']==ledger['root_flags'] and len(card['root_flags'])==8 and all(t is True for t in card['root_flags'].values())
assert ledger['reading_completed'] is True and card['full_problem_solved'] is False and card['partial_valid'] is True
assert H((A/'root_current_freeze_actual_capture/CAPTURE.json').read_bytes())==v['root_current_capture_sha256']
record=dict(schema='pr41-root-entire-closed-whole-current-review/v1',status='PASS',utc=dt.datetime.now(dt.timezone.utc).isoformat(),independent_family_manifest_sha256=pin,authored_members=143,separately_bound_foreign_members=17,whole_independent_verdict=v,entire_actual_capture_objects=capobjects,entire_independent_math_control_object=mathresult,current_members=547,current_manifest_sha256=H(currentraw),whole_dependency_members=469,root_full_report_and_result_read=True,root_full_proof_and_current_source_qualifications_read=True,root_independent_analytic_certificate=H((A/'ROOT_PARTIAL_SCOPE_CERTIFICATE.md').read_bytes()),exact_scientific_remaining_gap='The ordinary SIRSN axioms do not yet supply expected exterior all-pair route-union o(k); the tail hypothesis is additional, not proved from those axioms.',nonblocking_context_pointer_qualification='The inherited follows/appended-below summary phrases point to the exact SOURCE_PROOF_QUALIFICATIONS.md and four full operative current surfaces, not an embedded body in each summary.',full_problem_solved=False,partial_valid=True,positive_novelty_claim=False,original_substantive_attempts=2,new_substantive_attempts=0,audit_turns=0,current_accepted_or_future_gate_claimed=False,own_failed_inspector_qualification=dict(actual_pid=83631,exit_code=1,source='inspect_whole_current_review.py',capture='pr39_9500008/root_pr41_whole_inspection_actual_capture/CAPTURE.json',failure='Own checker expected bytes on one administrative capture whose exact schema uses size; complete member already verified with either declared schema. No record written or candidate/native mutation. V2 accepts only the declared integer size/bytes field.'))
with (A/'ROOT_WHOLE_CURRENT_REVIEW.json').open('x') as out:
    json.dump(record,out,indent=2);out.write('\n')
print(json.dumps(dict(status='PASS',authored_members=143,separately_bound_foreign_members=17,current_members=547,dependency_members=469,root_inspection_sha256=H((A/'ROOT_WHOLE_CURRENT_REVIEW.json').read_bytes()))))
