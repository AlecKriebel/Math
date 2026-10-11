"""Replay a reviewed checker in a disposable clone, preserving its closed originals."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil, subprocess
A = Path(__file__).resolve().parent
F = A / 'priority_correction_review'
sha = lambda b: hashlib.sha256(b).hexdigest()
P = A / 'correction_review_replay_private'
P.mkdir(exist_ok=False)
for name in ['snapshot_manifest.json', 'PRIORITY_CORRECTION_PREPARATION.json']:
    shutil.copy2(A / name, P / name)
for name in ['snapshot', 'priority_correction_packet']:
    shutil.copytree(A / name, P / name)
O = P / 'priority_correction_review'
(O / 'executions').mkdir(parents=True)
shutil.copy2(F / 'INDEPENDENT_SOURCE_CRITERIA.md', O / 'INDEPENDENT_SOURCE_CRITERIA.md')
source = (F / 'validate_artifacts.py').read_bytes()
needle = ("root=Path('" + str(A) + "')").encode()
if source.count(needle) != 1:
    raise RuntimeError('Unexpected checker root binding')
adapted = source.replace(needle, ("root=Path('" + str(P) + "')").encode())
program = P / 'validate_artifacts_disposable.py'
program.write_bytes(adapted)
inputs = {}
for q in sorted(P.rglob('*')):
    if q.is_file():
        inputs[str(q.relative_to(P))] = dict(bytes=q.stat().st_size, sha256=sha(q.read_bytes()))
argv = ['/opt/homebrew/bin/python3', '-B', str(program)]
started = datetime.now(timezone.utc).isoformat()
spec = dict(started_utc=started, argv=argv, cwd=str(P), original_checker_sha256=sha(source),
            adapted_checker_sha256=sha(adapted),
            adaptation='Exactly one hard-coded audit-root path replaced; all scientific controls and artifact predicates byte-preserved',
            inputs=inputs)
(P / 'execution_spec.json').write_text(json.dumps(spec, indent=2) + '\n')
run = subprocess.run(argv, cwd=P, capture_output=True)
(P / 'stdout.bin').write_bytes(run.stdout)
(P / 'stderr.bin').write_bytes(run.stderr)
spec.update(ended_utc=datetime.now(timezone.utc).isoformat(), exit_code=run.returncode,
            stdout_bytes=len(run.stdout), stdout_sha256=sha(run.stdout),
            stderr_bytes=len(run.stderr), stderr_sha256=sha(run.stderr))
(P / 'execution.json').write_text(json.dumps(spec, indent=2) + '\n')
if run.returncode:
    raise RuntimeError(run.stderr.decode(errors='replace'))
for name in ['artifact_validation.json', 'author_checker.stdout', 'author_checker.stderr',
             'independent_endpoint_controls.json']:
    if (O / 'executions' / name).read_bytes() != (F / 'executions' / name).read_bytes():
        raise RuntimeError('Disposable exact replay differs: ' + name)
closed = json.loads((F / 'REVIEW_MANIFEST.json').read_bytes())
for name, expected in closed['files'].items():
    q = F / name
    if q.stat().st_size != expected['bytes'] or sha(q.read_bytes()) != expected['sha256']:
        raise RuntimeError('Closed reviewer artifact changed: ' + name)
artifact = json.loads((O / 'executions/artifact_validation.json').read_bytes())
control = json.loads((O / 'executions/independent_endpoint_controls.json').read_bytes())
receipt = dict(utc=datetime.now(timezone.utc).isoformat(),
               status='PASS_DISPOSABLE_ROOT_CORRECTION_REVIEW_REPLAY',
               adapted_one_path_only=True, scientific_code_byte_preserved=True,
               artifact_assertions=artifact['artifact_assertions'],
               author_assertions=artifact['author_output']['assertions'],
               endpoint_controls=control['exact_assertions'],
               identity_cases=control['straddling_identity_cases'],
               all_four_complete_output_artifacts_byte_identical=True,
               closed_reviewer_evidence_unchanged=True,
               original_checker_sha256=sha(source), execution=spec)
(A / 'ROOT_CORRECTION_REPLAY.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(dict(status=receipt['status'], artifact_assertions=receipt['artifact_assertions'],
                      author_assertions=receipt['author_assertions'],
                      endpoint_controls=receipt['endpoint_controls'],
                      identity_cases=receipt['identity_cases'],
                      complete_outputs_byte_identical=True,
                      closed_reviewer_evidence_unchanged=True), indent=2))
