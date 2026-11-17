"""One passive D4 exact-work correspondence route; raw local Git data only."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
from html.parser import HTMLParser
import hashlib
import io
import json
import os
import re
import stat
import unicodedata
import zipfile
import subprocess

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
M = P.parent
A = P / 'verification/d4-canonical-potential-legacy-sol-20261117'
FAILURE_ROOT = P / 'verification/mink-riesz-k3-runtime-sol-20261117/d4-legacy-failure-20261117'
GIT_RESULTS = []
SRC = P / 'papers/23439776/sources'
WRITER = P / 'verification/d4-canonical-potential-editorial-v2-sol-20261117'
REVIEW = P / 'papers/23439776/reviews/root-continuation-20261117/ROOT_REVIEW.md'
CLEARANCE = P / 'verification/root-clearance-23439776-20261117.json'
ADOPTION = P / 'verification/root-d4-final-adoption-20261117.json'
NATIVE = 'a4ce3c37dad209339e490d18dcced6c48cf912d2'
RELEASED = 'b510aecb1a5ad89bc0efa0e2798aefa9f7a928c6'
TREES = {NATIVE: '6ccfd5ab446400dc7fb3933dcc2e374cb415fa90',
         RELEASED: 'e63ba1f227e5aa2f0e06fd6a52b36afa1531a4d0'}
ASSETS = [('Canonical_W_D4_Verification_v1.0.zip', 63134,
           'f5ccf88733160c457423613fa1e0e329a562a29bad15bd71ed118114e9b98eef'),
          ('Canonical_W_D4_Note_v1.0.pdf', 77127,
           '1edcf5f41308f1369f45dde8aa75111b69d73c56a5a1cdf6724f636ee2d9dcb1')]
FALSE = {
 'papers/exceptional-ybe-d4/index.html': ('Yang–Baxter', 'papers/exceptional-ybe-d4/paper.pdf', 194003,
    'a769689a4b5b9c48bf675f79d3b80916a7821ad5a8db0b9ec246df460dffb8de'),
 'papers/exceptional-ybe-constraints/index.html': ('Low-Schmidt', 'papers/exceptional-ybe-constraints/paper.pdf', 181708,
    '9ccbda6d98c172dd1a6761a06fc0934cb7b5293d5629ac645a79867fae1534a4'),
 'papers/symmetric-keller-and-vanishing/index.html': ('44-variable', 'papers/symmetric-keller-and-vanishing/paper.pdf', 88807,
    '50c08855d509b6f8c4e3e048f489347c453fa4e120621c1bf5e289bbadae3cb0')}

def require(value, reason):
    if not value:
        raise RuntimeError(reason)

def utc():
    return datetime.now(timezone.utc).isoformat()

def digest(data):
    return hashlib.sha256(data).hexdigest()

def data_pin(data):
    return {'bytes': len(data), 'SHA256': digest(data)}

def pin(path):
    st = path.lstat()
    require(stat.S_ISREG(st.st_mode), 'regular guarded file: ' + str(path))
    return {**data_pin(path.read_bytes()), 'mode': format(stat.S_IMODE(st.st_mode), '04o')}

def load(path):
    return json.loads(path.read_bytes())

def put(name, obj):
    with (A / name).open('x') as handle:
        handle.write(json.dumps(obj, indent=2) + '\n')

def snap(root):
    if not os.path.lexists(root):
        return {'root': str(root), 'absent': True}
    files, dirs, seen = {}, {}, set()
    def walk(path):
        st = path.lstat()
        require(stat.S_ISDIR(st.st_mode) and (st.st_dev, st.st_ino) not in seen, 'unique real directory')
        seen.add((st.st_dev, st.st_ino))
        children = sorted(path.iterdir())
        name = path.relative_to(root).as_posix()
        dirs[name] = {'mode': format(stat.S_IMODE(st.st_mode), '04o'), 'empty': not children,
                      'hidden': any(x.startswith('.') for x in Path(name).parts if x != '.')}
        for child in children:
            st = child.lstat()
            if stat.S_ISDIR(st.st_mode):
                walk(child)
            else:
                require(stat.S_ISREG(st.st_mode) and (st.st_dev, st.st_ino) not in seen, 'unique real regular file')
                seen.add((st.st_dev, st.st_ino))
                files[child.relative_to(root).as_posix()] = pin(child)
    walk(root)
    return {'root': str(root), 'files': files, 'directories': dirs,
            'regular_files': len(files), 'child_directories': len(dirs) - 1}

def capture():
    native = {name: pin(M / '.git' / name) for name in ['HEAD', 'index', 'config', 'packed-refs']}
    native['local_heads'] = snap(M / '.git/refs/heads')
    return {'native_M': native, 'docs': snap(M / 'docs'), 'source': snap(SRC), 'writer': snap(WRITER),
            'specific_root': {str(x.relative_to(P)): pin(x) for x in [REVIEW, CLEARANCE, ADOPTION]}}

def mode(value):
    return format(int(value, 8), '04o')

def authenticate(before):
    source, writer = before['source'], before['writer']
    require((source['regular_files'], source['child_directories']) == (72, 7), 'source72/7')
    require((writer['regular_files'], writer['child_directories']) == (30, 1), 'writer30/1')
    sf, sm = load(SRC / 'SOURCE_FINAL.json'), load(SRC / 'SOURCE_MANIFEST.json')
    require(sf['schema'] == 'opaque-native-source-final-v1' and sm['schema'] == 'opaque-native-source-manifest-v1', 'actual source schemas')
    require(source['files']['SOURCE_FINAL.json']['SHA256'] == 'e95d8717aee6b39ba23b73d85462a20340c823ff3ee5a09bc66470775a5b5a03', 'externally fixed source final')
    require(source['files']['SOURCE_MANIFEST.json']['SHA256'] == sf['SOURCE_MANIFEST']['SHA256'] and
            source['files']['SOURCE_MANIFEST.json']['bytes'] == sf['SOURCE_MANIFEST']['bytes'], 'source manifest terminal pin')
    excluded = sm['root_controls_excluded_from_own_list']
    require(excluded == ['SOURCE_MANIFEST.json', 'SOURCE_FINAL.json'] and sm['exact_controls_existed_before_enumeration'], 'actual exact source controls')
    rows = {x['path']: {k: x[k] for k in ['bytes', 'SHA256']} | {'mode': mode(x['mode'])} for x in sm['files']}
    require(set(rows) == set(source['files']) - set(excluded) and all(source['files'][k] == v for k, v in rows.items()), 'all source payload records')
    require(set(sm['actual_file_paths_including_controls']) == set(source['files']) and sm['ordinary_files_including_controls'] == 72, 'complete source file set')
    require({x['path']: mode(x['mode']) for x in sm['directories']} ==
            {k: v['mode'] for k, v in source['directories'].items() if k != '.'} and
            source['directories']['.']['mode'] == mode(sm['root_mode']), 'source full directories/modes')
    wf, wm = load(WRITER / 'FINAL.json'), load(WRITER / 'FINAL_MANIFEST.json')
    require(writer['files']['FINAL.json']['SHA256'] == '36eb02cf832f6734d40610a199f523b866e16505ee5e5d1ed252b63f2d27db4a' and
            writer['files']['FINAL_MANIFEST.json']['SHA256'] == '37b95cdf70d9cd8a4c7f521b6961bcbc52d4ff9726d2c5df7f2528bbda307a72', 'external writer terminal pair')
    require(wf['schema'] == 'private-D4-V2-FINAL-v1' and wm['schema'] == 'finite-private-D4-V2-complete-namespace-v1', 'actual writer schemas')
    terminals = [x['path'] for x in wm['terminal_pair']]
    require(terminals == ['FINAL_MANIFEST.json', 'FINAL.json'] and all(x['recursive_hash_excluded'] for x in wm['terminal_pair']), 'actual writer terminal pair schema')
    require(set(wm['payload_files']) == set(writer['files']) - set(terminals), 'whole writer file set')
    for name, row in wm['payload_files'].items():
        require(writer['files'][name] == {k: row[k] for k in ['bytes', 'SHA256']} | {'mode': mode(row['mode'])}, 'whole writer payload ' + name)
        require(hashlib.md5((WRITER / name).read_bytes()).hexdigest() == row['MD5'], 'declared writer MD5 ' + name)
    require({k: mode(v) for k, v in wm['directories'].items()} ==
            {k: v['mode'] for k, v in writer['directories'].items() if k != '.'}, 'writer directory modes')
    require(writer['directories']['.']['mode'] == mode(wm['root_mode']) and wm['file_count'] == 30 and wm['child_directory_count'] == 1, 'writer actual extent/rootmode')
    for row in wm['terminal_pair']:
        require(writer['files'][row['path']]['bytes'] == row['bytes'] and writer['files'][row['path']]['mode'] == mode(row['mode']), 'writer terminal metadata')
    require(before['specific_root'][str(REVIEW.relative_to(P))] == {'bytes': 11832, 'SHA256': '4836979d83da2747da766a2defc76bc0e5bbd6b48b25025c0de434aefd580e62', 'mode': '0644'}, 'whole accepted review pin')
    require(pin(CLEARANCE)['SHA256'] == 'd6a171c2f2a3b5480bd5bdc71e4c9fcb63bb2130bea2524e7e9df3cb9f6c6590' and
            pin(ADOPTION)['SHA256'] == '33f6646b0ae108700ba3b1571ac8ddb1c12060d98aa560f6ccd017cad88e55da', 'specific root receipt pins')
    clearance = load(CLEARANCE)
    require(clearance['record_id'] == '23439776' and clearance['sheet_row'] == 171 and clearance['follow_up'] is None and
            clearance['status'] == 'PASS_ORIGINAL_HISTORICAL_CANONICAL_W_COUNTEREXAMPLE', 'bounded accepted identity disposition')

class GitObjects:
    """Read existing local objects with the previously used native cat-file protocol."""
    def __init__(self):
        self.cache = {}
        self.reads = []

    def fetch(self, oids):
        selected = sorted(set(oids) - set(self.cache))
        if not selected:
            return
        require(all(re.fullmatch('[0-9a-f]{40}', oid) for oid in selected), 'literal existing object OIDs')
        request = ''.join(oid + '\n' for oid in selected).encode()
        env = os.environ.copy()
        for key in list(env):
            if key.startswith('GIT_'):
                env.pop(key)
        env.update({'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': '/dev/null',
                    'GIT_NO_LAZY_FETCH': '1', 'GIT_NO_REPLACE_OBJECTS': '1',
                    'GIT_TERMINAL_PROMPT': '0', 'GIT_OPTIONAL_LOCKS': '0',
                    'GIT_ALLOW_PROTOCOL': ''})
        argv = ['/usr/bin/git', '--no-optional-locks', '--git-dir=' + str(M / '.git'),
                '--work-tree=' + str(M), '-c', 'protocol.allow=never',
                '-c', 'core.hooksPath=/dev/null', '-c', 'core.fsmonitor=false',
                '-c', 'gc.auto=0', '-c', 'maintenance.auto=false', 'cat-file', '--batch']
        result = subprocess.run(argv, input=request, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                env=env, cwd=M, check=False)
        GIT_RESULTS.append((result.stdout, result.stderr, result.returncode))
        self.reads.append({'requested_objects': len(selected), 'request_SHA256': digest(request),
                           'exit_code': result.returncode, 'stdout_pin': data_pin(result.stdout),
                           'stderr_pin': data_pin(result.stderr), 'network_protocols_disabled': True})
        require(result.returncode == 0 and result.stderr == b'', 'read-only local cat-file returned success')
        cursor = 0
        for expected in selected:
            end = result.stdout.index(b'\n', cursor)
            fields = result.stdout[cursor:end].split(b' ')
            require(len(fields) == 3 and fields[0].decode() == expected and
                    fields[1] in [b'commit', b'tree', b'blob', b'tag'] and fields[2].isdigit(),
                    'literal complete local object response header')
            size = int(fields[2])
            body = result.stdout[end + 1:end + 1 + size]
            cursor = end + 1 + size
            require(len(body) == size and result.stdout[cursor:cursor + 1] == b'\n',
                    'complete local object response body and separator')
            cursor += 1
            require(hashlib.sha1(fields[1] + b' ' + str(size).encode() + b'\0' + body).hexdigest() == expected,
                    'whole actual local Git object SHA1')
            self.cache[expected] = (fields[1], body)
        require(cursor == len(result.stdout), 'entire opaque local response consumed')

    def get(self, oid):
        self.fetch([oid])
        return self.cache[oid]

    def tree(self, oid):
        kind, raw = self.get(oid)
        require(kind == b'tree', 'actual tree object')
        cursor, rows, names = 0, [], set()
        while cursor < len(raw):
            space = raw.index(b' ', cursor)
            end = raw.index(b'\0', space + 1)
            mode_bytes, name = raw[cursor:space], raw[space + 1:end]
            require(name not in names and name not in [b'', b'.', b'..'] and b'/' not in name,
                    'unique simple tree name')
            names.add(name)
            require(end + 21 <= len(raw), 'complete tree entry OID')
            rows.append((mode_bytes.decode(), name.decode('utf-8'), raw[end + 1:end + 21].hex()))
            cursor = end + 21
        return rows

    def docs(self, commit, expected):
        kind, raw = self.get(commit)
        require(kind == b'commit', 'actual specified commit')
        line = raw.split(b'\n', 1)[0]
        require(re.fullmatch(b'tree [0-9a-f]{40}', line) is not None, 'literal commit root tree')
        docs = [x for x in self.tree(line[5:].decode()) if x[1] == 'docs']
        require(docs == [('40000', 'docs', expected)], 'actual exact commit/docs association')
        leaves, directories, pending = {}, {}, [(expected, '')]
        while pending:
            self.fetch(oid for oid, prefix in pending)
            following = []
            for oid, prefix in pending:
                require(prefix not in directories, 'unique complete docs subtree')
                directories[prefix] = oid
                for filemode, name, child in self.tree(oid):
                    path = prefix + ('/' if prefix else '') + name
                    if filemode == '40000':
                        following.append((child, path))
                    else:
                        require(filemode in ['100644', '100755'] and path not in leaves,
                                'regular unique docs blob')
                        leaves[path] = {'Git_mode': filemode, 'OID': child}
            pending = following
        self.fetch(row['OID'] for row in leaves.values())
        for row in leaves.values():
            kind, body = self.get(row['OID'])
            require(kind == b'blob', 'actual complete docs blob')
            row.update(data_pin(body))
        return leaves, directories

    def close(self):
        pass

class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.skip, self.meta = [], 0, []
    def handle_starttag(self, tag, attrs):
        if tag in ['script', 'style']:
            self.skip += 1
        if tag == 'meta':
            values = dict(attrs)
            self.meta.append(values.get('content', ''))
    def handle_endtag(self, tag):
        if tag in ['script', 'style']:
            self.skip -= 1
    def handle_data(self, value):
        if not self.skip:
            self.parts.append(value)

def normalize(text):
    return ''.join(x for x in unicodedata.normalize('NFKD', text).casefold() if x.isalnum())

def scan_view(label, files, getter):
    strong = ['23439776', 'canonicalpotential', 'canonicalw', 'ghkk', 'schumann', 'spin8', 'stringcone', 'chamberansatz']
    matches, textual, archive_members = [], [], []
    assets = {h: name for name, size, h in ASSETS}
    def container(path, raw, depth=0):
        require(depth <= 6, 'bounded docs nested container depth')
        if not raw.startswith(b'PK\x03\x04'):
            return
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            for member in archive.infolist():
                if member.is_dir():
                    continue
                require(member.file_size < 536870912, 'finite docs archive member')
                data = archive.read(member)
                record = {'container': path, 'member': member.filename, **data_pin(data)}
                archive_members.append(record)
                if digest(data) in assets:
                    matches.append({'path': path + '!' + member.filename, 'identity': assets[digest(data)]})
                if data.startswith(b'PK\x03\x04'):
                    container(path + '!' + member.filename, data, depth + 1)
    for path, record in sorted(files.items()):
        raw = getter(path)
        require(data_pin(raw) == {k: record[k] for k in ['bytes', 'SHA256']}, 'whole view buffer identity')
        if digest(raw) in assets:
            matches.append({'path': path, 'identity': assets[digest(raw)]})
        container(path, raw)
        if PurePosixPath(path).suffix.casefold() in ['.html', '.htm', '.md', '.txt', '.json', '.xml', '.tex', '.bib', '.cff']:
            text = raw.decode('utf-8')
            if path.endswith(('.html', '.htm')):
                parsed = Text()
                parsed.feed(text)
                text = ' '.join(parsed.parts + parsed.meta)
            folded = normalize(text)
            hits = [word for word in strong if word in folded]
            if hits:
                textual.append({'path': path, 'identity_terms': hits, **data_pin(raw)})
    false = []
    for path, (phrase, pdf, size, sha) in FALSE.items():
        require(path in files and pdf in files, 'whole concrete false positive and linked asset present')
        html, binary = getter(path), getter(pdf)
        require(phrase in html.decode() and binary.startswith(b'%PDF-') and digest(binary) not in assets,
                'actual distinct false-positive work and PDF identity ' + path)
        physical_html = (M / 'docs' / path).read_bytes()
        identical = html == physical_html
        saved = None
        if not identical:
            saved = 'historical-false-' + digest(html) + '.html'
            destination = A / saved
            if not destination.exists():
                with destination.open('xb') as handle:
                    handle.write(html)
            else:
                require(destination.read_bytes() == html, 'same whole historical public article')
        if label == 'physical Math/docs':
            require(data_pin(binary) == {'bytes': size, 'SHA256': sha}, 'actual personally read physical false-positive PDF pin')
        false.append({'article': path, 'article_pin': data_pin(html), 'linked_PDF': pdf, 'PDF_pin': data_pin(binary),
                      'whole_article_identical_to_personally_read_physical_article': identical,
                      'differing_whole_public_article_saved_for_personal_read': saved, 'exact_target': False})
    return {'view': label, 'files': len(files), 'whole_native_asset_matches': matches, 'strong_text_identity_candidates': textual,
            'all_archive_member_count': len(archive_members), 'all_archive_member_fingerprints': archive_members,
            'concrete_false_positives': false}

def main():
    require(Path(__file__).resolve() == A / 'read_legacy_once.py' and not (A / 'RESULTS.json').exists(), 'one fresh fixed correspondence route')
    require(not os.path.lexists(FAILURE_ROOT), 'approved private failure-only path absent before first invocation')
    started = utc()
    before = capture()
    put('BEFORE.json', {'UTC': started, 'snapshot': before})
    authenticate(before)
    native = before['native_M']
    require(native['index']['SHA256'] == '91b10d938f7d737226662bbff3b07016dcc0e501376a045811ab4e930c6fbb11' and
            (M / '.git/HEAD').read_bytes() == b'ref: refs/heads/main\n', 'exact held native Math index/HEAD')
    heads = dict(line.split(' ', 1)[::-1] for line in (M / '.git/packed-refs').read_text().splitlines() if line and not line.startswith(('#', '^')))
    loose = M / '.git/refs/heads/main'
    require((loose.read_text().strip() if loose.exists() else heads['refs/heads/main']) == NATIVE, 'actual resolved native main')
    model, api = load(WRITER / 'MODEL.json'), load(SRC / 'record.response.body')
    tex = SRC / 'published-source/container-001/tree/manuscript/main.tex'
    require(pin(tex)['SHA256'] == 'd15c70dcc7ee0744a6ea34cd72049abacddebb43dd7034becd8d6fa153d86c22', 'whole native TeX identity')
    abstract = tex.read_text().split('\\begin{abstract}', 1)[1].split('\\end{abstract}', 1)[0]
    require(abstract == model['abstract']['literal_source_TeX_span'], 'whole native abstract span')
    rendered = abstract
    for row in model['abstract']['literal_rendering_replacements']:
        rendered = rendered.replace(row['from'], row['to'])
    rendered = ' '.join(rendered.split())
    require(rendered == model['abstract']['normalized_full_text'] and digest(rendered.encode()) == model['abstract']['normalized_SHA256'], 'exact normalized abstract')
    require(api['id'] == 23439776 and api['metadata']['version'] == model['native_version'] == '1.0' and
            api['metadata']['publication_date'] == model['native_publication_date'] == '2026-10-17' and
            'later string-coordinate converse is not refuted' in api['metadata']['description'], 'full actual API identity and explicit boundary')
    require([x['key'] for x in api['files']] == [x[0] for x in ASSETS] ==
            [x['native_filename'] for x in model['native_assets_in_original_order']], 'actual native ZIP then PDF order')
    for i, (name, size, sha) in enumerate(ASSETS):
        raw = (SRC / 'assets' / name).read_bytes()
        require(data_pin(raw) == {'bytes': size, 'SHA256': sha} and raw == (WRITER / 'private-page' / name).read_bytes(), 'whole native/writer asset identity')
        require(api['files'][i]['size'] == size and api['files'][i]['checksum'] == 'md5:' + hashlib.md5(raw).hexdigest(), 'actual API asset metadata')
    article = (WRITER / 'private-page/index.html').read_text()
    require('two monomials have X₆ exponent −2' in article and '22 distinct monomials' in article and
            'The later string-coordinate converse is not refuted.' in article and model['actual_canonical'] is None and
            model['legacy_redirect'] is None and model['follow_up'] is None and not model['publication_authority'], 'whole accepted private identity/boundary only')
    physical = before['docs']
    require(physical['regular_files'] == 257, 'complete observed physical docs extent')
    observations = [scan_view('physical Math/docs', physical['files'], lambda path: (M / 'docs' / path).read_bytes())]
    git = GitObjects()
    tree_maps = {}
    try:
        for commit, tree in TREES.items():
            files, directories = git.docs(commit, tree)
            tree_maps[commit] = {'docs_tree': tree, 'files': files, 'directories': directories}
            observations.append(scan_view('local commit ' + commit, files, lambda path, rows=files: git.get(rows[path]['OID'])[1]))
    finally:
        git.close()
    require(all(not row['whole_native_asset_matches'] and not row['strong_text_identity_candidates'] for row in observations),
            'no exact asset or strong identity candidate in three bounded complete views')
    native_files = tree_maps[NATIVE]['files']
    common = set(native_files) & set(physical['files'])
    comparison = {'physical_only_paths': sorted(set(physical['files']) - set(native_files)),
        'native_only_paths': sorted(set(native_files) - set(physical['files'])),
        'common_different_buffers': sorted(path for path in common if {k: native_files[path][k] for k in ['bytes', 'SHA256']} !=
                                          {k: physical['files'][path][k] for k in ['bytes', 'SHA256']})}
    after = capture()
    require(after == before, 'whole native/docs/source/writer/specific-root before-after custody exact')
    put('AFTER.json', {'UTC': utc(), 'snapshot': after})
    put('IDENTITY_DATA.json', {'schema': 'bounded-D4-exact-work-correspondence-data-v1', 'record': '23439776', 'row': 171,
        'native_assets_in_original_order': [{'name': n, 'bytes': b, 'SHA256': h} for n, b, h in ASSETS],
        'views': observations, 'complete_local_tree_maps': tree_maps, 'physical_versus_native_docs': comparison,
        'raw_private_index_config_or_journals_copied': False, 'readonly_local_Git_reads_derived_only': git.reads,
        'canonical': None, 'redirect': None, 'follow_up': None})
    put('RESULTS.json', {'schema': 'bounded-D4-legacy-correspondence-result-v1', 'UTC_start': started, 'UTC_end': utc(),
        'status': 'PASS_NO_EXACT_WORK_LEGACY_CORRESPONDENCE_IN_FIXED_VIEWS', 'completion_percent_assigned_correspondence_only': 100,
        'record': '23439776', 'row': 171, 'physical_docs_files': 257,
        'local_commit_docs_pairs': TREES, 'complete_three_view_checks': True,
        'whole_guard_before_after_exact': True, 'fresh_reader_invocations': 1, 'scientific_or_helper_execution': False,
        'Git_mutations_network_W_Sheet_deploy_redirect_or_outreach': False,
        'readonly_local_Git_batches': len(git.reads),
        'canonical': None, 'legacy_correspondence': None, 'redirect': None, 'follow_up': None,
        'future_publication_or_action_authority': False})

def retain_failure(error):
    if not GIT_RESULTS:
        return
    require(not os.path.lexists(FAILURE_ROOT), 'private failure path absent; never overwrite')
    require(stat.S_IMODE(FAILURE_ROOT.parent.stat().st_mode) == 0o700, 'approved private runtime root')
    os.mkdir(FAILURE_ROOT, 0o700)
    records = []
    for i, (stdout, stderr, code) in enumerate(GIT_RESULTS):
        row = {'read': i, 'exit_code': code}
        for kind, data in [('stdout', stdout), ('stderr', stderr)]:
            path = FAILURE_ROOT / (str(i).zfill(3) + '.' + kind + '.bin')
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
            try:
                os.fchmod(fd, 0o600)
                cursor = 0
                while cursor < len(data):
                    written = os.write(fd, data[cursor:])
                    require(written > 0, 'complete literal private failure stream write')
                    cursor += written
                os.fsync(fd)
            finally:
                os.close(fd)
            row[kind] = {'private_path': str(path), **data_pin(data), 'mode': '0600'}
        records.append(row)
    put('NESTED_READ_FAILURE.json', {'schema': 'approved-private-D4-legacy-failure-retention-v1',
        'error': repr(error), 'private_directory': str(FAILURE_ROOT), 'root_mode': '0700',
        'whole_literal_streams': records, 'public_raw_stream_copy': False, 'automatic_retry': False, 'follow_up': None})

if __name__ == '__main__':
    try:
        main()
    except BaseException as error:
        retain_failure(error)
        raise
