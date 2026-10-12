from pathlib import Path
import subprocess,json,datetime,hashlib,base64,re,os
A=Path(__file__).resolve().parent;C=A.parents[2];P=A.parents[1];D=P/'ordered_intake_20261005/after_PR95';D.mkdir(parents=True,exist_ok=False);records=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(c,m):
 if not c:raise RuntimeError(m)
def run(argv):
 t=now();p=subprocess.Popen(argv,cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate();records.append({'argv':argv,'actual_PID':p.pid,'UTC_start':t,'UTC_end':now(),'exit_code':p.returncode,'stdout_bytes':len(out),'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_bytes':len(err),'stderr_sha256':hashlib.sha256(err).hexdigest(),'retention':'Status/identity projection only; excluded mathematical prose is not retained.'});require(p.returncode==0,err.decode()[:1000]);return out
release=json.loads((A/'ROOT_FINAL_COMPLETION_RELEASE_20261005.json').read_text());require(release['advance_to_next_status_intake_authorized'] and release['metadata_remote_verified'],'completion gate')
require(run(['git','symbolic-ref','--short','HEAD']).strip()==b'main','branch');require(run(['git','rev-parse','HEAD']).strip().decode()==release['metadata_commit'],'main head')
raw=run(['/opt/homebrew/bin/gh','pr','list','--repo','AlecKriebel/Math','--state','open','--limit','1000','--json','number,isDraft,headRefOid,headRefName,baseRefName,url']);prs=sorted((r for r in json.loads(raw) if r['number']>95 and r['isDraft']),key=lambda r:r['number']);observations=[];next_pr=None
for pr in prs:
 match=re.fullmatch(r'dot/math-(\d+)',pr['headRefName'])
 if not match:continue
 pid=match[1];response=run(['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+pr['headRefOid']]);x=json.loads(response);qb=base64.b64decode(x['content']);require(x['encoding']=='base64' and hashlib.sha1(b'blob '+str(len(qb)).encode()+b'\0'+qb).hexdigest()==x['sha'],'queue blob identity');rows=[]
 for s in qb.decode().splitlines():
  if s.startswith('|'):
   cells=s.split('|')
   if len(cells)>12 and cells[2].strip().split('/')[0].strip()==pid:rows.append((s,cells))
 require(len(rows)==1,'unique status row for '+pid);row,cells=rows[0];status=cells[8].strip();eligible=status=='claimed_solved';o={'PR':pr['number'],'problem_id':pid,'current_GitHub_metadata':pr,'literal_submitted_status':status,'original_budget':cells[9].strip(),'eligible':eligible,'QUEUE_blob_SHA1':x['sha'],'whole_QUEUE_bytes':len(qb),'whole_QUEUE_sha256':hashlib.sha256(qb).hexdigest(),'selected_row_sha256':hashlib.sha256(row.encode()).hexdigest(),'excluded_science_reviewed_or_retained':False,'action':'CONTINUE_ORDERED_REVIEW' if eligible else 'SKIP_ENTIRELY_NONCLAIM_STATUS'};observations.append(o)
 if eligible:next_pr=pr['number'];break
out={'schema':'ordered-status-intake-after-PR95/v1','UTC':now(),'actual_reader_PID':os.getpid(),'previous_completed_PR':95,'completed_metadata_commit':release['metadata_commit'],'completion_release_sha256':hashlib.sha256((A/'ROOT_FINAL_COMPLETION_RELEASE_20261005.json').read_bytes()).hexdigest(),'observations':observations,'next_eligible_PR':next_pr,'actual_commands':records,'excluded_science_processed':False};(D/'INTAKE_AFTER_PR95.json').write_text(json.dumps(out,indent=2)+'\n');(D/'RESEARCH_LOG.md').write_text('# Ordered intake after PR95\n\n'+out['UTC']+' — status-only intake complete (100%). PR95 workflow is complete; dated program 13/99 (13.13%). Only current draft head QUEUE statuses were parsed. Excluded mathematics was not reviewed or retained. Next eligible PR: '+str(next_pr)+'.\n');print(json.dumps({'next_eligible_PR':next_pr,'observations':[{'PR':r['PR'],'problem_id':r['problem_id'],'literal_status':r['literal_submitted_status'],'original_budget':r['original_budget']} for r in observations]}))
