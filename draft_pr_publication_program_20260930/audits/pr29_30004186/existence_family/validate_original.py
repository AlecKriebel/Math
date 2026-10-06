#!/usr/bin/env python3
"""Read-only exact-head validation. Writes only inside this audit family."""
import hashlib,json,subprocess
from pathlib import Path
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
AUDIT=HERE.parent
HEAD='5ac4a57e08dd72a6f16768f2288b9c0349999431'
BASE='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
PREFIX='unsolved_math_prioritization/attempts/30004186/'
def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT)
def sha(b): return hashlib.sha256(b).hexdigest()
manifest=json.loads((AUDIT/'snapshot_manifest.json').read_text())
assert git('rev-parse',HEAD).decode().strip()==HEAD
assert git('merge-base',BASE,HEAD).decode().strip()==BASE
rows=[]
for record in manifest['files']:
    rel=record['path']; snapshot=(AUDIT/'source_snapshot'/rel).read_bytes()
    original=git('show',HEAD+':'+PREFIX+rel)
    blob=git('rev-parse',HEAD+':'+PREFIX+rel).decode().strip()
    raw_blob_sha=hashlib.sha1(b'blob '+str(len(original)).encode()+b'\0'+original).hexdigest()
    assert snapshot==original,rel
    assert sha(original)==record['sha256'],rel
    assert len(original)==record['bytes'],rel
    assert blob==record['git_blob_sha1']==raw_blob_sha,rel
    rows.append({'path':rel,'bytes':len(original),'sha256':sha(original),'git_blob_sha1':blob,'snapshot_equals_exact_head':True,'read_in_full':True})
assert len(rows)==16
paths=git('diff','--name-only',BASE,HEAD,'--').decode().splitlines()
assert paths==manifest['changed_paths']
assert len(paths)==17 and paths[0]=='unsolved_math_prioritization/QUEUE.md'
original_diff=git('diff',BASE,HEAD,'--')
frozen_diff=(AUDIT/'pr_input/diff.patch').read_bytes()
assert original_diff==frozen_diff
# All attempt files are new; parse and compare their complete addition bytes.
segments=frozen_diff.decode().split('diff --git ')[1:]
assert len(segments)==17
for segment in segments[1:]:
    header,*lines=segment.splitlines(keepends=True)
    path=header.strip().split(' b/',1)[1]
    content=''.join(line[1:] for line in lines if line.startswith('+') and not line.startswith('+++'))
    assert content.encode()==git('show',HEAD+':'+path),path
queue=git('show',HEAD+':unsolved_math_prioritization/QUEUE.md').decode()
queue_rows=[line for line in queue.splitlines() if '30004186 / OWR-17128-002' in line]
assert len(queue_rows)==1 and '| unsolved | 1/5 |' in queue_rows[0]
turns=json.loads((AUDIT/'source_snapshot/turns.json').read_text())
assert turns['limit']==5 and turns['used']==1 and len(turns['turns'])==1
assert turns['original_target_outcome']=='partial'
provenance=json.loads((AUDIT/'source_snapshot/provenance.json').read_text())
pr=json.loads((AUDIT/'pr_input/pr.json').read_text())
assert provenance['model']=='gpt-6-astra' and provenance['reasoning_effort']=='xhigh'
contradiction=(provenance['shared_queue_modified'] is False and
               'No shared queue/state/catalog edit' in pr['body'] and
               any(p.endswith('/QUEUE.md') for p in paths))
assert contradiction
receipt={'status':'PASS_EXACT_HEAD_WITH_HISTORICAL_SCOPE_CONTRADICTION',
         'utc':datetime.now(timezone.utc).isoformat(),'exact_head':HEAD,'base':BASE,
         'original_files':rows,'original_file_count':len(rows),'changed_paths':paths,
         'frozen_diff_sha256':sha(frozen_diff),'full_diff_bytes_match_readonly_git':True,
         'all_new_attempt_diff_additions_match_complete_original_bytes':True,
         'queue_row':queue_rows[0],'turn_ledger':turns,
         'historical_model_effort_attestation':{'model':provenance['model'],'effort':provenance['reasoning_effort'],'status':'Original metadata attestation only; not independent service telemetry.'},
         'historical_query_attestation':'Original readiness/source-audit report bounded searches; not a priority certificate and not independently reconstituted query telemetry.',
         'scope_contradiction':{'found':True,'original_provenance_shared_queue_modified':False,'original_body_denies_queue_edit':True,'exact_diff_queue_edit':True,'disposition':'Preserve original bytes; root must reconcile current PR metadata separately.'},
         'no_git_mutations':True,'script_sha256':sha(Path(__file__).read_bytes())}
(HERE/'ORIGINAL_VALIDATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in ['original_files','queue_row','turn_ledger','changed_paths']},indent=2))
