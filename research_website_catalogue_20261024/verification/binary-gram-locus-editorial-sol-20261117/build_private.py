"""Private editorial builder only; source TeX is inert text, no scientific execution."""
from pathlib import Path
from datetime import datetime, timezone
from html import escape
from html.parser import HTMLParser
import hashlib,json,re,shutil

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
A=P/'verification/binary-gram-locus-editorial-sol-20261117'
S=P/'papers/23318851/sources'
D=A/'private-page'
CSS=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research/research.css')
SLUG='binary-gram-locus-polynomial-obstruction'
DOI='10.5281/zenodo.23318851'
DOI_URL='https://doi.org/'+DOI
RECORD='https://zenodo.org/records/23318851'
ORCID='https://orcid.org/0009-0001-9320-500X'
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(v):return (json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode()
def h(v):return escape(str(v),quote=True)

assert not D.exists() and not (A/'MODEL.json').exists()
approval=P/'verification/root-clearance-23318851-20261117.json'
review=P/'papers/23318851/reviews/root-continuation-20261117/ROOT_REVIEW.md'
assert sha(approval.read_bytes())=='ef479bc20bdcd8d789736abd17b9999184fee354b3a15d41bc53a6c872b807d9'
assert sha(review.read_bytes())=='d6d6efca566214ccb39080bd7160c3437ede74c026150bc74e149d6878867d5f'
clearance=json.loads(approval.read_text())
assert clearance['prepare_factual_private_page_authorized'] is True
assert clearance['publication_or_AA_or_redirect_certificate'] is False
api=json.loads((S/'native-metadata/record-api.json').read_text())
meta=api['metadata'];title=meta['title']
assert meta['version']=='1.0.0' and meta['publication_date']=='2026-10-12'
assert meta['license']['id']=='cc-by-4.0' and meta['doi']==DOI
tex=(S/'archives/02-gram_locus_support.zip.extracted/gram_locus_note.tex').read_text()
assert sha(tex.encode())=='f6ddf7f510df8e7000a627a79be32413c53476104f87336b49dd0ded1983701a'
raw=tex.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0].strip()
replacements=[('\\(n\\geq3\\)','n ≥ 3'),('\\(n\\geq4\\)','n ≥ 4'),('\\(n\\)','n')]
abstract=raw
for old,new in replacements:abstract=abstract.replace(old,new)
abstract=re.sub(r'\s+',' ',abstract).strip()
assert '\\' not in abstract and abstract.endswith('certifying mutual independence.')
summary='For real binary tensors in the closed Frobenius unit ball, no single additional determinant-polynomial inequality defines the Gram locus when n ≥ 3.'
expected=[('gram_locus_note.pdf',74051,'ac0839eae1d0e83e0c47d3c840968363ce9271c83cc9ee88156197601b4d0018','application/pdf'),
          ('gram_locus_support.zip',147400,'4df495ac35094dfbacaf4453bde1a71ecae80de23aa50111b3eb7664c2f453e2','application/zip')]
assert [r['key'] for r in api['files']]==[r[0] for r in expected]
assets=[]
for i,(name,size,pin,mime) in enumerate(expected,1):
    b=(S/'zenodo-files'/name).read_bytes();native=api['files'][i-1]
    assert len(b)==size==native['size'] and sha(b)==pin
    assert 'md5:'+hashlib.md5(b).hexdigest()==native['checksum']
    assets.append({'native_order':i,'native_filename':name,'local_filename':name,'bytes':size,'SHA256':pin,
                   'media_type':mime,'native_content_url':native['links']['self']})
web_public=CSS.parent.parent
collision_paths=[web_public/'research'/SLUG,web_public/'blog'/SLUG,web_public/SLUG]
assert not any(p.exists() for p in collision_paths)
css_before=CSS.read_bytes()
before=json.loads((A/'CUSTODY_BEFORE.json').read_text())
css_pin=next(r for r in before['specific_inputs'] if r['path']==str(CSS))
assert sha(css_before)==css_pin['SHA256']
citations=['https://doi.org/10.1016/j.laa.2018.01.019','https://doi.org/10.4171/OWR/2017/20',
    'https://doi.org/10.1103/PhysRevLett.90.107902','https://arxiv.org/abs/quant-ph/0301014v1',
    'https://doi.org/10.1137/16M110770X','https://arxiv.org/abs/1108.2992v1','https://doi.org/10.5281/zenodo.23111048']
ld={'@context':'https://schema.org','@type':'ScholarlyArticle','name':title,'headline':title,
    'author':{'@type':'Person','name':'Alec Kriebel','sameAs':ORCID,'identifier':ORCID},
    'identifier':{'@type':'PropertyValue','propertyID':'DOI','value':DOI},'url':DOI_URL,
    'datePublished':'2026-10-12','version':'1.0.0','inLanguage':'en','isAccessibleForFree':True,
    'description':summary,'abstract':abstract,'keywords':meta['keywords'],
    'license':'https://creativecommons.org/licenses/by/4.0/','publisher':{'@type':'Organization','name':'Zenodo'},
    'sameAs':[RECORD],'citation':citations,
    'encoding':[{'@type':'MediaObject','name':r['native_filename'],'encodingFormat':r['media_type'],
                 'contentSize':str(r['bytes'])+' bytes','contentUrl':r['native_content_url']} for r in assets]}
model={'private_only':True,'publication_authority':False,'proposed_slug':SLUG,
    'proposed_path':'/research/'+SLUG+'/','actual_canonical':None,'base_url':None,'production_url':None,
    'page_publication_date':None,'AA':None,'legacy_redirect':None,'robots':'noindex, nofollow',
    'title':title,'author':{'name':'Alec Kriebel','ORCID':ORCID},'DOI':DOI,'native_record':RECORD,
    'native_version':'1.0.0','native_publication_date':'2026-10-12','follow_up':None,
    'abstract':{'source_tex':raw,'normalized_full_text':abstract,
        'literal_rendering_replacements':[{'from':a,'to':b} for a,b in replacements],
        'whitespace_rule':'Collapse each whitespace run to one space, then strip ends; no prose edits',
        'normalized_SHA256':sha(abstract.encode())},
    'native_assets_in_original_order':assets,'generated_citation_file':'citation.bib',
    'stylesheet':{'private_reference':'research.css','source':str(CSS),'SHA256':sha(css_before),'changed':False},
    'SEO':{'title':title+' | Alec Kriebel','description':summary,'canonical':None,'structured_data':ld},
    'rights':{'license':'CC-BY-4.0','scope':'Author’s original text, code, notes and results; third-party material retains its rights'},
    'collision_scope':'No matching proposed slug in current public filename scan and three direct local path checks; no live or historical determination'}
ld_text=json.dumps(ld,indent=2,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
page=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{h(title)} | Alec Kriebel</title>
<meta name="robots" content="noindex, nofollow">
<meta name="description" content="{h(summary)}">
<meta property="og:type" content="article">
<meta property="og:title" content="{h(title)}">
<meta property="og:description" content="{h(summary)}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{h(title)}">
<meta name="twitter:description" content="{h(summary)}">
<meta name="citation_title" content="{h(title)}">
<meta name="citation_author" content="Alec Kriebel">
<meta name="citation_author_orcid" content="{ORCID}">
<meta name="citation_author_institution" content="Independent researcher">
<meta name="citation_publication_date" content="2026/10/12">
<meta name="citation_date" content="2026/10/12">
<meta name="citation_version" content="1.0.0">
<meta name="citation_doi" content="{DOI}">
<meta name="citation_pdf_url" content="{assets[0]['native_content_url']}">
<meta name="citation_language" content="en">
<meta name="citation_abstract" content="{h(abstract)}">
<link rel="stylesheet" href="research.css">
<script type="application/ld+json">{ld_text}</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to the article</a>
<header>
<p class="site-title"><a href="/">Alec Kriebel</a></p>
<nav aria-label="Site"><a href="/research/">Research</a></nav>
</header>
<main id="main">
<article>
<p class="entry-meta">Private editorial draft</p>
<h1>{h(title)}</h1>
<p class="entry-meta"><a href="{ORCID}">Alec Kriebel</a> · Independent researcher<br>Version 1.0.0 · 12 October 2026 · Unrefereed research note</p>
<p>A binary tensor is an array with two positions along each of its directions. This note considers real tensors of Frobenius norm at most one. It studies the determinants of their one-mode Gram matrices and rules out describing all attainable tuples by one additional polynomial nonnegativity condition when there are at least three factors.</p>
<p><a href="gram_locus_note.pdf">Open the original PDF</a> · <a href="gram_locus_note.pdf" download="gram_locus_note.pdf">Download PDF</a> · <a href="gram_locus_support.zip" download="gram_locus_support.zip">Source and support archive</a> · <a href="citation.bib" download="citation.bib">BibTeX</a> · <a href="{RECORD}">Zenodo record</a></p>
<p>DOI: <a href="{DOI_URL}">{DOI}</a></p>

<section aria-labelledby="credit-heading">
<h2 id="credit-heading">Overlap and earlier work</h2>
<p><strong>Alper Ferudun’s <a href="https://doi.org/10.5281/zenodo.23111048">2 October 2026 unrefereed preprint</a> gives an overlapping, stronger theorem on the positive interior of the hull for every n ≥ 3.</strong> It is an earlier formal preprint than this 12 October note, and its multiplicity argument overlaps with the mechanism used here. This page makes no exclusive-firstness claim.</p>
<p>A theorem-bearing proof was submitted in <a href="https://github.com/AlecKriebel/Math/pull/170">GitHub PR170</a>, created on 30 September 2026. The formal preprint remains dated 12 October 2026. Those records do not certify mutual independence of authorship, literal simultaneity or historical public visibility; current public visibility does not independently archive what was public on the earlier date.</p>
<p>The marginal polygon inequalities and real constructions come from <a href="https://doi.org/10.1103/PhysRevLett.90.107902">Higuchi, Sudbery and Szulc</a>, <a href="https://arxiv.org/abs/quant-ph/0301014v1">Bravyi</a>, and <a href="https://doi.org/10.1137/16M110770X">Domanov, Stegeman and De Lathauwer</a>. <a href="https://arxiv.org/abs/1108.2992v1">Sinn</a> had given an earlier general boundary/interior obstruction. <a href="https://doi.org/10.1016/j.laa.2018.01.019">Seigal</a> identified the convex hull and proposed the determinant-polynomial condition addressed here. The note does not claim a new general obstruction principle.</p>
</section>

<section aria-labelledby="result-heading">
<h2 id="result-heading">The result and its limits</h2>
<p>Let d<sub>i</sub> be the determinant of the two-row mode-i flattening’s Gram matrix. The tensors are real and range over the closed Frobenius unit ball, including zero determinants. Write G<sub>n</sub> for their determinant tuples and C<sub>n</sub> = [0, 1/4]<sup>n</sup>.</p>
<p>For every fixed n ≥ 3, no real polynomial P in those determinant coordinates satisfies</p>
<p class="equation">G<sub>n</sub> = {{d ∈ C<sub>n</sub> : P(d) ≥ 0}}.</p>
<p>The same conclusion holds when the domain is the known convex hull H<sub>n</sub>, obtained by also imposing d<sub>i</sub> ≤ ∑<sub>j ≠ i</sub>d<sub>j</sub>. The assertion covers arbitrary polynomial degrees and real coefficients.</p>
<ul>
<li>For n = 1, the Gram locus is {{0}}. For n = 2, it is the diagonal segment; the single condition −(d<sub>1</sub> − d<sub>2</sub>)<sup>2</sup> ≥ 0 works inside the cube.</li>
<li>The higher-factor proof uses exact faces where added determinants are zero. It does not establish Ferudun’s stronger all-positive higher-factor result.</li>
<li>The conclusion concerns one additional weak inequality in determinant coordinates. It does not rule out several conditions, Boolean combinations or descriptions with auxiliary variables.</li>
</ul>
</section>

<section aria-labelledby="idea-heading">
<h2 id="idea-heading">Why one condition fails</h2>
<p>For three factors, the smaller Gram eigenvalues obey triangle inequalities, and an explicit real tensor realizes every admissible triple. In determinant coordinates, a polynomial has a reflection symmetry coming from the two roots of the same quadratic equation for each eigenvalue.</p>
<p>On a genuine boundary, a defining polynomial must change sign, so a boundary factor must occur an odd number of times. The reflection carries that same exact multiplicity to a surface inside the feasible region, where nonnegativity requires an even multiplicity. The contradiction rules out one defining polynomial. Exact zero-determinant slices then carry the obstruction to more factors.</p>
</section>

<section aria-labelledby="example-heading">
<h2 id="example-heading">A positive four-factor counterexample</h2>
<p>The manuscript also gives the rational tuple</p>
<p class="equation">d = (2401/10000, 81/625, 81/625, 1/10000).</p>
<p>Every coordinate is positive. The tuple lies strictly inside the cube and the convex hull, and it satisfies Seigal’s proposed condition Q<sub>1</sub> ≥ Q<sub>2</sub>. Nevertheless, it violates a necessary marginal polygon inequality and cannot arise from any real tensor of Frobenius norm at most one. Thus the four-factor counterexample is not confined to zero-determinant faces.</p>
</section>

<section aria-labelledby="abstract-heading">
<h2 id="abstract-heading">Original manuscript abstract</h2>
<p id="manuscript-abstract">{h(abstract)}</p>
</section>

<section aria-labelledby="paper-heading">
<h2 id="paper-heading">Read the unchanged manuscript</h2>
<p><a href="gram_locus_note.pdf">Open PDF</a> · <a href="gram_locus_note.pdf" download="gram_locus_note.pdf">Download PDF</a> · <a href="{assets[0]['native_content_url']}">Original PDF on Zenodo</a></p>
<iframe class="paper-pdf" src="gram_locus_note.pdf" title="{h(title)} — original PDF" loading="lazy"><p><a href="gram_locus_note.pdf">Read the original PDF</a>.</p></iframe>
<p><a href="gram_locus_support.zip" download="gram_locus_support.zip">Download source and support archive</a> · <a href="{assets[1]['native_content_url']}">Original archive on Zenodo</a></p>
</section>

<section aria-labelledby="citation-heading">
<h2 id="citation-heading">Citation and reuse</h2>
<p>Kriebel, Alec (2026). <em>{h(title)}</em>. Version 1.0.0. Zenodo. <a href="{DOI_URL}">{DOI}</a>. <a href="citation.bib" download="citation.bib">Download BibTeX</a>.</p>
<p>The manuscript and the author’s original text, code, notes and results in the support archive are shared under <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Cited third-party material retains its own rights.</p>
</section>

<section aria-labelledby="status-heading">
<h2 id="status-heading">Review status and contributions</h2>
<p>This work is unrefereed and has not undergone conventional human peer review. AI tools were used extensively in solving, drafting, source comparison, reproduction and adversarial verification. Alec Kriebel is responsible for the contents; formal proof certification is not claimed.</p>
<p>Substantial mathematical and expository contributions can support collaboration. Authorship and acknowledgments would reflect the actual intellectual and writing contributions.</p>
</section>
</article>
</main>
<footer><p><a href="/research/">Research</a> · <a href="{ORCID}">ORCID 0009-0001-9320-500X</a></p></footer>
</body>
</html>
'''
bib='''@misc{kriebel2026binarygramlocus,
  author = {Kriebel, Alec},
  title = {No single polynomial inequality defines a real binary Gram locus},
  year = {2026},
  month = oct,
  version = {1.0.0},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.23318851},
  url = {https://doi.org/10.5281/zenodo.23318851},
  note = {Version 1.0.0; unrefereed research note},
  license = {CC-BY-4.0}
}
'''
D.mkdir()
for r in assets:shutil.copy2(S/'zenodo-files'/r['native_filename'],D/r['local_filename'])
shutil.copy2(CSS,D/'research.css')
(D/'citation.bib').write_text(bib)
(D/'index.html').write_text(page)
(A/'MODEL.json').write_bytes(enc(model))
class Check(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.meta={};self.links=[];self.frames=[];self.canonical=[];self.abstract=[];self.ld=[];self.in_abs=False;self.in_ld=False;self.h1=0
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=='meta':self.meta[d.get('name',d.get('property',''))]=d.get('content','')
        if tag=='a':self.links.append(d.get('href',''))
        if tag=='iframe':self.frames.append(d)
        if tag=='h1':self.h1+=1
        if tag=='link' and d.get('rel')=='canonical':self.canonical.append(d)
        if tag=='p' and d.get('id')=='manuscript-abstract':self.in_abs=True
        if tag=='script' and d.get('type')=='application/ld+json':self.in_ld=True;self.ld.append('')
    def handle_endtag(self,tag):
        if tag=='p':self.in_abs=False
        if tag=='script':self.in_ld=False
    def handle_data(self,data):
        if self.in_abs:self.abstract.append(data)
        if self.in_ld:self.ld[-1]+=data
check=Check();check.feed(page);check.close()
assert check.h1==1 and check.meta['robots']=='noindex, nofollow' and not check.canonical
assert ''.join(check.abstract)==abstract and len(check.ld)==1 and json.loads(check.ld[0])==ld
assert page.count('"@type": "ScholarlyArticle"')==1
assert len(check.frames)==1 and check.frames[0]['src']==expected[0][0] and check.frames[0]['title']
assert check.meta['citation_doi']==DOI and check.meta['citation_author_orcid']==ORCID
assert check.meta['citation_pdf_url']==assets[0]['native_content_url'] and check.meta['citation_abstract']==abstract
for link in check.links:
    if link and not link.startswith(('http://','https://','/','#')):assert (D/link).is_file(),link
for r in assets:assert sha((D/r['local_filename']).read_bytes())==r['SHA256']
assert (D/'research.css').read_bytes()==css_before==CSS.read_bytes()
assert all(model[k] is None for k in ['actual_canonical','base_url','production_url','page_publication_date','AA','legacy_redirect','follow_up'])
receipt={'UTC':datetime.now(timezone.utc).isoformat(),'private_builder_attempts':1,'publication_authority':False,
    'root_clearance_SHA256':sha(approval.read_bytes()),'root_review_SHA256':sha(review.read_bytes()),
    'page_SHA256':sha((D/'index.html').read_bytes()),'model_SHA256':sha((A/'MODEL.json').read_bytes()),
    'native_assets':assets,'CSS_source':str(CSS),'CSS_SHA256':sha(css_before),'CSS_unchanged':True,
    'abstract_full_normalization_exact':True,'single_ScholarlyArticle':True,'parser_checks_passed':True,
    'observed_collision_paths':[{'path':str(p),'exists':p.exists()} for p in collision_paths],
    'scope':'Private editorial page only; no live/canonical, legacy, deployment or publication certification'}
(A/'BUILD_RECEIPT.json').write_bytes(enc(receipt))
print(json.dumps({'private_only':True,'page':str(D/'index.html'),'page_SHA256':receipt['page_SHA256'],
    'model_SHA256':receipt['model_SHA256'],'native_asset_count':2,'CSS_unchanged':True,'abstract_exact':True,'publication_authority':False}))
