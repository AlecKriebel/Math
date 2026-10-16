"""Verify new source-family custody and author actual ROOT scientific gate, without native mutations."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import sys

if sys.flags.optimize or not __debug__ or not sys.flags.ignore_environment or not sys.flags.dont_write_bytecode:
    raise RuntimeError('Invoke -E -B without optimization')
A=Path(__file__).resolve().parent
P=A.parents[1]
R=P.parent
F=A/'ROOT_provided_source_final_readback_20261004'
def sha(b):return hashlib.sha256(b).hexdigest()
def check(row,root):
    p=Path(row['path'])
    if not p.is_absolute():p=root/p
    if p.is_symlink() or not p.is_file():raise RuntimeError('Missing/linked custody member: '+str(p))
    b=p.read_bytes()
    if sha(b)!=row['sha256'] or ('bytes' in row and len(b)!=row['bytes']):raise RuntimeError('Custody mismatch: '+str(p))
    return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
families=['provided_source_mechanism_audit_20261004','provided_source_analytic_audit_20261004','provided_source_HL2019_status_audit_20261004','provided_priority_final_adversary_20261004']
inventories=[]
for name in families:
    d=A/name;j=json.loads((d/'MANIFEST.json').read_bytes())
    public=j.get('outputs',j.get('files',j.get('repository_inventory')))
    if not isinstance(public,list):raise RuntimeError('Unknown manifest shape')
    public_verified=[check(x,d) for x in public]
    private=[]
    if name==families[0]:private=[check(x,d) for x in json.loads((d/'PRIVATE_ASSET_MANIFEST.json').read_bytes())]
    if name==families[1]:private=[check(x,d) for x in json.loads((d/'source_pins.json').read_bytes())['private_artifact_inventory']]
    if name==families[2]:private=[check(x,Path(j['private_cache_root'])) for x in j['private_inventory']]
    executions=[]
    if name==families[0]:
        for x in (d/'PROVENANCE.jsonl').read_text().splitlines():
            q=json.loads(x)
            if q['exit_code']!=0 or not isinstance(q['pid'],int) or q['pid']<=0:raise RuntimeError('Mechanism process failed')
            for stream in ('stdout','stderr'):
                path=q.get(stream+'_path','/Users/alec/.cache/codex-pr65-priority-20261004/mechanism-independent-20261004/'+q['id']+'.'+stream)
                check({'path':path,'sha256':q[stream+'_sha256']},d)
            executions.append({'actual_child_pid':q['pid'],'exit_code':q['exit_code'],'argv':q['argv']})
    else:
        pattern='*.receipt.json' if name==families[2] else 'receipts/*.json'
        for p in sorted(d.glob(pattern)):
            q=json.loads(p.read_bytes())
            if 'exit_code' not in q:continue
            if q['exit_code']!=0:raise RuntimeError('Relied-on process failed: '+str(p))
            pid=q.get('child_pid',q.get('pid',q.get('actual_child_pid')))
            if not isinstance(pid,int) or pid<=0:raise RuntimeError('Actual child PID not recorded: '+str(p))
            for stream in ('stdout','stderr'):
                if isinstance(q.get(stream),dict):check(q[stream],d)
                elif stream+'_private_path' in q:check({'path':q[stream+'_private_path'],'sha256':q[stream+'_sha256']},d)
                elif stream+'_path' in q:check({'path':q[stream+'_path'],'sha256':q[stream+'_sha256']},d)
                else:raise RuntimeError('Missing actual stream shape: '+str(p))
            executions.append({'actual_child_pid':pid,'exit_code':q['exit_code'],'argv':q['argv']})
    inventories.append({'family':name,'public_member_count':len(public_verified),'private_member_count':len(private),'genuine_receipt_count':len(executions),'manifest_sha256':sha((d/'MANIFEST.json').read_bytes()),'executions':executions})
verdict=json.loads((A/families[3]/'VERDICT.json').read_bytes())
if verdict['blocking_findings'] or verdict['required_repairs'] or verdict['verdict']!='PASS_FOR_PROSPECTIVE_ATTRIBUTED_ALREADY_SOLVED_RESEARCH_DISPOSITION':raise RuntimeError('Fresh final adversary did not pass')
for row in json.loads((A/'attributed_prior_result_preparation_20261004/MANIFEST.json').read_bytes())['files']:check(row,A/'attributed_prior_result_preparation_20261004')
operator=A/'ROOT_integrate_attributed_prior_result_20261004.py'
compile(operator.read_bytes(),str(operator),'exec')
stamp=dt.datetime.now(dt.timezone.utc).isoformat()
readback={'UTC':stamp,'actual_controller_pid':os.getpid(),'new_source_family_custody':inventories,'ROOT_personally_read_all_four_new_reports':True,'ROOT_personally_read_all_four_verdicts':True,'ROOT_complete_1966_bodies_and_all16_scans_read':True,'ROOT_HL2019_complete_target_update_and_imprint_pixels_read':True,'ROOT_AAN_primary_pixels_printed':[320,326,327,328,329],'byte_custody_does_not_itself_certify_math_or_priority':True,'first_failed_status_scan_missing_PID_not_retrospectively_invented':'Declared in source family report; relied-on source scan rerun with genuine success receipts; independent ROOT and other source reads separately substantiate findings.','prospective_native_helper_in_memory_syntax_passed':True,'prospective_native_helper_sha256':sha(operator.read_bytes()),'Git_native_PR_or_publication_mutations':False}
F.mkdir(exist_ok=False)
(F/'READBACK.json').write_text(json.dumps(readback,indent=2)+'\n')
paths=[A/'original_source_authentication_20261004/ORIGINAL_AUTHENTICATION.json',A/'original_source_authentication_20261004/ORIGINAL_BLOB_MANIFEST.json',A/'ROOT_MATHEMATICAL_REVIEW_20261004.md',A/'ROOT_provided_source_final_readback_20261004/READBACK.json',A/'PUBLICATION_PACKAGE_V1_SUPERSEDED_20261004.json']
for family in families:
    d=A/family;paths.extend([d/'REPORT.md',d/'MANIFEST.json'])
    paths.append(d/('verdict.json' if family==families[1] else 'VERDICT.json'))
paths.extend((A/'attributed_prior_result_preparation_20261004'/n) for n in ['CURRENT_RESULT.md','CURRENT_PRIORITY_SPECIALIZATION.md','PR_BODY.md','DISPOSITION_PROPOSAL.json','MANIFEST.json'])
bound=[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in paths]
goal=Path('/Users/alec/.codex/attachments/4df73d3d-641f-4907-b9ad-c47c468f2589/goal-objective.md')
gate={'schema':'pr65-ROOT-provided-source-final-disposition/v1','UTC':stamp,'actual_recorder_pid':os.getpid(),'PR':65,'expected_original_head':'5cc1602c05d79502defb07cec7027963149494d2','eligible_intake_literal_status':'claimed_solved','original_proof_turns':'2/5','new_original_proof_turns':0,'ROOT_personally_read_all_four_new_reports':True,'candidate_mathematics_verified':True,'prior_resolution_of_exact_original_problem_verified':True,'audited_outcome':'already_solved','accepted_as':'attributed_partial_prior_result','full_source_solved':True,'full_source_solved_meaning':'Exact Holland target from prior construction plus checked normalization; separate submitted theorem verified; not a new open-problem resolution.','new_solution_priority_clearance':False,'identical_algorithm_or_earliest_priority_certified':False,'fresh_final_adversary_clean':True,'ROOT_authorizes_guarded_attributed_prior_result_acceptance':True,'human_partial_outcome_rule':'If the result was already_solved or unsolved, audit the findings, and if valid and everything checks out, merge the PR as a partial result. Do not make a paper for these.','ROOT_scope_interpretation':'Current goal narrows intake to literal claimed_solved heads. PR65 qualifies. Apply the original human partial-outcome rule for this eligible submission found to have a priority issue; the goal file itself omits that clause. Initially nonclaimed PRs remain entirely skipped.','goal_objective_sha256':sha(goal.read_bytes()),'bound_current_evidence':bound,'publication_authorized':False,'new_paper':False,'new_DOI':None,'tracker_append':False,'PR50_exception_extended':False,'actual_execution_complete':False,'actual_writer_ack_and_fresh_exact_head_eligibility_required':True,'prospective_native_helper_sha256':sha(operator.read_bytes()),'human_peer_review':False,'formal_proof_certification':False}
(A/'ROOT_PROVIDED_SOURCE_FINAL_DISPOSITION_20261004.json').write_text(json.dumps(gate,indent=2)+'\n')
(A/'ROOT_PROVIDED_SOURCE_PRIORITY_ADJUDICATION_20261004.md').write_text('# PR65 corrected priority disposition after supplied primary sources\n\nROOT read and rechecked the exact source evidence, all four new independent reports and verdicts, and their recorded custody. The supplied2019 update supersedes the authentic2018 no-progress report. AAN1999 Theorem2 with quadratic gauge, covering purity and normalization at a preimage of0 supplies exactly Holland’s requested pure Blaschke product and Bloch Cayley transform, with seminorm8. The general Cayley application is printed on328-329; normalization is the checked deduction, and HL2019 calls its cited inner construction explicit. This positive prior evidence supports already_solved for the original historical target without claiming earliest recognition or a certified effective universal-cover algorithm.\n\nPiranian1966 already prints Kahane’s fixed absorbed four-adic mechanism and all-point obstruction; DSS1966 prints its affine-periodic Zygmund/Herglotz Bloch bridge. The submitted ordering is different and no literal-copy claim is made. The submitted target theorem remains verified; no novel historical resolution is certified. The checked specialization and complete corrected current prose are in attributed_prior_result_preparation_20261004/.\n\nThe fresh final adversary passed without required repairs. ROOT applies the original human instruction to merge valid already_solved findings as attributed progress without a paper, while retaining claimed_solved-only intake. The original submitted source bodies and2/5 ledger remain dated inputs. The formerly prepared v1 note and its old-scope reviews are expressly superseded for current promotion; no current publication-ready package, new paper, Zenodo record, DOI or tracker row is authorized. The PR50 exception remains local. No native/PR/Git mutation has occurred in this scientific adjudication; guarded exact-head execution and actual readback are required.\n\n'+stamp+' checkpoint estimates: mathematical verification100%; bounded priority disposition100% (new-resolution clearancefalse); current workflow65%; ordered completed6/99=6.060606%. The persistent goal remains active.\n')
progress_path=P/'CURRENT_PROGRESS.json';progress=json.loads(progress_path.read_bytes())
if progress['current_PR']!=65 or progress['current_publication_authorization']:raise RuntimeError('Current program scope changed')
progress.update(UTC=stamp,current_priority_audit_percent=100,current_priority_audit_complete=True,current_priority_clearance=False,current_priority_record='audits/pr65_2305051/ROOT_PROVIDED_SOURCE_PRIORITY_ADJUDICATION_20261004.md',current_final_disposition_record='audits/pr65_2305051/ROOT_PROVIDED_SOURCE_FINAL_DISPOSITION_20261004.json',current_audited_outcome='already_solved',current_accepted_as='attributed_partial_prior_result',current_full_source_solved=True,current_new_open_problem_resolution=False,current_PR_workflow_percent=65,current_priority_final_adversary_status='clean; exact prior normalization and attributed disposition verified; no novel-resolution or execution authority from reviewer',remaining_current_step='Acquire actual shared writer acknowledgement; execute exact original-head attributed prior-result merge, independently verify GitHub and native current acceptance, checkpoint owned audit findings, then advance in PR order. No paper/DOI/tracker for this prior-result disposition.')
progress_path.write_text(json.dumps(progress,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n## '+stamp+' - final supplied-source priority adjudication\n\nFour independent renewed reports read completely and manifested bytes/actual process streams verified. Fresh final adversary found no blocking issue or required repair. ROOT concludes already-solved original target from positive1999/2019 primary evidence, retaining verified submitted construction as attributed progress. Original2/5 unchanged; earliest/identical-algorithm priority uncertified. Old publication packet withdrawn from current promotion. No native/Git/PR/publishing/editor mutation yet; real writer acknowledgement and execution readback remain. Estimates math100%, bounded priority100% with novel-resolution clearancefalse, workflow65%, ordered6/99=6.060606%.\n')
print(json.dumps({'status':'PASS','UTC':stamp,'actual_controller_pid':os.getpid(),'new_family_member_counts':[(x['family'],x['public_member_count'],x['private_member_count'],x['genuine_receipt_count']) for x in inventories],'ROOT_scientific_outcome':'already_solved','guarded_attributed_acceptance_authorized':True,'publication_authorized':False},indent=2))
