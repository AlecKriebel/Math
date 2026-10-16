"""Own finite drafting repair, with before/after bytes; no production source execution."""
from pathlib import Path
import json,hashlib,datetime,os,difflib
H=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
stamp=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
changes={
'pr43_guards.py':[("required(load(ps['previous_post']),{'status':'PASS','pr':43,'targets':34,","required(load(ps['previous_post']),{'status':'PASS','pr':42,'targets':33,"),("'Original17/18 snapshot'","'Original16/17 snapshot'"),("'Original17/18 counts'","'Original16/17 counts'")],
'integrate_reviewed_partial.py':[("Require postPR41 native32targets/39turns","Require postPR42 native33targets/41turns"),("Require31 complete primaries before42","Require32 complete primaries before43"),("UNSOLVED qualified partial","already_solved source-status partial"),("Original2/5","Original0/5")],
'state_mirror_reconciliation.py':[("Exactly32 primary completions","Exactly33 primary completions"),("Require32targets/39turns","Require33targets/41turns"),("Exactly33targets/41turns/32primary","Exactly34targets/41turns/33primary"),("Native original2/5 budget","Native original0/5 empty ledger budget")],
'verify_post_acceptance.py':[("Native present original2/5 budget","Native present original0/5 empty ledger budget")]
}
records=[];diff=[];old=H/'preserved_initial_authored_sources';old.mkdir(exist_ok=False)
for name,rr in changes.items():
    p=H/name;before=p.read_bytes();text=before.decode();(old/name).write_bytes(before)
    for x,y in rr:
        if x not in text:raise ValueError('Expected unique original drafting token absent: '+x)
        text=text.replace(x,y)
    after=text.encode();p.write_bytes(after)
    records.append({'path':name,'before_bytes':len(before),'before_sha256':sha(before),'after_bytes':len(after),'after_sha256':sha(after),'preserved_before':'preserved_initial_authored_sources/'+name})
    diff += list(difflib.unified_diff(before.decode().splitlines(True),text.splitlines(True),fromfile='initial/'+name,tofile='prepared/'+name))
(H/'OWN_DRAFT_REPAIR.patch').write_text(''.join(diff))
record={'schema':'pr43-own-source-drafting-correction/v1','created_utc':stamp(),'actual_child_pid':os.getpid(),'changed_files':records,'retained_initial_authoring_receipts_unchanged':True,'proposed_sources_imported_compiled_executed':False,'new_substantive_attempts':0,'audit_turns':0}
(H/'OWN_DRAFT_REPAIR.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))
