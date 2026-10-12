"""Own closure-source inspection. Outer operator completes capture before sole-self freezing."""
from pathlib import Path,PurePosixPath
import datetime as dt,hashlib,json,os,stat
H=Path(__file__).resolve().parent;A=H.parent;R=H.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}
def put(n,o):
 with (H/n).open('x') as f:json.dump(o,f,sort_keys=True,indent=2);f.write('\n')
def text(n,s):
 with (H/n).open('x') as f:f.write(s)
def require(c,m):
 if not c:raise ValueError(m)
def main():
 result=load(H/'OWN_CONTROL_RESULTS_V3.json');require(result['status']=='PASS_PRIVATE_CONTROLS_ONLY' and result['production_imported_compiled_executed'] is False,'Final genuine own controls')
 inputs=load(H/'INPUT_BINDINGS.json');external=list(inputs['pins'].values())+[inputs[k] for k in ['previous_mirror','previous_post','previous_root_post','closed_whole_manifest','closed_whole_report','closed_whole_result','closed_root_whole_inspection']]
 for z in external:
  p=R/z['path'];b=p.read_bytes();require(p.is_file() and not p.is_symlink() and len(b)==z['bytes'] and sha(b)==z['sha256'],'Complete input binding changed')
 captures=[]
 for n in ['AUTHORING_ACTUAL_CAPTURE','SOURCE_REPAIR_ACTUAL_CAPTURE','ROOT_BINDING_ACTUAL_CAPTURE','CONTROLS_ACTUAL_CAPTURE','SOURCE_REPAIR_V2_ACTUAL_CAPTURE','CONTROLS_V2_ACTUAL_CAPTURE','SOURCE_REPAIR_V3_ACTUAL_CAPTURE','CONTROLS_V3_ACTUAL_CAPTURE']:
  d=H/n;o=load(d/'CAPTURE.json');pre=o['prelaunch'];require(o['actual_execution'] is True and o['completed'] is True and type(o['pid']) is int and o['pid']>0 and type(o['operator_pid']) is int and o['operator_pid']>0,'Genuine captured source process')
  expected_exit=1 if n in ['SOURCE_REPAIR_V2_ACTUAL_CAPTURE','CONTROLS_V2_ACTUAL_CAPTURE'] else 0
  require(o['exit_code']==expected_exit and o['status']==('PASS' if expected_exit==0 else 'FAIL'),'Retained source/control outcome')
  require(load(d/'PRELAUNCH.json')==pre and sha((d/'PRELAUNCH_SOURCE.py').read_bytes())==pre['source_sha256'] and sha((d/'PRELAUNCH_OPERATOR.py').read_bytes())==pre['operator_sha256'],'Full prelaunch source/operator')
  for channel in ['stdout','stderr']:
   b=(d/o[channel]['path']).read_bytes();require(len(b)==o[channel]['bytes'] and sha(b)==o[channel]['sha256'],'Complete own stream binding')
  require(dt.datetime.fromisoformat(o['started_utc'])<=dt.datetime.fromisoformat(o['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'Actual clocks');captures.append({'capture':pin(d/'CAPTURE.json'),'entire_actual_capture':o})
 post_values={'status':'PASS','pr':45,'targets':36,'consumed_substantive_turns':44,'primary_acceptances':35,'program_completed_count':35,'program_completion_estimate_percent':35/180*100,'exact_original18_and_PARTIAL_unchanged':True,'whole_current497_and416dependencies_bound':True,'entire_history_prefix_and35prior_states_preserved':True,'one_present_primary_event':True,'new_duplicate_native_acceptance_added':False,'new_proof_turns':0,'current_metadata_present_null':True,'fresh_native_mirror_noop':True,'full_target_resolved_in_prior_published_literature':False,'prior_publication_doi':None,'full_problem_solved_by_project':False,'full_problem_solved':False,'novelty_claimed':False,'paper_or_new_doi_or_tracker':False,'scientific_completion_estimate_percent':0,'workflow_completion_estimate_percent':100}
 root_values={'status':'PASS','completed_primary_prs':35,'all35_prior_states_and_full_history_prefix_preserved':True,'current13_match_exact_allowed_acceptance_changes':True,'entire_current_inventory_reconstructed':True,'canonical507_plus_manifest_fullbytes_modes':True,'merge505_overlay_plus_queue_Git_bodies_and_parents':True,'entire_native_proposal_and_saved_plan_reconstructed':True,'fresh_noop_replayed_without_writes':True,'original_attempts':1,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False,'program_completion_percent':35/180*100}
 put('ROOT_POST_CONTRACT.json',{'schema':'pr45-future-ROOT-whole-post-contract/v1','source_only':True,'future_ROOT_post_completed':False,'predecessor':{'ROOT_schema':'pr44-root-complete-actual-post-inspection/v1','mirror':inputs['previous_mirror'],'post':inputs['previous_post'],'ROOT_post':inputs['previous_root_post'],'genuine_post_inspection_capture':inputs['pins']['actual44_CAPTURE.json'],'genuine_prelaunch_post_inspector_source':inputs['pins']['actual44_post_inspector_prelaunch_source'],'actual_post_capture_pid':42112,'merge_commit':'f369d1e8f74b6462a0866f4b57a888233420a149','merge_tree':'6fa2de74e3b7d658cde5b04b94bc699ad6648d88','full_root_entire_post_equals_actual_post':True,'targets':35,'consumed_substantive_turns':43,'primary_acceptances':34,'duplicate_mirrors':1},'future45_required_ROOT_schema':'pr45-root-complete-actual-post-inspection/v1','future45_required_completed_values':root_values,'future45_required_entire_post_values':post_values,'future45_required_ROOT_complete_keyset':['schema','status','utc','completed_primary_prs','all35_prior_states_and_full_history_prefix_preserved','current13_match_exact_allowed_acceptance_changes','new_substantive_attempts','audit_turns','full_problem_solved','entire_post','canonical507_plus_manifest_fullbytes_modes','merge505_overlay_plus_queue_Git_bodies_and_parents','entire_current_inventory_reconstructed','all_six_real_phase_captures','current13','original_attempts','program_completion_percent','entire_native_proposal_and_saved_plan_reconstructed','fresh_noop_replayed_without_writes','final_sealer_actual_capture'],'future45_required_complete_inspections':['Every entire prior35 state object has exactly identical recursive scalar types; new set is old set plus 9900007. New state/event unsolved1/5; original one-line JSONL exactly bound; no new attempt/duplicate/historical transition.','Whole history byte sequence is complete retained prefix plus precisely one saved planned present event; entire event equals plan.','Whole native proposal equals complete actual44 predecessor with exactly declared mutable creation/scope/current inventory/current queue/requiredprs fields and one exact PR45 primary; same old duplicate and all prior ledgers/budgets preserved.','Whole saved native plan independently reconstructed from complete actual preflight state/history at its original timestamp and complete typed equality; fresh final replay is byte-preserving no-op without writes.','Entire180-row inventory independently reconstructed from retained actual preflight bytes; exact selected45 accepted fields/clock/count/next46 metadata; all179 others and every other top-level value exact.','Original head d9b4acf5d070d1f04ffac86a4f08916a5629ff16 exact second parent and actual fresh main preflight exact first parent. Actual accepted merge/tree equals full fresh remote receipt/prepush/final receipt. Distinct Githubbasec6975ca.../mergebase01358... retained.','Full505-file merge overlay and complete whole queue in immutable Git100644 tree with exact changed-path set; no native inventory/state/history/protected foreign path enters original-head merge. Queue only named Status/Turns/Findings changes; Chat/DOI and every other byte exact.','Full507-member plus self accepted canonical closure and literal full0444 including special bits; exact directory topology, original18 archive and immutable12 complete body equality.','Fresh actual native13 bytes and full modes match exactly allowed queue/inventory/state/history derivations; stable9 unchanged. Every ROOT-declared foreign tracked path worktree fullbytes/modes/HEAD/index protected throughout.','All six real ROOT phase captures preflight/overlay/prepush/finalize/mirror/post completely read: actual child/operator PIDs/argv/cwd/UTC/prelaunch fullsource and operator/full stdout and stderr. All retained failures also read and preserved. Final sealer capture separately pins operator/source/entire stdout/stderr/native13+modes/main preservation.','Completed ROOT entire_post equals actual post record with full recursive scalar types and exact known post schema/pin fields; completed ROOT keyset exactly specified, no fabricated timestamps/PIDs/approval or abbreviated counters.','No solution/novelty/priority/paper/newDOI/tracker/release/human-review claims; broader characterization gap and historical source/priority limits remain globally explicit. All-fixed-couplings proof, stated metric law, nonnegative dependent finite/tight offsets and setwise boundary preserved.']})
 put('CLOSURE_SOURCE_INSPECTION.json',{'schema':'pr45-owned-source-final-inspection/v1','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_closure_child_pid':os.getpid(),'status':'PASS_SOURCE_ONLY_INSPECTION','complete_source_captures':captures,'individual_external_refs_rechecked':len(external),'external_refs':external,'production_imported_compiled_executed':False,'ROOT_approval_or_acceptance_claimed':False,'private_control_result':pin(H/'OWN_CONTROL_RESULTS_V3.json'),'source_preparation_completion_percent':100,'acceptance_completion_percent':0,'discovery_completion_percent':0})
 status=load(H/'SOURCE_STATUS.json');(H/'INITIAL_SOURCE_STATUS.json').write_text(json.dumps(status,sort_keys=True,indent=2)+'\n');status.update(status='CLOSED_SOURCE_ONLY_PENDING_NEW_ADVERSARY_AND_ROOT_APPROVAL',source_preparation_completion_percent=100);(H/'SOURCE_STATUS.json').write_text(json.dumps(status,sort_keys=True,indent=2)+'\n')
 text('CONTRACT.md',CONTRACT)
 text('FINAL_SOURCE_REPORT.md',REPORT.format(rootsha=inputs['closed_root_whole_inspection']['sha256']))
 with (H/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+dt.datetime.now(dt.timezone.utc).isoformat()+' — Final SOURCE checkpoint:100% source preparation,0% acceptance and0% mathematical discovery. Genuine operative64425 private controls PASS; full497/416/1068/1109 +original18/immutable12 and complete actual44 checked. Full modes/draftfalse/null/prospective exact schema controls; failures63648/63650 preserved. Outer closure will include genuine completed own child/operator capture and freeze every own file to literal full0444 with PREPARATION_MANIFEST sole self exclusion. Distinct new adversary and genuine ROOT source reading/approval remain. No Git/index/branch/native/canonical/remote mutation, commit/push, production importcompileexecute, or outreach.\n')
 print(json.dumps({'status':'PASS_SOURCE_ONLY_INSPECTION','actual_closure_child_pid':os.getpid(),'individual_external_refs_rechecked':len(external),'production_executed':False,'future_ROOT_approval_claimed':False,'source_preparation_percent':100,'acceptance_percent':0},sort_keys=True))
CONTRACT='''# PR45 source-only acceptance preparation contract

This family supplies future ROOT administrative source. Its author executed only
handwritten authoring, read-only controls and closure source. Proposed production
sources were read as text, never imported, compiled or executed. No sealer,
acceptance, native/canonical/index/branch/remote mutation, commit/push or external
communication occurred. Source preparation100%; acceptance0%; discovery0%.

Current497+self d136815406dc35265a828deece080813c716c69c2bb915192e606acafdcdd4c5
and dependencies416 e215d1b33f3cdc562aeb53cee76519386d7d203acbe8c1c251370b3fd3bd2410
stay closed. Whole1068+self b372d0fdad3ae40c6a1b82530504dd2584022f15e703b468a8631faa455f9646
and1109 ABSOLUTE excluded identities stay exact. Frozen epoch264c26d539d616b0da6f8df76478a213d20939e4
is historical authority only: four native bodies are independently read from
immutable100644 Git blobs, nine stable bodies remain checked in place. All64
primary/access/cookie/OCR/PDF/pixel bodies and full raw caches/SQL are excluded
from authored copies and publication. Full genuine first-party original/native4
Git streams are procedural evidence, preserved with actual capture metadata.

Actual44 predecessor is mergef369d1e8f74b6462a0866f4b57a888233420a149,
tree6fa2de74e3b7d658cde5b04b94bc699ad6648d88. Its complete actual post and whole
ROOT post retain exact schema pr44-root-complete-actual-post-inspection/v1,
all34 prior states, whole history/proposal/savedplan/inventory/native13 and full
438-overlay/440+self checks, plus actual42112 inspection capture/prelaunch source.
Before45:35targets/43turns/34primaries/one old duplicate. After45 prospectively:
36targets/44turns/35primaries/same duplicate; program35/180=19.4444%, next46.
No retrospective historical acceptance is inferred.

Original18 and immutable12 retain exact bytes. Original Githubbasec6975ca76f9f667f1250ba403d0e6da2aafe14d0,
mergebase01358d66fc67d1c462bddf31c0d4ee5b120e6737 and headd9b4acf5d070d1f04ffac86a4f08916a5629ff16
are distinct; original183402-byte19-path diff and literal snapshot row schema
(bytes/git_mode/git_object/path/relative_path) govern reconstruction. Original
one complete JSONL event consumes1/5; new0/audit0.

Scientific acceptance is UNSOLVED illustrative synchronous obstruction only.
Every fixed coupling is covered by the original full-path conditional-projection
and finite-history L1 proof. The numerical law uses the stated product metric;
other compatible metrics retain failure to zero. Offsets are nonnegative finite
or uniformly tight and may be dependent; escaping offsets are excluded. Setwise
convergence fails; distinct9900005 remains separate. Broader two-process
characterization and exhaustive priority/full published-original comparison are
unresolved. Audit-only alternative constructions do not expand the original.
AMR raw prior is PRESENT nonempty dict matching source_record.upstream_report.
Global SOURCE_PRECISION_QUALIFICATIONS.md applies to all current presentations.
No novelty/priority/solution/prior-literature-resolution/paper/new DOI/tracker/
release/human peer review/formal certification is asserted.

Actual ROOT whole128346-byte record is copied only after genuinely completed
inspection, with entire typed verdict, actual59667 checker,58 full capture reads
and8 genuine frozen4 ROOT body-then-tree queries. DRAFT_ROOT_IMMUTABLE_BINDINGS
and DRAFT_FINAL_PLAN retain false reading flags and null future references/times.
A new distinct source adversary must close SELF_MANIFEST and VERDICT with schema
pr45-acceptance-source-adversary-verdict/v1, verdictPASS_SOURCE_ONLY_SCOPED,
preparation_manifest_sha256 exact, mandatory_corrections[], production_imported_
compiled_executed false, future_acceptance_approved false. ROOT must personally
read the entire source/adversary/captures and separately create adjacent
ROOT_SOURCE_ACCEPTANCE_REVIEW.json using schema
pr45-root-complete-acceptance-source-inspection/v1, status
PASS_ROOT_COMPLETE_ACCEPTANCE_SOURCE_INSPECTION, utc genuine and all flags
all_prepared_source_and_controls_fully_read/exact_preparation_closure_and_full_modes_checked/
all_individual_source_adversary_inputs_checked/all_complete_actual_captures_checked
true, complete_VERDICT_object entire typed verdict, exact source manifest/verdict
refs and preparation SHA, mandatory_corrections[], future_execution_approvedfalse.
This record precedes genuine completed ROOT approval. No empty token or sentinel
supplies approval. Entire actual44 known records, not abbreviated counters or
substituted scientific flags, are required by source guards.

ROOT copies capture_root_final_operation.py literally to adjacent audit root,
reads it fully and binds its exact source. This sealer operator independently
captures then-current native13 bytes/full modes/main before/after with full
prelaunch source/operator, PIDs/UTC/argv/cwd/stdout/stderr. It is not launched here.
ROOT completes the final plan only through declared completion fields and
complete sorted immutable evidence references. The sealer requires --execute,
--root-bindings/SHA,--plan/SHA,--preparation-manifest-sha256 and absent adjacent
--output. It publishes precisely two records plus FINAL_MANIFEST via macOS
absent-only directory rename after full basis replay; all files literal full0444.
All other helpers require --execute/preparation SHA and eight path/SHA pairs:
final-plan/final-receipt/final-manifest/reconciliation-capture/previous-mirror/
previous-post/fresh-preimage/root-bindings. No draft PID or timestamp is invented.

Fresh acceptance authority is a NEW adjacent ROOT record, distinct from frozen
epoch, schema pr45-root-fresh-acceptance-input-preimages/v1; exact keys schema,
approved_by_root,created_utc,reason_date_utc,reason,current_head,files,
protected_foreign_tracked_paths. It requires actual approved ROOT date/reason,
13 exact path/bytes/SHA/full worktree_mode rows and exact sorted explicitly
reviewed protected_foreign_tracked_paths outside owned/native scope. Preflight
index is clean; every dirty tracked path must belong to that declared scope;
full foreign worktree bytes/modes/HEAD/index remain protected. No generic dirty
exception exists. Reassess after shared concurrent writers change state.

Phases preflight/overlay/prepush/finalize remain ROOT-owned; ROOT makes ready/body,
original-head no-ff merge, exact owned staging/commit/push. Overlay has505 files
plus only named whole queue update; accepted canonical507+self. Stage only exact
manifest-covered owned paths, excluding foreign bodies. Preserve Chat/DOI and
all other queue bytes; only Status/Turns/Findings change. Lowercase acceptance
requires actual MERGED remote receipt and full original-head parents/tree.
Mirror requires entire actual44 proposal plus exact one new primary, preserved
all35 old state objects and complete history prefix, original1/5 strict ledger
controls, history-first cooperative locked write, full saved plan reconstruction
and fresh byte-preserving no-op. ROOT_POST_CONTRACT supplies exact typed45 schema,
whole inventory/merge-overlay/canonical/native/proposal/history/capture/flag
requirements; full actual post is personally checked and equals ROOT entire_post.

Every source/control failure remains. Full stat.S_IMODE0444 including special
bits is a local contract; Git preserves only100644, so clean checkout must restore
literal full0444. Source closure excludes only its own PREPARATION_MANIFEST.json.
'''
REPORT='''# PR45 acceptance source preparation

The SOURCE kit is closed after handwritten private controls and full source
inspection. Preparation100%; acceptance0%; mathematical discovery0%. No proposed
production import/compile/execute, sealer, acceptance, native/canonical/index/
branch/remote mutation, commit/push or outreach occurred.

Current497+self/dependencies416 and whole1068+self/excluded1109 remain unchanged.
The genuine ROOT whole record is {rootsha}, including actual59667 complete
inspection and8 frozen4 body/tree queries. Expected copy was made only after that
record existed. Native4 are immutable Git evidence at264c26d; stable9 are live
checked. All64 foreign primary/access/PDF/OCR/pixels and full caches/SQL stay
references in place; first-party actual Git streams alone are procedural copies.

The actual completed44 predecessor is fully typed and hash-bound, including its
42112 ROOT post inspection capture and full prelaunch source. Before45 counts
35targets/43turns/34primary/one existing duplicate; proposed after45 counts
36targets/44turns/35primary/same duplicate, program35/180 and next46. Source guards
preserve entire old states/history/proposal/savedplan/inventory, full505 merge
Git overlay/queue and accepted507+self plus full0444 modes. Original18/immutable12
and19-path183402-byte diff retain exact original row schema and distinct three
base/head identities. Original one-line JSONL1/5,new0,audit0.

UNSOLVED original illustrative all-fixed-couplings synchronous obstruction
remains the only accepted scientific partial. Global stated-metric law,
nonnegative possibly-dependent finite/tight offset and setwise qualifications
apply. Broad characterization and exhaustive priority/full published-original
comparison remain unresolved. AMR prior is PRESENT nonempty dictionary matching
source_record.upstream_report. No novelty/priority/solution/paper/newDOI/tracker/
release/human review or formal certification is claimed.

Own author56831, initial precision repair57659, genuine Root binder61738,
first controls61741 and operative mode repair64423/final controls64425 are fully
captured. Failed63648 expected a double escape although actual query literals
were already correct; failed63650 rejected missing prospective full native modes.
Both complete captures, initial sources and deltas remain. Final64425 handwritten
controls verify all497/416/1068/1109 bodies, all original18/immutable12, entire
actual44 typed records,9 ROOT science flags, source lexing/delimiters without
creating code objects, strict JSON/path/type/one-turn mutants and all4096 modes
plus actual private probes. Its full read-only Git streams and untouched live13/
full modes/main checks remain. This is text-only/private evidence; proposed
production runtime success is unclaimed.

All draft approval fields are false/null. A new distinct adversary must inspect
this exact closure, and ROOT must separately read source/adversary/captures,
complete genuine immutable approval and independently capture fresh native13/
main authority before any production action. Exact scientific/source/whole/
actual predecessor schemas are kept; no shortened completion record is accepted.
CONTRACT.md and ROOT_POST_CONTRACT.json specify these future gates.
'''
if __name__=='__main__':main()
