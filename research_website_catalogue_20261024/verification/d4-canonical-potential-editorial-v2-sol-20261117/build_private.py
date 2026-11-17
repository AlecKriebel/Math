"""One fresh data-only private editorial builder. No source imports, scientific execution or network."""
import datetime, hashlib, html, json, stat
from html.parser import HTMLParser
from pathlib import Path
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN=P/'verification/d4-canonical-potential-editorial-v2-sol-20261117'
SRC=P/'papers/23439776/sources';OUT=OWN/'private-page'
CSS=P/'verification/binary-gram-locus-editorial-sol-20261117/private-page/research.css'
def digest(raw):return hashlib.sha256(raw).hexdigest()
def put(p,raw):
    with p.open('xb') as f:f.write(raw)
    p.chmod(0o644)
def putjson(p,value):put(p,(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode())
before=json.loads((OWN/'CUSTODY_BEFORE.json').read_bytes())
assert before['phase']=='before' and len(before['source']['files'])==72
record=json.loads((SRC/'record.response.body').read_bytes());meta=record['metadata']
assert record['id']==23439776 and meta['version']=='1.0' and meta['publication_date']=='2026-10-17'
title=meta['title'];assert title=='A type-D4 counterexample to the canonical-potential exponent converse'
doi=meta['doi'];assert doi=='10.5281/zenodo.23439776'
tex=(SRC/'published-source/container-001/tree/manuscript/main.tex').read_text()
assert digest(tex.encode())=='d15c70dcc7ee0744a6ea34cd72049abacddebb43dd7034becd8d6fa153d86c22'
assert tex.count(r'\begin{abstract}')==tex.count(r'\end{abstract}')==1
abstract_source=tex.split(r'\begin{abstract}',1)[1].split(r'\end{abstract}',1)[0]
replacements=[(r'$D_4$','D₄'),(r'$22$','22'),(r'$-2$','−2'),(r'$\{-1,0,1\}$','{−1,0,1}')]
abstract=abstract_source
for old,new in replacements:abstract=abstract.replace(old,new)
abstract=' '.join(abstract.split());assert '$' not in abstract and '\\' not in abstract
expected=[('Canonical_W_D4_Verification_v1.0.zip',63134,'f5ccf88733160c457423613fa1e0e329a562a29bad15bd71ed118114e9b98eef','d4443f1b3565f317c653f1013aa25520'),('Canonical_W_D4_Note_v1.0.pdf',77127,'1edcf5f41308f1369f45dde8aa75111b69d73c56a5a1cdf6724f636ee2d9dcb1','573d2455ed0379ead0ed0cd2bf9888c9')]
assert [(f['key'],f['size'],f['checksum']) for f in record['files']]==[(n,b,'md5:'+md5) for n,b,sha,md5 in expected]
assets=[];asset_bytes={}
for ordinal,(name,size,sha,md5) in enumerate(expected,1):
    p=SRC/'assets'/name;raw=p.read_bytes()
    assert len(raw)==size and digest(raw)==sha and hashlib.md5(raw).hexdigest()==md5 and stat.S_IMODE(p.stat().st_mode)==0o644
    url=record['files'][ordinal-1]['links']['self'];assert url=='https://zenodo.org/api/records/23439776/files/'+name+'/content'
    assets.append({'native_order':ordinal,'native_filename':name,'local_filename':name,'bytes':size,'SHA256':sha,'MD5':md5,'encoding_format':'application/zip' if name.endswith('.zip') else 'application/pdf','native_url':url});asset_bytes[name]=raw
css=CSS.read_bytes();assert len(css)==1170 and digest(css)=='f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a'
clearance=P/'verification/root-clearance-23439776-20261117.json';review=P/'papers/23439776/reviews/root-continuation-20261117/ROOT_REVIEW.md'
assert digest(clearance.read_bytes())=='d6a171c2f2a3b5480bd5bdc71e4c9fcb63bb2130bea2524e7e9df3cb9f6c6590'
assert digest(review.read_bytes())=='4836979d83da2747da766a2defc76bc0e5bbd6b48b25025c0de434aefd580e62'
description='A type-D4 example separates the historical canonical-potential exponent bound from facet irredundancy, with earlier string-support computations credited.'
references=[('Schumann, Optimality of string cone inequalities and potential functions (2021)','https://doi.org/10.4171/OWR/2021/20'),('Koshevoy and Schumann, Redundancy in string cone inequalities and multiplicities in potential functions on cluster varieties (2022)','https://doi.org/10.1007/s10801-022-01144-z'),('Genz, Koshevoy and Schumann, Polyhedral parametrizations of canonical bases & cluster duality (2020)','https://doi.org/10.1016/j.aim.2020.107178'),('Mironov, crystal dataset, Case 267 (pinned source)','https://github.com/mironovd/crystal/tree/0d6e564cf5e69d79c1074d5d1e3e72ac700904d6'),('Koshevoy and Mironov, F-polynomials and Newton polytopes (2022)','https://easychair.org/publications/preprint/z55N')]
scholar={'@context':'https://schema.org','@type':'ScholarlyArticle','name':title,'headline':title,'author':{'@type':'Person','name':'Alec Kriebel','sameAs':'https://orcid.org/0009-0001-9320-500X','identifier':'https://orcid.org/0009-0001-9320-500X'},'identifier':{'@type':'PropertyValue','propertyID':'DOI','value':doi},'url':'https://doi.org/'+doi,'sameAs':['https://zenodo.org/records/23439776'],'datePublished':meta['publication_date'],'version':meta['version'],'inLanguage':'en','abstract':abstract,'description':description,'keywords':meta['keywords'],'license':'https://creativecommons.org/licenses/by/4.0/','publisher':{'@type':'Organization','name':'Zenodo'},'creativeWorkStatus':'Unrefereed preprint','isAccessibleForFree':True,'citation':[url for label,url in references],'encoding':[{'@type':'MediaObject','name':a['native_filename'],'encodingFormat':a['encoding_format'],'contentSize':str(a['bytes'])+' bytes','contentUrl':a['native_url']} for a in assets]}
model={'schema':'private-D4-canonical-potential-editorial-model-v1','record_id':'23439776','inventory_row':171,'private_only':True,'publication_authority':False,'title':title,'author':'Alec Kriebel','ORCID':'https://orcid.org/0009-0001-9320-500X','DOI':doi,'native_version':meta['version'],'native_publication_date':meta['publication_date'],'native_record_created':record['created'],'native_record_updated':record['updated'],'proposed_slug':'d4-canonical-potential-exponent-converse','proposed_path':'/research/d4-canonical-potential-exponent-converse/','actual_canonical':None,'base_url':None,'production_url':None,'page_publication_date':None,'AA':None,'legacy_redirect':None,'follow_up':None,'robots':'noindex,nofollow','native_assets_in_original_order':assets,'abstract':{'literal_source_TeX_span':abstract_source,'literal_rendering_replacements':[{'from':old,'to':new} for old,new in replacements],'whitespace_rule':'Collapse whitespace runs to single spaces and strip ends; no prose or punctuation edits','normalized_full_text':abstract,'normalized_SHA256':digest(abstract.encode())},'exact_scope':'Historical designated canonical-X potential: 22 coefficient-one monomials, 22 distinct facets in dimension 12, two X6 exponents -2','exclusions':['Later string-coordinate converse not refuted','Separate coefficient criterion not refuted','KS sufficient-criterion theorem conclusion not refuted','No exclusive priority or current-openness claim'],'earlier_credit':'Mironov Case267 already supplies same reduced word and complete string-coordinate support','rights':{'manuscript_certificates_review_text':'CC-BY-4.0','original_Python_code':'MIT','third_party':'Own rights retained; no third-party dataset or downloaded primary redistribution'},'stylesheet':{'private_reference':'research.css','shared_style_reference':'/research/research.css','input':str(CSS),'SHA256':digest(css),'changed':False},'structured_data':scholar,'input_pins':{'root_review':digest(review.read_bytes()),'root_clearance':digest(clearance.read_bytes()),'source_TeX':digest(tex.encode()),'source_metadata':digest((SRC/'record.response.body').read_bytes())},'checkpoint_provenance_only':'14013a3a64b3beb7689a53d5551e9a9ca9a8d990','legacy_or_collision_or_live_certificate':False}
esc=html.escape;pdf=assets[1]['native_filename'];archive=assets[0]['native_filename']
head=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | Alec Kriebel</title>
<meta name="robots" content="noindex,nofollow">
<meta name="description" content="{esc(description,quote=True)}">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(title,quote=True)}">
<meta property="og:description" content="{esc(description,quote=True)}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{esc(title,quote=True)}">
<meta name="twitter:description" content="{esc(description,quote=True)}">
<meta name="citation_title" content="{esc(title,quote=True)}">
<meta name="citation_author" content="Alec Kriebel">
<meta name="citation_author_orcid" content="https://orcid.org/0009-0001-9320-500X">
<meta name="citation_author_institution" content="Independent researcher">
<meta name="citation_publication_date" content="2026/10/17">
<meta name="citation_date" content="2026/10/17">
<meta name="citation_version" content="1.0">
<meta name="citation_doi" content="{doi}">
<meta name="citation_pdf_url" content="{assets[1]['native_url']}">
<meta name="citation_language" content="en">
<meta name="citation_abstract" content="{esc(abstract,quote=True)}">
<meta name="DC.title" content="{esc(title,quote=True)}">
<meta name="DC.identifier" content="https://doi.org/{doi}">
<meta name="DC.description" content="{esc(abstract,quote=True)}">
<link rel="stylesheet" href="research.css">
<script type="application/ld+json">{json.dumps(scholar,ensure_ascii=False).replace('</','<\\/')}</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to the article</a>
<header><p class="site-title"><a href="/">Alec Kriebel</a></p><nav aria-label="Site"><a href="/research/">Research</a></nav></header>
<main id="main"><article>
<h1>{esc(title)}</h1>
<p class="entry-meta"><a href="https://orcid.org/0009-0001-9320-500X">Alec Kriebel</a> · Independent researcher<br>Version 1.0 · <time datetime="2026-10-17">17 October 2026</time> · Unrefereed research note</p>
<p>A list of linear inequalities can describe the faces of a cone. This note gives an explicit type-D₄ example in which every listed inequality is needed, yet the canonical potential has a coordinate exponent outside the proposed bound. The counterexample concerns a particular historical formulation and its designated canonical coordinates.</p>
<p><a href="{pdf}">Open the original PDF</a> · <a href="{pdf}" download="{pdf}">Download PDF</a> · <a href="{archive}" download="{archive}">Source and verification archive</a> · <a href="citation.bib" download>BibTeX</a> · <a href="https://doi.org/{doi}">DOI: {doi}</a></p>

<section aria-labelledby="credit-heading"><h2 id="credit-heading">Earlier computation and the note’s contribution</h2>
<p><strong>Denis Mironov’s earlier <a href="{references[3][1]}">crystal dataset, Case 267</a>, already contains the same reduced word and its complete string-coordinate support.</strong> This note credits that input. It extracts the consequence for the historical canonical-potential assertion, reconstructs the canonical potential and supplies explicit integer facet certificates. It makes no exclusive-priority or current-openness claim.</p>
<p>The historical converse appears in <a href="{references[0][1]}">Schumann’s 2021 Oberwolfach contribution</a>. The seed, potential and chamber-map conventions come from <a href="{references[1][1]}">Koshevoy and Schumann</a> and <a href="{references[2][1]}">Genz, Koshevoy and Schumann</a>. <a href="{references[4][1]}">Koshevoy and Mironov’s later computational article</a> cites the earlier repository.</p></section>

<section aria-labelledby="result-heading"><h2 id="result-heading">The explicit example</h2>
<p>For Spin₈(C), label node 2 as the central node of the D₄ diagram and take the reduced word</p>
<p class="equation">i = (1, 2, 3, 2, 4, 2, 1, 2, 3, 2, 4, 2).</p>
<p>In its specified canonical reduced-word cluster-X coordinates, the potential has <strong>22 distinct monomials, each with coefficient one</strong>. Their 22 tropical inequalities define distinct facets of a full-dimensional cone in R¹². Nevertheless, two monomials have X₆ exponent −2.</p>
<p>This disproves the necessary direction of the historical canonical-W converse: irredundancy of these inequalities does not force every exponent in those canonical coordinates to have absolute value at most one.</p></section>

<section aria-labelledby="coordinates-heading"><h2 id="coordinates-heading">Why the coordinates matter</h2>
<p>The chamber-ansatz change to string coordinates preserves the inequality presentation and its facets, but it can change the exponent of an individual coordinate. In this example every exponent after that pullback lies in &#123;−1, 0, 1&#125;.</p>
<p><strong>The later string-coordinate converse is not refuted.</strong> Neither is its separate coefficient criterion, nor the conclusion of the cited KS sufficient-criterion theorem. The note identifies a false equivalence of the two coordinate bounds within a printed proof; it does not supply a general replacement proof for that step. Its facet argument is direct and does not use that assertion.</p></section>

<section aria-labelledby="verification-heading"><h2 id="verification-heading">Proof and verification materials</h2>
<p>The manuscript displays the canonical potential and integer certificates separating each facet inequality from all the others. The unchanged verification archive includes the manuscript source, certificate data and exact-arithmetic programs. These materials support inspection of this explicit example; they do not establish a general classification or a later conjecture.</p></section>

<section aria-labelledby="abstract-heading"><h2 id="abstract-heading">Original manuscript abstract</h2>
<p id="manuscript-abstract">{esc(abstract)}</p></section>

<section aria-labelledby="files-heading"><h2 id="files-heading">Original files and citation</h2>
<p>The native files are listed in their original record order and retain their original names and bytes.</p>
<ol><li><a href="{archive}" download="{archive}">Source and verification archive — {archive}</a> · <a href="{assets[0]['native_url']}">Zenodo original</a></li>
<li><a href="{pdf}" download="{pdf}">Manuscript PDF — {pdf}</a> · <a href="{assets[1]['native_url']}">Zenodo original</a></li></ol>
<p>Kriebel, Alec (2026). <em>{esc(title)}</em>. Version 1.0. Zenodo. <a href="https://doi.org/{doi}">{doi}</a>. <a href="citation.bib" download>Download BibTeX</a> · <a href="https://zenodo.org/records/23439776">Zenodo record</a>.</p>
<p>The original manuscript, certificates and review text are licensed under <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>; the original Python verification code is MIT licensed. Third-party sources retain their own rights. The earlier unlicensed dataset and downloaded primary papers are linked as sources and are not redistributed here.</p></section>

<section aria-labelledby="paper-heading"><h2 id="paper-heading">Read the unchanged manuscript</h2>
<p><a href="{pdf}">Open PDF</a> · <a href="{pdf}" download="{pdf}">Download PDF</a> · <a href="{assets[1]['native_url']}">Original PDF on Zenodo</a></p>
<iframe class="paper-pdf" src="{pdf}" title="A type-D4 counterexample to the canonical-potential exponent converse — original PDF" loading="lazy"><p><a href="{pdf}">Read the original PDF</a>.</p></iframe></section>

<section aria-labelledby="status-heading"><h2 id="status-heading">Review status and contributions</h2>
<p>AI tools were used extensively in developing, solving, reconstructing, verifying and reviewing the arguments, searching the literature, and preparing the note and code. This work is unrefereed and has not undergone conventional external human peer review. Internal AI reviews are not a formal proof-assistant certificate. Alec Kriebel is responsible for the contents.</p>
<p>Substantial mathematical or expository contributions can support collaboration. Authorship and acknowledgments would reflect the work actually contributed.</p></section>
</article></main>
<footer><p><a href="/research/">Research</a> · <a href="https://orcid.org/0009-0001-9320-500X">ORCID</a></p></footer>
</body></html>
'''
bib='''@misc{Kriebel2026CanonicalD4,
  author = {Kriebel, Alec},
  title = {A type-D4 counterexample to the canonical-potential exponent converse},
  year = {2026},
  month = oct,
  version = {1.0},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.23439776},
  url = {https://doi.org/10.5281/zenodo.23439776},
  note = {Unrefereed research note, 17 October 2026}
}
'''
assert not OUT.exists();OUT.mkdir(mode=0o755)
for name,raw in asset_bytes.items():put(OUT/name,raw)
put(OUT/'research.css',css);put(OUT/'citation.bib',bib.encode());put(OUT/'index.html',head.encode());putjson(OWN/'MODEL.json',model)
class Check(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.metas={};self.links=[];self.iframes=[];self.h1=0;self.in_abstract=False;self.visible=[];self.in_scholar=False;self.scholar_text=[];self.scholar_count=0;self.canonical=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='meta' and 'name' in a:self.metas[a['name']]=a.get('content','')
        if tag=='h1':self.h1+=1
        if tag=='p' and a.get('id')=='manuscript-abstract':self.in_abstract=True
        if tag=='script' and a.get('type')=='application/ld+json':self.in_scholar=True;self.scholar_count+=1
        if tag=='iframe':self.iframes.append(a)
        if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a)
        self.links.extend(a[k] for k in ('href','src') if k in a)
    def handle_endtag(self,tag):
        if tag=='p':self.in_abstract=False
        if tag=='script':self.in_scholar=False
    def handle_data(self,data):
        if self.in_abstract:self.visible.append(data)
        if self.in_scholar:self.scholar_text.append(data)
check=Check();check.feed(head);check.close();parsed=json.loads(''.join(check.scholar_text))
assert check.h1==1 and check.scholar_count==1 and parsed==scholar and '@graph' not in parsed
assert ''.join(check.visible)==abstract==check.metas['citation_abstract']==check.metas['DC.description']==parsed['abstract']==model['abstract']['normalized_full_text']
assert check.metas['citation_title']==title and check.metas['citation_doi']==doi and check.metas['citation_version']=='1.0' and check.metas['citation_publication_date']=='2026/10/17'
assert check.metas['robots']=='noindex,nofollow' and not check.canonical
assert len(check.iframes)==1 and check.iframes[0]['src']==pdf and check.iframes[0]['title']
for link in check.links:
    if not link.startswith(('http://','https://','#','/')):assert (OUT/link).is_file(),link
assert [a['name'] for a in parsed['encoding']]==[a['native_filename'] for a in assets]
assert all(digest((OUT/a['local_filename']).read_bytes())==a['SHA256'] for a in assets) and digest((OUT/'research.css').read_bytes())==digest(css)
assert all(model[k] is None for k in ('actual_canonical','base_url','production_url','page_publication_date','AA','legacy_redirect','follow_up'))
receipt={'schema':'one-attempt-private-D4-editorial-build-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PRIVATE_PREPARED_STATIC_CHECKS_PASSED','attempt':1,'page_bytes':len(head.encode()),'page_SHA256':digest(head.encode()),'model_SHA256':digest((OWN/'MODEL.json').read_bytes()),'abstract_normalized_SHA256':digest(abstract.encode()),'native_assets_unchanged_original_order':assets,'CSS_bytes':len(css),'CSS_SHA256':digest(css),'one_scholar_no_graph':True,'complete_visible_DC_citation_Scholar_abstract_identical':True,'all_local_links_present':True,'PDF_iframe_open_download_same_original':True,'private_noindex_all_production_fields_null':True,'scientific_execution_or_network_Git_W_access':False,'browser_live_runtime_or_route_certificate':False,'publication_authority':False}
putjson(OWN/'BUILD_RECEIPT.json',receipt)
print(json.dumps({'status':receipt['status'],'page_bytes':receipt['page_bytes'],'native_asset_count':len(assets),'abstract_normalized_SHA256':receipt['abstract_normalized_SHA256'],'publication_authority':False}))
