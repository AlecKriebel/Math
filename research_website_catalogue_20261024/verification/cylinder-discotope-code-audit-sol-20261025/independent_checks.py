"""Independent custody/content checks, without renderer or legacy-suite execution."""
from pathlib import Path
from html import unescape,escape
from html.parser import HTMLParser
from io import BytesIO
import ast,datetime,hashlib,json,re,stat,sys,zipfile,xml.etree.ElementTree as ET
from pypdf import PdfReader
A=Path(__file__).resolve().parent;R=A.parents[1];S=R/'verification/local-cylinder-discotope-stage-sol-20261025';LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
sys.path[:0]=[str(S),str(R/'scripts')]
from cylinder_discotope_source import PINS,display_cd_abstract
checks=[];bindings={}
def read(p):
    p=Path(p);b=p.read_bytes();bindings[str(p)]={'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()};return b
def text(p):return read(p).decode()
def obj(p):return json.loads(read(p))
def sha(p):return hashlib.sha256(read(p)).hexdigest()
def check(tag,ok):
    checks.append({'tag':tag,'pass':bool(ok)})
    if not ok:raise RuntimeError(tag)
class Tags(HTMLParser):
    def __init__(self,h):super().__init__();self.tags=[];self.feed(h)
    def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
stage_before=obj(A/'STAGE_BEFORE.json')['bindings']
check('stage_complete_original_inventory',set(stage_before)=={str(p) for p in S.rglob('*') if p.is_file()})
for path,item in stage_before.items():check('original_stage:'+path,sha(path)==item['sha256'] and Path(path).stat().st_size==item['bytes'])
protected=obj(S/'protected-before.json')
for item in protected['files']:check('protected:'+item['path'],sha(item['path'])==item['sha256'] and Path(item['path']).stat().st_size==item['bytes'])
check('current_production_484_files',len([p for p in LIVE.rglob('*') if p.is_file()])==484)
check('old_current_renderer_exact',read(R/'scripts/render_page.py')==read(S/'inputs/render_page.py'))
check('old_current_checker_exact',read(R/'verification/final-content-check.py')==read(S/'inputs/final-content-check.py'))
check('helper_full_new_file_diff',text(S/'new-helper.diff').splitlines()[3:]==['+'+line for line in text(S/'cylinder_discotope_source.py').splitlines()])
rp=text(S/'render_page.proposed.py');rs=text(S/'render_page.stage.py')
check('renderer_only_private_root_overrides',rp.replace('ROOT = Path(__file__).resolve().parents[1]','ROOT = Path('+repr(str(R))+')').replace("SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')",'SITE = Path('+repr(str(S/'public/research'))+')')==rs)
cp=text(S/'final-content-check.proposed.py');cs=text(S/'final-content-check.stage.py')
check('checker_only_private_root_override',cp.replace('R=Path(__file__).resolve().parents[1]','R=Path('+repr(str(R))+')')==cs)
for name in ['cylinder_discotope_source.py','render_page.proposed.py','final-content-check.proposed.py','render_page.stage.py','final-content-check.stage.py']:ast.parse(text(S/name))
check('new_helper_security_guards_survive_optimization',not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(text(S/'cylinder_discotope_source.py')))))
targets=[]
for rid in ['23387774','23074543']:
    p=R/'papers'/rid;c=obj(p/'publication.json');g=obj(p/'promotion.json');raw=obj(p/'sources/receipt.json');api=obj(p/'sources/zenodo-record.raw.json');pin=PINS[rid]
    science=obj(R/('verification/root-clearance-'+rid+'-20261025.json'));ed=obj(R/('verification/root-editorial-'+rid+'-20261025.json'))
    check(rid+':whole_receipt',raw==c['source_binding']['source_receipt_original']==g['source_receipt_original'])
    check(rid+':whole_root_record',science==g['root_clearance_record'])
    check(rid+':literal_case_schema',pin['asset_key'] in raw and not any(k in raw for k in ['files','assets']))
    for role,item in g['reviews'].items():check(rid+':whole_custom_'+role,item['verdict']==obj(p/item['verdict_file']) and sha(p/item['verdict_file'])==item['verdict_sha256']==science['reviews'][role]['verdict_sha256'])
    article=S/'public/research'/c['slug'];h=text(article/'index.html');d=Tags(h);sections=dict(re.findall('<section id="([^"]+)">(.*?)</section>',h,re.S))
    section_paras=lambda sid:[unescape(t) for t in re.findall('<p>(.*?)</p>',sections[sid],re.S)]
    for sid,key in [('plain-language','plain_language'),('result','result'),('proof','why_it_works'),('limits','limitations')]:check(rid+':full_exact_'+sid,section_paras(sid)==c[key])
    check(rid+':full_exact_status',section_paras('status')==[c['status'],c['ai_disclosure']])
    check(rid+':full_abstract',section_paras('abstract')==[display_cd_abstract(rid,c['abstract'])])
    source=text(p/c['source_binding']['source_tex_path']);original=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',source,re.S).group(1)
    check(rid+':original_abstract_actual_TeX',text(p/'reviews/editorial/ORIGINAL_ABSTRACT.tex')==original)
    check(rid+':exact_visible_edition_and_date','</time> · '+escape(c['edition_label'])+' ·' in h and re.search('<time datetime="([^"]+)">([^<]+)</time>',h).groups()==(c['publication_date'],{'23387774':'15 October 2026','23074543':'30 September 2026'}[rid]))
    check(rid+':visible_citation_exact',('('+escape(c['citation_edition_label'])+') [Preprint]') in sections['cite'])
    meta={a.get('name',a.get('property')):a.get('content') for t,a in d.tags if t=='meta'};base='https://aleckriebel.com/research/'+c['slug']+'/'
    for name,value in {'description':c['description'],'citation_title':c['title'],'citation_author':'Alec Kriebel','citation_author_orcid':'0009-0001-9320-500X','citation_doi':c['doi'],'citation_publication_date':c['publication_date'].replace('-','/'),'citation_pdf_url':base+c['pdf_filename'],'og:title':c['title'],'og:description':c['description'],'og:url':base,'article:published_time':c['publication_date']}.items():check(rid+':meta_'+name,meta[name]==value)
    check(rid+':one_iframe',len([1 for t,a in d.tags if t=='iframe'])==1 and [a['src'] for t,a in d.tags if t=='iframe']==[c['pdf_filename']+'#view=FitH'])
    for name in [c['pdf_filename'],c['supplement_filename']]:
        data=read(p/'sources'/name);actual=read(article/name);item=next(x for x in raw[pin['asset_key']] if x['file_object']['key']==name)
        check(rid+':unchanged_asset:'+name,data==actual and len(data)==item['bytes']==item['file_object']['size'] and hashlib.sha256(data).hexdigest()==item[pin['sha_key']] and hashlib.md5(data).hexdigest()==item[pin['md5_key']])
        check(rid+':full_original_API_object:'+name,item['file_object']==next(x for x in api['files'] if x['key']==name))
    check(rid+':actual_page_count',len(PdfReader(BytesIO(read(article/c['pdf_filename']))).pages)==pin['pages'])
    check(rid+':exact_prepared_BibTeX',read(article/'citation.bib')==read(p/'reviews/editorial/citation.bib')==c['bibtex'].encode())
    check(rid+':only_four_article_assets',{x.name for x in article.iterdir() if x.is_file()}=={'index.html','citation.bib',c['pdf_filename'],c['supplement_filename']})
    with zipfile.ZipFile(BytesIO(read(article/c['supplement_filename']))) as z:
        members=[x for x in z.infolist() if not x.is_dir()];check(rid+':safe_unique_complete_ZIP',len(members)==(138 if rid=='23387774' else 87) and len({x.filename for x in members})==len(members) and z.testzip() is None and all(not x.filename.startswith('/') and '..' not in Path(x.filename).parts and not stat.S_ISLNK(x.external_attr>>16) for x in members))
        for entry in members:check(rid+':member:'+entry.filename,read(p/'sources/published-source'/entry.filename)==z.read(entry))
        readers=[x for x in members if x.filename.endswith('.pdf')]
        check(rid+':historical_reader_separated',not readers if rid=='23387774' else len(readers)==1 and len(PdfReader(BytesIO(z.read(readers[0]))).pages)==5 and z.read(readers[0])!=read(article/c['pdf_filename']))
    check(rid+':null_and_false_gates',c['AA'] is g['AA'] is c['follow_up'] is g['follow_up'] is None and all(obj[k] is False for obj in [g,c['review_metadata']] for k in ['rendered_public_copy_approved','local_http_verified','live_http_verified','browser_verified','native_sheet_publication_verified','public_page_published']))
    targets.append({'record_id':rid,'canonical_config_original':c['canonical_url'],'created':api['created'],'declared_date':c['publication_date'],'version':c['version'],'all_actual_asset_objects':api['files'],'root_editorial_production_authority':ed['production_integration_authorized']})
old=text(LIVE/'research/index.html');new=text(S/'public/research/index.html')
oldlis=re.findall('<li>.*?</li>',old,re.S);newlis=re.findall('<li>.*?</li>',new,re.S)
check('all60_old_visible_index_entries_exact_order',len(oldlis)==60 and len(newlis)==62 and newlis[:60]==oldlis)
ilist=lambda h:json.loads(re.search('<script type="application/ld\\+json">(.*?)</script>',h,re.S).group(1))['mainEntity']
check('all60_old_structured_entries_exact_order',ilist(new)['itemListElement'][:60]==ilist(old)['itemListElement'])
urls=lambda p:[x.text for x in ET.fromstring(text(p)).iter() if x.tag.endswith('loc')]
oldurls,newurls=urls(LIVE/'research/sitemap.xml'),urls(S/'public/research/sitemap.xml')
check('all61_old_sitemap_URLs_exact_order',len(oldurls)==61 and len(newurls)==len(set(newurls))==63 and newurls[:61]==oldurls)
equivalence=obj(S/'legacy-renderer-equivalence.json');legacy=obj(S/'legacy-full-proposed.json')
check('recorded_single_old59_suite',len(legacy['papers'])==59 and legacy['status']=='PASS' and sum(len(x['checks']) for x in legacy['papers'].values())==3377)
check('recorded118_renderer_execution_equality',equivalence['complete_renderer_executions']==118 and len(equivalence['comparisons'])==59 and all(x['all_original_and_proposed_output_bytes_equal'] and x['filesystem_output_writes']==0 for x in equivalence['comparisons']))
for record in equivalence['comparisons']:
    for path,item in record['original_read_bindings'].items():check('old_read:'+path,sha(path)==item['sha256'] and Path(path).stat().st_size==item['bytes'])
result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_INDEPENDENT_CONTENT_AND_CUSTODY','checks':checks,'targets':targets,'old59_suite_rerun':False,'renderer_executions':0,'source_program_executions':0,'bindings':bindings}
(A/'INDEPENDENT_CHECKS.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':result['status'],'checks':len(checks),'distinct_inputs_bound':len(bindings)},indent=2))
