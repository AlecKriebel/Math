#!/usr/bin/env python3
"""Verify package scope and metadata, never the uninspected analytic theorem."""
from pathlib import Path
import hashlib,json,subprocess,sys
R=Path(__file__).resolve().parent

def must(condition,message):
    if not condition: raise RuntimeError(message)

def digest(path):
    b=path.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def scoped_manifest(root,filename,entries):
    must({p.name for p in root.iterdir() if p.is_file()}==set(entries)|{filename},
         'Scoped allowlist mismatch: '+filename)
    must(all(p.is_file() and not p.is_symlink() for p in root.iterdir()),
         'Scoped directory or symlink rejected')
    for name,declared in entries.items():must(digest(root/name)==declared,'Scoped hash mismatch: '+name)

manifest=json.loads((R/'PUBLICATION_MANIFEST.json').read_text())
paths=list(R.rglob('*'))
must(not any(p.is_symlink() for p in paths),'Symlink rejected')
actual={p.relative_to(R).as_posix() for p in paths if p.is_file()}
expected=set(manifest['files'])|{'PUBLICATION_MANIFEST.json'}
must(actual==expected,'Publication file allowlist mismatch')
must({p.relative_to(R).as_posix() for p in paths if p.is_dir()}=={'submission','independent-audit'},'Unexpected directory')
for name,entry in manifest['files'].items():must(digest(R/name)==entry,'Publication hash mismatch: '+name)
S=R/'submission';A=R/'independent-audit'
must(digest(S/'SHA256SUMS.json')['sha256']=='78c55db696e21f0c0d2d071d0b80e7745810a54fe43cdb5f7e373ee4a61cf5ad','Frozen author binding mismatch')
sm=json.loads((S/'SHA256SUMS.json').read_text());scoped_manifest(S,'SHA256SUMS.json',sm['files'])
am=json.loads((A/'AUDIT_MANIFEST.json').read_text());scoped_manifest(A,'AUDIT_MANIFEST.json',am['files'])
must(am['bound_submission_manifest_sha256']==digest(S/'SHA256SUMS.json')['sha256'],'Audit source binding mismatch')
must(am['bound_canonical_artifact_sha256']==digest(S/'LITERATURE_STATUS.md')['sha256'],'Audit artifact binding mismatch')
result=json.loads((A/'AUDIT_RESULT.json').read_text());assessment=json.loads((R/'RELEASE_ASSESSMENT.json').read_text())
must(assessment['audit_manifest_sha256']==digest(A/'AUDIT_MANIFEST.json')['sha256'],'Release audit binding mismatch')
must(assessment['campaign_turns_used']==result['campaign_turns_used']==1,'Campaign count mismatch')
must(assessment['new_proof_search_turns']==result['new_proof_search_turns']==0,'Proof-search count mismatch')
must(assessment['latest_independent_audit']==result['independent_audit']=='passed_attribution_only','Audit scope mismatch')
for key in ['full_theorem_statement_inspected','full_published_proof_inspected','complete_candidate_proof','new_mathematical_result']:
    must(assessment[key] is False and result[key] is False,'False proof certification: '+key)
normal=subprocess.check_output([sys.executable,str(S/'verify.py')])
optimized=subprocess.check_output([sys.executable,'-O',str(S/'verify.py')])
must(normal==optimized==(S/'CONTROL_RESULTS.json').read_bytes(),'Author replay mismatch')
controls=json.loads(normal);must(controls['checks_passed']==6085 and controls['published_proof_certified'] is False,'Unexpected controls or theorem claim')
subprocess.check_output([sys.executable,str(S/'verify_manifest.py')])
print(json.dumps({'publication_files':len(actual),'author_files':len(sm['files'])+1,'audit_files':len(am['files'])+1,'author_controls':6085,'normal_optimized_recorded_identical':True,'campaign_turns_used':1,'new_proof_search_turns':0,'full_theorem_or_proof_certified':False,'status':'passed_attribution_only'},indent=2,sort_keys=True))
