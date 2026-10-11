"""One actual replay of each immutable submitted checker, with whole receipts."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, stat, subprocess, sys

A = Path(__file__).resolve().parent
S = A / 'snapshot'
D = A / 'root_replay_private/submitted_001'
utc = lambda: datetime.now(timezone.utc).isoformat()
sha = lambda b: hashlib.sha256(b).hexdigest()
m = json.loads((A / 'snapshot_manifest.json').read_bytes())
Q = S / 'problems/30005649_qss_self_duality'
def pin(p):
    st = p.lstat()
    assert stat.S_ISREG(st.st_mode), p
    b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'sha256': sha(b),
            'mode': stat.S_IMODE(st.st_mode)}
def snapshot():
    out = {str(p.relative_to(S)): pin(p) for p in sorted(S.rglob('*')) if p.is_file()}
    assert set(out) == {e['path'] for e in m['files']}
    for e in m['files']:
        v = out[e['path']]
        assert (v['bytes'], v['sha256'], v['mode']) == (e['bytes'], e['sha256'], 0o644)
    return out
before = snapshot()
author = json.loads((Q / 'FINAL_AUTHOR_MANIFEST.json').read_bytes())
publication = json.loads((Q / 'PUBLICATION_MANIFEST.json').read_bytes())
review = json.loads((Q / 'review/REVIEW_MANIFEST.json').read_bytes())
for name, digest in author['files'].items():
    assert name in {str(p.relative_to(Q)) for p in Q.rglob('*') if p.is_file()}
    assert sha((Q / name).read_bytes()) == digest
for name, digest in publication['files'].items():
    assert sha((Q / name).read_bytes()) == digest
for entry in review['files']:
    b = (Q / 'review' / entry['path']).read_bytes()
    assert len(b) == entry['bytes'] and sha(b) == entry['sha256']
assert len(author['files']) == 6 and len(publication['files']) == 14 and len(review['files']) == 5
sources = [A / 'root_sources_private' / n for n in
           ['owr2023-42.pdf', 'hoshi2021-revised.pdf', 'hoshi2021-revised.txt']]
source_before = [pin(p) for p in sources]
source_claims = json.loads((Q / 'SOURCE_HASHES.json').read_bytes())
for old, p in zip(['sources/owr.pdf', 'sources/hoshi2021.pdf', 'sources/hoshi2021.txt'], sources):
    assert sha(p.read_bytes()) == source_claims[old]
jobs = [('author', Q / 'turn1/check_module.py', Q / 'turn1/verification.json'),
        ('prior_reviewer', Q / 'review/independent_checks.py', Q / 'review/INDEPENDENT_CHECKS.json')]
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0')
pre = {'started_utc': utc(), 'runner': pin(Path(__file__)),
       'interpreter_requested': sys.executable, 'interpreter_resolved': str(Path(sys.executable).resolve()),
       'python_version': sys.version, 'snapshot_before': before,
       'sources_before': source_before,
       'jobs': [{'name': name, 'argv': [sys.executable, '-B', str(code)],
                 'cwd': str(Q), 'code': pin(code), 'expected_stdout': pin(expected)}
                for name, code, expected in jobs],
       'environment_overrides': {'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONHASHSEED': '0'}}
D.mkdir(parents=True, exist_ok=False)
(D / 'preexecution.json').write_text(json.dumps(pre, indent=2) + '\n')
results = []
for name, code, expected in jobs:
    argv = [sys.executable, '-B', str(code)]
    start = utc()
    r = subprocess.run(argv, cwd=Q, env=env, capture_output=True)
    (D / (name + '.stdout')).write_bytes(r.stdout)
    (D / (name + '.stderr')).write_bytes(r.stderr)
    rec = {'name': name, 'argv': argv, 'cwd': str(Q), 'started_utc': start,
           'finished_utc': utc(), 'exit_code': r.returncode,
           'stdout_bytes': len(r.stdout), 'stdout_sha256': sha(r.stdout),
           'stderr_bytes': len(r.stderr), 'stderr_sha256': sha(r.stderr),
           'whole_stdout_expected_equal': r.stdout == expected.read_bytes(),
           'code_unchanged': pin(code) == next(j['code'] for j in pre['jobs'] if j['name'] == name),
           'expected_unchanged': pin(expected) == next(j['expected_stdout'] for j in pre['jobs'] if j['name'] == name)}
    (D / (name + '.json')).write_text(json.dumps(rec, indent=2) + '\n')
    results.append(rec)
    assert r.returncode == 0 and not r.stderr and rec['whole_stdout_expected_equal']
    assert rec['code_unchanged'] and rec['expected_unchanged']
after = snapshot()
assert after == before and [pin(p) for p in sources] == source_before
record = {'finished_utc': utc(), 'status': 'PASS_COMPLETE_SUBMITTED_MANIFESTS_AND_TWO_WHOLE_NATIVE_REPLAYS',
          'pr': 344, 'head': m['head'], 'all_16_snapshot_files_unchanged': True,
          'all_manifest_payloads_verified': {'author': 6, 'publication': 14, 'review': 5},
          'historical_source_hashes_reproduced': ['sources/owr.pdf', 'sources/hoshi2021.pdf', 'sources/hoshi2021.txt'],
          'other_historical_source_hashes_not_reproduced': sorted(set(source_claims) -
              {'sources/owr.pdf', 'sources/hoshi2021.pdf', 'sources/hoshi2021.txt'}),
          'owr_layout_text_is_new_extraction_not_claimed_equal_to_historical_text': True,
          'author_assertions': json.loads((D / 'author.stdout').read_bytes())['assertions'],
          'prior_reviewer_assertions': json.loads((D / 'prior_reviewer.stdout').read_bytes())['independent_exact_assertions'],
          'native_capture_directory': str(D), 'preexecution_sha256': sha((D / 'preexecution.json').read_bytes()),
          'runner_sha256': sha(Path(__file__).read_bytes()), 'results': results,
          'scope': 'Actual reproduction and integrity; universal proof and foundational classification are separate mathematical gates.'}
(A / 'ROOT_SUBMITTED_REPRODUCTION.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
