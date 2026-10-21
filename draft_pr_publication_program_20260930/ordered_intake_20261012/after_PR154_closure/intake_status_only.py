#!/usr/bin/env python3
"""Read only submitted QUEUE statuses after actual PR154 closure; findings checkpoint pending."""
import base64,datetime,hashlib,json,subprocess
from pathlib import Path
P=Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout")/'draft_pr_publication_program_20260930'
A=P/'audits/pr154_30000229'
F=Path(__file__).resolve().parent
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
REG=Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/claimed_solved_scope_20261003/LIVE_DRAFT_ELIGIBILITY_REGISTRY.json')
def require(c,m):
 if not c:raise RuntimeError(m)
def api(e):
 r=subprocess.run([GH,'api','repos/AlecKriebel/Math/'+e],capture_output=True,text=True,timeout=90)
 require(r.returncode==0,r.stderr[:800]);return json.loads(r.stdout)
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(n,j):(F/n).write_text(json.dumps(j,indent=2)+'\n')
closure=json.loads((A/'PR_CLOSURE_ACCEPTANCE.json').read_text())
require(closure['status']=='ACTUAL_PR_CLOSED_UNMERGED_AND_EXACT_COMMENT_METADATA_ACCEPTED','Actual preceding closure required')
body=REG.read_bytes();known={r['pr']:r for r in json.loads(body)['rows']}
records=[]
for number in range(155,501):
 if number not in known:continue
 k=known[number];pr=api('pulls/'+str(number))
 require(pr['state']=='open' and pr['draft'] and pr['head']['sha']==k['headRefOid'],'Original draft/head changed '+str(number))
 targets=k['status_projection']['targets'];require(len(targets)==1,'Ambiguous original target')
 pid=targets[0]['problem_id'];head=pr['head']['sha']
 q=api('contents/unsolved_math_prioritization/QUEUE.md?ref='+head)
 require(q['encoding']=='base64','QUEUE encoding changed')
 b=base64.b64decode(q['content']);blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 require(blob==q['sha']==k['status_projection']['git_blob_oid'],'Submitted QUEUE identity differs')
 rows=[]
 for line in b.decode().splitlines():
  cells=[x.strip() for x in line.split('|')]
  if len(cells)>9 and cells[2].split(' / ',1)[0]==pid:rows.append((line,cells))
 require(len(rows)==1,'Target row not unique')
 line,cells=rows[0];status=cells[8];require(status==targets[0]['status'],'Original literal status differs')
 rec={'UTC':utc(),'PR':number,'original_head':head,'problem_id':pid,'code':cells[2],'literal_status':status,'effort':cells[9],'original_QUEUE_git_blob':blob,'whole_QUEUE_sha256':hashlib.sha256(b).hexdigest(),'target_row_sha256':hashlib.sha256(line.encode()).hexdigest(),'reviewed':False,'science_findings_retained':False,'action':'ELIGIBLE_NEXT_CLAIMED_SOLVED' if status=='claimed_solved' else 'SKIP_UNTOUCHED_NONCLAIMED','state':pr['state'],'draft':pr['draft'],'title':pr['title']}
 require(api('pulls/'+str(number))['head']['sha']==head,'Head moved during intake')
 records.append(rec);save('PR'+str(number)+'_STATUS_ONLY.json',rec);print(json.dumps(rec),flush=True)
 if status=='claimed_solved':break
require(records and records[-1]['literal_status']=='claimed_solved','No eligible next case')
save('INTAKE_AFTER_PR154_CLOSURE.json',{'UTC':utc(),'status':'PASS_READ_ONLY_ORDERED_LITERAL_STATUS_INTAKE','records':records,'next_eligible':records[-1]['PR'],'preceding_PR154_actually_closed':True,'preceding_PR154_findings_checkpoint_pending':True,'preceding_PR154_not_marked_fully_complete':True,'authorization_basis':'Actual closed disposition and priority decision complete; status-only read overlaps separately coordinated findings checkpoint. No MAIN/PR/ref/index mutations or new publication. Only literal original claimed_solved retained.','dated_registry_sha256':hashlib.sha256(body).hexdigest(),'MAIN_or_PR_or_index_or_ref_mutations':False,'fully_completed_count_unchanged':29,'persistent_goal_complete':False})
(F/'RESEARCH_LOG.md').write_text(utc()+' — Status-only original-head intake complete; next literal claimed_solved PR'+str(records[-1]['PR'])+'; all other statuses untouched. Preceding154 actual closed, findings checkpoint pending, no inflated completion. Programme29/dated99 complete,17published, goal active. Intake100%; mathematical audit0%.\n')

