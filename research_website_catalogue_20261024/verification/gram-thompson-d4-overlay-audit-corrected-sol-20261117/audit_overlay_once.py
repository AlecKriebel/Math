"""Independent passive three-page overlay audit. Writes only this audit packet."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import copy
import hashlib
import html
import json
import os
import posixpath
import re
import stat
import struct
import xml.etree.ElementTree as ET

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
S = P / 'verification/gram-thompson-d4-overlay-sol-20261117'
A = P / 'verification/gram-thompson-d4-overlay-audit-corrected-sol-20261117'
OLD = P / 'verification/gram-thompson-d4-overlay-audit-sol-20261117'
BASE = 'https://aleckriebel.com'
CSS = 'f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a'
PAPERS = [
 ('23318851', 'binary-gram-locus-polynomial-obstruction', 'binary-gram-locus-editorial-sol-20261117', 'zenodo-files', '2026-10-12', '12 October 2026', '1.0.0', 'Version 1.0.0', 5, 'derived/pdf-001/pdfinfo.stdout.txt', 'archives/02-gram_locus_support.zip.extracted/gram_locus_note.tex'),
 ('23204212', 'thompson-reduced-cstar-consequences', 'thompson-cstar-editorial-corrected-v2-sol-20261117', 'zenodo-files', '2026-10-06', '6 October 2026', None, 'Zenodo display edition: v1', 4, 'derived/pdf-003/pdfinfo.stdout.txt', 'archives/02-thompson-cstar-source.zip.extracted/main.tex'),
 ('23439776', 'd4-canonical-potential-exponent-converse', 'd4-canonical-potential-editorial-v2-sol-20261117', 'assets', '2026-10-17', '17 October 2026', '1.0', 'Version 1.0', 5, 'pdfinfo-001.stdout.txt', 'published-source/container-001/tree/manuscript/main.tex')]
ADOPTIONS = ['root-binary-gram-locus-editorial-adoption-20261117.json', 'root-thompson-cstar-editorial-adoption-20261117.json', 'root-d4-canonical-potential-editorial-adoption-20261117.json']
ADOPTION_PINS = ['600e1701f3951587fefabe9e8813efce864e2745395d22bd2141bb98b1c1074a', 'e7310696989e94e0041cb40fda170a5b8a2696b4b9976373db48e00dd531d624', '4eb74780ca57774a77f0c8c0bbd116806bdb4ad36c1696714aa1c8e03a83c5b9']
STAGE_PINS = {'FINAL.json': 'a8a21cbbd909f13d44dfa1ba35a10758acad996a831eaa756d8f053f1bbd4762', 'MANIFEST.json': '1206c4ca98ec65697440130c0b13534291804be09369acb05e7984f67f087fd9', 'SEAL.json': '8fa752e98d298d35b84f83d36c836e049f3afcbfb4f8987d0d218f36227cc554', 'TARGETS.json': 'f8c82bb2f5398f80ba8b75199a5cfd6f0ba214588ef9b2af91a158d0e703b8c5'}
SCRIPT = re.compile(rb'<script type="application/ld\+json">(.*?)</script>', re.S)
MARKER = b'<p class="entry-meta">Private editorial draft</p>\n'
CHECKS = 0

def require(value, reason):
    global CHECKS
    if not value:
        raise RuntimeError(reason)
    CHECKS += 1

def utc():
    return datetime.now(timezone.utc).isoformat()

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def load(path):
    return json.loads(path.read_bytes())

def save(name, value):
    with (A / name).open('x') as stream:
        stream.write(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def meta(path, relative):
    info = path.lstat()
    require(stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode), 'real guarded object ' + str(path))
    row = {'path': relative, 'mode': oct(stat.S_IMODE(info.st_mode)), 'mtime_ns': info.st_mtime_ns,
           'ctime_ns': info.st_ctime_ns, 'hidden': any(x.startswith('.') for x in Path(relative).parts if x != '.')}
    if stat.S_ISDIR(info.st_mode):
        row.update(kind='directory', empty=not any(path.iterdir()))
    else:
        raw = path.read_bytes()
        row.update(kind='file', bytes=len(raw), SHA256=sha(raw), empty=not raw)
    return row

def tree(root):
    seen, rows = set(), []
    def visit(path):
        info = path.lstat()
        if stat.S_ISDIR(info.st_mode):
            require((info.st_dev, info.st_ino) not in seen, 'unique real guarded directory')
            seen.add((info.st_dev, info.st_ino))
        relative = path.relative_to(root).as_posix()
        row = meta(path, relative)
        rows.append(row)
        if row['kind'] == 'directory':
            for child in sorted(path.iterdir()):
                visit(child)
    visit(root)
    rows.sort(key=lambda x: (x['path'] != '.', x['path']))
    return {'root': str(root), 'files': sum(x['kind'] == 'file' for x in rows),
            'child_directories': sum(x['kind'] == 'directory' for x in rows) - 1, 'entries': rows}

def capture():
    fixed = {'sources': {}, 'accepted_packets': {}, 'root_inputs': {}}
    for record, *unused in PAPERS:
        fixed['sources'][record] = tree(P / 'papers' / record / 'sources')
        for path in [P / 'papers' / record / 'reviews/root-continuation-20261117/ROOT_REVIEW.md', P / 'verification' / ('root-clearance-' + record + '-20261117.json')]:
            fixed['root_inputs'][str(path)] = meta(path, path.name)
    for name, expected in zip(ADOPTIONS, ADOPTION_PINS):
        path = P / 'verification' / name
        require(sha(path.read_bytes()) == expected, 'actual externally pinned root private adoption')
        fixed['root_inputs'][str(path)] = meta(path, path.name)
        for row in load(path)['packets']:
            root = P / row['path'] if row['path'].startswith('verification/') else P / 'verification' / row['path']
            require(root.parent == P / 'verification' and str(root) not in fixed['accepted_packets'], 'bounded distinct accepted packet')
            fixed['accepted_packets'][str(root)] = tree(root)
    native = {}
    for relative in ['.git/HEAD', '.git/index', '.git/config', '.git/config.worktree', '.git/packed-refs', '.git/shallow', 'firebase.json', '.firebaserc', '.gitignore']:
        path = W / relative
        native[relative] = meta(path, relative) if os.path.lexists(path) else {'path': relative, 'absent': True}
    native['local_heads'] = tree(W / '.git/refs/heads')
    return {'fixed': fixed, 'website': {'public': tree(W / 'public'), 'native_and_configuration': native}, 'stage': tree(S), 'original_failed_lane': tree(OLD)}

def entries(snapshot):
    return {x['path']: x for x in snapshot['entries']}

def declared_terminal_hash_exclusion(root, row, excluded, key, value):
    pair = {'FINAL_MANIFEST.json', 'FINAL_SEAL.json'}
    declared = len(excluded) == 2 and set(excluded) == pair and row['path'] in pair
    if root.name == 'binary-gram-locus-editorial-sol-20261117':
        return declared and key == 'SHA256' and value == 'EXCLUDED_TERMINAL_RECURSIVE_HASH'
    contracts = {
        'binary-gram-locus-editorial-fact-sol-20261117':
            ('SHA256', 'recursive_content_hash_excluded', True),
        'thompson-cstar-corrected-fact-sol-20261117':
            ('sha256', 'content_hash_exclusion', 'Already-created terminal pair only; exact object, mode, timestamp, bytes and topology retained'),
        'd4-canonical-potential-editorial-fact-sol-20261117':
            ('sha256', 'content_hash_exclusion', 'Already-created terminal pair only; exact objects/modes/timestamps/bytes/topology retained')}
    if root.name not in contracts or value is not None:
        return False
    expected_key, marker_key, marker = contracts[root.name]
    return declared and key == expected_key and row.get(marker_key) == marker

def verify_rows(root, actual, rows, excluded, directories=None):
    mapped = entries(actual)
    names = set()
    for row in rows:
        name = row['path']
        require(name not in names and name in mapped, 'manifest unique actual row ' + name)
        names.add(name)
        current = mapped[name]
        for key, value in row.items():
            translated = {'mode_octal': 'mode', 'sha256': 'SHA256', 'hidden_component': 'hidden'}.get(key, key)
            if translated == 'SHA256':
                if declared_terminal_hash_exclusion(root, row, excluded, key, value):
                    require(name in excluded, 'only exact declared terminal content hash excluded')
                else:
                    require(isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None and
                            current['SHA256'] == value, 'every unlisted or ordinary complete SHA256 ' + name)
            elif translated in ['path', 'kind', 'bytes', 'empty', 'hidden', 'mtime_ns', 'ctime_ns']:
                require(current[translated] == value, 'declared manifest field ' + name + ':' + translated)
            elif translated in ['recursive_content_hash_excluded', 'self_recursive_hash_excluded', 'recursive_hash_excluded']:
                require(name in excluded and value is True, 'actual exact terminal Boolean exclusion marker')
            elif translated == 'content_hash_exclusion':
                require(name in excluded and isinstance(value, str) and bool(value), 'actual exact terminal text exclusion marker')
            elif translated == 'mode':
                require(int(current['mode'], 8) == int(value, 8), 'declared individual mode ' + name)
            elif translated.lower() == 'md5':
                require(hashlib.md5((root / name).read_bytes()).hexdigest() == value, 'declared MD5 ' + name)
    if directories is not None:
        for name, value in directories.items():
            require(name in mapped and mapped[name]['kind'] == 'directory' and int(mapped[name]['mode'], 8) == int(value, 8), 'declared directory map')
            names.add(name)
        names.add('.')
    require(names | set(excluded) == set(mapped) and set(excluded) <= set(mapped), 'complete finite manifest coverage')

def verify_manifest(root, actual, filename):
    manifest = load(root / filename)
    if 'entries' in manifest:
        choices = [key for key in ['terminal_content_hash_exclusions_exact', 'only_recursive_hash_exclusions', 'only_recursive_content_hash_exclusions', 'excluded_control_files'] if key in manifest]
        require(len(choices) == 1, 'actual unambiguous entry manifest exclusion schema')
        verify_rows(root, actual, manifest['entries'], manifest[choices[0]])
    elif 'payload_files' in manifest:
        payload = manifest['payload_files']
        rows = [{'path': name, **value} for name, value in payload.items()] if isinstance(payload, dict) else payload
        if 'terminal_pair' in manifest:
            excluded = [x['path'] for x in manifest['terminal_pair']]
            rows += manifest['terminal_pair']
            directories = manifest['directories']
        else:
            excluded = manifest['exact_already_created_terminal_recursive_hash_exclusions']
            rows += manifest['directories']
            directories = None
        verify_rows(root, actual, rows, excluded, directories)
        require(int(entries(actual)['.']['mode'], 8) == int(manifest['root_mode'], 8), 'actual declared root mode')
    else:
        require(manifest['schema'] == 'opaque-native-source-manifest-v1', 'actual D4 source schema')
        rows = manifest['files'] + [{'path': x['path'], 'kind': 'directory', 'mode': x['mode']} for x in manifest['directories']]
        rows.append({'path': '.', 'kind': 'directory', 'mode': manifest['root_mode']})
        verify_rows(root, actual, rows, manifest['root_controls_excluded_from_own_list'])

def authenticate(before):
    old = before['original_failed_lane']
    require((old['files'], old['child_directories']) == (12, 0), 'whole frozen original failed lane12/0')
    require(sha((OLD / 'FINAL.json').read_bytes()) == 'dd7eae47db1dfb53e788aa60b5853904ec1d885b9a6ca529b25a126379c5395c' and
            sha((OLD / 'MANIFEST.json').read_bytes()) == 'd403419579bc571f86f821d11f02993cfad2de5de0633d43404649028d019110',
            'externally pinned original failed terminal pair')
    verify_manifest(OLD, old, 'MANIFEST.json')
    failed = load(OLD / 'FINAL.json')
    require(failed['status'] == 'FAILED_INCOMPLETE_FROZEN' and failed['reader_invocations'] == 1 and failed['reader_exit'] == 1 and
            all(not (OLD / name).exists() for name in ['AFTER.json', 'DETAILS.json', 'RESULTS.json']),
            'original failure remains incomplete forever, no retro-PASS')
    for name, expected in STAGE_PINS.items():
        require(sha((S / name).read_bytes()) == expected, 'external complete stage control pin ' + name)
    receipt = load(S / 'BUILDER_RUN.json')
    require(receipt['exit'] == 0 and receipt['attempt_count'] == 1 and receipt['repair_or_retry_count'] == 0 and
            receipt['builder_SHA256'] == sha((S / 'build_overlay.py').read_bytes()) and
            (S / 'builder.exit.txt').read_bytes() == b'0\n', 'retained single successful producer receipt as data only')
    for kind in ['stdout', 'stderr']:
        raw = (S / ('builder.' + kind + '.txt')).read_bytes()
        require(len(raw) == receipt[kind + '_bytes'] and sha(raw) == receipt[kind + '_SHA256'], 'retained literal producer stream identity')
    require(load(S / 'BUILD_RESULT.json') == json.loads((S / 'builder.stdout.txt').read_bytes()) and
            (S / 'builder.stderr.txt').read_bytes() == b'', 'complete retained producer stdout result')
    require((before['stage']['files'], before['stage']['child_directories']) == (41, 6), 'whole physical stage41/6')
    manifest = load(S / 'MANIFEST.json')
    require(manifest['schema'] == 'finite-owned-private-overlay-namespace-v1' and manifest['terminal_content_hash_exclusions_exact'] == ['MANIFEST.json', 'SEAL.json'], 'actual stage manifest schema and exact controls')
    verify_rows(S, before['stage'], manifest['entries'], manifest['terminal_content_hash_exclusions_exact'])
    fixed_expected = {k: v for k, v in load(S / 'FIXED_INPUTS_BEFORE.json').items() if k != 'UTC'}
    website_expected = {k: v for k, v in load(S / 'WEBSITE_BEFORE.json').items() if k != 'UTC'}
    require(before['fixed'] == fixed_expected and before['website'] == website_expected, 'entire actual fixed inputs/native public equal frozen baseline fingerprints')
    require({k: v for k, v in load(S / 'FIXED_INPUTS_AFTER.json').items() if k not in ['UTC', 'before_after_exact']} == fixed_expected and
            {k: v for k, v in load(S / 'WEBSITE_AFTER.json').items() if k not in ['UTC', 'before_after_exact']} == website_expected, 'retained producer custody exact as data')
    for paper in PAPERS:
        root = P / 'papers' / paper[0] / 'sources'
        verify_manifest(root, before['fixed']['sources'][paper[0]], 'SOURCE_MANIFEST.json')
    for name in ADOPTIONS:
        for packet in load(P / 'verification' / name)['packets']:
            root = P / packet['path'] if packet['path'].startswith('verification/') else P / 'verification' / packet['path']
            actual = before['fixed']['accepted_packets'][str(root)]
            require((actual['files'], actual['child_directories']) == (packet['files'], packet['child_directories']), 'actual adopted packet extent')
            if 'external_controls' in packet:
                for file, expected in packet['external_controls'].items():
                    require(sha((root / file).read_bytes()) == expected, 'whole adopted terminal external pin')
                filename = 'MANIFEST.json' if 'MANIFEST.json' in packet['external_controls'] else 'FINAL_MANIFEST.json'
            else:
                filename = 'FINAL_MANIFEST.json'
                require(sha((root / filename).read_bytes()) == packet['manifest_SHA256'], 'Gram actual manifest pin')
                require(sum(path.is_file() and sha(path.read_bytes()) == packet['terminal_SHA256'] for path in [root / 'FINAL_SEAL.json', root / 'FINAL.json']) == 1, 'Gram actual terminal pin')
            verify_manifest(root, actual, filename)
    require((before['website']['public']['files'], before['website']['public']['child_directories']) == (803, 387), 'whole baseline803/387')
    require(entries(before['website']['public'])['.']['mode'] == '0o750', 'preserved public root0750')
    require((W / '.git/HEAD').read_bytes() == b'ref: refs/heads/master\n' and (W / '.git/refs/heads/master').read_text().strip() == '4cc09d6bbbad61aa11077c5002cf84a1e93b1344', 'fixed current native website HEAD')
    require(sha((W / '.git/index').read_bytes()) == '6b76dc0a4e7a631587aec1c081057479883573f7ff284dfc88b5adad02317179', 'complete fixed raw native index')
    require(sha((W / 'public/research/research.css').read_bytes()) == CSS, 'actual unchanged root shared CSS')

class HTML(HTMLParser):
    def __init__(self, raw):
        super().__init__(convert_charrefs=True)
        self.events, self.meta, self.ids, self.links, self.labels, self.data = [], {}, set(), [], [], []
        self.feed(raw.decode())
    def handle_starttag(self, tag, attrs):
        self.events.append(['start', tag, [list(x) for x in attrs]])
        d = dict(attrs)
        if 'id' in d:
            require(d['id'] not in self.ids, 'unique HTML ID')
            self.ids.add(d['id'])
        if tag == 'meta':
            key = d.get('name', d.get('property'))
            if key:
                require(key not in self.meta, 'unique metadata key')
                self.meta[key] = d.get('content')
        for key in ['href', 'src', 'data']:
            if key in d:
                self.links.append((tag, key, d[key]))
        for key in ['aria-labelledby', 'aria-describedby']:
            self.labels += d.get(key, '').split()
    def handle_endtag(self, tag):
        self.events.append(['end', tag])
    def handle_data(self, value):
        self.events.append(['data', value])
        self.data.append(value)

def edits(original, changes):
    changes = sorted(changes)
    last, chunks, reverse = 0, [], []
    for start, end, new in changes:
        require(last <= start <= end <= len(original), 'disjoint closed independent spans')
        chunks += [original[last:start], new]
        position = sum(map(len, chunks)) - len(new)
        reverse.append((position, position + len(new), original[start:end]))
        last = end
    candidate = b''.join(chunks) + original[last:]
    restored, last, chunks = candidate, 0, []
    for start, end, old in reverse:
        chunks += [restored[last:start], old]
        last = end
    require(b''.join(chunks) + restored[last:] == original, 'independent WHOLE closed-span reverse')
    return candidate

def supplied_replay(original, candidate, rows):
    buffer = original
    for row in rows:
        start, old, new = row['start_byte'], row['old'].encode(), row['new'].encode()
        require(sha(buffer) == row['before_SHA256'] and buffer[start:start + len(old)] == old, 'every supplied exact old span/hash')
        buffer = buffer[:start] + new + buffer[start + len(old):]
        require(sha(buffer) == row['after_SHA256'], 'every supplied new whole hash')
    require(buffer == candidate, 'supplied whole forward exact')
    for row in reversed(rows):
        start, old, new = row['start_byte'], row['old'].encode(), row['new'].encode()
        require(buffer[start:start + len(new)] == new and sha(buffer) == row['after_SHA256'], 'supplied exact reverse span/hash')
        buffer = buffer[:start] + old + buffer[start + len(new):]
    require(buffer == original, 'supplied WHOLE reverse exact')

def only_match(pattern, raw):
    matches = list(pattern.finditer(raw)) if hasattr(pattern, 'finditer') else list(re.finditer(pattern, raw, re.S))
    require(len(matches) == 1, 'actual unique closed matching span')
    return matches[0]

def article(paper, recorded):
    record, slug, writer, assetdir, date, datelabel, version, versionlabel, pages, pdfinfo, texpath = paper
    root = P / 'verification' / writer
    model = load(root / 'MODEL.json')
    original = (root / 'private-page/index.html').read_bytes()
    relative = 'research/' + slug + '/index.html'
    candidate = (S / 'overlay' / relative).read_bytes()
    old, new = HTML(original), HTML(candidate)
    route, canonical = '/research/' + slug + '/', BASE + '/research/' + slug + '/'
    native = model['native_assets_in_original_order']
    names = [x['native_filename'] for x in native]
    pdf = next(name for name in names if name.endswith('.pdf'))
    old_schema_match = only_match(SCRIPT, original)
    old_schema = json.loads(old_schema_match.group(1))
    if record == '23318851':
        require(old_schema == model['SEO']['structured_data'], 'Gram actual nested structured-data model')
        abstract = model['abstract']['source_tex']
        normalized, replacements, abstracthash = model['abstract']['normalized_full_text'], model['abstract']['literal_rendering_replacements'], model['abstract']['normalized_SHA256']
    elif record == '23204212':
        abstract = model['original_abstract_tex']
        normalized, replacements, abstracthash = model['original_abstract_normalized'], model['abstract_rendering_replacements'], model['abstract_normalized_sha256']
        require(model['native_version_field_present'] is False and version is None and 'version' not in old_schema and 'citation_version' not in old.meta and 'citation_version' not in new.meta, 'no invented Thompson author version')
        require(b'complex linear span' in candidate and b'Zenodo' in candidate and b'v1' in candidate, 'corrected Thompson definition and qualified edition retained')
    else:
        require(old_schema == model['structured_data'], 'D4 actual structured-data model')
        abstract = model['abstract']['literal_source_TeX_span']
        normalized, replacements, abstracthash = model['abstract']['normalized_full_text'], model['abstract']['literal_rendering_replacements'], model['abstract']['normalized_SHA256']
    actual_tex = (P / 'papers' / record / 'sources' / texpath).read_text()
    actual_abstract = actual_tex.split('\\begin{abstract}', 1)[1].split('\\end{abstract}', 1)[0]
    require(' '.join(actual_abstract.split()) == ' '.join(abstract.split()), 'entire actual native TeX abstract correspondence')
    rendered = abstract
    for row in replacements:
        rendered = rendered.replace(row['from'], row['to'])
    require(' '.join(rendered.split()) == normalized and sha(normalized.encode()) == abstracthash and
            old_schema['abstract'] == normalized and old.meta['citation_abstract'] == new.meta['citation_abstract'] == normalized, 'complete normalized abstract in actual schema and metadata')
    require(model['native_publication_date'] == date and model['native_version'] == version and old_schema['datePublished'] == date, 'actual native date/version')
    desired = copy.deepcopy(old_schema)
    desired['url'] = canonical
    require([x['name'] for x in desired['encoding']] == names, 'all native encoding names/order')
    for encoding in desired['encoding']:
        encoding['contentUrl'] = canonical + encoding['name']
    changes = []
    for pattern, replacement in [(rb'<meta name="robots" content="[^"]+">', b'<meta name="robots" content="index,follow">'),
                                 (rb'<meta name="citation_pdf_url" content="[^"]+">', ('<meta name="citation_pdf_url" content="' + canonical + pdf + '">').encode())]:
        match = only_match(pattern, original)
        changes.append((match.start(), match.end(), replacement))
    css = only_match(rb'<link rel="stylesheet" href="research.css">', original)
    lines = ['<link rel="canonical" href="' + canonical + '">']
    if 'og:type' not in old.meta:
        lines += ['<meta property="og:type" content="article">', '<meta property="og:title" content="' + html.escape(model['title'], quote=True) + '">', '<meta property="og:description" content="' + html.escape(old.meta['description'], quote=True) + '">']
    lines += ['<meta property="og:url" content="' + canonical + '">', '<meta property="og:site_name" content="Alec Kriebel">', '<link rel="stylesheet" href="/research/research.css">']
    changes.append((css.start(), css.end(), '\n'.join(lines).encode()))
    changes.append((old_schema_match.start(), old_schema_match.end(), ('<script type="application/ld+json">' + json.dumps(desired, ensure_ascii=False) + '</script>').encode()))
    head_end = original.index(b'</head>')
    require(all(original.index(b'<head>') < start < end <= head_end for start, end, replacement in changes), 'all four independent HEAD spans closed')
    old_body = original[original.index(b'<body>'):]
    if record == '23318851':
        require(original.count(MARKER) == 1 and original.index(MARKER) > head_end, 'sole authorized exact Gram BODY marker')
        start = original.index(MARKER)
        changes.append((start, start + len(MARKER), b''))
        old_body = old_body.replace(MARKER, b'', 1)
    require(edits(original, changes) == candidate and candidate[candidate.index(b'<body>'):] == old_body, 'WHOLE accepted article forward/reverse and otherwise exact BODY/MAIN')
    supplied_replay(original, candidate, recorded['literal_changes'])
    require(recorded['source_path'] == str(root / 'private-page/index.html') and recorded['candidate_path'] == relative and
            len(recorded['literal_changes']) == len(changes), 'actual supplied article edit extent and source binding')
    new_schema = json.loads(only_match(SCRIPT, candidate).group(1))
    require(new_schema == desired and new.meta['robots'] == 'index,follow' and new.meta['og:url'] == canonical and
            new.meta['citation_pdf_url'] == canonical + pdf and new.meta['og:type'] == 'article', 'exact candidate canonical/SEO/Scholar/schema')
    require(all(new.meta.get(key) == old.meta.get(key) for key in old.meta if key not in ['robots', 'citation_pdf_url']), 'all remaining typed metadata unchanged')
    require(all(label in new.ids for label in new.labels), 'local ARIA references actual IDs')
    for asset in native:
        name = asset['native_filename']
        raw = (root / 'private-page' / name).read_bytes()
        require(raw == (S / 'overlay/research' / slug / name).read_bytes() == (P / 'papers' / record / 'sources' / assetdir / name).read_bytes(), 'whole accepted/native/overlay asset buffer')
        require(len(raw) == asset['bytes'] and sha(raw) == asset.get('SHA256', asset.get('sha256')), 'actual declared native asset metadata')
        require(PurePosixPath(name).name == name, 'native assets remain at page root')
        if name.endswith('.pdf'):
            require(raw.startswith(b'%PDF-') and re.search(r'^Pages:\s+' + str(pages) + r'\s*$', (P / 'papers' / record / 'sources' / pdfinfo).read_text(), re.M), 'native PDF identity/header and retained page-count metadata')
    require((root / 'private-page/citation.bib').read_bytes() == (S / 'overlay/research' / slug / 'citation.bib').read_bytes(), 'whole BibTeX buffer exact')
    require(sha((root / 'private-page/research.css').read_bytes()) == CSS, 'accepted shared CSS exact')
    return {'record': record, 'slug': slug, 'route': route, 'canonical': canonical, 'relative': relative,
            'title': model['title'], 'description': old.meta['description'], 'date': date, 'date_label': datelabel,
            'version': version, 'version_label': versionlabel, 'PDF': pdf, 'PDF_pages': pages,
            'native_names': names, 'independent_HEAD_spans': 4, 'authorized_BODY_spans': int(record == '23318851'), 'links': new.links}

def json_records(script):
    text = script.decode()
    marker = '"itemListElement"'
    require(text.count(marker) == 1, 'unique actual collection array')
    start = text.index('[', text.index(marker) + len(marker))
    array, end = json.JSONDecoder().raw_decode(text, start)
    cursor, rows = start + 1, []
    for item in array:
        while text[cursor].isspace():
            cursor += 1
        begin = cursor
        actual, cursor = json.JSONDecoder().raw_decode(text, cursor)
        require(actual == item, 'exact raw/typed collection unit correspondence')
        rows.append({'raw': text[begin:cursor], 'typed': item, 'position': item['position'], 'character_start': begin, 'character_end': cursor})
        while text[cursor].isspace():
            cursor += 1
        if text[cursor] == ',':
            cursor += 1
    return start, end, rows

def xml_typed(node):
    return {'tag': node.tag, 'attributes_in_order': [list(x) for x in node.attrib.items()], 'text': node.text,
            'tail': node.tail, 'children': [xml_typed(x) for x in node]}

def aggregates(pages):
    old = (W / 'public/research/index.html').read_bytes()
    old_xml = (W / 'public/research/sitemap.xml').read_bytes()
    require(old == (S / 'before/index.html').read_bytes() and old_xml == (S / 'before/sitemap.xml').read_bytes(), 'both WHOLE actual before globals')
    new, new_xml = (S / 'overlay/research/index.html').read_bytes(), (S / 'overlay/research/sitemap.xml').read_bytes()
    script = only_match(SCRIPT, old)
    newscript = only_match(SCRIPT, new)
    array_start, array_end, old_json = json_records(script.group(1))
    unused, unused2, new_json = json_records(newscript.group(1))
    require(len(old_json) == 133 and len(new_json) == 136 and new_json[:133] == old_json and
            [x['position'] for x in new_json] == list(range(1, 137)), 'all133 WHOLE raw/typed JSON records/positions exact prefix')
    additions, lis, urls = [], [], []
    for number, page in enumerate(pages, 134):
        additions.append({'@type': 'ListItem', 'position': number, 'url': page['canonical'], 'name': page['title']})
        e = lambda value: html.escape(value, quote=True)
        lis.append('<li><a href="' + page['route'] + '">' + e(page['title']) + '</a><br><span class="entry-meta"><time datetime="' + page['date'] + '">' + page['date_label'] + '</time> · ' + page['version_label'] + ' · Unrefereed, AI-assisted preprint</span><p>' + e(page['description']) + '</p><p><a href="' + page['route'] + page['PDF'] + '">PDF (' + str(page['PDF_pages']) + ' pages)</a> · <a href="https://doi.org/10.5281/zenodo.' + page['record'] + '">Zenodo</a></p></li>')
        urls.append('<url><loc>' + page['canonical'] + '</loc><lastmod>2026-11-17</lastmod></url>\n')
    require([x['typed'] for x in new_json[133:]] == additions, 'exact three independently derived new JSON items')
    script_text = script.group(1).decode()
    end_byte = script.start(1) + len(script_text[:array_end - 1].encode())
    count = only_match(rb'"numberOfItems": 133', script.group(1))
    count_start = script.start(1) + count.start()
    close_ul = only_match(rb'</ul>', old)
    changes = [(count_start, count_start + len(count.group()), b'"numberOfItems": 136'),
               (end_byte, end_byte, (', ' + ', '.join(json.dumps(x, ensure_ascii=False) for x in additions)).encode()),
               (close_ul.start(), close_ul.start(), ('\n'.join(lis) + '\n').encode())]
    require(edits(old, changes) == new, 'independent entire index forward/reverse with exactly three closed spans')
    old_li = list(re.finditer(rb'<li\b[^>]*>.*?</li>', old, re.S))
    new_li = list(re.finditer(rb'<li\b[^>]*>.*?</li>', new, re.S))
    require(len(old_li) == 133 and len(new_li) == 136, 'whole listing counts133/136')
    supplied = load(S / 'INDEX_PRESERVATION.json')
    visible = []
    for i, match in enumerate(old_li):
        raw = match.group()
        require(raw == new_li[i].group(), 'every WHOLE old HTML listing unit exact prefix')
        parsed, parsed_new = HTML(raw), HTML(new_li[i].group())
        require(parsed.events == parsed_new.events and ''.join(parsed.data).encode() == ''.join(parsed_new.data).encode(), 'every complete typed/visible HTML buffer')
        visible.append(len(''.join(parsed.data).encode()))
        expected = {'position': i + 1, 'start_byte': match.start(), 'end_byte': match.end(), 'raw': raw.decode(), 'typed_HTML': parsed.events, 'JSON': old_json[i]}
        require(expected == supplied['old_units'][i], 'all supplied old HTML/JSON raw/typed/positions authenticated')
    require([x.group().decode() for x in new_li[133:]] == lis, 'exact three independent whole new HTML units')
    require(supplied['new_units'] == [{'raw': raw, 'typed_HTML': HTML(raw.encode()).events, 'JSON': item} for raw, item in zip(lis, additions)], 'all supplied new listing metadata')
    supplied_replay(old, new, supplied['literal_changes'])
    old_root, new_root = ET.fromstring(old_xml), ET.fromstring(new_xml)
    old_units = list(re.finditer(rb'<url(?:\s[^>]*)?>.*?</url>', old_xml, re.S))
    new_units = list(re.finditer(rb'<url(?:\s[^>]*)?>.*?</url>', new_xml, re.S))
    require(len(old_root) == len(old_units) == 134 and len(new_root) == len(new_units) == 137, 'full XML134/137 counts')
    require((old_root.tag, list(old_root.attrib.items()), old_root.text, old_root.tail) ==
            (new_root.tag, list(new_root.attrib.items()), new_root.text, new_root.tail), 'whole parsed XML root metadata')
    saved = load(S / 'SITEMAP_PRESERVATION.json')
    require((saved['old_root_tag'], saved['old_root_attributes'], saved['old_root_text']) ==
            (old_root.tag, [list(x) for x in old_root.attrib.items()], old_root.text), 'supplied complete parsed XML root metadata')
    for i, (node, raw) in enumerate(zip(old_root, old_units)):
        require(raw.group() == new_units[i].group() and xml_typed(node) == xml_typed(new_root[i]), 'every old whole raw/full parsed XML child including tails/order')
        require(saved['old_units'][i] == {'position': i + 1, 'start_byte': raw.start(), 'end_byte': raw.end(), 'raw': raw.group().decode(), 'full_parsed': xml_typed(node)}, 'every supplied original XML record')
    close_xml = only_match(rb'</urlset>', old_xml)
    require(edits(old_xml, [(close_xml.start(), close_xml.start(), ''.join(urls).encode())]) == new_xml and
            [x.group().decode() for x in new_units[134:]] == [x.rstrip('\n') for x in urls], 'independent full XML forward/reverse and three new whole units')
    require(saved['new_units'] == [xml_typed(x) for x in list(new_root)[134:]], 'all new supplied parsed XML records')
    supplied_replay(old_xml, new_xml, saved['literal_changes'])
    return {'old_HTML_JSON_XML': [133, 133, 134], 'new_HTML_JSON_XML': [136, 136, 137],
            'independent_index_closed_spans': 3, 'independent_XML_closed_spans': 1, 'new_HTML_JSON_XML_units': [3, 3, 3],
            'whole_old_visible_bytes': visible, 'old_index_SHA256': sha(old), 'candidate_index_SHA256': sha(new),
            'old_XML_SHA256': sha(old_xml), 'candidate_XML_SHA256': sha(new_xml)}

def native_paths():
    raw = (W / '.git/index').read_bytes()
    require(raw[:4] == b'DIRC' and struct.unpack('>I', raw[4:8])[0] == 2 and hashlib.sha1(raw[:-20]).digest() == raw[-20:], 'complete actual index v2/checksum')
    count, cursor, paths = struct.unpack('>I', raw[8:12])[0], 12, set()
    require(count == 58743, 'actual native index record count')
    for unused in range(count):
        start = cursor
        flags = struct.unpack_from('>H', raw, cursor + 60)[0]
        end = raw.index(b'\0', cursor + 62)
        name = raw[cursor + 62:end].decode()
        require(name not in paths and flags & 0x7000 == 0 and min(len(name.encode()), 4095) == flags & 4095, 'unique ordinary native index path and flags')
        paths.add(name)
        cursor = end + 1
        cursor += -(cursor - start) % 8
    require(raw[cursor:cursor + 4] == b'TREE', 'actual unchanged extension boundary')
    return paths

def projection(before, pages):
    baseline = entries(before['website']['public'])
    files = {k: {f: row[f] for f in ['bytes', 'SHA256', 'mode']} for k, row in baseline.items() if row['kind'] == 'file'}
    directories = {k: row['mode'] for k, row in baseline.items() if row['kind'] == 'directory'}
    expected_new = {name for page in pages for name in ['research/' + page['slug'] + '/' + value for value in ['index.html', 'citation.bib'] + page['native_names']]}
    mods = {'research/index.html', 'research/sitemap.xml'}
    rows = load(S / 'TARGETS.json')
    target_rows = {x['path']: x for x in rows['changes']}
    require(set(target_rows) == expected_new | mods and len(expected_new) == 13 and len(rows['changes']) == 15 and rows['A'] == 13 and rows['M'] == 2, 'independently derived exact15 targets13A2M')
    overlay = tree(S / 'overlay')
    overlay_files = {x['path'] for x in overlay['entries'] if x['kind'] == 'file'}
    require(overlay_files == set(target_rows) and overlay['files'] == 15 and overlay['child_directories'] == 4, 'physical target overlay only; no whole website mirror')
    native = {x.casefold() for x in native_paths()}
    listing = (W / 'public/research/index.html').read_bytes().decode().casefold()
    old_locs = [x.text.casefold() for x in ET.fromstring((W / 'public/research/sitemap.xml').read_bytes()).iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    for page in pages:
        root = 'research/' + page['slug']
        require(not any(name.casefold() == root.casefold() or name.casefold().startswith(root.casefold() + '/') or name.casefold() in [root.casefold() + '.html', root.casefold() + '.htm'] for name in baseline), 'full physical casefold route collision check')
        require(not any(name == 'public/' + root.casefold() or name.startswith('public/' + root.casefold() + '/') or name in ['public/' + root.casefold() + '.html', 'public/' + root.casefold() + '.htm'] for name in native), 'full native-index route collision check')
        require(page['slug'].casefold() not in listing and page['canonical'].casefold() not in old_locs, 'current listing/sitemap route fresh')
        directories[root] = '0o755'
    require(len({name.casefold() for name in expected_new}) == 13, 'new paths pairwise casefold unique')
    for name, row in target_rows.items():
        actual = meta(S / 'overlay' / name, name)
        require(all(actual[key] == row[key] for key in ['bytes', 'SHA256', 'mode']) and row['mode'] == '0o644', 'all target literal bytes and actual modes')
        require((name in files) == (row['action'] == 'M') and row['action'] == ('M' if name in mods else 'A'), 'exact additions/modifications membership')
        files[name] = {key: actual[key] for key in ['bytes', 'SHA256', 'mode']}
    supplied = load(S / 'PUBLIC_PROJECTION.json')
    require(files == supplied['files'] and directories == supplied['directories_including_root'] and len(files) == 816 and len(directories) - 1 == 390, 'independent WHOLE projected file/mode/directory map')
    require(not any(PurePosixPath(name).name == 'research.css' for name in overlay_files), 'shared stylesheet not copied')
    def content(relative):
        return ((S / 'overlay' / relative) if relative in target_rows else (W / 'public' / relative)).read_bytes()
    for page in pages:
        parsed = HTML(content(page['relative']))
        for tag, attribute, value in parsed.links:
            url = urlsplit(value)
            if url.scheme or url.netloc:
                if url.scheme != 'https' or url.netloc != 'aleckriebel.com':
                    continue
            local = unquote(url.path)
            resolved = posixpath.normpath(local.lstrip('/') if local.startswith('/') else posixpath.join(posixpath.dirname(page['relative']), local))
            if not local:
                resolved = page['relative']
            elif local.endswith('/') or resolved in directories:
                resolved = posixpath.normpath(posixpath.join(resolved, 'index.html'))
            require(not resolved.startswith('../') and resolved in files, 'every local stylesheet/asset/anchor target exists in full projection: ' + resolved)
            raw = content(resolved)
            if resolved.endswith('.pdf'):
                require(raw.startswith(b'%PDF-'), 'actual local PDF target typed as PDF')
            if url.fragment and resolved.endswith(('.html', '.htm')):
                require(unquote(url.fragment) in HTML(raw).ids, 'HTML-only fragment target actual ID')
    return {'files': len(files), 'child_directories': len(directories) - 1, 'native_index_paths_checked': len(native),
            'new_page_directories': ['research/' + x['slug'] for x in pages], 'whole_projection_SHA256': sha(json.dumps({'files': files, 'directories': directories}, sort_keys=True).encode())}

def main():
    require(Path(__file__).resolve() == A / 'audit_overlay_once.py' and not (A / 'RESULTS.json').exists(), 'one fresh fixed passive audit invocation')
    started = utc()
    before = capture()
    save('BEFORE.json', {'UTC': started, 'snapshot': before})
    authenticate(before)
    activations = load(S / 'PAGE_ACTIVATIONS.json')
    require([x['record'] for x in activations] == [x[0] for x in PAPERS], 'actual accepted article order')
    pages = [article(paper, row) for paper, row in zip(PAPERS, activations)]
    require(load(S / 'PROJECTED_PAGE_METADATA.json') == [{'record': x['record'], 'route': x['route'],
        'candidate_canonical': x['canonical'], 'native_publication_date': x['date'], 'native_version': x['version'],
        'PDF_pages': x['PDF_pages'], 'native_assets_in_original_order': x['native_names'],
        'page_publication_date': None, 'AA': None, 'redirect': None, 'follow_up': None, 'private_stage_only': True} for x in pages],
        'all projected page metadata independently derived from actual accepted inputs')
    aggregate = aggregates(pages)
    projected = projection(before, pages)
    after = capture()
    require(after == before, 'entire fixed source/private/root/stage/native/public/config before-after exact')
    save('AFTER.json', {'UTC': utc(), 'snapshot': after})
    save('DETAILS.json', {'schema': 'independent-three-page-private-overlay-details-v1', 'pages': pages,
        'aggregates': aggregate, 'projection': projected, 'source_files_childdirs': [[95, 16], [55, 14], [72, 7]],
        'accepted_packets': 9, 'accepted_packet_files': 366, 'stage_files_childdirs': [41, 6],
        'physical_overlay_files_childdirs': [15, 4], 'whole_public_copy_created': False,
        'all_manifest_terminal_pairs_externally_pinned': True, 'original_failed_lane_files_childdirs': [12, 0], 'private_opaque_control_bytes_copied': False,
        'page_publication_date': None, 'AA': None, 'redirect': None, 'follow_up': None})
    save('RESULTS.json', {'schema': 'independent-three-page-private-overlay-result-v1', 'UTC_start': started, 'UTC_end': utc(),
        'status': 'PASS_CORRECTED_PRIVATE_OVERLAY_AUDIT_ONLY', 'original_failed_lane_whole_before_after_exact': True, 'completion_percent_assigned_private_audit_only': 100,
        'whole_projection_files_childdirs_articles_XML': [816, 390, 136, 137], 'targets_A_M': [13, 2],
        'whole_guard_before_after_exact': True, 'fresh_passive_checker_invocations': 1, 'checks_passed': CHECKS,
        'independent_article_HEAD_BODY_spans': [[4, 1], [4, 0], [4, 0]], 'PDF_page_counts': [5, 4, 5],
        'all_old133_HTML_JSON_and134_XML_prefix_full_buffers_preserved': True,
        'whole_public_copy_or_Git_network_W_Sheet_server_install_deploy_science_helper_import_AST_compile_help_test_or_retry': False,
        'actual_UI_live_canonical_AA_redirect_production_or_future_action_certificate': False,
        'page_publication_date': None, 'AA': None, 'redirect': None, 'follow_up': None, 'future_action_authority': False})

if __name__ == '__main__':
    main()
