from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, stat
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
D=P/'verification/hafnian-retract-postpublication-sol-20261117'
O=P/'verification/root-hafnian-retract-postpublication-adoption-20261117.json'
assert not O.exists()
def sha(f): return hashlib.sha256(f.read_bytes()).hexdigest()
pins={'FINAL.json':'eaa8cbb17517366b826a3b07b619dc36435eb9ca5f8b579f6d3ba4b2232c1b53','OWNED_MANIFEST.json':'a0858e6b2f4b42d5145758f782180d3bf95953a0303f7ef348e01708d88aa7c1'}
for name,pin in pins.items(): assert sha(D/name)==pin
m=json.loads((D/'OWNED_MANIFEST.json').read_text())
rows={e['path']:e for e in m['payload_files']}
rows.update({name:{'path':name,'mode':mode} for name,mode in m['terminal_modes'].items()})
actual={str(f.relative_to(D)):f for f in D.rglob('*')}
assert set(rows)==set(actual) and len(actual)==12
assert stat.S_IMODE(D.stat().st_mode)==int(m['root_mode'],8)
authenticated=[]
for name,f in sorted(actual.items()):
    assert f.is_file() and not f.is_symlink()
    e=rows[name];data=f.read_bytes()
    assert stat.S_IMODE(f.stat().st_mode)==int(e['mode'],8)
    digest=hashlib.sha256(data).hexdigest()
    if 'SHA256' in e: assert digest==e['SHA256'] and len(data)==e['bytes']
    else: assert digest==pins[name]
    authenticated.append({'path':name,'bytes':len(data),'SHA256':digest,'mode':oct(stat.S_IMODE(f.stat().st_mode))})
final=json.loads((D/'FINAL.json').read_text())
assert final['status']=='PASS_FIXED_LOCAL_POSTPUBLICATION_AUDIT'
assert (D/'GUARDS_BEFORE.json').read_bytes()==(D/'GUARDS_AFTER.json').read_bytes()
assert sha(D/'GUARDS_AFTER.json')=='7e90889d171db47cb0c8132481577cfdbf4befcfb427ef9e6cadba4fd0901189'
assert final['literal_root_execution_history']['exits']==[1,0,0,0,0]
adoption={'UTC':datetime.now(timezone.utc).isoformat(),'status':'ACCEPTED_FIXED_LOCAL_POSTPUBLICATION_AUDIT','completion_percent':100,'root_personally_read':['Entire actual FINAL6191B','Entire REPORT3316B','Entire FINDINGS5285B and all12 claim rows','Actual finite custody schema'],'authenticated':authenticated,'commit':final['commit'],'parent':final['parent'],'tree':final['tree'],'all790files381dirs_and_native_index_exact':True,'old128HTML_and129XML_whole_prefix_and_full_reversal_exact':True,'all58719untargeted_raw_index_records_and_wholeTREE_semantics_exact':True,'eleven_selected_records_intentionally_zero_stat':True,'literal_failures_preserved':True,'actual_UI_certificate':False,'fresh_network_certificate':False,'all_production_helper_modes_stale':True,'AA_or_redirect_authority':False,'follow_up':None}
O.write_text(json.dumps(adoption,indent=2)+'\n')
progress=P/'PROGRESS.json';old_sha=sha(progress);x=json.loads(progress.read_text())
receipt='verification/sheet-hafnian-retract-deployed141-20261117/FINAL_READBACK.json'
sheet=json.loads((P/receipt).read_text());counts=sheet['counts'];assert sum(counts.values())==245
assert sheet['scientific_dispositions']==141 and sheet['remaining_scientific']==62
for key in ['full_goal_partition','latest_native_status_partition']:
    x[key]=counts
x['native_current_status_counts']={k:counts[k] for k in ['Published — verified','Deployed — verification pending','Reviewed — preparing page','In review — full manuscript','Queued — eligible Zenodo paper','Deferred — defect found']}
x['native_current_status_counts'].update({'Review holds':2,'Excluded':36,'Aliases':6})
assert sum(x['native_current_status_counts'].values())==245
for key,value in {'sheet_final_receipt':receipt,'sheet_status_receipt':receipt,'native_sheet_published_count':123,'native_verified_published_count':123,'native_sheet_reviewed_or_deferred_count':141,'actual_scientific_disposed_count':141,'native_sheet_preparing_count':3,'native_sheet_deployed_pending_count':7,'root_cleared_preparation_count':3,'scientific_review_completion_percent':141/203*100,'authoritative_current_native_queue':'reconciliation/current-native-queue-20261117-pass141-deployed130.json','website_actual_public_index_sitemap_counts':[790,130,131],'editorial_preparing_or_awaiting_root_record_ids':['23203081','23202994','23204176']}.items():x[key]=value
x['current_hafnian_retract_postpublication_adoption']={'path':str(O.relative_to(P)),'SHA256':sha(O),'status':adoption['status']}
x['current_k3_private_editorial_adoption']='verification/root-mixed-k3-moduli-editorial-adoption-20261117.json'
x['current_gram194_root_INITIAL']='papers/23318851/reviews/root-initial-20261117/INITIAL_SEAL.json'
x['updated_utc']=datetime.now(timezone.utc).isoformat()
x['note']='141/203 reviewed:133 passes,8 deferred,62 scientific reviews remain. Native Sheet123 verified,7 deployed pending actual UI,3 preparing,9 in review,51 queued,2 holds;36 excluded+6 aliases. W217d41c/live9d7f8c6526f4153b;790public/381dirs/130articles/131XML. Independent fixed local postpublication audit accepted;13 HTTPS whole-file checks pass. All seven AA cells remain blank; browser control unavailable, no visual certificate or redirect. Mink/Riesz/K3 private copy accepted; fresh batch staging active. Gram194 all three original-only INITIALs frozen; checkpoint and explicit primary/support continuation pending. Native Math main/index remain protected. Goal active and incomplete.'
progress.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
journal=P/'verification/root-progress141-current-field-reconciliation-20261117.json'
assert not journal.exists()
journal.write_text(json.dumps({'UTC':x['updated_utc'],'old_PROGRESS_SHA256':old_sha,'new_PROGRESS_SHA256':sha(progress),'authority':receipt,'reason':'Reconcile current summary aliases with latest bounded native status readback; retain historical named records','scientific_dispositions':141,'percent':141/203*100,'goal_complete':False,'postpublication_adoption_SHA256':sha(O)},indent=2)+'\n')
print(json.dumps({'status':adoption['status'],'files_authenticated':12,'adoption_SHA256':sha(O),'scientific_dispositions':141,'percent':141/203*100,'current_progress_fields_reconciled':True}))
