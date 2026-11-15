#!/usr/bin/env python3
"""Independent pair custody. Stdlib only; no writes, imports of project code,
subprocesses, network, rendering, native/science execution. The optional
--live-baseline fence is deliberately separate from durable default custody.
--faults applies only new bounded edits to copied in-memory output buffers.
"""
from pathlib import Path
import copy
import hashlib
import html
from html.parser import HTMLParser
import json
import re
import sys
import xml.etree.ElementTree as ET

A=Path(__file__).resolve().parent
S=A.parent/'lefschetz-link-private-stage-sol-20261115'
checks=0
comparisons=[]
def need(ok,label):
 global checks
 checks+=1
 if not ok: raise ValueError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return p.read_bytes()
def obj(p):return json.loads(read(p))
def binding(p,r):
 b=read(p);need(len(b)==r['bytes'] and sha(b)==r['SHA256'],'byte binding '+str(p));return b
def equal(x,y):
 if type(x) is not type(y):return False
 if isinstance(x,dict):return list(x)==list(y) and all(equal(x[k],y[k]) for k in x)
 if isinstance(x,list):return len(x)==len(y) and all(equal(a,b) for a,b in zip(x,y))
 return x==y
def whole(x,y,label):
 need(equal(x,y),'whole typed/key/list/order/null '+label)
 comparisons.append({'label':label,'equal':True,'whole_ordered_SHA256':sha(json.dumps(x,ensure_ascii=False,separators=(',',':')).encode())})
def files(p):return sorted(str(f.relative_to(p)) for f in p.rglob('*') if f.is_file())
def dirs(p):return sorted(str(f.relative_to(p)) for f in p.rglob('*') if f.is_dir())
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__(convert_charrefs=True);self.meta={};self.links=[];self.scripts=[];self.tags=[];self._script=None;self.feed(text)
 def handle_starttag(self,t,a):
  d=dict(a);self.tags.append((t,d));need(len(a)==len(d),'no duplicate HTML attributes')
  if t=='meta':
   k=d.get('name',d.get('property', 'charset'));need(k not in self.meta,'unique metadata '+k);self.meta[k]=d.get('content',d.get('charset'))
  if t=='link':self.links.append(d)
  if t=='script':self._script=[d,''];self.scripts.append(self._script)
 def handle_endtag(self,t):
  if t=='script':self._script=None
 def handle_data(self,d):
  if self._script is not None:self._script[1]+=d

def jsonscript(t):
 parts=re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',t,re.S)
 need(len(parts)==1,'exactly one structured-data script');return json.loads(parts[0]),parts[0]
def restore_script(t,new):
 return re.sub(r'(<script\b[^>]*type="application/ld\+json"[^>]*>).*?(</script>)',lambda m:m[1]+new+m[2],t,count=1,flags=re.S)

E=obj(A/'EXPECTED_OUTPUTS.json');C=obj(A/'WHOLE_NATIVE_AND_EDITORIAL_CONTRACT.json');B=obj(A/'BASELINE.json');I=obj(A/'INPUT_MANIFEST.json')
W=Path(B['website_root']);records=C['records'];paths=E['exact_overlay_paths'];CC='https://creativecommons.org/licenses/by/4.0/'
oldindex=read(A/'baseline/index.html').decode();oldsitemap=read(A/'baseline/sitemap.xml').decode()
oldgraph,oldscript=jsonscript(oldindex)
oldli=re.findall(r'<li\b[^>]*>.*?</li>',oldindex,re.S)
oldnodes=re.findall(r'<url>.*?</url>',oldsitemap,re.S)
need(len(oldli)==90 and len(oldnodes)==91,'own actual baseline90/91')

# This oracle uses the pre-writer source contract and independent fresh baseline.
# It does not trust the writer's generated output contract or validation code.
def output_oracle(buffers):
 need(sorted(buffers)==paths,'independent exact eleven paths')
 expected_new=[]
 for r in records:
  slug=r['slug'];base='research/'+slug+'/';canonical=r['canonical_proposal'];t=buffers[base+'index.html'].decode();p=Page(t)
  ms=re.findall(r'<main\b[^>]*>.*?</main>',t,re.S)
  need(len(ms)==1 and ms[0]==r['expected_main_with_only_missing_id'],'exact whole original main '+r['record_id'])
  abstract=re.search(r'<section id="abstract">.*?<p>(.*?)</p>',ms[0],re.S)
  need(abstract is not None and html.unescape(abstract[1])==r['full_original_abstract'],'visible whole original abstract')
  m=p.meta
  requirements={'description':r['description'],'author':'Alec Kriebel','robots':'index,follow','citation_title':r['title'],'citation_author':'Alec Kriebel','citation_author_orcid':'https://orcid.org/0009-0001-9320-500X','citation_publication_date':r['datePublished'].replace('-','/'),'citation_version':r['native_version'],'citation_doi':'10.5281/zenodo.'+r['record_id'],'citation_language':'en','og:type':'article','og:title':r['title'],'og:description':r['description'],'og:url':canonical,'og:site_name':'Alec Kriebel','article:published_time':r['datePublished']}
  pdf=next(n for n in r['native_order'] if n.endswith('.pdf'));requirements['citation_pdf_url']=canonical+'assets/'+pdf
  for k,v in requirements.items():need(m.get(k)==v,'metadata '+r['record_id']+'/'+k)
  need('<title>'+html.escape(r['title'])+' | Alec Kriebel</title>' in t,'unique full title')
  for rel,url in [('canonical',canonical),('icon','/favicon.ico'),('stylesheet','/research/research.css')]:need([x['href'] for x in p.links if x.get('rel')==rel]==[url],'existing shared asset/canonical '+rel)
  need((W/'public/favicon.ico').as_posix() in baseline_by_path,'frozen existing favicon')
  need((W/'public/research/research.css').as_posix() in baseline_by_path,'frozen existing stylesheet')
  need(len(p.scripts)==1 and p.scripts[0][0]=={'type':'application/ld+json'},'no executable scripts')
  need(not re.search(r'\son[a-z]+\s*=',t,re.I),'no event handlers')
  styles=re.findall(r'<style>(.*?)</style>',t,re.S);need(len(styles)==1,'single bounded supplementary style')
  css=styles[0]
  need(not re.search(r'display\s*:\s*none|visibility\s*:\s*hidden|opacity\s*:\s*0|font-size\s*:\s*0|position\s*:\s*(absolute|fixed)|content\s*:',css,re.I),'nonhiding main styles')
  need('overflow-wrap:anywhere' in css and 'width:100%' in css and 'height:80vh' in css and 'min-height:500px' in css,'responsive full PDF and long formulas')
  need(r['actual_candidate_iframe_tag'] in ms[0] and ms[0].count('<iframe')==1,'original whole iframe')
  need('<a class="skip-link" href="#main">Skip to content</a>' in t,'skip link reaches main')
  foot=t.split('</main>',1)[1]
  need(foot=='\n<footer>\n<hr>\n<p><a href="/research/">Research home</a></p>\n<p class="copyright">© 2013–2026 Kriebel LLC.</p>\n</footer>\n</body>\n</html>\n','complete shared footer')
  graph,_=jsonscript(t);need(list(graph)==['@context','@graph'] and graph['@context']=='https://schema.org','graph shape')
  need(len(graph['@graph'])==2,'two linked nodes')
  page,article=graph['@graph'];need(page['@type']=='WebPage' and article['@type']=='ScholarlyArticle','WebPage/ScholarlyArticle')
  need(page['@id']==canonical+'#page' and page['url']==canonical and page['mainEntity']=={'@id':canonical+'#article'} and page['name']==r['title'],'WebPage identity')
  need(page['dateCreated']==page['dateModified']=='2026-11-15' and article['datePublished']==r['datePublished'],'builddate distinct original publication')
  need(article['@id']==canonical+'#article' and article['url']==canonical and article['mainEntityOfPage']=={'@id':canonical+'#page'},'mutual graph links')
  for k,v in r['original_full_scholarly_object'].items():
   if k not in ['@id','url','mainEntityOfPage','inLanguage','isAccessibleForFree','encoding']:
    need(equal(article.get(k),v),'original complete scholarly field '+k)
  need(article['abstract']==r['full_original_abstract'] and article['version']==r['native_version'],'whole abstract and native version')
  need(article['inLanguage']=='en' and article['isAccessibleForFree'] is True and article['creativeWorkStatus']=='Unrefereed preprint','language/access/review')
  enc=article['encoding'];need(len(enc)==len(r['native_order']),'native encodings count')
  for j,a in enumerate(r['native_assets_in_literal_order']):
   no=a['native_original_object'];name=no['original_api_file_object']['key'];path=base+a['candidate_relative'];bb=buffers[path]
   need(len(bb)==a['binding']['bytes'] and sha(bb)==a['binding']['SHA256'],'whole original native '+name)
   need(bb==read(Path(no['path'])),'literal original native bytes '+name)
   need(hashlib.md5(bb).hexdigest()==no['original_api_file_object']['checksum'].split(':')[1],'native original checksum '+name)
   q=enc[j];need(q['@type']=='MediaObject' and q['encodingFormat']==no['whole_original_native_files_entry']['mimetype'],'native MIME/original order '+name)
   need(q['contentUrl']==canonical+a['candidate_relative'] and q['sameAs']==no['original_api_file_object']['links']['self'],'native local/original URLs '+name)
   if r['record_id']=='23570763' and name.endswith('.zip'):need('license' not in q,'mixed ZIP no blanket grant')
   else:need(q.get('license')==CC,'actual broad encoding grant '+name)
  bib=buffers[base+r['BibTeX']['candidate_relative']];need(len(bib)==r['BibTeX']['binding']['bytes'] and sha(bib)==r['BibTeX']['binding']['SHA256'],'unchanged whole BibTeX')
  if r['record_id']=='23331295':need(r['printed_version'] is None and 'prints no version number' in ms[0] and 'MIT' not in ms[0],'absent printed version and no MIT invented')
  # Local document references resolve inside the independent virtual union.
  virtual=set(baseline_relative)|set(buffers)
  for tag,attrs in p.tags:
   for attr in ['href','src']:
    u=attrs.get(attr)
    if not u or u.startswith(('http:','https:','#','mailto:')):continue
    u=u.split('#',1)[0]
    if u.startswith('/'):target=u.lstrip('/')
    else:target=base+u
    if not target or target.endswith('/'):target+='index.html'
    need(target in virtual,'local link resolves '+target)
  expected_new.append({'@type':'ListItem','position':91+len(expected_new),'url':canonical,'name':r['title']})
 index=buffers['research/index.html'].decode();g,script=jsonscript(index)
 need(list(g)==list(oldgraph),'old index outer key order')
 for k,v in oldgraph.items():
  if k!='mainEntity':need(equal(g[k],v),'whole old index field '+k)
 me=g['mainEntity'];oldme=oldgraph['mainEntity'];need(list(me)==list(oldme),'ItemList key order')
 need(me['@type']=='ItemList' and me['numberOfItems']==92,'new92 index count')
 need(equal(me['itemListElement'][:90],B['old90typedorderedItemList']),'all90 old typed ordered items')
 need(equal(me['itemListElement'][90:],expected_new),'exact two new typed records positions91/92')
 lis=re.findall(r'<li\b[^>]*>.*?</li>',index,re.S);need(len(lis)==92 and lis[:90]==B['old90visible_li_bytes'],'all90 visible old items')
 # New visible entries are derived from frozen identity, not writer additions.
 for k,r in enumerate(records):
  li=lis[90+k];need(html.escape(r['title']) in li and html.escape(r['description']) in li and 'href="/research/'+r['slug']+'/"' in li and r['datePublished'][8:10]+' October 2026' in li and 'https://doi.org/10.5281/zenodo.'+r['record_id'] in li,'new visible identity '+r['record_id'])
 restored=index
 for li in lis[90:]:
  need(restored.count('      '+li+'\n')==1,'one complete inserted index line');restored=restored.replace('      '+li+'\n','',1)
 need(restore_script(restored,oldscript)==oldindex,'whole old index bytes restored')
 xml=buffers['research/sitemap.xml'].decode();nodes=re.findall(r'<url>.*?</url>',xml,re.S)
 need(len(nodes)==93 and nodes[:91]==B['old91wholeXMLnodebytes'],'all91 original whole XML nodes')
 ET.fromstring(xml)
 for j,r in enumerate(records):need(nodes[91+j]=='<url><loc>'+r['canonical_proposal']+'</loc><lastmod>2026-11-15</lastmod></url>','new sitemap identity/date')
 restored=xml
 for n in nodes[91:]:
  need(restored.count('  '+n+'\n')==1,'one complete inserted sitemap line');restored=restored.replace('  '+n+'\n','',1)
 need(restored==oldsitemap,'whole old sitemap bytes restored')
 need(len(set(baseline_relative)|set(buffers))==614 and len(set(buffers)-set(baseline_relative))==9,'derived614public nine new leaves')
 return True

# Strictly immutable initial and independent baseline capture, not live fence.
need(sha(read(A/'INITIAL_SEAL.json'))=='b8c8a28283a56d5108d351952fb5171043811888e17c52522e6457e4a0e3c44e','own initial seal')
need(sha(read(A/'BASELINE_SEAL.json'))=='fafc399ba6d9906f9267801d789f96f775b072e3af8f0f2505d6aa5ed68eec52','own baseline seal')
for mn,sn in [('INITIAL_MANIFEST.json','INITIAL_SEAL.json'),('BASELINE_MANIFEST.json','BASELINE_SEAL.json')]:
 seal=obj(A/sn);binding(A/mn,seal['manifest'])
 for n,r in obj(A/mn)['payloads'].items():binding(A/n,r)
# Whole original 245 inputs and four complete namespaces, every terminal included.
source=obj(S/'SOURCE_INPUTS.json');source_by_path={r['path']:r for r in source['files']}
need(len(source['files'])==len(source_by_path)==528,'whole528 source freeze paths')
for k,r in I['files'].items():
 b=binding(A/r['copy'],r);need(read(Path(r['original']))==b,'immutable original '+r['original']);q=source_by_path[r['original']];need(binding(S/q['blob'],q)==b,'all245 independent originals in writer freeze')
 if k.endswith('.json'):
  try:whole(json.loads(b),obj(S/q['blob']),k)
  except (UnicodeDecodeError,json.JSONDecodeError):raise ValueError('claimed JSON original is not JSON '+k)
for d,n in I['complete_namespaces'].items():need(files(Path(d))==n['relative_files'] and len(files(Path(d)))==n['count'],'whole source/editorial namespace '+d)
# Guard additional writer inputs as custody only, no new scientific opinion.
for r in source['files']:
 b=binding(S/r['blob'],r);need(read(Path(r['path']))==b,'whole writer frozen source original '+r['path'])
# Whole independent605 private baseline and writer611 rows incl six external.
baseline_by_path={r['original']:r for r in B['public_files']};baseline_relative={str(Path(p).relative_to(W/'public')) for p in baseline_by_path}
need(len(baseline_by_path)==605,'own fresh605 namespace')
wb=obj(S/'WEBSITE_BASELINE.json');go=obj(S/'ROOT_GO_RECEIPT.v2.json');wr={r['path']:r for r in wb['files']}
external={str(W/'firebase.json'),str(W/'.firebaserc'),go['prior_installation_receipt']['path'],str(S/'ROOT_GO_RECEIPT.v2.json'),go['root_fact_audit_adoption']['path'],go['prior_root_stage_adoption']['path']}
need(len(external)==6 and len(wb['files'])==len(wr)==611 and set(wr)==set(baseline_by_path)|external,'independent complete611 baseline row set')
need(set(wb['public_namespace'])==set(baseline_by_path) and len(wb['public_namespace'])==605,'independent605 writer namespace')
for p,r in baseline_by_path.items():need(binding(A/r['blob'],r)==binding(S/wr[p]['blob'],wr[p]),'whole605 baseline vs independently frozen bytes')
for r in B['site_configs']:
 need(binding(A/r['blob'],r)==binding(S/wr[r['original']]['blob'],wr[r['original']]),'whole original site configuration')
pr=B['root_publication_receipt'];need(binding(A/pr['blob'],pr)==binding(S/wr[pr['original']]['blob'],wr[pr['original']]),'literal previous publication receipt')
for p in external:need(binding(S/wr[p]['blob'],wr[p])==read(Path(p)),'six external baseline inputs')
whole(wb['prior_index_whole_schema'],B['old_complete_index_schema'],'writer whole old index schema')
for r in B['core_files']:need(binding(A/r['blob'],r)==read(Path(r['original'])),'core unchanged against authorized18 baseline')
if '--live-baseline' in sys.argv:
 need(set(str(W/'public'/n) for n in files(W/'public'))==set(baseline_by_path),'optional old live605 namespace')
 for p,r in baseline_by_path.items():need(read(Path(p))==read(A/r['blob']),'optional old605 live bytes')
# Exact immutable writer950 file closure, including nested history/terminal names.
need(sha(read(S/'FINAL_SEAL.json'))=='b42073395a01c7a60c733627212df7d56f484023662119a215a8b6cb57b89575','exact final writer seal')
need(sha(read(S/'OWNED_MANIFEST.json'))=='786bb967bd90a9caac34d99f773987e6dd7e164e5a418616bc5e7d49cdf1190b','exact writer owned manifest')
om=obj(S/'OWNED_MANIFEST.json');need(len(om['files'])==948 and files(S)==sorted([r['path'] for r in om['files']]+['OWNED_MANIFEST.json','FINAL_SEAL.json']),'strict complete950 writer file namespace')
need(dirs(S)==sorted(om['exact_relative_directories']),'strict writer directories')
for r in om['files']:binding(S/r['path'],r)
# Actual rendered normal/O files, not merely verifier optimization flags.
buffers={n:read(S/'candidate-a/public'/n) for n in paths};buffer_receipts=[]
for n in paths:
 b=buffers[n];need(b==read(S/'candidate-b/public'/n),'actual normal/O buffer equality '+n)
 need(b==read(S/'history/first-private-run/candidate-a/public'/n)==read(S/'history/first-private-run/candidate-b/public'/n),'actual current/first-run paired equality '+n)
 buffer_receipts.append({'path':n,'bytes':len(b),'SHA256':sha(b),'normal_optimized_whole_equal':True,'preserved_first_run_whole_equal':True})
need(files(S/'candidate-a/public')==files(S/'candidate-b/public')==paths,'actual both complete candidate namespaces')
output_oracle(buffers)
# Bind actual process receipts and complete stdout/stderr.
ledger=obj(S/'EXECUTION_LEDGER.json');actual=obj(S/'ACTUAL_TOOL_RECEIPTS.json');runs={r['name']:r for r in ledger['runs']}
for r in actual['actual_tool_results']:
 q=runs[r['name']];need(q['exit_code']==r['exit_code']==0,'actual process exit zero '+r['name'])
 for k in ['stdout','stderr']:
  bb=read(S/q[k]);need(sha(bb)==q[k+'_SHA256'] and len(bb)==q[k+'_bytes'],'actual whole '+k+' receipt')
  if k=='stdout':whole(json.loads(bb),q['whole_stdout_object'],'actual output '+r['name'])
  else:need(bb==b'','empty actual stderr')
for name,level,candidate in [('BUILD_NORMAL',0,'candidate-a'),('BUILD_OPTIMIZED',1,'candidate-b')]:
 r=runs[name];need(r['whole_stdout_object']['optimization_level']==level and r['whole_stdout_object']['candidate']==candidate and r['whole_stdout_object']['actual_all_eleven_buffers_written'] is True,'actual render mode '+name)
 need(('-O' in r['command_arguments'])==(level==1),'actual -O command flag distinct exit code')
# History is retained; exact old code differences are explicit.
h=S/'history/first-private-run';codechanges=[]
for n in ['stage_common.py','prepare_inputs.py','render_stage.py','integration_controls.py','finalize_stage.py','verify_stage_read_only.py']:
 same=read(S/n)==read(h/n);codechanges.append({'path':n,'unchanged_from_first_run':same});need(same==(n!='verify_stage_read_only.py'),'only standalone verifier changed')
f=obj(h/'PRESEAL_FAILURE_RECEIPTS.json');need([r['exit_code'] for r in f['actual_tool_results']]==[1,1] and all('whole actual fresh605 namespace' in r['output'] for r in f['actual_tool_results']),'whole actual old failures retained')
# Private final operational gates remain literal false/null.
ready=obj(S/'READY.json')
for k in ['root_stage_code_adopted','production_install_authorized','installed','deployed','live_verified','browser_verified','native_Sheet_publication_verified']:need(ready[k] is False,'private false gate '+k)
for k in ['canonical_url','AA','follow_up']:need(ready[k] is None,'private null '+k)
need(ready['virtual_counts']==[614,92,93] and ready['whole_native_assets']==5,'literal readiness count')

faults=[]
if '--faults' in sys.argv:
 def fault(name,target,mutate):
  changed=dict(buffers);mutate(changed);need(changed!=buffers,'actual fault applied '+name)
  try:output_oracle(changed)
  except (ValueError,KeyError,UnicodeDecodeError,json.JSONDecodeError,ET.ParseError) as e:faults.append({'name':name,'target':target,'applied':True,'rejected':True,'exception':type(e).__name__,'reason':str(e)});return
  raise ValueError('INDEPENDENT ORACLE MISSED '+name)
 def replace_fault(name,target,old,new):
  def mutate(v):need(v[target].count(old.encode())>=1,'exact current mutation anchor '+name);v[target]=v[target].replace(old.encode(),new.encode(),1)
  fault(name,target,mutate)
 for n in paths:
  if n.endswith(('.bib','.pdf','.tex','.zip')):fault('distinct-target-native-or-Bib-byte-'+n,n,lambda v,n=n:v.__setitem__(n,v[n][:-1]+bytes([v[n][-1]^1])))
  elif n=='research/index.html':replace_fault('distinct-target-old-visible-index',n,B['old90visible_li_bytes'][0],B['old90visible_li_bytes'][0].replace('Free spanning','Changed spanning',1))
  elif n.endswith('sitemap.xml'):replace_fault('distinct-target-old-XML-node',n,oldnodes[0],oldnodes[0].replace('2026-10-24','2026-10-25'))
  elif 'periodic-lefschetz' in n:replace_fault('distinct-target127-width1',n,'Width one is a separate case:','Width one follows the congruence criterion:')
  else:replace_fault('distinct-target128-all-radical-powers',n,'For every N≥1 and every finite-order multiplier h','Only for N≤4 and order≤4 multiplier h')
 p127='research/'+records[0]['slug']+'/index.html';p128='research/'+records[1]['slug']+'/index.html'
 for name,target,old,new in [
 ('127fixedchain',p127,'single fixed infinite field K = 𝔽ₚ(t)','field K varying with width'),
 ('127generation',p127,'the entire chain is generated from width three','the chain is only generated at finitely tested widths'),
 ('127arbitraryform',p127,'For an arbitrary linear form ℓ','For one symmetric test form ℓ'),
 ('127char2power',p127,'including in characteristic two','excluding characteristic two'),
 ('128ordinaryentire',p128,'ordinary, uncompleted unital complex algebra','completed unital complex algebra'),
 ('128Bdistinct',p128,'does not decide its radical/vanishing-ideal question','solves its radical/vanishing-ideal question'),
 ('128splitlabels',p128,'including split links','excluding split links'),
 ('128printedversion',p128,'prints no version number','prints version number 1.0'),
 ('128date',p128,'content="2026/10/12"','content="2026/10/13"'),
 ('headcanonical',p128,'rel="canonical" href="'+records[1]['canonical_proposal']+'"','rel="canonical" href="https://example.invalid/"'),
 ('hiddenmain',p127,'<style>','<style>main article{display:none}'),
 ('wholeabstract',p128,'"abstract": "Let V be the ordinary','"abstract": "Summary: ordinary')]:replace_fault(name,target,old,new)
 def encoding_fault(v,reverse=False,mit=False,blanket=False):
  target=p127 if blanket else p128;t=v[target].decode();g,ss=jsonscript(t);enc=g['@graph'][1]['encoding']
  if reverse:enc.reverse()
  if mit:enc[0]['license']='https://opensource.org/license/mit/'
  if blanket:enc[0]['license']=CC
  v[target]=restore_script(t,json.dumps(g,ensure_ascii=False)).encode()
 fault('128nativeorder',p128,lambda v:encoding_fault(v,reverse=True))
 fault('128inventedMIT',p128,lambda v:encoding_fault(v,mit=True))
 fault('127mixedblanketCCBY',p127,lambda v:encoding_fault(v,blanket=True))
 tex='research/'+records[1]['slug']+'/assets/nullstellensatz.tex';fault('missing128nativeTeX',tex,lambda v:v.pop(tex))
 fault('extraunrelatedoverlay','unrelated.txt',lambda v:v.__setitem__('unrelated.txt',b'changed'))
# If final sealed, durable custody includes every own payload and exact directories.
if (A/'FINAL_SEAL.json').exists():
 fs=obj(A/'FINAL_SEAL.json');binding(A/'OWNED_MANIFEST.json',fs['manifest']);own=obj(A/'OWNED_MANIFEST.json')
 need(files(A)==sorted(list(own['payloads'])+['OWNED_MANIFEST.json','FINAL_SEAL.json']),'strict own whole final namespace')
 need(dirs(A)==own['directories'],'strict own final directories')
 for n,r in own['payloads'].items():binding(A/n,r)
print(json.dumps({'disposition':'PASS_INDEPENDENT_LEFSCHETZ_LINK_CODE_INTEGRATION_CUSTODY','positive_checks':checks,'whole_typed_comparisons':len(comparisons),'comparison_receipts':comparisons,'actual_whole_buffer_comparisons':buffer_receipts,'current_vs_history_code_comparisons':codechanges,'bounded_new_memory_fault_count':len(faults),'faults':faults,'actual_process_exit_codes':[runs[n]['exit_code'] for n in ['BUILD_NORMAL','BUILD_OPTIMIZED']],'actual_render_optimization_levels':[runs[n]['whole_stdout_object']['optimization_level'] for n in ['BUILD_NORMAL','BUILD_OPTIMIZED']],'baseline':[605,90,91],'proposed':[614,92,93],'default_live_public_fence':False,'optional_live_baseline_requested':'--live-baseline' in sys.argv,'project_imports_subprocess_network_science_or_writes':False,'publication_authority':False,'canonical_url':None,'AA':None,'follow_up':None},ensure_ascii=False,indent=2))
