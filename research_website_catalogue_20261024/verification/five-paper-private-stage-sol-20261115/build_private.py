"""Pure five-record presentation plus explicitly fenced private disk output."""
from five_common import *
from five_source import load_bundles
from five_markup import Tree,node,nodes,text,serialize,block,background
from datetime import date
from html import escape as h
import argparse,copy
MONTHS=('January','February','March','April','May','June','July','August','September','October','November','December')
def display_date(iso):
 d=date.fromisoformat(iso);return str(d.day)+' '+MONTHS[d.month-1]+' '+str(d.year)
def top113_main(b):
 c=b['c'];rid=b['rid'];need(rid=='23441890','only_declared_top_MD_record')
 def section(sid,label,values):return '<section id="'+sid+'"><h2>'+h(label)+'</h2>'+''.join(block(x) for x in values)+'</section>'
 sections=section('abstract',c['abstract_heading'],[c['abstract']])
 sections+=section('plain-language','The idea in plain English',c['plain_language'])
 sections+=section('result','The precise result',c['result'])
 sections+=section('proof','Why the result holds',c['why_it_works'])
 sections+=section('limits','Scope and limitations',c['limitations'])
 sections+=section('status','Status and AI use',[c['status'],c['ai_disclosure'],c['edition_note']])
 sections+='<section id="paper"><h2>Read the paper</h2><p>'+h(c['reader_intro'])+'</p><p><a href="'+h(b['pdf']['name'])+'" target="_blank" rel="noopener">Open the complete PDF</a> · <a href="'+h(b['pdf']['name'])+'" download>Download the PDF</a></p><iframe class="paper-pdf" src="'+h(b['pdf']['name'])+'#view=FitH" title="'+h(c['title'])+' — complete six-page paper PDF" loading="lazy"></iframe></section>'
 sections+='<section id="materials"><h2>Supporting materials</h2><p><a href="'+h(b['zip']['name'])+'" download>'+h(c['supplement_label'])+'</a></p><ul>'+''.join('<li><a href="'+h(x['url'])+'">'+h(x['label'])+'</a></li>' for x in c['related_resources'])+'</ul><p>Authored paper, prose and code: CC BY 4.0. Cited third-party works retain their own rights.</p></section>'
 sections+=section('collaborate','Collaboration',[c['collaboration']])
 sections+='<section id="cite"><h2>Cite this paper</h2><p>Alec Kriebel. '+h(c['title'])+'. Version '+h(c['version'])+', '+display_date(c['publication_date'])+'. Zenodo. <a href="https://doi.org/'+c['doi']+'">https://doi.org/'+c['doi']+'</a>.</p><p><a href="citation.bib" download>BibTeX</a></p></section>'
 sections+='<section id="background"><h2>Background and prior work</h2>'+background(c['background'])+'</section>'
 source='<!doctype html><html><head><title>x</title></head><body><main id="main"><article><header><h1>'+h(c['title'])+'</h1><p class="entry-meta">By <a href="'+h(c['orcid'])+'">Alec Kriebel · ORCID</a><br>Original publication date <time datetime="'+c['publication_date']+'">'+display_date(c['publication_date'])+'</time> · Version '+h(c['version'])+' · Unrefereed preprint</p></header>'+sections+'</article></main></body></html>'
 return Tree(source).find('main')[0]
def main_tree(b,*,dlab_homepage):
 if b['source_html'] is None:main=top113_main(b)
 else:main=copy.deepcopy(Tree(b['source_html'],source_math_style=True).find('main')[0])
 main['attrs']={'id':'main'}
 changes=0;bib_changes=0
 for n in nodes(main):
  a=n['attrs']
  for field in ['href','src']:
   if field in a and a[field].startswith('assets/'):
    old=a[field];name=old[len('assets/'):].split('#',1)[0]
    need(name in {b['pdf']['name'],b['zip']['name']},'only_exact_asset_relative_rebase')
    a[field]=old[len('assets/'):]
  if n['tag']=='a' and a.get('href')=='../citation.bib':
   need(b['rid']=='23430498','only_declared115_BibTeX_rebase');a['href']='citation.bib';bib_changes+=1
  if a.get('class'):
   tokens=a['class'].split();tokens=[{'formula':'equation','byline':'entry-meta','meta':'entry-meta'}.get(x,x) for x in tokens];a['class']=' '.join(tokens)
  if 'style' in a:
   need(n['tag']=='span' and a['style']=='white-space: nowrap','only_visible_inline_math_style_rebase');del a['style'];a['class']='equation'
  if n['tag']=='iframe':a['class']='paper-pdf';a['loading']='lazy'
  if n['tag']=='a' and a.get('href')==OLD_DLAB and dlab_homepage:
   need(b['rid']=='23441890' and text(n)=='Kourovka Notebook','one_specific_Dlab_background_link');a['href']=NEW_DLAB;changes+=1
 need(bib_changes==(1 if b['rid']=='23430498' else 0),'exact115_single_BibTeX_rebase')
 need(changes==(1 if b['rid']=='23441890' and dlab_homepage else 0),'exact_private_Dlab_one_href_override')
 return main
def article_bytes(b,build_date,*,dlab_homepage):
 if dlab_homepage:authorize_dlab()
 base='https://aleckriebel.com/research/'+b['slug']+'/';doi='https://doi.org/'+b['doi']
 if b['source_html'] is None:
  c=b['c'];title=c['seo']['title'];head=node('head',{},[
   node('meta',{'charset':'utf-8'}),node('meta',{'name':'viewport','content':'width=device-width, initial-scale=1'}),
   node('title',{},[title]),node('meta',{'name':'description','content':c['description']}),
   node('meta',{'name':'citation_title','content':c['title']}),node('meta',{'name':'citation_author','content':c['author']}),
   node('meta',{'name':'citation_publication_date','content':c['publication_date'].replace('-','/')}),
   node('meta',{'name':'citation_doi','content':c['doi']}),node('meta',{'name':'citation_language','content':'en'})])
  article={'@type':'ScholarlyArticle','name':c['title'],'headline':c['title'],'description':c['description'],'abstract':c['abstract'],
   'author':{'@type':'Person','name':c['author'],'sameAs':c['orcid']},'datePublished':c['publication_date'],'version':c['version'],
   'creativeWorkStatus':c['status'],'inLanguage':'en','identifier':{'@type':'PropertyValue','propertyID':'DOI','value':c['doi']},
   'license':c['license_url'],'keywords':c['keywords'],'encoding':{'@type':'MediaObject','encodingFormat':'application/pdf','contentUrl':base+b['pdf']['name']}}
 else:
  original=Tree(b['source_html'],source_math_style=True);head=copy.deepcopy(original.find('head')[0])
  head['children']=[n for n in head['children'] if not(isinstance(n,dict) and n['tag'] in {'style','script'})]
  article=copy.deepcopy(strict_json(text(original.find('script')[0])));article.pop('@context',None)
 article['@id']=base+'#article';article['url']=base;article['sameAs']=doi
 enc=article['encoding'];encodings=enc if isinstance(enc,list) else [enc]
 for e in encodings:
  if e['encodingFormat']=='application/pdf':e['contentUrl']=base+b['pdf']['name']
  elif e['encodingFormat']=='application/zip':e['contentUrl']=base+b['zip']['name']
  else:raise ValueError('five_stage:unexpected_source_encoding')
 meta_nodes={n['attrs'].get('name'):n for n in nodes(head) if n['tag']=='meta'}
 for name,value in [('robots','index,follow'),('citation_pdf_url',base+b['pdf']['name']),('citation_author_orcid','0009-0001-9320-500X')]:
  if name in meta_nodes:meta_nodes[name]['attrs']['content']=value
  else:head['children'].append(node('meta',{'name':name,'content':value}))
 properties={n['attrs'].get('property') for n in nodes(head) if n['tag']=='meta'}
 for key,value in [('og:type','article'),('og:title',b['title']),('og:description',b['description'])]:
  if key not in properties:head['children'].append(node('meta',{'property':key,'content':value}))
 need(not any(n['tag']=='link' and n['attrs'].get('rel')=='canonical' for n in nodes(head)),'source_canonical_still_unassigned')
 head['children'] += [node('link',{'rel':'canonical','href':base}),node('link',{'rel':'icon','href':'/favicon.ico'}),node('link',{'rel':'stylesheet','href':'/research/research.css'})]
 head['children'].append(node('meta',{'property':'og:url','content':base}))
 schema={'@context':'https://schema.org','@graph':[{'@type':'WebPage','@id':base+'#page','url':base,'name':b['title'],'dateCreated':build_date,'dateModified':build_date,'mainEntity':{'@id':base+'#article'}},article]}
 schema_text=json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')
 # Script text is JSON, serialized without HTML-escaping its quotes/entities.
 head['children'].append(node('script',{'type':'application/ld+json'},[schema_text]))
 main=main_tree(b,dlab_homepage=dlab_homepage)
 header='<header><p class="site-title"><a href="/">Alec Kriebel</a></p><nav aria-label="Main navigation"><a href="/research/">Research</a> | <a href="/blog/">Blog</a> | <a href="https://orcid.org/0009-0001-9320-500X">ORCID</a></nav><p>Original Zenodo files: '+' · '.join('<a href="'+h(a['native_original_object']['original_api_file_object']['links']['self'])+'">'+('Complete PDF' if a['name']==b['pdf']['name'] else 'Complete ZIP')+'</a>' for a in b['asset_view'])+'</p></header>'
 footer='<footer><hr><p><a href="/research/">Research home</a></p><p class="copyright">© 2013–2026 Kriebel LLC.</p></footer>'
 # JSON must remain native JSON script data; all other nodes use escaped data.
 scripts=head['children'].pop();head_html=serialize(head);head_html=head_html[:-7]+'<script type="application/ld+json">'+schema_text+'</script></head>'
 document='<!doctype html>\n<html lang="en">'+head_html+'<body><a class="skip-link" href="#main">Skip to content</a>'+header+serialize(main)+footer+'</body></html>\n'
 Tree(document)
 return document.encode()
def overlays(bundles,build_date):
 index=(OWN/'baseline/research/index.html').read_text();sitemap=(OWN/'baseline/research/sitemap.xml').read_text()
 need(index.count('    </ul>')==1 and sitemap.count('</urlset>')==1,'exact_saved_overlay_anchors')
 m=re.search(r'(<script type="application/ld\+json">\s*)(.*?)(\s*</script>)',index,re.S);need(m is not None,'existing_index_schema')
 schema=strict_json(m.group(2));items=schema['mainEntity']['itemListElement'];need(len(items)==schema['mainEntity']['numberOfItems']==78,'actual_old78_index')
 lines=[];maps=[]
 for b in bundles:
  url='https://aleckriebel.com/research/'+b['slug']+'/';need('href="/research/'+b['slug']+'/"' not in index and '<loc>'+url+'</loc>' not in sitemap,'new_work_no_old_destination_collision')
  li='<li><a href="/research/'+b['slug']+'/">'+h(b['title'])+'</a><br><span class="entry-meta">'+display_date(b['publication_date'])+' · '+h(b['kind'])+'</span><p>'+h(b['description'])+'</p><p><a href="/research/'+b['slug']+'/'+b['pdf']['name']+'">PDF</a> · <a href="https://doi.org/'+b['doi']+'">Zenodo</a></p></li>\n';lines.append('      '+li)
  items.append({'@type':'ListItem','position':len(items)+1,'url':url,'name':b['title']});maps.append('  <url><loc>'+url+'</loc><lastmod>'+build_date+'</lastmod></url>\n')
 schema['mainEntity']['numberOfItems']=83;index=index[:m.start(2)]+json.dumps(schema,ensure_ascii=False)+index[m.end(2):]
 index=index.replace('    </ul>',''.join(lines)+'    </ul>',1);sitemap=sitemap.replace('</urlset>',''.join(maps)+'</urlset>')
 return {'research/index.html':index.encode(),'research/sitemap.xml':sitemap.encode()}
def files_in_memory(bundles,build_date,*,dlab_homepage):
 need(date.fromisoformat(build_date).isoformat()==build_date,'explicit_ISO_build_date')
 files=overlays(bundles,build_date)
 for b in bundles:
  prefix='research/'+b['slug']+'/'
  files[prefix+'index.html']=article_bytes(b,build_date,dlab_homepage=dlab_homepage);files[prefix+'citation.bib']=b['bib']
  for a in b['asset_view']:files[prefix+a['name']]=Path(a['path']).read_bytes()
 need(len(files)==22,'exact_five_target22_path_overlay')
 return files
def build(output_root,build_date,*,dlab_homepage):
 out=safe_output(output_root);need(not out.exists(),'fresh_private_output_tree_required')
 bundles=load_bundles();files=files_in_memory(bundles,build_date,dlab_homepage=dlab_homepage)
 out.mkdir(parents=True)
 for rel,data in files.items():
  p=out/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 return {'output_root':str(out),'records':list(IDS),'files':22,'build_date':build_date,'Dlab_one_href_private_override':dlab_homepage,'full_root_copy_code_stage_adoption_pending':True,'canonical_values_inside_private_HTML_are_proposals_only':True,'AA':None,'production_writes':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output-root',type=Path,required=True);p.add_argument('--build-date',required=True);p.add_argument('--dlab-homepage',action='store_true');a=p.parse_args()
 print(json.dumps(build(a.output_root,a.build_date,dlab_homepage=a.dlab_homepage),indent=2))
