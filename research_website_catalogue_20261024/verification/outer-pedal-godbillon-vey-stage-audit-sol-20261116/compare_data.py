"""Read-only, exact three-page stage comparison. No subprocess or write API."""
from pathlib import Path
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib
import json
import re
import stat
import sys
import xml.etree.ElementTree as ET

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
O = P / 'verification/outer-pedal-godbillon-vey-stage-audit-sol-20261116'
STAGE = P / 'verification/outer-pedal-godbillon-vey-stage-sol-20261116'
AUTH = P / 'verification/root-outer-pedal-godbillon-vey-gramian-editorial-adoption-20261116.json'
AUTH_SHA = '7b5367a6c98c13e304f93d8a582cc22c7fe0688e5cc0378bbbf1dce04b182cab'
BASE = 'https://aleckriebel.com/research/'
records = [('23398175', 'outer-focal-pedal-area-product'),
           ('23357329', 'unbounded-godbillon-vey-fixed-hyperbolic-manifold'),
           ('23153134', 'negative-curvature-observation-gramian')]

def need(condition, message):
    if not condition:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def utf8(path):
    return path.read_bytes().decode('utf-8')

def pin(path):
    need(path.is_file() and not path.is_symlink(), 'Nonordinary file: ' + str(path))
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data), 'SHA256': sha(data),
            'mode': stat.S_IMODE(path.stat().st_mode)}

def checksum_list(path, root):
    count = 0
    for line in path.read_text().splitlines():
        expected, rel = line.split('  ', 1)
        need(pin(root/rel)['SHA256'] == expected, 'Checksum mismatch: ' + rel)
        count += 1
    return count

def check_pin(item):
    actual = pin(P/item['path'])
    need(actual['bytes'] == item['bytes'] and actual['SHA256'] == item['SHA256'],
         'Authority pin mismatch: ' + item['path'])

def packet(root, manifest_name, final_name, expected_count, expected_dirs):
    m = json.loads((root/manifest_name).read_text())
    entries = m['payloads'] if 'payloads' in m else m['files']
    paths = [e['path'] for e in entries]
    actual = sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file())
    need(actual == sorted(paths+[manifest_name, final_name]), 'Packet extent: ' + str(root))
    for e in entries:
        p = pin(root/e['path'])
        need(p['bytes'] == e['bytes'] and p['SHA256'] == e.get('SHA256', e.get('sha256')),
             'Packet byte mismatch: ' + str(root/e['path']))
        if 'mode' in e:
            mode = e['mode'] if isinstance(e['mode'], int) else int(e['mode'], 8)
            need(p['mode'] == mode, 'Packet mode mismatch: ' + str(root/e['path']))
    dirs = sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_dir())
    declared = m.get('directories', m.get('finite_extent', {}).get('directories', []))
    for entry in declared:
        if isinstance(entry, dict) and 'mode' in entry:
            mode = entry['mode'] if isinstance(entry['mode'], int) else int(entry['mode'], 8)
            need(stat.S_IMODE((root/entry['path']).stat().st_mode) == mode, 'Packet directory mode: '+str(root/entry['path']))
    declared = [d['path'] if isinstance(d, dict) else d for d in declared]
    need(dirs == sorted(d for d in declared if d != '.'), 'Packet directories: ' + str(root))
    need(len(actual) == expected_count and len(dirs) == expected_dirs, 'Packet count: ' + str(root))
    need(all(not p.is_symlink() for p in root.rglob('*')), 'Packet symlink: ' + str(root))
    return {'root': str(root), 'files': len(actual), 'child_directories': len(dirs),
            'all_payload_bytes_and_available_mode_pins_match': True}

def guard_table(table):
    root = Path(table['root'])
    need(sorted(str(x.relative_to(root)) for x in root.rglob('*') if x.is_file()) == sorted(x['path'] for x in table['files']), 'Guard-table file extent: '+str(root))
    for entry in table['files']:
        current = pin(root/entry['path'])
        need(current['bytes'] == entry['bytes'] and current['SHA256'] == entry['sha256'] and current['mode'] == int(entry['mode'], 8), 'Guard-table current file: '+str(root/entry['path']))
    directories = ['.']+[str(x.relative_to(root)) for x in root.rglob('*') if x.is_dir()]
    need(sorted(directories) == sorted(x['path'] for x in table['directories']), 'Guard-table directory extent: '+str(root))
    for entry in table['directories']:
        need(stat.S_IMODE((root/entry['path']).stat().st_mode) == int(entry['mode'], 8), 'Guard-table directory mode: '+str(root/entry['path']))

def index_public_paths():
    data = (W/'.git/index').read_bytes()
    need(data[:8] == b'DIRC\0\0\0\2' and int.from_bytes(data[8:12], 'big') == 58667, 'Native v2/count')
    need(hashlib.sha1(data[:-20]).digest() == data[-20:], 'Native index trailing checksum')
    offset, paths = 12, set()
    for _ in range(58667):
        end = data.index(b'\0', offset+62)
        name = data[offset+62:end].decode('utf-8')
        if name.startswith('public/'):
            need(name not in paths, 'Duplicate native public path')
            paths.add(name)
        offset += ((end+1-offset+7)//8)*8
    need(offset <= len(data)-20 and len(paths) == 710, 'Native public subset count')
    return paths

def single(pattern, text):
    found = list(re.finditer(pattern, text, re.S))
    need(len(found) == 1, 'Expected one match: ' + pattern)
    return found[0]

def main_inner(text):
    return single(r'<main\b[^>]*>(.*?)</main>', text).group(1)

def scripts(text):
    return [m.group(1) for m in re.finditer(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', text, re.S)]

class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.meta, self.links, self.ids, self.hrefs = {}, [], [], []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'meta':
            key = a.get('name', a.get('property'))
            need(key not in self.meta, 'Duplicate metadata key: ' + str(key))
            self.meta[key] = a.get('content', '')
        if tag == 'link':
            self.links.append(a)
        if tag == 'a' and 'href' in a:
            self.hrefs.append(a['href'])

def plain(text):
    return ' '.join(unescape(re.sub(r'<[^>]+>', '', text)).split())

def raw_items(script):
    start = single(r'"itemListElement"\s*:\s*\[', script).end()
    out, pos, dec = [], start, json.JSONDecoder()
    while True:
        pos += len(script[pos:])-len(script[pos:].lstrip())
        if script[pos] == ']':
            break
        value, end = dec.raw_decode(script, pos)
        out.append((script[pos:end], value, pos, end))
        pos = end
        pos += len(script[pos:])-len(script[pos:].lstrip())
        if script[pos] == ',':
            pos += 1
        else:
            need(script[pos] == ']', 'Invalid item-list delimiter')
    return out

def typed(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))

def li_units(text):
    scope = single(r'<h2>Papers</h2>\s*<ul>(.*?)</ul>', text)
    return scope, list(re.finditer(r'<li\b[^>]*>.*?</li>', scope.group(1), re.S))

def main():
    need(len(sys.argv) == 4, 'Usage: compare_data.py PAYLOAD_ROOT FINAL_PATH EXPECTED_FINAL_SHA256')
    candidate, producer_final, expected_final_sha = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    need(candidate.resolve().is_relative_to(STAGE.resolve()), 'Candidate outside exact stage namespace')
    need(producer_final.resolve().is_relative_to(STAGE.resolve()), 'FINAL outside exact stage namespace')
    need(pin(producer_final)['SHA256'] == expected_final_sha, 'Producer FINAL pin differs')
    need(pin(STAGE/'OWNED_MANIFEST.json')['SHA256'] == 'b2e50e34c59ef8854eb2846bd308cad9d9353214e9259409a3a3bbe3d7c5d17a', 'Producer whole manifest pin differs')
    producer_packet = packet(STAGE, 'OWNED_MANIFEST.json', 'FINAL.json', 53, 6)
    need(pin(AUTH)['SHA256'] == AUTH_SHA, 'Three-source authority differs')
    need(pin(O/'INITIAL_SEAL.sha256')['SHA256'] == 'b767ce09e310c3838bdf1989b56f768bc4637340767782e224ba4c9e3f58de34', 'Original seal changed')
    need(pin(O/'THREE_SOURCE_INITIAL_SEAL.sha256')['SHA256'] == 'a2156fa63ea14b1f67137483c9f88ccc5f9bd247ed4293fdbd877ae4c08bf05a', 'Continuation seal changed')
    checksums = {name: checksum_list(O/name, O) for name in ['INITIAL_SEAL.sha256', 'THREE_SOURCE_INITIAL_SEAL.sha256']}
    checksum_list(O/'SOURCE_SHA256SUMS.txt', P)
    checksum_list(O/'THREE_SOURCE_SHA256SUMS.txt', P)
    checksum_list(O/'baselines/protected-sha256.txt', Path('/'))
    authority = json.loads(AUTH.read_text())
    editorials, sources = [], []
    expected_paths = {'public/research/index.html', 'public/research/sitemap.xml'}
    article_evidence = []
    for i, (record, slug) in enumerate(records):
        adopted = authority['records'][i]
        need(adopted['record'] == record and adopted['proposed_slug'] == slug, 'Authority order differs')
        for item in list(adopted['writer_pins'].values())+[adopted['fact_FINAL'], adopted['fact_manifest']]:
            check_pin(item)
        wr = P/f'papers/{record}/reviews/editorial'
        fr = (P/adopted['fact_FINAL']['path']).parent
        editorials.append(packet(wr, 'OWNED_MANIFEST.json', 'FINAL.json', adopted['writer_extent']['files'], 2))
        editorials.append(packet(fr, 'OWNED_MANIFEST.json', 'FINAL.json', adopted['fact_packet_files'], 0))
        sources.append(packet(P/f'papers/{record}/sources', 'SOURCE_MANIFEST.json', 'SOURCE_FINAL.json', adopted['source_extent']['files'], adopted['source_extent']['child_directories']))
        prefix = 'public/research/'+slug+'/'
        native = adopted['native_assets_order']
        expected_paths.update(prefix+n for n in ['index.html', 'citation.bib']+native)
        for name in ['citation.bib']+native:
            got = (candidate/(prefix+name)).read_bytes()
            need(got == (wr/'preview'/name).read_bytes(), 'Changed approved asset: '+prefix+name)
            if name in native:
                need(got == (P/f'papers/{record}/sources/assets'/name).read_bytes(), 'Changed native source asset: '+name)
        old = utf8(wr/'preview/index.html')
        new = utf8(candidate/(prefix+'index.html'))
        need(main_inner(new) == main_inner(old) == main_inner(utf8(wr/'MAIN.html')), 'MAIN inner bytes changed: '+record)
        need(new.split('</head>', 1)[1] == old.split('</head>', 1)[1], 'Changed adopted body/wrapper bytes: '+record)
        model = json.loads((wr/'PAGE_MODEL.json').read_text())
        oldtags, tags = Tags(old), Tags(new)
        need(len(tags.ids) == len(set(tags.ids)), 'Duplicate HTML id: '+record)
        url = BASE+slug+'/'
        need([x['href'] for x in tags.links if x.get('rel') == 'canonical'] == [url], 'Canonical mismatch: '+record)
        need([x['href'] for x in tags.links if x.get('rel') == 'stylesheet'] == ['../research.css'], 'CSS path mismatch: '+record)
        need('editorial-status' not in tags.meta and not any(x in tags.meta.get('robots', '').lower() for x in ['noindex', 'nofollow', 'noarchive']), 'Private head flags: '+record)
        pdf = next(n for n in native if n.endswith('.pdf'))
        need(tags.meta.get('citation_pdf_url') == url+pdf, 'Citation PDF URL: '+record)
        need(tags.meta.get('og:url') == url, 'OpenGraph URL: '+record)
        title = single(r'<title>(.*?)</title>', new).group(1)
        need(title == ('Negative-curvature observation Gramian | Alec Kriebel' if record == '23153134' else single(r'<title>(.*?)</title>', old).group(1)), 'Unauthorized SEO title: '+record)
        for key, value in oldtags.meta.items():
            if key not in ['robots', 'editorial-status', 'citation_pdf_url']:
                need(tags.meta.get(key) == value, 'Changed original metadata '+str(key)+': '+record)
        obj = json.loads(scripts(new)[0])
        original_obj = json.loads(scripts(old)[0])
        need(len(scripts(new)) == len(scripts(old)) == 1, 'Article schema block count: '+record)
        for key, value in original_obj.items():
            if key not in ['encoding', 'url', '@id', 'mainEntityOfPage']:
                need(typed(obj.get(key)) == typed(value), 'Changed original schema '+key+': '+record)
        need(obj.get('url') == url, 'Schema public URL: '+record)
        if '@id' in obj:
            need(obj['@id'] in [url, url+'#article'], 'Schema id: '+record)
        if 'mainEntityOfPage' in obj:
            value = obj['mainEntityOfPage']
            need((value.get('@id') if isinstance(value, dict) else value) == url, 'Schema main page: '+record)
        if 'encoding' in obj:
            need([x['contentUrl'] for x in obj['encoding']] == [url+n for n in native], 'Schema native URLs/order: '+record)
            for previous in original_obj.get('encoding', []):
                current = next(x for x in obj['encoding'] if x['contentUrl'] == url+previous['contentUrl'])
                need(all(current.get(k) == v for k, v in previous.items() if k != 'contentUrl'), 'Changed original encoding metadata: '+record)
        need(obj['abstract'] == model['abstract'] == tags.meta['DC.description'], 'Full metadata abstract: '+record)
        fragment = (single(r'<section id="original-abstract">.*?<p>(.*?)</p>', new).group(1) if record == '23398175' else single(r'<p id="original-abstract">(.*?)</p>', new).group(1))
        need(plain(fragment) == ' '.join(model['abstract'].split()), 'Full visible abstract: '+record)
        ol = single(r'<ol id="native-(?:assets|downloads)">(.*?)</ol>', new).group(1)
        download_order = re.findall(r'<a href="([^"]+)" download', ol)
        need(download_order == native, 'Native presentation order: '+record)
        for href in tags.hrefs:
            if href.startswith('#'):
                need(href[1:] in tags.ids, 'Missing fragment: '+href)
        need('/research/' in tags.hrefs and '/' in tags.hrefs, 'Home/research navigation: '+record)
        article_evidence.append({'record': record, 'canonical_candidate': url, 'MAIN_inner_SHA256': sha(main_inner(new).encode()), 'native_order': native, 'title': unescape(title), 'whole_HTML': pin(candidate/(prefix+'index.html'))})
    need(sum(x['files'] for x in editorials) == 172 and sum(x['files'] for x in sources) == 531 and sum(x['child_directories'] for x in sources) == 49, 'Full editorial/source totals')
    before_guard, after_guard = (STAGE/'GUARDS_BEFORE.json').read_bytes(), (STAGE/'GUARDS_AFTER.json').read_bytes()
    need(before_guard == after_guard, 'Producer complete before/after guard bytes differ')
    guards = json.loads(before_guard)
    tables = [guards['public']]+guards['sources']+guards['editorial_and_fact']
    need({t['root'] for t in tables} == {str(W/'public')}|{x['root'] for x in sources+editorials}, 'Guard-table root scope')
    for table in tables:
        guard_table(table)
    for group in ['W_native_Git', 'Math_native_Git']:
        for entry in guards[group]['files']:
            current = pin(Path(entry['path']))
            need(current['bytes'] == entry['bytes'] and current['SHA256'] == entry['sha256'] and current['mode'] == int(entry['mode'], 8), 'Producer native-state guard differs')
    failed = json.loads((STAGE/'FAILED_BUILD_RECEIPT.json').read_bytes())
    completed = json.loads((STAGE/'COMPLETE_EXECUTION_RECEIPT.json').read_bytes())
    need(failed['exit_status'] == 1 and completed['exit_status'] == 0 and completed['total_explicit_build_attempts'] == 2, 'Literal attempt history')
    need((STAGE/'BUILD.stdout.json').read_bytes() == b'' and (STAGE/'COMPLETE.stderr.txt').read_bytes() == b'', 'Literal empty streams changed')
    need(json.loads((STAGE/'COMPLETE.stdout.json').read_bytes())['status'] == 'PRIVATE_STAGE_BUILT', 'Completion stdout status')
    public_payload = candidate/'public'
    need(public_payload.is_dir() and not public_payload.is_symlink(), 'Missing ordinary public payload root')
    actual_paths = sorted(str(p.relative_to(candidate)) for p in public_payload.rglob('*') if p.is_file())
    need(set(actual_paths) == expected_paths and len(actual_paths) == 22, 'Exact22 candidate payload path set differs')
    need(all(not p.is_symlink() for p in public_payload.rglob('*')), 'Candidate symlink')
    need(all(pin(candidate/p)['mode'] == 0o644 for p in actual_paths), 'Candidate file mode')
    expected_dirs = {str(parent) for rel in expected_paths for parent in Path(rel).parents if str(parent) != '.'}
    need({'public'}|{str(p.relative_to(candidate)) for p in public_payload.rglob('*') if p.is_dir()} == expected_dirs, 'Candidate directory extent')
    base_files = {}
    for line in (O/'baselines/public-sha256.txt').read_text().splitlines():
        expected, rel = line.split('  ', 1)
        need(pin(W/rel)['SHA256'] == expected, 'Baseline public file changed: '+rel)
        base_files[rel] = expected
    current_files = sorted(str(p.relative_to(W)) for p in (W/'public').rglob('*') if p.is_file())
    need(current_files == sorted(base_files) and len(base_files) == 727, 'Baseline public extent')
    diagnostic_path = P/'verification/root-three-stage-index-path-diagnostic-20261116.json'
    need(pin(diagnostic_path)['SHA256'] == '68e379303f4dfa783246abe49af14ac84d97412d21d5e2c865315e26409fbced', 'Root exact tracking diagnostic changed')
    diagnostic = json.loads(diagnostic_path.read_bytes())
    native_paths = index_public_paths()
    need(set(base_files)-native_paths == set(diagnostic['filesystem_only_paths']) and native_paths <= set(base_files), 'Specific17 untracked extras differ')
    for entry in diagnostic['filesystem_only_pins']:
        current = pin(W/entry['path'])
        need(current['bytes'] == entry['bytes'] and current['SHA256'] == entry['SHA256'] and current['mode'] == int(entry['mode'], 8), 'Specific untracked file pin differs')
    need(all(not p.is_symlink() and (p.is_file() or p.is_dir()) for p in (W/'public').rglob('*')), 'Unexpected public node')
    for line in (O/'baselines/public-modes-sizes.txt').read_text().splitlines():
        mode, size, rel = line.split(' ', 2)
        p = pin(W/rel)
        need(p['mode'] == int(mode, 8) and p['bytes'] == int(size), 'Baseline mode/size: '+rel)
    old_dirs = (O/'baselines/public-directories.txt').read_text().splitlines()
    dirs = ['public']+sorted(str(p.relative_to(W)) for p in (W/'public').rglob('*') if p.is_dir())
    need(sorted(dirs) == sorted(old_dirs) and len(dirs) == 364, 'Baseline directory extent')
    need(len(set(old_dirs)|expected_dirs) == 367, 'Virtual overlay directory count')
    need(len(set(base_files)|expected_paths) == 747, 'Virtual overlay file count')
    need(set(expected_paths)&set(base_files) == {'public/research/index.html', 'public/research/sitemap.xml'}, 'Unexpected pre-existing new target')
    need(pin(W/'public/research/research.css')['SHA256'] == 'f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a', 'Shared CSS changed')
    windex = pin(W/'.git/index')
    need(windex['mode'] == 0o644 and windex['bytes'] == 9051646, 'W native index mode/size')
    need((W/'.git/index').read_bytes()[:12] == b'DIRC'+(2).to_bytes(4, 'big')+(58667).to_bytes(4, 'big'), 'W native index header/count')
    mindex = pin(Path('/Users/alec/Documents/Math/.git/index'))
    need(mindex['mode'] == 0o644 and mindex['bytes'] == 25854746, 'Math native index mode/size')
    old_index = utf8(O/'baselines/research-index.html')
    new_index = utf8(candidate/'public/research/index.html')
    old_script, new_script = scripts(old_index)[0], scripts(new_index)[0]
    need(len(scripts(old_index)) == len(scripts(new_index)) == 1, 'Collection schema block count')
    oi, ni = raw_items(old_script), raw_items(new_script)
    need(len(oi) == 118 and len(ni) == 121, 'Raw JSON item count')
    need([x[0] for x in ni[:118]] == [x[0] for x in oi], 'Old raw JSON units changed')
    need([typed(x[1]) for x in ni[:118]] == [typed(x[1]) for x in oi], 'Old typed JSON units changed')
    need([x[1]['position'] for x in oi] == list(range(1, 119)), 'Old position order')
    for pos, ((_, slug), item) in enumerate(zip(records, ni[118:]), 119):
        need(item[1]['position'] == pos and type(item[1]['position']) is int and item[1]['url'] == BASE+slug+'/' and item[1]['@type'] == 'ListItem', 'New JSON unit identity/order')
    new_obj = json.loads(new_script)
    need(type(new_obj['mainEntity']['numberOfItems']) is int and new_obj['mainEntity']['numberOfItems'] == 121, 'Declared index count')
    recovered_script = new_script[:ni[117][3]]+new_script[ni[-1][3]:]
    cm = single(r'"numberOfItems"\s*:\s*(121)', recovered_script)
    recovered_script = recovered_script[:cm.start(1)]+'118'+recovered_script[cm.end(1):]
    need(recovered_script == old_script, 'Whole raw JSON reversal fails')
    oscope, oli = li_units(old_index)
    nscope, nli = li_units(new_index)
    need(len(oli) == 118 and len(nli) == 121 and [x.group() for x in nli[:118]] == [x.group() for x in oli], 'Old visible li units changed')
    for (_, slug), item in zip(records, nli[118:]):
        need(re.findall(r'<a href="([^"]+)"', item.group())[0] == '/research/'+slug+'/', 'New visible unit order')
    recovered_list = nscope.group(1)[:nli[117].end()]+nscope.group(1)[nli[-1].end():]
    recovered = new_index[:nscope.start(1)]+recovered_list+new_index[nscope.end(1):]
    recovered = recovered.replace(new_script, old_script, 1)
    need(recovered == old_index, 'Whole index reversal fails')
    old_xml = utf8(O/'baselines/research-sitemap.xml')
    new_xml = utf8(candidate/'public/research/sitemap.xml')
    ou = list(re.finditer(r'<url\b[^>]*>.*?</url>', old_xml, re.S))
    nu = list(re.finditer(r'<url\b[^>]*>.*?</url>', new_xml, re.S))
    need(len(ou) == 119 and len(nu) == 122 and [x.group() for x in nu[:119]] == [x.group() for x in ou], 'Old XML units changed')
    ns = {'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    old_tree, new_tree = ET.fromstring(old_xml), ET.fromstring(new_xml)
    need([ET.tostring(x) for x in list(new_tree)[:119]] == [ET.tostring(x) for x in old_tree], 'Parsed old XML units changed')
    need([x.find('s:loc', ns).text for x in list(new_tree)[119:]] == [BASE+s+'/' for _, s in records], 'New sitemap identity/order')
    recovered_xml = new_xml[:nu[118].end()]+new_xml[nu[-1].end():]
    need(recovered_xml == old_xml, 'Whole sitemap reversal fails')
    print(json.dumps({'UTC': datetime.now(timezone.utc).isoformat(), 'status':'PASS',
        'source_first_seals_checked': checksums, 'producer_FINAL':pin(producer_final),
        'candidate_files': [pin(candidate/p) for p in actual_paths],
        'articles':article_evidence, 'editorial_packets':editorials, 'source_packets':sources,
        'producer_whole_packet':producer_packet, 'all_ten_guard_tables_checked_against_current_files_and_modes':True,
        'native_index_decoded_records':58667, 'native_public_paths':len(native_paths), 'specific_untracked_extras':len(set(base_files)-native_paths),
        'editorial_files':sum(x['files'] for x in editorials), 'source_files':sum(x['files'] for x in sources),
        'old_visible_raw_and_typed_JSON_units_preserved':118, 'old_raw_and_parsed_XML_units_preserved':119,
        'whole_index_and_sitemap_exactly_reversible':True,
        'virtual_counts':{'public_files':747,'public_child_directories':366,'index':121,'sitemap':122},
        'baseline_all_public_and_protected_states_unchanged':True,
        'no_builder_native_render_network_Git_or_write_API':True,
        'live_reader_download_certification':False}, indent=2))

if __name__ == '__main__':
    main()
