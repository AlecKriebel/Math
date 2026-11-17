"""One private data-only article preparation; never imports or runs source programs."""
import datetime, hashlib, html, json, os, re, stat
from html.parser import HTMLParser
from pathlib import Path

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
OWN = P/'verification/mixed-k3-moduli-editorial-sol-20261117'
SRC = P/'papers/23204176/sources'
SLUG = 'mixed-k3-moduli-hodge-classes'
TITLE = 'Rational Hodge classes on mixed products of K3 moduli spaces'
CLEAR = P/'verification/root-clearance-23204176-20261117.json'
REVIEW = P/'papers/23204176/reviews/root-continuation-20261117/ROOT_REVIEW.md'
CSS = W/'public/research/research.css'
CONTROL_PINS = {'SOURCE_MANIFEST.json':'53be96c6f47deccccc173286d10bdf46b50df4f237c985f42f2da8a69d8c8ffb','SOURCE_FINAL.json':'f7bc05f4e7d56f0fbad45d77bdb4992d9fd92de8d976bdc5ff3b446f7dbfe9c8'}

def pin(path):
    a = path.lstat()
    assert stat.S_ISREG(a.st_mode) and not path.is_symlink(), str(path)
    with path.open('rb') as f:
        opened = os.fstat(f.fileno())
        assert (a.st_dev,a.st_ino) == (opened.st_dev,opened.st_ino)
        raw = f.read()
        z = os.fstat(f.fileno())
    end = path.lstat()
    fields = lambda s:(s.st_dev,s.st_ino,s.st_size,s.st_mode,s.st_mtime_ns,s.st_ctime_ns)
    assert fields(a) == fields(z) == fields(end) and len(raw) == z.st_size
    return dict(bytes=len(raw),SHA256=hashlib.sha256(raw).hexdigest(),MD5=hashlib.md5(raw).hexdigest(),mode=oct(stat.S_IMODE(z.st_mode))),raw

def census(root):
    files,dirs = {},{'.':oct(stat.S_IMODE(root.lstat().st_mode))}
    todo = [root]
    while todo:
        here = todo.pop()
        a = here.lstat()
        assert stat.S_ISDIR(a.st_mode) and not here.is_symlink()
        for p in sorted(here.iterdir()):
            rel = p.relative_to(root).as_posix()
            s = p.lstat()
            assert not p.is_symlink()
            if stat.S_ISDIR(s.st_mode):
                dirs[rel] = oct(stat.S_IMODE(s.st_mode))
                todo.append(p)
            else:
                files[rel] = pin(p)[0]
        z = here.lstat()
        assert (a.st_dev,a.st_ino,a.st_mode,a.st_mtime_ns,a.st_ctime_ns) == (z.st_dev,z.st_ino,z.st_mode,z.st_mtime_ns,z.st_ctime_ns)
    return dict(schema='whole-original-source-guard-v1',root=str(root),files=files,directories=dirs,hidden_paths=[n for n in sorted(set(files)|set(dirs)) if n!='.' and any(t.startswith('.') for t in n.split('/'))],empty_files=[n for n,x in sorted(files.items()) if x['bytes']==0],empty_directories=[n for n in sorted(dirs) if n!='.' and not any(q.startswith(n+'/') for q in set(files)|set(dirs))])

def write(name,text):
    with (OWN/name).open('x',encoding='utf-8') as f:
        f.write(text)

def writej(name,data):
    write(name,json.dumps(data,ensure_ascii=False,indent=2)+'\n')

utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
inputs = {str(p.relative_to(P)):pin(p)[0] for p in (CLEAR,REVIEW)}
assert inputs[str(CLEAR.relative_to(P))]['SHA256'] == 'ea5472784dffe99ee849d40700541b9453466b2f3edf064a3a02fe091e7f55cd'
assert inputs[str(REVIEW.relative_to(P))]['SHA256'] == '726d07488144fb2a7e4cbc0351c235a4a422a42346e71410000833596c2f6b94'
assert inputs[str(REVIEW.relative_to(P))]['bytes'] == 20893
clear = json.loads(CLEAR.read_bytes())
assert clear['record_id']=='23204176' and clear['status']=='PASS_BOUNDED_SUBSTANTIVE_REVIEW'
before = census(SRC)
assert len(before['files'])==43 and len(before['directories'])==8
for name,digest in CONTROL_PINS.items():
    assert before['files'][name]['SHA256']==digest
manifest = json.loads((SRC/'SOURCE_MANIFEST.json').read_bytes())
assert manifest['schema']=='source-custody-manifest-v1' and manifest['record_id']==23204176
assert manifest['excluded_control_files']==['SOURCE_MANIFEST.json','SOURCE_FINAL.json']
assert manifest['terminal_control_topology']==[dict(path=n,kind='file',mode_octal='0o644') for n in CONTROL_PINS]
names = [x['path'] for x in manifest['entries']]
assert len(names)==len(set(names))
mf,md = {},{}
for row in manifest['entries']:
    n = row['path']
    assert n=='.' or (not n.startswith('/') and all(t not in ('','.','..') for t in n.split('/')))
    if row['kind']=='file':
        assert set(row)=={'path','kind','mode_octal','hidden_component','bytes','sha256','md5'}
        mf[n]=dict(bytes=row['bytes'],SHA256=row['sha256'],MD5=row['md5'],mode=row['mode_octal'])
    else:
        assert row['kind']=='directory' and set(row)=={'path','kind','mode_octal','hidden_component','empty'}
        md[n]=row['mode_octal']
        assert row['empty']==(n in before['empty_directories'])
    assert row['hidden_component']==(n in before['hidden_paths'])
assert mf=={n:x for n,x in before['files'].items() if n not in CONTROL_PINS} and md==before['directories']
assert len(mf)==manifest['file_count']==41 and len(md)==manifest['directory_count']==8
assert sum(x['bytes'] for x in mf.values())==manifest['total_file_bytes']
writej('SOURCE_GUARDS_BEFORE.json',before)
api = json.loads((SRC/'native-metadata/record-api.json').read_bytes())
meta = api['metadata']
assert api['id']==23204176 and meta['title']==TITLE and 'version' not in meta
assert meta['publication_date']=='2026-10-06' and meta['license']=={'id':'cc-by-4.0'}
assert [x['key'] for x in api['files']]==['paper.pdf','source-and-verification.zip']
css_before = pin(CSS)[0]
collision = W/'public/research'/SLUG
assert not os.path.lexists(collision)
writej('COLLISION_AND_CSS.json',dict(UTC=utc,checked_path=str(collision),absent=True,passive_data_only=True,stylesheet=str(CSS),stylesheet_pin=css_before,stylesheet_modified=False))
texpath = SRC/'archives/01-source-and-verification.zip.extracted/main.tex'
tex = texpath.read_text()
parts = re.findall(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S)
assert len(parts)==1
literal = parts[0]
replacement = {'B\\"ulles':'Bülles'}
rendered = literal
for a,b in replacement.items():
    assert rendered.count(a)==1
    rendered=rendered.replace(a,b)
abstract = ' '.join(rendered.split())
assert '\\' not in abstract and '$' not in abstract
write('ABSTRACT.txt',abstract+'\n')
writej('ABSTRACT_SOURCE.json',dict(source=str(texpath.relative_to(P)),source_pin=pin(texpath)[0],literal_original_abstract=literal,declared_rendering_replacements=replacement,whitespace_normalization='split/join to one ASCII space; no sentence omissions or additions',normalized_complete_abstract=abstract,native_API_Description=meta['description'],API_Description_is_not_manuscript_abstract=True))
assets=[]
(OWN/'assets').mkdir()
for item in api['files']:
    key=item['key']
    source=SRC/'zenodo-files'/key
    value,raw=pin(source)
    assert value['bytes']==item['size'] and item['checksum']=='md5:'+value['MD5']
    local='assets/'+key
    with (OWN/local).open('xb') as f:
        f.write(raw)
    os.chmod(OWN/local,0o644)
    assert (OWN/local).read_bytes()==raw
    assets.append(dict(name=key,local_path=local,**value,native_checksum=item['checksum'],format='application/pdf' if key.endswith('.pdf') else 'application/zip',native_url=item['links']['self']))
assert assets[0]['bytes']==67264 and assets[0]['SHA256']=='483a6edff90202ef4d31560049a32ce946dcd1c6a999ab5b1f25b66a8f326612'
assert assets[1]['SHA256']=='8f44cd5f9c447e40a97a07a3bcc62998accdb7aad4fce94b4020c5fe87f77ce0'
description='An attributed corollary for rational Hodge classes on mixed products of smooth projective stable K3 moduli spaces, using OpenAI and Bülles.'
seo='Hodge classes on mixed K3 moduli products | Alec Kriebel'
model=dict(schema='private-editorial-page-model-v1',record_id='23204176',sheet_row=191,title=TITLE,seo_title=seo,meta_description=description,author=dict(name='Alec Kriebel',ORCID='https://orcid.org/0009-0001-9320-500X'),doi=api['doi'],doi_url=api['doi_url'],zenodo_record='https://zenodo.org/records/23204176',native_version=None,native_API_version_field_present=False,host_display_version_not_adopted_as_API_version=True,printed_version=None,printed_date='October 6, 2026',publication_date=meta['publication_date'],record_created=api['created'],record_updated=api['updated'],status='Unrefereed, AI-assisted preprint',abstract=abstract,abstract_source='Complete original main.tex abstract; declared TeX accent rendering and whitespace only',abstract_rendering_replacements=replacement,native_Description_source='Native API metadata.description, distinct from manuscript abstract',canonical_url=None,base_url=None,production_url=None,actual_publication_date=None,AA=None,publication_authority=False,robots='noindex, nofollow',deployment_proposal=dict(slug=SLUG,path='/research/'+SLUG+'/',proposed_canonical_url='https://aleckriebel.com/research/'+SLUG+'/',current_public_page_created=False,passive_slug_collision_check_absent=True,future_payloads=['index.html','citation.bib','assets/paper.pdf','assets/source-and-verification.zip'],shared_stylesheet='/research/research.css',requires_separate_root_adoption_staging_publication_and_live_verification=True),native_asset_order=assets,pdf_pages=4,citation_bib='citation.bib',rights=dict(owned_original_text_source_code_notes_results='CC BY 4.0',third_party='Cited third-party works retain authorship and rights',source_statement='Native API license and root scientific review; no invented separate software license'),scientific_scope=dict(coefficients='Rational, all codimensions',bases='Any finite collection of different or repeated complex projective K3 surfaces, with Brauer classes',factors='Actual smooth projective stable twisted-sheaf or generic-stability Bridgeland moduli in precise Bülles Theorem0.1 scope; fixed data and polarization as applicable',hypotheses='Smoothness and projectivity are assumed; no added fine-moduli or primitivity hypothesis',boundaries='Empty factors vacuous; finite smooth zero-dimensional factors componentwise; empty product and Hilbert n=0 points; Hilbert n=1 recovers bases',transfer='Rational Chow split diagonal, actual correspondence codimensions, tensor/exterior-product assembly; no decomposable-class premise',input='Pinned OpenAI Theorem1.1 for arbitrary mixed K3 products; self-power results alone insufficient',limits='No arbitrary K3^[n] deformations, singular/semistable or abelian-surface extension, integral/generalized Hodge, finite-dimensional motives, formal geometry or human peer review'),attribution=['OpenAI pinned mixed-K3 theorem and its CM/KS chain','Bülles Theorem0.1 rational Chow splitting','Arapura earlier conditional/motivated transfers','Markman normalized non-fine diagonal construction'],framing='Explicit assembled corollary, inherited reduction, no independent breakthrough/firstness/substantial independent novelty claim',AI_disclosure='Extensive research/source checks/drafting/verification; unrefereed; automated review is not human peer review',collaboration='Passive substantive verification/exposition/journal work; authorship based on actual contributions',scientific_clearance=dict(inherited=True,new_scientific_review=False,path=str(CLEAR.relative_to(P)),SHA256=inputs[str(CLEAR.relative_to(P))]['SHA256']),follow_up=None,rendered_or_live_certificate=False,tracker_status_not_modified_or_inferred=True)
writej('page-model.json',model)
scholar={'@context':'https://schema.org','@type':'ScholarlyArticle','name':TITLE,'headline':TITLE,'description':description,'abstract':abstract,'author':{'@type':'Person','name':'Alec Kriebel','identifier':model['author']['ORCID']},'datePublished':meta['publication_date'],'dateCreated':api['created'],'dateModified':api['updated'],'creativeWorkStatus':model['status'],'inLanguage':'en','isAccessibleForFree':True,'identifier':{'@type':'PropertyValue','propertyID':'DOI','value':api['doi']},'sameAs':api['doi_url'],'license':'https://creativecommons.org/licenses/by/4.0/','keywords':meta['keywords'],'citation':[x['identifier'] for x in meta['related_identifiers']],'encoding':[{'@type':'MediaObject','name':x['name'],'contentUrl':x['local_path'],'encodingFormat':x['format'],'contentSize':str(x['bytes'])+' bytes','sameAs':x['native_url']} for x in assets]}
metadata=[('description',description),('author','Alec Kriebel'),('robots',model['robots']),('googlebot',model['robots']),('citation_title',TITLE),('citation_author','Kriebel, Alec'),('citation_author_orcid','0009-0001-9320-500X'),('citation_publication_date','2026/10/06'),('citation_date','2026/10/06'),('citation_doi',api['doi']),('citation_pdf_url','assets/paper.pdf'),('citation_language','en'),('DC.title',TITLE),('DC.creator','Alec Kriebel'),('DC.date',meta['publication_date']),('DC.description',abstract),('DC.identifier','doi:'+api['doi']),('DC.type','Text'),('DC.language','en'),('DC.rights','Original text/source/code/notes/results CC BY 4.0; third-party rights retained'),('twitter:card','summary'),('twitter:title',TITLE),('twitter:description',description)]
head='<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>'+html.escape(seo)+'</title>\n'
head+=''.join('<meta name="'+k+'" content="'+html.escape(v,quote=True)+'">\n' for k,v in metadata)
head+=''.join('<meta property="'+k+'" content="'+html.escape(v,quote=True)+'">\n' for k,v in [('og:type','article'),('og:title',TITLE),('og:description',description),('og:site_name','Alec Kriebel'),('article:published_time',meta['publication_date']),('article:modified_time',api['updated'])])
head+='<link rel="stylesheet" href="/research/research.css">\n<script type="application/ld+json">'+json.dumps(scholar,ensure_ascii=False).replace('</','<\\/')+'</script>\n</head>\n'
template=(OWN/'main.template.html').read_text()
assert template.count('@@ABSTRACT@@')==1
main=template.replace('@@ABSTRACT@@',html.escape(abstract))
article='<!doctype html>\n<html lang="en">\n'+head+'<body>\n<a class="skip-link" href="#main">Skip to content</a>\n<header><p class="site-title"><a href="https://aleckriebel.com/">Alec Kriebel</a></p><nav aria-label="Main navigation"><a href="https://aleckriebel.com/">Home</a> · <a href="https://aleckriebel.com/research/">Research</a></nav></header>\n'+main+'<footer><p><a href="https://aleckriebel.com/research/">Research index</a> · <a href="https://orcid.org/0009-0001-9320-500X">ORCID</a></p></footer>\n</body>\n</html>\n'
write('head.html',head)
write('main.html',main)
write('article.html',article)
write('citation.bib','@misc{kriebel2026mixedk3moduli,\n  author = {Kriebel, Alec},\n  title = {Rational Hodge classes on mixed products of {K3} moduli spaces},\n  year = {2026},\n  month = oct,\n  publisher = {Zenodo},\n  doi = {10.5281/zenodo.23204176},\n  url = {https://doi.org/10.5281/zenodo.23204176},\n  note = {Unrefereed, AI-assisted preprint; declared publication date 6 October 2026},\n  license = {CC BY 4.0}\n}\n')

class Inspect(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=[];self.links=[];self.meta={};self.scripts=[];self.abstract=[];self.in_abstract=False;self.in_json=False;self.frames=[];self.styles=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a':self.links.append(a.get('href',''))
        if tag=='link':self.styles.append(a)
        if tag=='meta' and 'name' in a:
            assert a['name'] not in self.meta
            self.meta[a['name']]=a['content']
        if a.get('id')=='abstract-text':self.in_abstract=True
        if tag=='script':
            assert a=={'type':'application/ld+json'}
            self.in_json=True;self.scripts.append('')
        if tag=='iframe':self.frames.append(a)
    def handle_data(self,data):
        if self.in_abstract:self.abstract.append(data)
        if self.in_json:self.scripts[-1]+=data
    def handle_endtag(self,tag):
        if tag=='p':self.in_abstract=False
        if tag=='script':self.in_json=False

check=Inspect();check.feed(article);check.close()
assert len(check.ids)==len(set(check.ids)) and len(check.scripts)==1
assert ''.join(check.abstract)==abstract==check.meta['DC.description']==json.loads(check.scripts[0])['abstract']==model['abstract']
assert json.loads(check.scripts[0])==scholar and '@graph' not in scholar and 'version' not in scholar
assert 'citation_version' not in check.meta and check.meta['robots']=='noindex, nofollow'
assert check.styles==[{'rel':'stylesheet','href':'/research/research.css'}]
assert len(check.frames)==1 and check.frames[0]['src']=='assets/paper.pdf#view=FitH' and check.frames[0]['title']
for link in check.links:
    if link.startswith('#'):assert link[1:] in check.ids
    elif not link.startswith(('https://','http://','/')):assert (OWN/link.split('#',1)[0]).is_file()
assert not re.search(r'<base\b|rel="canonical"|property="og:url"',article)
assert '@@' not in article
after=census(SRC)
assert before==after and css_before==pin(CSS)[0] and not os.path.lexists(collision)
assert inputs=={str(p.relative_to(P)):pin(p)[0] for p in (CLEAR,REVIEW)}
writej('SOURCE_GUARDS_AFTER.json',after)
writej('STATIC_CHECK.json',dict(UTC=utc,complete_original_abstract_equal_visible_DC_single_ScholarlyArticle_model=True,unique_ids=len(check.ids),one_ScholarlyArticle_no_graph=True,no_invented_version=True,local_links_resolve=True,native_PDF_then_ZIP_unchanged=True,PDF_iframe_open_download=True,shared_CSS_unchanged=True,no_actual_canonical_base_production_or_publication_claim=True,source_entire_43_files_7_childdirs_bytes_modes_hidden_empty_exact=True,browser_or_live_verification=False,new_scientific_execution=False))
writej('PREPARATION_RESULT.json',dict(schema='private-editorial-preparation-result-v1',UTC=utc,status='READY_FOR_INDEPENDENT_FACT_AND_ROOT_COPY_REVIEW',completion_percent=90,record_id='23204176',inputs=inputs,source_control_pins=CONTROL_PINS,source_files=43,source_childdirs=7,source_manifest_schema=manifest['schema'],native_asset_order=assets,article=pin(OWN/'article.html')[0],head=pin(OWN/'head.html')[0],main=pin(OWN/'main.html')[0],model=pin(OWN/'page-model.json')[0],builder=pin(OWN/'prepare.py')[0],scientific_clearance_inherited=True,no_new_scientific_programs_run=True,no_W_or_Git_or_Sheet_or_network_actions=True,follow_up=None))
with (OWN/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n'+datetime.datetime.now(datetime.timezone.utc).isoformat()+' — One private preparation completed. Full source43/7 and immutable custody controls verified before/after, assets unchanged, exact original abstract mapped to all four representations, absent API version retained. Completion90%; awaiting personal complete output read and finite seal.\n')
