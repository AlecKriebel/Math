#!/usr/bin/env python3
"""Real mutations to finite mathematical computations, never stale-hash substitutes."""
import hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path
SPECS = [('omit_nonlinear_ambient_error', 'check_algebra.py', 'run_math.py', ', nc_mul(nc_mul(d, x), ds))', ')', ['test_ambient_error_identity']), ('dyadic_rectangle_without_square', 'check_algebra.py', 'run_math.py', 'return s * s', 'return s', ['test_finite_dyadic_rectangle']), ('omit_corner_complement', 'independent_checks.py', 'run_independent.py', 'lift=add(w,sub(eye(3),p))', 'lift=w', ['test_04_corner_lift_and_omitted_complement_negative']), ('retain_range_projection_typo', 'independent_checks.py', 'run_independent.py', 'correct=mm(s,star(s)); printed=', 'correct=mm(star(s),star(s)); printed=', ['test_06_range_projection_typo_is_genuinely_false']), ('forget_reverse_path_adjoint', 'independent_checks.py', 'run_independent.py', 'conjugate(star(u),y)', 'conjugate(u,y)', ['test_08_reverse_path_by_adjoint']), ('wrong_technical_rotation_sign', 'independent_checks.py', 'run_independent.py', 'good=block(n,m,neg(m),n); bad=', 'good=block(n,m,m,n); bad=', ['test_10_wrong_rotation_sign_is_not_unitary']), ('incorrect_delayed_sequence_index', 'independent_checks.py', 'run_independent.py', 'correct=sum(F(m[k-1]-m[k-2]) for k in range(1,5))', 'correct=sum(F(m[k]-1-(m[k]-2)) for k in range(1,5))', ['test_12_delayed_telescoping_indices']), ('drop_fixed_strict_margin', 'independent_checks.py', 'run_independent.py', 'self.assertLessEqual(s*s-F(1,16),F(15,16))', 'self.assertLessEqual(s*s,F(15,16))', ['test_13_fixed_dyadic_margin']), ('unitary_quotient_lift_upstairs', 'independent_checks.py', 'run_independent.py', 'w=(zero(2),eye(2))', 'w=(eye(2),eye(2))', ['test_11_quotient_unitary_lift_is_only_contractive_upstairs']), ('erase_annihilator_error', 'independent_checks.py', 'run_independent.py', 'phi=(eye(2),F(1)); psi=(eye(2),F(0))', 'phi=(eye(2),F(0)); psi=(eye(2),F(0))', ['test_03_multiplier_equality_without_ideal_difference_negative']), ('compress_unitary_as_identity', 'independent_checks.py', 'run_independent.py', 'u[0][0]**2', 'F(1)', ['test_05_compression_does_not_destabilize']), ('naive_initial_normalization', 'independent_checks.py', 'run_independent.py', 'y=conjugate(w,x)', 'y=conjugate(eye(2),x)', ['test_07_forcing_initial_unitary_one_changes_conjugacy'])]
def need(ok,label):
 if not ok:raise ValueError(label)
def main():
 need(len(sys.argv)==1,'no arguments');need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000');need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'require -I -S -B')
 root=Path(__file__).absolute().parent;names=['check_algebra.py','independent_checks.py','run_math.py','run_independent.py'];original={n:(root/n).read_bytes() for n in names};rows=[];flags=['-I','-S','-B']+([] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize])
 for name,source,runner,old,new,expected_tests in SPECS:
  text=original[source].decode();need(text.count(old)==(2 if name=='compress_unitary_as_identity' else 1),'exact mutation sites: '+name);raw=text.replace(old,new).encode()
  with tempfile.TemporaryDirectory(prefix='kk-semantic-') as tmp:
   td=Path(tmp);candidate='mutant_'+name+'.py';(td/candidate).write_bytes(raw);(td/runner).write_bytes(original[runner])
   for p in td.iterdir():p.chmod(0o444)
   td.chmod(0o555)
   try:
    probes=[]
    for target,op in [(td/'FORBIDDEN_CREATE','create'),(td/candidate,'append')]:
     try:fd=os.open(target,os.O_WRONLY|(os.O_CREAT|os.O_EXCL if op=='create' else os.O_APPEND),0o600)
     except PermissionError as e:need(e.errno==13,'physical EACCES');probes.append(dict(operation=op,denied=True,errno=13))
     else:os.close(fd);raise ValueError('write allowed')
    command=[sys.executable,*flags,runner,'--candidate',candidate];r=subprocess.run(command,cwd=td,env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C'),capture_output=True,timeout=120)
    need(r.returncode==1 and r.stderr==b'','mutant process did not reject: '+name);out=json.loads(r.stdout)
    need(out['status']=='FAIL' and out['errors']==0 and out['skipped']==0,'semantic failure required: '+name)
    failed=sorted(set(x['test'] for x in out['test_outcomes'] if x['status']=='FAIL'));need(failed==expected_tests,'intended mathematical rejection: '+name+' '+str(failed))
    need(all(x.get('error_type')=='AssertionError' for x in out['test_outcomes'] if x['status']=='FAIL'),'mathematical assertion rejection')
    need((td/candidate).read_bytes()==raw and (td/runner).read_bytes()==original[runner],'mutation fixture changed')
    rows.append(dict(mutation=name,source=source,mutation_old=old,mutation_new=new,command=['python',*flags,runner,'--candidate',candidate],exit_code=r.returncode,stdout=r.stdout.decode(),stderr=r.stderr.decode(),mutant_bytes=len(raw),mutant_sha256=hashlib.sha256(raw).hexdigest(),expected_failed_tests=expected_tests,actual_failed_tests=failed,actual_permission_denials=probes,semantic_failure_before_any_hash_comparison=True))
   finally:
    td.chmod(0o755)
    for p in td.iterdir():p.chmod(0o644)
 need(all((root/n).read_bytes()==original[n] for n in names),'original checkers changed')
 print(json.dumps(dict(schema=1,problem_id=30005199,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,source_hashes={n:hashlib.sha256(raw).hexdigest() for n,raw in original.items()},mutations=rows,mutation_count=len(rows),originals_unchanged=True,scope='Actual finite mathematical computation mutations; not stale-hash failures and not analytic certification'),indent=2,sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,subprocess.TimeoutExpired) as e:print('REJECT: semantic mutation runner: '+str(e),file=sys.stderr);sys.exit(1)
