"""One-time independent input freeze. Reads approved sources and old site only; never stage."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
from html.parser import HTMLParser
import json, re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SITE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
def now(): return datetime.now(timezone.utc).isoformat()
def digest(b): return {'bytes':len(b),'SHA256':sha256(b).hexdigest()}
def save(name,obj): (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
class Head(HTMLParser):
 def __init__(self): super().__init__(); self.meta={};self.links=[];self.scripts=[];self.active=False;self.data=''; self.title=''; self.intitle=False
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='meta': self.meta[a.get('name',a.get('property',''))]=a.get('content','')
  if t=='link': self.links.append(a)
  if t=='title':self.intitle=True
  if t=='script' and a.get('type')=='application/ld+json':self.active=True;self.data=''
 def handle_data(self,d):
  if self.active:self.data+=d
  if self.intitle:self.title+=d
 def handle_endtag(self,t):
  if t=='title':self.intitle=False
  if t=='script' and self.active:self.scripts.append(json.loads(self.data));self.active=False
ids=['23578599','23423736','23333002']; slugs=['free-chain-nash-intersection-counterexample','projective-line-quotient-rogalski-sierra-algebra','robinson-ideal-only-tangency-certificates']
public={str(p.relative_to(SITE/'public')):digest(p.read_bytes()) for p in sorted((SITE/'public').rglob('*')) if p.is_file()}
index=(SITE/'public/research/index.html').read_text(); sm=(SITE/'public/research/sitemap.xml').read_text(); parser=Head();parser.feed(index)
olditems=parser.scripts[0]['mainEntity']['itemListElement']; visible=re.findall(r'<li>.*?</li>',index,re.S); nodes=re.findall(r'<url>.*?</url>',sm,re.S)
if len(public)!=593 or len(olditems)!=87 or len(visible)!=87 or len(nodes)!=88:raise RuntimeError('baseline counts')
(HERE/'baseline').mkdir(exist_ok=True)
for n in ['index.html','sitemap.xml','research.css']:(HERE/'baseline'/n).write_bytes((SITE/'public/research'/n).read_bytes())
inputs={}; namespaces={}; articles=[]; paths=[]
for record,slug in zip(ids,slugs):
 e=ROOT/'papers'/record/'reviews/editorial'; s=ROOT/'papers'/record/'sources'
 for folder in [s,e]:
  members=[]
  for p in sorted(folder.rglob('*')):
   if p.is_symlink():raise RuntimeError('symlink')
   if p.is_file(): rel=str(p.relative_to(ROOT));inputs[rel]=digest(p.read_bytes());members.append(rel)
  namespaces[str(folder.relative_to(ROOT))]=members
 a=ROOT/'verification'/f'root-editorial-{record}-20261115.json'; inputs[str(a.relative_to(ROOT))]=digest(a.read_bytes())
 raw=(e/'candidate/index.html').read_bytes(); txt=raw.decode(); m=re.search(r'<main\b[^>]*>.*?</main>',txt,re.S)
 if not m: raise RuntimeError('main missing')
 main=m.group(); expected=main if re.match(r'<main[^>]*\bid=',main) else main.replace('<main>','<main id="main">',1)
 parser=Head();parser.feed(txt)
 abstract=parser.scripts[0]['abstract']; title=parser.scripts[0].get('headline',parser.scripts[0].get('name'))
 assets={}
 for p in sorted((e/'candidate/assets').iterdir()):
  if p.is_file(): assets['assets/'+p.name]={'original':str(p),'binding':digest(p.read_bytes())}
 canonical='https://aleckriebel.com/research/'+slug+'/'
 article={'record_id':record,'slug':slug,'canonical':canonical,'original_HTML':str(e/'candidate/index.html'),'original_HTML_binding':digest(raw),'expected_main':expected,'expected_main_binding':digest(expected.encode()),'full_original_abstract':abstract,'title':title,'browser_title':parser.title,'description':parser.meta['description'],'original_head_metadata':parser.meta,'original_scholarly_object':parser.scripts[0],'assets':assets,'source_namespace_count':len(namespaces[str(s.relative_to(ROOT))]),'complete_editorial_namespace_count':len(namespaces[str(e.relative_to(ROOT))]),'datePublished':parser.scripts[0]['datePublished'],'version':parser.scripts[0]['version']}
 articles.append(article)
 for name in ['index.html',*assets]: paths.append('research/'+slug+'/'+name)
 # Fresh full original byte copies used as independently captured evidence, never imports.
 out=HERE/'approved'/record;out.mkdir(parents=True,exist_ok=True)
 for n in ['PUBLIC_COPY.md','candidate/index.html','PUBLICATION_REQUIREMENTS.json','RIGHTS_AND_IDENTITY.json','SCHEMA_ADAPTER.json','VERDICT.json','SOURCE_PROTOCOL_BINDINGS.json']:
  p=e/n
  if p.exists(): q=out/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes())
paths+=['research/index.html','research/sitemap.xml']
if [a['complete_editorial_namespace_count'] for a in articles]!=[56,62,77]:raise RuntimeError('editorial namespaces')
core={str(p.relative_to(ROOT)):digest(p.read_bytes()) for p in sorted((ROOT/'scripts').glob('*.py'))}
if core['scripts/checkpoint_subtree.py']['SHA256']!='405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0':raise RuntimeError('authorized checkpoint')
save('APPROVED_INPUT_MANIFEST.json',{'UTC':now(),'inputs':inputs,'complete_namespaces':namespaces,'all_current_script_bindings':core})
save('BASELINE.json',{'UTC':now(),'site':str(SITE),'head':'e2e064c48755452a56c2a31207fb12d7e55074fb','branch':'master','public':public,'public_count':593,'old_itemlist_complete_typed_ordered':olditems,'old_visible_li_bytes':visible,'old_sitemap_url_node_bytes':nodes})
save('EXPECTED.json',{'UTC':now(),'scope':'Independent informed integration oracle frozen before writer implementation/output; no new science','records':articles,'overlay_exact_paths':sorted(paths),'new_leaves':12,'overlay_count':14,'union_public_count':605,'research_item_count':90,'sitemap_url_count':91,'whole_main_rule':'Only add id=main to bare main if needed; zero prose/Unicode/structure changes','metadata_requirements':['index,follow','canonical','citation_author_orcid','absolute citation_pdf_url','original publication date distinct builddate','existing /research/research.css','/favicon.ico','WebPage/ScholarlyArticle graph','whole original abstract','correct DOI/version/author/license/assets'],'rights':['123 prose CC BY4.0 and code MIT','124 and125 broad CC BY4.0; separate code instrument null'],'private_flags':'Original false/null/historical states remain literal; root retains installation/live authority; canonical/AA null'})
faults=[{'target':p,'mechanism':('one-byte asset corruption' if p.endswith(('.pdf','.zip','.bib')) else 'scientific qualification/prose mutation' if p not in ['research/index.html','research/sitemap.xml'] else 'one preserved old typed/visible entry or XML node mutation'),'must_be_rejected':True} for p in sorted(paths)]
faults += [{'target':'HTML '+r,'mechanism':m,'must_be_rejected':True} for r,m in [('23578599','remove specified-reference limitation; preserve abstract/main and HTML table'),('23423736','change second left x4 factor f5 or positive pullback'),('23333002','remove epsilon0 or arbitrary-degree qualification'),('23333002','drop iframe width100%/height850'),('each','change original publication date to builddate'),('each','wrong canonical/citation_pdf_url'),('each','wrong whole abstract/DOI/type in scholarly graph'),('each','invent MIT for124/125')]]
save('FAULT_ORACLE.json',{'UTC':now(),'independence':'Written without opening stage implementation/output/report','minimum14distinct_overlay_target_faults':faults,'additional_namespace_requirements':['No extra/missing overlay file','No altered existing591 nonaggregate public files','Exact first87typed ItemList items and visibleli bytes','Exact first88XMLurlnodes','Complete source/editorial namespaces; no recursive basename exclusions','whole literal native/custom/verdict/API/transport/headerorder/null/history identity']})
log=f'# Research log\n\n- {now()} — Intake and independent expectation freeze; completion 30%. No stage implementation/output/report opened. Failed concatenated-ID reads corrected; broad file inventory exposed filenames only. Full source/editorial namespace and593public baseline captured. Root123/124full authority read;125entire object parsed and unique body read with repeated factaudit equality; native support is independently reading full literal objects.\n'
(HERE/'RESEARCH_LOG.md').write_text(log)
save('READ_LEDGER.json',{'UTC':now(),'root_authorities':[str(ROOT/'verification'/f'root-editorial-{x}-20261115.json') for x in ids],'fully_read_original_candidate_HTML_and_mains':ids,'PUBLIC_COPY':'123 and125 full;124 header rerun pending because combinedoutput truncation; full byte copies retained','complete_json_byte_capture':'All approved/editorial/native source bytes pinned; direct semantic reading and typed comparisons distinguished','stage_content_read_before_initial_seal':False})
seal={str(p.relative_to(HERE)):digest(p.read_bytes()) for p in sorted(HERE.rglob('*')) if p.is_file() and 'native-oracle' not in p.parts}
save('INITIAL_SEAL.json',{'UTC':now(),'completion_percent':30,'writer_content_unread':True,'payloads':seal})
print(json.dumps({'initial_seal':digest((HERE/'INITIAL_SEAL.json').read_bytes()),'input_files':len(inputs),'source_counts':[a['source_namespace_count'] for a in articles],'editorial_counts':[a['complete_editorial_namespace_count'] for a in articles],'overlay_paths':len(paths),'old_public':len(public),'old_items':len(olditems),'old_visible':len(visible),'old_sitemap':len(nodes)}))
