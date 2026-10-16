"""Consume PR identity and immutable-head QUEUE eligibility only; no math review."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,re,sys
D=Path(__file__).resolve().parent;P=D.parent;A=P/'audits/pr190_5000007'
s=importlib.util.spec_from_file_location('previous190',A/'prepare_final_scoped_merge.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
m.m.TREE_CACHE_PATH=D/'IMMUTABLE_TREE_CACHE.json'
def now():return datetime.datetime.now(datetime.UTC).isoformat()
f=json.loads((A/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json').read_text());m.require(f['fully_completed_count']==39 and f['published_count']==23,'Actual previous acceptance absent')
tip=m.api('git/ref/heads/main')['object']['sha'];progress=json.loads(m.body_at(m.PREFIX+'CURRENT_PROGRESS.json',tip));m.require(progress['last_completed_PR']==190 and progress['fully_completed_count']==39 and progress['published_count']==23,'Fresh accepted census changed')
for number in range(int(sys.argv[1]),int(sys.argv[2])+1):
 target=D/f'PR{number}_ORIGINAL_STATUS_INTAKE.json';m.require(not target.exists(),'Existing original intake must not be overwritten')
 pr=m.api(f'pulls/{number}');head=pr['head']['sha'];match=re.search(r'(?<!\d)(\d{6,})(?!\d)',pr['title']);m.require(match is not None,'Need explicit original problem identity from metadata')
 pid=int(match.group(1));rows=[x for x in m.body_at('unsolved_math_prioritization/QUEUE.md',head).decode().splitlines() if f'| {pid} /' in x];m.require(len(rows)==1,'Original QUEUE row not unique');cells=rows[0].split('|');m.require(len(cells)==14,'QUEUE schema changed');status=cells[8].strip();eligible=status=='claimed_solved'
 r={'UTC':now(),'PR':number,'title':pr['title'],'original_head':head,'state_at_intake':pr['state'],'draft_at_intake':pr['draft'],'merged_at_intake':pr['merged'],'problem_id':pid,'original_QUEUE_status':status,'original_effort':cells[9].strip(),'original_QUEUE_row':rows[0],'row_SHA256':hashlib.sha256(rows[0].encode()).hexdigest(),'decision':'ELIGIBLE_CLAIMED_SOLVED_UNREVIEWED' if eligible else 'SKIP_UNTOUCHED_NON_CLAIMED_SOLVED','mathematical_review_performed':False,'priority_review_performed':False,'PR_or_QUEUE_or_native_attempt_mutations':0,'prior_PR190_factual_commit':f['factual_commit'],'fresh_MAIN_observed':tip,'completed':39,'published':23}
 m.save(target,r)
 with (D/'RESEARCH_LOG.md').open('a') as out:out.write('\n'+r['UTC']+f' — PR{number}/{pid} originalhead{head}: status{status}, '+r['decision']+'. Status-only classification100%; mathematics/priority/publicationreview0%. No PR/QUEUE/nativeattempt mutation;39completed/23published unchanged, broadergoalactive.\n')
 print(json.dumps({k:r[k] for k in ['PR','title','original_head','state_at_intake','draft_at_intake','problem_id','original_QUEUE_status','original_effort','decision']}),flush=True)
 if eligible:break
