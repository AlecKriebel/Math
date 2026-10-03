import json, stat, sys
from closure_common import F, check_external, check_row, digest

assert len(sys.argv) == 2 and len(sys.argv[1]) == 64
b = (F / 'MANIFEST.json').read_bytes()
assert digest(b) == sys.argv[1]
m = json.loads(b)
assert m['schema'] == 'pr53-independent-closed-family/v1' and m['root_approval'] is False
assert m['self'] == {'path': 'MANIFEST.json', 'sha256': 'SELF', 'mode': '0444'}
names = {r['path'] for r in m['payload_rows']} | {'MANIFEST.json'}
assert {p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file()} == names
assert {p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_dir()} == set(m['directories'])
for row in m['payload_rows']:
    check_row(F, row)
    assert row['mode'] == '0444'
assert stat.S_IMODE((F / 'MANIFEST.json').lstat().st_mode) == 0o444
for p in [F] + [F / d for d in m['directories']]:
    assert p.resolve() == p and stat.S_IMODE(p.lstat().st_mode) == 0o555
n = check_external()
assert n == m['external_rows_checked']
print(json.dumps({'status': 'PASS', 'manifest_sha256': digest(b), 'family_files': len(names),
                  'directories': len(m['directories']), 'external_rows': n,
                  'read_only': True, 'root_approval': False}, indent=2))
