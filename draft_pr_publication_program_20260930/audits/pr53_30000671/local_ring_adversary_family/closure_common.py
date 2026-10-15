from pathlib import Path
import datetime, hashlib, json, os, stat

F = Path(__file__).resolve().parent
R = Path('/Users/alec/Documents/Math')
assert F == R / 'draft_pr_publication_program_20260930/audits/pr53_30000671/local_ring_adversary_family'

def digest(b):
    return hashlib.sha256(b).hexdigest()

def body_row(p, base):
    assert p.resolve() == p and stat.S_ISREG(p.lstat().st_mode)
    b = p.read_bytes()
    return {'path': p.relative_to(base).as_posix(), 'bytes': len(b),
            'sha256': digest(b), 'mode': format(stat.S_IMODE(p.lstat().st_mode), '04o')}

def check_row(base, row):
    assert type(row['bytes']) is int and row['bytes'] >= 0
    assert type(row['path']) is str and not Path(row['path']).is_absolute()
    assert '..' not in Path(row['path']).parts
    p = base / row['path']
    assert p.resolve() == p and stat.S_ISREG(p.lstat().st_mode), str(p)
    b = p.read_bytes()
    assert len(b) == row['bytes'] and digest(b) == row['sha256'], str(p)
    assert format(stat.S_IMODE(p.lstat().st_mode), '04o') == row['mode'], str(p)

def check_external():
    e = json.loads((F / 'EXTERNAL_REFERENCES.json').read_bytes())
    assert e['schema'] == 'pr53-independent-external-inputs/v1'
    for row in e['rows']:
        check_row(R, row)
    for row in e['closed_original_directories']:
        q = R / row['path']
        assert q.resolve() == q and q.is_dir()
        assert format(stat.S_IMODE(q.lstat().st_mode), '04o') == row['mode']
    for p in e['root_complete_capture_paths']:
        q = R / p
        c = json.loads(q.read_bytes())
        assert c['schema'] == 'root-explicit-command-capture/v1'
        assert c['actual_execution'] is True and c['completed'] is True and c['status'] == 'PASS'
        assert type(c['exit_code']) is int and type(c['expected_exit_code']) is int
        assert c['exit_code'] == c['expected_exit_code'] == 0
        assert type(c['pid']) is int and c['pid'] > 0
        assert type(c['argv']) is list and c['argv'] and all(type(x) is str for x in c['argv'])
        assert c['cwd'] == str(R) and c['operator_unchanged'] is True
        t0 = datetime.datetime.fromisoformat(c['started_utc'].replace('Z', '+00:00'))
        t1 = datetime.datetime.fromisoformat(c['finished_utc'].replace('Z', '+00:00'))
        assert t0.tzinfo is not None and t1.tzinfo is not None and t0 < t1
        for k in ('stdout', 'stderr'):
            r = c[k]
            z = q.parent / r['path']
            b = z.read_bytes()
            assert len(b) == r['bytes'] and digest(b) == r['sha256']
        assert digest((q.parent / 'prelaunch_operator.py').read_bytes()) == c['operator_sha256']
    return len(e['rows'])

def check_prepared():
    ready = json.loads((F / 'READY.json').read_bytes())
    assert ready['schema'] == 'pr53-independent-source-ready/v1' and ready['root_approval'] is False
    assert ready['mandatory_mathematical_corrections'] == []
    idxb = (F / 'PREPARED_PAYLOAD_INDEX.json').read_bytes()
    assert digest(idxb) == ready['index_sha256']
    idx = json.loads(idxb)
    assert idx['schema'] == 'pr53-independent-payload-index/v1'
    names = {r['path'] for r in idx['rows']} | {'READY.json', 'PREPARED_PAYLOAD_INDEX.json'}
    actual = {p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file()}
    assert actual == names and 'MANIFEST.json' not in names
    dirs = {p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_dir()}
    assert dirs == set(idx['directories'])
    for row in idx['rows']:
        check_row(F, row)
        assert row['mode'] == '0444'
    for p in (F / 'READY.json', F / 'PREPARED_PAYLOAD_INDEX.json'):
        assert stat.S_IMODE(p.lstat().st_mode) == 0o444 and p.resolve() == p
    return names, dirs, check_external()
