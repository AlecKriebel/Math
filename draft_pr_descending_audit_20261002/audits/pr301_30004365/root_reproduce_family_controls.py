"""Independently replay three supplementary mathematical control families."""
from pathlib import Path
from datetime import datetime, timezone
import gzip, hashlib, json, os, stat, subprocess, sys

A = Path(__file__).resolve().parent
D = A / 'root_family_reproduction'
sha = lambda b: hashlib.sha256(b).hexdigest()
utc = lambda: datetime.now(timezone.utc).isoformat()

def need(v, m):
    if not v:
        raise RuntimeError(m)

def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return dict(path=str(p), bytes=len(b), sha256=sha(b), mode=stat.S_IMODE(p.stat().st_mode))

def main():
    need(not sys.flags.optimize, 'assertions enabled')
    D.mkdir(exist_ok=False)
    original = json.loads((A / 'snapshot_manifest.json').read_bytes())
    for row in original['files']:
        need(pin(row['snapshot']['path'])['sha256'] == row['snapshot']['sha256'], 'immutable original')
    families = [
        ('surface_construction_adversary_01', 'surface_fixture_audit.py', 'surface_fixture_results.json'),
        ('effectivity_termination_adversary_01', 'exact_edge_controls.py', 'EXACT_EDGE_CONTROLS.json'),
        ('classification_invariant_adversary_01', 'check_classification.py', 'CONTROL_RESULTS.json'),
    ]
    results = []
    for family, name, result_name in families:
        q = D / family
        q.mkdir()
        source = q / name
        source.write_bytes((A / family / name).read_bytes())
        source.chmod(0o444)
        (q / 'source.gz').write_bytes(gzip.compress(source.read_bytes(), mtime=0))
        expected = A / family / result_name
        request = dict(argv=['/opt/homebrew/bin/python3', '-E', '-B', str(source)], cwd=str(q),
                       UTC=utc(), recorder=pin(__file__), source=pin(source),
                       original_source=pin(A / family / name), expected=pin(expected),
                       interpreter=pin(Path('/opt/homebrew/bin/python3').resolve()), automatic_retry=False)
        (q / 'request.json').write_text(json.dumps(request, indent=2) + '\n')
        (q / 'recorder.gz').write_bytes(gzip.compress(Path(__file__).read_bytes(), mtime=0))
        child = subprocess.Popen(request['argv'], cwd=q, stdin=subprocess.DEVNULL,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
        started = dict(actual_PID=child.pid, start_UTC=utc())
        (q / 'started.json').write_text(json.dumps(started, indent=2) + '\n')
        out, err = child.communicate(timeout=55)
        streams = {}
        for label, body in [('stdout', out), ('stderr', err)]:
            path = q / (label + '.gz')
            path.write_bytes(gzip.compress(body, mtime=0))
            streams[label] = dict(stored=pin(path), logical_bytes=len(body), logical_sha256=sha(body))
        record = dict(**started, end_UTC=utc(), exit_code=child.returncode,
                      parent_reaped=True, request=pin(q / 'request.json'), streams=streams)
        (q / 'execution.json').write_text(json.dumps(record, indent=2) + '\n')
        need(child.returncode == 0 and not err, 'actual mathematical controls succeeded')
        actual = q / result_name
        need(json.loads(actual.read_bytes()) == json.loads(expected.read_bytes()), 'full result equality')
        need(source.read_bytes() == (A / family / name).read_bytes(), 'source unchanged')
        results.append(dict(family=family, actual_PID=child.pid, execution=pin(q / 'execution.json'),
                            output=pin(actual), expected=pin(expected), full_JSON_equality=True))
    for row in original['files']:
        need(pin(row['snapshot']['path'])['sha256'] == row['snapshot']['sha256'], 'original unchanged after runs')
    report = dict(status='PASS_ROOT_REPRODUCES_THREE_INDEPENDENT_FINITE_FAMILIES', UTC=utc(),
                  actual_recorder_PID=os.getpid(), source=pin(__file__), original_head=original['head'],
                  results=results, universal_proof_or_full_algorithm_implementation=False,
                  classification_correction_and_primary_theorem_review_separately_required=True)
    target = A / 'ROOT_FAMILY_CONTROLS_REPRODUCTION.json'
    target.write_text(json.dumps(report, indent=2) + '\n')
    target.chmod(0o444)
    print(json.dumps(dict(status=report['status'], actual_recorder_PID=os.getpid(), result=pin(target)), indent=2))

if __name__ == '__main__':
    main()
