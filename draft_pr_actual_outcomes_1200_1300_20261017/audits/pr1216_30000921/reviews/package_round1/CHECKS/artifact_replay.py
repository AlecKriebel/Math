from pathlib import Path, PurePosixPath
import datetime, hashlib, json, os, shutil, subprocess, sys, zipfile
HERE=Path(__file__).resolve().parent
REVIEW=HERE.parent
PUB=REVIEW.parents[1]/'publication'
TEMP=REVIEW/'temp'
EXTRACT=TEMP/'fresh_extract'
def binding(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def need(x,m):
 if not x:raise RuntimeError(m)
if EXTRACT.exists():shutil.rmtree(EXTRACT)
EXTRACT.mkdir(parents=True)
receipt=json.loads((PUB/'BUILD_RECEIPT.json').read_text())
checks={}
for k in ['pdf','verification_zip']:
 item=receipt[k];actual=binding(PUB/item['path']);need(all(actual[f]==item[f] for f in actual),'artifact mismatch '+k);checks[k]=actual
checks['manuscript']=binding(PUB/'manuscript/main.tex');need(checks['manuscript']['sha256']==receipt['manuscript_source_sha256'],'source mismatch')
with zipfile.ZipFile(PUB/receipt['verification_zip']['path']) as archive:
 names=archive.namelist();need(len(names)==len(set(names))==104,'member count/duplicate')
 for i in archive.infolist():
  p=PurePosixPath(i.filename);need(not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename,'unsafe member')
  need(i.external_attr>>16==0o644,'unexpected mode')
 archive.extractall(EXTRACT)
need(binding(EXTRACT/'MANIFEST.json')['sha256']==receipt['manifest_sha256'],'root manifest hash')
need((EXTRACT/'manuscript/main.tex').read_bytes()==(PUB/'manuscript/main.tex').read_bytes(),'zip source mismatch')
manifest=json.loads((EXTRACT/'MANIFEST.json').read_text())
for e in manifest['files']:
 need(binding(EXTRACT/e['path'])=={'bytes':e['bytes'],'sha256':e['sha256']},'independent member hash '+e['path'])
for p in EXTRACT.rglob('*'):
 if p.is_file():need(p.read_bytes()==(PUB/'verification'/p.relative_to(EXTRACT)).read_bytes(),'staged archive mismatch '+str(p))
checks['manifest_members']=len(manifest['files']);checks['zip_members']=len(names)
checks['archive_equals_staging']=True
# All explicitly declared nested manifests, including the cross-freeze excluded by verify.py's special loops.
nested=[]
for p in EXTRACT.rglob('MANIFEST.json'):
 m=json.loads(p.read_text());entries=m.get('entries',m.get('files',[]));n=0
 for e in entries:
  if isinstance(e,str):continue
  rel=e.get('file',e.get('path'))
  if not rel or not (p.parent/rel).exists():continue
  actual=binding(p.parent/rel);expected={'bytes':e.get('bytes',e.get('size')),'sha256':e.get('sha256')}
  need(actual==expected,'nested manifest '+str(p)+' '+rel);n+=1
 nested.append({'manifest':p.relative_to(EXTRACT).as_posix(),'checked_entries':n})
checks['nested_manifests']=nested
modes=[]
env=dict(os.environ,TMPDIR=str(TEMP))
for flags in [[],['-O'],['-OO']]:
 run=subprocess.run([sys.executable,'-B',*flags,str(EXTRACT/'verify.py')],text=True,capture_output=True,env=env)
 need(run.returncode==0,'verify failed '+run.stderr)
 data=json.loads(run.stdout);need(data==receipt['verification_run'],'build replay mismatch')
 tag='normal' if not flags else flags[0][1:]
 (HERE/('verify_'+tag+'.json')).write_text(run.stdout)
 modes.append({'flags':flags,'returncode':run.returncode,'result_matches_build':True})
checks['replay_modes']=modes
checks['compile_receipt']=json.loads((PUB/'COMPILE_RECEIPT.json').read_text())
need(checks['compile_receipt']['source_sha256']==checks['manuscript']['sha256'],'compile source mismatch')
need(checks['compile_receipt']['pdf_sha256']==checks['pdf']['sha256'],'compile pdf mismatch')
checks['output_pdf_same']=binding(PUB/'output/pdf/main.pdf')==checks['pdf'];need(checks['output_pdf_same'],'output PDF differs')
checks['at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(HERE/'artifact_replay.json').write_text(json.dumps(checks,indent=2)+'\n')
(REVIEW/'RESEARCH_LOG.md').write_text('# Independent whole-package review log\n\n- '+checks['at_utc']+' — 40%: bound supplied PDF/ZIP/TeX; fresh ZIP extraction matched all staged members; independently checked nested manifests; full verify.py passed under normal, -O, and -OO Python with outputs equal to build receipt. Main annular and original fixed-p proofs reviewed analytically; primary-source and safeguard review continue. No publication input was altered and no external mutation was made.\n')
print(json.dumps(checks,indent=2))
