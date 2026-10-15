#!/usr/bin/env python3
"""Independent byte/type/path checks of actual evidence; never writes outside own folder."""
import ast, datetime, hashlib, json
from pathlib import Path

OWN = Path(__file__).resolve().parent
CASE = OWN.parent.parent
PROGRAM = CASE.parent.parent
HEAD = '87a39f7b4e5ef81aacf98464f86586cc95684d7f'
FAMILIES = {
 'source_admissibility': ('reviewer','problem_id','blocking_issues',0,0,'unresolved_mathematical_gaps'),
 'euler_adversary': ('reviewer','problem_id','blocking_issues',1,1,'unresolved_mathematical_gaps'),
 'reproduction': ('reviewer','problem_id','blocking_issues',1,3,'unresolved_mathematical_gaps'),
 'whole_math_adversary': ('reviewer','problem_id','blocking_issues',2,4,'unresolved_mathematical_gaps'),
 'unprimed_math_adversary': ('reviewer','problem_id','blocking_issues',2,4,'unresolved_mathematical_gaps'),
 'priority_adversary': ('reviewer_task','problem','blocking_findings',1,5,'central_mathematical_gaps'),
 'priority_coverage': ('reviewer_task_identity','problem_id','blocking_findings',1,2,'central_mathematical_gaps'),
 'classification_adversary': ('reviewer_task_identity','problem_id','blocking_findings',0,0,'central_mathematical_gaps')}

def check(c, message):
 if not c: raise RuntimeError(message)
def binding(p):
 b=p.read_bytes(); return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def exact_record(p,rec):
 check(p.resolve()==p and p.is_file() and p.stat().st_nlink==1, str(p)+' topology')
 check(type(rec['bytes']) is int and rec['bytes']>0 and type(rec['sha256']) is str, 'record types')
 check(binding(p)=={k:rec[k] for k in ['bytes','sha256']}, str(p)+' hash')
def main():
 gate=json.loads((CASE/'DRAFT_OPERATIONS_GATE.json').read_text())
 check(gate['operations_approval'] is False and gate['not_an_action_gate'] is True, 'actual draft approval')
 check(not (CASE/'PRIORITY_DISPOSITION_GATE.json').exists(), 'Unexpected actual action gate')
 check(len(gate['reviews'])==8, 'actual foundation count')
 evidence={}
 for rec in gate['reviewed_files']:
  check(rec['path'] not in evidence, 'duplicate evidence')
  exact_record(CASE/rec['path'],rec); evidence[rec['path']]=rec
 source=json.loads((CASE/'SOURCE_RECEIPT.json').read_text())
 check(source['head_sha']==HEAD and type(source['pr']) is int and source['pr']==458, 'source identity')
 check(len(source['files'])==27, 'source count')
 for rec in source['files']: exact_record(CASE/'source_snapshot'/rec['path'],rec)
 q=(CASE/'private_cases/original_QUEUE.md').read_bytes()
 check(hashlib.sha256(q).hexdigest()==source['queue_sha256'], 'original queue')
 rows=[x for x in q.decode().splitlines() if x.startswith('|') and x.split('|')[2].strip().startswith('20000693 /')]
 check(rows==[source['selected_queue_row']], 'selected row')
 summaries=[]; payloads=[]
 for family, spec in FAMILIES.items():
  rkey,pkey,bkey,block,repairs,gkey=spec
  d=CASE/'reviews'/family
  result=json.loads((d/'RESULT.json').read_text())
  check(type(result['pr']) is int and result['pr']==458 and result[pkey]=='20000693' and result['frozen_head']==HEAD, family+' identity')
  check(result[rkey]=='/root/pr458_'+family, family+' reviewer')
  for key,want in [(bkey,block),('required_repairs',repairs),(gkey,0)]:
   check(type(result[key]) is int and result[key]==want, family+' count '+key)
  manifest=json.loads((d/'PUBLIC_FILES.json').read_text()); seen=set()
  for rec in manifest['files']:
   name=rec['path']; p=d/name
   check(type(name) is str and not Path(name).is_absolute() and '..' not in Path(name).parts and Path(name).as_posix()==name, 'manifest path')
   check(name not in seen and name!='PUBLIC_FILES.json', 'manifest duplicate/self')
   check(not {'private','private_sources','private_cases','venv','__pycache__'}.intersection(Path(name).parts), 'private manifest')
   exact_record(p,rec); seen.add(name); payloads.append({'family':family,'path':name,**binding(p)})
  check({'REPORT.md','RESULT.json'}<=seen, 'report/result missing')
  review=next(x for x in gate['reviews'] if x['family']==family)
  check(review['raw_blocking_findings']==block and review['raw_required_repairs']==repairs, 'gate raw counts')
  summaries.append({'family':family,'blockers':block,'repairs':repairs,'central_heuristic_gaps':0,'status_recommendation':result.get('status_recommendation'), 'result':binding(d/'RESULT.json'),'report':binding(d/'REPORT.md'),'manifest':binding(d/'PUBLIC_FILES.json')})
 helper=PROGRAM/'repair_pr458_status.py'
 check(not any(isinstance(x,ast.Assert) for x in ast.walk(ast.parse(helper.read_text()))), 'helper assertions')
 out={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pr':458,'problem_id':'20000693','frozen_head':HEAD,'actual_foundations':8,'actual_evidence_files':len(evidence),'positive_manifest_records':len(payloads),'frozen_research_files':27,'helper':binding(helper),'synthesis':binding(CASE/'DISPOSITION_SYNTHESIS.md'),'foundations':summaries,'positive_payload_bindings':payloads,'actual_approval_gate_exists':False,'original_publication_blockers':['H1','V1'],'original_publication_correction_groups':['H1','V1','P2','C3']}
 (OWN/'INPUT_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k not in ['positive_payload_bindings','foundations']},indent=2))
if __name__=='__main__': main()
