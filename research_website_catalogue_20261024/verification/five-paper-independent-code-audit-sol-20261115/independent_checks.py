#!/usr/bin/env python3
"""Independent offline finite integration checks. No stage imports, network,
subprocess, renderer, scientific code, fault suite, or file writes."""
from pathlib import Path
from html.parser import HTMLParser
from hashlib import sha256
from copy import deepcopy
import json,re,sys,xml.etree.ElementTree as ET
A=Path(__file__).resolve().parent;P=A.parent.parent;E=P/'verification/five-paper-private-stage-sol-20261115'
N=0
def need(v,s):
 global N
 if not v:raise ValueError(s)
 N+=1
def load(p):return json.loads(Path(p).read_text())
def h(p):return sha256(Path(p).read_bytes()).hexdigest()
def typed(v):
 if isinstance(v,dict):return ('dict',tuple((k,typed(x)) for k,x in v.items()))
 if isinstance(v,list):return ('list',tuple(typed(x) for x in v))
 return(type(v).__name__,v)
class DOM(HTMLParser):
 def __init__(self,s):super().__init__(convert_charrefs=True);self.root={'tag':'root','a':{},'c':[]};self.stack=[self.root];self.feed(s)
 def handle_starttag(self,t,attrs):
  n={'tag':t,'a':dict(attrs),'c':[]};self.stack[-1]['c'].append(n)
  if t not in {'meta','link','br','hr','img','input'}:self.stack.append(n)
 def handle_endtag(self,t):
  if self.stack[-1]['tag']==t:self.stack.pop()
  else:raise ValueError('unbalanced DOM '+t)
 def handle_data(self,d):self.stack[-1]['c'].append(d)
def walk(n):
 if isinstance(n,dict):
  yield n
  for c in n['c']:yield from walk(c)
def find(n,t):return [x for x in walk(n) if x['tag']==t]
def text(n):return n if isinstance(n,str) else ''.join(text(x) for x in n['c'])
def source_words(n):
 if isinstance(n,str):return n
 if 'data-tex' in n['a']:return ('$$' if n['tag']=='div' else '$')+n['a']['data-tex']+('$$' if n['tag']=='div' else '$')
 return ''.join(source_words(x) for x in n['c'])+(' ' if n['tag']in {'p','li','h1','h2','h3','ul','ol','section'}else '')
def words(s):return ' '.join(s.split())
def stripmd(s):
 parts=re.split(r'(\$\$.*?\$\$|\$.*?\$)',s,flags=re.S);out=[]
 for p in parts:
  if p.startswith('$'):out.append(p)
  else:out.append(re.sub(r'\[([^\]]+)\]\([^\n]+?\)',r'\1',re.sub(r'^###\s+','',p)).replace('**','').replace('*',''))
 return words(''.join(out))
def normalized_main(n,rid):
 n=deepcopy(n)
 for x in walk(n):
  a=x['a']
  if x['tag']=='main':a.clear();a['id']='main'
  for key in ['href','src']:
   if a.get(key,'').startswith('assets/'):a[key]=a[key][7:]
  if a.get('href')=='../citation.bib':need(rid=='23430498','115-only relative Bib rebase');a['href']='citation.bib'
  if 'class'in a:a['class']=' '.join({'formula':'equation','byline':'entry-meta','meta':'entry-meta'}.get(c,c) for c in a['class'].split())
  if 'style'in a:need(a.pop('style')=='white-space: nowrap','only original visible nowrap style');a['class']='equation'
  if x['tag']=='iframe':a['class']='paper-pdf';a['loading']='lazy'
 return n

def validate113(c,main):
 sec={x['a']['id']:x for x in find(main,'section')};groups={'abstract':[c['abstract']],'plain-language':c['plain_language'],'result':c['result'],'proof':c['why_it_works'],'limits':c['limitations'],'status':[c['status'],c['ai_disclosure'],c['edition_note']]}
 for sid,raws in groups.items():
  children=[x for x in sec[sid]['c'] if isinstance(x,dict)][1:];need(len(children)==len(raws),'113 complete block count '+sid)
  for raw,actual in zip(raws,children):need(words(source_words(actual))==stripmd(raw),'113 complete prose/TeX block '+sid)
 bg=sec['background'];urls=[x['a']['href'] for x in find(bg,'a')];expected=re.findall(r'\]\(([^\n]+?)\)',c['background']);old=load(A/'inputs/root-dlab-background-link-adoption-20261115.json');expected=[old['new_href'] if x==old['old_href'] else x for x in expected]
 need(urls==expected and urls.count(old['new_href'])==1 and old['old_href'] not in urls,'exact one Dlab href and complete background destinations')
 bg_content=' '.join(source_words(x) for x in bg['c'] if isinstance(x,dict) and x['tag']!='h2');need(words(bg_content)==stripmd(c['background'].replace('* ','')),'all113 prior-credit words')
 need(c['collaboration'] in text(sec['collaborate']),'full113 passive collaboration')
 return sec

def overlays(index,sitemap,baseline,bundles):
 oldindex=(Path(baseline['public_root'])/'research/index.html').read_text() if '--current-base' in sys.argv else (E/'baseline/research/index.html').read_text()
 oldmap=(E/'baseline/research/sitemap.xml').read_text();rows=re.findall(r'<li>.*?</li>',index,re.S);oldrows=re.findall(r'<li>.*?</li>',oldindex,re.S)
 need(len(oldrows)==78 and len(rows)==83 and rows[:78]==oldrows,'old78 entire list items preserved, new total83')
 rx=r'(<script type="application/ld\+json">\s*)(.*?)(\s*</script>)';om=re.search(rx,oldindex,re.S);nm=re.search(rx,index,re.S);o=json.loads(om[2]);n=json.loads(nm[2]);expect=deepcopy(o);items=expect['mainEntity']['itemListElement'];urls=[]
 for b,row in zip(bundles,rows[78:]):
  u='https://aleckriebel.com/research/'+b['slug']+'/';urls.append(u);need(b['title'] in text(DOM(row).root),'new index title');need('/research/'+b['slug']+'/'+b['pdf'] in row,'new exact index PDF');need('https://doi.org/'+b['doi'] in row,'new index DOI')
  items.append({'@type':'ListItem','position':len(items)+1,'url':u,'name':b['title']})
 expect['mainEntity']['numberOfItems']=83;need(typed(n)==typed(expect),'complete old ItemList plus exact5 new positions')
 restored=index[:nm.start(2)]+om[2]+index[nm.end(2):]
 for row in rows[78:]:need(restored.count('      '+row+'\n')==1,'single exact new index row');restored=restored.replace('      '+row+'\n','',1)
 need(restored==oldindex,'every unrelated index byte unchanged')
 old=ET.fromstring(oldmap);new=ET.fromstring(sitemap);ol=[x.text for x in old.findall('{*}url/{*}loc')];nl=[x.text for x in new.findall('{*}url/{*}loc')];need(len(ol)==79 and nl==ol+urls and len(set(nl))==84,'all old79 plus exact5 sitemap locations')
 for u in urls:
  add='  <url><loc>'+u+'</loc><lastmod>2026-11-15</lastmod></url>\n';need(sitemap.count(add)==1,'one exact new sitemap entry');sitemap=sitemap.replace(add,'',1)
 need(sitemap==oldmap,'every unrelated sitemap byte unchanged')
 return urls

def run():
 need(h(E/'FINAL_SEAL.json')=='80db4036c349909dea6138effb23c3ae764a0e2a748aa2efc521b0b5a5439eec','actual final-ready stage seal')
 need(h(E/'OWNED_MANIFEST.json')=='4a470cdf6f34cae17e378a50f5d678d61a44f1053be8fe756d0f86f338a76a3a','actual final-ready owned manifest')
 stage=load(E/'OWNED_MANIFEST.json');expected={x['path'] for x in stage['files']}|{'OWNED_MANIFEST.json','FINAL_SEAL.json'}
 need({str(x.relative_to(E)) for x in E.rglob('*') if x.is_file()}==expected,'entire sealed219-file stage namespace')
 for x in stage['files']:p=E/x['path'];need(p.stat().st_size==x['bytes'] and h(p)==x['sha256'],'217 stage payload '+x['path'])
 frozen=load(E/'FROZEN_INPUT_SET.json')
 for x in frozen['input_files']:p=Path(x['path']);need(p.stat().st_size==x['bytes'] and h(p)==x['sha256'],'663 frozen input '+str(p))
 baseline=load(A/'BASELINE_INDEPENDENT.json');stagebase=load(E/'FRESH_BASELINE.json')
 need({x['relative_path']:(x['bytes'],x['sha256']) for x in baseline['public_files']}=={x['path']:(x['bytes'],x['sha256']) for x in stagebase['public_files']},'independent current556 baseline agrees with stage')
 need({x['absolute_path']:(x['bytes'],x['sha256']) for x in baseline['core_files']}=={x['path']:(x['bytes'],x['sha256']) for x in stagebase['installed_core_files']},'independent fresh18 core baseline agrees')
 for x in baseline['core_files']:need(h(x['absolute_path'])==x['sha256'],'current18 core unchanged')
 public=Path(baseline['public_root'])
 for x in baseline['public_files']:
  if '--current-base'in sys.argv or x['relative_path']not in {'research/index.html','research/sitemap.xml'}:need(h(public/x['relative_path'])==x['sha256'],'old public unchanged '+x['relative_path'])
 if '--current-base'in sys.argv:need({str(x.relative_to(public)) for x in public.rglob('*') if x.is_file()}=={x['relative_path']for x in baseline['public_files']},'production namespace still556')
 for x in load(A/'APPROVED_INPUT_BINDINGS.json')['files']:need(h(x['absolute_path'])==x['sha256'],'exact root-adopted approval input')
 ready=load(E/'CANDIDATE_READY.json');outputs=ready['all_22_exact_outputs'];need(len(outputs)==22,'exact22 listed outputs');paths={x['path']for x in outputs};need(len(paths)==22,'unique22 paths')
 for pair in ['candidate-a','candidate-b']:
  root=E/pair/'public';need({str(x.relative_to(root))for x in root.rglob('*')if x.is_file()}==paths,'exact22 candidate namespace '+pair)
  for x in outputs:p=root/x['path'];need(p.stat().st_size==x['bytes']and h(p)==x['sha256'],'paired complete output identity '+pair+':'+x['path'])
 need(len({x['relative_path']for x in baseline['public_files']}|paths)==576,'virtual installed union576')
 bundles=[];records={};body_cases=[]
 for rid,original in frozen['records'].items():
  c=original['whole_config_original'];p=original['whole_promotion_original'];layout=original['layout'];record=original['native_record_original'];meta=record['metadata'];native=original['source_ready_original'];slug=c['slug']if layout['kind']in {'config','html-config'} else p['proposed']['slug'];base='https://aleckriebel.com/research/'+slug+'/';folder=E/'candidate-a/public/research'/slug;raw=(folder/'index.html').read_text();dom=DOM(raw);main=find(dom.root,'main')[0];head=find(dom.root,'head')[0];scholar=json.loads(text(find(head,'script')[0]))['@graph'][1]
  title=meta['title'];pdf=next(x['key']for x in record['files']if x['key'].endswith('.pdf'));zipname=next(x['key']for x in record['files']if x['key'].endswith('.zip'));bundles.append({'rid':rid,'slug':slug,'title':title,'pdf':pdf,'doi':record['doi']})
  names={x['a'].get('name',x['a'].get('property')):x['a'].get('content')for x in find(head,'meta')};need(names['citation_title']==title and names['citation_publication_date']==meta['publication_date'].replace('-','/'),'exact native title/date '+rid);need(names['robots']=='index,follow','proposed publishable HTML robots '+rid);need(names['citation_pdf_url']==base+pdf and names['citation_doi']==record['doi'],'proposed reader/DOI metadata '+rid)
  need([x['a']['href']for x in find(head,'link')if x['a'].get('rel')=='canonical']==[base],'one exact proposed canonical '+rid);need(scholar['datePublished']==meta['publication_date']and scholar['version']==meta['version'],'native article edition/date '+rid)
  need(scholar['license']=='https://creativecommons.org/licenses/by/4.0/','actual authored-paper license '+rid)
  if layout['kind']=='config':need(scholar['abstract']==c['abstract'],'whole113 scholarly abstract');validate113(c,main)
  else:
   source=DOM((P/'papers'/rid/layout['html']).read_text());expected_main=normalized_main(find(source.root,'main')[0],rid);need(typed(main)==typed(expected_main),'full adopted nested HTML tree '+rid)
   original_scholar=json.loads(text(find(source.root,'script')[0]));abstract=c['abstract']if layout['kind']=='html-config'else(P/'papers'/rid/layout['abstract']).read_text().strip();need(scholar['abstract']==abstract,'whole original scholarly abstract '+rid)
  frame=find(main,'iframe');need(len(frame)==1 and frame[0]['a']['src'].split('#')[0]==pdf and frame[0]['a'].get('title'),'full accessible native reader '+rid)
  links=find(main,'a');need(any(x['a']['href']==pdf and 'download'in x['a']for x in links),'native PDF download '+rid);need(any(x['a']['href']==zipname for x in links),'whole ZIP link '+rid);need(any(x['a']['href']=='citation.bib'for x in links),'same-folder citation '+rid)
  need((folder/'citation.bib').read_bytes()==(P/'papers'/rid/layout['bib']).read_bytes(),'whole approved BibTeX '+rid)
  body=text(main);need('human peer review'in body and ('AI tools were used extensively'in body or 'Extensive AI assistance'in body),'AI/unrefereed/nonhuman status '+rid)
  for s in ['SOURCE_READY','root-clearance','sha256','SEAL.json','474 checks','663 frozen','2026-11-15']:need(s not in body,'no private audit-log leak '+rid+':'+s)
  for n in find(dom.root,'script'):need(n['a']=={'type':'application/ld+json'},'only nonexecuting JSON script '+rid)
  need(not find(dom.root,'style') and not find(dom.root,'template') and not find(dom.root,'noscript'),'no hidden article wrapper '+rid)
  records[rid]={'literal_status':'QUALIFIED_PASS_COMPLETE_ADOPTED_SCIENTIFIC_SCOPE_AND_NATIVE_READER_INTEGRATION','canonical_is_proposal_not_native_assignment':True,'source_unchanged':True,'license_paper':'CC BY 4.0','version':meta['version'],'publication_date':meta['publication_date'],'follow_up':None}
  body_cases.append((rid,dom,c,main))
 root=E/'candidate-a/public';index=(root/'research/index.html').read_text();sitemap=(root/'research/sitemap.xml').read_text();urls=overlays(index,sitemap,baseline,bundles)
 # Only six small, memory-only integration falsifiers; no stage code imported.
 faults=[]
 def rejects(label,fn):
  try:fn()
  except ValueError:faults.append(label);return
  raise ValueError('accepted integration mutation '+label)
 b=next(x for x in body_cases if x[0]=='23441890');bad=deepcopy(b[2]);bad['result'][2]=bad['result'][2].replace('including a right affine germ at $0$','without an endpoint restriction');rejects('113 endpoint qualification changed',lambda:validate113(bad,b[3]))
 bad=deepcopy(b[3]);bg=next(x for x in find(bad,'section')if x['a']['id']=='background');link=next(x for x in find(bg,'a')if x['a']['href']=='https://kourovkanotebookorg.wordpress.com/');link['a']['href']='https://example.invalid/';rejects('113 unapproved background destination',lambda:validate113(b[2],bad))
 rejects('old index entry changed',lambda:overlays(index.replace('<li>','<li>UNAPPROVED ',1),sitemap,baseline,bundles))
 rejects('index ItemList count altered',lambda:overlays(index.replace('"numberOfItems": 83','"numberOfItems": 82',1),sitemap,baseline,bundles))
 rejects('new sitemap destination changed',lambda:overlays(index,sitemap.replace(urls[-1],urls[-1]+'wrong/',1),baseline,bundles))
 rejects('whole original asset truncated',lambda:need(sha256((root/'research'/bundles[-1]['slug']/bundles[-1]['pdf']).read_bytes()[:-1]).hexdigest()==next(x['sha256']for x in outputs if x['path']=='research/'+bundles[-1]['slug']+'/'+bundles[-1]['pdf']),'damaged native asset rejected'))
 if (A/'FINAL_SEAL.json').exists():
  seal=load(A/'FINAL_SEAL.json');need(h(A/'OWNED_MANIFEST.json')==seal['owned_manifest_sha256'],'own audit manifest seal');m=load(A/'OWNED_MANIFEST.json')
  for x in m['files']:need(Path(x['absolute_path']).stat().st_size==x['bytes']and h(x['absolute_path'])==x['sha256'],'owned audit bytes '+x['absolute_path'])
  need({str(x)for x in A.rglob('*')if x.is_file()}=={x['absolute_path']for x in m['files']}|{str(A/'OWNED_MANIFEST.json'),str(A/'FINAL_SEAL.json')},'exact own audit namespace')
 else:need('--unsealed'in sys.argv,'own final audit seal required')
 return {'literal_custom_status':'QUALIFIED_PASS_FIVE_PRIVATE_CODE_COPY_INTEGRATION_NO_SUBSTANTIVE_LOSS_OR_UNAUTHORIZED_MUTATION_FOUND','checks':N,'records':records,'stage_owned_payloads_unchanged':217,'source_and_approved_input_files_unchanged':663,'current_baseline_checked':'--current-base'in sys.argv,'current_public_files':556 if '--current-base'in sys.argv else None,'old_nonoverlay_public_files':554,'current_core_files':18,'candidate_pair_outputs_each':22,'virtual_installed_files':576,'index_entries':83,'sitemap_locations':84,'six_small_in_memory_integration_falsifiers_rejected':faults,'network_subprocess_source_or_stage_code_imports_or_writes':False,'fresh_science_or_old457_69_138_campaigns_run':False,'publication_native_AA_or_browser_authority':False}
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
