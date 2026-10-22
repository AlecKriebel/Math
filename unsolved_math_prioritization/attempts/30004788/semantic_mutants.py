#!/usr/bin/env python3
"""Exercise every documented semantic mutation of both unchanged exact checkers."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
SPECS={
 'check_exact.py':[
  ('split_jordan','repeated-root quotient wrongly split'),
  ('merge_orbits','incorrect orbit stabilizer dimensions'),
  ('equal_fitting','Fitting ideals wrongly identified'),
  ('drop_factor','central support factor omitted')],
 'independent_exact.py':[
  ('split_jordan','Jordan nonzero nilpotent'),
  ('merge_orbits','full affine stabilizer equations'),
  ('drop_affine_constant','full affine stabilizer equations'),
  ('equal_fitting','distinct first Fitting ideals'),
  ('wrong_syzygy','presentation syzygy'),
  ('invert_nilpotent','Laurent localization unit witness'),
  ('drop_polynomial_factor','polynomial substitution zero factor')]
}
def need(ok,message):
 if not ok:raise ValueError(message)
def main():
 need(len(sys.argv)==1,'no arguments');need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000');need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'-I -S -B')
 root=Path(__file__).absolute().parent;names=['semantic_case.py',*SPECS];before={n:(root/n).read_bytes() for n in names};rows=[];probes=[]
 for n in names:
  p=root/n;need((p.stat().st_mode&0o777)==0o444,'readonly script')
  try:fd=os.open(p,os.O_WRONLY|os.O_APPEND)
  except PermissionError as e:need(e.errno==13,'EACCES');probes.append(dict(path=n,operation='append_open',errno=13,denied=True))
  else:os.close(fd);raise ValueError('append allowed')
 need((root.stat().st_mode&0o777)==0o555,'readonly directory')
 try:fd=os.open(root/'FORBIDDEN_CREATE',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
 except PermissionError as e:need(e.errno==13,'EACCES');probes.append(dict(path='.',operation='create',errno=13,denied=True))
 else:os.close(fd);raise ValueError('create allowed')
 flags=['-I','-S','-B']+([] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize])
 for script,cases in SPECS.items():
  for mutant,reason in cases:
   command=[sys.executable,*flags,'semantic_case.py',script,mutant]
   r=subprocess.run(command,cwd=root,env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C'),capture_output=True,timeout=120)
   expected=('SEMANTIC_REJECTION: '+reason+'\n').encode()
   need(type(r.returncode) is int and r.returncode==1 and r.stdout==b'' and r.stderr==expected,'complete intended semantic rejection: '+script+' '+mutant)
   rows.append(dict(script=script,mutation=mutant,expected_reason=reason,command=command,exit_code=r.returncode,stdout=r.stdout.decode(),stderr=r.stderr.decode(),full_stdout_stderr_equal_expected=True))
 after={n:(root/n).read_bytes() for n in names};need(after==before,'source bytes changed')
 pins={n:dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()) for n,raw in before.items()}
 print(json.dumps(dict(schema=1,problem_id=30004788,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,source_pins_before=pins,source_pins_after=pins,source_bytes_unchanged=True,mutation_count=len(rows),mutations=rows,physical_denials=probes,scope='All documented semantic mutants of unchanged mathematical code; bounded checks only.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,subprocess.TimeoutExpired) as e:print('REJECT: semantic runner: '+str(e),file=sys.stderr);sys.exit(1)
