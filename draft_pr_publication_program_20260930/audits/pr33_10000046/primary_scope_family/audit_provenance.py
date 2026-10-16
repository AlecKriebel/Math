#!/usr/bin/env python3
"""Read-only source/Git/database audit; writes only this audit family."""
from pathlib import Path
from datetime import datetime, timezone
import collections, hashlib, json, re, sqlite3, subprocess, shutil, copy

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
U=ROOT/'unsolved_math_prioritization'
SNAP=HERE.parent/'source_snapshot'
PR=HERE.parent/'pr_input'
HEAD='de5877c38bf3604f0a8e074af7a9c55fca334522'
BASE='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
MAIN='cab3546c2782846c3173e9ebc8c57d725603dbe9'
NUM=10000046
CODE='AMR-099-0046'
PREFIX='unsolved_math_prioritization/attempts/10000046/'
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def blob(ref,path):return git('show',ref+':'+path)
def load(p):return json.loads(p.read_text())
def dump(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def binding(p):
 b=p.read_bytes();return {'sha256':sha(b),'bytes':len(b)}
def queue_info(b):
 lines=b.decode().splitlines()
 header=next(x for x in lines if x.startswith('| Rank |'))
 rows=[x for x in lines if f'{NUM} / {CODE}' in x]
 return {'full_sha256':sha(b),'bytes':len(b),'header':header,
  'rows':[{'literal':x,'cells':[c.strip() for c in x.split('|')[1:-1]],'cell_count':len(x.split('|')[1:-1])} for x in rows]}

result={'at_utc':datetime.now(timezone.utc).isoformat(),'audit_completion_percent':55,
 'mathematical_goal_verification_percent':0,'original_substantive_turns':'1/5','verification_turns':0,
 'head':HEAD,'metadata_base':BASE,'dated_main':MAIN,'current_head':git('rev-parse','HEAD').decode().strip(),
 'actual_merge_base':git('merge-base',BASE,HEAD).decode().strip()}
metadata=load(PR/'pr.json')
diff=(PR/'diff.patch').read_bytes()
result['metadata']=metadata
result['diff']={**binding(PR/'diff.patch'),'git_diff_equal':diff==git('diff',BASE,HEAD),
 'changed_paths':git('diff','--name-only',BASE,HEAD).decode().splitlines()}
chunks=re.split(r'(?m)^diff --git ',diff.decode())[1:]
parsed=[]
for chunk in chunks:
 lines=chunk.splitlines();p=lines[0].split(' b/',1)[1]
 added=[x[1:] for x in lines[1:] if x.startswith('+') and not x.startswith('+++')]
 removed=[x[1:] for x in lines[1:] if x.startswith('-') and not x.startswith('---')]
 info={'path':p,'added_lines':len(added),'removed_lines':len(removed)}
 if p.startswith(PREFIX):
  actual=blob(HEAD,p)
  snapshot=(SNAP/p.removeprefix(PREFIX)).read_bytes()
  info.update(git_blob_sha256=sha(actual),snapshot_sha256=sha(snapshot),bytes=len(actual),
              snapshot_equals_blob=snapshot==actual,added_lines_reconstruct_blob=('\n'.join(added)+'\n').encode()==actual)
  target=HERE/'isolated'/'original'/p.removeprefix(PREFIX)
  target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(actual)
 parsed.append(info)
result['original_artifacts']=parsed
result['scope']={'numeric_original_files':sum(p['path'].startswith(PREFIX) for p in parsed),
 'diff_files':len(parsed),'original_body_only_folder_assertion':metadata['body'].split('Queue disposition:',1)[-1],
 'body_assertion_contradicted':any(x['path']=='unsolved_math_prioritization/QUEUE.md' for x in parsed)}
result['queue']={ref:queue_info(blob(ref,'unsolved_math_prioritization/QUEUE.md')) for ref in (BASE,HEAD,MAIN)}
result['queue']['live']=queue_info((U/'QUEUE.md').read_bytes())
result['queue']['head_changed_cells']=[i+1 for i,(a,b) in enumerate(zip(result['queue'][BASE]['rows'][0]['cells'],result['queue'][HEAD]['rows'][0]['cells'])) if a!=b]
result['queue']['main_to_head_changed_cells']=[i+1 for i,(a,b) in enumerate(zip(result['queue'][MAIN]['rows'][0]['cells'],result['queue'][HEAD]['rows'][0]['cells'])) if a!=b]
result['queue']['generator_has_eight_columns']='| Rank | ID / code | Problem | EV | Difficulty | Proposed | Status | Turns |' in (U/'queue.py').read_text()
result['protected_live']={p:binding(U/p) for p in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','assessment_history.jsonl','queue.py','policy.json','manifest.json','review_v2/related_target_groups.json']}
result['state_presence']={}
for ref in (BASE,HEAD,MAIN):
 for name in ('state.json','catalog.json','assessments.json'):
  data=json.loads(blob(ref,'unsolved_math_prioritization/'+name))
  rows=[x for x in data if str(x['id'])==str(NUM)] if isinstance(data,list) else data.get(str(NUM))
  result['state_presence'][ref+'/'+name]=rows
for name in ('state.json','catalog.json','assessments.json'):
 data=load(U/name)
 result['state_presence']['live/'+name]=[x for x in data if str(x['id'])==str(NUM)] if isinstance(data,list) else data.get(str(NUM))
result['relevant_local_history']={}
for name in ('history.jsonl','assessment_history.jsonl'):
 result['relevant_local_history'][name]=[json.loads(x) for x in (U/name).read_text().splitlines() if x and str(json.loads(x).get('id'))==str(NUM)]
result['related_target_groups']=[x for x in load(U/'review_v2/related_target_groups.json') if str(NUM) in json.dumps(x)]

# Fresh pinned source, never replacing the real cache or rebuilding it.
problems=load(HERE/'sources/problems.json');reports=load(HERE/'sources/research_results.json')
raws=[p for p in problems if p['id']==NUM]
code_records=[p for p in problems if p['problem_number']==CODE]
assert len(raws)==len(code_records)==1
raw=raws[0];prior=reports[CODE]
dump('source_record.raw.json',raw);dump('prior_report.json',prior)
result['fresh_upstream']={'revision':'37e53eabe540fb458758e198be61634bd02ee008',
 'files':{n:binding(HERE/'sources'/n) for n in ('problems.json','research_results.json')},
 'problem_count':len(problems),'numeric_matches':len(raws),'code_matches':len(code_records),
 'raw_problem_equals_original_record':raw==load(SNAP/'source_record.json'),
 'raw_plus_report_equals_original_record':{**raw,'research_classification':prior['classification'],'research_summary':prior['result']+' Literature status: '+prior['status_literature']}==load(SNAP/'source_record.json'),
 'prior_equals_original':prior==load(SNAP/'prior_report.json')}
db=sqlite3.connect('file:'+str(U/'cache/catalog.sqlite')+'?mode=ro',uri=True)
db.execute('PRAGMA query_only=ON')
dbrow=db.execute('SELECT key,payload,report,typeof(key),typeof(payload),typeof(report) FROM records WHERE key=?',(str(NUM),)).fetchall()
assert len(dbrow)==1
key,payload,report,*types=dbrow[0]
dbmeta=db.execute('SELECT revision FROM metadata').fetchall()
db.close()
review_hash=sha(json.dumps([raw,prior],sort_keys=True).encode())
statement_hash=sha(raw['statement'].encode())
result['database']={'mode':'read-only URI plus query_only','key':key,'sqlite_types':types,
 'metadata_revision':dbmeta,'payload_equals_fresh':json.loads(payload)==raw,'report_equals_fresh':json.loads(report)==prior,
 'payload_exact_import_serialization':payload==json.dumps(raw),'report_exact_import_serialization':report==json.dumps(prior),
 'payload_TEXT_sha256':sha(payload.encode()),'report_TEXT_sha256':sha(report.encode()),
 'review_hash_fresh_exact_queue_algorithm':review_hash,'statement_hash_fresh':statement_hash,
 'review_hash_original_readiness_matches':review_hash==load(SNAP/'readiness.json')['review_hash'],
 'statement_hash_original_readiness_matches':statement_hash==load(SNAP/'readiness.json')['statement_hash']}
review=load(SNAP/'review/review_summary.json')
result['old_review_bindings']={field:sha((SNAP/path).read_bytes())==review[field] for field,path in {
 'reviewed_sha256':'PARTIAL.md','review_sha256':'review/REVIEW.md','independent_check_sha256':'review/independent_checks.py','independent_receipt_sha256':'review/independent_results.json'}.items()}
inventory=load(HERE/'sources/github_allstate_inventory.json')
tokens=['10000046','AMR-099-0046','nonintersect','coupled but distant','random-walk coupling','random walk coupling']
result['github_inventory']={'retrieved_all_state_limit':500,'count':len(inventory),'states':dict(collections.Counter(x['state'] for x in inventory)),
 'queries':tokens,'matching_title_or_body':[x for x in inventory if any(t in (x['title']+' '+x['body']).lower() for t in tokens)],
 'attempt_path_history':load(HERE/'sources/github_attempt_history.json'),
 'pr33_commits':load(HERE/'sources/github_pr33_commits.json'),
 'limitations':'Bounded one-page all-state pull inventory and first 100 path commits; no claim of exhaustive duplicate/priority search. Self-reported model names in PR/readiness/review are metadata, not independently verified execution attestations.'}
dump('provenance_results.json',result)
print(json.dumps({'source_scope':result['scope'],'diff':result['diff'],'database':result['database'],
 'queue_changed_cells':result['queue']['head_changed_cells'],'queue_original_row':result['queue'][HEAD]['rows'],
 'live_queue_row':result['queue']['live']['rows'],'live_canonical_state':result['state_presence']['live/state.json'],
 'all_original_blob_bindings_pass':all(x.get('snapshot_equals_blob',True) and x.get('added_lines_reconstruct_blob',True) for x in parsed),
 'old_review_bindings':result['old_review_bindings'],'github_inventory_count':len(inventory),'prior_full':prior},indent=2))
