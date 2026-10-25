"""Lean private validation: one real stage and changed-read controls only."""
from pathlib import Path
from html import escape,unescape
from html.parser import HTMLParser
import ast,base64,datetime,hashlib,json,os,re,subprocess,unicodedata
import xml.etree.ElementTree as ET
O=Path(__file__).resolve().parent;R=O.parents[1];S=O/'public';LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
PY='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(O)+os.pathsep+str(R/'scripts'))
IDS=['23204952','22983138','23409904'];CONFIG={rid:json.loads((R/'papers'/rid/'publication.json').read_text()) for rid in IDS}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(name,obj):
 p=O/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(obj if isinstance(obj,str) else json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def run(cmd):
 import signal
 process=subprocess.Popen(cmd,env=ENV,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
 try:out,err=process.communicate(timeout=45)
 except subprocess.TimeoutExpired:
  os.killpg(process.pid,signal.SIGTERM)
  try:out,err=process.communicate(timeout=2)
  except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);out,err=process.communicate(timeout=2)
  raise RuntimeError('Owned subprocess exceeded45seconds: '+repr(cmd))
 return subprocess.CompletedProcess(cmd,process.returncode,out,err)
def check(rids,stem,case=None):
 dest=O if case is None else O/'controls';dest.mkdir(exist_ok=True)
 cmd=[str(O/'stage_reader.py'),str(O/'final-content-check.stage.py'),*rids,'--site',str(S),'--output-dir',str(dest),'--output-stem',stem]
 if case is not None:cmd=[str(O/'stage_reader.py'),str(O/'intercept_checker.py'),str(O/'controls/cases.json'),str(case),*cmd[1:]]
 proc=run([PY,'-B',*cmd]);report_path=dest/(stem+'.json')
 return proc,json.loads(report_path.read_text()) if report_path.exists() else None
# The primary stage is reset once and rendered in the specified order.
for rel in ['research/index.html','research/sitemap.xml']:(S/rel).write_bytes((LIVE/rel).read_bytes())
receipts=[]
for rid in IDS:
 proc=run([PY,'-B',str(O/'render_page.stage.py'),rid]);assert proc.returncode==0 and not proc.stderr,proc.stderr;receipts.append(json.loads(proc.stdout))
save('render-receipts.json',{'utc':now(),'scope':'Private output only','receipts':receipts})
proc,report=check(IDS,'target-stage-check-final');save('target-stage-check-final.stdout.json',proc.stdout);save('target-stage-check-final.stderr.txt',proc.stderr)
assert proc.returncode==0 and not proc.stderr and report['status']=='PASS',(proc.stderr[:3000],report['issues'] if report else None)
class Visible(HTMLParser):
 def __init__(self,h):super().__init__();self.body=False;self.parts=[];self.feed(h)
 def handle_starttag(self,t,a):
  if t=='body':self.body=True
  if self.body and t in ['p','h1','h2','li','br','section','header','footer']:self.parts.append('\n')
 def handle_endtag(self,t):
  if t=='body':self.body=False
  if self.body and t in ['p','h1','h2','li','section']:self.parts.append('\n')
 def handle_data(self,t):
  if self.body:self.parts.append(t)
for rid in IDS:
 c=CONFIG[rid];page=S/'research'/c['slug']/'index.html';h=page.read_text();v=Visible(h)
 save('public-copy-'+rid+'.txt','\n\n'.join(' '.join(x.split()) for x in ''.join(v.parts).split('\n') if x.strip())+'\n')
 sections=[{'id':sid,'heading':unescape(re.search(r'<h2>(.*?)</h2>',seg,re.S).group(1)),'paragraphs':[unescape(re.sub('<[^>]+>','',x)) for x in re.findall(r'<p>(.*?)</p>',seg,re.S)],'list_items':[unescape(re.sub('<[^>]+>','',x)) for x in re.findall(r'<li>(.*?)</li>',seg,re.S)],'links':[{'label':unescape(re.sub('<[^>]+>','',txt)),'href':unescape(url),'download':'download' in attr} for url,attr,txt in re.findall(r'<a href="([^"]+)"([^>]*)>(.*?)</a>',seg,re.S)]} for sid,seg in re.findall(r'<section id="([^"]+)">(.*?)</section>',h,re.S)]
 save('public-sections-'+rid+'.json',{'record_id':rid,'state':'ACTUAL_PRIVATE_STAGE','sections':sections})
 expected=json.loads((R/'papers'/rid/'reviews/editorial/public-sections.json').read_text());actual={x['id']:x for x in sections}
 assert [x['heading'] for x in sections]==[x['heading'] for x in expected['sections']]
 for spec in expected['sections']:
  if spec['id'] in ['abstract','plain-language','result','proof','limits','status']:assert actual[spec['id']]['paragraphs']==spec['paragraphs']
  elif spec['id']=='paper':assert actual['paper']['paragraphs'][0]==spec['paragraphs'][0]
  elif spec['id']=='collaborate':assert actual['collaborate']['paragraphs'][0]==spec['paragraphs'][0]
  elif spec['id']=='background':assert actual['background']['list_items']==[x['title']+': '+x['note'] for x in spec['references']]
def ilist(h):return json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',h,re.S).group(1))['mainEntity']
old_index=(LIVE/'research/index.html').read_text();new_index=(S/'research/index.html').read_text();old=ilist(old_index);new=ilist(new_index)
oldlis=re.findall(r'<li>.*?</li>',old_index,re.S);newlis=re.findall(r'<li>.*?</li>',new_index,re.S)
assert old['numberOfItems']==len(oldlis)==57 and new['numberOfItems']==len(newlis)==60
assert newlis[:57]==oldlis and new['itemListElement'][:57]==old['itemListElement'] and len({x['url'] for x in new['itemListElement']})==60
new_urls=[CONFIG[rid]['canonical_url'] for rid in IDS];assert [x['url'] for x in new['itemListElement'][57:]]==new_urls
def urls(p):return [x.text for x in ET.fromstring(p.read_text()).iter() if x.tag.endswith('loc')]
oldurls=urls(LIVE/'research/sitemap.xml');newurls=urls(S/'research/sitemap.xml')
assert len(oldurls)==58 and newurls[:58]==oldurls and newurls[58:]==new_urls and len(newurls)==len(set(newurls))==61
assert all(sha(S/x)==sha(LIVE/x) for x in ['research/research.css','robots.txt'])
save('index-sitemap-checks.json',{'utc':now(),'status':'PASS','old_visible_entries_byte_identical':57,'old_structured_entries_exact_in_order':57,'new_entries':60,'old_sitemap_urls_exact_in_order':58,'new_sitemap_urls':61,'only_added_urls_in_order':new_urls,'css_and_robots_byte_identical':True})
def helpers(path):
 env={'Path':Path,'re':re,'unicodedata':unicodedata};nodes=[]
 for n in ast.parse(path.read_text()).body:
  if isinstance(n,ast.FunctionDef):nodes.append(n)
  elif isinstance(n,ast.Assign) and all(isinstance(t,ast.Name) and t.id.isupper() for t in n.targets):
   try:ast.literal_eval(n.value)
   except (ValueError,TypeError):continue
   nodes.append(n)
 exec(compile(ast.Module(body=nodes,type_ignores=[]),'<private pure helpers>','exec'),env);return env
before=helpers(O/'inputs/final-content-check.py');after=helpers(O/'final-content-check.proposed.py');legacy={};old_inputs={}
for rid,path in before['TEX_PATHS'].items():
 assert after['TEX_PATHS'][rid]==path
 source_path=R/'papers'/rid/'sources'/path;source=source_path.read_text();old_inputs[str(source_path)]={'bytes':source_path.stat().st_size,'sha256':sha(source_path)}
 if rid=='22089551':source=re.search(r'\\ifdefined\\japsubmission(.*?)\\else(.*?)\\fi',source,re.S).group(2)
 a=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',source,re.S).group(1);legacy[rid]=before['abstract_tokens'](a,rid)==after['abstract_tokens'](a,rid)
assert len(legacy)==56 and all(legacy.values()) and len(after['TEX_PATHS'])==59
save('legacy-dispatch-comparison.json',{'utc':now(),'status':'PASS','all_56_old_TEX_PATHS_and_actual_abstract_dispatches':legacy,'new_mappings':{rid:after['TEX_PATHS'][rid] for rid in IDS},'total_mappings':len(after['TEX_PATHS']),'pilot_page_remains_unmapped':True})
# All configured old pages are executed twice, capturing exact output bytes in
# memory. Only compact hashes/receipts are retained; no old asset tree is copied.
configured={}
for p in (R/'papers').glob('*/publication.json'):
 c=json.loads(p.read_text());url=c.get('canonical_url','https://aleckriebel.com/research/'+c['slug']+'/')
 if url in [x['url'] for x in old['itemListElement']]:configured[url]=p.parent.name
assert len(configured)==56
comparisons={}
for item in old['itemListElement']:
 if item['url'] not in configured:continue
 rid=configured[item['url']];outputs={}
 for label,source in [('original',O/'inputs/render_page.py'),('proposed',O/'render_page.proposed.py')]:
  proc=run([PY,'-B',str(O/'memory_render.py'),str(source),rid]);assert proc.returncode==0 and not proc.stderr,(rid,label,proc.stderr)
  result=json.loads(proc.stdout);outputs[label]=result['outputs'];old_inputs.update(result['original_read_bindings'])
 assert outputs['original']==outputs['proposed'],rid
 comparisons[rid]={'all_output_bytes_equal':True,'files':outputs['original']}
save('old-versioned-render-comparison.json',{'utc':now(),'status':'PASS','configured_old_records':len(comparisons),'mechanism':'Complete current/proposed renderer executions with output bytes captured in memory; unchanged original read-only inputs.','actual_output_files_written':0,'pilot':'free-spanning-forest-degree remains an unchanged unmapped manual page.','cases':comparisons})
save('old-comparison-inputs-before.json',{'utc':now(),'bindings':old_inputs})
with (O/'RESEARCH_LOG.md').open('a') as f:f.write(now()+' — 65%: New2 final target checks pass. Old55 index/old56 sitemap exact; all56 old dispatches and all56 configured old-page renderer outputs are byte-identical. Executed comparisons captured in memory without asset copies.\n')

