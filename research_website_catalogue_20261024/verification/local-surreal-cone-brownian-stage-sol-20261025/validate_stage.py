"""Lean private validation: one real stage and changed-read controls only."""
from pathlib import Path
from html import escape,unescape
from html.parser import HTMLParser
import ast,base64,datetime,hashlib,json,os,re,subprocess,unicodedata
import xml.etree.ElementTree as ET
O=Path(__file__).resolve().parent;R=O.parents[1];S=O/'public';LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
PY='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(R/'scripts'))
IDS=['23444606','23440119','23224103'];CONFIG={rid:json.loads((R/'papers'/rid/'publication.json').read_text()) for rid in IDS}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(name,obj):
 p=O/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(obj if isinstance(obj,str) else json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def run(cmd):return subprocess.run(cmd,env=ENV,capture_output=True,text=True)
def check(rids,stem,case=None):
 dest=O if case is None else O/'controls';dest.mkdir(exist_ok=True)
 cmd=[str(O/'final-content-check.stage.py'),*rids,'--site',str(S),'--output-dir',str(dest),'--output-stem',stem]
 if case is not None:cmd=[str(O/'intercept_checker.py'),str(O/'controls/cases.json'),str(case),*cmd]
 proc=run([PY,'-B',*cmd]);report_path=dest/(stem+'.json')
 return proc,json.loads(report_path.read_text()) if report_path.exists() else None
# The primary stage is reset once and rendered in the specified order.
for rel in ['research/index.html','research/sitemap.xml']:(S/rel).write_bytes((LIVE/rel).read_bytes())
receipts=[]
for rid in IDS:
 proc=run([PY,'-B',str(O/'render_page.stage.py'),rid]);assert proc.returncode==0 and not proc.stderr,proc.stderr;receipts.append(json.loads(proc.stdout))
save('render-receipts.json',{'utc':now(),'scope':'Private output only','receipts':receipts})
proc,report=check(IDS,'target-stage-check-final');save('target-stage-check-final.stdout.json',proc.stdout);save('target-stage-check-final.stderr.txt',proc.stderr)
assert proc.returncode==0 and not proc.stderr and report['status']=='PASS',(proc.stderr,report['issues'] if report else None)
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
assert old['numberOfItems']==len(oldlis)==52 and new['numberOfItems']==len(newlis)==55
assert newlis[:52]==oldlis and new['itemListElement'][:52]==old['itemListElement'] and len({x['url'] for x in new['itemListElement']})==55
new_urls=[CONFIG[rid]['canonical_url'] for rid in IDS];assert [x['url'] for x in new['itemListElement'][52:]]==new_urls
def urls(p):return [x.text for x in ET.fromstring(p.read_text()).iter() if x.tag.endswith('loc')]
oldurls=urls(LIVE/'research/sitemap.xml');newurls=urls(S/'research/sitemap.xml')
assert len(oldurls)==53 and newurls[:53]==oldurls and newurls[53:]==new_urls and len(newurls)==len(set(newurls))==56
assert all(sha(S/x)==sha(LIVE/x) for x in ['research/research.css','robots.txt'])
save('index-sitemap-checks.json',{'utc':now(),'status':'PASS','old_visible_entries_byte_identical':52,'old_structured_entries_exact_in_order':52,'new_entries':55,'old_sitemap_urls_exact_in_order':53,'new_sitemap_urls':56,'only_added_urls_in_order':new_urls,'css_and_robots_byte_identical':True})
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
assert len(legacy)==51 and all(legacy.values()) and len(after['TEX_PATHS'])==54
save('legacy-dispatch-comparison.json',{'utc':now(),'status':'PASS','all_51_old_TEX_PATHS_and_actual_abstract_dispatches':legacy,'new_mappings':{rid:after['TEX_PATHS'][rid] for rid in IDS},'total_mappings':54,'pilot_page_remains_unmapped':True})
# All configured old pages are executed twice, capturing exact output bytes in
# memory. Only compact hashes/receipts are retained; no old asset tree is copied.
configured={}
for p in (R/'papers').glob('*/publication.json'):
 c=json.loads(p.read_text());url=c.get('canonical_url','https://aleckriebel.com/research/'+c['slug']+'/')
 if url in [x['url'] for x in old['itemListElement']]:configured[url]=p.parent.name
assert len(configured)==51
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
with (O/'RESEARCH_LOG.md').open('a') as f:f.write(now()+' — 65%: New3 final target checks pass. Old52 index/old53 sitemap exact; all51 old dispatches and all51 configured old-page renderer outputs are byte-identical. Executed comparisons captured in memory without asset copies.\n')

# Controls contain only changed bytes. The same pristine private stage is read
# for every run. No full stage copy, alias, symlink or original write is used.
cases=[]
def add(name,rid,path,data,expected):
 cases.append({'case':name,'record_id':rid,'overrides':{str(path.resolve()):base64.b64encode(data).decode()},'expected_issue':rid+': '+expected})
def page_case(name,rid,old,new,expected):
 p=S/'research'/CONFIG[rid]['slug']/'index.html';h=p.read_text();assert old in h,(name,old);add(name,rid,p,h.replace(old,new,1).encode(),expected)
for rid in IDS:
 c=CONFIG[rid];p=R/'papers'/rid
 for which in ['first','middle','final']:
  sentences=re.split(r'(?<=\.)\s+',c['abstract']);sentences.pop(0 if which=='first' else len(sentences)//2 if which=='middle' else -1)
  page_case(rid+'-abstract-'+which,rid,'<p>'+escape(c['abstract'])+'</p>','<p>'+escape(' '.join(sentences))+'</p>','abstract')
 page_case(rid+'-wrong-citation-doi',rid,'name="citation_doi" content="'+c['doi']+'"','name="citation_doi" content="10.5281/zenodo.0"','citation_doi')
 for key in ['pdf_filename','supplement_filename']:
  path=S/'research'/c['slug']/c[key];add(rid+'-damaged-public-'+key,rid,path,path.read_bytes()+b'\nprivate control\n',key)
 path=p/c['source_binding']['source_tex_path'];add(rid+'-source-tex-bytes',rid,path,path.read_bytes()+b'\n','exact_source_tex_path_and_bytes')
 path=R/f'verification/root-clearance-{rid}-20261025.json';add(rid+'-root-authority-bytes',rid,path,path.read_bytes()+b' ','exact_separate_root_authority')
 path=p/'promotion.json';g=json.loads(path.read_text());g['reviews']['scope']['verdict']['private_stage_false_permission']=True
 add(rid+'-deep-custom-verdict-added-field',rid,path,json.dumps(g,ensure_ascii=False).encode(),'complete_original_custom_verdicts')
 path=p/'sources/receipt.json';data=json.loads(path.read_text());data['files'][0]['bytes']+=1;add(rid+'-receipt-size',rid,path,json.dumps(data).encode(),'complete_original_receipt_and_source_assets')
for rid,name,old,new,expected in [
 ('23444606','abstract-image','actual subgroup H⊆Oz that is initial in No','abstract subgroup of Oz with an isomorphic tree','surreal_actual_ambient_initial_image_and_class_scope'),
 ('23444606','class-sized-support','every individual normal-form support is a set','individual normal-form supports may be proper classes','surreal_actual_supports_bottom_and_limits'),
 ('23440119','parameter-three','normal barrier with parameter 100','normal barrier with parameter 3','cone_exact_barrier_parameter_and_all_directions'),
 ('23440119','parameter-improvement','no parameter improvement or optimality claim','a parameter improvement and optimality claim','cone_prior_three_no_parameter_improvement_and_degeneracy'),
 ('23224103','independent-query-clocks','retaining dependence among one walker’s query visits','treating one walker’s query visits as independent','brownian_joint_law_cumulative_clocks_and_quantifiers'),
 ('23224103','inner-remainder','controls only the outer series for real nonnegative θ','also controls inner Fourier truncation and quadrature','brownian_exact_outer_bound_and_inner_limits')]:
 page_case(rid+'-'+name,rid,escape(old),escape(new),expected)
# Three discovery/edition controls exercise different records, without repeats.
rid=IDS[0];c=CONFIG[rid];page_case(rid+'-canonical-omitted',rid,'<link rel="canonical" href="'+c['canonical_url']+'">','','canonical')
rid=IDS[1];c=CONFIG[rid];p=S/'research/index.html';add(rid+'-index-omitted',rid,p,p.read_text().replace('href="/research/'+c['slug']+'/"','href="/research/omitted/"').encode(),'index_entry')
rid=IDS[2];c=CONFIG[rid];p=S/'research/sitemap.xml';add(rid+'-sitemap-omitted',rid,p,p.read_text().replace('<loc>'+c['canonical_url']+'</loc>','<loc>https://aleckriebel.com/research/omitted/</loc>').encode(),'sitemap')
page_case(rid+'-metadata-date-change',rid,'>7 October 2026</time>','>10 October 2026</time>','edition_chronology')
save('controls/cases.json',cases);results=[]
for ix,case in enumerate(cases):
 proc,r=check([case['record_id']],'control-'+str(ix).zfill(2),ix);issues=r['issues'] if r else []
 assert proc.returncode!=0 and (case['expected_issue'] in issues or r is None and proc.stderr),(case['case'],issues,proc.stderr)
 results.append({'case':case['case'],'record_id':case['record_id'],'rejected':True,'expected_issue':case['expected_issue'],'issues':issues,'exception_rejection':proc.stderr if r is None else None,'stdout_sha256':hashlib.sha256(proc.stdout.encode()).hexdigest(),'overridden_paths':list(case['overrides']),'copied_changed_bytes':sum(len(base64.b64decode(v)) for v in case['overrides'].values()),'original_mutated':False})
save('negative-controls.json',{'utc':now(),'status':'PASS','controls_rejected':len(results),'mechanism':'Complete checker on one pristine stage; only changed Path-read bytes intercepted. All exact changed bytes retained in controls/cases.json.','fixture_stage_copies':0,'cases':results})
with (O/'RESEARCH_LOG.md').open('a') as f:f.write(now()+' — 90%: '+str(len(results))+' meaningful changed-read controls rejected by complete checker. One pristine stage, no fixture tree copies or source program reruns.\n')
save('stage-validation.json',{'utc':now(),'status':'PASS','completion_percent':95,'target_checks':{rid:{'passed':sum(v['checks'].values()),'total':len(v['checks'])} for rid,v in report['papers'].items()},'negative_controls':len(results),'all_old51_dispatches_preserved':True,'all_old51_configured_renderer_outputs_byte_identical':True,'private_index_entries':55,'private_sitemap_urls':56,'production_live_browser_native_pass':False})
print(json.dumps({'target':'PASS','checks':sum(len(x['checks']) for x in report['papers'].values()),'negative_controls':len(results),'old_dispatches':len(legacy),'old_configured_renderer_comparisons':len(comparisons)}))
