"""Private factual page builder; stdlib only, no project-source execution."""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
import datetime, hashlib, json, re, shutil

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
L = P / 'verification/thompson-cstar-editorial-sol-20261117'
S = P / 'papers/23204212/sources'
D = L / 'private-page'
CSS = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research/research.css')
REVIEW = P / 'papers/23204212/reviews/root-continuation-20261117/ROOT_REVIEW.md'
CLEARANCE = P / 'verification/root-clearance-23204212-20261117.json'
TEX = S / 'archives/02-thompson-cstar-source.zip.extracted/main.tex'
sha = lambda b: hashlib.sha256(b).hexdigest()
pins = {
    str(REVIEW): '71136fd6de5610566ccffa7142a2ecabac093e33bad245e06eb7a3d456d85501',
    str(CLEARANCE): 'cf26226d4c236473c5cb75ede27c50f77e486761df16a624d39cf26abdbb797c',
    str(TEX): '5a95378741e1a371056251df4d6a492c16169d349ecc02ddb1b0d3ecd791fe92',
    str(CSS): 'f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a',
}
assert not D.exists() and not (L / 'MODEL.json').exists()
for path, expected in pins.items():
    assert sha(Path(path).read_bytes()) == expected, ('input pin', path)
clearance = json.loads(CLEARANCE.read_text())
assert clearance['prepare_factual_private_page_authorized'] is True
assert clearance['publication_or_AA_or_redirect_certificate'] is False
api = json.loads((S / 'native-metadata/record-api.json').read_text())
md = api['metadata']
assert 'version' not in md and md['publication_date'] == '2026-10-06'
assert api['created'] == '2026-10-07T05:35:37.608378+00:00'
assert api['doi'] == '10.5281/zenodo.23204212'
source_metadata = json.loads((S / 'SOURCE_METADATA.json').read_text())
assert source_metadata['native_API_version_present'] is False
assert source_metadata['host_display_edition_labels'] == ['v1']
tex = TEX.read_text()
abstract_tex = re.search(r'\\begin\{abstract\}\s*(.*?)\s*\\end\{abstract\}', tex, re.S).group(1)
replacements = [('$\\Aut(F)$', 'Aut(F)'), ('$\\Comm(F)$', 'Comm(F)'), ('$F$', 'F'), ('$T$', 'T')]
abstract = abstract_tex
for old, new in replacements:
    abstract = abstract.replace(old, new)
abstract = ' '.join(abstract.split())
assert '$' not in abstract and '\\' not in abstract and abstract.endswith('same dependency on its validity.')
title = md['title']
doi = api['doi']
doi_url = 'https://doi.org/' + doi
record_url = 'https://zenodo.org/records/23204212'
orcid = 'https://orcid.org/0009-0001-9320-500X'
assert md['creators'] == [{'name': 'Kriebel, Alec', 'affiliation': None, 'orcid': '0009-0001-9320-500X'}]
native = [
    ('thompson-cstar-verification.zip', 50534, 'ec84a7112daaf322d094a2d8cff44d203fa722e7f431ce868d7b7c497b63157e', '628d9912c3f0c7ada14b6985eb948d36', 'application/zip'),
    ('thompson-cstar-source.zip', 7516, 'bee0a8503a8f6706a02e3cad69680c8057a39f361b9b7c622c297fac2217b3aa', 'e5a3d079a2d5bffee8327e9ba7c1e188', 'application/zip'),
    ('paper.pdf', 56917, '527ac7feb6f2c889998559122296dd8caab2def0cf7aeac00f79c1f8b0c8a978', 'd47f4c2acb85921e377cc69027d64fec', 'application/pdf'),
]
assert [f['key'] for f in api['files']] == [r[0] for r in native]
assets = []
for ordinal, (name, size, expected_sha, expected_md5, mime) in enumerate(native, 1):
    b = (S / 'zenodo-files' / name).read_bytes()
    f = api['files'][ordinal - 1]
    native_url = 'https://zenodo.org/api/records/23204212/files/' + name + '/content'
    assert (len(b), sha(b), hashlib.md5(b).hexdigest()) == (size, expected_sha, expected_md5)
    assert (f['size'], f['checksum'], f['links']['self']) == (size, 'md5:' + expected_md5, native_url)
    assets.append({'ordinal': ordinal, 'native_filename': name, 'local_filename': name, 'bytes': size, 'sha256': expected_sha, 'md5': expected_md5, 'encoding_format': mime, 'native_url': native_url})
upstream = 'https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Thompsons-group-F-is-nonamenable-September-23-2026/paper.pdf'
refs = [
    (upstream, "OpenAI, Thompson's group F is nonamenable (pinned written proof)"),
    ('https://doi.org/10.24033/asens.2361', 'Le Boudec and Matte Bon, Subgroup dynamics and C*-simplicity of groups of homeomorphisms (2018)'),
    ('https://doi.org/10.1007/s10240-017-0091-2', 'Breuillard, Kalantar, Kennedy and Ozawa, C*-simplicity and the unique trace property for discrete groups (2017)'),
    ('https://doi.org/10.5169/seals-87877', "Cannon, Floyd and Parry, Introductory notes on Richard Thompson's groups (1996)"),
    ('https://doi.org/10.1007/BF02698834', 'Brin, The chameleon groups of Richard J. Thompson: automorphisms and dynamics (1996)'),
    ('https://doi.org/10.2140/gt.2008.12.1701', "Burillo, Cleary and Röver, Commensurations and subgroups of finite index of Thompson's group F (2008)"),
    ('https://doi.org/10.1016/j.jfa.2017.02.003', 'Haagerup and Olesen, Non-inner amenability of the Thompson groups T and V (2017)'),
]
description = 'An attributed consequence for the reduced group C*-algebras of F, T, full Aut(F) and full Comm(F), retaining the dependency on OpenAI’s pinned nonamenability proof and crediting the established simplicity and trace theorems.'
null_fields = ['actual_canonical', 'base_url', 'production_url', 'page_publication_date', 'AA', 'legacy_route', 'legacy_redirect', 'follow_up']
model = {
    'schema': 'private-factual-editorial-model-v1', 'record_id': '23204212', 'inventory_row': 192,
    'title': title, 'author': {'name': 'Alec Kriebel', 'orcid': orcid, 'affiliation': None},
    'doi': doi, 'doi_url': doi_url, 'native_record_url': record_url,
    'native_publication_date': md['publication_date'], 'native_record_created': api['created'],
    'native_record_updated': api['updated'], 'native_version': None, 'native_version_field_present': False,
    'host_edition_label': 'v1', 'host_edition_qualification': 'Zenodo display label only; no author-supplied API version and no invented semantic version',
    'proposed_slug': 'thompson-reduced-cstar-consequences',
    'slug_collision_assessment': 'not performed; authorized website reading is limited to the shared CSS; root must check before assigning a route',
    'private_only': True, 'publication_authority': False, 'robots': 'noindex,nofollow',
    'original_abstract_tex': abstract_tex, 'original_abstract_normalized': abstract,
    'abstract_rendering_replacements': [{'from': old, 'to': new} for old, new in replacements],
    'abstract_whitespace_normalization': 'collapse whitespace to single spaces; no prose or punctuation changes',
    'abstract_normalized_sha256': sha(abstract.encode()), 'source_tex_sha256': pins[str(TEX)],
    'native_assets_in_original_order': assets,
    'upstream_written_proof': upstream, 'upstream_commit': 'adc7f1241b42e322a6451854ab7e4b4c146bf78a',
    'dependency': 'All conclusions using the new nonamenability input retain exactly its validity dependency; T unique trace was already unconditional.',
    'scope': 'Discrete reduced group C*-algebras of standard F, T, full abstract Aut(F), full abstract Comm(F); each countable subgroup of Homeo(S¹) containing the specified standard circle action of F.',
    'limitations': ['No full-group-C*-algebra conclusion', 'No abstract group simplicity conclusion', 'No arbitrary abstract-F containment substitute for the standard circle action', 'No independent nonamenability proof, new simplicity criterion, priority claim, human-referee or fresh formal certificate'],
    'rights': {'note_and_documentation': 'CC-BY-4.0', 'original_finite_check_code': 'MIT', 'third_party_material': 'retains its own rights'},
    'input_pins': pins, 'root_clearance_status': clearance['status'], 'writer_completion_percent': 100,
}
model.update({key: None for key in null_fields})
scholarly = {
    '@context': 'https://schema.org', '@type': 'ScholarlyArticle', 'name': title, 'headline': title,
    'author': {'@type': 'Person', 'name': 'Alec Kriebel', '@id': orcid},
    'identifier': doi_url, 'url': record_url, 'datePublished': md['publication_date'],
    'dateCreated': api['created'], 'inLanguage': 'en', 'abstract': abstract,
    'description': description, 'keywords': md['keywords'],
    'license': 'https://creativecommons.org/licenses/by/4.0/',
    'isAccessibleForFree': True, 'creativeWorkStatus': 'Preprint; unrefereed',
    'citation': [url for url, _ in refs],
    'encoding': [{'@type': 'MediaObject', 'name': a['native_filename'], 'contentUrl': a['native_url'], 'encodingFormat': a['encoding_format'], 'contentSize': str(a['bytes']) + ' bytes'} for a in assets],
}
bib = '@misc{kriebel2026thompsonreduced,\n  author = {Kriebel, Alec},\n  title = {' + title + '},\n  year = {2026},\n  month = oct,\n  publisher = {Zenodo},\n  doi = {' + doi + '},\n  url = {' + doi_url + '},\n  note = {Preprint dated October 6, 2026; Zenodo record created October 7, 2026},\n  orcid = {0009-0001-9320-500X}\n}\n'
e = escape
asset_labels = ['Verification and documentation archive', 'Manuscript source archive', 'Original manuscript PDF']
asset_list = '\n'.join('<li><a href="' + e(a['local_filename']) + '" download>' + e(label) + ' (' + e(a['native_filename']) + ')</a> · <a href="' + e(a['native_url']) + '">Zenodo original</a></li>' for a, label in zip(assets, asset_labels))
ref_list = '\n'.join('<li><a href="' + e(url) + '">' + e(label) + '</a></li>' for url, label in refs)
structured_json = json.dumps(scholarly, ensure_ascii=False).replace('</', '<' + chr(92) + '/')
page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{e(title)} | Alec Kriebel</title>
<meta name="description" content="{e(description)}">
<meta name="author" content="Alec Kriebel">
<meta name="citation_title" content="{e(title)}">
<meta name="citation_author" content="Alec Kriebel">
<meta name="citation_author_orcid" content="{orcid}">
<meta name="citation_publication_date" content="2026/10/06">
<meta name="citation_doi" content="{doi}">
<meta name="citation_pdf_url" content="{e(assets[2]['native_url'])}">
<meta name="citation_abstract" content="{e(abstract)}">
<meta name="DC.identifier" content="{doi_url}">
<link rel="stylesheet" href="research.css">
<script type="application/ld+json">{structured_json}</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to article</a>
<header><p class="site-title"><a href="/">Alec Kriebel</a></p><nav aria-label="Main"><a href="/research/">Research</a></nav></header>
<main id="main"><article>
<h1>{e(title)}</h1>
<p class="entry-meta"><a href="{orcid}">Alec Kriebel</a> · <time datetime="2026-10-06">6 October 2026</time> · Unrefereed preprint</p>
<p class="entry-meta">Zenodo record created 7 October 2026. Its displayed “v1” is a host edition label; the native API supplies no author version.</p>
<p><a href="#manuscript">Read the manuscript</a> · <a href="{doi_url}">DOI: {doi}</a> · <a href="citation.bib" download>BibTeX</a></p>

<section aria-labelledby="attribution"><h2 id="attribution">An attributed consequence</h2>
<p>This note applies <a href="{e(upstream)}">OpenAI’s pinned written proof that Thompson’s group F is nonamenable</a> to the published simplicity reductions of <a href="https://doi.org/10.24033/asens.2361">Adrien Le Boudec and Nicolás Matte Bon</a> and the trace theorem of <a href="https://doi.org/10.1007/s10240-017-0091-2">Emmanuel Breuillard, Mehrdad Kalantar, Matthew Kennedy and Narutaka Ozawa</a>. The resulting statements are consequences of those inputs. The note collects their hypotheses and attribution; it supplies no independent proof of nonamenability or new simplicity criterion.</p>
<p>The full automorphism and commensurator groups use the line realizations studied by <a href="https://doi.org/10.1007/BF02698834">Matthew Brin</a> and <a href="https://doi.org/10.2140/gt.2008.12.1701">José Burillo, Sean Cleary and Claas Röver</a>. <strong>Every conclusion using the new nonamenability input retains exactly the same dependency on its validity.</strong> No first-priority claim is made.</p>
<p><strong>The unique-trace property for T was already known unconditionally.</strong> <a href="https://doi.org/10.1016/j.jfa.2017.02.003">Haagerup and Olesen</a> record this prior result and credit Dudko and Medynets.</p></section>

<section aria-labelledby="meaning"><h2 id="meaning">What the consequence says</h2>
<p>A reduced group C*-algebra represents a discrete group by translation operators on square-summable functions on the group, then takes their operator-norm closure. Calling this algebra <em>simple</em> means that it has no nonzero proper closed two-sided ideals. Its canonical trace reads the coefficient of the identity element; a unique tracial state means that every normalized positive trace agrees with it.</p>
<p>Using the pinned nonamenability theorem, each of the following reduced algebras is simple and has its canonical trace as its unique tracial state:</p>
<ul>
<li>C*<sub>r</sub>(F), for the standard Thompson group F;</li>
<li>C*<sub>r</sub>(T), for Thompson’s circle group T;</li>
<li>C*<sub>r</sub>(Aut(F)), for the full abstract automorphism group of F;</li>
<li>C*<sub>r</sub>(Comm(F)), for the full abstract commensurator of F.</li>
</ul>
<p>All groups here carry the discrete topology. The full Aut(F) and Comm(F) include the orientation-reversing elements in their line realizations. Comm(F) identifies isomorphisms between finite-index subgroups when they agree after restriction to a further finite-index subgroup.</p>
<p>These groups are countable. F and T have finite dyadic descriptions. An automorphism of the two-generated F is determined by two images. Finite-index subgroups of F form a countable collection and are finitely generated, so the isomorphisms defining Comm(F), and hence their equivalence classes, also form a countable set.</p></section>

<section aria-labelledby="circle"><h2 id="circle">The specified circle action matters</h2>
<p>Standard F consists of increasing piecewise-linear maps of [0,1] with finitely many dyadic breakpoints and slopes that are powers of two. It fixes the endpoints; identifying them gives its standard action on the circle. T is the corresponding orientation-preserving dyadic piecewise-linear circle group preserving the dyadic points.</p>
<p>The same consequence holds for every <strong>countable subgroup G of Homeo(S¹) containing this specified standard circle action of F</strong>: its reduced algebra C*<sub>r</sub>(G) is simple and has a unique canonical trace. Containment of an arbitrary abstract copy of F in an unrelated action does not supply this hypothesis. This action-level consequence is inherited from Le Boudec and Matte Bon.</p></section>

<section aria-labelledby="limits"><h2 id="limits">Scope and limits</h2>
<p>The assertions concern reduced group algebras C*<sub>r</sub>(G). They do not assert simplicity of the full group algebra C*(G), or simplicity of the group as an abstract group. Simplicity and unique trace are distinct properties for general C*-algebras; the implication used here is the discrete-group theorem.</p>
<p>The upstream nonamenability proof is attributed entirely to OpenAI. A material defect in that input would remove the unconditional status of the conclusions that use it. The established conditional reductions and the previously known unique trace for T would remain.</p></section>

<section aria-labelledby="abstract"><h2 id="abstract">Original manuscript abstract</h2>
<p id="original-abstract">{e(abstract)}</p></section>

<section aria-labelledby="materials"><h2 id="materials">Original files and citation</h2>
<p>The native files are provided below in their original record order. The PDF and both archives are unchanged copies.</p>
<ol>{asset_list}</ol>
<p><a href="citation.bib" download>Download BibTeX citation</a> · <a href="{record_url}">Zenodo record</a></p>
<p>The original note and documentation are licensed <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. The original finite-check code is MIT licensed, as stated in LICENSE_CODE.txt inside the verification archive. Third-party sources retain their own rights.</p></section>

<section aria-labelledby="manuscript"><h2 id="manuscript">Read the manuscript</h2>
<p><a href="paper.pdf">Open the original PDF</a> · <a href="paper.pdf" download>Download the original PDF</a> · <a href="{e(assets[2]['native_url'])}">PDF at Zenodo</a></p>
<iframe class="paper-pdf" src="paper.pdf" title="Original manuscript: reduced C*-algebras of the Thompson family" loading="lazy"><a href="paper.pdf">Read the PDF manuscript</a></iframe></section>

<section aria-labelledby="references"><h2 id="references">Sources and credit</h2>
<ul>{ref_list}</ul></section>

<section aria-labelledby="disclosure"><h2 id="disclosure">Disclosure and contributions</h2>
<p>AI tools were used extensively in research, source inspection, drafting and verification. This preprint has not undergone conventional human peer review or refereeing. No formalization of this C*-algebra consequence note or fresh formal proof certificate is claimed.</p>
<p>Substantial contributions to the mathematics or exposition are welcome. Any collaboration and authorship should reflect the work actually contributed.</p></section>
</article></main>
<footer><p><a href="/research/">Research</a> · <a href="{orcid}">ORCID</a></p></footer>
</body></html>
'''

class Inspect(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.metas = {}; self.scripts = []; self.in_ld = False
        self.abstract_depth = 0; self.abstract_text = []; self.links = []; self.iframes = []; self.h1 = 0; self.canonical = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta' and 'name' in a: self.metas[a['name']] = a.get('content')
        if tag == 'h1': self.h1 += 1
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical.append(a)
        if tag == 'script' and a.get('type') == 'application/ld+json': self.in_ld = True; self.scripts.append('')
        if a.get('id') == 'original-abstract': self.abstract_depth = 1
        elif self.abstract_depth: self.abstract_depth += 1
        if tag in ('a', 'link') and 'href' in a: self.links.append(a['href'])
        if tag == 'iframe': self.iframes.append(a)
    def handle_endtag(self, tag):
        if tag == 'script': self.in_ld = False
        if self.abstract_depth: self.abstract_depth -= 1
    def handle_data(self, data):
        if self.in_ld: self.scripts[-1] += data
        if self.abstract_depth: self.abstract_text.append(data)

assert '\\begin' not in page and 'citation_version' not in page
parsed = Inspect(); parsed.feed(page); parsed.close()
assert parsed.h1 == 1 and parsed.canonical == []
assert parsed.metas['robots'] == 'noindex,nofollow'
assert parsed.metas['citation_abstract'] == abstract == ''.join(parsed.abstract_text)
assert parsed.metas['citation_doi'] == doi and parsed.metas['citation_author_orcid'] == orcid
assert parsed.metas['citation_pdf_url'] == assets[2]['native_url']
assert len(parsed.scripts) == 1 and json.loads(parsed.scripts[0]) == scholarly and 'version' not in scholarly
assert [a['name'] for a in scholarly['encoding']] == [r[0] for r in native]
assert len(parsed.iframes) == 1 and parsed.iframes[0]['src'] == 'paper.pdf' and parsed.iframes[0]['title']
assert all(model[key] is None for key in null_fields)
D.mkdir()
for a in assets:
    shutil.copy2(S / 'zenodo-files' / a['native_filename'], D / a['local_filename'])
    assert sha((D / a['local_filename']).read_bytes()) == a['sha256']
shutil.copy2(CSS, D / 'research.css')
assert sha((D / 'research.css').read_bytes()) == pins[str(CSS)]
(D / 'citation.bib').write_text(bib)
(D / 'index.html').write_text(page)
for link in parsed.links:
    if not link.startswith(('https://', '/', '#')):
        assert (D / link).is_file(), ('missing local link', link)
(L / 'MODEL.json').write_text(json.dumps(model, ensure_ascii=False, indent=2) + '\n')
receipt = {
    'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'private_only': True, 'publication_authority': False, 'writer_completion_percent': 100,
    'input_pins': pins, 'page_sha256': sha((D / 'index.html').read_bytes()),
    'model_sha256': sha((L / 'MODEL.json').read_bytes()),
    'bib_sha256': sha((D / 'citation.bib').read_bytes()), 'assets': assets,
    'checks': {'abstract_visible_meta_JSONLD_exact': True, 'single_ScholarlyArticle': True, 'no_API_version_invented': True, 'native_order_and_bytes_exact': True, 'CSS_exact': True, 'one_h1': True, 'local_links_exist': True, 'PDF_iframe_open_download_links': True, 'private_robots_and_all_null_publication_fields': True},
    'limits': ['Private writer only; no publication, AA, redirect or live-site certificate', 'No route collision search or live rendering; website input is CSS only', 'No scientific programs, formal build, project imports, network, Git, tracker or source mutation'],
}
(L / 'BUILD_RECEIPT.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'status': 'PRIVATE_EDITORIAL_BUILT', 'writer_completion_percent': 100, 'publication_authority': False, 'native_asset_count': 3, 'page_sha256': receipt['page_sha256'], 'model_sha256': receipt['model_sha256']}))
