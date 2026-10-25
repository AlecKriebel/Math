"""Execute private render, preservation checks and falsification controls."""
from pathlib import Path
from html.parser import HTMLParser
from html import escape,unescape
import ast, base64, copy, datetime, hashlib, json, os, re, shutil, subprocess, unicodedata
import xml.etree.ElementTree as ET
O=Path(__file__).resolve().parent;R=O.parents[1];S=O/'public'
LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
PY='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(R/'scripts'))
IDS=['23383961','23430906'];CONFIG={rid:json.loads((R/'papers'/rid/'publication.json').read_text()) for rid in IDS}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(name,value):
 p=O/name;p.parent.mkdir(parents=True,exist_ok=True);assert not p.exists(),p
 p.write_text(value if isinstance(value,str) else json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def run(command):return subprocess.run(command,env=ENV,capture_output=True,text=True)
def check(site,rids,out,stem,wrapper=None):
 command=[PY,'-B',str(O/'final-content-check.stage.py'),*rids,'--site',str(site),'--output-dir',str(out),'--output-stem',stem]
 if wrapper:command=[PY,'-B',str(O/'authority_runner.py'),str(wrapper),*command[2:]]
 proc=run(command);(out/(stem+'.stdout.json')).write_text(proc.stdout);(out/(stem+'.stderr.txt')).write_text(proc.stderr)
 p=out/(stem+'.json');report=json.loads(p.read_text()) if p.exists() else None
 return proc,report
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
receipts=[]
# Explicit sequential resets/renders preserve the intended old50 + new2 order.
for rel in ['research/index.html','research/sitemap.xml']:shutil.copyfile(LIVE/rel,S/rel)
for rid in IDS:
 proc=run([PY,'-B',str(O/'render_page.stage.py'),rid]);assert proc.returncode==0 and not proc.stderr,proc.stderr
 receipts.append(json.loads(proc.stdout))
save('render-receipts.json',{'utc':now(),'receipts':receipts,'actual_site_rendered':False})
proc,report=check(S,IDS,O,'target-stage-check-final');assert proc.returncode==0 and not proc.stderr and report['status']=='PASS',(proc.stderr,report)
for rid in IDS:
 c=CONFIG[rid];h=(S/'research'/c['slug']/'index.html').read_text();v=Visible(h)
 save('public-copy-'+rid+'.txt','\n\n'.join(' '.join(x.split()) for x in ''.join(v.parts).split('\n') if x.strip())+'\n')
 sections={sid:{'heading':unescape(re.search(r'<h2>(.*?)</h2>',seg,re.S).group(1)),'paragraphs':[unescape(x) for x in re.findall(r'<p>(.*?)</p>',seg,re.S)],'links':[{'label':unescape(re.sub('<[^>]+>','',text)),'href':unescape(href),'download':'download' in attr} for href,attr,text in re.findall(r'<a href="([^"]+)"([^>]*)>(.*?)</a>',seg,re.S)]} for sid,seg in re.findall(r'<section id="([^"]+)">(.*?)</section>',h,re.S)}
 save('public-sections-'+rid+'.json',sections)
 if rid=='23430906':
  expected=json.loads((R/'papers'/rid/'reviews/editorial/public-sections.json').read_text())
  for spec in expected['sections']:
   assert sections[spec['id']]['heading']==spec['heading']
   if 'paragraphs' in spec and spec['id'] not in ['paper','collaborate','cite']:assert sections[spec['id']]['paragraphs']==spec['paragraphs'],spec['id']
   if spec['id']=='paper':assert sections['paper']['paragraphs'][0]==spec['paragraphs'][0]
   if spec['id']=='collaborate':assert sections['collaborate']['paragraphs'][0]==spec['paragraphs'][0]
def ilist(h):return json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',h,re.S).group(1))['mainEntity']
oldindex=(LIVE/'research/index.html').read_text();newindex=(S/'research/index.html').read_text();old=ilist(oldindex);new=ilist(newindex)
oldlis=re.findall(r'<li>.*?</li>',oldindex,re.S);newlis=re.findall(r'<li>.*?</li>',newindex,re.S)
assert old['numberOfItems']==len(oldlis)==50 and new['numberOfItems']==len(newlis)==52
assert new['itemListElement'][:50]==old['itemListElement'] and newlis[:50]==oldlis
assert [x['url'] for x in new['itemListElement'][50:]]==[CONFIG[rid]['canonical_url'] for rid in IDS]
assert len({x['url'] for x in new['itemListElement']})==52
def urls(p):return [x.text for x in ET.fromstring(p.read_text()).iter() if x.tag.endswith('loc')]
oldurls=urls(LIVE/'research/sitemap.xml');newurls=urls(S/'research/sitemap.xml')
assert len(oldurls)==51 and newurls[:51]==oldurls and len(newurls)==len(set(newurls))==53
assert newurls[51:]==[CONFIG[rid]['canonical_url'] for rid in IDS]
assert all(sha(S/rel)==sha(LIVE/rel) for rel in ['research/research.css','robots.txt'])
save('index-sitemap-checks.json',{'utc':now(),'status':'PASS','old_visible_items_byte_identical':50,'old_structured_entries_exact_and_in_order':50,'new_entries':52,'old_sitemap_urls_exact_and_in_order':51,'new_sitemap_urls':53,'only_added_urls':[CONFIG[x]['canonical_url'] for x in IDS],'css_and_robots_byte_identical':True})
def helpers(path):
 nodes=[];env={'re':re,'unicodedata':unicodedata,'Path':Path}
 for n in ast.parse(path.read_text()).body:
  if isinstance(n,ast.FunctionDef):nodes.append(n)
  elif isinstance(n,ast.Assign) and all(isinstance(t,ast.Name) and t.id.isupper() for t in n.targets):
   try:ast.literal_eval(n.value)
   except (ValueError,TypeError):continue
   nodes.append(n)
 exec(compile(ast.Module(body=nodes,type_ignores=[]),'<private pure helpers>','exec'),env);return env
before=helpers(O/'inputs/final-content-check.py');after=helpers(O/'final-content-check.proposed.py');legacy={}
for rid,path in before['TEX_PATHS'].items():
 assert after['TEX_PATHS'][rid]==path
 source=(R/'papers'/rid/'sources'/path).read_text()
 if rid=='22089551':source=re.search(r'\\ifdefined\\japsubmission(.*?)\\else(.*?)\\fi',source,re.S).group(2)
 a=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',source,re.S).group(1)
 legacy[rid]=before['abstract_tokens'](a,rid)==after['abstract_tokens'](a,rid)
assert len(legacy)==49 and all(legacy.values()) and len(after['TEX_PATHS'])==51
save('legacy-dispatch-comparison.json',{'utc':now(),'status':'PASS','all_49_old_mappings_and_actual_source_abstract_dispatches':legacy,'new_mappings':{rid:after['TEX_PATHS'][rid] for rid in IDS},'total_mappings':51,'pilot_50th_old_page_still_unmapped':True})
# Before/after executable render comparisons, using current live index metadata.
comparison={}
for rid in ['23539283','23306332','22089807','23203100']:
 root=O/'versioned-comparison'/rid;root.mkdir(parents=True);outputs={}
 for label,source in [('original',O/'inputs/render_page.py'),('proposed',O/'render_page.proposed.py')]:
  target=root/label/'public';(target/'research').mkdir(parents=True)
  for rel in ['research/index.html','research/research.css','research/sitemap.xml','robots.txt']:shutil.copyfile(LIVE/rel,target/rel)
  script=root/(label+'.py');code=source.read_text().replace('ROOT = Path(__file__).resolve().parents[1]','ROOT = Path('+repr(str(R))+')').replace("SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')",'SITE = Path('+repr(str(target/'research'))+')');script.write_text(code)
  proc=run([PY,'-B',str(script),rid]);assert proc.returncode==0 and not proc.stderr,(rid,label,proc.stderr)
  outputs[label]={str(p.relative_to(target)):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(target.rglob('*')) if p.is_file()}
 assert outputs['original']==outputs['proposed'],rid
 comparison[rid]={'files_byte_identical':outputs['original']}
save('versioned-render-comparison.json',{'utc':now(),'status':'PASS','actual_private_render_comparisons':comparison,'actual_site_rendered':False})
with (O/'RESEARCH_LOG.md').open('a') as f:f.write(now()+' — 65%: Final private target checks pass; old50 index entries and old51 sitemap URLs preserved in order. All49 old source dispatches and four executable renderer comparisons are unchanged.\n')
negative=[]
def page_replace(old,new):
 def mutate(site,page,c):
  h=page.read_text();assert old in h,old;page.write_text(h.replace(old,new,1))
 return mutate
def alter(name,rid,mutate,expected):
 root=O/'negative'/name;root.mkdir(parents=True);site=root/'public';shutil.copytree(S,site)
 c=CONFIG[rid];mutate(site,site/'research'/c['slug']/'index.html',c)
 proc,r=check(site,[rid],root,'check');issues=r['issues'] if r else []
 assert proc.returncode!=0 and (rid+': '+expected in issues or r is None and proc.stderr),(name,expected,issues,proc.stderr)
 negative.append({'case':name,'record_id':rid,'rejected':True,'expected_issue':rid+': '+expected,'issues':issues,'exception_rejection':proc.stderr if r is None else None})
for rid in IDS:
 c=CONFIG[rid]
 for which in ['first','middle','final']:
  sentences=re.split(r'(?<=\.)\s+',c['abstract']);ix=0 if which=='first' else len(sentences)//2 if which=='middle' else -1;sentences.pop(ix)
  alter(rid+'-abstract-'+which,rid,page_replace('<p>'+escape(c['abstract'])+'</p>','<p>'+escape(' '.join(sentences))+'</p>'),'abstract')
 for name,old,new,expected in [
  ('wrong-citation-doi','name="citation_doi" content="'+c['doi']+'"','name="citation_doi" content="10.5281/zenodo.0"','citation_doi'),
  ('wrong-version','"version": "1.0"','"version": "2.0"','jsonld'),
  ('canonical-omitted','<link rel="canonical" href="'+c['canonical_url']+'">','','canonical'),
  ('wrong-visible-date','>14 October 2026</time>','>15 October 2026</time>','edition_chronology'),
  ('abstract-heading','<h2>Original abstract</h2>','<h2>Abstract</h2>','original_abstract_heading'),
  ('pdf-download-attribute','<a href="'+c['pdf_filename']+'" download>Download PDF</a>','<a href="'+c['pdf_filename']+'">Download PDF</a>','original_pdf_download_and_open'),
  ('original-zip-omitted','https://zenodo.org/records/'+rid+'/files/'+c['supplement_filename'],'https://zenodo.org/records/'+rid+'/files/omitted.zip','complete_supporting_material_links')]:
  alter(rid+'-'+name,rid,page_replace(old,new),expected)
 def drop_index(site,page,c):
  p=site/'research/index.html';p.write_text(p.read_text().replace('href="/research/'+c['slug']+'/"','href="/research/omitted/"'))
 alter(rid+'-index-omitted',rid,drop_index,'index_entry')
 def drop_sitemap(site,page,c):
  p=site/'research/sitemap.xml';p.write_text(p.read_text().replace('<loc>'+c['canonical_url']+'</loc>','<loc>https://aleckriebel.com/research/omitted/</loc>'))
 alter(rid+'-sitemap-omitted',rid,drop_sitemap,'sitemap')
 for key in ['pdf_filename','supplement_filename']:
  def corrupt(site,page,c,key=key):
   p=page.parent/c[key];p.write_bytes(p.read_bytes()+b'\nprivate alteration\n')
  alter(rid+'-corrupt-'+key,rid,corrupt,key)
for rid,name,old,new,expected in [
 ('23383961','some-maximizer','Every such maximizer','Some such maximizer','slit_every_maximizer_fixed_parameters'),
 ('23383961','arbitrary-epsilon','Set ε = 10⁻²⁴','Set ε > 0','slit_every_maximizer_fixed_parameters'),
 ('23383961','wrong-tangent','Increasing t points inward','Increasing t points outward','slit_actual_geometry_and_angle_mechanisms'),
 ('23430906','H-endpoints','Fix H ∈ (1/4,1)','Fix H ∈ [1/4,1]','gaussian_fixed_all_parameter_quantifiers'),
 ('23430906','linear-only','Every F ∈ L²(G_(T,n))','Every linear F ∈ L²(G_(T,n))','gaussian_fixed_all_parameter_quantifiers'),
 ('23430906','missing-terminal','including T, with n observations per component','excluding T, with n total observations','gaussian_fixed_all_parameter_quantifiers'),
 ('23430906','sharp-uniform-constant','No sharp constant','A sharp constant','gaussian_convention_and_scope_limits'),
 ('23430906','wrong-antisymmetric-factor','unhalved antisymmetric difference has twice','unhalved antisymmetric difference has the same','gaussian_convention_and_scope_limits')]:
 alter(rid+'-'+name,rid,page_replace(old,new),expected)
save('negative-controls.json',{'utc':now(),'status':'PASS','rejected_controls':len(negative),'cases':negative})

# Every authority control runs the complete checker, with copied byte overrides.
# Interception cannot write or change an original path, source, config or object.
authority=[]
def auth(name,rid,relative,transform,expected):
 root=O/'authority-negative'/name;root.mkdir(parents=True)
 source=R/relative if relative.startswith('verification/') else R/'papers'/rid/relative
 data=transform(source.read_bytes());owned=root/'mutated-input.bin';owned.write_bytes(data)
 control=root/'control.json';control.write_text(json.dumps({'path':str(source),'bytes_file':str(owned)}))
 proc,r=check(S,[rid],root,'check',control);issues=r['issues'] if r else []
 assert proc.returncode!=0 and (rid+': '+expected in issues or r is None and proc.stderr),(name,expected,issues,proc.stderr)
 authority.append({'case':name,'record_id':rid,'intercepted_source':str(source),'copied_mutant_sha256':sha(owned),'rejected':True,'expected_issue':rid+': '+expected,'issues':issues,'exception_rejection':proc.stderr if r is None else None,'original_mutated':False})
def mutate_json(fn):
 def transform(b):
  obj=json.loads(b);fn(obj);return json.dumps(obj,ensure_ascii=False).encode()
 return transform
for rid in IDS:
 c=CONFIG[rid];g=json.loads((R/'papers'/rid/'promotion.json').read_text());b=c['source_binding']
 auth(rid+'-source-tex-bytes',rid,b['source_tex_path'],lambda x:x+b'\n','exact_tex_path_and_bytes')
 auth(rid+'-source-receipt-bytes',rid,'sources/receipt.json',lambda x:x+b' ','receipt_metadata_and_assets')
 auth(rid+'-metadata-bytes',rid,'sources/record.json',lambda x:x+b' ','receipt_metadata_and_assets')
 auth(rid+'-root-authority-bytes',rid,g['root_clearance_file'],lambda x:x+b' ','exact_root_authority')
 auth(rid+'-editorial-authority-bytes',rid,'verification/root-editorial-'+rid+'-20261025.json',lambda x:x+b' ','exact_editorial_authority')
 for role,v in g['reviews'].items():
  auth(rid+'-report-'+role,rid,v['report'],lambda x:x+b' ','complete_custom_verdict_objects')
  auth(rid+'-verdict-'+role,rid,v['verdict_file'],lambda x:x+b' ','complete_custom_verdict_objects')
 auth(rid+'-rewritten-root-object',rid,'promotion.json',mutate_json(lambda x:x['root_clearance_record'].update(status='PASS_REWRITTEN')),'exact_root_authority')
 auth(rid+'-rewritten-scope-object',rid,'promotion.json',mutate_json(lambda x:x['reviews']['scope']['verdict'].update(status='PASS')),'complete_custom_verdict_objects')
 auth(rid+'-rewritten-root-disposition',rid,'promotion.json',mutate_json(lambda x:x['reviews']['scope'].update(root_disposition='PASS')),'complete_custom_verdict_objects')
 auth(rid+'-false-source-scope-quantifier',rid,'publication.json',mutate_json(lambda x:x['result'].__setitem__(0,x['result'][0].replace('Every','Some').replace('Fix H ∈ (1/4,1)','Fix H ∈ [1/4,1]'))),'exact_approved_config_bytes')
 for key in ['pdf_filename','supplement_filename']:
  auth(rid+'-original-source-'+key,rid,'sources/'+c[key],lambda x:x+b' ','receipt_metadata_and_assets')
 if rid=='23430906':
  auth(rid+'-raw-record-bytes',rid,b['record_raw_path'],lambda x:x+b' ','original_receipt_shape_preserved')
  auth(rid+'-raw-receipt-schema',rid,'sources/receipt.json',mutate_json(lambda x:x.update(record_sha256=x['record_raw_sha256'])),'original_receipt_shape_preserved')
save('authority-negative-controls.json',{'utc':now(),'status':'PASS','rejected_controls':len(authority),'mechanism':'Full checker executed with copied-byte Path read interception; no original mutations.','cases':authority})
with (O/'RESEARCH_LOG.md').open('a') as f:f.write(now()+' — 90%: '+str(len(negative))+' altered private stages and '+str(len(authority))+' copied-byte authority controls rejected by the complete target checker. Original inputs still read-only.\n')
save('stage-validation.json',{'utc':now(),'status':'PASS','completion_percent':95,'target_checks':{rid:{'passed':sum(v['checks'].values()),'total':len(v['checks'])} for rid,v in report['papers'].items()},'altered_stage_controls_rejected':len(negative),'authority_controls_rejected':len(authority),'old_source_dispatches_unchanged':len(legacy),'old_versioned_private_render_cases_byte_identical':len(comparison),'actual_render_live_browser_native_gates_passed':False})
print(json.dumps({'target':report['status'],'negative_controls':len(negative),'authority_controls':len(authority),'legacy_dispatches':len(legacy),'private_old_renderer_comparisons':len(comparison)}))
