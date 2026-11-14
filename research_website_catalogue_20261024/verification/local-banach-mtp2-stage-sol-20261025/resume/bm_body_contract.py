"""Whole visible-body contract from approved fields and fixed labels, independent of generated HTML."""
from datetime import date
from abm_body_contract import BodyText
from pathlib import Path
from html.parser import HTMLParser
from html import unescape
from urllib.parse import urlsplit, unquote
from collections import Counter
import hashlib, json, re
from banach_mtp2_source import banach_mtp2_source_view, normalize_bm_abstract, STATUSES, same

def expected_body(c):
    dt=date.fromisoformat(c['publication_date']);day=f'{dt.day} {dt.strftime("%B %Y")}';doi='https://doi.org/'+c['doi'];author='; '.join(c.get('authors',[c['author']]))
    words=['Skip to content','Alec Kriebel','Research | Blog | ORCID',c['title'],f"By {author}, independent researcher. {c['publication_date_label']} {day} · {c['edition_label']} · Unrefereed preprint",f"Read the paper (PDF, {c['pdf_pages']} pages) · {c['supplement_label']} · Zenodo record · CC BY 4.0",'Plain-English explanation · Read on this page · Collaboration',c['abstract_heading'],c['abstract'],'The idea in plain English',*c['plain_language'],'The precise result',*c['result'],'Why the result holds',*c['why_it_works'],'Scope and limitations',*c['limitations'],'Status and AI use',c['status'],c['ai_disclosure']]
    if c.get('edition_note'):words.append(c['edition_note'])
    words+=['Read the paper',c['reader_intro'],'Open PDF · Download PDF · Download original PDF from Zenodo','Supporting materials','Download complete ZIP · Download original complete ZIP from Zenodo']
    words += [x['label'] for x in c['related_resources']]
    if c['source_binding']['record_id']==23217863:words+=['Licensing',c['license'],c['license_note']]
    words+=['Collaborate on this result',c['collaboration'],'Authorship and responsibilities would be discussed in relation to the substantive contributions made.','Contact Alec','Cite this paper',f"{author}. ({dt.year}). {c['title']} ({c['citation_edition_label']}) [Preprint]. Zenodo. {doi}",'Download BibTeX','Background and prior work']
    words += [x['title']+(' : '+x['note'] if x.get('note') else '') for x in c['background']]
    words+=['Research home | me@aleckriebel.com','© 2013–2026 Kriebel LLC.']
    return ' '.join(' '.join(words).split())

class StrictMarkup(HTMLParser):
    """Closed static article grammar; reject hidden and active article content.

    This is deliberately narrower than browser CSS visibility. The sole stylesheet
    remains the separately pinned production CSS; native PDF/browser gates remain.
    """
    def __init__(self,html):
        super().__init__(convert_charrefs=True);self.tags=[];self.faults=[];self.body=False;self.stack=[];self.feed(html)
        if self.stack:self.faults.append('unclosed_document_tags')
    def handle_starttag(self,t,attrs):
        parent=self.stack[-1] if self.stack else None
        parents={'html':{None},'head':{'html'},'body':{'html'},'meta':{'head'},'link':{'head'},'title':{'head'},'script':{'head'},'a':{'body','p','nav','h1','li'},'header':{'body','article'},'p':{'header','section','article','footer'},'nav':{'header'},'main':{'body'},'article':{'main'},'h1':{'header'},'h2':{'section'},'br':{'p'},'time':{'p'},'strong':{'p'},'hr':{'article','footer'},'section':{'article'},'iframe':{'section'},'ul':{'section'},'li':{'ul'},'i':{'p'},'footer':{'body'}}
        if t not in parents or parent not in parents[t]:self.faults.append('unexpected_document_nesting:'+str(parent)+'/'+t)
        if t not in {'meta','link','br','hr'}:self.stack.append(t)
        if t=='body':self.body=True
        a=dict(attrs);self.tags.append((t,a))
        if t=='style':self.faults.append('unexpected_inline_stylesheet')
        if len(a)!=len(attrs):self.faults.append('duplicate_attribute')
        if any(k in a for k in ('hidden','inert','style','aria-hidden')) or any(k.startswith('on') for k in a):self.faults.append('visibility_or_event_attribute')
        if 'class' in a and a['class'] not in ('skip-link','site-title','entry-meta','paper-pdf','copyright'):self.faults.append('unknown_class')
        if self.body and t not in {'body','a','header','p','nav','main','article','h1','h2','br','time','strong','hr','section','iframe','ul','li','i','footer'}:self.faults.append('unexpected_body_tag:'+t)
        allowed={'html':{'lang'},'meta':{'charset','name','property','content'},'link':{'rel','href'},'script':{'type'},'a':{'class','href','download'},'p':{'class'},'nav':{'aria-label'},'main':{'id'},'time':{'datetime'},'section':{'id'},'iframe':{'class','src','title','loading'}}.get(t,set())
        if set(a)-allowed:self.faults.append('unexpected_attribute:'+t)
    def handle_endtag(self,t):
        if not self.stack or self.stack[-1]!=t:self.faults.append('unbalanced_document_tag:'+t)
        else:self.stack.pop()
        if t=='body':self.body=False
    def handle_comment(self,text):self.faults.append('unexpected_document_comment')
    def handle_data(self,text):
        if text.strip() and (not self.stack or self.stack[-1] in {'html','head'}):self.faults.append('unexpected_document_text')

def check_bm_page(programme,site,rid,index,sitemap):
    """Read authenticated originals, then independently compare real public DOM."""
    from pypdf import PdfReader
    paper=programme/'papers'/rid;c=json.loads((paper/'publication.json').read_bytes());g=json.loads((paper/'promotion.json').read_bytes())
    raw,receipt,asset_root=banach_mtp2_source_view(paper,c,g)
    out=site/'research'/c['slug'];f=out/'index.html';html=f.read_text();body=BodyText(html);markup=StrictMarkup(html);tags=markup.tags
    checks={};test=lambda k,v:checks.__setitem__(k,bool(v));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    base='https://aleckriebel.com/research/'+c['slug']+'/';prefix='/research/'+c['slug']+'/' if rid=='23146753' else ''
    test('exact_whole_approved_body_text',body.bodies==1 and body.text==expected_body(c))
    test('closed_static_visible_article_grammar',not markup.faults and sum(t=='article' for t,a in tags)==1 and sum(t=='main' for t,a in tags)==1)
    test('single_ordered_document_roots',[t for t,a in tags if t in {'html','head','body'}]==['html','head','body'])
    test('exact_single_h1',body.headings==[c['title']])
    test('exact_visible_time_date',[a for t,a in tags if t=='time']==[{'datetime':c['publication_date']}])
    test('exact_class_placements',[(t,a) for t,a in tags if 'class' in a]==[('a',{'class':'skip-link','href':'#main'}),('p',{'class':'site-title'}),('p',{'class':'entry-meta'}),('iframe',{'class':'paper-pdf','src':c['pdf_filename']+'#view=FitH','title':c['title']+f" — complete {c['pdf_pages']}-page paper",'loading':'lazy'}),('p',{'class':'copyright'})])
    expected_sections=['abstract','plain-language','result','proof','limits','status','paper','materials']+(['licensing'] if rid=='23217863' else [])+['collaborate','cite','background']
    test('exact_section_order',[a.get('id') for t,a in tags if t=='section']==expected_sections)
    for sid,key in [('abstract','abstract'),('plain-language','plain_language'),('result','result'),('proof','why_it_works'),('limits','limitations'),('status',None),('collaborate',None),('licensing',None)]:
        if sid=='licensing' and rid!='23217863':continue
        part=re.findall(r'<section id="'+sid+r'">(.*?)</section>',html,re.S)
        paras=[unescape(x) for x in re.findall(r'<p>(.*?)</p>',part[0],re.S)] if len(part)==1 else []
        expected=(c[key] if isinstance(c[key],list) else [c[key]]) if key else ([c['status'],c['ai_disclosure']]+([c['edition_note']] if c.get('edition_note') else []) if sid=='status' else [c['collaboration'],'Authorship and responsibilities would be discussed in relation to the substantive contributions made.'] if sid=='collaborate' else [c['license'],c['license_note']])
        test('exact_ordered_paragraphs_'+sid,paras==expected)
    tex=(paper/c['source_binding']['source_tex_path']).read_text();abstract=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1)
    test('full_original_abstract',normalize_bm_abstract(rid,abstract)==c['abstract'] and '<h2>Original abstract</h2>' in html)
    expected_anchors=[('#main','Skip to content',False),('/','Alec Kriebel',False),('/research/','Research',False),('/blog/','Blog',False),(c['orcid'],'ORCID',False),('/research/'+c['slug']+'/',c['title'],False),(c['pdf_filename'],f"Read the paper (PDF, {c['pdf_pages']} pages)",False),(c['supplement_filename'],c['supplement_label'],True),('https://doi.org/'+c['doi'],'Zenodo record',False),(c['license_url'],'CC BY 4.0',False),('#plain-language','Plain-English explanation',False),('#paper','Read on this page',False),('#collaborate','Collaboration',False),(prefix+c['pdf_filename'],'Open PDF',False),(prefix+c['pdf_filename'],'Download PDF',True)]
    urls={x['name']:x['url'] for x in receipt['files']}
    expected_anchors += [(urls[c['pdf_filename']],'Download original PDF from Zenodo',True),(prefix+c['supplement_filename'],'Download complete ZIP',True),(urls[c['supplement_filename']],'Download original complete ZIP from Zenodo',True)]
    expected_anchors += [(x['url'],x['label'],False) for x in c['related_resources']]
    expected_anchors += [('mailto:me@aleckriebel.com','Contact Alec',False),('https://doi.org/'+c['doi'],'https://doi.org/'+c['doi'],False),(prefix+'citation.bib','Download BibTeX',True)]
    expected_anchors += [(x['url'],x['title'],False) for x in c['background']]
    expected_anchors += [('/research/','Research home',False),('mailto:me@aleckriebel.com','me@aleckriebel.com',False)]
    test('all_exact_ordered_anchor_labels_destinations_downloads',[(a.get('href'),s,'download' in a) for a,s in body.anchors]==expected_anchors)
    test('one_complete_reader',[a for t,a in tags if t=='iframe']==[{'class':'paper-pdf','src':c['pdf_filename']+'#view=FitH','title':c['title']+f" — complete {c['pdf_pages']}-page paper",'loading':'lazy'}])
    titles=re.findall(r'<title>(.*?)</title>',html,re.S);test('exact_title',list(map(unescape,titles))==[c['title']+' | Alec Kriebel'])
    meta=[(a.get('name',a.get('property')),a.get('content')) for t,a in tags if t=='meta' and 'charset' not in a]
    expect_meta={'viewport':'width=device-width, initial-scale=1','description':c['description'],'author':c['author'],'citation_title':c['title'],'citation_author':c['author'],'citation_author_orcid':'0009-0001-9320-500X','citation_publication_date':c['publication_date'].replace('-','/'),'citation_doi':c['doi'],'citation_pdf_url':base+c['pdf_filename'],'citation_language':'en','og:type':'article','og:title':c['title'],'og:description':c['description'],'og:url':base,'og:site_name':'Alec Kriebel','article:published_time':c['publication_date'],'twitter:card':'summary'}
    test('exact_unique_all_head_metadata',len(meta)==len(expect_meta) and dict(meta)==expect_meta)
    test('exact_canonical_stylesheet_icon',[a for t,a in tags if t=='link']==[{'rel':'canonical','href':base},{'rel':'icon','href':'/favicon.ico'},{'rel':'stylesheet','href':'/research/research.css'}])
    schemas=re.findall(r'<script type="application/ld\+json">(.*?)</script>',html,re.S);schema=json.loads(schemas[0]) if len(schemas)==1 else {};graph=schema.get('@graph',[])
    art=graph[1] if len(graph)==2 else {};web=graph[0] if len(graph)==2 else {}
    expected_article={'@type':'ScholarlyArticle','@id':base+'#article','url':base,'name':c['title'],'headline':c['title'],'description':c['description'],'abstract':c['abstract'],'author':[{'@type':'Person','name':c['author'],'sameAs':c['orcid']}],'datePublished':c['publication_date'],'creativeWorkStatus':'Unrefereed preprint','inLanguage':'en','isAccessibleForFree':True,'sameAs':'https://doi.org/'+c['doi'],'identifier':{'@type':'PropertyValue','propertyID':'DOI','value':c['doi']},'encoding':{'@type':'MediaObject','contentUrl':base+c['pdf_filename'],'encodingFormat':'application/pdf'},'license':c['license_url']}
    if c['version'] is not None:expected_article['version']=c['version']
    test('exact_whole_scholarly_schema',same(art,expected_article) and schema.get('@context')=='https://schema.org' and set(schema)=={'@context','@graph'})
    test('exact_page_schema',set(web)=={'@type','@id','url','name','dateCreated','dateModified','mainEntity'} and all(web.get(k)==v for k,v in {'@type':'WebPage','@id':base+'#page','url':base,'name':c['title'],'mainEntity':{'@id':base+'#article'}}.items()) and all(re.fullmatch(r'\d{4}-\d{2}-\d{2}',web.get(k,'')) for k in ('dateCreated','dateModified')))
    test('no_extra_scripts',len([t for t,a in tags if t=='script'])==1)
    test('no_raw_math_markup',not any(x in body.text for x in ['\\','$']))
    test('exact_four_article_files',{x.name for x in out.iterdir()}=={'index.html','citation.bib',c['pdf_filename'],c['supplement_filename']} and all(x.is_file() and not x.is_symlink() for x in out.iterdir()))
    test('exact_prepared_citation',(out/'citation.bib').read_bytes()==c['prepared_bibtex'].encode()==(paper/c['source_binding']['prepared_bibtex_path']).read_bytes())
    hashes={'html':sha(f),'publication':sha(paper/'publication.json'),'promotion':sha(paper/'promotion.json')}
    for key in ('pdf','supplement'):
        name=c[key+'_filename'];test('unchanged_complete_'+key,(out/name).read_bytes()==(asset_root/name).read_bytes());hashes[key]=sha(out/name)
    reader=PdfReader(out/c['pdf_filename']);texts=[page.extract_text() or '' for page in reader.pages]
    test('searchable_complete_pdf',len(texts)==c['pdf_pages'] and all(len(t.strip())>100 for t in texts))
    test('literal_qualified_scientific_status',g['status']==STATUSES[rid])
    test('index_single_article_link',index.count('href="/research/'+c['slug']+'/"')==1)
    test('sitemap_single_canonical',sitemap.count('<loc>'+base+'</loc>')==1)
    local=0
    for a,label in body.anchors:
        u=urlsplit(a['href'])
        if u.scheme or u.netloc:continue
        target=(site/unquote(u.path.lstrip('/'))) if u.path.startswith('/') else (out/unquote(u.path)) if u.path else f
        if u.path.endswith('/'):target=target/'index.html'
        if not target.exists():test('local_destination_'+label,False)
        if u.fragment and not re.search(r'\bid="'+re.escape(u.fragment)+'"',target.read_text()):test('local_anchor_'+label,False)
        local+=1
    return {'checks':checks,'hashes':hashes,'local_links_checked':local,'pdf_pages':len(texts),'pdf_chars_per_page':[len(t) for t in texts]}
