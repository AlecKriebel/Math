"""Standard-library frozen-candidate replay with complete per-checker receipts.
Reads the private copy only; never writes candidate snapshot or repository state.
"""
import hashlib,json,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parent
COPY=ROOT.parent/'private'/'author_copy'
records=[]
for name in ['REPLAY_ALL.py','gaussian_matrix.py','hessian_certificate.py',*[f'verify_turn{t}.py' for t in range(1,6)],'verify_review.py']:
    b=(COPY/name).read_bytes()
    records.append({'path':name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
replays=[]
for t in range(1,6):
    p=subprocess.run([sys.executable,str(COPY/f'verify_turn{t}.py')],cwd=COPY,capture_output=True)
    (ROOT/f'author_turn{t}_stdout.json').write_bytes(p.stdout)
    (ROOT/f'author_turn{t}_stderr.txt').write_bytes(p.stderr)
    same=p.stdout==(COPY/f'TURN_{t}_CHECKS.json').read_bytes()
    replays.append({'turn':t,'returncode':p.returncode,'stdout_exact_match':same,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_bytes':len(p.stderr)})
    assert p.returncode==0 and same and not p.stderr,replays[-1]
p=subprocess.run([sys.executable,str(COPY/'hessian_certificate.py')],cwd=COPY,capture_output=True)
(ROOT/'author_full_hessian_certificate_stdout.json').write_bytes(p.stdout)
(ROOT/'author_full_hessian_certificate_stderr.txt').write_bytes(p.stderr)
assert p.returncode==0 and not p.stderr
assert json.loads(p.stdout)==json.loads((COPY/'TURN_4_CERTIFICATE.json').read_bytes())
print(json.dumps({'python':sys.version,'executables':records,'turn_receipts':replays,'full_hessian_certificate_returncode':p.returncode,'full_hessian_certificate_sha256':hashlib.sha256(p.stdout).hexdigest(),'scope':'Author controls reproduced independently in ignored private copy; no all-size conclusion inferred.'},indent=2,sort_keys=True))
