"""Separate outer-inventory metadata repair; immutable scientific sources."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json
H=Path(__file__).resolve().parent
V=H.parent/'durable_facing_v02'
B=H.parent.parent
F=B/'fresh_public_findings_export_adversary_01'
UTC=datetime.now(timezone.utc).isoformat()
checks=[];direct=[]
def ck(ok,label):
 assert ok,label
 checks.append(label)
def measure(p):
 ck(p.is_file() and not p.is_symlink(),'regular:'+str(p))
 raw=p.read_bytes();ck(raw==p.read_bytes(),'stable-read:'+str(p))
 return raw,{'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
             'git_blob_oid':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}
def bind(p,role):
 raw,pin=measure(p);direct.append({'path':str(p),'role':role,**pin});return raw,pin
def dump(name,obj):
 p=H/name;ck(not p.exists(),'new-addendum-only:'+name);p.write_text(json.dumps(obj,indent=2)+'\n')

outerraw,outerpin=bind(V/'FINAL_MANIFEST.json','immutable original outer247-entry manifest; declared own self exclusion and previously undeclared nested omission')
outer=json.loads(outerraw);original={r['path']:r for r in outer['files']}
ck(len(original)==len(outer['files'])==247,'247 unique original outer entries')
actual={p.relative_to(V).as_posix():p for p in V.rglob('*') if p.is_file()}
ck(len(actual)==249,'exact249 original durable preparation files')
ck(not any(p.is_symlink() for p in V.rglob('*')),'no symlinks in frozen durable preparation')
nested='payloads/draft_pr_descending_audit_20261002/audits/pr259_5100026/initial_review_20261012/elliptic_centroid_adversary/FINAL_MANIFEST.json'
omitted=sorted(set(actual)-set(original));ck(omitted==['FINAL_MANIFEST.json',nested],'only original outer self and selected nested omissions')
ck(not (set(original)-set(actual)),'no original manifest phantom entries')
inventory=[]
for rel,p in sorted(actual.items()):
 raw,pin=measure(p)
 if rel in original:
  ck(pin['bytes']==original[rel]['bytes'] and pin['sha256']==original[rel]['sha256'],'original247 entry authenticated:'+rel)
  role='original outer-manifest listed entry authenticated'
 elif rel=='FINAL_MANIFEST.json':role='original outer self; explicitly inventoried here without mutating original'
 else:role='previously undeclared omission; selected nested family manifest fully authenticated here'
 inventory.append({'path':rel,**pin,'coverage_role':role})
by={r['path']:r for r in inventory}
planraw,planpin=bind(V/'SCOPED_FILE_PLAN.json','immutable existing231 scientific selection plan')
plan=json.loads(planraw);ck(plan['selected_count']==231 and plan['selected_bytes']==4152796,'exact accepted scientific selection dimensions')
planrows={r['payload_relative_path']:r for r in plan['paths']};ck(len(planrows)==231,'231 unique scientific payloads')
for rel,r in planrows.items():
 ck(rel in by,'selected file covered:'+rel)
 ck(all(by[rel][k]==r[k] for k in ['bytes','sha256','git_blob_oid']),'existing plan binding:'+rel)
prefix='payloads/draft_pr_descending_audit_20261002/audits/pr259_5100026/initial_review_20261012/'
pubrel=prefix+'PUBLIC_FINDINGS_EXPORT_MANIFEST.json'
pubraw,pubpin=bind(V/pubrel,'immutable current public230-entry selection manifest; own recursive pin excluded')
pub=json.loads(pubraw);pubrows={prefix+r['audit_relative_path']:r for r in pub['files']}
ck(len(pubrows)==230 and set(pubrows)==set(planrows)-{pubrel},'public scientific inventory excludes only own recursive pin')
for rel,r in pubrows.items():ck(all(by[rel][k]==r[k] for k in ['bytes','sha256','git_blob_oid']),'existing public manifest binding:'+rel)
ck(nested in planrows and nested in pubrows,'previously omitted nested file selected by both exact inventories')
historicalraw,historicalpin=bind(B/'elliptic_centroid_adversary/FINAL_MANIFEST.json','immutable original historical elliptic-family manifest')
ck(historicalraw==(V/nested).read_bytes(),'nested selected family manifest equals historical original')
mapsraw,mapspin=bind(V/'CANONICAL_PUBLIC_MAP_PINS.json','immutable six author-facing canonical source pins')
maps=json.loads(mapsraw)
ck(len(maps['pins'])==6,'six canonical author-facing map pins')
canonical=[]
for name,r in sorted(maps['pins'].items()):
 rel=prefix+name;ck(rel in by,'canonical map covered:'+name)
 ck(all(by[rel][k]==r[k] for k in ['bytes','sha256','git_blob_oid']),'six canonical author-facing pins unchanged:'+name)
 canonical.append({'name':name,'path':rel,**{k:by[rel][k] for k in ['bytes','sha256','git_blob_oid']}})

reviewmfraw,reviewmfpin=bind(F/'PUBLIC_MANIFEST.json','complete frozen fresh scientific export review inventory')
rm=json.loads(reviewmfraw);listed={r['path']:r for r in rm['files']};ra={p.relative_to(F).as_posix():p for p in F.rglob('*') if p.is_file()}
ck(len(listed)==37 and len(ra)==38,'complete fresh review37listed plus own manifest')
ck(set(ra)-set(listed)=={'PUBLIC_MANIFEST.json'} and not(set(listed)-set(ra)),'fresh review sole declared own self exclusion')
reviewinventory=[]
for rel,p in sorted(ra.items()):
 raw,pin=measure(p)
 if rel in listed:ck(pin['bytes']==listed[rel]['bytes'] and pin['sha256']==listed[rel]['sha256'],'fresh complete review original pin:'+rel)
 reviewinventory.append({'path':rel,**pin})
decisionraw,decisionpin=bind(F/'DECISION.json','fresh review decision: sciencePASS with EXPORT-PREP-001 remaining')
decision=json.loads(decisionraw)
ck(decision['completed'] is True and decision['scientific_selection_verdict']=='PASS','actual fresh scoped scientific review facts')
ck(decision['independent_primary_checker_checks']==5863 and decision['actual_unchanged_core_replays']==4,'actual5863/four fresh review counts')
ck([x['id'] for x in decision['findings']]==['EXPORT-PREP-001'],'sole fresh issue is outer inventory coverage')
bound=json.loads((F/'BOUNDARY_AND_PREPARATION_INVENTORY_REVIEW.json').read_bytes())
ck(bound['exact_preparation_inventory']['outer_manifest_unlisted_paths']==omitted,'fresh issue omission list matches exhaustive current read')
failure_bindings=[]
for folder,kind in [('root_public_export_v02_verification_01','Root independently observed exact outer-inventory coverage failure'),
                    ('root_public_export_v02_selection_verification_02','Root harness derivative-classification error, explicitly not a source defect'),
                    ('root_public_export_v02_selection_verification_03','Root harness overlapping-header-removal error, explicitly not a source defect')]:
 p=B/folder/'FAILURE_RECEIPT.json';raw,pin=bind(p,kind);d=json.loads(raw)
 ck(d['completed'] is False and d['observed_exit_code']==1,'preserved actual Root failure:'+folder)
 c=B/folder/'FAILED_CHECKER.py';cr,cp=bind(c,'preserved exact failed Root checker body:'+folder)
 ck(cp['sha256']==d['checker_sha256'],'failed checker receipt pin:'+folder)
 failure_bindings.append({'folder':folder,'failure_role':kind,'receipt_pin':pin,'failed_checker_pin':cp,'source_defect':folder=='root_public_export_v02_verification_01'})
rootpassraw,rootpasspin=bind(B/'root_public_export_v02_selection_verification_04/VERIFICATION.json','later Root exact scientific-selection PASS only; outer exhaustive acceptance explicitlyfalse')
rootpass=json.loads(rootpassraw)
ck(rootpass['status']=='PASS_DURABLE_PUBLIC_EXPORT_EXACT_BYTES_AND_SELECTION_ONLY' and rootpass['outer_preparation_inventory_exhaustive'] is False,'Root bounded selection-only pass remains honest')

dump('EXHAUSTIVE_V02_249_FILE_INVENTORY.json',{'schema':'pr259-outer-preparation-exhaustive-coverage-v1','utc':UTC,'root':str(V),
     'actual_file_count':249,'files':inventory,'declared_exclusions':[],'recursive_self_issue':'This inventory resides in a separate sibling addendum folder, so the original outer FINAL_MANIFEST is included without self-recursion.',
     'scientific_selection_unchanged':True,'no_new_scientific_or_promotion_or_execution_acceptance':True})
dump('FRESH_REVIEW_AND_ROOT_FAILURE_BINDINGS.json',{'schema':'pr259-outer-coverage-evidence-bindings-v1','utc':UTC,
     'complete_fresh_review_root':str(F),'complete_fresh_review_file_count':38,'complete_fresh_review_files':reviewinventory,
     'complete_fresh_review_manifest_pin':reviewmfpin,'fresh_decision_pin':decisionpin,
     'fresh_scientific_review_recorded_facts':{'scientific_verdict':'PASS','explicit_checks':5863,'actual_unchanged_core_replays':4,'sole_issue':'EXPORT-PREP-001'},
     'all_known_Root_failures_preserved':failure_bindings,'later_Root_selection_only_receipt_pin':rootpasspin,
     'original_preparation_outer_manifest_failure':{'pin':outerpin,'listed':247,'actual':249,'only_omissions':omitted},
     'direct_input_bindings':direct,'bodies_copied':False,'new_review_or_case_acceptance':False})
dump('OUTER_COVERAGE_ADDENDUM.json',{'schema':'pr259-export-prep-001-separate-outer-coverage-addendum-v1','utc':UTC,
     'state':'FROZEN_PREPARATION_METADATA_ONLY_FRESH_REVIEW_PENDING','issue':'EXPORT-PREP-001','original_v02_root':str(V),
     'original_outer_manifest_pin':outerpin,'original_outer_manifest_listed_count':247,'all_original247_entries_authenticated':True,
     'actual249_files_exhaustively_inventoried':True,'exact_omissions_from_original_outer_manifest':[
      {'path':'FINAL_MANIFEST.json','pin':outerpin,'original_self_exclusion_declared':True,'coverage_now':'Listed in separate exhaustive249-file inventory.'},
      {'path':nested,'pin':{k:by[nested][k] for k in ['bytes','sha256','git_blob_oid']},'original_outer_second_exclusion_declared':False,
       'coverage_now':'Explicitly declared here and listed in exhaustive249-file inventory; it remains an unchanged selected scientific file.',
       'existing_scoped_plan_entry':planrows[nested],'existing_public_selection_manifest_entry':pubrows[nested],
       'historical_family_original_pin':historicalpin}],
     'other_omissions':[],'original_phantom_entries':[],
     'existing_selection_bindings':{'SCOPED_FILE_PLAN.json':planpin,'PUBLIC_FINDINGS_EXPORT_MANIFEST.json':pubpin,'CANONICAL_PUBLIC_MAP_PINS.json':mapspin},
     'six_canonical_author_facing_payloads_unchanged':canonical,
     'all231_scientific_payloads_unchanged':True,'scientific_selected_count':231,'scientific_selected_bytes':4152796,
     'no_original_bytes_modified':True,'no_new_scientific_acceptance':True,'no_promotion_acceptance':True,'no_execution_authority':True,
     'case_complete':False,'provider_actions':0,'shared_git_actions':0,'outside_person_communications':0,
     'remaining':'New fresh subagent review of this separate metadata addendum and frozen scientific selection, then Root personal acceptance. Actual author/Main/global/package/publication acceptance remains separately outside this repair.'})
dump('BUILD_VERIFICATION.json',{'schema':'pr259-outer-coverage-local-build-verification-v1','utc':UTC,'decision':'PASS_LOCAL_PREPARATION_METADATA_CONSTRUCTION_ONLY','checks':len(checks),'check_labels':checks,
     'prep_completion_percent':90,'case_complete':False,'no_scientific_or_promotion_or_execution_acceptance':True,'provider_actions':0,'shared_git_actions':0})
print(json.dumps({'actual_v02_inventory':len(inventory),'original247_entries_authenticated':True,'complete_fresh_review_files':len(reviewinventory),'checks':len(checks),'new_scientific_acceptance':False},indent=2))
