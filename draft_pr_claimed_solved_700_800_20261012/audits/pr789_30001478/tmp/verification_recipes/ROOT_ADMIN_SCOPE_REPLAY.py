from pathlib import Path
import datetime, hashlib, json, stat, subprocess, sys

T = Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp')
W = T / 'admin_scope'
P = W / 'packet'
M = T / 'root-receipts'
pins = json.loads((M / 'ADMIN_EXPECTED_PINS.json').read_text())
mp, cp, rp = [pins[k] for k in ['manifest_sha256', 'checker_sha256', 'runner_sha256']]
for path, pin in [(P / 'MANIFEST.json', mp), (P / 'CHECKS.py', cp), (W / 'REPLAY_PACKET_CONTROLS.py', rp)]:
    assert stat.S_ISREG(path.lstat().st_mode) and path.stat().st_nlink == 1 and not path.is_symlink()
    assert hashlib.sha256(path.read_bytes()).hexdigest() == pin
entries = json.loads((P / 'MANIFEST.json').read_text())['files']
assert len(entries) == 22 and len({x['path'] for x in entries}) == 22
assert {p.name for p in P.iterdir()} == {x['path'] for x in entries} | {'MANIFEST.json'}
for row in entries:
    p = P / row['path']
    assert p.name == row['path'] and p.is_file() and not p.is_symlink() and p.stat().st_nlink == 1
    raw = p.read_bytes()
    assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
verdict = json.loads((P / 'VERDICT.json').read_text())
assert verdict['result'] == 'PASS_ADMINISTRATIVE_CUSTODY_AND_EXACT_MERGE_SCOPE'
assert type(verdict['required_administrative_issues']) is int and verdict['required_administrative_issues'] == 0
assert verdict['actual_merge_commit'] == 'ed23ab7fb9f8cea120db982b6e39366ccddd9178'
assert verdict['approved_administrative_PR_head'] == 'eb9f6de34861610cf7355a630603a0d18a13f39a'
before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in P.iterdir()}
baselines, controls = [], []
for py in [sys.executable, '/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3']:
    for opt in [False, True]:
        flags = [py, '-I', '-B'] + (['-O'] if opt else [])
        command = flags + [str(P / 'CHECKS.py'), '--packet', str(P), '--expected-manifest-sha256', mp, '--package', str(T / 'preprint')]
        r = subprocess.run(command, cwd='/', capture_output=True, text=True, timeout=120)
        if r.returncode or r.stderr:
            raise RuntimeError(r.stdout + r.stderr)
        result = json.loads(r.stdout)
        assert result['result'] == 'PASS' and result['external_source_PDF_custody_replayed'] is True
        baselines.append({'python': py, 'optimized': opt, 'result': result})
        if py == sys.executable:
            out = W / 'scratch' / ('ROOT_FINAL_PACKET_CONTROLS_' + ('O' if opt else 'normal') + '.json')
            assert not out.exists(), 'Use a new receipt path; do not overwrite prior controls'
            command = flags + [str(W / 'REPLAY_PACKET_CONTROLS.py'), '--packet', str(P), '--expected-manifest-sha256', mp, '--package', str(T / 'preprint'), '--out', str(out)]
            r = subprocess.run(command, cwd='/', capture_output=True, text=True, timeout=180)
            if r.returncode or r.stderr:
                raise RuntimeError(r.stdout + r.stderr)
            result = json.loads(r.stdout)
            assert result['result'] == 'PASS_PACKET_REPLAY_AND_TAMPER_CONTROLS'
            assert result['controls'] == 19 and all(c['control_pass'] is True for c in result['cases'])
            assert sum(c['expected_acceptance'] is True for c in result['cases']) == 3
            assert result['all_original_packet_files_untouched'] is True
            assert result['network_or_remote_mutations'] is False
            (M / out.name).write_bytes(out.read_bytes())
            controls.append({'python': py, 'optimized': opt, 'result': result})
assert before == {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in P.iterdir()}
rec = {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'result': 'PASS',
    'manifest_sha256': mp, 'checker_sha256': cp, 'runner_sha256': rp,
    'closed_authored_files': 23, 'baselines': baselines, 'control_reproductions': controls,
    'packet_controls_each': {'positive': 3, 'negative': 16},
    'bound_administrative_control_counts': {'driver': 49, 'known_draft_repair': 40, 'public_metadata': 13, 'tracker': 18, 'Merkle': 7},
    'exact_actual_integration_two_parents_required': True,
    'remaining_actionable_issues': [],
    'administrative_scope_not_fifth_whole_review': True,
    'native_acceptance_still_pending': True,
    'source151_and_six_unchanged': True,
}
(M / 'ADMIN_SCOPE_ROOT_REPLAY.json').write_text(json.dumps(rec, indent=2) + '\n')
print(json.dumps({'result': 'PASS', 'authored_files': 23, 'baseline_modes': 4,
                  'packet_control_runs': 2, 'positive_each': 3, 'negative_each': 16,
                  'remaining_actionable_issues': 0}))
