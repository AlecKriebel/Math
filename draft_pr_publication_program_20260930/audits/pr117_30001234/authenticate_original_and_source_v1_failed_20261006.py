"""Immutable PR117 bodies and complete source/prior authentication; no ref/index edits."""
from pathlib import Path
import datetime,hashlib,json,os,sqlite3,subprocess
A=Path(__file__).resolve().parent
P=A.parent.parent
C=P.parent
R=Path('/Users/alec/Documents/Math')
GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git'
HEAD='8163ee0dc7a0f944570925984cef2dc0fb291ad8'
PREFIX='unsolved_math_prioritization/attempts/30001234/'
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
    require(child.returncode==0,err.decode('utf-8','replace')[:1000])
    return out
require(not F.exists(),'Original authentication already exists; inspect before retry')
O.mkdir(parents=True)
base=git('rev-parse','HEAD').decode().strip()
index_before=git('diff','--cached','--name-only','-z')
dirty_before=git('diff','--name-only','--diff-filter=ACMRTUXB','-z')
require(git('branch','--show-current').strip()==b'main','Not main')
intake=json.loads((P/'ordered_intake_20261006/after_PR111/INTAKE_AFTER_PR111.json').read_text())
selected=intake['next_selected']
require(selected['PR']==117 and selected['head']==HEAD and selected['literal_status']=='claimed_solved' and selected['effort']=='1/5','Selected immutable status/head')
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
    path.write_bytes(body)
    pins.append({'path':str(relative),'bytes':len(body),'sha256':sha(body),'Git_blob':blob})
require(len(pins)==20,'Original file count')
queue=git('show',HEAD+':unsolved_math_prioritization/QUEUE.md')
require(sha(queue)==selected['queue_sha256'],'Full original QUEUE changed')
(F/'ORIGINAL_HEAD_QUEUE.md').write_bytes(queue)
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
raw,priorraw=db.execute('SELECT payload,report FROM records WHERE key=?',('30001234',)).fetchone()
db.close()
source,prior=json.loads(raw),json.loads(priorraw)
require(source==json.loads((O/'source_record.json').read_text()),'Full source statement semantics')
require(prior=={},'Prior report expected empty; reread if different')
review_hash=sha(json.dumps([source,prior],sort_keys=True).encode())
ready=json.loads((O/'readiness.json').read_text())
require(ready['review_hash']==review_hash,'Original readiness source binding')
turns=[json.loads(line) for line in (O/'turns.jsonl').read_text().splitlines()]
require(len(turns)==1 and turns[0]['turn']==1,'Original effort ledger')
dump(F/'SOURCE_STATEMENT.json',source)
dump(F/'PRIOR_REPORT.json',prior)
dump(F/'SOURCEPAIR_AUTHENTICATION.json',{'UTC':now(),'actual_operator_PID':os.getpid(),'numeric_id':30001234,
    'revision':cached_manifest['revision'],'SQL_records':15458,'cache_pins':cachepins,'full_statement_matches_original':True,
    'complete_prior_report':prior,'review_hash':review_hash,'original_budget':'1/5','new_central_proof_search_turns':0})
require(git('rev-parse','HEAD').decode().strip()==base and git('diff','--cached','--name-only','-z')==index_before
    and git('diff','--name-only','--diff-filter=ACMRTUXB','-z')==dirty_before,'Read-only checkout/index invariance')
record={'schema':'pr117-immutable-original-and-source-authentication/v1','UTC':now(),'actual_operator_PID':os.getpid(),
    'PR':117,'problem_id':30001234,'original_head':HEAD,'original_literal_status':'claimed_solved','original_budget':'1/5',
    'original_files':pins,'original_file_count':20,'original_ledger_entries':1,'full_source_prior_pair_verified':True,
    'review_hash':review_hash,'local_main_unchanged':base,'index_and_materialized_tracked_changes_unchanged':True,
    'new_central_proof_search_turns':0,'remote_service_mutations':False}
dump(F/'ORIGINAL_AUTHENTICATION.json',record)
dump(F/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'events':events})
(A/'RESEARCH_LOG.md').write_text('# PR117 /30001234 research log\n\n'+now()+': Literal incoming claimed_solved1/5 selected in ascending order after PR111 completion/release;112already_solved and113–116unsolved skipped by status only. All20 original Git bodies and full immutable source/empty prior authenticated. Original one-turn ledger preserved; no new central proof-search turn. Mathematical/source audit beginning: best guess10%; workflow5%; program19/99=19.19%; persistent goal active. No native/PR/publication/tracker mutation.\n')
print(json.dumps({k:v for k,v in record.items() if k!='original_files'},sort_keys=True))
