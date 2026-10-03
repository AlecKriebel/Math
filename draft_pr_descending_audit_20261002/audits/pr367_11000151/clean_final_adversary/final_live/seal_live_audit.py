"""Seal this additive namespace only after the complete exact-live gate passes."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
D=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def row(p):
 b=p.read_bytes();return {'path':p.relative_to(D).as_posix(),'bytes':len(b),'sha256':sha(b)}
def write(p,o):p.write_text(json.dumps(o,indent=2)+'\n')
r=json.loads((D/'receipts/FINAL_LIVE_RECEIPT.json').read_bytes())
assert r['status']=='QUALIFIED_EXACT_LIVE_ACCEPTANCE_PASS'
checks=json.loads((D/'receipts/CHECKS.json').read_bytes())
assert len(checks)==r['checks'] and all(c['pass'] is True for c in checks)
(D/'FINAL_REPORT.md').write_text(
 '# Additive exact-live acceptance audit of PR367\n\n'
 'Qualified PASS at head '+r['head']+' and current main/base '+r['base']+'. '
 'The complete accepted body binding is '+r['body']['sha256']+'. '
 'Actual GitHub test-merge '+r['testmerge_sha']+' has the exact expected parents and tree '+r['testmerge_tree']+'.\n\n'
 'All44 changed Git/API blobs and modes, the43 unchanged original target files, only own queue line400 cells8/9, '
 'four actual author checkpoints,106 original nested binding records, all immutable prior audit/family/priority/review seals, '
 'the four exact reviewed submission files and all60 ZIP members passed. Full original replays with and without sources, '
 'both separately authored packaged backward controls, all810 actions and all90921 full records passed literal output comparisons. '
 'Only each dynamically validated independent timestamp was substituted for the archived timestamp; all other bytes matched. '
 'All complete mathematical outputs and negative-control failures are retained losslessly.\n\n'
 'Fresh source retrieval followed the earlier source/math/code gates and establishes byte refresh, not a new source-first chronology. '
 'The obsolete Numdam item route is recorded as historical metadata; the current article PDF freshly retrieved has the exact historical binding.\n\n'
 'This audit checks the fixed positive standard-generator theorem under both equivalence conventions. '
 'It certifies neither historical novelty nor current openness, unrestricted geometric classification, nor external human peer review. '
 'No publication/deposit is asserted. No candidate, Git, remote service or other person was modified or contacted. '
 'The original127-file public audit and its seals remain unchanged.\n\n'
 'The first live checker attempt failed on manifest-relative path resolution and received no acceptance credit. '
 'All144 complete failed-attempt captures, its full traceback and the exact sealed checker sources are preserved in failed_attempt_01. '
 'The additive checker was corrected and resealed before this successful complete rerun.\n')
sealed=[D/'FINAL_REPORT.md',D/'CODE_READY_SEAL.json']+sorted((D/'receipts').glob('*'))
write(D/'FINAL_SEAL.json',{'utc':datetime.now(timezone.utc).isoformat(),'status':r['status'],'workflow_completion_percent':100,
 'original_discovery_completion_percent':0,'head':r['head'],'base':r['base'],'sealed_artifacts':[row(p) for p in sealed]})
files=[p for p in D.rglob('*') if p.is_file() and p.name!='PUBLIC_MANIFEST.json'
       and not any(part in {'private_runtime','__pycache__','post_merge'} for part in p.relative_to(D).parts)]
write(D/'PUBLIC_MANIFEST.json',{'utc':datetime.now(timezone.utc).isoformat(),'self_excluded':True,'files':[row(p) for p in sorted(files)]})
