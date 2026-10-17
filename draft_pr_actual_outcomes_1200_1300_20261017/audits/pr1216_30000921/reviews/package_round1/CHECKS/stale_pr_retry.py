"""Demonstrate stale intent/receipt acceptance without Git or network mutation."""
from pathlib import Path
import hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;PUB=HERE.parent.parents[1]/'publication'
results=[]
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x)+'\n')
for mode in ['stale_intent','stale_receipt']:
 spec=importlib.util.spec_from_file_location('prretry_'+mode,PUB/'update_pr_publication.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 m.ROOT=HERE.parent/'temp'/mode;m.ROOT.mkdir(exist_ok=True)
 build=json.loads((PUB/'BUILD_RECEIPT.json').read_text())
 for key in ['pdf','verification_zip']:(m.ROOT/build[key]['path']).write_bytes((PUB/build[key]['path']).read_bytes())
 (m.ROOT/'zenodo-deposit.json').write_bytes((PUB/'zenodo-deposit.json').read_bytes())
 gate={'status':'pass','pdf_sha256':build['pdf']['sha256'],'verification_zip_sha256':build['verification_zip']['sha256'],'metadata_sha256':hashlib.sha256((PUB/'zenodo-deposit.json').read_bytes()).hexdigest(),'workflow':{}}
 pub={'state':'published','doi':'10.0000/current-fixture','files':[{'name':build[k]['path'],'sha256':build[k]['sha256'],'size':build[k]['bytes']} for k in ['pdf','verification_zip']]}
 tracker={'readback_verified':True}
 stale={'commit':'stale-commit-from-an-earlier-package','review_gate_sha256':'obsolete-review-gate','doi':'10.0000/obsolete-fixture','files':{'old.pdf':{'sha256':'obsolete','bytes':1}},'paths':['obsolete/old.pdf']}
 for name,v in [('BUILD_RECEIPT.json',build),('FINAL_REVIEW_GATE.json',gate),('PUBLICATION_RECEIPT.json',pub),('tracker/TRACKER_RECEIPT.json',tracker),('PR_BRANCH_INTENT.json' if mode=='stale_intent' else 'PR_BRANCH_RECEIPT.json',stale)]:save(m.ROOT/name,v)
 save(m.ROOT.parent/'SUBMITTED_SNAPSHOT.json',{'files':[],'body_sha256':'unused'})
 current={'headRefName':m.BRANCH,'state':'OPEN','headRefOid':m.ORIGINAL if mode=='stale_intent' else stale['commit']}
 calls=[]
 def fakegit(*args,**kw):
  calls.append(list(args))
  if args==('branch','--show-current'):return b'main'
  if args[0]=='ls-remote':return (stale['commit']+'\trefs/heads/'+m.BRANCH+'\n').encode()
  raise RuntimeError('Unexpected Git request '+str(args))
 m.git=fakegit;m.pr=lambda:current
 m.main()
 output=json.loads((m.ROOT/'PR_BRANCH_RECEIPT.json').read_text())
 if output['review_gate_sha256']!='obsolete-review-gate' or output['doi']!='10.0000/obsolete-fixture':raise RuntimeError('fixture did not exercise stale branch')
 results.append({'case':mode,'accepted_stale_review_gate_and_artifacts':True,'old_intent_doi':output['doi'],'current_publication_doi':pub['doi'],'git_calls_fully_stubbed':calls,'external_calls':0})
(HERE/'stale_pr_retry.json').write_text(json.dumps({'status':'REPRODUCED_GUARD_GAP','cases':results,'repair':'Before accepting either intent or receipt, compare its review_gate_sha256 and DOI plus expected committed path/byte bindings against the current review/build/publication/tracker package, and inspect recorded commit blobs using read-only Git. Fail closed on any drift.'},indent=2)+'\n')
print(json.dumps(results,indent=2))
