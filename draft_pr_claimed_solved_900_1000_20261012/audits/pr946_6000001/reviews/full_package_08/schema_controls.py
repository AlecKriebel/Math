import sys
if not sys.flags.isolated or sys.flags.optimize:raise RuntimeError('Use -I -B')
from pathlib import Path
import json,copy,hashlib,shutil
O=Path(__file__).resolve().parent;R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';root=O/'private/current08_context';p=root/P.name;a=p/'audits/pr946_6000001';d=a/'preprint';N={'__name__':'_schema05_','__file__':str(P/'accept_pr946.py')};exec(compile((P/'accept_pr946.py').read_bytes(),N['__file__'],'exec'),N);N.update(ROOT=root,P=p,A=a,D=d)
w=a/'reviews/full_package_08';results=[]
def reject(label,fn):
 try:fn()
 except (RuntimeError,ValueError,TypeError,OSError):results.append({'case':label,'rejected':True});return
 raise RuntimeError('Invalid accepted '+label)
for filename,func in [('RESULT.json','result_schema'),('AUTHENTICATION_START.json','authentication_schema'),('COLD_REPLAY.json','cold_schema')]:
 obj=json.loads((w/filename).read_text());N[func](obj)
 # These are documented mandatory fields, not arbitrary optional provenance.
 keys=[k for k in obj if k!='inspected_publication_operator'] if filename=='RESULT.json' else ['status','utc','original_pr_head','freeze_sha256','package_manifest_sha256','future_helpers','candidate_files','payloads','archive_members','originals'] if filename.startswith('AUTH') else ['status','utc','cold_extraction','typed_float_policy_verified','historical_strict_failure_preserved','package_manifest_sha256','externally_pinned_verifier_sha256','normalized_fields_ignored','modes']
 for key in keys:
  altered=copy.deepcopy(obj);del altered[key];reject(filename+'_missing_'+key,lambda:N[func](altered))
  if key=='mathematical_remaining_gap_for_stated_theorem':wrong=0
  else:wrong=0 if type(obj[key]) is not int else True
  altered=copy.deepcopy(obj);altered[key]=wrong;reject(filename+'_wrongtype_'+key,lambda:N[func](altered))
accepted=json.loads((a/'ACCEPTANCE.json').read_text());specs=[f"{r['round']:02d}:"+r['manifest_sha256'] for r in accepted['full_package_reviews']];N['require_complete_review_history'](specs)
for name in ['full_package_09','full_package_XX','FULL_PACKAGE_09','full_package_10']:
 path=a/'reviews'/name;path.mkdir();reject('canonical_directory_'+name,lambda:N['require_complete_review_history'](specs));path.rmdir()
path=a/'reviews/full_package_09';path.symlink_to(w,target_is_directory=True);reject('canonical_directory_symlink',lambda:N['require_complete_review_history'](specs));path.unlink()
reject('omitted_latest_prefix',lambda:N['require_complete_review_history'](specs[:-1]));reject('sequence_gap',lambda:N['validate_review_sequence']([specs[0],specs[2]]))
(O/'SCHEMA_CONTROLS.json').write_text(json.dumps({'status':'PASS','subject_candidate_revision':6,'actual_current_schema_functions':True,'actual_canonical_directory_scan':True,'controls':results,'control_count':len(results),'external_mutations':0},indent=2)+'\n');print(json.dumps({'status':'PASS','controls':len(results)}))
