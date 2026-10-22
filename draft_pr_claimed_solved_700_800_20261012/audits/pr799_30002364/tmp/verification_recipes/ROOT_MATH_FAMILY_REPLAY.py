from pathlib import Path
import datetime, hashlib, json, os, shutil, stat, subprocess, sys
T = Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr799_30002364/tmp')
M = T / 'root-receipts'
specs = [
    ('math_cm_hodge', 'sealed', 'verify_bundle.py',
     'a2806da4b642a30c304e78aac91b986375e98ea837c5fc97cfca6a3112eb0e4a',
     '91cee94a55310b98734c3a7b82bc2a719d3ebfd06c5eaf388e69ba9807461bbc', 9),
    ('math_frobenius', 'packet', 'verify_packet.py',
     'a65dadc0e0bb1c54d500a09be2b1d9eb59b6b642a0dee6d05e72e7f0bcee5802',
     'cd30f5265ec0da96116c9a78a036abde57321fc878882a610fb66310ce45083f', 13),
]
records = []
for family, folder, checker, mp, cp, count in specs:
    packet = T / family / folder
    assert hashlib.sha256((packet / 'MANIFEST.json').read_bytes()).hexdigest() == mp
    assert hashlib.sha256((packet / checker).read_bytes()).hexdigest() == cp
    entries = json.loads((packet / 'MANIFEST.json').read_text())['files']
    wanted = set(entries) | {'MANIFEST.json', checker}
    assert len(wanted) == count and {p.name for p in packet.iterdir()} == wanted
    for p in packet.iterdir():
        assert stat.S_ISREG(p.lstat().st_mode) and not p.is_symlink() and p.stat().st_nlink == 1
        if p.name in entries:
            r = entries[p.name]
            raw = p.read_bytes()
            assert len(raw) == r['bytes'] and hashlib.sha256(raw).hexdigest() == r['sha256']
    before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in packet.iterdir()}
    runs = []
    for py in [sys.executable, '/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3']:
        for optimized in [False, True]:
            cmd = [py, '-I', '-S', '-B'] + (['-O'] if optimized else []) + [str(packet / checker), str(packet), mp, cp]
            r = subprocess.run(cmd, cwd='/', capture_output=True, text=True, timeout=120)
            if r.returncode or r.stderr:
                raise RuntimeError(r.stdout + r.stderr)
            result = json.loads(r.stdout)
            if family == 'math_cm_hodge':
                assert result['integrity'] == result['finite']['result'] == 'PASS'
            else:
                assert result['arithmetic'] == 'PASS' and result['authenticated_inventory'] == 13 and result['optimized'] is optimized
            runs.append({'python': py, 'optimized': optimized, 'stdout_sha256': hashlib.sha256(r.stdout.encode()).hexdigest(), 'result': result})
    if family == 'math_cm_hodge':
        owner = T / 'root-cm-family-controls'
        assert not owner.exists(), 'Use a fresh disposable control copy'
        owner.mkdir()
        (owner / 'excluded_scratch').mkdir()
        shutil.copytree(packet, owner / 'sealed', copy_function=shutil.copyfile)
        runner = T / family / 'validate_sealed.py'
        shutil.copyfile(runner, owner / runner.name)
        r = subprocess.run([sys.executable, '-I', '-S', '-B', str(owner / runner.name)], cwd='/', capture_output=True, text=True, timeout=180)
        if r.returncode or r.stderr:
            raise RuntimeError(r.stdout + r.stderr)
        c = json.loads((owner / 'VALIDATION_RECEIPT.json').read_text())
        assert len(c['controls']) == 13 and all(x['pass'] is True for x in c['controls'])
        assert c['hostile_payload_executed'] is False and c['normal_optimized_equal'] is True
        controls = {'count': 13, 'positive': 4, 'negative': 9, 'result': 'PASS',
                    'original_runner_sha256': hashlib.sha256(runner.read_bytes()).hexdigest(),
                    'unchanged_runner_in_root_owned_copy': True}
        (M / 'ROOT_CM_FAMILY_CONTROLS.json').write_text(json.dumps(c, indent=2) + '\n')
    else:
        runner = packet / 'test_packet.py'
        r = subprocess.run([sys.executable, '-I', '-S', '-B', str(runner), str(packet), mp, cp], cwd='/',
                           env=dict(os.environ, TMPDIR=str(T / 'owned-runtime-tmp')), capture_output=True, text=True, timeout=180)
        if r.returncode or r.stderr:
            raise RuntimeError(r.stdout + r.stderr)
        c = json.loads(r.stdout)
        assert c['control_count'] == 17 and c['all_expected'] is True and c['untrusted_marker_executed'] is False
        assert all(x['expected_pass'] is x['actual_pass'] for x in c['controls'])
        controls = {'count': 17, 'positive': 3, 'negative': 14, 'result': 'PASS', 'mathematical_mutations_under_fresh_fixture_manifest': 2}
        (M / 'ROOT_FROBENIUS_FAMILY_CONTROLS.json').write_text(r.stdout)
    assert before == {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in packet.iterdir()}
    records.append({'family': family, 'packet': packet.relative_to(T).as_posix(), 'manifest_sha256': mp,
                    'checker': checker, 'checker_sha256': cp, 'closed_files': count,
                    'baseline_modes': runs, 'controls': controls, 'original_bundle_unchanged': True})
rec = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'result': 'PASS',
       'fresh_independent_math_families': 2, 'records': records,
       'root_read_full_reports_code_source_and_reading_scope_ledgers': True,
       'current_primary_scope_in_separate_root_reading_receipt': True,
       'finite_diagnostics_not_formal_geometric_proof': True,
       'new_substantive_proof_turns': 0, 'original_budget': '5/5'}
(M / 'ROOT_MATH_FAMILY_REPLAYS.json').write_text(json.dumps(rec, indent=2) + '\n')
print(json.dumps({'result': 'PASS', 'families': 2, 'baseline_executions': 8,
                  'CM_controls': 13, 'Frobenius_controls': 17, 'remaining_math_issues': 0}))
