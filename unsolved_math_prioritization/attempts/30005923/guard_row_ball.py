#!/usr/bin/env python3
"""Read-only bounded code-mutation controls for row-ball interfaces."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
def need(ok,message):
 if not ok:raise ValueError(message)
def main():
 need(len(sys.argv)==1,'no output arguments');need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000')
 need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'-I -S -B')
 source=Path(__file__).with_name('verify_row_ball.py').read_text();mode=[] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize]
 env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C');rows=[]
 mutations=[
  ('tuple count removed from ceiling','return (1+r*math.sqrt(g))**2','return (1+r*math.sqrt(1))**2','corrected_ceiling_exact'),
  ('all-g scope promoted',"'constant_uniform_in_g':False","'constant_uniform_in_g':True",'variable-count-scope'),
  ('positive logarithm sign reversed','(-1)**(n+1)*0.25**n/n','(-1)**n*0.25**n/n','log_plus_sign_numeric'),
  ('reciprocal determinant sign reversed','minuslog=sum(0.25**n/n','minuslog=-sum(0.25**n/n','inverse_determinant_log_sign_numeric'),
  ('second factor conjugation dropped','check(a*b.conjugate()==1','check(a*b==1','complex_conjugation_required'),
  ('covariance multiplicity collapsed','count=sum(rotation(v,j)==w for j in range(n))','count=int(any(rotation(v,j)==w for j in range(n)))','full_gaussian_covariance_sum_2'),
  ('covariance coefficient length factor dropped','Q(count,n*n)','Q(count,n)','full_gaussian_covariance_sum_2'),
  ('tail integration constant dropped','check(1+0==math.exp(0)','check(0==math.exp(0)','tail_constant_exact'),
  ('pure-power stabilizer collapsed','stabilizer=sum(rotation(w,j)==w for j in range(n))','stabilizer=1','periodic-word:'),
 ]
 for label,old,new,reason in mutations:
  need(source.count(old)==1,'unique mutant target '+label);altered=source.replace(old,new)
  r=subprocess.run([sys.executable,'-I','-S','-B',*mode,'-c',altered],env=env,capture_output=True,timeout=40)
  need(r.returncode==1 and r.stdout==b'','mutant accepted '+label)
  result=json.loads(r.stderr);need(result.get('status')=='FAIL' and reason in result.get('reason',''),'wrong rejection '+label)
  rows.append(dict(control=label,mutant_sha256=hashlib.sha256(altered.encode()).hexdigest(),exit_code=r.returncode,stdout=r.stdout.decode(),stderr=r.stderr.decode(),expected_reason=reason))
 arguments=[]
 for args in [['--output','FORBIDDEN'],['--packet','FORBIDDEN'],['unexpected']]:
  r=subprocess.run([sys.executable,'-I','-S','-B',*mode,'-c',source,*args],env=env,capture_output=True,timeout=40)
  need(r.returncode==1 and r.stdout==b'' and json.loads(r.stderr)=={'status':'FAIL','reason':'no-output-or-other-arguments'},'output argument accepted')
  arguments.append(dict(arguments=args,exit_code=r.returncode,stdout=r.stdout.decode(),stderr=r.stderr.decode()))
 print(json.dumps(dict(status='PASS',uid=os.getuid(),euid=os.geteuid(),proof_turns=0,optimization=sys.flags.optimize,code_mutants=rows,invalid_arguments=arguments,limits='Mutation-sensitive finite checks and scope guards; not a proof of infinite analytic assertions.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired) as e:print('REJECT: row-ball guard '+str(e),file=sys.stderr);sys.exit(1)
