"""Check this prepared or closed family; custody never grants mathematical approval."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import stat

F = Path(__file__).resolve().parent
R = F.parents[3]
EXCLUDED = {'PAYLOAD_INDEX.json', 'READY.json', 'MANIFEST.json'}

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def file_row(path):
    st = path.lstat()
    assert stat.S_ISREG(st.st_mode) and not path.is_symlink()
    return {'path': str(path.relative_to(F)), 'bytes': st.st_size,
            'sha256': digest(path), 'mode': format(stat.S_IMODE(st.st_mode), '04o')}

def inventory():
    all_entries = list(F.rglob('*'))
    assert not any(p.is_symlink() for p in all_entries)
    assert all(p.is_file() or p.is_dir() for p in all_entries)
    files = {str(p.relative_to(F)) for p in all_entries if p.is_file()}
    dirs = {'.'} | {str(p.relative_to(F)) for p in all_entries if p.is_dir()}
    return files, dirs

def external_check():
    d = json.loads((F / 'FIXED_EXTERNAL_INPUTS.json').read_bytes())
    assert d['schema'] == 'pr53-model-theory-fixed-external-inputs/v1'
    assert d['root_approval'] is False
    assert d['original_manifest_sha256'] == 'd10783bb3d60becaa765d36a5cd5ff303c978049b9527266a2be4b2dc92f49b7'
    refs = d['references']
    assert len(refs) == 185 and len({x['absolute_path'] for x in refs}) == 185
    for item in refs:
        p = Path(item['absolute_path'])
        assert p.is_relative_to(R)
        for ancestor in (p,) + tuple(p.parents):
            assert not ancestor.is_symlink()
            if ancestor == R:
                break
        st = p.lstat()
        assert stat.S_ISREG(st.st_mode)
        assert st.st_size == item['bytes'] and digest(p) == item['sha256']
        assert format(stat.S_IMODE(st.st_mode), '04o') == item['mode']
    return len(refs)

def own_captures_check():
    expected = [('independent_inverse_checks_actual_capture', 35731, 0),
                ('independent_scope_custody_actual_capture', 38002, 1),
                ('independent_scope_custody_corrected_actual_capture', 38698, 0)]
    results = {}
    for name, pid, code in expected:
        directory = F / name
        assert {p.name for p in directory.iterdir()} == {'CAPTURE.json', 'prelaunch_operator.py', 'stdout.bin', 'stderr.bin'}
        cap = json.loads((directory / 'CAPTURE.json').read_bytes())
        assert cap['schema'] == 'pr53-independent-command-capture/v1'
        assert cap['actual_execution'] is True and cap['completed'] is True
        assert type(cap['pid']) is int and cap['pid'] == pid
        assert type(cap['exit_code']) is int and cap['exit_code'] == code
        assert cap['status'] == ('PASS' if code == 0 else 'FAIL')
        assert cap['operator_unchanged'] is True and cap['root_approval'] is False
        assert cap['cwd'] == str(R) and cap['argv'][:2] == ['/usr/bin/python3', '-B']
        assert digest(directory / 'prelaunch_operator.py') == cap['operator_sha256']
        assert dt.datetime.fromisoformat(cap['started_utc']) <= dt.datetime.fromisoformat(cap['finished_utc'])
        for stream in ('stdout', 'stderr'):
            p = directory / (stream + '.bin')
            assert p.stat().st_size == cap[stream]['bytes']
            assert digest(p) == cap[stream]['sha256']
        if code == 0:
            result = json.loads((directory / 'stdout.bin').read_bytes())
            source = F / ('independent_inverse_checks.py' if pid == 35731 else 'independent_scope_custody.py')
            assert result['source_sha256'] == digest(source)
            assert result['root_approval'] is False
            results[pid] = result
        else:
            assert (directory / 'stdout.bin').read_bytes() == b''
            assert b'AssertionError' in (directory / 'stderr.bin').read_bytes()
    assert results[35731]['assertions'] == 275054
    assert results[35731]['finite_inverse_systems'] == 958
    assert results[35731]['actual_automorphisms_checked'] == 35
    assert results[38698]['assertions'] == 711
    assert results[38698]['external_fixed_references'] == 185
    return 3

def prepared_check():
    assert not (F / 'MANIFEST.json').exists()
    ready = json.loads((F / 'READY.json').read_bytes())
    assert ready['schema'] == 'pr53-model-theory-adversary-ready/v1'
    assert ready['status'] == 'READY_FOR_ROOT_CUSTODY_ONLY'
    assert ready['root_approval'] is False and ready['root_closer_executed'] is False
    index = json.loads((F / 'PAYLOAD_INDEX.json').read_bytes())
    assert ready['payload_index_sha256'] == digest(F / 'PAYLOAD_INDEX.json')
    files, dirs = inventory()
    rows = index['files']
    assert files == {x['path'] for x in rows} | {'PAYLOAD_INDEX.json', 'READY.json'}
    assert len(files) == ready['prepared_payload_files'] and len(files) <= 35
    assert sum((F / name).stat().st_size for name in files) < 1000000
    assert dirs == set(index['directories'])
    for item in rows:
        assert file_row(F / item['path']) == item
    for name, sha in ready['key_sha256'].items():
        assert digest(F / name) == sha
    verdict = json.loads((F / 'VERDICT.json').read_bytes())
    assert verdict['mandatory_repairs'] == [] and verdict['root_approval'] is False
    assert verdict['recommended_queue_status'] == 'already_solved'
    return files, dirs, external_check(), own_captures_check()

def closed_check(expected_manifest_sha):
    mf = F / 'MANIFEST.json'
    assert digest(mf) == expected_manifest_sha
    d = json.loads(mf.read_bytes())
    assert d['schema'] == 'pr53-model-theory-adversary-closed-manifest/v1'
    assert d['root_approval'] is False
    files, dirs = inventory()
    assert files == {x['path'] for x in d['files']}
    assert dirs == set(d['directories'])
    assert len(files) <= 36
    for item in d['files']:
        if item['path'] == 'MANIFEST.json':
            assert item == {'path': 'MANIFEST.json', 'bytes': None,
                            'sha256': 'LITERAL_SELF_REFERENCE_NOT_A_DIGEST', 'mode': '0444'}
            assert file_row(mf)['mode'] == '0444'
        else:
            assert file_row(F / item['path']) == item
    for name in dirs:
        p = F if name == '.' else F / name
        assert stat.S_IMODE(p.stat().st_mode) == 0o555
    return len(files), len(dirs), external_check(), own_captures_check()
