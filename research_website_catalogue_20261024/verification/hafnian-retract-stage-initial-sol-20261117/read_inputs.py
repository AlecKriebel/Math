"""One passive INITIAL reader: explicit accepted data only; stdout JSON only.
No subprocess, network, project imports, source execution, or filesystem writes.
"""
from pathlib import Path
from datetime import datetime, timezone
from html.parser import HTMLParser
import hashlib
import html
import json
import os
import re
import stat
import struct
import xml.etree.ElementTree as ET
import zlib

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
M = Path('/Users/alec/Documents/Math')
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
V = P / 'verification'
ADOPTIONS = {
    'root-hafnian-editorial-adoption-20261117.json': '775b1ef8b9592e55d21fcd45e4bf381f3965a27282f41277ac7ab8e9880c07dc',
    'root-complex-retract-editorial-adoption-20261117.json': 'ea048b2f612c2c6a7593fcd51184ad72918200dc88d2565d307dec44a8284df5',
}
LANES = [
    ('hafnian-editorial-sol-20261117', 'MANIFEST.json', 'FINAL.json', 23, 1),
    ('hafnian-fact-sol-20261117', 'MANIFEST.json', 'FINAL.json', 10, 0),
    ('hafnian-legacy-sol-20261117', 'FINAL_MANIFEST.json', 'FINAL_SEAL.json', 16, 11),
    ('complex-retract-editorial-sol-20261117', 'MANIFEST.json', 'FINAL.json', 22, 1),
    ('complex-retract-fact-sol-20261117', 'MANIFEST.json', 'FINAL.json', 10, 0),
    ('complex-retract-legacy-sol-20261117', 'OWNED_MANIFEST.json', 'FINAL.json', 123, 0),
]
SOURCES = [(P/'papers/23205294/sources', 56, 10), (P/'papers/23203270/sources', 97, 12)]
SLUGS = ['nonnegative-rational-hafnians', 'complex-polynomial-retract-five-variables']

def now():
    return datetime.now(timezone.utc).isoformat()

def sha(b):
    return hashlib.sha256(b).hexdigest()

def mode(v):
    if isinstance(v, str):
        assert re.fullmatch(r'(?:0o)?[0-7]{3,4}', v), v
        v = int(v.removeprefix('0o'), 8)
    assert type(v) is int and 0 <= v <= 0o7777, v
    return format(v, '04o')

def pairhook(pairs):
    result = {}
    for k, v in pairs:
        assert k not in result, ('duplicate JSON key', k)
        result[k] = v
    return result

def load(s):
    return json.loads(s, object_pairs_hook=pairhook,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))

def filepin(p):
    st = p.lstat()
    assert stat.S_ISREG(st.st_mode), str(p)
    b = p.read_bytes()
    return {'bytes': len(b), 'SHA256': sha(b), 'mode': mode(stat.S_IMODE(st.st_mode))}

def relpath(s, root_allowed=False):
    assert isinstance(s, str) and '\\' not in s and '\x00' not in s
    assert (root_allowed and s == '.') or (s and not s.startswith('/') and
           all(x not in ('', '.', '..') for x in s.split('/'))), s
    return s

def census(root):
    st = root.lstat()
    assert stat.S_ISDIR(st.st_mode), str(root)
    files, dirs = {}, {}
    for base, ds, fs in os.walk(root, topdown=True, followlinks=False):
        base = Path(base)
        r = base.relative_to(root).as_posix()
        ds.sort(); fs.sort()
        assert all(not (base/x).is_symlink() for x in ds + fs)
        dirs[r] = {'mode': mode(stat.S_IMODE(base.lstat().st_mode)), 'empty': not ds and not fs}
        for n in ds:
            assert stat.S_ISDIR((base/n).lstat().st_mode)
        for n in fs:
            q = base/n
            files[relpath(q.relative_to(root).as_posix())] = filepin(q)
    assert not (set(files) & set(dirs))
    return {'root': str(root), 'files': files, 'directories': dirs,
            'regular_files': len(files), 'child_directories': len(dirs)-1}

def native(root):
    g = root/'.git'
    assert g.is_dir() and not g.is_symlink()
    ans = {n: filepin(g/n) for n in ('HEAD', 'index', 'config')}
    ans['HEAD_text'] = (g/'HEAD').read_text()
    ans['local_loose_heads'] = census(g/'refs/heads')
    packed = g/'packed-refs'
    local = []
    if packed.exists():
        lines = packed.read_text().splitlines(keepends=True)
        for i, line in enumerate(lines):
            if re.fullmatch(r'[0-9a-f]{40} refs/heads/[^\n]+\n?', line):
                local.append(line)
                if i+1 < len(lines) and lines[i+1].startswith('^'):
                    local.append(lines[i+1])
        ans['packed_local_heads'] = {'file_mode': mode(stat.S_IMODE(packed.stat().st_mode)), 'raw_lines': local}
    else:
        ans['packed_local_heads'] = {'absent': True}
    ref = ans['HEAD_text'].strip().removeprefix('ref: ')
    assert ref.startswith('refs/heads/')
    if (g/ref).exists():
        oid = (g/ref).read_text().strip()
    else:
        matches = [x.split()[0] for x in local if x.rstrip().endswith(' '+ref)]
        assert len(matches) == 1
        oid = matches[0]
    assert re.fullmatch('[0-9a-f]{40}', oid)
    ans['resolved_native_HEAD'] = oid
    return ans

def guards():
    roots = {str(V/n): census(V/n) for n, _, _, _, _ in LANES}
    roots.update({str(s): census(s) for s, _, _ in SOURCES})
    controls = {str(V/n): filepin(V/n) for n in ADOPTIONS}
    for record in ('23205294', '23203270'):
        c = V/('root-clearance-'+record+'-20261117.json')
        d = load(c.read_text())
        controls[str(c)] = filepin(c)
        review = P/d['root_review']['path']
        controls[str(review)] = filepin(review)
        assert controls[str(review)]['SHA256'] == d['root_review']['SHA256']
    return {'roots': roots, 'controls': controls, 'public': census(W/'public'),
            'native_M': native(M), 'native_W': native(W)}

def check_manifest(root, snap, name, terminal):
    d = load((root/name).read_text())
    rows = d.get('payload_files', d.get('files', d.get('entries')))
    assert isinstance(rows, list), str(root)
    entries = 'entries' in d
    seen, seen_dirs, terminal_rows = set(), set(), []
    for row in rows:
        assert isinstance(row, dict) and 'path' in row
        r = relpath(row['path'], root_allowed=entries)
        assert r not in seen and r not in seen_dirs, r
        m = mode(row.get('mode', row.get('mode_octal')))
        if entries and row['kind'] == 'directory':
            assert snap['directories'][r]['mode'] == m
            assert snap['directories'][r]['empty'] == row['empty']
            seen_dirs.add(r)
            continue
        assert not entries or row['kind'] == 'file'
        seen.add(r)
        actual = snap['files'][r]
        assert actual['mode'] == m
        if row.get('terminal_control') is True:
            assert r in (name, terminal) and set(row) == {'path', 'mode', 'terminal_control'}
            terminal_rows.append(r)
            continue
        assert type(row['bytes']) is int and row['bytes'] >= 0
        assert actual['bytes'] == row['bytes']
        assert actual['SHA256'] == row.get('SHA256', row.get('sha256'))
        md5 = row.get('MD5', row.get('md5'))
        if md5 is not None:
            assert hashlib.md5((root/r).read_bytes()).hexdigest() == md5
    if terminal_rows:
        assert set(terminal_rows) == {name, terminal}
        assert seen == set(snap['files'])
    else:
        assert seen == set(snap['files']) - {name, terminal}
    if not entries:
        assert snap['directories']['.']['mode'] == mode(d['root_mode'])
        seen_dirs = {'.'}
        for row in d['directories']:
            r = relpath(row['path'])
            assert r not in seen_dirs and r not in seen
            assert snap['directories'][r]['mode'] == mode(row['mode'])
            if 'empty' in row:
                assert snap['directories'][r]['empty'] == row['empty']
            seen_dirs.add(r)
    assert seen_dirs == set(snap['directories'])
    return {'schema': d['schema'], 'manifest': filepin(root/name),
            'terminal': filepin(root/terminal), 'complete_actual_namespace': True,
            'payload_rows': len(rows), 'terminal_control_rows': terminal_rows}

class AttrReader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []
    def handle_starttag(self, tag, attrs):
        names = [x[0] for x in attrs]
        assert len(names) == len(set(names)), ('duplicate HTML attribute', tag, attrs)
        self.tags.append((tag, attrs))
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

def raw_json_units(s):
    m = re.search(r'"itemListElement"\s*:\s*\[', s)
    assert m
    decoder = json.JSONDecoder(object_pairs_hook=pairhook)
    pos, out = m.end(), []
    while True:
        while s[pos].isspace():
            pos += 1
        if s[pos] == ']':
            return out
        start = pos
        _, pos = decoder.raw_decode(s, pos)
        out.append(s[start:pos])
        while s[pos].isspace():
            pos += 1
        if s[pos] == ',':
            pos += 1
        else:
            assert s[pos] == ']'

started = now()
before = guards()
adoptions = {n: load((V/n).read_text()) for n in ADOPTIONS}
for n, expected in ADOPTIONS.items():
    assert before['controls'][str(V/n)]['SHA256'] == expected
assert adoptions['root-hafnian-editorial-adoption-20261117.json']['status'] == 'ADOPTED_PRIVATE_EDITORIAL_FOR_LATER_STAGING'
assert adoptions['root-complex-retract-editorial-adoption-20261117.json']['status'] == 'PRIVATE_EDITORIAL_FIDELITY_ACCEPTED_FOR_LATER_SEPARATE_STAGING'
bindings = {}
for n, manifest, terminal, nf, nd in LANES:
    snap = before['roots'][str(V/n)]
    assert (snap['regular_files'], snap['child_directories']) == (nf, nd)
    bindings[str(V/n)] = check_manifest(V/n, snap, manifest, terminal)
ha = adoptions['root-hafnian-editorial-adoption-20261117.json']
for row in ha['fresh_finite_authentication']:
    root = Path(row['root'])
    b = bindings[str(root)]
    assert b['manifest']['SHA256'] == row['manifest_SHA256']
    assert filepin(root/'FINAL.json')['SHA256'] == row['FINAL_SHA256']
ca = adoptions['root-complex-retract-editorial-adoption-20261117.json']
for row in ca['finite_packet_authentication']:
    root = P/row['root']
    snap = before['roots'][str(root)]
    expected = row['complete_before_after']
    assert set(expected['files']) == set(snap['files'])
    assert set(expected['directories']) == set(snap['directories'])
    for r, x in expected['files'].items():
        assert snap['files'][r] == {'bytes': x['bytes'], 'SHA256': x['SHA256'], 'mode': mode(x['mode'])}
    for r, x in expected['directories'].items():
        assert snap['directories'][r] == {'mode': mode(x['mode']), 'empty': x['empty']}
for root, nf, nd in SOURCES:
    snap = before['roots'][str(root)]
    assert (snap['regular_files'], snap['child_directories']) == (nf, nd)
    bindings[str(root)] = check_manifest(root, snap, 'SOURCE_MANIFEST.json', 'SOURCE_FINAL.json')
hs = load((V/'hafnian-editorial-sol-20261117/SOURCE_GUARDS_FINAL.json').read_text())
assert before['roots'][str(SOURCES[0][0])]['files'] == {
    r: {'bytes': x['bytes'], 'SHA256': x['SHA256'], 'mode': mode(x['mode'])}
    for r, x in hs['source']['files'].items()}
pages = []
for family, slug in zip(('hafnian', 'complex-retract'), SLUGS):
    root = V/(family+'-editorial-sol-20261117')
    article = (root/'article.html').read_bytes().decode('utf-8')
    head = re.search(r'<head>.*?</head>', article, re.S).group()+'\n'
    main = re.search(r'<main\b[^>]*>.*?</main>', article, re.S).group()+'\n'
    body = re.search(r'<body>.*</body>', article, re.S).group()
    assert head == (root/'head.html').read_text()
    assert main == (root/'main.html').read_text()
    parser = AttrReader(); parser.feed(article); parser.close()
    scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', head, re.S)
    assert len(scripts) == 1
    scholarly = load(scripts[0]); model = load((root/'page-model.json').read_text())
    assert scholarly['@type'] == 'ScholarlyArticle' and '@graph' not in scholarly
    abstract = html.unescape(re.search(r'<p id="abstract-text">(.*?)</p>', main, re.S).group(1))
    dc = [dict(a)['content'] for t,a in parser.tags if t == 'meta' and dict(a).get('name') == 'DC.description']
    assert dc == [model['abstract']] and abstract == scholarly['abstract'] == model['abstract']
    assert model['deployment_proposal']['slug'] == slug
    assets = []
    for row, encoding in zip(model['native_asset_order'], scholarly['encoding'], strict=True):
        pin = filepin(root/row['local_path'])
        assert pin == {'bytes': row['bytes'], 'SHA256': row['SHA256'], 'mode': mode(row['mode'])}
        assert encoding['contentUrl'] == row['local_path'] and encoding['name'] == row['name']
        assert encoding['contentSize'] == str(pin['bytes'])+' bytes'
        assert encoding['sameAs'] == row['native_url'] and encoding['encodingFormat'] == row['format']
        matches = [r for r,x in before['roots'][str(SOURCES[len(pages)][0])]['files'].items()
                   if (x['bytes'], x['SHA256']) == (pin['bytes'], pin['SHA256'])]
        assert matches
        assets.append({'relative_path': row['local_path'], **pin, 'native_source_matches': matches})
    pages.append({'family': family, 'slug': slug, 'model_schema': model['schema'],
                  'article': filepin(root/'article.html'), 'head': filepin(root/'head.html'),
                  'MAIN': filepin(root/'main.html'), 'BODY': {'bytes': len(body.encode()), 'SHA256': sha(body.encode())},
                  'Bib': filepin(root/'citation.bib'), 'abstract': abstract,
                  'head_shape': 'wrapped', 'schema_object': scholarly,
                  'native_encoding_names': [x['name'] for x in scholarly['encoding']], 'assets': assets,
                  'whole_assembly_and_strict_JSON_HTML_attributes': True})
public = before['public']
assert (public['regular_files'], public['child_directories'], public['directories']['.']['mode']) == (781,377,'0750')
assert sum(Path(r).name == '.DS_Store' for r in public['files']) == 17
index = (W/'public/research/index.html').read_bytes().decode('utf-8')
parser = AttrReader(); parser.feed(index); parser.close()
js = re.findall(r'<script type="application/ld\+json">(.*?)</script>', index, re.S)
assert len(js) == 1
collection = load(js[0]); itemlist = collection['mainEntity']; typed = itemlist['itemListElement']
assert collection['@type'] == 'CollectionPage' and itemlist['@type'] == 'ItemList'
assert itemlist['numberOfItems'] == len(typed) == 128
assert [r['position'] for r in typed] == list(range(1,129))
assert len({r['url'] for r in typed}) == 128
ul = re.findall(r'<ul>(.*?)</ul>', index, re.S)
assert len(ul) == 1
visible = re.findall(r'<li\b[^>]*>.*?</li>', ul[0], re.S)
assert len(visible) == 128
raw_json = raw_json_units(js[0]); assert len(raw_json) == 128
assert [load(r) for r in raw_json] == typed
for raw, obj in zip(visible, typed, strict=True):
    a = re.search(r'<a href="([^"]+)">(.*?)</a>', raw, re.S)
    assert obj['url'] == 'https://aleckriebel.com'+a.group(1)
    assert html.unescape(a.group(2)) == obj['name']
xml = (W/'public/research/sitemap.xml').read_bytes().decode('utf-8')
assert '<!DOCTYPE' not in xml and '<!ENTITY' not in xml
tree = ET.fromstring(xml); ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
assert tree.tag == ns+'urlset'
nodes = list(tree); assert len(nodes) == 129 and all(x.tag == ns+'url' for x in nodes)
locs = [x.find(ns+'loc').text for x in nodes]; assert len(set(locs)) == 129
raw_xml = re.findall(r'<url>.*?</url>', xml, re.S); assert len(raw_xml) == 129
parsed_xml = [{'tag':x.tag, 'attributes':x.attrib, 'children':[
    {'tag':y.tag, 'attributes':y.attrib, 'text':y.text, 'tail':y.tail} for y in x]} for x in nodes]
new_leaves, new_dirs = [], []
for page in pages:
    base = 'research/'+page['slug']
    new_dirs.extend([base, base+'/assets'])
    new_leaves.extend([base+'/index.html', base+'/citation.bib']+[base+'/'+x['relative_path'] for x in page['assets']])
for r in new_leaves + new_dirs:
    assert r not in public['files'] and r not in public['directories'] and not (W/'public'/r).exists()
assert len(new_leaves) == 9 and len(new_dirs) == 4
wi = (W/'.git/index').read_bytes()
assert len(wi) == 9059206 and sha(wi) == '592a25281b63a357fbe4fe2580e2c9764ba2b4836650d8751ac573ff8117c365'
assert wi[:4] == b'DIRC' and struct.unpack('!II',wi[4:12]) == (2,58721)
assert hashlib.sha1(wi[:-20]).digest() == wi[-20:]
assert before['native_W']['resolved_native_HEAD'] == '7d5ac8ea5dc8d6cddee457da7a5b40042d36d344'
assert before['native_M']['resolved_native_HEAD'] == 'a4ce3c37dad209339e490d18dcced6c48cf912d2'
oid = before['native_W']['resolved_native_HEAD']
loose = W/'.git/objects'/oid[:2]/oid[2:]
obj = zlib.decompress(loose.read_bytes())
assert hashlib.sha1(obj).hexdigest() == oid and obj.startswith(b'commit ')
native_tree = obj.split(b'\x00',1)[1].splitlines()[0].decode().removeprefix('tree ')
assert native_tree == 'c59d0d0a542f20bceb3556b1e936e86b22626434'
after = guards(); assert before == after
out = {'schema':'independent-hafnian-retract-stage-INITIAL-inputs-v1', 'UTC_start':started, 'UTC_end':now(),
       'status':'PASS_INPUT_BINDINGS_ONLY', 'guard_schema':'complete dictionaries keyed by canonical relative path; full bytes/SHA256/mode and all directory modes/emptiness; root is dot',
       'guards_before':before, 'guards_after_exact_equal':True, 'after_guard_digest':sha(json.dumps(after,sort_keys=True).encode()),
       'adoptions':adoptions, 'authenticated_finite_manifests':bindings, 'pages':pages,
       'aggregate_baseline':{'index_whole_UTF8':index,'sitemap_whole_UTF8':xml,
          'raw_visible_HTML_units':visible,'raw_JSON_units':raw_json,'typed_ItemList_units':typed,
          'raw_XML_units':raw_xml,'parsed_XML_units':parsed_xml,'XML_locations':locs,
          'counts':{'visible_HTML':128,'raw_JSON':128,'typed_JSON':128,'XML':129}},
       'new_public_relative_leaves':new_leaves,'new_public_relative_directories':new_dirs,
       'expected_candidate_derived_not_observed':{'files':790,'child_directories':381,'index_units':130,'sitemap_nodes':131},
       'exact_Git_relative_targets':['public/'+r for r in new_leaves+['research/index.html','research/sitemap.xml']],
       'native_W_commit_tree':native_tree, 'native_index':{'version':2,'records':58721,'bytes':len(wi),'SHA256':sha(wi),'checksum_valid':True},
       'new_producer_or_candidate_opened':False,'production_or_scientific_execution':False,
       'Git_network_W_source_otherpacket_writes':False,'future_persistence_or_live_certificate':False}
print(json.dumps(out, indent=2, ensure_ascii=False))
