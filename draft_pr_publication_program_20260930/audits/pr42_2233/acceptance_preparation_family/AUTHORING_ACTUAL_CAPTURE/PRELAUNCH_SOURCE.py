"""Own source authoring only; never import, compile or execute proposed helpers."""
from pathlib import Path
import json, hashlib, re
H=Path(__file__).resolve().parent
A=H.parent
R=A.parents[2]
OLD=A.parent/'pr41_9700035/acceptance_preparation_family_v2'
def put(name,text):
    p=H/name
    if p.exists(): raise ValueError('Retain existing source rather than overwrite: '+name)
    p.write_text(text)
def obj(name,value):put(name,json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def substitute(t):
    for x,y in [('pr41','pr42'),('PR41','PR42'),('pr40','pr41'),('PR40','PR41'),('9700035','2233'),('AMR-096-0035','EP-653'),('292b95ca601f166e6d246e609cf7ed5ca5653e25','099ae5e4d06d8789214cfaaece87309c87e914f9'),('c6975ca76f9f667f1250ba403d0e6da2aafe14d0','60292bed09f59236aa192cb17aa138f7b4750e1a'),('3431ca2dfb332500f3815ea1e61f089744b3bacd9c3659018537016b9396fbfa','09ac3a27edc2113da9574e57a13e7a0c99baa194fa50efb07548ec47fa7493de'),('ade2f6fe9890f1038810158a284f4a8924e34d6d2f95b3a07654d78fa6501ff6','7570cec29df5d916107f566e3fd15c48228c6ea3f6b420fc40e05b48898799c6'),('d86ee1dc749ef5b9a0446109fb6f0278246cf3584f36aa70205b5bc6c683782f','9441de78ed662c85c03125baf6d85de2388762488affb3a9769a88037d9e8974'),('bd0a82165c3ac81f7a7d35ace164f20ecb87e6b73a9155815e4eecac655a2549','60d0413980ac5f251913a26298692c5efc797d8f5084ca03e8d134472ab820e4'),('464af6d259f9275ca9f0056567f5301bc228465fa0ddaf2faece0920cab6bd7c','0b116a4593d84d7e9d02f635a080eb0e2242aaba66acfc8efeae74462ad89898'),('69196e84de0d627b31b6f2a20a3745ba33048969cb93efba92a886bfedf8bc7e','3529898445960cde70381bf99ea8287ec88a1003d8ca1cb4c3e0d088abdee570'),('SOURCE_PROOF_QUALIFICATIONS.md','SOURCE_PRECISION_QUALIFICATIONS.md'),('CURRENT_PROOF_DEPENDENCIES.json','CURRENT_DEPENDENCIES.json'),('PROOF.md','PARTIAL.md'),('turns.json','turns.jsonl'),('snapshot_manifest.json','snapshot_manifest_v2.json'),("A/'source_snapshot'","A/'source_snapshot_v2'"),('qualified-conditional-partial','qualified-scoped-partial'),('qualified conditional partial','qualified scoped partial'),('source/PRESENT prior','source/absent-raw-prior SQL fallback'),('PRESENT prior','absent-raw-prior SQL fallback')]:t=t.replace(x,y)
    t=re.sub(r'(?<![A-Za-z0-9_])(30|31|32|37|39|40|41|42|469|547)(?![A-Za-z0-9_])',lambda m:{'30':'31','31':'32','32':'33','37':'39','39':'41','40':'41','41':'42','42':'43','469':'517','547':'385'}[m[0]],t)
    t=t.replace('original16','original17').replace('Original16','Original17').replace('16/17','17/18')
    return t
def replace_function(text,name,new):
    pattern=r'(?ms)^def '+name+r'\([^\n]*\):\n.*?(?=^def |\Z)'
    text,n=re.subn(pattern,lambda m:new+'\n\n',text)
    if n!=1:raise ValueError('Function replacement not unique: '+name)
    return text
guard=substitute((OLD/'pr41_guards.py').read_text())
guard=guard.replace("ADMIN = {'status.json', 'attempt.json', 'readiness.json', 'review/verdict.json'}","ADMIN = {'status.json', 'readiness.json', 'review/verdict.json'}")
guard=re.sub(r'(?m)^IMMUTABLE = .*$',"IMMUTABLE = {'PARTIAL.md','check_spectra.py','check_results.json','source_record.json','source_checksums.json','turns.jsonl','review/PARTIAL.md','review/independent_checks.py','review/independent_results.json','review/submitted_check_spectra.py','review/submitted_results.json'}",guard)
guard=guard.replace("'PASS_QUALIFIED_UNSOLVED_PARTIAL_NEW_WHOLE_CURRENT'","'PASS_QUALIFIED_UNSOLVED_PARTIAL_NEW_WHOLE_CURRENT'")
guard=replace_function(guard,'original_native',"""def original_native(base):
    snapshot=load(A/'snapshot_manifest_v2.json')
    require(snapshot['schema']=='pr42-root-readonly-original-snapshot/v1' and len(snapshot['files'])==17,'Complete original17 required')
    exact(base,{z['path'] for z in rows(snapshot['files'])})
    for z in rows(snapshot['files']):
        raw=regular(base,z['path']).read_bytes()
        require(raw==regular(A/'source_snapshot_v2',z['path']).read_bytes() and len(raw)==z['bytes'] and sha(raw)==z['sha256'],'Original17 bytes differ')""")
guard=replace_function(guard,'source',"""def source(base):
    original_native(base/'original_archive')
    for n in IMMUTABLE:
        require(regular(base,n).read_bytes()==regular(A/'source_snapshot_v2',n).read_bytes(),'Immutable math/code/saved full result/source/ledger changed')
    require(sha(regular(base,'PARTIAL.md').read_bytes())==SCIENCE_SHA and sha(regular(base,'source_record.json').read_bytes())==SOURCE_SHA,'Scientific/source anchors changed')
    raw=regular(base,'turns.jsonl').read_bytes();require(sha(raw)==LEDGER_SHA,'Exact original two-entry JSONL ledger changed')
    turns=ledger_list(raw)
    require(type(turns) is list and len(turns)==2 and all(type(z) is dict and type(z['turn']) is int for z in turns) and [z['turn'] for z in turns]==[1,2],'Typed original two-entry ledger in order[1,2] required')
    prior=regular(base,'root_evidence/pinned_prior_report.json').read_bytes()
    require(prior==regular(A,'pinned_prior_report.json').read_bytes() and equal(parse(prior),{}),'Absent raw EP-653 key and exact SQL fallback{} must not become PRESENT/null prior')
    require(sha(regular(base,'SOURCE_PRECISION_QUALIFICATIONS.md').read_bytes())=='3529898445960cde70381bf99ea8287ec88a1003d8ca1cb4c3e0d088abdee570','Exact operative source qualifications required')""")
guard += """
def ledger_list(raw):
    require(type(raw) is bytes and raw.endswith(b'\\n'),'Complete exact JSONL bytes required')
    return [parse(line) for line in raw.splitlines()]

def keyset(obj,keys,context):
    require(type(obj) is dict and set(obj)==set(keys),context+': unknown/missing critical fields prohibited')
"""
# basis() is deliberately installed only after the independent whole family's
# actual closed schema has been read; this author does not inspect active files.
start=guard.index('def basis(');end=guard.index('\ndef plan_scope(',start)
guard=guard[:start]+'''def basis(root_bindings,root_bindings_sha256):
    raise ValueError('SOURCE_NOT_CLOSED: actual independent whole schema not yet bound')

'''+guard[end+1:]
guard=guard.replace("'dependency_anchor_repository_relative'","'anchor_repository_relative'")
guard=guard.replace("previous_root=B/'audits/pr41_2814'","previous_root=B/'audits/pr41_9700035'")
guard=guard.replace("len(previous['entries'])==31", "len(previous['entries'])==31")
guard=guard.replace("require(len(snap['files'])==16 and len(snap['changed_paths'])==17", "require(len(snap['files'])==17 and len(snap['changed_paths'])==18")
guard=guard.replace("len(raw)==201709", "len(raw)==122952").replace("A/'pr_input/diff.patch'","A/'pr_input/diff.patch'")
guard=guard.replace("identities.count(42)","identities.count(42)")
guard=guard.replace("'prior_report.json'", "'root_evidence/pinned_prior_report.json'")
guard=guard.replace("'16'", "'17'")
put('pr42_guards.py',guard)
body='Accept PR42 / 2233 / EP-653 as an UNSOLVED scoped partial. For distinct finite planar point sets and the stated hypotheses, the unchanged PARTIAL establishes the generic-gluing deficit-spectrum union identity and small-seed obstruction, the sharp ceil(n/2) line/circle restriction with its t=o(n) exception extension, and the credited classical Erdos-Saldanha two-pin square-root defect. None proves the unrestricted n-o(n) target or a universal fixed-proportion obstruction. Complete original17 and original two-entry JSONL attempts are exact archives. Raw EP-653 prior key is absent; saved {} is a SQL fallback, not a retrieved null/PRESENT prior. Actual ROOT reproductions and bounded source reading are retained; finite controls are not asymptotic proof. The NEW whole-source-first gate, ROOT full reading and final reconciliation must be actually completed and bound before acceptance. Current model/reasoning/deadline stay null. Original2/5,new0,audit0; fullfalse, noveltyfalse; no paper, new DOI, tracker, release or human peer-review claim. One present native acceptance event follows the exact original-head merge; no historical event is reconstructed.\\n'
present='The NEW whole-current source-first gate has passed for this scoped partial, as bound in acceptance.json; the unrestricted target remains UNSOLVED. Mathematical bodies, original code/results/source and two JSONL attempts are unchanged. SOURCE_PRECISION_QUALIFICATIONS.md supplies the operative source and historical qualifications. All pending statements within CURRENT_CONTEXT.md, SOURCE_PRECISION_QUALIFICATIONS.md, README.md, SOURCE_AUDIT.md, review/REVIEW.md, pr_body.md, archived pending administration, original_archive, build, family_evidence and root_evidence are dated records of their preacceptance stages. Their saved historic PASS labels remain attributed evidence and do not supply this new gate. The dated source records do not assert current model/reasoning/deadline or exhaustive primary-proof verification. The absent raw prior key and SQL fallback{} remain distinct. See acceptance.json and ACCEPTANCE.md for the actual merged disposition and bindings.\\n'
integrate=substitute((OLD/'integrate_reviewed_partial.py').read_text())
begin=integrate.index('BODY = ');end=integrate.index('\n\ndef queue_after',begin)
integrate=integrate[:begin]+"BODY = "+repr(body.replace('\\n','\n'))+"\nPRESENT_SCOPE = "+repr(present.replace('\\n','\n'))+integrate[end:]
integrate=integrate.replace('Accepted qualified conditional partial','Accepted scoped partial')
integrate=integrate.replace('qualified conditional partial','scoped partial')
integrate=integrate.replace("archive =", "archive =")
integrate=integrate.replace("'snapshot_manifest_v2.json')['files']", "'snapshot_manifest_v2.json')['files']")
integrate=integrate.replace("'current_audit_scope_path'", "'current_audit_scope_path'")
integrate=integrate.replace("Program31/180=17.2222%", "Program32/180=17.7778%")
integrate=integrate.replace("Program32/180=17.2222%", "Program32/180=17.7778%")
integrate=integrate.replace('original2/5 ledger and PRESENT source/prior remain unchanged','original2/5 ledger, source, absent raw prior and SQL fallback remain unchanged')
put('integrate_reviewed_partial.py',integrate)
for name in ['seal_final_evidence.py','state_mirror_reconciliation.py','verify_post_acceptance.py']:
    t=substitute((OLD/name).read_text())
    t=t.replace("original=g.load(g.K/'turns.jsonl')", "original=g.ledger_list((g.K/'turns.jsonl').read_bytes())")
    t=t.replace("m.ledger_budget(g.encode(obj)","m.ledger_budget(b''.join(g.encode(z).replace(b'\\n',b'')+b'\\n' for z in obj)")
    t=t.replace('exact_original16_and_PROOF_unchanged','exact_original17_and_PARTIAL_unchanged')
    t=t.replace('whole_current547_and469dependencies_bound','whole_current385_and517dependencies_bound')
    t=t.replace('entire_history_prefix_and31prior_states_preserved','entire_history_prefix_and32prior_states_preserved')
    put(name,t)
scope={'schema':'pr42-proposed-accepted-scientific-scope/v1','id':'2233','problem_number':'EP-653','literal_target_status':'UNSOLVED','full_problem_solved':False,'novelty_claimed':False,'definition':'n distinct planar points, n>=2; r(p) distinct positive distances; sigma(P) number of distinct integers among r(p); g(n)=max sigma(P).','target':'g(n)/n -> 1, equivalently n-o(n) pinned-count values for all sufficiently large n.','scoped_results':['Under full independent-translation admissibility, forbidden collisions are proper polynomial zero sets and the union deficit spectrum equals the union of seed spectra; max seed size o(n) cannot give a linear spectrum.','Exact common line or positive-radius circle support gives sharp sigma<=ceil(n/2); t=o(n) off-support exceptions give sigma<=(1/2+o(1))n.','Credited classical Erdos-Saldanha two-pin bound n-2<=2r(p)r(q) gives the square-root defect n-sigma>=(sqrt(2n-3)-1)/2, compatible with the target.'],'boundaries':'Singleton/all-singleton seeds and n=2 covered; proper polynomial argument uses unrestricted translations; circle arc sharpness requires span<pi; approximate support is excluded; nongeneric controls are not target counterexamples.','exact_remaining_gap':'Construct n-o(n) distinct pinned-count values for all sufficiently large n, or prove a universal fixed-proportion obstruction for unrestricted distinct planar point sets.','source_read_limits':'Operative distinct-point target and Saldanha credit read on1995 manuscript pages14-15. Exact1997, Erdos-Fishburn, Csizmadia-Ismailescu and2026 preprint proofs are not recertified; reported external bounds are not elementary-proof premises, novelty or best-known claims.','qualification_path':'SOURCE_PRECISION_QUALIFICATIONS.md','qualification_sha256':'3529898445960cde70381bf99ea8287ec88a1003d8ca1cb4c3e0d088abdee570','prior_semantics':'Raw EP-653 key absent; saved{} SQL fallback is not a retrieved prior/null. Dated OPEN triage is historical background.','saved_result_qualification':'Final PARTIAL hash0b116a45 differs from reviewedb51799d2 only in review-status header; mathematical body identical. Current author replay differs only in partial_sha256; reviewed author and independent saved full objects exact.','original17_and_PARTIAL_unchanged':True,'historical_metadata_archival_only':True,'original_substantive_attempts':2,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'paper_or_new_DOI_or_tracker':False}
obj('SCIENTIFIC_SCOPE.json',scope)
obj('DRAFT_ROOT_IMMUTABLE_BINDINGS.json',{'schema':'pr42-root-approved-immutable-acceptance-bindings/v1','status':'PENDING_ROOT_CLOSED_WHOLE_READING','created_utc':None,'root_full_current_read_completed':False,'root_full_whole_read_completed':False,'root_acceptance_source_review_completed':False,'independent_whole_current_pass':False,'mandatory_corrections':[],'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'whole_manifest':None,'root_whole_inspection':None})
obj('DRAFT_FINAL_PLAN.json',{'schema':'pr42-root-reviewed-final-plan/v1','plan_status':'PENDING_ROOT_FULL_REVIEW_AND_ACTUAL_RECONCILIATION','pr':42,'problem_id':2233,'original_head':'099ae5e4d06d8789214cfaaece87309c87e914f9','original_base':'60292bed09f59236aa192cb17aa138f7b4750e1a','reviewed_candidate_manifest_sha256':'09ac3a27edc2113da9574e57a13e7a0c99baa194fa50efb07548ec47fa7493de','current_dependencies_sha256':'7570cec29df5d916107f566e3fd15c48228c6ea3f6b420fc40e05b48898799c6','whole_manifest_sha256':None,'preparation_manifest_sha256':None,'root_bindings':None,'root_bindings_sha256':None,'root_full_current_read_completed':False,'root_full_whole_read_completed':False,'root_acceptance_source_review_completed':False,'independent_whole_current_pass':False,'mandatory_corrections':[],'science_reexecution_of_current':False,'historical_PASS_transferred':False,'immutable_evidence_references':[],'scientific_scope':scope,'full_problem_solved':False,'partial_valid':None,'novelty_claimed':False,'original_substantive_attempts':2,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'paper_or_new_doi_or_tracker':False})
names=['snapshot_manifest_v2.json','ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md','ROOT_PRIMARY_READ_LEDGER.json','ROOT_SCIENCE_CARD.json','ROOT_CURRENT_INPUT_PREIMAGES.json','ROOT_CURRENT_PREREQUISITES_INSPECTION.json','root_current_freeze_actual_capture/CAPTURE.json','root_current_freeze_actual_capture/PRELAUNCH_OPERATOR.py','root_current_freeze_actual_capture/PRELAUNCH_SOURCE.py','root_current_freeze_actual_capture/stdout.bin','root_current_freeze_actual_capture/stderr.bin']
pins={n:{'path':(A/n).relative_to(R).as_posix(),'bytes':len((A/n).read_bytes()),'sha256':hashlib.sha256((A/n).read_bytes()).hexdigest()} for n in names}
prev=A.parent/'pr41_9700035'
for n in ['state_mirror_bindings.json','post_acceptance_verification.json','ROOT_ACTUAL_POST_INSPECTION.json']:
 p=prev/n;pins['previous/'+n]={'path':p.relative_to(R).as_posix(),'bytes':len(p.read_bytes()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
obj('INPUT_BINDINGS.json',{'schema':'pr42-acceptance-source-input-bindings/v1','source_only':True,'pins':pins,'current_manifest_sha256':'09ac3a27edc2113da9574e57a13e7a0c99baa194fa50efb07548ec47fa7493de','current_members':385,'current_dependencies_sha256':'7570cec29df5d916107f566e3fd15c48228c6ea3f6b420fc40e05b48898799c6','current_dependency_members':517,'future_whole_manifest':None,'future_root_whole_inspection':None})
print(json.dumps({'authored_source_only':True,'proposed_helpers_imported_compiled_executed':False,'future_whole_unbound':True,'files_written':sorted(p.name for p in H.iterdir() if p.is_file())}))
