"""Own source authoring only: read repaired PR43 source as text, author PR44 source and false/null drafts."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import re
import os

H=Path(__file__).resolve().parent
A=H.parent
R=H.parents[3]
T=R/'draft_pr_publication_program_20260930/audits/pr43_30004386/acceptance_preparation_family_v2'
A43=T.parent
C=A/'reviewed_candidate'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def pin(p):
    b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}
def put(n,v):
    p=H/n
    b=v.encode() if isinstance(v,str) else (json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
    with p.open('xb') as f:f.write(b)
def replace_function(s,n,new):
    start=s.index('def '+n+'(')
    end=s.find('\n\ndef ',start+1)
    return s[:start]+new.strip()+'\n'+(s[end:] if end>=0 else '')
def transform(s):
    replacements={
      'pr42_2233':'__PREDECESSOR__','pr43':'pr44','PR43':'PR44','PR42':'PR43',
      '30004386':'2912','OWR-17469-011':'KP-4.36',
      '86be0f85c7a37a5cad8d24abd16a32d8d1f27e62':'c772dc5b851ec91da9d46d534577609e5d3ca389',
      '60292bed09f59236aa192cb17aa138f7b4750e1a':'01358d66fc67d1c462bddf31c0d4ee5b120e6737',
      '4849e6037a5db3dce546a656dcd57063ae83d782c19e24d4e3dff97ebbcdec14':'169f2825a8f730735627bdc33a43366c05e317fdf7ec4df4cd96a31e37329eb0',
      '4cec33dfaee001419ccf07dc2483d3c8bdf67f0308e5601cbefb4e620c45337e':'2c8d2ef1cd1846a0b82dce49b8c8891f6821ca129bd42ec20cf4fc45ae258c18',
      'a98970b4196fbc9f53d8b9ba431337b88d5807e73c7bfdda63a091ad166765b6':'44162e54c0f08a328332fc98980ff7e3fa50c96b9dade7583a53c480baf5eb30',
      '90402aea80b79b7713d740863b6058b43c64050c3499701b2bf8490c90b210e3':'69a3ffb7b6c2ba3bf1a4df8d7d83960d66095db9d175d78cfe49e2324aac1a71',
      'SOURCE_STATUS.md':'OBSTRUCTION.md','already_solved':'unsolved','source-status':'standard-partial','source_status':'standard_partial',
      'snapshot_manifest.json':'snapshot_manifest_v2.json','original16':'original18','Original16':'Original18',
      'current347':'current430','274dependencies':'369dependencies','347':'430','274':'369',
      'original0/5':'original2/5','Original0/5':'Original2/5','original0':'original2',
    }
    # One lexical replacement pass keeps PR43 and its actual PR43 predecessor distinct.
    pattern=re.compile('|'.join(re.escape(k) for k in sorted(replacements,key=len,reverse=True)))
    s=pattern.sub(lambda m:replacements[m.group()],s).replace('__PREDECESSOR__','pr43_30004386')
    nums={'32':'33','33':'34','34':'35','41':'43','43':'44','44':'45','16':'18','17':'19'}
    s=re.sub(r'(?<![\w])(?:32|33|34|41|43|44|16|17)(?![\w])',lambda m:nums[m.group()],s)
    # Numbers in identifier/string words require explicit source-family count updates.
    for old,new in [('33prior','34prior'),('33_prior','34_prior'),('32-primary','33-primary'),('32typed','33typed'),('33targets','34targets'),('34targets','35targets'),('33primary','34primary'),('32prior','33prior')]:
        # These are adjusted below in the authored whole/post functions, not globally.
        pass
    return s

GAPS=['No required map/homology comparison from unmarked full2type, particularly no meridian-compatible degree-one pair map established.','No pair of actual smooth/locallyflatPL S2-in-S4 exteriors with equal full(G,pi2module,k) and verified differing homotopy types.']
SCIENCE={'full_problem_solved':False,'full_target_resolved_in_prior_published_literature':False,'full_problem_solved_by_project':False,'prior_publication_doi':None,'partial_valid':True,'novelty_claimed':False,'priority_claimed':False,'original_substantive_attempts':2,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'verification_attempts_added':0,'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'paper_or_new_doi_or_tracker':False,'human_referee_review_claimed':False}
SCOPE={**SCIENCE,'schema':'pr44-proposed-accepted-scientific-scope/v1','id':'2912','problem_number':'KP-4.36','literal_target_status':'unsolved','literal_target':'Homotopy type of actual smooth or locally flat PL S2 complements in S4 from their unmarked full (G,pi2 with action,k) triple, up to compatible group/module isomorphisms carrying k.','strongest_verified_partial':'Standard finite-support meridional restriction-kernel formula; sufficient relative-degree-one pair-map criterion; conditional nonzero integral R^C/R^A for the specified abstract group-pair (G,<t>).','exact_remaining_gaps':GAPS,'full_triple_contains_peripheral_or_boundary_data':False,'specified_group_pair_geometrically_realized_and_compared':False,'finite_controls_prove_geometric_realization_or_classification':False,'historical_metadata_archival_only':True,'original18_and_immutable_science_helpers_results_source_ledger_unchanged':True,'global_qualification_path':'SOURCE_PRECISION_QUALIFICATIONS.md','global_qualification_sha256':sha((C/'SOURCE_PRECISION_QUALIFICATIONS.md').read_bytes()),'primary_limits':'Operative target/proof excerpts only; Hillman locally flat category is not silently smooth/PL; Jabłonowski inspected examples differ in full k; Conway-Kasprowski extra boundary hypotheses retained; 1983 construction full proof not read. No exhaustive priority or universal present literature absence.','AI_tools_used_extensively':True,'human_peer_review':False,'formal_certification':False}

ROOT_BINDING_FUNCTION=r'''
def root_binding_input(name,pin_value):
    p=regular(R,name)
    require(p.parent==A and p.name!='DRAFT_ROOT_IMMUTABLE_BINDINGS.json','Genuine adjacent ROOT completed bindings required')
    require(sha(p.read_bytes())==digest(pin_value),'Actual ROOT immutable-bindings SHA differs')
    o=parse(p.read_bytes());draft=load(HERE/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json')
    reference_keys=['whole_manifest','root_whole_inspection','root_capture_operator','previous_mirror','previous_post','previous_root_post','acceptance_source_manifest','acceptance_source_verdict','root_source_inspection']
    for key in reference_keys:exact_reference(o[key]);check(R,[o[key]])
    draft.update(status='ROOT_APPROVED_CLOSED_WHOLE_SOURCE_AND_ACTUAL_PR43_EVIDENCE',created_utc=o['created_utc'],root_full_current_read_completed=True,root_full_whole_read_completed=True,root_acceptance_source_review_completed=True,independent_whole_current_pass=True,root_actual_PR43_predecessor_read_completed=True)
    for key in reference_keys:draft[key]=o[key]
    require(equal(o,draft),'Complete exact typed ROOT binding keys and values required')
    require(utc_clock(o['created_utc'],'ROOT binding creation')<=dt.datetime.now(dt.timezone.utc),'No future ROOT approval')
    inputs=load(HERE/'INPUT_BINDINGS.json')
    for key in ['previous_mirror','previous_post','previous_root_post']:
        require(equal(o[key],inputs[key]),'Actual43 predecessor entire immutable binding differs')
    previous=load(R/o['previous_mirror']['path']);post=load(R/o['previous_post']['path']);rootpost=load(R/o['previous_root_post']['path'])
    require(type(previous['entries']) is list and len(previous['entries'])==33 and all(type(z['pr']) is int for z in previous['entries']),'Exact33 original primary entries')
    numbers=[z['pr'] for z in previous['entries']]
    require(len(set(numbers))==33 and 43 in numbers and 44 not in numbers and equal(sorted(numbers),previous['required_completed_prs']),'Actual43 prior identities')
    required(post,{'status':'PASS','pr':43,'targets':34,'consumed_substantive_turns':41,'primary_acceptances':33,'program_completed_count':33,'merge_commit':'c60255489a342fae02c0acf3d1026255b47be3d1','merge_tree':'fdc2bb213905051a430d24e13afb20e54fa9106a','fresh_native_mirror_noop':True,'one_present_primary_event':True,'new_duplicate_native_acceptance_added':False,'new_proof_turns':0,'full_problem_solved':False,'paper_or_new_doi_or_tracker':False},'Actual43 completed predecessor')
    required(rootpost,{'schema':'pr43-root-complete-actual-post-inspection/v1','status':'PASS','completed_primary_prs':33,'all33_prior_states_and_full_history_prefix_preserved':True,'current13_match_exact_allowed_acceptance_changes':True,'canonical357_plus_manifest_fullbytes_modes':True,'merge355_overlay_plus_queue_Git_bodies_and_parents':True,'entire_current_inventory_reconstructed':True,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False},'Actual43 ROOT entire-post reading')
    require(equal(rootpost['entire_post'],post),'Entire actual43 predecessor post equals completed ROOT read')
    require(utc_clock(rootpost['utc'],'Actual43 ROOT post')<=utc_clock(o['created_utc'],'ROOT44 approval'),'ROOT44 approval cannot precede predecessor actual post')
    expected_operator=regular(HERE,'capture_root_final_operation.py').read_bytes()
    require(o['root_capture_operator']['path']==(A/'capture_root_final_operation.py').relative_to(R).as_posix() and bound(o['root_capture_operator'])==expected_operator,'Literal personally reviewed ROOT operator must equal prepared complete source')
    sm=regular(R,o['acceptance_source_manifest']['path']);sv=regular(R,o['acceptance_source_verdict']['path']);sr=regular(R,o['root_source_inspection']['path'])
    require(sm.parent==sv.parent and sm.parent.parent==A and sm.parent not in {C,HERE} and sm.name=='SELF_MANIFEST.json' and sv.name=='VERDICT.json','New distinct source-adversary literal closure and verdict required')
    require(sr.parent==A and sr.name=='ROOT_SOURCE_ACCEPTANCE_REVIEW.json','Literal genuine ROOT source inspection required')
    own=load(sm);rr=rows(own['files']);require(own['self_excluded']==['SELF_MANIFEST.json'] and type(own['files_count']) is int and own['files_count']==len(rr),'Exact source-adversary self-only closure')
    check(sm.parent,rr);exact(sm.parent,{z['path'] for z in rr}|{'SELF_MANIFEST.json'});frozen_files(sm.parent,rr,'SELF_MANIFEST.json')
    verdict=load(sv)
    required(verdict,{'schema':'pr44-acceptance-source-adversary-verdict/v1','verdict':'PASS_SOURCE_ONLY_SCOPED','preparation_manifest_sha256':sha((HERE/'PREPARATION_MANIFEST.json').read_bytes()),'mandatory_corrections':[],'production_imported_compiled_executed':False,'future_acceptance_approved':False},'New actual independent source gate')
    root=load(sr)
    required(root,{'schema':'pr44-root-complete-acceptance-source-inspection/v1','status':'PASS_ROOT_COMPLETE_ACCEPTANCE_SOURCE_INSPECTION','all_prepared_source_and_controls_fully_read':True,'exact_preparation_closure_and_full_modes_checked':True,'all_individual_source_adversary_inputs_checked':True,'all_complete_actual_captures_checked':True,'complete_VERDICT_object':verdict,'preparation_manifest_sha256':sha((HERE/'PREPARATION_MANIFEST.json').read_bytes()),'acceptance_source_manifest':o['acceptance_source_manifest'],'acceptance_source_verdict':o['acceptance_source_verdict'],'mandatory_corrections':[],'future_execution_approved':False},'Genuine ROOT complete source/adversary reading')
    require(utc_clock(root['utc'],'ROOT source read')<=utc_clock(o['created_utc'],'Completed approval'),'Source read after approval prohibited')
    return o,p
'''

BASIS_FUNCTION=r'''
def basis(root_bindings,root_bindings_sha256):
    approved,rp=root_binding_input(root_bindings,root_bindings_sha256)
    inputs=load(HERE/'INPUT_BINDINGS.json');refs=[]
    for n in sorted(inputs['pins']):
        ref=exact_reference(inputs['pins'][n]);check(R,[ref]);refs.append(ref)
    frozen=manifest(C,'MANIFEST.json',CURRENT_SHA,430,frozen=True)
    deps=load(C/'CURRENT_DEPENDENCIES.json')
    keyset(deps,{'anchor_repository_relative','resolution','files','foreign_primary_and_derivative_members_individually_hash_bound_not_copied','current_native13','current_main_head'},'Exact portable dependency schema')
    required(deps,{'anchor_repository_relative':A.relative_to(R).as_posix(),'resolution':'repository_root / anchor_repository_relative / files.path; never scratch','foreign_primary_and_derivative_members_individually_hash_bound_not_copied':True,'current_main_head':'2b9d0234b1396fa84c4b34055b5e8e14c873588b'},'Exact dated dependencies')
    require(sha((C/'CURRENT_DEPENDENCIES.json').read_bytes())==DEPS_SHA and len(rows(deps['files']))==369,'Complete369 dependencies');check(A,deps['files']);source(C)
    for n in ADMIN:require(equal(load(C/n),load(HERE/'EXPECTED_CURRENT_ADMIN.json')),'Entire dated pending admin differs')
    w=A/'whole_current_source_first_family';wm=exact_reference(approved['whole_manifest'])
    require(equal(wm,inputs['closed_whole_manifest']),'Exact actual whole manifest')
    whole=parse(bound(wm));keyset(whole,{'schema','utc','operator_pid','files_count','files','directories','self_excluded','full_permission_mode','foreign_inputs_manifest','foreign_primary_or_raw_cache_bodies_copied','whole_native4_Git_stdout_is_procedural_actual_evidence','candidate_manifest_sha256','original_substantive_attempts','new_substantive_attempts','audit_turns','full_problem_solved','future_ROOT_acceptance_or_reconciliation_approved'},'Exact actual whole closure schema')
    required(whole,{'schema':'pr44-whole-current-source-first-self-only-closure/v1','files_count':96,'self_excluded':['SELF_MANIFEST.json'],'full_permission_mode':'0444','candidate_manifest_sha256':CURRENT_SHA,'foreign_primary_or_raw_cache_bodies_copied':False,'future_ROOT_acceptance_or_reconciliation_approved':False,'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False},'Actually closed whole family')
    authored=rows(whole['files']);require(len(authored)==96,'Exact96 whole members');check(w,authored);exact(w,{z['path'] for z in authored}|{'SELF_MANIFEST.json'});frozen_files(w,authored,'SELF_MANIFEST.json')
    require(equal(sorted(topology(w)[1]),whole['directories']),'Entire required whole directory topology')
    foreign_inventory=load(w/whole['foreign_inputs_manifest']);foreign=rows(foreign_inventory['files'])
    required(foreign_inventory,{'schema':'pr44-source-first-individual-foreign-inputs/v1','resolution':'repository_root / files.path','foreign_bodies_copied':False,'git_stdout_firstparty_native4_and_query_metadata_are_procedural_evidence':True},'Individual foreign scope')
    require(len(foreign)==964,'Exact964 individual foreign identities')
    dated_head='2b9d0234b1396fa84c4b34055b5e8e14c873588b';historical={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
    dated=load(A/'ROOT_CURRENT_INPUT_PREIMAGES.json');require(dated['current_head']==dated_head,'Dated freeze authority stays fixed');dated_native={z['path']:z for z in rows(dated['files'])};require(set(dated_native)==NATIVE,'Exact frozen native13')
    historical_checked=set();names=set()
    for z in foreign:
        keyset(z,{'path','bytes','sha256','excluded_from_family_authorship'},'Exact individual foreign reference');require(z['excluded_from_family_authorship'] is True,'Foreign exclusion true required');relative(z['path']);names.add(z['path'])
        if z['path'] in historical:
            require(z['bytes']==dated_native[z['path']]['bytes'] and z['sha256']==dated_native[z['path']]['sha256'],'Dated foreign row differs')
            entries=git_bytes('ls-tree','-z',dated_head,'--',z['path']).decode().split('\0');require(len(entries)==2 and entries[-1]=='','One historical Git blob');fields,literal=entries[0].split('\t');mode,kind,blob=fields.split();require(mode=='100644' and kind=='blob' and literal==z['path'],'Historical exact Git path/mode')
            raw=git_bytes('show',dated_head+':'+z['path']);historical_checked.add(z['path'])
        else:raw=regular(R,z['path']).read_bytes()
        require(len(raw)==z['bytes'] and sha(raw)==digest(z['sha256']),'Entire individual input changed')
    require(len(names)==964 and NATIVE<=names and historical_checked==historical,'Exact identities/native13/historical4')
    verdict=parse(bound(inputs['closed_whole_result']));require(equal(verdict,load(HERE/'EXPECTED_WHOLE_VERDICT.json')),'Entire actual typed whole verdict')
    required(verdict,{'verdict':WHOLE_VERDICT,'candidate_manifest_sha256':CURRENT_SHA,'mandatory_mathematical_corrections':[],'mandatory_source_scope_corrections':[],'mandatory_current_contract_corrections':[],'full_problem_solved':False,'novelty_claimed':False,'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'exact_remaining_gaps':load(HERE/'SCIENTIFIC_SCOPE.json')['exact_remaining_gaps']},'Scoped UNSOLVED mathematical gate')
    bound(inputs['closed_whole_report'])
    rootref=exact_reference(approved['root_whole_inspection']);require(equal(rootref,inputs['closed_root_whole_inspection']),'Genuine ROOT whole read pin')
    root=parse(bound(rootref));require(equal(root,load(HERE/'EXPECTED_ROOT_WHOLE_REVIEW.json')) and equal(root['complete_VERDICT_object'],verdict),'Entire exact ROOT44 whole read')
    required(root,{'schema':'pr44-root-complete-closed-whole-inspection/v1','status':'PASS_ROOT_COMPLETE_CLOSED_WHOLE_INSPECTION','candidate_manifest_sha256':CURRENT_SHA,'closed_whole_manifest_sha256':wm['sha256'],'first_party_members':96,'individually_bound_foreign_inputs':964,'personal_report_and_verdict_fully_read':True,'all_first_party_whole_bytes_and_modes_checked':True,'all_foreign_individual_whole_bytes_checked':True,'exact_self_only_recursive_closure_checked':True,'future_execution_approved':False,'mandatory_defects':[],'mandatory_corrections':[],'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved_by_project':False,'full_target_resolved_in_prior_published_literature':False,'dated_four_native_source_head':dated_head},'ROOT44 complete whole read flags and explicit source limits')
    ledger=load(A/'ROOT_PRIMARY_READ_LEDGER.json');card=load(A/'ROOT_SCIENCE_CARD.json');require(ledger['reading_completed'] is True and card['reading_completed'] is True and len(ledger['root_flags'])==9 and equal(ledger['root_flags'],card['root_flags']) and all(v is True for v in ledger['root_flags'].values()),'Nine distinct actual ROOT source/math flags')
    refs += [pin(C/'MANIFEST.json'),pin(C/'CURRENT_DEPENDENCIES.json'),wm,inputs['closed_whole_result'],inputs['closed_whole_report'],rootref,pin(rp)]
    refs += [approved[n] for n in ['previous_mirror','previous_post','previous_root_post','acceptance_source_manifest','acceptance_source_verdict','root_source_inspection','root_capture_operator']]
    out={}
    for z in refs:
        require(z['path'] not in out or equal(out[z['path']],z),'Conflicting immutable identity');out[z['path']]=z
    return frozen,sorted(out.values(),key=lambda z:z['path'])
'''

SOURCE_FUNCTION=r'''
def source(base):
    original_native(base/'original_archive')
    for n in IMMUTABLE:require(regular(base,n).read_bytes()==regular(A/'source_snapshot',n).read_bytes(),'Immutable science/helper/result/source/ledger changed')
    require(sha(regular(base,'OBSTRUCTION.md').read_bytes())==SCIENCE_SHA and sha(regular(base,'source_record.json').read_bytes())==SOURCE_SHA,'Science/source anchors changed')
    raw=regular(base,'turns.jsonl').read_bytes();require(raw==regular(A/'source_snapshot','turns.jsonl').read_bytes() and sha(raw)==LEDGER_SHA,'Exact original two-turn ledger required')
    entries=ledger_list(raw);require(len(entries)==2 and all(type(z.get('turn')) is int for z in entries) and [z['turn'] for z in entries]==[1,2] and all(z['outcome']=='stalled' for z in entries),'Original2/5 stalled routes only')
    require(sha(regular(base,'SOURCE_PRECISION_QUALIFICATIONS.md').read_bytes())==load(HERE/'SCIENTIFIC_SCOPE.json')['global_qualification_sha256'],'Global category/source/realization qualification exact')
'''

BODY='Accept PR44 / 2912 / Kirby4.36 as an UNSOLVED repository report of standard conditional deductions. The finite-support meridional restriction kernel, sufficient relative-degree-one pair-map criterion and conditional integral R^C/R^A for the specified abstract group-pair are valid scoped partials. Neither a degree-one meridian-compatible pair map from the unmarked full(G,pi2module,k) nor two actual smooth/locally flat PL S2-in-S4 exteriors with equal full triples and different homotopy types is realized. Both gaps remain explicit. Original18 and twelve immutable science/helper/result/source/ledger bodies are unchanged; original2/5,new0,audit0. The NEW whole-current source-first audit and genuine ROOT full reading/final reconciliation are separately bound. Global source/category/integral/history qualifications remain operative, including finite checks not proving realization/classification and absent raw prior versus SQL fallback{}. Current model/reasoning/deadline are null. No novelty, project solution, full prior-literature resolution, exhaustive priority, human peer review, paper, new DOI, tracker or release is claimed. One present acceptance event follows the exact original-head no-ff merge, preserves every prior state and the full history prefix, and consumes only the original two turns.\n'
PRESENT='The NEW whole-current source-first audit has passed for this scoped UNSOLVED standard partial; actual completed acceptance is bound in acceptance.json. SOURCE_PRECISION_QUALIFICATIONS.md and CURRENT_OBSTRUCTION_CONTEXT.md apply globally to OBSTRUCTION.md, every presentation and metadata file. The unmarked full triple supplies no boundary/meridian marking or degree-one pair map; no actual allowed-category equal-full-triple exterior pair is realized. The integral quotient is conditional on the specified abstract group-pair, and augmentation-lattice substitution is invalid. Original18 archive and twelve immutable bodies remain exact. Earlier PENDING/source-only/PASS/runtime/search/access/model statements in the frozen current packet and original archives remain dated attributions at or before its frozen publication; later actual acceptance records alone describe the present disposition. Raw prior absence and SQL fallback{} remain distinct. Original2/5,new0,audit0; current runtime fields null; no novelty, human referee, paper/new DOI/tracker/release.\n'
MIRROR_SCOPE='Incremental present accepted primary PR44 standard partial; original2/5, no new proof turn or historical reconstruction.'

def main():
    if not (A/'ROOT_WHOLE_CURRENT_REVIEW.json').is_file():raise ValueError('Actual ROOT whole inspection must exist before source authoring; no invented expected approval')
    manifest=load(C/'MANIFEST.json');assert sha((C/'MANIFEST.json').read_bytes())=='169f2825a8f730735627bdc33a43366c05e317fdf7ec4df4cd96a31e37329eb0' and manifest['files_count']==430
    wm=A/'whole_current_source_first_family/SELF_MANIFEST.json';assert sha(wm.read_bytes())=='ea6416b54945bf80d0a706cf878c8de707464ddcdaea66ae0e812868ff547c9f'
    sources=['pr43_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py']
    inputs={'schema':'pr44-source-preparation-individual-bindings/v1','pins':{},'external_inputs_excluded_from_authorship_and_copy':True,'production_sources_read_only_as_text':True}
    for n in sources:inputs['pins']['template_'+n]=pin(T/n)
    inputs['pins']['template_closure']=pin(T/'PREPARATION_MANIFEST.json')
    for n in ['snapshot_manifest_v2.json','ROOT_CURRENT_INPUT_PREIMAGES.json','ROOT_PRIMARY_READ_LEDGER.json','ROOT_SCIENCE_CARD.json','ROOT_CURRENT_FREEZE_INSPECTION.json']:
        inputs['pins'][n]=pin(A/n)
    for key,n in [('previous_mirror','state_mirror_bindings.json'),('previous_post','post_acceptance_verification.json'),('previous_root_post','ROOT_ACTUAL_POST_INSPECTION.json')]:inputs[key]=pin(A43/n)
    for p in sorted((A43/'root_pr43_complete_actual_post_inspection_capture').iterdir()):inputs['pins']['actual43_'+p.name]=pin(p)
    inputs['pins']['actual43_post_inspector_source']=pin(A43/'inspect_complete_actual_post.py')
    for key,p in [('closed_whole_manifest',wm),('closed_whole_report',wm.parent/'REPORT.md'),('closed_whole_result',wm.parent/'VERDICT.json'),('closed_root_whole_inspection',A/'ROOT_WHOLE_CURRENT_REVIEW.json')]:inputs[key]=pin(p)
    # Derived expected JSON objects are administrative specifications, not claimed new executions.
    put('EXPECTED_CURRENT_ADMIN.json',load(C/'status.json'));put('EXPECTED_WHOLE_VERDICT.json',load(wm.parent/'VERDICT.json'));put('EXPECTED_ROOT_WHOLE_REVIEW.json',load(A/'ROOT_WHOLE_CURRENT_REVIEW.json'))
    put('SCIENTIFIC_SCOPE.json',SCOPE)
    draft={'schema':'pr44-root-approved-immutable-acceptance-bindings/v1','status':'PENDING_ROOT_SOURCE_AND_PREDECESSOR_READING','created_utc':None,'root_full_current_read_completed':False,'root_full_whole_read_completed':False,'root_acceptance_source_review_completed':False,'independent_whole_current_pass':False,'root_actual_PR43_predecessor_read_completed':False,'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'mandatory_corrections':[]}
    for n in ['whole_manifest','root_whole_inspection','root_capture_operator','previous_mirror','previous_post','previous_root_post','acceptance_source_manifest','acceptance_source_verdict','root_source_inspection']:draft[n]=None
    put('DRAFT_ROOT_IMMUTABLE_BINDINGS.json',draft)
    plan={**SCIENCE,'schema':'pr44-root-reviewed-final-plan/v1','pr':44,'problem_id':2912,'original_head':'c772dc5b851ec91da9d46d534577609e5d3ca389','original_base':'01358d66fc67d1c462bddf31c0d4ee5b120e6737','reviewed_candidate_manifest_sha256':sha((C/'MANIFEST.json').read_bytes()),'current_dependencies_sha256':sha((C/'CURRENT_DEPENDENCIES.json').read_bytes()),'scientific_scope':SCOPE,'plan_status':'PENDING_ROOT_FULL_REVIEW_AND_ACTUAL_RECONCILIATION','partial_valid':None,'preparation_manifest_sha256':None,'whole_manifest_sha256':None,'root_bindings':None,'root_bindings_sha256':None,'root_full_current_read_completed':False,'root_full_whole_read_completed':False,'root_acceptance_source_review_completed':False,'root_actual_PR43_predecessor_read_completed':False,'independent_whole_current_pass':False,'immutable_evidence_references':[],'mandatory_corrections':[],'historical_PASS_transferred':False,'science_reexecution_of_current':False}
    put('DRAFT_FINAL_PLAN.json',plan)
    for n in sources:
        s=transform((T/n).read_text())
        if n=='pr43_guards.py':
            s=re.sub(r"LEDGER_SHA = '[^']+'",'LEDGER_SHA = '+repr(sha((C/'turns.jsonl').read_bytes())),s)
            s=re.sub(r'^IMMUTABLE = .*$',"IMMUTABLE = "+repr({'OBSTRUCTION.md','SOURCES.md','group_block_verification.json','review/independent_checks.py','review/independent_results.json','review/reviewed_obstruction.md','review/submitted_results.json','review/submitted_verifier.py','source_manifest.json','source_record.json','turns.jsonl','verify_group_block.py'}),s,flags=re.M)
            s=re.sub(r'^SCIENCE = .*$',"SCIENCE = "+repr(SCIENCE),s,flags=re.M)
            s=re.sub(r'^WHOLE_VERDICT = .*$',"WHOLE_VERDICT = 'PASS_SCOPED_ACTUAL_WHOLE_CURRENT_STANDARD_PARTIAL_ONLY'",s,flags=re.M)
            s=s.replace("'PR44_STRICT_CURRENT_PACKET_v1':{'schema','self_excluded','files_count','files','current_gate','prior_source_status','full_problem_solved_by_project','novelty_claimed','original_substantive_attempts','new_substantive_attempts','audit_turns'},","'PR44_STRICT_CURRENT_PACKET_v1':{'schema','self_excluded','files_count','files','current_gate','status','full_problem_solved','novelty_claimed','original_substantive_attempts','new_substantive_attempts','audit_turns','full_permission_mode'},")
            s=replace_function(s,'root_binding_input',ROOT_BINDING_FUNCTION);s=replace_function(s,'basis',BASIS_FUNCTION);s=replace_function(s,'source',SOURCE_FUNCTION)
            s=s.replace("len(snapshot['files'])==18","len(snapshot['files'])==18")
            s=s.replace("len(raw)==54344","len(raw)==75046")
            s=s.replace("original_substantive_attempts': 0","original_substantive_attempts': 2").replace("original_substantive_attempts':0","original_substantive_attempts':2")
            s=s.replace("substantive_attempts_used':0","substantive_attempts_used':2").replace("original_attempts='0/5'","original_attempts='2/5'").replace("cumulative_attempts='0/5'","cumulative_attempts='2/5'")
            s=s.replace("'full_target_resolved_in_prior_published_literature':True","'full_target_resolved_in_prior_published_literature':False").replace("'prior_publication_doi':'10.4064/sm210413-16-9'","'prior_publication_doi':None")
            s=s.replace("len(previous['entries'])==33 and 42 in previous['required_completed_prs'] and 44 not", "len(previous['entries'])==33 and 43 in previous['required_completed_prs'] and 44 not")
            # gates' predecessor checks use the actual43 schema, not a shifted PR42 label.
            start=s.index("    previous_root=B/'audits/pr43_30004386'",s.index('def gates('));end=s.index("    fresh=load(ps['fresh_preimage'])",start)
            s=s[:start]+"    authority,_=root_binding_input(a.root_bindings,a.root_bindings_sha256)\n    require(equal(pin(ps['previous_mirror']),authority['previous_mirror']) and equal(pin(ps['previous_post']),authority['previous_post']),'Entire actual43 predecessor references')\n"+s[end:]
            s=s.replace("entire_history_prefix_and33prior_states_preserved","entire_history_prefix_and34prior_states_preserved")
            s=s.replace("scope='Incremental present accepted primary PR44 standard-partial correction; original2/5, no new proof turn or historical reconstruction.'","scope="+repr(MIRROR_SCOPE))
            s=s.replace("'status':'unsolved','turns_used':0", "'status':'unsolved','turns_used':2")
            s=s.replace("'budget':{'used':0,'limit':5,'kind':'pr44_exact_original_empty_ledger'", "'budget':{'used':2,'limit':5,'kind':'pr44_exact_original_two_turn_JSONL'")
            s=s.replace("'negative_ledger_controls':['nonempty','whitespace_only','invented_JSONL','bool_used','wrong_used','wrong_limit']", "'negative_ledger_controls':['empty','whitespace_only','invented_JSONL','bool_used','wrong_used','wrong_limit']")
        elif n=='integrate_reviewed_partial.py':
            s=re.sub(r'^BODY = .*$', 'BODY = '+repr(BODY),s,flags=re.M);s=re.sub(r'^PRESENT_SCOPE = .*$', 'PRESENT_SCOPE = '+repr(PRESENT),s,flags=re.M)
            s=s.replace("cells[8]=' unsolved '; cells[11]=' [Accepted qualified scoped partial](attempts/2912/ACCEPTANCE.md) '","cells[8]=' unsolved '; cells[9]=' 2/5 '; cells[11]=' Standard meridional duality kernel, sufficient degree-one pair-map criterion and conditional integral kernel for the specified abstract group-pair; unmarked full2type pair-map and actual equal-full-triple exterior realization gaps remain. [Accepted scoped UNSOLVED partial](attempts/2912/ACCEPTANCE.md). Original2/5,new0,audit0; no novelty/paper/new DOI/tracker. '")
            s=s.replace("set(changed)<={8,11} and cells[9]==row.split('|')[9] and", "set(changed)=={8,9,11} and")
            s=s.replace("named_changes':['Status','Findings']", "named_changes':['Status','Turns','Findings']")
            s=s.replace("original_substantive_attempts':0","original_substantive_attempts':2")
            s=s.replace("sum(z['turns_used'] for z in state.values())==43", "sum(z['turns_used'] for z in state.values())==41")
            s=s.replace("original empty", "original two-turn")
            s=s.replace("original0/5", "original2/5").replace("original2/5 empty ledger", "original2/5 exact two-turn ledger")
            s=s.replace("Program34/180=18.3333%", "Program34/180=18.8889%")
            s=s.replace("original0/5", "original2/5")
        elif n=='state_mirror_reconciliation.py':
            s=s.replace("original_attempts':'0/5'", "original_attempts':'2/5'").replace("cumulative_attempts':'0/5'", "cumulative_attempts':'2/5'")
            s=s.replace("named_changes':['Status','Findings']", "named_changes':['Status','Turns','Findings']")
            s=s.replace("sum(z['turns_used'] for z in prior.values())==43", "sum(z['turns_used'] for z in prior.values())==41")
            s=s.replace("scope='Incremental present accepted primary PR44 standard-partial correction; original2/5, no new proof turn or historical reconstruction.'", "scope="+repr(MIRROR_SCOPE))
            s=s.replace("'budget':{'used':0,'limit':5,'kind':'pr44_exact_original_empty_ledger'", "'budget':{'used':2,'limit':5,'kind':'pr44_exact_original_two_turn_JSONL'")
            old="for label,raw,used,limit in [('nonempty',b'x',0,5),('whitespace_only',b'\\n',0,5),('invented_JSONL',b'{\"turn\":1}\\n',0,5),('bool_used',b'',False,5),('wrong_used',b'',1,5),('wrong_limit',b'',0,4)]:"
            new="for label,raw,used,limit in [('empty',b'',2,5),('whitespace_only',b'\\n',2,5),('invented_JSONL',b'{\"turn\":1}\\n',2,5),('bool_used',g.regular(g.K,'turns.jsonl').read_bytes(),True,5),('wrong_used',g.regular(g.K,'turns.jsonl').read_bytes(),1,5),('wrong_limit',g.regular(g.K,'turns.jsonl').read_bytes(),2,4)]:"
            if old not in s:raise ValueError('Expected exact ledger control source absent')
            s=s.replace(old,new).replace("'pr44_exact_original_empty_ledger'","'pr44_exact_original_two_turn_JSONL'")
            s=s.replace("'turns_used':0,'turn_limit':5,'status':'unsolved'", "'turns_used':2,'turn_limit':5,'status':'unsolved'")
        elif n=='verify_post_acceptance.py':
            s=s.replace("'turns_used':0,'turn_limit':5", "'turns_used':2,'turn_limit':5")
            s=s.replace("entire_history_prefix_and33prior_states_preserved", "entire_history_prefix_and34prior_states_preserved")
            s=s.replace("'full_target_resolved_in_prior_published_literature':True,'prior_publication_doi':'10.4064/sm210413-16-9'", "'full_target_resolved_in_prior_published_literature':False,'prior_publication_doi':None")
        output='pr44_guards.py' if n=='pr43_guards.py' else n
        put(output,s)
    operator=(A43/'capture_root_final_operation_v2.py').read_text()
    operator=operator.replace("script.parent in (A, A / 'acceptance_preparation_family_v2')", "script.parent in (A, A / 'acceptance_preparation_family')")
    operator=operator.replace('5e28953d65bf1490bc6519c55e8c27972b6bcbd788e20280c149bf688b24f011',sha((A/'ROOT_CURRENT_INPUT_PREIMAGES.json').read_bytes())).replace('PR43_ROOT_FRESH13_INPUT_PREIMAGES_v1',load(A/'ROOT_CURRENT_INPUT_PREIMAGES.json')['schema'])
    put('capture_root_final_operation.py',operator);inputs['pins']['template_root_operator']=pin(A43/'capture_root_final_operation_v2.py')
    put('INPUT_BINDINGS.json',inputs)
    put('SOURCE_STATUS.json',{'schema':'pr44-source-only-preparation-status/v1','status':'SOURCE_PREPARED_PENDING_INDEPENDENT_SOURCE_ADVERSARY_AND_ROOT','source_only':True,'production_imported_compiled_executed':False,'root_approval_claimed':False,'actual_acceptance_or_sealing_or_integration_or_native_mirror':False,'external_communication':False,'native_index_branch_remote_mutation':False,'source_preparation_completion_percent':100,'acceptance_completion_percent':0,'discovery_completion_percent':0})
    put('EXPECTED_NATIVE_TRANSITION.json',{'schema':'pr44-prospective-native-transition/v1','predecessor_pr':43,'predecessor_merge':'c60255489a342fae02c0acf3d1026255b47be3d1','predecessor_tree':'fdc2bb213905051a430d24e13afb20e54fa9106a','before':{'targets':34,'consumed_substantive_turns':41,'primary_acceptances':33,'duplicate_mirrors':1,'completed':33,'current_pr':44},'after':{'targets':35,'consumed_substantive_turns':43,'primary_acceptances':34,'duplicate_mirrors':1,'completed':34,'current_pr':45,'program_completion_estimate_percent':34/180*100},'selected_id':'2912','selected_status':'unsolved','original_attempts':'2/5','new_substantive_attempts':0,'audit_turns':0,'history_events_added':1,'entire_old_states_and_history_prefix_preserved':True,'new_duplicate_added':False,'whole_inventory_derived_preserving179others':True,'proposal_executed':False})
    put('CONTRACT.md',CONTRACT)
    put('RESEARCH_LOG.md','# PR44 acceptance source preparation research log\n\n'+dt.datetime.now(dt.timezone.utc).isoformat()+' — Source authoring checkpoint. Completion100% toward source preparation;0% toward acceptance and0% new discovery. Source-only scripts are proposed future ROOT operations. Actual43 predecessor and actual44 whole-current review are pinned. Two realization gaps retained. No production source imported, compiled or executed. Private independent controls and final closure remain.\n')
    print(json.dumps({'status':'SOURCE_AUTHORED','actual_author_pid':os.getpid(),'production_sources_executed':False,'outputs':len(list(H.iterdir())),'source_preparation_percent':100,'acceptance_percent':0},sort_keys=True))

CONTRACT='''# PR44 source-only final acceptance kit

This closed family supplies proposed future ROOT administrative scripts. No sealer,
acceptance, original-head merge, native mirror, index, branch or remote action was
executed by its author. Its own captured authoring and handwritten private controls
read production snippets as text only. Every capture preserves actual child and
operator PIDs, UTC launch/finish, exact argv/cwd, prelaunch full sources and complete
stdout/stderr; failures must stay preserved. Completion100% source preparation,
0% acceptance,0% discovery. A new different adversary and genuine ROOT full reading
are future gates.

The closed reviewed candidate has430 members plus MANIFEST.json, SHA256
169f2825a8f730735627bdc33a43366c05e317fdf7ec4df4cd96a31e37329eb0; its369 dependency
rows have SHA2562c8d2ef1cd1846a0b82dce49b8c8891f6821ca129bd42ec20cf4fc45ae258c18.
The new whole-current96+self closure is ea6416b54945bf80d0a706cf878c8de707464ddcdaea66ae0e812868ff547c9f.
The original18/19-path75046-byte diff is preserved. M1 uses the literal actual
snapshot_manifest_v2.json for PR44. M2 uses precisely the same complete literal
mirror scope in writer and guard, including semicolon and terminal punctuation.

The disposition stays UNSOLVED original2/5,new0,audit0, standard conditional
deductions only. The unmarked full(G,pi2module,k) supplies no meridian/boundary
marking or relative-degree-one pair map. No actual allowed-category equal-full-triple
exterior pair with different homotopy types is realized. The finite-support
duality kernel, sufficient pair-map criterion and nonzero integral quotient for
the specified abstract group-pair are the strongest verified partials. Source,
category, integral and historical qualifications apply globally. No novelty,
project solution, exhaustive priority, full prior-literature resolution, paper,
new DOI, tracker, release, human review or formal certification is claimed.

The actual predecessor is completed PR43, not PR42. All three actual43 records,
the genuine PID77832 full ROOT post capture and source, and the repaired45+self
source template are individually pinned as excluded inputs. The whole actual43
post equals its ROOT inspection's entire_post. Its accepted merge is
c60255489a342fae02c0acf3d1026255b47be3d1, treefdc2bb213905051a430d24e13afb20e54fa9106a.
Before44:34 native targets/41 consumed turns/33 primaries/one old duplicate.
After44:35 targets/43 turns/34 primaries/the same old duplicate; program34/180.
All34 entire old state objects and the full original history prefix are retained;
one present unsolved2/5 event is appended. The complete180-row inventory is
derived from retained actual preflight bytes with only the selected item and
declared clocks/counts/next45 metadata changed; all179 other entries stay exact.

The frozen epoch2b9d0234b1396fa84c4b34055b5e8e14c873588b remains fixed. Four dated
native queue/inventory/state/history bodies must be verified against immutable
Git100644 blobs. Nine stable bodies still match live dated hashes. Actual whole
964 foreign identities are individually checked; raw caches, third-party PDFs,
texts and renders are hash-bound references only and excluded from copies and
publication. Git preserves only100644, while every PRIMARY closed worktree file
uses literal full stat.S_IMODE0444; a clean checkout must restore that full mode.

Future ROOT fills false/null typed DRAFT_ROOT_IMMUTABLE_BINDINGS.json only after
genuine full current/whole/source/predecessor reading. It must bind a new distinct
source adversary SELF_MANIFEST.json and VERDICT.json and its own complete
ROOT_SOURCE_ACCEPTANCE_REVIEW.json, with the exact declared known schemas and
whole verdict, closure, input and actual-capture reading flags. There is no
sentinel or empty token that grants approval. ROOT copies the prepared exact
capture_root_final_operation.py source to the audit root, reads it completely,
and binds that actual operator. ROOT completes DRAFT_FINAL_PLAN.json only through
declared completed fields and the complete sorted immutable references. No draft
timestamp or future PID is fabricated.

The sealer requires --execute, --root-bindings and SHA,--plan and SHA,
--preparation-manifest-sha256 and one absent adjacent --output. It performs a
fresh whole-basis reconciliation and publishes exactly two records plus
FINAL_MANIFEST.json with all full0444 by absent-only rename. The five-member
genuine final ROOT capture binds prelaunch sealer/operator and complete stdio,
unchanged native13 and HEAD, its actual PID and clocks. This preparation runs it
zero times. Other scripts require --execute, preparation-manifest SHA and eight
path/SHA pairs:final-plan,final-receipt,final-manifest,reconciliation-capture,
previous-mirror,previous-post,fresh-preimage,root-bindings. Previous ROOT43 post is
explicitly in root-bindings. A genuine fresh13/mainHEAD preimage is required,
separate from the frozen epoch; its dated substantive rebase reason must be real.

Integration phases are preflight,overlay,prepush,finalize. ROOT performs ready/body,
the exact original-head no-ff merge, precise owned staging, commit and push. No
whole-directory staging is authorized: use the complete reviewed overlay names
and exact audit-owned release list, excluding every raw/foreign body. Guards
check parents[actualfreshmain,c772dc5b851ec91da9d46d534577609e5d3ca389], full canonical
Git100644 bodies, full queue and no unrelated changed merge paths. Only selected
Status,Turns,Findings change; Chat/DOI and every other queue byte stay exact.
The prospective finding names the specified abstract group-pair and both gaps.
Immutable science/helper/source/result/ledger and original18 archive stay exact.
Archived pending administration is preserved; present scope is a new separate
qualification. Lowercase acceptance is written only after actual MERGED receipt.

Native mirror reconstruction binds all prior exact ledger bodies and budgets,
actual source plus full proposal. Its strict two-turn controls reject empty,
whitespace,invented JSONL,bool used,wrong used and wrong limit. It rebuilds the
entire saved plan at its actual timestamp from retained old state/history before
comparing it, appends history first under a cooperative lock, and checks all
protected bodies and prior states. A fresh final replay must be a byte-preserving
no-op. Final post and a separate genuine ROOT whole-post inspection must check
full acceptance/parents/tree/inventory/publication flags, full counts, entire
old states/history and every complete capture. No broad guard is weakened.
'''
if __name__=='__main__':main()
