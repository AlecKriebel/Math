"""Exact two-paper layout transform. Import performs no rendering or file reads.

CLI writes only eleven overlay files under a fresh private candidate-a/b,
after the separate pinned root website GO and fresh605/90/91 freeze exist.
"""
from pathlib import Path, PurePosixPath
import copy
import datetime
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from stage_common import A,W,IDS,ASSET_NAMES,BASE_COUNTS,FINAL_COUNTS,CSS
from stage_common import need,sha,same,read,structured,main_block,dump,frozen_inputs,records

HEADER = ('<header>\n<p class="site-title"><a href="/">Alec Kriebel</a></p>\n'
          '<nav aria-label="Main navigation"><a href="/research/">Research</a> | '
          '<a href="/blog/">Blog</a> | <a href="https://orcid.org/0009-0001-9320-500X">ORCID</a></nav>\n</header>\n')
FOOTER = ('\n<footer>\n<hr>\n<p><a href="/research/">Research home</a></p>\n'
          '<p class="copyright">© 2013–2026 Kriebel LLC.</p>\n</footer>\n</body>\n</html>\n')
CCBY = 'https://creativecommons.org/licenses/by/4.0/'


def body_contract(main):
    allowed={'main','article','header','h1','h2','p','a','section','ul','li','iframe'}
    attrs={'id','class','href','src','title','download','target','rel','loading','width','height'}
    stack=[];frames=[]
    tokens=list(re.finditer(r'<(/?)([a-z][a-z0-9]*)([^<>]*)>',main))
    need(len(tokens)==main.count('<'),'all actual markup recognized, no hidden comment/declaration')
    for token in tokens:
        close,tag,tail=token.groups();need(tag in allowed,'known visible owner tag')
        if close:
            need(not tail.strip() and stack and stack.pop()==tag,'balanced exact main tags');continue
        found={};pos=0
        for at in re.finditer(r'\s+([a-z][a-z0-9-]*)(?:="([^"]*)")?',tail):
            need(not tail[pos:at.start()].strip(),'exact quoted attribute grammar')
            name,value=at.groups();need(name in attrs and name not in found,'unique nonhiding allowed attribute')
            found[name]=value;pos=at.end()
        need(not tail[pos:].strip(),'no unparsed main attribute')
        if 'class' in found:need(found['class']=='paper-pdf','only actual visible reader class')
        for name in ['href','src']:
            if name in found:
                value=html.unescape(found[name]);need(value.startswith(('https://','/','#','assets/')),'safe URL scheme')
                need('..' not in PurePosixPath(value.split('#')[0]).parts,'no parent URL path')
        if tag=='iframe':
            frames.append(found);need(found.get('loading')=='lazy' and bool(found.get('title')) and
                                     found.get('src','').startswith('assets/') and '.pdf' in found['src'],'one complete unchanged PDF reader')
        stack.append(tag)
    need(not stack and len(frames)==1 and main.count('<h1>')==1 and main.count('<section ')==12,
         'actual complete adopted article/reader/twelve sections')


def production_article(row):
    article=copy.deepcopy(row['article']);url=row['url']
    article.update({'@id':url+'#article','url':url,'mainEntityOfPage':{'@id':url+'#page'},
                    'inLanguage':'en','isAccessibleForFree':True})
    article['creativeWorkStatus']='Unrefereed preprint'
    encodings=[]
    for original,native in zip(row['article']['encoding'],row['assets']):
        value=copy.deepcopy(original);key=native['original_api_file_object']['key']
        value['contentUrl']=url+'assets/'+key
        value['sameAs']=native['original_api_file_object']['links']['self']
        # This is the exact new root refinement, solely in the production head.
        if row['rid']==IDS[0] and key.endswith('.zip'):
            value.pop('license',None)
        else:
            value['license']=CCBY
        encodings.append(value)
    article['encoding']=encodings
    return article


def document(row,build_date):
    c=row['config'];url=row['url'];h=html.escape
    body_contract(row['main'])
    graph={'@context':'https://schema.org','@graph':[
        {'@type':'WebPage','@id':url+'#page','url':url,'name':c['title'],'dateCreated':build_date,
         'dateModified':build_date,'mainEntity':{'@id':url+'#article'}},production_article(row)]}
    fields=[('description',c['description']),('author',c['author']),('robots','index,follow'),
            ('citation_title',c['title']),('citation_author',c['author']),('citation_author_orcid',c['orcid']),
            ('citation_publication_date',c['publication_date'].replace('-','/')),('citation_version',c['version']),
            ('citation_doi',c['doi']),('citation_pdf_url',url+'assets/'+c['pdf_filename']),
            ('citation_language','en'),('twitter:card','summary')]
    head='<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
    head+='<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    head+='<title>'+h(c['seo']['title'])+'</title>\n'
    head+=''.join('<meta name="'+k+'" content="'+h(v)+'">\n' for k,v in fields)
    head+='<link rel="canonical" href="'+url+'">\n<link rel="icon" href="/favicon.ico">\n'
    head+='<link rel="stylesheet" href="/research/research.css">\n'
    for k,v in [('type','article'),('title',c['title']),('description',c['description']),('url',url),('site_name','Alec Kriebel')]:
        head+='<meta property="og:'+k+'" content="'+h(v)+'">\n'
    head+='<meta property="article:published_time" content="'+c['publication_date']+'">\n'
    head+='<script type="application/ld+json">'+dump(graph)+'</script>\n<style>'+CSS+'</style>\n</head>\n<body>\n'
    head+='<a class="skip-link" href="#main">Skip to content</a>\n'
    return (head+HEADER+row['main']+FOOTER).encode()


def additions(rows,build_date):
    entries='';nodes='';h=html.escape
    for row in rows:
        c=row['config'];d=datetime.date.fromisoformat(c['publication_date']);local='/research/'+c['slug']+'/'
        label=str(d.day)+' '+d.strftime('%B %Y')
        entries+=('      <li><a href="'+local+'">'+h(c['title'])+'</a><br><span class="entry-meta">'+label+
                  ' · Unrefereed preprint</span><p>'+h(c['description'])+'</p><p><a href="'+local+'assets/'+c['pdf_filename']+
                  '">PDF</a> · <a href="https://doi.org/'+c['doi']+'">Zenodo</a></p></li>\n')
        nodes+='  <url><loc>'+row['url']+'</loc><lastmod>'+build_date+'</lastmod></url>\n'
    return entries,nodes


def render_buffers(by,rows,build_date):
    buffers={}
    for row in rows:
        c=row['config'];need(re.fullmatch('[a-z0-9-]+',c['slug']) is not None,'bounded exact article slug')
        base='research/'+c['slug']+'/'
        buffers[base+'index.html']=document(row,build_date)
        for native in row['assets']:
            key=native['original_api_file_object']['key']
            buffers[base+'assets/'+key]=by[str(row['ed']/'candidate/assets'/key)]
        buffers[base+'assets/citation.bib']=by[str(row['ed']/'candidate/assets/citation.bib')]
    index=by[str(W/'public/research/index.html')].decode();match,value=structured(index);new=copy.deepcopy(value)
    items=new['mainEntity']['itemListElement'];need(len(items)==90,'exact authorized old90 records')
    for row in rows:items.append({'@type':'ListItem','position':len(items)+1,'url':row['url'],'name':row['config']['title']})
    new['mainEntity']['numberOfItems']=92
    index=index[:match.start(1)]+dump(new)+index[match.end(1):]
    entries,nodes=additions(rows,build_date)
    need(index.count('    </ul>')==1,'one exact visible index insertion site')
    buffers['research/index.html']=index.replace('    </ul>',entries+'    </ul>',1).encode()
    sitemap=by[str(W/'public/research/sitemap.xml')].decode();need(sitemap.count('</urlset>')==1,'one exact sitemap insertion')
    buffers['research/sitemap.xml']=sitemap.replace('</urlset>',nodes+'</urlset>',1).encode()
    return buffers


def validate_buffers(buffers,by,website,rows,build_date):
    expected=render_buffers(by,rows,build_date)
    need(len(buffers)==len(expected)==11 and set(buffers)==set(expected),'exact eleven overlay paths')
    need(all(buffers[k]==v for k,v in expected.items()),'whole exact rendered buffers and all seven downloads')
    for row in rows:
        c=row['config'];base='research/'+c['slug']+'/'
        text=buffers[base+'index.html'].decode();need(main_block(text)==row['main'],'whole approved body except initial main id')
        body_contract(main_block(text))
        need(text.count('<style>')==1 and '<style>'+CSS+'</style>' in text,'exact nonhiding supplemental style')
        need('<meta name="robots" content="index,follow">' in text and 'noindex' not in text,'future production index/follow head')
        need('<link rel="canonical" href="'+row['url']+'">' in text,'exact real canonical proposal in private output')
        _,graph=structured(text);page,article=graph['@graph']
        need(page['dateCreated']==page['dateModified']==build_date and article['datePublished']==c['publication_date'],
             'new webpage dates separate from original scholarly publication')
        need(article['abstract']==c['abstract'] and article['version']==c['version'],'full original abstract and exact native version')
        permitted={'@id','url','mainEntityOfPage','inLanguage','isAccessibleForFree','encoding'}
        for k,v in row['article'].items():
            if k not in permitted:need(k in article and same(v,article[k]),'every unchanged original scholarly field')
        need(article['license']==CCBY,'authored paper article license retained')
        need(len(article['encoding'])==len(row['assets']),'complete native encodings')
        for native,encoding in zip(row['assets'],article['encoding']):
            key=native['original_api_file_object']['key']
            need(buffers[base+'assets/'+key]==by[native['path']],'whole unchanged original native asset')
            need(encoding['contentUrl']==row['url']+'assets/'+key and encoding['sameAs']==native['original_api_file_object']['links']['self'],
                 'local/original complete native encoding order and URLs')
            if row['rid']==IDS[0] and key.endswith('.zip'):need('license' not in encoding,'root127 mixed-ZIP no blanket encoding license')
            else:need(encoding['license']==CCBY,'actual PDF or broad128 CC BY asset rights')
    oldindex=by[str(W/'public/research/index.html')].decode();oldmatch,olddata=structured(oldindex)
    index=buffers['research/index.html'].decode();_,data=structured(index)
    need(same(data['mainEntity']['itemListElement'][:90],olddata['mainEntity']['itemListElement']),'all90 ordered typed old records retained')
    need(data['mainEntity']['numberOfItems']==len(data['mainEntity']['itemListElement'])==92,'actual92 new index records')
    entries,nodes=additions(rows,build_date);need(index.count(entries)==1,'one visible exact two-paper addition')
    restored=index.replace(entries,'',1);rm,_=structured(restored)
    need(restored[:rm.start(1)]+oldmatch[1]+restored[rm.end(1):]==oldindex,'all prior visible index/scaffold bytes unchanged')
    sitemap=buffers['research/sitemap.xml'];addition=nodes.encode()
    need(sitemap.count(addition)==1 and sitemap.replace(addition,b'',1)==by[str(W/'public/research/sitemap.xml')],
         'all91 whole old sitemap nodes and raw bytes preserved')
    need(len(ET.fromstring(sitemap))==93,'actual93 sitemap nodes')
    baseline={str(Path(p).relative_to(W/'public')) for p in website['public_namespace']}
    need(len(baseline)==605 and len(baseline|set(buffers))==614 and len(baseline-set(buffers))==603 and
         baseline&set(buffers)=={'research/index.html','research/sitemap.xml'},'nine new leaves, two aggregates, all603 unrelated files protected')
    return {'overlay_files':11,'new_leaf_files':9,'aggregate_overlays':2,'virtual_counts':[614,92,93],
            'all_prior_index_records_preserved':90,'all_prior_sitemap_nodes_preserved':91,'unrelated_public_files_unchanged':603,
            'whole_native_assets':5,'whole_BibTeX_assets':2,'main_transform':'only initial main id added',
            '127_ZIP_blanket_encoding_license_omitted_by_exact_root_authority':True,
            '128_native_TeX_ZIP_PDF_broad_CCBY_and_absent_printed_version_preserved':True}


if __name__=='__main__':
    need(sys.argv[1:] in (['candidate-a'],['candidate-b']),'only candidate-a or candidate-b')
    # No render function is called until this specific pinned fresh GO loader succeeds.
    g,source,website,by=frozen_inputs();rows=records(by)
    buffers=render_buffers(by,rows,g['build_date']);result=validate_buffers(buffers,by,website,rows,g['build_date'])
    target=A/sys.argv[1]
    need(not target.exists() and not target.is_symlink(),'refuse preexisting candidate root')
    for relative,body in buffers.items():
        p=PurePosixPath(relative);need(not p.is_absolute() and '..' not in p.parts,'bounded output path')
        out=target/'public'/relative;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(body)
    frozen_inputs()  # independently recheck originals after writing the private overlay
    print(json.dumps({'candidate':sys.argv[1],'optimization_level':sys.flags.optimize,'actual_all_eleven_buffers_written':True,
                      **result,'production_installation_authorized':False,'live_or_browser_verified':False},indent=2))
