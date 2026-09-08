#!/usr/bin/env python3
"""Check the frozen source and the structure of this read-only referee record."""
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PROJECT = HERE.parent.name
inventory = json.loads((HERE / 'SOURCE_INVENTORY.json').read_text())
expected = {row['path']: row for row in inventory['files']}
snapshot = HERE / 'source_snapshot'
actual = {str(p.relative_to(snapshot)) for p in snapshot.rglob('*') if p.is_file()}
if actual != set(expected):
    raise RuntimeError('Snapshot file set differs from the source inventory')
for relative, row in expected.items():
    data = (snapshot / relative).read_bytes()
    if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
        raise RuntimeError('Snapshot content differs: ' + relative)
archive = subprocess.check_output(['git', 'archive', inventory['commit'], PROJECT], cwd=REPO)
if hashlib.sha256(archive).hexdigest() != inventory['archive_sha256']:
    raise RuntimeError('Fresh archive differs from preserved archive digest')

# Use Git's ignore policy so disposable builds and rendered images stay outside
# the retained evidence set. Parse programs but do not execute their mutations.
listed = subprocess.check_output(
    ['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard', '--',
     str(HERE.relative_to(REPO))], cwd=REPO)
files = sorted({REPO / p.decode() for p in listed.split(b'\0') if p})
counts = {'python': 0, 'json': 0, 'jsonl_rows': 0, 'report_links': 0}
for path in files:
    if path.suffix == '.py':
        ast.parse(path.read_text(), filename=str(path))
        counts['python'] += 1
    elif path.suffix == '.json':
        json.loads(path.read_text())
        counts['json'] += 1
    elif path.suffix == '.jsonl':
        for line in path.read_text().splitlines():
            if line.strip():
                json.loads(line)
                counts['jsonl_rows'] += 1
report = (HERE / 'REFEREE_REPORT.md').read_text()
for link in re.findall(r'\]\(([^)]+)\)', report):
    if link.startswith(('https://', 'http://', '#')):
        continue
    if not (HERE / link).is_file():
        raise RuntimeError('Broken report evidence link: ' + link)
    counts['report_links'] += 1
result = {
    'status': 'PASS', 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
    'target_commit': inventory['commit'], 'source_files': len(expected),
    'source_bytes': sum(row['bytes'] for row in expected.values()),
    'fresh_archive_sha256': hashlib.sha256(archive).hexdigest(),
    'evidence_structure_checks': counts,
    'scope': 'Snapshot identity, fresh archive identity, retained Python/JSON syntax, '
             'and root report evidence links. Scientific and build outcomes are '
             'supported by the separately retained referee scripts and logs.'
}
(HERE / 'AUDIT_EVIDENCE_CHECK.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
