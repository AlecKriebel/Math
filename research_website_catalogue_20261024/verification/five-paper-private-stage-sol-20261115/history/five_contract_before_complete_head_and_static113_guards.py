"""Independent complete-copy contracts. Does not import the builder."""
from five_common import *
from five_markup import Tree,nodes,text,serialize
import copy,re
def significant(n):return [x for x in n['children'] if isinstance(x,dict) or x.strip()]
def signature(n):
 if isinstance(n,str):return ('text',n)
 return (n['tag'],tuple(sorted(n['attrs'].items())),tuple(signature(x) for x in n['children']))
def source_reconstruction(n):
 if isinstance(n,str):return n
 if 'data-tex' in n['attrs']:
  marker='$$' if n['tag']=='div' else '$';return marker+n['attrs']['data-tex']+marker
 inside=''.join(source_reconstruction(x) for x in n['children'])
 return inside+(' ' if n['tag'] in {'p','li','h1','h2','h3','ul','ol','section'} else '')
def md_words(raw):
 # Independent from the presentation lexer: preserve every TeX token and
 # remove only prose Markdown delimiters/link destinations in comparison.
 parts=re.split(r'(\$\$.*?\$\$|\$.*?\$)',raw,flags=re.S);out=[]
 for s in parts:
  if s.startswith('$'):out.append(s)
  else:
   s=re.sub(r'\[([^\]]+)\]\(([^\n]+?)\)',r'\1',s)
   s=re.sub(r'^###\s+','',s);out.append(s.replace('**','').replace('*',''))
 return ' '.join(''.join(out).split())
def canonical_prose(n):return ' '.join(source_reconstruction(n).split())
def expected_nested_main(b):
 # Full original main tree is retained. Only independently enumerated
 # publication path/style rebases are permitted; source/copy stays frozen.
 n=copy.deepcopy(Tree(b['source_html'],source_math_style=True).find('main')[0]);n['attrs']={'id':'main'}
 for e in nodes(n):
  a=e['attrs']
  for field in ['href','src']:
   v=a.get(field)
   if isinstance(v,str) and v.startswith('assets/'):
    basename=v[7:].split('#')[0];need(basename in {b['pdf']['name'],b['zip']['name']},'source_exact_asset_rebase');a[field]=v[7:]
  if a.get('href')=='../citation.bib':need(b['rid']=='23430498','115_only_BibTeX_parent_rebase');a['href']='citation.bib'
  if a.get('class'):
   a['class']=' '.join('equation' if c=='formula' else 'entry-meta' if c in {'byline','meta'} else c for c in a['class'].split())
  if 'style' in a:need(e['tag']=='span' and a.pop('style')=='white-space: nowrap','original_inline_math_style_only');a['class']='equation'
  if e['tag']=='iframe':a['class']='paper-pdf';a['loading']='lazy'
 return n
def verify113_body(b,main,dlab_homepage):
 c=b['c'];article=next(x for x in nodes(main) if x['tag']=='article')
 sections=[x for x in significant(article) if isinstance(x,dict) and x['tag']=='section']
 expected=[('abstract',c['abstract_heading'],[c['abstract']]),('plain-language','The idea in plain English',c['plain_language']),('result','The precise result',c['result']),('proof','Why the result holds',c['why_it_works']),('limits','Scope and limitations',c['limitations']),('status','Status and AI use',[c['status'],c['ai_disclosure'],c['edition_note']])]
 need([x['attrs'].get('id') for x in sections]==['abstract','plain-language','result','proof','limits','status','paper','materials','collaborate','cite','background'],'all113_sections_and_order')
 for sid,label,values in expected:
  sec=next(s for s in sections if s['attrs']['id']==sid);children=significant(sec)
  need(children[0]['tag']=='h2' and text(children[0])==label,'113_section_label:'+sid)
  need(len(children)==len(values)+1,'all113_paragraphs_and_equations:'+sid)
  for src,actual in zip(values,children[1:]):
   tag='div' if src.startswith('$$') else 'h3' if src.startswith('### ') else 'p'
   need(actual['tag']==tag and canonical_prose(actual)==md_words(src),'complete113_source_words_and_TeX:'+sid)
 for math in [n for n in nodes(main) if 'data-tex' in n['attrs']]:
  need(math['attrs']['role']=='math' and math['attrs']['aria-label']==math['attrs']['data-tex'],'original_math_accessibility_and_complete_token_source')
  approved=load(OWN/'MATH_PRESENTATION_AUDIT.json')['approved_visible_HTML']
  need(math['attrs']['data-tex'] in approved and ''.join(serialize(x) for x in math['children'])==approved[math['attrs']['data-tex']],'exact_manually_reviewed_visible_math_presentation')
 background=next(s for s in sections if s['attrs']['id']=='background')
 expected_text=md_words(c['background'].replace('* ',' '))
 need(canonical_prose(background).removeprefix('Background and prior work').strip()==expected_text,'entire113_background_and_credit_sentences')
 expected_urls=re.findall(r'\]\(([^\n]+?)\)',c['background'])
 if dlab_homepage:expected_urls=[NEW_DLAB if x==OLD_DLAB else x for x in expected_urls]
 actual_urls=[n['attrs']['href'] for n in nodes(background) if n['tag']=='a']
 need(actual_urls==expected_urls,'all113_background_destinations_and_one_authorized_delta')
 collaboration=next(s for s in sections if s['attrs']['id']=='collaborate')
 need(text(next(x for x in nodes(collaboration) if x['tag']=='p'))==c['collaboration'],'entire113_contribution_based_collaboration')
 reader=next(s for s in sections if s['attrs']['id']=='paper');ps=[x for x in nodes(reader) if x['tag']=='p']
 need(text(ps[0])==c['reader_intro'],'complete113_reader_intro')
 links=[n['attrs'] for n in nodes(reader) if n['tag']=='a'];need([x['href'] for x in links]==[b['pdf']['name'],b['pdf']['name']] and 'download' in links[1],'113_open_and_download_whole_reader')
 material=next(s for s in sections if s['attrs']['id']=='materials');links=[n for n in nodes(material) if n['tag']=='a']
 need([n['attrs']['href'] for n in links]==[b['zip']['name']]+[x['url'] for x in c['related_resources']],'113_complete_material_links')
 need([text(n) for n in links]==[c['supplement_label']]+[x['label'] for x in c['related_resources']],'113_complete_material_labels')
 need('Authored paper, prose and code: CC BY 4.0. Cited third-party works retain their own rights.' in text(material),'113_exact_license_scope')
 cite=next(s for s in sections if s['attrs']['id']=='cite');need('Version '+b['version'] in text(cite) and 'https://doi.org/'+b['doi'] in text(cite),'113_versioned_citation')
 header=significant(article)[0];need(header['tag']=='header' and 'Version '+b['version'] in text(header) and b['title'] in text(header),'113_exact_title_byline_version')
 # No additional article content outside the header and enumerated sections.
 need(significant(article)==[header,*sections],'no_extra113_prose_or_hidden_status')
def check_page(b,data,files,build_date,*,dlab_homepage):
 source=data.decode('utf8');tree=Tree(source);main=tree.find('main');need(len(main)==1,'single_complete_main')
 need(len(tree.find('h1'))==1 and text(tree.find('h1')[0])==b['title'],'exact_h1')
 need(len(tree.find('article'))==1 and len(tree.find('style'))==0,'one_article_no_hidden_styles')
 if b['source_html'] is not None:need(signature(main[0])==signature(expected_nested_main(b)),'complete_frozen_editorial_main_tree:'+b['rid'])
 else:verify113_body(b,main[0],dlab_homepage)
 frame=tree.find('iframe');need(len(frame)==1 and frame[0]['attrs']['class']=='paper-pdf' and frame[0]['attrs'].get('loading')=='lazy','one_complete_accessible_reader')
 need(frame[0]['attrs']['src'].split('#')[0]==b['pdf']['name'] and frame[0]['attrs'].get('title'),'correct_unmodified_PDF_frame')
 # Exact closed wrapper: skip link, ordinary blog header, frozen main, footer.
 body=tree.find('body')[0];children=significant(body);need([n['tag'] for n in children]==['a','header','main','footer'],'exact_simple_blog_wrapper')
 need(children[0]['attrs']=={'class':'skip-link','href':'#main'} and text(children[0])=='Skip to content','accessible_skip_link')
 wrapper=children[1];anchors=[n for n in nodes(wrapper) if n['tag']=='a'];expect=['/','/research/','/blog/','https://orcid.org/0009-0001-9320-500X']+[a['native_original_object']['original_api_file_object']['links']['self'] for a in b['asset_view']]
 need([a['attrs']['href'] for a in anchors]==expect,'ordinary_navigation_and_original_native_asset_order')
 need(text(children[-1])=='Research home© 2013–2026 Kriebel LLC.','exact_footer_no_new_outreach')
 head=tree.find('head')[0];links=tree.find('link');base='https://aleckriebel.com/research/'+b['slug']+'/'
 need([(x['attrs'].get('rel'),x['attrs'].get('href')) for x in links]==[('canonical',base),('icon','/favicon.ico'),('stylesheet','/research/research.css')],'one_proposed_canonical_and_unchanged_blog_stylesheet')
 metas=tree.find('meta');names={}
 for x in metas:
  k=x['attrs'].get('name',x['attrs'].get('property',x['attrs'].get('charset')));need(k not in names,'no_duplicate_metadata');names[k]=x['attrs'].get('content')
 for key,value in [('robots','index,follow'),('citation_title',b['title']),('citation_author','Alec Kriebel'),('citation_publication_date',b['publication_date'].replace('-','/')),('citation_doi',b['doi']),('citation_pdf_url',base+b['pdf']['name']),('citation_author_orcid','0009-0001-9320-500X'),('description',b['description']),('og:type','article'),('og:url',base)]:need(names.get(key)==value,'complete_native_metadata:'+key)
 scripts=tree.find('script');need(len(scripts)==1 and scripts[0]['attrs']=={'type':'application/ld+json'},'only_nonexecuting_scholarly_JSON')
 schema=strict_json(text(scripts[0]));graph=schema['@graph'];need(schema['@context']=='https://schema.org' and len(graph)==2,'exact_scholarly_graph_envelope')
 webpage,article=graph;need(webpage=={'@type':'WebPage','@id':base+'#page','url':base,'name':b['title'],'dateCreated':build_date,'dateModified':build_date,'mainEntity':{'@id':base+'#article'}},'explicit_build_date_not_original_date')
 original_scholar=(strict_json(text(Tree(b['source_html'],source_math_style=True).find('script')[0])) if b['source_html'] is not None else None)
 scholarly_description=original_scholar['description'] if original_scholar is not None else b['description']
 for key,val in [('@type','ScholarlyArticle'),('@id',base+'#article'),('url',base),('sameAs','https://doi.org/'+b['doi']),('name',b['title']),('headline',b['title']),('description',scholarly_description),('abstract',b['abstract']),('datePublished',b['publication_date']),('version',b['version']),('creativeWorkStatus',b['kind'])]:need(article.get(key)==val,'complete_scholarly_value:'+key)
 need(article['identifier']=={'@type':'PropertyValue','propertyID':'DOI','value':b['doi']} and article['license']=='https://creativecommons.org/licenses/by/4.0/','DOI_license_identity')
 enc=article['encoding'];enc=enc if isinstance(enc,list) else [enc]
 need(any(x['encodingFormat']=='application/pdf' and x['contentUrl']==base+b['pdf']['name'] for x in enc),'proposed_local_unchanged_reader_metadata')
 if b['source_html'] is not None:
  original=original_scholar;expected=copy.deepcopy(original);expected.pop('@context',None)
  if 'abstract' not in expected:expected['abstract']=b['abstract']
  expected['@id']=base+'#article';expected['url']=base;expected['sameAs']='https://doi.org/'+b['doi']
  values=expected['encoding'];values=values if isinstance(values,list) else [values]
  for x in values:x['contentUrl']=base+(b['pdf']['name'] if x['encodingFormat']=='application/pdf' else b['zip']['name'])
  need(same(article,expected),'every_original_scholarly_field_and_type_retained')
 expected_files={'index.html','citation.bib',b['pdf']['name'],b['zip']['name']}
 need(set(files)==expected_files,'exact_four_article_outputs')
 need(files['citation.bib']==b['bib'],'whole_prepared_BibTeX_bytes')
 for a in b['asset_view']:need(bind(a['path'])=={'bytes':len(files[a['name']]),'sha256':sha(files[a['name']])},'complete_original_PDF_ZIP_bytes')
 for n in tree.find('a'):
  href=n['attrs']['href']
  if not href.startswith(('https://','/','#')):need(href in expected_files,'every_local_link_resolves_to_complete_asset')
 return {'literal_status':'COMPLETE_NEW_TARGET_BODY_METADATA_READERS_AND_NATIVE_BYTES_AGREE','record_id':b['rid'],'full_source_main_tree_or_all_MD_blocks_checked':True,'root_editorial_source_flags_unmodified':True}
