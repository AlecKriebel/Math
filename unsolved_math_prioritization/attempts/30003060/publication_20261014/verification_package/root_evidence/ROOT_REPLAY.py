#!/usr/bin/env python3
"""Replay frozen PR evidence in canonical temporary paths on macOS and Unix."""
import datetime
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def inventory(path):
    return {p.relative_to(path).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in path.rglob('*') if p.is_file()}


def main():
    source = ROOT / 'source'
    manifest = json.loads((ROOT / 'SOURCE_MANIFEST.json').read_text())
    expected = {f['path']: f['sha256'] for f in manifest['files']}
    need(len(expected) == 65 and inventory(source) == expected, 'Frozen source inventory changed')
    # The historical controls reject every symlink ancestor. macOS /var is a
    # symlink to /private/var, so all nested temporary paths must be canonical.
    scratch = ROOT / 'replay'
    scratch.mkdir(exist_ok=True)
    scratch = scratch.resolve()
    env = dict(os.environ, TMPDIR=str(scratch), TMP=str(scratch), TEMP=str(scratch))
    results = []
    for optimized in [False, True]:
        with tempfile.TemporaryDirectory(prefix='pr826 relocated input with spaces ', dir=scratch) as td:
            copied = pathlib.Path(td).resolve() / 'frozen input'
            shutil.copytree(source, copied)
            command = ['python3', '-I', '-S', '-B', *(['-O'] if optimized else []),
                       str(copied / 'verify_publication.py'), str(copied)]
            run = subprocess.run(command, cwd='/', env=env, capture_output=True, text=True, timeout=600)
            if run.returncode:
                (ROOT / ('ROOT_REPLAY_CANONICAL_FAILURE_' + str(optimized) + '.json')).write_text(
                    json.dumps({'command': command, 'returncode': run.returncode,
                                'stdout': run.stdout, 'stderr': run.stderr}, indent=2) + '\n')
            need(run.returncode == 0, run.stderr)
            result = json.loads(run.stdout)
            need(result['status'] == 'PASS' and result['archives_verified'] == 4
                 and result['members_verified'] == 55, 'Unexpected replay result')
            need(inventory(copied) == expected, 'Replay changed frozen inputs')
            results.append({'optimized_parent': optimized, 'result': result,
                            'all_65_input_files_unchanged': True})
    need(inventory(source) == expected, 'Original source changed')
    output = {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'status': 'PASS', 'source_files': 65, 'archive_members': 55,
              'temporary_paths': 'Canonical resolved TMPDIR inherited by all child processes',
              'modes': results,
              'optimized_rejections': 'Author and second-review children deliberately fail closed under -O; not counted as optimized mathematical passes',
              'separate_universal_proof_and_primary_source_review_required': True}
    (ROOT / 'ROOT_REPLAY_RESULTS.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'modes': 2, 'source_files': 65,
                      'archive_members': 55,
                      'runs_per_mode': [len(x['result']['runs']) for x in results]}))


if __name__ == '__main__':
    main()
