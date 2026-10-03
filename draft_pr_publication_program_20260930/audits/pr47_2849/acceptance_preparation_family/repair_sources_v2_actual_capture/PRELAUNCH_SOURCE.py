"""Private textual preparation. Reads prior completed pattern, never imports it."""
import copy, hashlib, json, os, re
from pathlib import Path
F=Path(__file__).absolute().parent; A=F.parent; R=F.parents[3]; B=R/'draft_pr_publication_program_20260930'; T=B/'audits/pr45_9900007/acceptance_preparation_family'; C=A/'reviewed_candidate'
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return p.read_bytes()
def load(p):return json.loads(read(p))
def output(n,b):
    with (F/n).open('xb') as h:h.write(b.encode() if type(b) is str else b);h.flush();os.fsync(h.fileno())
def dump(n,o):output(n,(json.dumps(o,sort_keys=True,indent=2,allow_nan=False)+'\n').encode())
def replace_function(s,name,new):
    pattern=r'(?ms)^def '+re.escape(name)+r'\(.*?(?=^def |\Z)'; s,n=re.subn(pattern,lambda m:new.rstrip()+'\n\n\n',s)
    if n!=1:raise ValueError('One textual function '+name)
    return s
def transform(s):
    s=s.replace('pr45','pr47').replace('PR45','PR47').replace('9900007','2849').replace('AMR-098-0007','KP-3.51')
    s=s.replace('turns.jsonl','turns.json').replace('PARTIAL.md','OBSTRUCTION.md').replace('pr47_exact_original_one_turn_JSONL','pr47_exact_original_one_turn_object')
    s=s.replace("'pr':45","'pr':47").replace("'pr': 45","'pr': 47").replace("'number':45","'number':47").replace("'number': 45","'number': 47").replace("pull/45","pull/47").replace("[45]","[47]").replace("==45","==47")
    s=s.replace("'current_pr':46","'current_pr':48").replace('current_pr=46','current_pr=48')
    # Distinct before/after counters:37 targets44 turns36 primary ->38/45/37.
    s=s.replace('len(state)==35','len(state)==37').replace('len(prior)==35','len(prior)==37').replace('len(current)==36','len(current)==38').replace("len(plan['state_after'])==36","len(plan['state_after'])==38")
    s=s.replace("sum(z['turns_used'] for z in state.values())==43","sum(z['turns_used'] for z in state.values())==44").replace("sum(z['turns_used'] for z in prior.values())==43","sum(z['turns_used'] for z in prior.values())==44").replace("sum(z['turns_used'] for z in current.values())==44","sum(z['turns_used'] for z in current.values())==45").replace("sum(z['turns_used'] for z in plan['state_after'].values())==44","sum(z['turns_used'] for z in plan['state_after'].values())==45")
    for old,new in [("'prior_state_entries_preserved':35","'prior_state_entries_preserved':37"),("'primary_acceptances':35","'primary_acceptances':37"),("'current_targets':36","'current_targets':38"),("'targets':36","'targets':38"),("'targets': 36","'targets': 38"),("'consumed_substantive_turns':44","'consumed_substantive_turns':45"),("'consumed_turns':44","'consumed_turns':45"),("'turns':44","'turns':45"),("'program_completed_count':35","'program_completed_count':37"),("'completed_count':35","'completed_count':37"),("plan['primary_count']==35","plan['primary_count']==37"),("inv['completed_count']==35","inv['completed_count']==37"),("inv['completed_count']==34","inv['completed_count']==36"),("for z in inv['items'])==35","for z in inv['items'])==37"),("for z in inv['items'])==34","for z in inv['items'])==36")]:s=s.replace(old,new)
    s=s.replace('entire_history_prefix_and35prior_states_preserved','entire_history_prefix_and37prior_states_preserved').replace('exact_original18_and_PARTIAL_unchanged','exact_original16_and_corrected_OBSTRUCTION_unchanged').replace('whole_current497_and416dependencies_bound','whole_current1328_and1422dependencies_bound')
    s=s.replace('illustrative synchronous coupling obstruction','corrected reducible Floer obstruction and known realized degeneracy').replace('UNSOLVED probability gate','UNSOLVED Floer partial gate')
    s=s.replace('Original18','Original16').replace('original18','original16').replace('immutable12','immutable10').replace('Immutable12','Immutable10').replace('twelve immutable','ten immutable')
    return s

BODY='Accept PR47 / 2849 / KP-3.51 as a corrected UNSOLVED partial repository report. The target remains the assertion that every closed connected oriented SU(2)-abelian rational homology three-sphere has framed-instanton rank equal to the order of its first homology. Reducible critical-set counting supplies a conditional route subject to the complete nondegeneracy hypotheses; a universal normal-cohomology vanishing route is false. The realized degenerate Seifert example and its complete SU(2)-abelian classification are credited to Sivek-Zentner; the project does not claim a new example, an instanton-rank computation, or a counterexample to KP-3.51. The quartic lower-link model is unrealized, and the trefoil surgery is an auxiliary known rank-six example with version-specific unsquared-character scope. Exact remaining gap: actual degenerate reducible Floer contribution and differential control, or another sufficient mechanism. The corrected OBSTRUCTION, realized-degeneracy proof and global source/provenance qualifications govern all operative presentations. Literal original16 archive and operative immutable10 remain exact. Original1/5,new0,audit0. Raw upstream prior absence, literal null and source authentication limits remain qualified; no historical model, PASS, PDF hash or runtime is promoted to current authority. Extensive AI use; unrefereed; no human peer review, full solution, novelty, priority, paper, new DOI, tracker or release. PR46 must actually complete before this one present acceptance; all prior states, history, ledgers and duplicate accounting remain exact.\n'
PRESENT_SCOPE=BODY+'Actual accepted disposition alone is recorded in lowercase acceptance.json after the genuine merge receipt. SOURCE_PRECISION_QUALIFICATIONS.md, SOURCE_PROVENANCE_CORRECTION.md and REALIZED_DEGENERACY_PROOF.md apply globally; inherited dated PENDING and runtime metadata remain archival. Current model, reasoning effort and deadline are null.\n'

rootbinding=r'''def root_binding_input(name,pin_value):
    p=regular(R,name);require(p.parent==A and p.name=='ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json','Genuine adjacent final ROOT approval required');require(sha(p.read_bytes())==digest(pin_value),'Actual ROOT approval pin')
    o=parse(p.read_bytes());draft=load(HERE/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json');keys=['whole_manifest','root_whole_inspection','root_capture_operator','previous_mirror','previous_post','previous_root_post','previous_post_contract','acceptance_source_manifest','acceptance_source_verdict','root_source_inspection']
    for k in keys:exact_reference(o[k]);check(R,[o[k]])
    draft.update(status='ROOT_APPROVED_CLOSED_WHOLE_SOURCE_AND_ACTUAL_PR46_EVIDENCE',created_utc=o['created_utc'],root_full_current_read_completed=True,root_full_whole_read_completed=True,root_acceptance_source_review_completed=True,independent_whole_current_pass=True,root_actual_PR46_predecessor_read_completed=True)
    for k in keys:draft[k]=o[k]
    require(equal(o,draft),'Complete typed ROOT approval, no extension or pending predecessor');clock=utc_clock(o['created_utc'],'Actual ROOT approval');require(clock<=dt.datetime.now(dt.timezone.utc),'No future approval')
    predecessor46(o,clock)
    require(o['root_capture_operator']['path']==(A/'capture_root_final_operation.py').relative_to(R).as_posix() and bound(o['root_capture_operator'])==regular(HERE,'capture_root_final_operation.py').read_bytes(),'Exact prepared final operator separately read by ROOT')
    sm=regular(R,o['acceptance_source_manifest']['path']);sv=regular(R,o['acceptance_source_verdict']['path']);sr=regular(R,o['root_source_inspection']['path'])
    require(sm.parent==sv.parent and sm.parent.parent==A and sm.parent.name.startswith('acceptance_source_adversary_family') and sm.name=='SELF_MANIFEST.json' and sv.name=='VERDICT.json','New distinct acceptance SOURCE adversary closure required')
    own=load(sm);rr=rows(own['files']);require(own['self_excluded']==['SELF_MANIFEST.json'] and type(own['files_count']) is int and own['files_count']==len(rr),'Literal SOURCE self-only count');check(sm.parent,rr);exact(sm.parent,{z['path'] for z in rr}|{'SELF_MANIFEST.json'});frozen_files(sm.parent,rr,'SELF_MANIFEST.json')
    verdict=load(sv);required(verdict,{'schema':'pr47-acceptance-source-adversary-verdict/v1','verdict':'PASS_SOURCE_ONLY_SCOPED','preparation_manifest_sha256':sha((HERE/'PREPARATION_MANIFEST.json').read_bytes()),'mandatory_corrections':[],'production_imported_compiled_executed':False,'future_acceptance_approved':False},'New SOURCE gate')
    require(sr.parent==A and sr.name=='ROOT_SOURCE_ACCEPTANCE_REVIEW.json','Genuine ROOT acceptance SOURCE read')
    root=load(sr);required(root,{'schema':'pr47-root-complete-acceptance-source-inspection/v1','status':'PASS_ROOT_COMPLETE_ACCEPTANCE_SOURCE_INSPECTION','all_prepared_source_and_controls_fully_read':True,'exact_preparation_closure_and_full_modes_checked':True,'all_individual_source_adversary_inputs_checked':True,'all_complete_actual_captures_checked':True,'complete_VERDICT_object':verdict,'preparation_manifest_sha256':sha((HERE/'PREPARATION_MANIFEST.json').read_bytes()),'acceptance_source_manifest':o['acceptance_source_manifest'],'acceptance_source_verdict':o['acceptance_source_verdict'],'mandatory_corrections':[],'future_execution_approved':False},'Complete genuine ROOT SOURCE reading')
    full_source_adversary_bindings(root,sm.parent)
    require(utc_clock(root['utc'],'Actual SOURCE read')<=clock,'SOURCE reading precedes approval')
    return o,p

def predecessor46(o,clock):
    previous=load(R/o['previous_mirror']['path']);post=load(R/o['previous_post']['path']);rootpost=load(R/o['previous_root_post']['path']);contract=load(R/o['previous_post_contract']['path'])
    p46=B/'audits/pr46_30004438'
    for k,n in [('previous_mirror','state_mirror_bindings.json'),('previous_post','post_acceptance_verification.json'),('previous_root_post','ROOT_ACTUAL_POST_INSPECTION.json')]:require(R/o[k]['path']==p46/n,'Exact actual predecessor46 path')
    cp=R/o['previous_post_contract']['path'];require(cp.parent.parent==p46 and cp.parent.name.startswith('acceptance_preparation_family') and cp.name=='ROOT_POST_CONTRACT.json','Closed46 source contract, not manufacture')
    require(stat.S_IMODE(cp.stat().st_mode)==0o444 and cp.parent!=HERE,'Actual closed predecessor source contract');manifest(cp.parent,'PREPARATION_MANIFEST.json',frozen=True)
    require(contract['schema']=='pr46-future-ROOT-whole-post-contract/v1' and contract['source_only'] is True,'Literal predecessor contract schema')
    keyset(rootpost,contract['future46_required_ROOT_complete_keyset'],'Entire real completed46 ROOT post contract')
    required(rootpost,{'schema':contract['future46_required_ROOT_schema'],**contract['future46_required_completed_values'],'entire_post':post},'Actual completed46 ROOT post, entire typed post')
    require(rootpost['status']=='PASS' and type(rootpost['completed_primary_prs']) is int and rootpost['completed_primary_prs']==36,'Actual36 predecessor primaries')
    required(post,contract['future46_required_entire_post_values'],'Actual46 complete post values');required(post,{'status':'PASS','pr':46,'targets':37,'consumed_substantive_turns':44,'primary_acceptances':36,'program_completed_count':36,'program_completion_estimate_percent':20.0,'new_proof_turns':0,'paper_or_new_doi_or_tracker':False},'PR46 actually complete37/44/36, not SOURCE readiness')
    require(utc_clock(rootpost['utc'],'Actual46 post')<=clock and utc_clock(post['utc'],'Actual46 verifier')<=utc_clock(rootpost['utc'],'Actual46 ROOT'),'Actual predecessor must precede47 approval')
    require(type(previous['entries']) is list and len(previous['entries'])==36 and all(type(z['pr']) is int for z in previous['entries']),'All36 prior primary records');nums=[z['pr'] for z in previous['entries']];require(len(set(nums))==36 and 46 in nums and 47 not in nums and equal(sorted(nums),previous['required_completed_prs']),'Exact completed46 primary membership')
    require(type(previous['duplicate_mirrors']) is list and len(previous['duplicate_mirrors'])==1,'Preserved one actual duplicate')
    # Actual completed ROOT must individually bind/read every genuine phase capture.
    caps=rootpost['all_six_real_phase_captures'];require(type(caps) is list and len(caps)>=6,'Complete actual46 captures, no Boolean substitute')
    for item in caps:
        require(type(item) is dict,'Actual capture binding row');ref=item.get('capture',item.get('CAPTURE',item));exact_reference(ref);check(R,[ref]);p=R/ref['path'];cap=load(p);required(cap,{'actual_execution':True,'completed':True,'exit_code':0,'stdin_supplied':False},'Completed actual predecessor child');require(type(cap['pid']) is int and cap['pid']>0,'Actual child PID')
        for channel in ['stdout','stderr']:exact_reference(cap[channel]);check(p.parent,[cap[channel]])
        require(regular(p.parent,'stderr.bin').read_bytes()==b'','Entire successful predecessor stderr')

def full_source_adversary_bindings(root,folder):
    refs=root['normalized_complete_external_input_bindings'];require(type(refs) is list and refs and all(type(z) is dict for z in refs),'Complete SOURCE individual external body bindings')
    seen=set()
    for z in refs:
        keyset(z,{'path','bytes','sha256','full_mode'},'Full SOURCE binding');check(R,[z]);require(type(z['full_mode']) is int and stat.S_IMODE(regular(R,z['path']).stat().st_mode)==z['full_mode'],'SOURCE input fullmode');require(z['path'] not in seen,'Duplicate SOURCE binding');seen.add(z['path'])
    captures=root['complete_actual_closing_and_postclosing_readback_captures'];require(type(captures) is list and len(captures)==2,'Actual SOURCE closer and separate readback')
    clocks=[]
    for row in captures:
        ref=row['capture'];exact_reference(ref);check(R,[ref]);p=R/ref['path'];cap=load(p);require(equal(cap,row['complete_capture']),'Entire actual SOURCE capture');required(cap,{'actual_execution':True,'completed':True,'exit_code':0,'stdin_supplied':False},'Actual SOURCE completed capture');require(type(cap['pid']) is int and cap['pid']>0,'Actual SOURCE PID');clocks.extend([utc_clock(cap['started_utc'],'SOURCE start'),utc_clock(cap['finished_utc'],'SOURCE finish')]);check(R,row['complete_members'])
        for channel in ['stdout','stderr']:exact_reference(cap[channel]);check(p.parent,[cap[channel]])
        require(regular(p.parent,'stderr.bin').read_bytes()==b'','Whole SOURCE stderr')
    require(clocks==sorted(clocks) and clocks[-1]<=utc_clock(root['utc'],'ROOT SOURCE read'),'SOURCE close/readback before ROOT read')
'''

basis=r'''def basis(root_bindings,root_bindings_sha256):
    approved,rp=root_binding_input(root_bindings,root_bindings_sha256);inputs=load(HERE/'INPUT_BINDINGS.json');refs=[]
    require(inputs['whole_binding_completed'] is True and inputs['actual_predecessor_PR46_completed'] is False,'SOURCE records completed WHOLE only, actual46 supplied later')
    for n in sorted(inputs['pins']):z={k:v for k,v in inputs['pins'][n].items() if k!='full_mode'};exact_reference(z);check(R,[z]);refs.append(z)
    frozen=manifest(C,'MANIFEST.json',CURRENT_SHA,1328,frozen=True);deps=load(C/'CURRENT_DEPENDENCIES.json');require(equal(deps,load(HERE/'EXPECTED_CURRENT_DEPENDENCIES.json')) and deps['anchor']=='repository_root' and len(rows(deps['files']))==1422 and sha((C/'CURRENT_DEPENDENCIES.json').read_bytes())==DEPS_SHA,'Entire1422 repository-root dependency metadata')
    # Frozen dated native4 are historical Git bodies. Stable9 are checked live;
    # actual acceptance requires the separate then-current ROOT13/main gate.
    historical={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
    for z in deps['files']:
        if z['path'] not in historical:check(R,[z])
    dated=load(A/'ROOT_CURRENT_INPUT_PREIMAGES.json');require(dated['current_head']==deps['current_main_head']=='e491808c3544ff44e8526d9b24857b5c9ca64208','Dated immutable epoch');native={z['path']:z for z in rows(dated['files'])};require(set(native)==NATIVE,'Exact dated13')
    for n in sorted(historical):
        entries=git_bytes('ls-tree','-z',dated['current_head'],'--',n).decode().split('\0');require(len(entries)==2 and entries[-1]=='','Exactly one dated Git native entry');fields,literal=entries[0].split('\t');mode,kind,blob=fields.split();require(mode=='100644' and kind=='blob' and literal==n,'Historical native100644');raw=git_bytes('show',dated['current_head']+':'+n);require(len(raw)==native[n]['bytes'] and sha(raw)==native[n]['sha256'],'Whole historical native4 body')
    source(C)
    for n in ADMIN:require(equal(load(C/n),load(HERE/'EXPECTED_CURRENT_ADMIN.json')),'Entire four operative corrected current administrative bodies')
    w=A/'current_whole_adversary_family';whole=load(w/'MANIFEST.json');require(equal(whole,load(HERE/'EXPECTED_WHOLE_MANIFEST.json')) and sha((w/'MANIFEST.json').read_bytes())==approved['whole_manifest']['sha256'],'Entire fixed WHOLE manifest');rr=rows(whole['files']);require(len(rr)==385 and whole['files_count']==385 and whole['self_excluded']==['MANIFEST.json'],'WHOLE385 self-only');check(w,rr);exact(w,{z['path'] for z in rr}|{'MANIFEST.json'});frozen_files(w,rr,'MANIFEST.json');require(sorted(topology(w)[1])==sorted(whole['directories']),'WHOLE84 complete directory topology')
    names=set()
    for z in inputs['external_input_rows']:
        keyset(z,{'path','bytes','sha256','full_mode'},'Individual excluded body binding');check(R,[z]);p=regular(R,z['path']);require(type(z['full_mode']) is int and stat.S_IMODE(p.stat().st_mode)==z['full_mode'],'Full excluded mode');require(z['path'] not in names,'No duplicate external member');names.add(z['path'])
    require(len(names)==2933 and len(inputs['external_input_rows'])==inputs['external_input_count']==2933 and not names.intersection(historical),'All2933 fixed excluded inputs; never future live native4')
    verdict=load(w/'VERDICT.json');root=load(A/'ROOT_WHOLE_CURRENT_REVIEW.json');require(equal(verdict,load(HERE/'EXPECTED_WHOLE_VERDICT.json')) and equal(root,load(HERE/'EXPECTED_ROOT_WHOLE_REVIEW.json')) and equal(root['complete_VERDICT_object'],verdict),'Entire known typed WHOLE and ROOT bodies')
    required(verdict,{'verdict':WHOLE_VERDICT,'mandatory_corrections':[],'status':'unsolved','original_substantive_attempts':1,'new_substantive_attempts':0,'audit_turns':0,'future_acceptance_approved':False},'Scoped WHOLE partial')
    required(root,{'schema':'pr47-root-complete-closed-whole-inspection/v1','status':'PASS_ROOT_COMPLETE_CLOSED_WHOLE_INSPECTION','actual_readback_pid':89547,'candidate_manifest_sha256':CURRENT_SHA,'first_party_members':385,'individually_bound_foreign_inputs':2933,'personal_report_and_verdict_fully_read':True,'all_first_party_whole_bytes_and_modes_checked':True,'all_external_individual_whole_bytes_checked':True,'exact_self_only_recursive_closure_checked':True,'ROOT_actual_inner49_complete_read':True,'frozen_inner47_honest_prefix':True,'future_execution_approved':False,'future_acceptance_approved':False,'mandatory_defects':[],'mandatory_corrections':[],'full_target_resolved':False,'realized_example_Isharp_rank_computed':False},'Entire genuine ROOT WHOLE meaning')
    ledger=load(A/'ROOT_PRIMARY_READ_LEDGER.json');card=load(A/'ROOT_SCIENCE_CARD.json');require(equal(ledger,load(HERE/'EXPECTED_PRIMARY_READ_LEDGER.json')) and equal(card,load(HERE/'EXPECTED_SCIENCE_CARD.json')) and ledger['reading_completed'] is True and card['reading_completed'] is True and equal(ledger['root_flags'],card['root_flags']) and len(ledger['root_flags'])==10 and all(v is True for v in ledger['root_flags'].values()),'Ten complete scientific/source ROOT flags')
    literal_original_captures()
    refs+=[pin(C/'MANIFEST.json'),pin(C/'CURRENT_DEPENDENCIES.json'),pin(w/'MANIFEST.json'),pin(w/'AUDIT.md'),pin(w/'VERDICT.json'),pin(A/'ROOT_WHOLE_CURRENT_REVIEW.json'),pin(rp)]+[approved[k] for k in ['previous_mirror','previous_post','previous_root_post','previous_post_contract','acceptance_source_manifest','acceptance_source_verdict','root_source_inspection','root_capture_operator']]
    out={}
    for z in refs:require(z['path'] not in out or equal(out[z['path']],z),'Conflicting immutable identity');out[z['path']]=z
    return frozen,sorted(out.values(),key=lambda z:z['path'])

def literal_original_captures():
    result=load(A/'root_original_actual_reproduction/ROOT_REPRODUCTION_RESULT.json');require(equal(result,load(HERE/'EXPECTED_ORIGINAL_CAPTURE_RESULT.json')),'Whole historical original reproduction body')
    helpers=result['complete_actual_helper_captures'];queries=result['complete_actual_Git_captures'];require(len(helpers)==3 and len(queries)==33,'Three typed helpers,33 genuine null Git queries')
    keys={'schema','argv','cwd','started_utc','actual_operator_pid','stdin_supplied','source','actual_execution','pid','completed','exit_code','finished_utc','stdout','stderr','source_unchanged'}
    originals=load(A/'snapshot_manifest.json')['files'];expected=[]
    for i,z in enumerate(originals):expected.extend([['git','show',HEAD+':'+z['path']],['git','ls-tree',HEAD,'--',z['path']]])
    expected.append(['git','diff',ORIGINAL_BASE,HEAD])
    require(equal([z['argv'] for z in queries],expected),'Complete literal33 Git argv whitelist, source:null/unchanged:null')
    for z in helpers+queries:
        keyset(z,keys,'Literal actual reproduction schema');required(z,{'schema':'pr47-root-literal-operation-capture/v1','cwd':str(R),'actual_operator_pid':22446,'stdin_supplied':False,'actual_execution':True,'completed':True,'exit_code':0},'Actual complete original capture');require(type(z['pid']) is int and z['pid']>0,'Actual typed PID');require(utc_clock(z['started_utc'],'Original start')<=utc_clock(z['finished_utc'],'Original finish'),'Original clock')
        for ch in ['stdout','stderr']:exact_reference(z[ch]);check(R,[z[ch]])
        require(regular(R,z['stderr']['path']).read_bytes()==b'','Full original stderr')
    for z in queries:require(z['source'] is None and z['source_unchanged'] is None,'Genuine Git requires both null, no helper substitution')
    paths=['author/verify.py','submitted_copy/submitted_verify.py','historical_independent/independent_checks.py']
    for z,n in zip(helpers,paths):
        exact_reference(z['source']);check(R,[z['source']]);require(z['source_unchanged'] is True and equal(z['argv'],['/usr/bin/python3','-B',str(A/'root_original_actual_reproduction'/n)]),'Literal typed helper argv and source')
'''

source=r'''def source(base):
    original_native(base/'original_archive')
    for n in IMMUTABLE:require(regular(base,n).read_bytes()==regular(A/'source_snapshot',n).read_bytes(),'Literal operative immutable10 changed')
    for n in ['OBSTRUCTION.md','REALIZED_DEGENERACY_PROOF.md','SOURCE_PRECISION_QUALIFICATIONS.md','SOURCE_PROVENANCE_CORRECTION.md']:
        require(sha(regular(base,n).read_bytes())==load(HERE/'SCIENTIFIC_SCOPE.json')['operative_artifact_sha256'][n],'Entire globally qualified corrected source changed')
    require(sha(regular(base,'OBSTRUCTION.md').read_bytes())==SCIENCE_SHA and sha(regular(base,'source_record.json').read_bytes())==SOURCE_SHA,'Corrected science and literal source anchors')
    raw=regular(base,'turns.json').read_bytes();require(raw==regular(A/'source_snapshot','turns.json').read_bytes() and sha(raw)==LEDGER_SHA,'Entire original one-turn object ledger');ledger=parse(raw);require(equal(ledger,load(HERE/'EXPECTED_ORIGINAL_LEDGER.json')),'Whole typed original ledger');required(ledger,{'id':2849,'count':1},'Original one genuine substantive turn');require(type(ledger['attempts']) is list and len(ledger['attempts'])==1 and type(ledger['attempts'][0]['number']) is int and ledger['attempts'][0]['number']==1,'Original1/5 object, not JSONL or review attempts');require(regular(base,'prior_report.json').read_bytes()==b'null\n','Original literal null does not itself infer raw-source absence')
'''

owned=r'''PROGRAM_LOG=B/'RESEARCH_LOG.md'
ADDITIONAL_OWNED_MUTATION_PATHS={PROGRAM_LOG.relative_to(R).as_posix()}
OWNED_OPERATIONAL_LOGS=[('root_problem',A/'ROOT_RESEARCH_LOG.md'),('program',PROGRAM_LOG)]

def owned_mutation_path(name):
    relative(name)
    return name in NATIVE or name in ADDITIONAL_OWNED_MUTATION_PATHS or name.startswith(K.relative_to(R).as_posix()+'/') or name.startswith(A.relative_to(R).as_posix()+'/')

def protected_foreign_paths(fresh):
    paths=fresh['protected_foreign_tracked_paths'];require(type(paths) is list and all(type(n) is str for n in paths) and paths==sorted(set(paths)),'Exact sorted foreign identities')
    for name in paths:require(not owned_mutation_path(name),'Owned mutation path may never be declared protected foreign: '+name)
    return paths

def operational_log_note(clock):
    utc_clock(clock,'Actual finalization log clock')
    return '\n## '+clock+' — PR47 actual accepted corrected UNSOLVED partial\n\nWorkflow100%; scientific discovery0%; original1/5,new0,audit0. Known realized degeneracy credited; actual degenerate Floer contribution/differential remains unresolved. Actual MERGED original-head/tree checked. Program37/180=20.555555555555557%; one present native mirror remains. Extensive AI use; unrefereed; no paper/newDOI/tracker/release.\n'

def owned_log_append_check(pre):
    foreign_check(pre);record=load(A/'integration_log_append_receipt.json');keyset(record,{'schema','utc','logs','note','source_preparation_did_not_append'},'Exact owned append receipt');required(record,{'schema':'pr47-owned-operational-log-appends/v1','source_preparation_did_not_append':True},'Actual append, not preparation mutation');final=load(A/'integration_finalization.json');note=operational_log_note(final['utc']);require(record['note']==note and type(record['logs']) is list and len(record['logs'])==2,'Only two authorized exact prefix appends')
    require(utc_clock(final['utc'],'Finalization')<=utc_clock(record['utc'],'Append')<=dt.datetime.now(dt.timezone.utc),'Append actual clock')
    for row,(label,path) in zip(record['logs'],OWNED_OPERATIONAL_LOGS):
        keyset(row,{'log','before','retained_preimage','after','before_worktree_mode','after_worktree_mode'},'Complete owned log identity and full modes')
        name=path.relative_to(R).as_posix();require(row['log']==name and row['before']['path']==name and row['after']['path']==name,'Exact authorized program/A47 log only')
        for k in ['before','retained_preimage','after']:exact_reference(row[k])
        retained=A/'integration_log_preimages'/(label+'.bin');require(row['retained_preimage']['path']==retained.relative_to(R).as_posix(),'Exact retained full prefix path');check(R,[row['retained_preimage'],row['after']]);prefix=regular(R,row['retained_preimage']['path']).read_bytes();require(len(prefix)==row['before']['bytes'] and sha(prefix)==row['before']['sha256'] and regular(R,name).read_bytes()==prefix+note.encode(),'Exact retained prefix plus fixed append, no rewrite')
        before=row['before_worktree_mode'];after=row['after_worktree_mode'];require(type(before) is int and type(after) is int and 0<=before<=0o7777 and before==after==stat.S_IMODE(regular(R,name).stat().st_mode),'Authorized full mode preserved')
    return record
'''

def main():
    inspected=load(F/'COMPLETE_INPUT_INSPECTION.json')
    if inspected['current_payload']!=1328 or inspected['whole_payload']!=385 or inspected['actual_PR46_predecessor_completed'] is not False:raise ValueError('Actual inspection required')
    science={'schema':'pr47-proposed-accepted-scientific-scope/v1','id':'2849','problem_id':2849,'problem_number':'KP-3.51','literal_target':'Every closed connected oriented SU(2)-abelian rational homology three-sphere Y has dim_C I#(Y)=|H1(Y)|.','literal_target_status':'unsolved','strongest_verified_partial':'Conditional reducible-count route; unrealized quartic local-homology obstruction; auxiliary trefoil-surgery checks; complete credited known realized SU(2)-abelian Seifert degeneracy.','exact_remaining_gaps':['Actual degenerate reducible Floer contribution/differential control or another sufficient mechanism.'],'original16_and_operative_immutable10_unchanged':True,'universal_normal_vanishing_false':True,'known_realized_degeneracy_credited_to_Sivek_Zentner':True,'realized_example_instanton_rank_computed':False,'counterexample_to_full_target_claimed':False,'quartic_model_realized_as_Chern_Simons':False,'trefoil_auxiliary_version_scope_only':True,'imported_gauge_theorem_conditional':True,'source_access_limits_preserved':True,'literal_null_not_raw_absence_authority':True,'full_problem_solved':False,'full_problem_solved_by_project':False,'full_target_resolved_in_prior_published_literature':False,'partial_valid':True,'novelty_claimed':False,'priority_claimed':False,'prior_publication_doi':None,'original_substantive_attempts':1,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'verification_attempts_added':0,'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'paper_or_new_doi_or_tracker':False,'human_referee_review_claimed':False,'AI_tools_used_extensively':True,'human_peer_review':False,'formal_certification':False,'historical_metadata_archival_only':True,'global_qualification_path':'SOURCE_PRECISION_QUALIFICATIONS.md','global_qualification_sha256':sha(read(C/'SOURCE_PRECISION_QUALIFICATIONS.md')),'operative_artifact_sha256':{n:sha(read(C/n)) for n in ['OBSTRUCTION.md','REALIZED_DEGENERACY_PROOF.md','SOURCE_PRECISION_QUALIFICATIONS.md','SOURCE_PROVENANCE_CORRECTION.md']}}
    dump('SCIENTIFIC_SCOPE.json',science)
    inputs=load(F/'INPUT_BINDINGS.json');rootdraft=transform((T/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json').read_text());obj=json.loads(rootdraft);obj.pop('root_actual_PR44_predecessor_read_completed');obj['root_actual_PR46_predecessor_read_completed']=False;obj['previous_post_contract']=None;dump('DRAFT_ROOT_IMMUTABLE_BINDINGS.json',obj)
    plan=json.loads(transform((T/'DRAFT_FINAL_PLAN.json').read_text()));plan.pop('root_actual_PR44_predecessor_read_completed');plan.update(root_actual_PR46_predecessor_read_completed=False,original_head='487327b2412c436ae69e8c52bf353a9a1fb7594e',original_base='c6975ca76f9f667f1250ba403d0e6da2aafe14d0',original_github_base='c6975ca76f9f667f1250ba403d0e6da2aafe14d0',reviewed_candidate_manifest_sha256=inputs['pins'][str((C/'MANIFEST.json').relative_to(R))]['sha256'],current_dependencies_sha256=inputs['pins'][str((C/'CURRENT_DEPENDENCIES.json').relative_to(R))]['sha256'],scientific_scope=science);dump('DRAFT_FINAL_PLAN.json',plan)
    g=transform((T/'pr45_guards.py').read_text());g=g.replace("ID, CODE, PR = '2849', 'KP-3.51', 45","ID, CODE, PR = '2849', 'KP-3.51', 47")
    constants={'HEAD':'487327b2412c436ae69e8c52bf353a9a1fb7594e','ORIGINAL_BASE':'c6975ca76f9f667f1250ba403d0e6da2aafe14d0','CURRENT_SHA':sha(read(C/'MANIFEST.json')),'DEPS_SHA':sha(read(C/'CURRENT_DEPENDENCIES.json')),'SOURCE_SHA':sha(read(C/'source_record.json')),'LEDGER_SHA':sha(read(C/'turns.json')),'SCIENCE_SHA':sha(read(C/'OBSTRUCTION.md')),'WHOLE_VERDICT':'PASS_EXACT_CURRENT_CORRECTED_UNRESOLVED_PARTIAL_NO_MANDATORY_CORRECTION'}
    for name,val in constants.items():g=re.sub(r'(?m)^'+name+r' = .*$',name+' = '+repr(val),g)
    g=re.sub(r'(?m)^ADMIN = .*$',"ADMIN = {'status.json','readiness.json','review/verdict.json','review/review_summary.json'}",g)
    immutable=['verify.py','verification.json','source_checksums.json','source_record.json','turns.json','prior_report.json','review/independent_checks.py','review/independent_results.json','review/submitted_verify.py','review/submitted_results.json'];g=re.sub(r'(?m)^IMMUTABLE = .*$','IMMUTABLE = '+repr(set(immutable)),g)
    g=replace_function(g,'root_binding_input',rootbinding);g=replace_function(g,'basis',basis);g=replace_function(g,'source',source)
    g=g.replace("len(snapshot['files'])==18","len(snapshot['files'])==16").replace('original18','original16').replace('Original18','Original16')
    g=g.replace("'original_substantive_attempts','new_substantive_attempts','audit_turns','full_permission_mode'","'original_substantive_attempts','new_substantive_attempts','audit_turns','full_permission_mode','directories'")
    # Historical files are byte-bound archival records; only operative JSON is parsed
    # through the separately exact known objects. Never reinterpret empty/failed captures.
    start=g.index('    for z in rr:\n        if z[\'path\'].endswith(\'.json\'):');end=g.index('    if frozen:frozen_files',start);g=g[:start]+g[end:]
    g=g.replace('root_actual_PR44_predecessor_read_completed=True','root_actual_PR46_predecessor_read_completed=True').replace('actual44 predecessor','actual46 predecessor').replace('Actual44 predecessor','Actual46 predecessor')
    g=g.replace("raw)==183402","raw)==59460").replace('==183402','==59460').replace('==19,\'Original19 changed paths\'','==17,\'Original17 changed paths\'').replace('Entire original19-path diff','Entire original17-path diff')
    g=g.replace('completed_count=35','completed_count=37').replace('35/180*100','37/180*100').replace("before['completed_count']==34","before['completed_count']==36").replace("for z in before['items'])==34","for z in before['items'])==36")
    g=g.replace("for n in paths:\n        relative(n);require(n not in NATIVE and not n.startswith(K.relative_to(R).as_posix()+'/') and not n.startswith(A.relative_to(R).as_posix()+'/'),'Protected foreign path outside all owned/native scope required')","protected_foreign_paths(fresh)")
    g=g.replace("fresh=load(R/pre['fresh_preimage']);paths=fresh['protected_foreign_tracked_paths'];rr=pre['foreign_logs']","fresh=load(R/pre['fresh_preimage']);paths=protected_foreign_paths(fresh);rr=pre['foreign_logs']")
    g=g.replace("    for n in foreign_paths:\n        relative(n);require(n not in NATIVE and not n.startswith(K.relative_to(R).as_posix()+'/') and not n.startswith(A.relative_to(R).as_posix()+'/'),'Foreign exception outside exact owned/native scope')","    protected_foreign_paths(fresh)")
    g+='\n\n'+owned
    output('pr47_guards.py',g)
    integrate=transform((T/'integrate_reviewed_partial.py').read_text());integrate=re.sub(r'(?m)^BODY = .*$',lambda m:'BODY = '+repr(BODY),integrate);integrate=re.sub(r'(?m)^PRESENT_SCOPE = .*$',lambda m:'PRESENT_SCOPE = '+repr(PRESENT_SCOPE),integrate)
    integrate=re.sub(r"(?m)^    cells\[8\]=' unsolved '; cells\[9\]=' 1/5 '; cells\[11\]=.*$",lambda m:"    cells[8]=' unsolved '; cells[9]=' 1/5 '; cells[11]="+repr(' Corrected conditional reducible Floer route; known realized SU(2)-abelian degeneracy credited to Sivek-Zentner; no instanton rank or full-target counterexample claimed. Actual degenerate Floer contribution/differential control remains unresolved. [Accepted corrected UNSOLVED partial](attempts/2849/ACCEPTANCE.md). Original1/5,new0,audit0; extensive AI use, unrefereed; no novelty/priority/paper/new DOI/tracker. '),integrate)
    integrate=integrate.replace("# Accepted unsolved corrected reducible Floer obstruction and known realized degeneracy: 2849 / KP-3.51","# Accepted corrected unsolved Floer partial: 2849 / KP-3.51").replace('source, present raw prior and matching upstream dictionary remain unchanged.','literal null, raw-source absence qualification and corrected global provenance remain unchanged.')
    start=integrate.index("    note='\\n## '");end=integrate.index("    print('FINALIZE",start)
    integrate=integrate[:start]+r'''    g.foreign_check(pre);note=g.operational_log_note(now)
    logdir=g.A/'integration_log_preimages';g.require(not logdir.exists() and not logdir.is_symlink(),'Absent retained log-prefix directory');logdir.mkdir()
    log_receipt=[]
    for name,f in g.OWNED_OPERATIONAL_LOGS:
        f=g.regular(g.R,f.relative_to(g.R).as_posix());previous=f.read_bytes();before_pin=g.pin(f);before_mode=g.stat.S_IMODE(f.stat().st_mode)
        g.write(logdir/(name+'.bin'),previous,exclusive=True);g.require(f.read_bytes()==previous and g.stat.S_IMODE(f.stat().st_mode)==before_mode,'Exact owned log prefix/mode immediately before append')
        g.write(f,previous+note.encode());f.chmod(before_mode)
        log_receipt.append({'log':f.relative_to(g.R).as_posix(),'before':before_pin,'retained_preimage':g.pin(logdir/(name+'.bin')),'after':g.pin(f),'before_worktree_mode':before_mode,'after_worktree_mode':g.stat.S_IMODE(f.stat().st_mode)})
    g.dump(g.A/'integration_log_append_receipt.json',{'schema':'pr47-owned-operational-log-appends/v1','utc':g.stamp(),'logs':log_receipt,'note':note,'source_preparation_did_not_append':True},exclusive=True);g.owned_log_append_check(pre)
'''+integrate[end:]
    output('integrate_reviewed_partial.py',integrate)
    mirror=transform((T/'state_mirror_reconciliation.py').read_text());mirror=mirror.replace('    return pre,canonical','    g.owned_log_append_check(pre)\n    return pre,canonical');output('state_mirror_reconciliation.py',mirror)
    post=transform((T/'verify_post_acceptance.py').read_text());post=post.replace("    final,remote=g.finalization(pins,pre);inventory", "    g.owned_log_append_check(pre)\n    final,remote=g.finalization(pins,pre);inventory").replace("'fresh_native_mirror_noop':True","'fresh_native_mirror_noop':True,'owned_operational_log_appends_exact':True,'protected_foreign_paths_exclude_owned_program_log':True");output('verify_post_acceptance.py',post)
    output('seal_final_evidence.py',transform((T/'seal_final_evidence.py').read_text()))
    operator=transform((T/'capture_root_final_operation.py').read_text());operator=operator.replace("assert script.parent in (A, A / 'acceptance_preparation_family')","assert script.parent == A / 'acceptance_preparation_family' and script.name == 'seal_final_evidence.py'")
    output('capture_root_final_operation.py',operator)
    contract=load(T/'ROOT_POST_CONTRACT.json');contract=json.loads(transform(json.dumps(contract)))
    for key in list(contract):
        if key.startswith('future45_'):contract[key.replace('future45_','future47_')]=contract.pop(key)
    contract['future47_required_ROOT_schema']='pr47-root-complete-actual-post-inspection/v1'
    keys=contract['future47_required_ROOT_complete_keyset'];keys=[k.replace('all35_prior','all37_prior').replace('canonical507_plus','canonical1340_plus').replace('merge505_overlay','merge1338_overlay') for k in keys];keys+=['owned_operational_log_appends_exact','protected_foreign_paths_exclude_owned_program_log'];contract['future47_required_ROOT_complete_keyset']=keys
    vals=contract['future47_required_completed_values'];vals={k.replace('all35_prior','all37_prior').replace('canonical507_plus','canonical1340_plus').replace('merge505_overlay','merge1338_overlay'):v for k,v in vals.items()};vals.update(completed_primary_prs=37,program_completion_percent=37/180*100,owned_operational_log_appends_exact=True,protected_foreign_paths_exclude_owned_program_log=True);contract['future47_required_completed_values']=vals
    vals=contract['future47_required_entire_post_values'];vals.pop('exact_original18_and_OBSTRUCTION_unchanged',None);vals.update(exact_original16_and_corrected_OBSTRUCTION_unchanged=True,targets=38,consumed_substantive_turns=45,primary_acceptances=37,program_completed_count=37,program_completion_estimate_percent=37/180*100,owned_operational_log_appends_exact=True,protected_foreign_paths_exclude_owned_program_log=True);contract['future47_required_entire_post_values']=vals
    contract['predecessor']={'pr':46,'actually_completed':False,'mirror':None,'post':None,'ROOT_post':None,'ROOT_post_contract':None,'targets':37,'consumed_substantive_turns':44,'primary_acceptances':36,'duplicate_mirrors':1,'inventory_completed':36,'inventory_total':180};contract['future_ROOT_post_completed']=False
    contract['future47_required_complete_inspections']=[
      'Every37 prior state object and complete history prefix is retained with exact recursive scalar types. One selected2849 ordinary unsolved1/5 primary event gives38targets45turns37primary1duplicate; no new author or audit turn.',
      'Actual46 must have completed before47: genuine completed36primary/37target/44turn mirror and post, exact entire ROOT post against its closed source contract, actual predecessor captures; pending46/source readiness does not confer authority.',
      'All180 inventory entries are independently reconstructed from actual preflight. Exactly37 complete primaries, next48, 37/180=20.555555555555557%; every179 other entry and every nondeclared top-level value remains typed-identical.',
      'Original487327b2412c436ae69e8c52bf353a9a1fb7594e is exact second parent; actual fresh main preflight is exact first parent. No rebase, force push, blanket staging or invented merge receipt.',
      'Merge1338-file full canonical overlay and whole queue are exact100644 Git bodies; actual accepted closure1340 payload plus self has exact topology and full0444. Original16 archive, operative immutable10, and entire corrected global mathematics/provenance remain exact.',
      'Entire current1328, full1422 dependency metadata and new WHOLE385/all2933 external body bindings, genuine ROOT89547 and complete actual86916/87026/53866/53867/final49/prefix47 are bound. Dated native4 are read from immutable historical Git epoch, never future live authorization.',
      'Fresh native13 fullbytes/fullmodes/main and all ROOT declared foreign tracked paths fullbytes/modes/HEAD/index are checked before mutation and through every phase. Exact program RESEARCH_LOG is excluded from protected foreign before irreversible operations; no broad program-prefix exemption.',
      'Only exact A47 ROOT_RESEARCH_LOG and exact program RESEARCH_LOG receive two authorized full retained prefixes plus the fixed finalization note; exact path/length/hash/fullmode evidence, fresh foreign check, and full equality repeat at finalize, mirror and post. Logs are excluded from merge staging.',
      'Every actual preflight/overlay/prepush/finalize/mirror/post capture, final sealer and ROOT ready/body/merge/commit/push records is read completely with actual child/operator PIDs, exact argv/cwd/UTC/prelaunch source/operator/full stdout and stderr; retain failures, never infer execution from drafted source.',
      'Entire saved mirror proposal and plan are independently reconstructed at original timestamp from actual full state/history, exact prior ledgers/budgets and duplicate accounting. Final fresh native replay is byte-preserving no-op with no writes.',
      'Full target remains unresolved; credited known Seifert degeneracy has no computed instanton rank or counterexample; quartic is unrealized, trefoil auxiliary version scope and conditional gauge theorem are retained globally. Extensive AI, unrefereed, no novelty/priority/full solution/paper/new DOI/tracker/release or human peer review.',
      'ROOT complete keyset has22 exact keys, entire_post typed-identical to real verifier output, all flags evidence-bound; no future timestamps/PIDs/approval or abbreviated counter receipts.']
    dump('ROOT_POST_CONTRACT.json',contract)
    for n in ['DRAFT_ROOT_PRIMARY_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json','DRAFT_ROOT_SCOPE_CERTIFICATE.json']:
        dump(n,{'schema':'pr47-pending-root-acceptance-record/v1','status':'PENDING_ROOT_PERSONAL_READING','root_completed':False,'created_utc':None,'actual_pid':None,'preparation_manifest_sha256':None,'entire_known_scientific_scope':science,'actual_PR46_predecessor_completed':False,'future_execution_approved':False,'future_acceptance_approved':False,'paper_or_new_doi_or_tracker':False,'original_substantive_attempts':1,'new_substantive_attempts':0,'audit_turns':0})
    dump('EXPECTED_NATIVE_TRANSITION.json',{'schema':'pr47-source-proposed-native-transition/v1','before':{'targets':37,'turns':44,'primary':36,'duplicate':1,'inventory_complete':36},'after':{'targets':38,'turns':45,'primary':37,'duplicate':1,'inventory_complete':37},'inventory_total':180,'program_percent':37/180*100,'new_scientific_targets':1,'new_original_turns':1,'new_author_attempts':0,'audit_turns':0,'selected_original_attempts':'1/5','status':'unsolved','actual46_predecessor_pending':True,'live_execution':False})
    sourcepins={n:sha(read(F/n)) for n in ['pr47_guards.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','seal_final_evidence.py','capture_root_final_operation.py']}
    dump('AUTHORING_RESULT.json',{'schema':'pr47-acceptance-source-textual-authoring/v1','actual_pid':os.getpid(),'derived_completed_pattern':'PR45','unfinished46_design_reference_only':'exact program-log exclusion + two verified prefix/append/fullmode receipts','source_sha256':sourcepins,'production_imported_compiled_executed':False,'native_index_remote_mutated':False,'actual46_predecessor_completed':False,'future_acceptance_approved':False});print(json.dumps({'status':'TEXT_SOURCE_PREPARED','actual_pid':os.getpid(),'source_sha256':sourcepins,'production_imported_compiled_executed':False},sort_keys=True))
def repair_v2():
    names=['pr47_guards.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','seal_final_evidence.py','capture_root_final_operation.py','ROOT_POST_CONTRACT.json','AUTHORING_RESULT.json','INPUT_BINDINGS.json']
    history=F/'source_history/v1';history.mkdir(parents=True,exist_ok=False)
    for n in names:(history/n).write_bytes(read(F/n))
    g=(F/'pr47_guards.py').read_text();g=g.replace('identities.count(45)==1','identities.count(47)==1')
    for x in ['ROOT_complete_keyset','ROOT_schema','completed_values','entire_post_values']:g=g.replace("contract['future46_required_"+x+"']","contract['required_"+x+"']")
    entry="        'pr46-acceptance-source-closure/v1':{'schema','status','utc','self_excluded','files_count','files','source_only','proposed_helpers_imported_compiled_executed','future_acceptance_or_ROOT_approval_claimed'},\n"
    g=g.replace('    known={\n','    known={\n'+entry).replace("if obj['schema']=='pr47-acceptance-source-closure/v1':","if obj['schema'] in {'pr47-acceptance-source-closure/v1','pr46-acceptance-source-closure/v1'}:")
    g=g.replace("expected.append(['git','diff',ORIGINAL_BASE,HEAD])","expected.append(['git','diff','--no-ext-diff','--no-textconv','--binary',ORIGINAL_BASE,HEAD,'--'])")
    g=g.replace('Actual34 prior primaries','Actual36 prior primaries').replace('Exactly35 derived primary completions','Exactly37 derived primary completions')
    (F/'pr47_guards.py').write_text(g)
    for n in ['integrate_reviewed_partial.py','state_mirror_reconciliation.py']:
        text=(F/n).read_text().replace('postPR44 native35targets/43turns','postPR46 native37targets/44turns').replace('Require33 complete primaries before44','Require36 complete primaries after46').replace('Exactly35 primary completions','Exactly37 primary completions').replace('Require35targets/43turns','Require37targets/44turns').replace('Exactly36targets/44turns/35primary','Exactly38targets/45turns/37primary')
        (F/n).write_text(text)
    contract=load(F/'ROOT_POST_CONTRACT.json');body=json.dumps(contract).replace('canonical1340_plus_manifest','canonical1339_plus_manifest').replace('merge1338_overlay','merge1337_overlay').replace('Merge1338-file','Merge1337-file').replace('closure1340 payload','closure1339 payload');contract=json.loads(body);contract['future47_required_entire_post_values']['pr']=47;dump_path=F/'ROOT_POST_CONTRACT.json';dump_path.write_text(json.dumps(contract,sort_keys=True,indent=2)+'\n')
    inputs=load(F/'INPUT_BINDINGS.json')
    for n in ['pr45_guards.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','seal_final_evidence.py','capture_root_final_operation.py','CONTRACT.md','ROOT_POST_CONTRACT.json','PREPARATION_MANIFEST.json']:
        p=T/n;b=read(p);row={'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b),'full_mode':os.stat(p).st_mode&0o7777};inputs['pins'][row['path']]=row
    # Only the exact narrow owned-log patch is an unfinished design reference.
    p=B/'audits/pr46_30004438/acceptance_preparation_family_v2/S1_SCOPED_OWNERSHIP_REPAIR.patch';b=read(p);row={'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b),'full_mode':os.stat(p).st_mode&0o7777};inputs['unfinished_design_reference']=row
    (F/'INPUT_BINDINGS.json').write_text(json.dumps(inputs,sort_keys=True,indent=2)+'\n')
    sourcepins={n:sha(read(F/n)) for n in names[:6]}
    dump('TEXTUAL_REPAIR_V2_RESULT.json',{'schema':'pr47-acceptance-preparation-textual-repair/v2','actual_pid':os.getpid(),'preserved_initial_source':names,'source_sha256':sourcepins,'corrections':['selected inventory identity47','actual predecessor46 contract field names and known closure class','complete original33Git literal binary diff argv','set-derived1337overlay1339accepted payload and selected47post','stale numerical diagnostic prose'],'production_imported_compiled_executed':False,'future_actual46_predecessor_completed':False,'future_acceptance_approved':False});print(json.dumps({'status':'TEXTUAL_REPAIR_V2_COMPLETE','actual_pid':os.getpid(),'source_sha256':sourcepins,'production_imported_compiled_executed':False},sort_keys=True))
if __name__=='__main__':
    if (F/'AUTHORING_RESULT.json').exists():repair_v2()
    else:main()
