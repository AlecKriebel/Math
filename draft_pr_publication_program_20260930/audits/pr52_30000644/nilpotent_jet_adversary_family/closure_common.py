"""SOURCE for ROOT's later independent closure and readback; no imports of production."""
import hashlib
import json
import stat
from pathlib import Path

F = Path(__file__).resolve().parent
MF = F / 'SELF_MANIFEST.json'
def digest(b): return hashlib.sha256(b).hexdigest()
def read_json(p): return json.loads(p.read_bytes())
def identity(p):
    s = p.lstat()
    assert stat.S_ISREG(s.st_mode), str(p)
    b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'sha256': digest(b), 'mode': stat.S_IMODE(s.st_mode)}
def inspect(expected_index, expected_ready, closed):
    assert digest((F / 'INDEX.json').read_bytes()) == expected_index
    assert digest((F / 'READY.json').read_bytes()) == expected_ready
    idx, ready = read_json(F / 'INDEX.json'), read_json(F / 'READY.json')
    assert idx['schema'] == 'pr52-nilpotent-jet-index/v1'
    assert ready['schema'] == 'pr52-nilpotent-jet-ready/v1'
    assert ready['index_sha256'] == expected_index
    assert ready['root_personal_read_attestation'] is False
    assert ready['native_acceptance_authority'] is False
    assert ready['remote_action_authority'] is False
    assert ready['closer_reader_executed_by_preparer'] is False
    actual = sorted(str(p.relative_to(F)) for p in F.rglob('*') if p.is_file() and p != MF)
    expected = sorted([row['relative_path'] for row in idx['payload_bindings']] + ['INDEX.json', 'READY.json'])
    assert actual == expected
    rows = []
    for row in idx['payload_bindings']:
        p = F / row['relative_path']
        got = identity(p)
        assert {k: got[k] for k in ('bytes', 'sha256', 'mode')} == {k: row[k] for k in ('bytes', 'sha256', 'mode')}
        assert got['mode'] == 0o444
        rows.append(got)
    for name in ('INDEX.json', 'READY.json'):
        row = identity(F / name)
        assert row['mode'] == 0o444
        rows.append(row)
    for row in idx['fixed_external_rows']:
        assert identity(Path(row['path'])) == row
    for cpath in idx['actual_capture_paths'] + idx['retained_interrupted_capture_paths']:
        cp = Path(cpath)
        capture = read_json(cp / 'CAPTURE.json')
        assert capture['schema'] == 'pr52-independent-jet-child-capture/v1'
        expected_exit = -2 if cpath in idx['retained_interrupted_capture_paths'] else 0
        assert capture['exit_code'] == expected_exit and capture['source_unchanged_after'] is True
        assert type(capture['child_pid']) is int and capture['child_pid'] > 0
        assert capture['started_utc'] < capture['ended_utc']
        assert digest((cp / 'source_prelaunch.py').read_bytes()) == capture['source_sha256']
        assert digest((cp / 'operator_prelaunch.py').read_bytes()) == capture['operator_sha256']
        for stream in ('stdout', 'stderr'):
            b = (cp / (stream + '.bin')).read_bytes()
            assert len(b) == capture[stream + '_bytes'] and digest(b) == capture[stream + '_sha256']
    directories = sorted(str(p.relative_to(F)) for p in F.rglob('*') if p.is_dir())
    assert directories == idx['directories']
    assert all(not p.is_symlink() for p in F.rglob('*'))
    assert MF.exists() == closed
    if closed:
        assert identity(MF)['mode'] == 0o444
        assert stat.S_IMODE(F.stat().st_mode) == 0o555
        assert all(stat.S_IMODE((F / d).stat().st_mode) == 0o555 for d in directories)
    return {'file_bindings': sorted(rows, key=lambda x: x['path']), 'directories': directories,
            'fixed_external_rows': idx['fixed_external_rows'], 'capture_count': len(idx['actual_capture_paths']),
            'retained_interrupted_capture_count': len(idx['retained_interrupted_capture_paths'])}
