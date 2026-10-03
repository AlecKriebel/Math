"""SOURCE ONLY: separate read-only readback after ROOT actually closes this family."""
import json, os, stat
from custody_checks import F, MANIFEST, SCHEMA, sha, load, files_and_dirs, verify_results
def main():
    manifest = F/MANIFEST
    m = load(manifest)
    assert m['schema'] == SCHEMA and m['root'] == str(F)
    assert m['self_excluded'] == MANIFEST and m['ROOT_acceptance_certified'] is False
    assert type(m['actual_closer_pid']) is int and m['actual_closer_pid'] > 0
    files, dirs = files_and_dirs()
    assert m['files_count'] == len(m['files']) == len(files)
    rows = {r['path']: r for r in m['files']}
    assert len(rows) == len(files)
    assert set(rows) == {p.relative_to(F).as_posix() for p in files}
    assert set(m['directories']) == {p.relative_to(F).as_posix() for p in dirs}
    assert len(m['directories']) == len(dirs) and m['directory_full_mode'] == 0o555
    for p in files:
        row = rows[p.relative_to(F).as_posix()]; b = p.read_bytes()
        assert len(b) == row['bytes'] and sha(b) == row['sha256']
        assert stat.S_IMODE(p.lstat().st_mode) == row['full_mode'] == 0o444
    assert stat.S_IMODE(manifest.lstat().st_mode) == 0o444
    for p in dirs: assert stat.S_IMODE(p.lstat().st_mode) == 0o555
    assert sha((F/'REPORT.md').read_bytes()) == m['report_sha256']
    assert sha((F/'VERDICT.json').read_bytes()) == m['verdict_sha256']
    verify_results()
    print(json.dumps(dict(schema='pr50-virtual-markov-priority-closed-readback/v1',
                         actual_pid=os.getpid(), status='PASS_READONLY_SELF_ONLY_CUSTODY',
                         manifest_sha256=sha(manifest.read_bytes()), files_count=len(files),
                         ROOT_acceptance_certified=False), sort_keys=True))
if __name__ == '__main__': main()
