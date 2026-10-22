#!/usr/bin/env python3
"""Deterministic isolated guard checks and actual mathematical code mutations."""
import ast,hashlib,json,os,subprocess,sys
from pathlib import Path

def need(ok,message):
 if not ok:raise ValueError(message)

def main():
 need(len(sys.argv)==1,'no arguments');need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000')
 need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'-I -S -B')
 source=Path('verify_conventions.py').read_bytes();before=hashlib.sha256(source).hexdigest()
 need(not any(isinstance(x,ast.Assert) for x in ast.walk(ast.parse(source))),'assertion-free mathematical checker')
 ns={'__name__':'guarded_mathematical_module'};exec(compile(source,'<guarded-mathematical-module>','exec'),ns)
 guards=[]
 def rejected(label,call,expected):
  try:call()
  except RuntimeError as e:
   need(str(e)==expected,'unexpected guard reason');guards.append(dict(control=label,rejected=True,exception='RuntimeError',message=str(e)))
  else:raise ValueError('invalid input accepted: '+label)
 for k in (-3,0,2,43,True):rejected('invalid order '+repr(k),lambda k=k:ns['change'](k),'not an odd integrable order')
 for sig in ((),[],tuple([-1]*7)):rejected('invalid signature '+repr(sig),lambda sig=sig:ns['expansion'](sig),'signature length guard')
 for g in (0,-1,True,1.0):rejected('invalid tail genus '+repr(g),lambda g=g:ns['power_tail_factor'](g),'invalid tail genus')
 flags=['-I','-S','-B']+([] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize]);env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C')
 # Read only the authored source on stdin, with fixed compile names. Full child
 # stdout/stderr are deterministic and retained without path normalization.
 driver="import sys\nraw=sys.stdin.buffer.read()\nexec(compile(raw, '<guarded-mathematical-checker>', 'exec'), {'__name__':'__main__'})\n"
 controls=[]
 def child(label,raw,args,reason):
  r=subprocess.run([sys.executable,*flags,'-c',driver,*args],input=raw,env=env,capture_output=True,timeout=200)
  need(type(r.returncode) is int and r.returncode==1 and r.stdout==b'','negative exit/stdout')
  need(r.stderr.endswith(('RuntimeError: '+reason+'\n').encode()),'negative stderr reason')
  controls.append(dict(control=label,exit_code=r.returncode,stdout=r.stdout.decode(),stderr=r.stderr.decode(),rejected=True,source_sha256=hashlib.sha256(raw).hexdigest()))
 child('command-line output arguments',source,['--output','forbidden.json'],'This verifier takes no arguments and never writes files.')
 replacements=[('altered OWR coefficient','(3,): {((-1,), (0,)): Q(1)}','(3,): {((-1,), (0,)): Q(2)}','OWR to DGY factor differs'),('constant per-tail factor','return 2 ** (2 * g - 1)','return 2','quadratic-power tail calibration'),('incremented star-bottom formula','    return value\n\n\ndef cycle_joinings','    return value + 1\n\n\ndef cycle_joinings','star bottom/cycle joining equality')]
 text=source.decode()
 for label,old,new,reason in replacements:
  need(text.count(old)==1,'unique mutation target');mutated=text.replace(old,new).encode();need(mutated!=source,'actual changed code');child(label,mutated,[],reason)
 need(Path('verify_conventions.py').read_bytes()==source,'mathematical checker changed')
 print(json.dumps(dict(schema=1,problem_id=30004710,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,source_sha256=before,guards=guards,code_and_argument_negative_controls=controls,actual_mathematical_mutation_count=3,source_unchanged=True,scope='Finite input guards and three deliberately altered mathematical programs; no geometric theorem certification.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,subprocess.TimeoutExpired) as e:print('REJECT: convention guard failed: '+str(e),file=sys.stderr);sys.exit(1)
