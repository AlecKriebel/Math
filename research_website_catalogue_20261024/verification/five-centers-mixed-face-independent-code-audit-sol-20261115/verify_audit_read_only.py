#!/usr/bin/env python3
"""Independent sealed-stage/output custody. No rendering, project imports, network or writes."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,html,json,re,sys
import xml.etree.ElementTree as ET
A=Path(__file__).resolve().parent
S=A.parent/'five-centers-mixed-face-private-stage-sol-20261115'
checks=0;typed=0
def need(c,m):
 global checks
 checks+=1
 if not c:raise ValueError(m)
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def check(e,base=None):
 p=Path(e['path'])
 if not p.is_absolute():p=base/p
 b=p.read_bytes();need(not p.is_symlink(),'symlink '+str(p));need(len(b)==e['bytes'] and sha(b)==e.get('SHA256',e.get('sha256')),'whole bytes '+str(p));return b
def same(a,b):
 if type(a) is not type(b):return False
 if isinstance(a,dict):return list(a)==list(b) and all(same(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
def whole(a,b,label):
 global typed
 need(same(a,b),'typed/key/list/null whole '+label);typed+=1
def script(t):
 ss=re.findall(r'<script\b[^>]*>(.*?)</script>',t,re.S);ld=re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',t,re.S)
 need(len(ss)==len(ld)==1,'single inert JSONLD script');return json.loads(ld[0]),ld[0]
class Head(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.meta=[];self.links=[];self.in_title=False;self.title=''
 def handle_starttag(self,t,attrs):
  d=dict(attrs)
  if t=='meta':self.meta.append(d)
  if t=='link':self.links.append(d)
  if t=='title':self.in_title=True
 def handle_endtag(self,t):
  if t=='title':self.in_title=False
 def handle_data(self,s):
  if self.in_title:self.title+=s
def main():
 args=set(sys.argv[1:]);need(args<=set(['--preseal','--live-baseline']),'recognized options only');pre='--preseal' in args;live='--live-baseline' in args
 need(pre or (A/'FINAL_SEAL.json').exists(),'default requires final audit seal')
 if not pre:
  final=load(A/'FINAL_SEAL.json');need(final['status']=='FINAL_PASS_PRIVATE_EXACT11_INTEGRATION_AUDIT_NO_PRODUCTION_AUTHORITY','literal final audit status')
  for e in final['bindings'].values():check(e)
  fm=load(A/'FINAL_MANIFEST.json')
  for e in fm['files']:check(e)
  names={q.relative_to(A).as_posix() for q in A.rglob('*') if q.is_file()}
  need(names=={Path(e['path']).relative_to(A).as_posix() for e in fm['files']}|{'FINAL_MANIFEST.json','FINAL_CLOSURE.json','FINAL_SEAL.json'},'entire own final namespace; exact root terminals only')
 for n in ['INITIAL_MANIFEST.json','BASELINE_MANIFEST.json']:
  for e in load(A/n)['files']:check(e)
 need(not any(q.is_symlink() for q in A.rglob('*')),'no own symlinks')
 need(sha((S/'FINAL_SEAL.json').read_bytes())=='1fb0b5d399d013a729e3d709e18581e011d1643f88e1622f63dd62d2169cd24f','neutral writer FINAL anchor')
 need(sha((S/'OWNED_MANIFEST.json').read_bytes())=='cc692a0f9da84cec8c45c7e38350474bd3a7d16694dc15d7de59135845988be2','neutral writer manifest anchor')
 sm=load(S/'OWNED_MANIFEST.json');need(sm['only_exact_root_terminal_exclusions']==['OWNED_MANIFEST.json','FINAL_SEAL.json'],'writer exact root terminals')
 need(not any(q.is_symlink() for q in S.rglob('*')),'writer namespace no symlinks')
 need({q.relative_to(S).as_posix() for q in S.rglob('*') if q.is_file()}==set(sm['payloads'])|{'OWNED_MANIFEST.json','FINAL_SEAL.json'},'entire963 writer namespace')
 need(len(sm['payloads'])==961,'whole961 writer payloads')
 for n,e in sm['payloads'].items():check({'path':str(S/n),**e})
 need(sorted(q.relative_to(S).as_posix() for q in S.rglob('*') if q.is_dir())==sm['directories'],'whole writer directories')
 for e in load(S/'CURRENT_CODE_MANIFEST.json')['files']:check(e,S)
 # Whole original source/private/custom data, not a semantic scientific replay.
 si=load(S/'SOURCE_INPUTS.json');need(len(si['files'])==341,'whole341 writer original paths')
 for e in si['files']:
  b=check(e);held=check({'path':str(S/e['blob']),'bytes':e['bytes'],'SHA256':e['SHA256']});need(b==held,'whole original stage snapshot')
  try:x=json.loads(b);y=json.loads(held)
  except (UnicodeDecodeError,json.JSONDecodeError):continue
  whole(x,y,'entire original JSON object')
 source_names=load(A/'PROTECTED_NAMESPACE_MANIFEST.json')['namespaces']
 for ns in source_names:
  root=Path(ns['path']);need({str(q) for q in root.rglob('*') if q.is_file()}=={e['path'] for e in ns['files']},'complete original121/69/81/59 membership')
  for e in ns['files']:check(e)
 ownbase=load(A/'FRESH_WEBSITE_BASELINE.json');old={e['public_relative_path']:check(e['snapshot']) for e in ownbase['public_files']};need(len(old)==614,'own entire614 baseline')
 wb=load(S/'WEBSITE_BASELINE.json');need(wb['baseline_counts']==[614,92,93] and wb['local_HEAD_and_origin_master_tracking']==ownbase['HEAD'],'independently captured same actual baseline identity')
 stage_old={}
 W=Path(ownbase['website_root'])
 for e in wb['files']:
  data=check({'path':str(S/e['blob']),'bytes':e['bytes'],'SHA256':e['SHA256']})
  if Path(e['path']).is_relative_to(W/'public'):stage_old[Path(e['path']).relative_to(W/'public').as_posix()]=data
 need(stage_old==old and set(wb['public_namespace'])==set(old),'all614 independently frozen whole bodies agree')
 for e in ownbase['configs']:
  row=next(x for x in wb['files'] if x['path']==e['source_path']);need((S/row['blob']).read_bytes()==check(e['snapshot']),'both whole site configs agree')
 scope=load(A/'ACTUAL_EXPECTED_OUTPUT_PATHS.json')['paths'];wanted={e['website_relative_path'] for e in scope}
 output={}
 for name in ['candidate-a','candidate-b']:
  root=S/name/'public';need({q.relative_to(root).as_posix() for q in root.rglob('*') if q.is_file()}==wanted,'exact11 actual '+name+' scope')
  need(not any(q.is_symlink() for q in root.rglob('*')),'actual candidate no symlinks')
  for n in wanted:
   data=(root/n).read_bytes()
   if name=='candidate-a':output[n]=data
   else:need(output[n]==data,'all11 complete normal/optimized buffers equal')
 overlay=load(S/'OVERLAY_MANIFEST.json')['files'];need({e['path'] for e in overlay}==wanted,'entire overlay manifest scope')
 for e in overlay:need(len(output[e['path']])==e['bytes'] and sha(output[e['path']])==e['SHA256'],'whole actual overlay manifest')
 need(len(wanted)==11 and len(wanted-set(old))==9 and len(set(old)|wanted)==623 and len(set(old)-wanted)==612,'exact11 virtual623 and612 unrelated paths')
 expect=load(A/'INDEPENDENT_EXPECTATIONS.json');frame=load(A/'BASELINE_STANDARD_FRAME.json');go=load(S/'ROOT_WEBSITE_GO.json')
 need(go['installed_commit']==ownbase['HEAD'] and go['baseline_counts']==[614,92,93],'same actually authorized GO')
 article_results=[]
 for t in expect['targets']:
  rid=t['record_id'];c=load(A/'inputs'/rid/'publication.json');original=load(A/'inputs'/rid/'SCHOLARLY_METADATA.json');base='research/'+c['slug']+'/';canonical=t['future_canonical_proposal_not_current_authority'];text=output[base+'index.html'].decode()
  mains=re.findall(r'<main\b[^>]*>.*?</main>',text,re.S);need(len(mains)==1,'one complete actual main')
  need((mains[0]+'\n').encode()==check(t['expected_complete_transformed_main']),'complete independently frozen main exactly')
  need(text.split('<body>',1)[1].split('<main',1)[0]==frame['whole_body_prefix_before_main'],'exact shared skip/header/navigation')
  need(text.split('</main>',1)[1]==frame['whole_suffix_after_main'],'exact shared footer')
  need(re.findall(r'<style>(.*?)</style>',text,re.S)==frame['nonhiding_supplemental_CSS'],'exact approved nonhiding supplemental CSS')
  need('<object' not in mains[0] and t['exact_reader_transform']['to'] in mains[0],'exact approved iframe initial FitH')
  head=Head();head.feed(text.split('</head>',1)[0]);meta={}
  for e in head.meta:
   k=e.get('name',e.get('property'))
   if k:need(k not in meta,'no duplicate meta '+k);meta[k]=e.get('content')
  required={'viewport':'width=device-width, initial-scale=1','description':c['description'],'author':'Alec Kriebel','robots':'index,follow','citation_title':c['title'],'citation_author':'Alec Kriebel','citation_author_orcid':c['orcid'],'citation_publication_date':c['publication_date'].replace('-','/'),'citation_doi':c['doi'],'citation_pdf_url':canonical+c['pdf_filename'],'citation_language':'en','twitter:card':'summary','og:type':'article','og:title':c['title'],'og:description':c['description'],'og:url':canonical,'og:site_name':'Alec Kriebel','article:published_time':c['publication_date']}
  if t['native_version_present']:required['citation_version']='1.0.0'
  need(meta==required,'all and only exact approved public meta values')
  need(head.title==c['title']+' | Alec Kriebel','exact readable SEO title')
  need(head.links==[{'rel':'canonical','href':canonical},{'rel':'icon','href':'/favicon.ico'},{'rel':'stylesheet','href':'/research/research.css'}],'exact canonical/favicon/stylesheet')
  graph,_=script(text);need(graph['@context']=='https://schema.org' and len(graph['@graph'])==2,'linked two-node scholarly graph')
  page,article=graph['@graph'];need(page['@type']=='WebPage' and article['@type']=='ScholarlyArticle','graph roles')
  need(page=={'@type':'WebPage','@id':canonical+'#page','url':canonical,'name':c['title'],'dateCreated':go['build_date'],'dateModified':go['build_date'],'mainEntity':{'@id':canonical+'#article'}},'exact WebPage publication/build-date distinction')
  allowed={'@id','url','mainEntityOfPage','encoding','inLanguage','isAccessibleForFree'}
  need(set(article)==set(original)|allowed,'no extra/private scholarly keys')
  for k,v in original.items():
   if k not in allowed:whole(article[k],v,'whole adopted scholarly field '+k)
  need(article['url']==canonical and article['@id']==canonical+'#article' and article['mainEntityOfPage']=={'@id':canonical+'#page'} and article['inLanguage']=='en' and article['isAccessibleForFree'] is True,'exact local linked article')
  need(article['abstract']==t['full_unchanged_abstract'] and html.escape(t['full_unchanged_abstract']) in mains[0],'full abstract visible and scholarly')
  enc=[{'@type':'MediaObject','encodingFormat':e['encodingFormat'],'contentUrl':e['contentUrl'],'sameAs':e['sameAs'],'license':e['license']} for e in t['native_assets_and_media_expectations_in_original_order']]
  whole(article['encoding'],enc,'whole native ordered media objects')
  for e in t['native_assets_and_media_expectations_in_original_order']:
   need(output[base+e['filename']]==check(e['whole_original_source_asset']),'whole native original at article root')
  need(output[base+'citation.bib']==(A/'inputs'/rid/'citation.bib').read_bytes(),'whole unchanged Bib at article root')
  if not t['native_version_present']:need('version' not in article and 'citation_version' not in meta,'130 missing version remains omitted')
  else:need(article['version']==meta['citation_version']=='1.0.0','131 literal1.0.0 edition')
  article_results.append({'record_id':rid,'complete_HTML_bytes':len(output[base+'index.html']),'HTML_SHA256':sha(output[base+'index.html']),'whole_expected_main_equal':True,'native_asset_count':len(enc)})
 oldindex=old['research/index.html'].decode();newindex=output['research/index.html'].decode();og,os=script(oldindex);ng,ns=script(newindex)
 need(list(og)==list(ng) and list(og['mainEntity'])==list(ng['mainEntity']),'whole index key orders')
 for k,v in og.items():
  if k!='mainEntity':whole(ng[k],v,'entire unchanged index field '+k)
 whole(ng['mainEntity']['itemListElement'][:92],og['mainEntity']['itemListElement'],'all92 original typed ordered entries')
 newitems=[{'@type':'ListItem','position':93+i,'url':t['future_canonical_proposal_not_current_authority'],'name':t['whole_public_config_unique_fields_in_original_order']['title']} for i,t in enumerate(expect['targets'])]
 whole(ng['mainEntity']['itemListElement'][92:],newitems,'two exact new typed entries')
 need(ng['mainEntity']['numberOfItems']==len(ng['mainEntity']['itemListElement'])==94,'candidate typed94')
 oldcards=re.findall(r'<li\b[^>]*>.*?</li>',oldindex,re.S);newcards=re.findall(r'<li\b[^>]*>.*?</li>',newindex,re.S)
 need(newcards[:92]==oldcards and len(newcards)==94,'all92 whole original visible cards plus2')
 restored=newindex.replace(ns,os,1)
 for card in newcards[92:]:restored=restored.replace('      '+card+'\n','',1)
 need(restored==oldindex,'recover entire old research index bytes')
 for card,t in zip(newcards[92:],expect['targets']):
  c=t['whole_public_config_unique_fields_in_original_order'];base='/research/'+c['slug']+'/'
  need('<a href="'+base+'">'+html.escape(c['title'])+'</a>' in card and c['publication_date_label']+' · Unrefereed preprint' in card,'new card exact title/date/status')
  need(html.escape(c['description']) in card and 'href="'+base+c['pdf_filename']+'"' in card and 'href="https://doi.org/'+c['doi']+'"' in card,'new card exact adopted summary/PDF/DOI')
 oldxml=old['research/sitemap.xml'].decode();newxml=output['research/sitemap.xml'].decode();on=re.findall(r'<url>.*?</url>',oldxml,re.S);nn=re.findall(r'<url>.*?</url>',newxml,re.S)
 need(len(nn)==95 and nn[:93]==on,'all93 whole original sitemap nodes plus2')
 root=ET.fromstring(newxml);locs=[x.text for x in root.findall('{*}url/{*}loc')];need(len(locs)==len(set(locs))==95,'candidate95 distinct parsed locations')
 restored=newxml
 for node,t in zip(nn[93:],expect['targets']):
  need(node=='<url><loc>'+t['future_canonical_proposal_not_current_authority']+'</loc><lastmod>'+go['build_date']+'</lastmod></url>','two exact new sitemap node identities')
  restored=restored.replace('  '+node+'\n','',1)
 need(restored==oldxml,'recover entire original sitemap bytes')
 execution=load(S/'EXECUTION_LEDGER.json')
 need(execution['actual_render_process_exit_codes']==[0,0] and execution['actual_render_optimization_levels']==[0,1] and execution['render_code_changed_after_builds'] is False,'bound prior render evidence')
 for item in execution['actual_tool_results']:
  check(item['stdout'],S);err=check(item['stderr'],S);need(err==b'' and item['actual_process_exit_code']==0,'bound actual prior process result')
  whole(load(S/item['stdout']['path']),item['whole_actual_stdout_object'],'entire original prior stdout object')
 need(load(S/'FINAL_SEAL.json')['production_installation_authorized'] is False,'writer seal grants no production authority')
 if live:
  need({q.relative_to(W/'public').as_posix() for q in (W/'public').rglob('*') if q.is_file()}==set(old),'live actual public namespace unchanged')
  for n,b in old.items():need((W/'public'/n).read_bytes()==b,'live entire614 body unchanged')
  for e in ownbase['configs']:need(Path(e['source_path']).read_bytes()==check(e['snapshot']),'live exact site config')
  gi=load(A/'FRESH_GIT_OBSERVATIONS.json');check(gi['actual_raw_index_file_observation'])
  for e in load(A/'CORE17_AND_AUTHORIZED_CHECKPOINT.json')['current_actual_file_snapshots']:check(e['source'])
 print(json.dumps({'status':'PASS_INDEPENDENT_EXACT11_PRIVATE_INTEGRATION_AUDIT','checks':checks,'whole_typed_objects':typed,'stage_payloads':961,'stage_files':963,'whole_baseline_public_files':614,'paired_outputs':11,'new_leaves':9,'unchanged_native_assets':5,'unchanged_BibTeX':2,'candidate_counts':[623,94,95],'old_typed_visible_cards':92,'old_whole_XML_nodes':93,'protected_unrelated_public_paths':612,'fresh_protected_index_records':58552,'articles':article_results,'optional_live_baseline_compared':live,'renderer_or_fault_or_scientific_replay':False,'network':0,'subprocesses':0,'writes':0,'project_imports':0,'production_authority':False},indent=2))
if __name__=='__main__':main()
