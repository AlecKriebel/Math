"""Immutable original-QUEUE eligibility only. No mathematical review or PR write."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,re,sys
D=Path(__file__).resolve().parent;P=D.parent;A=P/'audits/pr201_5100014'
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main(num):
 p=A/'publication_lifecycle_01/finish201.py';sp=importlib.util.spec_from_file_location('completed201lowlevel',p);v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v);c,h,rv,n=v.load();h.m.TREE_CACHE_PATH=D/'PRIVATE_TREE_CACHE.json';prior=v.m.read(A/'publication_lifecycle_01/completion100_01/ACCEPTANCE.json')
 assert prior['accepted'] and prior['completion_metadata_accepted'] and prior['advance_to_next_PR_authorized_now'] and prior['every_selected_identity_checked_at_actual_observed_MAIN'] and prior['checkpoint_commit']=='0c0ef219dd5aa4547ad7ee47ac1ab5b08ca232f0' and prior['selected_files']==2960 and prior['actual_current_selected_map_sha256']=='899483aceb752476b19db7be18c13ac484907380da6b2cefe7fbad3b597e53f6'
 assert pin((A/'publication_lifecycle_01/completion100_01/ACCEPTANCE.json').read_bytes())=={'bytes': 1636, 'sha256': '9d6c23ec88334eb88553dfe7f70aa629bf36143a678fbaa21591c89fcb541606'}
 assert num>=202
 if num>202:
  previous=v.m.read(D/f'PR{num-1}_ORIGINAL_STATUS_INTAKE.json');assert previous['eligible'] is False and previous['next_status_only_cursor']==num
 pr=h.api('pulls/'+str(num));assert pr['state']=='open' and pr['draft'] and not pr['merged']
 current_head=pr['head']['sha'];current_co=h.api('git/commits/'+current_head);assert len(current_co['parents'])==1;commits=[];page=1
 while True:
  xs=h.api(f'pulls/{num}/commits?per_page=100&page={page}');commits+=xs
  if len(xs)<100:break
  page+=1
 assert len(commits)==pr['commits'] and commits[-1]['sha']==current_head
 for x,y in zip(commits,commits[1:]):assert len(y['parents'])==1 and y['parents'][0]['sha']==x['sha']
 events=[];page=1
 while True:
  xs=h.api(f'issues/{num}/timeline?per_page=100&page={page}');events+=xs
  if len(xs)<100:break
  page+=1
 assert not any(x.get('event')=='head_ref_force_pushed' for x in events)
 assert [x.get('sha') for x in events if x.get('event')=='committed']==[x['sha'] for x in commits]
 original_prefix=[]
 for x in commits:
  if x['commit']['committer']['date']>pr['created_at']:break
  original_prefix.append(x)
 assert original_prefix and all(x['commit']['committer']['date']>pr['created_at'] for x in commits[len(original_prefix):])
 later_count=len(commits)-len(original_prefix)
 if pr['created_at']!=pr['updated_at'] and later_count==0:assert len(commits)==1,'Need further custody if edited PR has multiple possible precreation heads'
 head=original_prefix[-1]['sha'];co=h.api('git/commits/'+head);assert len(co['parents'])==1
 q='unsolved_math_prioritization/QUEUE.md';body=h.body_at(q,head);x=c.byte_pin(body);assert h.lookup(co['tree']['sha'],q)==('100644','blob',x['git_blob']);pid=pr['title'].split(':',1)[0].strip()
 if not pid.isdigit():
  match=re.fullmatch(r'dot/math-([0-9]+)',pr['head']['ref']);assert match;pid=match[1]
 rows=[row for row in body.splitlines(keepends=True) if len(row.decode().split('|'))==14 and row.decode().split('|')[2].strip().split(' / ')[0]==pid];assert len(rows)==1;row=rows[0];cells=row.decode().split('|');status=cells[8].strip();eligible=status=='claimed_solved';stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
 j={'UTC':stamp,'PR':num,'problem_id':int(pid),'PR_title_metadata':pr['title'],'original_submitted_head':head,'head_tree':co['tree']['sha'],'head_sole_parent':co['parents'][0]['sha'],'original_range_base':commits[0]['parents'][0]['sha'],'original_author_commit_count':len(commits),'created_at':pr['created_at'],'updated_at':pr['updated_at'],'open_original_draft':True,'all_original_author_commits_predate_creation_and_form_complete_linear_chain':True,'complete_PR_timeline_count':len(events),'no_force_push_events':True,'original_QUEUE_blob':x,'original_QUEUE_row':pin(row),'original_QUEUE_status':status,'original_QUEUE_effort_cell':cells[9].strip(),'eligible':eligible,'action':'ELIGIBLE_CUSTODY_REQUIRED_BEFORE_ANY_MATH' if eligible else 'STATUS_ONLY_SKIP_UNTOUCHED','no_mathematical_content_reviewed':True,'no_PR_comment_merge_close_paper_or_repair':True,'prior_actual_PR201_completion_receipt':c.byte_pin((A/'publication_lifecycle_01/completion100_01/ACCEPTANCE.json').read_bytes()),'prior_status_only_record':pin((D/f'PR{num-1}_ORIGINAL_STATUS_INTAKE.json').read_bytes()) if num>202 else None,'procedure_source':pin(Path(__file__).read_bytes()),'prior_actual_completed_count':45,'prior_actual_published_count':29,'next_status_only_cursor':num if eligible else num+1}
 j['original_author_commit_count']=len(original_prefix);j['current_branch_commit_count']=len(commits);j['current_branch_head']=current_head;j['post_creation_commits_excluded_from_original_eligibility']=later_count;j['original_range_base']=original_prefix[0]['parents'][0]['sha'];j['PR_metadata_edit_present']=pr['created_at']!=pr['updated_at'];j['edited_PR_original_head_evidence']='Complete linear pre/post creation commit-prefix partition and matching committed timeline, no force-push events; original head is last precreation prefix commit. Later commits excluded.' if later_count else ('Sole committed timeline item and sole PR commit equal current HEAD, one parent and commit predating creation, complete no-force-push timeline.' if j['PR_metadata_edit_present'] else 'Creation and update timestamps identical; complete precreation commit chain and no-force-push timeline.')
 path=D/f'PR{num}_ORIGINAL_STATUS_INTAKE.json'
 with path.open('xb') as f:f.write((json.dumps(j,indent=2)+'\n').encode())
 path.chmod(0o444);print(json.dumps({'PR':num,'problem_id':int(pid),'original_HEAD':head,'original_QUEUE_status':status,'eligible':eligible,'action':j['action'],'next_status_only_cursor':j['next_status_only_cursor'],'record_SHA256':hashlib.sha256(path.read_bytes()).hexdigest()}))
if __name__=='__main__':
 assert sys.dont_write_bytecode
 main(int(sys.argv[1]))
