"""Complete only the interrupted receipt phase; do not repeat native CLI/history events."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,sqlite3
A=Path(__file__).resolve().parent;C=A.parents[2]
D=A/'native_published_obstruction_preparation_20261006';B=D/'private_backend';N=D/'proposed_native_attempt'
GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git';K='10400231';base='5de48499b84f168099d0273a340f4976f841f691';prefix='unsolved_math_prioritization/'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(v,s):
 if not v:raise RuntimeError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
require(not (D/'PREPARED_RECEIPT.json').exists(),'Preparation receipt already complete')
original_journal=load(D/'PROCESS_JOURNAL.json')
require(original_journal['actual_operator_PID']==68361,'Actual original preparer')
commands=original_journal['records']
require(len([x for x in commands if 'assess' in x['argv'] and x['exit_code']==0])==1,'Exactly one actual assess')
require(len([x for x in commands if 'status' in x['argv'] and x['exit_code']==0])==1,'Exactly one actual status')
original_script=(A/'prepare_native_published_obstruction_20261006.py').read_bytes()
needle=b"'cache_snapshot_sha256':sha(cache.read_bytes())"
require(original_script.count(needle)==1,'Single repaired source expression')
dump(D/'ACTUAL_INTERRUPTED_RECEIPT_PHASE.json',{'UTC_recorded':now(),'failed_actual_operator_PID':68361,'actual_tool_exit_code':1,'last_successful_child_recorded_UTC':commands[-1]['UTC_end'],'failure_type':'TypeError: object supporting the buffer API required','failed_expression':'sha(cache) passed a Path rather than bytes','actual_executed_original_script_sha256':sha(original_script.replace(needle,b"'cache_snapshot_sha256':sha(cache)")),'corrected_script_sha256':sha(original_script),'private_native_commands_completed_once':True,'shared_tracked_files_exported':False,'continuation_does_not_repeat_native_events':True})
names=['queue.py','manifest.json','policy.json','catalog.json','assessments.json','state.json','history.jsonl','assessment_history.jsonl','ranking.csv','summary.json','SHORTLIST.md','QUEUE.md'];before={};events=[]
for name in names:
 argv=[GIT,'show',base+':'+prefix+name];start=now();ch=subprocess.Popen(argv,cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=ch.communicate()
 require(ch.returncode==0,'Baseline full Git read')
 expected=[x for x in commands if x['argv']==argv];require(len(expected)==1 and len(out)==expected[0]['stdout_bytes'] and sha(out)==expected[0]['stdout_sha256'],'Actual baseline source mismatch')
 before[name]=out;events.append({'PID':ch.pid,'UTC_start':start,'UTC_end':now(),'argv':argv,'exit_code':ch.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out)})
oldass=json.loads(before['assessments.json']);afterass=load(B/'assessments.json')
require({k:v for k,v in oldass.items() if k!=K}=={k:v for k,v in afterass.items() if k!=K},'Other assessments changed')
oldstates=json.loads(before['state.json']);afterstates=load(B/'state.json')
require(K not in oldstates and {k:v for k,v in afterstates.items() if k!=K}==oldstates,'Other states changed')
require(afterstates[K]['status']=='already_solved' and afterstates[K]['turns_used']==2,'Target effort/status')
oldrows=json.loads(before['catalog.json']);catalog={x['id']:x for x in oldrows};newcat={x['id']:x for x in load(B/'catalog.json')}
require(set(catalog)==set(newcat),'Catalog identity')
for key,x in catalog.items():
 if key!=K:require({f:v for f,v in x.items() if f!='rank'}=={f:v for f,v in newcat[key].items() if f!='rank'},'Unrelated semantic row changed')
require(newcat[K]['local_status']=='already_solved' and newcat[K]['turns_used']==2 and not newcat[K]['eligible'],'Target catalog projection')
for name,count in [('history.jsonl',2),('assessment_history.jsonl',1)]:
 b=(B/name).read_bytes();require(b.startswith(before[name]),'History prefix changed')
 extra=[json.loads(s) for s in b[len(before[name]):].decode().splitlines()]
 require(len(extra)==count and all(x['id']==K for x in extra),'Exactly once native event scope')
oldlines=before['QUEUE.md'].decode().splitlines();newlines=(B/'QUEUE.md').read_text().splitlines()
require(len(oldlines)==len(newlines),'Campaign row count')
diff=[i for i,(x,y) in enumerate(zip(oldlines,newlines)) if x!=y]
require(len(diff)==1 and '| 10400231 / AMR-103-0231 |' in oldlines[diff[0]],'Only original target campaign row')
cells=newlines[diff[0]].split('|');require(cells[8].strip()=='already_solved' and cells[9].strip()=='2/5','Target campaign effort')
F=A/'original_head_authentication_20261006';O=F/'original_attempt'
for x in load(F/'ORIGINAL_AUTHENTICATION.json')['original_files']:
 b=(O/x['path']).read_bytes();require(len(b)==x['bytes'] and sha(b)==x['sha256'],'Original changed')
manifest=load(B/'manifest.json');cache=B/'cache/catalog.sqlite'
db=sqlite3.connect('file:'+str(cache)+'?mode=ro',uri=True)
require(db.execute('SELECT revision FROM metadata').fetchone()==(manifest['revision'],),'Cache revision')
raw,report=db.execute('SELECT payload,report FROM records WHERE key=?',(K,)).fetchone();db.close()
require(json.loads(raw)==load(O/'source_record.json') and json.loads(report)==load(O/'prior_imported_report.json'),'Full source/prior binding')
evidence=load(B/'evidence.json');closed=load(A/'actual_closure_20261006/RECEIPT.json')
require(closed['same_head_closed_without_merge'] and evidence['closed_PR_comment']==closed['closing_comment_url'],'Actual closure')
require(evidence['original_budget']=='2/5' and not evidence['express_historical_refutation_established'],'Scoped priority and effort')
drift=load(D/'UNRELATED_BASELINE_PROJECTION_DRIFT.json')['differences']
# Execute only the corrected final receipt construction from the original preparer.
source=(A/'prepare_native_published_obstruction_20261006.py').read_text()
tail=source[source.index("record={'schema':'pr124-private-prepared-native-published-obstruction-correction/v1'"):]
require("run(" not in tail and "git(" not in tail,'Receipt phase must not repeat commands')
exec(compile(tail,str(A/'prepare_native_published_obstruction_20261006.py')+':receipt-phase-continuation','exec'),globals())
r=load(D/'PREPARED_RECEIPT.json')
r.update({'private_native_command_operator_PID':68361,'actual_receipt_completion_operator_PID':os.getpid(),'interrupted_receipt_phase_corrected':True,'native_commands_repeated':False,'actual_failure_record':'ACTUAL_INTERRUPTED_RECEIPT_PHASE.json','read_only_revalidation_events':events})
dump(D/'PREPARED_RECEIPT.json',r)
print(json.dumps({'UTC':now(),'PID':os.getpid(),'proposed_native_members':len(r['proposed_native_pins']),'baseline_drift_preserved':len(drift),'native_commands_repeated':False,'shared_exports':False}))

