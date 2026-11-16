#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Bounded three-page private stage. Default reads only; --build writes only this folder."""
import hashlib
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import stat
import struct
import sys
from datetime import datetime, timezone
from xml.etree import ElementTree as ET

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
R = P / 'verification/outer-pedal-godbillon-vey-stage-sol-20261116'
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
M = Path('/Users/alec/Documents/Math')
A = P / 'verification/root-outer-pedal-godbillon-vey-gramian-editorial-adoption-20261116.json'
ORDER = ['23398175', '23357329', '23153134']
SLUGS = ['outer-focal-pedal-area-product', 'unbounded-godbillon-vey-fixed-hyperbolic-manifold', 'negative-curvature-observation-gramian']
PDFS = ['k605a-outer-focal-pedal-areas.pdf', 'taut_godbillon_vey.pdf', 'negative_gramian_cover.pdf']
CSS_SHA = 'f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a'

def need(test, message):
    if not test:
        raise RuntimeError(message)
def sha(body):
    return hashlib.sha256(body).hexdigest()
def pin(path):
    s = path.lstat()
    need(stat.S_ISREG(s.st_mode), 'Not a regular file: ' + str(path))
    b = path.read_bytes()
    blob = hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
    return {'path': str(path), 'bytes': len(b), 'sha256': sha(b), 'mode': format(stat.S_IMODE(s.st_mode), '04o'), 'Git_blob_SHA1': blob}
def check_pin(item):
    path = P / item['path']
    actual = pin(path)
    need(actual['bytes'] == item['bytes'] and actual['sha256'] == item.get('SHA256', item.get('sha256')), 'Input mismatch: ' + str(path))
    return actual
def inventory(root):
    need(root.is_dir() and not root.is_symlink(), 'Unsafe inventory root')
    files, directories = [], []
    for here, dirs, names in os.walk(root, followlinks=False):
        dirs.sort()
        names.sort()
        hp = Path(here)
        s = hp.lstat()
        need(stat.S_ISDIR(s.st_mode), 'Non-directory topology')
        directories.append({'path': str(hp.relative_to(root)), 'mode': format(stat.S_IMODE(s.st_mode), '04o')})
        for name in dirs:
            need(stat.S_ISDIR((hp / name).lstat().st_mode), 'Symlink/special directory')
        for name in names:
            item = pin(hp / name)
            item['path'] = str((hp / name).relative_to(root))
            files.append(item)
    return {'root': str(root), 'files': sorted(files, key=lambda x: x['path']), 'directories': sorted(directories, key=lambda x: x['path'])}
def ref_head(root):
    git = root / '.git'
    need(git.is_dir() and not git.is_symlink(), 'Expected native .git directory')
    text = (git / 'HEAD').read_text().strip()
    need(text.startswith('ref: refs/heads/'), 'Unexpected detached HEAD')
    ref = text[5:]
    loose = git / ref
    if loose.is_file():
        commit = loose.read_text().strip()
    else:
        matches = [line.split()[0] for line in (git / 'packed-refs').read_text().splitlines() if line.endswith(' ' + ref)]
        need(len(matches) == 1, 'Packed ref absent/ambiguous')
        commit = matches[0]
    return text, commit
def git_guard(root, head_expected, index_bytes, index_sha, config_sha):
    git = root / '.git'
    need(not (git / 'index.lock').exists(), 'Native index lock present')
    head, commit = ref_head(root)
    need(commit == head_expected, 'Unexpected HEAD drift')
    index = pin(git / 'index')
    need(index['bytes'] == index_bytes and index['sha256'] == index_sha and index['mode'] == '0644', 'Native index drift')
    signature, version, records = struct.unpack('>4sII', (git / 'index').read_bytes()[:12])
    need(signature == b'DIRC' and version in (2, 3, 4), 'Unexpected native index header')
    config = pin(git / 'config')
    need(config['sha256'] == config_sha, 'Config drift')
    guards = [pin(git / 'HEAD'), index, config]
    for relative in ['packed-refs', head[5:], 'config.worktree']:
        if (git / relative).exists():
            guards.append(pin(git / relative))
    return {'HEAD': head, 'commit': commit, 'index_version': version, 'index_records': records, 'files': guards}
def public_index_binding(public):
    data = (W / '.git/index').read_bytes()
    signature, version, count = struct.unpack('>4sII', data[:12])
    need(signature == b'DIRC' and version == 2 and count == 58667, 'Unexpected exact W index schema')
    offset, indexed = 12, {}
    for _ in range(count):
        start = offset
        need(start + 62 <= len(data) - 20, 'Truncated index entry')
        mode = struct.unpack('>I', data[start+24:start+28])[0]
        blob = data[start+40:start+60].hex()
        flags = struct.unpack('>H', data[start+60:start+62])[0]
        need(not (flags & 0x4000) and ((flags >> 12) & 3) == 0, 'Extended/unmerged index entry')
        end = data.index(b'\0', start + 62)
        path = data[start+62:end].decode('utf-8')
        offset = start + ((end + 1 - start + 7) // 8) * 8
        if path.startswith('public/'):
            need(path[7:] not in indexed, 'Duplicate public index path')
            indexed[path[7:]] = {'Git_blob_SHA1': blob, 'Git_mode': format(mode, 'o')}
    need(hashlib.sha1(data[:-20]).digest() == data[-20:], 'Native index checksum mismatch')
    need(set(indexed) == {x['path'] for x in public['files']}, 'Public/native-index path set drift')
    for item in public['files']:
        entry = indexed[item['path']]
        need(item['Git_blob_SHA1'] == entry['Git_blob_SHA1'], 'Public/native-index content drift: ' + item['path'])
        need(entry['Git_mode'] in ['100644', '100755'], 'Nonregular public Git entry')
        need(bool(int(item['mode'], 8) & 0o111) == (entry['Git_mode'] == '100755'), 'Public execute-mode drift')
    return {'public_entries_bound': len(indexed), 'all58667_entries_decoded': count, 'index_checksum_valid': True, 'public_blobs_and_exec_bits_match': True}
def guards(authority):
    public = inventory(W / 'public')
    need(len(public['files']) == 727 and len(public['directories']) == 364, 'Public topology drift')
    wg = git_guard(W, 'ff36a8299805d9a6196a3d5b081d354c87627056', 9051646, '1959097114e85b4e451c3dca1a2bcf35cf1592442378633688d85d8416d69a7e', '63d9c1bb64a26d8b6505c6e16b299decb2884d3bf3de3c5862eb4655442f4c54')
    need(wg['HEAD'] == 'ref: refs/heads/master' and wg['index_records'] == 58667, 'Wrong W branch/count')
    mg = git_guard(M, 'a4ce3c37dad209339e490d18dcced6c48cf912d2', 25854746, '91b10d938f7d737226662bbff3b07016dcc0e501376a045811ab4e930c6fbb11', '2c083de0f0839443ce1ed062a8c1f2be83cbc30f838e5350e567a8153b7b3a47')
    need(mg['HEAD'] == 'ref: refs/heads/main', 'Wrong Math branch')
    source, editorial = [], []
    for record in authority['records']:
        rid = record['record']
        s = inventory(P / 'papers' / rid / 'sources')
        e = inventory(P / 'papers' / rid / 'reviews/editorial')
        f = inventory((P / record['fact_FINAL']['path']).parent)
        need(len(s['files']) == record['source_extent']['files'] and len(s['directories']) - 1 == record['source_extent']['child_directories'], 'Source extent drift')
        need(len(e['files']) == record['writer_extent']['files'] and len(e['directories']) - 1 == record['writer_extent']['child_directories'], 'Writer extent drift')
        need(len(f['files']) == record['fact_packet_files'], 'Fact extent drift')
        source.append(s)
        editorial.extend([e, f])
    need(sum(len(x['files']) for x in source) == 531 and sum(len(x['files']) for x in editorial) == 172, 'Whole input count mismatch')
    return {'public': public, 'W_public_native_index_binding': public_index_binding(public), 'W_native_Git': wg, 'Math_native_Git': mg, 'sources': source, 'editorial_and_fact': editorial}
def typed(value):
    if isinstance(value, dict):
        return ['dict', [[key, typed(item)] for key, item in value.items()]]
    if isinstance(value, list):
        return ['list', [typed(item) for item in value]]
    return [type(value).__name__, value]
def json_array_units(text):
    found = list(re.finditer(r'"itemListElement"\s*:\s*\[', text))
    need(len(found) == 1, 'Ambiguous ItemList array')
    i = found[0].end()
    units = []
    decoder = json.JSONDecoder()
    while True:
        while text[i].isspace():
            i += 1
        if text[i] == ']':
            return units, i
        start = i
        _, i = decoder.raw_decode(text, i)
        units.append(text[start:i])
        while text[i].isspace():
            i += 1
        need(text[i] in ',]', 'Malformed JSON array separator')
        if text[i] == ',':
            i += 1
def main_bytes(body):
    matches = list(re.finditer(br'<main id="main">(.*?)</main>', body, re.S))
    need(len(matches) == 1, 'Expected one exact semantic MAIN')
    return matches[0].group(1)
class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
    def handle_data(self, value):
        self.parts.append(value)
def plain(fragment):
    parser = Text()
    parser.feed(fragment)
    return ' '.join(''.join(parser.parts).split())
def schema_span(text):
    matches = list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', text, re.S))
    need(len(matches) == 1, 'Expected one JSON-LD script')
    return matches[0]
def meta_value(head, key):
    m = re.findall(r'<meta name="' + re.escape(key) + r'" content="([^"]*)">', head)
    need(len(m) == 1, 'Missing/ambiguous meta ' + key)
    return html.unescape(m[0])
def deployment_page(record, source, model, pdf):
    raw = source.decode('utf-8')
    old_head, rest = raw.split('</head>', 1)
    head = old_head
    for key in ['robots', 'editorial-status']:
        head, count = re.subn(r'<meta name="' + key + r'" content="[^"]*">\n', '', head)
        need(count == 1, 'Expected exact private meta flag')
    need(head.count('href="research.css"') == 1, 'Unexpected stylesheet reference')
    head = head.replace('href="research.css"', 'href="../research.css"')
    canonical = 'https://aleckriebel.com/research/' + record['proposed_slug'] + '/'
    old_pdf = '<meta name="citation_pdf_url" content="' + pdf + '">'
    need(head.count(old_pdf) == 1, 'Unexpected PDF citation')
    head = head.replace(old_pdf, '<meta name="citation_pdf_url" content="' + canonical + pdf + '">')
    if record['record'] == '23153134':
        head, count = re.subn(r'<title>.*?</title>', '<title>Negative-curvature observation Gramian | Alec Kriebel</title>', head)
        need(count == 1, 'Ambiguous SEO title')
    span = schema_span(head)
    scholarly = json.loads(span.group(1))
    original_scholarly = json.loads(span.group(1))
    need(scholarly['abstract'] == model['abstract'], 'Original schema abstract/model mismatch')
    scholarly['url'] = canonical
    scholarly['@id'] = canonical + '#article'
    scholarly['mainEntityOfPage'] = canonical
    scholarly['isAccessibleForFree'] = True
    old_encoding = scholarly.get('encoding', [])
    need(isinstance(old_encoding, list), 'Unexpected encoding type')
    encoding = []
    for name in record['native_assets_order']:
        previous = next((dict(x) for x in old_encoding if x.get('contentUrl') == name), {})
        previous.update({'@type': 'MediaObject', 'contentUrl': canonical + name})
        if not previous.get('encodingFormat'):
            previous['encodingFormat'] = {'.pdf': 'application/pdf', '.zip': 'application/zip', '.json': 'application/json'}.get(Path(name).suffix, 'text/plain')
        encoding.append(previous)
    scholarly['encoding'] = encoding
    for key, value in original_scholarly.items():
        if key not in ['url', '@id', 'mainEntityOfPage', 'isAccessibleForFree', 'encoding']:
            need(typed(scholarly[key]) == typed(value), 'Changed scholarly content: ' + key)
    head = head[:span.start(1)] + json.dumps(scholarly, ensure_ascii=False, indent=2) + head[span.end(1):]
    need('rel="canonical"' not in head and 'property="og:url"' not in head, 'Unexpected existing canonical/OG URL')
    title = scholarly['name']
    description = meta_value(head, 'description')
    extra = '\n<link rel="canonical" href="' + canonical + '">\n<meta property="og:url" content="' + canonical + '">\n'
    for key, value in [('type', 'article'), ('title', title), ('description', description)]:
        if 'property="og:' + key + '"' not in head:
            extra += '<meta property="og:' + key + '" content="' + html.escape(value, quote=True) + '">\n'
    head += extra
    result = (head + '</head>' + rest).encode('utf-8')
    need(main_bytes(result) == main_bytes(source), 'Changed approved MAIN inner bytes')
    need(result.split(b'</head>', 1)[1] == source.split(b'</head>', 1)[1], 'Changed body/exterior')
    need(meta_value(head, 'DC.description') == model['abstract'], 'DC abstract mismatch')
    fragment = raw.split('<section id="original-abstract">', 1)[1].split('</section>', 1)[0] if record['record'] == '23398175' else raw
    match = re.search(r'<p(?: id="original-abstract")?>(.*?)</p>', fragment, re.S) if record['record'] == '23398175' else re.search(r'<p id="original-abstract">(.*?)</p>', fragment, re.S)
    need(match is not None and plain(match.group(1)) == model['abstract'], 'Visible original abstract mismatch')
    ordered = re.search(r'<ol id="native-(?:downloads|assets)">(.*?)</ol>', raw, re.S)
    need(ordered is not None, 'Missing native list')
    links = [x for x in re.findall(r'href="([^"]+)"', ordered.group(1)) if ':' not in x]
    need(links == record['native_assets_order'], 'Native asset order changed')
    return result, {'record': record['record'], 'slug': record['proposed_slug'], 'canonical': canonical, 'title': title, 'description': description, 'date': scholarly['datePublished'], 'MAIN_inner_bytes': len(main_bytes(result)), 'MAIN_inner_sha256': sha(main_bytes(result)), 'body_exterior_exact': True, 'abstract_visible_schema_DC_exact': True}

def main():
    need(Path(__file__).resolve() == R / 'stage_builder.py', 'Unexpected builder location')
    need(sys.argv[1:] in ([], ['--build']), 'Only explicit --build or read-only default accepted')
    build = sys.argv[1:] == ['--build']
    need(sha(A.read_bytes()) == '7b5367a6c98c13e304f93d8a582cc22c7fe0688e5cc0378bbbf1dce04b182cab' and A.stat().st_size == 18652, 'Root authority mismatch')
    authority = json.loads(A.read_bytes())
    need([x['record'] for x in authority['records']] == ORDER and [x['proposed_slug'] for x in authority['records']] == SLUGS, 'Wrong record/slug scope')
    hold_path = R / 'HOLD_CHECKPOINT.json'
    need(sha(hold_path.read_bytes()) == '6e33aa8a243e76ff2e4993db2903572cbf3183d6bc0a00e06e4fc4b3cac92248', 'Old HOLD changed')
    hold = json.loads(hold_path.read_bytes())
    for item in hold['payloads']:
        actual = pin(R / item['path'])
        need(all(actual[k] == item[k] for k in ['bytes', 'sha256', 'mode']), 'Original HOLD payload changed')
    need(pin(hold_path)['mode'] == '0644', 'Old HOLD mode changed')
    inputs = [pin(A), pin(hold_path)] + [pin(R / item['path']) for item in hold['payloads']]
    for record in authority['records']:
        for item in list(record['writer_pins'].values()) + [record['fact_FINAL'], record['fact_manifest'], record['fact_REPORT']] + record['root_individually_viewed_selected_images']:
            inputs.append(check_pin(item))
        for manifest_item in [record['writer_pins']['OWNED_MANIFEST.json'], record['fact_manifest']]:
            mp = P / manifest_item['path']
            manifest = json.loads(mp.read_bytes())
            payloads = manifest['files'] if record['record'] == '23357329' and manifest_item == record['writer_pins']['OWNED_MANIFEST.json'] else manifest['payloads']
            bound = {item['path'] for item in payloads} | {'FINAL.json', 'OWNED_MANIFEST.json'}
            actual_names = {str(x.relative_to(mp.parent)) for x in mp.parent.rglob('*') if x.is_file()}
            need(actual_names == bound, 'Whole manifest extent mismatch')
            for item in payloads:
                p = mp.parent / item['path']
                need(p.resolve().is_relative_to(mp.parent.resolve()), 'Manifest escaped packet')
                actual = pin(p)
                need(actual['bytes'] == item['bytes'] and actual['sha256'] == item.get('sha256', item.get('SHA256')), 'Manifest payload mismatch')
                if 'mode' in item:
                    mode = item['mode'] if isinstance(item['mode'], int) else int(item['mode'], 8)
                    need(int(actual['mode'], 8) == mode, 'Manifest mode mismatch')
    before = guards(authority)
    need(pin(W / 'public/research/research.css')['sha256'] == CSS_SHA, 'Shared CSS drift')
    outputs, pages, native_pins = {}, [], []
    for record, pdf in zip(authority['records'], PDFS):
        root = P / 'papers' / record['record'] / 'reviews/editorial'
        source = (root / 'preview/index.html').read_bytes()
        need(main_bytes(source) == main_bytes((root / 'MAIN.html').read_bytes()), 'Writer MAIN mismatch')
        model = json.loads((root / 'PAGE_MODEL.json').read_bytes())
        candidate, details = deployment_page(record, source, model, pdf)
        prefix = 'research/' + record['proposed_slug'] + '/'
        need(not (W / 'public' / prefix).exists(), 'Target slug already exists')
        outputs[prefix + 'index.html'] = candidate
        for name in record['native_assets_order'] + ['citation.bib']:
            body = (root / 'preview' / name).read_bytes()
            if name != 'citation.bib':
                native = P / 'papers' / record['record'] / 'sources/assets' / name
                need(native.read_bytes() == body, 'Native asset differs: ' + name)
                native_pins.append(pin(native))
            outputs[prefix + name] = body
        pages.append(details)
    old_index = (W / 'public/research/index.html').read_text()
    need(sha(old_index.encode()) == 'a46f44595c3843232722caa098f42e94920fb7fc83e04c2410768e0b46c780ad', 'Index baseline drift')
    need(all(x['canonical'] not in old_index for x in pages), 'New canonical already occurs in old index')
    old_script_match = schema_span(old_index)
    old_script = old_script_match.group(1)
    old_object = json.loads(old_script)
    old_units, close = json_array_units(old_script)
    need(len(old_units) == 118 and old_object['mainEntity']['numberOfItems'] == 118, 'Wrong index baseline')
    append_units = [json.dumps({'@type': 'ListItem', 'position': 119 + i, 'url': x['canonical'], 'name': x['title']}, ensure_ascii=False) for i, x in enumerate(pages)]
    new_script = old_script[:close] + ', ' + ', '.join(append_units) + old_script[close:]
    new_script, count = re.subn(r'("numberOfItems"\s*:\s*)118\b', r'\g<1>121', new_script)
    need(count == 1, 'Ambiguous item count')
    new_units, _ = json_array_units(new_script)
    new_object = json.loads(new_script)
    urls = [x['url'] for x in new_object['mainEntity']['itemListElement']]
    need(len(urls) == len(set(urls)) == 121, 'Duplicate/new ItemList URL mismatch')
    need(new_units[:118] == old_units and len(new_units) == 121, 'Old raw JSON elements changed')
    reverted = json.loads(new_script)
    reverted['mainEntity']['numberOfItems'] = old_object['mainEntity']['numberOfItems']
    reverted['mainEntity']['itemListElement'] = reverted['mainEntity']['itemListElement'][:118]
    need(typed(reverted) == typed(old_object), 'Old typed JSON/order changed')
    visible = ''
    for details, pdf in zip(pages, PDFS):
        date = datetime.strptime(details['date'], '%Y-%m-%d').strftime('%-d %B %Y')
        href = '/research/' + details['slug'] + '/'
        doi = '10.5281/zenodo.' + details['record']
        visible += '<li><a href="' + href + '">' + html.escape(details['title']) + '</a><br><span class="entry-meta">' + date + ' · Unrefereed preprint</span><p>' + html.escape(details['description']) + '</p><p><a href="' + href + pdf + '">PDF</a> · <a href="https://doi.org/' + doi + '">Zenodo</a></p></li>\n'
    need(old_index.count('    </ul>') == 1, 'Unexpected visible list boundary')
    index = old_index[:old_script_match.start(1)] + new_script + old_index[old_script_match.end(1):]
    index = index.replace('    </ul>', visible + '    </ul>', 1)
    old_li = re.findall(r'<li\b[^>]*>.*?</li>', old_index, re.S)
    new_li = re.findall(r'<li\b[^>]*>.*?</li>', index, re.S)
    need(len(old_li) == 118 and len(new_li) == 121 and new_li[:118] == old_li, 'Visible old units changed')
    need(index.replace(visible, '', 1).replace(new_script, old_script, 1) == old_index, 'Whole index not reversible')
    outputs['research/index.html'] = index.encode()
    old_site = (W / 'public/research/sitemap.xml').read_text()
    need(sha(old_site.encode()) == '45f5ef4f00587b36f2d574b31b47d245a8822462fe4499526a525500ab506985', 'Sitemap baseline drift')
    additions = ''.join('<url><loc>' + x['canonical'] + '</loc><lastmod>' + x['date'] + '</lastmod></url>\n' for x in pages)
    need(old_site.count('</urlset>') == 1, 'Unexpected sitemap boundary')
    site = old_site.replace('</urlset>', additions + '</urlset>', 1)
    old_xml = re.findall(r'<url>.*?</url>', old_site, re.S)
    new_xml = re.findall(r'<url>.*?</url>', site, re.S)
    need(len(old_xml) == 119 and len(new_xml) == 122 and new_xml[:119] == old_xml, 'Old sitemap units changed')
    need(site.replace(additions, '', 1) == old_site, 'Whole sitemap not reversible')
    ET.fromstring(site)
    locs = [x.text for x in ET.fromstring(site).iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    need(len(locs) == len(set(locs)) == 122, 'Duplicate/new sitemap URL mismatch')
    outputs['research/sitemap.xml'] = site.encode()
    expected = {'research/index.html', 'research/sitemap.xml'}
    for record in authority['records']:
        expected.update('research/' + record['proposed_slug'] + '/' + name for name in ['index.html', 'citation.bib'] + record['native_assets_order'])
    need(set(outputs) == expected and len(outputs) == 22 and len(native_pins) == 14, 'Wrong exact public file set')
    before_paths = {x['path'] for x in before['public']['files']}
    need(len(set(outputs) - before_paths) == 20 and len(before_paths | set(outputs)) == 747, 'Wrong projected file count')
    need(not any(x.endswith('research.css') for x in outputs), 'CSS addition forbidden')
    checks = {'UTC': datetime.now(timezone.utc).isoformat(), 'pages': pages, 'exact_candidate_paths': sorted(outputs), 'native_assets': native_pins, 'original_HOLD_preserved': True, 'old_visible_units_exact': 118, 'old_raw_typed_JSON_units_exact': 118, 'old_sitemap_units_exact': 119, 'whole_aggregates_reversible': True, 'candidate_index_units': 121, 'candidate_sitemap_units': 122, 'projected_public_files': 747, 'projected_public_child_directories': 366, 'new_CSS_files': [], 'native_scientific_or_old_helper_executions': [], 'actual_install_publication_authority': False}
    if not build:
        print(json.dumps({'mode': 'READ_ONLY_NO_WRITES', 'checks': checks}, indent=2, ensure_ascii=False))
        return
    need(not (R / 'public').exists() and not (R / 'before').exists(), 'Build outputs already exist; no replay')
    planned = {'public/' + name: value for name, value in outputs.items()}
    planned.update({'before/research-index.html': old_index.encode(), 'before/research-sitemap.xml': old_site.encode()})
    def write_own(relative, body):
        dest = R / relative
        need(dest.resolve().is_relative_to(R.resolve()) and not dest.exists(), 'Output escape/overwrite')
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open('xb') as handle:
            handle.write(body)
        need(pin(dest)['mode'] == '0644', 'Unexpected created file mode; no chmod performed')
    for name, body in planned.items():
        write_own(name, body)
    after = guards(authority)
    need(after == before, 'Protected public/source/editorial/native Git drift; HALT without repair')
    for item in inputs + native_pins:
        need(pin(Path(item['path'])) == item, 'Bound copy/source input drift')
    checks['candidate_inventory'] = inventory(R / 'public')
    need(len(checks['candidate_inventory']['files']) == 22 and len(checks['candidate_inventory']['directories']) == 5, 'Candidate topology mismatch')
    for filename, value in [('GUARDS_BEFORE.json', before), ('GUARDS_AFTER.json', after), ('INPUT_PINS.json', inputs), ('STATIC_CHECKS.json', checks)]:
        write_own(filename, (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode())
    print(json.dumps({'status': 'PRIVATE_STAGE_BUILT', 'checks': checks, 'builder': pin(Path(__file__)), 'no_W_or_Git_mutation': True}, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
