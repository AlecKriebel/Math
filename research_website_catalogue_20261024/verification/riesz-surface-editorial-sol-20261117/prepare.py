"""Fresh bounded private editorial data builder. No scientific or Git execution."""
import datetime
import hashlib
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = P / 'verification/riesz-surface-editorial-sol-20261117'
SOURCE = P / 'papers/23202994/sources'
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
SLUG = 'hypersingular-riesz-surface-constants'
TITLE = 'Hypersingular Riesz-energy constants on surfaces from triangular-lattice universal optimality'
DOI = '10.5281/zenodo.23202994'
ROOT_CLEARANCE = P / 'verification/root-clearance-23202994-20261117.json'
ROOT_REVIEW = P / 'papers/23202994/reviews/root-continuation-20261117/ROOT_REVIEW.md'
TEX = SOURCE / 'archives/01-source-and-verification.zip.extracted/publication/main.tex'
CSS = W / 'public/research/research.css'

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def raw_file(path):
    first = path.lstat()
    assert stat.S_ISREG(first.st_mode) and not path.is_symlink(), str(path)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        opened = os.fstat(fd)
        assert (first.st_dev,first.st_ino) == (opened.st_dev,opened.st_ino)
        chunks = []
        while True:
            chunk = os.read(fd, 1048576)
            if not chunk:
                break
            chunks.append(chunk)
        last = os.fstat(fd)
        assert (opened.st_dev,opened.st_ino,opened.st_size,opened.st_mode,opened.st_mtime_ns,opened.st_ctime_ns) == (last.st_dev,last.st_ino,last.st_size,last.st_mode,last.st_mtime_ns,last.st_ctime_ns)
        assert (path.lstat().st_dev,path.lstat().st_ino) == (last.st_dev,last.st_ino)
        raw = b''.join(chunks)
        assert len(raw) == last.st_size
        return raw
    finally:
        os.close(fd)

def pin(path):
    raw = raw_file(path)
    return dict(bytes=len(raw), SHA256=hashlib.sha256(raw).hexdigest(), MD5=hashlib.md5(raw).hexdigest(), mode=format(stat.S_IMODE(path.lstat().st_mode),'04o'))

def census(root):
    files, directories = {}, {}
    pending = [root]
    while pending:
        here = pending.pop()
        first = here.lstat()
        assert stat.S_ISDIR(first.st_mode) and not here.is_symlink()
        for path in sorted(here.iterdir()):
            rel = path.relative_to(root).as_posix()
            info = path.lstat()
            if stat.S_ISDIR(info.st_mode):
                assert not path.is_symlink()
                directories[rel] = format(stat.S_IMODE(info.st_mode),'04o')
                pending.append(path)
            else:
                files[rel] = pin(path)
        last = here.lstat()
        assert (first.st_dev,first.st_ino,first.st_mode,first.st_mtime_ns,first.st_ctime_ns) == (last.st_dev,last.st_ino,last.st_mode,last.st_mtime_ns,last.st_ctime_ns)
    return dict(root=str(root),root_mode=format(stat.S_IMODE(root.lstat().st_mode),'04o'),files=files,directories=directories)

def unique(pairs):
    result = {}
    for key,value in pairs:
        assert key not in result, key
        result[key] = value
    return result

def read_json(path):
    return json.loads(raw_file(path), object_pairs_hook=unique)

def write(name, text):
    with (OWN/name).open('x',encoding='utf-8') as stream:
        stream.write(text)

def write_json(name, value):
    write(name,json.dumps(value,indent=2,ensure_ascii=False)+'\n')

def collision():
    public = W/'public'
    research = public/'research'
    assert public.is_dir() and research.is_dir() and not public.is_symlink() and not research.is_symlink()
    targets = [research/SLUG,research/(SLUG+'.html')]
    states = {str(p):os.path.lexists(p) for p in targets}
    assert not any(states.values()), states
    return dict(UTC=utc(),actual_public_root=str(public),root_mode=format(stat.S_IMODE(public.lstat().st_mode),'04o'),checked_paths=states,absent=True,scope='Only actual local proposed target paths; no global/history/live claim')

started = utc()
assert pin(ROOT_CLEARANCE)['SHA256'] == '6631b8b7c7a5452b6f1867400f6f2d3bec454b100daf8f5b8bd54f620cfeb843'
assert pin(ROOT_REVIEW)['bytes'] == 15870 and pin(ROOT_REVIEW)['SHA256'] == '6ade63069c5793ba730d1526876e3de34b88e0540b3dcff385c5890c31dd467f'
clearance = read_json(ROOT_CLEARANCE)
assert clearance['status'] == 'PASS' and clearance['review_completion_percent'] == 100 and clearance['record_id'] == '23202994'
assert clearance['private_editorial_preparation_allowed'] and not clearance['W_installation_or_deployment_authority']
before = census(SOURCE)
assert (len(before['files']),len(before['directories'])) == (39,15)
assert before['files']['SOURCE_MANIFEST.json']['SHA256'] == '7a6854f7ebb1caf7a0f26c5cb6014872ee0ce93f03414c3f48d965ff13c9a976'
assert before['files']['SOURCE_FINAL.json']['SHA256'] == 'd90fbadc2f49aa86904695ce60c2042eef4e6850f70d3972b5f48fdb8913c27e'
old = read_json(P/'papers/23202994/reviews/scope-sol-continuation-20261117/GUARDS_AFTER.json')['source']
assert before['root'] == old['root'] and before['root_mode'] == old['root_mode'] and before['directories'] == old['directories']
assert {k:{f:v[f] for f in ('bytes','SHA256','mode')} for k,v in before['files'].items()} == old['files']
native_manifest = read_json(SOURCE/'SOURCE_MANIFEST.json')
assert native_manifest['schema'] == 'source-custody-manifest-v1' and native_manifest['record_id'] == 23202994
assert native_manifest['excluded_control_files'] == ['SOURCE_MANIFEST.json','SOURCE_FINAL.json']
seen = set()
for item in native_manifest['entries']:
    name = item['path']
    assert name not in seen
    seen.add(name)
    expected_mode = format(int(item['mode_octal'],8),'04o')
    if item['kind'] == 'directory':
        assert (before['root_mode'] if name == '.' else before['directories'][name]) == expected_mode
    else:
        actual = before['files'][name]
        assert actual['bytes'] == item['bytes'] and actual['SHA256'] == item['sha256'] and actual['mode'] == expected_mode and actual['MD5'] == item['md5']
assert seen == (set(before['files'])-{'SOURCE_MANIFEST.json','SOURCE_FINAL.json'})|set(before['directories'])|{'.'}
write_json('SOURCE_GUARDS_BEFORE.json',before)
collision_before = collision()
css_before = pin(CSS)
api = read_json(SOURCE/'native-metadata/record-api.json')
metadata = api['metadata']
assert api['id'] == 23202994 and metadata['title'] == TITLE and api['doi'] == DOI
assert metadata['publication_date'] == '2026-10-06' and metadata['version'] == '1.0.0' and metadata['license']['id'] == 'cc-by-4.0'
assert [x['key'] for x in api['files']] == ['paper.pdf','source-and-verification.zip']
tex = raw_file(TEX).decode('utf-8')
assert tex.count('\\begin{abstract}') == tex.count('\\end{abstract}') == 1
original = tex.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0]
normalized = re.sub(r'\s+',' ',original).strip()
renderings = {'$s>2$':'s>2','$N^{1-s/2}$':'N^(1−s/2)','Hardin--Saff':'Hardin–Saff'}
abstract = normalized
for a,b in renderings.items():
    assert a in abstract
    abstract = abstract.replace(a,b)
assert '$' not in abstract and '\\' not in abstract and '{' not in abstract and '}' not in abstract
write('ABSTRACT.txt',abstract+'\n')
write_json('ABSTRACT_SOURCE.json',dict(source=str(TEX),source_pin=pin(TEX),native_abstract_tex=original,whitespace_normalized_tex=normalized,declared_renderings=renderings,rendered_abstract=abstract,source_description_not_substituted=True))
(OWN/'assets').mkdir()
assets = []
for item in api['files']:
    name = item['key']
    source_asset = SOURCE/'zenodo-files'/name
    data = raw_file(source_asset)
    assert len(data) == item['size'] and 'md5:'+hashlib.md5(data).hexdigest() == item['checksum']
    dest = OWN/'assets'/name
    with dest.open('xb') as stream:
        stream.write(data)
    os.chmod(dest,stat.S_IMODE(source_asset.lstat().st_mode))
    assert pin(dest) == pin(source_asset)
    assets.append(dict(name=name,local_path='assets/'+name,**pin(dest),native_checksum=item['checksum'],format='application/pdf' if name.endswith('.pdf') else 'application/zip',native_url=item['links']['self']))
assert assets[0]['SHA256'] == 'b9e7c887787b911b55f012cc640621fedc282dd71e8c57fa01c1f9db49612d9d'
assert assets[1]['SHA256'] == '0da7186f4a5fae4395347ce46963365f449a65f2d14b468cd28746b6d9d48ebd'
description = 'An attributed consequence of triangular-lattice universal optimality: exact leading Riesz-energy constants on smooth surfaces for each fixed s > 2.'
model = dict(schema='private-editorial-page-model-v1',record_id='23202994',sheet_row=190,title=TITLE,seo_title='Riesz-energy constants on surfaces | Alec Kriebel',meta_description=description,author=dict(name='Alec Kriebel',ORCID='https://orcid.org/0009-0001-9320-500X'),doi=DOI,doi_url=api['doi_url'],zenodo_record='https://zenodo.org/records/23202994',native_version='1.0.0',printed_version=None,printed_date='October 6, 2026',publication_date=metadata['publication_date'],record_created=api['created'],record_updated=api['updated'],status='Unrefereed, AI-assisted preprint',abstract=abstract,abstract_source='Complete original main.tex abstract; whitespace and declared math/TeX-dash rendering only',abstract_math_rendering=renderings,native_Description_source='papers/23202994/sources/native-metadata/record-api.json metadata.description; not the manuscript abstract',canonical_url=None,base_url=None,production_url=None,actual_publication_date=None,AA=None,publication_authority=False,robots='noindex, nofollow',deployment_proposal=dict(slug=SLUG,path='/research/'+SLUG+'/',proposed_canonical_url='https://aleckriebel.com/research/'+SLUG+'/',current_public_page_created=False,passive_slug_collision_check_absent=True,future_payloads=['index.html','citation.bib','assets/paper.pdf','assets/source-and-verification.zip'],shared_stylesheet='/research/research.css',requires_separate_root_adoption_staging_publication_and_live_verification=True),native_asset_order=assets,pdf_pages=5,citation_bib='citation.bib',rights=dict(owned_original_text_source_code_notes_results='CC BY 4.0',third_party='Cited third-party works retain authorship and rights',source_statement='Native publication/LICENSE.md and README; no invented MIT/Apache exception'),scientific_scope=dict(exponent='Each fixed real s>2',pairs='Ordered off-diagonal; collisions have infinite energy',lattice='b=sqrt(3)/2; Lambda=b^(-1/2){(j+k/2,kb)}; covolume one',constant='Z_s=sum_(v in Lambda,v!=0)|v|^(-s); exact ordered unit-square limit',surface='Smooth compact embedded two-dimensional surfaces of positive ordinary area A, including smooth boundary; leading minimum Z_s A^(-s/2)N^(1+s/2)',distance='Ambient Euclidean; chordal on unit sphere',sphere_coefficient='Z_s/(4pi)^(s/2)',bridge='Fixed positive gaps, exact periodic centered-disk average, inter-box error O_epsilon(N^(1-s/2)); disk limit first, then N, then gap down to0',limits='No crystallization, finite-minimizer uniqueness, second term, new s<=2 result, joint uniform limits, other-dimensional constant, formal or human-review claim'),attribution=['OpenAI exact pinned universal-energy theorem and atomic companion; substantive new input','Hardin–Saff corrected Theorem2.4/definition19/addendum; area universality','HSS2014 Theorem3.2 and HLSS2018 Proposition3.1; known finite/periodic/thermodynamic reductions','Cohn–Kumar periodic averaging','Kuijlaars–Saff Conjecture1 and BHS2012 Conjecture2 dimension2 candidate'],framing='Attributed consequence/exposition; no independent base breakthrough, invented reduction or firstness claim',AI_disclosure='Extensive research/drafting/computation/verification; unrefereed; automated reviews are not human peer review',collaboration='Passive substantive independent verification/exposition/journal-version contributions; authorship based on actual contributions',scientific_clearance=dict(inherited=True,new_scientific_review=False,path=str(ROOT_CLEARANCE.relative_to(P)),SHA256=pin(ROOT_CLEARANCE)['SHA256']),follow_up=None,rendered_or_live_certificate=False)
write_json('page-model.json',model)
scholar = {'@context':'https://schema.org','@type':'ScholarlyArticle','name':TITLE,'headline':TITLE,'description':description,'abstract':abstract,'author':{'@type':'Person','name':'Alec Kriebel','identifier':'https://orcid.org/0009-0001-9320-500X'},'datePublished':metadata['publication_date'],'dateCreated':api['created'],'dateModified':api['updated'],'version':'1.0.0','creativeWorkStatus':model['status'],'inLanguage':'en','isAccessibleForFree':True,'identifier':{'@type':'PropertyValue','propertyID':'DOI','value':DOI},'sameAs':api['doi_url'],'license':'https://creativecommons.org/licenses/by/4.0/','keywords':metadata['keywords'],'encoding':[{'@type':'MediaObject','name':a['name'],'contentUrl':a['local_path'],'encodingFormat':a['format'],'contentSize':str(a['bytes'])+' bytes','sameAs':a['native_url']} for a in assets]}
metas = [('description',description),('author','Alec Kriebel'),('robots','noindex, nofollow'),('googlebot','noindex, nofollow'),('citation_title',TITLE),('citation_author','Kriebel, Alec'),('citation_author_orcid','0009-0001-9320-500X'),('citation_publication_date','2026/10/06'),('citation_date','2026/10/06'),('citation_version','1.0.0'),('citation_doi',DOI),('citation_pdf_url','assets/paper.pdf'),('citation_language','en'),('DC.title',TITLE),('DC.creator','Alec Kriebel'),('DC.date','2026-10-06'),('DC.description',abstract),('DC.identifier','doi:'+DOI),('DC.type','Text'),('DC.language','en'),('DC.rights','Original text/source/code/notes/results CC BY 4.0; third-party rights retained'),('twitter:card','summary'),('twitter:title',TITLE),('twitter:description',description)]
properties = [('og:type','article'),('og:title',TITLE),('og:description',description),('og:site_name','Alec Kriebel'),('article:published_time','2026-10-06'),('article:modified_time',api['updated'])]
head = '<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>'+html.escape(model['seo_title'])+'</title>\n'
head += ''.join('<meta name="'+k+'" content="'+html.escape(v,quote=True)+'">\n' for k,v in metas)
head += ''.join('<meta property="'+k+'" content="'+html.escape(v,quote=True)+'">\n' for k,v in properties)
head += '<link rel="stylesheet" href="/research/research.css">\n<script type="application/ld+json">'+json.dumps(scholar,ensure_ascii=False).replace('<','\\u003c')+'</script>\n</head>\n'
body_template = raw_file(OWN/'main.template.html').decode('utf-8')
assert body_template.count('{{ABSTRACT}}') == 1
main = body_template.replace('{{ABSTRACT}}',html.escape(abstract,quote=False))
article = '<!doctype html>\n<html lang="en">\n'+head+'<body>\n<a class="skip-link" href="#main">Skip to content</a>\n<header><p class="site-title"><a href="https://aleckriebel.com/">Alec Kriebel</a></p><nav aria-label="Main navigation"><a href="https://aleckriebel.com/">Home</a> · <a href="https://aleckriebel.com/research/">Research</a></nav></header>\n'+main+'<footer><p><a href="https://aleckriebel.com/research/">Research index</a> · <a href="https://orcid.org/0009-0001-9320-500X">ORCID</a></p></footer>\n</body>\n</html>\n'
write('head.html',head)
write('main.html',main)
write('article.html',article)
write('citation.bib','@misc{Kriebel2026RieszSurfaceConstants,\n  author = {Kriebel, Alec},\n  title = {{'+TITLE+'}},\n  year = {2026},\n  date = {2026-10-06},\n  version = {1.0.0},\n  doi = {'+DOI+'},\n  url = {https://zenodo.org/records/23202994},\n  publisher = {Zenodo},\n  note = {Unrefereed, AI-assisted preprint}\n}\n')

class Inspect(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids,self.tags,self.meta,self.local,self.scripts = [],[],{},[],[]
        self.abstract,self.capture,self.script = '',False,False
    def handle_starttag(self,tag,attrs):
        a = dict(attrs)
        self.tags.append(tag)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'meta' and 'name' in a:
            assert a['name'] not in self.meta
            self.meta[a['name']] = a['content']
        if a.get('id') == 'abstract-text':
            self.capture = True
        if tag == 'script':
            assert a.get('type') == 'application/ld+json'
            self.script = True
            self.scripts.append('')
        for key in ('href','src'):
            if key in a and not a[key].startswith(('https://','http://','#','/')):
                self.local.append(a[key].split('#',1)[0])
    def handle_data(self,data):
        if self.capture:
            self.abstract += data
        if self.script:
            self.scripts[-1] += data
    def handle_endtag(self,tag):
        if tag == 'p':
            self.capture = False
        if tag == 'script':
            self.script = False

parsed = Inspect()
parsed.feed(article)
assert len(parsed.ids) == len(set(parsed.ids)) and parsed.tags.count('main') == parsed.tags.count('article') == parsed.tags.count('h1') == parsed.tags.count('iframe') == 1
assert len(parsed.scripts) == 1 and json.loads(parsed.scripts[0]) == scholar and '@graph' not in scholar
assert parsed.abstract == parsed.meta['DC.description'] == scholar['abstract'] == model['abstract'] == abstract
assert [x['name'] for x in scholar['encoding']] == ['paper.pdf','source-and-verification.zip']
assert parsed.meta['robots'] == parsed.meta['googlebot'] == 'noindex, nofollow'
assert not re.search(r'<base\b|rel=["\']canonical|og:url',head)
assert all(model[k] is None for k in ('canonical_url','base_url','production_url','actual_publication_date','AA','follow_up'))
assert not model['publication_authority'] and not model['rendered_or_live_certificate']
for rel in parsed.local:
    assert (OWN/rel).is_file(), rel
assert '/research/research.css' in head and '<style' not in article and 'MIT' not in article and 'Apache' not in article
assert article.count('<head>') == article.count(head) == article.count(main) == 1
assert pin(CSS) == css_before
collision_after = collision()
after = census(SOURCE)
assert after == before
write_json('SOURCE_GUARDS_AFTER.json',after)
write_json('COLLISION_AND_CSS.json',dict(collision_before=collision_before,collision_after=collision_after,stylesheet_path=str(CSS),stylesheet_before=css_before,stylesheet_after=pin(CSS),stylesheet_changed=False,public_namespace_not_modified=True))
write_json('STATIC_CHECK.json',dict(schema='private-editorial-static-data-check-v1',UTC=utc(),head_main_assembly_exact=True,single_article_single_ScholarlyArticle=True,original_abstract_exact_with_declared_renderings=True,abstract_visible_DC_model_schema_identical=True,native_assets_in_order=True,native_asset_whole_bytes_modes_equal=True,source39_15_exact_before_after=True,private_noindex_actual_authority_fields_null=True,proposed_slug_separate=True,relative_links_exist=True,shared_stylesheet_unchanged=True,rendered_browser_or_HTTP_certificate=False,new_scientific_program_runs=0))
write('REPORT.md','# Private editorial preparation: row190 /23202994\n\nThis packet inherits the exact root scientific PASS and prepares private article/head/main/model/BibTeX plus the two unchanged native assets. It introduces no new scientific validation or public installation. The complete original abstract is derived from main.tex by whitespace normalization and the three explicitly declared math/TeX-dash replacements; it is identical in visible text, DC.description, model and the one ScholarlyArticle. Native asset and encoding order is PDF thenZIP. The rights statement is CC BY4.0 for original text/source/code/notes/results, with third-party rights retained and no invented code-license exception.\n\nThe page explains each fixed s>2, ordered pairs, the covolume-one triangular Epstein sum, ambient/chordal distance, positive ordinary area and smooth boundary. It credits OpenAI, correctedHardin–Saff, knownHSS/HLSS reductions, periodic averaging and earlier conjectures. Verification language is concise and distinguishes finite checks from analytic proofs and formal verification. ExtensiveAIuse, unrefereedstatus and contribution-based collaboration/authorship are disclosed. Follow-up is null.\n\nCanonical/base/production URL, actual website publication date and AA remain null; the proposed canonical appears only as a separate model proposal. The actual current W/public target was checked absent without a directory census or mutation; /research/research.css is referenced and whole-byte guarded unchanged. Source39files/15dirs, hidden/empty topology and modes match the accepted source guard and actual native manifest before/after.\n\nStatic consistency checks passed. No rendered/browser/live certificate, network request, source/helper import, scientific execution, Git/Sheet/W action, outreach or publication authority was exercised. Separate independent fact review and root actual copy reading remain required.\n')
with (OWN/'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n'+utc()+' — One fresh private data-builder attempt complete. Source39/15 unchanged; original abstract and two native assets exact; static metadata/assembly/link/order checks pass. Sharedstylesheet unchanged; actual proposed local target absent. Completion90%; finite sealing remains.\n')
write_json('PREPARATION_RESULT.json',dict(schema='row190-private-editorial-preparation-result-v1',started_UTC=started,finished_UTC=utc(),status='READY_FOR_INDEPENDENT_FACT_REVIEW',source_files_dirs=[39,15],native_assets=assets,clearance=pin(ROOT_CLEARANCE),root_review=pin(ROOT_REVIEW),builder=pin(Path(__file__)),scientific_clearance_inherited=True,scientific_runs=0,production_authority=False,actual_canonical=None,actual_publication_date=None,AA=None,follow_up=None,limitations=['Static data checks only; browser/render/live checks not performed','No W/Git/Sheet/network/publication action','Independent fact/root actual copy review pending']))
