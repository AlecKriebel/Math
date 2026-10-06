import base64,concurrent.futures,hashlib,json,os,pathlib,shutil,subprocess,sys,tempfile
ROOT=pathlib.Path(sys.argv[1]).resolve();OUT=pathlib.Path(sys.argv[2]).resolve()

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(c,l):
 if not c:raise RuntimeError(l)
def run(path,*args,optimized=False):
 r=subprocess.run([sys.executable,'-I','-B',*(['-O'] if optimized else []),str(path),*map(str,args)],cwd='/',capture_output=True,text=True,timeout=1200)
 need(r.returncode==0,str(path)+' '+r.stderr);return json.loads(r.stdout)
pin=digest(ROOT/'PUBLICATION_MANIFEST.json')
source=(ROOT/'verify_publication.py').read_bytes()
encoded=base64.b64encode(source).decode('ascii')
runner="import base64,sys;filename=sys.argv[1];sys.argv=[filename,sys.argv[2]];exec(compile(base64.b64decode("+repr(encoded)+"),'<pinned publication verifier>','exec'),{'__name__':'__main__','__file__':filename})"
results={'full_replays':[],'publication_controls':[],'finite_controls_are_a_topology_proof':False}
with tempfile.TemporaryDirectory(prefix='Wu manifold publication ') as td:
 t=pathlib.Path(td);rel=t/'relocated with spaces';shutil.copytree(ROOT,rel)
 jobs=[(ROOT,False,'normal'),(ROOT,True,'optimized'),(rel,False,'relocated'),(rel,True,'relocated_optimized')]
 def test(job):
  root,opt,name=job;result=run(root/'verify_publication.py',pin,'--full',optimized=opt);result.pop('files');print(name+' PASS',flush=True);return {'mode':name,'result':result}
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results['full_replays']=list(pool.map(test,jobs))
 for opt in (False,True):
  mode='optimized' if opt else 'normal'
  for kind in ('changed_bytes','missing_file','extra_file','extra_directory','symlink','fifo','bytecode_directory','sourceless_bytecode','changed_manifest','tampered_verifier','rehashed_prose'):
   d=t/(mode+'_'+kind);shutil.copytree(ROOT,d)
   if kind=='changed_bytes':(d/'README.md').write_bytes((d/'README.md').read_bytes()+b'\n')
   elif kind=='missing_file':(d/'README.md').unlink()
   elif kind=='extra_file':(d/'extra').write_text('x')
   elif kind=='extra_directory':(d/'extra').mkdir()
   elif kind=='symlink':(d/'README.md').unlink();(d/'README.md').symlink_to(ROOT/'README.md')
   elif kind=='fifo':(d/'README.md').unlink();os.mkfifo(d/'README.md')
   elif kind=='bytecode_directory':(d/'__pycache__').mkdir();(d/'__pycache__'/'sympy.cpython-312.pyc').write_bytes(b'not executed')
   elif kind=='sourceless_bytecode':(d/'sympy.pyc').write_bytes(b'not executed')
   elif kind=='changed_manifest':(d/'PUBLICATION_MANIFEST.json').write_bytes((d/'PUBLICATION_MANIFEST.json').read_bytes()+b'\n')
   elif kind=='tampered_verifier':(d/'verify_publication.py').write_text('print("untrusted")')
   elif kind=='rehashed_prose':
    (d/'README.md').write_bytes((d/'README.md').read_bytes()+b'\nchanged')
    m=json.loads((d/'PUBLICATION_MANIFEST.json').read_text())
    row=next(x for x in m['files'] if x['path']=='README.md');row.update(bytes=(d/'README.md').stat().st_size,sha256=digest(d/'README.md'))
    (d/'PUBLICATION_MANIFEST.json').write_text(json.dumps(m))
   r=subprocess.run([sys.executable,'-I','-B',*(['-O'] if opt else []),'-c',runner,str(d/'verify_publication.py'),pin],cwd='/',capture_output=True,text=True,timeout=30)
   need(r.returncode!=0 and 'RuntimeError' in r.stderr,'publication corruption survived '+kind)
   results['publication_controls'].append({'mode':mode,'control':kind,'result':'REJECTED_BEFORE_MATH_EXECUTION'})
results['status']='PASS';results['formal_topology_verification']=False
OUT.write_text(json.dumps(results,indent=2)+'\n');print('ALL PASS '+str(OUT),flush=True)
