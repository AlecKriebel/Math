"""Fresh adversarial release attacks; all mutations are disposable local copies."""
from pathlib import Path
import sys,subprocess,json,hashlib,shutil,os,tempfile,datetime
HERE=Path(__file__).resolve().parent; AUDIT=HERE.parent.parent; BASE=HERE/'tmp/extracted'; PY=str(AUDIT/'tmp/venv/bin/python'); PDF=AUDIT/'publication/output/pdf/note.pdf'; PIN='a50792f1c2d55ba4b4d0085369ca08b0d47296d1a3963ea0c2fe820433093832'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,label):
 if not ok:raise RuntimeError(label)
def run(root,mode='normal',args=(),env_override=None):
 opts={'normal':[],'-O':['-O'],'-OO':['-OO']}[mode];env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
 if env_override:env.update(env_override)
 p=subprocess.run([PY,*opts,str(root/'verify_package.py'),*args],cwd=root,env=env,capture_output=True,text=True,timeout=300)
 return {'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'mode':mode,'environment_override':env_override or {}}
def rehash(root,name):
 mp=root/'PACKAGE_MANIFEST.json';m=json.loads(mp.read_text());p=root/name;m['files'][name]={'bytes':p.stat().st_size,'sha256':sha(p)};mp.write_text(json.dumps(m,indent=2)+'\n');return sha(mp)
cases=[];baselines=[]
with tempfile.TemporaryDirectory(prefix='fresh_tools_',dir=HERE/'tmp') as td:
 td=Path(td)
 for mode in ('normal','-O','-OO'):
  b=run(BASE,mode,args=['--expected-manifest',PIN,'--pdf',str(PDF)],env_override={'PYTHONOPTIMIZE':'2'} if mode=='normal' else None)
  require(b['returncode']==0,'Baseline '+mode);baselines.append(b)
 for mode in ('normal','-O'):
  def reject(label,mutate,pin=PIN,extra=()):
   root=td/(str(len(cases))+'_'+mode.replace('-',''));shutil.copytree(BASE,root)
   altered=mutate(root)
   used=altered if isinstance(altered,str) else pin
   p=run(root,mode,args=['--expected-manifest',used,*extra]);require(p['returncode']!=0,'Mutation false PASS: '+label)
   cases.append({'case':label,'rejected':True,'record':p})
  reject('Payload byte corruption',lambda r:(r/'note.tex').write_bytes((r/'note.tex').read_bytes()+b'%changed'))
  reject('Missing original proof',lambda r:(r/'original_packet/author/PROOF.md').unlink())
  reject('Unlisted executable file',lambda r:(r/'rogue.py').write_text('print("PASS")'))
  reject('Listed file symlink',lambda r:((r/'requirements.txt').unlink(),(r/'requirements.txt').symlink_to(BASE/'requirements.txt')))
  reject('Unlisted directory symlink',lambda r:(r/'source-link').symlink_to(BASE,target_is_directory=True))
  reject('Unlisted FIFO',lambda r:os.mkfifo(r/'private_fifo'))
  def bad_identity(r):
   p=r/'PACKAGE_MANIFEST.json';m=json.loads(p.read_text());m['problem_id']=30000718;p.write_text(json.dumps(m));return sha(p)
  reject('Wrong release identity even with supplied new manifest hash',bad_identity)
  def bad_size_type(r):
   p=r/'PACKAGE_MANIFEST.json';m=json.loads(p.read_text());m['files']['note.tex']['bytes']=float(m['files']['note.tex']['bytes']);p.write_text(json.dumps(m));return sha(p)
  reject('Floating-point manifest byte count',bad_size_type)
  def bad_path(r):
   p=r/'PACKAGE_MANIFEST.json';m=json.loads(p.read_text());m['files']['../note.tex']=m['files'].pop('note.tex');p.write_text(json.dumps(m));return sha(p)
  reject('Traversal path in trusted-rehashed manifest',bad_path)
  reject('Original proof changed and outer record rehashed',lambda r:((r/'original_packet/author/PROOF.md').write_bytes((r/'original_packet/author/PROOF.md').read_bytes()+b'\n'),rehash(r,'original_packet/author/PROOF.md'))[-1])
  reject('Original manifest changed and outer record rehashed',lambda r:((r/'original_packet/PUBLIC_MANIFEST.json').write_bytes((r/'original_packet/PUBLIC_MANIFEST.json').read_bytes()+b'\n'),rehash(r,'original_packet/PUBLIC_MANIFEST.json'))[-1])
  def proof_math(r):
   n='reviews/proof_family/check_exact.py';p=r/n;s=p.read_text();old='scale(mul(mul(power(x, 2), power(y, 2)), power(z, 2)), 3)';require(s.count(old)==1,'Proof mutation selector');p.write_text(s.replace(old,old[:-2]+'4)'));return rehash(r,n)
  reject('Fresh proof checker false sextic coefficient despite recomputed outer hash',proof_math)
  def computation_math(r):
   n='reviews/computation_family/checks/exact_controls.py';p=r/n;s=p.read_text();old="require(det==Q(-128),'Cubic determinant exactly -128 via Fraction elimination')";require(s.count(old)==1,'Computation selector');p.write_text(s.replace(old,old.replace('-128','-64')));return rehash(r,n)
  reject('Fresh computation checker false determinant despite recomputed outer hash',computation_math)
  badpdf=td/(mode.replace('-','')+'_bad.pdf');badpdf.write_bytes(PDF.read_bytes()+b'\n')
  reject('Separate PDF corrupted',lambda r:None,extra=['--pdf',str(badpdf)])
 # Explicit authenticity boundary, as documented: trusting a self-computed digest can admit changed descriptive prose.
 r=td/'self_rehash';shutil.copytree(BASE,r);(r/'README.md').write_text('An untrusted arbitrary claim: 0=1.\n');newpin=rehash(r,'README.md')
 trusted=run(r,args=['--integrity-only','--expected-manifest',PIN]);selfpin=run(r,args=['--integrity-only','--expected-manifest',newpin]);require(trusted['returncode']!=0 and selfpin['returncode']==0,'Trust boundary')
 boundary={'external_pin_rejects':trusted,'self_computed_pin_passes':selfpin,'interpretation':'Expected documented limit; only trusted external release digests bind descriptions. Integrity verification is not mathematical prose certification.'}
result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline_modes':baselines,'fresh_rejected_mutations':len(cases),'cases':cases,'authenticity_boundary':boundary,'raw_assert_checker_optimization_boundary':'Supported wrapper strips PYTHONOPTIMIZE and uses -I without -O for mathematical children; standalone historical optimized execution is explicitly unsupported.'}
(HERE/'evidence/tool_attacks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','fresh_rejected_mutations':len(cases),'modes':'normal/-O/-OO and inherited PYTHONOPTIMIZE=2','trust_boundary_verified':True},indent=2))
