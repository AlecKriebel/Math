"""Close only this independent review with literal 0444 files and external pins."""
from pathlib import Path,PurePosixPath
import datetime,hashlib,json,os,stat
P=Path(__file__).resolve().parent;A=P.parent
def sha(b):return hashlib.sha256(b).hexdigest()
def require(v,s):
    if not v:raise ValueError(s)
def j(p):return json.loads(p.read_bytes())
require(P.name=='whole_current_source_first_family','own exact family')
require(not (P/'SELF_MANIFEST.json').exists(),'never overwrite own closure')
mh=sha((A/'reviewed_candidate/MANIFEST.json').read_bytes())
require(mh=='4849e6037a5db3dce546a656dcd57063ae83d782c19e24d4e3dff97ebbcdec14','exact reviewed manifest')
seal=j(P/'INITIAL_SEAL.json')
require(sha((P/'INITIAL_INDEPENDENT_DERIVATION.md').read_bytes())==seal['sha256'],'own initial seal unchanged')
for directory,source,operator in [('actual_whole_inspection_001','inspect_whole_source.py','capture_own_inspection.py'),('actual_acceptance_controls_001','independent_acceptance_controls.py','capture_own_acceptance_controls.py'),('actual_supplement_001','supplemental_closed_inputs.py','capture_own_supplement.py')]:
    d=P/directory;r=j(d/'CAPTURE.json')
    require(type(r['actual_child_pid']) is int and r['actual_child_pid']>0 and type(r['exit_code']) is int and r['exit_code']==0,'actual own child completed')
    source_name='PRELAUNCH_READER.py' if directory=='actual_whole_inspection_001' else 'PRELAUNCH_SOURCE.py'
    require((d/source_name).read_bytes()==(P/source).read_bytes() and (d/'PRELAUNCH_OPERATOR.py').read_bytes()==(P/operator).read_bytes(),'exact own prelaunch sources')
    for ch in ['stdout','stderr']:
        b=(d/(ch+'.bin')).read_bytes();require(len(b)==r[ch]['bytes'] and sha(b)==r[ch]['sha256'],'complete own actual stream')
    require((d/'stderr.bin').read_bytes()==b'','own stderr empty')
require(j(P/'INDEPENDENT_ACCEPTANCE_CONTROLS_RESULT.json')['all_passed'] is True and j(P/'SUPPLEMENTAL_SOURCE_READ.json')['all_passed'] is True,'own checks pass')
inputs={}
for filename in ['WHOLE_SOURCE_READ_LEDGER.json','SUPPLEMENTAL_SOURCE_READ.json']:
    for r in j(P/filename)['reads']:
        path=Path(r['path']);b=path.read_bytes()
        require(len(b)==r['bytes'] and sha(b)==r['sha256'],'read input changed before own closure '+r['path'])
        if r['path'] in inputs:require(inputs[r['path']]['sha256']==r['sha256'],'repeated input inconsistent')
        else:inputs[r['path']]={'path':r['path'],'bytes':r['bytes'],'sha256':r['sha256'],'role':r['role'],'individual_exclusion':'Outside this family authorship; attributed frozen/primary/native/process evidence only, no novelty claim.'}
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
verdict={'schema':'PR43_NEW_WHOLE_CURRENT_SOURCE_FIRST_INDEPENDENT_VERDICT_v1','created_utc':now,'verdict':'PASS_EXACT_FROZEN_CURRENT_PACKET_FOR_CREDITED_SOURCE_STATUS_ACCEPTANCE','candidate_manifest_sha256':mh,'mandatory_defects':[],'source_or_packet_repair_required':False,'mathematical_gap':None,'justified_status':'already_solved','full_target_resolved_in_prior_published_literature':True,'prior_publication_doi':'10.4064/sm210413-16-9','full_problem_solved_by_project':False,'novelty_claimed':False,'priority_claimed':False,'candidate_original_family_scripts_imported_compiled_executed':False,'own_actual_children':[72547,78301,82888],'whole_candidate_members_excluding_manifest':347,'external_candidate_dependencies':274,'current_native_preimages':13,'original_archive_files':16,'original_diff_paths':17,'original_diff_lines':957,'current_final_actual_git_commands':42,'frozen_prepublication_command_prefix':40,'raw_bytes_independently_compared':149266659,'SQL_rows_independently_compared':15458,'new_exact_probe_instances':1024,'current_runtime_unknown_fields_preserved_null':True,'historical_runtime_or_human_referee_certified':False,'old_verdict_transferred':False,'frozen_historical_current_gate':'PENDING_NEW_WHOLE_CURRENT_SOURCE_FIRST_ADVERSARY','this_verdict_is_new_separate_review':True,'ROOT_final_reconciliation_integration_merge_certified':False,'future_changed_packet_certified':False,'original_substantive_attempts':0,'substantive_attempt_limit':5,'new_substantive_attempts':0,'audit_turns':0,'review_completion_percent':100,'new_discovery_percent':0,'paper_new_DOI_tracker_created':False,'native_git_remote_mutations':False,'outside_human_contact':False,'optional_refinements_are_not_gates':['Standalone literal-line checks may be considered on an unrelated future source revision; no defect in actual separately read honest certificate.'],'initial_exposure_limit':'Parent disclosed target and expected identities/conclusions; own mechanism sealed before candidate mathematical source reading, not blind discovery.'}
(P/'VERDICT.json').write_text(json.dumps(verdict,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n- 2026-10-03T00:32:28.241584+00:00 — Actual initial whole-byte inspector child72547 exited0;347+self literal0444 candidate,274 anchored dependencies/current native13 checked. Review30%; discovery0%.\n')
    f.write('- 2026-10-03T00:38:38.985467+00:00 — Actual independent acceptance child78301 exited0;1117predicates, whole149266659rawbytes/all15458SQL and1024exactconstruction probes. Primaryfull12pages/OWRoperative3pages/bothproofs/currentbuilderoperator inspected. Review80%; discovery0%.\n')
    f.write('- 2026-10-03T00:41:53.775870+00:00 — Actual supplementary child82888 exited0;459reads/482predicates complete source-only/ROOTprerequisite/failure/closure evidence. No mandatory defect. Review95%; discovery0%.\n')
    f.write('- '+now+' — Closed own new whole-current PASS for exact frozen4849e603... manifest, mandatorydefectsnone, no repairs. Review100%; newdiscovery0%. ROOTfinalreconciliation/integration remains separate. No foreigncodeexecution/native/Git/remote mutation or outside contact. Actual ownclosurePID'+str(os.getpid())+'.\n')
files=[];dirs=[]
for p in sorted(P.rglob('*')):
    require(not p.is_symlink(),'own nonsymlink')
    if p.is_file():
        p.chmod(0o444);b=p.read_bytes();require(len(b)<100*1024*1024,'own singlefile limit')
        files.append({'path':str(p.relative_to(P)),'bytes':len(b),'sha256':sha(b),'mode':'0444','classification':'first_party_independent_review_artifact','novelty_claim':False})
    else:require(p.is_dir(),'own regular dirs');dirs.append(str(p.relative_to(P)))
required_dirs={str(q) for r in files for q in PurePosixPath(r['path']).parents if str(q)!='.'}
require(set(dirs)==required_dirs,'own exact nonempty directories')
mf={'schema':'PR43_NEW_WHOLE_CURRENT_SOURCE_FIRST_SELF_ONLY_CLOSURE_v1','created_utc':now,'actual_closure_pid':os.getpid(),'files_count':len(files),'files':files,'self_excluded':['SELF_MANIFEST.json'],'mode':'0444','directories':dirs,'candidate_manifest_sha256':mh,'external_individually_excluded_inputs':sorted(inputs.values(),key=lambda r:r['path']),'external_copied_members':[],'authorship_scope':'Only this family new notes/reports/handwritten controls/captures and manifest; no external source or other family artifact claimed as own authored science.','review_completion_percent':100,'new_discovery_percent':0,'ROOT_future_approval_certified':False}
with (P/'SELF_MANIFEST.json').open('x') as f:json.dump(mf,f,indent=2);f.write('\n')
(P/'SELF_MANIFEST.json').chmod(0o444)
require({str(p.relative_to(P)) for p in P.rglob('*') if p.is_file()}=={r['path'] for r in files}|{'SELF_MANIFEST.json'},'own exactselfclosure')
for r in files:
    p=P/r['path'];require(sha(p.read_bytes())==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444,'own frozen identity/fullmode')
print(json.dumps({'status':'CLOSED_NEW_INDEPENDENT_WHOLE_CURRENT_PASS','actual_closure_pid':os.getpid(),'manifest_sha256':sha((P/'SELF_MANIFEST.json').read_bytes()),'files_count':len(files),'individually_excluded_external_inputs':len(inputs),'verdict_sha256':sha((P/'VERDICT.json').read_bytes()),'report_sha256':sha((P/'FINAL_REPORT.md').read_bytes()),'candidate_manifest_sha256':mh,'mandatory_defects':[]},indent=2))
