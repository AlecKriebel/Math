"""Apply only the scientifically adjudicated original PR173 disposition."""
from pathlib import Path
import importlib.util,json,hashlib,datetime
A=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('safe_api',A.parent/'pr152_5000006/prepare_scoped_merge.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
ORIGINAL='eb68ee2ecda39a8ec2748796d716c7a7598b7bc6';TITLE='Audit: growing-seed FPP follows from earlier general theory (30003677)'
def stamp():return datetime.datetime.now(datetime.UTC).isoformat()
if __name__=='__main__':
 gate=json.loads((A/'ROOT_FINAL_SCIENTIFIC_DISPOSITION.json').read_text());m.require(gate['scientific_audits_complete'] and gate['fresh_implication_adversary_complete'] and gate['original_theorem_mathematically_valid'] and gate['entire_original_existence_conclusion_implied_by_prior_general_theorem'] and not gate['publication_clearance'],'Final science not accepted')
 m.require(not (A/'PR_CLOSURE_ACTION_RECEIPT.json').exists(),'Unknown prior action; reconcile instead of repeating')
 orig=json.loads((A/'original_submission/PR_METADATA.json').read_text());pr=m.api('pulls/173');m.require(pr['head']['sha']==ORIGINAL and pr['state']=='open' and not pr['merged'] and pr['body']==orig['body'] and pr['title']==orig['title'],'Original PR head/state/metadata changed')
 body=(A/'PR_CLOSURE_BODY.md').read_text();comment=(A/'PR_CLOSURE_COMMENT.md').read_text();m.require(orig['body'] in body,'Original PR body not preserved')
 existing=m.api('issues/173/comments?per_page=100');m.require(not any(x['body']==comment for x in existing),'Exact prior comment exists; reconcile')
 posted=m.api('issues/173/comments','POST',{'body':comment});m.require(posted['body']==comment,'Provider comment body differs')
 rec={'UTC':stamp(),'PR':173,'original_head':ORIGINAL,'status':'EXACT_CREDIT_COMMENT_POSTED_CLOSURE_PENDING','comment_id':posted['id'],'comment_url':posted['html_url'],'comment_sha256':hashlib.sha256(comment.encode()).hexdigest(),'intended_title':TITLE,'intended_body_sha256':hashlib.sha256(body.encode()).hexdigest(),'new_paper_or_DOI_or_tracker':False};m.save(A/'PR_CLOSURE_ACTION_RECEIPT.json',rec)
 updated=m.api('pulls/173','PATCH',{'state':'closed','title':TITLE,'body':body});actual=m.api('pulls/173');actual_comment=m.api('issues/comments/'+str(posted['id']))
 m.require(actual['head']['sha']==ORIGINAL and actual['state']=='closed' and not actual['merged'] and actual['title']==TITLE and actual['body']==body and actual_comment['body']==comment,'Actual exact closure/readback differs')
 rec.update(UTC=stamp(),status='EXACT_ORIGINAL_PR173_CLOSED_UNMERGED_PROVIDER_READBACK_ACCEPTED',closed_at=actual['closed_at']);m.save(A/'PR_CLOSURE_ACTION_RECEIPT.json',rec)
 acceptance={**rec,'state':'closed','merged':False,'original_head_preserved':True,'author_branch_changed':False,'title':TITLE,'exact_comment_title_and_body_read_back':True,'priority_classification':'already_solved exact growing-seed existence, prior general-theorem implication','MAIN_findings_acceptance_pending':True};m.save(A/'PR_CLOSURE_ACCEPTANCE.json',acceptance)
 print(json.dumps({k:acceptance[k] for k in ['status','comment_url','closed_at','original_head_preserved']}))
