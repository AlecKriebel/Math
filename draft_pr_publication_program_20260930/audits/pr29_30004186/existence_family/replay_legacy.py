#!/usr/bin/env python3
"""Run byte-identical legacy scripts only in ignored isolated subdirectories."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'source_snapshot'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
before={str(p.relative_to(SOURCE)):sha(p) for p in SOURCE.rglob('*') if p.is_file()}
jobs=[('submitted_original','check_identities.py','check_results.json'),
      ('old_independent','independent_review/independent_checks.py','independent_review/independent_results.json'),
      ('old_submitted_copy','independent_review/submitted_check_identities.py','independent_review/submitted_results.json')]
rows=[]
for name,script,receipt in jobs:
    dest=HERE/'ignoredtmp'/name
    dest.mkdir(parents=True,exist_ok=True)
    copied=dest/Path(script).name
    shutil.copyfile(SOURCE/script,copied)
    expected_sha=sha(SOURCE/script)
    assert sha(copied)==expected_sha
    run=subprocess.run(['/usr/bin/python3',str(copied)],cwd=dest,capture_output=True,text=True,timeout=60)
    (dest/'stdout.json').write_text(run.stdout)
    (dest/'stderr.txt').write_text(run.stderr)
    assert run.returncode==0,(name,run.stderr)
    produced=json.loads(run.stdout)
    frozen=json.loads((SOURCE/receipt).read_text())
    assert produced==frozen,name
    assert sha(copied)==expected_sha
    output_file=copied.with_name('check_results.json')
    file_match=None
    if name!='old_independent':
        assert output_file.read_bytes()==(SOURCE/receipt).read_bytes()
        file_match=True
    rows.append({'name':name,'script':script,'script_sha256':expected_sha,
                 'command':['/usr/bin/python3',str(copied)],'returncode':run.returncode,
                 'sympy_version':produced['sympy_version'],
                 'assertions':produced.get('assertions',produced.get('passed')),
                 'frozen_receipt_semantically_equal':True,'written_receipt_byte_equal':file_match,
                 'stdout_file':str((dest/'stdout.json').relative_to(HERE)),
                 'stderr_file':str((dest/'stderr.txt').relative_to(HERE)),
                 'stdout_sha256':hashlib.sha256(run.stdout.encode()).hexdigest(),
                 'scope':'Legacy exact finite identity/scale controls only; does not prove Banach existence or PDE departure.'})
after={str(p.relative_to(SOURCE)):sha(p) for p in SOURCE.rglob('*') if p.is_file()}
assert after==before
result={'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),
        'replays':rows,'original_snapshot_file_count':len(before),
        'original_snapshots_unchanged_before_after':True,
        'snapshot_hashes':before,'isolated_replay_root':'ignoredtmp/',
        'no_original_receipt_execution_or_rewrite':True,
        'script_sha256':sha(Path(__file__))}
(HERE/'REPLAY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='snapshot_hashes'},indent=2))
