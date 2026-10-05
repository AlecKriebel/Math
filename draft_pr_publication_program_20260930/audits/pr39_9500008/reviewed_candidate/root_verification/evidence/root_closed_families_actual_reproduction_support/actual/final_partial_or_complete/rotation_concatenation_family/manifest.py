"""Build/check the entire first-party tree; only tmp and manifest exclude.

Do not put foreign downloaded PDFs, extracted text, dependency files, or caches
outside tmp. Stdout is a receipt; this verifier does not generate extra files.
"""
from pathlib import Path
import hashlib
import json
import sys

root = Path(__file__).resolve().parent
manifest_name = 'FIRST_PARTY_MANIFEST.json'


def records():
    output = []
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root)
        if relative.parts[0] == 'tmp' or relative.as_posix() == manifest_name:
            continue
        if path.is_symlink():
            raise RuntimeError('Unexpected symlink: ' + relative.as_posix())
        if path.is_file():
            data = path.read_bytes()
            output.append({'path': relative.as_posix(), 'bytes': len(data),
                           'sha256': hashlib.sha256(data).hexdigest()})
    return output


mode = sys.argv[1] if len(sys.argv) > 1 else 'check'
actual = records()
if mode == 'build':
    (root / manifest_name).write_text(json.dumps({
        'scope': 'Every regular first-party file recursively under this directory',
        'excluded': ['tmp/** (ignored foreign material/cache/private replay tree)',
                     manifest_name + ' (self exclusion only)'],
        'symlinks_allowed': False,
        'file_count': len(actual),
        'files': actual,
    }, indent=2) + '\n')
elif mode != 'check':
    raise ValueError('mode must be build or check')
saved = json.loads((root / manifest_name).read_text())
assert saved['files'] == actual, 'Missing, added, or changed first-party files'
assert saved['file_count'] == len(actual)
print(json.dumps({'passed': True, 'recursive_file_count': len(actual),
                  'manifest_sha256': hashlib.sha256((root / manifest_name).read_bytes()).hexdigest(),
                  'self_exclusion': manifest_name,
                  'foreign_tmp_excluded': True}, indent=2))
