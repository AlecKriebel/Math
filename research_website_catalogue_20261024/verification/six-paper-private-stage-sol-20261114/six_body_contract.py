"""Independent complete-text/DOM/head/asset contract. Does not import the builder."""
from six_common import *
from six_presentation import presentation
from simple_dom import Document
from datetime import date
from html import unescape
from collections import Counter

def expected_body(bundle):
    c=bundle['c'];rid=bundle['rid'];v=presentation(bundle);dt=date.fromisoformat(c['publication_date']);day=f'{dt.day} {dt.strftime("%B %Y")}';doi='https://doi.org/'+c['doi']
    kind='Unrefereed research note' if rid in {'23333046','23320818'} else 'Unrefereed preprint'
    words=['Skip to content','Alec Kriebel','Research | Blog | ORCID',c['title'],
     f"By {c['author']}, independent researcher. {c['publication_date_label']} {day} · {c['edition_label']} · {kind}",
     f"Read the paper (PDF, {c['pdf_pages']} pages) · {c['supplement_label']} · Zenodo record · CC BY 4.0",'Plain-English explanation · Read on this page · Collaboration',
     c['abstract_heading'],c['abstract'],'The idea in plain English',*c['plain_language'],'The precise result',*c['result'],'Why the result holds',*c['why_it_works'],
     'Scope and limitations',*c['limitations'],'Status and AI use',c['status'],c['ai_disclosure']]
    if c.get('edition_note'):words.append(c['edition_note'])
    words+=['Read the paper',c['reader_intro'],' · '.join(x['label'] for x in v['pdf_links']),'Supporting materials',' · '.join(x['label'] for x in v['zip_links'])]
    words += [x['label'] for x in c['related_resources']]+v['material_notes']
    if v['license_notices']:words+=['Licensing',*v['license_notices']]
    words+=['Collaborate on this result',c['collaboration'],'Contact Alec','Cite this paper',
       f"{c['author']}. ({dt.year}). {c['title']} ({c['citation_edition_label']}) [Preprint]. Zenodo. {doi}",'Download BibTeX','Background and prior work']
    words += [x['title']+(' : '+x['note'] if x.get('note') else '') for x in c['background']]
    words+=['Research home | me@aleckriebel.com','© 2013–2026 Kriebel LLC.']
    return ' '.join(' '.join(words).split())

def check_page(bundle,html_bytes,article_files,*,index_bytes=None,sitemap_bytes=None,build_date=None):
    c=bundle['c'];rid=bundle['rid'];v=presentation(bundle);checks={};test=lambda k,x:checks.__setitem__(k,bool(x))
    try:html=html_bytes.decode('utf8');d=Document(html)
    except (UnicodeError,ValueError):return {'valid_UTF8_parse':False}
    tags=d.tags;base='https://aleckriebel.com/research/'+c['slug']+'/';doi='https://doi.org/'+c['doi'];dt=date.fromisoformat(c['publication_date'])
    kind='Unrefereed research note' if rid in {'23333046','23320818'} else 'Unrefereed preprint'
    test('closed_static_document_and_visibility_grammar',not d.faults and d.doctypes==['doctype html'])
    test('exact_single_ordered_document_roots',[t for t,a in tags if t in {'html','head','body'}]==['html','head','body'] and d.bodies==1)
    test('exact_HTML_language',[a for t,a in tags if t=='html']==[{'lang':'en'}])
    test('whole_indexable_approved_body',d.text==expected_body(bundle))
    test('exact_single_h1',d.h1s==[c['title']])
    test('actual_complete_source_abstract',bundle['normalized_source_abstract']==c['abstract'])
    sections=['abstract','plain-language','result','proof','limits','status','paper','materials']+(['licensing'] if v['license_notices'] else [])+['collaborate','cite','background']
    test('all_exact_sections_in_order',[a.get('id') for t,a in tags if t=='section']==sections)
    pmap={'abstract':[c['abstract']],'plain-language':c['plain_language'],'result':c['result'],'proof':c['why_it_works'],'limits':c['limitations'],
          'status':[c['status'],c['ai_disclosure']]+([c['edition_note']] if c.get('edition_note') else []),'collaborate':[c['collaboration']]}
    if v['license_notices']:pmap['licensing']=v['license_notices']
    for sid,expected in pmap.items():
        parts=re.findall(r'<section id="'+sid+r'">(.*?)</section>',html,re.S)
        paras=[unescape(x) for x in re.findall(r'<p>(.*?)</p>',parts[0],re.S)] if len(parts)==1 else []
        test('all_ordered_full_paragraphs_'+sid,paras==expected)
    links=[({'class':'skip-link','href':'#main'},'Skip to content'),({'href':'/'},'Alec Kriebel'),({'href':'/research/'},'Research'),({'href':'/blog/'},'Blog'),({'href':c['orcid']},'ORCID'),
      ({'href':'/research/'+c['slug']+'/'},c['title']),({'href':c['pdf_filename']},f"Read the paper (PDF, {c['pdf_pages']} pages)"),({'href':c['supplement_filename'],'download':None},c['supplement_label']),
      ({'href':doi},'Zenodo record'),({'href':c['license_url']},'CC BY 4.0'),({'href':'#plain-language'},'Plain-English explanation'),({'href':'#paper'},'Read on this page'),({'href':'#collaborate'},'Collaboration')]
    def dl(x):
        a={'href':x['href']}
        if x['download']:a['download']=v['download_values'][x['href']]
        return a,x['label']
    links += list(map(dl,v['pdf_links']))+list(map(dl,v['zip_links']))
    links += [({'href':x['url']},x['label']) for x in c['related_resources']]
    links += [({'href':'mailto:me@aleckriebel.com'},'Contact Alec'),({'href':doi},doi),dl(v['bib_link'])]
    links += [({'href':x['url']},x['title']) for x in c['background']]
    links += [({'href':'/research/'},'Research home'),({'href':'mailto:me@aleckriebel.com'},'me@aleckriebel.com')]
    test('all_exact_ordered_link_attributes_labels_and_downloads',same(d.anchors,links))
    iframe={'class':'paper-pdf','src':v['iframe_src'],'title':v['iframe_title'],'loading':'lazy'}
    test('one_exact_complete_reader',[a for t,a in tags if t=='iframe']==[iframe])
    test('exact_class_placements',[(t,a) for t,a in tags if 'class' in a]==[('a',{'class':'skip-link','href':'#main'}),('p',{'class':'site-title'}),('p',{'class':'entry-meta'}),('iframe',iframe),('p',{'class':'copyright'})])
    test('exact_actual_date_and_navigation',[a for t,a in tags if t=='time']==[{'datetime':c['publication_date']}] and [a for t,a in tags if t=='nav']==[{'aria-label':'Main navigation'}])
    ids=[a['id'] for t,a in tags if 'id' in a];test('exact_unique_ids',ids==['main',*sections] and len(ids)==len(set(ids)))
    expected_counts={'html':1,'head':1,'body':1,'title':1,'script':1,'link':3,'header':2,'nav':1,'main':1,'article':1,'h1':1,'section':len(sections),'h2':len(sections),'br':1,'time':1,'strong':1,'hr':2,'footer':1,'iframe':1,'ul':2,
       'li':1+len(c['related_resources'])+len(c['background']),'a':len(links),'i':1,'p':12+sum(len(x) for x in pmap.values())-1+len(v['material_notes'])}
    # pmap includes collaboration, already included in the twelve fixed paragraphs.
    meta=[(a.get('name',a.get('property')),a.get('content')) for t,a in tags if t=='meta' and 'charset' not in a]
    expect_meta={'viewport':'width=device-width, initial-scale=1','description':c['description'],'author':c['author']}
    if c.get('keywords'):expect_meta['keywords']=', '.join(c['keywords'])
    expect_meta.update({'citation_title':c['title'],'citation_author':c['author'],'citation_author_orcid':'0009-0001-9320-500X','citation_publication_date':c['publication_date'].replace('-','/'),
     'citation_doi':c['doi'],'citation_pdf_url':base+c['pdf_filename'],'citation_language':'en','og:type':'article','og:title':c['title'],'og:description':c['description'],'og:url':base,'og:site_name':'Alec Kriebel','article:published_time':c['publication_date'],'twitter:card':'summary'})
    expected_counts['meta']=len(expect_meta)+1
    test('exact_static_tag_inventory',Counter(t for t,a in tags)==Counter(expected_counts))
    test('all_exact_unique_head_metadata',len(meta)==len(expect_meta) and dict(meta)==expect_meta and [a for t,a in tags if t=='meta' and 'charset' in a]==[{'charset':'utf-8'}])
    test('exact_document_title',[unescape(x) for x in re.findall(r'<title>(.*?)</title>',html,re.S)]==[c['title']+' | Alec Kriebel'])
    test('exact_canonical_CSS_favicon',[a for t,a in tags if t=='link']==[{'rel':'canonical','href':base},{'rel':'icon','href':'/favicon.ico'},{'rel':'stylesheet','href':'/research/research.css'}])
    scripts=re.findall(r'<script type="application/ld\+json">(.*?)</script>',html,re.S)
    try:schema=strict_json(scripts[0]) if len(scripts)==1 else None
    except (json.JSONDecodeError,ValueError):schema=None
    art={'@type':'ScholarlyArticle','@id':base+'#article','url':base,'name':c['title'],'headline':c['title'],'description':c['description'],'abstract':c['abstract'],
       'author':[{'@type':'Person','name':c['author'],'sameAs':c['orcid']}],'datePublished':c['publication_date'],'version':c['version'],'creativeWorkStatus':kind,'inLanguage':'en','isAccessibleForFree':True,'sameAs':doi,
       'identifier':{'@type':'PropertyValue','propertyID':'DOI','value':c['doi']},'encoding':{'@type':'MediaObject','contentUrl':base+c['pdf_filename'],'encodingFormat':'application/pdf'},'license':c['license_url']}
    if c.get('keywords'):art['keywords']=c['keywords']
    web={'@type':'WebPage','@id':base+'#page','url':base,'name':c['title'],'dateCreated':build_date,'dateModified':build_date,'mainEntity':{'@id':base+'#article'}}
    test('exact_entire_scholarly_and_page_JSON',same(schema,{'@context':'https://schema.org','@graph':[web,art]}))
    test('no_extra_or_executable_scripts',[a for t,a in tags if t=='script']==[{'type':'application/ld+json'}])
    test('no_raw_TeX_math_in_body',not any(x in d.text for x in ('\\','$')))
    expected_files={'index.html','citation.bib',c['pdf_filename'],c['supplement_filename']}
    test('exact_four_article_files',set(article_files)==expected_files and article_files.get('index.html')==html_bytes)
    test('exact_prepared_citation_bytes',article_files.get('citation.bib')==bundle['prepared_bibtex'])
    for a in bundle['asset_view']:
        data=article_files.get(a['name'],b'');test('unchanged_complete_asset_'+a['name'],len(data)==a['bytes'] and sha(data)==a['sha256'] and data==Path(a['path']).read_bytes())
    test('complete_searchable_actual_PDF',len(bundle['pdf_chars_per_page'])==c['pdf_pages'] and all(n>100 for n in bundle['pdf_chars_per_page']))
    test('literal_qualified_scientific_status',(bundle['g']['status'] if rid in {'23124601','23333046'} else bundle['g']['scientific_status'])==STATUSES[rid])
    if index_bytes is not None:test('single_index_article_link',index_bytes.decode().count('href="/research/'+c['slug']+'/"')==1)
    if sitemap_bytes is not None:test('single_sitemap_canonical',sitemap_bytes.decode().count('<loc>'+base+'</loc>')==1)
    return checks
