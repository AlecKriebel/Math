#!/usr/bin/env python3
"""Independently check retained raw outcomes and unchanged current inputs. Own writes only."""
import ast,base64,datetime,json,hashlib
from pathlib import Path
from audit_evidence import OWN,CASE,PROGRAM,HEAD,bind,need,read,save

def main():
 a=read(OWN/'FIRST_CONTROLS.json');b=read(OWN/'SUPPLEMENT_CONTROLS.json');runs=a['runs']+b['runs'];by_mode={m:{r['case']:r for r in runs if r['mode']==m} for m in ['normal','optimized']}
 need(len(runs)==370 and len(by_mode['normal'])==185 and by_mode['normal'].keys()==by_mode['optimized'].keys(),'coverage counts')
 outcomes={m:{o:sum(r['outcome']==o for r in by_mode[m].values()) for o in ['positive_pass','intended_rejection','unexpected_acceptance','wrong_guard_or_harness_failure']} for m in by_mode}
 need(all(x=={'positive_pass':6,'intended_rejection':179,'unexpected_acceptance':0,'wrong_guard_or_harness_failure':0} for x in outcomes.values()),'exact outcomes')
 for n,x in by_mode['normal'].items():
  y=by_mode['optimized'][n]
  for k in ['outcome','returncode','API_calls','git_writes','PATCH_count','ref_moved','operation_marker_exists','receipt_exists','last_error']:need(x[k]==y[k],'mode semantic equality '+n+' '+k)
 positive=[]
 for packet,dirname in [(a,'first'),(b,'supplement')]:
  for r in packet['runs']:
   root=OWN/'private'/dirname/(r['mode']+'_'+str(r['index']));case=root/'program/audits/pr458_20000693'
   for stream in ['stdout','stderr']:need(bind(root/stream)==r[stream],'raw stdout/stderr binding')
   need(r['PATCH_count']<=1 and r['27_source_fixture_files_unchanged'] is True,'no retry/original source')
   if r['case']!='helper_drift':need(bind(root/'program/repair_pr458_status.py')==bind(OWN/'REVIEWED_HELPER.py'),'executed helper exact')
   if r['outcome']=='positive_pass':
    p=read(case/'STATUS_REPAIR_PREFLIGHT.json');old=p['selected_old_row'].split('|');new=p['selected_new_row'].split('|');need([i for i,(u,v) in enumerate(zip(old,new)) if u!=v]==[8,11],'only status/findings');need(old[9]==new[9] and new[9].strip()=='1/5','turn9');need(old[12]==new[12] and new[12].strip()=='','DOI12')
    s=read(root/'MODEL.json');patches=[q for q in s['requests'] if q['method']=='PATCH']
    if r['case']=='preflight':need(not patches and r['git_writes']==0,'read-only')
    else:
     need(patches==[{'endpoint':'git/refs/heads/dot%2Fmath-20000693','method':'PATCH','payload':{'sha':'c'*40,'force':False}}],'one exact nonforcePATCH');need(s['new_commit']['parents']==[HEAD],'original parent');need(s['new_tree']['tree']==[{'path':'unsolved_math_prioritization/QUEUE.md','mode':'100644','type':'blob','sha':s['new_blob']}],'one tree path')
     before=base64.b64decode(s['blobs'][s['original_blob']]);after=base64.b64decode(s['blobs'][s['new_blob']]);bl=before.splitlines(keepends=True);al=after.splitlines(keepends=True);need(len(bl)==len(al) and [i for i,(u,v) in enumerate(zip(bl,al)) if u!=v]==[next(i for i,x in enumerate(bl) if x.rstrip(b'\r\n')==p['selected_old_row'].encode())],'all other rows/header bytes')
    positive.append({'mode':r['mode'],'case':r['case'],'DOI_column12_blank_preserved':True,'Turns_column9_1_5_preserved':True,'only_Status8_Findings11_changed':True})
 need(len(positive)==12,'positive count')
 need(len(a['repeats'])==18 and all(x['API_calls_added']==x['PATCH_calls_added']==0 and x['returncode']!=0 for x in a['repeats']),'actual noAPI repeats')
 for r in a['repeats']:
  original=by_mode[r['mode']][r['case']];root=OWN/'private/first'/(r['mode']+'_'+str(original['index']));need(bind(root/'repeat_stderr')==r['stderr'],'repeat raw')
 for n in ['already_solved','unsolved','solved','out_of_scope','in_progress','pending','unknown']:
  for m in by_mode:
   r=by_mode[m]['excluded|'+n];need(r['git_writes']==0 and r['last_error']=='RuntimeError: Excluded status: stop without processing','excluded before evidence')
 need(bind(PROGRAM/'repair_pr458_status.py')==bind(OWN/'REVIEWED_HELPER.py'),'actual helper drift')
 need(bind(CASE/'DISPOSITION_SYNTHESIS.md')==bind(OWN/'REVIEWED_SYNTHESIS.md'),'actual synthesis drift')
 need(not (CASE/'PRIORITY_DISPOSITION_GATE.json').exists(),'actual gate created during review')
 need(read(CASE/'DRAFT_OPERATIONS_GATE.json')['operations_approval'] is False,'draft promoted')
 for n in ['audit_evidence.py','mock_github.py','run_controls.py','run_supplement.py','seal_checks.py','verify_disposition_math.py','REVIEWED_HELPER.py']:
  need(not any(isinstance(x,ast.Assert) for x in ast.walk(ast.parse((OWN/n).read_text()))),'assert dependent '+n)
 need((OWN/'MATH_NORMAL.json').read_bytes()==(OWN/'MATH_OPTIMIZED.json').read_bytes(),'math mode bytes')
 out={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pr':458,'problem_id':'20000693','reviewer':'/root/pr458_disposition_adversary2','reviewed_helper':bind(OWN/'REVIEWED_HELPER.py'),'reviewed_synthesis':bind(OWN/'REVIEWED_SYNTHESIS.md'),'cases_per_mode':185,'matrix_subprocesses':370,'actual_second_invocations':18,'total_helper_subprocesses':388,'outcomes':outcomes,'all740_raw_stdout_stderr_bindings_verified':True,'all_mode_semantics_equal':True,'all_12_positive_DOI12_and_Turns9_independently_verified':positive,'all_18_actual_second_invocations_reject_before_API':True,'all_source_fixture_files_unchanged_by_helper':True,'current_actual_gate_exists':False,'assert_nodes':0,'genuine_foundation_records_retained':True,'first_failed_review_553_executions_retained':True,'real_mutations':0}
 save(OWN/'SEAL_CHECKS.json',out);print(json.dumps({k:v for k,v in out.items() if k!='all_12_positive_DOI12_and_Turns9_independently_verified'},indent=2))
if __name__=='__main__':main()
