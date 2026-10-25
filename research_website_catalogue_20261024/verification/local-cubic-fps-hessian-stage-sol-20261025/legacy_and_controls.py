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

# Complete current/proposed checker executions on every configured old record.
tree=ast.parse((O/'inputs/final-content-check.py').read_text())
oldmaps=ast.literal_eval(next(x.value for x in tree.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='TEX_PATHS' for t in x.targets)))
assert len(oldmaps)==56
source=(O/'inputs/final-content-check.py').read_text()
original_stage=source.replace("sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))",'sys.path.insert(0, '+repr(str(R/'scripts'))+')').replace('R=Path(__file__).resolve().parents[1]','R=Path('+repr(str(R))+')')
save('final-content-check.original.stage.py',original_stage)
legacy={}
for label,path,site in [('current',O/'final-content-check.original.stage.py',LIVE),('proposed',O/'final-content-check.stage.py',S)]:
 stem='legacy-full-'+label
 if not (label=='current' and (O/(stem+'.json')).exists() and json.loads((O/(stem+'.json')).read_text())['status']=='PASS'):
  proc=run([PY,'-B',str(O/'stage_reader.py'),str(path),*oldmaps,'--site',str(site),'--output-dir',str(O),'--output-stem',stem])
  save(stem+'.stderr.txt',proc.stderr)
  assert proc.returncode==0 and not proc.stderr,(label,proc.stderr[:3000])
 report=json.loads((O/(stem+'.json')).read_text());assert report['status']=='PASS' and not report['issues'],(label,report['issues'])
 legacy[label]={rid:data['checks'] for rid,data in report['papers'].items()}
assert legacy['current']==legacy['proposed']
save('legacy-full-checker-compatibility.json',{'utc':now(),'status':'PASS','old_configured_records':56,'all_current_proposed_check_names_and_booleans_identical':True,'all_old_checks_passed':sum(len(x) for x in legacy['current'].values()),'old_asset_tree_copies':0,'old_site_resolution':'Missing private old site paths resolve read-only to original live-site bytes through stage_reader; no alias files or symlinks.'})

# Changed-read variants only; one pristine real stage and no fixture trees.
cases=[]
def add(name,rid,path,data):cases.append({'case':name,'record_id':rid,'overrides':{str(path.resolve()):base64.b64encode(data).decode()}})
def page(name,rid,old,new):
 path=S/'research'/CONFIG[rid]['slug']/'index.html';data=path.read_text();assert old in data,(name,old);add(name,rid,path,data.replace(old,new,1).encode())
for rid in IDS:
 c=CONFIG[rid];p=R/'papers'/rid
 for which in ['first','middle','final']:
  sentences=re.split(r'(?<=\.)\s+',c['abstract']);sentences.pop(0 if which=='first' else len(sentences)//2 if which=='middle' else -1)
  page(rid+'-abstract-'+which,rid,'<p>'+escape(c['abstract'])+'</p>','<p>'+escape(' '.join(sentences))+'</p>')
 page(rid+'-wrong-citation-doi',rid,'name="citation_doi" content="'+c['doi']+'"','name="citation_doi" content="10.5281/zenodo.0"')
 for key in ['pdf_filename','supplement_filename']:
  path=S/'research'/c['slug']/c[key];add(rid+'-damaged-public-'+key,rid,path,path.read_bytes()+b'\nchanged-read control\n')
 path=p/c['source_binding']['source_tex_path'];add(rid+'-source-TeX-changed',rid,path,path.read_bytes()+b'\n')
 path=R/f'verification/root-clearance-{rid}-20261025.json';add(rid+'-root-authority-byte-changed',rid,path,path.read_bytes()+b' ')
 path=p/'promotion.json';data=json.loads(path.read_text());data['reviews']['scope']['verdict']['invented_editorial_PASS']=True;add(rid+'-original-custom-verdict-added-field',rid,path,json.dumps(data).encode())
 path=p/'sources/receipt.json';data=json.loads(path.read_text());data['files'][0]['bytes']+=1;add(rid+'-receipt-file-size-changed',rid,path,json.dumps(data).encode())
 page(rid+'-canonical-removed',rid,'<link rel="canonical" href="'+c['canonical_url']+'">','')
 path=S/'research/index.html';add(rid+'-index-entry-omitted',rid,path,path.read_text().replace('href="/research/'+c['slug']+'/"','href="/research/omitted/"').encode())
 path=S/'research/sitemap.xml';add(rid+'-sitemap-entry-omitted',rid,path,path.read_text().replace('<loc>'+c['canonical_url']+'</loc>','<loc>https://aleckriebel.com/research/omitted/</loc>').encode())
 page(rid+'-license-schema-changed',rid,'"license": "https://creativecommons.org/licenses/by/4.0/"','"license": "https://example.org/wrong-license"')
 path=S/'research'/c['slug']/'citation.bib';add(rid+'-prepared-bib-doi-changed',rid,path,path.read_text().replace(c['doi'],'10.5281/zenodo.0',1).encode())
 page(rid+'-local-PDF-download-removed',rid,'<a href="'+c['pdf_filename']+'" download>Download PDF</a>','')
rid='23204952'
page('cubic-external-proof-limits-hidden',rid,'complete proofs are not freshly recertified','complete proofs have been freshly certified')
page('cubic-all-covers-weakened',rid,'every irreducible normal finite quasi-étale cover','one selected finite quasi-étale cover')
page('cubic-prior-comparison-cleared-as-new',rid,'stronger result of Kong, Shen, Zhao and Zhao','newly solved complex comparison')
rid='22983138'
page('fps-wrong-regular-equality',rid,'need not be regular','must be regular')
page('fps-centroid-term-removed',rid,escape('C₂(K)≥[r²+(n+1)‖g_K‖₂²]/(n+2)'),escape('C₂(K)≥r²/(n+2)'))
page('fps-checksum-original-link-removed',rid,'href="https://zenodo.org/records/22983138/files/SHA256SUMS"','href="https://example.org/omitted"')
path=R/'papers/22983138/sources/SHA256SUMS';add('fps-original-checksum-text-changed',rid,path,path.read_bytes()+b'\n')
rid='23409904'
page('hessian-properness-removed',rid,'proper smooth embedding f:M→U','local immersion f:M→U')
page('hessian-ordered-pair-reversed',rid,'exactly ∇ and ∇*, in that order','exactly ∇* and ∇, in that order')
page('hessian-one-torsion-omitted',rid,'both prescribed torsions vanish','one prescribed torsion vanishes')
path=R/'papers/23409904/sources/receipt.json';data=json.loads(path.read_text());data['files'].pop();add('hessian-endpoint-receipt-dropped',rid,path,json.dumps(data).encode())
assert len(cases)==59,len(cases)
save('controls/cases.json',cases);out=[]
for ix,case in enumerate(cases):
 proc,report=check([case['record_id']],'control-'+str(ix).zfill(2),ix)
 assert proc.returncode!=0,(case['case'],report)
 assert report is not None and report['issues'] or 'AssertionError' in proc.stderr or 'ValueError' in proc.stderr,(case['case'],proc.stderr[:1000])
 out.append(dict(case=case['case'],record_id=case['record_id'],rejected=True,issues=report['issues'] if report else [],exception_rejection=proc.stderr[-2500:] if report is None else None,overridden_paths=list(case['overrides']),changed_bytes=sum(len(base64.b64decode(v)) for v in case['overrides'].values()),fixture_copies=0,original_files_mutated=False))
save('negative-controls.json',dict(utc=now(),status='PASS',controls_rejected=len(out),fixture_stage_copies=0,mechanism='Complete proposed checker reads one pristine actual stage; each case intercepts only explicit changed Path-read bytes. The entire changed bytes are retained in controls/cases.json.',cases=out))
with (O/'RESEARCH_LOG.md').open('a') as f:f.write(now()+' — 90%: Complete old56 current/proposed checker outputs agree with every old check passing; 59 changed-read controls reject on the one pristine stage. No old asset or fixture trees copied.\n')
print(json.dumps({'full_old_checker_records':56,'full_old_checks':sum(len(x) for x in legacy['current'].values()),'negative_controls_rejected':len(out)}))
