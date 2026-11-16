#!/usr/bin/env python3
"""One fixed read-only data audit; no Git commands, network or project imports."""
import hashlib
import html
import json
import re
import stat
import struct
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

assert len(sys.argv) == 1
P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
O = P / 'verification/odd-areas-boolean-city-stage-audit-sol-20261116'
S = P / 'verification/odd-areas-boolean-city-stage-sol-20261116'
C = S / 'candidate'
ROOTS = {'23334001': (4345, '35067743c40008f58f5f89fe5358d8bece590f2cd0b282ab31637808ad1b5b02'), '23394004': (4342, 'a03bfee6ad864c35ee8cd322205843568f603396981fcce8da5dc03d8ddf92f0'), '23443301': (4367, '9d9e39487f2fca91f95502e506f91f90b250617496e031a154d701e6324cf5a0'), '23393139': (4316, 'fe3e276bb17fb83ef3279e13a4125ed2235b60692ceedfd4f83d83cc9eabbf73')}

def raw(p):
    assert p.is_file() and not p.is_symlink(), str(p)
    return p.read_bytes()

def obj(p):
    return json.loads(raw(p))

def sha(b):
    return hashlib.sha256(b).hexdigest()

def check(p, size, digest, mode=None):
    b = raw(p)
    assert len(b) == size and sha(b) == digest, str(p)
    if mode is not None:
        assert stat.S_IMODE(p.stat().st_mode) == (int(mode, 8) if isinstance(mode, str) else mode), str(p)

def checkq(base, q):
    check(base / q['path'], q['bytes'], q.get('SHA256', q.get('sha256')), q.get('mode'))

def extent(root):
    files, dirs = set(), set()
    for p in root.rglob('*'):
        assert not p.is_symlink(), str(p)
        if p.is_file(): files.add(p.relative_to(root).as_posix())
        elif p.is_dir(): dirs.add(p.relative_to(root).as_posix())
        else: raise AssertionError(str(p))
    return files, dirs

def topology(base, ledger, roots):
    expected = set()
    for line in raw(ledger).decode().splitlines():
        m = re.fullmatch(r'(Regular File|Directory) ([0-7]+) (\d+) (.+)', line)
        assert m, line
        kind, mode, size, name = m.groups()
        p = base / name
        assert not p.is_symlink() and stat.S_IMODE(p.stat().st_mode) == int(mode, 8), name
        assert (p.is_file() if kind == 'Regular File' else p.is_dir()), name
        if kind == 'Regular File': assert p.stat().st_size == int(size), name
        expected.add(name)
    actual = set()
    for root in roots:
        actual.add(root.relative_to(base).as_posix())
        actual.update(p.relative_to(base).as_posix() for p in root.rglob('*'))
    assert actual == expected

def hash_ledger(base, path):
    lines = raw(path).decode().splitlines()
    for line in lines:
        digest, name = line.split('  ', 1)
        assert sha(raw(base / name)) == digest, name
    return len(lines)

def head(root):
    g = root / '.git'
    symbolic = raw(g / 'HEAD').decode().strip()
    assert symbolic.startswith('ref: ')
    ref = symbolic[5:]
    if (g / ref).exists(): commit = raw(g / ref).decode().strip()
    else: commit = next(s.split()[0] for s in raw(g / 'packed-refs').decode().splitlines() if s.endswith(' ' + ref))
    return {'symbolic': symbolic, 'commit': commit}

def native_guards():
    for key in ['website_git', 'Math_git']:
        g = base[key]
        assert head(Path(g['root'])) == g['HEAD']
        for k in ['index', 'config', 'HEAD_file']: checkq(Path('/'), g[k])
    for q in base['source_guards'] + base['website_configuration_guards'] + base['template_guards']: checkq(Path('/'), q)
    b = raw(W / '.git/index')
    assert len(b) == 9049366 and sha(b) == '8db8d40ce28617085e5e3b7e61ba00bf2e68748a981b881e31d49d3edef21d6e'
    assert stat.S_IMODE((W / '.git/index').stat().st_mode) == 0o644
    assert b[:4] == b'DIRC' and struct.unpack('>II', b[4:12]) == (2, 58651)
    assert hashlib.sha1(b[:-20]).digest() == b[-20:]
    check(P.parent / '.git/index', 25854746, '91b10d938f7d737226662bbff3b07016dcc0e501376a045811ab4e930c6fbb11', '0644')
    assert hash_ledger(W, O / 'W_PUBLIC_SHA256.txt') == 711
    topology(W, O / 'W_PUBLIC_TOPOLOGY.txt', [W / 'public'])
    assert hash_ledger(P, O / 'SOURCE_SHA256.txt') == 614
    topology(P, O / 'SOURCE_TOPOLOGY.txt', [P / 'papers' / rid / 'sources' for rid in ROOTS])
    for line in raw(O / 'W_SOURCE_GUARDS.txt').decode().splitlines():
        if re.match(r'^[a-f0-9]{64}  ', line):
            digest, name = line.split('  ', 1)
            assert sha(raw(W / name)) == digest

def normalized_abstract(s):
    s = re.sub(r'<sub>(.*?)</sub>', r'_{\1}', s, flags=re.S)
    s = re.sub(r'<sup>(.*?)</sup>', r'^\1', s, flags=re.S)
    s = html.unescape(re.sub(r'<[^>]*>', '', s))
    for old, new in [(r'\alpha', 'α'), (r'\beta', 'β'), (r'\(', ''), (r'\)', ''), ('$', ''), ('--', '–'), ('’', "'"), ('−', '-'), ('⁸', '^8')]: s = s.replace(old, new)
    s = ' '.join(s.split())
    return re.sub(r'\s*([=<>])\s*', r'\1', s)

class Tags(HTMLParser):
    def __init__(self, s):
        super().__init__(convert_charrefs=True)
        self.meta, self.ids, self.refs, self.canonical, self.h1 = {}, [], [], [], 0
        self.feed(s)
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'meta':
            key = d.get('name', d.get('property'))
            assert key not in self.meta, key
            self.meta[key] = d.get('content')
        if 'id' in d: self.ids.append(d['id'])
        if tag == 'h1': self.h1 += 1
        if tag == 'link' and d.get('rel') == 'canonical': self.canonical.append(d['href'])
        for key in ['href', 'src']:
            if key in d: self.refs.append(d[key])

def json_script(s):
    matches = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', s, re.S)
    assert len(matches) == 1
    return matches[0]

def raw_items(s):
    pos = s.index('[', s.index('"itemListElement"')) + 1
    result = []
    while True:
        while s[pos].isspace() or s[pos] == ',': pos += 1
        if s[pos] == ']': return result
        _, n = json.JSONDecoder().raw_decode(s[pos:])
        result.append(s[pos:pos + n]); pos += n

check(O / 'INITIAL_SEAL.json', 4337, 'a82852017014fc27eb35c64715c099e2157885666bb036d3c261a0693671e48d')
for q in obj(O / 'INITIAL_SEAL.json')['files']: checkq(O, q)
check(O / 'LEGACY160_FINAL.json', 3005, '40255209c379a47705c7dd6504ac7e68b4981028a86ee87dee1ccd9688e57090')
for q in obj(O / 'LEGACY160_FINAL.json')['files']: checkq(O, q)
for name, size, digest in [('FINAL.json',18762,'44e1488e21bbf2042cc1b4baa8a206b53070f020bd3aa130df85336f63de334e'),('MANIFEST.json',9062,'757699582a402f41ec90fd4079a71bf04bd2c2c6b67b992ca8da214e2b35ab4e'),('REPORT.md',6098,'1dc2b3f9cfb59c9754ab25dd308ac6af3cbd502b52834fc181cdf574d54a43aa'),('PUBLIC_PAYLOADS.json',10541,'d0dc392f4cb8e2f7b8b4386a2b5187c2d54a0039955d53ed6eff26a91e286020')]: check(S/name,size,digest)
manifest = obj(S / 'MANIFEST.json')
stage_files, stage_dirs = extent(S)
assert stage_files == {q['path'] for q in manifest['files']} | {'MANIFEST.json','FINAL.json'} and len(stage_files) == 40
assert stage_dirs == {q['path'] for q in manifest['directories']} and len(stage_dirs) == 7
for q in manifest['files']: checkq(S, q)
for q in manifest['directories']: assert stat.S_IMODE((S/q['path']).stat().st_mode) == int(q['mode'],8)
base = obj(S / 'BASELINE.json')
native_guards()
model_rows = obj(S/'PUBLIC_MODELS.json')
public_models = {str(q['record_id']): q for q in model_rows}
assert len(model_rows) == len(public_models) == 4 and set(public_models) == set(ROOTS)
payloads = obj(S / 'PUBLIC_PAYLOADS.json')
assert len(payloads) == 18 and sum(q['operation']=='A' for q in payloads) == 16 and sum(q['operation']=='M' for q in payloads) == 2
for q in payloads: check(Path(q['path']), q['bytes'], q['SHA256'], q['mode'])
candidate_files, candidate_dirs = extent(C)
assert len(candidate_files) == 18 and len(candidate_dirs) == 6
assert candidate_files == {q['website_relative_path'] for q in payloads}
expected, article_results, packet_count = {'public/research/index.html','public/research/sitemap.xml'}, [], 0
template = raw(W/'public/research/three-summand-kato-kernel-counterexample/index.html').decode()
prefix = template[template.index('<body>'):template.index('<main')]
suffix = template[template.index('</main>')+7:]
for rid, (size, digest) in ROOTS.items():
    rp = P/f'verification/root-editorial-{rid}-20261116.json'; check(rp,size,digest); a=obj(rp)
    assert a['publication_authority'] is False and a['AA_authority'] is False and a['follow_up'] is None
    for lane in ['writer','independent_fact_fidelity']:
        d=a[lane]; folder=(P/d['FINAL']['path']).parent
        for k in ['FINAL','manifest','REPORT']: checkq(P,d[k])
        m=obj(P/d['manifest']['path']); entries=m.get('files',m.get('payloads'))
        for q in entries: checkq(folder,q)
        fs, ds=extent(folder)
        assert fs=={q['path'] for q in entries}|{'FINAL.json','OWNED_MANIFEST.json'} and len(fs)==d['whole_files'] and len(ds)==d['child_directories']
        packet_count += len(fs)
    for k in ['MAIN','model','whole_private_preview']: checkq(P,a[k])
    d=(P/a['MAIN']['path']).parent; private=obj(P/a['model']['path']); record=obj(P/'papers'/rid/'sources/record.response.body')
    slug=a['proposed_slug']; folder='public/research/'+slug; url='https://aleckriebel.com/research/'+slug+'/'
    names=[f['key'] for f in record['files']]; pdfs=[n for n in names if n.endswith('.pdf')]; assert len(pdfs)==1; pdf=pdfs[0]
    expected.update(folder+'/'+n for n in names); expected.update({folder+'/index.html',folder+'/citation.bib'})
    assert not (W/folder).exists()
    page=raw(C/folder/'index.html').decode(); main=re.search(r'<main\b.*?</main>',page,re.S).group(0)
    approved=raw(P/a['MAIN']['path']); assert main.encode()==approved.rstrip(b'\n')
    assert page[page.index('<body>'):page.index('<main')]==prefix and page[page.index('</main>')+7:]==suffix
    h=Tags(page); assert len(h.ids)==len(set(h.ids)) and h.h1==1 and h.canonical==[url]
    schema=json.loads(json_script(page)); pm=public_models[rid]
    assert schema==pm['ScholarlyArticle'] and pm['canonical_url']==url
    assert all(pm[k] is None for k in ['AA','follow_up']) and pm['publication_authority'] is False
    assert h.meta['DC.description']==schema['abstract']==private['abstract']==pm['full_abstract_DC_description']
    source=raw(O/f'ABSTRACT_{rid}.tex').decode().split(r'\begin{abstract}',1)[1].split(r'\end{abstract}',1)[0]
    visible=re.search(r'<p id="original-abstract">(.*?)</p>',main,re.S) if rid=='23443301' else re.search(r'<section id="original-abstract".*?<p>(.*?)</p>',main,re.S)
    assert normalized_abstract(source)==normalized_abstract(visible.group(1))==normalized_abstract(schema['abstract'])
    title=record['metadata']['title']; doi=record['metadata']['doi']; version=record['metadata']['version']; date=record['metadata']['publication_date']
    assert schema['name']==schema['headline']==h.meta['citation_title']==h.meta['DC.title']==title
    assert schema['datePublished']==date and schema['version']==h.meta['citation_version']==version
    assert h.meta['citation_publication_date']==date.replace('-','/') and h.meta['article:published_time']==date
    assert h.meta['citation_author_orcid']=='https://orcid.org/0009-0001-9320-500X'
    assert schema['author']['name']=='Alec Kriebel' and schema['author']['identifier']==h.meta['citation_author_orcid']
    assert h.meta['citation_doi']==doi and schema['sameAs']=='https://doi.org/'+doi
    assert schema['@id']==url+'#article' and schema['url']==schema['mainEntityOfPage']==url
    assert schema['license']=='https://creativecommons.org/licenses/by/4.0/' and schema['creativeWorkStatus']=='Unrefereed preprint'
    assert h.meta['robots']=='index, follow, max-image-preview:large' and 'editorial-status' not in h.meta
    assert h.meta['og:url']==url and h.meta['og:title']==h.meta['twitter:title']==title
    assert h.meta['description']==h.meta['og:description']==h.meta['twitter:description']==pm['short_description']
    assert h.meta['citation_pdf_url']==url+pdf and 'href="/research/research.css"' in page
    assets=re.search(r'<ol id="native-(?:downloads|assets)">(.*?)</ol>',main,re.S).group(1)
    assert re.findall(r'<li>\s*<a href="([^"]+)" download>',assets)==names
    assert [x['name'] for x in schema['encoding']]==names
    for f, enc in zip(record['files'],schema['encoding']):
        b=raw(P/'papers'/rid/'sources/assets'/f['key']); assert b==raw(C/folder/f['key'])
        assert len(b)==f['size'] and 'md5:'+hashlib.md5(b).hexdigest()==f['checksum']
        assert enc['contentUrl']==url+f['key'] and enc['sameAs']==f['links']['self'] and enc['contentSize']==str(len(b))+' bytes'
    assert raw(C/folder/'citation.bib')==raw(d/'preview/citation.bib')
    for ref in h.refs:
        u=urlsplit(ref)
        if u.netloc and u.netloc!='aleckriebel.com': continue
        if u.scheme and u.scheme!='https': raise AssertionError(ref)
        if not u.path: assert not u.fragment or u.fragment in h.ids; continue
        path='public'+unquote(u.path) if u.path.startswith('/') else str(Path(folder)/unquote(u.path))
        if u.path.endswith('/'): path+='index.html'
        target=C/path if (C/path).is_file() else W/path
        assert target.is_file(), (rid,ref,path)
        if u.fragment and path.endswith('.html'): assert u.fragment in Tags(raw(target).decode()).ids
    article_results.append({'record_id':rid,'canonical':url,'MAIN_external_LF_removed':len(approved)-len(main.encode()),'full_abstract_surfaces_exact':True,'original_native_order':names})
assert candidate_files==expected
old=raw(O/'BASELINE_INDEX.html').decode(); new=raw(C/'public/research/index.html').decode()
old_li=re.findall(r'<li\b[^>]*>.*?</li>',old,re.S); new_li=re.findall(r'<li\b[^>]*>.*?</li>',new,re.S)
assert len(old_li)==114 and len(new_li)==118 and new_li[:114]==old_li
old_script=json_script(old); new_script=json_script(new)
assert raw_items(new_script)[:114]==raw_items(old_script)
old_items=json.loads(old_script)['mainEntity']['itemListElement']; new_items=json.loads(new_script)['mainEntity']['itemListElement']
assert len(new_items)==118 and new_items[:114]==old_items and json.loads(new_script)['mainEntity']['numberOfItems']==118
assert len({x['url'] for x in new_items})==118
assert new.replace(new_script,old_script,1).replace('\n'+'\n'.join(new_li[114:]),'',1)==old
old_xml=raw(O/'BASELINE_SITEMAP.xml').decode(); new_xml=raw(C/'public/research/sitemap.xml').decode()
old_nodes=re.findall(r'<url\b[^>]*>.*?</url>',old_xml,re.S); new_nodes=re.findall(r'<url\b[^>]*>.*?</url>',new_xml,re.S)
assert len(old_nodes)==115 and len(new_nodes)==119 and new_nodes[:115]==old_nodes
assert new_xml.replace('\n'+'\n'.join(new_nodes[115:]),'',1)==old_xml
assert len(set(re.findall(r'<loc>(.*?)</loc>',new_xml)))==119
for j,r in enumerate(article_results):
    record=obj(P/'papers'/r['record_id']/'sources/record.response.body'); title=record['metadata']['title']; date=record['metadata']['publication_date']; url=r['canonical']
    assert new_items[114+j]=={'@type':'ListItem','position':115+j,'url':url,'name':title}
    assert html.escape(title) in new_li[114+j] and url.removeprefix('https://aleckriebel.com') in new_li[114+j]
    assert '<loc>'+url+'</loc>' in new_nodes[115+j] and '<lastmod>'+date+'</lastmod>' in new_nodes[115+j]
assert len({q['website_relative_path'] for q in payloads})==18
assert {q['website_relative_path'] for q in payloads if q['operation']=='M'}=={'public/research/index.html','public/research/sitemap.xml'}
assert len(set(x.split('  ',1)[1] for x in raw(O/'W_PUBLIC_SHA256.txt').decode().splitlines())|{q['website_relative_path'] for q in payloads})==727
assert obj(S/'BUILD_EXECUTION.json')['exit_code']==0 and len(raw(S/'BUILD.stderr.txt'))==404 and b'SyntaxWarning' in raw(S/'BUILD.stderr.txt')
native_guards()
print(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS_INDEPENDENT_STATIC_DATA_SEMANTIC_INTEGRATION_ONLY','stage_files':40,'stage_child_directories':7,'candidate_files':18,'candidate_child_directories':6,'delta':{'A':16,'M':2},'projection':[727,118,119],'old_public_buffers_modes_topology_preserved':711,'frozen_source_files_guarded':614,'writer_and_fact_files_guarded':packet_count,'old_visible_and_raw_typed_units_preserved':114,'old_XML_nodes_preserved':115,'aggregate_other_bytes_exact_after_removing_only_four_additions':True,'articles':article_results,'W_native_index_SHA256':'8db8d40ce28617085e5e3b7e61ba00bf2e68748a981b881e31d49d3edef21d6e','W_native_index_mode':'0644','current_records':58651,'future_protected_raw_records':58649,'future_records_arithmetic_only':58667,'builder_exit':0,'literal_builder_stderr_bytes':404,'new_render_native_live_download_or_Git_actions':0,'publication_authority':False},indent=2))
