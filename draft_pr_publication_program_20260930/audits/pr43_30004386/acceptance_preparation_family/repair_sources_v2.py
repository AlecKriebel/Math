"""Preserve initial author bytes and failed partial repair; validate before new edits."""
from pathlib import Path
import json,hashlib,datetime,os,difflib
H=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
stamp=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
changes={
'pr43_guards.py':[("required(load(ps['previous_post']),{'status':'PASS','pr':43,'targets':34,","required(load(ps['previous_post']),{'status':'PASS','pr':42,'targets':33,"),("'Original17/18 snapshot'","'Original16/17 snapshot'"),("'Original17/18 counts'","'Original16/17 counts'")],
'integrate_reviewed_partial.py':[("Require postPR41 native32targets/39turns","Require postPR42 native33targets/41turns"),("Require31 complete primaries before42","Require32 complete primaries before43"),("original2/5","original0/5")],
'state_mirror_reconciliation.py':[("Exactly32 primary completions","Exactly33 primary completions"),("Require32targets/39turns","Require33targets/41turns"),("Exactly33targets/41turns/32primary","Exactly34targets/41turns/33primary"),("Native original2/5 budget","Native original0/5 empty ledger budget")],
'verify_post_acceptance.py':[("Native present original2/5 budget","Native present original0/5 empty ledger budget")]
}
old=H/'preserved_initial_authored_sources';failed=H/'preserved_failed_repair_current_sources';failed.mkdir(exist_ok=False)
anchors={z['path'].split('/')[-1]:z for z in json.loads((H/'AUTHORING_RESULT.json').read_bytes())['prepared_members']}
prepared=[];records=[];diff=[]
for name,rr in changes.items():
    current=(H/name).read_bytes();(failed/name).write_bytes(current)
    initial=(old/name).read_bytes() if (old/name).exists() else current
    if sha(initial)!=anchors[name]['sha256'] or len(initial)!=anchors[name]['bytes']:raise ValueError('Exact initial author bytes required')
    if not (old/name).exists():(old/name).write_bytes(initial)
    text=initial.decode()
    for x,y in rr:
        if x not in text:raise ValueError('Expected original drafting token absent: '+x)
        text=text.replace(x,y)
    after=text.encode();prepared.append((name,after))
    records.append({'path':name,'initial_bytes':len(initial),'initial_sha256':sha(initial),'before_corrected_repair_bytes':len(current),'before_corrected_repair_sha256':sha(current),'after_bytes':len(after),'after_sha256':sha(after),'preserved_initial':'preserved_initial_authored_sources/'+name,'preserved_after_failure':'preserved_failed_repair_current_sources/'+name})
    diff+=list(difflib.unified_diff(initial.decode().splitlines(True),text.splitlines(True),fromfile='initial/'+name,tofile='prepared/'+name))
for name,after in prepared:(H/name).write_bytes(after)
(H/'OWN_DRAFT_REPAIR.patch').write_text(''.join(diff))
record={'schema':'pr43-own-source-drafting-correction/v2','created_utc':stamp(),'actual_child_pid':os.getpid(),'changed_files':records,'retained_initial_authoring_and_failed_receipts_unchanged':True,'failed_V1_reason':'One message token had already been corrected during initial authoring. V1 stopped after the guard file edit and before integration edit; every observed partial current body is preserved. V2 validates all original anchors and drafting tokens before writes.','proposed_sources_imported_compiled_executed':False,'new_substantive_attempts':0,'audit_turns':0}
(H/'OWN_DRAFT_REPAIR.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))
