#!/usr/bin/env python3
"""Strict immutable publication binding and portable exact replay. No network."""
from pathlib import Path
import hashlib,json,subprocess,sys
R=Path(__file__).resolve().parent
AUTHOR='d12fd724d5a5b5f27024b14eea46ff9402139a793fe2636c7f0985a5fc4e8403'

def must(x,msg):
    if not x:raise RuntimeError(msg)
def digest(p):
    b=p.read_bytes();return {'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def run(p):
    return json.loads(subprocess.check_output([sys.executable,str(p)],cwd=p.parent,text=True))
def scoped(root,manifest):
    expected=set(manifest['files'])|{'SHA256SUMS.json'}
    must({p.name for p in root.iterdir()}==expected,'Scoped inventory mismatch')
    must(all(p.is_file() and not p.is_symlink() for p in root.iterdir()),'Scoped non-file')
    for name,entry in manifest['files'].items():must(digest(root/name)==entry,'Scoped byte binding: '+name)

manifest=json.loads((R/'PUBLICATION_MANIFEST.json').read_text())
paths=list(R.rglob('*'))
must(not any(p.is_symlink() for p in paths),'Symlink rejected')
actual={p.relative_to(R).as_posix() for p in paths if p.is_file()}
must(actual==set(manifest['files'])|{'PUBLICATION_MANIFEST.json'},'Publication file allowlist mismatch')
must({p.relative_to(R).as_posix() for p in paths if p.is_dir()}=={'submission','independent-audit'},'Publication directory allowlist mismatch')
for name,entry in manifest['files'].items():
    p=R/name;must(p.resolve().is_relative_to(R),'Path escaped root')
    must(digest(p)==entry,'Publication byte binding: '+name)
S=R/'submission';A=R/'independent-audit'
sm=json.loads((S/'SHA256SUMS.json').read_text());am=json.loads((A/'SHA256SUMS.json').read_text())
scoped(S,sm);scoped(A,am)
must(digest(S/'SHA256SUMS.json')['sha256']==AUTHOR,'Frozen author manifest changed')
bound=json.loads((A/'INPUT_BINDING.json').read_text())
must(bound['manifest_file']==digest(S/'SHA256SUMS.json') and bound['manifest_contents']==sm,'Audit input binding mismatch')
must(am['bound_author_manifest_sha256']==AUTHOR,'Audit author binding mismatch')
assessment=json.loads((R/'RELEASE_ASSESSMENT.json').read_text());audit=json.loads((A/'AUDIT.json').read_text())
must(assessment['audit_manifest_sha256']==digest(A/'SHA256SUMS.json')['sha256'],'Frozen audit binding mismatch')
must(assessment['status']==audit['accepted_status']=='already_solved','Classification mismatch')
must(assessment['campaign_turns_used']==5 and assessment['new_mathematical_result'] is False,'Accounting/novelty mismatch')
must(audit['verdict']=='pass' and not audit['blocking_findings'],'Audit did not pass')
author=run(S/'verify.py');independent=run(A/'independent_checks.py')
must(author==json.loads((S/'CONTROL_RESULTS.json').read_text())==json.loads((A/'AUTHOR_REPLAY_RESULTS.json').read_text()),'Author replay mismatch')
must(independent==json.loads((A/'INDEPENDENT_RESULTS.json').read_text()),'Independent replay mismatch')
must(author['assertions']==1980 and independent['assertions']==1067,'Unexpected check counts')
replay=run(A/'verify_audit.py')
must(replay['passed'] and replay['author_assertions']==1980 and replay['independent_assertions']==1067,'Audit replay mismatch')
print(json.dumps({'passed':True,'publication_files':len(actual),'author_files':len(sm['files'])+1,'audit_files':len(am['files'])+1,'author_assertions':1980,'independent_assertions':1067,'audit_replayed':True,'status':'already_solved','scope':'formal scalar algebraic; no novelty, minimality, analytic or full-center claim'},indent=2))
