#!/usr/bin/env python3
"""Verify static audit inventory. Anchor this code using the external receipt."""
import hashlib
import json
from pathlib import Path
import stat

NAMES={'AUDIT.md','PROOF_SUPPLEMENT.md','CLARIFICATION.patch','README.md',
       'SOURCE_REVIEW.json','IDENTITY_RECHECK.json','REPLAY_RESULTS.json',
       'MATH_RESULTS.json','independent_replay.py','identity_recheck.py',
       'mathematical_controls.py','verify_audit.py','MANIFEST.json'}

def require(value,message):
 if not value:raise RuntimeError(message)

def run():
 root=Path(__file__).absolute().parent
 require(stat.S_ISDIR(root.lstat().st_mode),'root is not regular directory')
 require({p.name for p in root.iterdir()}==NAMES,'inventory mismatch')
 for path in root.iterdir():require(stat.S_ISREG(path.lstat().st_mode),'nonregular node: '+path.name)
 manifest=json.loads((root/'MANIFEST.json').read_bytes())
 require(set(manifest)=={'schema','files'} and manifest['schema']==1,'manifest schema mismatch')
 require(set(manifest['files'])==NAMES-{'MANIFEST.json'},'manifest inventory mismatch')
 for name,item in manifest['files'].items():
  data=(root/name).read_bytes()
  require(set(item)=={'bytes','sha256'},'manifest record mismatch')
  require(item['bytes']==len(data),'size mismatch: '+name)
  require(item['sha256']==hashlib.sha256(data).hexdigest(),'hash mismatch: '+name)
 replay=json.loads((root/'REPLAY_RESULTS.json').read_bytes())
 require(replay['positive_count']==4 and replay['negative_count']==24,'replay counts mismatch')
 require(all(r['outcome']=='passed' for r in replay['positive_controls']),'positive control mismatch')
 require(all(r['outcome']=='rejected' for r in replay['negative_controls']),'negative control mismatch')
 math=json.loads((root/'MATH_RESULTS.json').read_bytes())
 require(math['identities_passed']==38 and math['negative_count']==5,'symbolic counts mismatch')
 identity=json.loads((root/'IDENTITY_RECHECK.json').read_bytes())
 require(identity['review_sha256']=='93431b0f7dfb31ed0a593e4e93b1f50f721e616143e026971b66530bdf2ce11b','review pin mismatch')
 require(identity['review_match'] is True and identity['statement_match'] is True,'identity mismatch')
 return {'schema':1,'files':len(NAMES),'verified':True,'scope':'audit inventory and stored-results consistency only; not theorem verification'}

if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
