#!/usr/bin/env python3
"""Delete only this family's transient primary PDFs, OCR and pixels after inspection."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import sys

assert __debug__ and sys.flags.optimize == 0
FAMILY = Path(__file__).resolve().parent
TEMP = FAMILY / 'tmp/pdfs'
assert TEMP.resolve().parent == FAMILY / 'tmp' and not TEMP.is_symlink()
bindings_path = FAMILY / 'FRESH_PRIMARY_SOURCE_BINDINGS.json'
bindings = json.loads(bindings_path.read_bytes())
expected = {}
for source in bindings['sources']:
    expected[source['filename']] = (source['bytes'], source['sha256'])
    expected[source['filename'] + '.txt'] = (source['full_text_read_bytes'], source['text_sha256'])
    for page in source['selected_page_renders']:
        assert page['personally_visually_inspected'] is True
        expected[Path(page['path']).name] = (page['bytes'], page['sha256'])
paths = sorted(TEMP.iterdir())
assert {path.name for path in paths} == set(expected) and len(paths) == 29
removed = []
for path in paths:
    assert path.is_file() and not path.is_symlink()
    body = path.read_bytes()
    digest = hashlib.sha256(body).hexdigest()
    assert (len(body), digest) == expected[path.name]
    removed.append({'path': path.relative_to(FAMILY).as_posix(), 'bytes': len(body), 'sha256': digest,
                    'full_mode_before_removal': path.stat().st_mode & 0o7777,
                    'entire_body_read_before_removal': True, 'removed': True})
    path.unlink()
assert not any(TEMP.iterdir())
TEMP.rmdir()
(FAMILY / 'tmp').rmdir()
now = datetime.now(timezone.utc).isoformat()
bindings['foreign_bodies_deleted'] = True
bindings['foreign_cleanup_completed_utc'] = now
bindings['foreign_cleanup_actual_pid'] = os.getpid()
bindings_path.write_text(json.dumps(bindings, indent=2) + '\n')
result = {'schema': 'pr48-algebra-family-foreign-input-removal/v1', 'actual_pid': os.getpid(),
          'completed_utc': now, 'status': 'PASS_ALL_29_FOREIGN_BODIES_REMOVED', 'removed': removed,
          'only_own_transient_directory_touched': True, 'foreign_raw_or_SQL_bodies_copied': False,
          'foreign_network_headers_or_cookies_stored': False}
(FAMILY / 'FOREIGN_INPUT_REMOVAL.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'removed_files': len(removed), 'removed_bytes': sum(row['bytes'] for row in removed)}, indent=2))
