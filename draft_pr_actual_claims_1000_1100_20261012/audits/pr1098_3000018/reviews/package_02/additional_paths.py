"""Additional separate-input/output faults on unchanged scripts, real external fixture."""
from pathlib import Path
import os,sys,json,hashlib,subprocess,uuid,zipfile,shutil
R=Path(__file__).resolve().parent;A=R.parents[1];C=A/'preprint_v1_0';T=Path('/private/tmp')/('pr1098-whole02-'+str(uuid.uuid4()));T.mkdir();rows=[]
def need(x,m):
 if not x:raise ValueError(m)
def sh(b):return hashlib.sha256(b).hexdigest()
def save(n,x):(R/n).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
def run(cmd):
 p=subprocess.run(list(map(str,cmd)),capture_output=True,text=True);rows.append({'argv':list(map(str,cmd)),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr});need(p.returncode!=0,'fault accepted')
try:
 K=T/'kit';K.mkdir()
 with zipfile.ZipFile(C/'pr1098_support_v1_0.zip') as z:z.extractall(K)
 for n in ('paper.pdf','pr1098_support_v1_0.zip'):shutil.copyfile(C/n,K/n)
 for opt in (False,True):
  cmd=[sys.executable]+(['-O'] if opt else [])+['-B']
  for writer,flag in [('rebuild_archive.py','--output'),('build_pdf.py','--out-dir')]:
   original_alias=Path(str(A).upper());need(original_alias.exists() and os.path.samefile(original_alias,A),'actual original case alias')
   for dest in [original_alias/'whole02-must-not-create-alias',T/'no-parent'/'new']:
    run(cmd+[K/'code'/writer,flag,dest]);need(not dest.exists(),'output created')
   # Independent well-formed external output plus hardlinked TeX input.
   p=K/'paper.tex';q=T/'tex-hardlink';os.link(p,q);dest=T/('new-source-'+writer+str(opt));run(cmd+[K/'code'/writer,flag,dest]);need(not dest.exists(),'hardlinked input output');q.unlink()
   # Symlinked input directory ancestor is rejected without creating output.
   p=K/'publication';q=T/'real-publication';p.rename(q);p.symlink_to(q,target_is_directory=True);dest=T/('new-dirlink-'+writer+str(opt));run(cmd+[K/'code'/writer,flag,dest]);need(not dest.exists(),'input ancestor output');p.unlink();q.rename(p)
  for name,mut in [('metadata.json',lambda b:json.dumps({**json.loads(b),'creators':[]} ).encode()),('publication/zenodo-deposit.json',lambda b:json.dumps({**json.loads(b),'files':[{'path':'../paper.pdf','name':'paper.pdf'}]}).encode()),('paper.pdf',lambda b:b+b'changed'),('ARTIFACT_BINDINGS.json',lambda b:json.dumps({'paper.pdf':{'bytes':0,'sha256':'0'*64}}).encode())]:
   p=K/name;b=p.read_bytes();p.write_bytes(mut(b));run(cmd+[K/'code/verify_kit.py']);p.write_bytes(b)
 save('ADDITIONAL_ACTUAL_PATHS.json',{'status':'PASS','runtime_ROOT_or_ORIGINAL_modified':False,'commands':rows,'command_count':len(rows),'scope':'Actual unchanged scripts, own external fixture; each protected alias/no-parent/well-formed-output-bad-input rejected with absent destination.'})
finally:
 pins=[{'path':str(p.relative_to(T)),'bytes':p.stat().st_size,'sha256':sh(p.read_bytes())} for p in sorted(T.rglob('*')) if p.is_file() and not p.is_symlink()]
 save('ADDITIONAL_CLEANUP.json',{'absolute_path':str(T),'before_removal':pins,'only_own_unsealed_derivatives':True,'removed':False});shutil.rmtree(T);save('ADDITIONAL_CLEANUP.json',{'absolute_path':str(T),'before_removal':pins,'only_own_unsealed_derivatives':True,'removed':True})
