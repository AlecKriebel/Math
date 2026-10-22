#!/usr/bin/env python3
"""Full-output exact replay and 39 genuine algebra mutants per optimization mode."""
import ast,concurrent.futures,hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path
def need(ok,label):
 if not ok:raise ValueError(label)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def same(a,b):
 if type(a) is not type(b):return False
 if type(a) is dict:return set(a)==set(b) and all(same(a[k],b[k]) for k in a)
 if type(a) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
MUTATIONS = [('annulus_constant', '1-2**(-n)), 2**n)', '1-2**(-n)), 2**n+1)', 'annulus_average_constant'), ('thickness_factor', '**n, 16)', '**n, 8)', 'thickness_radius_factor'), ('spike_exponent', '2**(3*k+8))', '2**(3*k+7))', 'spike_height_scaling'), ('spike_support_ratio', '9*2**(-2*k-6))', '8*2**(-2*k-6))', 'adjacent_support_ratio'), ('curvature_ratio', '2**(k*k-2*k+2))', '2**(k*k-2*k+1))', 'curvature_ratio_exponent'), ('oscillatory_derivative', 's.Rational(4,5)*s.cos(t)))', 's.Rational(3,5)*s.cos(t)))', 'oscillatory_f_second_derivative'), ('entire_rhs', 'G = 2*(n-2)*s.exp(t)+4*s.exp(2*t)', 'G = 2*(n-2)*s.exp(t)+5*s.exp(2*t)', 'entire_solution_PDE'), ('hardy_threshold', '(n-2)*(n-10)/4)', '(n-2)*(n-9)/4)', 'Hardy_dimension_threshold'), ('normalization_amplitude', 'a = n/(n+2)', 'a = (n+2)/n', 'normalized_g_derivative'), ('normalization_radius', 'r*r/(2*n+4)', 'r*r/(2*n)', 'normalized_entire_PDE'), ('cylinder_drift', '-wtt+(n-2)*wt+2*(n-2))', '-wtt+(n+2)*wt+2*(n-2))', 'cylindrical_radial_operator'), ('cylinder_measure', 'n-1-2*beta-2, -1)', 'n-1-2*beta-2, -2)', 'cylinder_measure_exponent'), ('chain_rule_sign', 'Fpp*F-Fppp*grad2)', 'Fpp*F+Fppp*grad2)', 'potential_chain_rule_jets'), ('spike_relative_scale', 'rho/rk, 2**(-2*k-4))', 'rho/rk, 2**(-3*k-4))', 'spike_relative_radius'), ('first_derivative_coefficient', 's.exp(t)*(1+s.Rational(2,5)*(s.sin(t)+s.cos(t))))', 's.exp(t)*(1+s.Rational(1,5)*(s.sin(t)+s.cos(t))))', 'oscillatory_f_first_derivative'), ('negative_third_sign', '1-s.Rational(4,5)*s.sqrt(2))', '1+s.Rational(4,5)*s.sqrt(2))', 'negative_third_derivative_value'), ('entire_potential_coefficient', '2*(n-2)/(1+r*r)+8/(1+r*r)**2)', '2*(n-2)/(1+r*r)+4/(1+r*r)**2)', 'entire_stability_potential'), ('entire_comparison_coefficient', '(2*(n-2)+2*(n-6)*r*r)/(1+r*r)**2)', '(2*(n-2)+2*(n-5)*r*r)/(1+r*r)**2)', 'entire_potential_Hardy_comparison'), ('normalized_value', "eq('normalized_g_value', g.subs(t,0), 1)", "eq('normalized_g_value', g.subs(t,0), 2)", 'normalized_g_value'), ('energy_cross_coefficient', 'H*z*z, 2*beta*z*zt)', 'H*z*z, 3*beta*z*zt)', 'cylinder_energy_cross_term')]
INDEPENDENT = [('cutoff_annulus', 'cutoff_energy_without_ball_volume'), ('thickness_radius', 'thickness_ratio'), ('spike_height', 'spike_height'), ('spike_support', 'adjacent_separation'), ('form_margin', 'strict_form_margin'), ('mass_baseline', 'baseline_mass'), ('curvature_ratio', 'curvature_ratio_exponent'), ('oscillatory_coefficient', 'osc_first'), ('entire_rhs', 'entire_equation'), ('entire_potential', 'entire_linearization'), ('hardy_threshold', 'dimension_threshold'), ('normalize_amplitude', 'normalized_derivative'), ('normalize_radius', 'normalized_equation'), ('blowup_lambda', 'blowup_PDE_factor'), ('cylinder_drift', 'cylinder_equation_radial'), ('cylinder_hardy', 'cylinder_energy_expansion'), ('angular_sign', 'angular_equation'), ('chain_rule_sign', 'potential_chain_rule'), ('compatibility_sign', 'gradient_compatibility')]
LAUNCHER = "import os,sys,sysconfig;from pathlib import Path;\nif os.getuid()!=1000 or os.geteuid()!=1000:raise RuntimeError('UID/EUID 1000 required')\nsys.path.append(sysconfig.get_path('purelib'));import sympy,mpmath\nif sympy.__version__!='1.14.0' or mpmath.__version__!='1.3.0':raise RuntimeError('tested dependency versions required')\nn=sys.argv[1];sys.argv=sys.argv[1:];exec(compile(Path(n).read_bytes(),n,'exec'),{'__name__':'__main__','__file__':str(Path(n).resolve())})"

def main():
 need(len(sys.argv)==1,'no arguments');need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000')
 need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'-I -S -B')
 root=Path(__file__).resolve().parent;mode=[] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize]
 scripts=('check_exact.py','audit_exact.py');sources={n:(root/n).read_bytes() for n in scripts}
 accepted={n:{k:(root/(n[:-3]+'.mode'+str(sys.flags.optimize)+'.reference.'+k)).read_bytes() for k in ('stdout','stderr')} for n in scripts}
 with tempfile.TemporaryDirectory(prefix='extremal-mathematics-') as td:
  p=Path(td)
  for n,raw in sources.items():(p/n).write_bytes(raw)
  for label,old,new,condition in MUTATIONS:
   source=sources['check_exact.py'].decode();need(source.count(old)==1,'one intended algebra mutation '+label)
   (p/(label+'.py')).write_text(source.replace(old,new))
  for f in p.iterdir():f.chmod(0o444)
  p.chmod(0o555)
  def snapshot():return {f.name:{'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in sorted(p.iterdir())}
  before=snapshot();denials=[]
  try:
   for f in [p,*sorted(p.iterdir())]:
    directory=f==p;need((f.stat().st_mode&0o777)==(0o555 if directory else 0o444) and not os.access(f,os.W_OK),'readonly fixture')
    try:fd=os.open(f/'FORBIDDEN_CREATE' if directory else f,os.O_WRONLY|(os.O_CREAT|os.O_EXCL if directory else os.O_APPEND),0o600)
    except PermissionError as e:need(e.errno==13,'physical EACCES');denials.append({'path':'.' if directory else f.name,'errno':13,'denied':True})
    else:os.close(fd);raise ValueError('write permitted')
   def run(case):
    label,n,args,condition=case
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
    r=subprocess.run([sys.executable,'-I','-S','-B',*mode,'-c',probe+LAUNCHER,n,*args],cwd=p,env=dict(PATH=os.defpath,HOME=str(p),TMPDIR=str(p),LC_ALL='C'),capture_output=True,timeout=120)
    envline,sep,body=r.stdout.partition(b'\n');need(sep and envline.startswith(b'ENV '),'child execution evidence')
    expected={'uid':1000,'euid':1000,'optimization':sys.flags.optimize,'directory_mode':'0o555','target_mode':'0o444','physical_denials':[{'operation':'create','errno':13,'denied':True},{'operation':'append_open','errno':13,'denied':True}]}
    need(same(json.loads(envline[4:]),expected),'exact child readonly evidence');need(envline==b'ENV '+json.dumps(expected,sort_keys=True).encode(),'complete child evidence format')
    row={'case':label,'script':n,'arguments':list(args),'exit_code':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode(),'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr),'environment':expected}
    if condition is None:
     need(r.returncode==0 and r.stderr==accepted[n]['stderr'] and body==accepted[n]['stdout'],'complete baseline equality '+n)
     need(same(json.loads(body),json.loads(accepted[n]['stdout'])),'recursive exact JSON types')
     j=json.loads(body);need(j['count']==(23 if n=='check_exact.py' else 41) and j['full_target_proved'] is False,'exact check count and scope')
     row.update(complete_reference_equality=True,recursive_exact_types=True)
    else:
     need(r.returncode==1 and body==b'','intended negative exit '+label)
     j=json.loads(r.stderr);need(j['status']=='fail' and type(j['error']) is str and (j['error']==condition if condition.startswith('intentional') else j['error'].startswith(condition+':')),'intended mathematical condition '+label+' '+str(j))
     need(set(j)==({'status','error'} if n!='audit_exact.py' else {'status','error','uid','euid'}),'exact rejection schema')
     if n=='audit_exact.py':need(type(j['uid']) is int and type(j['euid']) is int and j['uid']==j['euid']==1000,'independent rejection UID')
     need(r.stderr==(json.dumps(j)+'\n').encode(),'complete rejection JSON format');row.update(rejected=True,intended_condition=condition)
    return row
   cases=[('baseline-'+n,n,(),None) for n in scripts]
   cases += [('authored-'+label,label+'.py',(),condition) for label,old,new,condition in MUTATIONS]
   cases += [('independent-'+label,'audit_exact.py',('--mutant',label),condition) for label,condition in INDEPENDENT]
   cases += [('explicit-original-failure','check_exact.py',('--inject-failure',),'intentional explicit failure: optimization must not disable checks'),('explicit-independent-failure','audit_exact.py',('--inject-failure',),'intentional explicit failure')]
   with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:records=list(pool.map(run,cases))
   after=snapshot();need(after==before,'mathematical fixture changed')
  finally:
   p.chmod(0o755)
   for f in p.iterdir():f.chmod(0o644)
 need(all((root/n).read_bytes()==v for n,v in sources.items()),'accepted source changed')
 print(json.dumps({'schema':1,'problem_id':30005996,'status':'PASS','uid':os.getuid(),'euid':os.geteuid(),'optimization':sys.flags.optimize,'positive_runs':2,'mathematical_negative_controls':39,'authored_algebra_mutants':20,'independent_algebra_mutants':19,'explicit_failure_runs':2,'runs':records,'physical_denials':denials,'child_physical_denials':2*len(records),'before':before,'after':after,'fixture_unchanged':True,'source_unchanged':True,'normalization':'NONE','scope':'Exact algebra support only; mathematical and source-scope conclusions rest on the independent written audit.'},indent=2,sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,TypeError,KeyError,OSError,subprocess.TimeoutExpired) as e:print('REJECT: mathematical guard: '+str(e),file=sys.stderr);sys.exit(1)
