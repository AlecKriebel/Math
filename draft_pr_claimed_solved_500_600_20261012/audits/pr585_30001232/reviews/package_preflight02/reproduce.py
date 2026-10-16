import sys
sys.dont_write_bytecode=True
import os,pathlib,hashlib,json,zipfile,subprocess,shutil,time
R=pathlib.Path(__file__).resolve().parent; A=R.parent.parent; P=A/'publication'; C=R/'.cache'; E=C/'extracted'
for d in [C/'tmp',C/'tex',C/'renders']:d.mkdir(parents=True,exist_ok=True)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(C/'tmp'))
PYTHON=A/'root_reproduction/.cache/venv/bin/python'; SB=['/usr/bin/sandbox-exec','-p','(version 1) (allow default) (deny network*)']
sha=lambda b:hashlib.sha256(b).hexdigest()
def run(label,cmd,cwd):
 t=time.time();p=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,text=True)
 (R/(label+'.stdout.txt')).write_text(p.stdout);(R/(label+'.stderr.txt')).write_text(p.stderr)
 assert p.returncode==0,(label,p.stdout,p.stderr)
 return {'command':cmd,'returncode':p.returncode,'seconds':time.time()-t,'stdout':p.stdout,'stderr':p.stderr}
freeze={f.name:{'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in P.iterdir() if f.is_file()}
with zipfile.ZipFile(P/'verification_package.zip') as z:
 names=z.namelist();assert len(names)==len(set(names))==102
 E.mkdir();prefix='seshadri_counterexample_verification/'
 for n in names:
  rel=n.removeprefix(prefix);assert n.startswith(prefix) and not pathlib.PurePosixPath(rel).is_absolute() and '..' not in pathlib.PurePosixPath(rel).parts
  f=E/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(z.read(n))
manifest=json.loads((E/'MANIFEST.json').read_bytes());assert len(manifest['files'])==101
blobs=[]
for rec in json.loads((E/'ORIGINAL_SNAPSHOT.json').read_bytes())['files']:
 data=subprocess.check_output(['git','show','0a94b2a7e8d682af7d51a3fba7fe8df4a36f6f27:'+rec['path']],cwd=A)
 actual=(E/'original'/rec['path']).read_bytes();assert actual==data and sha(data)==rec['sha256'] and len(data)==rec['size']
 blobs.append({'path':rec['path'],'sha256':sha(data),'bytes':len(data),'git_blob_equal':True})
probe=run('NETWORK_PROBE',SB+[str(PYTHON),'-B','-c',"import socket,json,sympy,mpmath; s=socket.socket();\ntry: s.connect(('1.1.1.1',443)); d={'denied':False}\nexcept OSError as e: d={'denied':True,'errno':e.errno}\nprint(json.dumps(dict(d,sympy=sympy.__version__,mpmath=mpmath.__version__)))"],E)
assert json.loads(probe['stdout'])=={'denied':True,'errno':1,'sympy':'1.14.0','mpmath':'1.3.0'}
replay=run('NINE_JOB_REPLAY',SB+[str(PYTHON),'-B',str(E/'run_all.py')],E)
rows=[json.loads(x) for x in replay['stdout'].splitlines()];assert len(rows)==10 and rows[-1]['replayed_jobs']==9
# Install the unchanged flat payload into the producer's documented repository layout.
D=C/'unrelated_cache/scratch/standalone_audit'; Q=D/'publication';Q.mkdir(parents=True)
flat={'seshadri_counterexample.tex','README.md','CORRECTIONS.md','BUILD.json','PDF_QA.json','requirements.txt','integrity.py','run_all.py','make_package.py','JOBS.json','SEALS.json'}
for f in E.rglob('*'):
 if not f.is_file():continue
 n=f.relative_to(E); dest=Q/n if n.as_posix() in flat else Q/'zenodo-deposit.json' if n.as_posix()=='metadata.json' else D/n
 if n.as_posix()=='MANIFEST.json':continue
 dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(f.read_bytes())
(Q/'seshadri_counterexample.pdf').write_bytes((P/'seshadri_counterexample.pdf').read_bytes())
reb=run('ZIP_REBUILD',SB+[str(PYTHON),'-B',str(Q/'make_package.py')],Q)
assert (Q/'verification_package.zip').read_bytes()==(P/'verification_package.zip').read_bytes()
tex=C/'tex';(tex/'seshadri_counterexample.tex').write_bytes((P/'seshadri_counterexample.tex').read_bytes());env['SOURCE_DATE_EPOCH']='1792022400'
pdf=run('PDF_REBUILD',SB+['/opt/homebrew/bin/tectonic','--only-cached','seshadri_counterexample.tex'],tex)
assert (tex/'seshadri_counterexample.pdf').read_bytes()==(P/'seshadri_counterexample.pdf').read_bytes()
run('PDFINFO',['/opt/homebrew/bin/pdfinfo',str(tex/'seshadri_counterexample.pdf')],tex)
run('PDF_RENDER',['/opt/homebrew/bin/pdftoppm','-r','115','-png',str(tex/'seshadri_counterexample.pdf'),str(C/'renders/page')],tex)
assert freeze=={f.name:{'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in P.iterdir() if f.is_file()}
result={'status':'PASS','freeze':freeze,'archive_members':len(names),'original_git_blobs':blobs,'probe':probe,'replay':replay,'zip_rebuild':reb,'pdf_rebuild':pdf,'all_publication_files_unchanged':True,'env_beside_extraction':str(PYTHON),'write_root':str(R)}
(R/'REPRODUCTION_LEDGER.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','nine_jobs':rows,'zip_byte_identical':True,'pdf_byte_identical':True,'git_blobs':len(blobs)},indent=2))
