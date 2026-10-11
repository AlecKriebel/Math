"""Own source author: reads closed PR42 V2 text, writes only this family's source."""
from pathlib import Path
import json, hashlib, re, datetime, os, difflib
H=Path(__file__).resolve().parent;A=H.parent;R=A.parents[2]
PREV=R/'draft_pr_publication_program_20260930/audits/pr42_2233/acceptance_preparation_family_v2'
sha=lambda b:hashlib.sha256(b).hexdigest()
stamp=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(ok,msg):
    if not ok:raise ValueError(msg)
def encode(o):return (json.dumps(o,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
def pin(p):
    raw=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(raw),'sha256':sha(raw)}
def put(name,raw):
    p=H/name;require(not p.exists(),'Absent own prepared source required: '+name);p.write_bytes(raw if isinstance(raw,bytes) else raw.encode())
def dump(name,o):put(name,encode(o))
raw=(PREV/'PREPARATION_MANIFEST.json').read_bytes()
require(sha(raw)=='f5cd2d41d448c97fcf160afeca63dc4c57c283deb03ffa4fe2292125db06b1a8','Closed exact PR42 V2 source basis required')
prior=json.loads(raw);require(prior['files_count']==51 and prior['source_only'] is True,'51 own source members')
for z in prior['files']:
    b=(PREV/z['path']).read_bytes();require(len(b)==z['bytes'] and sha(b)==z['sha256'],'Entire closed source basis')
sources={n:(PREV/n).read_text() for n in ['pr42_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py']}
require(sha(sources['pr42_guards.py'].encode())=='f7d7116101a21dc79dcbbf6049436be51ac469e1359a020229d4ddd916ef960a','Literal revised guard')
def identity(text):
    for x,y in [('PR42','PR43'),('pr42','pr43'),('2233','30004386'),('EP-653','OWR-17469-011'),('099ae5e4d06d8789214cfaaece87309c87e914f9','86be0f85c7a37a5cad8d24abd16a32d8d1f27e62')]:text=text.replace(x,y)
    return text
def replace_function(text,name,new):
    match=re.search(r'^def '+re.escape(name)+r'\([^\n]*\):.*?(?=^def |\Z)',text,re.M|re.S)
    require(match is not None,'One named source function required: '+name)
    return text[:match.start()]+new.strip()+'\n\n\n'+text[match.end():]
science={'full_problem_solved':False,'full_target_resolved_in_prior_published_literature':True,'full_problem_solved_by_project':False,'prior_publication_doi':'10.4064/sm210413-16-9','partial_valid':True,'novelty_claimed':False,'priority_claimed':False,'original_substantive_attempts':0,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'verification_attempts_added':0,'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'paper_or_new_doi_or_tracker':False,'human_referee_review_claimed':False}
scope={'schema':'pr43-proposed-accepted-scientific-scope/v1','id':'30004386','problem_number':'OWR-17469-011','literal_target_status':'already_solved','full_target_resolved_in_prior_published_literature':True,'full_problem_solved_by_project':False,'novelty_claimed':False,'priority_claimed':False,'prior_publication_doi':'10.4064/sm210413-16-9','prior_authors':['Samuel G. G. Johnston','Zakhar Kabluchko','Joscha Prochno'],'publication':'Studia Mathematica264(2022)103-119; online17December2021','literal_model':'Random conditional probability law of sum of independent Uniform[-1,1] variables with Haar-uniform unit direction; fixed projection dimension1, weakP(R) or Prohorov topology, speedN. Probability is over the direction, not a sampled scalar or its direction average.','target_and_resolution':'JKP TheoremA supplies the full good LDP; Proposition3.1 and all-N unit-vector fillers supply exactly all Gaussian-completed square-summable uniform series with coefficient norm<=1 as Prohorov limits.','rate':'-log(1-||a||^2)/2 for canonical coefficient norm<1; infinity for norm1 or outside compact law image. Boundary laws stay in the full limit set.','normalization':'Gaussian missing coefficient mass has variance(1-||a||^2)/3; every target law has variance1/3. Coordinate topology and no l1 assumption.','printed_source_repairs':json.loads((A/'reviewed_candidate/status.json').read_bytes())['printed_source_repairs'],'proof_limits':'Read complete12-page arXivv2 author manuscript and operativeOWR411-413 plus rendered formulas; typeset journal proof not obtained or byte-certified; not all40-page workshop or every foundational work. No exhaustive priority or current-open claim.','qualification_path':'SOURCE_PRECISION_QUALIFICATIONS.md','qualification_sha256':'868b8e2af799f8371c3900529079af354ef51cf01ee08adeccc666ec0884d3cd','prior_semantics':'Raw OWR-17469-011 key absent; saved{} is exactSQL importer fallback, not retrieved prior/null. Dated2026OPEN triage is historical background.','saved_result_qualification':'Current527 author replay differs from historical527 only in bound SOURCE_STATUS hash; final90402aea source differs from historical98918841 only in review-status sentence; historical527 and independent664 full saved objects reproduce exactly. Finite controls do not prove an LDP.','original16_and_SOURCE_STATUS_unchanged':True,'historical_metadata_archival_only':True,'original_substantive_attempts':0,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'paper_or_new_DOI_or_tracker':False}
draft={'schema':'pr43-root-approved-immutable-acceptance-bindings/v1','status':'PENDING_ROOT_SOURCE_AND_PREDECESSOR_READING','created_utc':None,'root_full_current_read_completed':False,'root_full_whole_read_completed':False,'root_acceptance_source_review_completed':False,'independent_whole_current_pass':False,'root_actual_PR42_predecessor_read_completed':False,'mandatory_corrections':[],'original_substantive_attempts':0,'new_substantive_attempts':0,'audit_turns':0,'whole_manifest':None,'root_whole_inspection':None,'root_capture_operator':None,'previous_mirror':None,'previous_post':None,'previous_root_post':None}
dump('SCIENTIFIC_SCOPE.json',scope);dump('DRAFT_ROOT_IMMUTABLE_BINDINGS.json',draft)
dump('DRAFT_FINAL_PLAN.json',{'schema':'pr43-root-reviewed-final-plan/v1','plan_status':'PENDING_ROOT_FULL_REVIEW_AND_ACTUAL_RECONCILIATION','pr':43,'problem_id':30004386,'original_head':'86be0f85c7a37a5cad8d24abd16a32d8d1f27e62','original_base':'60292bed09f59236aa192cb17aa138f7b4750e1a','reviewed_candidate_manifest_sha256':'4849e6037a5db3dce546a656dcd57063ae83d782c19e24d4e3dff97ebbcdec14','current_dependencies_sha256':'4cec33dfaee001419ccf07dc2483d3c8bdf67f0308e5601cbefb4e620c45337e','whole_manifest_sha256':None,'preparation_manifest_sha256':None,'root_bindings':None,'root_bindings_sha256':None,'root_full_current_read_completed':False,'root_full_whole_read_completed':False,'root_acceptance_source_review_completed':False,'independent_whole_current_pass':False,'root_actual_PR42_predecessor_read_completed':False,'mandatory_corrections':[],'science_reexecution_of_current':False,'historical_PASS_transferred':False,'immutable_evidence_references':[],'scientific_scope':scope,**science,'partial_valid':None})
for name,p in [('EXPECTED_CURRENT_ADMIN.json',A/'reviewed_candidate/status.json'),('EXPECTED_WHOLE_VERDICT.json',A/'whole_current_source_first_family/VERDICT.json'),('EXPECTED_ROOT_WHOLE_REVIEW.json',A/'ROOT_WHOLE_CURRENT_REVIEW.json')]:
    dump(name,json.loads(p.read_bytes()))
input_names=['snapshot_manifest.json','ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md','ROOT_PRIMARY_READ_LEDGER.json','ROOT_SCIENCE_CARD.json','ROOT_CURRENT_INPUT_PREIMAGES.json','ROOT_CURRENT_PREREQUISITES_INSPECTION.json','ROOT_ACTUAL_CURRENT_PACKET_INSPECTION.json','capture_root_final_operation.py','ROOT_SOURCE_MATCH_AND_PROOF_NOTES.md','root_original_actual_reproduction/MANIFEST.json','current_preparation_family/PREPARATION_MANIFEST.json','current_source_adversary_family/SELF_MANIFEST.json']
inputs={'schema':'pr43-acceptance-source-input-bindings/v1','source_only':True,'pins':{n:pin(A/n) for n in input_names},'current_manifest_sha256':'4849e6037a5db3dce546a656dcd57063ae83d782c19e24d4e3dff97ebbcdec14','current_members':347,'current_dependencies_sha256':'4cec33dfaee001419ccf07dc2483d3c8bdf67f0308e5601cbefb4e620c45337e','current_dependency_members':274,'closed_whole_manifest':pin(A/'whole_current_source_first_family/SELF_MANIFEST.json'),'closed_whole_result':pin(A/'whole_current_source_first_family/VERDICT.json'),'closed_whole_report':pin(A/'whole_current_source_first_family/FINAL_REPORT.md'),'closed_root_whole_inspection':pin(A/'ROOT_WHOLE_CURRENT_REVIEW.json'),'root_capture_operator':pin(A/'capture_root_final_operation.py'),'required_future_PR42_predecessor':{'previous_mirror':None,'previous_post':None,'previous_root_post':None},'closed_PR42_V2_source_context':pin(PREV/'PREPARATION_MANIFEST.json'),'PR42_source_PASS_transferred':False}
require(inputs['root_capture_operator']['sha256']=='0da8951ebcbbe8e410e2390d838a76e95da9a1d9df7dd7f61ba39f93a86a5ecf','Actual ROOT43 operator')
dump('INPUT_BINDINGS.json',inputs)
g=identity(sources['pr42_guards.py'])
g=g.replace("ID, CODE, PR = '30004386', 'OWR-17469-011', 42","ID, CODE, PR = '30004386', 'OWR-17469-011', 43")
for old,new in [('09ac3a27edc2113da9574e57a13e7a0c99baa194fa50efb07548ec47fa7493de','4849e6037a5db3dce546a656dcd57063ae83d782c19e24d4e3dff97ebbcdec14'),('7570cec29df5d916107f566e3fd15c48228c6ea3f6b420fc40e05b48898799c6','4cec33dfaee001419ccf07dc2483d3c8bdf67f0308e5601cbefb4e620c45337e'),('9441de78ed662c85c03125baf6d85de2388762488affb3a9769a88037d9e8974','a98970b4196fbc9f53d8b9ba431337b88d5807e73c7bfdda63a091ad166765b6'),('60d0413980ac5f251913a26298692c5efc797d8f5084ca03e8d134472ab820e4',sha(b'')),('0b116a4593d84d7e9d02f635a080eb0e2242aaba66acfc8efeae74462ad89898','90402aea80b79b7713d740863b6058b43c64050c3499701b2bf8490c90b210e3')]:g=g.replace(old,new)
g=re.sub(r'^SCIENCE = .*$', 'SCIENCE = '+repr(science),g,flags=re.M)
g=re.sub(r'^IMMUTABLE = .*$',"IMMUTABLE = {'SOURCE_STATUS.md','check_normalization.py','check_results.json','source_record.json','source_checksums.json','turns.jsonl','review/author_replay/check_normalization.py','review/author_replay/check_results.json','review/independent_checks.py','review/independent_results.json'}",g,flags=re.M)
g=g.replace("WHOLE_VERDICT = 'PASS_NEW_WHOLE_CURRENT_SOURCE_FIRST_ADVERSARY'","WHOLE_VERDICT = 'PASS_EXACT_FROZEN_CURRENT_PACKET_FOR_CREDITED_SOURCE_STATUS_ACCEPTANCE'")
g=g.replace("'PR43_STRICT_CURRENT_PACKET_v1':{'schema','self_excluded','files_count','files','current_gate','full_problem_solved'}","'PR43_STRICT_CURRENT_PACKET_v1':{'schema','self_excluded','files_count','files','current_gate','prior_source_status','full_problem_solved_by_project','novelty_claimed','original_substantive_attempts','new_substantive_attempts','audit_turns'}")
g=g.replace("{'number':42,'url':'https://github.com/AlecKriebel/Math/pull/42'","{'number':43,'url':'https://github.com/AlecKriebel/Math/pull/43'")
g=replace_function(g,'original_native', '''def original_native(base):
    snapshot=load(A/'snapshot_manifest.json')
    require(snapshot['schema']=='pr43-root-readonly-original-snapshot/v1' and len(snapshot['files'])==16,'Complete original16 required')
    exact(base,{z['path'] for z in rows(snapshot['files'])})
    for z in rows(snapshot['files']):
        raw=regular(base,z['path']).read_bytes()
        require(raw==regular(A/'source_snapshot',z['path']).read_bytes() and len(raw)==z['bytes'] and sha(raw)==z['sha256'],'Original16 bytes differ')''')
g=replace_function(g,'source', '''def source(base):
    original_native(base/'original_archive')
    for n in IMMUTABLE:
        require(regular(base,n).read_bytes()==regular(A/'source_snapshot',n).read_bytes(),'Immutable math/code/saved result/source/empty ledger changed')
    require(sha(regular(base,'SOURCE_STATUS.md').read_bytes())==SCIENCE_SHA and sha(regular(base,'source_record.json').read_bytes())==SOURCE_SHA,'Scientific/source anchors changed')
    raw=regular(base,'turns.jsonl').read_bytes();require(raw==b'' and sha(raw)==LEDGER_SHA,'Literal original zero-byte ledger required, no fictitious attempt')
    prior=regular(base,'root_evidence/pinned_prior_report.json').read_bytes()
    require(prior==regular(A,'pinned_prior_report.json').read_bytes() and equal(parse(prior),{}),'Absent raw OWR-17469-011 key and SQL fallback{} must not become PRESENT/null')
    require(sha(regular(base,'SOURCE_PRECISION_QUALIFICATIONS.md').read_bytes())=='868b8e2af799f8371c3900529079af354ef51cf01ee08adeccc666ec0884d3cd','Exact global source qualifications required')''')
g=replace_function(g,'root_binding_input', '''def root_binding_input(name,pin_value):
    p=regular(R,name)
    require(p.resolve().is_relative_to(A.resolve()) and not p.resolve().is_relative_to(C.resolve()) and not p.resolve().is_relative_to(HERE.resolve()),'Genuine external ROOT bindings outside closed packets required')
    require(sha(p.read_bytes())==digest(pin_value),'Actual ROOT immutable-bindings SHA differs')
    o=parse(p.read_bytes())
    for key in ['whole_manifest','root_whole_inspection','root_capture_operator','previous_mirror','previous_post','previous_root_post']:exact_reference(o[key])
    expected=load(HERE/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json')
    expected.update(status='ROOT_APPROVED_CLOSED_WHOLE_AND_ACTUAL_PR42_EVIDENCE',created_utc=o['created_utc'],root_full_current_read_completed=True,root_full_whole_read_completed=True,root_acceptance_source_review_completed=True,independent_whole_current_pass=True,root_actual_PR42_predecessor_read_completed=True)
    for key in ['whole_manifest','root_whole_inspection','root_capture_operator','previous_mirror','previous_post','previous_root_post']:expected[key]=o[key]
    require(equal(o,expected),'Complete typed external ROOT bindings equality required')
    require(utc_clock(o['created_utc'],'ROOT binding creation')<=dt.datetime.now(dt.timezone.utc),'ROOT binding may not be future dated')
    previous_root=B/'audits/pr42_2233'
    for key,file in [('previous_mirror','state_mirror_bindings.json'),('previous_post','post_acceptance_verification.json'),('previous_root_post','ROOT_ACTUAL_POST_INSPECTION.json')]:
        require(o[key]['path']==(previous_root/file).relative_to(R).as_posix(),'Literal genuine completed PR42 predecessor required')
        check(R,[o[key]])
    return o,p''')
g=replace_function(g,'basis', '''def basis(root_bindings,root_bindings_sha256):
    approved,rp=root_binding_input(root_bindings,root_bindings_sha256)
    inputs=load(HERE/'INPUT_BINDINGS.json');refs=[]
    for n in sorted(inputs['pins']):
        ref=exact_reference(inputs['pins'][n]);check(R,[ref]);refs.append(ref)
    frozen=manifest(C,'MANIFEST.json',CURRENT_SHA,347,frozen=True)
    deps=load(C/'CURRENT_DEPENDENCIES.json')
    keyset(deps,{'anchor_repository_relative','resolution','files','foreign_primary_and_derivative_members_individually_hash_bound_not_copied','current_native13','current_main_head'},'Exact portable dependency schema')
    required(deps,{'anchor_repository_relative':A.relative_to(R).as_posix(),'resolution':'repository_root / anchor_repository_relative / files.path; never scratch','foreign_primary_and_derivative_members_individually_hash_bound_not_copied':True,'current_main_head':'c61dc0cb572de281b871264819c8b80d647d0373'},'Exact dated dependencies')
    require(sha((C/'CURRENT_DEPENDENCIES.json').read_bytes())==DEPS_SHA and len(rows(deps['files']))==274,'Complete274 dependencies');check(A,deps['files']);source(C)
    for n in ADMIN:require(equal(load(C/n),load(HERE/'EXPECTED_CURRENT_ADMIN.json')),'Complete dated pending admin differs')
    w=A/'whole_current_source_first_family';wm=exact_reference(approved['whole_manifest'])
    require(equal(wm,inputs['closed_whole_manifest']) and wm['path']==(w/'SELF_MANIFEST.json').relative_to(R).as_posix(),'Exact actual whole closure required')
    whole=parse(bound(wm));keyset(whole,{'schema','created_utc','actual_closure_pid','files_count','files','self_excluded','mode','directories','candidate_manifest_sha256','external_individually_excluded_inputs','external_copied_members','authorship_scope','review_completion_percent','new_discovery_percent','ROOT_future_approval_certified'},'Complete known whole closure')
    required(whole,{'schema':'PR43_NEW_WHOLE_CURRENT_SOURCE_FIRST_SELF_ONLY_CLOSURE_v1','files_count':30,'self_excluded':['SELF_MANIFEST.json'],'mode':'0444','candidate_manifest_sha256':CURRENT_SHA,'external_copied_members':[],'ROOT_future_approval_certified':False},'Actually closed new whole family')
    authored=rows(whole['files']);require(len(authored)==30,'Exact30 owned whole members')
    for z in whole['files']:keyset(z,{'path','bytes','sha256','mode','classification','novelty_claim'},'Complete whole owned reference');require(z['mode']=='0444' and z['novelty_claim'] is False,'Declared whole ownership/mode')
    check(w,authored);exact(w,{z['path'] for z in authored}|{'SELF_MANIFEST.json'});frozen_files(w,authored,'SELF_MANIFEST.json')
    dated_head='c61dc0cb572de281b871264819c8b80d647d0373';historical={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
    dated=load(A/'ROOT_CURRENT_INPUT_PREIMAGES.json');required(dated,{'schema':'PR43_ROOT_FRESH13_INPUT_PREIMAGES_v1','current_head':dated_head},'Genuine dated freeze13 authority, not current state')
    dated_native={z['path']:z for z in rows(dated['files'])};require(set(dated_native)==NATIVE and len(dated_native)==13,'Exact dated13')
    foreign=whole['external_individually_excluded_inputs'];require(type(foreign) is list and len(foreign)==756,'Exact756 individual excluded references')
    literal_names=set();canonical_names=set();historical_checked=set()
    for z in foreign:
        keyset(z,{'path','bytes','sha256','role','individual_exclusion'},'Exact foreign reference')
        require(z['path'] not in literal_names,'Duplicate literal foreign identity');literal_names.add(z['path'])
        canonical=resolve_foreign_literal(z['path']);n=canonical.relative_to(R).as_posix();canonical_names.add(n)
        if n in historical:
            captured=dated_native[n];require(type(z['bytes']) is int and z['bytes']==captured['bytes'] and z['sha256']==captured['sha256'],'Historical row must equal actual freeze13 pin')
            entries=git_bytes('ls-tree','-z',dated_head,'--',n).decode().split('\\0');require(len(entries)==2 and entries[-1]=='','One immutable historical Git blob')
            fields,literal=entries[0].split('\\t');mode,kind,blob=fields.split();require(mode=='100644' and kind=='blob' and literal==n,'Exact historical Git path/mode')
            raw=git_bytes('show',dated_head+':'+n);historical_checked.add(n)
        else:raw=canonical.read_bytes()
        require(type(z['bytes']) is int and len(raw)==z['bytes'] and sha(raw)==digest(z['sha256']),'Entire individual foreign input changed')
    require(len(literal_names)==756 and NATIVE<=canonical_names and historical_checked==historical,'Exact756 identities, native13 and historical4')
    verdict=parse(bound(inputs['closed_whole_result']));require(equal(verdict,load(HERE/'EXPECTED_WHOLE_VERDICT.json')),'Entire exact typed new independent VERDICT')
    required(verdict,{'verdict':WHOLE_VERDICT,'candidate_manifest_sha256':CURRENT_SHA,'mandatory_defects':[],'source_or_packet_repair_required':False,'mathematical_gap':None,'justified_status':'already_solved','full_target_resolved_in_prior_published_literature':True,'prior_publication_doi':'10.4064/sm210413-16-9','full_problem_solved_by_project':False,'original_substantive_attempts':0,'new_substantive_attempts':0,'audit_turns':0},'Scientific/source-status independent gate')
    bound(inputs['closed_whole_report'])
    rootref=exact_reference(approved['root_whole_inspection']);require(equal(rootref,inputs['closed_root_whole_inspection']),'Exact ROOT whole read pin')
    root=parse(bound(rootref));require(equal(root,load(HERE/'EXPECTED_ROOT_WHOLE_REVIEW.json')) and equal(root['complete_VERDICT_object'],verdict),'Entire genuine ROOT whole inspection and complete VERDICT')
    required(root,{'schema':'pr43-root-complete-closed-whole-inspection/v1','status':'PASS_ROOT_COMPLETE_CLOSED_WHOLE_INSPECTION','personal_report_and_verdict_fully_read':True,'all_first_party_whole_bytes_and_modes_checked':True,'all_foreign_individual_whole_bytes_checked':True,'exact_self_only_recursive_closure_checked':True,'future_execution_approved':False,'mandatory_defects':[],'mandatory_corrections':[]},'Genuine own ROOT full reading')
    require(utc_clock(root['created_utc'],'ROOT whole read')<=dt.datetime.now(dt.timezone.utc),'No future ROOT read')
    ledger=load(A/'ROOT_PRIMARY_READ_LEDGER.json');card=load(A/'ROOT_SCIENCE_CARD.json')
    require(ledger['schema']=='PR43_ROOT_PRIMARY_READ_LEDGER_v1' and card['schema']=='PR43_ROOT_SCIENCE_CARD_v1' and ledger['reading_completed'] is True and card['reading_completed'] is True and len(ledger['root_flags'])==8 and equal(ledger['root_flags'],card['root_flags']) and all(v is True for v in ledger['root_flags'].values()),'Distinct actual scientific ledger/card schemas and eight true flags')
    operator=exact_reference(approved['root_capture_operator']);require(equal(operator,inputs['root_capture_operator']),'ROOT43 reviewed operator differs');bound(operator)
    refs += [pin(C/'MANIFEST.json'),pin(C/'CURRENT_DEPENDENCIES.json'),wm,inputs['closed_whole_result'],inputs['closed_whole_report'],rootref,pin(rp)]
    refs += [approved[n] for n in ['previous_mirror','previous_post','previous_root_post']]
    require(len({z['path'] for z in refs})==len(refs),'No duplicate immutable evidence identity')
    return frozen,sorted(refs,key=lambda z:z['path'])''')
# Add genuine predecessor reading completion to the completed plan only.
g=g.replace("independent_whole_current_pass=True,immutable_evidence_references=refs)","independent_whole_current_pass=True,root_actual_PR42_predecessor_read_completed=True,immutable_evidence_references=refs)")
start=g.index("    previous_root=B/'audits/pr41_9700035'",g.index('def gates('));end=g.index("    fresh=load(ps['fresh_preimage'])",start)
g=g[:start]+'''    previous_root=B/'audits/pr42_2233'
    authority,_=root_binding_input(a.root_bindings,a.root_bindings_sha256)
    require(equal(pin(ps['previous_mirror']),authority['previous_mirror']) and equal(pin(ps['previous_post']),authority['previous_post']),'Exact genuine ROOT-approved PR42 predecessor bytes')
    previous=load(ps['previous_mirror']);require(len(previous['entries'])==32 and 42 in previous['required_completed_prs'] and 43 not in previous['required_completed_prs'],'Actual completed PR42 prior scope')
    required(load(ps['previous_post']),{'status':'PASS','pr':42,'targets':33,'consumed_substantive_turns':41,'primary_acceptances':32,'program_completed_count':32,'fresh_native_mirror_noop':True},'Completed actual PR42 predecessor post')
    rootpost=load(R/authority['previous_root_post']['path'])
    required(rootpost,{'schema':'pr42-root-complete-actual-post-inspection/v1','status':'PASS','completed_primary_prs':32,'all32_prior_states_and_full_history_prefix_preserved':True,'current13_match_exact_allowed_acceptance_changes':True,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False},'Genuine completed ROOT PR42 post read')
    require(equal(rootpost['entire_post'],load(ps['previous_post'])),'Entire genuine predecessor post object')
'''+g[end:]
g=g.replace("snapshot_manifest_v2.json","snapshot_manifest.json").replace("len(snap['files'])==17 and len(snap['changed_paths'])==18","len(snap['files'])==16 and len(snap['changed_paths'])==17").replace("len(raw)==122952","len(raw)==54344")
g=replace_function(g,'derive_inventory', '''def derive_inventory(before,remote,finalized_utc):
    require(type(before) is dict and type(before.get('items')) is list and len(before['items'])==180,'Complete retained180 inventory')
    require(all(type(z) is dict and type(z.get('number')) is int for z in before['items']),'Typed inventory identities')
    identities=[z['number'] for z in before['items']];require(len(set(identities))==180 and identities.count(43)==1,'Unique original selected PR43')
    require(type(before.get('completed_count')) is int and before['completed_count']==32 and sum(z.get('stage')=='complete' for z in before['items'])==32,'Actual32 prior primaries')
    required(remote,{'state':'MERGED','isDraft':False,'number':43,'headRefOid':HEAD,'headRefName':'dot/math-'+ID,'baseRefName':'main'},'Actual merged source-status remote')
    require(type(remote['mergeCommit']) is dict and set(remote['mergeCommit'])=={'oid'} and type(remote['mergeCommit']['oid']) is str and re.fullmatch('[0-9a-f]{40}',remote['mergeCommit']['oid']),'Exact actual merge oid')
    clock=utc_clock(finalized_utc,'Actual finalization');merged=utc_clock(remote['mergedAt'],'Actual mergedUTC');require(merged<=clock<=dt.datetime.now(dt.timezone.utc),'No reversed/future merge finalization')
    inv=copy.deepcopy(before);chosen=next(z for z in inv['items'] if z['number']==43);require(chosen.get('stage')!='complete','Selected not already complete')
    chosen.update(stage='complete',outcome='already_solved_accepted_partial',queue_status='already_solved',audited_head=HEAD,merge_commit=remote['mergeCommit']['oid'],merged_at=remote['mergedAt'],workflow_completion_estimate_percent=100,original_attempts='0/5',new_substantive_attempts=0,cumulative_attempts='0/5',paper_or_new_doi_or_tracker=False)
    require(sum(z.get('stage')=='complete' for z in inv['items'])==33,'Exactly33 derived primary completions')
    inv.update(updated_at_utc=finalized_utc,last_checkpoint_utc=finalized_utc,completed_count=33,program_completion_estimate_percent=33/180*100,completion_estimate_percent=33/180*100,current_pr=44)
    return inv''')
g=replace_function(g,'expected_acceptance', '''def expected_acceptance(pins,pre):
    final,remote=finalization(pins,pre)
    return {'schema':'pr43-accepted-qualified-source-status-partial/v1','utc':final['utc'],**SCIENCE,**pins,'pr':43,'id':30004386,'problem_id':30004386,'problem_number':CODE,'queue_status':'already_solved','outcome':'already_solved_accepted_partial_merged','original_head':HEAD,'original_base':ORIGINAL_BASE,'merge_commit':final['merge_commit'],'merge_tree':final['merge_tree'],'merge_parents':[pre['main_before'],HEAD],'merged_at':remote['mergedAt'],'remote_state':'MERGED','remote_isDraft':False,'canonical_scientific_artifact_sha256':SCIENCE_SHA,'source_record_sha256':SOURCE_SHA,'original_ledger_sha256':LEDGER_SHA,'substantive_attempts_used':0,'substantive_attempt_limit':5,'native_historical_events_inferred':False,'historical_metadata_archival_only':True,'workflow_completion_estimate_percent':100,'full_resolution_by_project_completion_estimate_percent':0,'scientific_scope':load(HERE/'SCIENTIFIC_SCOPE.json')}''')
g=g.replace("status='unsolved_accepted_partial_merged'","status='already_solved_accepted_source_status_merged'")
g=g.replace("'original_substantive_attempts':2","'original_substantive_attempts':0").replace("'pr':42","'pr':43")
g=g.replace("{'number':42,'url':'https://github.com/AlecKriebel/Math/pull/42'","{'number':43,'url':'https://github.com/AlecKriebel/Math/pull/43'")
g=replace_function(g,'mirror_proposal', '''def mirror_proposal(proposal,pins):
    previous=load(R/pins['previous_mirror']);expected=copy.deepcopy(previous)
    expected.update(created_at_utc=proposal.get('created_at_utc'),scope='Incremental present accepted primary PR43 source-status correction; original0/5, no new proof turn or historical reconstruction.')
    for n in ['inventory','queue']:expected[n]=binding(R/previous[n]['path'])
    expected['required_completed_prs']=sorted(previous['required_completed_prs']+[43])
    expected['entries'].append({'pr':43,'id':ID,'status':'already_solved','acceptance':binding(K/'acceptance.json'),'audit_acceptance':binding(A/'acceptance.json'),'remote':binding(A/'remote_merge_receipt.json'),'accepted_source':binding(K/'source_record.json'),'canonical_acceptance_text':binding(K/'ACCEPTANCE.md'),'canonical_manifest':binding(K/'MANIFEST.json'),'artifact':{**binding(K/'SOURCE_STATUS.md'),'acceptance_hash_field':'canonical_scientific_artifact_sha256'},'budget':{'used':0,'limit':5,'kind':'pr43_exact_original_empty_ledger','ledger':binding(K/'turns.jsonl')},'duplicates':[]})
    require(equal(proposal,expected),'Entire typed exact old proposal plus one source-status primary')
    require(utc_clock(proposal['created_at_utc'],'Actual proposalUTC')<=dt.datetime.now(dt.timezone.utc),'No future proposal clock')''')
g=g.replace("['bool_turn','phantom_attempt','missing_turn','wrong_order','extra_field']","['nonempty','whitespace_only','invented_JSONL','bool_used','wrong_used','wrong_limit']")
g=g.replace("'prior_state_entries_preserved':32,'current_targets':33,'consumed_substantive_turns':41,'primary_acceptances':32","'prior_state_entries_preserved':33,'current_targets':34,'consumed_substantive_turns':41,'primary_acceptances':33").replace("'targets':33","'targets':34")
# Complete read-only reconstruction of the historical native plan, not merely a hash.
g+='''\n\ndef rebuild_saved_mirror_plan(proposal,timestamp,old_state,old_history):
    m=mirror_module(proposal)
    overrides={str((R/'unsolved_math_prioritization/state.json').resolve()):old_state,str((R/'unsolved_math_prioritization/history.jsonl').resolve()):old_history}
    class ArchivedReadPath(type(Path())):
        def read_bytes(self):
            key=str(self.resolve())
            return overrides[key] if key in overrides else Path.read_bytes(self)
    actual_path=m.Path;m.Path=ArchivedReadPath
    try:return m.build_plan(R,proposal,timestamp)
    finally:m.Path=actual_path
'''
needle="    expected={'schema':'pr43-present-acceptance-mirror/v1'"
where=g.index(needle,g.index('def mirror_records('))
g=g[:where]+"    require(equal(plan,rebuild_saved_mirror_plan(proposal,plan['created_at_utc'],before_state,before_history)),'Entire native plan must derive exactly from actual old bodies and same timestamp')\n"+g[where:]
g=replace_function(g,'ledger_list', '''def ledger_list(raw):
    require(type(raw) is bytes and (not raw or raw.endswith(b'\\n')),'Exact complete JSONL bytes')
    return [parse(line) for line in raw.splitlines()]''')
put('pr43_guards.py',g)
body='Accept PR43 / 30004386 / OWR-17469-011 as an already_solved source-status partial. Johnston, Kabluchko and Prochno resolved the exact full weak-P(R) random-conditional-law LDP at speedN and the entire Prohorov limit set for Uniform[-1,1] coordinates and fixed projection dimension1; credit and DOI10.4064/sm210413-16-9 remain theirs. This project claims no discovery, novelty or exhaustive priority. The unchanged SOURCE_STATUS and original16 files, original empty research ledger0/5, full957-line17-path diff, exact historical527/current527/664 diagnostics, whole raw/allSQL provenance and global printed-proof/source/history qualifications are retained. Finite checks are not LDP proof. Raw OWR-17469-011 prior key is absent; saved{} is SQL fallback, not retrieved prior/null. The NEW whole-current source-first review passed; genuine ROOT full reading and actual final reconciliation are bound. Current model/reasoning/deadline remain null, original0/5,new0,audit0. No new paper, DOI, tracker, release or human peer-review claim. One present acceptance event follows the exact original-head merge and preserves all prior native states and the full history prefix.\n'
present='The NEW whole-current source-first gate has passed for this already_solved source-status partial, as bound in acceptance.json. The literal mathematical target was fully resolved by Johnston, Kabluchko and Prochno; prior DOI10.4064/sm210413-16-9. No project full-resolution or discovery is claimed. Original16 and immutable mathematics/code/results/source and the zero-byte research ledger are unchanged. SOURCE_PRECISION_QUALIFICATIONS.md is operative globally. All PENDING/source-only descriptions and archived oldPASS/runtime/access claims in CURRENT_CONTEXT.md, CURRENT_SOURCE_STATUS.md, SOURCE_PRECISION_QUALIFICATIONS.md, README.md, SOURCE_AUDIT.md, review/REVIEW.md, pr_body.md, archived administration, original_archive, build, family_evidence, root_evidence and root_approval are dated records at or before frozen current publication2026-10-03T00:27:15.171673+00:00. Later accepted records alone give the present disposition. Neither oldPASS nor original runtime/model/access/human referee claims certify this new gate. Raw prior absence differs from SQLfallback{}. Original0/5,new0,audit0, current runtime fields null; no new paper/DOI/tracker. See acceptance.json and ACCEPTANCE.md for actual merged disposition.\n'
i=identity(sources['integrate_reviewed_partial.py'])
i=re.sub(r'^BODY = .*$', 'BODY = '+repr(body),i,flags=re.M);i=re.sub(r'^PRESENT_SCOPE = .*$', 'PRESENT_SCOPE = '+repr(present),i,flags=re.M)
i=i.replace("cells[8]=' unsolved '; cells[9]=' 2/5 ';","cells[8]=' already_solved ';").replace("set(changed)<={8,9,11}","set(changed)<={8,11} and cells[9]==row.split('|')[9]").replace("Only named Status/Turns/Findings","Only named Status/Findings")
i=i.replace("['Status','Turns','Findings']","['Status','Findings']")
i=i.replace("len(state)==32","len(state)==33").replace("==39","==41").replace("inv['completed_count']==31","inv['completed_count']==32").replace("=='complete' for z in inv['items'])==31","=='complete' for z in inv['items'])==32").replace("z['number']==42","z['number']==43")
i=i.replace("'original_substantive_attempts':2","'original_substantive_attempts':0").replace("'pr':42","'pr':43")
i=i.replace("status='unsolved_accepted_partial_integration_pending_remote_verification'","status='already_solved_accepted_source_status_integration_pending_remote_verification'").replace("status='unsolved_accepted_partial_merged'","status='already_solved_accepted_source_status_merged'")
i=i.replace("# Accepted UNSOLVED qualified partial", "# Accepted already_solved source-status partial").replace("original2/5 ledger","original0/5 empty ledger").replace("Original2/5,new0,audit0", "Original0/5,new0,audit0").replace("Program32/180=17.7778%", "Program33/180=18.3333%")
put('integrate_reviewed_partial.py',i)
s=identity(sources['seal_final_evidence.py']).replace("'pr':42,'problem_id':30004386","'pr':43,'problem_id':30004386")
put('seal_final_evidence.py',s)
m=identity(sources['state_mirror_reconciliation.py'])
m=m.replace("['Status','Turns','Findings']","['Status','Findings']").replace("{'current_pr':43,'completed_count':32}","{'current_pr':44,'completed_count':33}").replace("inv['completed_count']==32","inv['completed_count']==33").replace("=='complete' for z in inv['items'])==32","=='complete' for z in inv['items'])==33").replace("z['number']==42","z['number']==43").replace("'outcome':'unsolved_accepted_partial','queue_status':'unsolved'","'outcome':'already_solved_accepted_partial','queue_status':'already_solved'").replace("'original_attempts':'2/5','cumulative_attempts':'2/5'","'original_attempts':'0/5','cumulative_attempts':'0/5'")
m=m.replace("len(prior)==32","len(prior)==33").replace("==39","==41").replace("'pr':42","'pr':43").replace("'status':'unsolved'","'status':'already_solved'").replace("+[42]","+[43]").replace("K/'PARTIAL.md'","K/'SOURCE_STATUS.md'")
m=m.replace("original2/5, no new proof turn or historical native reconstruction.","source-status correction; original0/5, no new proof turn or historical reconstruction.").replace("'used':2,'limit':5,'kind':'pr43_exact_original_two_turn_list'","'used':0,'limit':5,'kind':'pr43_exact_original_empty_ledger'")
start=m.index("    m=g.mirror_module(proposal);original=");end=m.index("    plan=m.build_plan",start)
m=m[:start]+'''    m=g.mirror_module(proposal);negatives=[]
    for label,raw,used,limit in [('nonempty',b'x',0,5),('whitespace_only',b'\\n',0,5),('invented_JSONL',b'{"turn":1}\\n',0,5),('bool_used',b'',False,5),('wrong_used',b'',1,5),('wrong_limit',b'',0,4)]:
        try:m.ledger_budget(raw,'pr43_exact_original_empty_ledger',used,limit)
        except m.Rejected:negatives.append(label)
        else:raise ValueError('Exact empty-ledger guard accepted mutant '+label)
'''+m[end:]
m=m.replace("plan['primary_count']==32","plan['primary_count']==33").replace("len(plan['state_after'])==33","len(plan['state_after'])==34").replace("'turns_used':2","'turns_used':0").replace("'prior_state_entries_preserved':32,'current_targets':33","'prior_state_entries_preserved':33,'current_targets':34").replace("'primary_acceptances':32","'primary_acceptances':33").replace("'targets':33","'targets':34")
put('state_mirror_reconciliation.py',m)
v=identity(sources['verify_post_acceptance.py'])
v=v.replace("'pr':42","'pr':43").replace("'status':'unsolved'","'status':'already_solved'").replace("'turns_used':2","'turns_used':0").replace("'prior_state_entries_preserved':32,'current_targets':33","'prior_state_entries_preserved':33,'current_targets':34").replace("'primary_acceptances':32","'primary_acceptances':33").replace("'targets':33","'targets':34").replace("len(current)==33","len(current)==34").replace("'program_completed_count':32","'program_completed_count':33").replace("'exact_original17_and_PARTIAL_unchanged'","'exact_original16_and_SOURCE_STATUS_unchanged'").replace("'whole_current385_and517dependencies_bound'","'whole_current347_and274dependencies_bound'").replace("'entire_history_prefix_and32prior_states_preserved'","'entire_history_prefix_and33prior_states_preserved'")
v=v.replace("'full_problem_solved':False,'novelty_claimed':False","'full_target_resolved_in_prior_published_literature':True,'prior_publication_doi':'10.4064/sm210413-16-9','full_problem_solved_by_project':False,'full_problem_solved':False,'novelty_claimed':False")
put('verify_post_acceptance.py',v)
dump('SOURCE_STATUS.json',{'schema':'pr43-source-only-acceptance-status/v1','source_preparation_complete':None,'proposed_helpers_imported_compiled_executed':False,'ROOT_source_approval_authored':False,'future_final_reconciliation_executed':False,'future_acceptance_performed':False,'native_Git_remote_people_mutation':False,'full_target_resolved_in_prior_published_literature':True,'full_problem_solved_by_project':False,'novelty_claimed':False,'original_substantive_attempts':0,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'current_whole_verdict':None,'future_acceptance_verdict':None,'paper_or_new_DOI_or_tracker':False,'PR42_future_predecessor_certified':False,'independent_acceptance_source_verdict':None})
dump('AUTHORING_RESULT.json',{'schema':'pr43-source-only-authorship/v1','created_utc':stamp(),'actual_child_pid':os.getpid(),'basis_PR42_closed_source':pin(PREV/'PREPARATION_MANIFEST.json'),'PR42_SOURCE_PASS_transferred':False,'original_substantive_attempts':0,'new_substantive_attempts':0,'audit_turns':0,'production_sources_imported_compiled_executed':False,'prepared_members':[pin(H/n) for n in ['pr43_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py']]})
print(json.dumps({'status':'SOURCE_ONLY_AUTHORED','actual_child_pid':os.getpid(),'production_sources_imported_compiled_executed':False,'future_PR42_refs':None}))
