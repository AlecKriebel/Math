"""Bounded data-only legacy collector. Local Git objects; no network or code replay."""
import datetime
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import stat
import subprocess

M = Path('/Users/alec/Documents/Math')
P = M / 'research_website_catalogue_20261024'
OWN = P / 'verification/complex-retract-legacy-sol-20261117'
SRC = P / 'papers/23203270/sources'
NATIVE = 'a4ce3c37dad209339e490d18dcced6c48cf912d2'
RELEASED = 'd50dd343726978c0bc4a27ee81113f8f3ce4e3d6'
PATTERN = '23203270|complex.polynomial.retract|polynomial.retract|retract|cancellation|Costa'
COMMANDS = []

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def metadata(path):
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode), str(path)
    raw = path.read_bytes()
    return {'bytes': len(raw), 'SHA256': sha(raw), 'mode': format(stat.S_IMODE(info.st_mode), '04o')}

def save(name, value):
    with (OWN / name).open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')

def run(args, accepted=(0,)):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update({'GIT_OPTIONAL_LOCKS': '0', 'GIT_NO_LAZY_FETCH': '1', 'GIT_NO_REPLACE_OBJECTS': '1', 'GIT_TERMINAL_PROMPT': '0', 'LC_ALL': 'C'})
    start = utc()
    result = subprocess.run(args, cwd=M, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    number = len(COMMANDS) + 1
    stdout = 'command-%02d.stdout' % number
    stderr = 'command-%02d.stderr' % number
    (OWN / stdout).write_bytes(result.stdout)
    (OWN / stderr).write_bytes(result.stderr)
    COMMANDS.append({'started_UTC': start, 'completed_UTC': utc(), 'argv': args, 'exit_code': result.returncode, 'stdout': stdout, 'stderr': stderr, 'stdout_bytes': len(result.stdout), 'stderr_bytes': len(result.stderr), 'stdout_SHA256': sha(result.stdout), 'stderr_SHA256': sha(result.stderr)})
    save('COMMANDS-%02d.json' % number, COMMANDS[-1])
    assert result.returncode in accepted and result.stderr == b'', COMMANDS[-1]
    return result.stdout, result.returncode

def git(*args, accepted=(0,)):
    assert args and args[0] in {'rev-parse', 'for-each-ref', 'ls-tree', 'grep', 'cat-file'}
    return run(['/usr/bin/git', '--no-optional-locks', '-c', 'core.hooksPath=/dev/null', '-c', 'core.fsmonitor=false', '-c', 'gc.auto=0', '-c', 'maintenance.auto=false', *args], accepted)

def snapshot():
    refs = git('for-each-ref', '--format=%(refname) %(objectname)', 'refs/heads', 'refs/remotes/origin/main')[0].decode().splitlines()
    head = git('rev-parse', 'HEAD', 'refs/heads/main', 'refs/remotes/origin/main')[0].decode().splitlines()
    trees = {label: git('rev-parse', commit + ':docs')[0].decode().strip() for label, commit in [('native', NATIVE), ('released', RELEASED), ('observed_origin_main', head[2])]}
    return {'UTC': utc(), 'HEAD_main_origin_main': head, 'refs': refs, 'docs_trees': trees, 'native_files': {name: metadata(M / '.git' / name) for name in ['HEAD', 'index', 'config']}}

def source_census():
    files, directories = {}, {}
    stack = [SRC]
    while stack:
        root = stack.pop()
        for path in sorted(root.iterdir()):
            rel = path.relative_to(SRC).as_posix()
            kind = path.lstat().st_mode
            if stat.S_ISDIR(kind):
                directories[rel] = format(stat.S_IMODE(kind), '04o')
                stack.append(path)
            else:
                files[rel] = metadata(path)
    return {'root': str(SRC), 'root_mode': format(stat.S_IMODE(SRC.lstat().st_mode), '04o'), 'files': files, 'directories': directories}

class Headings(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.active = None
        self.titles = []
        self.h1 = []
        self.links = []
        self.attrs = []
    def handle_starttag(self, tag, attrs):
        if tag in ('title', 'h1'):
            self.active = tag
        if tag in ('a', 'link', 'meta'):
            self.attrs.append({'tag': tag, 'attributes': attrs})
            self.links.extend(v for k, v in attrs if k == 'href' and v is not None)
    def handle_endtag(self, tag):
        if self.active == tag:
            self.active = None
    def handle_data(self, data):
        if self.active == 'title':
            self.titles.append(data)
        elif self.active == 'h1':
            self.h1.append(data)

started = utc()
initial = snapshot()
save('START.json', initial)
assert initial['HEAD_main_origin_main'][:2] == [NATIVE, NATIVE]
assert initial['docs_trees']['native'] == '6ccfd5ab446400dc7fb3933dcc2e374cb415fa90'
assert initial['docs_trees']['released'] == 'e63ba1f227e5aa2f0e06fd6a52b36afa1531a4d0'
source_before = source_census()
assert (len(source_before['files']), len(source_before['directories'])) == (97, 12)
save('SOURCE_GUARDS_BEFORE.json', source_before)
clearance = P / 'verification/root-clearance-23203270-20261117.json'
review = P / 'papers/23203270/reviews/root-continuation-20261117/ROOT_REVIEW.md'
assert metadata(clearance)['SHA256'].startswith('7b7096d4')
assert metadata(review)['SHA256'] == '3a8c154c15491194fc85df87faabe47a4ed65e2d644f4c02b6cf27749a093300'
save('IDENTITY_PINS.json', {'clearance': {'path': str(clearance), **metadata(clearance)}, 'full_ROOT_REVIEW': {'path': str(review), **metadata(review)}})
native_assets = {}
for name, size, digest in [('source-and-verification.zip', 153906, '1d5fad97e53c8e265c1e70485182976d9882f26e4f58d0ff430db354e8ec2620'), ('paper.pdf', 74424, 'c579ec3442f4bcdf68ed737ad8bc65328682158845ed2e14e6636b2b119f52c6')]:
    path = SRC / 'zenodo-files' / name
    raw = path.read_bytes()
    assert len(raw) == size and sha(raw) == digest
    native_assets[name] = {'path': str(path), **metadata(path), 'Git_blob_OID': hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()}
save('NATIVE_ASSETS.json', native_assets)
searches, inventories, pages, asset_matches = {}, {}, [], []
physical, physical_exit = run(['rg', '-l', '-i', '--hidden', '--no-ignore', '--glob', '*.html', PATTERN, 'docs'], (0, 1))
searches['physical_docs'] = {'exit_code': physical_exit, 'matching_paths': physical.decode().splitlines()}
for label, commit in [('native', NATIVE), ('released', RELEASED)]:
    raw = git('ls-tree', '-r', '-z', '--full-tree', commit, '--', 'docs')[0]
    rows = []
    for unit in raw.split(b'\0'):
        if not unit:
            continue
        header, name = unit.split(b'\t', 1)
        mode, kind, oid = header.decode().split()
        rows.append({'path': name.decode(), 'mode': mode, 'type': kind, 'OID': oid})
    inventories[label] = {'commit': commit, 'docs_tree': initial['docs_trees'][label], 'leaves': rows}
    found, code = git('grep', '-I', '-l', '-i', '-E', PATTERN, commit, '--', 'docs', accepted=(0, 1))
    paths = [line.split(':', 1)[1] for line in found.decode().splitlines()]
    searches[label] = {'commit': commit, 'exit_code': code, 'matching_paths': paths, 'path_keyword_matches': [r['path'] for r in rows if re.search('retract|cancell|polynomial|23203270|complex', r['path'], re.I)]}
    selected = {r['path'] for r in rows if r['path'] in paths and r['path'].endswith('.html')}
    for name, asset in native_assets.items():
        for row in rows:
            if row['OID'] != asset['Git_blob_OID']:
                continue
            body = git('cat-file', 'blob', row['OID'])[0]
            assert body == Path(asset['path']).read_bytes()
            asset_matches.append({'snapshot': label, 'commit': commit, 'path': row['path'], 'native_asset': name, 'whole_bytes_equal': True, 'SHA256': sha(body), 'bytes': len(body), 'OID': row['OID']})
            parent = Path(row['path']).parent
            selected.update(r['path'] for r in rows if r['path'].endswith('.html') and Path(r['path']).parent == parent)
    mapping = {row['path']: row for row in rows}
    for name in sorted(selected):
        row = mapping[name]
        body = git('cat-file', 'blob', row['OID'])[0]
        filename = label + '--' + hashlib.sha256(name.encode()).hexdigest()[:16] + '.html'
        (OWN / filename).write_bytes(body)
        parser = Headings()
        parser.feed(body.decode('utf-8'))
        pages.append({'snapshot': label, 'commit': commit, 'path': name, 'saved_whole_HTML': filename, 'OID': row['OID'], 'bytes': len(body), 'SHA256': sha(body), 'title': parser.titles, 'h1': parser.h1, 'DOIs': sorted(set(re.findall(r'10\.5281/zenodo\.\d+', body.decode()))), 'hrefs': parser.links, 'head_attributes': parser.attrs})
save('DOCS_INVENTORIES.json', inventories)
save('SEARCH_RESULTS.json', searches)
save('MATCHED_HTML.json', pages)
save('WHOLE_ASSET_MATCHES.json', asset_matches)
source_after = source_census()
assert source_after == source_before
save('SOURCE_GUARDS_AFTER.json', source_after)
final = snapshot()
save('END.json', final)
assert final['HEAD_main_origin_main'][:2] == initial['HEAD_main_origin_main'][:2] and final['native_files'] == initial['native_files']
assert [x for x in final['refs'] if x.startswith('refs/heads/')] == [x for x in initial['refs'] if x.startswith('refs/heads/')]
assert final['docs_trees']['native'] == initial['docs_trees']['native'] and final['docs_trees']['released'] == initial['docs_trees']['released'] and final['docs_trees']['observed_origin_main'] == initial['docs_trees']['observed_origin_main']
save('COLLECTION.json', {'schema': 'bounded-complex-retract-local-legacy-data-v1', 'started_UTC': started, 'completed_UTC': utc(), 'source_files': 97, 'source_child_directories': 12, 'native_commit': NATIVE, 'released_commit': RELEASED, 'Git_command_count': sum(x['argv'][0] == '/usr/bin/git' for x in COMMANDS), 'command_count': len(COMMANDS), 'matched_HTML_snapshots': len(pages), 'whole_asset_matches': len(asset_matches), 'literal_search_exit_codes': {k: v['exit_code'] for k, v in searches.items()}, 'native_guards_and_sources_unchanged': True, 'network_requests': 0, 'scientific_or_archived_code_executed': False, 'status': 'DATA_COLLECTED_FOR_PERSONAL_CORRESPONDENCE_REVIEW', 'completion_percent': 65})
print(json.dumps({'status': 'DATA_COLLECTED_FOR_PERSONAL_CORRESPONDENCE_REVIEW', 'pages': len(pages), 'asset_matches': len(asset_matches), 'commands': len(COMMANDS)}))
