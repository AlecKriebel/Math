"""Read-only default private-page data comparison; no network, subprocess or project-code imports."""
from pathlib import Path
from html.parser import HTMLParser
import datetime,hashlib,html,json,re,stat,sys
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
O=Path(__file__).resolve().parent;S=P/'papers/23153134/sources';V=O/'preview'
if len(sys.argv)!=1:raise SystemExit('Only ordinary read-only default is supported')
checks=[]
def need(name,value):checks.append({'check':name,'PASS':bool(value)})
def load(q):return json.loads(q.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def match(q,v):
 b=q.read_bytes();mode=v.get('mode');mode=int(mode,8) if isinstance(mode,str) else mode
 return q.is_file() and not q.is_symlink() and len(b)==v['bytes'] and sha(b)==v.get('sha256',v.get('SHA256')) and (mode is None or stat.S_IMODE(q.stat().st_mode)==mode)
def plain(t):return html.unescape(re.sub(r'<[^>]+>','',t))
class Page(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.tags=[]
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
seal=load(O/'INITIAL_SEAL.json');custody=load(O/'SOURCE_CUSTODY.json');e=load(O/'EXPECTATIONS.json');m=load(O/'PAGE_MODEL.json')
need('All six original INITIAL payloads unchanged',all(match(O/x['path'],x) for x in seal['payloads']))
need('Exact original INITIAL seal',match(O/'INITIAL_SEAL.json',{'bytes':2246,'SHA256':'19e90a73d80bef02071b8424c726d5e7747858319e5ed47762982ceaa1a3fd97'}))
actual=list(S.rglob('*'));sf=sorted(str(q.relative_to(S)) for q in actual if q.is_file());sd=sorted(str(q.relative_to(S)) for q in actual if q.is_dir())
need('All94 source files/4 dirs bytes and modes unchanged',len(sf)==94 and len(sd)==4 and not any(q.is_symlink() for q in actual) and sf==[x['path'] for x in custody['files']] and sd==[x['path'] for x in custody['directories']] and all(match(S/x['path'],x) for x in custody['files']) and all(oct(stat.S_IMODE((S/x['path']).stat().st_mode))==x['mode'] for x in custody['directories']))
need('All16 source reading references unchanged',all(match(P/x['path'],x) for x in load(O/'SOURCE_PINS.json')['entries']))
need('Concrete full-original authority pins',match(P/'verification/root-clearance-23153134-20261116.json',{'bytes':2357,'SHA256':'d6d321645e3fbe7bac44892273e5398622e15c740604c2376720ed4f1325af9f'}) and match(P/'papers/23153134/reviews/root/ROOT_REVIEW.md',{'bytes':13180,'SHA256':'7bb3f9959fd985688ab87fb9955e464d51dc9fcd94de9fc1077ee3c533a1e444'}))
r=load(S/'record.response.body');f=load(S/'files-23153134.response.body')
need('Whole original native metadata/file API objects literal',e['native_metadata_entire_original']==r['metadata'] and e['native_record_file_objects_original_order']==r['files'] and e['whole_native_files_endpoint_original']==f)
raw=(V/'index.html').read_text();page=Page();page.feed(raw)
main=re.search(r'<main\b[^>]*>[\s\S]*?</main>\n',raw).group();head=re.search(r'<head>\n([\s\S]*?)</head>',raw).group(1)
need('Exact whole page/MAIN/head/model binding',main.encode()==(O/'MAIN.html').read_bytes() and head.encode()==(O/'HEAD.html').read_bytes() and all(match(O/x,m[k]) for x,k in [('MAIN.html','whole_MAIN'),('HEAD.html','HEAD'),('preview/index.html','whole_page'),('citation.bib','BibTeX')]))
meta={a.get('name',a.get('property')):a['content'] for t,a in page.tags if t=='meta' and 'content' in a}
a=json.loads(re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>',head).group(1))
tex=(S/'assets/negative_gramian_cover.tex').read_text();at=re.search(r'\\begin\{abstract\}\n([\s\S]*?)\n\\end\{abstract\}',tex).group(1);abstract=' '.join(at.split())
for x,y in [(r'$\R^{17}$','ℝ¹⁷'),('$T>0$','T > 0'),(r'$P_T=T\pi^*g$','P_T = Tπ*g'),('$-1/T$','−1/T')]:abstract=abstract.replace(x,y)
visible=plain(re.search(r'<p id="original-abstract">([\s\S]*?)</p>',main).group(1))
need('Full original abstract visible/model/schema/DC',at==e['full_original_abstract_TeX'] and abstract==visible==m['abstract']==a['abstract']==meta['DC.description'] and a==m['scholarly_article'])
need('Distinct full Description retained without visible duplication',e['full_distinct_native_Description_HTML']==r['metadata']['description'] and r['metadata']['description'] not in main and m['duplicate_native_Description_visible'] is False)
need('Original title/DOI/ORCID/date/printed-and-native1.0',a['name']==r['metadata']['title']==meta['citation_title'] and a['identifier']=='https://doi.org/'+r['doi'] and a['author']['identifier']=='https://orcid.org/0009-0001-9320-500X' and a['datePublished']==r['metadata']['publication_date']=='2026-10-05' and a['version']==r['metadata']['version']==m['printed_version']=='1.0' and a['dateCreated']==r['created'] and meta['citation_publication_date']=='2026/10/05')
ids=[x['id'] for t,x in page.tags if 'id' in x]
need('One MAIN id=main, one H1 and unique IDs',len(ids)==len(set(ids)) and len([1 for t,x in page.tags if t=='main'])==1 and any(t=='main' and x.get('id')=='main' for t,x in page.tags) and len([1 for t,x in page.tags if t=='h1'])==1)
need('Private noindex/null canonical/base/production/AA/followup',meta['robots']=='noindex,nofollow,noarchive' and all(m[k] is None for k in ['canonical_url','base_url','production_url','AA','follow_up']) and m['publication_authority'] is False and not any(t=='base' or (t=='link' and x.get('rel')=='canonical') for t,x in page.tags))
links=[]
for t,x in page.tags:
 for key in ['href','src']:
  u=x.get(key)
  if not u or u.startswith('https://') or u in ['/','/research/']:continue
  links.append(u[1:] in ids if u.startswith('#') else '/' not in u.split('#')[0] and (V/u.split('#')[0]).is_file())
need('Actual local links/resources/fragments exist',all(links))
order=[x['key'] for x in r['files']];assetlist=re.search(r'<ol id="native-assets">([\s\S]*?)</ol>',main).group(1)
need('All9 native assets unchanged and native order/MD5',len(order)==9 and order==m['native_asset_order']==re.findall(r'<li><a href="([^"]+)" download>',assetlist) and all((V/x['key']).read_bytes()==(S/'assets'/x['key']).read_bytes() and 'md5:'+hashlib.md5((V/x['key']).read_bytes()).hexdigest()==x['checksum'] for x in r['files']))
need('Actual native licence retained, no native MIT split',r['metadata']['license']=={'id':'cc-by-4.0'} and (V/'LICENSE.txt').read_bytes()==(S/'assets/LICENSE.txt').read_bytes() and 'verification code, results and authored documentation' in (V/'LICENSE.txt').read_text() and a['license']=='https://creativecommons.org/licenses/by/4.0/')
need('Titled native PDF FitH/direct download/citation',meta['citation_pdf_url']=='negative_gramian_cover.pdf' and any(t=='iframe' and x.get('src')=='negative_gramian_cover.pdf#view=FitH' and x.get('title') for t,x in page.tags) and any(t=='a' and x.get('href')=='negative_gramian_cover.pdf' and 'download' in x for t,x in page.tags))
bib=(O/'citation.bib').read_bytes();need('Bib copies identical and edition accurate',bib==(V/'citation.bib').read_bytes() and all(x in bib.decode() for x in ['2026-10-05','version = {1.0}','10.5281/zenodo.23153134','CC-BY-4.0']))
need('Exact shared1170B white Arial CSS',match(V/'research.css',{'bytes':1170,'sha256':'f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a'}))
words=len(' '.join(plain(x) for x in re.findall(r'<p data-explanation>([\s\S]*?)</p>',main)).split())
need('600–900 explanatory words',600<=words<=900 and words==m['explanatory_words_outside_abstract_references_resources'])
result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS' if all(x['PASS'] for x in checks) else 'NO_GO','checks':checks,'explanatory_words':words,'whole_MAIN':m['whole_MAIN'],'whole_page':m['whole_page'],'source_files':94,'source_directories':4,'initial_files_unchanged':7,'scientific_native_or_renderer_runs':0,'writes':0,'follow_up':None,'publication_authority':False}
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(0 if result['status']=='PASS' else 1)
