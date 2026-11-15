"""Independent static output checks. Standard library only; read-only, no project imports."""
from pathlib import Path
from hashlib import sha256
import json,re,html
from html.parser import HTMLParser
import xml.etree.ElementTree as ET
A=Path(__file__).resolve().parent; P=A.parent; S=P.parent/'nash-quotient-robinson-private-stage-sol-20261115'
N=0
checks=[]
def need(ok,label):
 global N
 N+=1
 if not ok: raise ValueError(label)
 checks.append(label)
def same(x,y):
 if type(x) is not type(y):return False
 if isinstance(x,dict):return list(x)==list(y) and all(same(x[k],y[k]) for k in x)
 if isinstance(x,list):return len(x)==len(y) and all(same(a,b) for a,b in zip(x,y))
 return x==y
def struct(t):
 matches=re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',t,re.S)
 need(len(matches)==1,'one scholarly script')
 return json.loads(matches[0])
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.tags=[];self.ids=[];self.meta={};self.links=[];self.hrefs=[];self.src=[]
 def handle_starttag(self,t,at):
  d=dict(at);self.tags.append((t,d))
  if 'id'in d:self.ids.append(d['id'])
  if t=='meta':
   key=d.get('name',d.get('property',''))
   need(key not in self.meta,'unique metadata name '+key);self.meta[key]=d.get('content')
  if t=='link':self.links.append(d)
  if t=='a':self.hrefs.append(d.get('href'))
  if 'src'in d:self.src.append(d['src'])
expected=json.loads((P/'EXPECTED.json').read_bytes());baseline=json.loads((P/'BASELINE.json').read_bytes())
need(sha256((P/'INITIAL_SEAL.json').read_bytes()).hexdigest()=='2fe08817cd30a6dbc0b65f7f626fac3714eae11c164ba67ddec571d26c87748c','parent independent seal')
need(sha256((S/'FINAL_SEAL.json').read_bytes()).hexdigest()=='e0bb4ec8ae90cf48e0d71f9e66b723f65403d743610d5477916f7dda6a6a00e9','exact staged final seal')
paths=expected['overlay_exact_paths']; buffers={}
for c in ['candidate-a','candidate-b']:
 actual=sorted(str(p.relative_to(S/c/'public')) for p in (S/c/'public').rglob('*') if p.is_file())
 need(actual==paths,'candidate exact14 namespace '+c)
for path in paths:
 a=(S/'candidate-a/public'/path).read_bytes();b=(S/'candidate-b/public'/path).read_bytes()
 need(a==b,'actual normal O whole buffer '+path);buffers[path]=a
for label,opt in [('BUILD_NORMAL',0),('BUILD_OPTIMIZED',1)]:
 r=json.loads((S/(label+'.stdout.json')).read_bytes())
 need(r['optimization_level']==opt and r['rendered_all14_buffers_and_wrote_exact_bytes']is True,'actual distinct render receipt '+label)
 need((S/(label+'.exitcode')).read_text().strip()=='0' and (S/(label+'.stderr')).read_bytes()==b'','receipt exit and stderr '+label)
articles=[]
for rec in expected['records']:
 base='research/'+rec['slug']+'/'; t=buffers[base+'index.html'].decode();p=Parser();p.feed(t)
 main=re.findall(r'<main\b[^>]*>.*?</main>',t,re.S)
 need(len(main)==1 and main[0]==rec['expected_main'],'entire independent original main '+rec['record_id'])
 need(len(p.ids)==len(set(p.ids)) and 'main'in p.ids,'unique ids and skip target '+rec['record_id'])
 need(p.meta['robots']=='index,follow' and 'noindex'not in t,'indexable actual document '+rec['record_id'])
 metas={'description':rec['description'],'citation_title':rec['title'],'citation_author':'Alec Kriebel','citation_author_orcid':'https://orcid.org/0009-0001-9320-500X','citation_publication_date':rec['datePublished'].replace('-','/'),'citation_version':rec['version'],'citation_doi':'10.5281/zenodo.'+rec['record_id']}
 for k,v in metas.items():need(p.meta[k]==v,'exact head '+rec['record_id']+' '+k)
 need(any(x.get('rel')=='canonical' and x.get('href')==rec['canonical'] for x in p.links),'correct canonical '+rec['record_id'])
 need(any(x.get('rel')=='icon' and x.get('href')=='/favicon.ico' for x in p.links),'favicon '+rec['record_id'])
 need(any(x.get('rel')=='stylesheet' and x.get('href')=='/research/research.css' for x in p.links),'shared stylesheet '+rec['record_id'])
 graph=struct(t);page,article=graph['@graph']
 need(page['@type']=='WebPage' and article['@type']=='ScholarlyArticle','scholarly graph types')
 need(page['mainEntity']['@id']==article['@id']==rec['canonical']+'#article' and article['mainEntityOfPage']['@id']==page['@id']==rec['canonical']+'#page','mutual graph linkage')
 need(article['abstract']==rec['full_original_abstract'] and article['datePublished']==rec['datePublished'] and article['version']==rec['version'],'original abstract date version')
 need(page['dateCreated']==page['dateModified']=='2026-11-15' and page['dateCreated']!=article['datePublished'],'build versus publication dates')
 old=rec['original_scholarly_object']; mutable={'@id','url','mainEntityOfPage','inLanguage','isAccessibleForFree','creativeWorkStatus','encoding'}
 for k,v in old.items():
  if k not in mutable:need(k in article and same(v,article[k]),'retained original scholarly field '+k)
 need(article['creativeWorkStatus']=='Unrefereed preprint','accurate status')
 for asset,info in rec['assets'].items():
  value=buffers[base+asset]; need(len(value)==info['binding']['bytes'] and sha256(value).hexdigest()==info['binding']['SHA256'],'whole native or Bib identity '+base+asset)
  if asset.endswith('.pdf'):need(p.meta['citation_pdf_url']==rec['canonical']+asset,'absolute PDF citation exact')
 for href in p.hrefs+p.src:
  if href and href.startswith('assets/'):
   local=base+href.split('#',1)[0];need(local in buffers,'local actual material link resolves '+local)
 need(len(article['encoding'])==2,'two whole native encodings')
 for e in article['encoding']:
  need(e['contentUrl'].startswith(rec['canonical']+'assets/') and e['sameAs'].startswith('https://zenodo.org/api/records/'+rec['record_id']+'/files/'),'native and local graph assets')
  if rec['record_id']=='23578599' and e['encodingFormat']=='application/zip':need('license'not in e,'mixed-license ZIP has no blanket prose grant')
  else:need(e['license']=='https://creativecommons.org/licenses/by/4.0/','actual asset prose grant')
 styles=re.findall(r'<style>(.*?)</style>',t,re.S)
 need(len(styles)==1 and not re.search(r'(display\s*:\s*none|visibility\s*:\s*hidden|opacity\s*:\s*0|overflow\s*:\s*hidden|position\s*:\s*absolute)',styles[0],re.I),'no hiding clipping stylesheet')
 need('overflow-wrap:anywhere'in styles[0] and 'white-space:pre-wrap'in styles[0],'math wrapping supplement')
 for tag,d in p.tags:
  need(not any(k=='hidden'or k.startswith('on') for k in d),'no hidden or event attribute')
 if rec['record_id']=='23578599':need(main[0].count('<table>')==1 and main[0].count('<tbody>')==1,'actual Nash table')
 if rec['record_id']=='23333002':need(any(tag=='iframe'and d.get('width')=='100%'and d.get('height')=='850' for tag,d in p.tags),'actual Robinson raw reader dimensions')
 articles.append({'record_id':rec['record_id'],'main_SHA256':sha256(main[0].encode()).hexdigest(),'graph_and_assets_verified':True})
index=buffers['research/index.html'].decode();schema=struct(index);items=schema['mainEntity']['itemListElement']
need(len(items)==schema['mainEntity']['numberOfItems']==90,'90 actual typed items')
need(same(items[:87],baseline['old_itemlist_complete_typed_ordered']),'whole87 typed ordered old items')
li=re.findall(r'<li>.*?</li>',index,re.S)
need(len(li)==90 and li[:87]==baseline['old_visible_li_bytes'],'87 prior visible li bytes')
old=(P/'baseline/index.html').read_text();restored=index
for rec in expected['records']:
 restored=''.join(line for line in restored.splitlines(keepends=True) if '<li><a href="/research/'+rec['slug']+'/">'not in line)
newld=re.search(r'(<script type="application/ld\+json">\s*)(.*?)(\s*</script>)',restored,re.S);oldld=re.search(r'(<script type="application/ld\+json">\s*)(.*?)(\s*</script>)',old,re.S)
restored=restored[:newld.start(2)]+oldld[2]+restored[newld.end(2):]
need(restored==old,'entire old index restored independently')
sm=buffers['research/sitemap.xml'].decode();nodes=re.findall(r'<url>.*?</url>',sm,re.S)
need(len(ET.fromstring(sm))==len(nodes)==91 and nodes[:88]==baseline['old_sitemap_url_node_bytes'],'all88 raw old XML nodes preserved')
restored=''.join(line for line in sm.splitlines(keepends=True) if not any('<loc>'+r['canonical']+'</loc>'in line for r in expected['records']))
need(restored==(P/'baseline/sitemap.xml').read_text(),'entire old sitemap restored independently')
need(len(set(baseline['public'])|set(buffers))==605 and set(baseline['public'])&set(buffers)=={'research/index.html','research/sitemap.xml'},'605 exact virtual namespace and2replacements')
print(json.dumps({'checks':N,'articles':articles,'paired_rendered_buffers':14,'prior_typed_and_visible_items':87,'prior_sitemap_nodes':88,'native_and_Bib_assets':9,'material_integration_defects':[],'network_project_imports_subprocess_file_writes':False,'scientific_or_owner_campaign_execution':False,'browser_live_verification_claimed':False,'all_labels':checks},ensure_ascii=False,indent=2))
