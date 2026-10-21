"""UNEXECUTED ROOT-only closer; custody is not a native or mathematical approval."""
from pathlib import Path
import json
import os
import stat
from closed_scope_common import F, prepared_check, file_row, digest, closed_check

def main():
    files, dirs, refs, captures = prepared_check()
    assert not (F / 'MANIFEST.json').exists()
    for name in sorted(files):
        os.chmod(F / name, 0o444)
    rows = [file_row(F / name) for name in sorted(files)]
    rows.append({'path': 'MANIFEST.json', 'bytes': None,
                 'sha256': 'LITERAL_SELF_REFERENCE_NOT_A_DIGEST', 'mode': '0444'})
    d = {'schema': 'pr53-model-theory-adversary-closed-manifest/v1',
         'scope': 'Independent source/mathematical boundary audit only; no ROOT approval',
         'files': sorted(rows, key=lambda x: x['path']), 'directories': sorted(dirs),
         'root_approval': False}
    mf = F / 'MANIFEST.json'
    with mf.open('x') as stream:
        stream.write(json.dumps(d, indent=2) + '\n')
        stream.flush()
        os.fsync(stream.fileno())
    os.chmod(mf, 0o444)
    for name in sorted(dirs, key=lambda x: x.count('/'), reverse=True):
        p = F if name == '.' else F / name
        os.chmod(p, 0o555)
    sha = digest(mf)
    n, ndirs, nrefs, ncaps = closed_check(sha)
    print(json.dumps({'status': 'PASS_ADVERSARY_CUSTODY_ONLY', 'manifest_sha256': sha,
                      'prepared_payload_files': n - 1, 'closed_files_including_literal_self': n,
                      'directories': ndirs, 'external_fixed_references': nrefs,
                      'actual_independent_capture_objects': ncaps, 'root_approval': False}))

if __name__ == '__main__':
    main()
