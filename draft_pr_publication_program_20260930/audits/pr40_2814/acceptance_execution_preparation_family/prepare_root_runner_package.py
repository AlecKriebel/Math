#!/usr/bin/env python3
"""Own finite source/data authoring only; never import, compile, or run candidates."""
import ast
import datetime as dt
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat

R = Path('/Users/alec/Documents/Math')
A = R/'draft_pr_publication_program_20260930/audits/pr40_2814'
S = A/'acceptance_execution_preparation_family/integration_source_revision_v2'
P = A/'root_runner_preparation_family'
W = A/'execute_root_acceptance_revised.py'
A39 = A.parent/'pr39_9500008'
PREP = 'e5f0ce1f9cbc890767ef8131ac760d39562c9fba0faf41df208c3d0ebb3832ba'
FIVE = {
 'pr40_guards.py':'1382ae7f88bd6ace26eb8be09386c7c5d1076e20cfe470824a54945377e936d6',
 'seal_final_evidence.py':'acca1d4777cce70f3bf209bfd2b5a722c7ecbb4bfc6873a6736b187f8404772c',
 'integrate_reviewed_partial.py':'e181ed1725b096608481325b2b60f07654b699b1ce802929251d189d936cac5d',
 'state_mirror_reconciliation.py':'f6dc5e80df90391c8b2e869219ebda5eb3a231a0018efa54efa2c6554e926f1e',
 'verify_post_acceptance.py':'d31b99ec427f5e07d40e58ccd5c913e1dd8281e959ce214f3d184a2917fcae38',
}
CLOSURES = [
 (A/'acceptance_preparation_family','PREPARATION_MANIFEST.json',12,'a7bbde5e024a6e432d7456586651208b3f365170cfc80112e0b98de1cae4c39b'),
 (A/'acceptance_static_adversary_family','FIRST_PARTY_MANIFEST.json',22,'84b0e1c5364fac20617c1242e36c0d5b9130ea2784de81d3557ae8cbe94ab526'),
 (A/'acceptance_execution_preparation_family/integration_source_revision','PREPARATION_MANIFEST.json',15,'65e71adae289b4243036f50be90b28bdeadca3dbd3fd99c5dfc605a72e053c0e'),
 (A/'acceptance_revised_static_adversary_family','FIRST_PARTY_MANIFEST.json',31,'0480281a6dd9629183d1d7e2ad98b098a3b5eae8b8b423dbc4bc72eda85403cf'),
 (A/'acceptance_revised_static_adversary_metadata_qualification_family','FIRST_PARTY_MANIFEST.json',6,'bc05c4971ee61d50080005ce2084597098c97acc8a11f66d95d08514524cb8bb'),
 (S,'PREPARATION_MANIFEST.json',17,PREP),
 (A/'reviewed_candidate','MANIFEST.json',239,'8de92d903edaec7471f4ecc3df443b7e779732b0ee83cdec507c22025bfae25f'),
]

def require(ok,message):
 if not ok: raise ValueError(message)
def sha(raw): return hashlib.sha256(raw).hexdigest()
def stamp(): return dt.datetime.now(dt.timezone.utc).isoformat()
def parse(raw):
 def pairs(items):
  o={}
  for k,v in items:
   require(k not in o,'duplicate JSON key');o[k]=v
  return o
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))
def reg(path):
 require(path.is_file() and not path.is_symlink(),'regular file required '+str(path))
 for p in path.parents:
  require(not p.is_symlink(),'symlink ancestor')
  if p==R:break
 return path.read_bytes()
def pin(path):
 raw=reg(path)
 return {'path':path.relative_to(R).as_posix(),'bytes':len(raw),'sha256':sha(raw),'mode':stat.S_IMODE(path.stat().st_mode)}
def exact(root,names):
 files=set();dirs=set()
 for p in root.rglob('*'):
  require(not p.is_symlink() and (p.is_file() or p.is_dir()),'special/symlink closure')
  (files if p.is_file() else dirs).add(p.relative_to(root).as_posix())
 want={p.as_posix() for n in names for p in PurePosixPath(n).parents if p.as_posix()!='.'}
 require(files==set(names) and dirs==want,'exact recursive closure differs '+str(root))
def closure(root,name,count,digest):
 raw=reg(root/name);require(sha(raw)==digest,'closed manifest pin differs')
 obj=parse(raw);rows=obj['files'];require(type(rows)is list and len(rows)==count,'row count differs')
 names={name}
 for z in rows:
  n=z['path'];p=PurePosixPath(n)
  require(type(n)is str and p.as_posix()==n and not p.is_absolute() and '..'not in p.parts and n not in names,'bad/duplicate path')
  names.add(n);body=reg(root/n);size=z['bytes']if'bytes'in z else z['size']
  require(type(size)is int and len(body)==size and sha(body)==z['sha256'],'whole member differs')
  if n.endswith('.json'):parse(body)
 exact(root,names)
 return {'root':root.relative_to(R).as_posix(),'manifest':pin(root/name),'authored_members_excluding_self':count,'exact_recursive_files_and_directories':True,'foreign_exclusions':[]}
def dump(path,value):
 data=(json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
 with path.open('xb')as f:f.write(data)
def text(path,value):
 with path.open('xb')as f:f.write(value.encode())
def literal(tree,name):
 matches=[n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name)and t.id==name for t in n.targets)]
 require(len(matches)==1,'literal source assignment missing '+name)
 return ast.literal_eval(matches[0].value)

def main():
 before=[closure(*z)for z in CLOSURES]
 require(not P.exists() and not P.is_symlink(),'new source package must be absent')
 wrapper=reg(W);tree=ast.parse(wrapper,filename=str(W))
 require(literal(tree,'PREP')==PREP and literal(tree,'SOURCE_HASHES')==FIVE,'wrapper exact source pins differ')
 require(literal(tree,'CURRENT_PR_AFTER_ACCEPTANCE')==41,'wrong next PR')
 native=list(literal(tree,'NATIVE13'));require(len(native)==len(set(native))==13,'native13 literal differs')
 gates=list(literal(tree,'GATE_NAMES'));require(gates==['final-plan','final-receipt','final-manifest','reconciliation-capture','previous-mirror','fresh-preimage'],'exact gate six differs')
 allowed=literal(tree,'ALLOWED');require(allowed=={'overlay':{'unsolved_math_prioritization/QUEUE.md'},'finalize':{'draft_pr_publication_program_20260930/inventory.json'},'mirror':{'unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}},'phase whitelist differs')
 for name,digest in FIVE.items():
  body=reg(S/name);require(sha(body)==digest,'one of five source pins differs');ast.parse(body,filename=str(S/name))
 imports=[n.module for n in ast.walk(tree)if isinstance(n,ast.ImportFrom)]+[alias.name for n in ast.walk(tree)if isinstance(n,ast.Import)for alias in n.names]
 require(not any('pr40_guards'in s or'integrate_reviewed_partial'in s or'seal_final_evidence'in s for s in imports),'candidate import in outer runner')
 require(b"'--output', final_output.name"in wrapper and b'--fresh-queue-preimage-sha256'not in wrapper,'PR40 final/preflight interface differs')
 require(b'root_full_whole_read_completed=True'in wrapper and b'root_full_whole_scope_read_completed'not in wrapper,'PR40 root scope flag differs')
 require(b'os.O_NONBLOCK'in wrapper and b'os.O_NOFOLLOW'in wrapper and b'renamex_np'in wrapper and b'0x00000004'in wrapper,'regular/atomic controls missing')
 require(b'mode_changes'in wrapper and b'not mode_changes'in wrapper and b'allowed_changed_native_modes=[]'in wrapper,'native modes not protected')
 require(b'reserved_captures'in wrapper and b'final_output.name not in reserved_captures'in wrapper,'reserved phase captures not protected')
 draft=parse(reg(S/'DRAFT_FINAL_PLAN.json'));require(draft['root_full_current_read_completed']is False and draft['root_full_whole_read_completed']is False and draft['independent_whole_current_pass']is False and draft['preparation_manifest_sha256']is None,'inactive original draft differs')
 prototype=A39/'execute_root_acceptance_revised.py';require(sha(reg(prototype))=='2de301f2f37837b8729d606962599c04bd380d1f6473cc4a76a9c46cef1c0b88','whole prototype changed')
 P.mkdir()
 created=stamp()
 contract='''# PR40 proposed ROOT execution wrapper contract

This is a closed SOURCE-ONLY preparation beside the immutable scientific and source review roots. Neither this wrapper nor any of the five candidate helper sources was imported, compiled, or executed while preparing it. Static AST parsing and whole-byte inspection are source-data operations only. ROOT's full reading, a NEW independent review of both cache-corrected v2 and this wrapper, and all actual execution remain PENDING. A false template is never a review or a runtime certificate. Source preparation100%; actual acceptance execution0%; scientific discovery0%. Original0/5,new0,audit0. The project disposition remains UNSOLVED/source hold/valid partial, without novelty, paper, DOI, tracker, release, or separate duplicate20001896 native acceptance. Current model/reasoning/deadline remain present-null.

The standalone source is the adjacent execute_root_acceptance_revised.py, with a byte-identical archival WRAPPER_SOURCE.py.txt here. Its exact SHA, mode and all external inputs are in SOURCE_BINDINGS.json. The source checks its own explicit startup SHA, all seventeen authored v2 preparation members plus literal manifest self, exact recursive directories, all five helper SHAs and0444 modes. It repeats these checks after the child. PREP is e5f0ce1f9cbc890767ef8131ac760d39562c9fba0faf41df208c3d0ebb3832ba; v1/old static reviews remain archival and are never substituted for a new v2/wrapper adversary.

## Full outer interface

Run only from ROOT after full source and argument review. The interpreter is /usr/bin/python3 -B. The source requires macOS, main branch, the exact adjacent pathname, an explicit --execute, and --reviewed-runner-source-sha256 with the entire actual wrapper source SHA. Positional phase is exactly final, preflight, overlay, prepush, finalize, mirror, or post. ROOT retains its complete outer-command stdout/stderr/exit status as well as the published child capture. There is no automatic retry or cleanup.

For final, ROOT must first create ROOT_REVIEWED_FINAL_PLAN.json from the entire v2 DRAFT_FINAL_PLAN.json. Only plan_status, three completed-reading flags and preparation_manifest_sha256 may change to the required reviewed values. All other objects, evidence references, scientific qualifications and null metadata must stay typed-byte-bound. Supply --reviewed-plan-sha256 and --final-output NEW_DIRECT_CHILD_BASENAME. The output must be absent, regular-path-safe and distinct from all seven reserved phase capture names. The wrapper constructs the child's complete argv: /usr/bin/python3 -B ABSOLUTE_V2/seal_final_evidence.py --execute --preparation-manifest-sha256 PREP --plan REPOSITORY_RELATIVE_ROOT_PLAN --plan-sha256 ACTUAL_ROOT_PLAN_SHA --output NEW_DIRECT_CHILD_BASENAME. PR40's mandatory --output is present. The final helper writes only the new adjacent final output; failure or partial output remains for inspection.

For every nonfinal phase, ROOT creates ROOT_REVIEWED_GATE_ARGUMENTS.json with approved_by_root, root_full_runner_and_helper_review_completed and new_independent_runner_review_completed all true ONLY after the actual reviews. Supply --reviewed-gate-arguments-sha256 and --reviewed-previous-mirror-sha256. The latter is an explicit reviewed actual SHA of the completed PR39 state_mirror_bindings.json, presently unknown and never guessed. It must match the full gate map and live bytes. The previous file is exactly audits/pr39_9500008/state_mirror_bindings.json; its full object has29 entries, includes39, excludes40. Parent review and helper semantics establish full prior proposal validity.

The complete explicit_arguments object contains exactly thirteen STRING values: preparation-manifest-sha256; final-plan and final-plan-sha256; final-receipt and final-receipt-sha256; final-manifest and final-manifest-sha256; reconciliation-capture and reconciliation-capture-sha256; previous-mirror and previous-mirror-sha256; fresh-preimage and fresh-preimage-sha256. Every path is repository relative and canonical. All six artifacts are read wholly, hash-checked and mode-bound before and after the child; only the literal previous-mirror may be outside the selected PR40 audit. The other actual gate artifacts must be in PR40 and outside reviewed_candidate and v2. The wrapper appends each of the thirteen explicit helper flags, --execute, and the positional phase only for integrate_reviewed_partial.py. Mirror and post receive no positional phase. DRAFT_ROOT_GATE_ARGUMENTS.json is deliberately rejected because its three review flags are false and unknown values null.

Preflight additionally requires --reviewed-fresh-main-sha256. fresh-preimage must be literal adjacent ROOT_FRESH_MAIN_PREIMAGES.json and the supplied SHA must equal its map SHA. There is no PR39-only --fresh-queue-preimage-sha256 helper flag. ROOT alone creates the fresh metadata AFTER PR39 integration/checkpoint. It contains approved_by_root:true; real aware UTC created_utc no later than invocation; reason_date_utc equal to that UTC date; a stripped substantive reason at least40 characters and six words (ROOT supplies semantic justification); actual independent current_head40hex; whole_queue_sha256; and exactly thirteen ordered path/bytes/SHA rows in the native order of SOURCE_BINDINGS. At preflight all13 full live bytes, actual current HEAD and entire queue must match. The older dated replay HEAD remains archival, without false same-head assertions. No fresh metadata was generated by the source preparer.

Overlay additionally requires --reviewed-automatic-merge-sha256 of ROOT_AUTOMATIC_MERGE_INSPECTION.json. ROOT must read the entire actual automatic/conflicted queue and actual merge stages before approving it. approved_by_root:true and the full live queue SHA are checked and retained. The wrapper adds the exact --merge-queue-preimage-sha256. The helper then independently checks original-head/main/conflict stages and the complete queue replacement semantics.

## Child launch and genuine capture

The selected child is one of the four v2 entry points, selected by the exact phase table: final seal_final_evidence.py; preflight/overlay/prepush/finalize integrate_reviewed_partial.py; mirror state_mirror_reconciliation.py; post verify_post_acceptance.py. The outer source imports only standard-library modules and never a prepared helper. Actual future ROOT invocation launches the child with real subprocess.Popen, cwd equal to the absolute PR40 audit, stdin DEVNULL, full binary stdout/stderr and180-second timeout. Real PID is recorded only after launch. No launch yields actual_execution:false/PID:null; complete launch failure evidence remains. A timeout kills and retains the child's full available output; no timeout can PASS.

Capture destinations are absent direct children of the audit: root_final_reconciliation_actual_capture for final, otherwise root_integration_PHASE_actual_capture. Final capture has exactly four files: literal CAPTURE.json, literal prelaunch_source.py, stdout.bin and stderr.bin. Nonfinal capture has exactly five, adding literal prelaunch_guards.py. Source copies match complete raw bytes and modes. CAPTURE/streams are0600. All source and declared stream names are distinct. CAPTURE records whole argv, cwd, real launch/completion/PID/exit, timezone-aware ordered UTC start/end, full streams' bytes/SHA, source bytes/modes, all13 before/after bytes/modes and HEAD, permitted/actual native changes and full reviewed artifact pins. The final receipt and manifest UTC must lie within the real child interval. Only actual completed positive integer PID, exact integer exit0, no timeout, no outer errors and all checks can yield child-capture status PASS. Root approval alone never yields that status.

Before launch a new unique private stage is created. Every complete file uses exclusive nonsymlink creation, full writes, fchmod, flush and fsync. The stage is fsynced, then published by macOS renamex_np with RENAME_EXCL=4, followed by parent directory fsync. An intervening destination causes atomic refusal, retaining the complete stage and existing target. A failed write leaves its stage; existing capture/final output is never overwritten. A failure before stage creation is retained in the outer command's complete error/exit log. A failure after rename but before parent fsync may leave CAPTURE present; actual outer exit0 is independently required as the witness of durable publication. ROOT must never infer whole action success from CAPTURE alone.

## Independent checks and exact mutation scope

Every phase records all thirteen whole native/inventory files and modes and current HEAD immediately before and after child execution. All13 mode changes are forbidden, including paths whose bytes may change. HEAD must remain unchanged within a child. The exact byte whitelist is queue only for overlay, inventory only for finalize, state/history only for mirror; final/preflight/prepush/post allow zero native byte changes. This is a thirteen-file outer guard, not a blanket whole-repository safety assertion. Canonical scientific/admin writes, helper audit receipts, cooperative lock and specified research logs are controlled by the fully reviewed helper contract and ROOT's independent scope/tree inspection, outside this thirteen-file guard. The wrapper itself does not stage, commit, push, merge, ready, or mutate the remote. Those actual actions belong to ROOT between the prescribed phases.

The corrected v2 helper separately checks the literal three ignored caches cache/problems.json, cache/research_results.json and cache/catalog.sqlite under unsolved_math_prioritization: no entry in actual fresh HEAD or exact merge tree, and full live bytes equal fresh pins. The other ten tracked files (nine at accepted tree with only the separately full-checked queue skipped) require exact tracked blobs. There is no blanket optional path. All13 worktree pins remain live checks in every helper phase. The wrapper never conflates Git absence with absent or optional live data.

After actual final child success the wrapper independently inspects all three output files at0444, exact two-member self-excluding final manifest, full typed scope equal ROOT's plan, entire required receipt including immutable references before/after, plan/sealer pins, false science/shared mutation flags and zero budgets; full stdout actual receipt/manifest hashes; real receipt/manifest UTC inside actual capture interval. No synthesized final PASS is accepted.

After actual finalize/mirror/post success it independently requires typed inventory current_pr41 and completed_count30. Helper checks establish29 primary completions/native30targets/37turns before40,30 primary completions/native31targets/37turns after40, exact preservation of all30 prior state objects and full history prefix, exactly one present primary acceptance event and no duplicate20001896 state. Queue0/5, original13, SOURCE_STATUS, current239, prior and zero ledger remain exact. ROOT finishes with fresh mirror no-op and post verification, then its own checkpoint/commit/push. The current work provides SOURCE ONLY; no such action has occurred here.
'''
 text(P/'CONTRACT.md',contract)
 source_paths=[W]+[S/n for n in FIVE]+[S/n for n in ['PREPARATION_MANIFEST.json','CONTRACT.md','DRAFT_FINAL_PLAN.json','SCIENTIFIC_SCOPE.json','CACHE_GIT_SCOPE.json','PREDECESSOR_REVISION_BINDINGS.json','REVISION_BINDINGS.json','INPUT_BINDINGS.json','CHANGE_RECORD.json','SOURCE_CHANGES.patch']]
 source_paths += [prototype,A39/'root_runner_revision_preparation_family/CONTRACT.md',A39/'root_runner_revision_preparation_family/SOURCE_BINDINGS.json',A39/'root_runner_revision_preparation_family/ROOT_REVIEW_CHECKLIST.md',A39/'root_runner_revision_preparation_family/READ_NOTES.md',A39/'root_runner_revision_preparation_family/MANIFEST.json']
 source_paths += [A/'acceptance_revised_static_adversary_family/REPORT.md',A/'acceptance_revised_static_adversary_metadata_qualification_family/CURRENT_ASSESSMENT.json',A/'acceptance_revised_static_adversary_metadata_qualification_family/CURRENT_READ_COVERAGE.json',A39/'inspect_actual_final_and_prepare_preflight_v2.py',A39/'ROOT_ACTUAL_FINAL_GATE_INSPECTION.json']
 bindings={'schema':'pr40-proposed-root-runner-source-bindings/v1','prepared_utc':created,'status':'SOURCE_ONLY_NEW_REVIEW_PENDING','approved_by_root':False,'root_full_runner_and_helper_review_completed':False,'new_independent_runner_review_completed':False,'wrapper_import_compile_execution':False,'candidate_helper_import_compile_execution':False,'actual_root_execution':False,'actual_pid':None,'actual_exit_code':None,'actual_current_head':None,'actual_fresh_created_utc':None,'actual_previous_pr39_mirror_sha256':None,'preparation_manifest_sha256':PREP,'whole_source_pins':[pin(p)for p in source_paths],'immutable_exact_closures':before,'native13_ordered_paths':native,'ignored_cache3_exact_paths':native[8:11],'helper_gate_names':gates,'helper_gate_string_count':13,'current_pr_after_acceptance':41,'allowed_native_byte_changes':{k:sorted(v)for k,v in allowed.items()},'allowed_native_mode_changes':[],'original_substantive_attempts':0,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False,'partial_valid':True,'novelty_claimed':False,'source_hold':True,'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'paper_or_new_doi_or_tracker':False,'source_preparation_completion_estimate_percent':100,'actual_execution_completion_estimate_percent':0,'scientific_completion_estimate_percent':0}
 dump(P/'SOURCE_BINDINGS.json',bindings)
 args={'preparation-manifest-sha256':PREP}
 for n in gates:args[n]=None;args[n+'-sha256']=None
 args['final-plan']=(A/'ROOT_REVIEWED_FINAL_PLAN.json').relative_to(R).as_posix()
 args['previous-mirror']=(A39/'state_mirror_bindings.json').relative_to(R).as_posix()
 args['fresh-preimage']=(A/'ROOT_FRESH_MAIN_PREIMAGES.json').relative_to(R).as_posix()
 require(len(args)==13,'draft13keys')
 dump(P/'DRAFT_ROOT_GATE_ARGUMENTS.json',{'schema':'pr40-root-gate-arguments-draft/v1','status':'DRAFT_REQUIRES_ACTUAL_REVIEWED_ARTIFACTS','approved_by_root':False,'root_full_runner_and_helper_review_completed':False,'new_independent_runner_review_completed':False,'explicit_arguments':args,'actual_pid':None,'actual_execution':False})
 dump(P/'DRAFT_ROOT_FRESH_MAIN_PREIMAGES.json',{'schema':'pr40-root-fresh-main-preimage-draft/v1','status':'DRAFT_CREATE_ONLY_AFTER_PR39_INTEGRATION','approved_by_root':False,'created_utc':None,'reason_date_utc':None,'reason':None,'current_head':None,'whole_queue_sha256':None,'files':None,'required_ordered_paths':native,'actual_execution':False,'actual_pid':None})
 dump(P/'DRAFT_ROOT_AUTOMATIC_MERGE_INSPECTION.json',{'schema':'pr40-root-automatic-merge-inspection-draft/v1','status':'DRAFT_REQUIRES_ROOT_WHOLE_ACTUAL_QUEUE_AND_STAGE_READING','approved_by_root':False,'created_utc':None,'whole_queue_sha256':None,'actual_main_head':None,'actual_merge_head':None,'queue_conflict_stages':None,'entire_actual_queue_read_by_root':False,'actual_execution':False,'actual_pid':None})
 checklist='''# ROOT review checklist — all actual work PENDING

- Read the complete adjacent wrapper and byte-identical archival copy, all five v2 helper sources (696 lines), complete v2 contract/scientific scope/final draft and seventeen-member closure plus literal self. Compare each raw SHA and0444 modes with SOURCE_BINDINGS and v2 manifest. Pin the entire wrapper separately. Read this full contract and complete argument templates. Prior source author reading is not ROOT's reading.
- Have a NEW independent adversary inspect cache-corrected v2 and this complete wrapper package. Fix mandatory issues in a new adjacent revision and refresh the review; preserve prior exact closures. Archived v1 static review31+self and qualification6+self do not certify S7 or this wrapper. No existing historical PASS may be promoted.
- Review exact scientific partial/source hold credit and limitations: published orientable cusp Kuhlmann2006 Th1.1; nonorientable cusp Xia v1 Th1.2/4.1 as preprint; no novel theorem, full recursive certification, human peer review or whole-source-unexposed claim. Original13/SOURCE_STATUS/current239 and zero ledger remain exact; original0/5,new0,audit0; current model/reasoning/deadline null; no paper/DOI/tracker.
- Create full ROOT_REVIEWED_FINAL_PLAN only after actual ROOT reading. Change only allowed status, three flags and e5f0ce1f… preparation SHA. Pin entire plan. Run final with explicit source/plan/output arguments, absent direct-child output distinct from every reserved capture name. Retain actual outer stdout/stderr/exit and child PID/full streams/argv/cwd/UTC/modes/HEAD/native13. Verify whole actual final output closure and capture plus durable outer exit0. Failed or partial outputs/stages are retained without automatic retries.
- AFTER actual PR39 integration/checkpoint, read and pin actual complete PR39 state_mirror_bindings.json (29 prior entries, includes39, excludes40). Its SHA is currently unspecified. Supply that actual reviewed SHA explicitly on every nonfinal outer invocation; never copy a future guessed SHA or a pending PR39 source draft.
- Only then create new ROOT_FRESH_MAIN_PREIMAGES.json from the entire actual thirteen files, preserving ordered exact paths/typed integer sizes/SHA. Record current actual HEAD separately from dated replay, real aware UTC/date-consistent substantive rebase reason, whole queue SHA and explicit ROOT approval. Prove exact3 caches absent in selected Git HEAD with full regular worktree bytes bound; other tracked10 HEAD blobs exact. Never infer optional data from ignored status. Pin full fresh object.
- Construct full ROOT_REVIEWED_GATE_ARGUMENTS with exactly thirteen string values and actual SHA/path pairs for all six gates; make three review flags true only after reviews. Pin complete object. Execute preflight with complete map, wrapper, prior mirror and fresh-object SHA. Require full ROOT outer exit0 plus genuine complete child capture; helper checks absent selected/duplicate paths/state, clean index, tracked foreign logs, native30targets/37turns and29 primaries.
- ROOT alone makes PR40 ready with the exact accepted body and starts exact original-head no-ff/no-commit merge. Read entire actual automatic/conflicted queue and actual stages. Create/pin ROOT_AUTOMATIC_MERGE_INSPECTION and run overlay with its full SHA. Check only named queue Status/Turns/Findings changed, Chat/DOI/unselected bytes preserved; canonical exact science/admin overlay and archived pending administration; all13 modes unchanged.
- ROOT alone stages exact owned canonical/queue paths and commits exact two-parent merge. Run prepush with unchanged complete gates. Independently inspect full merge tree/canonical Git modes and blobs/changed-path whitelist, original head/base, queue and foreign logs. Exact cache3 Git absence plus whole live bytes; tracked9 tree exact with only separately checked queue excluded. ROOT alone performs actual push, then reads actual MERGED/nondraft/original-head/body/date/tree.
- Run finalize then mirror then post under unchanged actual complete gate pins. Each requires real positive child PID, complete streams, actual outer exit0, exact sources/modes/UTC/HEAD and all13 before/after checks. Native byte changes only queue overlay/inventory finalize/state+history mirror; no modes change in any phase. Review helper canonical/receipt/log writes outside this thirteen-file outer guard separately.
- Verify typed current_pr41/completed_count30; native31targets/37turns; all30 prior state objects and whole history prefix unchanged; exactly one present primary event for2814, no duplicate20001896 event/state; original0/5 plus new0/audit0; exact canonical closure at0444; all239 current/all216 dependencies; full prior proposal/zero ledgers; fresh mirror byte-preserving no-op. ROOT checkpoint/commit/push remains separate from this source preparation.

ROOT completed reading: PENDING. New independent v2 review: PENDING. New independent wrapper review: PENDING. Actual source plan/reconciliation/preflight/merge/push/finalize/mirror/post: PENDING. No future PID, runtime HEAD, fresh clock, PR39 SHA or PASS is declared here.
'''
 text(P/'ROOT_REVIEW_CHECKLIST.md',checklist)
 text(P/'READ_NOTES.md','''# Source author read record

This preparation adapts the whole PR39 execute_root_acceptance_revised.py (18198 bytes, SHA2de301f2f37837b8729d606962599c04bd380d1f6473cc4a76a9c46cef1c0b88), its full contract/checklist/source bindings/read notes, to exact PR40 interfaces. The source author read all670 v1 helper lines earlier; after S7, read all696 v2 helper lines in bounded full-source excerpts (guard1–260/261–436, sealer1–30, integration1–70/71–119, mirror1–79, post1–32). A combined source read was truncated and was not counted as complete; all affected sources were reread separately before closing this package. Entire v2 contract and DRAFT_FINAL_PLAN were read, scientific credits and immutable scope compared. The new wrapper was read in full1–240/241–end, then its reserved-name/null-metadata edit separately reviewed. Own AST parsing/hashing below is source-data inspection only, never candidate execution.

PR40-specific interfaces corrected relative to39: final --output mandatory; nonfinal thirteen exact flags (one prep plus six path/SHA pairs); no preflight-only fresh-queue helper flag; ROOT plan root_full_whole_read_completed spelling; fresh approved_by_root/current_head/realUTC/date/reason requirements; unknown completed39 mirror SHA required explicitly; inventory current_pr41. The v2 guard repairs exact ignoredcache3 Git absence while retaining full13 live checks. Prior15+self, static31+self, qualifier6+self and original12/22/current239 closures are preserved. Their archival assessments do not constitute a fresh v2 or wrapper PASS.

This is source author reading, not a claim that ROOT or a fresh adversary has read this package. It performs no new mathematical attempt, no source-first independent reconstruction, no recursive external-proof certification, no execution of mathematical or scientific helpers and no native/Git/remote writes. The underlying qualified whole-current scientific audit and ROOT reading remain bound archived evidence with their explicit exposure/standard-input limitations. Actual acceptance remains pending ROOT action. Original0/5,new0,audit0; discovery0%; preparation100%; execution0%.
''')
 static={'schema':'pr40-own-source-data-static-inspection/v1','utc':stamp(),'scope':'Own finite AST/literal/hash/closure inspection of source data; no candidate import, compilation or execution','wrapper_pin':pin(W),'wrapper_lines':len(wrapper.splitlines()),'helper_sources':[{'pin':pin(S/n),'lines':len(reg(S/n).splitlines())}for n in FIVE],'helper_line_total':sum(len(reg(S/n).splitlines())for n in FIVE),'wrapper_imports':imports,'all_exact_prior_closures_checked':before,'static_checks_completed':['wrapper PREP equals exactv2 manifest pin','five source literal SHAs equal wholebytes','native13 literal unique ordered paths','current_pr_after_acceptance integer41','exact sixgate names and thirteen full flags','phase byte whitelist and zero allowed modechanges','PR40 final output flag/no invalid preflightflag','whole plan flag spelling','regular-file nonblocking/nonsymlink guard','macOS absent-only renamex_np bit4','reserved phasecapture names excluded from final output','inactive full finaldraft flags/null prep','whole PR39 prototype rawSHA bound','all candidate AST parsed only'],'candidate_import_compile_execution':False,'actual_root_execution':False,'actual_pid':None,'actual_exit_code':None,'new_independent_review_completed':False,'status':'SOURCE_DATA_CHECKS_COMPLETED_RUNTIME_UNTESTED','new_substantive_attempts':0,'audit_turns':0}
 require(static['helper_line_total']==696,'helper line total differs')
 dump(P/'STATIC_SOURCE_INSPECTION.json',static)
 text(P/'README.md','''# PR40 ROOT runner source-only preparation

Read CONTRACT.md, complete SOURCE_BINDINGS.json, false/null DRAFT files and ROOT_REVIEW_CHECKLIST.md together with the entire adjacent execute_root_acceptance_revised.py and all five v2 helpers. WRAPPER_SOURCE.py.txt is an exact archival source copy. This package has no actual ROOT runtime result or fresh native metadata. ROOT reading and a NEW independent adversary are pending. Closed original/v1/review/current packets remain byte unchanged. Original0/5,new0,audit0, UNSOLVED source hold partial; no paper/DOI/tracker. Preparation100%, execution0%, scientific discovery0%.
''')
 text(P/'RESEARCH_LOG.md','# PR40 ROOT runner source-only preparation log\n\n## '+created+' — full source preparation\n\nAdapted complete reviewed39 wrapper to exact40 v2 five source interfaces/pins, fresh13 contract and explicit unknown predecessor39 SHA. All source author AST/data checks complete without candidate import/compile/execution. Reserved capture-name guard and present-null current metadata added. Original/v1/static/qualifier/current closures preserved; actual ROOT and fresh independent reviews remain pending. Source preparation100%; actual execution0%; mathematical discovery0%; original0/5,new0,audit0. No Git/index/native/canonical/remote writes or paper/DOI/tracker.\n')
 with (P/'WRAPPER_SOURCE.py.txt').open('xb')as f:f.write(wrapper)
 after=[closure(*z)for z in CLOSURES];require(after==before,'closed predecessor changed during authoring')
 require(reg(W)==wrapper,'standalone wrapper changed during authoring')
 files=[]
 for p in sorted(P.iterdir()):
  body=reg(p)
  if p.suffix=='.json':parse(body)
  files.append({'path':p.name,'bytes':len(body),'sha256':sha(body)})
 require(len(files)==11,'source package authored count differs')
 mf={'schema':'pr40-proposed-root-runner-exact-source-closure/v1','closed_utc':stamp(),'status':'CLOSED_SOURCE_ONLY_NEW_REVIEW_PENDING','self_excluded_paths':['MANIFEST.json'],'files_count':len(files),'directories':[],'files':files,'foreign_excluded_prefixes':[],'scratch_exclusions':[],'actual_execution':False,'actual_pid':None,'actual_exit_code':None,'root_full_review_completed':False,'new_independent_review_completed':False,'prepared_helper_import_compile_execution':False,'wrapper_import_compile_execution':False,'preparation_manifest_sha256':PREP,'standalone_wrapper_pin':pin(W),'original_substantive_attempts':0,'new_substantive_attempts':0,'audit_turns':0,'source_preparation_completion_estimate_percent':100,'actual_execution_completion_estimate_percent':0,'scientific_completion_estimate_percent':0}
 dump(P/'MANIFEST.json',mf)
 for p in P.iterdir():p.chmod(0o444)
 result=closure(P,'MANIFEST.json',11,sha(reg(P/'MANIFEST.json')))
 require(all(stat.S_IMODE(p.stat().st_mode)==0o444 for p in P.iterdir()),'closed package must be0444')
 print(json.dumps({'status':'SOURCE_ONLY_PACKAGE_CLOSED','package':result,'standalone_wrapper_pin':pin(W),'own_utility_pid_note':'PID captured externally by own authoring capture','candidate_helpers_import_compile_execution':False,'wrapper_import_compile_execution':False,'actual_root_execution':False,'new_independent_review_completed':False},sort_keys=True))

if __name__=='__main__':main()
