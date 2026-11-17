"""One fixed private data assembly/static pass; no native science, renderer, network or Git."""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
from urllib.parse import urlsplit, unquote
import datetime, hashlib, json, os, re, stat

R=Path(__file__).resolve().parent
P=R.parents[1]
S=P/'papers/23331540/sources'
F=P/'papers/23331540/reviews/adversarial-sol'
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')

def require(test,message):
    if not test: raise RuntimeError(message)

def pin(p,root=None):
    st=p.lstat(); require(stat.S_ISREG(st.st_mode),'not regular: '+str(p)); b=p.read_bytes()
    return dict(path=p.relative_to(root).as_posix() if root else str(p),bytes=len(b),SHA256=hashlib.sha256(b).hexdigest(),mode=oct(stat.S_IMODE(st.st_mode)))

def normalized(q):
    return dict(q,mode=oct(q['mode']) if isinstance(q['mode'],int) else q['mode'])

def inventory(root):
    files=[];dirs=[]
    for p in sorted(root.rglob('*')):
        st=p.lstat()
        if stat.S_ISREG(st.st_mode): files.append(pin(p,root))
        elif stat.S_ISDIR(st.st_mode): dirs.append(dict(path=p.relative_to(root).as_posix(),mode=oct(stat.S_IMODE(st.st_mode))))
        else: raise RuntimeError('unexpected topology: '+str(p))
    return files,dirs

def create(name,data):
    with (R/name).open('xb') as f: f.write(data.encode('utf-8') if isinstance(data,str) else data)

def create_json(name,value): create(name,json.dumps(value,ensure_ascii=False,indent=2)+'\n')

for n in ('article.html','head.html','research.css','assets','original-objects','SOURCE_GUARDS.json','STATIC_CHECK.json','REPORT.md','MANIFEST.json','FINAL.json'):
    require(not os.path.lexists(R/n),'already exists: '+n)
require(pin(F/'FINAL.json')['SHA256']=='86f026af59ac42c04ad675bb0b823f16838d8df1c3f987085920b756c93cceec','prior review control differs')
require(pin(F/'MANIFEST.json')['SHA256']=='74506aa7169e5b185cff17a0643b7d83ed27fc182601874edafaa1449ee6c412','prior review manifest differs')
old_manifest=json.loads((F/'MANIFEST.json').read_text())
old_pin=next(q for q in old_manifest['payload_files'] if q['path']=='SOURCE_CUSTODY.json')
require(pin(F/'SOURCE_CUSTODY.json',F)==normalized(old_pin),'prior source custody differs')
old=json.loads((F/'SOURCE_CUSTODY.json').read_text())
sf,sd=inventory(S)
require(sf==[normalized(q) for q in old['files']] and sd==[normalized(q) for q in old['directories']],'source bytes/modes/topology differ')
require(oct(stat.S_IMODE(S.lstat().st_mode))==oct(old['root_mode']),'source root mode differs')
require(len(sf)==133 and len(sd)==14,'source finite extent differs')
clearance=P/'verification/root-clearance-23331540-20261116.json'
review=P/'papers/23331540/reviews/root/ROOT_REVIEW.md'
require(pin(clearance)['SHA256']=='4f3f2819ac1faa001448c450c39a2815eb3b115626e7a28b7b7a54a270713022','root clearance differs')
require(pin(review)['SHA256']=='8e58b63db77e0480a880ba1a9aa4c33a553b64954d23c25384f26a0b165d6e99','root report differs')
a=json.loads(clearance.read_text())
require(a['scientific_disposition']=='PASS_FULL_ORIGINAL_FIXED_LABEL_STRESS_PARTITION' and a['publication_or_AA_authority'] is False,'root scope differs')
m=json.loads((R/'page-model.json').read_text()); rec=json.loads((S/'record.response.body').read_text()); n=rec['metadata']
for key in ('title','version','doi','publication_date'):
    require((m['native_version'] if key=='version' else m[key])==n[key],'model/native identity differs: '+key)
require(m['record_created']==rec['created'] and m['record_updated']==rec['updated'],'record dates differ')
require(n['license']['id']=='cc-by-4.0' and m['printed_version'] is None,'rights/printed version differ')
require(all(m[k] is None for k in ('canonical_url','base_url','production_url','AA','follow_up')) and m['publication_authority'] is False,'private/null gate differs')
target=W/'public/research'/m['deployment_proposal']['slug']; require(not os.path.lexists(target),'proposed slug exists')
css=W/'public/research/research.css'; css_pin=pin(css); require(css_pin['bytes']==1170,'shared CSS size differs')
base='published-source/container-001/tree/full_stress_stratifications_v1/'
tex=(S/(base+'research_note.tex')).read_text()
abstract=' '.join(re.search(r'\\begin\{abstract\}\s*(.*?)\s*\\end\{abstract\}',tex,re.S).group(1).replace('~',' ').split())
require(abstract==m['abstract'],'complete original abstract differs')
require([q['name'] for q in m['native_asset_order']]==[q['key'] for q in rec['files']],'native asset order differs')
for d in ('assets','original-objects'): (R/d).mkdir()
copies=[]
for q,r in zip(m['native_asset_order'],rec['files']):
    src=S/'assets'/q['name']; b=src.read_bytes()
    require(len(b)==q['bytes']==r['size'] and 'md5:'+hashlib.md5(b).hexdigest()==q['native_checksum']==r['checksum'],'asset identity differs')
    create(q['local_path'],b)
    require((R/q['local_path']).read_bytes()==b,'asset copy differs')
    copies.append(dict(source=pin(src,S),private_copy=pin(R/q['local_path'],R)))
for source,dest in [('record.response.body','record.json'),('files-23331540.response.body','files.json'),(base+'metadata.json','authored-metadata.json'),(base+'README.md','RIGHTS_README.md')]:
    create('original-objects/'+dest,(S/source).read_bytes())
    copies.append(dict(source=pin(S/source,S),private_copy=pin(R/'original-objects'/dest,R)))
create('research.css',css.read_bytes())

def meta(name,value,prop=False):
    return '<meta '+('property' if prop else 'name')+'="'+escape(name,quote=True)+'" content="'+escape(value,quote=True)+'">'

sch={'@context':'https://schema.org','@type':'ScholarlyArticle','name':m['title'],'headline':m['title'],'description':m['meta_description'],'abstract':m['abstract'],
    'author':{'@type':'Person','name':m['author']['name'],'identifier':m['author']['ORCID'],'affiliation':{'@type':'Organization','name':m['author']['affiliation']}},
    'datePublished':m['publication_date'],'version':m['native_version'],'inLanguage':'en','creativeWorkStatus':m['status'],'isAccessibleForFree':True,
    'identifier':{'@type':'PropertyValue','propertyID':'DOI','value':m['doi']},'sameAs':m['doi_url'],'license':'https://creativecommons.org/licenses/by/4.0/',
    'keywords':n['keywords'],'encoding':[{'@type':'MediaObject','name':q['name'],'contentUrl':q['local_path'],'encodingFormat':q['format'],'contentSize':str(q['bytes'])+' bytes','sameAs':q['native_url']} for q in m['native_asset_order']]}
fields=[('description',m['meta_description']),('author',m['author']['name']),('robots',m['robots']),('googlebot',m['robots']),
    ('citation_title',m['title']),('citation_author',m['author']['name']),('citation_author_orcid',m['author']['ORCID']),
    ('citation_publication_date',m['publication_date'].replace('-','/')),('citation_date',m['publication_date'].replace('-','/')),
    ('citation_version',m['native_version']),('citation_doi',m['doi']),('citation_language','en'),('citation_pdf_url',m['native_asset_order'][0]['local_path']),
    ('DC.title',m['title']),('DC.description',abstract),('DC.date',m['publication_date']),('DC.identifier','doi:'+m['doi']),('DC.rights','CC BY 4.0 as stated in native metadata and authored package'),
    ('twitter:card','summary'),('twitter:title',m['title']),('twitter:description',m['meta_description'])]
head='<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>'+escape(m['seo_title'])+'</title>\n'
head+='\n'.join(meta(k,v) for k,v in fields)+'\n'
head+='\n'.join(meta(k,v,True) for k,v in [('og:type','article'),('og:title',m['title']),('og:description',m['meta_description']),('article:published_time',m['publication_date'])])+'\n'
head+='<link rel="stylesheet" href="research.css">\n<script type="application/ld+json">'+json.dumps(sch,ensure_ascii=False)+'</script>\n</head>\n'
create('head.html',head); main=(R/'public-main.html').read_text()
before='<!DOCTYPE html>\n<html lang="en">\n'+head+'<body>\n<a class="skip-link" href="#main">Skip to content</a>\n<header><p class="site-title"><a href="https://aleckriebel.com/">Alec Kriebel</a></p><nav aria-label="Main navigation"><a href="https://aleckriebel.com/">Home</a> · <a href="https://aleckriebel.com/research/">Research</a></nav></header>\n'
after='<footer><p><a href="https://aleckriebel.com/research/">Research index</a></p><p class="copyright">© 2026 Alec Kriebel</p></footer>\n</body>\n</html>\n'
create('article.html',before+main+after)

class Inspect(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.ids=[];self.links=[];self.meta={};self.abstract=[];self.capture=None;self.iframe=[];self.canonical=[];self.bases=[];self.scripts=[]
    def handle_starttag(self,tag,attrs):
        q=dict(attrs)
        if 'id' in q:self.ids.append(q['id'])
        if q.get('id')=='abstract-text':self.capture=tag
        if tag=='meta':self.meta[q.get('name',q.get('property'))]=q.get('content')
        if tag=='iframe':self.iframe.append(q.get('src'))
        if tag=='link' and q.get('rel')=='canonical':self.canonical.append(q.get('href'))
        if tag=='base':self.bases.append(q)
        if tag=='script':self.scripts.append(q.get('type'))
        for key in ('href','src'):
            if key in q:self.links.append(q[key])
    def handle_endtag(self,tag):
        if tag==self.capture:self.capture=None
    def handle_data(self,data):
        if self.capture:self.abstract.append(data)

html=(R/'article.html').read_text(); v=Inspect(); v.feed(html)
require(len(v.ids)==len(set(v.ids)),'duplicate HTML id')
require(' '.join(''.join(v.abstract).split())==abstract==v.meta['DC.description']==sch['abstract'],'visible/schema/DC abstract differs')
require(v.meta['citation_title']==n['title'] and v.meta['citation_version']==n['version'],'citation identity differs')
require(v.meta['robots']=='noindex, nofollow' and not v.canonical and not v.bases and 'og:url' not in v.meta,'private wrapper differs')
require(not any(k in sch for k in ('url','@id','mainEntityOfPage')),'active production schema identity')
require(v.iframe==[m['native_asset_order'][0]['local_path']] and v.scripts==['application/ld+json'],'reader/script setup differs')
require(re.search(r'<main\b.*?</main>\n?',html,re.S).group(0)==main and re.search(r'<head>.*?</head>\n?',html,re.S).group(0)==head,'whole body/head differs')
for link in v.links:
    u=urlsplit(link)
    if not u.scheme and not u.netloc:
        path=unquote(u.path); require(not path.startswith('/') and '..' not in Path(path).parts,'unexpected local link')
        if path:require((R/path).is_file(),'missing local link: '+link)
        elif u.fragment:require(u.fragment in v.ids,'missing local fragment')
require(v.links.index(m['native_asset_order'][0]['local_path'])<v.links.index(m['native_asset_order'][1]['local_path']),'visible asset order differs')
for forbidden in ('Original Zenodo description','ROOT_REVIEW','INITIAL_SEAL','71280','1099','Example 1.4','erratum','MIT'):
    require(forbidden not in main,'unexpected public narrative: '+forbidden)
bib=(R/'citation.bib').read_text(); require(all(x in bib for x in (n['title'],n['doi'],'{1.0}','12 October 2026')),'Bib native identity differs')
require(pin(css)==css_pin and pin(R/'research.css')['SHA256']==css_pin['SHA256'],'CSS drift')
require(not os.path.lexists(target),'public slug appeared')
af,ad=inventory(S);require(af==sf and ad==sd and stat.S_IMODE(S.lstat().st_mode)==old['root_mode'],'source drift during pass')
for name in ('STATIC_CHECK.stdout.txt','STATIC_CHECK.stderr.txt'):require((R/name).read_bytes()==b'','nonempty literal pass stream')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
create_json('SOURCE_GUARDS.json',dict(UTC=now,source_root=str(S),root_mode=oct(old['root_mode']),files=sf,directories=sd,source133files14dirs_unchanged_before_after=True,
    original_copies=copies,shared_W_css=css_pin,shared_private_css=pin(R/'research.css',R),proposed_slug_absent_before_after=str(target),
    actual_clearance=pin(clearance,P),actual_root_report=pin(review,P),prior_manifest=pin(F/'MANIFEST.json',P),prior_source_custody=pin(F/'SOURCE_CUSTODY.json',P)))
create_json('STATIC_CHECK.json',dict(UTC=now,status='PASS_PRIVATE_DATA_AND_COPY_CONSISTENCY_ONLY',ordinary_passes=1,full_native_abstract_visible_schema_DC_equal=True,
    whole_MAIN_head_exact=True,native_asset_order_bytes_checksums_copies_exact=True,native_metadata_dates_versions_rights_retained=True,
    private_noindex_null_active_canonical_base_production_AA=True,shared1170CSS_exact=True,local_links_ids_valid=True,no_duplicate_Description_internal_audit_narrative=True,
    source_regular_files=len(sf),source_child_directories=len(sd),literal_stdout_bytes=0,literal_stderr_bytes=0,
    source_native_science_old_helper_network_Git_W_Sheet_render_CUA_or_server_actions=False,follow_up=None,
    reader_limit='No new render, native PDF-reader display, live-link/download or deployment certification'))
create('REPORT.md','# Private editorial handoff — row183 /23331540\n\nREADY for independent copy-fidelity review. Whole actual root clearance and10840byte ROOT_REVIEW were read. This is informed editorial work after the writer\'s own full-original adversarial review, not a new scientific family. The source180TeXlines/all3PDFtext pages/fresh own pixels are reused with disclosure; complete native objects and rights were reread.\n\nFull original abstract is present without omission in visible HTML, ScholarlyArticle.abstract and DC.description. Exact simple-graph/fixed-label/n,d≥1/full Cartesian collision-inclusive connected coordinate-sign partition theorem, specified permutation corollary, positive singleton detector, connected nonedge witness and ambient-linear path/star boundary are retained. Panina\'s detector/collinear observations and DKS/Karpenkov framework receive prominent credit. The page makes no arbitrary-ambient, unwritten-intent, exhaustive-priority, human-refereeing or formal-proof claim and omits public internal counts/date logs/external-example disputes. Follow-up is null; collaboration is passive and contribution-based.\n\nOriginal12October2026/native1.0 is distinguished from record creation13OctoberUTC and no printed numeric version. PDF thenZIP bytes/order and actual CC BY4authored-release rights are preserved. No MIT split is inferred. Complete raw native Description/metadata and README rights remain archived rather than duplicated visibly.\n\nThe sole fully read data-only assembly/static pass succeeded with empty literal stdout/stderr. Whole MAIN/head, model/Bib/native identity, local links, shared1170CSS and all133sourcefiles/14dirs were checked before/after. No source/native/old-helper execution, W/Git/Sheet/deploy/render/browser/CUA/server/network mutation or outreach occurred. Proposed /research/full-stress-stratifications-labelled-graph/ was absent readonly; active canonical/base/production/AA remainnull, HTMLnoindex, publicationauthorityfalse.\n\nReader limits: no new article desktop/mobile view, iframe/PDF display, live download or deployment certification. The scientific edition limits in the root report are retained without an external-erratum narrative in public copy; this task did not reacquire or compare primary editions. Final whole assembled HTML/model are for actual reading before handoff. Every owned regular file, ignored/empty stream, hash/mode and child directory is in the finite manifest, excluding only terminal controls themselves. Freeze for independent review; quiescent after FINAL.\n')
with (R/'RESEARCH_LOG.md').open('a') as f:f.write('\n- '+now+' — 100% private preparation: one data-only assembly/static pass completed, literal streams empty; final finite seal and actual HTML/model reading for handoff. No reader/live or production claim.\n')
files,dirs=inventory(R)
create_json('MANIFEST.json',dict(schema='whole-private-editorial-manifest-v1',UTC=now,payload_files=files,directories=dirs,root_mode=oct(stat.S_IMODE(R.lstat().st_mode)),exact_terminal_exclusions=['MANIFEST.json','FINAL.json'],includes_all_ignored_empty_bytes_modes=True))
create_json('FINAL.json',dict(schema='private-editorial-final-v1',UTC=now,record='23331540',row=183,status='FROZEN_PRIVATE_EDITORIAL_READY_FOR_INDEPENDENT_COPY_FACT',
    article=pin(R/'article.html',R),whole_MAIN=pin(R/'public-main.html',R),head=pin(R/'head.html',R),model=pin(R/'page-model.json',R),Bib=pin(R/'citation.bib',R),
    report=pin(R/'REPORT.md',R),manifest=pin(R/'MANIFEST.json',R),source_guards=pin(R/'SOURCE_GUARDS.json',R),static_check=pin(R/'STATIC_CHECK.json',R),actual_authority=pin(clearance,P),
    native_assets=copies[:2],source133files14dirs_unchanged=True,informed_prior_role_disclosed=True,new_scientific_family=False,root_editorial_adoption=False,
    static_passes=1,static_exit=0,literal_stdout=pin(R/'STATIC_CHECK.stdout.txt',R),literal_stderr=pin(R/'STATIC_CHECK.stderr.txt',R),
    canonical_url=None,base_url=None,production_url=None,AA=None,publication_authority=False,follow_up=None,
    no_new_render_reader_live_download_or_deployment_certificate=True,all_writes_confined_to_owned_folder=True,completion_percent_private_editorial=100,
    extent=dict(regular_files=len(files)+2,child_directories=len(dirs),all_paths=sorted([q['path'] for q in files]+['MANIFEST.json','FINAL.json']),directories=dirs),
    all_handles_terminal_at_return=True,quiescent_after_seal=True,terminal_self_hash_excluded=True))
ef,ed=inventory(R);require(len(ef)==len(files)+2 and ed==dirs,'final finite extent drift')
for q in files:require(pin(R/q['path'],R)==q,'owned payload drift while sealing')
