from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,zipfile
PRE=Path(__file__).resolve().parent
P=PRE.parents[2]
D=PRE.parent/'initial_review_20261013'
R=PRE/'fresh_review_03'
utc=datetime.now(timezone.utc).isoformat()
def digest(b):return hashlib.sha256(b).hexdigest()
def norm(x):return {k:v for k,v in x.items() if k not in {'utc','python'}}
m=json.loads((R/'FINAL_AUDIT_MANIFEST.json').read_text())
assert m['verdict']=='PASS' and m['mandatory_issues']==[]
assert digest((R/'FINAL_AUDIT_MANIFEST.json').read_bytes())=='d5aa84a52322a4a51a923ebac25ab61f04aaf1ae528bbcee2d8933492cf5a979'
for q in m['public_authored_relative_paths']:
    b=(R/q['path']).read_bytes();assert len(b)==q['bytes'] and digest(b)==q['sha256']
frozen=json.loads((PRE/'FROZEN_CANDIDATE.json').read_text())
assert m['candidate_files']==frozen['files']
for q in frozen['files']:
    b=(PRE/q['path']).read_bytes();assert len(b)==q['bytes'] and digest(b)==q['sha256']
q=m['initial_independence']['pin']
b=(R/q['path']).read_bytes();assert len(b)==q['bytes'] and digest(b)==q['sha256']
q=m['planned_source_script']
b=Path(q['path']).read_bytes();assert len(b)==q['bytes'] and digest(b)==q['sha256']
package=json.loads((R/'PACKAGE_REPRODUCTION.json').read_text())
allpins=json.loads((R/'ALL_NESTED_PIN_REPRODUCTION.json').read_text())
assert allpins['status']=='PASS' and allpins['nested_sha256_objects_checked']==375 and allpins['unresolved_historical_objects']==[]
with zipfile.ZipFile(PRE/'output/critical_wave_verification.zip') as z:
    archive={n:z.read(n) for n in z.namelist()}
    specs=json.loads(archive['CHECKSETS.json'])
    for record in package['independent_checksets']:
        spec=next(q for q in specs if q['name']==record['name'])
        assert record['returncode']==0 and norm(record['receipt'])==norm(json.loads(archive[spec['reference']]))
    assert len(package['independent_checksets'])==7 and package['portable_result']['status']=='PASS'
    for q in allpins['results']:
        target=q['verified_against']
        b=archive[target[4:]] if target.startswith('ZIP:') else Path(target).read_bytes()
        assert digest(b)==q['sha256'] and (q['bytes'] is None or len(b)==q['bytes'])
    intake=json.loads((D/'INTAKE.json').read_text())
    for q in package['original_files']:
        b=archive['original_submission/'+q['path']]
        old=next(x for x in intake['original_source_files'] if x['native_path']==intake['native_source_prefix']+q['path'])
        assert digest(b)==q['sha256']==old['sha256'] and len(b)==q['bytes']==old['bytes']
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==q['git_blob_oid']==old['native_blob']
accept={'utc':utc,'verdict':'PASS; no mandatory issues','root_full_read':['REPORT.md','INITIAL_INDEPENDENT_RECONSTRUCTION.md','independent_package_audit.py','check_all_nested_pins.py'],
        'public_authored_pins_verified':len(m['public_authored_relative_paths']),
        'manifest_sha256':digest((R/'FINAL_AUDIT_MANIFEST.json').read_bytes()),
        'all375_nested_SHA256_objects_independently_rechecked':True,
        'all7_complete_scientific_receipts_independently_compared':True,
        'all19_original_native_blob_SHA1_SHA256_size_rechecked':True,
        'current_candidate5_pins_verified':True,'corrected_planned_script_static_verdict':'PASS',
        'independence_timestamp_qualification':{'sampled_checkpoint_label':'2026-10-14T05:12:39Z','actual_filesystem_save':'2026-10-14T05:13:38.132320Z','initial_artifact_sha256':m['initial_independence']['pin']['sha256'],'both_before_older_records_access':True},
        'historical_report_binding':'Exact five-pair deterministic reconstruction verified by root and reviewer03 against10340 bytes and pre-existing SHA256; not native retrieval or endorsement of superseded verdict.',
        'fresh_full_reviews_completed':3,'full_reviews_on_current_revised_payload':1,
        'additional_current_revised_independent_delta_payload_review':True,
        'scope':'Unmodified ordinary-cone implication; bounded priority and explicit classical credits; replacement/sharp-rate questions excluded'}
(PRE/'ROOT_REVIEW03_ACCEPTANCE.json').write_text(json.dumps(accept,indent=2)+'\n')
delta=json.loads((PRE/'ROOT_EDITORIAL_DELTA_ACCEPTANCE.json').read_text())
assert delta['all_current_candidate5_pins_unchanged'] and delta['actual_scientific_receipts_all7_match']
clear={'utc':utc,'mathematical_verdict':'PASS','source_verdict':'PASS scoped negative answer to unchanged ordinary-critical-cone implication',
       'priority_verdict':'Bounded no complete or automatically covering earlier wave construction authenticated; established mechanisms credited; no worldwide-firstness certificate.',
       'fresh_clean_reviews':3,'sequential_NEW_full_reviewers':['fresh_review_01','fresh_review_02','fresh_review_03'],
       'old_two_full_review_scope':'Preserved initial draft; science unchanged by four elected editorial refinements.',
       'current_revised_full_review':'fresh_review_03','current_revised_additional_payload_review':'editorial_delta_review_01',
       'mandatory_issues':[],'planned_current_source_script_sha256':m['planned_source_script']['sha256'],
       'candidate_files':{q['path']:{k:q[k] for k in ['bytes','sha256']} for q in frozen['files']},
       'PDF_pages':6,'archive_files':113,'exact_assertions':5603,'noncertified_diagnostics':5,
       'additional_root_reproduced_review02_stress_exact_assertions':2274,
       'historical_input_reconstruction_explicitly_qualified':True,
       'scientific_publication_cleared':True,'publication_cleared':True,'case_completion_percent':90,
       'Zenodo_publication_yet_confirmed':False,'tracker_append_yet_confirmed':False,'native_merge_yet_confirmed':False}
(PRE/'FINAL_CLEARANCE.json').write_text(json.dumps(clear,indent=2)+'\n')
for f,fields in [(D/'CURRENT_AUDIT_STATE.json',{'completion_percent':90,'stage':'three_NEW_full_reviews_and_revised_delta_accepted_publication_cleared','fresh_clean_manuscript_reviews_completed':3,'revised_final_review_pending':False,'preprint_upload_cleared':True}), (P/'CURRENT_GOAL_SELECTION_20261013.json',{'case_completion_percent':90,'current_stage':'three_NEW_full_reviews_and_revised_delta_accepted_publication_cleared'})]:
    x=json.loads(f.read_text());x.update(utc=utc,**fields);f.write_text(json.dumps(x,indent=2)+'\n')
note=utc+' — Best guess90% PR248 completion. Three sequential NEW full manuscript reviewers PASS, including full revised science/archive audit03, plus separate revised-payload delta. Root read full final proof/source/priority report and verification code, rechecked11 fresh authored pins, all375 nested source/historical objects, complete7 scientific receipts and19 original native blob identities. Exact historical10340-byte report reconstructed from5 actual reverse edits and independently authenticated by pre-existing digest; not represented as native retrieval or current priority verdict. Planned current-source attribution and at-zero wording corrected before execution and independently checked. Clock/save timestamp and delta-manifest UTC prose clarified in root acceptances; no paper/math change. Candidate5 pins unchanged; publication cleared. Exact Zenodo/tracker/native merge still pending. Counts39/16/16/0; whole goal active/incomplete.\n'
for f in [P/'RESEARCH_LOG.md',PRE/'RESEARCH_LOG.md',D/'RESEARCH_LOG.md']:
    with f.open('a') as out:out.write('\n'+note)
print(json.dumps({'status':'PASS','case_percent':90,'fresh_NEW_full_reviews':3,'current_revised_independent_payload_reviews':2,'nested_objects_rechecked':375,'publication_cleared':True},indent=2))
