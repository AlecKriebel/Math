#!/usr/bin/env python3
"""One separately approved, previously unattempted body PATCH; no ref retry."""
from pathlib import Path
import hashlib, json, sys, types, datetime
HERE=Path(__file__).absolute().parent
CASE=HERE.parent
source=(HERE/'update_package.py').read_bytes()
assert hashlib.sha256(source).hexdigest()=='e32d5a12d08f6c7331070e2a5e7368aec5c1a44f6e1e8d2bef2623df9afb8ebf'
m=types.ModuleType('pr411_body_recovery_pinned_helper');m.__file__=str(HERE/'update_package.py');sys.modules[m.__name__]=m;exec(compile(source,m.__file__,'exec'),m.__dict__)
plan=json.loads((HERE/'ROOT_ACTUAL_UPDATE_PLAN_V2.json').read_text())
assert m.sha(m.encoded(plan))=='aeb7023a1d7812294b34f8edb687f246d22fb834b111dabbd564680ab9d35f9a'
original_journal=HERE/'ROOT_ACTUAL_UPDATE_JOURNAL_V2.json'
old=json.loads(original_journal.read_text()); original=Path(old['evidence_dir'])
intents=[json.loads(p.read_text()) for p in sorted(original.glob('*_intent.json'))]
assert sum(x['record']['method']=='PATCH' and x['record']['endpoint']==f'pulls/{m.PR}' for x in intents)==0
refs=[x for x in intents if x['record']['method']=='PATCH' and x['record']['endpoint']=='git/refs/heads/'+m.BRANCH]
assert len(refs)==1 and refs[0]['payload']=={'sha':plan['commit_sha'],'force':False}
index=refs[0]['record']['index'];native=json.loads((original/f'{index:04d}_native.json').read_text());response=json.loads((original/f'{index:04d}_response.json').read_text())
assert native['returncode']==0 and response['object']['sha']==plan['commit_sha'] and json.loads(native['stdout'])==response
reconciliation=CASE/'private_sources/package_update_preparation/20261013T034103Z_1d301552246e4b8fa774fab665a09fb1/RESULT.json'
r=json.loads(reconciliation.read_text());assert r['status']=='branch_confirmed_body_pending' and r['read_only'] is True and r['observed_head']==plan['commit_sha'] and r['journal_sha256']==m.sha(original_journal.read_bytes()) and r['observed_body_sha256']==plan['source']['body_sha256']
body=(CASE/'publication_package/PR_BODY_PREPARED.md').read_bytes();assert m.sha(body)==plan['body_sha256']
root_approval={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'authorize_one_previously_unattempted_body_only_PATCH':True,'approved_plan_sha256':m.sha(m.encoded(plan)),'original_confirmed_ref_response_sha256':m.sha((original/f'{index:04d}_response.json').read_bytes()),'actual_read_only_all99_reconciliation_sha256':m.sha(reconciliation.read_bytes()),'science_head':plan['commit_sha'],'body_sha256':plan['body_sha256'],'no_ref_retry':True}
m.durable(HERE/'ROOT_BODY_ONLY_RECOVERY_APPROVAL.json',root_approval,exclusive=True)
journal=HERE/'ROOT_BODY_ONLY_RECOVERY_JOURNAL.json'
e=m.Engine(m.Native(),CASE/'private_sources/package_update_preparation/root_body_only_recovery_20261013T0343',journal)
e.state={'phase':'root_body_only_prepared','original_journal_sha256':m.sha(original_journal.read_bytes()),'approval_sha256':m.sha(m.encoded(root_approval)),'plan_sha256':m.sha(m.encoded(plan)),'plan':plan,'evidence_dir':str(e.evidence_dir)}
m.durable(journal,e.state,exclusive=True)
gate=e.gate(plan['commit_sha'],plan['source']['body_sha256'],plan['source']['title_sha256']);assert gate['root_tree']==plan['root_tree'];e.verify_commit(plan)
response=e.call('PATCH',f'pulls/{m.PR}',{'body':body.decode()});assert m.sha((response.get('body') or '').encode())==plan['body_sha256']
e.state['phase']='body_response_confirmed_native_readback_pending';e.save()
gate=e.gate(plan['commit_sha'],plan['body_sha256'],plan['source']['title_sha256']);assert gate['root_tree']==plan['root_tree']
e.state['phase']='confirmed_complete_body_only_recovery';e.save()
result={'status':'confirmed_complete','evidence_kind':'native_gh_api','science_head':plan['commit_sha'],'body_sha256':plan['body_sha256'],'root_tree':plan['root_tree'],'packet_files':99,'native_files_verification':'Actual GET-only original reconciliation verified all99 files/modes and deterministic preservation; unchanged immutable commit/tree additionally confirmed before and after body PATCH','one_ref_PATCH_original_response_confirmed':True,'one_body_PATCH_here_response_and_readback_confirmed':True,'original_apply_stop':'Immediate original PR GET still showed old head, while actual Git ref/PATCH showed new head; original journal retained without retry','ref_retry_count':0,'original_reconciliation_sha256':m.sha(reconciliation.read_bytes()),'private_custody_dir':str(e.evidence_dir),'production_stage_publish_append_merge':0}
m.durable(e.evidence_dir/'RESULT.json',result,exclusive=True,private=True)
m.durable(HERE/'ROOT_ACTUAL_UPDATE_CONFIRMATION.json',result,exclusive=True)
print(json.dumps(result,sort_keys=True))
