"""Canonical-gate/native02 offline-only tests. Never imports operational helpers."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from datetime import datetime,timezone
import copy,hashlib,importlib.util,json
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('native02',P/'make_native.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
R=P/'fixtures/SYNTHETIC_CASE'
R.mkdir(parents=True,exist_ok=True)
records=[]
def check(ok,label):
    if not ok:raise RuntimeError(label)
def write(name,data):
    q=R/name;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
def pin(name):
    b=(R/name).read_bytes();return {'path':name,**m.byte_pin(b)}
def plainpin(name):return {k:pin(name)[k] for k in ('bytes','sha256')}
def put(name,obj):write(name,m.enc(obj));return pin(name)
def snapshot(root, names):
    out={}
    for name in names:
        q=root/name;b=q.read_bytes();st=q.stat()
        out[name]={'bytes':len(b),'sha256':m.digest(b),'mtime_ns':st.st_mtime_ns,'ctime_ns':st.st_ctime_ns,'mode':st.st_mode}
    return out
def fixture_snapshot():return snapshot(R,[x.relative_to(R).as_posix() for x in R.rglob('*') if x.is_file()])
actual_names=['original_submitted_head/'+n for n in m.originals()]
actual_before=snapshot(m.A,actual_names)
# Actual already accepted first review is read-only authenticated; no source bytes copied.
check(m.byte_pin((m.A/m.FIRST_REVIEW_FILE).read_bytes())==m.FIRST_REVIEW_PLAIN,'Real first-review anchor drift')
write('ORIGINAL_SUBMISSION_CUSTODY.json',(m.A/'ORIGINAL_SUBMISSION_CUSTODY.json').read_bytes())
for n,b in m.originals().items():write('original_submitted_head/'+n,b)
baseline=json.loads((P/'PREPARATION_INPUT_PINS.json').read_bytes())['receipts']
other_names={p['path'] for p in baseline.values()}|{'ROOT_SOURCE_FIRST_CONTRACT_01.md','ROOT_PACKAGE_PREPARATION_ACCEPTANCE_01.json','ROOT_PDF_VISUAL_QA_V1.json'}
for n in other_names:write(n,(m.A/n).read_bytes())
other={n:plainpin(n) for n in other_names}
package='publication_package_v9'
metadata={'title':'SYNTHETIC_OFFLINE_FIXTURE centered origin note','creators':[{'name':'Kriebel, Alec','orcid':'0009-0001-9320-500X'}]}
for name in sorted(m.UPLOAD_NAMES):write(package+'/'+name,('SYNTHETIC_OFFLINE_FIXTURE '+name+'\n').encode())
write(package+'/portable_verification_01/verify_portable.py',b'# SYNTHETIC_OFFLINE_FIXTURE, never executed\n')
put(package+'/zenodo-deposit.json',{'metadata':metadata,'files':[{'path':n} for n in sorted(m.UPLOAD_NAMES)]})
files={x.relative_to(R/package).as_posix():m.byte_pin(x.read_bytes()) for x in (R/package).rglob('*') if x.is_file() and x.name!='PACKAGE_SEAL.json'}
seal={'schema':'pr204-publication-package-seal-v1','evidence_scope':'SYNTHETIC_OFFLINE_FIXTURE','UTC':'2026-10-17T10:09:00Z','package_prepared':True,'publication_ready':False,'files':files,'file_count_excluding_seal':len(files),'intended_uploads':{n:files[n] for n in m.UPLOAD_NAMES}}
sp=put(package+'/PACKAGE_SEAL.json',seal)
safe={**files,'PACKAGE_SEAL.json':m.byte_pin((R/package/'PACKAGE_SEAL.json').read_bytes())}
events=[];acceptance_objects={}
for i in (1,2):
    directory='SYNTHETIC_whole_review_'+str(i);report='REPORT.md'
    write(directory+'/'+report,('SYNTHETIC_OFFLINE_FIXTURE whole review '+str(i)+'\n').encode())
    ae={'directory':directory,'verdict':'CLEANPASS','reviewed_package':package,'reviewed_package_seal':safe['PACKAGE_SEAL.json'],'report_pin':plainpin(directory+'/'+report),'safe_files':{report:plainpin(directory+'/'+report)},'Root_read_entire_final_report':True}
    acceptance={'schema':'pr204-root-entire-package-review-acceptance-v1','evidence_scope':'SYNTHETIC_OFFLINE_FIXTURE','PR':204,'original_head':m.HEAD,'UTC':f'2026-10-17T10:{9+i:02d}:10Z','review_accepted':True,'NEW_whole_package_reviews_completed':i,'review_cycle_repairs_required_now':False,'review_event':ae}
    af='ROOT_WHOLE_PACKAGE_REVIEW_ACCEPTANCE_'+str(i).zfill(2)+'.json'
    put(af,acceptance);acceptance_objects[af]=acceptance
    events.append({**ae,'review_number':i,'report_file':report,'Root_acceptance_file':af,'Root_acceptance_pin':plainpin(af),'UTC':f'2026-10-17T10:{9+i:02d}:00Z','whole_scope':True,'open_findings':0,'report':pin(directory+'/'+report)})
gate={'schema':'pr204-root-publication-ready-v1','evidence_scope':'SYNTHETIC_OFFLINE_FIXTURE','PR':204,'problem_id':5100012,'original_head':m.HEAD,'UTC':'2026-10-17T10:12:00Z','accepted':True,'publication_ready':True,'release_authorized':True,'publication_ready_gate_accepted':True,'whole_package_review_loop_complete':True,'mathematical_clearance':True,'source_contract_clearance':True,'bounded_priority_audit_complete':True,'historical_priority_established':False,'proof_kind':'origin_only_Jacobi_direct_foot_two_pole','preparation_receipts':baseline,'package':package,'package_seal':safe['PACKAGE_SEAL.json'],'package_safe_files':safe,'paper':'centered_pedal_dn.tex','portable_entrypoint':'portable_verification_01/verify_portable.py','metadata':metadata,'intended_upload_files':{n:safe[n] for n in m.UPLOAD_NAMES},'whole_package_review_events':events,'other_safe_files':other}
gp=put(m.GATE_NAME,gate)
# Canonical actual-ready selected map fixture; only a small synthetic map is written.
selected={}
for name in [m.GATE_NAME]+[package+'/'+n for n in safe]+['original_submitted_head/'+n for n in m.originals(R)]:
    raw=(R/name).read_bytes();selected[m.CASE+name]={**m.byte_pin(raw),'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}
ds=m.digest(json.dumps(selected,sort_keys=True,separators=(',',':')).encode())
ready_dir='publication_checkpoint_01/SYNTHETIC_ready90'
map_pin=put(ready_dir+'/ACCEPTANCE_CURRENT_SELECTED_MAP.json',{'evidence_scope':'SYNTHETIC_OFFLINE_FIXTURE','selected_files':selected,'selected_map_sha256':ds})
ready={'evidence_scope':'SYNTHETIC_OFFLINE_FIXTURE','PR':204,'original_head':m.HEAD,'UTC':'2026-10-17T10:12:20Z','case_percent':90,'checkpoint_commit':'c'*40,'main_observed':'d'*40,'historical_firstness_independence_established':False,'selected_files':len(selected),'actual_current_map_file':{k:map_pin[k] for k in ('bytes','sha256')},'actual_current_selected_map_sha256':ds,**{k:True for k in m.READY_FIELDS}}
ready_pin=put(ready_dir+'/ACCEPTANCE.json',ready)
pointer={'evidence_scope':'SYNTHETIC_OFFLINE_FIXTURE','PR':204,'phase':'ready','UTC':'2026-10-17T10:12:30Z','directory':ready_dir,'checkpoint_commit':'c'*40,'main_observed':'d'*40,'acceptance_pin':plainpin(ready_dir+'/ACCEPTANCE.json'),'Root_recorded_only_after_actual_full_scope_acceptance':True}
put('ROOT_ACTUAL_READY_CHECKPOINT.json',pointer)
context={'gate_pin':plainpin(m.GATE_NAME),'ready_pointer_pin':plainpin('ROOT_ACTUAL_READY_CHECKPOINT.json'),'ready_acceptance_pin':plainpin(ready_dir+'/ACCEPTANCE.json'),'checkpoint_commit':'c'*40,'package_seal':gate['package_seal'],'package':package,'manifest_pin':safe['zenodo-deposit.json']}
rid=999999999999;doi='10.5281/zenodo.'+str(rid)
publication={'evidence_scope':'SYNTHETIC_OFFLINE_FIXTURE','UTC':'2026-10-17T10:13:00Z','PR':204,'actual_publication_verified':True,'metadata_exact_verified':True,'metadata_normalizations':[],'metadata_exact_evidence':'SYNTHETIC_OFFLINE_FIXTURE','metadata_sha256':m.digest((json.dumps(metadata,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()),'all_three_public_download_SHA256_verified':True,'verified_public_download_names':sorted(m.UPLOAD_NAMES),'public_downloads':[{'name':n,'url':'https://zenodo.org/api/records/'+str(rid)+'/files/'+n+'/content','final_url':'https://zenodo.org/api/records/'+str(rid)+'/files/'+n+'/content',**v} for n,v in gate['intended_upload_files'].items()],'id':rid,'state':'published','doi':doi,'doi_url':'https://doi.org/'+doi,'record_url':'https://zenodo.org/records/'+str(rid),'doi_resolution':{'status':'resolved','http_status':200,'final_url':'https://zenodo.org/records/'+str(rid)},'files':[{'name':n,'size':v['bytes'],'sha256':v['sha256']} for n,v in gate['intended_upload_files'].items()],'gate_sha256':gp['sha256'],'publication_gate':m.GATE_NAME,'package':package,'context':context,'inspect_doi_receipt':{'bytes':22,'sha256':m.digest(b'SYNTHETIC inspect')},'historical_firstness_independence_established':False}
pub_pin=put('ROOT_PUBLICATION_RECEIPT.json',publication)
tracker={'evidence_scope':'SYNTHETIC_OFFLINE_FIXTURE','UTC':'2026-10-17T10:14:00Z','PR':204,'doi':doi,'spreadsheet_id':'1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','sheet_gid':1254632077,'range':"'Math Puzzles'!A999:D999",'row':['k203b: centered original-side pedal-area product (AMR-050-0012)','','https://doi.org/'+doi,metadata['title']+'; PR204 synthetic test only'],'actual_tracker_row_verified':True,'own_row_readback_verified':True,'foreign_rows_retained':True,'original_preappend_baseline_retained':True,'original_preappend_baseline':{'file':'before2_0001.json','pin':{'bytes':22,'sha256':m.digest(b'SYNTHETIC baseline')},'row_count':2,'counter_sha256':m.digest(b'SYNTHETIC Counter')},'two_fresh_full_prechecks':True,'RAW_INSERT_ROWS':True,'B_intentionally_blank_no_verified_chat_share_URL':True,'recovered_unknown_outcome':False,'gate_sha256':gp['sha256'],'publication_receipt':{k:pub_pin[k] for k in ('bytes','sha256')},'context':context}
put('ROOT_TRACKER_RECEIPT.json',tracker)
merge={'schema':'pr204-root-merge-receipt-v1','evidence_scope':'SYNTHETIC_OFFLINE_FIXTURE','UTC':'2026-10-17T10:15:00Z','PR':204,'original_head':m.HEAD,'package_seal':sp,'accepted':True,'merged':True,'original_HEAD_safe':True,'full_scope_verified':True,'merge_commit':'e'*40}
put('ROOT_SYNTHETIC_MERGE_RECEIPT.json',merge)
# Authentic actual98 aliases. These safeguards are consumed then omitted from native CURRENT program-completion claims.
factual={'schema':'pr204-root-factual-receipt-v1','evidence_scope':'SYNTHETIC_OFFLINE_FIXTURE','UTC':'2026-10-17T10:16:00Z','PR':204,'original_head':m.HEAD,'package_seal':sp,'accepted':True,'full_scope_MAIN_accepted':True,'actual_factual_accepted':True,'case_percent':98,'completed':False,'publication_receipt_sha256':pin('ROOT_PUBLICATION_RECEIPT.json')['sha256'],'tracker_receipt_sha256':pin('ROOT_TRACKER_RECEIPT.json')['sha256'],'merge_receipt_sha256':pin('ROOT_SYNTHETIC_MERGE_RECEIPT.json')['sha256'],'completion_facts':{'case_completed':False,'goal_complete':False,'fully_completed_count':46,'published_count':30,'last_completed_PR':203,'next_numeric_intake_cursor':204,'advance_to_next_PR_authorized_now':False}}
put('ROOT_SYNTHETIC_FACTUAL98_RECEIPT.json',factual)
paths={'publication_ready_gate':m.GATE_NAME,'publication_receipt':'ROOT_PUBLICATION_RECEIPT.json','tracker_receipt':'ROOT_TRACKER_RECEIPT.json','merge_receipt':'ROOT_SYNTHETIC_MERGE_RECEIPT.json','factual_receipt':'ROOT_SYNTHETIC_FACTUAL98_RECEIPT.json'}
def facts(stage='published_pending_merge'):
    keys=['publication_ready_gate','publication_receipt','tracker_receipt']
    if stage!='published_pending_merge':keys+=['merge_receipt']
    if stage=='factual_checkpoint_accepted':keys+=['factual_receipt']
    return {'schema':'pr204-native-facts-v1','original_head':m.HEAD,'UTC':'2026-10-17T10:17:00Z','package_seal':sp,**{k:pin(paths[k]) for k in keys}}
postimages={}
for stage in m.STAGES:
    before=fixture_snapshot();out=m.construct_fixture(stage,facts(stage),R);check(before==fixture_snapshot(),'Constructor side effect')
    check(len(out)==27 and all(n.startswith('SYNTHETIC_ONLY/') for n in out),'Synthetic native namespace leaked')
    current={n.removeprefix('SYNTHETIC_ONLY/'+m.NATIVE):b for n,b in out.items()}
    for name,raw in m.originals(R).items():check((current[name]==raw)==(name not in m.CHANGED),'Preservation set differs')
    status=json.loads(current['CURRENT_STATUS.json']);check(not status['actual_publication_verified'] and not status['actual_merge_accepted'],'Synthetic actual fact leakage')
    check(all(k not in status for k in ('completed','completion_facts','fully_completed_count','published_count','last_completed_PR','next_numeric_intake_cursor')) and status['goal_complete'] is False,'Native presentation invented program completion/counters')
    check(package in status['package'],'Final package hardwired')
    for row in current['SHA256SUMS'].decode().splitlines():
        sha,name=row.split('  ',1);check(sha==m.digest(current[name]),'Native SHA256 mismatch')
    postimages[stage]=json.loads(current['NATIVE_PRESENTATION_RECEIPT.json'])
    records.append({'test':'valid_'+stage,'outcome':'PASS_SYNTHETIC_ONLY','payload_sha256':m.digest(m.enc({n:m.digest(b) for n,b in sorted(out.items())}))})
def refused(label,stage='published_pending_merge',given=None,mutations=None):
    saved=[]
    try:
        if mutations:
            for name,change in mutations.items():
                raw=(R/name).read_bytes();saved.append((name,raw));obj=json.loads(raw);change(obj);put(name,obj)
        use=copy.deepcopy(facts(stage) if given is None else given)
        before=fixture_snapshot()
        try:m.construct_fixture(stage,use,R)
        except m.Refused as exc:records.append({'test':label,'outcome':'REFUSED','reason':str(exc)})
        else:raise RuntimeError('Invalid evidence accepted: '+label)
        check(before==fixture_snapshot(),'Constructor wrote during refusal')
    finally:
        for name,raw in saved:write(name,raw)
# Gate/custody/stage guards.
f=facts();del f['publication_ready_gate'];refused('missing_actual_gate',given=f)
f=facts();f['original_head']='0'*40;refused('wrong_HEAD',given=f)
f=facts();f['completed']=True;refused('invented_completion',given=f)
f=facts();f['package_seal']['path']='publication_package_v8/PACKAGE_SEAL.json';refused('native_seal_path_does_not_match_gate',given=f)
refused('wrong_stage','actual_merge_accepted',facts())
refused('premature_merge_receipt',given=facts('actual_merge_accepted'))
refused('gate_plain_pin_replaced_by_path_pin',mutations={m.GATE_NAME:lambda g:g.update(package_seal=sp)})
refused('ready_gate_false',mutations={m.GATE_NAME:lambda g:g.update(publication_ready_gate_accepted=False)})
refused('legacy_shadow_gate_not_supported',mutations={m.GATE_NAME:lambda g:g.update(package_seal={'bytes':0,'sha256':'0'*64})})
refused('gate_metadata_mismatch',mutations={m.GATE_NAME:lambda g:g['metadata'].update(title='incorrect')})
refused('gate_other_scientific_history_removed',mutations={m.GATE_NAME:lambda g:g.update(other_safe_files={})})
refused('only_one_review',mutations={m.GATE_NAME:lambda g:g.update(whole_package_review_events=g['whole_package_review_events'][:1])})
refused('last_not_CLEANPASS',mutations={m.GATE_NAME:lambda g:g['whole_package_review_events'][-1].update(verdict='CHANGES_REQUESTED',open_findings=1)})
refused('CLEANPASS_has_open_findings',mutations={m.GATE_NAME:lambda g:g['whole_package_review_events'][0].update(open_findings=1)})
refused('review_count_not_sequential',mutations={m.GATE_NAME:lambda g:g['whole_package_review_events'][-1].update(review_number=3)})
refused('Root_acceptance_reused',mutations={m.GATE_NAME:lambda g:g['whole_package_review_events'][-1].update(Root_acceptance_file=g['whole_package_review_events'][0]['Root_acceptance_file'],Root_acceptance_pin=g['whole_package_review_events'][0]['Root_acceptance_pin'])})
refused('review_directory_reused',mutations={m.GATE_NAME:lambda g:g['whole_package_review_events'][-1].update(directory=g['whole_package_review_events'][0]['directory'])})
refused('Root_accepted_event_field_changed',mutations={m.GATE_NAME:lambda g:g['whole_package_review_events'][0].update(Root_read_entire_final_report=False)})
refused('report_alias_wrong',mutations={m.GATE_NAME:lambda g:g['whole_package_review_events'][0]['report'].update(sha256='0'*64)})
refused('safe_review_artifact_changed',mutations={m.GATE_NAME:lambda g:g['whole_package_review_events'][0]['safe_files']['REPORT.md'].update(sha256='0'*64)})
refused('review_scope_false',mutations={m.GATE_NAME:lambda g:g['whole_package_review_events'][0].update(whole_scope=False)})
refused('review_gate_chronology_stale',mutations={m.GATE_NAME:lambda g:g.update(UTC='2026-10-17T10:00:00Z')})
# Authentic publication and actual-ready context guard cases.
pub='ROOT_PUBLICATION_RECEIPT.json';tr='ROOT_TRACKER_RECEIPT.json'
refused('publication_not_verified',mutations={pub:lambda j:j.update(actual_publication_verified=False)})
refused('publication_wrong_DOI_id',mutations={pub:lambda j:j.update(doi='10.5281/zenodo.123')})
refused('publication_prior_DOI_reuse',mutations={pub:lambda j:j.update(id=23085904,doi='10.5281/zenodo.23085904')})
refused('publication_gate_SHA_stale',mutations={pub:lambda j:j.update(gate_sha256='0'*64)})
refused('publication_package_stale',mutations={pub:lambda j:j.update(package='publication_package_v8')})
refused('publication_metadata_not_exact',mutations={pub:lambda j:j.update(metadata_normalizations=['changed'])})
refused('publication_independent_download_bad_bytes',mutations={pub:lambda j:j['public_downloads'][0].update(sha256='0'*64)})
refused('publication_download_not_HTTPS',mutations={pub:lambda j:j['public_downloads'][0].update(final_url='http://example.invalid')})
refused('publication_missing_download',mutations={pub:lambda j:j.update(public_downloads=j['public_downloads'][:2])})
refused('publication_kit_file_bad_bytes',mutations={pub:lambda j:j['files'][0].update(size=0)})
refused('publication_resolver_not_200',mutations={pub:lambda j:j['doi_resolution'].update(http_status=404)})
refused('publication_resolver_wrong_record',mutations={pub:lambda j:j['doi_resolution'].update(final_url='https://zenodo.org/records/123')})
refused('publication_before_readiness',mutations={pub:lambda j:j.update(UTC='2026-10-17T10:00:00Z')})
refused('ready_context_gate_pin_stale',mutations={pub:lambda j:j['context']['gate_pin'].update(sha256='0'*64)})
refused('ready_context_package_seal_stale',mutations={pub:lambda j:j['context']['package_seal'].update(sha256='0'*64)})
refused('ready_pointer_not_exact',mutations={pub:lambda j:j['context']['ready_pointer_pin'].update(sha256='0'*64)})
refused('ready_acceptance_not_exact',mutations={pub:lambda j:j['context']['ready_acceptance_pin'].update(sha256='0'*64)})
refused('ready_context_commit_wrong',mutations={pub:lambda j:j['context'].update(checkpoint_commit='f'*40)})
# Rebind a fully self-consistent synthetic ready chain to test semantic guards,
# rather than accepting a rejection caused only by an obsolete outer byte pin.
def ready_chain_attack(label,change):
    names=[ready_dir+'/ACCEPTANCE_CURRENT_SELECTED_MAP.json',ready_dir+'/ACCEPTANCE.json','ROOT_ACTUAL_READY_CHECKPOINT.json',pub,tr]
    saved={n:(R/n).read_bytes() for n in names}
    try:
        mapped=json.loads(saved[names[0]]);ac=json.loads(saved[names[1]]);ptr=json.loads(saved[names[2]])
        change(mapped,ac,ptr)
        ds2=m.digest(json.dumps(mapped['selected_files'],sort_keys=True,separators=(',',':')).encode())
        mapped['selected_map_sha256']=ds2;put(names[0],mapped)
        ac.update(selected_files=len(mapped['selected_files']),actual_current_selected_map_sha256=ds2,actual_current_map_file=plainpin(names[0]));put(names[1],ac)
        ptr['acceptance_pin']=plainpin(names[1]);put(names[2],ptr)
        pj=json.loads(saved[pub]);pj['context'].update(ready_acceptance_pin=plainpin(names[1]),ready_pointer_pin=plainpin(names[2]));put(pub,pj)
        tj=json.loads(saved[tr]);tj['context']=pj['context'];tj['publication_receipt']=plainpin(pub);put(tr,tj)
        refused(label)
    finally:
        for n,b in saved.items():write(n,b)
ready_chain_attack('ready_MAIN_missing_in_both',lambda mapped,ac,ptr:(ac.pop('main_observed'),ptr.pop('main_observed')))
ready_chain_attack('ready_MAIN_invalid_in_both',lambda mapped,ac,ptr:(ac.update(main_observed='not-a-commit'),ptr.update(main_observed='not-a-commit')))
ready_chain_attack('ready_map_missing_archived_original',lambda mapped,ac,ptr:mapped['selected_files'].pop(m.CASE+'original_submitted_head/PROOF.md'))
ready_chain_attack('ready_map_archived_original_identity_drift',lambda mapped,ac,ptr:mapped['selected_files'][m.CASE+'original_submitted_head/PROOF.md'].update(sha256='0'*64))
# Canonical tracker guards.
refused('tracker_not_verified',mutations={tr:lambda j:j.update(actual_tracker_row_verified=False)})
refused('tracker_wrong_DOI',mutations={tr:lambda j:j.update(doi='10.5281/zenodo.123')})
refused('tracker_wrong_publication_pin',mutations={tr:lambda j:j['publication_receipt'].update(sha256='0'*64)})
refused('tracker_wrong_context',mutations={tr:lambda j:j['context'].update(checkpoint_commit='f'*40)})
refused('tracker_foreign_rows_not_retained',mutations={tr:lambda j:j.update(foreign_rows_retained=False)})
refused('tracker_original_baseline_not_retained',mutations={tr:lambda j:j.update(original_preappend_baseline_retained=False)})
refused('tracker_B_filled',mutations={tr:lambda j:j['row'].__setitem__(1,'invented chat URL')})
refused('tracker_row_DOI_wrong',mutations={tr:lambda j:j['row'].__setitem__(2,'https://doi.org/10.5281/zenodo.123')})
refused('tracker_range_not_one_row',mutations={tr:lambda j:j.update(range="'Math Puzzles'!A999:D1000")})
refused('tracker_target_gid_wrong',mutations={tr:lambda j:j.update(sheet_gid=1)})
refused('tracker_before_publication',mutations={tr:lambda j:j.update(UTC='2026-10-17T10:00:00Z')})
refused('merge_not_accepted','actual_merge_accepted',mutations={paths['merge_receipt']:lambda j:j.update(accepted=False)})
factual_name=paths['factual_receipt']
refused('factual98_not_accepted','factual_checkpoint_accepted',mutations={factual_name:lambda j:j.update(actual_factual_accepted=False)})
refused('circular_premature100_completed_true','factual_checkpoint_accepted',mutations={factual_name:lambda j:j.update(completed=True)})
refused('factual98_case_completed_true','factual_checkpoint_accepted',mutations={factual_name:lambda j:j['completion_facts'].update(case_completed=True)})
refused('factual98_premature47_count','factual_checkpoint_accepted',mutations={factual_name:lambda j:j['completion_facts'].update(fully_completed_count=47)})
refused('factual98_premature31_published_count','factual_checkpoint_accepted',mutations={factual_name:lambda j:j['completion_facts'].update(published_count=31)})
refused('factual98_premature_next_cursor205','factual_checkpoint_accepted',mutations={factual_name:lambda j:j['completion_facts'].update(next_numeric_intake_cursor=205)})
refused('factual98_premature_advance','factual_checkpoint_accepted',mutations={factual_name:lambda j:j['completion_facts'].update(advance_to_next_PR_authorized_now=True)})
refused('factual98_unbound_publication','factual_checkpoint_accepted',mutations={factual_name:lambda j:j.update(publication_receipt_sha256='0'*64)})
# Original and final-package byte mutations are restored exactly.
for label,name in [('modified_original','original_submitted_head/PROOF.md'),('modified_final_paper',package+'/centered_pedal_dn.tex')]:
    old=(R/name).read_bytes();write(name,old+b' changed');refused(label);write(name,old)
extra=R/package/'unsealed.txt';extra.write_text('SYNTHETIC_OFFLINE_FIXTURE')
refused('unsealed_extra_file');extra.unlink()
try:m.construct('published_pending_merge',{'schema':'pr204-native-facts-v1','original_head':m.HEAD,'UTC':'2026-10-17T10:17:00Z'})
except m.Refused as exc:records.append({'test':'actual_case_no_ready_gate_refuses','outcome':'REFUSED','reason':str(exc)})
else:raise RuntimeError('Actual missing gate accepted')
actual_after=snapshot(m.A,actual_names);check(actual_before==actual_after,'Actual20 originals changed')
(P/'ACTUAL_ORIGINAL20_IMMUTABILITY.json').write_bytes(m.enc({'all20_unchanged':True,'before':actual_before,'after':actual_after,'no_actual_native_or_external_action':True}))
result={'evidence_scope':'SYNTHETIC_OFFLINE_FIXTURE','UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS','python_optimization':sys.flags.optimize,'test_count':len(records),'tests':records,'actual_original20_unchanged':True,'actual_publication_tracker_merge_or_native_action':False,'actual_whole_package_review_events_contributed':0}
(P/('OFFLINE_TEST_RECEIPT_OPTIMIZED.json' if sys.flags.optimize else 'OFFLINE_TEST_RECEIPT_NORMAL.json')).write_bytes(m.enc(result))
(P/'SYNTHETIC_POSTIMAGE_BEFORE_AFTER.json').write_bytes(m.enc({'evidence_scope':'SYNTHETIC_OFFLINE_FIXTURE','no_actual_native_output_written':True,'stages':postimages}))
print(json.dumps({'status':'PASS','tests':len(records),'optimization':sys.flags.optimize,'actual_original20_unchanged':True}))
