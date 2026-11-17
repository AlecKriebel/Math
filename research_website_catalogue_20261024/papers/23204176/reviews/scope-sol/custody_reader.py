"""Data-only source inventory and native metadata extraction; no project imports."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from html.parser import HTMLParser

ROOT = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
SOURCE = ROOT / 'papers/23204176/sources'
OWN = ROOT / 'papers/23204176/reviews/scope-sol'
ADOPTION = ROOT / 'verification/root-source190191-custody-adoption-20261117.json'
PINS = {'SOURCE_MANIFEST.json': '53be96c6f47deccccc173286d10bdf46b50df4f237c985f42f2da8a69d8c8ffb',
        'SOURCE_FINAL.json': 'f7bc05f4e7d56f0fbad45d77bdb4992d9fd92de8d976bdc5ff3b446f7dbfe9c8'}


def need(condition, reason):
    if not condition:
        raise AssertionError(reason)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inventory():
    rows = []
    def visit(path):
        st = path.lstat()
        rel = path.relative_to(SOURCE).as_posix()
        row = {'path': rel, 'mode_octal': oct(stat.S_IMODE(st.st_mode)),
               'hidden_component': any(p.startswith('.') and p != '.' for p in Path(rel).parts)}
        if stat.S_ISDIR(st.st_mode):
            children = sorted(path.iterdir(), key=lambda p: os.fsencode(p.name))
            row.update(kind='directory', empty=not children)
            rows.append(row)
            for child in children:
                visit(child)
        else:
            need(stat.S_ISREG(st.st_mode), 'no symlink or special source object')
            data = path.read_bytes()
            need(len(data) == st.st_size, 'file length stable while reading')
            row.update(kind='file', bytes=len(data), sha256=digest(data), md5=hashlib.md5(data).hexdigest())
            rows.append(row)
    visit(SOURCE)
    need(sum(r['kind'] == 'file' for r in rows) == 43, 'whole source43 files')
    need(sum(r['kind'] == 'directory' for r in rows) == 8, 'source root plus7 child directories')
    for name, pin in PINS.items():
        need(digest((SOURCE / name).read_bytes()) == pin, 'source terminal pin ' + name)
    need(digest(ADOPTION.read_bytes()) == '9ab699b60b7ac0a9be04db1211f144ccb6db852b573a71a18aa37bb2a4fa707b', 'root adoption pin')
    manifest = json.loads((SOURCE / 'SOURCE_MANIFEST.json').read_bytes())
    excluded = set(manifest['excluded_control_files'])
    need(excluded == set(PINS), 'only exact two existing terminal controls excluded')
    actual = {r['path']: r for r in rows if r['path'] not in excluded}
    expected = {r['path']: r for r in manifest['entries']}
    need(actual == expected, 'all source bytes modes hidden empty topology exact')
    for row in manifest['terminal_control_topology']:
        current = next(r for r in rows if r['path'] == row['path'])
        need(all(current[k] == v for k, v in row.items()), 'terminal mode/type exact')
    need(digest((SOURCE / 'zenodo-files/paper.pdf').read_bytes()) == '483a6edff90202ef4d31560049a32ce946dcd1c6a999ab5b1f25b66a8f326612', 'outer controlling PDF pin')
    return {'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'source_root': str(SOURCE),
            'files': 43, 'child_directories': 7, 'all_manifest_entries_exact': True,
            'root_adoption_sha256': digest(ADOPTION.read_bytes()), 'entries': rows}


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta, self.links, self.visible, self.scripts = [], [], [], []
        self.hidden = 0
        self.script = None

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == 'meta':
            self.meta.append(data)
        elif tag == 'link':
            self.links.append(data)
        if tag in ('script', 'style'):
            self.hidden += 1
            if tag == 'script':
                self.script = {'attributes': data, 'text': ''}
                self.scripts.append(self.script)
        if tag in ('p', 'div', 'h1', 'h2', 'h3', 'li', 'dt', 'dd', 'br'):
            self.visible.append('\n')

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.hidden -= 1
            self.script = None
        if tag in ('p', 'div', 'h1', 'h2', 'h3', 'li', 'dt', 'dd'):
            self.visible.append('\n')

    def handle_data(self, data):
        if self.script is not None:
            self.script['text'] += data
        elif not self.hidden:
            self.visible.append(data)


phase = sys.argv[1]
need(phase in ('before', 'after'), 'explicit source inventory phase')
target = OWN / ('SOURCE_' + phase.upper() + '.json')
need(not target.exists(), 'no overwrite of custody snapshot')
result = inventory()
if phase == 'after':
    old = json.loads((OWN / 'SOURCE_BEFORE.json').read_bytes())
    need(result['entries'] == old['entries'], 'entire source before/after preserved')
    result['whole_source_before_after_exact'] = True
target.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
if phase == 'before':
    html = (SOURCE / 'native-metadata/record-page.html').read_text()
    parser = Metadata()
    parser.feed(html)
    extracted = {'source': str(SOURCE / 'native-metadata/record-page.html'),
                 'source_sha256': digest(html.encode()), 'metadata_tags': parser.meta,
                 'link_tags': parser.links,
                 'json_scripts': [r for r in parser.scripts if 'json' in r['attributes'].get('type', '')]}
    output = OWN / 'NATIVE_HTML_METADATA.json'
    visible = OWN / 'NATIVE_HTML_VISIBLE.txt'
    need(not output.exists() and not visible.exists(), 'fresh metadata extracts')
    output.write_text(json.dumps(extracted, indent=2, sort_keys=True) + '\n')
    visible.write_text('\n'.join(line.strip() for line in ''.join(parser.visible).splitlines() if line.strip()) + '\n')
print(json.dumps({'phase': phase, 'files': result['files'], 'child_directories': result['child_directories'],
                  'exact': True, 'snapshot_sha256': digest(target.read_bytes())}, sort_keys=True))
