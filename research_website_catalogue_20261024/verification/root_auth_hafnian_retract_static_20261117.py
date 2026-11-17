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

result = sealed(V / 'hafnian-retract-production-audit-sol-20261117', 'OWNED_MANIFEST.json', {
 'FINAL.json': 'c4097bee1f854db2362148f6ac85c5bb754f7e8ce371fee0d8cfdc831e508faa',
 'OWNED_MANIFEST.json': 'e8efe6129469f3e88f591c937ab6e50b8ffbf1df8f6a5ec4ee3a16eecd227b25',
}, (18, 0))
helper = V / 'hafnian-retract-production-prepare-sol-20261117/release_two.py'
plan = helper.with_name('PLAN.json')
assert digest(helper) == '6a831b55fbd1d49196619e047e6461d36c9171da94f5ede8d45cdd8148d5b734'
assert digest(plan) == '682ae4747c3004aef1b74fb8bce7f43b76984c427353419a7e8c770e941fa2a1'
audit = obj(V / 'hafnian-retract-production-audit-sol-20261117/FINAL.json')
assert audit['blocking_static_findings'] == audit['required_source_corrections'] == []
value = dict(schema='root-hafnian-retract-newhelper-static-adoption-v1', UTC=datetime.now(timezone.utc).isoformat(),
 status='ALL_STATIC_FINDINGS_RESOLVED_FOR_EXACT_ACTION', complete_actual_helper_lines_personally_read=1260,
 complete_actual_PLAN_TARGETS_REPORT_FINAL_FINDINGS_personally_read=True,
 actual_static_scope_not_executed_runtime_certificate=True, fresh_audit_custody=result,
 helper_SHA256=digest(helper), PLAN_SHA256=digest(plan), runtime_ignore_prerequisite_pending=True,
 separate_current_action_authorities_required=True, helper_modes_executed=0,
 deployment_or_Sheet_or_AA_authority=False, AA=None, follow_up=None)
target = V / 'root-hafnian-retract-newhelper-static-adoption-20261117.json'
assert not target.exists()
target.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(status=value['status'],path=str(target),SHA256=digest(target))))
