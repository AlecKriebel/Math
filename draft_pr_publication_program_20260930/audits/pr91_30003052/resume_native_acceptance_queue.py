from pathlib import Path
import json,subprocess,hashlib,datetime,os,ast
A=Path(__file__).resolve().parent;C=A.parents[2];D=A/'native_acceptance_20261005';N=C/'unsolved_math_prioritization/attempts/30003052';base='165350df9ca81d8bad9f3447130930d73b6c7ee4';old='657add47248e08c05126627b7e2caa6a597d4831';records=[]
def require(c,m):
 if not c:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def git(*args):
 argv=['git',*args];t=now();p=subprocess.Popen(argv,cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate();i=len(records)
 for name,b in [('stdout',out),('stderr',err)]:(D/('resume_'+str(i)+'.'+name+'.bin')).write_bytes(b)
 records.append({'argv':argv,'PID':p.pid,'UTC_start':t,'UTC_end':now(),'exit_code':p.returncode,'stdout_file':'resume_'+str(i)+'.stdout.bin','stderr_file':'resume_'+str(i)+'.stderr.bin','stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_sha256':hashlib.sha256(err).hexdigest()});dump(D/'QUEUE_RESUME_PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'records':records});require(p.returncode==0,'git command');return out
j=json.loads((D/'PROCESS_JOURNAL.json').read_text());require(len(j['records'])==32 and all(r['exit_code']==0 for r in j['records']),'prior actual operations')
for r in j['records']:
 for channel in ['stdout','stderr']:require(sha(D/r[channel+'_file'])==r[channel+'_sha256'],'prior full stream changed')
require(git('rev-parse','HEAD').strip().decode()==base and git('symbolic-ref','--short','HEAD').strip()==b'main' and not git('diff','--cached','--name-only','-z'),'base/index changed')
for rel,expected in [('verify.py','89d760d1a41553c9d4ae3b7261fd24c3c24403dac37304c1dfc2a6057e6260f7'),('review/author_replay/verify.py','89d760d1a41553c9d4ae3b7261fd24c3c24403dac37304c1dfc2a6057e6260f7'),('review/independent_checks.py','d7ed5c686d31f435248aaca4eb3bd3dd8251c1894e3bcbc1f1e2ba159767f1a1')]:
 require(sha(N/rel)==expected and not any(isinstance(x,ast.Assert) for x in ast.walk(ast.parse((N/rel).read_text()))),'active minimal guard repair differs')
current_hash=sha(N/'CLASSIFICATION.md')
for index,rel,count in [(28,'verification.json',473),(29,'review/author_replay/verification.json',473),(30,'review/independent_results.json',907)]:
 r=j['records'][index];require('-O' in r['argv'],'not optimized');x=json.loads((D/r['stdout_file']).read_bytes());require(x['status']=='PASS' and x['exact_assertions']==count,'native count');require((N/rel).read_bytes()==(D/r['stdout_file']).read_bytes() if count==473 else json.loads((N/rel).read_text())==x,'native receipt changed')
require(json.loads((N/'verification.json').read_text())['artifact_sha256']==current_hash,'current proof receipt')
for rel in ['status.json','readiness.json']:require(json.loads((N/rel).read_text())['artifact_sha256']==current_hash,'active metadata changed')
orig=json.loads((A/'original_source_authentication_20261005/ORIGINAL_BLOB_MANIFEST.json').read_text())
for row in orig['files']:require(sha(Path(row['preserved_path']))==row['sha256'],'original archive changed')
q=C/'unsolved_math_prioritization/QUEUE.md';before=q.read_bytes();oldbody=git('show',old+':unsolved_math_prioritization/QUEUE.md');require(before==oldbody,'queue has unknown worktree edits')
qb=git('show',base+':unsolved_math_prioritization/QUEUE.md').decode();lines=qb.splitlines();ix=[i for i,s in enumerate(lines) if '| 30003052 / OWR-14215-004 |' in s];require(len(ix)==1,'unique row');i=ix[0];cells=lines[i].split('|');require(cells[8].strip()=='claimed_solved' and cells[9].strip()=='1/5','status or budget changed')
cells[11]=' 2026-10-05: Verified full closed-ball C(U) classification; explicit mixed converse completed by credited classical JdLG specialization. Known cases and immediate full-disk consequence credited. Two fresh whole-package AI reviews, attribution repair and optimization-safe verifiers; unrefereed, bounded priority audit, no firstness claim. PR91 accepted and preprint published. ';cells[12]=' https://doi.org/10.5281/zenodo.23171212 ';lines[i]='|'.join(cells);q.write_text('\n'.join(lines)+'\n')
(A/'actual_operations/prepare_native_acceptance/FAILURE_NOTE.md').write_text('The actual preparation exited 1 at the queue worktree-equality guard after fetching the actual merge and preparing all native files. All 32 recorded commands succeeded, including the three optimized verification runs. The queue worktree still matched the previous committed main body exactly; the incoming merge had changed the same PR91 row. This was expected committed-base lag, not a foreign uncommitted edit. The failed invocation and all process streams are preserved. A separately recorded bounded resume authenticates the previous committed queue body, preserves the complete new merged main queue, and updates only the accepted row. No repeat publication, tracker append, PR merge or checker execution is performed.\n')
tracker=json.loads((A/'ROOT_TRACKER_RECORD.json').read_text());pub=json.loads((A/'actual_operations/zenodo_publish/stdout.bin').read_bytes());x={'schema':'pr91-native-acceptance-preparation/v1','UTC':now(),'actual_operator_PID':os.getpid(),'actual_preparation_PID':j['operator_PID'],'actual_preparation_exit_code':1,'bounded_queue_resume_completed':True,'PR':91,'head':'2ea84c5de45cb92783b5b55057af1f52590be6bf','merge_commit':base,'base_commit':base,'DOI':pub['doi'],'record_url':pub['record_url'],'tracker_range':tracker['range'],'original_budget':'1/5','new_central_proof_search_turns':0,'incoming_bodies_unchanged':20,'native_exact_controls':[473,473,907],'native_optimized_runs_passed':True,'current_artifact_sha256':current_hash,'native_paths':[r['path'] for r in orig['files']]+['unsolved_math_prioritization/QUEUE.md'],'main_checkpoint_pending':True,'primary_checkout_mutated':False,'primary_synchronization_pending':True,'old_queue_proved_equal_to_premerge_committed_main':True}
dump(D/'PREPARED_RECEIPT.json',x);print(json.dumps({k:v for k,v in x.items() if k!='native_paths'}))
