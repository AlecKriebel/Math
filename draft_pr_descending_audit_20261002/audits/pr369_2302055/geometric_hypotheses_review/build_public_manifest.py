"""Build and verify an exact self-excluded manifest of this family's own files."""
import datetime as dt
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PRIVATE = {"private_sources", "private_replay", "__pycache__"}
MANIFEST = "PUBLIC_MANIFEST.json"

def public_files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file()
                  and not any(part in PRIVATE for part in p.relative_to(ROOT).parts)
                  and p.relative_to(ROOT).as_posix() != MANIFEST)

def verify():
    obj = json.loads((ROOT / MANIFEST).read_text())
    paths = [row['path'] for row in obj['files']]
    assert len(paths) == len(set(paths)), "Duplicate manifest entry"
    assert set(paths) == {p.relative_to(ROOT).as_posix() for p in public_files()}, "Manifest is not exact"
    for row in obj['files']:
        raw = (ROOT / row['path']).read_bytes()
        assert len(raw) == row['bytes']
        assert hashlib.sha256(raw).hexdigest() == row['sha256']
    return len(paths)

if __name__ == '__main__':
    payload = {'generated_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
               'owner':'PR369 independent geometric_hypotheses_review family',
               'frozen_head':'d9e4600d05b8272fe913a22ae7dcc0fbe0a26344',
               'original_base':'efd29c05204703acca9a0860812f54b94fae54b1',
               'self_excluded':MANIFEST,
               'ignored_private_roots':sorted(PRIVATE),
               'files':[{'path':p.relative_to(ROOT).as_posix(), 'bytes':p.stat().st_size,
                         'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
                        for p in public_files()]}
    (ROOT / MANIFEST).write_text(json.dumps(payload,indent=2)+'\n')
    print(json.dumps({'status':'PASS','exact_self_excluded_public_files':verify()}))
