"""Authenticate the frozen checkpoint as data; never invoke its helpers."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
R = P / 'verification/checkpoint-pentagon-pass145-20261117'
OUT = P / 'verification/root-checkpoint-bbfb-adoption-20261117.json'
assert not OUT.exists()
pins = {
    'FINAL.json': (721, 'dc1f8986f7672fdcf015b5522e57e9dbb80db9396bd53b268f6c25453c6899ee'),
    'REPORT.md': (1983, 'c934c0cf6d08b7dae8414b2c1ad805afc2db26904028b273f36479521aeb79f3'),
    'MANIFEST.json': (12966, '27f1346db14f543ecb3136772a672f98431be7eaab0bd26e0f81e6baf6465f11'),
    'FINAL_CHECKS.json': (18761, 'bcef878d1af8126aaefbf62388efe30509fa4a861ebf594f358f3a7817046934'),
}
sha = lambda b: hashlib.sha256(b).hexdigest()
for name, expected in pins.items():
    raw = (R / name).read_bytes()
    assert (len(raw), sha(raw)) == expected, name
manifest = json.loads((R / 'MANIFEST.json').read_bytes())
files = sorted(x.relative_to(R).as_posix() for x in R.rglob('*') if x.is_file())
assert len(files) == manifest['regular_files'] == 56
assert not any(x.is_dir() for x in R.rglob('*'))
assert stat.S_IMODE(R.stat().st_mode) == int(manifest['root_mode'], 8)
terminals = {x['path']: x for x in manifest['terminal_controls']}
assert set(terminals) == {'MANIFEST.json', 'FINAL.json'}
assert set(manifest['exact_already_created_terminal_recursive_hash_exclusions']) == {str(R / x) for x in terminals}
rows = manifest['payload_files']
assert len(rows) == 54 and len({x['path'] for x in rows}) == 54
assert set(files) == {x['path'] for x in rows} | set(terminals)
for row in rows:
    path = R / row['path']
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode), row['path']
    raw = path.read_bytes()
    assert (len(raw), sha(raw), stat.S_IMODE(info.st_mode)) == (row['bytes'], row['SHA256'], int(row['mode'], 8)), row['path']
    assert (not raw) == row['empty']
    assert any(x.startswith('.') for x in Path(row['path']).parts) == row['hidden']
for name, row in terminals.items():
    assert stat.S_ISREG((R / name).lstat().st_mode)
    assert stat.S_IMODE((R / name).stat().st_mode) == int(row['mode'], 8)
final = json.loads((R / 'FINAL.json').read_bytes())
checks = json.loads((R / 'FINAL_CHECKS.json').read_bytes())
commit = 'bbfb7abf5c56e3f8d090e125784ff357138076fb'
assert final['commit'] == checks['commit'] == commit
assert final['parent'] == checks['parent'] == 'b510aecb1a5ad89bc0efa0e2798aefa9f7a928c6'
assert final['tree'] == checks['tree'] == '9292edc3ce873cf8ecc809ba2f7e88fc4b324817'
assert checks['changed_paths'] == 224 and checks['status_counts'] == {'M': 4, 'A': 220}
assert checks['dry_push_exits'] == [0, 0]
assert len(checks['all_wrapper_runs']) == 6 and all(x['exit_code'] == 0 for x in checks['all_wrapper_runs'])
assert checks['all_159_untargeted_root_siblings_and_docs_exact'] and checks['whole_public_bytes_modes_topology_exact']
assert checks['complete_durable_packet_source_closures'] == 64 and checks['key_actual_file_identities'] == 175
assert (checks['scientific_reviewed'], checks['native_Sheet_reviewed'], checks['scientific_remaining']) == (145, 144, 58)
record = {'UTC': datetime.now(timezone.utc).isoformat(), 'status': 'ACCEPTED_SCOPED_CHECKPOINT',
          'commit': commit, 'parent': final['parent'], 'tree': final['tree'],
          'packet_files': 56, 'all_payload_bytes_individual_modes_and_terminal_controls_exact': True,
          'actual_FINAL_REPORT_and_full_FINAL_CHECKS_personally_read': True,
          'six_runs_exit0': True, 'changed_paths': 224, 'durable_closures': 64, 'keys': 175,
          'untargeted_siblings': 159, 'nativeM_W_public_unchanged_in_checkpoint': True,
          'scientific145_native144_distinguished': True, 'programme_complete': False,
          'external_control_pins': {name: {'bytes': n, 'SHA256': h} for name, (n, h) in pins.items()},
          'no_helper_scientific_Git_or_network_execution_by_this_reader': True}
OUT.write_text(json.dumps(record, indent=2) + '\n')
raw = OUT.read_bytes()
print(json.dumps({'status': record['status'], 'files_authenticated': 56, 'adoption': str(OUT), 'bytes': len(raw), 'SHA256': sha(raw)}))
