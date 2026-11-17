from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json, stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
V = P / 'verification'
R = P / 'papers/23204176/reviews'

def obj(path):
    return json.loads(path.read_text())

def digest(path):
    return sha256(path.read_bytes()).hexdigest()

def snapshot(root):
    entries = []
    for path in [root] + sorted(root.rglob('*')):
        s = path.lstat()
        assert stat.S_ISREG(s.st_mode) or stat.S_ISDIR(s.st_mode), str(path)
        name = path.relative_to(root).as_posix()
        row = dict(path=name, kind='file' if path.is_file() else 'directory',
                   mode=oct(stat.S_IMODE(s.st_mode)),
                   hidden=any(x.startswith('.') for x in Path(name).parts if x != '.'))
        if path.is_file():
            row.update(bytes=s.st_size, SHA256=digest(path), empty=s.st_size == 0)
        else:
            row['empty'] = not any(path.iterdir())
        entries.append(row)
    return entries

def authenticate(root, expected, counts):
    actual = snapshot(root)
    indexed = {r['path']: r for r in actual}
    assert len(indexed) == len(actual)
    assert set(indexed) == {r['path'] for r in expected}, str(root)
    assert len(expected) == len(actual)
    for row in expected:
        current = indexed[row['path']]
        assert current['kind'] == row['kind'], (str(root), row['path'], 'kind')
        mode = row.get('mode', row.get('mode_octal'))
        assert current['mode'] == oct(int(mode, 8)), (str(root), row['path'], 'mode')
        if current['kind'] == 'file' and row.get('SHA256', row.get('sha256')) is not None:
            assert current['bytes'] == row['bytes']
            assert current['SHA256'] == row.get('SHA256', row.get('sha256')), (str(root), row['path'], 'bytes')
        for key, alias in [('empty', 'empty'), ('hidden', 'hidden_component')]:
            if key in row or alias in row:
                assert current[key] == row.get(key, row.get(alias)), (str(root), row['path'], key)
    observed = (sum(r['kind'] == 'file' for r in actual),
                sum(r['kind'] == 'directory' for r in actual) - 1)
    assert observed == counts, (str(root), observed, counts)
    return dict(root=str(root), files=observed[0], child_directories=observed[1],
                all_actual_bytes_modes_hidden_empty_topology_exact=True, entries=actual)

def sealed(root, manifest_name, controls, counts):
    for name, wanted in controls.items():
        assert digest(root / name) == wanted, (str(root), name, 'external control pin')
    manifest = obj(root / manifest_name)
    if 'entries' in manifest:
        rows = manifest['entries']
    else:
        rows = [dict(row, kind='file') for row in manifest['payload_files']]
        rows += [dict(row, kind='directory') for row in manifest['directories']]
        if not any(r['path'] == '.' for r in rows):
            rows.append(dict(path='.', kind='directory', mode=manifest['root_mode']))
        rows += [dict(path=name, kind='file', mode='0644',
                      bytes=(root / name).stat().st_size, SHA256=wanted)
                 for name, wanted in controls.items() if not any(r['path'] == name for r in rows)]
    rows = [dict(row, SHA256=controls[row['path']], bytes=(root / row['path']).stat().st_size)
            if row['path'] in controls else row for row in rows]
    result = authenticate(root, rows, counts)
    result['external_control_pins'] = controls
    return result

k3 = []
k3.append(sealed(R / 'scope-sol-continuation-20261117', 'FINAL_MANIFEST.json', {
    'FINAL.json': '1fe19b0ba1740dabbc4b6f00c03ba5594d8ff0b6ec4123b487060853e3b97564',
    'FINAL_MANIFEST.json': 'b3666e8926f91104e0c298751bfb57568edcc96d256b3174036f3e07a958b7b0',
    'FINAL_SEAL.json': '6a17374661feb3d770de266bb05a40be686c436431f62576bbd215fbfe36c134',
}, (1016, 38)))
k3.append(sealed(R / 'adversarial-sol-finalization-20261117', 'FINAL_MANIFEST.json', {
    'FINAL.json': '95bf6c10c426c949cc06abf7d26a4d610808948c69140b0b4fff5693d6213dea',
    'FINAL_MANIFEST.json': '0c696aafce29f8b0495c751898d94128522ff21fc8bed246c2e6a184b758a47d',
    'FINAL_SEAL.json': 'b1c1a6e79bd1813a92c01463e0402a523684218760b37c54f5666e0c6f46e9e9',
}, (10, 0)))
protected = obj(R / 'adversarial-sol-finalization-20261117/PROTECTED_AFTER.json')
for key, root, counts in [
    ('source', P / 'papers/23204176/sources', (43, 7)),
    ('INITIAL', R / 'adversarial-sol', (20, 1)),
    ('old_failed_continuation', R / 'adversarial-sol-continuation-20261117', (157, 32)),
]:
    k3.append(authenticate(root, protected[key], counts))
scope_guards = obj(R / 'scope-sol-continuation-20261117/CUSTODY_AFTER.json')
k3.append(authenticate(R / 'scope-sol', scope_guards['entries'][str(R / 'scope-sol')], (30, 0)))
intake = obj(R / 'root-continuation-20261117/INTAKE.json')
primary = []
for row in intake['all74exact_primary_files_copied']:
    path = R / 'root-continuation-20261117/primary' / row['path']
    assert path.stat().st_size == row['bytes'] and digest(path) == row['SHA256'], str(path)
    primary.append(dict(row, actual_mode=oct(stat.S_IMODE(path.stat().st_mode))))
assert len(primary) == 74

stage = []
stage.append(sealed(V / 'hafnian-retract-stage-corrected-sol-20261117', 'OWNED_MANIFEST.json', {
    'FINAL.json': '4282c414493774f4d562af7f6b0364a8f3efb90d026b7116936f17f01ef792e5',
    'OWNED_MANIFEST.json': 'e2a0e565f7849c11af60c774b1cec4903ceae4a7b22f2ac61dcc3ea0002c6318',
}, (1598, 760)))
stage.append(sealed(V / 'hafnian-retract-stage-corrected-audit-sol-20261117', 'OWNED_MANIFEST.json', {
    'FINAL.json': '9bca1054938f93d5f5ade1a590c435fe673c083126b27f38c7216fece9ddd864',
    'OWNED_MANIFEST.json': '31fa54b5e3dcdf33396276ccdeba666849eea0c365f16d41e1811bc10bb2526e',
}, (12, 0)))
stage.append(sealed(V / 'hafnian-retract-stage-audit-continuation-sol-20261117', 'OWNED_MANIFEST.json', {
    'FINAL.json': '32f304fa1ef31a62897d384ba0785b39a3b357e6931cb99a9668fa99c43465dc',
    'OWNED_MANIFEST.json': '9aefd0049fc758708dd61972944e87a3369832eae28586ea2c4573597769e845',
}, (12, 0)))
criteria = obj(V / 'hafnian-retract-stage-audit-continuation-sol-20261117/CRITERIA.json')
assert len(criteria['criteria']) == criteria['criterion_count'] == 28
assert {r['id'] for r in criteria['criteria']} == {f'C{i:02d}' for i in range(1, 29)}
assert all(r['status'].startswith('PASS') for r in criteria['criteria'])

now = datetime.now(timezone.utc).isoformat()
for target, value in [
    (R / 'root-continuation-20261117/FINAL_EVIDENCE_AUTHENTICATION.json',
     dict(schema='root-K3-fresh-evidence-authentication-v1', UTC=now,
          scientific_verdict_not_derived_from_hashes=True, families_and_protected=k3,
          original74primary_pins_exact=primary, root_scientific_runs=0)),
    (V / 'root-hafnian-retract-corrected-stage-adoption-20261117.json',
     dict(schema='root-hafnian-retract-corrected-private-stage-adoption-v1', UTC=now,
          status='ALL_28_FIXED_PRIVATE_STAGE_CRITERIA_ACCEPTED', criteria=criteria,
          fresh_complete_custody=stage,
          root_actual_reading='All actual670builder lines,65diff lines, wholePLAN/FINAL/TARGETS/HEAD and aggregate receipts, both whole accepted candidate articles; current independent REPORT/FINAL/all28criteria personally read.',
          failed_producer_exit_1_and_failed_auditor_exit_1_preserved=True,
          corrected_producer_exit_0_and_separate_audit_continuation_exit_0=True,
          fixed_input_duplicate_checks_not_generic_future_parser_certificate=True,
          stage_FINAL_SHA256='4282c414493774f4d562af7f6b0364a8f3efb90d026b7116936f17f01ef792e5',
          stage_manifest_SHA256='e2a0e565f7849c11af60c774b1cec4903ceae4a7b22f2ac61dcc3ea0002c6318',
          installation_or_publication_authority=False, actual_UI_verification=False,
          AA=None, follow_up=None)),
]:
    assert not target.exists(), str(target)
    target.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(dict(path=str(target), SHA256=digest(target),
                          files=sum(x['files'] for x in (k3 if 'papers/' in str(target) else stage)))))
