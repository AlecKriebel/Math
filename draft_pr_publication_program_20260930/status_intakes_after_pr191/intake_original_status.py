"""Read only original PR metadata and immutable-head QUEUE eligibility; import is inert."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,re,sys
D=Path(__file__).resolve().parent;P=D.parent;A=P/'audits/pr191_5000005'
def now():return datetime.datetime.now(datetime.UTC).isoformat()
def main(first,last):
 s=importlib.util.spec_from_file_location('native_status_only_after191',P/'audits/pr190_5000007/prepare_final_scoped_merge.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h);h.m.TREE_CACHE_PATH=D/'IMMUTABLE_TREE_CACHE.json'
 receipt=json.loads((A/'final_receipt_checkpoint_preparation_01/checkpoint_receipt01/CHECKPOINT_ACCEPTANCE.json').read_text())
 h.require(receipt['status']=='ACTUAL_PR191_FINAL_RECEIPT_CHECKPOINT_PARENT_FULL_DELTA_CURRENT_IDENTITIES_ACCEPTED' and receipt['fully_completed_count']==40 and receipt['published_count']==24 and receipt['every_selected_identity_checked_at_actual_observed_MAIN'] and receipt['next_numeric_intake_cursor']==192,'Actual previous own acceptance missing')
 tip=h.api('git/ref/heads/main')['object']['sha'];h.require(h.api('compare/'+receipt['checkpoint_commit']+'...'+tip)['status'] in ['identical','ahead'],'Accepted own checkpoint absent from MAIN')
 progress=json.loads(h.body_at(h.PREFIX+'CURRENT_PROGRESS.json',tip));h.require(progress['last_completed_PR']==191 and progress['fully_completed_count']==40 and progress['published_count']==24 and progress['actual_factual_checkpoint_accepted'] is True and progress['next_numeric_intake_cursor']==192 and progress['advance_to_next_PR_authorized_now'] is True,'Fresh prior acceptance/cursor changed')
 for number in range(first,last+1):
  target=D/f'PR{number}_ORIGINAL_STATUS_INTAKE.json';h.require(not target.exists(),'Never overwrite an original status intake')
  pr=h.api(f'pulls/{number}');head=pr['head']['sha'];match=re.search(r'(?<!\d)(\d{6,})(?!\d)',pr['title']);h.require(match is not None,'Need explicit problem identity from title metadata')
  pid=int(match.group(1));rows=[x for x in h.body_at('unsolved_math_prioritization/QUEUE.md',head).decode().splitlines() if f'| {pid} /' in x];h.require(len(rows)==1,'Original QUEUE row not unique');cells=rows[0].split('|');h.require(len(cells)==14,'QUEUE schema changed');status=cells[8].strip();eligible=status=='claimed_solved'
  out={'UTC':now(),'PR':number,'title':pr['title'],'original_head':head,'state_at_intake':pr['state'],'draft_at_intake':pr['draft'],'merged_at_intake':pr['merged'],'problem_id':pid,'original_QUEUE_status':status,'original_effort':cells[9].strip(),'original_QUEUE_row':rows[0],'row_SHA256':hashlib.sha256(rows[0].encode()).hexdigest(),'decision':'ELIGIBLE_CLAIMED_SOLVED_UNREVIEWED' if eligible else 'SKIP_UNTOUCHED_NON_CLAIMED_SOLVED','mathematical_review_performed':False,'priority_review_performed':False,'PR_or_QUEUE_or_native_attempt_mutations':0,'prior_PR191_factual_commit':'cb2504c65d87c14597fbd33cff98ad5f1d6ff0ee','prior_PR191_actual_own_checkpoint':receipt['checkpoint_commit'],'fresh_MAIN_observed':tip,'completed':40,'published':24}
  with target.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
  target.chmod(0o444)
  with (D/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+out['UTC']+f' — PR{number}/{pid} originalhead{head}: status{status}; '+out['decision']+'. Status classification100%; mathematical/priority/publicationreview0%. No PR/QUEUE/native attempt mutation;40completed/24published, broader goal active.\n')
  print(json.dumps({k:out[k] for k in ['PR','title','original_head','state_at_intake','draft_at_intake','merged_at_intake','problem_id','original_QUEUE_status','original_effort','decision']}),flush=True)
  if eligible:break
if __name__=='__main__':
 if not sys.dont_write_bytecode:raise RuntimeError('Use -B')
 main(int(sys.argv[1]),int(sys.argv[2]))

