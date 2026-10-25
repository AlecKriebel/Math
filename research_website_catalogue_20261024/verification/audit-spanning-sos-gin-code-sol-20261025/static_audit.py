"""Independent read-only frozen-stage content/scope audit. Writes only own receipt."""
import ast,json,re,hashlib,difflib,subprocess,datetime
from pathlib import Path
from html import unescape
from html.parser import HTMLParser
E=Path(__file__).resolve().parent;P=E.parents[1]
S=P/'verification/local-spanning-sos-gin-stage-sol-20261025'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bound(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
def need(ok,tag):
 if not ok:raise ValueError(tag)
mod=ast.parse((S/'spanning_sos_gin_source.py').read_text())
literals={n.targets[0].id:ast.literal_eval(n.value) for n in mod.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ['MATH','NORMALIZATIONS','SCHEMAS','PINS']}
def display(rid,s):
 def sub(m):return literals['MATH'][rid][m[1]]
 s=re.sub(r'\$([^$]+)\$',sub,s);need('\\' not in s and '$' not in s,'unknown_math');return s
class Body(HTMLParser):
 blocks={'p','section','h1','h2','li','ul','nav','header','footer','main','article','hr','br'}
 def __init__(self,h):super().__init__();self.inside=False;self.out=[];self.tags=[];self.feed(h)
 def handle_starttag(self,t,a):
  if t=='body':self.inside=True
  if self.inside:
   self.tags.append((t,dict(a)))
   if t in self.blocks:self.out.append('\n')
 def handle_endtag(self,t):
  if self.inside and t in self.blocks:self.out.append('\n')
  if t=='body':self.inside=False
 def handle_data(self,s):
  if self.inside:self.out.append(s)
rows=[];mathrows=[]
for rid in ['23181280','23442760','23395703']:
 paper=P/'papers'/rid;c=json.loads((paper/'publication.json').read_text())
 f=S/'public/research'/c['slug']/'index.html';h=f.read_text();d=Body(h)
 public=(S/f'public-copy-{rid}.txt').read_text();body=' '.join(''.join(d.out).split())
 need(body==' '.join(public.split()),rid+':whole_public_body')
 need(re.search(r'<h1><a href="([^\"]+)">(.*?)</a></h1>',h).groups()==('/research/'+c['slug']+'/',c['title']),rid+':actual_h1')
 schemas=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',h,re.S)[1]);article=next(x for x in schemas['@graph'] if x['@type']=='ScholarlyArticle')
 b=c['source_binding'];tex=(paper/b['source_tex_path']).read_text()
 abstract=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S)[1];norm=' '.join(abstract.replace('~',' ').split())
 for a,z in literals['NORMALIZATIONS'][rid].items():norm=norm.replace(a,z)
 need(norm==c['abstract']==article['abstract'],rid+':exact_source_abstract')
 expected={sid:[display(rid,x) for x in c[key]] for sid,key in [('plain-language','plain_language'),('result','result'),('proof','why_it_works'),('limits','limitations')]}
 for sid,vals in expected.items():
  seg=re.search('<section id="'+sid+'">(.*?)</section>',h,re.S)[1]
  ps=[unescape(x) for x in re.findall('<p>(.*?)</p>',seg,re.S)];need(ps==vals,rid+':paragraphs:'+sid)
 for key in ['plain_language','result','why_it_works','limitations']:
  for i,p in enumerate(c[key]):
   for token in re.findall(r'\$([^$]+)\$',p):mathrows.append({'record':rid,'field':key,'paragraph_index':i,'original':token,'display':literals['MATH'][rid][token]})
 if rid=='23395703':
  need(c['version'] is None and 'version' not in article and 'version =' not in (f.parent/'citation.bib').read_text(),'Gin_missing_version')
  url=next(x['url'] for x in c['related_resources'] if 'seven_plane_gin.tex' in x['url'])
  need('<a href="'+url+'">Zenodo original published TeX source</a>' in h,'Gin_actual_TeX_label_and_href')
 inventory=sorted(x.name for x in f.parent.iterdir() if x.is_file())
 need(inventory==sorted(['index.html','citation.bib',c['pdf_filename'],c['supplement_filename']]),rid+':four_files')
 need((f.parent/'citation.bib').read_bytes()==(paper/b['prepared_bibtex_path']).read_bytes(),rid+':exact_bib')
 assets=[]
 for name in [c['pdf_filename'],c['supplement_filename']]:
  a=paper/'sources'/name;z=f.parent/name;need(a.read_bytes()==z.read_bytes(),rid+':actual_asset_copy');assets.append(bound(z))
 info=subprocess.check_output(['pdfinfo',str(f.parent/c['pdf_filename'])],text=True)
 pages=int(re.search(r'^Pages:\s*(\d+)',info,re.M)[1]);need(pages==c['pdf_pages'],rid+':pages')
 rows.append({'record':rid,'title':c['title'],'whole_body_matches_actual_public_copy':True,'whole_original_abstract_matches_config_and_schema':True,'all_approved_body_paragraphs_match_literal_math_display':True,'actual_h1_title_and_url_exact':True,'source_version':c['version'],'schema_version_present':'version' in article,'PDF_pages':pages,'assets':assets,'local_output_names':inventory,'HTML':bound(f),'public_copy':bound(S/f'public-copy-{rid}.txt')})
scopes=[]
for kind,installed,prop,private in [('renderer',P/'scripts/render_page.py',S/'render_page.proposed.py',S/'render_page.stage.py'),('checker',P/'verification/final-content-check.py',S/'final-content-check.proposed.py',S/'final-content-check.stage.py')]:
 current=S/'inputs'/installed.name;need(current.read_bytes()==installed.read_bytes(),kind+':current_input_exact')
 diff=''.join(difflib.unified_diff(current.read_text().splitlines(keepends=True),prop.read_text().splitlines(keepends=True),fromfile='current',tofile='proposed'))
 need(diff==(S/('shared-'+kind+'.diff')).read_text(),kind+':declared_diff_exact')
 pdiff=''.join(difflib.unified_diff(prop.read_text().splitlines(keepends=True),private.read_text().splitlines(keepends=True),fromfile='proposed',tofile='private-only'))
 need(pdiff==(S/(kind+'-private-overrides.diff')).read_text(),kind+':private_diff_exact')
 scopes.append({'kind':kind,'installed':bound(installed),'proposed':bound(prop),'private_execution':bound(private),'declared_diff_exact':True,'private_only_roots_match_declared':True,'hunks':diff.count('@@')//2})
seal=json.loads((S/'FINAL_SEAL.json').read_text());mf=S/'FINAL_MANIFEST.json'
need(sha(mf)==seal['manifest_SHA256'],'stage_seal');m=json.loads(mf.read_text())
for x in m['files']:
 p=S/x['path'];need(p.stat().st_size==x['bytes'] and sha(p)==x['SHA256'],'stage_owned:'+x['path'])
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_EXACT_FROZEN_RENDERED_CONTENT_AND_CODE_SCOPE','stage_owned_bindings_rehashed':len(m['files']),'stage_manifest_sha256':sha(mf),'stage_seal':bound(S/'FINAL_SEAL.json'),'records':rows,'math_display_occurrences':len(mathrows),'math_map_distinct_entries':sum(len(v) for v in literals['MATH'].values()),'code_scope':scopes,'scientific_scope':'No new proof review; exact root/editorial approved content and code-consumer checks only.','UI_used':False,'renderer_executed':False,'old_suite_rerun':False}
(E/'STATIC_CONTENT_AND_CODE_SCOPE.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
(E/'MATH_DISPLAY_CHECK.json').write_text(json.dumps({'human_read_all66_map_pairs':True,'occurrences':mathrows},indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':result['status'],'stage_owned':len(m['files']),'math_entries':result['math_map_distinct_entries'],'math_occurrences':len(mathrows),'records':[(r['record'],r['PDF_pages']) for r in rows]},indent=2))
