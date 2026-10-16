"""Immutable PR124 bodies and complete source/prior authentication; no ref/index edits."""
from pathlib import Path
import datetime,hashlib,json,os,sqlite3,subprocess
A=Path(__file__).resolve().parent
P=A.parent.parent
C=P.parent
R=Path('/Users/alec/Documents/Math')
GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git'
HEAD='d110ad761291aa6ac1d66d2a49e8b8212c18bed6'
PREFIX='unsolved_math_prioritization/attempts/10400231/'
F=A/'original_head_authentication_20261006'
O=F/'original_attempt'
events=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(value,label):
    if not value:raise RuntimeError(label)
def sha(body):return hashlib.sha256(body).hexdigest()
def dump(path,obj):path.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def git(*args):
    child=subprocess.Popen([GIT,*args],cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate()
    events.append({'argv':[GIT,*args],'PID':child.pid,'ended_UTC':now(),'exit_code':child.returncode,
        'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err)})
    dump(F/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'events':events})
    require(child.returncode==0,err.decode('utf-8','replace')[:1000])
    return out
require(not (F/'ORIGINAL_AUTHENTICATION.json').exists(),'Final original authentication already exists; inspect before retry')
O.mkdir(parents=True,exist_ok=True)
base=git('rev-parse','HEAD').decode().strip()
index_before=git('diff','--cached','--name-only','-z')
dirty_before=git('diff','--name-only','--diff-filter=ACMRTUXB','-z')
require(git('branch','--show-current').strip()==b'main','Not main')
intake=json.loads((P/'ordered_intake_20261006/after_PR117/INTAKE_AFTER_PR117.json').read_text())
selected=intake['next_selected']
require(selected['PR']==124 and selected['head']==HEAD and selected['literal_status']=='claimed_solved' and selected['effort']=='2/5','Selected immutable status/head')
entries=git('ls-tree','-r','--long','-z',HEAD,'--',PREFIX).split(b'\0')
pins=[]
for entry in entries:
    if not entry:continue
    meta,name=entry.decode().split('\t')
    mode,kind,blob,size=meta.split()
    require(mode=='100644' and kind=='blob' and name.startswith(PREFIX),'Regular exact original blob')
    relative=Path(name[len(PREFIX):])
    require(not relative.is_absolute() and '..' not in relative.parts,'Original path containment')
    body=git('show',HEAD+':'+name)
    require(len(body)==int(size) and hashlib.sha1(('blob '+str(len(body))+'\0').encode()+body).hexdigest()==blob,'Full original Git body')
    path=O/relative
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():
        require(path.read_bytes()==body,'Already materialized original body differs')
    else:
        path.write_bytes(body)
    pins.append({'path':str(relative),'bytes':len(body),'sha256':sha(body),'Git_blob':blob})
require(len(pins)==17,'Original file count')
queue=git('show',HEAD+':unsolved_math_prioritization/QUEUE.md')
require(sha(queue)==selected['queue_sha256'],'Full original QUEUE changed')
queue_path=F/'ORIGINAL_HEAD_QUEUE.md'
if queue_path.exists():
    require(queue_path.read_bytes()==queue,'Already materialized original QUEUE differs')
else:
    queue_path.write_bytes(queue)
cache=R/'unsolved_math_prioritization/cache'
cached_manifest=json.loads((R/'unsolved_math_prioritization/manifest.json').read_text())
require(cached_manifest['revision']=='37e53eabe540fb458758e198be61634bd02ee008','Immutable source revision')
cachepins={}
previous=json.loads((P/'audits/pr111_4900006/original_head_authentication_20261006/SOURCEPAIR_AUTHENTICATION.json').read_text())
for name in ['problems.json','research_results.json','catalog.sqlite']:
    body=(cache/name).read_bytes()
    item={'bytes':len(body),'sha256':sha(body)}
    require(item==previous['cache_pins'][name],'Immutable cache pin changed '+name)
    cachepins[name]=item
db=sqlite3.connect('file:'+str(cache/'catalog.sqlite')+'?mode=ro',uri=True)
require(db.execute('SELECT revision FROM metadata').fetchone()==(cached_manifest['revision'],),'SQL source revision')
require(db.execute('SELECT count(*) FROM records').fetchone()[0]==15458,'SQL count')
raw,priorraw=db.execute('SELECT payload,report FROM records WHERE key=?',('10400231',)).fetchone()
db.close()
source,prior=json.loads(raw),json.loads(priorraw)
require(source==json.loads((O/'source_record.json').read_text()),'Full source statement semantics')
require(prior==json.loads((O/'prior_imported_report.json').read_text()),'Full nonempty prior report semantics')
require(bool(prior) and len((O/'prior_imported_report.json').read_bytes())==1856,'Expected complete nonempty prior')
review_hash=sha(json.dumps([source,prior],sort_keys=True).encode())
require(not (O/'readiness.json').exists() and not (O/'turns.jsonl').exists(),'Unexpected original readiness/turn ledger; inspect rather than invent')
original_log=(O/'RESEARCH_LOG.md').read_text()
require('candidate2/5' in original_log and '1. Investigated' in original_log and '2. Proved' in original_log,'Original effort is authenticated by QUEUE and numbered research log')
dump(F/'SOURCE_STATEMENT.json',source)
dump(F/'PRIOR_REPORT.json',prior)
dump(F/'SOURCEPAIR_AUTHENTICATION.json',{'UTC':now(),'actual_operator_PID':os.getpid(),'numeric_id':10400231,
    'revision':cached_manifest['revision'],'SQL_records':15458,'cache_pins':cachepins,'full_statement_matches_original':True,
    'complete_prior_report':prior,'review_hash':review_hash,'original_budget':'2/5','new_central_proof_search_turns':0})
require(git('rev-parse','HEAD').decode().strip()==base and git('diff','--cached','--name-only','-z')==index_before
    and git('diff','--name-only','--diff-filter=ACMRTUXB','-z')==dirty_before,'Read-only checkout/index invariance')
record={'schema':'pr124-immutable-original-and-source-authentication/v1','UTC':now(),'actual_operator_PID':os.getpid(),
    'PR':124,'problem_id':10400231,'original_head':HEAD,'original_literal_status':'claimed_solved','original_budget':'2/5',
    'original_files':pins,'original_file_count':17,'original_ledger_entries':0,'original_effort_provenance':'Immutable QUEUE2/5 plus original two numbered research-log entries; no submitted turns/readiness fabricated','full_source_prior_pair_verified':True,
    'review_hash':review_hash,'local_main_unchanged':base,'index_and_materialized_tracked_changes_unchanged':True,
    'new_central_proof_search_turns':0,'remote_service_mutations':False}
dump(F/'ORIGINAL_AUTHENTICATION.json',record)
dump(F/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'events':events})
(A/'RESEARCH_LOG.md').write_text('# PR124 /10400231 research log\n\n'+now()+': Literal incoming claimed_solved2/5 selected after actual PR117 completion/release;118–123unsolved skipped by status only. All17 original Git bodies, full immutable source and nonempty imported prior authenticated. Original two numbered substantive entries preserved in research log; no submitted turns/readiness exist and none invented. Mathematical/source audit beginning: best guess10%; workflow5%; program20/99=20.20%; persistent goal active. No new central proof-search turn, native/PR/publication/tracker mutation.\n')

print(json.dumps({k:v for k,v in record.items() if k!='original_files'},sort_keys=True))

