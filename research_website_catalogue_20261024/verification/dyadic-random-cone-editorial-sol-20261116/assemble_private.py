"""One private data-only assembly; no native execution, rendering or network."""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
import datetime, hashlib, json, os, re, stat

OWN = Path(__file__).resolve().parent
P = OWN.parents[1]
SOURCE = P/'papers/23205181/sources'
TREE = SOURCE/'published-source/container-001/tree'
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
GUARD = P/'papers/23205181/reviews/scope-sol/INITIAL_SOURCE_GUARDS.json'
CLEARANCE = P/'verification/root-clearance-23205181-20261116.json'
ROOT_REVIEW = P/'papers/23205181/reviews/root/ROOT_REVIEW.md'

def pin(p):
    s=p.lstat()
    if not stat.S_ISREG(s.st_mode):
        raise ValueError('Not a regular file: '+str(p))
    b=p.read_bytes()
    return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest(),'mode':stat.S_IMODE(s.st_mode)}

def source_guard():
    g=json.loads(GUARD.read_text())
    files,dirs=[],[]
    for base,names,leaves in os.walk(SOURCE,followlinks=False):
        for name in names:
            p=Path(base)/name
            if p.is_symlink():
                raise ValueError('Source symlink')
            dirs.append({'path':p.relative_to(SOURCE).as_posix(),'mode':stat.S_IMODE(p.stat().st_mode)})
        for name in leaves:
            p=Path(base)/name
            files.append({'path':p.relative_to(SOURCE).as_posix(),**pin(p)})
    files.sort(key=lambda x:x['path']); dirs.sort(key=lambda x:x['path'])
    assert files==g['files'] and dirs==g['directories']
    assert len(files)==69 and len(dirs)==10
    return {'files':69,'child_directories':10,'all_bytes_modes_topology_exact':True,'guard':{'path':str(GUARD),**pin(GUARD)}}

def write(p,b):
    assert p.is_relative_to(OWN)
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:
        f.write(b)

def write_json(p,obj):
    write(p,(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode())

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=[]; self.links=[]; self.meta={}; self.abstract=[]; self.in_abstract=False
        self.iframe=[]; self.stack=[]; self.schema=[]; self.in_schema=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
            if a['id']=='original-abstract': self.in_abstract=True
        if tag=='p' and self.in_abstract: self.abstract_depth=len(self.stack)
        for k in ('href','src'):
            if k in a: self.links.append(a[k])
        if tag=='meta': self.meta[a.get('name',a.get('property'))]=a.get('content')
        if tag=='iframe': self.iframe.append(a)
        if tag=='script' and a.get('type')=='application/ld+json': self.in_schema=True
        if tag not in {'meta','link','br','hr','img','input','source','wbr'}: self.stack.append(tag)
    def handle_endtag(self,tag):
        if self.in_abstract and tag=='p': self.in_abstract=False
        if tag=='script': self.in_schema=False
        assert self.stack and self.stack.pop()==tag, 'Unbalanced '+tag
    def handle_data(self,data):
        if self.in_abstract: self.abstract.append(data)
        if self.in_schema: self.schema.append(data)

def main():
    assert pin(CLEARANCE)['SHA256']=='0630fbf063143c523587b695fcd35a395358a2ef3a1e5968bb83f1910ec054f5'
    assert pin(ROOT_REVIEW)['bytes']==11644 and pin(ROOT_REVIEW)['SHA256']=='e1df8634d4d788c9ebccfb1ce5c8acc937d32d1a446737a98e052a6e83b9d34b'
    authority=json.loads(CLEARANCE.read_text())
    assert authority['full_original_no_repair_or_narrowing'] is True
    assert authority['publication_or_AA_authority'] is False
    before=source_guard()
    editorial=json.loads((OWN/'EDITORIAL.json').read_text())
    assert editorial['slug']=='sharp-dyadic-threshold-random-cone'
    assert all(editorial[k] is None for k in ['canonical_url','base_url','production_url','AA','follow_up'])
    assert not editorial['publication_authority']
    proposed=W/'public/research'/editorial['slug']
    assert not proposed.exists() and not proposed.is_symlink()
    record=json.loads((SOURCE/'record.response.body').read_bytes())
    inventory=json.loads((SOURCE/'files-23205181.response.body').read_bytes())
    m=record['metadata']
    assert m['title']==editorial['title'] and m['version']==editorial['native_version']
    assert m['publication_date']==editorial['publication_date']
    assert m['license']=={'id':'cc-by-4.0'}
    assert [f['key'] for f in record['files']]==['paper.pdf','source-and-audit.zip']
    assert [f['key'] for f in inventory['entries']]==['paper.pdf','source-and-audit.zip']
    tex=(TREE/'main.tex').read_text()
    abstract_tex=re.search(r'\\begin\{abstract\}\n(.*?)\\end\{abstract\}',tex,re.S).group(1)
    abstract=re.sub(r'\s+',' ',abstract_tex.replace('$','').replace(r'\ge','≥')).strip()
    main=(OWN/'MAIN.html').read_text()
    assert m['description'] not in main
    article=OWN/'candidate/research'/editorial['slug']
    targets=[article/'index.html',article/'paper.pdf',article/'source-and-audit.zip',article/'citation.bib',OWN/'candidate/research/research.css',OWN/'HEAD.html',OWN/'MODEL.json',OWN/'SOURCE_AUTHORITY.json',OWN/'BUILD_RECEIPT.json']
    assert not (OWN/'candidate').exists()
    assert all(not p.exists() for p in targets)
    assets=[]
    for f in inventory['entries']:
        p=SOURCE/'assets'/f['key']; actual=pin(p)
        assert actual['bytes']==f['size']
        assert 'md5:'+hashlib.md5(p.read_bytes()).hexdigest()==f['checksum']
        assets.append({'name':f['key'],'source':str(p),**actual,'MD5':f['checksum'],'native_content_url':f['links']['content'],'native_mimetype':f['mimetype']})
    css=W/'public/research/research.css'; css_pin=pin(css)
    assert css_pin['bytes']==1170
    schema={'@context':'https://schema.org','@type':'ScholarlyArticle','name':editorial['title'],'headline':editorial['title'],
        'author':{'@type':'Person','name':editorial['author'],'identifier':editorial['ORCID']},
        'datePublished':m['publication_date'],'dateCreated':record['created'],'version':m['version'],
        'identifier':record['doi_url'],'abstract':abstract,'inLanguage':'en','creativeWorkStatus':editorial['status'],
        'license':'https://creativecommons.org/licenses/by/4.0/','isAccessibleForFree':True,
        'encoding':[{'@type':'MediaObject','contentUrl':a['native_content_url'],'encodingFormat':a['native_mimetype']} for a in assets]}
    tags=[('description',editorial['description']),('author',editorial['author']),('robots','noindex,nofollow'),
        ('citation_title',editorial['title']),('citation_author',editorial['author']),('citation_author_orcid',editorial['ORCID']),
        ('citation_publication_date',m['publication_date'].replace('-','/')),('citation_version',m['version']),
        ('citation_doi',record['doi']),('citation_pdf_url',assets[0]['native_content_url']),
        ('DC.title',editorial['title']),('DC.creator',editorial['author']),('DC.date',m['publication_date']),
        ('DC.identifier','doi:'+record['doi']),('DC.rights',editorial['rights']),('DC.description',abstract),
        ('twitter:card','summary'),('twitter:title',editorial['title']),('twitter:description',editorial['description'])]
    head='<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    head+='<title>'+escape(editorial['title'])+' | Alec Kriebel</title>\n'
    head+=''.join('<meta name="'+escape(k)+'" content="'+escape(v,quote=True)+'">\n' for k,v in tags)
    head+='<link rel="stylesheet" href="../research.css">\n'
    head+='<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False,indent=2).replace('</','<\\/')+'</script>\n'
    head+=''.join('<meta property="'+k+'" content="'+escape(v,quote=True)+'">\n' for k,v in [('og:type','article'),('og:title',editorial['title']),('og:description',editorial['description'])])
    header='<a class="skip-link" href="#main">Skip to main content</a>\n<header><p class="site-title"><a href="/">Alec Kriebel</a></p><nav aria-label="Main navigation"><a href="/">Home</a> · <a href="/research/">Research</a></nav></header>\n'
    footer='<footer><p><a href="/research/">Research</a> · <a href="https://orcid.org/0009-0001-9320-500X">Alec Kriebel’s ORCID</a></p></footer>\n'
    page='<!doctype html>\n<html lang="en">\n<head>\n'+head+'</head>\n<body>\n'+header+main+footer+'</body>\n</html>\n'
    parsed=Page(); parsed.feed(page); parsed.close()
    assert not parsed.stack and len(parsed.ids)==len(set(parsed.ids))
    assert ''.join(parsed.abstract)==abstract
    assert parsed.meta['DC.description']==abstract and json.loads(''.join(parsed.schema))['abstract']==abstract
    assert parsed.meta['robots']=='noindex,nofollow'
    assert '<base' not in page and 'rel="canonical"' not in page and 'og:url' not in page
    assert not any(k in schema for k in ['url','@id','mainEntityOfPage'])
    assert len(parsed.iframe)==1 and parsed.iframe[0]['src']=='paper.pdf#view=FitH'
    assert main.count('id="original-abstract"')==1 and main.count('id="native-assets"')==1
    assert main.index('>paper.pdf</a>')<main.index('>source-and-audit.zip</a>')
    for required in ['q=32','532','ab=1','ac=0','c≠0','e=1−ba','e≠0,1','S<sub>S</sub> ≅ S<sub>S</sub> ⊕ P','[P]=0','characteristic-two','OpenAI','MIT','contributed']:
        assert required in main, required
    write(article/'index.html',page.encode())
    write(OWN/'HEAD.html',head.encode())
    for a in assets:
        write(article/a['name'],Path(a['source']).read_bytes())
        assert pin(article/a['name'])=={k:a[k] for k in ['bytes','SHA256','mode']}
    write(article/'citation.bib',(OWN/'citation.bib').read_bytes())
    write(OWN/'candidate/research/research.css',css.read_bytes())
    for link in parsed.links:
        if link.startswith(('https://','http://','/')): continue
        path,_,fragment=link.partition('#')
        if path:
            assert (article/path).resolve().is_relative_to(OWN)
            assert (article/path).is_file(),link
        else: assert fragment in parsed.ids,link
    assert pin(css)==css_pin and not proposed.exists()
    after=source_guard()
    model={**editorial,'proposed_path':'/research/'+editorial['slug']+'/',
        'private_article_path':str((article/'index.html').relative_to(OWN)),
        'native_abstract_tex':abstract_tex,'complete_original_abstract':abstract,
        'native_metadata':m,'native_record_created':record['created'],'native_record_updated':record['updated'],
        'native_files_returned_order':assets,'native_files_explicit_order_value':inventory['order'],
        'printed_date':'October 6, 2026','printed_numeric_version':None,'PDF_pages':7,
        'schema':schema,'head_private_robots':'noindex,nofollow','source69_10_unchanged':True,
        'browser_render_native_download_live_checks':None,'collaboration':'Passive, substantive work; authorship according to actual contribution.'}
    write_json(OWN/'MODEL.json',model)
    write_json(OWN/'SOURCE_AUTHORITY.json',{'root_clearance':{'path':str(CLEARANCE),**pin(CLEARANCE)},
        'root_review':{'path':str(ROOT_REVIEW),**pin(ROOT_REVIEW)},'record':{'path':str(SOURCE/'record.response.body'),**pin(SOURCE/'record.response.body')},
        'files_API':{'path':str(SOURCE/'files-23205181.response.body'),**pin(SOURCE/'files-23205181.response.body')},
        'controlling_TeX':{'path':str(TREE/'main.tex'),**pin(TREE/'main.tex')},'native_record':record,'native_files_API':inventory,
        'rights_files':[{'path':str(TREE/n),**pin(TREE/n)} for n in ['LICENSES.md','LICENSE_CODE.txt','sources/UPSTREAM_LICENSE.txt']],
        'source_before':before,'source_after':after,'shared_css':{'path':str(css),**css_pin},
        'proposed_website_path_observed_absent':str(proposed),'prior_role':'Opaque source intake, then independent source-first scope reviewer; informed editorial author.'})
    outputs=[p for p in targets if p.name!='BUILD_RECEIPT.json']
    write_json(OWN/'BUILD_RECEIPT.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PRIVATE_DATA_ASSEMBLY_AND_STATIC_CHECKS_PASS',
        'outputs':[{'path':str(p.relative_to(OWN)),**pin(p)} for p in outputs],
        'MAIN':pin(OWN/'MAIN.html'),'EDITORIAL':pin(OWN/'EDITORIAL.json'),'citation':pin(OWN/'citation.bib'),
        'full_abstract_visible_schema_DC_exact':True,'native_asset_order_MD5_SHA_wholebytes_exact':True,
        'local_asset_and_fragment_references_resolve':True,'unique_ids_balanced_HTML':True,
        'source_before':before,'source_after':after,'shared_css_unchanged':True,'proposed_slug_absent':True,
        'noindex_and_inactive_canonical_base_AA_production':True,'native_science_old_helper_or_render_execution':False,
        'browser_PDF_mobile_download_live_certification':False,'publication_authority':False})
    print(json.dumps({'status':'PRIVATE_STATIC_PASS','article':str((article/'index.html').relative_to(OWN)),'native_assets':len(assets),'source_unchanged':True}))

if __name__=='__main__':
    main()
