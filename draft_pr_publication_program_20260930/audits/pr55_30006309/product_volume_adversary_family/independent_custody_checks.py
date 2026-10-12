"""Independent full-body/mode source accounting without reading old math reviews."""
from pathlib import Path
import hashlib
import json
import sqlite3
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE.parent / 'original_preparation_family'
A45 = HERE.parent.parent / 'pr45_9900007'

def pin(path):
    p = Path(path)
    assert p.is_absolute() and p.is_file() and not p.is_symlink()
    b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(),
            'mode': p.stat().st_mode & 0o777}

def verify(expected):
    actual = pin(expected['path'])
    assert actual == expected, (expected['path'], actual, expected)

def main():
    manifest = ORIGINAL / 'SELF_MANIFEST.json'
    assert pin(manifest)['sha256'] == 'b1124133d9c9cd88206c8a61755d36e16ca94a90a91a512b99fb755f2ee6a270'
    mf = json.loads(manifest.read_text())
    assert mf['actual_closer_pid'] == 84050 and mf['complete_prepared_file_count'] == 127
    refs = [pin(manifest)] + mf['files']
    for r in refs:
        verify(r)
    assert {Path(r['path']) for r in refs} == {p for p in ORIGINAL.rglob('*') if p.is_file()}
    for d in mf['directories']:
        p = Path(d['path']); assert p.is_dir() and not p.is_symlink() and (p.stat().st_mode & 0o777) == d['mode']
    auth = json.loads((ORIGINAL / 'ORIGINAL_AUTHENTICATION.json').read_text())
    assert auth['original_head'] == '85c78d0cf3959d9d492a637cb90835ebc6a0e828'
    assert auth['actual_merge_base_oid'] == '01358d66fc67d1c462bddf31c0d4ee5b120e6737'
    assert auth['github_base_oid'] == 'c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
    for r in auth['original_science_files']:
        b = Path(r['local_path']).read_bytes()
        assert hashlib.sha256(b).hexdigest() == r['sha256']
        assert hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == r['git_blob_sha1']
    assert len(auth['original_science_files']) == 16
    for name, pid in [('root_pr55_original_source_closure_actual_capture', 84050),
                      ('root_pr55_original_source_closed_readback_actual_capture', 84166)]:
        folder = A45 / name
        c = json.loads((folder / 'CAPTURE.json').read_text())
        assert c['pid'] == pid and c['status'] == 'PASS' and c['exit_code'] == 0
        assert c['actual_execution'] is True and c['completed'] is True
        assert c['started_utc'] < c['finished_utc']
        for stream in ('stdout', 'stderr'):
            p = folder / c[stream]['path']; b = p.read_bytes()
            assert len(b) == c[stream]['bytes'] and hashlib.sha256(b).hexdigest() == c[stream]['sha256']
        refs.extend(pin(p) for p in sorted(folder.iterdir()) if p.is_file())
    account = json.loads((ORIGINAL / 'SOURCE_ACCOUNTING.json').read_text())
    for r in list(account['raw_corpus_references'].values()) + [account['SQL_database_reference']]:
        expected = dict(r); expected['mode'] = int(expected['mode'], 8)
        verify(expected); refs.append(expected)
    source = json.loads((ORIGINAL / 'original' / 'source_record.json').read_text())
    problems = json.loads(Path(account['raw_corpus_references']['problems.json']['path']).read_text())
    selected = [p for p in problems if p['id'] == 30006309 and p['problem_number'] == 'OWR-14299288-015']
    assert len(selected) == 1 and selected[0] == source['problem']
    reports = json.loads(Path(account['raw_corpus_references']['research_results.json']['path']).read_text())
    assert 'OWR-14299288-015' not in reports and '30006309' not in reports
    assert source['upstream_report'] is None and 'upstream_report' in source
    db = Path(account['SQL_database_reference']['path'])
    con = sqlite3.connect('file:' + str(db) + '?mode=ro', uri=True)
    sql = con.execute('SELECT payload, report, report IS NULL FROM records WHERE key=?', ('30006309',)).fetchall()
    rev = con.execute('SELECT revision FROM metadata').fetchall(); con.close()
    assert len(sql) == 1 and json.loads(sql[0][0]) == selected[0]
    assert sql[0][1] == '{}' and sql[0][2] == 0
    assert rev == [('37e53eabe540fb458758e198be61634bd02ee008',)]
    assert account['original_draft_proposes'] == {'Status': 'claimed_solved', 'Turns': '1/5'}
    assert account['original_turn_log_entry_count'] == 1
    for r in refs:
        verify(r)
    result = {'status': 'PASS_INDEPENDENT_FULL_BODY_SOURCE_ACCOUNTING', 'utc': datetime.now(timezone.utc).isoformat(),
              'immutable_external_references': refs, 'closed_original_prepared_files': 127,
              'original_science_git_blobs': 16, 'raw_report_key': 'ABSENT; no raw value',
              'archived_wrapper_upstream_report': 'present JSON null placeholder',
              'SQL_report': 'non-NULL TEXT {} fallback', 'original_status_and_turns': 'claimed_solved 1/5',
              'original_turn_entries': 1, 'generic_response_count': 'not separately supplied',
              'limits': 'Integrity/accounting tests are not personal semantic reading of every original review or a mathematical theorem proof. Native mutable QUEUE/state snapshots remain dated only.'}
    (HERE / 'CUSTODY_RESULTS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'immutable_external_references'}, sort_keys=True))

if __name__ == '__main__':
    main()
