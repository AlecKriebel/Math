#!/usr/bin/env python3
"""Record the completed, source-matched mathematical adjudication only."""
import datetime, hashlib, json, pathlib, stat
A=pathlib.Path(__file__).resolve().parent
P=A.parent.parent
def pin(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':stat.S_IMODE(p.stat().st_mode)}
def inventory(base): return {p.relative_to(base).as_posix():pin(p) for p in sorted(base.rglob('*')) if p.is_file()}
out=A/'ROOT_MATHEMATICAL_ACCEPTANCE.json'
if out.exists(): raise RuntimeError('Mathematical checkpoint already exists')
families={}
for name,count in [('honda_lifting',68),('intrinsic_invariants',40),('semilinear_modules',59)]:
    capture=A/'root_family_capture_private'/name
    if name=='semilinear_modules':
        closure_path=capture/'close001/ROOT_RECEIPT.json'; post_path=capture/'postcheck001/ROOT_RECEIPT.json'
        closure=json.loads(closure_path.read_text()); post=json.loads(post_path.read_text())
        assert closure['status']=='PASS_ONE_TIME_SEMILINEAR_NATIVE_EXTERNAL_CLOSURE'
        assert post['status']=='PASS_COMPLETE_CLOSED_SEMILINEAR_NAMESPACE_ROOT_READBACK'
        actual=capture/'close001/actual_outer_sealer.json'
        assert json.loads(actual.read_text())['exit_status']==0
    else:
        closure_path=capture/'closure001/ROOT_CLOSURE_RECEIPT.json'; post_path=capture/'postseal001/ROOT_RECEIPT.json'
        closure=json.loads(closure_path.read_text()); post=json.loads(post_path.read_text())
        assert closure['status']=='PASS_EXACT_ONE_TIME_REVIEWED_FAMILY_CLOSURE'
        assert post['status']=='PASS_ROOT_EXTERNAL_READONLY_COMPLETE_FAMILY_REPRODUCTION' and post['stage']=='post_seal'
    current=inventory(A/name)
    assert current==closure['whole_namespace_after'] and len(current)==count
    assert post['namespace_file_count']==count
    families[name]={'namespace_file_count':count,'closure_receipt':pin(closure_path),'postseal_root_receipt':pin(post_path),'whole_current_namespace':current,'family_completion_estimate_percent':100}
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
record={'utc':utc,'status':'MATHEMATICS_ACCEPTED_THREE_INDEPENDENT_FAMILIES_AND_ROOT','problem_id':'30005649','pr':344,'submitted_head':'86a758b1cc9c94322ce6afc3d17150fa2c90327a','submitted_base':'bd0b6f8ffe4382fff9f1a7cbaf7755bd058494c4','submitted_status':'claimed_solved','submitted_turns':'1/5','exact_target':'Unnumbered higher-n automatic Cartier self-duality question following Takao Proposition2, printed2479, OWR42/2023, under its special-fiber qss hypothesis.','strongest_verified_result':'For every prime p>3 and n>=3 over k=an algebraic closure of F_p, the explicit finite Honda datum gives a p-killed finite flat commutative W(k)-group of rank p^(2n) with qss special fiber; both special fiber and lift fail Cartier self-duality.','mathematical_completion_estimate_percent':100,'acceptance_publication_workflow_percent':30,'root_source_only_gate':pin(A/'ROOT_SOURCE_ONLY_GATE.json'),'root_first_candidate_gate':pin(A/'ROOT_FIRST_CANDIDATE_GATE.json'),'root_original_git_verification':pin(A/'ROOT_FROZEN_GIT_VERIFICATION.json'),'root_whole_submitted_reproduction':pin(A/'ROOT_SUBMITTED_REPRODUCTION.json'),'root_odd_degree_verification':pin(A/'ROOT_ODD_DEGREE_VERIFICATION.json'),'snapshot':inventory(A/'snapshot'),'families':families,'no_unresolved_mathematical_defect_found':True,'scope_limits':['No Coleman/torsion/Jacobian or polarization result.','The qss filtration is required for the special fiber, not lifted over W(k).','Classical Dieudonne/finite-Honda/superspecial classification inputs are cited and their hypotheses checked, not newly proved.','Finite controls corroborate symbolic all-field proofs.','Only three of ten historical private source captures independently reproduced; seven ancillary old captures remain historical testimony.','One family saw a late sibling summary after its proof/tests/report were complete; dated exposure and historical versions retained, no mathematical changes.'],'remaining_gates':['Deep current priority audit with original-problem and stronger-classification comparison.','Concise preprint and portable verification package.','Sequential NEW adversarial full-package reviews with all findings resolved.','Exact live PR acceptance/merge, production Zenodo publication and independently verified one-time Google tracker append.'],'pr_merged':False,'published':False,'paper_created':False,'priority_complete':False}
out.write_text(json.dumps(record,indent=2)+'\n')
(A/'README.md').write_text('# PR344 acceptance audit\n\nMathematical validation is complete (100%): the root and three independent families verified the exact special-fiber qss counterexample, its finite Honda lift, the all-field duality obstruction, and the all-n extension. Actual native reproductions and complete closed evidence inventories passed. The submitted status and turn count remain claimed_solved,1/5.\n\nFull acceptance/publication workflow:30%. Priority audit, paper/package preparation, sequential new preprint adversaries, exact live merge and publication/tracker steps remain pending. No PR merge or external publication has occurred. See ROOT_MATHEMATICAL_ACCEPTANCE.json and the dated root report/log for scope, evidence and provenance limits.\n')
message='\n### '+utc+' — completed root mathematical adjudication\n\nAll three materially independent source-first families passed and were precisely closed after full proof/code/manifest/native-evidence review and independent root external whole-output replays. Closed file counts: Honda68, intrinsic40, semilinear59; complete bodies/modes unchanged on post-seal readback. The semilinear late summary exposure occurred after its independent proof/tests/report and is retained honestly; its actual outer closure exit0 was captured externally. No mathematical defect remains. Verified result: all p>3,n>=3 algebraically closed counterexamples to the exact special-fiber-qss automatic self-duality question, with actual finite Honda realization. Mathematical validation100%; full acceptance/publication workflow30%. Priority, preprint, fresh adversarial reviews, merge/deposit/tracker remain open. No new original proof-search turn or source-status change.\n'
with (A/'RESEARCH_LOG.md').open('a') as f: f.write(message)
with (A/'ROOT_MATHEMATICAL_REVIEW.md').open('a') as f: f.write(message)
with (P/'RESEARCH_LOG.md').open('a') as f: f.write(message)
status_path=P/'SHARED_GIT_WINDOW_STATUS.json'; status=json.loads(status_path.read_text())
assert status['shared_git_writes_paused'] is False
status.update({'utc':utc,'descending_344_provisional_math_percent':100,'descending_344_mathematical_verification_complete':True,'descending_344_workflow_percent':30,'descending_344_priority_complete':False,'descending_active_pr':344})
status_path.write_text(json.dumps(status,indent=2)+'\n')
print(json.dumps({'status':record['status'],'utc':utc,'math_percent':100,'workflow_percent':30,'record':str(out),'record_sha256':pin(out)['sha256']},indent=2))
