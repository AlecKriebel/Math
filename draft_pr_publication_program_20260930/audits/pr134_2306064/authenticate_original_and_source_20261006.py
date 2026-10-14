"""Authenticate entire submitted PR134 attempt and full cached source/prior without live mutation."""
from pathlib import Path
import base64,datetime,hashlib,json,os,sqlite3,subprocess
A=Path(__file__).resolve().parent;P=A.parent.parent;C=P.parent;R=Path('/Users/alec/Documents/Math')
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh';GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git'
HEAD='6a865c574586d08e6fa185b09ebe746122457ff0';PREFIX='unsolved_math_prioritization/attempts/2306064/'
F=A/'original_head_authentication_20261006';O=F/'original_attempt';events=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(v,s):
 if not v:raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def run(exe,args):
 t=now();ch=subprocess.Popen([exe,*args],cwd=C,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'},stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=ch.communicate()
 events.append({'argv':[exe,*args],'actual_child_PID':ch.pid,'UTC_start':t,'UTC_end':now(),'exit_code':ch.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err)})
 dump(F/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'events':events});require(ch.returncode==0,err.decode()[:1000]);return out
def api(endpoint):return json.loads(run(GH,['api','--hostname','github.com',endpoint]))
def git(*args):return run(GIT,list(args))
require(not F.exists(),'Existing original authentication: inspect before rerun');O.mkdir(parents=True)
selected=json.loads((P/'ordered_intake_20261006/after_PR126/INTAKE_AFTER_PR126.json').read_text())['next_selected']
require(selected['PR']==134 and selected['head']==HEAD and selected['literal_status']=='claimed_solved' and selected['effort']=='1/5','Literal original eligibility')
base=git('rev-parse','HEAD').decode().strip();require(git('branch','--show-current').strip()==b'main','Stay main');index=git('diff','--cached','--name-only','-z');dirty=git('diff','--name-only','--diff-filter=ACMRTUXB','-z');pins=[]
def walk(path):
 entries=api('repos/AlecKriebel/Math/contents/'+path+'?ref='+HEAD);require(isinstance(entries,list),'Full immutable directory')
 for entry in sorted(entries,key=lambda x:x['path']):
  require(entry['path'].startswith(PREFIX),'Original containment')
  if entry['type']=='dir':walk(entry['path']);continue
  require(entry['type']=='file','Regular original file only')
  x=api('repos/AlecKriebel/Math/contents/'+entry['path']+'?ref='+HEAD);require(x['type']=='file' and x['path']==entry['path'] and x['encoding']=='base64' and x['sha']==entry['sha'],'Full exact original body')
  b=base64.b64decode(x['content']);require(len(b)==entry['size']==x['size'] and hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==entry['sha'],'Actual Git blob authentication')
  rel=Path(entry['path'][len(PREFIX):]);require(not rel.is_absolute() and '..' not in rel.parts,'Contained original path');p=O/rel;p.parent.mkdir(parents=True,exist_ok=True);require(not p.exists(),'Original duplicate');p.write_bytes(b);pins.append({'path':str(rel),'bytes':len(b),'sha256':sha(b),'Git_blob':entry['sha']})
walk(PREFIX.rstrip('/'));require(len(pins)==17,'Full submitted17 bodies')
q=api('repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+HEAD);body=base64.b64decode(q['content']);require(sha(body)==selected['queue_sha256'] and len(body)==selected['queue_bytes'],'Full original queue');(F/'ORIGINAL_HEAD_QUEUE.md').write_bytes(body)
previous=json.loads((P/'audits/pr124_10400231/original_head_authentication_20261006/SOURCEPAIR_AUTHENTICATION.json').read_text());cache=R/'unsolved_math_prioritization/cache';cachepins={}
for name in ['problems.json','research_results.json','catalog.sqlite']:
 b=(cache/name).read_bytes();pin={'bytes':len(b),'sha256':sha(b)};require(pin==previous['cache_pins'][name],'Complete source snapshot changed');cachepins[name]=pin
manifest=json.loads((R/'unsolved_math_prioritization/manifest.json').read_text());db=sqlite3.connect('file:'+str(cache/'catalog.sqlite')+'?mode=ro',uri=True);require(db.execute('SELECT revision FROM metadata').fetchone()==(manifest['revision'],) and db.execute('SELECT count(*) FROM records').fetchone()[0]==15458,'Immutable full cache revision/count');raw,priorraw=db.execute('SELECT payload,report FROM records WHERE key=?',('2306064',)).fetchone();db.close();source,prior=json.loads(raw),json.loads(priorraw)
require(source==json.loads((O/'source_record.json').read_text()) and prior==json.loads((O/'prior_imported_report.json').read_text()),'Full source/prior originals')
review_hash=sha(json.dumps([source,prior],sort_keys=True).encode());ready=json.loads((O/'readiness.json').read_text());require(ready['review_hash']==review_hash and ready['statement_hash']==sha(source['statement'].encode()),'Original readiness full source binding')
require(not (O/'turns.jsonl').exists(),'Unexpected native turn ledger: inspect');require(ready.get('turns_used',ready.get('budget',{}).get('substantive_attempts_used',1))==1,'Original1/5 counter')
dump(F/'SOURCE_STATEMENT.json',source);dump(F/'PRIOR_REPORT.json',prior);dump(F/'SOURCEPAIR_AUTHENTICATION.json',{'schema':'pr134-full-source-prior-original-binding/v1','UTC':now(),'actual_operator_PID':os.getpid(),'revision':manifest['revision'],'SQL_records':15458,'cache_pins':cachepins,'full_statement_and_prior_match_original':True,'complete_prior_report':prior,'review_hash':review_hash,'statement_hash':sha(source['statement'].encode()),'original_budget':'1/5','new_central_proof_search_turns':0})
live=api('repos/AlecKriebel/Math/pulls/134');require(live['html_url']=='https://github.com/AlecKriebel/Math/pull/134' and live['state']=='open' and live['draft'] and live['head']['sha']==HEAD and not live['merged'],'Same immutable open draft');require(git('rev-parse','HEAD').decode().strip()==base and git('diff','--cached','--name-only','-z')==index and git('diff','--name-only','--diff-filter=ACMRTUXB','-z')==dirty,'Read-only checkout invariance')
x={'schema':'pr134-immutable-full-original-and-source-authentication/v1','UTC':now(),'actual_operator_PID':os.getpid(),'PR':134,'problem_id':2306064,'original_head':HEAD,'original_literal_status':'claimed_solved','original_budget':'1/5','original_file_count':17,'original_files':pins,'full_source_prior_pair_verified':True,'review_hash':review_hash,'original_readiness_authenticated':True,'original_turn_ledger_absent_no_fabrication':True,'local_main_unchanged':base,'index_and_materialized_tracked_changes_unchanged':True,'new_central_proof_search_turns':0,'service_mutations':False};dump(F/'ORIGINAL_AUTHENTICATION.json',x)
(A/'RESEARCH_LOG.md').write_text('# PR134 /2306064 research log\n\n'+now()+': Literal incoming claimed_solved1/5 selected after actual PR126 completion/readback/release;127–133ineligible skipped status-only. All17 original bodies, full source/prior and original readiness authenticated. Mathematical/source audit beginning10%, workflow5%; program22/99=22.22%,11published; goalactive. No new central proof-search turn or service/shared/index/native mutation.\n');print(json.dumps({k:v for k,v in x.items() if k!='original_files'}))
