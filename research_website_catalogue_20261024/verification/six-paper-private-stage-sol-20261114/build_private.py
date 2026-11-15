"""Build only six new articles and two overlays, under explicit private output/date."""
from six_common import *
from six_source import load_bundles
from six_presentation import presentation
from datetime import date
from html import escape as h
import argparse,copy

KINDS={rid:('Unrefereed research note' if rid in {'23333046','23320818'} else 'Unrefereed preprint') for rid in IDS}
def article_bytes(bundle,build_date):
    c=bundle['c'];rid=bundle['rid'];v=presentation(bundle);published=date.fromisoformat(c['publication_date'])
    day=f'{published.day} {published.strftime("%B %Y")}';base='https://aleckriebel.com/research/'+c['slug']+'/';doi='https://doi.org/'+c['doi']
    def paras(xs):return ''.join('<p>'+h(x)+'</p>' for x in xs)
    def sec(sid,title,xs):return '<section id="'+sid+'"><h2>'+h(title)+'</h2>'+paras(xs)+'</section>'
    def link(x):
        dl=''
        if x['download']:
            val=v['download_values'][x['href']];dl=' download'+('="'+h(val)+'"' if val is not None else '')
        return '<a href="'+h(x['href'])+'"'+dl+'>'+h(x['label'])+'</a>'
    sections=sec('abstract',c['abstract_heading'],[c['abstract']])+sec('plain-language','The idea in plain English',c['plain_language'])+sec('result','The precise result',c['result'])
    sections+=sec('proof','Why the result holds',c['why_it_works'])+sec('limits','Scope and limitations',c['limitations'])
    sections+=sec('status','Status and AI use',[c['status'],c['ai_disclosure']]+([c['edition_note']] if c.get('edition_note') else []))
    sections+='<section id="paper"><h2>Read the paper</h2>'+paras([c['reader_intro']])+'<p>'+' · '.join(map(link,v['pdf_links']))+'</p><iframe class="paper-pdf" src="'+h(v['iframe_src'])+'" title="'+h(v['iframe_title'])+'" loading="lazy"></iframe></section>'
    sections+='<section id="materials"><h2>Supporting materials</h2><ul><li>'+' · '.join(map(link,v['zip_links']))+'</li>'
    sections+=''.join('<li><a href="'+h(x['url'])+'">'+h(x['label'])+'</a></li>' for x in c['related_resources'])+'</ul>'+paras(v['material_notes'])+'</section>'
    if v['license_notices']:sections+=sec('licensing','Licensing',v['license_notices'])
    sections+=sec('collaborate','Collaborate on this result',[c['collaboration']])+'<p><a href="mailto:me@aleckriebel.com">Contact Alec</a></p>'
    sections+='<section id="cite"><h2>Cite this paper</h2><p>'+h(c['author'])+'. ('+str(published.year)+'). <i>'+h(c['title'])+'</i> ('+h(c['citation_edition_label'])+') [Preprint]. Zenodo. <a href="'+doi+'">'+doi+'</a></p><p>'+link(v['bib_link'])+'</p></section>'
    sections+='<section id="background"><h2>Background and prior work</h2><ul>'+''.join('<li><a href="'+h(x['url'])+'">'+h(x['title'])+'</a>'+(': '+h(x['note']) if x.get('note') else '')+'</li>' for x in c['background'])+'</ul></section>'
    article={'@type':'ScholarlyArticle','@id':base+'#article','url':base,'name':c['title'],'headline':c['title'],'description':c['description'],'abstract':c['abstract'],
             'author':[{'@type':'Person','name':c['author'],'sameAs':c['orcid']}],'datePublished':c['publication_date'],'version':c['version'],
             'creativeWorkStatus':KINDS[rid],'inLanguage':'en','isAccessibleForFree':True,'sameAs':doi,
             'identifier':{'@type':'PropertyValue','propertyID':'DOI','value':c['doi']},'encoding':{'@type':'MediaObject','contentUrl':base+c['pdf_filename'],'encodingFormat':'application/pdf'},'license':c['license_url']}
    if c.get('keywords'):article['keywords']=c['keywords']
    schema={'@context':'https://schema.org','@graph':[{'@type':'WebPage','@id':base+'#page','url':base,'name':c['title'],'dateCreated':build_date,'dateModified':build_date,'mainEntity':{'@id':base+'#article'}},article]}
    keywords='\n<meta name="keywords" content="'+h(', '.join(c['keywords']))+'">' if c.get('keywords') else ''
    downloads='<a href="'+h(c['pdf_filename'])+'">Read the paper (PDF, '+str(c['pdf_pages'])+' pages)</a> · <a href="'+h(c['supplement_filename'])+'" download>'+h(c['supplement_label'])+'</a> · <a href="'+doi+'">Zenodo record</a> · <a href="'+h(c['license_url'])+'">CC BY 4.0</a>'
    schema_text=json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')
    text=f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{h(c['title'])} | Alec Kriebel</title>
<meta name="description" content="{h(c['description'])}">
<meta name="author" content="{h(c['author'])}">{keywords}
<link rel="canonical" href="{base}"><link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="/research/research.css">
<meta name="citation_title" content="{h(c['title'])}"><meta name="citation_author" content="{h(c['author'])}">
<meta name="citation_author_orcid" content="0009-0001-9320-500X"><meta name="citation_publication_date" content="{c['publication_date'].replace('-','/')}">
<meta name="citation_doi" content="{c['doi']}"><meta name="citation_pdf_url" content="{base+c['pdf_filename']}"><meta name="citation_language" content="en">
<meta property="og:type" content="article"><meta property="og:title" content="{h(c['title'])}"><meta property="og:description" content="{h(c['description'])}"><meta property="og:url" content="{base}"><meta property="og:site_name" content="Alec Kriebel"><meta property="article:published_time" content="{c['publication_date']}"><meta name="twitter:card" content="summary">
<script type="application/ld+json">{schema_text}</script>
</head><body>
<a class="skip-link" href="#main">Skip to content</a>
<header><p class="site-title"><a href="/">Alec Kriebel</a></p><nav aria-label="Main navigation"><a href="/research/">Research</a> | <a href="/blog/">Blog</a> | <a href="https://orcid.org/0009-0001-9320-500X">ORCID</a></nav></header>
<main id="main"><article><header>
<h1><a href="/research/{c['slug']}/">{h(c['title'])}</a></h1>
<p class="entry-meta">By {h(c['author'])}, independent researcher.<br>{h(c['publication_date_label'])} <time datetime="{c['publication_date']}">{day}</time> · {h(c['edition_label'])} · <strong>{KINDS[rid]}</strong></p>
<p>{downloads}</p>
<p><a href="#plain-language">Plain-English explanation</a> · <a href="#paper">Read on this page</a> · <a href="#collaborate">Collaboration</a></p>
</header><hr>{sections}</article></main>
<footer><hr><p><a href="/research/">Research home</a> | <a href="mailto:me@aleckriebel.com">me@aleckriebel.com</a></p><p class="copyright">© 2013–2026 Kriebel LLC.</p></footer>
</body></html>
'''
    return text.encode('utf8')

def overlays(bundles,build_date):
    index=(OWN/'baseline/research/index.html').read_text();sitemap=(OWN/'baseline/research/sitemap.xml').read_text()
    require(index.count('    </ul>')==1 and sitemap.count('</urlset>')==1,'unambiguous_saved_overlay_anchors')
    m=re.search(r'(<script type="application/ld\+json">\s*)(.*?)(\s*</script>)',index,re.S);require(m is not None,'existing_index_schema')
    data=json.loads(m.group(2));items=data['mainEntity']['itemListElement'];require(len(items)==data['mainEntity']['numberOfItems']==72,'actual_old_index_count')
    entries=[];sites=[]
    for b in bundles:
        c=b['c'];url='https://aleckriebel.com/research/'+c['slug']+'/';dt=date.fromisoformat(c['publication_date']);day=f'{dt.day} {dt.strftime("%B %Y")}';doi='https://doi.org/'+c['doi']
        require('href="/research/'+c['slug']+'/"' not in index and '<loc>'+url+'</loc>' not in sitemap,'no_existing_target_entry')
        entries.append('<li><a href="/research/'+c['slug']+'/">'+h(c['title'])+'</a><br><span class="entry-meta">'+day+' · '+KINDS[b['rid']]+'</span><p>'+h(c['description'])+'</p><p><a href="/research/'+c['slug']+'/'+c['pdf_filename']+'">PDF</a> · <a href="'+doi+'">Zenodo</a></p></li>\n')
        items.append({'@type':'ListItem','position':len(items)+1,'url':url,'name':c['title']});sites.append('  <url><loc>'+url+'</loc><lastmod>'+build_date+'</lastmod></url>\n')
    data['mainEntity']['numberOfItems']=len(items)
    index=index[:m.start(2)]+json.dumps(data,ensure_ascii=False)+index[m.end(2):]
    index=index.replace('    </ul>',''.join('      '+x for x in entries)+'    </ul>',1)
    sitemap=sitemap.replace('</urlset>',''.join(sites)+'</urlset>')
    return {'research/index.html':index.encode(),'research/sitemap.xml':sitemap.encode()}

def build(output_root,build_date):
    require(date.fromisoformat(build_date).isoformat()==build_date,'explicit_ISO_build_date')
    target=safe_output(output_root);require(not target.exists(),'fresh_private_output_required')
    bundles=load_bundles();files=overlays(bundles,build_date)
    for b in bundles:
        c=b['c'];prefix='research/'+c['slug']+'/'
        files[prefix+'index.html']=article_bytes(b,build_date);files[prefix+'citation.bib']=b['prepared_bibtex']
        for a in b['asset_view']:files[prefix+a['name']]=Path(a['path']).read_bytes()
    require(len(files)==26,'exact_26_path_overlay')
    target.mkdir(parents=True)
    for rel,data in files.items():
        p=target/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    return {'private_output_root':str(target),'build_date':build_date,'records':list(IDS),'public_overlay_files':len(files),'production_writes':False}
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-root',required=True,type=Path);parser.add_argument('--build-date',required=True)
    a=parser.parse_args();print(json.dumps(build(a.output_root,a.build_date),sort_keys=True))
