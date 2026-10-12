"""Descending status-only original-QUEUE eligibility filter after PR302.

No excluded problem mathematics, repair, comment, merge or service mutation.
Complete read-only native API captures are retained. Stop at the first eligible
open draft whose original inventory head has exactly claimed_solved status.
"""
from pathlib import Path
from datetime import datetime,timezone
import base64,gzip,hashlib,json,os,re,stat,subprocess,sys
R=Path('/Users/alec/Documents/Math');P=Path(__file__).parent;D=P/'status_filter_after_pr302_20261005_v02';sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat();load=lambda p:json.loads(Path(p).read_bytes())
def need(v,m):
 if not v:raise RuntimeError(m+'; preserve read-only evidence and do not process an unauthenticated status')
def pin(p):
 p=Path(p);need(p.is_file() and not p.is_symlink(),'literal complete artifact');b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
def capture(directory,label,endpoint):
 q=directory/label;q.mkdir();argv=['/opt/homebrew/bin/gh','api',endpoint];request=dict(argv=argv,cwd=str(R),requested_UTC=utc(),source=pin(__file__),automatic_retry=False);(q/'request.json').write_text(json.dumps(request,indent=2)+'\n');(q/'source.gz').write_bytes(gzip.compress(Path(__file__).read_bytes(),mtime=0));proc=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);started=dict(**request,actual_PID=proc.pid,start_UTC=utc());(q/'started.json').write_text(json.dumps(started,indent=2)+'\n');out,err=proc.communicate(timeout=55);streams={}
 for n,b in [('stdout',out),('stderr',err)]:
  z=q/(n+'.gz');z.write_bytes(gzip.compress(b,mtime=0));streams[n]=dict(stored=pin(z),logical_bytes=len(b),logical_sha256=sha(b))
 (q/'execution.json').write_text(json.dumps(dict(**started,end_UTC=utc(),exit_code=proc.returncode,parent_reaped=True,read_only=True,streams=streams),indent=2)+'\n');need(proc.returncode==0 and not err,'actual read-only API result');return json.loads(out)
def main():
 need(not sys.flags.optimize,'no optimization');accepted=P/'audits/pr302_30003508/ROOT_ACTUAL_COMPLETION_CHECKPOINT038_ACCEPTANCE.json';a=load(accepted);need(a['status']=='ROOT_ACCEPTS_ACTUAL_PR302_COMPLETION_CHECKPOINT038' and a['actual_checkpoint_exit_code']==0 and a['estimates_percent']['PR302_workflow']==100,'PR302 must actually finish first')
 control=load(P/'SHARED_GIT_WINDOW_STATUS.json');need(not control['shared_git_writes_paused'] and not control['descending_302_native_integration_lease']['active'] and not control['descending_302_final_checkpoint038_lease']['active'],'all exact writer scopes closed before descending continuation')
 inventory=load(P/'inventory.json');need(inventory['current_scope']=='submitted_QUEUE_status_exactly_claimed_solved_only' and next(x for x in inventory['items'] if x['number']==302)['merged'] is True,'exact human-edited filter and previous completion')
 D.mkdir(exist_ok=False);(D/'ATTEMPT.json').write_text(json.dumps(dict(UTC=utc(),actual_recorder_PID=os.getpid(),source=pin(__file__),inventory=pin(P/'inventory.json'),PR302_completion=pin(accepted),starting_control=pin(P/'SHARED_GIT_WINDOW_STATUS.json'),direction='descending',start_below=302,excluded_PR=8,status_filter='exact original/submitted claimed_solved only',no_write_authority=True),indent=2)+'\n');rows=[];eligible=None
 for item in sorted([x for x in inventory['items'] if x['number']<302],key=lambda x:x['number'],reverse=True):
  number=item['number']
  if number==8:rows.append(dict(PR=8,decision='SKIP_EXPLICIT_EXCLUSION'));continue
  directory=D/f'pr{number}';directory.mkdir();pr=capture(directory,'PR_metadata',f'repos/AlecKriebel/Math/pulls/{number}');need(pr['number']==number and pr['base']['repo']['full_name']=='AlecKriebel/Math','literal target repository identity')
  if pr['state']!='open' or not pr['draft']:
   row=dict(PR=number,decision='SKIP_NOT_CURRENT_OPEN_DRAFT',state=pr['state'],draft=pr['draft']);rows.append(row);(directory/'DECISION.json').write_text(json.dumps(row,indent=2)+'\n');continue
  original=item['headRefOid'];need(re.fullmatch('[0-9a-f]{40}',original),'exact original inventory head');match=re.fullmatch(r'(?:math/|dot/math-)(\d+)(?:-.*)?',item['headRefName']);need(match is not None,'unambiguous original problem identity');problem=match.group(1)
  file=capture(directory,'original_QUEUE',f'repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref={original}');need(file['type']=='file' and file['encoding']=='base64' and file['path']=='unsolved_math_prioritization/QUEUE.md','complete original QUEUE response');b=base64.b64decode(file['content'],validate=False);blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();need(len(b)==file['size'] and blob==file['sha'],'whole original QUEUE bytes/Git blob');(directory/'ORIGINAL_QUEUE.md.gz').write_bytes(gzip.compress(b,mtime=0))
  candidates=[line for line in b.splitlines() if line.startswith(b'|') and len(line.split(b'|'))==14 and line.split(b'|')[2].strip().split(b'/')[0].strip()==problem.encode()];need(len(candidates)==1,'exact original target row');line=candidates[0];cells=line.decode().split('|');need(len(cells)==14,'expected QUEUE schema');status=cells[8].strip();row=dict(PR=number,problem_id=problem,original_head=original,current_head=pr['head']['sha'],original_status=status,original_queue=dict(bytes=len(b),sha256=sha(b),git_blob=blob),original_queue_row=line.decode(),decision='ELIGIBLE_CLAIMED_SOLVED' if status=='claimed_solved' else 'SKIP_NON_CLAIMED_SOLVED_WITHOUT_PROCESSING',original_head_changed_since_inventory=original!=pr['head']['sha'],current_title=pr['title'],current_url=pr['html_url']);rows.append(row);(directory/'DECISION.json').write_text(json.dumps(row,indent=2)+'\n')
  print(json.dumps({k:row[k] for k in ['PR','original_status','decision']}),flush=True)
  if status=='claimed_solved':eligible=row;break
 result=dict(status='PASS_DESCENDING_STATUS_ONLY_FILTER',UTC=utc(),actual_recorder_PID=os.getpid(),source=pin(__file__),checked=rows,next_eligible=eligible,original_noneligible_rows_not_reviewed_repaired_commented_merged_closed_or_published=True,eligible_head_change_requires_explicit_source_reconciliation=bool(eligible and eligible['original_head_changed_since_inventory']),no_index_shared_control_Git_or_service_mutation=True,estimates_percent=dict(PR302_workflow=100,next_problem_mathematical_review=0,overall_descending_goal=None))
 out=D/'RESULT.json';out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(status=result['status'],checked=len(rows),next_eligible=eligible,result=pin(out)),indent=2))
if __name__=='__main__':main()
