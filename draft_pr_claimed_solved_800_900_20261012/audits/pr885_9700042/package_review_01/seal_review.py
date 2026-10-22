#!/usr/bin/env python3
"""Hash only the explicit safe outputs of this finished review; no remote action."""
import hashlib, json, os, sys
from pathlib import Path
root=Path(__file__).resolve().parent
candidate=Path(sys.argv[1])
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def save(name,value):
    path=root/(name+'.new')
    with path.open('xb') as f:f.write((json.dumps(value,indent=2,sort_keys=True)+'\n').encode())
    os.replace(path,root/name)
names=['SOURCE_FIRST_FREEZE.md','ANALYTIC_FREEZE.md','RESEARCH_LOG.md','REPORT.md','DECISION.json',
       'VISUAL_AND_SOURCE_RECEIPT.json','AUTHENTICATION.json','FINITE_CHECKS.json','CONTROL_RECEIPTS.json',
       'CURRENT_normal.stdout.json','CURRENT_normal.stderr.txt','CURRENT_normal.receipt.json','CURRENT_normal.validated.json',
       'CURRENT_optimized.stdout.json','CURRENT_optimized.stderr.txt','CURRENT_optimized.receipt.json','CURRENT_optimized.validated.json',
       'SOURCE_ONLY.stdout.json','check_package.py','seal_review.py']
snapshot=json.loads((root/'AUTHENTICATION.json').read_bytes())['snapshot']
for n,row in snapshot.items():
    if pin((candidate/n).read_bytes())!=row:raise RuntimeError('candidate changed: '+n)
decision=json.loads((root/'DECISION.json').read_bytes())
decision['final_all197_reauthenticated_unchanged']=True
core=['CURRENT_PUBLICATION_MANIFEST.json','CURRENT_PUBLICATION.json','portable.py','note.tex',
      'oriented-flow-note.pdf','oriented-flow-verification.zip','metadata.json','zenodo-deposit.json',
      'verification/portable.py','verification/note.tex','verification/metadata.json',
      'verification/zenodo-deposit.json','verification/package_index.json']
decision['exact_core_files']=[{'path':n,**snapshot[n]} for n in core]
save('DECISION.json',decision)
rows=[]
for n in names:
    data=(root/n).read_bytes()
    if n.endswith('.json'):json.loads(data)
    rows.append({'path':n,**pin(data)})
manifest={'schema':'pr885-package-review-01-safe-authored-files-v1','scope':'Explicit review outputs only; no recursive publication authorization.',
          'verdict':'CLEAR','current_manifest_sha256':decision['current_manifest_sha256'],
          'excluded':['SAFE_FILES_MANIFEST.json itself','private_tmp/','primary bodies','raw corpora','renders','credentials'],
          'files':rows}
save('SAFE_FILES_MANIFEST.json',manifest)
print(json.dumps({'status':'PASS','safe_file_count':len(rows),'safe_manifest':pin((root/'SAFE_FILES_MANIFEST.json').read_bytes()),
                 'all197_unchanged':True,'report':pin((root/'REPORT.md').read_bytes()),'decision':pin((root/'DECISION.json').read_bytes())},sort_keys=True))
