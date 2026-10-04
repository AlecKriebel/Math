from pathlib import Path
import json, os, stat
from closure_common import F, body_row, check_prepared, digest

mf = F / 'MANIFEST.json'
assert not mf.exists() and not mf.is_symlink(), 'ROOT closure is absent-only'
names, dirs, external_count = check_prepared()
rows = [body_row(F / p, F) for p in sorted(names)]
result = {'schema': 'pr53-independent-closed-family/v1',
          'payload_rows': rows,
          'self': {'path': 'MANIFEST.json', 'sha256': 'SELF', 'mode': '0444'},
          'directories': sorted(dirs), 'directory_mode': '0555',
          'external_rows_checked': external_count, 'root_approval': False}
b = (json.dumps(result, indent=2) + '\n').encode()
fd = os.open(str(mf), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
with os.fdopen(fd, 'wb') as f:
    f.write(b)
    f.flush()
    os.fchmod(f.fileno(), 0o444)
    os.fsync(f.fileno())
for p in sorted((F / d for d in dirs), key=lambda z: len(z.parts), reverse=True):
    assert p.resolve() == p
    p.chmod(0o555)
F.chmod(0o555)
print(json.dumps({'status': 'PASS', 'manifest_sha256': digest(b),
                  'payload_files': len(rows), 'directories': len(dirs),
                  'external_rows': external_count, 'root_approval': False}, indent=2))
