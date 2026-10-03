#!/usr/bin/env python3
"""Own source author only: no prepared-helper imports or executions."""
import ast
import datetime as dt
import hashlib
import json
from pathlib import Path
P=Path(__file__).resolve().parent
A=P.parent
R=A.parents[2]
T=R/'draft_pr_publication_program_20260930/audits/pr40_2814/acceptance_execution_preparation_family/integration_source_revision_v2'
def sha(b):return hashlib.sha256(b).hexdigest()
def encode(o):return (json.dumps(o,indent=2,ensure_ascii=False)+'\n').encode()
def put(n,b):
 p=P/n;assert not p.exists();p.write_bytes(b.encode() if isinstance(b,str) else encode(b))
original={n:(T/n).read_bytes() for n in ['pr40_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py']}
put('ADAPTATION_SOURCE_PINS.json',{'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'scope':'Read-only source adaptation; no adapted helper imported/executed','files':[{'path':(T/n).relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)} for n,b in original.items()]})
g=original['pr40_guards.py'].decode().replace('pr40','pr41').replace('PR40','PR41')
g=g.replace('import json\n','import json\nimport math\n').replace('A = HERE.parents[1]','A = HERE.parent')
g=g.replace("ID, CODE, PR = '2814', 'KP-3.16', 40","ID, CODE, PR = '9700035', 'AMR-096-0035', 41")
g=g.replace("K = R / 'unsolved_math_prioritization/attempts/2814'","K = R / 'unsolved_math_prioritization/attempts/9700035'")
g=g.replace('163e34d566d6cbaee3a2a8fdc6394fbb9e49a539','292b95ca601f166e6d246e609cf7ed5ca5653e25')
g=g.replace('8de92d903edaec7471f4ecc3df443b7e779732b0ee83cdec507c22025bfae25f','3431ca2dfb332500f3815ea1e61f089744b3bacd9c3659018537016b9396fbfa')
g=g.replace('b2c6d31f3e7230e132761322bef9d3b99e1b0f53521fbefc5a281e6682199a37','ade2f6fe9890f1038810158a284f4a8924e34d6d2f95b3a07654d78fa6501ff6')
g=g.replace("WHOLE_SHA = '90fbc21a211e29a3ba7a385c68479ff5effd864af6247f224d0b7843a447dabc'\n",'')
g=g.replace('63363142a7a478b9e57692b0136a601934d1a9fb5b5aae63e6ffb8dd87add60c','d86ee1dc749ef5b9a0446109fb6f0278246cf3584f36aa70205b5bc6c683782f')
g=g.replace('3d74f9a6f0185e200349b2f303468d1c97fd7379dd470ea12dfca22585745a62','bd0a82165c3ac81f7a7d35ace164f20ecb87e6b73a9155815e4eecac655a2549')
g=g.replace('c232697fb80c20a88efe7db12390d9bda2d7f5c2fdc96e5cfad3a98a8cfdf16c','464af6d259f9275ca9f0056567f5301bc228465fa0ddaf2faece0920cab6bd7c')
g=g.replace("ADMIN = {'acceptance.json', 'status.json', 'attempt.json', 'current_readiness.json'}","ADMIN = {'status.json', 'attempt.json', 'readiness.json', 'review/verdict.json'}\nIMMUTABLE = {'PROOF.md','verify.py','verification.json','source_record.json','prior_report.json','source_provenance.json','turns.json','review/independent_checks.py','review/independent_results.json','review/review_summary.json'}\nWHOLE_VERDICT = 'PASS_QUALIFIED_UNSOLVED_PARTIAL_NEW_WHOLE_CURRENT'")
g=g.replace("'source_hold': True, 'original_substantive_attempts': 0","'original_substantive_attempts': 2")
g=g.replace("    return json.loads(data, object_pairs_hook=pairs, parse_constant=lambda v: (_ for _ in ()).throw(ValueError('Nonfinite JSON: '+v)))","    def floating(v):\n        n=float(v); require(math.isfinite(n),'Nonfinite decoded JSON number'); return n\n    return json.loads(data, object_pairs_hook=pairs, parse_float=floating, parse_constant=lambda v: (_ for _ in ()).throw(ValueError('Nonfinite JSON: '+v)))")
g=g.replace("not p.is_absolute() and '..' not in p.parts and p.as_posix() == n","not p.is_absolute() and not {'.','..','.git','__pycache__'}.intersection(p.parts) and p.as_posix() == n")
g=g.replace("'number':40,'url':'https://github.com/AlecKriebel/Math/pull/40'","'number':41,'url':'https://github.com/AlecKriebel/Math/pull/41'")
start=g.index('def source(base):');end=g.index('\ndef utc_clock(',start)
g=g[:start]+'''def original_native(base):
    snapshot=load(A/'snapshot_manifest.json')
    require(len(snapshot['files'])==16,'Complete original16 required')
    exact(base,{z['path'] for z in rows(snapshot['files'])})
    for z in rows(snapshot['files']):
        raw=regular(base,z['path']).read_bytes()
        require(raw==regular(A/'source_snapshot',z['path']).read_bytes() and len(raw)==z['bytes'] and sha(raw)==z['sha256'],'Original16 bytes differ')


def source(base):
    original_native(base/'original_archive')
    for n in IMMUTABLE:
        require(regular(base,n).read_bytes()==regular(A/'source_snapshot',n).read_bytes(),'Immutable current math/code/full saved object/source/prior/ledger changed')
    require(sha(regular(base,'PROOF.md').read_bytes())==SCIENCE_SHA and sha(regular(base,'source_record.json').read_bytes())==SOURCE_SHA,'Scientific/source anchors changed')
    raw=regular(base,'turns.json').read_bytes();require(sha(raw)==LEDGER_SHA,'Exact original two-turn list changed')
    turns=parse(raw);require(type(turns) is list and len(turns)==2 and all(type(z) is dict and type(z['turn']) is int for z in turns) and [z['turn'] for z in turns]==[1,2],'Typed complete original2/5 ledger required')
    prior=parse(regular(base,'prior_report.json').read_bytes());require(type(prior) is dict and bool(prior),'Original prior is PRESENT; null/empty fallback prohibited')
    require(sha(regular(base,'SOURCE_PROOF_QUALIFICATIONS.md').read_bytes())=='69196e84de0d627b31b6f2a20a3745ba33048969cb93efba92a886bfedf8bc7e','Exact operative imported proof qualifications required')

''' +g[end:]
start=g.index('def revision_basis():');end=g.index('\ndef args(',start)
g=g[:start]+'''def root_binding_input(name,pin_value):
    p=regular(R,name)
    require(p.resolve().is_relative_to(A.resolve()) and not p.resolve().is_relative_to(C.resolve()) and not p.resolve().is_relative_to(HERE.resolve()),'Genuine external ROOT bindings outside closed packets required')
    require(sha(p.read_bytes())==digest(pin_value),'Actual ROOT immutable-bindings SHA differs')
    o=parse(p.read_bytes())
    required(o,{'schema':'pr41-root-approved-immutable-acceptance-bindings/v1','status':'ROOT_APPROVED_CLOSED_WHOLE_EVIDENCE','root_full_current_read_completed':True,'root_full_whole_read_completed':True,'independent_whole_current_pass':True,'mandatory_corrections':[],'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0},'Explicit ROOT whole reading, not a draft')
    utc_clock(o['created_utc'],'ROOT binding creation')
    require(type(o['whole_manifest']) is dict and type(o['root_whole_inspection']) is dict,'Actual explicit whole/root references required')
    return o,p


def basis(root_bindings,root_bindings_sha256):
    reviewed,rp=root_binding_input(root_bindings,root_bindings_sha256)
    inputs=load(HERE/'INPUT_BINDINGS.json');require(inputs['source_only'] is True,'Prepared input contract is source-only')
    refs=[]
    for n in sorted(inputs['pins']):
        v=inputs['pins'][n];bound(v);refs.append(v)
    for c in inputs['closures']:
        root=A/c['directory'];raw=regular(root,c['manifest_name']).read_bytes()
        require(sha(raw)==c['manifest_sha256'],'Closed included manifest changed')
        check(root,c['members']+c['foreign_members'])
        exact(root,{z['path'] for z in rows(c['members']+c['foreign_members'])}|{c['manifest_name']})
    frozen=manifest(C,'MANIFEST.json',CURRENT_SHA,547)
    require(all((C/z['path']).stat().st_mode&0o777==0o444 for z in frozen) and (C/'MANIFEST.json').stat().st_mode&0o777==0o444,'Frozen current0444 required')
    deps=load(C/'CURRENT_PROOF_DEPENDENCIES.json')
    required(deps,{'dependency_anchor_repository_relative':A.relative_to(R).as_posix()},'Exact portable dependency anchor')
    require(sha((C/'CURRENT_PROOF_DEPENDENCIES.json').read_bytes())==DEPS_SHA and len(rows(deps['files']))==469,'Complete469 dependency rows required');check(A,deps['files'])
    source(C)
    for n in ADMIN:
        required(load(C/n),{'id':ID,'problem_number':CODE,'status':'unsolved_scoped_conditional_partial_pending_NEW_whole_gate','full_problem_solved':False,'novelty_claimed':False,'current_gate':'pending_NEW_whole_current_packet_source_first_adversary','current_verdict':None,'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'original_substantive_attempts':2,'substantive_attempt_limit':5,'new_substantive_attempts':0,'audit_turns':0,'historical_verdict_transferred':False,'canonical_historical_events_inferred':False},'Dated pending administration retained')
    w=A/'whole_current_source_first_family';wm=reviewed['whole_manifest'];require(wm['path']==(w/'FIRST_PARTY_MANIFEST.json').relative_to(R).as_posix(),'Literal whole-family manifest anchor required')
    raw=bound(wm);whole=parse(raw)
    required(whole,{'status':'CLOSED_NEW_WHOLE_CURRENT_SOURCE_FIRST_REVIEW','excluded':['FIRST_PARTY_MANIFEST.json'],'files_count':143,'foreign_count':17,'reviewed_current_manifest_sha256':CURRENT_SHA,'all_members_0444':True},'Closed whole authored/foreign classification')
    authored,foreign=rows(whole['files']),rows(whole['foreign_files'])
    require(len(authored)==143 and len(foreign)==17 and not {z['path'] for z in authored}.intersection(z['path'] for z in foreign),'Exact143/17 distinct whole members')
    check(w,authored+foreign);exact(w,{z['path'] for z in authored+foreign}|{'FIRST_PARTY_MANIFEST.json'})
    for z in authored+foreign:
        require((w/z['path']).stat().st_mode&0o777==0o444,'Whole files must remain0444')
        if z['path'].endswith('.json'):parse((w/z['path']).read_bytes())
    verdict=load(w/'RESULT.json')
    required(verdict,{'verdict':WHOLE_VERDICT,'review_completed':True,'partial_valid':True,'full_problem_solved':False,'novelty_claimed':False,'mandatory_repairs':[],'original_substantive_attempts':2,'substantive_attempt_limit':5,'new_substantive_attempts':0,'audit_turns':0,'paper_DOI_tracker_promotion':False,'candidate_helpers_imported_or_executed':False},'Complete new whole scientific disposition')
    required(verdict['reviewed_current'],{'manifest_sha256':CURRENT_SHA,'members':547,'all_modes':'0444'},'Whole exact current')
    require(whole['result_sha256']==sha((w/'RESULT.json').read_bytes()) and whole['report_sha256']==sha((w/'WHOLE_CURRENT_ADVERSARIAL_REVIEW.md').read_bytes()),'Complete whole verdict/report binding differs')
    root= parse(bound(reviewed['root_whole_inspection']))
    required(root,{'status':'PASS','independent_family_manifest_sha256':wm['sha256'],'authored_members':143,'separately_bound_foreign_members':17,'whole_independent_verdict':verdict},'ROOT actual complete whole reading')
    for key in ['root_full_current_read_completed','root_full_whole_read_completed']:
        if key in root:require(root[key] is True,'Typed ROOT read flag required')
    cap=load(A/'root_current_freeze_actual_capture/CAPTURE.json')
    required(cap,{'actual_execution':True,'completed':True,'pid':36236,'exit_code':0,'status':'PASS','stdin_supplied':False,'native13_and_HEAD_unchanged':True},'Actual current freeze')
    require(utc_clock(cap['started_utc'],'Freeze start')<=utc_clock(cap['finished_utc'],'Freeze finish'),'Freeze clock order')
    check(A/'root_current_freeze_actual_capture',[cap['stdout'],cap['stderr']])
    require(equal(cap['fresh_native13_before'],cap['fresh_native13_after']) and cap['head_before']==cap['head_after'],'Dated freeze actual pre/post equality required')
    ledger=load(A/'ROOT_PRIMARY_READ_LEDGER.json');card=load(A/'ROOT_SCIENCE_CARD.json')
    require(ledger['reading_completed'] is True and type(ledger['root_flags']) is dict and len(ledger['root_flags'])==8 and equal(ledger['root_flags'],card['root_flags']) and all(v is True for v in ledger['root_flags'].values()),'Exact eight genuine read-ledger/card flags required')
    refs += [wm,reviewed['root_whole_inspection'],pin(rp),pin(w/'RESULT.json'),pin(w/'WHOLE_CURRENT_ADVERSARIAL_REVIEW.md')]
    require(len({z['path'] for z in refs})==len(refs),'Duplicate immutable evidence reference')
    return frozen,sorted(refs,key=lambda z:z['path'])


def plan_scope(o,prep,root_bindings,root_bindings_sha256):
    _,refs=basis(root_bindings,root_bindings_sha256)
    bindings,_=root_binding_input(root_bindings,root_bindings_sha256)
    draft=load(HERE/'DRAFT_FINAL_PLAN.json')
    draft.update(plan_status='ROOT_REVIEWED_FOR_ACTUAL_RECONCILIATION',preparation_manifest_sha256=prep,root_bindings=root_bindings,root_bindings_sha256=root_bindings_sha256,whole_manifest_sha256=bindings['whole_manifest']['sha256'],root_full_current_read_completed=True,root_full_whole_read_completed=True,independent_whole_current_pass=True,immutable_evidence_references=refs)
    require(equal(o,draft),'Only explicit completed ROOT fields and complete actual immutable refs may replace draft placeholders')
    require(equal(o['scientific_scope'],load(HERE/'SCIENTIFIC_SCOPE.json')),'Full scientific qualification differs')
    return refs

''' +g[end:]
g=g.replace("['final-plan','final-receipt','final-manifest','reconciliation-capture','previous-mirror','fresh-preimage']","['final-plan','final-receipt','final-manifest','reconciliation-capture','previous-mirror','previous-post','fresh-preimage','root-bindings']")
g=g.replace("or n=='previous_mirror'","or n in {'previous_mirror','previous_post'}")
g=g.replace("['final_plan','final_receipt','final_manifest','reconciliation_capture','previous_mirror','fresh_preimage']","['final_plan','final_receipt','final_manifest','reconciliation_capture','previous_mirror','previous_post','fresh_preimage','root_bindings']")
g=g.replace('plan_scope(scope,a.preparation_manifest_sha256)','plan_scope(scope,a.preparation_manifest_sha256,a.root_bindings,a.root_bindings_sha256)')
g=g.replace("'pr':40,'problem_id':2814","'pr':41,'problem_id':9700035")
g=g.replace("[('--plan',a.final_plan)","[('--root-bindings',a.root_bindings),('--root-bindings-sha256',a.root_bindings_sha256),('--plan',a.final_plan)")
old="""    require(ps['previous_mirror']==B/'audits/pr39_9500008/state_mirror_bindings.json','Actual completed PR39 proposal required')
    previous=load(ps['previous_mirror']); require(len(previous['entries'])==29 and 39 in previous['required_completed_prs'] and 40 not in previous['required_completed_prs'],'Require completed PR39 prior scope')"""
new="""    previous_root=B/'audits/pr40_2814'
    require(ps['previous_mirror']==previous_root/'state_mirror_bindings.json' and ps['previous_post']==previous_root/'post_acceptance_verification.json','Literal actual completed PR40 predecessor evidence required')
    previous=load(ps['previous_mirror']); require(len(previous['entries'])==30 and 40 in previous['required_completed_prs'] and 41 not in previous['required_completed_prs'],'Actual completed PR40 prior scope required')
    required(load(ps['previous_post']),{'status':'PASS','pr':40,'targets':31,'consumed_substantive_turns':37,'primary_acceptances':30,'program_completed_count':30,'fresh_native_mirror_noop':True},'Completed actual predecessor post verification')"""
assert old in g;g=g.replace(old,new)
g=g.replace("'Original13/14 snapshot'); require(len(snap['files'])==13 and len(snap['changed_paths'])==14,'Original13/14 counts')","'Original16/17 snapshot'); require(len(snap['files'])==16 and len(snap['changed_paths'])==17,'Original16/17 counts')")
g=g.replace("len(raw)==snap['diff_bytes'] and sha(raw)==snap['diff_sha256'] and raw==(A/'pr_input/diff.patch').read_bytes()","len(raw)==201709 and raw==(A/'pr_input/diff.patch').read_bytes()")
g=g.replace("ID not in state and '20001896' not in state","ID not in state").replace("in {ID,'20001896'}","in {ID}")
g=g.replace("frozen,_=basis()","frozen,_=basis(a.root_bindings,a.root_bindings_sha256)")
g=g.replace("'previous_mirror','previous_mirror_sha256','fresh_preimage','fresh_preimage_sha256'","'previous_mirror','previous_mirror_sha256','previous_post','previous_post_sha256','fresh_preimage','fresh_preimage_sha256','root_bindings','root_bindings_sha256'")
start=g.index('def accepted_invariants(');end=g.index('\ndef foreign_capture(',start)
g=g[:start]+'''def accepted_invariants(o,pins,pre):
    required(o,{'schema':'pr41-accepted-qualified-conditional-partial/v1','pr':41,'id':9700035,'problem_id':9700035,'problem_number':CODE,'queue_status':'unsolved','outcome':'unsolved_accepted_partial_merged','original_head':HEAD,'original_base':ORIGINAL_BASE,'merge_parents':[pre['main_before'],HEAD],'remote_state':'MERGED','remote_isDraft':False,'canonical_scientific_artifact_sha256':SCIENCE_SHA,'source_record_sha256':SOURCE_SHA,'original_ledger_sha256':LEDGER_SHA,'substantive_attempts_used':2,'substantive_attempt_limit':5,'native_historical_events_inferred':False,'historical_metadata_archival_only':True,'workflow_completion_estimate_percent':100,'full_resolution_completion_estimate_percent':0,'scientific_scope':load(HERE/'SCIENTIFIC_SCOPE.json'),**SCIENCE,**pins},'Strict final acceptance')
    for k in ['merge_commit','merge_tree']:require(type(o[k]) is str and re.fullmatch('[0-9a-f]{40}',o[k]),'Actual merge object required')
    utc_clock(o['merged_at'],'Actual merge date');source(K)
    for n in ADMIN:
        required(load(K/n),{**SCIENCE,**pins,'id':9700035,'status':'unsolved_accepted_partial_merged','merge_commit':o['merge_commit'],'merge_tree':o['merge_tree'],'merged_at':o['merged_at'],'new_whole_current_gate':WHOLE_VERDICT,'historical_verdict_transferred':False,'current_context_path':'CURRENT_CONTEXT_PRESENT.md','current_audit_scope_path':'CURRENT_AUDIT_SCOPE_PRESENT.md'},'Present final administrative scope '+n)


def canonical_names(frozen,accepted=False):
    return {z['path'] for z in frozen}|{'reviewed_pending_administration/'+n for n in ADMIN}|{'reviewed_pending_administration/MANIFEST.json','ACCEPTED_QUEUE_PATCH.json','CURRENT_ACCEPTANCE_SCOPE.md','CURRENT_CONTEXT_PRESENT.md','CURRENT_AUDIT_SCOPE_PRESENT.md'}|({'acceptance.json','ACCEPTANCE.md','MANIFEST.json'} if accepted else set())


def canonical(frozen,accepted=False):
    exact(K,canonical_names(frozen,accepted))
    for z in frozen:
        p=K/('reviewed_pending_administration/'+z['path'] if z['path'] in ADMIN else z['path'])
        require(p.read_bytes()==(C/z['path']).read_bytes(),'Frozen science/archival administration changed')
    require((K/'reviewed_pending_administration/MANIFEST.json').read_bytes()==(C/'MANIFEST.json').read_bytes(),'Dated frozen manifest changed');source(K)

''' +g[end:]
# Bound all ledgers exactly and strengthen the imported module's loose path reader.
g=g.replace("    m.ledger_budget=ledger\n    return m","    m.ledger_budget=ledger\n    def strict_bound(repo,reference):\n        require(Path(repo).resolve()==R.resolve(),'Exact native mirror repository required')\n        raw=regular(R,reference['path']).read_bytes();require(sha(raw)==digest(reference['sha256']),'Strict native mirror binding changed');return raw\n    m.bound=strict_bound\n    return m")
ast.parse(g);put('pr41_guards.py',g)

body='''Accept PR41 / 9700035 / AMR-096-0035 as an UNSOLVED qualified partial. The unchanged PROOF establishes the unconditional expected interior all-pair prescribed route-union law and full-length lower bound. The full expected-length law additionally requires t^4 P(D>t)->0; finite fourth moment suffices. The indexed2012 unconditional target remains open; published2014 Problem9 asks which added assumptions suffice. Full SIRSN finite major-road intensity is used; weak SIRSN does not automatically supply it. Imported model proof qualifications, credited foundations and bounded primary-read limits remain explicit. Original16, complete PRESENT prior and two research turns are exact archives. Actual root211/3809 and1326/122 finite/data replays, the NEW whole-source-first qualified review and actual final reconciliation are bound; finite controls are not universal proof. Current model/reasoning/deadline remain null. Original2/5,new0,audit0; no novelty, general solution, exhaustive priority or human peer-review claim. One present acceptance event follows the exact original-head merge; no historical event is reconstructed. No paper, new DOI, tracker or release.
'''
scope_note='''The operative qualification is SOURCE_PROOF_QUALIFICATIONS.md (SHA25669196e84de0d627b31b6f2a20a3745ba33048969cb93efba92a886bfedf8bc7e). It is appended in README.md, SOURCE_AUDIT.md, review/REVIEW.md and pr_body.md. The exact original source/review bodies are in original_archive/SOURCE_AUDIT.md and original_archive/review/REVIEW.md. Dated CURRENT_CONTEXT.md and CURRENT_AUDIT_SCOPE.md remain frozen archival summaries: their phrases "appended below"/"historical text follows" do not mean those summaries embed the bodies. These present summaries point to the exact operative files instead. Old pending/null review metadata remains archived, and the separate accepted metadata is the current disposition. Root primary-read limits and all printed Kahn joint-event/T_n/constant/speed-times-time qualifications remain bound; full external constructions are credited imports.
'''
i=original['integrate_reviewed_partial.py'].decode().replace('pr40_guards','pr41_guards').replace('PR40','PR41').replace('pr40','pr41')
start=i.index('BODY = ');end=i.index('\n\ndef queue_after',start)
i=i[:start]+'BODY = '+repr(body)+'\nPRESENT_SCOPE = BODY + "\\n" + '+repr(scope_note)+'\n'+i[end:]
i=i.replace("cells[9]=' 0/5 '","cells[9]=' 2/5 '").replace('attempts/2814/ACCEPTANCE.md','attempts/9700035/ACCEPTANCE.md').replace('Accepted source-hold partial','Accepted qualified conditional partial')
i=i.replace("old['number']!=40","old['number']!=41").replace("z['number']==40","z['number']==41").replace("z['number']==41];","z['number']==41];")
i=i.replace("and not (g.K.parent/'20001896').exists() and not (g.K.parent/'20001896').is_symlink()",'')
i=i.replace('Primary and duplicate native canonical paths must be absent','Selected native canonical path must be absent')
i=i.replace("len(state)==30 and g.ID not in state and '20001896' not in state","len(state)==31 and g.ID not in state")
i=i.replace('postPR39 native30targets/37turns, both selected identities absent','postPR40 native31targets/37turns, selected identity absent')
i=i.replace("inv['completed_count']==29 and sum(z.get('stage')=='complete' for z in inv['items'])==29","inv['completed_count']==30 and sum(z.get('stage')=='complete' for z in inv['items'])==30")
i=i.replace('Require29 complete primaries before40','Require30 complete primaries before41').replace('dot/math-2814','dot/math-9700035')
i=i.replace("'original_substantive_attempts':0","'original_substantive_attempts':2")
i=i.replace("g.exact(g.K,{z['path'] for z in orig}); g.source(g.K)","g.exact(g.K,{z['path'] for z in orig}); g.original_native(g.K)")
i=i.replace("for n in g.ADMIN-{'acceptance.json'}:","for n in g.ADMIN:")
i=i.replace("id=2814,status=", "id=9700035,current_context_path='CURRENT_CONTEXT_PRESENT.md',current_audit_scope_path='CURRENT_AUDIT_SCOPE_PRESENT.md',current_gate='accepted_qualified_partial',current_verdict=g.WHOLE_VERDICT,status=")
i=i.replace("new_whole_current_gate='PASS_BOUNDED_PARTIAL_SOURCE_HOLD'","new_whole_current_gate=g.WHOLE_VERDICT")
start=i.index("        g.write(g.K/'CURRENT_ACCEPTANCE_SCOPE.md'");end=i.index("        g.write(g.A/'integration_merge_queue_before.md'",start)
i=i[:start]+"        for n in ['CURRENT_ACCEPTANCE_SCOPE.md','CURRENT_CONTEXT_PRESENT.md','CURRENT_AUDIT_SCOPE_PRESENT.md']:g.write(g.K/n,PRESENT_SCOPE.encode(),exclusive=True)\n"+i[end:]
i=i.replace("'pr41-accepted-bounded-source-hold/v1'","'pr41-accepted-qualified-conditional-partial/v1'")
i=i.replace("'pr':40,'id':2814,'problem_id':2814","'pr':41,'id':9700035,'problem_id':9700035")
i=i.replace("'substantive_attempts_used':0","'substantive_attempts_used':2")
i=i.replace("'duplicate_native_acceptance_added':False,",'')
i=i.replace("(g.K/'acceptance.json').read_bytes()==(g.C/'acceptance.json').read_bytes() and ","not (g.K/'acceptance.json').exists() and ")
i=i.replace('Only exact pending lowercase receipt may be replaced once','New lowercase accepted receipt must be absent')
i=i.replace("original_attempts='0/5'","original_attempts='2/5'").replace("cumulative_attempts='0/5'","cumulative_attempts='2/5'")
i=i.replace("done==30,'Expected30 primary completions after40'","done==31,'Expected31 primary completions after41'")
i=i.replace("completed_count=30,program_completion_estimate_percent=30/180*100,completion_estimate_percent=30/180*100,current_pr=41","completed_count=31,program_completion_estimate_percent=31/180*100,completion_estimate_percent=31/180*100,current_pr=42")
i=i.replace("g.dump(g.K/'acceptance.json',accept)","g.dump(g.K/'acceptance.json',accept,exclusive=True)")
i=i.replace('Accepted UNSOLVED source-hold partial: 2814 / KP-3.16','Accepted UNSOLVED qualified partial: 9700035 / AMR-096-0035').replace('original0/5 ledger and duplicate source/prior remain unchanged','original2/5 ledger and PRESENT source/prior remain unchanged')
i=i.replace('original0/5,new0,audit0','original2/5,new0,audit0').replace('Program30/180=16.6667%','Program31/180=17.2222%')
ast.parse(i);put('integrate_reviewed_partial.py',i)

s=original['seal_final_evidence.py'].decode().replace('pr40_guards','pr41_guards').replace('pr40','pr41').replace("'pr':40,'problem_id':2814","'pr':41,'problem_id':9700035")
s=s.replace("p.add_argument('--execute',action='store_true');", "p.add_argument('--root-bindings',required=True); p.add_argument('--root-bindings-sha256',required=True); p.add_argument('--execute',action='store_true');")
s=s.replace('g.plan_scope(scope,a.preparation_manifest_sha256)','g.plan_scope(scope,a.preparation_manifest_sha256,a.root_bindings,a.root_bindings_sha256)').replace('_,after=g.basis()','_,after=g.basis(a.root_bindings,a.root_bindings_sha256)')
# Stage and publish final evidence atomically into an absent new adjacent directory.
s=s.replace('import argparse\n','import argparse\nimport ctypes\nimport os\nfrom pathlib import Path\n')
s=s.replace('    output.mkdir()','    target=output; stage=g.A/(".pr41-final-stage-"+str(os.getpid())+"-"+g.stamp().replace(":",""));stage.mkdir(exist_ok=False);output=stage')
s=s.replace("    for f in output.iterdir(): f.chmod(0o444)\n", "    for f in output.iterdir(): f.chmod(0o444)\n    g.require(sys.platform=='darwin','Reviewed macOS absent-only directory publication required');libc=ctypes.CDLL(None,use_errno=True);rename=libc.renamex_np;rename.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint];rename.restype=ctypes.c_int\n    if rename(os.fsencode(stage),os.fsencode(target),4)!=0:\n        error=ctypes.get_errno();raise OSError(error,os.strerror(error),str(target))\n    output=target\n")
ast.parse(s);put('seal_final_evidence.py',s)

m=original['state_mirror_reconciliation.py'].decode().replace('pr40_guards','pr41_guards').replace('pr40','pr41').replace('PR40','PR41')
m=m.replace("'current_pr':41,'completed_count':30","'current_pr':42,'completed_count':31")
m=m.replace("inv['completed_count']==30 and sum(z.get('stage')=='complete' for z in inv['items'])==30","inv['completed_count']==31 and sum(z.get('stage')=='complete' for z in inv['items'])==31").replace('Exactly30 primary completions','Exactly31 primary completions')
m=m.replace("z['number']==40","z['number']==41").replace("'original_attempts':'0/5','cumulative_attempts':'0/5'","'original_attempts':'2/5','cumulative_attempts':'2/5'")
m=m.replace("len(prior)==30 and g.ID not in prior and '20001896' not in prior","len(prior)==31 and g.ID not in prior")
m=m.replace('Require30targets/37turns and both selected identities absent','Require31targets/37turns and selected identity absent')
m=m.replace('Incremental present accepted primary PR41; original0/5, duplicate raw source/prior only, no historical native reconstruction or independent duplicate effort.','Incremental present accepted primary PR41; original2/5, no new proof turn or historical native reconstruction.')
m=m.replace("proposal['required_completed_prs']+[40]","proposal['required_completed_prs']+[41]").replace("{'pr':40,'id':g.ID","{'pr':41,'id':g.ID")
m=m.replace("g.K/'SOURCE_STATUS.md'","g.K/'PROOF.md'").replace("'used':0,'limit':5,'kind':'pr41_exact_original_zero_attempt_object'","'used':2,'limit':5,'kind':'pr41_exact_original_two_turn_list'")
start=m.index('    m=g.mirror_module(proposal); original=');end=m.index('    plan=m.build_plan',start)
m=m[:start]+'''    m=g.mirror_module(proposal);original=g.load(g.K/'turns.json');negatives=[]
    for label in ['bool_turn','phantom_attempt','missing_turn','wrong_order','extra_field']:
        obj=copy.deepcopy(original)
        if label=='bool_turn':obj[0]['turn']=True
        elif label=='phantom_attempt':obj.append({'turn':3})
        elif label=='missing_turn':obj.pop()
        elif label=='wrong_order':obj.reverse()
        else:obj[0]['extra']=None
        try:m.ledger_budget(g.encode(obj),'pr41_exact_original_two_turn_list',2,5)
        except m.Rejected:negatives.append(label)
        else:raise ValueError('Exact two-turn ledger guard accepted mutant '+label)
''' +m[end:]
m=m.replace("plan['primary_count']==30 and plan['duplicate_count']==1 and len(plan['state_after'])==31 and sum(z['turns_used'] for z in plan['state_after'].values())==37","plan['primary_count']==31 and plan['duplicate_count']==1 and len(plan['state_after'])==32 and sum(z['turns_used'] for z in plan['state_after'].values())==39")
m=m.replace('Exactly31targets/37turns/30primary/one preserved duplicate required','Exactly32targets/39turns/31primary/one preserved duplicate required')
m=m.replace(" and '20001896' not in plan['state_after']",'').replace('Every prior state unchanged; no new duplicate state','Every prior state unchanged; no new duplicate')
m=m.replace("{'turns_used':0,'turn_limit':5,'status':'unsolved'}","{'turns_used':2,'turn_limit':5,'status':'unsolved'}").replace('Native zero budget','Native original2/5 budget')
m=m.replace("'prior_state_entries_preserved':30,'current_targets':31,'consumed_substantive_turns':37,'primary_acceptances':30","'prior_state_entries_preserved':31,'current_targets':32,'consumed_substantive_turns':39,'primary_acceptances':31")
m=m.replace("'duplicate20001896_native_acceptance_added':False", "'new_duplicate_native_acceptance_added':False")
m=m.replace("'pr':40,'targets':31,'consumed_turns':37,'primary_acceptances':30","'pr':41,'targets':32,'consumed_turns':39,'primary_acceptances':31")
ast.parse(m);put('state_mirror_reconciliation.py',m)

v=original['verify_post_acceptance.py'].decode().replace('pr40_guards','pr41_guards').replace('pr40','pr41')
v=v.replace("'prior_state_entries_preserved':30,'current_targets':31,'consumed_substantive_turns':37,'primary_acceptances':30","'prior_state_entries_preserved':31,'current_targets':32,'consumed_substantive_turns':39,'primary_acceptances':31")
v=v.replace("'duplicate20001896_native_acceptance_added':False","'new_duplicate_native_acceptance_added':False")
v=v.replace("len(current)==31 and sum(z['turns_used'] for z in current.values())==37 and '20001896' not in current","len(current)==32 and sum(z['turns_used'] for z in current.values())==39")
v=v.replace("'id':g.ID,'pr':40,'status':'unsolved','turns_used':0","'id':g.ID,'pr':41,'status':'unsolved','turns_used':2").replace('Native present zero budget','Native present original2/5 budget')
v=v.replace("'pr':40,**pins","'pr':41,**pins").replace("'targets':31,'consumed_substantive_turns':37,'primary_acceptances':30,'program_completed_count':30,'program_completion_estimate_percent':30/180*100","'targets':32,'consumed_substantive_turns':39,'primary_acceptances':31,'program_completed_count':31,'program_completion_estimate_percent':31/180*100")
v=v.replace("'exact_original13_and_SOURCE_STATUS_unchanged':True,'whole_current_and216dependencies_bound':True,'entire_history_prefix_and30prior_states_preserved':True","'exact_original16_and_PROOF_unchanged':True,'whole_current547_and469dependencies_bound':True,'entire_history_prefix_and31prior_states_preserved':True")
v=v.replace("'duplicate_native_acceptance_added':False","'new_duplicate_native_acceptance_added':False").replace("'pr':40,'targets':31,'turns':37,'primary_acceptances':30","'pr':41,'targets':32,'turns':39,'primary_acceptances':31")
ast.parse(v);put('verify_post_acceptance.py',v)
print(json.dumps({'status':'SOURCE_ONLY_HELPERS_AUTHORED','helpers':5,'prepared_helpers_imported_or_executed':False,'bytes':sum((P/n).stat().st_size for n in ['pr41_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py'])},indent=2))
