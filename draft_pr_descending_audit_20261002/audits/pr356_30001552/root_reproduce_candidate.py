"""Whole public mathematical reproduction; do not imply missing private-source checks."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess

A = Path(__file__).resolve().parent
R = A.parents[2]
S = A / 'snapshot'
C = S / 'problems/30001552_antimorphic_periods'
D = A / 'root_replay_private/candidate_001'
D.mkdir(parents=True, exist_ok=False)
sha = lambda b: hashlib.sha256(b).hexdigest()
utc = lambda: datetime.now(timezone.utc).isoformat()
manifest = json.loads((A / 'snapshot_manifest.json').read_bytes())
def inventory():
    return {str(p.relative_to(S)): (len(p.read_bytes()), sha(p.read_bytes()), p.stat().st_mode & 0o777)
            for p in S.rglob('*') if p.is_file()}
before = inventory()
assert len(before) == 17
for e in manifest['files']:
    assert before[e['path']] == (e['bytes'], e['sha256'], 0o644)
bindings = []
for name, base in [('FINAL_AUTHOR_MANIFEST.json', C), ('PUBLICATION_MANIFEST.json', C), ('review/REVIEW_MANIFEST.json', C / 'review')]:
    j = json.loads((C / name).read_bytes())
    for path, h in j.items():
        assert sha((base / path).read_bytes()) == h
        bindings.append({'manifest': name, 'path': path, 'sha256': h})
assert len(bindings) == 25
captured = []
for label, program, expected in [('author', C / 'check_turn1.py', C / 'TURN_1_CHECKS.json'),
                                 ('portable_public', C / 'review/run_portable.py', C / 'review/PORTABLE_CHECKS.json')]:
    args = ['/opt/homebrew/bin/python3.11', '-B', str(program.resolve())]
    source_bytes = program.read_bytes()
    (D / (label + '.source.py')).write_bytes(source_bytes)
    start = utc()
    r = subprocess.run(args, cwd=R, capture_output=True)
    rec = {'argv': args, 'cwd': str(R), 'started_utc': start, 'completed_utc': utc(), 'exit_code': r.returncode,
           'source_sha256_before_execution': sha(source_bytes), 'source_unchanged_after': program.read_bytes() == source_bytes}
    for name, b in [('stdout', r.stdout), ('stderr', r.stderr)]:
        f = D / (label + '.' + name)
        f.write_bytes(b)
        rec[name + '_path'] = str(f.relative_to(A))
        rec[name + '_bytes'] = len(b)
        rec[name + '_sha256'] = sha(b)
    (D / (label + '.json')).write_text(json.dumps(rec, indent=2) + '\n')
    assert r.returncode == 0 and not r.stderr and rec['source_unchanged_after']
    assert r.stdout == expected.read_bytes(), 'Whole saved output differs'
    captured.append(rec)
assert inventory() == before
old = json.loads((C / 'review/INDEPENDENT_CHECKS.json').read_bytes())
new = json.loads((C / 'review/PORTABLE_CHECKS.json').read_bytes())
assert old['independent_assertions'] == new['independent_assertions'] + 5 == 68413
assert {k: v for k, v in old.items() if k != 'independent_assertions'} == {k: v for k, v in new.items() if k != 'independent_assertions'}
rec = {'utc': utc(), 'status': 'PASS_ENTIRE_PUBLIC_MATHEMATICAL_OUTPUTS_AND_25_NESTED_BINDINGS',
       'author_assertions': 526887, 'portable_public_independent_assertions': 68408,
       'all_17_frozen_files_unchanged': True, 'all_25_nested_public_bindings_exact': True,
       'manifest_reference_count_including_five_optional_sources': 30,
       'all_program_outputs_compared_byte_for_byte': True, 'captures': captured,
       'historical_private_source_68413_replay_performed': False,
       'historical_private_source_check_count_difference': 5,
       'historical_linux_absolute_path_reviewer_executable_not_portable': True,
       'source_hashes_are_optional_separate_binding_obligations': True,
       'local_literal_git_scope_check_still_pending': manifest['local_git_diff_and_blob_verification_pending'],
       'mathematical_proof_is_analytical_not_inferred_from_finite_counts': True,
       'program_sha256': sha(Path(__file__).read_bytes())}
(A / 'ROOT_CANDIDATE_REPLAY_RECEIPT.json').write_text(json.dumps(rec, indent=2) + '\n')
print(json.dumps({k: v for k, v in rec.items() if k != 'captures'}, indent=2))
