from pathlib import Path
import subprocess,json,hashlib,datetime
A=Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr124_10400231')
G='/opt/homebrew/Cellar/git/2.38.2/bin/git'
C='/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout'
body=subprocess.check_output([G,'show','d110ad761291aa6ac1d66d2a49e8b8212c18bed6:unsolved_math_prioritization/review_v2/related_target_groups.json'],cwd=C)
groups=json.loads(body)
def walk(v):
 if isinstance(v,dict):
  if any(str(x)=='10400231' for x in v.values() if isinstance(x,(str,int))):yield v
  for x in v.values():
   if isinstance(x,(list,dict)):yield from walk(x)
 elif isinstance(v,list):
  if any(str(x)=='10400231' for x in v if isinstance(x,(str,int))):yield v
  for x in v:
   if isinstance(x,(list,dict)):yield from walk(x)
hits=list(walk(groups))
out={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'numeric_id':10400231,'immutable_head':'d110ad761291aa6ac1d66d2a49e8b8212c18bed6','related_groups_body_sha256':hashlib.sha256(body).hexdigest(),'direct_membership_hits':hits,'related_PR_processing':False}
(A/'RELATED_TARGET_SCOPE_CHECK_20261006.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out))

