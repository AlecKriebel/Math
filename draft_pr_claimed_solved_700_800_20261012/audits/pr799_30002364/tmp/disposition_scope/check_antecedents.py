"""Read-only PR799 administrative gate and preserved-source authentication.

Does not execute candidate mathematical code, mutate Git/GitHub/native state,
claim mathematical formalization, or inspect any other problem's mathematics.
"""
from pathlib import Path
import hashlib,json,zipfile,io

T=Path(__file__).resolve().parent.parent
HEAD='cc45ec9dc93515593c3b2a228def86c3a562e13f'
IDENTITY='a875b05b2fd00b21dde0328993d8ae6492588c9b02f03f2655ee6cdb0d51b9fe'
COMMENT='bed43312c2e0d80d5067f130e0c479ee829b03decd96dabed270bc082014dea4'
def need(v,m):
 if not v: raise ValueError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p):return json.loads((T/p).read_bytes())
G=load('intake/ELIGIBILITY.json');S=load('intake/ROOT_SOURCE_IDENTITY.json')
M=load('root-receipts/MATH_GATE.json');P=load('root-receipts/PRIORITY_GATE.json');R=load('root-receipts/ROOT_PRIORITY_REPLAYS.json')
need(sha((T/'intake/ROOT_SOURCE_IDENTITY.json').read_bytes())==IDENTITY,'Source identity pin')
need(sha((T/'root-receipts/CLOSE_COMMENT.md').read_bytes())==COMMENT,'Comment pin')
need(G['pr']==799 and G['problem']=='30002364' and G['eligible'] is True,'Eligibility target')
need(G['PR_metadata']['headRefOid']==HEAD and G['PR_metadata']['state']=='OPEN' and G['PR_metadata']['isDraft'] is True and G['PR_metadata']['merged'] is False,'Eligible immutable head')
cells=G['exact_immutable_head_QUEUE_row'].split('|')
need(len(cells)==14 and cells[8].strip()==G['exact_status']=='claimed_solved' and cells[9].strip()=='5/5' and not cells[12].strip(),'Exact original eligibility and budget')
need(S['reviewed_head']==M['reviewed_head']==P['reviewed_head']==HEAD,'Cross-gate reviewed head')
need(M['source_identity_sha256']==IDENTITY and M['result']=='PASS' and M['remaining_mathematical_issues']==[],'Math administrative antecedent')
need(P['result']=='FULL_PREDECESSOR_BY_TWO_INDEPENDENT_CHECKED_COROLLARIES' and P['mathematical_gate']=='PASS' and P['remaining_central_priority_gaps']==[],'Priority antecedent')
need(P['priority_families']==R['independent_discovery_families']==2 and P['fresh_priority_adversaries']==R['fresh_priority_adversaries']==2 and R['result']=='PASS','Independent-family/replay count')
need(sha((T/'root-receipts'/P['root_replay']).read_bytes())==P['root_replay_sha256'],'Root replay pin')
need(P['exact_eightfold_firstness_established'] is False and P['earliest_global_priority_certified'] is False and P['no_source_claimed_to_explicitly_state_this_exact_question_answer'] is True,'Priority limits')
need(P['recommended_original_problem_status']=='already_solved' and P['recommended_PR_disposition']=='close_without_merge_with_explanation' and P['new_original_resolution_preprint_warranted'] is False,'Recommended disposition')
need(P['original_explicit_budget']==M['original_explicit_budget']=='5/5' and P['new_substantive_proof_turns']==M['new_substantive_proof_turns']==0,'No new proof budget')
need(P['action_executed'] is False,'This is a pre-disposition gate')
selected=load('intake/SELECTED_PUBLIC_RECORD.json');problem=selected['problem'];prior=selected['prior_research']
need(sha(problem['statement'].encode())==S['statement_sha256']==M['statement_hash'],'Statement pin')
need(sha(json.dumps([problem,prior],sort_keys=True).encode())==S['review_hash']==M['review_hash'],'Complete selected-record review pin')
originals=S['original_files'];need(len(originals)==54 and len({r['path'] for r in originals})==54,'54 unique originals')
for row in originals:
 path=T/'intake/original'/row['path'];need(path.is_file() and not path.is_symlink(),'Regular preserved original')
 b=path.read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'Original content identity: '+row['path'])
 gitsha=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();need(gitsha==row['git_blob'],'Original Git-blob identity')
archive_members=0
for archive in S['ZIP_archives']:
 with zipfile.ZipFile(T/'intake/original'/archive['path']) as z:
  names=z.namelist();need(len(names)==len(set(names))==len(archive['members']),'ZIP exact unique member count')
  need(set(names)=={r['path'] for r in archive['members']},'ZIP exact inventory')
  for row in archive['members']:
   b=z.read(row['path']);need(len(b)==row['bytes'] and sha(b)==row['sha256'],'ZIP member content identity')
   archive_members+=1
need(len(S['ZIP_archives'])==4 and archive_members==30,'Four original archives, thirty members')
for pkt,receipt in zip(P['priority_packets'],R['records']):
 need(pkt['family']==receipt['family'] and pkt['result']==receipt['result']=='PASS' and receipt['original_unchanged'] is True,'Per-family replay agreement')
 for key in ['manifest_sha256','checker_sha256','closed_files']:need(pkt[key]==receipt[key],'Per-family pin agrees')
 base=T/pkt['family']
 need(sha((base/pkt['manifest']).read_bytes())==pkt['manifest_sha256'],'Priority manifest pin')
 need(sha((base/pkt['checker']).read_bytes())==pkt['checker_sha256'],'Priority checker pin')
print(json.dumps({'result':'PASS','scope':'Administrative antecedents and preserved bytes only; no mathematical re-review','head':HEAD,'source_identity_sha256':IDENTITY,'comment_sha256':COMMENT,'original_files':54,'original_bytes':sum(r['bytes'] for r in originals),'original_archives':4,'original_archive_members':archive_members,'priority_packets_pinned':4,'original_budget':'5/5','new_proof_turns':0,'future_actions_not_verified':['Exact-head closure and posted comment','Native eight-path mirror and preservation','Final shard metadata screen and delivery']},sort_keys=True))
