#!/usr/bin/env python3
"""One fixed, read-only data audit. No producer/native imports, subprocess or writes."""
from pathlib import Path
import copy
import hashlib
import html
from html.parser import HTMLParser
import json
import posixpath
import re
import stat
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urlsplit

O = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/low-exponent-su5-stage-audit-sol-20261116')
P = O.parent.parent
A = P / 'verification/low-exponent-su5-stage-sol-20261116'
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
checks = []

def require(value, label):
    if not value:
        raise AssertionError(label)
    checks.append(label)

def pin(f, root=None):
    s = f.lstat()
    require(stat.S_ISREG(s.st_mode), 'regular:' + str(f))
    b = f.read_bytes()
    return {'path': str(f.relative_to(root)) if root else str(f), 'bytes': len(b),
            'SHA256': hashlib.sha256(b).hexdigest(), 'mode': format(stat.S_IMODE(s.st_mode), '04o')}

def equal_pin(f, row):
    a = pin(f)
    require(a['bytes'] == row['bytes'] and a['SHA256'] == row.get('SHA256', row.get('sha256'))
            and int(a['mode'], 8) == int(row['mode'], 8), 'whole-pin:' + str(f))

def snapshot(root):
    files, dirs = [], [{'path': '.', 'mode': format(stat.S_IMODE(root.lstat().st_mode), '04o')}]
    require(root.is_dir() and not root.is_symlink(), 'ordinary-root:' + str(root))
    for f in sorted(root.rglob('*')):
        require(not f.is_symlink(), 'no-symlink:' + str(f))
        if f.is_file():
            files.append(pin(f, root))
        else:
            require(f.is_dir(), 'ordinary-directory:' + str(f))
            dirs.append({'path': f.relative_to(root).as_posix(), 'mode': format(stat.S_IMODE(f.stat().st_mode), '04o')})
    return files, dirs

def element(text, tag):
    m = re.findall(r'<' + tag + r'\b[^>]*>.*?</' + tag + '>', text, re.S)
    require(len(m) == 1, 'one-element:' + tag)
    return m[0]

def schema(text):
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)
    require(m is not None and len(re.findall(r'application/ld\+json', text)) == 1, 'one-JSON-LD')
    return json.loads(m.group(1)), m.group(1)

def raw_items(script):
    start = script.index('"itemListElement"')
    start = script.index('[', start) + 1
    decoder, values, raws, pos = json.JSONDecoder(), [], [], start
    while True:
        while script[pos].isspace() or script[pos] == ',':
            pos += 1
        if script[pos] == ']':
            return values, raws, start, pos
        value, size = decoder.raw_decode(script[pos:])
        values.append(value)
        raws.append(script[pos:pos + size])
        pos += size

class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.nodes = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))

def normalize_head(h):
    h = re.sub(r'(<script type="application/ld\+json">).*?(</script>)', r'\1<JSON>\2', h, flags=re.S)
    h = re.sub(r'<meta name="(?:robots|citation_pdf_url)"[^>]*>\n?', '', h)
    h = re.sub(r'<link rel="canonical"[^>]*>\n?', '', h)
    return re.sub(r'<meta property="og:url"[^>]*>\n?', '', h)

def overlay(relative):
    candidate = A / 'public' / relative
    return candidate if candidate.is_file() else W / 'public' / relative

def main():
    baseline = json.loads((O / 'BASELINE.json').read_text())
    expected = json.loads((O / 'EXPECTED_CONTRACT.json').read_text())
    inputs = json.loads((O / 'EXPECTED_INPUTS.json').read_text())
    initial = json.loads((O / 'INITIAL_SEAL.json').read_text())
    equal_pin(O / 'INITIAL_SEAL.json', {'bytes': 1648, 'SHA256': '8ae68af900b89f19aea545e010074370deb3f45ce9dd2dc354acc2cd439b08bb', 'mode': '0644'})
    for row in initial['payloads']:
        equal_pin(O / row['path'], row)
    for name, size, digest in [('FINAL.json', 15851, 'aa081369d082b380eabd0722cbc7a5bf3458d123c8f8778dbd2fe43ffbaf74b5'),
                               ('OWNED_MANIFEST.json', 8835, '0f8f75c60d0ba1ec0780e97db5669f192b6a07055f320a426a039c4df9c81d81'),
                               ('TARGET_PLAN.json', 6051, '0b9f1bfd79badaf0386748caba2ac195fbb63e2e83717ede89ad1aa3f274253f')]:
        equal_pin(A / name, {'bytes': size, 'SHA256': digest, 'mode': '0644'})
    stage_before = snapshot(A)
    manifest = json.loads((A / 'OWNED_MANIFEST.json').read_text())
    require(len(stage_before[0]) == 34 and len(stage_before[1]) == 5, 'exact-stage34/4')
    require({r['path'] for r in manifest['files']} == {r['path'] for r in stage_before[0]}, 'complete-stage-manifest-paths')
    require(stage_before[1] == manifest['directories'], 'stage-directory-modes')
    for row in manifest['files']:
        if 'bytes' in row:
            equal_pin(A / row['path'], row)
    for row in inputs['root_clearance_reports'] + [inputs['adoption']]:
        equal_pin(Path(row['path']), row)
    for packet in inputs['adopted_packets']:
        root = Path(packet['root'])
        require(snapshot(root)[0] == packet['files'], 'whole-adopted-packet:' + root.name)
        require(len(snapshot(root)[1]) == 1, 'flat-adopted-packet:' + root.name)
    source_count = 0
    for source in inputs['sources']:
        root = P / 'papers' / str(source['record']) / 'sources'
        for row in source['controls']:
            equal_pin(Path(row['path']), row)
        sm = json.loads((root / 'SOURCE_MANIFEST.json').read_text())
        rows = sm['files']
        current, dirs = snapshot(root)
        require({r['path'] for r in current} == {r['path'] for r in rows} | {'SOURCE_FINAL.json', 'SOURCE_MANIFEST.json'}, 'whole-source-paths')
        for row in rows:
            equal_pin(root / row['path'], row)
        require({r['path']: int(r['mode'], 8) for r in dirs[1:]} == {r['path']: int(r['mode'], 8) for r in sm['directories']}, 'source-directory-topology-modes')
        source_count += len(current)
    require(source_count == 306, 'both-native-source306-files')
    current_public, current_dirs = snapshot(W / 'public')
    require(current_public == baseline['public_files'], 'all747-current-public-buffers-modes')
    require(current_dirs == baseline['public_directory_modes_including_root'], 'all366-current-public-directory-modes')
    for g in [baseline['website_git'], baseline['Math_git']]:
        for key in ['HEAD_file', 'index', 'config']:
            equal_pin(Path(g[key]['path']), g[key])
        if g['commit_read_from'].endswith('packed-refs'):
            require(g['commit'] + ' ' + g['ref'] in Path(g['commit_read_from']).read_text().splitlines(), 'packed-main-ref-exact')
        else:
            require(Path(g['commit_read_from']).read_text().strip() == g['commit'], 'current-master-ref-exact')
    global_guards = json.loads((O / 'GLOBAL_TEMPLATE_GUARDS.json').read_text())
    for row in global_guards['website_configuration_guards']:
        equal_pin(Path(row['path']), row)
    targets = {r['path']: r for r in expected['exact_target_paths']}
    candidate, candidate_dirs = snapshot(A / 'public')
    require({r['path'] for r in candidate} == set(targets), 'exact15-candidate-paths-no-extra')
    require(sum(r['change'] == 'A' for r in targets.values()) == 13 and sum(r['change'] == 'M' for r in targets.values()) == 2, '13A2M')
    for path, row in targets.items():
        if row.get('expected_whole_buffer'):
            equal_pin(A / 'public' / path, row['expected_whole_buffer'])
        require((W / 'public' / path).exists() == (row['change'] == 'M'), 'target-baseline-presence:' + path)
    plan = json.loads((A / 'TARGET_PLAN.json').read_text())
    require({r['target'] for r in plan['targets']} == set(targets), 'actual-plan-exact-target-set')
    for row in plan['targets']:
        equal_pin(A / 'public' / row['target'], row['after'])
        require(row['operation'] == ('ADD' if targets[row['target']]['change'] == 'A' else 'MODIFY'), 'plan-operation')
    page_results = []
    for paper in expected['papers']:
        root = Path(paper['writer'])
        relative = 'research/' + paper['slug'] + '/index.html'
        old = (root / 'index.html').read_text()
        text = (A / 'public' / relative).read_text()
        head, oldhead = element(text, 'head'), element(old, 'head')
        require(text.replace(head, '<HEAD>', 1) == old.replace(oldhead, '<HEAD>', 1), 'whole-outside-HEAD-exact')
        require(element(text, 'main').encode() == (root / 'MAIN.html').read_bytes().rstrip(b'\n'), 'approved-entire-MAIN')
        require(normalize_head(head) == normalize_head(oldhead), 'all-other-head-bytes-exact')
        tags = Tags(text)
        ids = [a['id'] for _, a in tags.nodes if 'id' in a]
        require(len(ids) == len(set(ids)), 'unique-HTML-IDs')
        for _, attrs in tags.nodes:
            if 'aria-labelledby' in attrs:
                require(all(x in ids for x in attrs['aria-labelledby'].split()), 'aria-label-targets')
        meta = {a.get('name', a.get('property')): a['content'] for t, a in tags.nodes if t == 'meta' and 'content' in a}
        canonical = paper['canonical']
        require([a['href'] for t, a in tags.nodes if t == 'link' and a.get('rel') == 'canonical'] == [canonical], 'exact-canonical')
        require(meta['og:url'] == canonical and not any('noindex' in str(x).lower() for x in meta.values()), 'public-indexable-og')
        require(meta['description'] == meta['og:description'] == paper['description'], 'approved-short-description')
        visible = re.search(r'<p id="original-abstract">(.*?)</p>', text, re.S).group(1)
        require(html.unescape(re.sub('<[^>]+>', '', visible)) == paper['complete_original_abstract'] == meta['DC.description'], 'whole-abstract-visible-DC')
        model = json.loads((root / 'model.json').read_text())
        sch, _ = schema(text)
        exp = copy.deepcopy(model.get('scholarly_schema', model.get('schema')))
        exp.update(url=canonical, mainEntityOfPage=canonical)
        exp['@id'] = canonical + '#article'
        for e in exp['encoding']:
            e['contentUrl'] = canonical + e['contentUrl']
        require(sch == exp and sch['abstract'] == paper['complete_original_abstract'], 'exact-approved-schema-activation-and-abstract')
        require(model['native_record_description'] == paper['distinct_native_Description'], 'distinct-original-Description-unmodified')
        native_list = re.search(r'<ol id="native-assets">(.*?)</ol>', text, re.S).group(1)
        names = [a['href'] for t, a in Tags(native_list).nodes if t == 'a' and not urlsplit(a['href']).scheme]
        require(names == paper['native_order'], 'exact-native-download-order')
        pdf = next(n for n in names if n.endswith('.pdf'))
        require(meta['citation_pdf_url'] == canonical + pdf, 'absolute-citation-PDF')
        require(sch['author']['identifier'] == 'https://orcid.org/0009-0001-9320-500X', 'author-ORCID')
        for t, attrs in tags.nodes:
            value = attrs.get('href', attrs.get('src'))
            if not value:
                continue
            u = urlsplit(value)
            if u.scheme or u.netloc:
                continue
            if not u.path:
                require(not u.fragment or unquote(u.fragment) in ids, 'local-fragment-target')
                continue
            dest = posixpath.normpath(u.path.lstrip('/') if u.path.startswith('/') else posixpath.join(posixpath.dirname(relative), unquote(u.path)))
            if u.path.endswith('/'):
                dest += '/index.html'
            require(not dest.startswith('../') and overlay(dest).is_file(), 'local-overlay-resolves:' + dest)
        page_results.append({'record': paper['record'], 'HTML_SHA256': hashlib.sha256(text.encode()).hexdigest(), 'MAIN_SHA256': hashlib.sha256(element(text, 'main').encode()).hexdigest(), 'native_order': names, 'all_local_paths_resolve_statically': True})
    old_index = (W / 'public/research/index.html').read_text()
    new_index = (A / 'public/research/index.html').read_text()
    old_sch, old_raw = schema(old_index)
    new_sch, new_raw = schema(new_index)
    values, raw, _, _ = raw_items(old_raw)
    newvalues, newraw, _, _ = raw_items(new_raw)
    require(len(values) == 121 and len(newvalues) == 123 and newvalues[:121] == values and newraw[:121] == raw, 'all121-old-typed-and-raw-JSON-items-order-exact')
    old_lis = re.findall(r'<li\b[^>]*>.*?</li>', re.search(r'<ul>(.*?)</ul>', old_index, re.S).group(1), re.S)
    new_lis = re.findall(r'<li\b[^>]*>.*?</li>', re.search(r'<ul>(.*?)</ul>', new_index, re.S).group(1), re.S)
    require(old_lis == baseline['old_visible_items_raw'] and new_lis[:121] == old_lis and len(new_lis) == 123, 'all121-old-visible-raw-units-order-exact')
    reduced = copy.deepcopy(new_sch)
    reduced['mainEntity']['itemListElement'] = reduced['mainEntity']['itemListElement'][:121]
    reduced['mainEntity']['numberOfItems'] = 121
    require(reduced == old_sch and new_sch['mainEntity']['numberOfItems'] == 123, 'only-two-typed-additions-and-count')
    for j, paper in enumerate(expected['papers'], 122):
        require(newvalues[j-1] == {'@type': 'ListItem', 'position': j, 'url': paper['canonical'], 'name': json.loads((Path(paper['writer']) / 'model.json').read_text())['title']}, 'new-typed-entry-identity')
    without_new = new_index.replace('\n'.join(new_lis[121:]) + '\n', '', 1).replace(new_raw, old_raw, 1)
    require(without_new == old_index, 'entire-index-reverses-to-original-bytes')
    old_xml = (W / 'public/research/sitemap.xml').read_text()
    new_xml = (A / 'public/research/sitemap.xml').read_text()
    old_nodes = re.findall(r'<url>.*?</url>', old_xml, re.S)
    new_nodes = re.findall(r'<url>.*?</url>', new_xml, re.S)
    require(old_nodes == baseline['old_sitemap_nodes_raw'] and new_nodes[:122] == old_nodes and len(new_nodes) == 124, 'all122-old-whole-sitemap-nodes-order-exact')
    require(new_xml.replace('\n'.join(new_nodes[122:]) + '\n', '', 1) == old_xml, 'entire-sitemap-reverses-to-original-bytes')
    ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
    parsed = ET.fromstring(new_xml)
    locs = [x.find(ns + 'loc').text for x in parsed]
    require(len(locs) == len(set(locs)) == 124 and locs[-2:] == [p['canonical'] for p in expected['papers']], 'unique-sitemap-new-identity')
    require(all(x.find(ns + 'lastmod').text == '2026-11-17' for x in list(parsed)[-2:]), 'actual-stage-day-new-lastmod')
    receipt = json.loads((A / 'AGGREGATE_PROOF.json').read_text())
    require(isinstance(receipt['new_visible_units'], list) and receipt['new_visible_units'] == new_lis[121:], 'literal-two-HTML-unit-list-not-count')
    require(json.loads((A / 'BUILD_RESULTS.json').read_text())['index_items_after'] == 123, 'separate-actual-total123')
    require(snapshot(A) == stage_before, 'whole-frozen34/4-stage-unchanged-after-audit')
    require(snapshot(W / 'public') == (current_public, current_dirs), 'whole747/366-W-unchanged-after-audit')
    print(json.dumps({'status': 'PASS_FIXED15_PRIVATE_STAGE_DATA_FIDELITY', 'checks_including_whole-file-guards': len(checks), 'candidate_files': candidate, 'candidate_child_directories': len(candidate_dirs)-1, 'pages': page_results, 'source_files': source_count, 'index_items': 123, 'sitemap_nodes': 124, 'public_files_if_installed': 760, 'stage34_4_and_W747_366_unchanged': True, 'producer_builder_executions_by_auditor': 0, 'own_data_audit_invocations': 1, 'production_authority': False, 'browser_native_reader_download_or_live_certificate': False}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
