#!/usr/bin/env python3
"""Independently bind genuine packets. Writes solely this review folder."""
import ast,datetime,hashlib,json,re
from pathlib import Path
OWN=Path(__file__).resolve().parent
CASE=OWN.parent.parent
PROGRAM=CASE.parent.parent
HEAD='87a39f7b4e5ef81aacf98464f86586cc95684d7f'
FAMILIES={'source_admissibility':('reviewer','problem_id','blocking_issues',0,0,'unresolved_mathematical_gaps'),'euler_adversary':('reviewer','problem_id','blocking_issues',1,1,'unresolved_mathematical_gaps'),'reproduction':('reviewer','problem_id','blocking_issues',1,3,'unresolved_mathematical_gaps'),'whole_math_adversary':('reviewer','problem_id','blocking_issues',2,4,'unresolved_mathematical_gaps'),'unprimed_math_adversary':('reviewer','problem_id','blocking_issues',2,4,'unresolved_mathematical_gaps'),'priority_adversary':('reviewer_task','problem','blocking_findings',1,5,'central_mathematical_gaps'),'priority_coverage':('reviewer_task_identity','problem_id','blocking_findings',1,2,'central_mathematical_gaps'),'classification_adversary':('reviewer_task_identity','problem_id','blocking_findings',0,0,'central_mathematical_gaps')}
def need(c,m):
 if not c:raise RuntimeError(m)
def bind(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(p):return json.loads(p.read_text())
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def check_record(base,r):
 need(type(r) is dict and type(r['bytes']) is int and r['bytes']>0,'strict record')
 n=r['path'];need(type(n) is str and n==Path(n).as_posix() and not Path(n).is_absolute() and '..' not in Path(n).parts,'path')
 p=base/n;need(p.resolve()==p and p.is_file() and p.stat().st_nlink==1,'topology')
 need(bind(p)=={k:r[k] for k in ['bytes','sha256']},'binding '+n)
 return {'path':n,**bind(p)}
def main():
 g=read(CASE/'DRAFT_OPERATIONS_GATE.json');need(g['operations_approval'] is False and g['not_an_action_gate'] is True and g['missing_actual_final_operations_review'] is True and len(g['reviews'])==8,'actual unapproved')
 need(not (CASE/'PRIORITY_DISPOSITION_GATE.json').exists(),'actual gate exists')
 records=[check_record(CASE,r) for r in g['reviewed_files']];need(len(records)==187 and len({x['path'] for x in records})==187,'draft evidence count')
 foundation=read(CASE/'FROZEN_FOUNDATION_BINDINGS.json');need(bind(CASE/'FROZEN_FOUNDATION_BINDINGS.json')['sha256']=='84281ba210adf18cf431cc4ec9ede8e32873f680852e48ef5e7ef601ca4b0303','literal pin');need(len(foundation['files'])==158,'foundation count')
 for r in foundation['files']:check_record(CASE,r)
 source=read(CASE/'SOURCE_RECEIPT.json');need(len(source['files'])==27 and type(source['pr']) is int and source['pr']==458 and source['head_sha']==HEAD,'source identity')
 for r in source['files']:check_record(CASE/'source_snapshot',r)
 payloads=[];counts=[]
 for f,spec in FAMILIES.items():
  d=CASE/'reviews'/f; rk,pk,bk,bc,rc,gk=spec;r=read(d/'RESULT.json')
  need(r[rk]=='/root/pr458_'+f and r[pk]=='20000693' and type(r['pr']) is int and r['pr']==458 and r['frozen_head']==HEAD,'identity '+f)
  for k,n in [(bk,bc),('required_repairs',rc),(gk,0)]:need(type(r[k]) is int and r[k]==n,f+' count '+k)
  m=read(d/'PUBLIC_FILES.json');need({'REPORT.md','RESULT.json'}<={x['path'] for x in m['files']},'report/result membership')
  for rec in m['files']:payloads.append({'family':f,**check_record(d,rec)})
  counts.append({'family':f,'blockers':bc,'repairs':rc,'central_heuristic_gaps':0,'status_recommendation':r.get('status_recommendation')})
 # Every positive failure-record byte is independently checked and every JSON parsed.
 old=CASE/'reviews/disposition_adversary1';old_m=read(old/'PUBLIC_FILES.json');oldrecs=[]
 for r in old_m['files']:
  oldrecs.append(check_record(old,r))
  if Path(r['path']).suffix=='.json':read(old/r['path'])
 oldr=read(old/'RESULT.json');need([oldr[k] for k in ['blocking_findings','required_repairs','unresolved_disposition_issues']]==[3,3,3] and oldr['operations_approved'] is False and oldr['publication_accepted'] is False,'old failure preserved')
 history=[('INITIAL_PARTIAL_CONTROLS.json',75),('INITIAL_COMPLETE_CONTROLS.json',226),('INITIAL_REPEAT_CONTROLS.json',10),('CONTROL_RESULTS.json',232),('REPEAT_CONTROLS.json',10)]
 for n,c in history:need(len(read(old/n)['runs'])==c,'old executions '+n)
 for name in ['SOURCE_FAMILY_READBACK.json','MATHEMATICAL_FAMILIES_READBACK.json','WHOLE_MATH_FAMILY_READBACK.json','UNPRIMED_MATH_FAMILY_READBACK.json','PRIORITY_ADVERSARY_FAMILY_READBACK.json','PRIORITY_COVERAGE_FAMILY_READBACK.json','CLASSIFICATION_FAMILY_READBACK.json']:
  r=read(CASE/name)
  def walk(x):
   if isinstance(x,dict):
    if {'path','bytes','sha256'}<=set(x) and (CASE/x['path']).is_file():check_record(CASE,x)
    for y in x.values():walk(y)
   elif isinstance(x,list):
    for y in x:walk(y)
  walk(r)
 for r in records:
  p=CASE/r['path']
  if p.suffix=='.json':read(p)
 need(len(payloads)==100,'eight positive records')
 need(bind(OWN/'REVIEWED_HELPER.py')==bind(PROGRAM/'repair_pr458_status.py'),'current helper drift')
 need(bind(OWN/'REVIEWED_SYNTHESIS.md')==bind(CASE/'DISPOSITION_SYNTHESIS.md'),'current synthesis drift')
 need(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse((OWN/'REVIEWED_HELPER.py').read_text()))),'assert guard')
 save(OWN/'INPUT_BINDINGS.json',{'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pr':458,'problem_id':'20000693','frozen_head':HEAD,'helper':bind(OWN/'REVIEWED_HELPER.py'),'synthesis':bind(CASE/'DISPOSITION_SYNTHESIS.md'),'actual_action_gate_exists':False,'draft_approval':False,'evidence':records,'fixed_foundation_files':158,'source_files':27,'positive_payloads':payloads,'foundation_counts':counts,'retained_first_failed_review':oldrecs,'retained_first_failed_executions':553,'strict_jsons_parsed':True})
 print(json.dumps({'draft_evidence':len(records),'foundation_fixed':158,'source':27,'eight_positive_payloads':len(payloads),'failed_review_positive_payloads':len(oldrecs),'first_failure_executions':553,'result':'PASS'}))
if __name__=='__main__':main()
