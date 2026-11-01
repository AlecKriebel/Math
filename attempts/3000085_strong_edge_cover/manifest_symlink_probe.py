"""Controlled harmless symlink test. Never references a real sensitive file."""
import json
from pathlib import Path
import runpy
import sys

root = Path(sys.argv[1]).resolve()
reads = []
original_text = Path.read_text
original_bytes = Path.read_bytes

def tracked_text(self, *args, **kwargs):
    if self.name in {'MANIFEST.json', 'harmless_manifest_target.json'}:
        reads.append(str(self.name))
    return original_text(self, *args, **kwargs)

def tracked_bytes(self, *args, **kwargs):
    if self.name in {'MANIFEST.json', 'harmless_manifest_target.json'}:
        reads.append(str(self.name))
    return original_bytes(self, *args, **kwargs)

Path.read_text = tracked_text
Path.read_bytes = tracked_bytes
try:
    runpy.run_path(str(root / 'validate.py'), run_name='__main__')
except RuntimeError as exc:
    if str(exc) != 'Nonregular entry forbidden: MANIFEST.json':
        raise RuntimeError('Wrong rejection reason') from exc
    if reads:
        raise RuntimeError('Manifest content read before rejection') from exc
    print(json.dumps({'manifest_reads': 0, 'rejected_before_read': True}, sort_keys=True))
else:
    raise RuntimeError('Manifest symlink accepted')
