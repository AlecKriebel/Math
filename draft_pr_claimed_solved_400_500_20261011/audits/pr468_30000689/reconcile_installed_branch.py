#!/usr/bin/env python3
"""Read-only recovery after an interrupted binary Contents API readback."""
import base64,concurrent.futures,datetime,hashlib,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent
REPO='AlecKriebel/Math'
def api(s):
 p=subprocess.run(['gh','api','repos/'+REPO+'/'+s],capture_output=True)
 if p.returncode: raise RuntimeError(p.stderr.decode().strip())
 return json.loads(p.stdout)
def main():
 x=json.loads((R/'BRANCH_INTEGRATION_RECEIPT.json').read_text());head=x['commit_sha'];pr=api('pulls/468')
 if pr['head']['sha']!=head or pr['state']!='open' or pr['draft'] is not True: raise RuntimeError('Recorded installed branch head changed')
 tree=api('git/commits/'+head)['tree']['sha'];cache={}
 def child(sha,name):
  if sha not in cache: cache[sha]={e['path']:e for e in api('git/trees/'+sha)['tree']}
  return cache[sha][name]
 entries={}
 for path,expected in x['files_sha256'].items():
  sha=tree;parts=path.split('/')
  for part in parts[:-1]:
   e=child(sha,part)
   if e['type']!='tree':raise RuntimeError('Installed ancestor is not tree')
   sha=e['sha']
  e=child(sha,parts[-1])
  if e['type']!='blob' or e['sha']!=x['files_git_blob_sha'][path]:raise RuntimeError('Actual tree blob differs from recorded installation')
  entries[path]=e['sha']
 def verify(item):
  path,sha=item;b=api('git/blobs/'+sha)
  if b['encoding']!='base64':raise RuntimeError('Unsupported Git blob encoding')
  data=base64.b64decode(b['content']);digest=hashlib.sha256(data).hexdigest()
  if digest!=x['files_sha256'][path]:raise RuntimeError('Installed content changed: '+path)
  return {'path':path,'bytes':len(data),'sha256':digest,'git_blob_sha':sha}
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: verified=list(pool.map(verify,entries.items()))
 if api('pulls/468')['head']['sha']!=head:raise RuntimeError('PR moved during complete installed readback')
 diff=api('compare/'+x['parent_main_sha']+'...'+head)
 if not all(e['filename']=='unsolved_math_prioritization/QUEUE.md' or e['filename'].startswith('unsolved_math_prioritization/attempts/30000689/') for e in diff['files']):raise RuntimeError('Installed comparison has unrelated paths')
 now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 recovery={'verified_at_utc':now,'head_sha':head,'all_installed_files_verified':True,'verified_files':verified,'original_failure':'GitHub binary Contents API readback: transform: short source buffer','recovery':'Read-only Git tree/path and base64 Git-blob verification; no repeat branch mutation','scope_comparison_verified':True,'remote_mutations':0}
 (R/'BRANCH_READBACK_RECOVERY.json').write_text(json.dumps(recovery,indent=2)+'\n')
 x.update(state='branch_updated_verified',verified_at_utc=now,url='https://github.com/'+REPO+'/commit/'+head,readback_recovery='BRANCH_READBACK_RECOVERY.json');(R/'BRANCH_INTEGRATION_RECEIPT.json').write_text(json.dumps(x,indent=2)+'\n')
 pub=json.loads((R/'ZENODO_PUBLISH_RECEIPT.json').read_text())
 body=('Adjoining a missing middle-dimensional simplex to the middle skeleton of any finite triangulation of a topological even sphere prevents every topological embedding into that sphere. The note proves the precise Nevo–Wagner conjecture statement by a credited synthesis and an explicit dimension-four argument in the actual PL class.\n\n'
       'Published preprint: ['+pub['title']+']('+pub['doi_url']+'). Includes the accepted paper, source, exact canonical metadata, reproducible verification archive, and verified publication/tracker receipts. Original author and audit files remain frozen historical inputs.\n\n'
       'Validation: independent mathematical and bounded priority families, four successive complete-package adversaries, normal/optimized finite reproductions and actual fault controls. Complete installed Git tree/blob readback verifies all 95 selected files after an interrupted binary Contents API response.\n\n'
       'AI tools were used extensively. The preprint is unrefereed, with no independent human peer review, formal certification, first-priority or new-method claim. Only this problem’s QUEUE row and attempt folder differ from captured current main.\n')
 (R/'PR_BODY_CURRENT.md').write_text(body)
 print(json.dumps({'state':x['state'],'commit_sha':head,'verified_files':len(verified),'scope_comparison_verified':True},indent=2))
if __name__=='__main__':main()
