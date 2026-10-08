"""Ascending status-only intake after genuine completed PR147."""
from pathlib import Path
import argparse,json,os,base64,types,hashlib
parser=argparse.ArgumentParser();parser.add_argument('--acceptance-sha',required=True);args=parser.parse_args()
R=Path('/Users/alec/Documents/Math')
C=R/'draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout'
P=C/'draft_pr_publication_program_20260930'
A=P/'audits/pr147_5100001';F=P/'ordered_intake_20261008/after_PR147'
source=A/'final_completion_operator_preparation_20261008/final_completion_operator.py'
body=source.read_bytes()
if len(body)!=31924 or hashlib.sha256(body).hexdigest()!='74eef283454986dcd2d8678465465fab4141896d8bb77b69068a1eda52ca69a8':raise RuntimeError('audited final source')
f=types.ModuleType('readonly_intake_mechanisms');f.__file__=str(source);exec(compile(body,str(source),'exec'),f.__dict__)
s=f.m
accept=A/'ROOT_FINAL_METADATA_ACCEPTANCE_20261008.json'
gate=f.path_pin(accept);s.require(gate['sha256']==args.acceptance_sha,'actual final ROOT acceptance exact pin')
a=s.native_json(f.read(gate))
s.require(a['schema']=='pr147-root-actual-final-metadata-acceptance/v1' and a['status']=='ACCEPTED_FINAL_PUBLIC_PACKAGE_AND_LOCAL_PROGRAM3' and a['PR']==147,'actual final case accepted')
s.require(a['public_full_body_mode_readback'] is True and a['local_full_body_mode_readback'] is True and a['all_obtained_children_complete'] is True and a['own_operation_lock_released'] is True and a['cooperative_known_selected_writer_exclusion_confirmed'] is True,'completed public/local/custody/release')
s.require(a['overall_goal_complete'] is False and a['persistent_goal_status']=='active' and a['fully_completed_count']==26 and a['published_count']==14 and a['next_numeric_intake_cursor']==148,'unfinished goal26/14 next148')
for key in ['source','dependency','request','plan','review','published','installed','independent_ROOT_execution']:s.full_pin(a[key])
root=s.native_json(f.read(a['independent_ROOT_execution']))
s.require(root['status']=='PASS' and s.children_custody_complete(root),'actual independent ROOT closed final readback')
for child in root['children']:s.authenticate_child_custody(child);s.require(child['exit_code']==0,'successful final ROOT child')
program=s.native_json((P/'CURRENT_PROGRESS.json').read_bytes())
s.require(program['current_PR']==147 and program['fully_completed_count']==26 and program['published_count']==14 and program['persistent_goal_complete'] is False,'current complete program baseline')
s.require(not(f.D/'private/OPERATION_LOCK.json').exists(),'owned final barrier released')
pub=s.native_json(f.read(a['published']))
custody=f.D/'private/ROOT_AFTER147_INTAKE_OBSERVATIONS_01';custody.mkdir(exist_ok=False)
j={'schema':'ordered-literal-status-intake/v1','actual_PID':os.getpid(),'UTC_start':s.utc(),'children':[],'child_custody_root':str(custody/'raw'),'object_workspace':pub['object_workspace'],'provider_mutation_performed':False,'PR_science_review_performed':False}
s.dump(custody/'RECEIPT.json',j)
records=[]
try:
 s.require(s.remote(j)==a['final_commit'],'fresh direct main exact accepted final metadata commit')
 registry=s.native_json(s.git(['cat-file','blob',a['final_commit']+':draft_pr_publication_program_20260930/claimed_solved_scope_20261003/LIVE_DRAFT_ELIGIBILITY_REGISTRY.json'],j))
 known={x['pr']:x for x in registry['rows']}
 live=s.native_json(s.run([f.n.GH,'pr','list','--repo','AlecKriebel/Math','--state','open','--limit','1000','--json','number,title,isDraft,headRefOid'],j))
 ordered=sorted([x for x in live if x['isDraft'] and x['number']>=148 and x['number']!=8],key=lambda x:x['number'])
 s.dump(F/'OPEN_DRAFT_METADATA_SNAPSHOT.json',{'UTC':s.utc(),'actual_PID':os.getpid(),'rows':ordered,'scope':'PR metadata inventory only; no math/results read or reviewed'})
 with (F/'RESEARCH_LOG.md').open('a') as log:log.write('\n'+s.utc()+' — Ascending literal status intake after actual PR147 final acceptance '+a['final_commit']+'. Completed26/99=26.26%,14 publications; persistent goal active and incomplete.\n')
 for item in ordered:
  number=item['number']
  p=s.native_json(s.run([f.n.GH,'pr','view',str(number),'--repo','AlecKriebel/Math','--json','number,isDraft,state,headRefOid'],j))
  s.require(p['number']==number and p['state']=='OPEN' and p['isDraft'] is True,'live draft metadata identity')
  head=p['headRefOid'];s.require(head==item['headRefOid'],'original head unchanged since metadata inventory')
  s.require(number in known and known[number]['headRefOid']==head,'new/changed target needs separate unambiguous status-only identification')
  targets=known[number]['status_projection']['targets'];s.require(len(targets)==1,'one exact problem required');pid=targets[0]['problem_id']
  c=s.native_json(s.run([f.n.GH,'api','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+head],j))
  s.require(c['encoding']=='base64','QUEUE provider encoding')
  b=base64.b64decode(c['content'].replace('\n',''),validate=True);rows=[]
  s.require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==c['sha'],'full submitted QUEUE Git identity')
  for row in b.decode().splitlines():
   cells=[x.strip() for x in row.split('|')]
   if len(cells)>9 and cells[2].split(' / ',1)[0]==pid:rows.append((row,cells))
  s.require(len(rows)==1,'unique target QUEUE row');row,cells=rows[0];status=cells[8]
  record={'PR':number,'original_head':head,'problem_id':pid,'code':cells[2],'literal_status':status,'effort':cells[9],
   'selected_row_sha256':s.digest(row.encode()),'whole_QUEUE_sha256':s.digest(b),'QUEUE_Git_blob':c['sha'],'UTC':s.utc(),'actual_reader_PID':os.getpid(),
   'reviewed':False,'original_substantive_findings_retained':False,'action':'ELIGIBLE_NEXT_CLAIMED_SOLVED' if status=='claimed_solved' else 'SKIP_UNTOUCHED_NONCLAIMED'}
  records.append(record);s.dump(F/('PR'+str(number)+'_STATUS_ONLY.json'),record)
  with (F/'RESEARCH_LOG.md').open('a') as log:log.write(record['UTC']+' — PR'+str(number)+': literal '+status+', effort '+cells[9]+'. '+record['action']+'; no math review, repair, PR comment, merge, close or publication performed.\n')
  print(json.dumps(record),flush=True)
  if status=='claimed_solved':break
 s.require(s.remote(j)==a['final_commit'],'direct main remains unchanged during status-only intake')
 j.update(status='PASS',records=records,next_eligible=records[-1]['PR'] if records and records[-1]['literal_status']=='claimed_solved' else None,prior_acceptance=gate,prior_acceptance_commit=a['final_commit'],program_workflow_percent=26/99*100,goal_complete=False)
except BaseException as error:j.update(status='FAIL',error_type=type(error).__name__,error=str(error));raise
finally:
 j.update(UTC_end=s.utc(),all_obtained_children_complete=s.children_custody_complete(j));s.dump(custody/'RECEIPT.json',j)
s.require(j['all_obtained_children_complete'],'complete intake custody')
for child in j['children']:s.authenticate_child_custody(child);s.require(child['exit_code']==0,'successful intake child')
s.dump(F/'INTAKE_AFTER_PR147.json',j)
print(json.dumps({'status':'PASS','next_eligible':j['next_eligible'],'record_count':len(records),'children':len(j['children'])}))

