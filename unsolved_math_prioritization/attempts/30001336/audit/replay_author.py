#!/usr/bin/env python3
"""Replay pinned author code and controlled temporary-copy mutations. No network.
Only temporary test directories are modified; caller can redirect JSON output.
"""
import hashlib,json,os,pathlib,shutil,stat,subprocess,sys,tempfile,zipfile
if len(sys.argv)!=2: raise SystemExit('Usage: python -I -B replay_author.py AUTHOR_SAFE_FREEZE.zip')
ZIP=pathlib.Path(sys.argv[1]).resolve()
PIN='fcb64d4662bb9b54b5047557807ab1a5e3560b2261f1544d0248497a31a627ee'
MAN='dfcf5632ba6ac56d177f308bf0dec215fe397c46cc7f1bb3f55ba1efb49088f2'

def need(c,label):
 if not c: raise RuntimeError(label)

def external_bind(root):
 manifest=root/'MANIFEST.json';need(stat.S_ISREG(manifest.lstat().st_mode),'manifest regular')
 raw=manifest.read_bytes();need(hashlib.sha256(raw).hexdigest()==MAN,'pinned manifest')
 records=json.loads(raw)['files']; expected={e['path'] for e in records}|{'MANIFEST.json'}
 need({p.name for p in root.iterdir()}==expected,'inventory')
 for e in records:
  p=root/e['path'];need(stat.S_ISREG(p.lstat().st_mode),'regular '+p.name)
  data=p.read_bytes();need(len(data)==e['bytes'] and hashlib.sha256(data).hexdigest()==e['sha256'],'bytes '+p.name)

raw=ZIP.read_bytes();need(len(raw)==18567 and hashlib.sha256(raw).hexdigest()==PIN,'archive pin')
results=[]
with tempfile.TemporaryDirectory(prefix='rooted-audit-independent-') as temp:
 temp=pathlib.Path(temp); original=temp/'clean'; original.mkdir()
 with zipfile.ZipFile(ZIP) as z:
  need(len(z.infolist())==10,'archive count')
  for info in z.infolist():
   need(pathlib.PurePosixPath(info.filename).name==info.filename,'flat safe zip')
   need(not info.is_dir(),'regular ZIP member')
  z.extractall(original)
 external_bind(original)
 for optimized in (False,True):
  flags=['-I','-B']+(['-O'] if optimized else [])
  mode='optimized' if optimized else 'normal'
  for name in ('verify_packet.py','verify_math.py'):
   out=subprocess.run([sys.executable,*flags,str(original/name)],cwd='/',capture_output=True,text=True,timeout=120)
   need(out.returncode==0,'relocated '+name+' '+out.stderr)
   j=json.loads(out.stdout);results.append({'control':'relocated_'+name,'mode':mode,'result':'PASS','assertions':sum(j.get('assertions_by_family',{}).values())})
   external_bind(original)
  mutations=['changed_bytes','missing_file','extra_file','extra_directory','symlink','fifo','bytecode_directory','sourceless_bytecode']
  for mutation in mutations:
   root=temp/(mode+'_'+mutation);shutil.copytree(original,root)
   if mutation=='changed_bytes': (root/'README.md').write_bytes((root/'README.md').read_bytes()+b'\n')
   elif mutation=='missing_file': (root/'README.md').unlink()
   elif mutation=='extra_file': (root/'extra').write_text('x')
   elif mutation=='extra_directory': (root/'unexpected').mkdir()
   elif mutation=='symlink': (root/'README.md').unlink();(root/'README.md').symlink_to(original/'README.md')
   elif mutation=='fifo': (root/'README.md').unlink();os.mkfifo(root/'README.md')
   elif mutation=='bytecode_directory': (root/'__pycache__').mkdir();(root/'__pycache__'/'sympy.cpython-311.pyc').write_bytes(b'not executed')
   elif mutation=='sourceless_bytecode': (root/'sympy.pyc').write_bytes(b'not executed')
   try: external_bind(root)
   except RuntimeError: pass
   else: raise RuntimeError('external binder accepted '+mutation)
   out=subprocess.run([sys.executable,*flags,str(root/'verify_packet.py')],cwd='/',capture_output=True,text=True,timeout=20)
   need(out.returncode!=0,'author verifier accepted '+mutation)
   results.append({'control':mutation,'mode':mode,'result':'REJECTED_BEFORE_MATH_EXECUTION'})
  math_mutations={
   'missing_y_subtraction':('A*(M1b-L1b-b)+B*(M1a-L1a-a)','A*(M1b-L1b)+B*(M1a-L1a-a)'),
   'missing_quotient_denominator':('q1=g1-(x-a)','q1=g1'),
   'wrong_N_orientation':('n=integral(lambda r:(g1(r,b)-g1(a,b))/(r-a)','n=integral(lambda r:(g1(a,b)-g1(r,b))/(r-a)'),
   'wrong_zero_letter_sign':('((0,-1),)','((0,1),)'),
   'wrong_inverse_sign':('d.append(-sum(h[j]*d[n-j]','d.append(sum(h[j]*d[n-j]'),
   'removed_shuffle_multiplicity':('c[(v[0],)+w]+=n','c[(v[0],)+w]=n')}
  for mutation,(old,new) in math_mutations.items():
   root=temp/(mode+'_'+mutation);shutil.copytree(original,root)
   code=(root/'verify_math.py').read_text();need(code.count(old)==1,'controlled patch location '+mutation)
   (root/'verify_math.py').write_text(code.replace(old,new))
   out=subprocess.run([sys.executable,*flags,str(root/'verify_math.py')],cwd='/',capture_output=True,text=True,timeout=120)
   need(out.returncode!=0,'math mutation survived '+mutation)
   need('RuntimeError' in out.stderr,'mutation was not semantic rejection '+out.stderr)
   results.append({'control':mutation,'mode':mode,'result':'REJECTED_BY_MATH_CHECKS','reason':out.stderr.strip().splitlines()[-1]})
result={'author_zip_sha256':PIN,'author_manifest_sha256':MAN,'author_bytes':len(raw),'author_files':10,'controls':results,'note':'Controlled mathematical mutations were deliberately executed only after their exact authored changes were reviewed. Unverified injected bytecode was never executed.'}
print(json.dumps(result,indent=2))
