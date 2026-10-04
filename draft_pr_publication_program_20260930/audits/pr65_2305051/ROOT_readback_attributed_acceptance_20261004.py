"""Independently read native/remote acceptance, then record checkpoint readiness."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import sqlite3
import subprocess
import sys

if sys.flags.optimize or not sys.flags.ignore_environment or not sys.flags.dont_write_bytecode:
    raise RuntimeError('Invoke -E -B without optimization')
A=Path(__file__).resolve().parent
P=A.parents[1]
R=P.parent
F=A/'ROOT_attributed_acceptance_readback_20261004'
D=Path('/Users/alec/.cache/codex-pr65-priority-20261004/ROOT_acceptance_readback_20261004')
D.mkdir(exist_ok=False)
(D/'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
commands=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_bytes())
def require(v,s):
    if not v:raise RuntimeError(s)
def run(argv):
    start=dt.datetime.now(dt.timezone.utc).isoformat()
    c=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=c.communicate();n=str(len(commands)+1)
    q={'argv':argv,'actual_child_pid':c.pid,'start_utc':start,'finish_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'exit_code':c.returncode}
    for k,b in [('stdout',out),('stderr',err)]:
        f=D/(n+'.'+k);f.write_bytes(b);q[k]={'private_path':str(f),'bytes':len(b),'sha256':sha(b)}
    commands.append(q);(D/'COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n')
    require(c.returncode==0,'Read command failed; inspect retained streams')
    return out
def git(*v):return run(['git','--no-optional-locks',*v])
O=A/'native_attributed_result_operations_20261004'
m=read(O/'NATIVE_MERGE_RESULT.json');a=read(O/'NATIVE_ACCEPTANCE_RESULT.json')
head='5cc1602c05d79502defb07cec7027963149494d2'
require(m['submitted_head']==a['submitted_head']==head and a['merge_commit']==m['merge_commit'],'Receipt identity differs')
require(git('branch','--show-current').strip()==b'main' and git('rev-parse','HEAD').decode().strip()==a['acceptance_commit'],'Native branch/head differs')
require(not git('diff','--cached','--name-only','-z'),'Shared index occupied')
require(git('ls-remote','--heads','origin','main').decode().split()[0]==a['acceptance_commit'],'Remote acceptance differs')
pr=json.loads(run(['gh','pr','view','65','--repo','AlecKriebel/Math','--json','number,state,headRefOid,mergeCommit,mergedAt,title,body,url']))
require(pr['state']=='MERGED' and pr['headRefOid']==head and pr['mergeCommit']['oid']==m['merge_commit'],'GitHub exact merge differs')
require(pr['title']=='2305051: attributed Blaschke construction; prior resolution credited' and pr['body']==(A/'ROOT_PUBLISHED_PR_BODY_20261004.md').read_text(),'Published metadata correction differs')
require(git('show','-s','--format=%P',m['merge_commit']).decode().split()==[m['base'],head],'Merge parent continuity differs')
require(git('show','-s','--format=%P',a['acceptance_commit']).decode().strip()==m['merge_commit'],'Acceptance parent differs')
Q='unsolved_math_prioritization/QUEUE.md';T='unsolved_math_prioritization/attempts/2305051'
manifest=read(A/'original_source_authentication_20261004/ORIGINAL_BLOB_MANIFEST.json')
originals=[x for x in manifest['artifacts'] if x['incoming_changed_domain'] and x['path']!=Q]
require(len(originals)==18,'Original scope differs')
for row in originals:
    require(sha((R/row['path']).read_bytes())==row['sha256'] and sha(git('show',a['acceptance_commit']+':'+row['path']))==row['sha256'],'Original science body differs')
    require(git('ls-tree',a['acceptance_commit'],'--',row['path']).decode().split()[:3]==[row['mode'],'blob',row['git_blob_SHA1']],'Original Git mode/blob differs')
merge_names={p.decode() for p in git('diff','--name-only','-z',m['base'],m['merge_commit']).split(b'\0') if p}
mirror_names={p.decode() for p in git('diff','--name-only','-z',m['merge_commit'],a['acceptance_commit']).split(b'\0') if p}
require(merge_names=={x['path'] for x in originals}|{Q},'Merge domain differs')
require(mirror_names=={T+'/acceptance.json',T+'/CURRENT_RESULT.md',T+'/CURRENT_PRIORITY_SPECIALIZATION.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'},'Mirror domain differs')
before=git('show',m['base']+':'+Q).decode().splitlines()
now=(R/Q).read_text().splitlines()
require(len(now)==len(before),'Queue row count differs')
changed=[(x,y) for x,y in zip(before,now) if x!=y]
require(len(changed)==1 and '| 2305051 /' in changed[0][0] and '| 2305051 /' in changed[0][1],'Other queue rows differ')
cells=changed[0][1].split('|')
require(cells[8].strip()=='already_solved' and cells[9].strip()=='2/5' and not cells[12].strip(),'Current disposition/budget/DOI differs')
accept=read(R/(T+'/acceptance.json'))
require(accept['status']=='already_solved' and accept['accepted_as']=='attributed_partial_prior_result' and accept['full_source_solved'] is True and accept['new_open_problem_resolution'] is False,'Scientific meaning differs')
require(accept['reviewed_head']==head and accept['merge_commit']==m['merge_commit'] and accept['original_budget']=='2/5' and accept['new_original_proof_turns']==0,'Acceptance identity/budget differs')
require(accept['new_paper'] is False and accept['Zenodo_upload'] is False and accept['new_publication_DOI'] is None and accept['tracker_append'] is False,'Prior-result publication exclusion differs')
require([json.loads(x)['turn'] for x in (R/(T+'/turns.jsonl')).read_text().splitlines()]==[1,2],'Original ledger differs')
state_path='unsolved_math_prioritization/state.json';history_path='unsolved_math_prioritization/history.jsonl'
old_state=json.loads(git('show',m['merge_commit']+':'+state_path));state=read(R/state_path)
old_history=git('show',m['merge_commit']+':'+history_path);history=(R/history_path).read_bytes()
require({k:v for k,v in state.items() if k!='2305051'}==old_state and history.startswith(old_history),'Other native history/state differs')
events=history[len(old_history):].splitlines();require(len(events)==1,'Expected one current import event')
event=json.loads(events[0]);require(event==state['2305051'] and event['event']=='acceptance_mirror_import' and event['event_id']==a['event_id'],'Actual event/state differs')
source=read(R/(T+'/source_record.json'))
problems=read(R/'unsolved_math_prioritization/cache/problems.json');reports=read(R/'unsolved_math_prioritization/cache/research_results.json')
require([p for p in problems if str(p['id'])=='2305051']==[source['problem']] and reports['AMR-022-5051']==source['upstream_report'],'Current raw source pair differs')
with sqlite3.connect('file:'+str(R/'unsolved_math_prioritization/cache/catalog.sqlite')+'?mode=ro',uri=True) as db:
    row=db.execute('SELECT payload,report FROM records WHERE key=?',('2305051',)).fetchone()
require(row is not None and json.loads(row[0])==source['problem'] and row[1] is not None and json.loads(row[1])==source['upstream_report'],'Current SQL source pair differs')
stamp=dt.datetime.now(dt.timezone.utc).isoformat();F.mkdir(exist_ok=False)
result={'UTC':stamp,'actual_controller_pid':os.getpid(),'status':'PASS','PR':65,'reviewed_head':head,'merge_commit':m['merge_commit'],'acceptance_commit':a['acceptance_commit'],'GitHub_exact_merge_and_corrected_metadata_verified':True,'original_18_bodies_modes_blobs_preserved':True,'original_budget':'2/5','other_queue_rows_state_entries_history_prefix_preserved':True,'one_actual_current_import_event':True,'raw_SQL_wrapper_typed_source_pair_verified':True,'outcome':'already_solved','accepted_as':'attributed_partial_prior_result','full_source_solved':True,'new_open_problem_resolution':False,'new_paper':False,'new_DOI':None,'tracker_append':False,'scoped_checkpoint_pending':True,'actual_command_count':len(commands),'actual_commands':commands}
(F/'READBACK.json').write_text(json.dumps(result,indent=2)+'\n')
progress=read(P/'CURRENT_PROGRESS.json');require(progress['current_PR']==65,'Progress cursor differs')
progress.update(UTC=stamp,current_PR_workflow_percent=95,current_merge_commit=m['merge_commit'],current_acceptance_commit=a['acceptance_commit'],current_acceptance_readback_record='audits/pr65_2305051/ROOT_attributed_acceptance_readback_20261004/READBACK.json',remaining_current_step='Push the scoped supplied-source and exact-acceptance audit checkpoint, then advance ordered intake to66. No new paper/DOI/tracker for PR65.')
(P/'CURRENT_PROGRESS.json').write_text(json.dumps(progress,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n## '+stamp+' - actual attributed acceptance independently read back\n\nExact submitted head merged at '+m['merge_commit']+'; current acceptance pushed at '+a['acceptance_commit']+'. GitHub corrected title/body and exact merge independently verified. All18 original bodies/modes and2/5 ledger preserved; other queue rows, state entries and history prefix preserved with one present-day import event. Raw/SQL/wrapper pair agrees. already_solved; no novel-resolution clearance, paper, DOI or tracker row. Scoped audit checkpoint pending. Estimates math100%, bounded priority100%, workflow95%, completed6/99.\n')
print(json.dumps({k:v for k,v in result.items() if k!='actual_commands'},indent=2))
