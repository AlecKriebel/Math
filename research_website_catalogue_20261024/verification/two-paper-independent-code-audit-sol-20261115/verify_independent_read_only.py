"""Bounded independent custody/integration verification; standard library only.

No project imports, builder calls, source-program execution, network, subprocess,
dynamic execution, or file writes. All synthetic faults exist only as strings.
The caller may capture stdout inside this audit folder. This checks the exact
two sealed candidates and does not supply scientific or publication authority.
"""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
import re
import copy
import xml.etree.ElementTree as ET

A = Path(__file__).resolve().parent
P = A.parents[1]
S = P / 'verification/two-paper-private-stage-sol-20261115'
FIVE = P / 'verification/five-paper-private-stage-sol-20261115'
SEAL_HASH = 'a45d001076d00146aeccc7ebf0c4244cd9c755ad75b9a6fdd5e1d7be8592f012'
MANIFEST_HASH = '4ab11d2140f7e28ea0f87c2ffe3910a28a5208c4525288771276e14787842a4b'
PINNED = {
 '23385145': ('89d8f041c3dcd378080b800404910935c847405f00ca974d09c8805f720e3130',
              '7103359ae07eb8c6e6560c7c8626cd991cc0c69f222134e10bea642b50350331'),
 '22983513': ('7f690a368ebcfee37c85d0eeffbfc70fe58d2eecd1e2acab17b4e174799d1499',
              '048205b0aa267298ac034afa9fdf2c88973c05e68e6d0278e4accfcac2c0da57')}
CHECKS = []

def require(ok, label):
 if not ok:
  raise ValueError(label)
 CHECKS.append(label)

def digest(data):
 return hashlib.sha256(data).hexdigest()

def bind(path):
 path = Path(path)
 require(path.is_file() and not path.is_symlink(), 'regular:' + str(path))
 data = path.read_bytes()
 return {'bytes': len(data), 'sha256': digest(data)}

def parse(raw):
 def pairs(items):
  d = {}
  for k, v in items:
   if k in d:
    raise ValueError('duplicate JSON key:' + k)
   d[k] = v
  return d
 def invalid(v):
  raise ValueError('nonfinite JSON constant:' + v)
 return json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid)

def load(path):
 return parse(Path(path).read_bytes())

def literal(a, b):
 if type(a) is not type(b):
  return False
 if type(a) is dict:
  return list(a) == list(b) and all(literal(a[k], b[k]) for k in a)
 if type(a) is list:
  return len(a) == len(b) and all(literal(x, y) for x, y in zip(a, b))
 return a == b

def text(n):
 if isinstance(n, str):
  return n
 return ''.join(text(c) for c in n[2])

def walk(n):
 if isinstance(n, tuple):
  yield n
  for c in n[2]:
   yield from walk(c)

class Document(HTMLParser):
 def __init__(self, raw):
  super().__init__(convert_charrefs=True)
  self.root = ('root', {}, [])
  self.stack = [self.root]
  self.feed(raw)
  self.close()
  require(len(self.stack) == 1, 'balanced independent DOM')
 def handle_starttag(self, tag, attrs):
  require(len(dict(attrs)) == len(attrs), 'unique HTML attributes')
  n = (tag, dict(attrs), [])
  self.stack[-1][2].append(n)
  if tag not in {'meta', 'link', 'br', 'hr', 'img', 'input', 'source', 'wbr'}:
   self.stack.append(n)
 def handle_endtag(self, tag):
  require(len(self.stack) > 1 and self.stack[-1][0] == tag, 'balanced tag:' + tag)
  self.stack.pop()
 def handle_data(self, data):
  self.stack[-1][2].append(data)
 def handle_comment(self, data):
  raise ValueError('unexpected HTML comment')
 def all(self, tag):
  return [n for n in walk(self.root) if n[0] == tag]
 def one(self, tag):
  found = self.all(tag)
  require(len(found) == 1, 'unique element:' + tag)
  return found[0]

def main_signature(n):
 if isinstance(n, str):
  return ('text', n)
 return (n[0], tuple(sorted(n[1].items())), tuple(main_signature(c) for c in n[2]))

def inline_text(raw):
 return re.sub(r'\[([^\]]+)\]\(([^\s)]+)\)', r'\1', raw)

def markdown_blocks(raw):
 rows = []
 for block in re.split(r'\n\s*\n', raw.strip()):
  if block.startswith('```bibtex\n'):
   require(block.endswith('\n```'), 'complete approved BibTeX fence')
   rows.append(('code', block[10:-4] + '\n'))
  elif block.startswith('## '):
   rows.append(('h2', block[3:]))
  elif block.startswith('# '):
   rows.append(('h1', block[2:]))
  elif all(line.startswith('- ') for line in block.splitlines()):
   rows.extend(('li', inline_text(line[2:])) for line in block.splitlines())
  else:
   rows.append(('p', inline_text(' '.join(block.splitlines()))))
 return rows

def verify_article(raw, o, files):
 c = o['whole_publication_original']
 rid = str(o['whole_SOURCE_READY_original']['record_id'])
 base = c['proposed_canonical_url']
 doc = Document(raw)
 article = doc.one('article')
 main = doc.one('main')
 require(main[1] == {'id': 'main'}, rid + ':main destination')
 require(doc.one('h1')[2] == [('a', {'href': '/research/' + c['slug'] + '/'}, [c['title']])], rid + ':self title')
 require(not doc.all('style'), rid + ':no inline hiding CSS')
 for n in walk(doc.root):
  require(n[0] not in {'template', 'noscript', 'object', 'embed'}, rid + ':no hidden container')
  require(not any(k in n[1] for k in ('style', 'hidden', 'inert', 'aria-hidden')),
          rid + ':no hiding attributes')
  require(not any(k.startswith('on') for k in n[1]), rid + ':no event handlers')
 skip = [n for n in walk(doc.root) if 'skip-link' in n[1].get('class', '').split()]
 require(len(skip) == 1 and skip[0] == ('a', {'class': 'skip-link', 'href': '#main'}, ['Skip to content']), rid + ':only legitimate skip link')
 require(all('skip-link' not in n[1].get('class', '').split() for n in walk(article)), rid + ':no hidden article paragraph')
 approved = (P / 'papers' / rid / 'reviews/editorial/PUBLIC_COPY.md').read_text()
 if rid == '23385145':
  old = Document((P / 'papers' / rid / o['layout']['source_html']).read_text())
  n = copy.deepcopy(old.one('main'))
  n[1].clear()
  n[1]['id'] = 'main'
  n[2][:] = [('article', {}, n[2][:])]
  for q in walk(n):
   for key in ('href', 'src'):
    if q[1].get(key, '').startswith('assets/'):
     q[1][key] = q[1][key][7:]
   if q[1].get('class') == 'byline':
    q[1]['class'] = 'entry-meta'
   if q[0] == 'h1':
    q[2][:] = [('a', {'href': '/research/' + c['slug'] + '/'}, q[2][:])]
   if q[0] == 'iframe':
    q[1]['class'] = 'paper-pdf'
    q[1]['loading'] = 'lazy'
    # Current stdlib HTMLParser treats iframe fallback as raw text. The
    # approved source has a single fallback PDF link; rebase its exact path
    # as well, without depending on the owner's older parser behavior.
    q[2][:] = [v.replace('href="assets/weighted_centers.pdf"', 'href="weighted_centers.pdf"') if isinstance(v, str) else v for v in q[2]]
  require(main_signature(main) == main_signature(n), rid + ':whole approved source DOM with only declared presentation transforms')
  visible = [(q[0], text(q)) for q in walk(article) if q[0] in {'h1', 'h2', 'p', 'li'}]
  for kind, value in markdown_blocks(approved):
   if kind in {'h1', 'h2', 'p'}:
    require((kind, value) in visible, rid + ':every complete approved prose block')
  original_scholar = parse(text(old.one('script')))
  expected_metas = {q[1].get('name', q[1].get('property', q[1].get('charset'))): q[1].get('content') for q in old.all('meta')}
 else:
  visible = [(q[0], text(q)) for q in walk(article) if q[0] in {'h1', 'h2', 'p', 'li', 'code'}]
  require(visible == markdown_blocks(approved), rid + ':whole approved Markdown block content and order')
  require(all(not q[1] for q in walk(article) if q[0] in {'p', 'h1', 'h2', 'li', 'code'}), rid + ':ordinary article nodes cannot carry hiding classes')
  meta = load(P / 'papers' / rid / o['layout']['metadata'])
  original_scholar = meta['jsonld']
  expected_metas = {'utf-8': None, 'viewport': 'width=device-width, initial-scale=1', 'description': c['description'], **meta['citation_meta']}
  expected_metas.update({'og:' + k: meta['open_graph'][k] for k in ('type', 'title', 'description')})
  wanted_hrefs = ['/research/' + c['slug'] + '/'] + re.findall(r'\[[^\]]+\]\(([^\s)]+)\)', approved)
  require([q[1]['href'] for q in walk(article) if q[0] == 'a'] == wanted_hrefs, rid + ':all approved link destinations and order')
 expected_metas.update({'robots': 'index,follow', 'citation_pdf_url': base + c['pdf_filename'], 'citation_author_orcid': '0009-0001-9320-500X', 'citation_language': 'en', 'og:url': base})
 for k, v in [('og:type', 'article'), ('og:title', c['title']), ('og:description', c['description'])]:
  expected_metas.setdefault(k, v)
 metas = {}
 for q in doc.all('meta'):
  k = q[1].get('name', q[1].get('property', q[1].get('charset')))
  require(k not in metas, rid + ':metadata uniqueness')
  metas[k] = q[1].get('content')
 require(metas == expected_metas, rid + ':all approved metadata fields')
 require(text(doc.one('title')) == c['title'] + ' | Alec Kriebel', rid + ':SEO title')
 require([q[1] for q in doc.all('link')] == [
  {'rel': 'canonical', 'href': base}, {'rel': 'icon', 'href': '/favicon.ico'},
  {'rel': 'stylesheet', 'href': '/research/research.css'}], rid + ':proposed canonical and existing stylesheet')
 script = doc.one('script')
 require(script[1] == {'type': 'application/ld+json'}, rid + ':only static JSON-LD')
 graph = parse(text(script))
 require(list(graph) == ['@context', '@graph'] and graph['@context'] == 'https://schema.org' and len(graph['@graph']) == 2, rid + ':complete schema graph')
 page, scholar = graph['@graph']
 require(page == {'@type': 'WebPage', '@id': base + '#page', 'url': base, 'name': c['title'], 'dateCreated': '2026-11-15', 'dateModified': '2026-11-15', 'mainEntity': {'@id': base + '#article'}}, rid + ':webpage dates distinct from edition')
 expected = copy.deepcopy(original_scholar)
 expected.pop('@context')
 for k, v in [('name', c['title']), ('version', c['version']), ('creativeWorkStatus', 'Unrefereed preprint')]:
  expected.setdefault(k, v)
 expected.update({'@id': base + '#article', 'url': base, 'sameAs': 'https://doi.org/' + c['doi']})
 if 'encoding' in expected:
  for encoding in expected['encoding']:
   encoding['contentUrl'] = base + c['pdf_filename']
 else:
  expected['encoding'] = [
   {'@type': 'MediaObject', 'encodingFormat': 'application/pdf', 'contentUrl': base + c['pdf_filename']},
   {'@type': 'MediaObject', 'encodingFormat': 'application/zip', 'contentUrl': base + c['supplement_filename']}]
 require(literal(scholar, expected), rid + ':all scholarly fields including literal abstract')
 require(scholar['abstract'] == c['abstract'] and scholar['datePublished'] == c['publication_date'], rid + ':complete abstract and original date')
 frame = doc.one('iframe')
 require(frame[1]['src'] == c['pdf_filename'] and frame[1]['class'] == 'paper-pdf' and frame[1]['loading'] == 'lazy' and frame[1]['title'], rid + ':accessible complete native reader')
 links = [q for q in walk(article) if q[0] == 'a']
 expected_leaves = {'index.html', 'citation.bib'} | {x['original_api_file_object']['key'] for x in o['whole_SOURCE_READY_original']['all_assets_in_original_order']}
 require(set(files) == expected_leaves, rid + ':complete exact native leaf namespace')
 for q in doc.all('a'):
  href = q[1]['href']
  if not href.startswith(('https://', '/', '#')):
   require(href in files, rid + ':local link resolves:' + href)
 for name in [c['pdf_filename'], c['supplement_filename'], 'citation.bib'] + (['SHA256SUMS.txt'] if rid == '22983513' else []):
  require(any(q[1].get('href') == name and 'download' in q[1] for q in links), rid + ':real download:' + name)
 require(files['citation.bib'].decode() == c['prepared_bibtex'], rid + ':complete approved citation')
 require([q[1]['href'] for q in walk(doc.all('header')[0]) if q[0] == 'a'][4:] == [x['original_api_file_object']['links']['self'] for x in o['whole_SOURCE_READY_original']['all_assets_in_original_order']], rid + ':native API asset order')
 return {'record_id': rid, 'article_sha256': digest(raw.encode()), 'native_pages_preserved_by_approved_PDF_bytes': c['pdf_pages'], 'asset_leaves': len(files), 'literal_full_copy_and_metadata': True}

def verify_overlays(index, sitemap, source):
 before = (S / 'baseline/research/index.html').read_text()
 oldmap = (S / 'baseline/research/sitemap.xml').read_text()
 rows = re.findall(r'<li>.*?</li>', index, re.S)
 oldrows = re.findall(r'<li>.*?</li>', before, re.S)
 require(len(rows) == 85 and len(oldrows) == 83 and rows[:83] == oldrows, '85 index entries preserve complete old83')
 rx = r'<script type="application/ld\+json">\s*(.*?)\s*</script>'
 original_schema_match = re.search(rx, before, re.S)
 schema_match = re.search(rx, index, re.S)
 oldschema = parse(original_schema_match[1])
 newschema = parse(schema_match[1])
 expected_schema = copy.deepcopy(oldschema)
 expected_schema['mainEntity']['numberOfItems'] = 85
 urls = []
 for pos, (rid, o) in enumerate(source['records'].items(), 84):
  c = o['whole_publication_original']
  urls.append(c['proposed_canonical_url'])
  expected_schema['mainEntity']['itemListElement'].append({'@type': 'ListItem', 'position': pos, 'url': c['proposed_canonical_url'], 'name': c['title']})
  d = Document('<!doctype html><html><body><ul>' + rows[pos - 1] + '</ul></body></html>')
  require(text(d.all('a')[0]) == c['title'] and d.all('a')[0][1]['href'] == '/research/' + c['slug'] + '/', rid + ':index complete title')
  require(text(d.all('p')[0]) == c['description'], rid + ':index complete scoped description')
  require([q[1]['href'] for q in d.all('a')[1:]] == ['/research/' + c['slug'] + '/' + c['pdf_filename'], 'https://doi.org/' + c['doi']], rid + ':index native PDF and DOI')
 require(literal(newschema, expected_schema), 'complete old ItemList plus exact two')
 restored = index[:schema_match.start(1)] + original_schema_match[1] + index[schema_match.end(1):]
 for row in rows[-2:]:
  require(restored.count('      ' + row + '\n') == 1, 'unique appended index row')
  restored = restored.replace('      ' + row + '\n', '', 1)
 require(restored == before, 'every other index byte preserved')
 oldlocs = [n.text for n in ET.fromstring(oldmap).findall('{*}url/{*}loc')]
 newlocs = [n.text for n in ET.fromstring(sitemap).findall('{*}url/{*}loc')]
 require(len(oldlocs) == 84 and newlocs == oldlocs + urls and len(set(newlocs)) == 86, '86 unique sitemap locations preserve old84')
 restored = sitemap
 for url in urls:
  row = '  <url><loc>' + url + '</loc><lastmod>2026-11-15</lastmod></url>\n'
  require(restored.count(row) == 1, 'exact appended sitemap row')
  restored = restored.replace(row, '', 1)
 require(restored == oldmap, 'every other sitemap byte preserved')

def run():
 initial = load(A / 'INPUT_MANIFEST.json')
 for x in initial['all_input_files']:
  require(bind(x['path']) == {k: x[k] for k in ('bytes', 'sha256')}, 'unchanged initial custody:' + x['path'])
 require(digest((S / 'FINAL_SEAL.json').read_bytes()) == SEAL_HASH, 'exact final stage seal')
 require(digest((S / 'OWNED_MANIFEST.json').read_bytes()) == MANIFEST_HASH, 'exact final stage manifest')
 seal = load(S / 'FINAL_SEAL.json')
 manifest = load(S / 'OWNED_MANIFEST.json')
 require(len(manifest['files']) == 99, '99 sealed payloads')
 require({str(q.relative_to(S)) for q in S.rglob('*') if q.is_file()} == {x['path'] for x in manifest['files']} | {'FINAL_SEAL.json', 'OWNED_MANIFEST.json'}, 'entire stage namespace sealed')
 require(not any(q.is_symlink() for q in S.rglob('*')), 'no stage symlinks')
 for x in manifest['files']:
  require(bind(S / x['path']) == {k: x[k] for k in ('bytes', 'sha256')}, 'stage payload:' + x['path'])
 for k, name in [('report_sha256', 'REPORT.md'), ('verdict_sha256', 'VERDICT.json'), ('ready_sha256', 'CANDIDATE_READY.json'), ('code_manifest_sha256', 'CODE_MANIFEST.json'), ('source_inputs_sha256', 'SOURCE_INPUTS.json'), ('baseline_sha256', 'FRESH_BASELINE.json')]:
  require(bind(S / name)['sha256'] == seal[k], 'stage seal field:' + name)
 codes = load(S / 'CODE_MANIFEST.json')['files']
 require(len(codes) == 11, 'all11 code bodies')
 for x in codes:
  require(bind(S / x['path']) == {k: x[k] for k in ('bytes', 'sha256')}, 'read exact helper body:' + x['path'])
 source = load(S / 'SOURCE_INPUTS.json')
 require(list(source['records']) == ['23385145', '22983513'] and len(source['input_files']) == 356, 'exact two records and356 input bindings')
 for x in source['input_files']:
  require(bind(x['path']) == {k: x[k] for k in ('bytes', 'sha256')}, 'frozen source/editorial/reference binding:' + x['path'])
 ready = load(S / 'CANDIDATE_READY.json')
 expected = {x['path']: x for x in ready['all11_output_paths_and_hashes']}
 require(len(expected) == 11, 'exact11 paired output paths')
 for pair in ('candidate-a', 'candidate-b'):
  root = S / pair / 'public'
  require({str(q.relative_to(root)) for q in root.rglob('*') if q.is_file()} == set(expected), pair + ':exact complete output namespace')
  for rel, x in expected.items():
   require(bind(root / rel) == {k: x[k] for k in ('bytes', 'sha256')}, pair + ':whole output bytes:' + rel)
 records = []
 family_count = 0
 for rid, o in source['records'].items():
  paper = P / 'papers' / rid
  c, promotion = o['whole_publication_original'], o['whole_promotion_original']
  for name, key in [('publication.json', 'whole_publication_original'), ('promotion.json', 'whole_promotion_original'), ('sources/SOURCE_READY.json', 'whole_SOURCE_READY_original'), ('reviews/editorial/PUBLICATION_REQUIREMENTS.json', 'whole_requirements_original')]:
   require(literal(load(paper / name), o[key]), rid + ':whole original heterogeneous object:' + name)
  for prefix, key, wanted in [('root-editorial-', 'whole_editorial_root_authority_original', PINNED[rid][0]), ('root-clearance-', 'whole_scientific_root_authority_original', PINNED[rid][1])]:
   path = P / 'verification' / (prefix + rid + '-20261115.json')
   require(bind(path)['sha256'] == wanted and literal(load(path), o[key]), rid + ':whole exact adopted authority:' + prefix)
  require(literal(promotion['whole_root_scientific_clearance_record'], o['whole_scientific_root_authority_original']), rid + ':qualified scientific authority preserved literally')
  for key in ('AA', 'canonical_url', 'follow_up'):
   require(c[key] is None and promotion[key] is None, rid + ':original null unchanged:' + key)
  for key in ('rendered', 'deployed', 'rendered_public_copy_approved', 'local_http_verified', 'live_http_verified', 'browser_verified', 'native_sheet_publication_verified', 'public_page_published', 'root_editorial_clearance_received', 'production_integration_authorized', 'publication_clearance', 'ready_to_publish', 'canonical_verified'):
   require(promotion[key] is False, rid + ':historical closed flag unchanged:' + key)
  for role, api in o['whole_native_API_objects_original'].items():
   x = api['binding_original']
   require(bind(x['path']) == {'bytes': x['bytes'], 'sha256': x['SHA256']} and literal(load(x['path']), api['whole_original_object']), rid + ':whole original API object:' + role)
  rr = o['whole_SOURCE_READY_original']
  require(literal(load(rr['actual_transport_receipt_path']), o['whole_native_transport_aggregate_original']), rid + ':complete transport schema order and failures unchanged')
  native = o['whole_native_API_objects_original']['record']['whole_original_object']
  require(native['files'] == [x['original_api_file_object'] for x in rr['all_assets_in_original_order']], rid + ':original native asset objects and order')
  require(c['publication_date'] == native['metadata']['publication_date'] and c['version'] == native['metadata']['version'], rid + ':native declared edition')
  require(c['code_license'] == (None if rid == '23385145' else 'MIT'), rid + ':correct mixed licensing')
  reviews = promotion['reviews']
  if rid == '23385145':
   require(type(reviews) is list and literal(reviews, promotion['whole_original_custom_family_verdicts']), '118 original review list retained')
   entries = [(x['actual_verdict_path'], x['sha256'], x['whole_literal_original_object']) for x in reviews]
  else:
   require(type(reviews) is dict and list(reviews) == ['scope', 'analytic', 'adversarial'], '119 original keyed review object retained')
   entries = [(x['verdict_path'], x['verdict_sha256'], x['whole_original_custom_verdict']) for x in reviews.values()]
  require(len(entries) == 3, rid + ':all three whole custom verdicts')
  for path, wanted, obj in entries:
   require(bind(path)['sha256'] == wanted and literal(load(path), obj), rid + ':whole exact custom verdict:' + path)
   family_count += 1
  root = S / 'candidate-a/public/research' / c['slug']
  files = {q.name: q.read_bytes() for q in root.iterdir() if q.is_file()}
  for x in rr['all_assets_in_original_order']:
   api = x['original_api_file_object']
   body = files[api['key']]
   expected_sha = x['sha256'] if rid == '23385145' else x['SHA256']
   require(len(body) == api['size'] == x['bytes'] and digest(body) == expected_sha and hashlib.md5(body).hexdigest() == api['checksum'][4:], rid + ':entire original asset:' + api['key'])
  if rid == '22983513':
   checksums = {line.split()[-1]: line.split()[0] for line in files['SHA256SUMS.txt'].decode().splitlines()}
   require(len(files['SHA256SUMS.txt']) == 170 and checksums == {name: digest(files[name]) for name in ('paper.pdf', 'source-and-verification.zip')}, '119 original170B checksum covers exact PDF and ZIP')
  records.append(verify_article(files['index.html'].decode(), o, files))
 index = (S / 'candidate-a/public/research/index.html').read_text()
 sitemap = (S / 'candidate-a/public/research/sitemap.xml').read_text()
 verify_overlays(index, sitemap, source)
 baseline = load(S / 'FRESH_BASELINE.json')
 public = Path(baseline['public_root'])
 require(len(baseline['public_files']) == 576 and len(baseline['installed_core_files']) == 18, '576 baseline files and18 core files')
 require({str(q.relative_to(public)) for q in public.rglob('*') if q.is_file()} == {x['path'] for x in baseline['public_files']}, 'unchanged production namespace')
 for x in baseline['public_files']:
  require(bind(public / x['path']) == {k: x[k] for k in ('bytes', 'sha256')}, 'unchanged production file:' + x['path'])
 for x in baseline['installed_core_files']:
  require(bind(x['path']) == {k: x[k] for k in ('bytes', 'sha256')}, 'unchanged core:' + x['path'])
 require(len({x['path'] for x in baseline['public_files']} | set(expected)) == 585, 'hypothetical union585 with exactly nine new leaves')
 require({str(q.relative_to(FIVE)) for q in FIVE.rglob('*') if q.is_file()} == set(initial['whole_frozen_five_namespace']), 'whole frozen-five namespace unchanged')
 faults = []
 def reject(label, action):
  checkpoint = len(CHECKS)
  try:
   action()
  except ValueError as exc:
   faults.append({'fault': label, 'rejected_by': str(exc)})
  else:
   raise ValueError('accepted independent fault:' + label)
  del CHECKS[checkpoint:]
 o = source['records']['22983513']
 root = S / 'candidate-a/public/research/strict-dirichlet-gap'
 files = {q.name: q.read_bytes() for q in root.iterdir()}
 raw = files['index.html'].decode()
 reject('new119_reader_rebound_to_existing_ZIP', lambda: verify_article(raw.replace('src="paper.pdf"', 'src="source-and-verification.zip"', 1), o, files))
 reject('new119_abstract_heading_hidden_by_inert', lambda: verify_article(raw.replace('<section id="abstract">', '<section id="abstract" inert>', 1), o, files))
 reject('new119_full_threshold_quantifier_narrowed', lambda: verify_article(raw.replace('for every real z &gt; E₁', 'for integer z &gt; E₁', 1), o, files))
 row1, row2 = re.findall(r'<li>.*?</li>', index, re.S)[-2:]
 swapped = index.replace(row1, 'AUDIT_ROW_TEMP', 1).replace(row2, row1, 1).replace('AUDIT_ROW_TEMP', row2, 1)
 reject('new_index_new_article_rows_swapped_against_ItemList', lambda: verify_overlays(swapped, sitemap, source))
 for x in initial['all_input_files']:
  require(bind(x['path']) == {k: x[k] for k in ('bytes', 'sha256')}, 'final unchanged custody:' + x['path'])
 return {'scope_specific_result': 'Independent sealed-two integration custody and full-copy checks support later root adoption; no substantive integration defect found in this bounded audit.', 'checks': len(CHECKS), 'source_original_bindings': 356, 'total_unchanged_input_bindings': len(initial['all_input_files']), 'stage_payloads': 99, 'helper_bodies': 11, 'paired_outputs_each': 11, 'record_results': records, 'whole_literal_custom_science_verdicts': family_count, 'production_files_unchanged': 576, 'core_files_unchanged': 18, 'whole_frozen_five_files_unchanged': len(initial['whole_frozen_five_namespace']), 'hypothetical_union': 585, 'index_entries': 85, 'sitemap_locations': 86, 'independent_new_faults': faults, 'project_imports': 0, 'source_scientific_or_old_campaign_execution': 0, 'network_calls': 0, 'file_writes': 0, 'publication_authority': False, 'browser_or_live_checks_claimed': False, 'AA': None, 'canonical_assignment': None}

if __name__ == '__main__':
 print(json.dumps(run(), indent=2, ensure_ascii=False))
