"""New two-target private renderer, pure bytes plus fenced new-folder writing."""
from two_common import *
from two_source import load_bundles
from two_dom import Tree,node,nodes,text,serialize
from two_body import main_tree
from datetime import date
from html import escape as h
import copy,argparse,re
MONTHS=('January','February','March','April','May','June','July','August','September','October','November','December')
def authenticate_baseline():
 seal=load(OWN/'BASELINE_SEAL.json');need(bind(OWN/'FRESH_BASELINE.json')['sha256']==seal['baseline_sha256'] and bind(OWN/'BASELINE_AUTHORITY.json')['sha256']==seal['authority_sha256'],'exact_root_released_baseline_seal')
 authority=load(OWN/'BASELINE_AUTHORITY.json');need(authority['root_released_exact_post_five_baseline'] is True and authority['two_stage_install_authorized'] is False,'root_released_baseline_not_installation_authority')
 for a in authority['whole_original_authorities']:need(bind(a['path'])=={k:a[k] for k in ['bytes','sha256']} and same(load(a['path']),a['whole_original_authority']),'complete_root_post_five_authority')
 return load(OWN/'FRESH_BASELINE.json')
def article_bytes(b,build_date):
 base='https://aleckriebel.com/research/'+b['slug']+'/';c=b['c'];doi='https://doi.org/'+b['doi']
 if b['rid']=='23385145':
  old=Tree(b['source_html'],source_editorial=True);head=copy.deepcopy(old.find('head')[0]);head['children']=[x for x in head['children'] if not(isinstance(x,dict) and x['tag'] in {'style','script'})];scholar=copy.deepcopy(strict_json(text(old.find('script')[0])));scholar.pop('@context')
 else:
  template=b['metadata'];scholar=copy.deepcopy(template['jsonld']);scholar.pop('@context');head=node('head',{},[node('meta',{'charset':'utf-8'}),node('meta',{'name':'viewport','content':'width=device-width, initial-scale=1'}),node('title',{},[b['title']+' | Alec Kriebel']),node('meta',{'name':'description','content':b['description']})])
  for key,value in template['citation_meta'].items():head['children'].append(node('meta',{'name':key,'content':base+b['pdf']['name'] if key=='citation_pdf_url' else value}))
  for key in ['type','title','description']:head['children'].append(node('meta',{'property':'og:'+key,'content':template['open_graph'][key]}))
 metas={x['attrs'].get('name'):x for x in nodes(head) if x['tag']=='meta'}
 for key,value in [('robots','index,follow'),('citation_pdf_url',base+b['pdf']['name']),('citation_author_orcid','0009-0001-9320-500X'),('citation_language','en')]:
  if key in metas:metas[key]['attrs']['content']=value
  else:head['children'].append(node('meta',{'name':key,'content':value}))
 props={x['attrs'].get('property') for x in nodes(head) if x['tag']=='meta'}
 for key,value in [('og:type','article'),('og:title',b['title']),('og:description',b['description'])]:
  if key not in props:head['children'].append(node('meta',{'property':key,'content':value}))
 head['children']+=[node('meta',{'property':'og:url','content':base}),node('link',{'rel':'canonical','href':base}),node('link',{'rel':'icon','href':'/favicon.ico'}),node('link',{'rel':'stylesheet','href':'/research/research.css'})]
 need(scholar['abstract']==b['abstract'] and scholar['datePublished']==b['publication_date'],'whole_abstract_original_date')
 for key,value in [('name',b['title']),('version',b['version']),('creativeWorkStatus','Unrefereed preprint')]:
  if key in scholar:need(scholar[key]==value,'original_scholarly_identity:'+key)
  else:scholar[key]=value
 scholar['@id']=base+'#article';scholar['url']=base;scholar['sameAs']=doi
 if 'encoding' not in scholar:scholar['encoding']=[{'@type':'MediaObject','encodingFormat':'application/pdf','contentUrl':base+b['pdf']['name']},{'@type':'MediaObject','encodingFormat':'application/zip','contentUrl':base+b['zip']['name']}]
 else:
  for e in scholar['encoding']:need(e['encodingFormat']=='application/pdf','original119_PDF_encoding');e['contentUrl']=base+b['pdf']['name']
 schema={'@context':'https://schema.org','@graph':[{'@type':'WebPage','@id':base+'#page','url':base,'name':b['title'],'dateCreated':build_date,'dateModified':build_date,'mainEntity':{'@id':base+'#article'}},scholar]};schema_text=json.dumps(schema,ensure_ascii=False).replace('<','\\u003c');headhtml=serialize(head)[:-7]+'<script type="application/ld+json">'+schema_text+'</script></head>'
 header='<header><p class="site-title"><a href="/">Alec Kriebel</a></p><nav aria-label="Main navigation"><a href="/research/">Research</a> | <a href="/blog/">Blog</a> | <a href="https://orcid.org/0009-0001-9320-500X">ORCID</a></nav><p>Original Zenodo files: '+' · '.join('<a href="'+h(a['original_native_asset']['original_api_file_object']['links']['self'])+'">'+h(a['name'])+'</a>' for a in b['assets'])+'</p></header>'
 footer='<footer><hr><p><a href="/research/">Research home</a></p><p class="copyright">© 2013–2026 Kriebel LLC.</p></footer>'
 doc='<!doctype html>\n<html lang="en">'+headhtml+'<body><a class="skip-link" href="#main">Skip to content</a>'+header+serialize(main_tree(b))+footer+'</body></html>\n';Tree(doc);return doc.encode()
def overlays(bundles,build_date):
 authenticate_baseline();index=(OWN/'baseline/research/index.html').read_text();sitemap=(OWN/'baseline/research/sitemap.xml').read_text();rx=r'(<script type="application/ld\+json">\s*)(.*?)(\s*</script>)';m=re.search(rx,index,re.S);need(m is not None,'saved_index_schema');s=strict_json(m.group(2));items=s['mainEntity']['itemListElement'];need(len(items)==s['mainEntity']['numberOfItems']==83,'exact_released83_itemlist');lines=[];maps=[]
 for b in bundles:
  url='https://aleckriebel.com/research/'+b['slug']+'/';need('href="/research/'+b['slug']+'/"' not in index and '<loc>'+url+'</loc>' not in sitemap,'two_new_destinations_only');d=date.fromisoformat(b['publication_date']);stamp=str(d.day)+' '+MONTHS[d.month-1]+' '+str(d.year)
  lines.append('      <li><a href="/research/'+b['slug']+'/">'+h(b['title'])+'</a><br><span class="entry-meta">'+stamp+' · '+h(b['kind'])+'</span><p>'+h(b['description'])+'</p><p><a href="/research/'+b['slug']+'/'+b['pdf']['name']+'">PDF</a> · <a href="https://doi.org/'+b['doi']+'">Zenodo</a></p></li>\n');maps.append('  <url><loc>'+url+'</loc><lastmod>'+build_date+'</lastmod></url>\n');items.append({'@type':'ListItem','position':len(items)+1,'url':url,'name':b['title']})
 s['mainEntity']['numberOfItems']=85;index=index[:m.start(2)]+json.dumps(s,ensure_ascii=False)+index[m.end(2):];need(index.count('    </ul>')==1 and sitemap.count('</urlset>')==1,'exact_overlay_insertion_anchors');return {'research/index.html':index.replace('    </ul>',''.join(lines)+'    </ul>',1).encode(),'research/sitemap.xml':sitemap.replace('</urlset>',''.join(maps)+'</urlset>',1).encode()}
def files_in_memory(bundles,build_date):
 need(date.fromisoformat(build_date).isoformat()==build_date,'explicit_ISO_build_date');out=overlays(bundles,build_date)
 for b in bundles:
  prefix='research/'+b['slug']+'/';out[prefix+'index.html']=article_bytes(b,build_date);out[prefix+'citation.bib']=b['bib']
  for a in b['assets']:out[prefix+a['name']]=Path(a['path']).read_bytes()
 need(len(out)==11,'exact_two11_outputs');return out
def build(out,build_date):
 out=safe_output(out);need(not out.exists(),'absent_new_private_output_only');bs=load_bundles();files=files_in_memory(bs,build_date);out.mkdir(parents=True)
 for rel,data in files.items():p=out/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 return {'output_root':str(out),'files':11,'records':list(IDS),'proposed_canonical_inside_private_HTML_only':True,'native_canonical_assignment':None,'AA':None,'production_install_authorized':False,'browser_or_deployment_claimed':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output-root',type=Path,required=True);p.add_argument('--build-date',required=True);a=p.parse_args();print(json.dumps(build(a.output_root,a.build_date),indent=2))
