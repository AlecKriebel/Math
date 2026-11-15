"""Complete-copy/head/asset contracts, independent of the two renderer."""
from two_common import *
from two_dom import Tree,node,nodes,text,serialize
import copy,re
def significant(n):return [x for x in n['children'] if isinstance(x,dict) or x.strip()]
def signature(n):
 if isinstance(n,str):return ('text',n)
 return (n['tag'],tuple(sorted(n['attrs'].items())),tuple(signature(x) for x in n['children']))
def expected118_main(b):
 n=copy.deepcopy(Tree(b['source_html'],source_editorial=True).find('main')[0]);n['attrs']={'id':'main'};n['children']=[node('article',{},n['children'])]
 for x in nodes(n):
  a=x['attrs']
  for field in ['href','src']:
   if a.get(field,'').startswith('assets/'):
    name=a[field][7:];need(name in {'citation.bib'}|{v['name'] for v in b['assets']},'118_only_exact_asset_paths');a[field]=name
  if a.get('class')=='byline':a['class']='entry-meta'
  if x['tag']=='h1':x['children']=[node('a',{'href':'/research/'+b['slug']+'/'},x['children'])]
  if x['tag']=='iframe':a['class']='paper-pdf';a['loading']='lazy'
 return n
def source119_linear_blocks(raw):
 # Independent blank-block inspection of the complete approved Markdown,
 # rather than the renderer's line-oriented construction.
 expected=[]
 for block in re.split(r'\n\s*\n',raw.strip()):
  if block.startswith('```bibtex\n'):
   need(block.endswith('\n```'),'original_closed_BibTeX');expected.append(('code',block[len('```bibtex\n'):-4]+'\n'));continue
  if block.startswith('# '):expected.append(('h1',block[2:]));continue
  if block.startswith('## '):expected.append(('h2',block[3:]));continue
  lines=block.splitlines();values=[('li',line[2:]) for line in lines] if all(line.startswith('- ') for line in lines) else [('p',' '.join(lines))]
  for kind,value in values:expected.append((kind,re.sub(r'\[([^\]]+)\]\(([^\s)]+)\)',r'\1',value)))
 return expected
def check119_body(b,main):
 article=next(x for x in nodes(main) if x['tag']=='article');ordered=[(x['tag'],text(x)) for x in nodes(article) if x['tag'] in {'h1','h2','p','li','code'}];need(ordered==source119_linear_blocks(b['public_copy']),'every119_complete_Markdown_block_and_order')
 expected_hrefs=['/research/'+b['slug']+'/']+re.findall(r'\[[^\]]+\]\(([^\s)]+)\)',b['public_copy']);actual=[x['attrs']['href'] for x in nodes(article) if x['tag']=='a'];need(actual==expected_hrefs,'all119_original_link_destinations_and_order')
 need(set(x['tag'] for x in nodes(article))<={'article','header','h1','a','p','section','h2','ul','li','div','code','br','iframe'},'119_no_unapproved_body_elements')
 code=[x for x in nodes(article) if x['tag']=='code'];need(len(code)==1 and text(code[0])==b['bib'].decode(),'whole119_visible_BibTeX');need(all(isinstance(x,str) or x['tag']=='br' for x in code[0]['children']),'119_wrapping_BibTeX_only_linebreaks')
 div=[x for x in nodes(article) if x['tag']=='div'];need(len(div)==1 and div[0]['attrs']=={'class':'equation'} and significant(div[0])==code,'119_BibTeX_uses_existing_wrapping_style')
 reader=next(x for x in nodes(article) if x['tag']=='section' and x['attrs'].get('id')=='reader');anchors=[x for x in nodes(reader) if x['tag']=='a'];requirements=b['original']['whole_requirements_original']['reader']
 for field in ['local_PDF_download','local_ZIP_download','original_checksums_download','citation_download']:
  req=requirements[field];matches=[x for x in anchors if x['attrs'].get('href')==req['href'] and x['attrs'].get('download')==req['download_attribute']];need(len(matches)==1,'119_actual_required_download:'+field)
 for field in ['original_PDF_open_and_download','original_complete_ZIP_download']:need(requirements[field] in [x['attrs']['href'] for x in anchors],'119_original_complete_native_link:'+field)
 return article
def expected_head(b):
 base='https://aleckriebel.com/research/'+b['slug']+'/'
 if b['rid']=='23385145':
  old=Tree(b['source_html'],source_editorial=True);title=text(old.find('title')[0]);metas={}
  for n in old.find('meta'):
   a=n['attrs'];metas[a.get('name',a.get('property',a.get('charset')))]=a.get('content')
  scholar=copy.deepcopy(strict_json(text(old.find('script')[0])));scholar.pop('@context')
 else:
  title=b['title']+' | Alec Kriebel';metas={'utf-8':None,'viewport':'width=device-width, initial-scale=1','description':b['description'],**b['metadata']['citation_meta']}
  for key in ['type','title','description']:metas['og:'+key]=b['metadata']['open_graph'][key]
  scholar=copy.deepcopy(b['metadata']['jsonld']);scholar.pop('@context')
 metas.update({'robots':'index,follow','citation_pdf_url':base+b['pdf']['name'],'citation_author_orcid':'0009-0001-9320-500X','citation_language':'en'})
 for key,val in [('og:type','article'),('og:title',b['title']),('og:description',b['description'])]:metas.setdefault(key,val)
 metas['og:url']=base
 for key,val in [('name',b['title']),('version',b['version']),('creativeWorkStatus','Unrefereed preprint')]:scholar.setdefault(key,val)
 scholar.update({'@id':base+'#article','url':base,'sameAs':'https://doi.org/'+b['doi']})
 if 'encoding' in scholar:
  for e in scholar['encoding']:e['contentUrl']=base+b['pdf']['name']
 else:scholar['encoding']=[{'@type':'MediaObject','encodingFormat':'application/pdf','contentUrl':base+b['pdf']['name']},{'@type':'MediaObject','encodingFormat':'application/zip','contentUrl':base+b['zip']['name']}]
 return title,metas,scholar
def check_page(b,data,files,build_date):
 tree=Tree(data.decode());need(len(tree.find('main'))==len(tree.find('article'))==len(tree.find('h1'))==1,'one_complete_visible_article')
 main=tree.find('main')[0];need(main['attrs']=={'id':'main'},'main_skip_destination')
 if b['rid']=='23385145':need(signature(main)==signature(expected118_main(b)),'entire118_frozen_original_main_tree')
 else:check119_body(b,main)
 need(text(tree.find('h1')[0])==b['title'] and tree.find('h1')[0]['children']==[node('a',{'href':'/research/'+b['slug']+'/'},[b['title']])],'exact_title_proposed_self_link')
 body=significant(tree.find('body')[0]);need([x['tag'] for x in body]==['a','header','main','footer'],'exact_blog_wrapper_no_hidden_article')
 need(body[0]['attrs']=={'class':'skip-link','href':'#main'} and text(body[0])=='Skip to content','accessible_skip')
 navlinks=[x['attrs']['href'] for x in nodes(body[1]) if x['tag']=='a'];need(navlinks==['/','/research/','/blog/','https://orcid.org/0009-0001-9320-500X']+[a['original_native_asset']['original_api_file_object']['links']['self'] for a in b['assets']],'complete_original_native_asset_order_navigation')
 need(text(body[-1])=='Research home© 2013–2026 Kriebel LLC.','ordinary_footer')
 frame=tree.find('iframe');need(len(frame)==1 and frame[0]['attrs']=={'src':b['pdf']['name'],'title':(b['title']+' — original five-page PDF' if b['rid']=='23385145' else b['original']['whole_requirements_original']['reader']['accessible_title']),'class':'paper-pdf','loading':'lazy'},'complete_native_reader_accessibility_and_loading')
 base='https://aleckriebel.com/research/'+b['slug']+'/';title,metas,scholar=expected_head(b);need(len(tree.find('title'))==1 and text(tree.find('title')[0])==title,'complete_approved_SEO_title');actual={}
 for n in tree.find('meta'):
  a=n['attrs'];key=a.get('name',a.get('property',a.get('charset')));need(key not in actual,'no_duplicate_head_meta');actual[key]=a.get('content')
 need(actual==metas,'all_original_SEO_citation_OpenGraph_fields_and_types');need([(n['attrs'].get('rel'),n['attrs'].get('href')) for n in tree.find('link')]==[('canonical',base),('icon','/favicon.ico'),('stylesheet','/research/research.css')],'one_proposed_canonical_existing_white_Arial_stylesheet');need(not tree.find('style'),'no_hidden_or_inline_styles')
 scripts=tree.find('script');need(len(scripts)==1 and scripts[0]['attrs']=={'type':'application/ld+json'},'only_static_scholarly_JSON_script');s=strict_json(text(scripts[0]));need(list(s)==['@context','@graph'] and s['@context']=='https://schema.org' and len(s['@graph'])==2,'scholarly_schema_graph_shape')
 page={'@type':'WebPage','@id':base+'#page','url':base,'name':b['title'],'dateCreated':build_date,'dateModified':build_date,'mainEntity':{'@id':base+'#article'}};need(s['@graph'][0]==page and same(s['@graph'][1],scholar),'every_complete_scholarly_field_abstract_identity_date_and_type')
 expected={'index.html','citation.bib'}|{a['name'] for a in b['assets']};need(set(files)==expected,'all_native_plus_citation_leaves_including119_checksum');need(files['citation.bib']==b['bib'],'complete_original_prepared_citation')
 for a in b['assets']:need({'bytes':len(files[a['name']]),'sha256':sha(files[a['name']])}==bind(a['path']),'complete_original_native_asset:'+a['name'])
 if b['rid']=='22983513':
  checksum=files['SHA256SUMS.txt'].decode().splitlines();want={sha(files[b['pdf']['name']]):b['pdf']['name'],sha(files[b['zip']['name']]):b['zip']['name']};found={line.split()[0]:line.split()[-1].lstrip('*') for line in checksum};need(found==want,'original119_checksums_cover_exact_PDF_ZIP_not_new_BibTeX')
 for a in tree.find('a'):
  href=a['attrs']['href']
  if not href.startswith(('https://','/','#')):need(href in expected,'every_local_asset_link_resolves')
 return {'record_id':b['rid'],'literal_custom_status':'FULL_APPROVED_BODY_ABSTRACT_HEAD_NATIVE_ASSETS_AND_QUALIFICATIONS_RETAINED','native_assets':len(b['assets']),'actual_PDF_pages':b['ready']['selected_actual_PDF']['pages'],'original_flags_and_AA_unmodified':True}
