"""PR57-only nonmutating status-first source/remote inspection.
Writes only the new operations evidence folder; records actual serial commands.
No fetch, ref/index write, native modification, external mutation or contact.
"""
import base64, datetime as dt, hashlib, json, os, sqlite3, stat, subprocess
from pathlib import Path
HEAD='4ecc453d6f9ec2e64cdb2d4b41c018fffbe85b29'
ID='30003354'; CODE='OWR-15208-008'; QUEUE='unsolved_math_prioritization/QUEUE.md'
PREFIX='unsolved_math_prioritization/attempts/'+ID
GOAL=Path('/Users/alec/.codex/attachments/4df73d3d-641f-4907-b9ad-c47c468f2589/goal-objective.md')
def sha(b):return hashlib.sha256(b).hexdigest()
def jb(x):return (json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
def must(ok,m):
 if not ok:raise RuntimeError(m)
def main():
 own=Path(__file__).resolve().parent; audit=own.parent; repo=own.parents[3]
 actual=own/'private/actual_readonly_inspection';must(not actual.exists(),'Prior inspection exists; preserve it')
 actual.mkdir(parents=True);(actual/'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes());commands=[]
 def run(argv,allowed=(0,)):
  start=dt.datetime.now(dt.timezone.utc).isoformat();p=subprocess.Popen(argv,cwd=repo,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  out,err=p.communicate();n=str(len(commands)+1);(actual/(n+'.stdout')).write_bytes(out);(actual/(n+'.stderr')).write_bytes(err)
  commands.append({'argv':argv,'actual_pid':p.pid,'started_UTC':start,'finished_UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'exit_code':p.returncode,'stdout_sha256':sha(out),'stderr_sha256':sha(err)})
  (actual/'COMMANDS.json').write_bytes(jb(commands));must(p.returncode in allowed,'Actual read failed; preserve partial evidence');return out,p.returncode
 def git(*x):return run(['git','--no-optional-locks',*x])[0]
 def pin(p):
  b=p.read_bytes();return {'path':str(p.resolve()),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.stat().st_mode)}
 pr=json.loads(run(['gh','pr','view','57','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,headRefName,baseRefName,mergeCommit,mergedAt,url,title'])[0])
 must(pr['headRefOid']==HEAD and pr['baseRefName']=='main','Incoming exact head/base drifted; stop SOURCE')
 q=json.loads(run(['gh','api','repos/AlecKriebel/Math/contents/'+QUEUE+'?ref='+HEAD])[0]);queue=base64.b64decode(q['content'])
 rows=[s for s in queue.decode().splitlines() if '| '+ID+' /' in s];must(len(rows)==1,'Target intake row must be unique');cells=rows[0].split('|')
 if cells[8].strip()!='claimed_solved':
  (own/'INELIGIBLE_STOP.json').write_bytes(jb({'literal_status':cells[8].strip(),'action':'STOP_SOURCE_SKIP_ENTIRELY','PR':57,'actual_pid':os.getpid(),'UTC':dt.datetime.now(dt.timezone.utc).isoformat()}));return
 must(cells[9].strip()=='1/5' and pr['state']=='OPEN' and pr['isDraft'] is True,'Exact open-draft/budget changed')
 auth=json.loads((audit/'original_preparation_family/ORIGINAL_AUTHENTICATION.json').read_bytes());must(auth['original_head']==HEAD and len(auth['original_science_files'])==17,'Original domain differs')
 blob=hashlib.sha1(b'blob '+str(len(queue)).encode()+b'\0'+queue).hexdigest();must(blob==q['sha']==auth['original_queue_destination_blob_sha1'],'Submitted QUEUE blob differs')
 files=json.loads(run(['gh','api','repos/AlecKriebel/Math/pulls/57/files?per_page=100'])[0]);expected={QUEUE}|{x['repository_path'] for x in auth['original_science_files']}
 must(len(files)==18 and {x['filename'] for x in files}==expected,'Incoming domain differs')
 tree=json.loads(run(['gh','api','repos/AlecKriebel/Math/git/trees/'+HEAD+'?recursive=1'])[0]);must(tree['truncated'] is False,'Tree truncated')
 entries={x['path']:x for x in tree['tree']};remote=[]
 for x in auth['original_science_files']:
  p=x['repository_path'];t=entries[p];must(t['mode']==x['git_mode'] and t['sha']==x['git_blob_sha1'] and t['type']=='blob','Fresh incoming tree mode/blob differs')
  fresh=json.loads(run(['gh','api','repos/AlecKriebel/Math/contents/'+p+'?ref='+HEAD])[0]);body=base64.b64decode(fresh['content']);must(fresh['sha']==x['git_blob_sha1'] and len(body)==x['bytes'] and sha(body)==x['sha256'],'Fresh incoming body differs')
  cache=Path(x['local_path']);must(cache.read_bytes()==body,'Original cache differs from actual remote')
  remote.append({'repository_path':p,'bytes':len(body),'sha256':sha(body),'git_mode':t['mode'],'git_blob_sha1':t['sha']})
 source=json.loads((audit/'original_preparation_family/original/source_record.json').read_bytes());must(source['id']==int(ID) and source['problem_number']==CODE and 'upstream_report' not in source,'Flat original field-presence changed')
 turns=json.loads((audit/'original_preparation_family/original/turns.json').read_bytes());must(turns['substantive_proof_attempts']==1 and turns['budget']==5 and len(turns['turns'])==1 and turns['turns'][0]['number']==1,'Actual original 1/5 ledger changed')
 manifest=json.loads((repo/'unsolved_math_prioritization/manifest.json').read_bytes());raw_pins=[]
 for name in ['problems.json','research_results.json']:
  p=repo/'unsolved_math_prioritization/cache'/name;b=p.read_bytes();must({'bytes':len(b),'sha256':sha(b)}==manifest['files'][name],'Raw corpus manifest mismatch');raw_pins.append(pin(p))
 problems=json.loads((repo/'unsolved_math_prioritization/cache/problems.json').read_bytes());matches=[x for x in problems if str(x['id'])==ID];must(matches==[source],'Flat original/raw selected typed problem differs')
 reports=json.loads((repo/'unsolved_math_prioritization/cache/research_results.json').read_bytes());must(CODE not in reports,'Selected raw report no longer absent')
 with sqlite3.connect('file:'+str(repo/'unsolved_math_prioritization/cache/catalog.sqlite')+'?mode=ro',uri=True) as db:
  row=db.execute('SELECT payload,report FROM records WHERE key=?',(ID,)).fetchone();revision=db.execute('SELECT revision FROM metadata').fetchall()
 must(row and json.loads(row[0])==source and row[1] is not None and row[1]=='{}' and json.loads(row[1])=={},'SQL typed problem/nonNULL fallback differs');must(revision==[(manifest['revision'],)],'SQL revision differs')
 pair=sha(json.dumps([source,{}],sort_keys=True).encode());null_pair=sha(json.dumps([source,None],sort_keys=True).encode())
 catalog=[x for x in json.loads((repo/'unsolved_math_prioritization/catalog.json').read_bytes()) if x['id']==ID];must(len(catalog)==1 and catalog[0]['review_hash']==pair,'Catalog current selected pair hash differs')
 local=git('rev-parse','HEAD').decode().strip();remote_main=git('ls-remote','--heads','origin','main').decode().split()[0];branch=git('branch','--show-current').decode().strip()
 staged=[x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x];dirty=[x.decode() for x in git('diff','--name-only','-z').split(b'\0') if x]
 available=run(['git','--no-optional-locks','cat-file','-e',HEAD+'^{commit}'],allowed=(0,128))[1]==0
 state=json.loads((repo/'unsolved_math_prioritization/state.json').read_bytes());history=(repo/'unsolved_math_prioritization/history.jsonl').read_bytes();native=[x for x in (repo/QUEUE).read_text().splitlines() if '| '+ID+' /' in x];must(len(native)==1,'Native row not unique')
 window=repo/'draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json';w=json.loads(window.read_bytes())
 result={'schema':'pr57-ordered-publication-operations-readonly-inspection/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'source':pin(Path(__file__)),'goal':pin(GOAL),'PR':pr,'literal_current_submitted_status':cells[8].strip(),'literal_current_submitted_budget':cells[9].strip(),'eligible_at_current_intake':True,'submitted_queue_row':rows[0],'submitted_queue_blob_SHA1':blob,'submitted_queue_sha256':sha(queue),'current_incoming_file_count':len(files),'exact_incoming_paths':sorted(expected),'all_17_fresh_remote_science_bodies_modes_and_blobs_verified':True,'fresh_remote_science':remote,'source_record_flat_problem':True,'original_upstream_report_field_present':False,'original_upstream_report_value':'ABSENT; no wrapper value','raw_report_key_present':False,'raw_report_interpretation':'ABSENT; no raw value','SQL_report_is_NULL':False,'SQL_report_literal':'{}','catalog_review_hash_SQL_typed_pair':pair,'hypothetical_null_pair_hash_not_original_report':null_pair,'raw_corpus_pins':raw_pins,'source_revision':manifest['revision'],'original_ledger_file':'turns.json','original_status_file_present':PREFIX+'/status.json' in entries,'original_turns_jsonl_present':PREFIX+'/turns.jsonl' in entries,'original_budget':'1/5','native_branch':branch,'native_main':local,'remote_main':remote_main,'main_remote_equal':local==remote_main,'all_staged_paths':staged,'foreign_dirty_tracked_path_count':len(dirty),'original_commit_available_locally':available,'native_original_paths_present':[p for p in sorted(expected-{QUEUE}) if (repo/p).exists()],'native_target_queue_row':native[0],'native_target_state_present':ID in state,'native_target_history_count':sum(str(json.loads(x).get('id'))==ID for x in history.splitlines()),'window_observation_pin':pin(window),'window_paused_for':w.get('paused_for'),'actual_PR57_exclusive_window_claimed':False,'ROOT_authority_claimed':False,'helper_execution_performed':False,'source_only':True,'native_Git_PR_Zenodo_tracker_mutation':False,'human_contact':False,'new_central_proof_attempts':0,'operations_preparation_percent':40}
 must(not (own/'READONLY_INSPECTION.json').exists(),'Actual observation exists');(own/'READONLY_INSPECTION.json').write_bytes(jb(result));print(json.dumps({k:v for k,v in result.items() if k not in ['fresh_remote_science','raw_corpus_pins','exact_incoming_paths']},indent=2))
if __name__=='__main__':main()
