"""Record observed successful audit publication, without guessing commit IDs."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess
A=Path(__file__).resolve().parent;P=A.parents[1];R=P.parent;C='11590683569346ea67151a497e798094347c8d29';sha=lambda b:hashlib.sha256(b).hexdigest()
start=datetime.now(timezone.utc).isoformat()
def run(argv):
 z=subprocess.run(argv,cwd=R,capture_output=True);assert z.returncode==0 and not z.stderr;return z.stdout
local=run(['git','rev-parse','HEAD']);remote=run(['git','ls-remote','origin','refs/heads/main']);assert local.decode().strip()==C and remote.decode().split()==[C,'refs/heads/main']
parent=run(['git','show','-s','--format=%P',C]).decode().split();assert parent==['6c120b2c88436b2e3f23e63861ece85db8d95eef']
allow=json.loads((P/'checkpoint_366_final_allowlist.json').read_bytes());changed=set(run(['git','diff-tree','--no-commit-id','--name-only','-r',C]).decode().splitlines());assert len(changed)==641 and changed<=set(allow['explicit_owned_paths'])
bindings=[]
for family,mf in [('priority_method_review','REVIEW_MANIFEST.json'),('variational_capacity_review','IMMUTABLE_MANIFEST.json'),('clean_final_adversary','IMMUTABLE_MANIFEST.json'),('post_merge_review','PUBLIC_MANIFEST.json')]:
 d=A/family;m=d/mf;assert run(['git','show',C+':'+str(m.relative_to(R))])==m.read_bytes()
 entries=json.loads(m.read_bytes())['files']
 for e in entries:
  p=d/e['path'];b=run(['git','show',C+':'+str(p.relative_to(R))]);assert len(b)==e['bytes'] and sha(b)==e['sha256']
 bindings.append({'family':family,'files':len(entries),'manifest_sha256':sha(m.read_bytes()),'all_committed_bytes_exact':True})
end=datetime.now(timezone.utc).isoformat()
out={'status':'OBSERVED_FINAL_PR366_AUDIT_PUBLICATION_PASS','observation_start_utc':start,'observation_end_utc':end,'published_audit_commit':C,'parent':parent[0],'owned_changed_paths':641,'all_four_public_manifests_verified_in_published_commit':bindings,'foreign_index_preserved':json.loads((P/'checkpoint_366_final_publication.stdout').read_bytes())['foreign_index_preserved'],'complete_local_main_stdout':local.decode(),'complete_raw_remote_main_stdout':remote.decode(),'actual_math_merge':'a7931795d85cd86c414200c5828d175046f707d5','accepted_status':'already_solved','turns':'1/5','audit_workflow_percent':100,'credited_method_resolution_percent':100,'new_theorem_percent':0,'program_completed':23,'program_total':349,'program_percent':23/349*100,'no_paper_zenodo_doi_tracker_release':True,'this_receipt_is_new_after_publication':'To be included in next owned checkpoint; published audit core commit is independently observed above.'}
(A/'GIT_PUBLICATION_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
c=json.loads((A/'acceptance_criteria.json').read_bytes());c['audit_artifact_publication_pending']=False;c['published_audit_commit']=C;(A/'acceptance_criteria.json').write_text(json.dumps(c,indent=2)+'\n')
o=json.loads((P/'inventory.json').read_bytes());e=next(e for e in o['items'] if e['number']==366);e['audit_artifact_publication_pending']=False;e['published_audit_commit']=C;e['completed_at']=end;(P/'inventory.json').write_text(json.dumps(o,indent=2)+'\n')
note=f'{end}: PR366 final audit publication OBSERVED as `{C}`, parent`{parent[0]}`:641 owned paths, complete8+26+194+99 manifest entries and manifest bytes checked from published Git objects; raw remote/localmain equal exact commit, foreign index preserved. Audit workflow100%, credited method100%, new theorem0%; program23/349=6.5903%. PR365 original19-file/18-target freeze included. No paper/DOI/tracker/release. This post-publication receipt will enter next checkpoint.\n'
for p in [A/'CURRENT_ACCEPTANCE_STATUS.md',A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
 with p.open('a') as f:f.write('\n'+note)
print(json.dumps({k:out[k] for k in ['status','published_audit_commit','owned_changed_paths','observation_end_utc']},indent=2))
