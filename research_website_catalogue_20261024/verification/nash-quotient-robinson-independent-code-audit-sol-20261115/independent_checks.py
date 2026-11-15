"""Independent integration/custody checker. Default reads only, no imports from project.
No network, subprocess, bytecode generation, filesystem writes, rendering or old tests.
--live-baseline additionally checks the preinstallation593-file site fence.
--faults runs only this audit's new bounded memory faults; --preseal skips own final seal.
"""
from pathlib import Path, PurePosixPath
from hashlib import sha256
from html.parser import HTMLParser
from html import unescape
import json, re, sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
STAGE=ROOT/'verification/nash-quotient-robinson-private-stage-sol-20261115'
SITE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
checks=0
def need(ok,label):
 global checks
 checks+=1
 if not ok:raise ValueError(label)
def binding(b):return {'bytes':len(b),'SHA256':sha256(b).hexdigest()}
def read(p):
 need(p.is_file() and not p.is_symlink(),'regular nonlink '+str(p))
 return p.read_bytes()
def obj(p):return json.loads(read(p))
def typed(a,b):
 if type(a)!=type(b):return False
 if isinstance(a,dict):return list(a)==list(b) and all(typed(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(typed(x,y) for x,y in zip(a,b))
 return a==b
def files(folder):
 allp=list(folder.rglob('*'));need(not any(p.is_symlink() for p in allp),'namespace no symlink')
 return sorted(str(p.relative_to(folder)) for p in allp if p.is_file())
def main(text):
 a=re.findall(r'<main\b[^>]*>.*?</main>',text,re.S)
 need(len(a)==text.count('<main')==text.count('</main>')==1,'one complete main')
 return a[0]
def ld(text):
 a=list(re.finditer(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',text,re.S));need(len(a)==1,'one JSONLD script')
 return a[0],json.loads(a[0][1])
class Head(HTMLParser):
 def __init__(self):super().__init__();self.meta={};self.links=[];self.title='';self.intitle=False
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='meta':
   k=a.get('name',a.get('property','charset'))
   need(k not in self.meta,'unique meta '+k);self.meta[k]=a.get('content',a.get('charset'))
  if t=='link':self.links.append(a)
  if t=='title':self.intitle=True
 def handle_data(self,d):
  if self.intitle:self.title+=d
 def handle_endtag(self,t):
  if t=='title':self.intitle=False
E=obj(HERE/'EXPECTED.json'); B=obj(HERE/'BASELINE.json')
def validate(buffers):
 need(sorted(buffers)==E['overlay_exact_paths'] and len(buffers)==14,'exact independent14 overlay namespace')
 details=[]
 for a in E['records']:
  base='research/'+a['slug']+'/';text=buffers[base+'index.html'].decode();m=main(text)
  need(m==a['expected_main'],'full approved '+a['record_id']+' main; zero prose/Unicode/tag mutation')
  h=Head();h.feed(text.split('</head>',1)[0]);canonical=a['canonical'];date=a['datePublished'];doi='10.5281/zenodo.'+a['record_id']
  need(h.title==a['title']+' | Alec Kriebel','accurate title')
  expected={'description':a['description'],'author':'Alec Kriebel','robots':'index,follow','citation_title':a['title'],'citation_author':'Alec Kriebel','citation_author_orcid':'https://orcid.org/0009-0001-9320-500X','citation_publication_date':date.replace('-','/'),'citation_doi':doi,'citation_version':a['version'],'citation_language':'en','og:type':'article','og:title':a['title'],'og:description':a['description'],'og:url':canonical,'og:site_name':'Alec Kriebel','article:published_time':date}
  pdf=next(k for k in a['assets'] if k.endswith('.pdf'))
  expected['citation_pdf_url']=canonical+pdf
  for k,v in expected.items():need(h.meta.get(k)==v,'head '+a['record_id']+' '+k)
  for rel,href in [('canonical',canonical),('icon','/favicon.ico'),('stylesheet','/research/research.css')]:need(len([q for q in h.links if q.get('rel')==rel and q.get('href')==href])==1,'existing wrapper '+rel)
  need('noindex' not in text and '<a class="skip-link" href="#main">' in text and m.startswith('<main id="main">'),'indexable main skip target')
  am=re.findall(r'<h2>Original abstract</h2>\s*<p(?: class="math")?>(.*?)</p>',m,re.S)
  need(len(am)==1 and unescape(am[0])==a['full_original_abstract'],'one entire original visible abstract')
  _,g=ld(text);need(g.get('@context')=='https://schema.org' and len(g.get('@graph',[]))==2,'pagearticle graph')
  page,art=g['@graph'];need(page['@type']=='WebPage' and art['@type']=='ScholarlyArticle','graph exact types')
  need(page['@id']==canonical+'#page' and art['@id']==canonical+'#article' and page['mainEntity']=={'@id':art['@id']} and art['mainEntityOfPage']=={'@id':page['@id']},'mutual graph references')
  need(page['dateCreated']==page['dateModified']=='2026-11-15' and art['datePublished']==date,'original vsbuild dates')
  need(art['abstract']==a['full_original_abstract'] and art['creativeWorkStatus']=='Unrefereed preprint','whole scholarly abstract/status')
  for k,v in a['original_scholarly_object'].items():
   if k not in {'@id','url','mainEntityOfPage','inLanguage','isAccessibleForFree','encoding'}:need(k in art and typed(v,art[k]),'whole original scholarly field '+k)
  enc=art['encoding'];need(type(enc)==list and len(enc)==2,'exact2 native encodings')
  for local,info in a['assets'].items():need(binding(buffers[base+local])==info['binding'],'full original '+a['record_id']+' '+local+' bytes')
  for q in enc:
   filename=q['contentUrl'].removeprefix(canonical)
   need(filename in a['assets'] and not filename.endswith('.bib'),'encoding actual complete native asset')
   need(q['sameAs']=='https://zenodo.org/api/records/'+a['record_id']+'/files/'+PurePosixPath(filename).name+'/content','exact native encoding URL')
   need(q['encodingFormat']==('application/pdf' if filename.endswith('.pdf') else 'application/zip'),'correct asset MIME')
   if a['record_id']=='23578599' and filename.endswith('.zip'):need('license' not in q,'no blanket prose license on mixedMIT ZIP')
   else:need(q.get('license')=='https://creativecommons.org/licenses/by/4.0/','actual authored CC BY asset license')
  css=re.findall(r'<style>(.*?)</style>',text,re.S);need(len(css)==1,'one bounded supplemental CSS')
  need(not re.search(r'display\s*:\s*none|visibility|opacity|position|font-size|overflow\s*:\s*hidden',css[0]),'no hidden substantive content CSS')
  need('overflow-wrap:anywhere' in css[0] and 'main iframe' in css[0] and 'width:100%' in css[0] and 'min-height:500px' in css[0],'readable wrapping and PDF supplement')
  if a['record_id']=='23578599':need(m.count('<table>')==m.count('</table>')==1 and m.count('<tbody>')==1,'actual source convention table')
  if a['record_id']=='23333002':need(re.search(r'<iframe[^>]*width="100%"[^>]*height="850"',m) is not None,'explicit original125iframe dimensions')
  footer=text.split('</main>',1)[1];need('<footer>' in footer and 'Research home' in footer and '© 2013–2026 Kriebel LLC.' in footer,'existing footer pattern')
  details.append({'record_id':a['record_id'],'entire_main':binding(m.encode()),'datePublished':date,'abstract_characters':len(a['full_original_abstract']),'assets':len(a['assets'])})
 oldindex=read(HERE/'baseline/index.html').decode();index=buffers['research/index.html'].decode();oldmatch,olddata=ld(oldindex);match,data=ld(index)
 items=data['mainEntity']['itemListElement'];need(type(data['mainEntity']['numberOfItems']) is int and data['mainEntity']['numberOfItems']==len(items)==90,'exact90 typed ItemList')
 need(typed(items[:87],B['old_itemlist_complete_typed_ordered']),'all87 whole typed/key/list/order old items')
 lis=re.findall(r'<li>.*?</li>',index,re.S);need(len(lis)==90 and lis[:87]==B['old_visible_li_bytes'],'all87visible index bytes/order')
 restored=index
 for i,(a,li) in enumerate(zip(E['records'],lis[87:]),88):
  need(items[i-1]=={'@type':'ListItem','position':i,'url':a['canonical'],'name':a['title']},'new exact index identity'+str(i))
  need('/research/'+a['slug']+'/' in li and a['description'] in unescape(li),'new visible index identity')
  restored,n=re.subn(r'(?m)^ *'+re.escape(li)+r'\n','',restored,count=1);need(n==1,'one removable new visible entry')
 rm,_=ld(restored);restored=restored[:rm.start(1)]+oldmatch[1]+restored[rm.end(1):]
 need(restored==oldindex,'entire old index recovered byteexact without3new entries/JSONLD')
 sm=buffers['research/sitemap.xml'].decode();nodes=re.findall(r'<url>.*?</url>',sm,re.S)
 need(len(nodes)==91 and nodes[:88]==B['old_sitemap_url_node_bytes'],'all88 whole old XMLnodes datesorder')
 restored=sm
 for a,node in zip(E['records'],nodes[88:]):
  need(node=='<url><loc>'+a['canonical']+'</loc><lastmod>2026-11-15</lastmod></url>','correct new sitemap node')
  restored,n=re.subn(r'(?m)^ *'+re.escape(node)+r'\n','',restored,count=1);need(n==1,'one new sitemap node')
 need(restored.encode()==read(HERE/'baseline/sitemap.xml'),'entire old sitemap recovered byteexact')
 need(len(set(B['public'])|set(buffers))==605 and set(B['public'])&set(buffers)=={'research/index.html','research/sitemap.xml'},'exact605virtual union12new2existing')
 return details

def custody():
 manifest=obj(HERE/'APPROVED_INPUT_MANIFEST.json')
 for p,b in manifest['inputs'].items():need(binding(read(ROOT/p))==b,'independent original input '+p)
 for p,names in manifest['complete_namespaces'].items():need([p+'/'+q for q in files(ROOT/p)]==names,'complete source/editorial namespace '+p)
 for p,b in manifest['all_current_script_bindings'].items():need(binding(read(ROOT/p))==b,'current core script remains literal')
 # Whole native/scientific authorities are custody inputs, not generic PASS gates.
 native=obj(HERE/'native-oracle/INPUT_MANIFEST.json')
 for row in native['files']:
  expected={'bytes':row['bytes'],'SHA256':row['SHA256']}
  need(binding(read(Path(row['original'])))==expected,'whole original native authority custody')
  need(binding(read(HERE/'native-oracle'/row['copy']))==expected,'whole raw native authority copy')
 # The original baseline contains18core paths:17unchanged and one authorized replacement.
 core=obj(STAGE/'CORE_INPUTS.json');oldcore={r['path']:r for r in core['original_core_file_bindings']}
 need(len(core['files'])==len(oldcore)==18,'current18 core interfaces')
 unchanged=0
 for row in core['files']:
  expected={'bytes':row['bytes'],'SHA256':row['SHA256']}
  need(binding(read(Path(row['path'])))==expected,'current whole corefile unchanged')
  prior=oldcore[row['path']]
  if row['path'].endswith('/scripts/checkpoint_subtree.py'):
   need(row['SHA256']=='405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0' and prior['SHA256']=='91d5c5d285502e5a82f3eb090cf3399458c96416a873a674439ef5a1b435af5b','only root-authorized checkpoint qualification')
  else:
   need(row['bytes']==prior['bytes'] and row['SHA256']==prior['SHA256'],'original core baseline literal');unchanged+=1
 need(unchanged==17 and core['claim_all18_unchanged_from_original_baseline'] is False,'17original unchanged; no18unchanged claim')
 # Hold original baseline in private stage blobs, not mutable production aggregate state.
 wb=obj(STAGE/'WEBSITE_BASELINE.json')
 for row in wb['public_files']:
  key=str(Path(row['path']).relative_to(SITE/'public'))
  need(binding(read(STAGE/row['blob']))==B['public'][key],'old593 custody '+key)
 need(len(wb['public_files'])==593,'old593 full snapshot')
 return manifest

def faults(buffers):
 out=[]
 def reject(label,target,change):
  bad=dict(buffers);bad[target]=change(bad[target]);need(bad[target]!=buffers[target],'fault actually applied '+label)
  try:validate(bad)
  except (ValueError,KeyError,UnicodeDecodeError,json.JSONDecodeError) as exc:out.append({'fault':label,'target':target,'rejected':True,'actual_exception':str(exc)})
  else:raise RuntimeError('undetected independent fault '+label)
 for p in E['overlay_exact_paths']:
  if p.endswith(('.pdf','.zip','.bib')):reject('full original asset corruption',p,lambda b:b[:-1])
  elif p=='research/index.html':reject('old typed ItemList URL corrupted',p,lambda b:b.replace(b'free-spanning-forest-degree',b'changed-prior-paper',1))
  elif p=='research/sitemap.xml':reject('old sitemap lastmod changed',p,lambda b:b.replace(b'2026-10-24',b'2026-10-25',1))
  else:
   a=next(q for q in E['records'] if '/'+q['slug']+'/' in p)
   needle,replace={'23578599':('The conclusion concerns a specified reference divisor.','The conclusion concerns an arbitrary divisor.'),'23423736':('second left factor in both f₅ and f₆ is x₄','second left factor in both f₅ and f₆ is x₃'),'23333002':('every real ε≥0','every real ε&gt;0')}[a['record_id']]
   reject('scientific scoped prose corrupted',p,lambda b,n=needle,r=replace:b.replace(n.encode(),r.encode(),1))
 # Additional frozen fault mechanisms; each is isolated and in-memory.
 p='research/'+E['records'][2]['slug']+'/index.html'
 reject('Robinson actual height850 silently dropped',p,lambda b:b.replace(b' height="850"',b'',1))
 reject('hidden substantive paragraph',p,lambda b:b.replace(b'<p class="math">',b'<p class="math" hidden>',1))
 p='research/'+E['records'][0]['slug']+'/index.html'
 reject('wrong canonical',p,lambda b:b.replace(b'<link rel="canonical" href="https://aleckriebel.com/research/',b'<link rel="canonical" href="https://invalid.example/research/',1))
 reject('original date overwritten bybuilddate',p,lambda b:b.replace(b'content="2026/10/22"',b'content="2026/11/15"',1))
 reject('citationPDF points toZIP',p,lambda b:b.replace(b'free-chain-nash-intersections.pdf">',b'free-chain-nash-intersections-source-and-verification.zip">',1))
 def mutate_graph(b,key,value):
  t=b.decode();m,g=ld(t);g['@graph'][1][key]=value;return (t[:m.start(1)]+json.dumps(g,ensure_ascii=False)+t[m.end(1):]).encode()
 reject('whole scholarly abstract replaced bysummary',p,lambda b:mutate_graph(b,'abstract','A short summary.'))
 p='research/'+E['records'][1]['slug']+'/index.html'
 reject('invented MIT license for124 authoredpackage',p,lambda b:mutate_graph(b,'license','https://opensource.org/license/mit/'))
 return out

def run():
 args=set(sys.argv[1:]);need(args<={'--faults','--preseal','--live-baseline'},'bounded options')
 need(binding(read(STAGE/'FINAL_SEAL.json'))['SHA256']=='e0bb4ec8ae90cf48e0d71f9e66b723f65403d743610d5477916f7dda6a6a00e9','neutral writer finalseal pin')
 custody(); paired={}; receipts=[]
 for name,opt in [('candidate-a',0),('candidate-b',1)]:
  root=STAGE/name/'public';need(files(root)==E['overlay_exact_paths'],'actual14 output paths '+name)
  buffers={p:read(root/p) for p in E['overlay_exact_paths']}
  if not paired:paired=buffers
  else:
   for p in buffers:need(buffers[p]==paired[p],'actual normal/-O whole rendered BUFFER identity '+p)
  prefix='BUILD_NORMAL' if opt==0 else 'BUILD_OPTIMIZED';receipt=obj(STAGE/(prefix+'.stdout.json'))
  need(receipt['optimization_level']==opt and receipt['rendered_all14_buffers_and_wrote_exact_bytes'] is True,'actual distinct renderer optimization receipt')
  need(read(STAGE/(prefix+'.exitcode')).strip()==b'0' and read(STAGE/(prefix+'.stderr'))==b'','actual render exit0 emptystderr')
  receipts.append({'candidate':name,'optimization_level':opt,'buffers':{p:binding(v) for p,v in buffers.items()},'receipt':binding(read(STAGE/(prefix+'.stdout.json')))})
 details=validate(paired)
 if '--live-baseline' in args:
  need(files(SITE/'public')==sorted(B['public']),'optional oldlive593 namespace')
  for p,b in B['public'].items():need(binding(read(SITE/'public'/p))==b,'optional oldlivepublic '+p)
 if '--preseal' not in args:
  sealed=obj(HERE/'SEAL.json');payloads=obj(HERE/'MANIFEST.json')['payloads']
  need(binding(read(HERE/'MANIFEST.json'))==sealed['manifest'],'own exact manifest seal')
  need(sorted(set(files(HERE))-{'MANIFEST.json','SEAL.json'})==sorted(payloads),'own whole namespace exactrootexclusionsonly')
  for p,b in payloads.items():need(binding(read(HERE/p))==b,'own sealedpayload '+p)
  stage=obj(HERE/'STAGE_CUSTODY.json')
  need(files(STAGE)==sorted(stage['payloads']),'full stage namespace includingallhistory')
  for p,b in stage['payloads'].items():need(binding(read(STAGE/p))==b,'stage fullsealedpayload '+p)
 result={'scope':'bounded independent informed integration; no newscience orpublicationauthority','positive_checks':checks,'all14_actual_normal_O_buffers_byteidentical':True,'actual_renderer_receipts':receipts,'articles':details,'all87oldtyped_andvisible_index_preserved':True,'all88wholeoldXMLnodes_preserved':True,'virtual_counts':[605,90,91],'default_has_no_mutable_production_baseline_fence':True,'live_baseline_checked':'--live-baseline' in args,'projectimports_network_subprocess_writes_native_or_owner_campaigns':False}
 if '--faults' in args:result['own_bounded_memory_faults']=faults(paired);result['fault_count']=len(result['own_bounded_memory_faults']);result['distinct_target_paths']=len(set(q['target'] for q in result['own_bounded_memory_faults']))
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':run()
