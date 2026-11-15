"""Explicit static editorial checks and optional eight small in-memory controls."""
from pathlib import Path
from html.parser import HTMLParser
import argparse
import copy
import hashlib
import html
import io
import json
import platform
import re
import zipfile

HERE = Path(__file__).absolute().parent
PAPER = HERE.parent.parent
PROJECT = PAPER.parent.parent
CC = 'https://creativecommons.org/licenses/by/4.0/'
MIT = 'https://opensource.org/license/mit/'


def require(ok, why):
    if not ok: raise ValueError(why)


def same(a, b):
    return json.dumps(a, ensure_ascii=False, separators=(',', ':')) == json.dumps(b, ensure_ascii=False, separators=(',', ':'))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


class Visible(HTMLParser):
    parents = {'html': {None}, 'head': {'html'}, 'body': {'html'}, 'title': {'head'}, 'meta': {'head'}, 'link': {'head'}, 'script': {'head'}, 'style': {'head'},
        'main': {'body'}, 'article': {'main'}, 'header': {'article'}, 'section': {'article'}, 'h1': {'header'}, 'h2': {'section'},
        'p': {'header','section'}, 'a': {'p','li'}, 'ul': {'section'}, 'li': {'ul'}, 'iframe': {'section'}}

    def __init__(self):
        super().__init__(convert_charrefs=True); self.stack=[]; self.count={}; self.meta=[]; self.links=[]; self.a=[]; self.frames=[]; self.scripts=[]; self.styles=[]; self.title=''; self.doctype=0; self.head_done=False

    def handle_decl(self, decl):
        require(decl.lower()=='doctype html' and not self.stack and not self.count, 'initial HTML doctype');self.doctype+=1

    def handle_starttag(self, tag, attrs):
        parent=self.stack[-1] if self.stack else None;require(tag in self.parents and parent in self.parents[tag], 'unknown/inert/misnested tag '+tag)
        a=dict(attrs);require(len(a)==len(attrs), 'duplicate attrs');require(not any(k.startswith('on') or k in {'hidden','inert','style','aria-hidden','srcdoc'} for k in a), 'hiding/executable attribute')
        allowed={'html':{'lang'},'meta':{'charset','name','property','content'},'link':{'rel','href'},'script':{'type'},'section':{'id'},'a':{'href','download','target','rel'},'iframe':{'class','loading','src','title'}}.get(tag,set())
        require(set(a)<=allowed,'unexpected attributes '+tag)
        if tag in {'html','head','body','main','article','title','h1','iframe','script','style'}:require(self.count.get(tag,0)==0,'unique '+tag)
        if tag=='body':require(self.head_done,'head before body')
        if tag=='script':require(a=={'type':'application/ld+json'},'only head JSON-LD script');self.scripts.append('')
        if tag=='style':self.styles.append('')
        if tag=='meta':self.meta.append(a)
        if tag=='link':self.links.append(a)
        if tag=='a':require(a.get('href','').startswith(('https://','assets/')),'safe actual link');self.a.append(a)
        if tag=='iframe':self.frames.append(a)
        self.count[tag]=self.count.get(tag,0)+1
        if tag not in {'meta','link'}:self.stack.append(tag)

    def handle_endtag(self, tag):
        require(self.stack and self.stack[-1]==tag,'explicit balanced close '+tag);self.stack.pop()
        if tag=='head':self.head_done=True

    def handle_data(self, text):
        parent=self.stack[-1] if self.stack else None
        if parent=='iframe':require(not text.strip(),'iframe raw text must be empty; article cannot be hidden inside it')
        elif parent=='script':self.scripts[-1]+=text
        elif parent=='style':self.styles[-1]+=text
        elif parent=='title':self.title+=text
        elif 'body' not in self.stack:require(not text.strip(),'no outside/head stray text')

    def handle_comment(self, text):raise ValueError('no comment-hidden content')

    def finish(self, text):
        self.feed(text);self.close();require(not self.stack and self.doctype==1,'complete closed document');require(all(self.count.get(x)==1 for x in ['html','head','body','main','article','h1','title','iframe','script','style']),'complete unique visible main/reader/head');return self


def wrappers(obj):
    count=0
    if isinstance(obj,dict):
        if {'path','bytes','SHA256','whole_literal_object'}<=set(obj):
            raw=Path(obj['path']).read_bytes();require(len(raw)==obj['bytes'] and sha(raw)==obj['SHA256'],'original whole wrapper bytes');require(same(json.loads(raw),obj['whole_literal_object']),'original whole wrapper types/key/list order/nulls');count+=1
        for value in obj.values():count+=wrappers(value)
    elif isinstance(obj,list):
        for value in obj:count+=wrappers(value)
    return count


def check(overrides=None):
    overrides=overrides or {}
    def raw(name):return overrides[name] if name in overrides else (HERE/name).read_bytes()
    def obj(name):return json.loads(raw(name))
    pub=obj('config/publication.json');pr=obj('config/promotion.json');protocol=obj('SOURCE_PROTOCOL_BINDINGS.json');source=json.loads((PAPER/'sources/SOURCE_READY.json').read_bytes());root=json.loads((PROJECT/'verification/root-clearance-23570763-20261115.json').read_bytes())
    require(sha((PROJECT/'verification/root-clearance-23570763-20261115.json').read_bytes())=='56a6e20fcef53e11e3cd7ab2bba1ad6503d0720509983be7b60d5a19bd9dc33f','root clearance exact')
    require(pub['publication_date']=='2026-10-22' and pub['version']=='1.0.0' and pub['pdf_pages']==4,'original printed/native date/version/pages')
    require(pub['title']==source['title'] and pub['doi']==source['DOI'],'exact published title and target DOI')
    require(pub['native_record_created']=='2026-10-22T16:11:19.267654+00:00' and pub['native_record_updated']=='2026-10-22T16:11:19.600939+00:00','created/updated remain separate')
    require(pub['license']=='CC BY 4.0' and pub['code_license']=='MIT','actual distinct native licenses')
    require(pub['canonical_url'] is None and pub['AA'] is None and pub['native_sheet_aa_url'] is None and pub['follow_up'] is None,'private canonical/null followup')
    require(all(pr[k] is False for k in ['deployed','live_verified','browser_verified','native_verified','public_page_published','production_integration_authorized','ready_to_publish','canonical_verified']),'publication gates false')
    require(same(pub['source_binding']['whole_original_source_ready'],source) and same(pr['whole_original_source_ready'],source) and same(protocol['original_source_ready']['whole_literal_object'],source),'whole historical READY unchanged')
    require(source['printed_date'] is None and source['printed_version'] is None and source['mathematical_PDF_TeX_or_pixels_read'] is False,'historical acquisition null/unread fields not rewritten')
    require(type(protocol['transport_aggregate']['whole_literal_object']) is list and len(protocol['transport_objects'])==7 and len(protocol['native_API_objects'])==4,'actual7-list/4-API objects')
    wcount=wrappers(protocol)
    require(pub['source_binding']['source_protocol_binding_sha256']==sha(raw('SOURCE_PROTOCOL_BINDINGS.json')),'whole native sidecar byte binding')
    adapter=obj('SCHEMA_ADAPTER.json');require(same(adapter['whole_original_source_binding'],pub['source_binding']) and same(adapter['whole_original_review_metadata'],pub['review_metadata']),'nested adapter whole source/review equality')
    verdicts=pub['review_metadata']['whole_original_two_scientific_custom_verdicts'];require(len(verdicts)==2 and same(verdicts,pr['whole_original_two_scientific_custom_verdicts']) and same(verdicts,protocol['whole_original_two_science_verdicts']),'exactly two complete distinct science verdicts')
    require(same(verdicts[0]['whole_literal_object'],root['whole_independent_scope_VERDICT']) and same(verdicts[1]['whole_literal_object'],root['whole_independent_adversarial_VERDICT']),'actual complete custom verdicts, not generic PASS')
    # Independent, declared transcription of the full original abstract, without importing the preparer.
    tex=Path(source['controlling_TeX']['extracted_path']).read_text();abstract=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1)
    for before,after in [(r'$p$','p'),(r'$n\geq2$','n ≥ 2'),(r'$p\nmid n-1$','p ∤ n − 1'),(r'$\mathbb F_p(t)$','𝔽ₚ(t)'),('R\\"omer','Römer')]:abstract=abstract.replace(before,after)
    require(pub['abstract']==' '.join(abstract.split()),'every original abstract word/math symbol retained')
    text=raw('candidate/index.html').decode();dom=Visible().finish(text);main=raw('PUBLIC_MAIN.html').decode().rstrip('\n')
    require(re.findall(r'<main>.*?</main>',text,re.S)==[main] and text[text.index('<body>'):]=='<body>\n'+main+'\n</body></html>\n','entire visible main and no alternative body')
    for key in ['abstract','plain_language','result','why_it_works','limitations','background','collaboration','status','ai_disclosure','rights_notice','reader_intro']:
        vals=pub[key] if isinstance(pub[key],list) else [pub[key]]
        for value in vals:require('<p>'+html.escape(value,quote=True)+'</p>' in main,'complete public paragraph '+key)
    scope=' '.join(pub['result']+pub['why_it_works']+pub['limitations']+pub['background'])
    for fragment in ['every field K and every n ≥ 2','every field extension','Width one is a separate case','every n ≥ 3','single fixed infinite field','every k ≥ 1','arbitrary linear form','including in characteristic two','every choice of coefficients','no negative answer','1594–1596','1544–1545','general (r,d)-symmetric ideal','n ≥ max{d + 1','r ≤ P(d)','Construction 6.8','18 June 2025','19 June 2025']:
        require(fragment in scope,'required full-scope/credit boundary '+fragment)
    names={m['name']:m['content'] for m in dom.meta if 'name' in m};props={m['property']:m['content'] for m in dom.meta if 'property' in m}
    require(len(names)==len([m for m in dom.meta if 'name' in m]) and len(props)==len([m for m in dom.meta if 'property' in m]),'unique named/property metadata')
    require([m for m in dom.meta if 'charset' in m]==[{'charset':'utf-8'}] and names['viewport']=='width=device-width,initial-scale=1','UTF8 and responsive viewport')
    require(dom.title==pub['seo']['title'] and names['description']==pub['description'] and names['robots']=='noindex,nofollow','complete private SEO')
    require({k:names[k] for k in ['citation_title','citation_author','citation_author_orcid','citation_publication_date','citation_version','citation_doi','citation_pdf_url']}=={'citation_title':pub['title'],'citation_author':pub['author'],'citation_author_orcid':pub['orcid'],'citation_publication_date':'2026/10/22','citation_version':'1.0.0','citation_doi':pub['doi'],'citation_pdf_url':'assets/'+pub['pdf_filename']},'original scholarly citation metadata')
    require(props=={'og:type':'article','og:title':pub['title'],'og:description':pub['description'],'og:url':pub['proposed_canonical_url']},'OG proposal')
    require(dom.links==[{'rel':'canonical','href':pub['proposed_canonical_url']}],'canonical proposal only')
    expected_css='body{font-family:Arial,Helvetica,sans-serif;color:#111;background:#fff;max-width:850px;margin:0 auto;padding:26px 20px;line-height:1.6}h1{line-height:1.2;font-size:2rem}h2{line-height:1.3;margin-top:2.1rem;font-size:1.3rem}p,a{overflow-wrap:anywhere}a{color:#24558b}.paper-pdf{display:block;width:100%;height:80vh;min-height:500px;max-height:1000px;border:1px solid #ccc;box-sizing:border-box}li{margin:.5em 0}@media(max-width:600px){body{padding:20px 15px}h1{font-size:1.65rem}}'
    require(dom.styles==[expected_css],'exact plain nonhiding white Arial CSS')
    graph=json.loads(dom.scripts[0]);page,article=graph['@graph'];require(page['dateModified']=='2026-11-15' and article['datePublished']=='2026-10-22' and article['version']=='1.0.0','page date distinct from original edition')
    require(article['abstract']==pub['abstract'] and article['license']==CC and article['identifier']['value']==pub['doi'],'full scholarly abstract/rights/DOI')
    require([x['encodingFormat'] for x in article['encoding']]==['application/zip','application/pdf'] and article['encoding'][0]['license']==[CC,MIT] and article['encoding'][1]['license']==CC,'native encoding order and actual mixed package licenses')
    for x,a in zip(article['encoding'],source['all_native_assets_in_original_order']):require(x['contentUrl']==a['original_api_file_object']['links']['self'],'actual native source links')
    url=pub['proposed_canonical_url'];require(set(graph)=={'@context','@graph'} and graph['@context']=='https://schema.org' and len(graph['@graph'])==2,'complete structured graph')
    require(page=={'@type':'WebPage','@id':url+'#page','url':url,'name':pub['title'],'dateModified':'2026-11-15','mainEntity':{'@id':url+'#article'}},'private WebPage proposal')
    expected_article={'@type':'ScholarlyArticle','@id':url+'#article','headline':pub['title'],'name':pub['title'],'description':pub['description'],'abstract':pub['abstract'],'author':{'@type':'Person','name':pub['author'],'sameAs':pub['orcid']},'datePublished':'2026-10-22','version':'1.0.0','creativeWorkStatus':'Unrefereed preprint','identifier':{'@type':'PropertyValue','propertyID':'DOI','value':pub['doi']},'sameAs':'https://doi.org/'+pub['doi'],'license':CC,'keywords':pub['keywords'],'encoding':article['encoding']}
    require(article==expected_article,'complete original scholarly identity/description/author/status')
    require(dom.frames==[{'class':'paper-pdf','loading':'lazy','src':'assets/'+pub['pdf_filename']+'#view=FitH','title':pub['title']+' — complete four-page PDF'}],'actual complete four-page reader')
    for name in [pub['pdf_filename'],pub['supplement_filename'],'citation.bib']:require(any(a.get('href')=='assets/'+name and 'download' in a for a in dom.a),'actual local download '+name)
    for a in source['all_native_assets_in_original_order']:
        name=a['original_api_file_object']['key'];data=raw('candidate/assets/'+name);require(data==Path(a['path']).read_bytes() and sha(data)==a['SHA256'],'unchanged complete native asset')
    require(raw('citation.bib')==raw('candidate/assets/citation.bib')==pub['prepared_bibtex'].encode(),'complete prepared BibTeX')
    archive=zipfile.ZipFile(io.BytesIO(raw('candidate/assets/'+pub['supplement_filename'])));members=[m for m in archive.infolist() if not m.is_dir()];require(len(members)==18 and archive.testzip() is None,'complete18 CRC-checked ZIP payloads')
    embedded=[m for m in members if m.filename.endswith('/paper.pdf')];require(len(embedded)==1 and archive.read(embedded[0])==raw('candidate/assets/'+pub['pdf_filename']),'original embedded PDF byte identity')
    require('Follow-up' not in main and 'proof development and reconstruction' in main,'null followup and extensive AI disclosure')
    require(pr['publication_sha256']==sha(raw('config/publication.json')),'nested publication/promotion binding')
    return {'status':'PASS_PRIVATE_EDITORIAL_ONLY','python':platform.python_version(),'optimized':not __debug__,'whole_native_wrappers_authenticated':wcount,'whole_science_verdicts':2,'source_transports':7,'native_API_objects':4,'PDF_pages':4,'complete_ZIP_payloads':18,'no_scientific_replay':True,'no_production_or_native_verification_claim':True}


def small_controls():
    results=[];page=(HERE/'candidate/index.html').read_bytes()
    def reject(name,overrides):
        try:check(overrides)
        except (ValueError,KeyError,TypeError,IndexError) as error:results.append({'case':name,'rejected':True,'reason':str(error)})
        else:raise ValueError('unrejected small control '+name)
    reject('outer_template_hides_body',{'candidate/index.html':page.replace(b'<body>',b'<template><body>',1)})
    reject('article_inside_iframe_rawtext',{'candidate/index.html':page.replace(b'<article>',b'<iframe class="paper-pdf" loading="lazy" src="assets/x.pdf" title="hidden"><article>',1)})
    reject('hiding_CSS_added',{'candidate/index.html':page.replace(b'</style>',b'main{height:0;overflow:clip}</style>',1)})
    start=page.index(b'<section id="abstract">');damaged=page[:start]+page[start:].replace(b'classification over every field extension',b'classification over some extensions',1)
    reject('full_abstract_word_removed',{'candidate/index.html':damaged})
    pub=json.loads((HERE/'config/publication.json').read_bytes());pub['code_license']='CC BY 4.0';reject('invented_uniform_code_license',{'config/publication.json':json.dumps(pub,ensure_ascii=False).encode()})
    protocol=json.loads((HERE/'SOURCE_PROTOCOL_BINDINGS.json').read_bytes());protocol['original_source_ready']['whole_literal_object']['printed_date']='2026-10-22';reject('historical_READY_null_normalized',{'SOURCE_PROTOCOL_BINDINGS.json':json.dumps(protocol,ensure_ascii=False).encode()})
    pub=json.loads((HERE/'config/publication.json').read_bytes());pub['review_metadata']['whole_original_two_scientific_custom_verdicts'][0]['whole_literal_object']={'verdict':'PASS'};reject('generic_scientific_PASS_substitution',{'config/publication.json':json.dumps(pub,ensure_ascii=False).encode()})
    name='candidate/assets/periodic-lefschetz-source-and-verification.zip';reject('original_ZIP_truncated',{name:(HERE/name).read_bytes()[:-1]})
    return {'cases':results,'all8_rejected':len(results)==8,'faults_in_memory_only':True,'no_program_or_old_campaign_execution':True}


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--small-controls',action='store_true');args=ap.parse_args();result=check()
    if args.small_controls:result['optional_small_controls']=small_controls()
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
