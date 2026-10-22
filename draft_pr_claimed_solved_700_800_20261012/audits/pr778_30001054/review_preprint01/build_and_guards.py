from pathlib import Path
import subprocess,sys,json,hashlib,os,shutil,tempfile,datetime
B=Path(__file__).resolve().parent; S=B/'extracted'; P=B.parent/'preprint'; PDF=P/'output/pdf/paper.pdf'
T=B/'tmp';T.mkdir(exist_ok=True)
env=os.environ.copy();env['TMPDIR']=str(T)
for k in ['PYTHONOPTIMIZE','PYTHONPATH','PYTHONHOME']:env.pop(k,None)
def identity(p):
 x=p.read_bytes();return {'bytes':len(x),'sha256':hashlib.sha256(x).hexdigest()}
def snap(root):return {p.relative_to(root).as_posix():identity(p) for p in root.rglob('*') if p.is_file()}
def need(x,m):
 if not x:raise RuntimeError(m)
before=snap(S);pdfbefore=identity(PDF);rows=[]
for opt in [False,True]:
 pre=[sys.executable,'-E','-s','-B']+(['-O'] if opt else [])
 dest=B/('rebuilt-O' if opt else 'rebuilt-normal')
 cmd=pre+[str(S/'build_package.py'),'--pdf',str(PDF),'--output-dir',str(dest)]
 r=subprocess.run(cmd,cwd='/',env=env,capture_output=True,timeout=120)
 need(r.returncode==0,r.stderr.decode())
 expected=json.loads((B.parent/'PREPRINT_REVIEW_INPUTS_01.json').read_text())['six']
 need(all(identity(dest/n)==v for n,v in expected.items()),'six mismatch')
 rows.append({'mode':'O' if opt else 'normal','case':'relocated rebuild','PASS':True,'six_identical':True})
 # Each output control uses owned fixture only. Batch validation must preserve source/PDF.
 for case in ['inside_source','symlink_output_ancestor','hardlink_external_pdf','nonregular_fifo','symlink_file']:
  with tempfile.TemporaryDirectory(dir=T,prefix='builder-') as tmp:
   root=Path(tmp); target=root/'out'; target.mkdir()
   supplied=root/'input.pdf';supplied.write_bytes(PDF.read_bytes())
   given=supplied
   if case=='inside_source':target=S/'forbidden-build-output'
   elif case=='symlink_output_ancestor':
    actual=root/'actual';actual.mkdir();link=root/'alias';link.symlink_to(actual,target_is_directory=True);target=link/'out'
   elif case=='hardlink_external_pdf':
    (target/'output/pdf').mkdir(parents=True);os.link(supplied,target/'output/pdf/paper.pdf')
   elif case=='nonregular_fifo':os.mkfifo(target/'zenodo-metadata.json')
   elif case=='symlink_file':(target/'paper.tex').symlink_to(supplied)
   r=subprocess.run(pre+[str(S/'build_package.py'),'--pdf',str(given),'--output-dir',str(target)],cwd='/',env=env,capture_output=True,timeout=60)
   need(r.returncode!=0,'guard accepted '+case)
   need(supplied.read_bytes()==PDF.read_bytes(),'input PDF mutated '+case)
   need(snap(S)==before,'source mutated '+case)
   if case=='inside_source':need(not target.exists(),'inside output created')
   rows.append({'mode':'O' if opt else 'normal','case':case,'PASS':True,'returncode':r.returncode,'rejection':r.stderr.decode().strip().splitlines()[-1]})
need(snap(S)==before and identity(PDF)==pdfbefore,'input mutation')
# Physical top verifier mutations and mtime-only relocation positive control.
for opt in [False,True]:
 pre=[sys.executable,'-E','-s','-B']+(['-O'] if opt else [])
 for case in ['relocated_mtime_changed','extra_hidden','missing','altered','symlink','fifo','empty_directory']:
  with tempfile.TemporaryDirectory(dir=T,prefix='source-') as tmp:
   move=Path(tmp)/'relocated package with spaces';shutil.copytree(S,move)
   for p in move.rglob('*'):os.utime(p,(946684800,946684800))
   path=move/'paper.tex'
   if case=='extra_hidden':(move/'.hidden').write_bytes(b'extra')
   elif case=='missing':path.unlink()
   elif case=='altered':path.write_bytes(path.read_bytes()+b'\n%extra')
   elif case=='symlink':path.unlink();path.symlink_to(S/'paper.tex')
   elif case=='fifo':os.mkfifo(move/'special')
   elif case=='empty_directory':(move/'empty').mkdir()
   r=subprocess.run(pre+[str(move/'verify_bundle.py'),'--integrity-only','--pdf',str(PDF)],cwd='/',env=env,capture_output=True,timeout=60)
   need((r.returncode==0)==(case=='relocated_mtime_changed'),'wrong source guard '+case)
   rows.append({'mode':'O' if opt else 'normal','case':case,'PASS':True,'returncode':r.returncode})
need(snap(S)==before,'input mutation')
need(list(T.iterdir())==[],'scratch not cleaned')
(B/'BUILD_GUARD_RESULTS.json').write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','rows':rows,'closed_source_before_after_identical':True,'supplied_pdf_before_after_identical':True,'temporary_copies_removed':True},indent=2)+'\n')
print('builder same6 normal/O +10 output rejects +12 physical rejects +2mtime positives PASS')
