#!/usr/bin/env python3
"""Read-only independent fixed-stage mechanism checks and in-memory falsifiers.

Default authenticates immutable inputs and stage, with optional --live-baseline
for the separately time-sensitive pre-install website fence. No project imports,
native execution, network, subprocesses or writes.
"""
from pathlib import Path, PurePosixPath
from html.parser import HTMLParser
from urllib.parse import urlsplit
import ast, copy, hashlib, json, os, re, stat, sys
import xml.etree.ElementTree as ET

A = Path(__file__).absolute().parent
S = A.parent / 'three-research-private-stage-sol-20261115'
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
STAGE_FINAL = {'bytes': 1113, 'SHA256': '4f9cb2f5c8779a586bbfa34efc6f498d677bcd15826f28f7c4f4ecf33cd43b11'}
STAGE_CODE = {'bytes': 24045, 'SHA256': '44ed6c1ffa36b5f2a853516c4de6346d2903cafe35e462fadf4e0e295454ded6'}
TERMS = {'OWNED_MANIFEST.json', 'FINAL_SEAL.json'}
CHECKS = 0


def need(ok, reason):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise ValueError(reason)


def pin(b):
    return {'bytes': len(b), 'SHA256': hashlib.sha256(b).hexdigest()}


def read(p):
    p = Path(p)
    need(p.is_absolute() and '..' not in p.parts, 'absolute ordinary input')
    for ancestor in p.parents:
        need(stat.S_ISDIR(ancestor.lstat().st_mode), 'ordinary input ancestor')
    before = p.lstat()
    need(stat.S_ISREG(before.st_mode), 'ordinary input file')
    fd = os.open(p, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        held = os.fstat(fd)
        need((before.st_dev, before.st_ino) == (held.st_dev, held.st_ino), 'opened identity')
        chunks = []
        while True:
            part = os.read(fd, 1048576)
            if not part:
                break
            chunks.append(part)
        after, end = os.fstat(fd), p.lstat()
        need((held.st_dev, held.st_ino, held.st_size, held.st_mtime_ns, held.st_ctime_ns) ==
             (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns), 'stable held buffer')
        need((held.st_dev, held.st_ino) == (end.st_dev, end.st_ino), 'stable pathname')
        body = b''.join(chunks)
        need(len(body) == held.st_size, 'complete buffer')
        return body
    finally:
        os.close(fd)


def bound(row):
    b = read(Path(row['path']))
    need(pin(b) == {k: row[k] for k in ['bytes', 'SHA256']}, 'whole pinned input ' + row['path'])
    return b


def obj(p):
    return json.loads(read(p))


def typed(a, b):
    need(type(a) is type(b), 'typed aggregate node')
    if type(a) is dict:
        need(list(a) == list(b), 'ordered aggregate keys')
        for k in a:
            typed(a[k], b[k])
    elif type(a) is list:
        need(len(a) == len(b), 'aggregate array extent')
        for x, y in zip(a, b):
            typed(x, y)
    else:
        need(a == b, 'aggregate literal')


def extent(root):
    files, dirs = [], []
    def visit(d):
        before = d.lstat()
        need(stat.S_ISDIR(before.st_mode), 'ordinary namespace directory')
        for p in sorted(d.iterdir()):
            rel = p.relative_to(root).as_posix()
            mode = p.lstat().st_mode
            if stat.S_ISDIR(mode):
                dirs.append(rel)
                visit(p)
            elif stat.S_ISREG(mode):
                files.append({'path': rel, **pin(read(p))})
            else:
                raise ValueError('symlink/FIFO/special namespace entry')
        after = d.lstat()
        need((before.st_dev, before.st_ino, before.st_mtime_ns, before.st_ctime_ns) ==
             (after.st_dev, after.st_ino, after.st_mtime_ns, after.st_ctime_ns), 'stable namespace')
    visit(root)
    return sorted(files, key=lambda x: x['path']), sorted(dirs)


class Page(HTMLParser):
    def __init__(self, body):
        super().__init__(convert_charrefs=True)
        self.tags, self.ids = [], []
        self.feed(body.decode())
        self.close()
    def handle_starttag(self, tag, attrs):
        need(len(attrs) == len(dict(attrs)), 'no duplicate HTML attribute')
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if 'id' in attrs:
            self.ids.append(attrs['id'])


def jsonld(body):
    matches = re.findall(rb'<script type="application/ld\+json">(.*?)</script>', body, re.S)
    need(len(matches) == 1, 'one JSON-LD block')
    return json.loads(matches[0])


def replace_ld(body, value):
    old = re.search(rb'(<script type="application/ld\+json">)(.*?)(</script>)', body, re.S)
    return body[:old.start(2)] + json.dumps(value, ensure_ascii=False).replace('<', '\\u003c').encode() + body[old.end(2):]


def main():
    need(sys.argv[1:] in [[], ['--live-baseline']], 'only optional live baseline')
    old_initial = obj(A / 'INITIAL_SEAL.json')
    for row in old_initial['files']:
        bound(row)
    takeover_initial = obj(A / 'TAKEOVER_INITIAL_SEAL.json')
    bound(takeover_initial['old_INITIAL_SEAL'])
    for row in takeover_initial['new_own_inputs']:
        bound(row)
    oracle = obj(A / 'EXPECTED_OUTPUTS.json')
    aggregates = obj(A / 'BASELINE_AGGREGATES.json')
    original_index = bound(aggregates['raw_index'])
    original_sitemap = bound(aggregates['raw_sitemap'])
    original_config = read(A / 'raw/firebase.json')
    stage_seal_bytes = read(S / 'FINAL_SEAL.json')
    need(pin(stage_seal_bytes) == STAGE_FINAL, 'forwarded exact stage FINAL')
    stage_seal = json.loads(stage_seal_bytes)
    manifest_bytes = read(S / 'OWNED_MANIFEST.json')
    need(pin(manifest_bytes) == stage_seal['manifest'], 'stage manifest binding')
    manifest = json.loads(manifest_bytes)
    stage_files, stage_dirs = extent(S)
    need([x for x in stage_files if x['path'] not in TERMS] == manifest['files'], 'entire stage85-file namespace')
    need(stage_dirs == manifest['directories'] and len(stage_dirs) == 14 and len(stage_files) == 85, 'entire stage14-directory extent')
    need(manifest['exact_root_terminal_exclusions'] == sorted(TERMS) and manifest['subtree_or_future_exclusions'] == [], 'finite stage controls')
    code = read(S / 'stage_three.py')
    need(pin(code) == STAGE_CODE, 'current fully read code')
    references = obj(S / 'REFERENCE_INPUTS.json')
    protected_count = 0
    for ns in references['complete_frozen_namespaces_by_reference'].values():
        files, dirs = extent(Path(ns['root']))
        expected = [{'path': x['relative_path'], 'bytes': x['bytes'], 'SHA256': x['SHA256']} for x in ns['files']]
        need(files == sorted(expected, key=lambda x: x['path']) and dirs == ns['directories'], 'whole frozen namespace')
        protected_count += len(files)
    core = references['qualified_core']['named17_original_plus_sole_authorized405b']
    need(len(core) == 18, '17 originals plus sole405b')
    checkpoints = [row for row in core if Path(row['path']).name == 'checkpoint_subtree.py']
    need(len(checkpoints) == 1 and checkpoints[0]['SHA256'] == '405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0', 'sole separately authorized405b checkpoint')
    for row in core:
        bound(row)
    code_custody = {'protected_frozen_files': protected_count, 'qualified_core_entries': len(core)}
    approved_mains, native, media_orders = {}, {}, {}
    for row, reference in zip(oracle['rows'], references['records']):
        need(row['record_id'] == reference['record_id'], 'fixed reference order')
        approved_mains[row['slug']] = bound(row['MAIN'])
        source_ld = jsonld(bound(reference['approved_head_source']))
        media = source_ld.get('encoding', source_ld.get('associatedMedia'))
        media_orders[row['slug']] = [Path(urlsplit(x['contentUrl']).path).name for x in media]
        for asset in row['original_native_assets_full_literal']:
            native['public/research/' + row['slug'] + '/' + asset['original_api_file_object']['key']] = bound(asset)
        native['public/research/' + row['slug'] + '/citation.bib'] = bound(row['Bib'])
    candidate = {x['path']: read(S / 'candidate' / x['path']) for x in extent(S / 'candidate')[0]}
    expected_paths = {'public/' + x for x in oracle['exact_overlay_paths']} | {'firebase.json'}
    frame = read(S / 'raw/public/research/five-outgoing-centers-alpha16/index.html')
    frame_prefix = frame.split(b'<body>', 1)[1].split(b'<main ', 1)[0]
    frame_suffix = frame.rsplit(b'</main>', 1)[1]

    def guard(buffers):
        names = list(buffers)
        need(len(names) == len(set(x.casefold() for x in names)), 'case-unique output names')
        for name in names:
            parts = name.split('/')
            need(not name.startswith('/') and all(x not in ['', '.', '..'] for x in parts) and str(PurePosixPath(name)) == name, 'safe exact output pathname')
        need(set(names) == expected_paths, 'exact19 output map')
        for row in oracle['rows']:
            slug, url = row['slug'], row['proposed_canonical']
            page_bytes = buffers['public/research/' + slug + '/index.html']
            page = Page(page_bytes)
            need(len(page.ids) == len(set(page.ids)), 'unique page IDs')
            for tag in ['main', 'article', 'h1']:
                need(sum(t == tag for t, a in page.tags) == 1, 'one main/article/h1')
            scripts = [a for t, a in page.tags if t == 'script']
            need(scripts == [{'type': 'application/ld+json'}], 'nonexecutable JSON-LD only')
            frames = [a for t, a in page.tags if t == 'iframe']
            need([a.get('src') for a in frames] == (['paper.pdf#view=FitH', 'height-repair.pdf#view=FitH'] if row['record_id'] == '23205305' else ['paper.pdf#view=FitH']), 'exact original readers')
            need(all(a.get('title') for a in frames), 'titled readers')
            need([a.get('href') for t, a in page.tags if t == 'a' and a.get('class') == 'skip-link'] == ['#' + row['main_id']], 'matching skip target')
            need(page_bytes.count(approved_mains[slug]) == 1, 'whole approved MAIN bytes')
            main_start = page_bytes.index(approved_mains[slug])
            need(page_bytes.split(b'<body>', 1)[1][:main_start - page_bytes.index(b'<body>') - 6] == frame_prefix.replace(b'href="#main"', ('href="#' + row['main_id'] + '"').encode()), 'actual native header/navigation')
            need(page_bytes.endswith(frame_suffix), 'actual native footer')
            need(b'href="/research/research.css"' in page_bytes and b'href="/favicon.ico"' in page_bytes, 'shared stylesheet/favicon')
            need(b'main iframe{display:block;width:100%;height:80vh;min-height:500px;max-height:1000px;' in page_bytes, 'reader sizing')
            metas = [(a.get('name'), a.get('content')) for t, a in page.tags if t == 'meta' and 'name' in a]
            need(len(metas) == len(dict(metas)), 'unique meta names')
            metas = dict(metas)
            need(metas['robots'] == 'index,follow', 'indexable production robots')
            need(metas['citation_pdf_url'] == url + 'paper.pdf', 'correct local citation PDF')
            need(metas['citation_title'] == row['title'] and metas['citation_publication_date'] == row['datePublished'].replace('-', '/'), 'original citation identity/date')
            need(metas['citation_doi'] == '10.5281/zenodo.' + row['record_id'] and metas['citation_author_orcid'] == 'https://orcid.org/0009-0001-9320-500X', 'DOI/ORCID')
            need(('citation_version' in metas) == row['version_present'] and metas.get('citation_version') == row['version'], 'literal version presence')
            need([a.get('href') for t, a in page.tags if t == 'link' and a.get('rel') == 'canonical'] == [url], 'exact canonical')
            need([a.get('content') for t, a in page.tags if t == 'meta' and a.get('property') == 'og:url'] == [url], 'exact og:url')
            graph = jsonld(page_bytes)['@graph']
            need(len(graph) == 2, 'two coherent graph nodes')
            webpage, article = graph
            need(webpage['@id'] == url + '#page' and article['@id'] == url + '#article' and webpage['mainEntity'] == {'@id': article['@id']} and article['mainEntityOfPage'] == {'@id': webpage['@id']}, 'coherent graph identity')
            need(article['abstract'] == row['abstract_full'] and article['datePublished'] == row['datePublished'], 'complete abstract/original date')
            need(('version' in article) == row['version_present'] and article.get('version') == row['version'], 'JSON-LD version presence')
            media = article.get('encoding', article.get('associatedMedia'))
            need([Path(urlsplit(m['contentUrl']).path).name for m in media] == media_orders[slug], 'approved scholarly media order')
            by_name = {a['original_api_file_object']['key']: a for a in row['original_native_assets_full_literal']}
            need(len(media) == len(by_name), 'complete native media extent')
            for m in media:
                name = Path(urlsplit(m['contentUrl']).path).name
                need(name in by_name and m['contentUrl'] == url + name and m['encodingFormat'] == by_name[name]['whole_original_native_files_entry']['mimetype'] and m['sameAs'] == by_name[name]['original_api_file_object']['links']['self'], 'exact native media URL/MIME')
                if row['record_id'] == '23205305' and name.endswith('.zip'):
                    need('license' not in m, 'no blanket mixed-ZIP license')
        for name, data in native.items():
            need(buffers[name] == data, 'unchanged native/Bib asset')
        index = buffers['public/research/index.html']
        collection = jsonld(index)
        need(collection['mainEntity']['numberOfItems'] == 99, 'new ItemList count')
        restored = copy.deepcopy(collection)
        added_items = restored['mainEntity']['itemListElement'][96:]
        need(len(added_items) == 3 and [x['url'] for x in added_items] == [r['proposed_canonical'] for r in oracle['rows']] and [x['position'] for x in added_items] == [97, 98, 99], 'exact appended typed items')
        restored['mainEntity']['numberOfItems'] = 96
        del restored['mainEntity']['itemListElement'][96:]
        typed(restored, aggregates['CollectionPage_full_typed_object'])
        visible = re.findall(rb'<li>.*?</li>', index, re.S)
        need(visible[:96] == [x.encode() for x in aggregates['original_96_visible_li_buffers']] and len(visible) == 99, 'all old visible item bytes/order')
        old_script = re.search(rb'<script type="application/ld\+json">(.*?)</script>', original_index, re.S).group(1)
        new_script = re.search(rb'<script type="application/ld\+json">(.*?)</script>', index, re.S).group(1)
        recovered = index.replace(new_script, old_script, 1)
        for item in visible[96:]:
            need(recovered.count(b'      ' + item + b'\n') == 1, 'bounded appended visible buffer')
            recovered = recovered.replace(b'      ' + item + b'\n', b'', 1)
        need(recovered == original_index, 'all unrelated index bytes preserved')
        sitemap = buffers['public/research/sitemap.xml']
        nodes = re.findall(rb'<url>.*?</url>', sitemap, re.S)
        need(len(nodes) == 100 and nodes[:97] == [x.encode() for x in aggregates['original_97_sitemap_node_buffers']], 'all original sitemap nodes/order/date')
        need([x[0].text for x in list(ET.fromstring(sitemap))[97:]] == [r['proposed_canonical'] for r in oracle['rows']], 'exact added sitemap URLs')
        recovered = sitemap
        for node in nodes[97:]:
            need(recovered.count(b'  ' + node + b'\n') == 1, 'bounded sitemap addition')
            recovered = recovered.replace(b'  ' + node + b'\n', b'', 1)
        need(recovered == original_sitemap, 'all unrelated sitemap bytes preserved')
        need(buffers['firebase.json'] == original_config.replace(b'      "**/README.md",\n', b'', 1), 'only authorized README ignore removal')
        return True

    guard(candidate)
    mutations = []
    def reject(label, mutate):
        altered = dict(candidate)
        mutate(altered)
        try:
            guard(altered)
        except (ValueError, KeyError, IndexError) as exc:
            mutations.append({'id': label, 'rejected': True, 'reason': str(exc)})
        else:
            raise ValueError('in-memory falsifier escaped: ' + label)
    p132 = 'public/research/simple-young-nonprojective-injectives/index.html'
    p135 = 'public/research/binary-relation-liveness/index.html'
    p136 = 'public/research/rational-point-undecidability/index.html'
    def change(path, old, new):
        def mutate(buffers):
            need(old in buffers[path], 'actual finite mutation target')
            buffers[path] = buffers[path].replace(old, new, 1)
        return mutate
    def ld_change(path, callback):
        def mutate(buffers):
            value = jsonld(buffers[path])
            callback(value)
            buffers[path] = replace_ld(buffers[path], value)
        return mutate
    reject('F01-MAIN-word-loss', change(p132, b'A simple module', b'A module'))
    reject('F02-reader-directory', change(p135, b'src="paper.pdf#view=FitH"', b'src="/assets/paper.pdf#view=FitH"'))
    reject('F03-native-ZIP-byte', lambda b: b.__setitem__('public/research/rational-point-undecidability/source.zip', b['public/research/rational-point-undecidability/source.zip'] + b'X'))
    reject('F04-missing-README', lambda b: b.pop('public/research/binary-relation-liveness/README.md'))
    reject('F05-noindex', change(p132, b'content="index,follow"', b'content="noindex,nofollow"'))
    reject('F06-canonical', change(p132, b'rel="canonical" href="https://aleckriebel.com/research/simple-young-nonprojective-injectives/"', b'rel="canonical" href="https://example.invalid/"'))
    reject('F07-invented-version', ld_change(p135, lambda g: g['@graph'][1].__setitem__('version', '1.0')))
    reject('F08-MIME', ld_change(p132, lambda g: g['@graph'][1]['encoding'][0].__setitem__('encodingFormat', 'application/zip')))
    reject('F09-mixed-ZIP-license', ld_change(p136, lambda g: g['@graph'][1]['associatedMedia'][0].__setitem__('license', 'https://opensource.org/license/mit')))
    reject('F10-old-typed-ItemList', ld_change('public/research/index.html', lambda g: g['mainEntity']['itemListElement'][0].__setitem__('position', '1')))
    first_visible = aggregates['original_96_visible_li_buffers'][0].encode()
    reject('F11-old-visible-item', change('public/research/index.html', first_visible, first_visible.replace(b'Free spanning', b'Altered spanning', 1)))
    reject('F12-old-sitemap-date', change('public/research/sitemap.xml', b'2026-10-24', b'2026-11-16'))
    reject('F13-extra-excluded-output', lambda b: b.__setitem__('public/research/row133/index.html', b'excluded'))
    reject('F14-traversal', lambda b: b.__setitem__('public/research/../escape', b'escape'))
    reject('F14-case-alias', lambda b: b.__setitem__(p132.upper(), b[p132]))
    reject('F15-skip-target', change(p132, b'class="skip-link" href="#main-content"', b'class="skip-link" href="#main"'))
    reject('F15-executable-script', change(p132, b'</head>', b'<script>alert(1)</script></head>'))
    reject('F16-reader-sizing', change(p132, b'main iframe{display:block;width:100%;height:80vh;min-height:500px;max-height:1000px;', b'main iframe{display:block;'))
    reject('F04-config-README-still-ignored', lambda b: b.__setitem__('firebase.json', original_config))
    authority = json.loads(stage_seal_bytes)
    def guard_authority(value):
        need(value['production_install_authority'] is False and value['publication_authority'] is False and value['canonical_url'] is None and value['AA'] is None, 'F17 no inferred lifecycle authority')
    guard_authority(authority)
    altered_authority = dict(authority, production_install_authority=True)
    try:
        guard_authority(altered_authority)
    except ValueError as exc:
        authority_rejection = str(exc)
    else:
        raise ValueError('F17 authority mutation escaped')
    tree = ast.parse(code)
    verify = next(x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == 'verify')
    direct_fence = any(isinstance(x, ast.Expr) and isinstance(x.value, ast.Call) and isinstance(x.value.func, ast.Name) and x.value.func.id == 'fence' for x in verify.body)
    need(direct_fence, 'F18 actual pre-install-only direct baseline fence')
    old_public = {x['relative_path'] for x in obj(A / 'ACTUAL_WEBSITE_BASELINE.json')['public_files']}
    virtual_public = old_public | {x[7:] for x in candidate if x.startswith('public/')}
    need(len(old_public) == 631 and len(virtual_public) == 647 and old_public != virtual_public, 'F18 virtual install necessarily violates old live fence')
    if sys.argv[1:] == ['--live-baseline']:
        base = obj(A / 'ACTUAL_WEBSITE_BASELINE.json')
        current, dirs = extent(W / 'public')
        need(current == sorted([{'path': x['relative_path'], 'bytes': x['bytes'], 'SHA256': x['SHA256']} for x in base['public_files']], key=lambda x: x['path']) and dirs == base['public_directories'], 'optional old-live fence')
        index = read(W / '.git/index')
        need(pin(index) == {k: base['index'][k] for k in ['bytes', 'SHA256']}, 'restored original index bytes')
        need(stat.S_IMODE((W / '.git/index').stat().st_mode) == 0o600, 'restored original index mode')
    own_final = (A / 'FINAL_SEAL.json').exists()
    if own_final:
        final = obj(A / 'FINAL_SEAL.json')
        manifest_raw = read(A / 'OWNED_MANIFEST.json')
        need(pin(manifest_raw) == final['manifest'], 'own exact final manifest binding')
        own_manifest = json.loads(manifest_raw)
        files, dirs = extent(A)
        need([x for x in files if x['path'] not in TERMS] == own_manifest['files'] and dirs == own_manifest['directories'], 'own strict entire finite namespace')
        need(own_manifest['exact_root_terminal_exclusions'] == sorted(TERMS) and own_manifest['subtree_or_future_exclusions'] == [], 'own exact already-present terminals only')
    return {'status': 'PRIVATE_STAGE_MECHANISMS_PASS_WITH_EXPLICIT_LIMITS', 'checks': CHECKS, 'source_custody': code_custody, 'stage_extent': [85, 14], 'candidate_W_paths': 19, 'unchanged_MAIN_bytes': 40599, 'unchanged_native_assets': 10, 'unchanged_Bib': 3, 'virtual_counts': [647, 99, 100], 'in_memory_rejections': mutations, 'authority_mutation_detected': True, 'authority_rejection_reason': authority_rejection, 'writer_closure_scope': 'pre-install current-W-only; no post-install capability inferred', 'row132_metadata_order': {'native_API': ['source-and-verification.zip', 'paper.pdf'], 'approved_source_and_actual_stage_JSON_LD': media_orders['simple-young-nonprojective-injectives'], 'qualification': 'Source scholarly order retained; no asset or MAIN loss. Difference from pre-candidate expectation is explicit.'}, 'symlink_FIFO_and_output_race_scope': 'Actual namespace ordinary and static code reviewed; no foreign-path/race mutation or authoring replay.', 'live_baseline_checked': bool(sys.argv[1:]), 'own_final_bound': own_final, 'production_authority': False, 'writes': 0, 'network': 0}


if __name__ == '__main__':
    print(json.dumps(main(), ensure_ascii=False, sort_keys=True))
