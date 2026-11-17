"""Passive source custody and native-page text reader; no source execution."""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser

LANE = Path(__file__).resolve().parent
SOURCE = LANE.parent.parent / 'sources'
PINS = {
    'SOURCE_FINAL.json': 'b68fbb425b7d910a2508c46ff311491a1c797568dcf39d3c7deb0a0545e1afd5',
    'SOURCE_MANIFEST.json': 'afa64c126da0aabc4a44ec242553e5b2354540eb1b0b60e55ab7b1a9855a09be',
}

def inventory():
    result = []
    for path in [SOURCE] + sorted(SOURCE.rglob('*')):
        info = path.lstat()
        relative = str(path.relative_to(SOURCE))
        entry = {'path': relative, 'mode_octal': oct(stat.S_IMODE(info.st_mode))}
        if stat.S_ISDIR(info.st_mode):
            entry.update(kind='directory', empty=not any(path.iterdir()))
        elif stat.S_ISREG(info.st_mode):
            data = path.read_bytes()
            entry.update(kind='file', bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                         md5=hashlib.md5(data).hexdigest(), empty=not data)
        else:
            raise RuntimeError('Unexpected source object: ' + relative)
        result.append(entry)
    return result

class NativePage(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.suppressed = 0
        self.visible = []
        self.metadata = []
        self.jsonld = []
        self.in_jsonld = False
    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag in ('style', 'script'):
            self.suppressed += 1
        if tag == 'script' and attributes.get('type') == 'application/ld+json':
            self.in_jsonld = True
        if tag in ('meta', 'link'):
            self.metadata.append({'tag': tag, 'attributes': attributes})
        if tag in ('p', 'div', 'section', 'h1', 'h2', 'h3', 'li', 'dt', 'dd', 'br'):
            self.visible.append('\n')
    def handle_endtag(self, tag):
        if tag in ('style', 'script'):
            self.suppressed -= 1
        if tag == 'script':
            self.in_jsonld = False
        if tag in ('p', 'div', 'section', 'h1', 'h2', 'h3', 'li', 'dt', 'dd'):
            self.visible.append('\n')
    def handle_data(self, data):
        if self.in_jsonld:
            self.jsonld.append(data)
        if not self.suppressed:
            self.visible.append(data)

phase = sys.argv[1]
assert phase in ('before', 'after')
entries = inventory()
actual = {entry['path']: entry for entry in entries}
assert sum(e['kind'] == 'file' for e in entries) == 55
assert sum(e['kind'] == 'directory' for e in entries) - 1 == 14
for name, digest in PINS.items():
    assert actual[name]['sha256'] == digest, name
manifest = json.loads((SOURCE / 'SOURCE_MANIFEST.json').read_text())
assert set(manifest['excluded_control_files']) == set(PINS)
assert {e['path'] for e in manifest['entries']} | set(PINS) == set(actual)
for expected in manifest['entries']:
    for key in ('kind', 'mode_octal', 'empty', 'bytes', 'sha256', 'md5'):
        if key in expected:
            assert actual[expected['path']][key] == expected[key], (expected['path'], key)
result = {'UTC': datetime.now(timezone.utc).isoformat(), 'phase': phase,
          'source': str(SOURCE), 'file_count': 55, 'child_directory_count': 14,
          'external_pins': PINS, 'manifest_exact': True, 'entries': entries}
if phase == 'after':
    before = json.loads((LANE / 'SOURCE_BEFORE.json').read_text())
    assert before['entries'] == entries, 'Source custody differs from BEFORE'
    result['before_after_exact'] = True
else:
    page = NativePage()
    page.feed((SOURCE / 'native-metadata/record-page.html').read_text())
    page.close()
    visible = '\n'.join(line.strip() for line in ''.join(page.visible).splitlines() if line.strip())
    (LANE / 'NATIVE_PAGE_VISIBLE.txt').write_text(visible + '\n')
    (LANE / 'NATIVE_PAGE_META.json').write_text(json.dumps(
        {'metadata': page.metadata, 'jsonld': page.jsonld}, indent=2) + '\n')
(LANE / ('SOURCE_' + phase.upper() + '.json')).write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({key: value for key, value in result.items() if key != 'entries'}, indent=2))
