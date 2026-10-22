#!/usr/bin/env python3
"""Fresh complete-output, original forced failure and independent semantic controls."""
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

MUTANTS=[('adjacent_only', 'RuntimeError: CHECK_FAILED[resolvent]: R=Q+zQR'), ('diagonal_included', 'RuntimeError: CHECK_FAILED[campbell]: same-configuration Campbell/Palm at aa'), ('edge_instead_of_vertex_deletion', 'RuntimeError: CHECK_FAILED[lattice]: bowtie marked single'), ('first_moment_controls_pairs', 'RuntimeError: CHECK_FAILED[ui]: nonvanishing pair intensity'), ('generation_mark_shifted', 'RuntimeError: CHECK_FAILED[resolvent]: R=Q+zQR'), ('identity_generation_included', 'RuntimeError: CHECK_FAILED[resolvent]: R=Q+zQR'), ('independent_realizations', 'RuntimeError: CHECK_FAILED[campbell]: same-configuration Campbell/Palm at aa'), ('low_fugacity_sign', 'RuntimeError: CHECK_FAILED[lattice]: linked_triangles fugacity coefficient'), ('modulus_marginals_suffice', 'RuntimeError: CHECK_FAILED[conditional]: embedded-shape conditional law'), ('ordered_pair_halved', 'RuntimeError: CHECK_FAILED[lattice]: linked_triangles ordered distinct pair'), ('pair_ratio_inverted', 'RuntimeError: CHECK_FAILED[lattice]: linked_triangles pair ratio'), ('per_realization_normalization', 'RuntimeError: CHECK_FAILED[campbell]: same-configuration Campbell/Palm at ab'), ('single_missing_fugacity', 'RuntimeError: CHECK_FAILED[lattice]: linked_triangles marked single'), ('unbiased_palm', 'RuntimeError: CHECK_FAILED[campbell]: same-configuration Campbell/Palm at ab'), ('wrong_ars_generation', 'RuntimeError: CHECK_FAILED[numeric]: independent source transcription'), ('wrong_ars_sine_factor', 'RuntimeError: CHECK_FAILED[numeric]: independent source transcription'), ('wrong_dilute_parameter', 'RuntimeError: CHECK_FAILED[symbolic]: n=1 at kappa=3'), ('wrong_kappa4_prefactor', 'RuntimeError: CHECK_FAILED[symbolic]: kappa4 removable prefactor'), ('wrong_laplace_scale', 'RuntimeError: CHECK_FAILED[numeric]: independent source transcription')]

def main():
 need(len(sys.argv)==1,'no arguments');need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000')
 need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'-I -S -B')
 root=Path(__file__).resolve().parent;mode=[] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize]
 scripts=('check_exact.py','audit_exact.py');support=('DEPENDENCY_RUNNER.py',)
 sources={n:(root/n).read_bytes() for n in scripts+support}
 accepted={n:{k:(root/(n[:-3]+'.mode'+str(sys.flags.optimize)+'.reference.'+k)).read_bytes() for k in ('stdout','stderr')} for n in scripts}
 records=[]
 with tempfile.TemporaryDirectory(prefix='two-loop-mathematics-') as td:
  p=Path(td)
  for n,raw in sources.items():(p/n).write_bytes(raw)
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
    launcher=probe+"sys.argv=['DEPENDENCY_RUNNER.py',"+repr(n)+"]+sys.argv[1:];code=open('DEPENDENCY_RUNNER.py','rb').read();exec(compile(code,'<two-loop-dependency-runner>','exec'),{'__name__':'__main__','__file__':str(Path('DEPENDENCY_RUNNER.py').resolve())})"
    r=subprocess.run([sys.executable,'-I','-S','-B',*mode,'-c',launcher,*args],cwd=p,env=dict(PATH=os.defpath,HOME=str(p),TMPDIR=str(p),LC_ALL='C'),capture_output=True,timeout=200)
    envline,sep,body=r.stdout.partition(b'\n');need(sep and envline.startswith(b'ENV '),'child execution evidence')
    expected={'uid':1000,'euid':1000,'optimization':sys.flags.optimize,'directory_mode':'0o555','target_mode':'0o444','physical_denials':[{'operation':'create','errno':13,'denied':True},{'operation':'append_open','errno':13,'denied':True}]}
    need(same(json.loads(envline[4:]),expected),'exact child readonly evidence')
    need(envline==b'ENV '+json.dumps(expected,sort_keys=True).encode(),'complete child evidence formatting')
    row={'case':label,'script':n,'arguments':list(args),'exit_code':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode(),'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr),'environment':expected}
    records.append(row);return r,row,body
   for n in scripts:
    args=('--require-readonly',) if n=='audit_exact.py' else ()
    r,row,body=run('baseline-'+n,n,args);need(r.returncode==0 and r.stderr==accepted[n]['stderr'] and body==accepted[n]['stdout'],'complete baseline output equality')
    need(same(json.loads(body),json.loads(accepted[n]['stdout'])),'recursive exact baseline JSON types')
    data=json.loads(body)
    if n=='check_exact.py':need(data['finite_graph_checks']==1482 and data['symbolic_checks']==6 and data['rare_event_checks']==60 and data['continuum_claim_verified'] is False,'original exact check scope')
    else:
     counts={'environment':1,'lattice':41766,'campbell':10,'resolvent':6,'conditional':6,'symbolic':11,'numeric':297,'ui':298}
     need(same(data['counts'],counts) and data['mutant'] is None and data['continuum_theorem_proved'] is False,'independent exact/numeric scope')
     need(sum(v for k,v in data['counts'].items() if k not in ('environment','numeric'))==42097,'independent exact check count')
     need(len(data['outputs']['lattice'])==82,'independent graph inputs')
    row.update(complete_reference_equality=True,recursive_exact_types=True)
   r,row,body=run('intentional-forced-failure','check_exact.py',('--force-failure',))
   condition='RuntimeError: intentional failure: optimization must not disable this'
   need(r.returncode==1 and body==b'' and r.stderr.endswith((condition+'\n').encode()),'original intended forced failure')
   row.update(rejected=True,intended_condition=condition,semantic_mutation=False)
   for label,condition in MUTANTS:
    r,row,body=run(label,'audit_exact.py',('--require-readonly','--mutant',label))
    need(r.returncode==1 and body==b'' and r.stderr.endswith((condition+'\n').encode()),'independent intended rejection '+label)
    row.update(rejected=True,intended_condition=condition,semantic_mutation=True,numerical_diagnostic=label in ('wrong_laplace_scale','wrong_ars_generation','wrong_ars_sine_factor'))
   after=snapshot();need(after==before,'mathematical fixture changed')
  finally:
   p.chmod(0o755)
   for f in p.iterdir():f.chmod(0o644)
 need(all((root/n).read_bytes()==v for n,v in sources.items()),'accepted source changed')
 print(json.dumps({'schema':1,'problem_id':30006088,'status':'PASS','uid':os.getuid(),'euid':os.geteuid(),'optimization':sys.flags.optimize,'positive_runs':2,'mathematical_negative_controls':19,'intentional_failure_controls':1,'independent_semantic_mutants':19,'exact_mathematical_checks':42097,'separate_numerical_diagnostics':297,'runs':records,'physical_denials':denials,'child_physical_denials':2*len(records),'before':before,'after':after,'fixture_unchanged':True,'source_unchanged':True,'normalization':'NONE','historical_audit_harness_replay':'NOT_RUN','scope':'Unchanged original and independent safe checks with explicit failures; exact checks and high-precision numerical diagnostics remain distinct; no continuum theorem or full embedded-pair comparison is certified.'},indent=2,sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,TypeError,KeyError,OSError,subprocess.TimeoutExpired) as e:print('REJECT: mathematical guard: '+str(e),file=sys.stderr);sys.exit(1)
