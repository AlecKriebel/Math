"""Physical package controls in owned scratch copies; never modifies reviewed inputs."""
from pathlib import Path
import argparse,hashlib,io,json,os,shutil,subprocess,sys,tempfile,zipfile,time
PIN='51b58386f8733c0e58703cffd3641f6cec73538aba3c44be0077a465a945bf7a'
def need(x,m):
 if not x:raise ValueError(m)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def tree(p):return {x.relative_to(p).as_posix():sha(x.read_bytes()) for x in p.rglob('*') if x.is_file() and not x.is_symlink()}
def run(cmd):
 t=time.monotonic();r=subprocess.run(cmd,capture_output=True,text=True,timeout=8)
 return r,round(time.monotonic()-t,5)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--package',type=Path,required=True);ap.add_argument('--scratch',type=Path,required=True);a=ap.parse_args();P=a.package
 original=tree(P/'source');release=json.loads((P/'RELEASE_INVENTORY.json').read_bytes());results=[]
 need(sha((P/'source/MANIFEST.json').read_bytes())==PIN,'external source pin')
 need(len(original)==150,'source closure count')
 for row in release['files']:
  raw=(P/row['path']).read_bytes();need(len(raw)==row['bytes'] and sha(raw)==row['sha256'],'six bytes')
 def audit_zip(raw):
  with zipfile.ZipFile(io.BytesIO(raw)) as z:
   names=z.namelist();need(len(set(names))==len(names),'zip duplicate')
   for info in z.infolist():
    need(not info.filename.startswith('/') and '..' not in Path(info.filename).parts,'zip path')
    need(info.external_attr>>16==0o100644,'zip regular0644')
    need(info.date_time==(2026,10,16,0,0,0),'fixed timestamp')
   return {n:z.read(n) for n in names}
 source=audit_zip((P/'source-and-verification.zip').read_bytes());need({n:sha(v) for n,v in source.items()}==original,'portable archive source')
 kit=audit_zip((P/'zenodo-upload-kit.zip').read_bytes());need(len(kit)==5,'kit closure')
 need(kit['paper.pdf']==(P/'output/pdf/paper.pdf').read_bytes(),'kit pdf');need(kit['source-and-verification.zip']==(P/'source-and-verification.zip').read_bytes(),'kit source')
 with tempfile.TemporaryDirectory(prefix='physical-',dir=a.scratch) as temp:
  w=Path(temp);copy=w/'source';copy.mkdir()
  for n,raw in source.items():
   t=copy/n;t.parent.mkdir(parents=True,exist_ok=True);t.write_bytes(raw)
  pdf=w/'external.pdf';pdf.write_bytes((P/'output/pdf/paper.pdf').read_bytes());sentinel=w/'sentinel';sentinel.write_bytes(b'protected sentinel\n')
  for optimized in (False,True):
   flags=[sys.executable,'-I','-B']+(['-O'] if optimized else [])
   # Rebuild the entire exact six objects from the extracted portable source.
   out=w/('rebuild'+str(optimized));cmd=flags+[str(P/'source/build_package.py'),'--source',str(copy),'--expected-manifest-sha256',PIN,'--pdf',str(pdf),'--output-dir',str(out)]
   r,t=run(cmd);need(r.returncode==0,r.stderr)
   for row in release['files']:need((out/row['path']).read_bytes()==(P/row['path']).read_bytes(),'byte-identical rebuild')
   need((out/'RELEASE_INVENTORY.json').read_bytes()==(P/'RELEASE_INVENTORY.json').read_bytes(),'inventory rebuild')
   results.append({'case':'exact_six_rebuild','optimized':optimized,'result':'PASS','seconds':t})
   for tool in ('verifier','builder'):
    for target in ('manifest','helper','pdf'):
     p={'manifest':copy/'MANIFEST.json','helper':copy/'build_package.py','pdf':pdf}[target];saved=p.read_bytes()
     for kind in ('fifo','directory','symlink'):
      p.unlink()
      if kind=='fifo':os.mkfifo(p)
      elif kind=='directory':p.mkdir()
      else:p.symlink_to(sentinel)
      if tool=='verifier':cmd=flags+[str(copy/'verify_bundle.py'),'--expected-manifest-sha256',PIN,'--pdf',str(pdf)]
      else:cmd=flags+[str(P/'source/build_package.py'),'--source',str(copy),'--expected-manifest-sha256',PIN,'--pdf',str(pdf),'--output-dir',str(w/'negative-out')]
      try:
       r,t=run(cmd);need(r.returncode!=0 and t<8,'malformed input accepted/blocked')
       need(any(x in r.stdout+r.stderr for x in ('Nonregular','symlink','Unexpected empty source directory')), 'expected rejection class: '+tool+' '+target+' '+kind+' '+r.stdout+r.stderr)
       need(sentinel.read_bytes()==b'protected sentinel\n','sentinel changed')
       results.append({'case':'input_'+target+'_'+kind,'tool':tool,'optimized':optimized,'result':'REJECTED','seconds':t})
      finally:
       if p.is_dir() and not p.is_symlink():p.rmdir()
       else:p.unlink()
       p.write_bytes(saved)
   for kind in ('late_fifo','late_symlink','hardlink','directory','ancestor_symlink','inside_source'):
    area=w/(kind+str(optimized));area.mkdir();out=area/'out';out.mkdir()
    if kind=='late_fifo':os.mkfifo(out/'RELEASE_INVENTORY.json')
    elif kind=='late_symlink':(out/'zenodo-upload-kit.zip').symlink_to(sentinel)
    elif kind=='hardlink':os.link(copy/'paper.tex',out/'zenodo-deposit.json')
    elif kind=='directory':(out/'source-and-verification.zip').mkdir()
    elif kind=='ancestor_symlink':link=area/'alias';link.symlink_to(out);out=link
    else:out=copy
    cmd=flags+[str(P/'source/build_package.py'),'--source',str(copy),'--expected-manifest-sha256',PIN,'--pdf',str(pdf),'--output-dir',str(out)]
    r,t=run(cmd);need(r.returncode!=0,'unsafe output accepted');need(tree(copy)==original,'copied source mutated');need(sentinel.read_bytes()==b'protected sentinel\n','output sentinel mutated')
    if kind not in ('inside_source','ancestor_symlink'):need(not (out/'paper.tex').exists(),'partial batch write')
    results.append({'case':'output_'+kind,'optimized':optimized,'result':'REJECTED_BEFORE_BATCH_WRITE','seconds':t})
   helper=copy/'build_package.py';saved=helper.read_bytes();helper.write_bytes(saved+b'\nraise RuntimeError("UNAUTHENTICATED_HELPER_EXECUTED")\n')
   r,t=run(flags+[str(copy/'verify_bundle.py'),'--expected-manifest-sha256',PIN]);need(r.returncode!=0 and json.loads(r.stdout)['error']=='Builder binding differs','helper execution before authentication');helper.write_bytes(saved)
   results.append({'case':'tampered_helper','optimized':optimized,'result':'REJECTED_BEFORE_IMPORT','seconds':t})
 need(tree(P/'source')==original,'reviewed input mutation')
 print(json.dumps({'result':'PASS','source_manifest_sha256':PIN,'six_artifacts_bound':6,'source_files':len(source),'kit_files':len(kit),'cases':results,'case_count':len(results),'protected_source_unchanged':True,'scope':'Physical malformed-input, output preflight, helper-authentication controls and exact portable rebuilds.'},indent=2))
if __name__=='__main__':main()
