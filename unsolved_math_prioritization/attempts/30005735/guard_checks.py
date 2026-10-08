#!/usr/bin/env python3
"""Fresh exact-output and intended mathematical-mutation guards. Standard library only."""
import hashlib,json,os,stat,subprocess,sys,tempfile
from fractions import Fraction as F
from pathlib import Path

def need(ok,label):
 if not ok:raise ValueError(label)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def same(a,b):
 if type(a) is not type(b):return False
 if type(a) is dict:return set(a)==set(b) and all(same(a[k],b[k]) for k in a)
 if type(a) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b

def exact_flat_output(raw):
 data=json.loads(raw);rows=data['checks']['flat_scanning']
 need(type(rows) is list and len(rows)==5,'flat-scanning rows')
 for row,N in zip(rows,(1,2,4,8,16)):
  es=[F(1,2**(n+6)) for n in range(N)]
  expected={'number_of_pulses':N,'initial_TV_h':str(2*sum(es,F(0))),
   'spacing_TV_at_positive_time':str(2*N+2*sum(es,F(0))),
   'spacing_L1_change_at_t_1':str(2*sum((F(4,5)*e-e*e/20 for e in es),F(0)))}
  need(same(row,expected),'flat-scanning exact rational result')
 return True

def main():
 need(len(sys.argv)==1,'no arguments');need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000')
 need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'-I -S -B')
 root=Path(__file__).resolve().parent;mode=[] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize]
 sources={n:(root/n).read_bytes() for n in ('check_calculations.py','audit_exact.py')}
 accepted={n:(root/n).read_bytes() for n in ('CALCULATION_RESULTS.json','EXACT_AUDIT_RESULTS.json')}
 exact_flat_output(accepted['CALCULATION_RESULTS.json'])
 fixtures=[('reversed_upwind',{'scheme_sign':'-1'},'route1 velocity maximum principle'),
 ('wrong_transmission_polynomial',{'H_linear_coefficient':'1'},'route2 transmitted root bracket'),
 ('incoming_wave_exits_scanning',{'alpha_delta_ratio':'2'},'route2 right scanning feasibility'),
 ('lost_pulse_memory',{'pulse_final_ratio':'0'},'route3 retained memory at pulse return'),
 ('wrong_entropy_cross_sign',{'entropy_cross_sign':'-1'},'route4 mixed-derivative identity'),
 ('wrong_increasing_shock_direction',{'up_speed_sign':'1'},'route5 increasing-edge Rankine-Hugoniot'),
 ('wrong_decreasing_shock_speed',{'down_speed_factor':'-1'},'route5 decreasing-edge Rankine-Hugoniot'),
 ('wrong_contact_excursion_sign',{'contact_velocity_sign':'1'},'stationary contact viscosity equation')]
 records=[]
 with tempfile.TemporaryDirectory(prefix='traffic-mathematics-') as td:
  p=Path(td)
  for n,raw in sources.items():(p/n).write_bytes(raw)
  for label,config,_ in fixtures:(p/(label+'.json')).write_text(json.dumps(config,sort_keys=True)+'\n')
  mutations=[('doubled_H','check_calculations.py','H=2*float(a)/(2+sqrt(4-float(a)))','H=4*float(a)/(2+sqrt(4-float(a)))'),
   ('float_increment','audit_exact.py','dv=f(2+e)-f(2)','dv=float(f(2+e)-f(2))'),
   ('historical_float_contamination','check_calculations.py','f=lambda r:F(r)-F(r)*F(r)/20','f=lambda r:r-r*r/20')]
  for label,n,old,new in mutations:
   s=sources[n].decode();need(s.count(old)==1,'unique mutation target '+label)
   (p/(label+'.py')).write_text(s.replace(old,new))
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
    launcher="import sys; code=open("+repr(n)+",'rb').read(); sys.argv=["+repr(n)+"]+sys.argv[1:]; exec(compile(code,"+repr('<traffic-'+label+'>')+",'exec'), {'__name__':'__main__'})"
    r=subprocess.run([sys.executable,'-I','-S','-B',*mode,'-c',launcher,*args],cwd=p,env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C'),capture_output=True,timeout=30)
    row={'case':label,'script':n,'exit_code':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode(),'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr)}
    records.append(row);return r,row
   for n,res in [('check_calculations.py','CALCULATION_RESULTS.json'),('audit_exact.py','EXACT_AUDIT_RESULTS.json')]:
    r,row=run('baseline-'+n,n);need(r.returncode==0 and r.stderr==b'' and r.stdout==accepted[res],'full baseline stdout/stderr')
    need(same(json.loads(r.stdout),json.loads(accepted[res])),'recursive exact baseline JSON types')
    row.update(complete_reference_equality=True,recursive_exact_types=True)
   for label,config,condition in fixtures:
    r,row=run(label,'audit_exact.py',('--fixture',label+'.json'))
    need(r.returncode==1 and r.stdout==b'' and r.stderr==('verification failed: '+condition+'\n').encode(),'intended condition '+label)
    row.update(rejected=True,intended_condition=condition)
   r,row=run('doubled_H','doubled_H.py');condition='check_5: abs(f_local(3+H)+H-(3+float(a)))<1e-13'
   need(r.returncode==1 and r.stdout==b'' and r.stderr.endswith(('ValueError: '+condition+'\n').encode()),'doubled H intended condition')
   row.update(rejected=True,intended_condition=condition)
   r,row=run('float_increment','float_increment.py');condition='route5 rational arithmetic type'
   need(r.returncode==1 and r.stdout==b'' and r.stderr==('verification failed: '+condition+'\n').encode(),'float increment intended condition')
   row.update(rejected=True,intended_condition=condition)
   r,row=run('historical_float_contamination','historical_float_contamination.py')
   need(r.returncode==0 and r.stderr==b'','float contamination reproduces unchecked successful exit')
   try:exact_flat_output(r.stdout)
   except ValueError as e:need(str(e)=='flat-scanning exact rational result','specific exact rational guard');row.update(rejected=True,intended_condition=str(e),rejection_layer='independent semantic output guard; mutated small checker itself exited 0')
   else:raise ValueError('float contamination escaped independent semantic guard')
   after=snapshot();need(after==before,'mathematical fixture changed')
  finally:
   p.chmod(0o755)
   for f in p.iterdir():f.chmod(0o644)
 need(all((root/n).read_bytes()==v for n,v in sources.items()),'accepted source changed')
 print(json.dumps({'schema':1,'problem_id':30005735,'status':'PASS','uid':os.getuid(),'euid':os.geteuid(),'optimization':sys.flags.optimize,'positive_runs':2,'mathematical_negative_controls':11,'runs':records,'physical_denials':denials,'before':before,'after':after,'fixture_unchanged':True,'source_unchanged':True,'normalization':'NONE','historical_replay':'NOT_RUN','scope':'Current exact rational output and explicit mutated-input regressions; historical original checker excluded, analytic PDE proofs not certified.'},indent=2,sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,TypeError,KeyError,OSError,subprocess.TimeoutExpired) as e:print('REJECT: mathematical guard: '+str(e),file=sys.stderr);sys.exit(1)
