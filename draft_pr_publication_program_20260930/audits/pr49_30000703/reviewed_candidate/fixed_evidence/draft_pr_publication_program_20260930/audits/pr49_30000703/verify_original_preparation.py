"""Separate read-only verification after ROOT's PR49 original closing child has exited."""
from pathlib import Path, PurePosixPath
import argparse, datetime as dt, hashlib, json, os, stat
A=Path(__file__).resolve().parent
def sha(body):return hashlib.sha256(body).hexdigest()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--expected-manifest-sha256',required=True);args=parser.parse_args()
    target=A/'ORIGINAL_PREPARATION_MANIFEST.json';body=target.read_bytes();assert sha(body)==args.expected_manifest_sha256 and stat.S_IMODE(target.stat().st_mode)==0o444
    manifest=json.loads(body);assert manifest['schema']=='pr49-original-preparation-self-only-manifest/v1'
    assert manifest['self_excluded']==['ORIGINAL_PREPARATION_MANIFEST.json'] and manifest['future_acceptance_authority'] is False
    assert manifest['helper_execution_performed'] is False and manifest['current_mathematical_verdict'] is None and manifest['source_claim_validation_verdict'] is None
    assert manifest['outer_capture_status_at_child_closure']=='PENDING_CHILD_EXIT' and manifest['outer_post_child_completion_and_ROOT_readback_required'] is True
    rows=manifest['files'];assert len(rows)==manifest['files_count']==350 and len({row['path'] for row in rows})==350
    for row in rows:
        literal=PurePosixPath(row['path']);assert not literal.is_absolute() and '..' not in literal.parts
        path=A/row['path'];assert path.is_file() and not path.is_symlink();value=path.read_bytes()
        assert len(value)==row['bytes'] and sha(value)==row['sha256'] and stat.S_IMODE(path.stat().st_mode)==row['full_mode']==0o444
    for row in manifest['owned_directory_bindings']:
        path=A/row['path'];assert path.is_dir() and not path.is_symlink() and stat.S_IMODE(path.stat().st_mode)==row['full_mode']
    actual_files={name for name in manifest['authorship_root_files']}
    actual_dirs=set()
    for name in manifest['authorship_directory_roots']:
        directory=A/name;assert directory.is_dir() and not directory.is_symlink()
        for path in [directory]+list(directory.rglob('*')):
            assert not path.is_symlink() and (path.is_file() or path.is_dir())
            if path.is_file():actual_files.add(path.relative_to(A).as_posix())
            else:actual_dirs.add(path.relative_to(A).as_posix())
    assert actual_files=={row['path'] for row in rows} and actual_dirs==set(manifest['owned_directories'])=={row['path'] for row in manifest['owned_directory_bindings']}
    assert stat.S_IMODE(A.stat().st_mode)==manifest['authorship_root_full_mode']
    print(json.dumps(dict(status='CLOSED_ORIGINAL_PREPARATION_READ_ONLY_VERIFY_PASS',actual_pid=os.getpid(),verified_utc=dt.datetime.now(dt.timezone.utc).isoformat(),manifest_sha256=sha(body),owned_files=len(rows),owned_directories=len(actual_dirs),full_modes_and_exact_owned_topology_verified=True,future_external_capture_not_certified_by_child_manifest=True,current_mathematical_verdict=None,acceptance_verdict=None),sort_keys=True))
if __name__=='__main__':main()
