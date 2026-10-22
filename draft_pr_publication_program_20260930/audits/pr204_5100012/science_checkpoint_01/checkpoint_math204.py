"""PR204 math45 checkpoint: Root's scoped mathematics, not operational endorsement.
Root alone executes prepare. No ref/PR/tracker writes. Normal interpreter with -B.
The sealed custody15 receipt remains historical; phase authority is explicitly45.
"""
from pathlib import Path
import datetime,hashlib,importlib.util,json,os,re,sys
if sys.flags.optimize or not sys.dont_write_bytecode:
    raise RuntimeError('Use ordinary Python with -B; optimization or bytecode writes forbidden')
D=Path(__file__).resolve().parent;A=D.parent;P=A.parent.parent;ROOT=P.parent
CUSTODY=A/'custody_checkpoint_01'
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
CORE_PIN={'bytes':33976,'sha256':'520171b2a762625cd58a08873dea7b1795671c492af138d86958b1928c603593'}
require(pin((CUSTODY/'checkpoint204.py').read_bytes())==CORE_PIN,'Sealed custody helper drift')
sp=importlib.util.spec_from_file_location('custody204_sealed_native_primitives',CUSTODY/'checkpoint204.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
CASE=v.CASE;PREFIX=v.PREFIX;Q=v.Q;HEAD=v.HEAD;OWN=CASE+'science_checkpoint_01/';VIEWS=v.VIEWS
ROOT_GATE='ROOT_MATHEMATICAL_ACCEPTANCE_01.json'
ROOT_GATE_PIN={'bytes':4887,'sha256':'970aa71eac868d3ef4b0a57132a90a6c33e1dc0ac53e96f5ddbfab859bc23f59'}
ROOT_READING='ROOT_CANDIDATE_READING_AND_DERIVATION_01.md'
ROOT_READING_PIN={'bytes':6443,'sha256':'fe61d18c55c744bba79e4383594af7a760ca09c57577fc31e504f7d39d7c681f'}
REPAIR_GATE='ROOT_VERIFICATION_REPAIR_ACCEPTANCE_01.json'
REPAIR_GATE_PIN={'bytes':2276,'sha256':'838ee963a9bb58e07b2f63b58b3704cccbf622fb87b537aab4768dd7d5899d0c'}
CUSTODY_MANIFEST_PIN={'bytes':1209,'sha256':'e7d21a6820fa4904023971b70c16112641a66216ebc6f6d45d437a46ec79b19b'}
PRIVATE_INVENTORY='math_direct_geometry_01/RUNTIME_CACHE_INCIDENT_01.json'
OWN_FILES=['checkpoint_math204.py','SCIENCE_INPUT_BINDINGS.json','RESOLVED_RUNTIME_INCIDENT.md','CHECKPOINT_CONTRACT.md','RESEARCH_LOG.md','SAFE_AUTHORED_MANIFEST.json']
STATUS='ROOT_SCOPED_MATHEMATICS_SOURCE_AND_VERIFICATION_REPAIRS_ACCEPTED_PRIORITY_ACTIVE'
CLAIM='For a>b>0,0<lambda<b^2 and a fixed proper confocal elliptical caustic, signed trajectory area times signed area of perpendicular feet from center O to the original complete supporting side lines is phase independent on physical orbits of least N>=3, N odd or divisible4. Includes admitted coprime stars, either direction, signed zero/negative; no segment clipping. Unrestricted repeated-list extension is false.'
WARNING='RGK Table3 k203,b is signed trajectory area times original-side origin-pedal area in a proper confocal ellipse pair, N not congruent2mod4. Printed table does not literally say least/primitive; explicit least physical period is a necessary qualified convention. An exact physical6 duplicated to nominal12 refutes unrestricted list-length wording. Historical question marks/imported OPEN-TRIAGE do not certify current openness, novelty or priority.'
INDEPENDENCE='Four assigned audits complete. Source-analytic and complex families froze routes independently before exposure but completed universal Jacobi verification after reading the submitted mechanism. Direct geometry proves all N3/N4 and keeps the general route partial/blocked. Physical/exact family supplies independent finite diagnostics and low-period controls, not a universal proof. Root flag route is unfinished and supplies no additional proof. No independent-discovery claim.'
REMAIN='Finish bounded deep positive-priority audit. Root separately accepted finite-verification integrity repairs; historical original optimized enforcement defect remains disclosed. Priority NOT CLEARED; no paper, deposit, whole-package reviews, tracker update, original PR mutation/merge or next-PR advance. Later package promotion requires its own gates.'
FAMILY_STATUS=[
 {'family':'math_source_analytic_01','assigned_audit_complete':True,'universal_route':'Verified submitted Jacobi mechanism after exposure; early source/analytic plan independent.'},
 {'family':'math_independent_complex_01','assigned_audit_complete':True,'universal_route':'Verified submitted meromorphic/Jacobi mechanism after exposure; early complex plan independent.'},
 {'family':'math_direct_geometry_01','assigned_audit_complete':True,'universal_route':'PARTIAL/BLOCKED; complete independent N3/N4 only, general scalar step unproved.'},
 {'family':'math_algebra_physical_01','assigned_audit_complete':True,'universal_route':'Finite independent physical diagnostics and exact low-period controls; no universal proof.'}
]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(p):return json.loads(p.read_bytes())
def enc(j):return (json.dumps(j,indent=2)+'\n').encode()
def save(p,b):
    require(p.resolve().is_relative_to(D),'Output outside science helper directory')
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    p.chmod(0o444)
def safe_relative(s):
    p=Path(s);require(not p.is_absolute() and '..' not in p.parts and s and not s.endswith('/'),'Unsafe artifact path');return s
def frozen(rel,expected=None):
    safe_relative(rel);p=A/rel
    require(p.is_file() and not p.is_symlink() and p.stat().st_mode&0o777==0o444,'Unfrozen artifact '+rel)
    b=p.read_bytes()
    if expected is not None:require(pin(b)==expected,'Pinned artifact drift '+rel)
    return b
def inputs():
    """Verify all explicit source/family allowlists; exclude only private inventory."""
    out={};gate=json.loads(frozen(ROOT_GATE,ROOT_GATE_PIN));frozen(ROOT_READING,ROOT_READING_PIN)
    require(gate['estimate_case_completion_percent']==45 and gate['original_head']==HEAD and gate['verdict'].startswith('MATHEMATICAL PASS'),'Root mathematical scope')
    require(not gate['priority_clearance'] and not gate['whole_package_review_clearance'] and not gate['publication_clearance'],'Root gate grants no later clearance')
    require(gate['root_full_reading_and_calculations']=={'path':ROOT_READING,**ROOT_READING_PIN},'Root reading binding')
    require(len(gate['verified_family_artifacts'])==4 and {x['family'] for x in gate['verified_family_artifacts']}==set(v.FAMILIES),'Four assigned mathematical audits')
    custody_manifest=frozen('custody_checkpoint_01/SAFE_AUTHORED_MANIFEST.json',CUSTODY_MANIFEST_PIN);cm=json.loads(custody_manifest)
    require(set(cm['files'])==set(v.OWN_FILES)-{'SAFE_AUTHORED_MANIFEST.json'},'Sealed01 explicit allowlist')
    for name,x in cm['files'].items():out['custody_checkpoint_01/'+name]=pin(frozen('custody_checkpoint_01/'+name,x))
    out['custody_checkpoint_01/SAFE_AUTHORED_MANIFEST.json']=pin(custody_manifest)
    cr=json.loads(frozen('custody_checkpoint_01/INDEPENDENT_CUSTODY_RECHECK.json',cm['files']['INDEPENDENT_CUSTODY_RECHECK.json']))
    require(cr['case_percent']==15 and not cr['mathematical_clearance'] and not cr['priority_clearance'],'Historical custody receipt must retain15 scope')
    for rel in v.INPUTS:out[rel]=pin(frozen(rel,cr['input_pins'][rel]))
    for rel,x in cr['original_files'].items():
        b=frozen('original_submitted_head/'+rel,{z:x[z] for z in ['bytes','sha256']});require(v.bpin(b)['git_blob']==x['git_blob'],'Original native blob identity');out['original_submitted_head/'+rel]=pin(b)
    require(len(cr['original_files'])==20 and sum(x['bytes'] for x in cr['original_files'].values())==59343,'Original archive census')
    out[ROOT_GATE]=ROOT_GATE_PIN;out[ROOT_READING]=ROOT_READING_PIN
    excluded={};families=[]
    for entry in gate['verified_family_artifacts']:
        family=entry['family'];mr=entry['manifest']['path'];require(mr.startswith(family+'/'),'Family manifest containment')
        mb=frozen(mr,{k:entry['manifest'][k] for k in ['bytes','sha256']});man=json.loads(mb);out[mr]=pin(mb)
        if family=='math_source_analytic_01':
            rows=man['sha256_excluding_this_self_manifest'];require(set(rows)|{Path(mr).name}==set(man['exact_authored_allowlist']),'Source family exact allowlist')
        elif family=='math_independent_complex_01':
            rows={x['path']:{k:x[k] for k in ['bytes','sha256']} for x in man['files']};require(len(rows)==len(man['files']),'Complex duplicate artifact')
        elif family=='math_direct_geometry_01':
            rows={x['relative_path']:{k:x[k] for k in ['bytes','sha256']} for x in man['files']};require(len(rows)==len(man['files']),'Direct duplicate artifact')
            for x in man['files']:require(Path(x['path']).resolve()==(A/family/x['relative_path']).resolve(),'Direct absolute/relative binding')
        else:rows=man['files']
        require(len(rows)==entry['content_files_verified'] and sum(x['bytes'] for x in rows.values())==entry['total_content_bytes'],'Root family content census')
        included=0
        for name,x in rows.items():
            safe_relative(name);rel=family+'/'+name
            require(not any(t in Path(name).parts for t in ['disposable_unchanged','disposable_false_identity','repaired_original_controls_01']),'Disposable or later repair artifact in sealed family allowlist')
            b=frozen(rel,x)
            if rel==PRIVATE_INVENTORY:excluded[rel]=pin(b);continue
            out[rel]=pin(b);included+=1
        rr=entry['report'];require(out[rr['path']]=={k:rr[k] for k in ['bytes','sha256']},'Root report binding')
        families.append({'family':family,'manifest':entry['manifest'],'included_content_files':included,'excluded_private_inventory_files':len(rows)-included})
    require(set(excluded)=={PRIVATE_INVENTORY},'Only identified runtime inventory excluded')
    repair=json.loads(frozen(REPAIR_GATE,REPAIR_GATE_PIN));out[REPAIR_GATE]=REPAIR_GATE_PIN
    require(repair['mathematical_acceptance']=={'path':ROOT_GATE,**ROOT_GATE_PIN} and repair['verification_integrity_required_repairs_complete'],'Repair acceptance binding/integrity')
    require(not repair['priority_clearance'] and not repair['whole_package_clearance'] and not repair['publication_ready'] and repair['original_evidence_not_rewritten'] and repair['no_finite_or_noninterval_test_is_a_universal_proof'],'Repair gate scope')
    require(len(repair['accepted_supplement_manifests'])==2,'Exactly two accepted repair supplements')
    supplement_files=0
    for entry in repair['accepted_supplement_manifests']:
        mr=entry['manifest']['path'];mp={k:entry['manifest'][k] for k in ['bytes','sha256']};man=json.loads(frozen(mr,mp));out[mr]=mp;parent=Path(mr).parent.as_posix()
        require(parent in ['math_independent_complex_01/v2_validation','math_algebra_physical_01/repaired_original_controls_01'],'Unexpected repair supplement')
        rows=man['files']
        if isinstance(rows,list):
            items=rows;rows={x['path']:{k:x[k] for k in ['bytes','sha256']} for x in items};require(len(rows)==len(items),'Duplicate repair file')
        require(len(rows)==entry['content_files_verified'] and sum(x['bytes'] for x in rows.values())==entry['total_bytes'],'Repair content census')
        for name,x in rows.items():
            safe_relative(name);rel=parent+'/'+name;require(rel not in out,'Duplicate scientific artifact');out[rel]=pin(frozen(rel,x));supplement_files+=1
    require(supplement_files==37,'Exactly37 accepted repair content artifacts')
    # These are small Root incident facts; the 512k inventory is never public.
    cleanup=read(A/'PRIVATE_REGENERABLE_RUNTIME_CLEANUP_01.json')
    require(cleanup['inventory_sha256']==excluded[PRIVATE_INVENTORY]['sha256'] and cleanup['all_inventory_records_validated_before_cleanup'] and cleanup['all_deleted_paths_now_absent'],'Resolved runtime incident validation')
    return {'UTC':now(),'PR':204,'phase':'math45','case_percent':45,'authority':'Root scoped mathematical acceptance and separate finite-verification repair acceptance; operational helper only authenticates exact artifacts.','Root_mathematical_acceptance_pin':ROOT_GATE_PIN,'Root_verification_repair_acceptance_pin':REPAIR_GATE_PIN,'historical_custody_case_percent':15,'files':out,'excluded_private_inventory':excluded,'private_cleanup_receipt_pin':pin((A/'PRIVATE_REGENERABLE_RUNTIME_CLEANUP_01.json').read_bytes()),'families':families,'repair_supplement_content_files':37,'qualified_mathematical_and_source_clearance_from_Root':True,'priority_active':True,'priority_clearance':False,'verification_integrity_required_repairs_complete':True,'verification_code_publication_clearance':False,'paper_or_deposit_prepared':False}
def check_bindings():
    b=read(D/'SCIENCE_INPUT_BINDINGS.json');fresh=inputs()
    require({k:x for k,x in b.items() if k!='UTC'}=={k:x for k,x in fresh.items() if k!='UTC'},'Scientific artifact binding changed')
    j=read(D/'SAFE_AUTHORED_MANIFEST.json');require(set(j['files'])==set(OWN_FILES)-{'SAFE_AUTHORED_MANIFEST.json'},'Science authored allowlist')
    for n,x in j['files'].items():frozen('science_checkpoint_01/'+n,x)
    return b
def overlay(c,h,parent,stamp):
    b=check_bindings();out={CASE+rel:frozen(rel,x) for rel,x in b['files'].items()}
    for name in OWN_FILES:out[OWN+name]=frozen('science_checkpoint_01/'+name)
    p=json.loads(v.native_body(h,PREFIX+'CURRENT_PROGRESS.json',parent))
    require((p['current_PR'],p['fully_completed_count'],p['published_count'],p['last_completed_PR'],p['current_PR_workflow_percent'],p['current_completed'])==(203,46,30,203,100,True),'Actual203 must remain preceding case')
    retired={k:p[k] for k in list(p) if k.lower().startswith(('current_','next_','conditional_','program_snapshot_')) or k in ['advance_to_next_PR_authorized_now','remaining_current_step','next_step','latest_ordered_intake_record','latest_ordered_intake_records']}
    p.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':203,'prior_phase':'actual_completed_before204_combined_math45_checkpoint','actual_completion_commit':v.BASE_COMMIT,'actual_completion_receipt_pin':v.BASE_ACCEPT,'values':retired})
    for k in retired:del p[k]
    gate_ref={'path':'audits/pr204_5100012/'+ROOT_GATE,**ROOT_GATE_PIN};repair_ref={'path':'audits/pr204_5100012/'+REPAIR_GATE,**REPAIR_GATE_PIN}
    case={'UTC':stamp,'PR':204,'problem_id':5100012,'original_head':HEAD,'original_QUEUE_status':'claimed_solved','original_QUEUE_effort_cell':'1/5','original_effort':'Original QUEUE reports1/5; actual model/reasoning effort unverified. New audits are not original author effort.','status':STATUS,'case_percent':45,'exact_claim':CLAIM,'source_contract_record':'ROOT_SOURCE_FIRST_CONTRACT_01.md','source_contract_clearance':True,'source_contract_clearance_qualified':True,'source_provenance_warning':WARNING,'original_archive_files':20,'original_native_bytes':59343,'historical_custody_receipt':'custody_checkpoint_01/INDEPENDENT_CUSTODY_RECHECK.json','historical_custody_case_percent':15,'mathematical_gate':gate_ref,'mathematical_acceptance_authority':'Root accepted exact four-family reports, independently from this operational helper.','mathematical_clearance':True,'mathematical_result_valid':True,'independent_mathematical_families':v.FAMILIES,'independent_mathematical_families_active':False,'independent_mathematical_families_complete':4,'independent_family_statuses':FAMILY_STATUS,'universal_Jacobi_verification_families_after_exposure':2,'independence_limits':INDEPENDENCE,'direct_geometry_general_route':'PARTIAL/BLOCKED; independent fullN3/N4 only.','Root_flag_route_accepted_as_proof':False,'independent_discovery_certified':False,'historical_novelty_or_firstness_established':False,'priority_audit_active':True,'priority_audit_complete':False,'priority_clearance':False,'original_optimized_checker_false_mutations_accepted':True,'verification_code_publication_clearance':False,'verification_code_hardening_pending_separate_gate':False,'verification_code_hardening_receipt_consumed_by_this_checkpoint':True,'verification_integrity_required_repairs_complete':True,'verification_repair_gate':repair_ref,'code_clearance_not_a_remaining_mathematical_theorem_gap':True,'publication_ready':False,'paper_prepared':False,'deposit_prepared':False,'whole_publication_package_reviews_complete':False,'actual_Zenodo_published':False,'actual_tracker_updated':False,'actual_original_PR_merged':False,'actual_factual_MAIN_accepted':False,'completed':False,'fully_completed_count':46,'published_count':30,'last_completed_PR':203,'next_numeric_intake_cursor':204,'conditional_next_numeric_intake_cursor':205,'advance_to_next_PR_authorized_now':False,'remaining_required_steps':REMAIN,'goal_complete':False,'checkpoint_postimage_effective_only_after_own_actual_MAIN_full_scope_acceptance':True}
    out[CASE+'CURRENT_CASE_STATUS.json']=enc(case)
    note='\n'+stamp+' — PR204 combined custody/source/math checkpoint45%: original HEAD'+HEAD+', claimed_solved1/5 and all20 files59343B preserved. Historical independent custody15 receipt retained unchanged. Root accepted scoped least-physical-period signed original-side origin-pedal theorem and qualified source contract via exact receipt '+ROOT_GATE_PIN['sha256']+'. Four assigned audits complete: two universal Jacobi verifications after exposure, direct fullN3/N4 with general route blocked, physical finite diagnostics; no independent-discovery claim. Source table does not literally say least/primitive; unrestricted repeated-list extension false. Priority ACTIVE/NOT CLEARED; Root separately accepted required finite-verification integrity repairs; original optimized defect remains historical. No paper/deposit/package review/tracker/PRmerge/advance.46completed/30published,last203,cursor204/advancefalse; goal active.\n'
    initial=(A/'RESEARCH_LOG.md').read_bytes();cr=read(CUSTODY/'INDEPENDENT_CUSTODY_RECHECK.json');require(pin(initial)==cr['initial_case_log_pin'],'Original local intake log changed')
    out[CASE+'RESEARCH_LOG.md']=initial+note.encode()
    p.update(UTC=stamp,updated_UTC=stamp,current_PR=204,current_problem_id=5100012,current_original_head=HEAD,current_original_QUEUE_status='claimed_solved',current_original_QUEUE_effort_cell='1/5',current_original_budget=case['original_effort'],current_PR_workflow_percent=45,current_workflow_estimate_percent=45,current_status=STATUS,current_completed=False,current_closed=False,current_closed_without_merge=False,current_original_PR_state='open',current_original_PR_merged=False,current_original_PR_open_draft=True,current_mathematical_clearance=True,current_mathematics_cleared=True,current_mathematical_result_valid=True,current_mathematical_gate=gate_ref,current_mathematical_acceptance_authority=case['mathematical_acceptance_authority'],current_source_contract_clearance=True,current_source_contract_clearance_qualified=True,current_source_contract='audits/pr204_5100012/ROOT_SOURCE_FIRST_CONTRACT_01.md',current_source_provenance_warning=WARNING,current_independent_mathematical_audit_active=False,current_independent_mathematical_audit_families=4,current_independent_mathematical_audit_families_complete=4,current_independent_mathematical_audit_names=v.FAMILIES,current_independent_family_statuses=FAMILY_STATUS,current_universal_Jacobi_verification_families_after_exposure=2,current_independence_limits=INDEPENDENCE,current_direct_geometry_general_route=case['direct_geometry_general_route'],current_Root_flag_route_accepted_as_proof=False,current_priority_audit_active=True,current_priority_audit_complete=False,current_priority_clearance=False,current_historical_novelty_or_firstness_established=False,current_independent_discovery_certified=False,current_theorem_novelty_cleared=False,current_proof_method_novelty_cleared=False,current_verification_code_publication_clearance=False,current_verification_code_hardening_pending_separate_gate=False,current_verification_code_hardening_receipt_consumed_by_this_checkpoint=True,current_verification_integrity_required_repairs_complete=True,current_verification_repair_gate=repair_ref,current_code_clearance_not_a_remaining_mathematical_theorem_gap=True,current_publication_ready=False,current_paper_prepared=False,current_deposit_prepared=False,current_publication_package=None,current_publication_package_reviews_complete=False,current_NEW_whole_publication_package_reviews_completed=0,current_NEW_whole_publication_package_review_active=False,current_Zenodo_published=False,current_DOI=None,current_tracker_updated=False,current_tracker_range=None,current_actual_publication_verified=False,current_actual_tracker_row_verified=False,current_actual_merge_accepted=False,current_actual_factual_checkpoint_accepted=False,current_record='audits/pr204_5100012/CURRENT_CASE_STATUS.json',current_exact_claim=CLAIM,current_remaining_required_steps=REMAIN,remaining_current_step=REMAIN,next_step=REMAIN,next_numeric_intake_cursor=204,conditional_next_numeric_intake_cursor=205,advance_to_next_PR_authorized_now=False,next_intake_requires_actual_completion_receipt=True,next_intake_requires_actual_completed_PR=204,next_status_only_intake_performed=True,latest_ordered_intake_record='audits/pr204_5100012/ORIGINAL_STATUS_INTAKE.json',persistent_goal_complete=False,goal_work_continuing=True,program_snapshot_semantics='PR203 actual completion retained:46completed/30published,last203. PR204 original claimed_solved1/5/all20files custody preserved. Root accepted explicit least-period signed origin-pedal theorem and qualified source contract at45%; four assigned audits complete with two exposed universal Jacobi verifications, general direct route partial and physical finite. Priority active/notcleared; required finite-verification integrity repairs separately Rootaccepted; no paper/deposit/PRmerge/advance.',program_snapshot_authority_condition='Math45 postimage effective only after Root actual trueparent/fullforeignscope/everyselectedidentity acceptance. Root mathematical receipt supplies scientific authority; this helper supplies operational custody only.')
    out[PREFIX+'CURRENT_PROGRESS.json']=enc(p)
    for name in ['CURRENT_PROGRESS.md','RESEARCH_LOG.md']:out[PREFIX+name]=v.native_body(h,PREFIX+name,parent)+note.encode()
    require(Q not in out and not any(k.startswith('unsolved_math_prioritization/attempts/') for k in out),'Forbidden QUEUE/native overlay')
    require(CASE+PRIVATE_INVENTORY not in out and not any('/disposable_' in k  for k in out),'Private inventory/disposable copied')
    return out
def message(d):return 'PR204 math45: Root accepted scoped origin-pedal theorem; priority active\n\nQualified least physical period; four assigned audits complete with independence and general-route limits explicit. Required finite-verification integrity repairs separately accepted; publication clearance pending.46completed/30published,last203,cursor204,advancefalse.\nPR204 mathematical selected-map SHA256: '+d
v.message=message # Reuse the sealed generic exact-parent/full-leaf verifier with this phase message.
def generation(name):
    require(re.fullmatch('[a-z][a-z0-9_]{0,48}',name) is not None,'Unsafe generation name');return D/name
def facts():return {'case_percent':45,'Root_mathematical_acceptance_pin':ROOT_GATE_PIN,'Root_verification_repair_acceptance_pin':REPAIR_GATE_PIN,'verification_integrity_required_repairs_complete':True,'mathematical_clearance':True,'source_contract_clearance':True,'source_contract_clearance_qualified':True,'mathematical_result_valid':True,'assigned_mathematical_audits_complete':4,'universal_Jacobi_verification_families_after_exposure':2,'independent_discovery_certified':False,'priority_audit_active':True,'priority_clearance':False,'verification_code_publication_clearance':False,'publication_ready':False,'paper_or_deposit_prepared':False,'fully_completed_count':46,'published_count':30,'last_completed_PR':203,'next_numeric_intake_cursor':204,'advance_to_next_PR_authorized_now':False,'goal_complete':False}
def run(mode,name):
    c,h,rv,n=v.load();base=v.baseline(c);dest=generation(name)
    if mode=='prepare':
        require(not dest.exists(),'Generation exists');parent=h.api('git/ref/heads/main')['object']['sha']
        require(h.api('compare/'+v.BASE_COMMIT+'...'+parent)['status'] in ['identical','ahead'],'Fresh MAIN must descend from actual203')
        inherited,ack=v.reconcile(c,h,base,parent);pt=c.selected_current(h,parent,inherited,base['tree']);v.validate_caches(h);v.unchanged_pr();stamp=now();out=overlay(c,h,parent,stamp)
        # Capture/validate all local guards before creating remote native objects.
        local_pre={}
        for rel in VIEWS:
            p=ROOT/rel;local_pre[rel]=pin(p.read_bytes()) if p.exists() else None;remote=v.native_body(h,rel,parent)
            if not rel.startswith(CASE):require(remote is not None and local_pre[rel]==pin(remote),'Global3 local/fresh-parent mismatch')
            elif rel==CASE+'CURRENT_CASE_STATUS.json':require(not p.exists() and remote is None,'Newcase status must be absent')
            else:require(remote is None and local_pre[rel]==read(CUSTODY/'INDEPENDENT_CUSTODY_RECHECK.json')['initial_case_log_pin'],'Newcase local intake-log pin')
        dest.mkdir();save(dest/'FOREIGN_QUEUE_RECONCILIATION.json',enc(ack));out[OWN+name+'/FOREIGN_QUEUE_RECONCILIATION.json']=(dest/'FOREIGN_QUEUE_RECONCILIATION.json').read_bytes();expected=v.selected(c,inherited,out)
        # Root alone executes these two native-object writes. No ref or PR write exists.
        tree=h.api('git/trees','POST',{'base_tree':pt,'tree':[{'path':k,'mode':'100644','type':'blob','content':z.decode('utf-8')} for k,z in sorted(out.items())]})['sha']
        commit=h.api('git/commits','POST',{'tree':tree,'parents':[parent],'message':message(c.selected_digest(expected))})['sha']
        h.m.m.h.warm_selected_directories([pt,tree],expected)
        r={'UTC':stamp,'PR':204,'phase':'math45',**facts(),'original_head':HEAD,'expected_main':parent,'parent_tree':pt,'tree':tree,'commit':commit,'selected_files':expected,'selected_map_sha256':c.selected_digest(expected),'overlay_paths':sorted(out),'changed_paths':sorted(k for k,x in expected.items() if h.lookup(pt,k)!=('100644','blob',x['git_blob'])),'local_five_expected_preimages':local_pre,'MAIN_moved':False};save(dest/'PREPARATION.json',enc(r))
    else:
        r=read(dest/'PREPARATION.json');require(r['phase']=='math45' and all(r[k]==x for k,x in facts().items()),'Prepared phase facts')
        parent=r['expected_main'];stamp=r['UTC'];ack=read(dest/'FOREIGN_QUEUE_RECONCILIATION.json');inherited={**base['selected_files'],Q:ack['current_QUEUE']};out=overlay(c,h,parent,stamp);out[OWN+name+'/FOREIGN_QUEUE_RECONCILIATION.json']=(dest/'FOREIGN_QUEUE_RECONCILIATION.json').read_bytes();expected=v.selected(c,inherited,out)
    v.verify(c,h,r,out,expected);main=h.api('git/ref/heads/main')['object']['sha']
    if mode in ['prepare','verify']:
        require(main==parent,'MAIN changed; regenerate against fresh parent')
        pre={'UTC':now(),'PR':204,'phase':'math45','commit':r['commit'],'expected_main':parent,'observed_MAIN':main,'exact_single_trueparent_fullforeignscope_everyselectedidentity_verified':True,'original_head_unchanged':True,'no_QUEUE_native_or_PR_mutation':True,'selected_files':len(expected),'selected_map_sha256':r['selected_map_sha256'],'actual_MAIN_acceptance':False,**facts()}
        if mode=='prepare':save(dest/'ROOT_PRE_MOVE_VERIFICATION.json',enc(pre))
        print(json.dumps({'mode':mode,'expected_main':parent,'commit':r['commit'],'tree':r['tree'],'selected_files':len(expected),'selected_map_sha256':r['selected_map_sha256'],'changed_paths':len(r['changed_paths']),'observed_MAIN':main,**facts()}));return
    require(mode=='accept','Unsupported phase');require(h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'],'Actual MAIN lacks checkpoint')
    actual,post=v.reconcile(c,h,r,main);actual_tree=c.selected_current(h,main,actual,r['tree']);v.validate_caches(h);v.unchanged_pr()
    for k,z in out.items():require(c.byte_pin(z)==expected[k] and h.lookup(actual_tree,k)==('100644','blob',expected[k]['git_blob']),'Actual overlay identity drift '+k)
    body=enc({'selected_files':actual,'selected_map_sha256':c.selected_digest(actual),'foreign_QUEUE_reconciliation_after_checkpoint':post});save(dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json',body)
    a={'UTC':now(),'PR':204,'phase':'math45','accepted':True,'checkpoint_commit':r['commit'],'sole_parent':parent,'main_observed':main,'actual_tree':actual_tree,'original_head':HEAD,'original_PR_open_draft_unchanged':True,'selected_files':len(actual),'selected_map_sha256':r['selected_map_sha256'],'actual_current_selected_map_sha256':c.selected_digest(actual),'actual_current_map_file':pin(body),'every_selected_identity_checked_at_actual_observed_MAIN':True,'all_overlay_body_identities_verified':True,'full_foreign_tree_scope_preserved_at_checkpoint':True,'foreign_QUEUE_exact_byte_acknowledgement':True,'QUEUE_native_original_PR_unchanged_by_checkpoint':True,'scientific_authority':'Exact Root acceptance receipt, not a mathematical endorsement by operational helper.',**facts()};save(dest/'ACCEPTANCE.json',enc(a));print(json.dumps(a))
def sync(name):
    c,h,rv,n=v.load();dest=generation(name);r=read(dest/'PREPARATION.json');a=read(dest/'ACCEPTANCE.json');mp=read(dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json')
    require(a['accepted'] and a['every_selected_identity_checked_at_actual_observed_MAIN'] and a['checkpoint_commit']==r['commit'] and all(a[k]==x for k,x in facts().items()),'Actual math45 acceptance required')
    require(a['actual_current_map_file']==pin((dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json').read_bytes()) and mp['selected_map_sha256']==a['actual_current_selected_map_sha256']==c.selected_digest(mp['selected_files']),'Actual accepted map drift')
    main=h.api('git/ref/heads/main')['object']['sha'];require(h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'],'Checkpoint no longer on MAIN');c.selected_current(h,main,mp['selected_files'],a['actual_tree']);v.validate_caches(h);rows=[]
    for rel in VIEWS:
        p=ROOT/rel;post=v.native_body(h,rel,r['commit']);require(c.byte_pin(post)==r['selected_files'][rel],'Local postimage drift');old=p.read_bytes() if p.exists() else None
        require((None if old is None else pin(old)) in [r['local_five_expected_preimages'][rel],pin(post)],'Unexpected local view change '+rel)
        if old!=post:
            tmp=p.with_name(p.name+'.pr204_math45_sync_tmp')
            with tmp.open('xb') as f:f.write(post);f.flush();os.fsync(f.fileno())
            require(tmp.read_bytes()==post,'Temporary bytes');tmp.chmod(0o444);os.replace(tmp,p)
        p.chmod(0o444);require(p.read_bytes()==post,'Local readback');rows.append({'path':rel,'postimage':pin(post),'prior_or_postimage_guard':True})
    j={'UTC':now(),'PR':204,'phase':'math45','actual_checkpoint':r['commit'],'all_five_local_files_match_actual_checkpoint':True,'files':rows,**facts()};save(dest/'LOCAL_GLOBAL_FIVE_SYNC.json',enc(j));print(json.dumps(j))
if __name__=='__main__':
    require(len(sys.argv)>=2,'bindings | prepare GEN | verify GEN | accept GEN | sync GEN')
    mode=sys.argv[1]
    if mode=='bindings':require(len(sys.argv)==2,'bindings takes no generation');j=inputs();save(D/'SCIENCE_INPUT_BINDINGS.json',enc(j));print(json.dumps({'phase':'math45','files':len(j['files']),'public_bytes':sum(x['bytes'] for x in j['files'].values()),'excluded_private_inventory_files':len(j['excluded_private_inventory']),'Root_gate_pin':ROOT_GATE_PIN,'no_remote_mutation':True}))
    elif mode=='sync':require(len(sys.argv)==3,'sync GEN');sync(sys.argv[2])
    else:require(mode in ['prepare','verify','accept'] and len(sys.argv)==3,'Unknown phase');run(mode,sys.argv[2])
