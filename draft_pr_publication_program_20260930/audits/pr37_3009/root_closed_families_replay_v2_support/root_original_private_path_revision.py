"""Actual original13/14diff/full corpus replay; no scientific or shared-state edits."""
from pathlib import Path
import datetime, hashlib, importlib.util, json, shutil, sqlite3, subprocess, sys
sys.dont_write_bytecode=True
R=Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr37_3009/root_replay_execution_revision/tmp/root_replay_20261002T085640496242Z');A=Path(__file__).resolve().parent;S=A/'source_snapshot';Q=R/'unsolved_math_prioritization'
sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes())
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def main():
 assert sys.flags.optimize==0 and not (A/'ROOT_ORIGINAL_INTEGRITY_AND_REPLAY.json').exists()
 assert git('branch','--show-current').strip()==b'main'
 before={p.name:sha(p.read_bytes()) for p in [Q/'QUEUE.md',Q/'state.json',Q/'history.jsonl']}
 m=load(A/'snapshot_manifest.json');assert len(m['files'])==13 and len(m['changed_paths'])==14
 for x in m['files']:
  b=(S/x['path']).read_bytes();assert len(b)==x['size'] and sha(b)==x['sha256']
  path='unsolved_math_prioritization/attempts/3009/'+x['path'];assert git('show',m['head']+':'+path)==b
  tree=git('ls-tree',m['head'],'--',path).decode().strip();assert tree==x['mode']+' blob '+x['git_blob']+'\t'+path
  if x['path'].endswith('.json'):json.loads(b)
 assert git('diff','--name-only',m['base'],m['head']).decode().splitlines()==m['changed_paths']
 assert git('diff',m['base'],m['head'])==(A/'pr_input/diff.patch').read_bytes()
 mf=load(Q/'manifest.json');raw={}
 for name,rec in mf['files'].items():
  b=(Q/'cache'/name).read_bytes();assert len(b)==rec['bytes'] and sha(b)==rec['sha256'];raw[name]=json.loads(b)
 assert len(raw['problems.json'])==15458
 ps=[p for p in raw['problems.json'] if p['id']==3009];assert len(ps)==1;p=ps[0]
 assert p==load(S/'source_record.json') and sum(x['problem_number']==p['problem_number'] for x in raw['problems.json'])==1
 reports=raw['research_results.json'];present=p['problem_number'] in reports;r=reports.get(p['problem_number'],{})
 assert not present and r=={}
 db=sqlite3.connect((Q/'cache/catalog.sqlite').as_uri()+'?mode=ro',uri=True);db.execute('PRAGMA query_only=ON')
 row=db.execute('SELECT payload,report FROM records WHERE key=?',('3009',)).fetchone()
 assert json.loads(row[0])==p and json.loads(row[1])==r
 revision=db.execute('SELECT revision FROM metadata').fetchone()[0];count=db.execute('SELECT count(*) FROM records').fetchone()[0];db.close()
 assert revision==mf['revision'] and count==15458
 spec=importlib.util.spec_from_file_location('root_pr37_pure_queue',Q/'queue.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 score=mod.score(p,r,load(Q/'policy.json'));assert score['review_hash']==sha(json.dumps([p,r],sort_keys=True).encode()) and score['statement_hash']==sha(p['statement'].encode())
 for name,obj in [('pinned_problem.json',p),('pinned_importer_prior_fallback.json',r)]:
  f=A/name;assert not f.exists();f.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 provenance=load(S/'provenance.json');turns=load(S/'turns.json');summary=load(S/'independent_review/review_summary.json')
 assert turns['problem_id']==3009 and turns['problem_number']=='KP-5.2' and turns['substantive_turns_used']==1 and turns['turn_limit']==5 and turns['outcome']=='unsolved'
 assert [x['turn'] for x in turns['responses']]==[1] and turns['responses'][0]['artifact']=='PARTIAL.md'
 assert sha((S/'PARTIAL.md').read_bytes())==provenance['artifact_sha256']==summary['reviewed_artifact_sha256']
 assert sha((S/'independent_review/REVIEW.md').read_bytes())==provenance['independent_review']['review_sha256']==summary['review_sha256']
 stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ');private=A/'tmp'/('root_original_replay_'+stamp);private.mkdir(parents=True,exist_ok=False)
 records=[]
 for code,expected in [('check_controls.py','check_results.json'),('independent_review/independent_checks.py','independent_review/independent_results.json')]:
  dst=private/code;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(S/code,dst)
  cp=subprocess.run(['/usr/bin/python3',str(dst)],cwd=private,capture_output=True,timeout=120)
  (dst.parent/'actual_stdout.txt').write_bytes(cp.stdout);(dst.parent/'actual_stderr.txt').write_bytes(cp.stderr)
  assert cp.returncode==0 and not cp.stderr and dst.read_bytes()==(S/code).read_bytes()
  actual_file=dst.with_name(Path(expected).name);saved=(S/expected).read_bytes()
  assert actual_file.read_bytes()==saved and load(actual_file)==json.loads(saved)
  want=saved if code=='check_controls.py' else (json.dumps({k:v for k,v in json.loads(saved).items() if k!='checks'},indent=2)+'\n').encode()
  assert cp.stdout==want
  result=json.loads(saved);assert result['passed']==len(result['checks'])==(31 if code=='check_controls.py' else 8462) and result['failed']==0 and result['sympy_version']=='1.14.0'
  records.append({'program':code,'program_sha256':sha(dst.read_bytes()),'actual_runtime':'/usr/bin/python3','exit':cp.returncode,'stderr_sha256':sha(cp.stderr),'generated_complete_receipt_BYTE_equal':True,'generated_complete_receipt_JSON_equal':True,'generated_receipt_sha256':sha(saved),'checks':result['passed'],'stdout_sha256':sha(cp.stdout),'stdout_comparison':'Full saved receipt' if code=='check_controls.py' else 'Exact deterministic saved metadata serialization, excluding checks, as the unchanged original program specifies. No saved historical stdout exists.'})
 assert before=={p.name:sha(p.read_bytes()) for p in [Q/'QUEUE.md',Q/'state.json',Q/'history.jsonl']}
 out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','head':m['head'],'base':m['base'],'original_git_files':13,'changed_diff_paths':14,'full_raw_corpus_bytes':sum(x['bytes'] for x in mf['files'].values()),'raw_and_SQL_full_problem_equal_snapshot':True,'SQL_readonly':True,'SQL_revision':revision,'SQL_count':count,'source_pair_review_hash':score['review_hash'],'statement_hash':score['statement_hash'],'separate_prior_report_present':False,'prior_fallback_qualification':'No separate research_results entry exists. The native importer and pure score use {}; this is a fallback value, not a fabricated retrieved report. Complete dated literature triage remains in the full raw problem.','original_budget':'1/5','new_substantive_attempts':0,'original_ledger_sha256':sha((S/'turns.json').read_bytes()),'actual_original_replays':records,'live_queue_state_history_unchanged':before,'scope':'Complete source/Git/budget provenance and finite diagnostic reproduction. Imported topology, priority wording and higher-dimensional gap remain separately under adversarial audit.'}
 (A/'ROOT_ORIGINAL_INTEGRITY_AND_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
