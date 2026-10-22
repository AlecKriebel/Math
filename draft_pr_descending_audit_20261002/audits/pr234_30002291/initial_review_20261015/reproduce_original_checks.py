"""Execute unchanged original programs in isolated owned folders, then compare."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json
import shutil
import subprocess

D=Path(__file__).resolve().parent
S=D/'submitted/unsolved_math_prioritization/attempts/30002291'
W=D/'root_reproduction';W.mkdir(exist_ok=False)
PY=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/reproduction_environment/bin/python')
assert PY.is_file()
intake=json.loads((D/'INTAKE.json').read_text())
def validate_native():
    for row in intake['original_source_files']:
        path=D/'submitted'/row['native_path'];raw=path.read_bytes()
        assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
        assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==row['native_blob']
validate_native()
for base,filename in [(S,'FROZEN_MANIFEST.json'),(S/'independent_review','REVIEW_MANIFEST.json')]:
    for name,digest in json.loads((base/filename).read_text())['files'].items():
        assert hashlib.sha256((base/name).read_bytes()).hexdigest()==digest
cases=[('author','checks/verify_exact.py','checks/EXACT_CHECKS.json'),
       ('inherited_independent','independent_review/independent_checks.py','independent_review/INDEPENDENT_CHECKS.json')]
results=[]
for label,script,expected in cases:
    out=W/label;out.mkdir()
    code=out/Path(script).name;shutil.copy2(S/script,code)
    raw=(S/script).read_bytes();assert code.read_bytes()==raw
    run=subprocess.run([str(PY),'-I','-B',str(code)],cwd=out,capture_output=True,timeout=60)
    (out/'stdout.json').write_bytes(run.stdout);(out/'stderr.txt').write_bytes(run.stderr)
    assert run.returncode==0 and not run.stderr
    assert run.stdout==(S/expected).read_bytes()
    result=json.loads(run.stdout);assert result['status']=='PASS'
    results.append(dict(label=label,exact_assertions=result['exact_assertions'],stdout_byte_identical=True,
                        source_sha256=hashlib.sha256(raw).hexdigest(),stdout_sha256=hashlib.sha256(run.stdout).hexdigest()))
validate_native()
version=subprocess.run([str(PY),'-c','import sys,sympy;print(sys.version);print(sympy.__version__)'],capture_output=True,check=True)
(W/'runtime.txt').write_bytes(version.stdout)
receipt=dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS',runtime=str(PY),
             unchanged_native_files_verified=len(intake['original_source_files']),
             author_manifest_pins=9,inherited_review_manifest_pins=6,actual_replays=results,
             total_exact_assertions=sum(row['exact_assertions'] for row in results),
             scope='Finite identity checks only; no stochastic limit theorem proved by computation')
(D/'ROOT_ORIGINAL_REPLAY_ACCEPTANCE.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
