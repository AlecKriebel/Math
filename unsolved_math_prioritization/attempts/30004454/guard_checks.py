#!/usr/bin/env python3
"""Fresh complete-output and intended semantic mutation controls; no original replay."""
import ast,hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path

def need(ok,label):
 if not ok:raise ValueError(label)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def same(a,b):
 if type(a) is not type(b):return False
 if type(a) is dict:return set(a)==set(b) and all(same(a[k],b[k]) for k in a)
 if type(a) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b

MUTANTS=[
 ('reflection_entry','each generator preserves the exact Gram form'),
 ('reverse_st','column-vector product is rho(s)rho(t)'),
 ('root_polynomial','coefficient-wise universal recurrence A v(n)=v(n+1)'),
 ('pairing_sign','coefficient-wise pairing B(e_t,v(n))=-1-4n'),
 ('spherical_triangle','triangle must have d at least 3'),
 ('nondivisible_label','common divisor must divide every finite label'),
 ('disconnected_part','each contracted part is connected'),
 ('kill_partial_odd_component','each original relator survives in D_infinity'),
 ('separated_even_cross_edge','each original relator survives in D_infinity'),
 ('invent_missing_edge','missing edges must not be given order-two relations'),
 ('trivial_overlap_centralizer','transposition centralizer has order two, not one'),
 ('homomorphic_conjugator','anchor conjugator satisfies crossed composition law'),
 ('replace_full_stabilizer_by_spe','full stabilizer has full Aut(C2^2) restriction image'),
 ('finite_index_image_is_coxeter','infinite cyclic finite-index image is not an infinite Coxeter group'),
]

class Corrupt(ast.NodeTransformer):
 def __init__(self,name):self.name=name;self.count=0
 def visit_Assign(self,node):
  node=self.generic_visit(node)
  if len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
   target=node.targets[0].id
   if self.name=='bad_reflection' and target=='s':node.value.elts[0].elts[1]=ast.Constant(3);self.count+=1
   elif self.name=='bad_triangle_d' and target=='d':node.value=ast.Constant(4);self.count+=1
   elif self.name=='zero_initial_vector' and target=='v' and isinstance(node.value,ast.List):node.value=ast.List([ast.Constant(0),ast.Constant(0),ast.Constant(0)],ast.Load());self.count+=1
  return node

def main():
 need(len(sys.argv)==1,'no arguments');need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000')
 need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'-I -S -B')
 root=Path(__file__).resolve().parent;mode=[] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize]
 scripts=('verify_calculations_hardened.py','independent_verify.py')
 sources={n:(root/n).read_bytes() for n in scripts}
 accepted={n:{k:(root/(n[:-3]+'.mode'+str(sys.flags.optimize)+'.reference.'+k)).read_bytes() for k in ('stdout','stderr')} for n in scripts}
 records=[]
 with tempfile.TemporaryDirectory(prefix='coxeter-mathematics-') as td:
  p=Path(td)
  for n,raw in sources.items():(p/n).write_bytes(raw)
  hard=[('bad_reflection','Failed original check at line 33'),('bad_triangle_d','Failed original check at line 52'),('zero_initial_vector','Failed original check at line 39')]
  for label,_ in hard:
   t=Corrupt(label);tree=t.visit(ast.parse(sources['verify_calculations_hardened.py']));need(t.count==1,'one intended semantic mutation '+label)
   (p/(label+'.py')).write_text(ast.unparse(ast.fix_missing_locations(tree))+'\n')
  for f in p.iterdir():f.chmod(0o444)
  p.chmod(0o555)
  def snapshot():return {f.name:{'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in sorted(p.iterdir())}
  before=snapshot();denials=[]
  try:
   for f in [p,*sorted(p.iterdir())]:
    directory=f==p;need((f.stat().st_mode&0o777)==(0o555 if directory else 0o444) and not os.access(f,os.W_OK),'read-only mathematical fixture')
    try:fd=os.open(f/'FORBIDDEN_CREATE' if directory else f,os.O_WRONLY|(os.O_CREAT|os.O_EXCL if directory else os.O_APPEND),0o600)
    except PermissionError as e:need(e.errno==13,'physical EACCES');denials.append({'path':'.' if directory else f.name,'errno':13,'denied':True})
    else:os.close(fd);raise ValueError('write permitted')
   def run(label,n,args=()):
    probe="""import json,os,sys
from pathlib import Path
if os.getuid()!=1000 or os.geteuid()!=1000:raise RuntimeError('UID/EUID 1000 required')
probes=[]
for file,create in [(Path('FORBIDDEN_CHILD_CREATE'),True),(Path(TARGET),False)]:
 try:fd=os.open(file,os.O_WRONLY|(os.O_CREAT|os.O_EXCL if create else os.O_APPEND),0o600)
 except PermissionError as e:
  if e.errno!=13:raise RuntimeError('expected EACCES')
  probes.append({'operation':'create' if create else 'append_open','errno':13,'denied':True})
 else:os.close(fd);raise RuntimeError('child write permitted')
print('ENV '+json.dumps({'uid':os.getuid(),'euid':os.geteuid(),'optimization':sys.flags.optimize,'directory_mode':oct(Path.cwd().stat().st_mode&0o777),'target_mode':oct(Path(TARGET).stat().st_mode&0o777),'physical_denials':probes},sort_keys=True),flush=True)
""".replace('TARGET',repr(n))
    launcher=probe+"code=open("+repr(n)+",'rb').read();sys.argv=["+repr(n)+"]+sys.argv[1:];exec(compile(code,"+repr('<coxeter-'+label+'>')+",'exec'),{'__name__':'__main__'})"
    r=subprocess.run([sys.executable,'-I','-S','-B',*mode,'-c',launcher,*args],cwd=p,env=dict(PATH=os.defpath,HOME=str(p),TMPDIR=str(p),LC_ALL='C'),capture_output=True,timeout=30)
    envline,sep,body=r.stdout.partition(b'\n');need(sep and envline.startswith(b'ENV '),'child execution evidence')
    expected={'uid':1000,'euid':1000,'optimization':sys.flags.optimize,'directory_mode':'0o555','target_mode':'0o444','physical_denials':[{'operation':'create','errno':13,'denied':True},{'operation':'append_open','errno':13,'denied':True}]}
    need(same(json.loads(envline[4:]),expected),'exact child readonly evidence')
    need(envline==b'ENV '+json.dumps(expected,sort_keys=True).encode(),'complete child evidence formatting')
    row={'case':label,'script':n,'arguments':list(args),'exit_code':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode(),'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr),'environment':expected}
    records.append(row);return r,row,body
   for n in scripts:
    r,row,body=run('baseline-'+n,n);need(r.returncode==0 and r.stderr==accepted[n]['stderr'] and body==accepted[n]['stdout'],'complete baseline output equality')
    if n=='independent_verify.py':
     need(same(json.loads(body),json.loads(accepted[n]['stdout'])),'recursive exact baseline JSON types')
     need(json.loads(body)=={'checks':6066,'cyclic_graphs':626,'euid':1000,'mutant':None,'optimization':sys.flags.optimize,'result':'PASS','uid':1000},'independent baseline scope')
    row.update(complete_reference_equality=True,recursive_exact_types=n=='independent_verify.py')
   for label,condition in hard:
    r,row,body=run(label,label+'.py');need(r.returncode==1 and body==b'' and r.stderr.endswith(('RuntimeError: '+condition+'\n').encode()),'hardened intended rejection '+label)
    row.update(rejected=True,intended_condition=condition)
   for label,condition in MUTANTS:
    r,row,body=run(label,'independent_verify.py',('--mutant',label));j=json.loads(body)
    need(r.returncode==1 and r.stderr==b'' and set(j)=={'result','check','checks','uid','euid','optimization','mutant'},'independent rejection schema '+label)
    need(j['result']=='FAIL' and j['check']==condition and type(j['checks']) is int and j['checks']>0 and type(j['uid']) is int and j['uid']==1000 and type(j['euid']) is int and j['euid']==1000 and type(j['optimization']) is int and j['optimization']==sys.flags.optimize and j['mutant']==label,'independent intended rejection '+label)
    need(body==(json.dumps(j,sort_keys=True)+'\n').encode(),'full independent rejection format')
    row.update(rejected=True,intended_condition=condition)
   after=snapshot();need(after==before,'mathematical fixture changed')
  finally:
   p.chmod(0o755)
   for f in p.iterdir():f.chmod(0o644)
 need(all((root/n).read_bytes()==v for n,v in sources.items()),'accepted source changed')
 print(json.dumps({'schema':1,'problem_id':30004454,'status':'PASS','uid':os.getuid(),'euid':os.geteuid(),'optimization':sys.flags.optimize,'positive_runs':2,'mathematical_negative_controls':17,'hardened_semantic_mutants':3,'independent_semantic_mutants':14,'runs':records,'physical_denials':denials,'child_physical_denials':2*len(records),'before':before,'after':after,'fixture_unchanged':True,'source_unchanged':True,'normalization':'NONE','portable_original_checker_replay':'NOT_RUN','scope':'Current hardened and independent mathematical controls; historical assertion-only original is excluded; finite support does not certify universal proofs.'},indent=2,sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,TypeError,KeyError,OSError,subprocess.TimeoutExpired) as e:print('REJECT: mathematical guard: '+str(e),file=sys.stderr);sys.exit(1)
