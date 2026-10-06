#!/usr/bin/env python3
"""Post-verdict corroboration only; execute frozen copies inside ignored own tmp."""
from pathlib import Path
import hashlib,json,subprocess,datetime
OWN=Path(__file__).absolute().parent
SOURCE=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr374_30005116/snapshot/problems/30005116_induced_four_cycle_profile')
MANIFEST=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr374_30005116/snapshot_manifest.json')
RUNTIME='/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
COPY=OWN/'tmp'/'author_replay'
COPY.mkdir(parents=True,exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
manifest=json.loads(MANIFEST.read_bytes())
expected={Path(v['path']).name:v for v in manifest['files'] if '/independent_review/' not in v['path']}
assert manifest['head']=='c683fc4b84266a6a153c087e182cf427ed502d6c'
results=[]
for turn in (2,3,5):
    script=f'verify_turn{turn}.py';receipt=f'TURN_{turn}_CHECKS.json'
    for name in (script,receipt,f'TURN_{turn}.md'):
        data=(SOURCE/name).read_bytes()
        assert sha(data)==expected[name]['sha256'],name
        if name in (script,receipt): (COPY/name).write_bytes(data)
    assert (COPY/script).read_bytes()==(SOURCE/script).read_bytes()
    assert (COPY/receipt).read_bytes()==(SOURCE/receipt).read_bytes()
    run=subprocess.run([RUNTIME,'-B',str(COPY/script)],cwd=COPY,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (OWN/f'author_turn{turn}.stdout.fullstream.txt').write_bytes(run.stdout)
    (OWN/f'author_turn{turn}.stderr.fullstream.txt').write_bytes(run.stderr)
    byte_match=run.stdout==(SOURCE/receipt).read_bytes()
    result={'turn':turn,'exit_code':run.returncode,'stdout_sha256':sha(run.stdout),'stderr_sha256':sha(run.stderr),'expected_sha256':sha((SOURCE/receipt).read_bytes()),'byte_match':byte_match,'assertions':json.loads(run.stdout)['assertions'] if run.returncode==0 else None,'script_sha256':sha((SOURCE/script).read_bytes()),'proof_sha256':sha((SOURCE/f'TURN_{turn}.md').read_bytes())}
    results.append(result)
    assert run.returncode==0 and byte_match and not run.stderr,result
out={'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mathematical_verdict_precedes_replay':True,'role':'post-seal corroboration only, not independent proof or source binding','frozen_head':manifest['head'],'runtime_literal':RUNTIME,'snapshot_manifest_sha256':sha(MANIFEST.read_bytes()),'results':results,'total_assertions':sum(v['assertions'] for v in results)}
(OWN/'author_replay_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
