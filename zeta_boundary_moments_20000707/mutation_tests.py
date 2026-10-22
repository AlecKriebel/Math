"""Reject actual mathematical changes and recursive inventory tampering in both modes."""
import hashlib,json,pathlib,subprocess,sys,tempfile
ROOT=pathlib.Path(__file__).resolve().parent
source=(ROOT/'checks.py').read_text()
mutations=[
 ('bump_coefficient','1 - 7 * v * v','1 - 6 * v * v'),
 ('bump_primitive','v * (1 - v * v) ** 3','v * (1 - v * v) ** 2'),
 ('zeta_zero','z0 = -s.Rational(1, 2)','z0 = s.Rational(1, 2)'),
 ('zeta_derivative','zprime0 = -s.log(2 * pi) / 2','zprime0 = s.log(2 * pi) / 2'),
 ('secondary_pole_sign','secondary_sign = -1','secondary_sign = 1'),
 ('pole_cross_sign','cross_sign = -1','cross_sign = 1'),
 ('D_gamma_sign','D_gamma_sign = -1','D_gamma_sign = 1'),
 ('endpoint_sign','endpoint_sign = -1','endpoint_sign = 1'),
 ('bump_positivity_budget','K = 1000','K = 100'),
 ('smoothing_sign','smoothing_sign=1','smoothing_sign=-1')]
results=[]
def run(label,path,mode,args=()):
 cmd=[sys.executable]+(['-O'] if mode=='optimized' else [])+[str(path),*args]
 proc=subprocess.run(cmd,capture_output=True,text=True)
 results.append({'test':label,'mode':mode,'command':['python']+(['-O'] if mode=='optimized' else [])+[path.name,*args],'exit_code':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr.replace(str(path.parent),'<temporary-test-directory>')})
 if proc.returncode==0:
  raise RuntimeError('Mutation survived: '+label+' '+mode)
with tempfile.TemporaryDirectory() as temp:
 temp=pathlib.Path(temp)
 for name,old,new in mutations:
  if source.count(old)!=1:
   raise RuntimeError('Mutation target must occur exactly once: '+name)
  path=temp/(name+'.py');path.write_text(source.replace(old,new))
  for mode in ('normal','optimized'): run(name,path,mode,('--symbolic-only',))
 for name in ('nested_manifest','symlink','unsafe_parent','unsafe_absolute','duplicate','extra_nested','missing','changed_bytes'):
  root=temp/name;root.mkdir()
  verifier=root/'verify_integrity.py';verifier.write_bytes((ROOT/'verify_integrity.py').read_bytes())
  data=root/'data.txt';data.write_text('test fixture\n')
  rows=[{'path':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (verifier,data)]
  if name=='nested_manifest':
   (root/'nested').mkdir();(root/'nested/MANIFEST.json').write_text('{}')
  elif name=='symlink': (root/'alias').symlink_to('data.txt')
  elif name=='unsafe_parent': rows[1]['path']='../data.txt'
  elif name=='unsafe_absolute': rows[1]['path']='/data.txt'
  elif name=='duplicate': rows.append(dict(rows[1]))
  elif name=='extra_nested':
   (root/'nested').mkdir();(root/'nested/extra.txt').write_text('extra')
  elif name=='missing': data.unlink()
  elif name=='changed_bytes': data.write_text('changed')
  (root/'MANIFEST.json').write_text(json.dumps({'schema':1,'files':rows}))
  for mode in ('normal','optimized'): run(name,verifier,mode)
print(json.dumps({'status':'PASS','warning':'Mutations test checks, not analytic truth or novelty.','results':results},indent=2))
