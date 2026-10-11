"""Small self-only custody checks; these do not establish mathematical truth."""
from pathlib import Path
import datetime as dt, hashlib, json, stat
F = Path(__file__).resolve().parent
MANIFEST = 'SELF_ONLY_CLOSURE.json'
SCHEMA = 'pr50-virtual-markov-priority-self-only-closure/v1'
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_bytes())
def files_and_dirs():
    files, dirs = [], [F]
    for p in sorted(F.rglob('*')):
        s = p.lstat()
        assert not p.is_symlink(), str(p)
        if stat.S_ISDIR(s.st_mode): dirs.append(p)
        else:
            assert stat.S_ISREG(s.st_mode), str(p)
            if p.name != MANIFEST or p.parent != F: files.append(p)
    return files, dirs
def verify_selected():
    data = load(F/'SELECTED_INPUT_BINDINGS.json')
    assert data['head'] == '7260315f8b8b193020c09d4ef6df9d943a3a13ff'
    assert data['selected_count'] == len(data['files']) == 8
    for row in data['files']:
        p = Path(row['path']); s = p.lstat(); b = p.read_bytes()
        assert p.parent == F.parent/'original' and stat.S_ISREG(s.st_mode)
        assert not p.is_symlink() and stat.S_IMODE(s.st_mode) == row['full_mode'] == 0o444
        assert len(b) == row['bytes'] and sha(b) == row['sha256']
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest() == row['git_blob_sha1']
    # Shared snapshot-manifest mode was dated metadata, not an eternal mode assertion.
def verify_captures():
    for name, result, pid in [
        ('VIRTUAL_LIFT_CONTROLS_ACTUAL_CAPTURE', 'CONTROL_RESULT.json', 53953),
        ('SELECTED_INPUTS_ACTUAL_CAPTURE', 'SELECTED_INPUT_BINDINGS.json', 61032)]:
        d = F/name
        assert {p.name for p in d.iterdir()} == {
            'PRELAUNCH.json','CAPTURE.json','prelaunch_operator.py','prelaunch_target.py','stdout.bin','stderr.bin'}
        pre, cap = load(d/'PRELAUNCH.json'), load(d/'CAPTURE.json')
        assert pre['actual_execution'] is False and pre['completed'] is False
        assert pre['pid'] is None and pre['exit_code'] is None
        assert cap['schema'] == 'pr50-virtual-markov-adversary-actual-command/v1'
        assert cap['actual_execution'] is True and cap['completed'] is True
        assert type(cap['pid']) is int and cap['pid'] == pid
        assert type(cap['operator_pid']) is int and cap['operator_pid'] > 0
        assert type(cap['exit_code']) is int and cap['exit_code'] == cap['expected_exit'] == 0
        assert cap['operator_unchanged'] is True and cap['target_unchanged'] is True
        assert cap['capture_status'] == 'EXPECTED_ACTUAL_EXIT_COMPLETE'
        assert cap['argv'] == pre['argv'] and cap['stdin_supplied'] is False
        assert cap['started_utc'] == pre['started_utc']
        start, end = [dt.datetime.fromisoformat(cap[k]) for k in ('started_utc','finished_utc')]
        assert start.utcoffset() == end.utcoffset() == dt.timedelta(0) and start <= end
        for stream in ('stdout','stderr'):
            b = (d/(stream+'.bin')).read_bytes(); r = cap[stream]
            assert r['path'] == stream+'.bin' and len(b) == r['bytes'] and sha(b) == r['sha256']
        assert (d/'stderr.bin').read_bytes() == b''
        assert load(d/'stdout.bin') == load(F/result)
        target = cap['target_source']; path = Path(target['path'])
        assert path.parent == F and path == Path(cap['argv'][2])
        b = path.read_bytes()
        assert b == (d/'prelaunch_target.py').read_bytes()
        assert len(b) == target['bytes'] and sha(b) == target['sha256']
        op = (F/'capture_actual_command.py').read_bytes()
        assert op == (d/'prelaunch_operator.py').read_bytes() and sha(op) == cap['operator_sha256']
def verify_results():
    v = load(F/'VERDICT.json')
    assert v['verdict'] == 'PASS_LITERAL_MATH_PRIORITY_UNESTABLISHED'
    assert v['mandatory_mathematical_defects'] == []
    assert v['historical_novelty'] == 'unestablished'
    assert v['ROOT_approval_or_acceptance'] is False and v['own_closure_executed'] is False
    c = load(F/'CONTROL_RESULT.json')
    assert c['assertions'] == 32984 and c['edge_cases'] == 4666
    assert set(c['coverage']) == {'C','BC','T','D','R','L','BR','BL'}
    verify_selected(); verify_captures()
