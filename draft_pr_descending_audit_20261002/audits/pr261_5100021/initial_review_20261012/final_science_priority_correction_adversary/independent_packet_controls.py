"""Local byte/integrity and exact-change audit, no operational utility import/execution."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,difflib,collections
out=Path(__file__).resolve().parent;N=out.parent;prep=N/'credited_correction_preparation';cand=prep/'candidate';sub=N/'submitted'
attempt=Path('unsolved_math_prioritization/attempts/5100021');c=cand/attempt;s=sub/attempt;h=c/'historical_submission_20261001'
def pin(p):
 raw=p.read_bytes();return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'git_blob_oid':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}
def match(p,r):
 got=pin(p)
 for key in ('bytes','sha256','git_blob_oid'):
  if key in r:assert got[key]==r[key],(str(p),key,got[key],r[key])
 return got
# All historical bodies correspond to exact submitted bytes, no wrappers inside history.
old={str(p.relative_to(s)):p for p in s.rglob('*') if p.is_file()};hist={str(p.relative_to(h)):p for p in h.rglob('*') if p.is_file()}
assert len(old)==len(hist)==25 and set(old)==set(hist)
for name in old:assert old[name].read_bytes()==hist[name].read_bytes()
fm=json.loads((h/'FROZEN_MANIFEST.json').read_text());rm=json.loads((h/'independent_review/REVIEW_MANIFEST.json').read_text())
for e in fm['files']:match(h/e['path'],e)
for name,e in rm['files'].items():match(h/'independent_review'/name,e)
assert pin(h/'PROOF.md')['sha256']==rm['author_proof_sha256'];assert pin(h/'FROZEN_MANIFEST.json')['sha256']==rm['author_manifest_sha256']
# Current manifest verifies all 40 nonmanifest current+historical files, with 15 current bodies.
vm=json.loads((c/'VERIFICATION_MANIFEST.json').read_text());current={str(p.relative_to(c)):p for p in c.iterdir() if p.is_file()}
all_attempt={str(p.relative_to(c)) for p in c.rglob('*') if p.is_file()}
assert len(current)==16 and set(vm['files'])==all_attempt-{'VERIFICATION_MANIFEST.json'}
for name,e in vm['files'].items():match(c/name,e)
assert set(vm['historical_original_path_pins'])==set(old)
for name,e in vm['historical_original_path_pins'].items():match(h/name,e)
for e in vm['external_current_evidence_pins']:match(Path(e['path']),e)
for name in vm['unchanged_current_author_files']:assert (c/name).read_bytes()==(s/name).read_bytes()
# All changes and preserved/deleted paths independently reconstructed; hash computations do not invoke Git.
change=json.loads((prep/'AUTHOR_EXACT_CHANGE_MAP.json').read_text());seen=set();op=collections.Counter()
expectedpaths={str(p.relative_to(sub)) for p in sub.rglob('*') if p.is_file()}|{str(p.relative_to(cand)) for p in cand.rglob('*') if p.is_file()}
assert len(change['entries'])==57
for e in change['entries']:
 name=e['repository_path'];assert name not in seen;seen.add(name);before=sub/name;after=cand/name;operation=e['operation'];op[operation]+=1
 if 'before' in e:match(before,e['before'])
 else:assert not before.exists()
 if 'after' in e:match(after,e['after'])
 else:assert not after.exists()
 if operation=='unchanged':assert before.read_bytes()==after.read_bytes()
 if operation=='remove_from_current_view':assert before.read_bytes()==(cand/e['byte_preserved_at']).read_bytes()
 assert name=='unsolved_math_prioritization/QUEUE.md' or name.startswith(str(attempt)+'/')
assert seen==expectedpaths
# Single QUEUE line and precisely two semantic columns changed; all surrounding bytes identical.
q0=(sub/'unsolved_math_prioritization/QUEUE.md').read_bytes();q1=(cand/'unsolved_math_prioritization/QUEUE.md').read_bytes();l0=q0.splitlines(keepends=True);l1=q1.splitlines(keepends=True)
assert len(l0)==len(l1);changed=[i for i,(a,b) in enumerate(zip(l0,l1)) if a!=b];assert len(changed)==1
idx=changed[0];oldcols=l0[idx].decode().strip().split('|');newcols=l1[idx].decode().strip().split('|');changedcols=[i for i,(a,b) in enumerate(zip(oldcols,newcols)) if a!=b];assert changedcols==[8,11]
assert oldcols[8].strip()=='claimed_solved' and newcols[8].strip()=='already_solved' and oldcols[9]==newcols[9] and newcols[9].strip()=='1/5'
qc=json.loads((prep/'QUEUE_CHANGE.json').read_text());match(sub/'unsolved_math_prioritization/QUEUE.md',qc['before']);match(cand/'unsolved_math_prioritization/QUEUE.md',qc['after'])
assert qc['before_row']==l0[idx].decode().strip() and qc['after_row']==l1[idx].decode().strip()
# Mathematical display equations exactly unchanged; disclosed wording map reconstructs pre-append body.
orig=(s/'PROOF.md').read_text();now=(c/'PROOF.md').read_text();displays=lambda x:re.findall(r'\$\$([\s\S]*?)\$\$',x)
assert displays(orig)==displays(now)
em=json.loads((prep/'PROOF_EDIT_MAP.json').read_text());reconstructed=orig
for e in em['replacements']:
 assert reconstructed.count(e['old'])==1;reconstructed=reconstructed.replace(e['old'],e['new'])
assert reconstructed.rstrip()==now.split('## 8. Earlier proof, current contribution and disclosure')[0].rstrip()
assert len(em['replacements'])==6
# Literal/qualified target statement digest independently checks.
target=json.loads((c/'TARGET.json').read_text());oldtarget=json.loads((s/'TARGET.json').read_text())
assert target['literal_imported_statement']==oldtarget['exact_target']
for field in ('literal_imported_statement','qualified_proved_target'):assert hashlib.sha256(target[field].encode()).hexdigest()==target[field+'_sha256']
assert target['current_disposition']=='already_solved' and 'least period' in target['qualified_proved_target'] and 'signed' in target['qualified_proved_target']
status=json.loads((c/'CURRENT_STATUS.json').read_text());assert status['current_mathematical_disposition']=='already_solved' and status['original_substantive_author_turns']==1 and status['author_turns_added_by_audit_correction']==0
assert status['intended_operational_disposition']=='Retain OPEN/DRAFT; no native merge or closure in this correction.'
for key in ('new_DOI','new_Zenodo_deposit','paper_prepared','paper_tracker_row'):assert status[key] is False
# Preparation workflow fields are scoped and dated, so frozen bodies do not falsely claim perpetual state.
assert status['correction_preparation_snapshot']['observed_utc']==status['prepared_utc'];assert 'supersede' in status['correction_preparation_snapshot']['scope_note']
assert vm['preparation_workflow_snapshot']['observed_utc']==vm['prepared_utc'] and 'supersede' in vm['preparation_workflow_snapshot']['scope_note']
metadata=json.loads((prep/'PR_METADATA_DRAFT.json').read_text());assert metadata['body']==(prep/'PR_BODY.md').read_text();assert metadata['title']==(prep/'PR_TITLE.txt').read_text().strip();assert metadata['intended_state']=='OPEN' and metadata['intended_draft'] and not metadata['native_merge'] and not metadata['closure']
source=json.loads((c/'source_manifest.json').read_text())
for e in source['current_review_report_pins']:match(Path(e['path']),e)
# Pin whole exact candidate and draft controls after successful checks.
pins={str(p.relative_to(N)):pin(p) for p in cand.rglob('*') if p.is_file()}
for name in ('AUTHOR_EXACT_CHANGE_MAP.json','PREPARATION_RECEIPT.json','PROOF_EDIT_MAP.json','PROOF_WORDING_DIFF.patch','QUEUE_CHANGE.json','PR_BODY.md','PR_TITLE.txt','PR_METADATA_DRAFT.json'):pins[str((prep/name).relative_to(N))]=pin(prep/name)
result={'UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS_LOCAL_CANDIDATE_SCIENCE_AND_INTEGRITY_ONLY','candidate_files':len(pins)-8,'current_attempt_files':len(current),'historical_bodies_byte_preserved':len(hist),'original_author_manifest_records':len(fm['files']),'original_review_manifest_records':len(rm['files']),'external_current_manifest_evidence_pins_checked':len(vm['external_current_evidence_pins']),'change_map_entries':len(seen),'change_operations':dict(op),'queue_changed_line_one_based':idx+1,'queue_changed_column_indices':changedcols,'author_budget':'1/5','unchanged_display_math_blocks':len(displays(orig)),'exact_disclosed_wording_replacements':len(em['replacements']),'full_candidate_and_draft_pins':pins,'no_remote_or_Git_operations':True,'no_publisher_execution_authority':True,'pending_or_remote_state_wording':'All frozen workflow observations explicitly dated, with later Root/provider receipts superseding them.'}
(out/'INDEPENDENT_PACKET_CONTROLS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='full_candidate_and_draft_pins'},indent=2))
