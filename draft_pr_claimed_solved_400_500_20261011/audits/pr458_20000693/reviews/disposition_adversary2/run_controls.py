#!/usr/bin/env python3
"""New independent complete current-helper controls; all action gates are PRIVATE HYPOTHETICAL ONLY.

Copies the reviewed helper byte-for-byte, invokes actual subprocesses and substitutes
only gh. It never creates an actual root gate or calls a real mutation endpoint.
"""
import argparse,base64,datetime,hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
from audit_evidence import OWN,CASE,PROGRAM,HEAD,FAMILIES,bind,need,read,save
QUEUE='unsolved_math_prioritization/QUEUE.md';GATE='PRIORITY_DISPOSITION_GATE.json';FAKE='disposition_adversary999';NEW='c'*40

def fixture(root):
 program=root/'program';case=program/'audits/pr458_20000693';case.mkdir(parents=True)
 shutil.copyfile(OWN/'REVIEWED_HELPER.py',program/'repair_pr458_status.py')
 draft=read(CASE/'DRAFT_OPERATIONS_GATE.json')
 for rec in draft['reviewed_files']:
  p=case/rec['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((CASE/rec['path']).read_bytes())
 d=case/'reviews'/FAKE;d.mkdir(parents=True)
 (d/'REPORT.md').write_text('PRIVATE HYPOTHETICAL ONLY. Counterfactual clean ninth-review model, not an actual review or authority.\n')
 save(d/'RESULT.json',{'private_fixture_only':True,'pr':458,'problem_id':'20000693','frozen_head':HEAD,'reviewer':'/root/pr458_'+FAKE,'blocking_findings':0,'required_repairs':0,'unresolved_disposition_issues':0,'status_recommendation':'already_solved','acceptance_scope':'one_row_priority_correction_then_immediate_skip','publication_accepted':False,'operations_approved':True,'current_helper_accepted':True,'reviewed_helper_sha256':bind(program/'repair_pr458_status.py')['sha256'],'reviewed_synthesis_sha256':bind(case/'DISPOSITION_SYNTHESIS.md')['sha256']})
 save(d/'PUBLIC_FILES.json',{'private_fixture_only':True,'files':[{'path':n,**bind(d/n)} for n in ['REPORT.md','RESULT.json']]})
 g=draft;g.update(verdict='ACCEPTED_PRIORITY_CLASSIFICATION',root_read_entire_final_reports=True,operations_approval=True,not_an_action_gate=False,missing_actual_final_operations_review=False,private_fixture_only=True,not_actual_gate=True)
 g['reviews'].append({'family':'disposition_adversary','reviewer':'/root/pr458_'+FAKE,'report_path':'reviews/'+FAKE+'/REPORT.md','result_path':'reviews/'+FAKE+'/RESULT.json','raw_blocking_findings':0,'raw_required_repairs':0,'unresolved_disposition_issues':0})
 g['reviewed_files'] +=[{'path':'reviews/'+FAKE+'/'+n,**bind(d/n)} for n in ['REPORT.md','RESULT.json','PUBLIC_FILES.json']]
 pubpath=str((case/'DISPOSITION_SYNTHESIS.md').relative_to(program.parent));g['published_disposition_url']='https://github.com/AlecKriebel/Math/blob/'+'f'*40+'/'+pubpath;save(case/GATE,g)
 b=(OWN/'private/original_QUEUE.md').read_bytes();blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 state=root/'MODEL.json';save(state,{'private_fixture_only':True,'ref':HEAD,'original_blob':blob,'blobs':{blob:base64.b64encode(b).decode()},'synthesis':base64.b64encode((case/'DISPOSITION_SYNTHESIS.md').read_bytes()).decode(),'requests':[],'pr_reads':0,'ref_reads':0,'config':{}})
 binpath=root/'bin';binpath.mkdir();gh=binpath/'gh';gh.write_text('#!'+sys.executable+'\nimport runpy\nrunpy.run_path('+repr(str(OWN/'mock_github.py'))+',run_name="__main__")\n');gh.chmod(0o755)
 return program,case,state,binpath

def rebind(case):
 # Deliberate private re-signing, without changing the literal foundation pin.
 for f in list(FAMILIES)+[FAKE]:
  p=case/'reviews'/f/'PUBLIC_FILES.json'
  if p.exists():
   try:m=read(p)
   except ValueError:continue
   if type(m) is dict and type(m.get('files')) is list:
    for r in m['files']:
     if type(r) is dict and isinstance(r.get('path'),str) and (p.parent/r['path']).is_file():r.update(bind(p.parent/r['path']))
    save(p,m)
 g=read(case/GATE)
 for r in g['reviewed_files']:
  if type(r) is dict and isinstance(r.get('path'),str) and (case/r['path']).is_file():r.update(bind(case/r['path']))
 save(case/GATE,g)

def json_change(case,path,fn,resign=True):
 p=case/path;x=read(p);fn(x);save(p,x)
 if resign:rebind(case)

def change(name,program,case,state):
 s=read(state);g=read(case/GATE);apply=True;positive=False;guard=None
 if name=='preflight':apply=False;positive=True
 elif name in ['apply','uncertain_moved','malformed_moved','duplicate_json_moved','json_array_moved']:positive=True
 if name=='uncertain_moved':s['config']={'patch_fail':True}
 elif name=='malformed_moved':s['config']={'patch_raw':'{'}
 elif name=='duplicate_json_moved':s['config']={'patch_raw':'{"sha":"a","sha":"b"}'}
 elif name=='json_array_moved':s['config']={'patch_raw':'[]'}
 elif name=='missing_gate':(case/GATE).unlink();guard='PRIORITY_DISPOSITION_GATE.json'
 elif name=='actual_unapproved_draft':shutil.copyfile(CASE/'DRAFT_OPERATIONS_GATE.json',case/GATE);guard='Final exact classification/helper gate absent'
 elif name.startswith('gate|'):
  _,key,value=name.split('|',2);g[key]=json.loads(value);save(case/GATE,g);guard='Final exact classification/helper gate absent'
 elif name=='raw_blockers_erased':g['retained_original_publication_blockers']=[];save(case/GATE,g);guard='Raw publication findings'
 elif name=='coverage_vote_erased':g['priority_coverage_already_solved_recommendation']=True;save(case/GATE,g);guard='Raw publication findings'
 elif name=='helper_drift':(program/'repair_pr458_status.py').write_bytes((program/'repair_pr458_status.py').read_bytes()+b'\n# drift\n');guard='Final exact classification/helper gate absent'
 elif name=='synthesis_drift':(case/'DISPOSITION_SYNTHESIS.md').write_bytes(b'changed synthesis');rebind(case);guard='Final operations reviewer binds different helper/synthesis'
 elif name=='foundation_resealed':
  json_change(case,'reviews/euler_adversary/RESULT.json',lambda x:x.update(asymptotic_proved=True))
  f=read(case/'FROZEN_FOUNDATION_BINDINGS.json')
  for r in f['files']:r.update(bind(case/r['path']))
  save(case/'FROZEN_FOUNDATION_BINDINGS.json',f);rebind(case);guard='Canonical frozen foundation manifest changed'
 elif name=='missing_fixed_evidence':g['reviewed_files']=[r for r in g['reviewed_files'] if not r['path'].endswith('CHECKS_NORMAL.json')];save(case/GATE,g);guard='Canonical frozen foundation bytes differ'
 elif name=='missing_mandatory':g['reviewed_files']=[r for r in g['reviewed_files'] if r['path']!='CONTEXT_INDEPENDENCE_CAVEAT.md'];save(case/GATE,g);guard='Mandatory complete source/decision evidence absent'
 elif name.startswith('foundation|'):
  _,path,key,value=name.split('|',3)
  def update(x):
   keys=key.split('.');o=x
   for k in keys[:-1]:o=o[k]
   o[keys[-1]]=json.loads(value)
  json_change(case,path,update);guard='Canonical frozen foundation bytes differ'
 elif name=='report_wrong_identity':
  p=case/'reviews/source_admissibility/REPORT.md';p.write_text(p.read_text().replace('/root/pr458_source_admissibility','/root/other'));rebind(case);guard='Canonical frozen foundation bytes differ'
 elif name=='missing_foundation_manifest_result':json_change(case,'reviews/source_admissibility/PUBLIC_FILES.json',lambda x:x.update(files=[r for r in x['files'] if r['path']!='RESULT.json']));guard='Canonical frozen foundation bytes differ'
 elif name=='manifest_bytes_float':json_change(case,'reviews/source_admissibility/PUBLIC_FILES.json',lambda x:x['files'][0].update(bytes=float(x['files'][0]['bytes'])),False);rebind_gate_only(case);guard='Canonical frozen foundation bytes differ'
 elif name=='source_bytes_float':json_change(case,'SOURCE_RECEIPT.json',lambda x:x['files'][0].update(bytes=float(x['files'][0]['bytes'])));guard='Canonical frozen foundation bytes differ'
 elif name=='source_drift':
  p=case/'source_snapshot'/read(case/'SOURCE_RECEIPT.json')['files'][0]['path'];p.write_bytes(p.read_bytes()+b' ');rebind(case);guard='Canonical frozen foundation bytes differ'
 elif name.startswith('evidence|'):
  _,key,value=name.split('|',2)
  if key=='null':g['reviewed_files'][0]=None
  elif key=='duplicate':g['reviewed_files'].append(g['reviewed_files'][0])
  else:g['reviewed_files'][0][key]=json.loads(value)
  save(case/GATE,g);guard='Evidence duplicate/type/byte binding differs' if key=='duplicate' else 'Unsafe evidence path' if key=='path' else 'Evidence entry type/byte/hash schema'
 elif name.startswith('review|'):
  _,key,value=name.split('|',2)
  if key=='null':g['reviews'][-1]=None
  elif key=='missing':g['reviews'].pop()
  elif key=='duplicate':g['reviews'][-1]=g['reviews'][0]
  else:g['reviews'][-1][key]=json.loads(value)
  save(case/GATE,g);guard={'null':'Review entry schema','missing':'Nine actual complete reviews required','duplicate':'Unknown/duplicate family','reviewer':'Fresh numbered final operations reviewer required','raw_blocking_findings':'Final scope blockers','raw_required_repairs':'Final scope repairs','unresolved_disposition_issues':'Accepted classification has unresolved issues'}.get(key,'Report/result/manifest disconnected')
 elif name.startswith('ops|'):
  _,key,value=name.split('|',2);json_change(case,'reviews/'+FAKE+'/RESULT.json',lambda x:x.update({key:json.loads(value)}));guard='Actual reviewer result identity' if key in ['pr','reviewer','problem_id','frozen_head'] else 'Final operations reviewer binds different helper/synthesis' if key in ['reviewed_helper_sha256','reviewed_synthesis_sha256'] else 'Operations disposition issues' if key=='unresolved_disposition_issues' else 'Unresolved final classification/operations' if key in ['blocking_findings','required_repairs'] else 'Operations acceptance scope' if key in ['operations_approved','current_helper_accepted','acceptance_scope','publication_accepted'] else 'Final classification recommendation'
 elif name.startswith('dynamic_manifest|'):
  op=name.split('|')[1];p='reviews/'+FAKE+'/PUBLIC_FILES.json'
  if op=='missing_result':json_change(case,p,lambda x:x.update(files=[r for r in x['files'] if r['path']!='RESULT.json']));guard='Complete positive report/result packet required'
  elif op=='empty':json_change(case,p,lambda x:x.update(files=[]));guard='Empty positive manifest'
  elif op=='duplicate':json_change(case,p,lambda x:x['files'].append(x['files'][0]));guard='Complete public payload disconnected or drifted'
  elif op=='float_bytes':json_change(case,p,lambda x:x['files'][0].update(bytes=float(x['files'][0]['bytes'])),False);rebind_gate_only(case);guard='Manifest record byte/hash schema'
  elif op=='null':json_change(case,p,lambda x:x['files'].__setitem__(0,None));guard='Manifest record byte/hash schema'
 elif name.startswith('json|'):
  _,target,value=name.split('|',2);p=case/(GATE if target=='gate' else 'reviews/'+FAKE+'/RESULT.json');p.write_text(value)
  if target!='gate':rebind(case)
  guard='Duplicate JSON key' if '"pr":458,"pr":458' in value else 'Malformed JSON evidence' if value=='{' else 'Evidence JSON object required'
 elif name.startswith('topology|'):
  _,target,kind=name.split('|');p=case/target;dest=case/'sentinel'
  if p.exists():p.rename(dest)
  else:dest.write_text('sentinel')
  if kind=='symlink':p.symlink_to(dest)
  elif kind=='hardlink':os.link(dest,p)
  else:p.mkdir()
  guard='Output alias' if target.startswith('STATUS_') and kind=='symlink' else 'Nonregular/hardlinked output' if target.startswith('STATUS_') else 'Evidence topology'
 elif name=='audit_symlink':dest=case.parent/'real_case';case.rename(dest);case.symlink_to(dest,target_is_directory=True);guard='Output alias'
 elif name=='prior_operation':(case/'STATUS_REPAIR_OPERATION.json').write_text('{}');guard='Prior operation: no repeated mutation'
 elif name.startswith('excluded|'):
  status=name.split('|')[1];alter_queue(case,s,8,' '+status+' ')
  for f in FAMILIES:shutil.rmtree(case/'reviews'/f)
  (case/GATE).unlink();guard='Excluded status: stop without processing'
 elif name=='turns_drift':alter_queue(case,s,9,' 2/5 ');guard='Author turns/DOI drift'
 elif name=='doi_drift':alter_queue(case,s,12,' 10.fake ');guard='Author turns/DOI drift'
 elif name=='queue_hash_drift':s['blobs'][s['original_blob']]=base64.b64encode(b'changed').decode();guard='Frozen original QUEUE mismatch'
 elif name=='duplicate_row':
  b=base64.b64decode(s['blobs'][s['original_blob']]);b+=read(case/'SOURCE_RECEIPT.json')['selected_queue_row'].encode()+b'\n';s['blobs'][s['original_blob']]=base64.b64encode(b).decode();json_change(case,'SOURCE_RECEIPT.json',lambda x:x.update(queue_sha256=hashlib.sha256(b).hexdigest()));guard='Selected row not unique'
 elif name.startswith('pr|'):
  _,key,value,stage=name.split('|');s['config']={'pr_field':key,'pr_value':json.loads(value),'pr_stage':int(stage)};guard='Original open draft head/repository/base changed'
 elif name.startswith('ref|'):s['config']={'ref_stage':int(name.split('|')[1])};guard='Original branch ref changed'
 elif name=='tree_duplicate':s['config']={'duplicate_tree':True};guard='QUEUE Git tree path not unique'
 elif name=='tree_symlink':s['config']={'queue_mode':'120000'};guard='QUEUE not regular Git blob'
 elif name=='tree_wrong_type':s['config']={'queue_type':'tree'};guard='QUEUE not regular Git blob'
 elif name=='extra_commit_path':s['config']={'compare_paths':[QUEUE,'extra.txt']};guard='Commit changed other paths'
 elif name=='uncertain_unmoved':s['config']={'patch_fail':True,'patch_move':False};guard='Branch update uncertain; no retry'
 elif name=='success_unmoved':s['config']={'patch_move':False};guard='Branch readback differs'
 elif name=='malformed_unmoved':s['config']={'patch_raw':'{','patch_move':False};guard='Branch update uncertain; no retry'
 elif name=='wrong_blob':s['config']={'wrong_blob':True};guard='QUEUE blob exact bytes differ'
 elif name.startswith('api_raw|'):
  _,endpoint,raw=name.split('|',2);s['config']={'raw_endpoint':endpoint,'raw_response':raw};guard='Duplicate JSON key' if raw=='{"state":"open","state":"closed"}' else 'Malformed GitHub JSON response' if raw=='{' else 'GitHub response object required'
 elif name.startswith('fail|'):s['config']={'fail_endpoint':name[5:]};guard='Mock uncertain/error response'
 elif name.startswith('url|'):
  op=name.split('|')[1]
  if op=='mutable':g['published_disposition_url']=g['published_disposition_url'].replace('f'*40,'main')
  elif op=='query':g['published_disposition_url']+='?raw=1'
  elif op=='wrong_hash':g['published_disposition_sha256']='0'*64
  elif op=='wrong_repo':g['published_disposition_url']=g['published_disposition_url'].replace('AlecKriebel/Math','Other/Math')
  save(case/GATE,g);guard='Exact immutable published disposition URL/hash absent'
 elif name=='published_wrong_bytes':s['synthesis']=base64.b64encode(b'wrong').decode();guard='Immutable published synthesis bytes differ'
 elif name=='published_wrong_type':s['config']={'published_changes':{'type':'dir'}};guard='Published synthesis not a file'
 elif name=='published_wrong_path':s['config']={'published_changes':{'path':'wrong'}};guard='Published synthesis not a file'
 elif name in ['preflight','apply']:pass
 else:raise RuntimeError('Unimplemented control '+name)
 save(state,s);return apply,positive,guard

def rebind_gate_only(case):
 g=read(case/GATE)
 for r in g['reviewed_files']:r.update(bind(case/r['path']))
 save(case/GATE,g)
def alter_queue(case,s,index,value):
 old=read(case/'SOURCE_RECEIPT.json')['selected_queue_row'];cells=old.split('|');cells[index]=value;row='|'.join(cells);b=base64.b64decode(s['blobs'][s['original_blob']]).replace(old.encode(),row.encode());s['blobs'][s['original_blob']]=base64.b64encode(b).decode();json_change(case,'SOURCE_RECEIPT.json',lambda x:x.update(queue_sha256=hashlib.sha256(b).hexdigest(),selected_queue_row=row))

def cases():
 c=['preflight','apply','uncertain_moved','malformed_moved','duplicate_json_moved','json_array_moved','missing_gate','actual_unapproved_draft','raw_blockers_erased','coverage_vote_erased','helper_drift','synthesis_drift','foundation_resealed','missing_fixed_evidence','missing_mandatory','report_wrong_identity','missing_foundation_manifest_result','manifest_bytes_float','source_bytes_float','source_drift','evidence|null|null','evidence|duplicate|null','evidence|bytes|true','evidence|bytes|42.0','evidence|sha256|"BAD"','evidence|path|"../outside"','evidence|path|"private/foreign"','review|null|null','review|missing|null','review|duplicate|null','review|reviewer|"/root/other"','review|raw_blocking_findings|false','review|raw_required_repairs|0.0','review|unresolved_disposition_issues|false','prior_operation','audit_symlink','turns_drift','doi_drift','queue_hash_drift','duplicate_row','tree_duplicate','tree_symlink','tree_wrong_type','extra_commit_path','uncertain_unmoved','success_unmoved','malformed_unmoved','wrong_blob','published_wrong_bytes','published_wrong_type','published_wrong_path']
 for key,value in [('pr','458.0'),('publication_accepted','true'),('recommended_status','"solved"'),('acceptance_scope','"publish"'),('original_head','"changed"'),('operations_approval','false'),('not_an_action_gate','true'),('missing_actual_final_operations_review','true'),('root_read_entire_final_reports','false')]:c.append('gate|'+key+'|'+value)
 raw_mutations=[('reviews/whole_math_adversary/RESULT.json','current_publication_scope.accepted','true'),('reviews/euler_adversary/RESULT.json','asymptotic_proved','true'),('reviews/whole_math_adversary/RESULT.json','proposed_mathematical_interpretation_scope.unresolved_central_math_gaps','1'),('PRIORITY_ADVERSARY_FAMILY_READBACK.json','raw_counts.promotion_priority_blockers','0'),('reviews/priority_coverage/RESULT.json','count_scopes.actual_general_asymptotic_unproved_inputs','0'),('SOURCE_RECEIPT.json','pr','458.0'),('reviews/euler_adversary/RESULT.json','blocking_issues','0'),('reviews/euler_adversary/RESULT.json','required_repairs','0'),('reviews/euler_adversary/RESULT.json','unresolved_mathematical_gaps','1'),('reviews/unprimed_math_adversary/RESULT.json','blocking_findings','0'),('reviews/priority_coverage/RESULT.json','status_recommendation','"already_solved"'),('reviews/classification_adversary/RESULT.json','authority.operational_action_authorized_by_this_review','true')]
 for path,key,value in raw_mutations:c.append('foundation|'+path+'|'+key+'|'+value)
 for key,value in [('operations_approved','false'),('current_helper_accepted','false'),('operations_approved','1'),('publication_accepted','true'),('pr','458.0'),('reviewer','"/root/wrong"'),('blocking_findings','false'),('required_repairs','0.0'),('unresolved_disposition_issues','1'),('reviewed_helper_sha256','"stale"'),('reviewed_synthesis_sha256','"stale"'),('acceptance_scope','"publish"')]:c.append('ops|'+key+'|'+value)
 for op in ['missing_result','empty','duplicate','float_bytes','null']:c.append('dynamic_manifest|'+op)
 for target in ['gate','ops']:
  for value in ['{','[]','null','{"pr":458,"pr":458}']:c.append('json|'+target+'|'+value)
 for target in ['STATUS_REPAIR_PREFLIGHT.json','STATUS_REPAIR_OPERATION.json','STATUS_REPAIR_RECEIPT.json','reviews/source_admissibility/REPORT.md']:
  for kind in ['symlink','hardlink','directory']:c.append('topology|'+target+'|'+kind)
 for status in ['already_solved','unsolved','solved','out_of_scope','in_progress','pending','unknown']:c.append('excluded|'+status)
 for key,value in [('state','"closed"'),('draft','false'),('head.sha','"wrong"'),('head.ref','"other"'),('head.repo.full_name','"Other/Repo"'),('base.ref','"other"'),('base.repo.full_name','"Other/Repo"')]:
  for stage in [1,2,3]:c.append('pr|'+key+'|'+value+'|'+str(stage))
 for stage in [1,2,3]:c.append('ref|'+str(stage))
 for op in ['mutable','query','wrong_hash','wrong_repo']:c.append('url|'+op)
 for endpoint in ['pulls/458','git/blobs','git/trees','git/commits','compare/'+HEAD+'...'+NEW]:c.append('fail|'+endpoint)
 for raw in ['{','[]','null','{"state":"open","state":"closed"}']:c.append('api_raw|pulls/458|'+raw)
 return c

def execute(root,name,mode,index):
 program,case,state,binpath=fixture(root);apply,positive,guard=change(name,program,case,state)
 snapshot={str(p.relative_to(case)):bind(p) for p in (case/'source_snapshot').rglob('*') if p.is_file()}
 env=dict(os.environ);env['PATH']=str(binpath)+os.pathsep+env.get('PATH','');env['REVIEW_PRIVATE_STATE']=str(state);env['PYTHONDONTWRITEBYTECODE']='1'
 if mode=='optimized':env['PYTHONOPTIMIZE']='1'
 else:env.pop('PYTHONOPTIMIZE',None)
 cmd=[sys.executable,str(program/'repair_pr458_status.py')]+(['--apply'] if apply else [])
 proc=subprocess.run(cmd,capture_output=True,env=env,cwd=root,timeout=40);(root/'stdout').write_bytes(proc.stdout);(root/'stderr').write_bytes(proc.stderr);s=read(state);err=proc.stderr.decode();writes=[r for r in s['requests'] if r['method']!='GET'];patch=[r for r in writes if r['method']=='PATCH']
 after={str(p.relative_to(case)):bind(p) for p in (case/'source_snapshot').rglob('*') if p.is_file()};need(snapshot==after,'original research changed');need(len(patch)<=1,'blind retry')
 outcome='positive_pass' if positive and proc.returncode==0 else 'intended_rejection' if not positive and proc.returncode!=0 and guard in err else 'unexpected_acceptance' if not positive and proc.returncode==0 else 'wrong_guard_or_harness_failure'
 extra={}
 if outcome=='positive_pass':
  pre=read(case/'STATUS_REPAIR_PREFLIGHT.json');old=pre['selected_old_row'].split('|');new=pre['selected_new_row'].split('|');need([i for i,(a,b) in enumerate(zip(old,new)) if a!=b]==[8,11],'only status findings');need(old[9]==new[9] and new[9].strip()=='1/5','turns');need(old[12]==new[12] and new[12].strip()=='','actual DOI12')
  if apply:
   need(len(patch)==1 and patch[0]['payload']=={'sha':NEW,'force':False},'one nonforce PATCH');need(s['new_tree']=={'base_tree':'a'*40,'tree':[{'path':QUEUE,'mode':'100644','type':'blob','sha':s['new_blob']}]},'one QUEUE tree');need(s['new_commit']['parents']==[HEAD],'original parent');b=base64.b64decode(s['blobs'][s['original_blob']]);a=base64.b64decode(s['blobs'][s['new_blob']]);bl=b.splitlines(keepends=True);al=a.splitlines(keepends=True);need(len(bl)==len(al) and sum(x!=y for x,y in zip(bl,al))==1,'all other rows header bytes');need(read(case/'STATUS_REPAIR_RECEIPT.json')['state']=='status_repair_verified_immediately_excluded','receipt')
  else:need(len(writes)==0,'preflight mutation')
  extra={'only_status8_findings11_changed':True,'turns9_1_5_preserved':True,'DOI12_blank_and_preserved':True,'other_rows_headers_cells_preserved':True,'only_QUEUE_tree_path':apply}
 if name.startswith('excluded|'):need(not writes and not (case/'STATUS_REPAIR_PREFLIGHT.json').exists(),'excluded processed math or mutated')
 if name=='prior_operation':need(not s['requests'],'prior operation API')
 rec={'index':index,'case':name,'mode':mode,'outcome':outcome,'returncode':proc.returncode,'expected_guard':guard,'last_error':err.strip().splitlines()[-1] if err.strip() else '', 'stdout':bind(root/'stdout'),'stderr':bind(root/'stderr'),'API_calls':len(s['requests']),'git_writes':len(writes),'PATCH_count':len(patch),'ref_moved':s['ref']!=HEAD,'operation_marker_exists':(case/'STATUS_REPAIR_OPERATION.json').exists(),'receipt_exists':(case/'STATUS_REPAIR_RECEIPT.json').exists(),'27_source_fixture_files_unchanged':True,**extra}
 save(root/'RECORD.json',rec)
 repeat=None
 if name in ['apply','uncertain_moved','malformed_moved','duplicate_json_moved','json_array_moved','uncertain_unmoved','malformed_unmoved','success_unmoved','wrong_blob']:
  need((case/'STATUS_REPAIR_OPERATION.json').exists(),'no operation marker')
  prior=state.read_bytes();p2=subprocess.run(cmd,capture_output=True,env=env,cwd=root,timeout=40);(root/'repeat_stdout').write_bytes(p2.stdout);(root/'repeat_stderr').write_bytes(p2.stderr);need(p2.returncode!=0 and b'Prior operation: no repeated mutation' in p2.stderr,'repeat guard');need(prior==state.read_bytes(),'repeat API call');repeat={'mode':mode,'case':name,'returncode':p2.returncode,'API_calls_added':0,'PATCH_calls_added':0,'stderr':bind(root/'repeat_stderr')}
 return rec,repeat

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--run',required=True);args=parser.parse_args();need(args.run.isidentifier(),'run identifier');root=OWN/'private'/args.run;need(not root.exists(),'preserve earlier raw failures');root.mkdir();(root/'PRIVATE_ONLY.txt').write_text('Counterfactual fixture reports, results and gates. No actual approval authority. No external API capability.\n')
 rows=[];repeats=[];names=cases()
 for mode in ['normal','optimized']:
  for i,n in enumerate(names):
   rec,rep=execute(root/(mode+'_'+str(i)),n,mode,i);rows.append(rec)
   if rep:repeats.append(rep)
   save(root/'PARTIAL_RESULTS.json',{'runs':rows,'repeat_runs':repeats})
   if rec['outcome'] not in ['positive_pass','intended_rejection']:print(json.dumps(rec),flush=True)
 out={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewed_helper':bind(OWN/'REVIEWED_HELPER.py'),'case_count_per_mode':len(names),'executions':len(rows),'actual_second_invocations':len(repeats),'summary':{m:{o:sum(r['mode']==m and r['outcome']==o for r in rows) for o in ['positive_pass','intended_rejection','unexpected_acceptance','wrong_guard_or_harness_failure']} for m in ['normal','optimized']},'runs':rows,'repeats':repeats,'private_hypothetical_ninth_and_gate_only':True,'real_mutations':0}
 save(OWN/(args.run.upper()+'_CONTROLS.json'),out);print(json.dumps({k:v for k,v in out.items() if k not in ['runs','repeats']},indent=2))
if __name__=='__main__':main()
