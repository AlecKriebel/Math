"""Passive source identity/import-text inventory; no imported source execution."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

LANE = Path(__file__).resolve().parent
PRIMARY = LANE / 'primary'
SOURCE = LANE.parent.parent / 'sources'
author_manifest = json.loads((SOURCE / 'archives/01-thompson-cstar-verification.zip.extracted/upstream_finite_lean_manifest.json').read_text())
directory = json.loads((PRIMARY / 'lean-directory.json').read_text())
assert len(directory) == 68
entries = []
for item in directory:
    path = PRIMARY / 'lean' / item['name']
    data = path.read_bytes()
    module = 'OAI.GroupTheory.Thompson.' + path.stem
    digest = hashlib.sha256(data).hexdigest()
    blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert len(data) == item['size'] and blob == item['sha']
    expected = author_manifest['internal_modules'][module]
    assert expected['sha256'] == digest and expected['bytes'] == len(data)
    text = data.decode()
    entries.append({'module': module, 'file': str(path.relative_to(LANE)), 'bytes': len(data),
                    'lines': len(text.splitlines()), 'sha256': digest, 'git_blob_sha1': blob,
                    'imports': re.findall(r'^import\s+(\S+)', text, flags=re.MULTILINE),
                    'personally_read_complete': True,
                    'declaration_hole_scan_hits': re.findall(r'\b(?:axiom|sorry|admit)\b', text)})
modules = {entry['module']: entry for entry in entries}
external = set()
reachable = set()
def follow(module):
    if module in reachable:
        return
    reachable.add(module)
    for dependency in modules[module]['imports']:
        if dependency.startswith('OAI.'):
            assert dependency in modules, dependency
            follow(dependency)
        else:
            external.add(dependency)
follow('OAI.GroupTheory.Thompson.Main')
pdf = (PRIMARY / 'openai-paper.pdf').read_bytes()
pdf_item = next(i for i in json.loads((PRIMARY / 'directory.json').read_text()) if i['name'] == 'paper.pdf')
assert len(pdf) == pdf_item['size']
assert hashlib.sha1(b'blob ' + str(len(pdf)).encode() + b'\0' + pdf).hexdigest() == pdf_item['sha']
result = {'UTC': datetime.now(timezone.utc).isoformat(),
          'pin': 'adc7f1241b42e322a6451854ab7e4b4c146bf78a',
          'actual_directory_files': len(entries), 'main_internal_import_closure_files': len(reachable),
          'all_actual_directory_files_personally_read': True,
          'external_library_imports_are_not_fresh_kernel_validated': sorted(external),
          'source_author_hash_manifest_matches_actual_primary': True,
          'total_lines': sum(e['lines'] for e in entries),
          'total_bytes': sum(e['bytes'] for e in entries),
          'openai_pdf_git_blob_matches_actual_pinned_directory': True,
          'entries': entries}
(LANE / 'PRIMARY_COVERAGE.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k not in ('entries', 'external_library_imports_are_not_fresh_kernel_validated')}, indent=2))
