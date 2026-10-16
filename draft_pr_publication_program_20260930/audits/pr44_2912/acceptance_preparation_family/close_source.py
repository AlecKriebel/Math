"""Own final source inspection only; outer capture closes after genuine child completion."""
from pathlib import Path, PurePosixPath
import datetime as dt
import hashlib
import json
import os
import stat

H=Path(__file__).resolve().parent;A=H.parent;R=H.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def pin(p):
    b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}
def dump(n,o):
    with (H/n).open('x') as f:json.dump(o,f,ensure_ascii=False,sort_keys=True,indent=2);f.write('\n')
def main():
    result=load(H/'OWN_CONTROL_RESULTS.json')
    if result['status']!='PASS_PRIVATE_CONTROLS_ONLY' or result['production_imported_compiled_executed'] is not False:raise ValueError('Own genuine private checks required')
    inputs=load(H/'INPUT_BINDINGS.json');external=list(inputs['pins'].values())+[inputs[n] for n in ['closed_whole_manifest','closed_whole_report','closed_whole_result','closed_root_whole_inspection','previous_mirror','previous_post','previous_root_post']]
    for z in external:
        p=R/z['path'];b=p.read_bytes()
        if p.is_symlink() or not p.is_file() or len(b)!=z['bytes'] or sha(b)!=z['sha256']:raise ValueError('Full external bound source changed')
    captures=[]
    for n in ['AUTHORING_ACTUAL_CAPTURE','SOURCE_REPAIR_ACTUAL_CAPTURE','CONTROLS_ACTUAL_CAPTURE']:
        folder=H/n;o=load(folder/'CAPTURE.json');pre=o['prelaunch']
        if o['actual_execution'] is not True or o['completed'] is not True or type(o['pid']) is not int or o['pid']<=0 or o['exit_code']!=0 or o['status']!='PASS':raise ValueError('Genuine actual source process required')
        if load(folder/'PRELAUNCH.json')!=pre or sha((folder/'PRELAUNCH_SOURCE.py').read_bytes())!=pre['source_sha256'] or sha((folder/'PRELAUNCH_OPERATOR.py').read_bytes())!=pre['operator_sha256']:raise ValueError('Prelaunch fullsource binding')
        for channel in ['stdout','stderr']:
            raw=(folder/o[channel]['path']).read_bytes()
            if len(raw)!=o[channel]['bytes'] or sha(raw)!=o[channel]['sha256']:raise ValueError('Complete actual streams changed')
        captures.append(o)
    rootpost_contract={'schema':'pr44-future-ROOT-whole-post-contract/v1','source_only':True,'future_ROOT_post_completed':False,'predecessor':{'ROOT_schema':'pr43-root-complete-actual-post-inspection/v1','mirror':inputs['previous_mirror'],'post':inputs['previous_post'],'ROOT_post':inputs['previous_root_post'],'actual_post_capture_pid':77832,'merge_commit':'c60255489a342fae02c0acf3d1026255b47be3d1','merge_tree':'fdc2bb213905051a430d24e13afb20e54fa9106a','full_root_entire_post_equals_actual_post':True,'primary_acceptances':33,'targets':34,'consumed_substantive_turns':41,'duplicate_mirrors':1},'future44_required_ROOT_schema':'pr44-root-complete-actual-post-inspection/v1','future44_required_completed_values':{'completed_primary_prs':34,'all34_prior_states_and_full_history_prefix_preserved':True,'current13_match_exact_allowed_acceptance_changes':True,'entire_current_inventory_reconstructed':True,'canonical440_plus_manifest_fullbytes_modes':True,'merge438_overlay_plus_queue_Git_bodies_and_parents':True,'original_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False,'program_completion_percent':34/180*100},'future44_required_entire_post_values':{'pr':44,'status':'PASS','targets':35,'consumed_substantive_turns':43,'primary_acceptances':34,'program_completed_count':34,'program_completion_estimate_percent':34/180*100,'exact_original18_and_OBSTRUCTION_unchanged':True,'whole_current430_and369dependencies_bound':True,'entire_history_prefix_and34prior_states_preserved':True,'one_present_primary_event':True,'new_duplicate_native_acceptance_added':False,'new_proof_turns':0,'current_metadata_present_null':True,'fresh_native_mirror_noop':True,'full_target_resolved_in_prior_published_literature':False,'prior_publication_doi':None,'full_problem_solved_by_project':False,'full_problem_solved':False,'novelty_claimed':False,'paper_or_new_doi_or_tracker':False,'scientific_completion_estimate_percent':0,'workflow_completion_estimate_percent':100},'future44_required_complete_inspections':['Every old state object exactly typed preserved, set(old)|{2912} equals entire new state; new unsolved2/5 source-only present event and no invented history','Whole history bytes equal retained full prefix plus exactly one planned event, not only length/count/hash','Complete mirror proposal equals entire actual43 predecessor plus precisely PR44 primary; duplicate list byte-semantics preserved','Complete saved native plan rebuilt from entire actual preflight state/history at same timestamp and entire typed equality; fresh replay byte-preserving noop','Entire180-row inventory derived from actual preflight bytes, exact selected44 accepted fields/clock/count/next45 metadata, all179 other rows preserved','Full438-file original-head merge overlay and full queue Git100644 bodies; originalHEAD c772dc5b851ec91da9d46d534577609e5d3ca389 is exact second parent; actual main preflight is exact first parent; actual accepted merge/tree equals fresh remote/prepush/final receipts','Full accepted440-member+self canonical worktree closure and every literal full0444 file; original18 archive and twelve immutable bodies byte exact','All native13 actual worktree bytes/modes equal precisely allowed queue/inventory/state/history changes; nine stable bodies unaffected','All six actual ROOT phase captures: preflight,overlay,prepush,finalize,mirror,post; complete prelaunch sources/operators/argv/cwd/UTC/PIDs/fullstdout/fullstderr. Final sealer separate actual unchanged-native13/HEAD capture is also bound','Exact future post fullobject equals ROOT entire_post with scalar types; no unsupported prior schema substitutions','All no solution/novelty/paper/new DOI/tracker flags and both scientific gaps remain globally explicit']}
    dump('ROOT_POST_CONTRACT.json',rootpost_contract)
    dump('CLOSURE_SOURCE_INSPECTION.json',{'schema':'pr44-owned-source-final-inspection/v1','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_closure_child_pid':os.getpid(),'status':'PASS_SOURCE_ONLY_INSPECTION','complete_source_captures':captures,'individual_external_refs_rechecked':len(external),'external_refs':external,'production_imported_compiled_executed':False,'ROOT_approval_or_acceptance_claimed':False,'private_control_result':pin(H/'OWN_CONTROL_RESULTS.json'),'source_preparation_completion_percent':100,'acceptance_completion_percent':0,'discovery_completion_percent':0})
    report='''# PR44 acceptance source preparation

The source kit is prepared and privately checked. No acceptance, sealer, original-
head integration, native mirror, staging, branch or remote operation was executed.
Completion100% source preparation;0% acceptance and0% mathematical discovery.

The current430+self and369 dependency packet, new whole96+self and964 individually
excluded input identities are unchanged. The exact actual ROOT whole record is
54c0944b7e6892ed0e04cab2a58432feb2afbf3694a04073f036fbeda466d1dc,
including eight genuinely captured independent frozen native4 Git queries. The
initial ROOT record with [] arrays is retained by ROOT and individually bound;
the initial author's expected copy is preserved here. The source basis requires
nine stable native inputs among964 and independently reads immutable Git native4.
No archive epoch is rebound to live native state.

PR43's actual completed post/whole ROOT post/mirror schema and genuine PID77832
capture are the predecessor. Before44:34targets/41turns/33primary/one old duplicate.
Prospectively after44:35targets/43turns/34primary/the same duplicate and program34/180.
The proposed original-head merge has438 canonical overlay files plus only the
selected whole queue change. Final canonical acceptance adds two records and its
self-excluded manifest:440 members plus MANIFEST.json. The full ROOT post contract
requires whole inventory, all34 prior state objects and the full history prefix,
original/accepted heads/parents/tree and publication flags; no42 substituted prior.

Both realization gaps remain explicit. The partial is the standard finite-support
meridional duality kernel, sufficient relative-degree-one pair-map criterion and
conditional nonzero integral quotient for the specified abstract group-pair.
Original2/5,new0,audit0; UNSOLVED; no novelty, solution, paper/newDOI/tracker or human
review. Global category, source, integral and historical qualifications persist.

Own genuine authoring99306, source-repair3789 and handwritten-control8465 captures
retain complete prelaunch sources and streams. Source repair preserves seven
initial generated bodies and a complete patch: direct repr slicing repairs two
lexical string literals; exact current-manifest keys replace inherited43 keys;
native4 is independently immutable rather than incorrectly required among964;
inherited43 scientific prior-resolution/DOI claims are removed from44 post; count
and two-turn prose is corrected. These are own drafting defects and do not alter
the candidate. The initial captured author source reproduces the initial state;
the separate captured repair reproduces the final proposed source.

Private controls read every candidate/whole/dependency/foreign bound body, actual43
post and full actual44 ROOT objects, check source lexing/delimiters without creating
an executable code object, and independently query frozen4 with complete actual
Git streams. They reject strict JSON/path/type/two-turn-ledger mutants and check
all4096 full permission modes, plus actual private permission probes. Every live
native13 body and main HEAD is preserved. These controls inspect handwritten
predicates and calculations; they are no claim of proposed production runtime
success or geometric realization.

A distinct new source adversary must read this exact closure. All approval drafts
have false read flags and null reference/time fields; no sentinel exists. Genuine
ROOT separately reads everything and binds its whole source-adversary inspection
before completing a plan and launching any proposed operation. Raw cache and
third-party PDF/text/pixels are excluded from authored copies and publication;
all individual input pins are references. Full0444 is a worktree permission
contract; Git preserves only100644. External communication was not performed.
'''
    with (H/'FINAL_SOURCE_REPORT.md').open('x') as f:f.write(report)
    with (H/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+dt.datetime.now(dt.timezone.utc).isoformat()+' — Final source checkpoint. Completion100% source/0% acceptance/0% discovery. Own8465 private controls PASS; exact two gaps, original2/5,new0,audit0. All source-only drafts still false/null. Final genuine outer capture and every owned file will be included by the outer sole-self-excluded closure, then frozen to full0444. Distinct independent source audit and genuine ROOT approval remain outstanding.\n')
    print(json.dumps({'status':'PASS_SOURCE_ONLY_INSPECTION','actual_closure_child_pid':os.getpid(),'individual_external_refs_rechecked':len(external),'production_executed':False,'future_ROOT_approval_claimed':False,'source_preparation_percent':100,'acceptance_percent':0},sort_keys=True))
if __name__=='__main__':main()
