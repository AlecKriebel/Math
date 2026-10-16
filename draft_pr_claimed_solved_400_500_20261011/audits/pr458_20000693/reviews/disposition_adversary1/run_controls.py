#!/usr/bin/env python3
"""Run the actual frozen helper in subprocesses against isolated, network-free fixtures.

The ninth report, result and action gate in these private fixtures are HYPOTHETICAL
test inputs only. They are not completed review evidence or authorization.
"""
import argparse, base64, datetime, hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path
from audit_inputs import binding, check, CASE, OWN, PROGRAM, HEAD, FAMILIES

QUEUE='unsolved_math_prioritization/QUEUE.md'
FAKE='disposition_adversary999'
GATE='PRIORITY_DISPOSITION_GATE.json'
PRIVATE=OWN/'private_cases/complete_run'
INPUT_CASE=OWN/'private_cases/INPUT_SNAPSHOT'
REVIEWED_HELPER=OWN/'REVIEWED_HELPER.py'

def read(p): return json.loads(p.read_text())
def write(p,x): p.write_text(json.dumps(x,indent=2)+'\n')

def resign(case):
 """Update mocked byte signatures after one deliberate private evidence mutation."""
 for family in list(FAMILIES)+[FAKE]:
  mp=case/'reviews'/family/'PUBLIC_FILES.json'
  if not mp.exists(): continue
  m=read(mp)
  for rec in m['files']:
   p=mp.parent/rec['path']
   if p.is_file(): rec.update(binding(p))
  write(mp,m)
 g=read(case/GATE)
 for rec in g['reviewed_files']:
  p=case/rec['path']
  if p.is_file(): rec.update(binding(p))
 write(case/GATE,g)

def baseline(root):
 program=root/'program'; case=program/'audits/pr458_20000693'; case.mkdir(parents=True)
 shutil.copy2(REVIEWED_HELPER if REVIEWED_HELPER.exists() else PROGRAM/'repair_pr458_status.py',program/'repair_pr458_status.py')
 source_case=INPUT_CASE if INPUT_CASE.exists() else CASE
 draft=read(source_case/'DRAFT_OPERATIONS_GATE.json')
 for rec in draft['reviewed_files']:
  p=case/rec['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source_case/rec['path'],p)
 d=case/'reviews'/FAKE;d.mkdir(parents=True)
 (d/'REPORT.md').write_text('PRIVATE HYPOTHETICAL MOCK ONLY: no actual reviewer, no operations approval.\n')
 result={'pr':458,'problem_id':'20000693','frozen_head':HEAD,'reviewer':'/root/pr458_'+FAKE,
  'blocking_findings':0,'required_repairs':0,'unresolved_disposition_issues':0,
  'status_recommendation':'already_solved','acceptance_scope':'one_row_priority_correction_then_immediate_skip',
  'publication_accepted':False,'reviewed_helper_sha256':binding(program/'repair_pr458_status.py')['sha256'],
  'reviewed_synthesis_sha256':binding(case/'DISPOSITION_SYNTHESIS.md')['sha256'],
  'private_fixture_only':True,'not_actual_reviewer_evidence':True}
 write(d/'RESULT.json',result)
 write(d/'PUBLIC_FILES.json',{'private_fixture_only':True,'files':[{'path':x,**binding(d/x)} for x in ['REPORT.md','RESULT.json']]})
 g=draft;g.update(verdict='ACCEPTED_PRIORITY_CLASSIFICATION',root_read_entire_final_reports=True,
  operations_approval=True,not_an_action_gate=False,missing_actual_final_operations_review=False)
 g['reviews'].append({'family':'disposition_adversary','reviewer':'/root/pr458_'+FAKE,
  'report_path':'reviews/'+FAKE+'/REPORT.md','result_path':'reviews/'+FAKE+'/RESULT.json',
  'raw_blocking_findings':0,'raw_required_repairs':0,'unresolved_disposition_issues':0})
 g['reviewed_files'] += [{'path':'reviews/'+FAKE+'/'+x,**binding(d/x)} for x in ['REPORT.md','RESULT.json','PUBLIC_FILES.json']]
 pubpath=str((case/'DISPOSITION_SYNTHESIS.md').relative_to(program.parent))
 g['published_disposition_url']='https://github.com/AlecKriebel/Math/blob/'+'f'*40+'/'+pubpath
 g.update(private_fixture_only=True,not_actual_action_gate=True)
 write(case/GATE,g)
 before=(CASE/'private_cases/original_QUEUE.md').read_bytes()
 sha=hashlib.sha1(b'blob '+str(len(before)).encode()+b'\0'+before).hexdigest()
 state={'private_fixture_only':True,'ref':HEAD,'original_blob':sha,'blobs':{sha:base64.b64encode(before).decode()},
  'synthesis_b64':base64.b64encode((case/'DISPOSITION_SYNTHESIS.md').read_bytes()).decode(),
  'pr_reads':0,'ref_reads':0,'trace':[],'scenario':{}}
 statep=root/'GH_STATE.json';write(statep,state)
 bindir=root/'bin';bindir.mkdir()
 gh=bindir/'gh';gh.write_text('#!'+sys.executable+'\nimport runpy\nrunpy.run_path('+repr(str(OWN/'mock_gh.py'))+',run_name="__main__")\n');gh.chmod(0o755)
 return program,case,statep,bindir

def modify_json(case,name,fn,resign_after=True):
 p=case/name; x=read(p);fn(x);write(p,x)
 if resign_after: resign(case)

def mutate(name,program,case,statep):
 s=read(statep);g=read(case/GATE)
 msg=None; apply=True; positive=False
 if name=='baseline_preflight': apply=False;positive=True
 elif name in ['baseline_apply','uncertain_patch_applied']: positive=True
 if name=='uncertain_patch_applied': s['scenario']={'patch_error':True}
 elif name=='missing_actual_gate': (case/GATE).unlink();msg='PRIORITY_DISPOSITION_GATE.json'
 elif name=='actual_eight_review_draft_as_gate': shutil.copy2((INPUT_CASE if INPUT_CASE.exists() else CASE)/'DRAFT_OPERATIONS_GATE.json',case/GATE);msg='Final exact classification/helper gate absent'
 elif name.startswith('gate:'):
  _,field,value=name.split(':',2);g[field]=json.loads(value);write(case/GATE,g);msg='Final exact classification/helper gate absent'
 elif name=='raw_pub_erased': g['retained_original_publication_blockers']=[];write(case/GATE,g);msg='Raw publication findings'
 elif name=='priority_vote_erased': g['priority_coverage_already_solved_recommendation']=True;write(case/GATE,g);msg='Raw publication findings'
 elif name=='missing_ninth': g['reviews']=g['reviews'][:-1];write(case/GATE,g);msg='Nine actual complete reviews required'
 elif name=='duplicate_family': g['reviews'][-1]=g['reviews'][0];write(case/GATE,g);msg='Unknown/duplicate family'
 elif name=='wrong_final_identity': g['reviews'][-1]['reviewer']='/root/other';write(case/GATE,g);msg='Fresh numbered final operations reviewer required'
 elif name=='stale_helper': (program/'repair_pr458_status.py').write_text((program/'repair_pr458_status.py').read_text()+'\n# private stale code probe\n');msg='Final exact classification/helper gate absent'
 elif name=='mandatory_missing': g['reviewed_files']=[r for r in g['reviewed_files'] if r['path']!='CONTEXT_INDEPENDENCE_CAVEAT.md'];write(case/GATE,g);msg='Mandatory complete source/decision evidence absent'
 elif name=='evidence_duplicate': g['reviewed_files'].append(g['reviewed_files'][0]);write(case/GATE,g);msg='Evidence duplicate/type/byte binding differs'
 elif name=='evidence_bytes_bool': g['reviewed_files'][0]['bytes']=True;write(case/GATE,g);msg='Evidence duplicate/type/byte binding differs'
 elif name=='evidence_bytes_float': g['reviewed_files'][0]['bytes']=float(g['reviewed_files'][0]['bytes']);write(case/GATE,g);msg='Evidence duplicate/type/byte binding differs'
 elif name=='evidence_hash_upper': g['reviewed_files'][0]['sha256']=g['reviewed_files'][0]['sha256'].upper();write(case/GATE,g);msg='Evidence duplicate/type/byte binding differs'
 elif name=='evidence_parent_path': g['reviewed_files'][0]['path']='../outside';write(case/GATE,g);msg='Unsafe evidence path'
 elif name=='evidence_private_path': g['reviewed_files'][0]['path']='private_cases/foreign.txt';write(case/GATE,g);msg='Unsafe evidence path'
 elif name=='evidence_symlink':
  p=case/g['reviewed_files'][0]['path']; dest=case/'OWN_SENTINEL';shutil.move(p,dest);p.symlink_to(dest);msg='Evidence topology'
 elif name=='evidence_hardlink':
  p=case/g['reviewed_files'][0]['path'];os.link(p,case/'OWN_SENTINEL');msg='Evidence topology'
 elif name=='source_count': modify_json(case,'SOURCE_RECEIPT.json',lambda x:x['files'].pop());msg='Frozen source identity'
 elif name=='source_head': modify_json(case,'SOURCE_RECEIPT.json',lambda x:x.update(head_sha='0'*40));msg='Frozen source identity'
 elif name=='source_pr_float': modify_json(case,'SOURCE_RECEIPT.json',lambda x:x.update(pr=458.0));msg='Frozen source identity'
 elif name=='source_unchanged_drift':
  p=case/'source_snapshot'/read(case/'SOURCE_RECEIPT.json')['files'][0]['path'];p.write_bytes(p.read_bytes()+b' ');resign(case);msg='Original source absent or changed'
 elif name.startswith('result:'):
  _,family,field,value=name.split(':',3)
  modify_json(case,'reviews/'+family+'/RESULT.json',lambda x:x.update({field:json.loads(value)}))
  msg='Actual reviewer result identity' if field in ['pr','frozen_head','reviewer','problem_id'] else 'Unprimed blocker aliases differ' if family=='unprimed_math_adversary' and field=='blocking_findings' else 'Raw family blockers changed' if field in ['blocking_issues','blocking_findings'] else 'Raw family repairs changed' if field=='required_repairs' else 'Central heuristic gap' if field=='unresolved_mathematical_gaps' else 'UNHANDLED_EXPECTED_GUARD'
 elif name=='priority_changed_recommendation': modify_json(case,'reviews/priority_coverage/RESULT.json',lambda x:x.update(status_recommendation='already_solved'));msg='Distinct conditional-heuristic recommendation relabeled'
 elif name=='priority_missing_theorem_gaps': modify_json(case,'reviews/priority_adversary/RESULT.json',lambda x:x['unresolved_mathematical_gaps'].pop());msg='Priority-adversary recommendation/theorem gaps differ'
 elif name=='classification_stale_draft': modify_json(case,'reviews/classification_adversary/LATER_EXPOSURE_BINDINGS.json',lambda x:[r.update(sha256='0'*64) for r in x['files'] if r['path']=='DRAFT_PRIORITY_DISPOSITION.md']);msg='Classification reviewer binds different draft'
 elif name=='operations_stale_synthesis': modify_json(case,'reviews/'+FAKE+'/RESULT.json',lambda x:x.update(reviewed_synthesis_sha256='0'*64));msg='Final operations reviewer binds different helper/synthesis'
 elif name=='operations_stale_helper': modify_json(case,'reviews/'+FAKE+'/RESULT.json',lambda x:x.update(reviewed_helper_sha256='0'*64));msg='Final operations reviewer binds different helper/synthesis'
 elif name=='operations_issue': modify_json(case,'reviews/'+FAKE+'/RESULT.json',lambda x:x.update(unresolved_disposition_issues=1));msg='Operations disposition issues'
 elif name=='manifest_missing_result':
  modify_json(case,'reviews/source_admissibility/PUBLIC_FILES.json',lambda x:x.update(files=[r for r in x['files'] if r['path']!='RESULT.json']));msg='Complete public payload disconnected or drifted'
 elif name=='manifest_empty': modify_json(case,'reviews/source_admissibility/PUBLIC_FILES.json',lambda x:x.update(files=[]));msg='Empty positive manifest'
 elif name=='manifest_duplicate': modify_json(case,'reviews/source_admissibility/PUBLIC_FILES.json',lambda x:x['files'].append(x['files'][0]));msg='Complete public payload disconnected or drifted'
 elif name=='manifest_bytes_float':
  modify_json(case,'reviews/source_admissibility/PUBLIC_FILES.json',lambda x:x['files'][0].update(bytes=float(x['files'][0]['bytes'])),False)
  g['reviewed_files']=[{**r,**binding(case/r['path'])} for r in g['reviewed_files']];write(case/GATE,g);msg='Manifest record byte type'
 elif name=='raw_scope_contradiction': modify_json(case,'reviews/whole_math_adversary/RESULT.json',lambda x:x['current_publication_scope'].update(accepted=True));msg='Contradictory raw publication scope'
 elif name=='raw_actual_theorem_true': modify_json(case,'reviews/euler_adversary/RESULT.json',lambda x:x.update(asymptotic_proved=True));msg='Contradictory raw theorem scope'
 elif name=='raw_central_alias_true': modify_json(case,'reviews/whole_math_adversary/RESULT.json',lambda x:x['proposed_mathematical_interpretation_scope'].update(unresolved_central_math_gaps=1));msg='Contradictory raw central alias'
 elif name=='report_wrong_identity':
  p=case/'reviews/source_admissibility/REPORT.md';p.write_text(p.read_text().replace('/root/pr458_source_admissibility','/root/pr999_other'));resign(case);msg='Contradictory report identity'
 elif name=='gate_review_issue_bool': g['reviews'][0]['unresolved_disposition_issues']=False;write(case/GATE,g);msg='Accepted classification has unresolved issues'
 elif name=='gate_raw_repair_float': g['reviews'][0]['raw_required_repairs']=0.0;write(case/GATE,g);msg='Gate erased raw repairs'
 elif name=='published_url_mutable': g['published_disposition_url']=g['published_disposition_url'].replace('f'*40,'main');write(case/GATE,g);msg='Exact immutable published disposition URL/hash absent'
 elif name=='published_url_query': g['published_disposition_url']+='?raw=1';write(case/GATE,g);msg='Exact immutable published disposition URL/hash absent'
 elif name=='published_wrong_bytes': s['synthesis_b64']=base64.b64encode(b'wrong').decode();msg='Immutable published synthesis bytes differ'
 elif name=='published_wrong_type': s['scenario']={'contents_changes':{'type':'dir'}};msg='Published synthesis not a file'
 elif name.startswith('pr:'):
  _,field,value,stage=name.split(':',3);s['scenario']={'pr_changes':{field:json.loads(value)},'change_at_pr_read':int(stage)};msg='Original open draft head/repository/base changed'
 elif name.startswith('ref:'):
  stage=int(name.split(':')[1]);s['scenario']={'ref_changed_to':'e'*40,'change_at_ref_read':stage};msg='Original branch ref changed'
 elif name=='tree_duplicate': s['scenario']={'duplicate_tree':True};msg='QUEUE Git tree path not unique'
 elif name=='queue_mode_symlink': s['scenario']={'queue_mode':'120000'};msg='QUEUE not regular Git blob'
 elif name.startswith('excluded:'):
  status=name.split(':')[1];b=base64.b64decode(s['blobs'][s['original_blob']]);old=read(case/'SOURCE_RECEIPT.json')['selected_queue_row'];cells=old.split('|');cells[8]=' '+status+' ';row='|'.join(cells);b=b.replace(old.encode(),row.encode())
  s['blobs'][s['original_blob']]=base64.b64encode(b).decode()
  # Administrative receipt updated only in fixture to reach the explicit status guard.
  modify_json(case,'SOURCE_RECEIPT.json',lambda x:x.update(queue_sha256=hashlib.sha256(b).hexdigest(),selected_queue_row=row));msg='Excluded status: stop without processing'
  # Removing all mathematical inputs makes any mathematical reread observable.
  for f in FAMILIES: shutil.rmtree(case/'reviews'/f)
  (case/GATE).unlink()
 elif name=='turns_drift':
  b=base64.b64decode(s['blobs'][s['original_blob']]);old=read(case/'SOURCE_RECEIPT.json')['selected_queue_row'];cells=old.split('|');cells[9]=' 2/5 ';row='|'.join(cells);b=b.replace(old.encode(),row.encode());s['blobs'][s['original_blob']]=base64.b64encode(b).decode();modify_json(case,'SOURCE_RECEIPT.json',lambda x:x.update(queue_sha256=hashlib.sha256(b).hexdigest(),selected_queue_row=row));msg='Author turns/DOI drift'
 elif name=='extra_commit_path': s['scenario']={'comparison_paths':[QUEUE,'extra.txt']};msg='Commit changed other paths'
 elif name=='uncertain_patch_not_applied': s['scenario']={'patch_error':True,'patch_updates':False};msg='Branch update uncertain; no retry'
 elif name=='patch_success_not_applied': s['scenario']={'patch_updates':False};msg='Branch readback differs'
 elif name=='patch_bad_json_applied': s['scenario']={'patch_bad_json':True};msg='JSONDecodeError'
 elif name=='wrong_blob_readback': s['scenario']={'wrong_blob_readback':True};msg='QUEUE blob exact bytes differ'
 elif name=='blob_create_error': s['scenario']={'fail_endpoint':'git/blobs'};msg='simulated endpoint failure'
 elif name=='compare_read_error': s['scenario']={'fail_endpoint':'compare/'+HEAD+'...'+'c'*40};msg='simulated endpoint failure'
 elif name=='output_symlink':
  p=case/'STATUS_REPAIR_PREFLIGHT.json';dest=case/'OWN_SENTINEL';dest.write_text('sentinel');p.symlink_to(dest);msg='Output alias'
 elif name=='output_hardlink':
  dest=case/'OWN_SENTINEL';dest.write_text('sentinel');os.link(dest,case/'STATUS_REPAIR_PREFLIGHT.json');msg='Nonregular/hardlinked output'
 elif name=='output_directory': (case/'STATUS_REPAIR_PREFLIGHT.json').mkdir();msg='Nonregular/hardlinked output'
 elif name=='audit_symlink':
  dest=case.parent/'real_case';shutil.move(case,dest);case.symlink_to(dest,target_is_directory=True);msg='Output alias'
 elif name=='prior_operation': (case/'STATUS_REPAIR_OPERATION.json').write_text('{}');msg='Prior operation: no repeated mutation'
 elif name=='manifest_wrong_json':
  p=case/'reviews/source_admissibility/PUBLIC_FILES.json';p.write_text('{')
  g['reviewed_files']=[{**r,**binding(case/r['path'])} for r in g['reviewed_files']];write(case/GATE,g);msg='JSONDecodeError'
 elif name=='gate_reviews_wrong_type': g['reviews']={};write(case/GATE,g);msg='Nine actual complete reviews required'
 elif name=='evidence_entry_wrong_type': g['reviewed_files'][0]=None;write(case/GATE,g);msg='Evidence entry type'
 elif name=='result_count_string': modify_json(case,'reviews/euler_adversary/RESULT.json',lambda x:x.update(blocking_issues='1'));msg='Raw family blockers changed'
 elif name=='nonnumeric_gate_raw': g['reviews'][1]['raw_blocking_findings']=True;write(case/GATE,g);msg='Gate erased raw blockers'
 elif name=='gate_root_read_false': g['root_read_entire_final_reports']=False;write(case/GATE,g);msg='Final exact classification/helper gate absent'
 elif name=='family_readback_raw_count': modify_json(case,'PRIORITY_ADVERSARY_FAMILY_READBACK.json',lambda x:x['raw_counts'].update(promotion_priority_blockers=0));msg='Canonical family readback count contradiction'
 elif name=='family_readback_hash_stale': modify_json(case,'CLASSIFICATION_FAMILY_READBACK.json',lambda x:[r.update(sha256='0'*64) for r in x['safe_payloads'] if r['path'].endswith('/REPORT.md')]);msg='Family readback binding contradiction'
 elif name=='source_manifest_bytes_float': modify_json(case,'SOURCE_RECEIPT.json',lambda x:x['files'][0].update(bytes=float(x['files'][0]['bytes'])));msg='Source byte count type'
 elif name=='final_reviewer_result_identity': modify_json(case,'reviews/'+FAKE+'/RESULT.json',lambda x:x.update(reviewer='/root/wrong'));msg='Actual reviewer result identity'
 elif name=='final_reviewer_result_pr_bool': modify_json(case,'reviews/'+FAKE+'/RESULT.json',lambda x:x.update(pr=True));msg='Actual reviewer result identity'
 elif name=='receipt_symlink':
  dest=case/'OWN_SENTINEL';dest.write_text('sentinel');(case/'STATUS_REPAIR_RECEIPT.json').symlink_to(dest);msg='Output alias'
 elif name=='operation_hardlink':
  dest=case/'OWN_SENTINEL';dest.write_text('sentinel');os.link(dest,case/'STATUS_REPAIR_OPERATION.json');msg='Nonregular/hardlinked output'
 elif name=='publication_claim_false_but_gap': modify_json(case,'reviews/priority_coverage/RESULT.json',lambda x:x['count_scopes'].update(actual_general_asymptotic_unproved_inputs=0));msg='Canonical actual inputs contradiction'
 elif name=='gate_operations_approval_false':g['operations_approval']=False;write(case/GATE,g);msg='Explicit operations approval absent'
 elif name=='gate_not_action_gate_true':g['not_an_action_gate']=True;write(case/GATE,g);msg='Explicitly non-action gate'
 elif name=='gate_missing_final_true':g['missing_actual_final_operations_review']=True;write(case/GATE,g);msg='Actual final operations review declared missing'
 write(statep,s)
 return apply,positive,msg

def run_one(name,mode,i):
 root=PRIVATE/(mode+'_'+str(i));program,case,statep,bindir=baseline(root)
 apply,positive,msg=mutate(name,program,case,statep)
 before_hashes={str(p.relative_to(case)):binding(p) for p in (case/'source_snapshot').rglob('*') if p.is_file()}
 env=dict(os.environ);env['PATH']=str(bindir)+os.pathsep+env.get('PATH','');env['PRIVATE_GH_STATE']=str(statep);env['PYTHONDONTWRITEBYTECODE']='1'
 if mode=='optimized': env['PYTHONOPTIMIZE']='1'
 else: env.pop('PYTHONOPTIMIZE',None)
 cmd=[sys.executable,str(program/'repair_pr458_status.py')]+(['--apply'] if apply else [])
 p=subprocess.run(cmd,capture_output=True,text=True,env=env,cwd=root,timeout=45)
 (root/'stdout.txt').write_text(p.stdout);(root/'stderr.txt').write_text(p.stderr)
 state=read(statep);writes=[x for x in state['trace'] if x['method']!='GET'];patches=[x for x in writes if x['method']=='PATCH']
 after_hashes={str(x.relative_to(case)):binding(x) for x in (case/'source_snapshot').rglob('*') if x.is_file()}
 check(before_hashes==after_hashes,'helper changed research fixture '+name)
 outcome='intended_guard_rejection' if p.returncode!=0 and msg and msg in p.stderr else 'unexpected_acceptance' if p.returncode==0 and not positive else 'test_defect_or_wrong_guard' if p.returncode!=0 else 'positive_pass'
 details={}
 if positive and p.returncode==0:
  pre=read(case/'STATUS_REPAIR_PREFLIGHT.json');old=pre['selected_old_row'].split('|');new=pre['selected_new_row'].split('|')
  check([n for n,(a,b) in enumerate(zip(old,new)) if a!=b]==[8,11],'unexpected selected cells')
  check(old[9]==new[9] and old[12]==new[12] and new[9].strip()=='1/5' and new[12].strip()=='','turn/DOI')
  if apply:
   check(len(patches)==1 and patches[0]['payload']['force'] is False,'PATCH count/force')
   check(state['created_tree']['base_tree']=='a'*40 and state['created_tree']['tree']==[{'path':QUEUE,'mode':'100644','type':'blob','sha':state['new_blob']}],'only QUEUE tree edit')
   check(state['created_commit']['parents']==[HEAD],'parent')
   b=base64.b64decode(state['blobs'][state['original_blob']]);a=base64.b64decode(state['blobs'][state['new_blob']]);bl=b.splitlines(keepends=True);al=a.splitlines(keepends=True)
   check(len(bl)==len(al) and sum(x!=y for x,y in zip(bl,al))==1,'other rows/header')
   receipt=read(case/'STATUS_REPAIR_RECEIPT.json');check(receipt['state']=='status_repair_verified_immediately_excluded','receipt')
   details['one_row_exact_preservation']=True
  else: check(not writes,'read-only preflight wrote Git objects')
 if msg and name.startswith('excluded:'): check(not writes and not (case/'STATUS_REPAIR_PREFLIGHT.json').exists(),'excluded status processed')
 if name=='prior_operation': check(not state['trace'],'repeat action reached network API')
 check(len(patches)<=1,'blind PATCH retry')
 record={'case':name,'mode':mode,'returncode':p.returncode,'outcome':outcome,'expected_guard':msg,'actual_last_error':p.stderr.strip().splitlines()[-1] if p.stderr.strip() else '',
  'stdout_bytes':len(p.stdout.encode()),'stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr.encode()).hexdigest(),
  'mock_api_calls':len(state['trace']),'mock_git_writes':len(writes),'mock_ref_patches':len(patches),'ref_moved':state['ref']!=HEAD,'operation_record_exists':(case/'STATUS_REPAIR_OPERATION.json').exists(),
  '27_research_fixture_files_unchanged':before_hashes==after_hashes,**details}
 write(root/'RAW_RUN_RESULT.json',record)
 return record

def cases():
 c=['baseline_preflight','baseline_apply','uncertain_patch_applied','missing_actual_gate','actual_eight_review_draft_as_gate',
  'gate:pr:true','gate:publication_accepted:true','gate:recommended_status:"solved"','gate:acceptance_scope:"publish"','gate:original_head:"wrong"',
  'raw_pub_erased','priority_vote_erased','missing_ninth','duplicate_family','wrong_final_identity','stale_helper','mandatory_missing','evidence_duplicate',
  'evidence_bytes_bool','evidence_bytes_float','evidence_hash_upper','evidence_parent_path','evidence_private_path','evidence_symlink','evidence_hardlink',
  'source_count','source_head','source_pr_float','source_unchanged_drift',
  'result:euler_adversary:pr:true','result:euler_adversary:pr:458.0','result:euler_adversary:reviewer:"/root/wrong"',
  'result:euler_adversary:frozen_head:"wrong"','result:euler_adversary:blocking_issues:0','result:euler_adversary:required_repairs:0',
  'result:euler_adversary:unresolved_mathematical_gaps:1','result:unprimed_math_adversary:blocking_findings:0',
  'priority_changed_recommendation','priority_missing_theorem_gaps','classification_stale_draft','operations_stale_synthesis','operations_stale_helper','operations_issue',
  'manifest_missing_result','manifest_empty','manifest_duplicate','manifest_bytes_float','raw_scope_contradiction','raw_actual_theorem_true','raw_central_alias_true','report_wrong_identity',
  'gate_review_issue_bool','gate_raw_repair_float','published_url_mutable','published_url_query','published_wrong_bytes','published_wrong_type',
  'tree_duplicate','queue_mode_symlink','excluded:solved','excluded:already_solved','excluded:out_of_scope','turns_drift',
  'extra_commit_path','uncertain_patch_not_applied','patch_success_not_applied','patch_bad_json_applied','wrong_blob_readback','blob_create_error','compare_read_error',
  'output_symlink','output_hardlink','output_directory','audit_symlink','prior_operation','manifest_wrong_json','gate_reviews_wrong_type','evidence_entry_wrong_type',
  'result_count_string','nonnumeric_gate_raw','gate_root_read_false','family_readback_raw_count','family_readback_hash_stale',
  'source_manifest_bytes_float','final_reviewer_result_identity','final_reviewer_result_pr_bool','receipt_symlink','operation_hardlink','publication_claim_false_but_gap',
  'gate_operations_approval_false','gate_not_action_gate_true','gate_missing_final_true']
 for field,value in [('state','"closed"'),('draft','false'),('head.sha','"changed"'),('head.repo.full_name','"Other/Repo"'),('base.ref','"other"'),('base.repo.full_name','"Other/Repo"'),('head.ref','"other"')]:
  for stage in [1,2,3]:c.append('pr:'+field+':'+value+':'+str(stage))
 for stage in [1,2,3]:c.append('ref:'+str(stage))
 return c

def main():
 global PRIVATE
 parser=argparse.ArgumentParser()
 parser.add_argument('--run-name',default=None,help='New private reproduction directory; original results are never overwritten')
 args=parser.parse_args()
 if args.run_name is not None:
  check(re.fullmatch('[a-z][a-z0-9_]{0,40}',args.run_name) is not None,'invalid private run name')
  PRIVATE=OWN/'private_cases'/('reproduction_'+args.run_name)
 check(not PRIVATE.exists(),'Refusing to overwrite retained private raw fixtures')
 PRIVATE.mkdir(parents=True)
 (PRIVATE/'README.txt').write_text('ALL FIXTURES ARE PRIVATE MOCKS. No actual ninth reviewer or gate is represented. No network/remote action is performed.\n')
 allruns=[]
 for mode in ['normal','optimized']:
  for i,name in enumerate(cases()):
   record=run_one(name,mode,i);allruns.append(record)
   if record['outcome'] not in ['intended_guard_rejection','positive_pass']: print(json.dumps(record),flush=True)
 summaries={mode:{outcome:sum(r['mode']==mode and r['outcome']==outcome for r in allruns) for outcome in ['positive_pass','intended_guard_rejection','unexpected_acceptance','test_defect_or_wrong_guard']} for mode in ['normal','optimized']}
 out={'completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewed_helper':binding(REVIEWED_HELPER if REVIEWED_HELPER.exists() else PROGRAM/'repair_pr458_status.py'),'actual_subprocess_executions':len(allruns),'cases_per_mode':len(cases()),'summary':summaries,'runs':allruns,
  'real_remote_mutations':0,'all_ninth_review_and_gate_inputs_private_hypothetical_only':True}
 write(PRIVATE/'REPRODUCTION_RESULTS.json' if args.run_name is not None else OWN/'CONTROL_RESULTS.json',out)
 print(json.dumps({'executions':len(allruns),'summary':summaries},indent=2))
if __name__=='__main__': main()
