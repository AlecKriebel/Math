"""Observe actual publication and complete committed manifest bytes."""
from pathlib import Path
import datetime,hashlib,json,subprocess
A=Path(__file__).resolve().parent;P=A.parents[1];R=P.parent;sha=lambda b:hashlib.sha256(b).hexdigest()
def run(argv):
 s=subprocess.run(argv,cwd=R,capture_output=True);assert s.returncode==0 and not s.stderr;return s.stdout
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
start=utc();r=json.loads((P/'checkpoint_365_final_publication_receipt.json').read_bytes());C=r['commit'];remote=run(['git','ls-remote','origin','refs/heads/main']);seen=remote.decode().split();assert len(seen)==2 and seen[1]=='refs/heads/main'
if seen[0]!=C:
 s=subprocess.run(['git','fetch','origin','main'],cwd=R,capture_output=True);assert s.returncode==0
 assert subprocess.run(['git','merge-base','--is-ancestor',C,seen[0]],cwd=R).returncode==0
assert run(['git','show','-s','--format=%P',C]).decode().split()==[r['parent']]
allowed=set(json.loads((P/'checkpoint_365_final_allowlist.json').read_bytes())['explicit_owned_paths']);changed=set(run(['git','diff-tree','--no-commit-id','--name-only','-r',C]).decode().splitlines());assert len(changed)==r['changed_owned_paths'] and changed<=allowed
families=[]
for f in r['families']:
 D=A/f['family'];mp=D/f['manifest'];b=run(['git','show',C+':'+str(mp.relative_to(R))]);assert b==mp.read_bytes() and sha(b)==f['manifest_sha256'];j=json.loads(b);files=j.get('files',j.get('public_files'));files={e['path']:e for e in files} if isinstance(files,list) else files
 for p,e in files.items():
  b=run(['git','show',C+':'+str((D/p).relative_to(R))]);assert len(b)==e.get('bytes',e.get('stored_bytes')) and sha(b)==e.get('sha256',e.get('stored_sha256'))
 seal=run(['git','show',C+':'+str((D/'FINAL_SEAL.json').relative_to(R))]);assert sha(seal)==f['seal_sha256'];families.append(dict(f,all_committed_bytes_exact=True))
end=utc();out={'status':'OBSERVED_PR365_FINAL_AUDIT_PUBLICATION_PASS','observation_start_utc':start,'observation_end_utc':end,'published_audit_commit':C,'parent':r['parent'],'changed_owned_paths':len(changed),'verified_committed_families':families,'complete_raw_remote_main_stdout':remote.decode(),'observed_remote_contains_published_commit':True,'foreign_index_preserved':r['foreign_index_preserved'],'actual_math_merge':r['actual_merge'],'accepted_status':'already_solved','genuine_discovery_turns':'0/5','audit_workflow_percent':100,'credited_resolution_percent':100,'new_theorems':0,'no_paper_zenodo_doi_tracker_release':True,'post_publication_receipt_pending_next_owned_checkpoint':True}
(A/'GIT_PUBLICATION_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n');c=json.loads((A/'acceptance_criteria.json').read_bytes());c.update(audit_artifact_publication_pending=False,published_audit_commit=C);(A/'acceptance_criteria.json').write_text(json.dumps(c,indent=2)+'\n');i=json.loads((P/'inventory.json').read_bytes());e=next(e for e in i['items'] if e['number']==365);e.update(audit_artifact_publication_pending=False,published_audit_commit=C,completed_at=end);(P/'inventory.json').write_text(json.dumps(i,indent=2)+'\n')
for p in [A/'CURRENT_ACCEPTANCE_STATUS.md',A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
 with p.open('a') as h:h.write('\n'+end+': PR365 final audit publication OBSERVED '+C+'; all five complete public manifests/seals and every committed bound byte verified. Credited resolution100%, new theorem0, workflow100%; program'+str(i['completed_by_descending'])+'/'+str(len(i['items']))+'='+str(100*i['completed_by_descending']/len(i['items']))+'%. No paper/DOI/tracker/release. This observed receipt will enter the next owned checkpoint.\n')
print(json.dumps({k:out[k] for k in ['status','published_audit_commit','changed_owned_paths','observation_end_utc']},indent=2))
