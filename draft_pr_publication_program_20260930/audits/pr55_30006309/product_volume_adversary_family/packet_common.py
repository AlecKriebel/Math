"""Read-only, bounded full-body closure validation for this exact SOURCE packet."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

HERE = Path(__file__).resolve().parent
SELF = 'SELF_MANIFEST.json'

def row(p):
    assert p.is_absolute() and p.is_file() and not p.is_symlink()
    b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(),
            'mode': p.stat().st_mode & 0o777}

def same(expected):
    assert row(Path(expected['path'])) == expected, expected['path']

def owned(p):
    assert p.is_absolute() and p.resolve() == p
    assert p.parent == HERE or HERE in p.parents, p
    assert not any(x.is_symlink() for x in [p] + list(p.parents)[:len(p.relative_to(HERE).parts)]), p

def validate(closed=False):
    index = json.loads((HERE / 'INDEX.json').read_text())
    ready = json.loads((HERE / 'READY.json').read_text())
    assert ready['index_sha256'] == row(HERE / 'INDEX.json')['sha256']
    assert ready['ROOT_personal_read_attestation'] is False
    expected = {Path(r['path']) for r in index['files']} | {HERE / 'INDEX.json', HERE / 'READY.json'}
    if closed:
        expected.add(HERE / SELF)
    actual = {p for p in HERE.rglob('*') if p.is_file()}
    assert expected == actual
    assert len(actual) <= 65 and sum(p.stat().st_size for p in actual) < 1000000
    for p in actual:
        owned(p)
    for r in index['files']:
        owned(Path(r['path'])); same(r)
    for r in index['immutable_external_references']:
        same(r)
    for d in index['directories']:
        p = Path(d['path']); assert p == HERE or HERE in p.parents
        assert p.is_dir() and not p.is_symlink() and p.stat().st_mode & 0o777 == d['mode']
    assert {Path(d['path']) for d in index['directories']} == {HERE} | {p for p in HERE.rglob('*') if p.is_dir()}
    # Recorded modes in historical CAPTURE rows describe the actual process
    # instant. Own files were subsequently frozen; exact current modes are in INDEX.
    for folder in sorted((HERE / 'captures').iterdir()):
        c = json.loads((folder / 'CAPTURE.json').read_text())
        assert c['actual_execution'] is True and c['completed'] is True
        assert type(c['pid']) is int and c['pid'] > 0 and c['exit_code'] == 0 and c['status'] == 'PASS'
        assert c['started_utc'] < c['finished_utc'] and c['source_unchanged'] and c['operator_unchanged']
        for label in ('stdout', 'stderr', 'source_prelaunch', 'operator_prelaunch', 'input_prelaunch'):
            r = c[label]; p = Path(r['path']); owned(p); b = p.read_bytes()
            assert len(b) == r['bytes'] and hashlib.sha256(b).hexdigest() == r['sha256']
        script = Path(c['argv'][-1]); owned(script)
        assert script.read_bytes() == (folder / 'source_prelaunch.py').read_bytes()
    result = json.loads((HERE / 'INDEPENDENT_RESULTS.json').read_text())
    assert result['assertions'] == 44459 and result['product_triangulations'] == 70 and result['nonstaircase_triangulations'] == 33
    assert result['source_sha256'] == row(HERE / 'independent_product_checks.py')['sha256']
    assert all(json.loads((HERE / 'NEGATIVE_RESULTS.json').read_text())['rejected_alternatives'].values())
    assert json.loads((HERE / 'UNUSED_RESULTS.json').read_text())['configurations'] == 6
    if closed:
        mf = json.loads((HERE / SELF).read_text())
        assert mf['ROOT_personal_read_not_inferred_from_integrity'] is True
        assert mf['index_sha256'] == row(HERE / 'INDEX.json')['sha256']
        assert mf['ready_sha256'] == row(HERE / 'READY.json')['sha256']
        assert {Path(r['path']) for r in mf['files']} == actual - {HERE / SELF}
        for r in mf['files']:
            same(r)
        assert all(row(p)['mode'] == 0o444 for p in actual)
    return index, ready, sorted(actual)

def timestamp():
    return datetime.now(timezone.utc).isoformat()
