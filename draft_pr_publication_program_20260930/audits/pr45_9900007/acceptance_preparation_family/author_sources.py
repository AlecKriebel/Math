"""Own administrative source authoring. All prior/production scripts are read as text only."""
from pathlib import Path
import datetime as dt, hashlib, json, os, re
H=Path(__file__).resolve().parent;A=H.parent;R=H.parents[3];T=R/'draft_pr_publication_program_20260930/audits/pr44_2912/acceptance_preparation_family';P=T.parent;C=A/'reviewed_candidate'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}
def put(n,v):
 b=v.encode() if isinstance(v,str) else (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
 with (H/n).open('xb') as f:f.write(b)
def fn(s,n,text):
 start=s.index('def '+n+'(');end=s.find('\n\ndef ',start+1)
 return s[:start]+text.strip()+'\n'+(s[end:] if end>=0 else '')
def line(s,n,text):
 start=s.index(n+' = ');end=s.index('\n',start)
 return s[:start]+n+' = '+repr(text)+s[end:]
def transform(s):
 pairs={'pr43_30004386':'__PREVIOUS_AUDIT__','pr44':'pr45','PR44':'PR45','PR43':'PR44','2912':'9900007','KP-4.36':'AMR-098-0007','c772dc5b851ec91da9d46d534577609e5d3ca389':'d9b4acf5d070d1f04ffac86a4f08916a5629ff16','169f2825a8f730735627bdc33a43366c05e317fdf7ec4df4cd96a31e37329eb0':'d136815406dc35265a828deece080813c716c69c2bb915192e606acafdcdd4c5','2c8d2ef1cd1846a0b82dce49b8c8891f6821ca129bd42ec20cf4fc45ae258c18':'e215d1b33f3cdc562aeb53cee76519386d7d203acbe8c1c251370b3fd3bd2410','snapshot_manifest_v2.json':'snapshot_manifest.json','OBSTRUCTION.md':'PARTIAL.md','CURRENT_OBSTRUCTION_CONTEXT.md':'CURRENT_PARTIAL_CONTEXT.md','430':'497','369':'416','438':'505','440':'507','2b9d0234b1396fa84c4b34055b5e8e14c873588b':'264c26d539d616b0da6f8df76478a213d20939e4','original2/5':'original1/5','Original2/5':'Original1/5','unsolved2/5':'unsolved1/5','two-turn':'one-turn','two_turn':'one_turn','two turns':'one turn','34prior':'35prior','34_prior':'35_prior','41turns':'43turns','75046':'183402'}
 pattern=re.compile('|'.join(re.escape(k) for k in sorted(pairs,key=len,reverse=True)));s=pattern.sub(lambda m:pairs[m.group()],s).replace('__PREVIOUS_AUDIT__','pr44_2912')
 nums={'33':'34','34':'35','35':'36','41':'43','43':'44','44':'45','45':'46'}
 s=re.sub(r'(?<![\w])(?:33|34|35|41|43|44|45)(?![\w])',lambda m:nums[m.group()],s)
 for old,new in [("original_substantive_attempts':2","original_substantive_attempts':1"),("original_substantive_attempts': 2","original_substantive_attempts': 1"),("substantive_attempts_used':2","substantive_attempts_used':1"),("turns_used':2","turns_used':1"),("'used':2","'used':1"),("original_attempts='2/5'","original_attempts='1/5'"),("cumulative_attempts='2/5'","cumulative_attempts='1/5'"),("original_attempts':'2/5'","original_attempts':'1/5'"),("cumulative_attempts':'2/5'","cumulative_attempts':'1/5'"),("sum(z['turns_used'] for z in prior.values())==44","sum(z['turns_used'] for z in prior.values())==43"),("sum(z['turns_used'] for z in state.values())==44","sum(z['turns_used'] for z in state.values())==43")]:s=s.replace(old,new)
 return s
SCIENCE={'full_problem_solved':False,'full_target_resolved_in_prior_published_literature':False,'full_problem_solved_by_project':False,'prior_publication_doi':None,'partial_valid':True,'novelty_claimed':False,'priority_claimed':False,'original_substantive_attempts':1,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'verification_attempts_added':0,'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'paper_or_new_doi_or_tracker':False,'human_referee_review_claimed':False}
GAPS=['Alternative general two-process characterization','Exhaustive historical priority and full published-original comparison','ROOT final reconciliation and independent fresh then-current native/main acceptance authority']
SCOPE={**SCIENCE,'schema':'pr45-proposed-accepted-scientific-scope/v1','id':'9900007','problem_number':'AMR-098-0007','literal_target_status':'unsolved','literal_target':'General two-process coupling characterization of weak path-shift convergence, including the illustrative synchronous metric condition for one fixed joint construction.','strongest_verified_partial':'Original fair binary independent-flip example: shifted laws converge weakly to stationary constant-path mixture; for every fixed coupling mismatch tends to one half and synchronous metric distance fails to tend to zero.','exact_remaining_gaps':GAPS,'general_two_process_characterization_supplied_or_ruled_out':False,'illustrative_synchronous_condition_only':True,'stated_numerical_limit_uses_stated_product_metric':True,'other_compatible_metrics_claim_only_failure_to_zero':True,'offsets_nonnegative_finite_or_uniformly_tight_and_may_be_dependent':True,'escaping_offsets_not_covered':True,'each_n_new_coupling_not_one_fixed_coupling':True,'setwise_convergence_fails':True,'distinct_9900005_not_revised':True,'finite_controls_do_not_prove_arbitrary_coupling_quantifier':True,'AMR_prior_raw_present_nonempty_dict_matching_source_record_upstream_report':True,'historical_metadata_archival_only':True,'original18_and_immutable12_science_helpers_results_source_ledger_unchanged':True,'global_qualification_path':'SOURCE_PRECISION_QUALIFICATIONS.md','global_qualification_sha256':sha((C/'SOURCE_PRECISION_QUALIFICATIONS.md').read_bytes()),'primary_limits':'Recovered Thorisson operative Section3 text only, complete published original not compared; full CNRS preprint read; bounded Asmussen1992 pp739–741 OCR/pixels comparison retains sufficient one-time-marginal, different-epsilon-construction, finite offset/eventual time, stationary right-continuous scope. No exhaustive priority or universal present literature absence.','AI_tools_used_extensively':True,'human_peer_review':False,'formal_certification':False}
IMMUTABLE={'PARTIAL.md','SOURCES.md','binary_verification.json','review/independent_checks.py','review/independent_results.json','review/reviewed_partial.md','review/submitted_results.json','review/submitted_verifier.py','source_manifest.json','source_record.json','turns.jsonl','verify_binary.py'}
BODY='Accept PR45 / 9900007 / AMR-098-0007 as an UNSOLVED repository report of the original illustrative synchronous coupling obstruction. The original fair binary independent-flip example converges weakly under shifts to the stationary constant-path mixture, yet every fixed coupling has mismatch tending to one half and fails synchronous metric convergence to zero. The numerical metric law uses the stated product metric; other compatible metrics retain failure to zero. Nonnegative finite or uniformly tight offsets may be dependent; escaping offsets and setwise convergence are excluded. The broader general two-process characterization and exhaustive historical priority/full published-original comparison remain unresolved. Original18 and twelve immutable science/helper/result/source/ledger bodies stay exact; original1/5,new0,audit0. New whole-current and genuine ROOT reading/reconciliation are separately bound. AMR raw prior is PRESENT as a nonempty dictionary matching source_record.upstream_report. Earlier metadata remains archival, current model/reasoning/deadline are null. No novelty, priority, project solution, full prior-literature resolution, human peer review, paper, new DOI, tracker or release is claimed. One present acceptance event follows the exact original-head no-ff merge and preserves all prior states/history.\n'
PRESENT='Actual scoped repository acceptance is bound in acceptance.json. SOURCE_PRECISION_QUALIFICATIONS.md and CURRENT_PARTIAL_CONTEXT.md apply globally to PARTIAL.md and all current presentations/metadata. The original all-fixed-couplings synchronous obstruction is valid; broader two-process characterization remains unresolved. Stated metric law, nonnegative dependent finite/tight offset bounds and setwise boundary remain explicit. Audit-only duplicate-block/escaping-offset constructions do not expand the original accepted theorem or consume new author attempts. Original18 and immutable12 remain exact. The AMR raw prior is PRESENT nonempty dictionary matching source_record.upstream_report; no absent-prior/fallback narrative applies. Historical PENDING/PASS/runtime/access/model statements remain dated attributions; actual acceptance alone records current disposition. Original1/5,new0,audit0; current runtime null; no novelty, priority, human referee, paper/new DOI/tracker/release.\n'
MIRROR_SCOPE='Incremental present accepted primary PR45 illustrative synchronous coupling obstruction; original1/5, no new proof turn or historical reconstruction.'
ROOT_FUNCTION=r'''
def root_binding_input(name,pin_value):
    p=regular(R,name);require(p.parent==A and p.name!='DRAFT_ROOT_IMMUTABLE_BINDINGS.json','Genuine adjacent completed ROOT bindings required')
    require(sha(p.read_bytes())==digest(pin_value),'Actual ROOT bindings SHA differs')
    o=parse(p.read_bytes());draft=load(HERE/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json')
    keys=['whole_manifest','root_whole_inspection','root_capture_operator','previous_mirror','previous_post','previous_root_post','acceptance_source_manifest','acceptance_source_verdict','root_source_inspection']
    for k in keys:exact_reference(o[k]);check(R,[o[k]])
    draft.update(status='ROOT_APPROVED_CLOSED_WHOLE_SOURCE_AND_ACTUAL_PR44_EVIDENCE',created_utc=o['created_utc'],root_full_current_read_completed=True,root_full_whole_read_completed=True,root_acceptance_source_review_completed=True,independent_whole_current_pass=True,root_actual_PR44_predecessor_read_completed=True)
    for k in keys:draft[k]=o[k]
    require(equal(o,draft),'Complete typed known ROOT binding schema required')
    require(utc_clock(o['created_utc'],'ROOT approval')<=dt.datetime.now(dt.timezone.utc),'No future approval')
    inputs=load(HERE/'INPUT_BINDINGS.json')
    for k in ['previous_mirror','previous_post','previous_root_post']:require(equal(o[k],inputs[k]),'Actual44 predecessor pin differs')
    previous=load(R/o['previous_mirror']['path']);post=load(R/o['previous_post']['path']);rootpost=load(R/o['previous_root_post']['path'])
    require(equal(post,load(HERE/'EXPECTED_PREVIOUS_POST.json')) and equal(rootpost,load(HERE/'EXPECTED_PREVIOUS_ROOT_POST.json')),'Whole completed actual44 known typed records required')
    require(rootpost['schema']=='pr44-root-complete-actual-post-inspection/v1' and equal(rootpost['entire_post'],post),'Exact complete actual44 schema and entire_post equality')
    require(type(previous['entries']) is list and len(previous['entries'])==34 and all(type(z['pr']) is int for z in previous['entries']),'Exact34 completed primaries')
    nums=[z['pr'] for z in previous['entries']];require(len(set(nums))==34 and 44 in nums and 45 not in nums and equal(sorted(nums),previous['required_completed_prs']),'Actual44 primary identities')
    require(utc_clock(rootpost['utc'],'Actual44 post')<=utc_clock(o['created_utc'],'ROOT45 approval'),'Approval before predecessor prohibited')
    require(o['root_capture_operator']['path']==(A/'capture_root_final_operation.py').relative_to(R).as_posix() and bound(o['root_capture_operator'])==regular(HERE,'capture_root_final_operation.py').read_bytes(),'Exact prepared operator personally reviewed by ROOT')
    sm=regular(R,o['acceptance_source_manifest']['path']);sv=regular(R,o['acceptance_source_verdict']['path']);sr=regular(R,o['root_source_inspection']['path'])
    require(sm.parent==sv.parent and sm.parent.parent==A and sm.parent not in {C,HERE} and sm.name=='SELF_MANIFEST.json' and sv.name=='VERDICT.json','Fresh distinct source adversary required')
    own=load(sm);rr=rows(own['files']);require(own['self_excluded']==['SELF_MANIFEST.json'] and type(own['files_count']) is int and own['files_count']==len(rr),'Self-only source adversary closure')
    check(sm.parent,rr);exact(sm.parent,{z['path'] for z in rr}|{'SELF_MANIFEST.json'});frozen_files(sm.parent,rr,'SELF_MANIFEST.json')
    verdict=load(sv);required(verdict,{'schema':'pr45-acceptance-source-adversary-verdict/v1','verdict':'PASS_SOURCE_ONLY_SCOPED','preparation_manifest_sha256':sha((HERE/'PREPARATION_MANIFEST.json').read_bytes()),'mandatory_corrections':[],'production_imported_compiled_executed':False,'future_acceptance_approved':False},'Actual independent source gate')
    require(sr.parent==A and sr.name=='ROOT_SOURCE_ACCEPTANCE_REVIEW.json','Genuine ROOT source review literal path')
    root=load(sr);required(root,{'schema':'pr45-root-complete-acceptance-source-inspection/v1','status':'PASS_ROOT_COMPLETE_ACCEPTANCE_SOURCE_INSPECTION','all_prepared_source_and_controls_fully_read':True,'exact_preparation_closure_and_full_modes_checked':True,'all_individual_source_adversary_inputs_checked':True,'all_complete_actual_captures_checked':True,'complete_VERDICT_object':verdict,'preparation_manifest_sha256':sha((HERE/'PREPARATION_MANIFEST.json').read_bytes()),'acceptance_source_manifest':o['acceptance_source_manifest'],'acceptance_source_verdict':o['acceptance_source_verdict'],'mandatory_corrections':[],'future_execution_approved':False},'ROOT whole source/adversary reading')
    require(utc_clock(root['utc'],'ROOT source read')<=utc_clock(o['created_utc'],'Approval'),'Source review must precede approval')
    return o,p
'''
SOURCE_FUNCTION=r'''
def source(base):
    original_native(base/'original_archive')
    for n in IMMUTABLE:require(regular(base,n).read_bytes()==regular(A/'source_snapshot',n).read_bytes(),'Immutable science/helper/result/source/ledger changed')
    require(sha(regular(base,'PARTIAL.md').read_bytes())==SCIENCE_SHA and sha(regular(base,'source_record.json').read_bytes())==SOURCE_SHA,'Science/source anchor differs')
    raw=regular(base,'turns.jsonl').read_bytes();require(raw==regular(A/'source_snapshot','turns.jsonl').read_bytes() and sha(raw)==LEDGER_SHA,'Exact original one-turn JSONL ledger')
    entries=ledger_list(raw);require(len(entries)==1 and type(entries[0].get('turn')) is int and entries[0]['turn']==1,'Original1/5 exact one complete JSONL event')
    require(sha(regular(base,'SOURCE_PRECISION_QUALIFICATIONS.md').read_bytes())==load(HERE/'SCIENTIFIC_SCOPE.json')['global_qualification_sha256'],'Global probability/source/metric/offset/setwise qualification exact')
    require(type(load(base/'source_record.json')['upstream_report']) is dict and bool(load(base/'source_record.json')['upstream_report']),'Present nonempty upstream prior dictionary retained')
'''
ORIGINAL_FUNCTION=r'''
def original_native(base):
    snapshot=load(A/'snapshot_manifest.json')
    require(snapshot['schema']=='pr45-original-source-snapshot/v1' and snapshot['head']==HEAD and snapshot['merge_base']==ORIGINAL_BASE and snapshot['github_base']=='c6975ca76f9f667f1250ba403d0e6da2aafe14d0' and len(snapshot['files'])==18,'Literal distinct original18/head/GitHubbase/mergebase')
    exact(base,{z['relative_path'] for z in snapshot['files']})
    for z in snapshot['files']:
        n=z['relative_path'];relative(n);require(z['path']=='unsolved_math_prioritization/attempts/'+ID+'/'+n and z['git_mode']=='100644','Exact original literal paths/Git mode')
        raw=regular(base,n).read_bytes();require(raw==regular(A/'source_snapshot',n).read_bytes() and len(raw)==z['bytes'] and sha(raw)==z['sha256'],'Original18 full bytes differ')
'''
BASIS_FUNCTION=r'''
def basis(root_bindings,root_bindings_sha256):
    approved,rp=root_binding_input(root_bindings,root_bindings_sha256);inputs=load(HERE/'INPUT_BINDINGS.json');refs=[]
    for n in sorted(inputs['pins']):z=exact_reference(inputs['pins'][n]);check(R,[z]);refs.append(z)
    frozen=manifest(C,'MANIFEST.json',CURRENT_SHA,497,frozen=True);deps=load(C/'CURRENT_DEPENDENCIES.json')
    keyset(deps,{'anchor_repository_relative','resolution','files','foreign_primary_and_derivative_members_individually_hash_bound_not_copied','current_native13','current_main_head'},'Exact dependency schema')
    required(deps,{'anchor_repository_relative':A.relative_to(R).as_posix(),'resolution':'repository_root / anchor_repository_relative / files.path; never scratch','foreign_primary_and_derivative_members_individually_hash_bound_not_copied':True,'current_main_head':'264c26d539d616b0da6f8df76478a213d20939e4'},'Immutable dated dependencies')
    require(sha((C/'CURRENT_DEPENDENCIES.json').read_bytes())==DEPS_SHA and len(rows(deps['files']))==416,'All416 dependencies');check(A,deps['files']);source(C)
    for n in ADMIN:require(equal(load(C/n),load(HERE/'EXPECTED_CURRENT_ADMIN.json')),'Entire pending current admin')
    wm=exact_reference(approved['whole_manifest']);require(equal(wm,inputs['closed_whole_manifest']),'Closed whole immutable pin');w=A/'whole_current_source_first_family';whole=parse(bound(wm))
    require(equal(whole,load(HERE/'EXPECTED_WHOLE_MANIFEST.json')),'Entire known typed whole manifest')
    required(whole,{'schema':'pr45-whole-current-source-first-family-self-only-closure/v1','files_count':1068,'self_excluded':['MANIFEST.json'],'full_file_mode':'0444','reviewed_candidate_manifest_sha256':CURRENT_SHA,'current_dependency_manifest_sha256':DEPS_SHA,'foreign_primary_access_OCR_cache_SQL_body_copies':False,'future_native_acceptance_approved':False,'original_substantive_attempts':1,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False},'Known complete whole closure')
    rr=rows(whole['files']);require(len(rr)==1068,'All1068 whole members');check(w,rr);exact(w,{z['path'] for z in rr}|{'MANIFEST.json'});frozen_files(w,rr,'MANIFEST.json')
    require(equal(sorted(topology(w)[1]),sorted(z['path'] for z in whole['directories'])),'Whole complete directory topology')
    inventory=load(w/'EXTERNAL_INPUT_INVENTORY.json');require(equal(inventory,load(HERE/'EXPECTED_EXTERNAL_INPUT_INVENTORY.json')),'Entire known absolute excluded-input inventory')
    require(inventory['schema']=='pr45-whole-current-family-external-read-inventory/v1' and inventory['foreign_input_count']==1109 and len(inventory['foreign_inputs'])==1109,'All1109 external input identities')
    names=set()
    for z in inventory['foreign_inputs']:
        keyset(z,{'path','bytes','sha256'},'Exact absolute external reference');p=resolve_foreign_literal(z['path']);raw=p.read_bytes();require(type(z['bytes']) is int and len(raw)==z['bytes'] and sha(raw)==digest(z['sha256']),'Entire external body differs');names.add(p.relative_to(R).as_posix())
    require(len(names)==1109,'Unique absolute external identities')
    historical={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'};dated_head='264c26d539d616b0da6f8df76478a213d20939e4';dated=load(A/'ROOT_CURRENT_INPUT_PREIMAGES.json');require(dated['current_head']==dated_head,'Frozen epoch never rebound');native={z['path']:z for z in rows(dated['files'])};require(set(native)==NATIVE and (NATIVE-historical)<=names and not historical.intersection(names),'Independent frozen4 plus stable9 split')
    for n in sorted(historical):
        entries=git_bytes('ls-tree','-z',dated_head,'--',n).decode().split('\0');require(len(entries)==2 and entries[-1]=='','Exactly one frozen native Git entry');fields,literal=entries[0].split('\t');mode,kind,blob=fields.split();require(mode=='100644' and kind=='blob' and literal==n,'Exact frozen native100644 path');raw=git_bytes('show',dated_head+':'+n);require(len(raw)==native[n]['bytes'] and sha(raw)==native[n]['sha256'],'Whole frozen native4 body')
    verdict=parse(bound(inputs['closed_whole_result']));require(equal(verdict,load(HERE/'EXPECTED_WHOLE_VERDICT.json')),'Whole typed actual verdict')
    required(verdict,{'schema':'pr45-independent-whole-current-source-first-verdict/v1','verdict':WHOLE_VERDICT,'mandatory_corrections':[],'full_problem_solved':False,'original_substantive_attempts':1,'new_substantive_attempts':0,'audit_turns':0,'exact_remaining_gaps':load(HERE/'SCIENTIFIC_SCOPE.json')['exact_remaining_gaps']},'Scoped UNSOLVED probability gate');bound(inputs['closed_whole_report'])
    rootref=exact_reference(approved['root_whole_inspection']);require(equal(rootref,inputs['closed_root_whole_inspection']),'Genuine ROOT read pin');root=parse(bound(rootref));require(equal(root,load(HERE/'EXPECTED_ROOT_WHOLE_REVIEW.json')) and equal(root['complete_VERDICT_object'],verdict),'Entire genuine known typed ROOT whole inspection')
    required(root,{'schema':'pr45-root-complete-closed-whole-inspection/v1','status':'PASS_ROOT_COMPLETE_CLOSED_WHOLE_INSPECTION','candidate_manifest_sha256':CURRENT_SHA,'closed_whole_manifest_sha256':wm['sha256'],'first_party_members':1068,'individually_bound_foreign_inputs':1109,'personal_report_and_verdict_fully_read':True,'all_first_party_whole_bytes_and_modes_checked':True,'all_foreign_individual_whole_bytes_checked':True,'exact_self_only_recursive_closure_checked':True,'future_execution_approved':False,'mandatory_defects':[],'mandatory_corrections':[],'original_substantive_attempts':1,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved_by_project':False,'full_target_resolved_in_prior_published_literature':False,'dated_four_native_source_head':dated_head,'direct_four_independent_ROOT_Git_checks_completed':True},'Full ROOT PR45 reading flags')
    require(type(root['actual_direct_four_operator_pid']) is int and root['actual_direct_four_operator_pid']>0,'Genuine direct ROOT operator PID');commands=root['complete_dated_git_captures'];require(type(commands) is list and len(commands)==8,'Eight genuine ROOT native4 queries');expected=[]
    for n in sorted(historical):expected.extend([['git','ls-tree',dated_head,'--',n],['git','show',dated_head+':'+n]])
    require(equal([z['argv'] for z in commands],expected),'Exact ROOT full argv sequence')
    for i,z in enumerate(commands):
        required(z,{'cwd':str(R),'operator_pid':root['actual_direct_four_operator_pid'],'stdin_supplied':False,'exit_code':0,'actual_execution':True,'completed':True},'Actual complete ROOT direct Git query');require(type(z['pid']) is int and z['pid']>0 and utc_clock(z['started_utc'],'Git start')<=utc_clock(z['finished_utc'],'Git finish')<=utc_clock(root['created_utc'],'Root complete'),'Actual query PID/clocks')
        for channel in ['stdout','stderr']:exact_reference(z[channel]);check(R,[z[channel]])
        require(regular(R,z['stderr']['path']).read_bytes()==b'','Complete direct stderr');raw=regular(R,z['stdout']['path']).read_bytes();n=sorted(historical)[i//2]
        if i%2:require(len(raw)==native[n]['bytes'] and sha(raw)==native[n]['sha256'],'Whole direct frozen show stdout')
        else:
            require(raw.endswith(b'\n') and raw.count(b'\n')==1,'One whole direct ls-tree line');fields,literal=raw.decode().rstrip('\n').split('\t');mode,kind,blob=fields.split();require(mode=='100644' and kind=='blob' and literal==n,'Direct ls-tree exact100644/path')
    require(type(root['complete_actual_captures_checked']) is list and bool(root['complete_actual_captures_checked']),'Genuine nonempty complete capture read list')
    require(utc_clock(root['created_utc'],'ROOT whole')<=utc_clock(approved['created_utc'],'Approval'),'Whole read precedes approval')
    ledger=load(A/'ROOT_PRIMARY_READ_LEDGER.json');card=load(A/'ROOT_SCIENCE_CARD.json');require(equal(ledger,load(HERE/'EXPECTED_PRIMARY_READ_LEDGER.json')) and equal(card,load(HERE/'EXPECTED_SCIENCE_CARD.json')),'Entire genuine PR45 ledger/card');flags=load(HERE/'EXPECTED_PRIMARY_READ_LEDGER.json')['root_flags'];require(len(flags)==9 and ledger['reading_completed'] is True and card['reading_completed'] is True and equal(ledger['root_flags'],card['root_flags']) and all(v is True for v in flags.values()),'Nine exact PR45 scientific/source flags')
    refs += [pin(C/'MANIFEST.json'),pin(C/'CURRENT_DEPENDENCIES.json'),wm,inputs['closed_whole_result'],inputs['closed_whole_report'],rootref,pin(rp)]+[approved[n] for n in ['previous_mirror','previous_post','previous_root_post','acceptance_source_manifest','acceptance_source_verdict','root_source_inspection','root_capture_operator']]
    out={}
    for z in refs:require(z['path'] not in out or equal(out[z['path']],z),'Conflicting immutable identity');out[z['path']]=z
    return frozen,sorted(out.values(),key=lambda z:z['path'])
'''
FOREIGN_FUNCTION=r'''
def foreign_capture(fresh):
    require(not git('diff','--cached','--name-only'),'Preflight index clean required')
    paths=fresh['protected_foreign_tracked_paths'];require(type(paths) is list and paths==sorted(set(paths)),'Exact ROOT-declared sorted protected foreign paths')
    for n in paths:
        relative(n);require(n not in NATIVE and not n.startswith(K.relative_to(R).as_posix()+'/') and not n.startswith(A.relative_to(R).as_posix()+'/'),'Protected foreign path outside all owned/native scope required')
    dirty=set(git_bytes('diff','--name-only','-z').decode().split('\0'))-{''};require(dirty<=set(paths),'No undeclared tracked dirty exception')
    out=[]
    for n in paths:
        e=git_bytes('ls-tree','-z','HEAD','--',n).decode().rstrip('\0');fields,literal=e.split('\t');mode,kind,blob=fields.split();require(literal==n and kind=='blob' and mode in {'100644','100755'},'Regular tracked foreign path');raw=regular(R,n).read_bytes();out.append({'path':n,'bytes':len(raw),'sha256':sha(raw),'worktree_mode':stat.S_IMODE(regular(R,n).stat().st_mode),'head_sha256':sha(git_bytes('show','HEAD:'+n)),'head_entry':e,'index_entry':mode+' '+blob+' 0\t'+n})
    foreign_check({'foreign_logs':out,'fresh_preimage':fresh['_actual_path']});return out
'''
FOREIGN_CHECK=r'''
def foreign_check(pre):
    fresh=load(R/pre['fresh_preimage']);paths=fresh['protected_foreign_tracked_paths'];rr=pre['foreign_logs'];require([z['path'] for z in rr]==paths,'Exact protected ROOT declared foreign identities');check(R,rr)
    for z in rr:
        keyset(z,{'path','bytes','sha256','worktree_mode','head_sha256','head_entry','index_entry'},'Complete exact protected foreign reference');require(type(z['worktree_mode']) is int and stat.S_IMODE(regular(R,z['path']).stat().st_mode)==z['worktree_mode'],'Protected foreign full modes changed');n=z['path'];require(git_bytes('ls-tree','-z','HEAD','--',n).decode().rstrip('\0')==z['head_entry'] and git_bytes('ls-files','--stage','-z','--',n).decode().rstrip('\0')==z['index_entry'] and sha(git_bytes('show','HEAD:'+n))==z['head_sha256'] and sha(git_bytes('show',':'+n))==z['head_sha256'],'Protected foreign exact HEAD/index body/mode changed')
'''
def main():
 assert sha((C/'MANIFEST.json').read_bytes())=='d136815406dc35265a828deece080813c716c69c2bb915192e606acafdcdd4c5'
 inputs={'schema':'pr45-source-preparation-individual-bindings/v1','pins':{},'external_inputs_excluded_from_authorship_and_copy':True,'production_sources_read_only_as_text':True}
 sources=['pr44_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','capture_root_final_operation.py']
 for n in sources:inputs['pins']['template_'+n]=pin(T/n)
 inputs['pins']['template_closure']=pin(T/'PREPARATION_MANIFEST.json');inputs['pins']['template_adversary_closure']=pin(P/'acceptance_source_adversary_family/SELF_MANIFEST.json')
 for n in ['snapshot_manifest.json','original_diff.patch','ROOT_CURRENT_INPUT_PREIMAGES.json','ROOT_PRIMARY_READ_LEDGER.json','ROOT_SCIENCE_CARD.json','ROOT_CURRENT_FREEZE_INSPECTION.json','ROOT_SOURCE_SAFETY_BINDING.json']:
  if (A/n).exists():inputs['pins'][n]=pin(A/n)
 for key,n in [('previous_mirror','state_mirror_bindings.json'),('previous_post','post_acceptance_verification.json'),('previous_root_post','ROOT_ACTUAL_POST_INSPECTION.json')]:inputs[key]=pin(P/n)
 for p in sorted((P/'root_pr44_complete_actual_post_inspection_v2_capture').iterdir()):inputs['pins']['actual44_'+p.name]=pin(p)
 inputs['pins']['actual44_post_inspector_source']=pin(P/'inspect_complete_actual_post_v2.py')
 w=A/'whole_current_source_first_family'
 for key,n in [('closed_whole_manifest','MANIFEST.json'),('closed_whole_report','REPORT.md'),('closed_whole_result','VERDICT.json')]:inputs[key]=pin(w/n)
 put('INPUT_BINDINGS_PENDING_ROOT.json',inputs)
 for n,p in [('EXPECTED_CURRENT_ADMIN.json',C/'status.json'),('EXPECTED_WHOLE_VERDICT.json',w/'VERDICT.json'),('EXPECTED_WHOLE_MANIFEST.json',w/'MANIFEST.json'),('EXPECTED_EXTERNAL_INPUT_INVENTORY.json',w/'EXTERNAL_INPUT_INVENTORY.json'),('EXPECTED_PREVIOUS_POST.json',P/'post_acceptance_verification.json'),('EXPECTED_PREVIOUS_ROOT_POST.json',P/'ROOT_ACTUAL_POST_INSPECTION.json'),('EXPECTED_PRIMARY_READ_LEDGER.json',A/'ROOT_PRIMARY_READ_LEDGER.json'),('EXPECTED_SCIENCE_CARD.json',A/'ROOT_SCIENCE_CARD.json')]:put(n,load(p))
 put('SCIENTIFIC_SCOPE.json',SCOPE)
 draft={'schema':'pr45-root-approved-immutable-acceptance-bindings/v1','status':'PENDING_ROOT_SOURCE_AND_PREDECESSOR_READING','created_utc':None,'root_full_current_read_completed':False,'root_full_whole_read_completed':False,'root_acceptance_source_review_completed':False,'independent_whole_current_pass':False,'root_actual_PR44_predecessor_read_completed':False,'original_substantive_attempts':1,'new_substantive_attempts':0,'audit_turns':0,'mandatory_corrections':[]}
 for n in ['whole_manifest','root_whole_inspection','root_capture_operator','previous_mirror','previous_post','previous_root_post','acceptance_source_manifest','acceptance_source_verdict','root_source_inspection']:draft[n]=None
 put('DRAFT_ROOT_IMMUTABLE_BINDINGS.json',draft)
 plan={**SCIENCE,'schema':'pr45-root-reviewed-final-plan/v1','pr':45,'problem_id':9900007,'original_head':'d9b4acf5d070d1f04ffac86a4f08916a5629ff16','original_base':'01358d66fc67d1c462bddf31c0d4ee5b120e6737','original_github_base':'c6975ca76f9f667f1250ba403d0e6da2aafe14d0','reviewed_candidate_manifest_sha256':sha((C/'MANIFEST.json').read_bytes()),'current_dependencies_sha256':sha((C/'CURRENT_DEPENDENCIES.json').read_bytes()),'scientific_scope':SCOPE,'plan_status':'PENDING_ROOT_FULL_REVIEW_AND_ACTUAL_RECONCILIATION','partial_valid':None,'preparation_manifest_sha256':None,'whole_manifest_sha256':None,'root_bindings':None,'root_bindings_sha256':None,'root_full_current_read_completed':False,'root_full_whole_read_completed':False,'root_acceptance_source_review_completed':False,'root_actual_PR44_predecessor_read_completed':False,'independent_whole_current_pass':False,'immutable_evidence_references':[],'mandatory_corrections':[],'historical_PASS_transferred':False,'science_reexecution_of_current':False}
 put('DRAFT_FINAL_PLAN.json',plan)
 for n in sources[:-1]:
  s=transform((T/n).read_text())
  if n=='pr44_guards.py':
   for key,val in [('SOURCE_SHA',sha((C/'source_record.json').read_bytes())),('LEDGER_SHA',sha((C/'turns.jsonl').read_bytes())),('SCIENCE_SHA',sha((C/'PARTIAL.md').read_bytes())),('IMMUTABLE',IMMUTABLE),('SCIENCE',SCIENCE),('WHOLE_VERDICT','PASS_WHOLE_CURRENT_SCOPED_NO_MANDATORY_CORRECTION')]:s=line(s,key,val)
   s=fn(s,'root_binding_input',ROOT_FUNCTION);s=fn(s,'basis',BASIS_FUNCTION);s=fn(s,'source',SOURCE_FUNCTION);s=fn(s,'original_native',ORIGINAL_FUNCTION);s=fn(s,'foreign_capture',FOREIGN_FUNCTION);s=fn(s,'foreign_check',FOREIGN_CHECK)
   # Complete original snapshot schema is materially different from predecessor.
   st=s.index("    snap=load(A/'snapshot_manifest.json');",s.index('def gates('));en=s.index('    for rev in [ORIGINAL_BASE,HEAD]:',st)
   s=s[:st]+"    snap=load(A/'snapshot_manifest.json');original_native(C/'original_archive')\n    raw=git_bytes('diff',ORIGINAL_BASE,HEAD);require(raw==(C/'original_diff.patch').read_bytes() and raw==(A/'original_diff.patch').read_bytes() and len(raw)==183402,'Entire original19-path diff')\n    require(len(git_bytes('diff','--name-only',ORIGINAL_BASE,HEAD).decode().splitlines())==19,'Original19 changed paths')\n    for z in snap['files']:\n        require(git_bytes('show',HEAD+':'+z['path'])==(C/'original_archive'/z['relative_path']).read_bytes(),'Original Git/archive full bytes')\n        require(git_bytes('ls-tree','-z',HEAD,'--',z['path']).decode().rstrip('\\0')==z['git_mode']+' blob '+z['git_object']+'\\t'+z['path'],'Exact original Git mode/object')\n"+s[en:]
   s=s.replace("'current_head','files'},'Exact current ROOT fresh input schema'","'current_head','files','protected_foreign_tracked_paths'},'Exact current ROOT fresh input schema'")
   s=s.replace("scope='Incremental present accepted primary PR45 standard partial; original1/5, no new proof turn or historical reconstruction.'",'scope='+repr(MIRROR_SCOPE))
   s=s.replace("FOREIGN_LOGS = {", "LEGACY_FOREIGN_LOGS_UNUSED = {")
  elif n=='integrate_reviewed_partial.py':
   s=line(s,'BODY',BODY);s=line(s,'PRESENT_SCOPE',PRESENT)
   s=s.replace("cells[9]=' 2/5 '","cells[9]=' 1/5 '")
   st=s.index("cells[11]=' Standard meridional");en=s.index('\n',st)
   s=s[:st]+"cells[11]="+repr(' Original all-fixed-couplings illustrative synchronous obstruction is valid; broad general two-process characterization and exhaustive priority/full published-original comparison remain unresolved. Metric law, nonnegative dependent finite/tight offsets and setwise boundary retained. [Accepted scoped UNSOLVED partial](attempts/9900007/ACCEPTANCE.md). Original1/5,new0,audit0; no novelty/priority/paper/new DOI/tracker. ')+s[en:]
   s=s.replace("Only named Status/Findings may change", "Only named Status/Turns/Findings may change")
   s=s.replace("foreign=g.foreign_capture(); fresh=g.load(g.R/a.fresh_preimage);", "fresh=g.load(g.R/a.fresh_preimage);foreign=g.foreign_capture({**fresh,'_actual_path':a.fresh_preimage});")
   s=s.replace("orig=g.rows(g.load(g.A/'snapshot_manifest.json')['files']); g.exact(g.K,{z['path'] for z in orig});", "orig=g.load(g.A/'snapshot_manifest.json')['files'];g.exact(g.K,{z['relative_path'] for z in orig});")
   s=s.replace('Kirby4.36','AMR-098-0007').replace('standard-partial partial','illustrative synchronous coupling obstruction').replace('absent raw prior and SQL fallback','present raw prior and matching upstream dictionary').replace('Program34/180=18.8889%','Program35/180=19.4444%')
  elif n=='state_mirror_reconciliation.py':
   s=s.replace("scope='Incremental present accepted primary PR45 standard partial; original1/5, no new proof turn or historical reconstruction.'",'scope='+repr(MIRROR_SCOPE))
   st=s.index("    for label,raw,used,limit in [");en=s.index('\n',st)
   s=s[:st]+"    for label,raw,used,limit in [('empty',b'',1,5),('whitespace_only',b'\\n',1,5),('invented_JSONL',b'{\"turn\":1}\\n',1,5),('bool_used',g.regular(g.K,'turns.jsonl').read_bytes(),True,5),('wrong_used',g.regular(g.K,'turns.jsonl').read_bytes(),2,5),('wrong_limit',g.regular(g.K,'turns.jsonl').read_bytes(),1,4)]:"+s[en:]
  out='pr45_guards.py' if n=='pr44_guards.py' else n;put(out,s)
 # Future genuine sealer capture operator retains source-only drafting status.
 operator=(T/'capture_root_final_operation.py').read_text()
 st=operator.index("    native_record_raw = ");en=operator.index('    def native():',st)
 operator=operator[:st]+"    native_paths = "+repr(sorted(load(A/'ROOT_CURRENT_INPUT_PREIMAGES.json')['files'],key=lambda z:z['path']))+"\n    native_paths=[z['path'] for z in native_paths]\n"+operator[en:]
 put('capture_root_final_operation.py',operator)
 put('SOURCE_STATUS.json',{'schema':'pr45-source-only-preparation-status/v1','status':'SOURCE_PREPARED_PENDING_ACTUAL_ROOT_WHOLE_REVIEW_BINDING_AND_CONTROLS','source_only':True,'production_imported_compiled_executed':False,'root_approval_claimed':False,'actual_acceptance_or_sealing_or_integration_or_native_mirror':False,'external_communication':False,'native_index_branch_remote_mutation':False,'source_preparation_completion_percent':70,'acceptance_completion_percent':0,'discovery_completion_percent':0})
 put('EXPECTED_NATIVE_TRANSITION.json',{'schema':'pr45-prospective-native-transition/v1','predecessor_pr':44,'predecessor_merge':'f369d1e8f74b6462a0866f4b57a888233420a149','predecessor_tree':'6fa2de74e3b7d658cde5b04b94bc699ad6648d88','before':{'targets':35,'consumed_substantive_turns':43,'primary_acceptances':34,'duplicate_mirrors':1,'completed':34,'current_pr':45},'after':{'targets':36,'consumed_substantive_turns':44,'primary_acceptances':35,'duplicate_mirrors':1,'completed':35,'current_pr':46,'program_completion_estimate_percent':35/180*100},'selected_id':'9900007','selected_status':'unsolved','original_attempts':'1/5','new_substantive_attempts':0,'audit_turns':0,'history_events_added':1,'entire_old_states_and_history_prefix_preserved':True,'new_duplicate_added':False,'whole_inventory_derived_preserving179others':True,'proposal_executed':False})
 put('RESEARCH_LOG.md','# PR45 acceptance source preparation research log\n\n'+dt.datetime.now(dt.timezone.utc).isoformat()+' — Initial source checkpoint:70% preparation,0% acceptance,0% discovery. Actual completed44 predecessor pinned, original1/5 unchanged, future approval fields false/null. Actual ROOT whole review not copied until genuine record exists. All production sources read as text only; no mutations outside this new family.\n')
 print(json.dumps({'status':'SOURCE_AUTHORED_PENDING_GENUINE_ROOT_WHOLE','actual_author_pid':os.getpid(),'production_sources_executed':False,'source_preparation_percent':70,'acceptance_percent':0},sort_keys=True))
if __name__=='__main__':main()
