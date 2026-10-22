from pathlib import Path,PurePosixPath
import os,sys,zipfile,hashlib,json,subprocess,stat,datetime,shutil
F=Path(__file__).resolve().parent;A=F.parent.parent;P=A/'publication';scratch=F/'_local';root=scratch/'actual_archive'
def need(x,m):
 if not x:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
anchors={'manifest':'6a3164a73be08b9c20c3b2fab5bdbcf1a4f1eb51ee1d8f7ce80184f41b8c6a22','context':'6f66797c62c2b1d0c5d3e681eadf48bc80c839f7145961a3197174db1f0dd69c','snapshot':'da2152816bbcd548e4db411ab57992c121009d935e2de59b3f6de93ae304a1d6'}
need(not root.exists(),'fixture already exists');root.mkdir()
zp=P/'Semibrace_Existence_Classification_Verification_v1.0.zip';pdf=P/'Semibrace_Existence_Classification_Note_v1.0.pdf'
need(len(zp.read_bytes())==453194 and sha(zp.read_bytes())=='5ac206025bc365f114b28da1b5c786653df30472b1cd40e4774d62b39b3a063e','zip external pin')
need(len(pdf.read_bytes())==51131 and sha(pdf.read_bytes())=='2665fbe257cf1b4cc9ad8f4d8057bb95ad3c65b1368f839c96f2bb2216323e42','PDF external pin')
with zipfile.ZipFile(zp) as z:
 names=z.namelist();need(len(names)==164 and len(set(names))==164 and len(set(n.casefold() for n in names))==164,'unique exact164 archive names')
 need(z.testzip() is None,'CRC')
 for i in z.infolist():
  n=i.filename;q=PurePosixPath(n)
  need(not q.is_absolute() and '..' not in q.parts and str(q)==n and '\\' not in n and not i.is_dir(),'safe archive member '+n)
  need(not stat.S_ISLNK(i.external_attr>>16),'ZIP symlink '+n)
  need(not {'_local','__pycache__','scratch_private'}&set(q.parts) and not n.endswith(('.pdf','.png','.jpg','.pyc','.zip')),'private/binary source member '+n)
  b=z.read(n);need((P/'verification'/n).read_bytes()==b,'archive versus prepared portable bytes '+n)
  out=root/n;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b)
need((root/'verify.py').read_bytes()==(P/'verification/verify.py').read_bytes(),'deployed verifier bytes')
c=json.loads((root/'provenance/CURRENT_PR1283_CONTEXT.json').read_text())
need(len(c['authored_freezes'])==12 and len(c['portable_files'])==138,'12families138 portable')
for prefix,source in [('original_submitted','submitted'),('current_edition','current_edition')]:
 need(len(list((root/prefix).iterdir()))==8,'8edition')
 for p in (root/prefix).iterdir():need(p.read_bytes()==(A/source/p.name).read_bytes(),'exact edition '+p.name)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(scratch));env.pop('PYTHONOPTIMIZE',None)
results=[]
def run(mode,label,changes=None):
 aa=dict(anchors);aa.update(changes or {});cmd=[sys.executable,'-B',*mode,str(root/'verify.py'),*[v for k,h in aa.items() for v in ['--expected-'+k+'-sha256',h]]]
 r=subprocess.run(cmd,env=env,cwd=scratch,capture_output=True,text=True,timeout=180)
 results.append({'label':label,'mode':mode,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 return r
for mode in [[],['-O'],['-OO']]:
 r=run(mode,'actual_archive_full_verifier');need(r.returncode==0,r.stderr);d=json.loads(r.stdout);need(d['authenticated_members']==163 and len(d['nested_manifests'])==12 and len(d['finite_diagnostic_replays'])==5,'actual verifier counts')
 for k in anchors:need(run(mode,'wrong_outside_'+k,{k:'0'*64}).returncode!=0,'accepted wrong anchor')
 # Bypass a changed outer binding with an explicit new outside root anchor;
 # independent inner context/manifest must still protect its exact member.
 target=root/'current_edition/PROOF_CLASSIFICATION.md';orig=target.read_bytes();m=root/'MANIFEST.json';mb=m.read_bytes();obj=json.loads(mb)
 target.write_bytes(orig+b'\nUNDECLARED ADVERSARIAL CHANGE\n')
 for e in obj['files']:
  if e['path']=='current_edition/PROOF_CLASSIFICATION.md':e.update(bytes=target.stat().st_size,sha256=sha(target.read_bytes()))
 m.write_text(json.dumps(obj,indent=2)+'\n')
 need(run(mode,'coupled_outer_and_current_source_corruption',{'manifest':sha(m.read_bytes())}).returncode!=0,'accepted coupled source corruption')
 target.write_bytes(orig);m.write_bytes(mb)
 extra=root/'UNREGISTERED.txt';extra.write_text('extra')
 need(run(mode,'unlisted_extra_member').returncode!=0,'accepted extra');extra.unlink()
 # Direct false predicate control proves optimized execution retains checks.
 r=subprocess.run([sys.executable,'-B',*mode,'-c',"import runpy; runpy.run_path("+repr(str(root/'verify.py'))+")[\"need\"](False,\"ROUND2_FALSE_PREDICATE\")"],env=env,cwd=scratch,capture_output=True,text=True)
 results.append({'label':'explicit_false_predicate','mode':mode,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr});need(r.returncode!=0 and 'ROUND2_FALSE_PREDICATE' in r.stderr,'false predicate escaped')
receipt={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_zip_sha256':sha(zp.read_bytes()),'actual_pdf_sha256':sha(pdf.read_bytes()),'archive_members':164,'uncompressed_bytes':sum(i.file_size for i in zipfile.ZipFile(zp).infolist()),'original8_current8_exact':True,'registered_families':12,'portable_files':138,'outside_anchors':anchors,'private_raw_bodies_cache_images_excluded':True,'results':results,'status':'PASS','limit':'Portable integrity and finite diagnostics only. No compilation replay or theorem/priority inference from PASS.'}
(F/'ARCHIVE_REVIEW.json').write_text(json.dumps(receipt,indent=2)+'\n');shutil.rmtree(root);print(json.dumps({k:v for k,v in receipt.items() if k!='results'},indent=2))
