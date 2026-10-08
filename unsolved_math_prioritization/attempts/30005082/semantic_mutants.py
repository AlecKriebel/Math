#!/usr/bin/env python3
"""Ten actual mathematical source mutations, checked independently before hashing."""
import hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
SPECS = [('max_replaced_with_min', "if mode=='min' else max(a,b)", "if mode=='min' else min(a,b)", 'candidate tropical maps'), ('drop_factor_negation', 'min(factor_sign*(v[1]+v[3]),factor_sign*v[4])', 'min(v[1]+v[3],v[4])', 'candidate factor signs'), ('reverse_direction_sign', 'out[0]-=direction*m', 'out[0]+=direction*m', 'candidate factor signs'), ('remove_difference_factor', 'out[0]+=min(0,d,-d)', 'out[0]+=0', 'candidate difference factor'), ('swap_wrong_cardinality', 'sum(j<=ell for j in I)==1', 'sum(j<=ell for j in I)==2', 'candidate block exponents'), ('misorient_diagonals', 'j-i==d', 'j+i==d', 'candidate rectangle rule'), ('miscount_semigroup', 'answer.append(len(values))', 'answer.append(len(values)+1)', 'candidate Hilbert'), ('lower_all_nonzero_ranks', 'return i\n', 'return max(0,i-1)\n', 'candidate block ranks'), ('incorrect_exchange_sign', '[(1,(2,3,6),(4,5,6)),(1,(2,5,6),(3,4,6)),(-1,(2,4,6),(3,5,6))]', '[(1,(2,3,6),(4,5,6)),(-1,(2,5,6),(3,4,6)),(-1,(2,4,6),(3,5,6))]', 'Square exchange polynomial identity failed'), ('choose_maximum_determinant', 'return scores[0][1]', 'return scores[-1][1]', 'candidate coherent minima')]
def need(ok,label):
 if not ok:raise ValueError(label)
def main():
 need(len(sys.argv)==1,'no arguments');need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000');need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'require -I -S -B')
 root=Path(__file__).absolute().parent;names=['check_math.py','independent_checks.py','run_independent.py'];original={n:(root/n).read_bytes() for n in names};source=original['check_math.py'].decode();rows=[];flags=['-I','-S','-B']+([] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize])
 for name,old,new,reason in SPECS:
  need(source.count(old)==1,'unique mutation site');raw=source.replace(old,new).encode()
  with tempfile.TemporaryDirectory(prefix='grassmannian-semantic-') as tmp:
   td=Path(tmp);candidate='mutant_'+name+'.py';(td/candidate).write_bytes(raw)
   for n in names[1:]:(td/n).write_bytes(original[n])
   for p in td.iterdir():p.chmod(0o444)
   td.chmod(0o555)
   try:
    probes=[]
    for target,op in [(td/'FORBIDDEN_CREATE','create'),(td/candidate,'append')]:
     try:fd=os.open(target,os.O_WRONLY|(os.O_CREAT|os.O_EXCL if op=='create' else os.O_APPEND),0o600)
     except PermissionError as e:need(e.errno==13,'physical EACCES');probes.append(dict(operation=op,denied=True,errno=13))
     else:os.close(fd);raise ValueError('write allowed')
    command=[sys.executable,*flags,'run_independent.py','--candidate',candidate]
    r=subprocess.run(command,cwd=td,env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C'),capture_output=True,timeout=120)
    expected=dict(status='FAIL',error_type='CheckFailure' if name=='incorrect_exchange_sign' else 'AuditFailure',reason=reason)
    need(r.returncode==1 and r.stderr==b'','mutation process did not reject')
    need(r.stdout==(json.dumps(expected,sort_keys=True)+'\n').encode(),'specific semantic rejection bytes')
    need((td/candidate).read_bytes()==raw and all((td/n).read_bytes()==original[n] for n in names[1:]),'mutation fixture changed')
    rows.append(dict(mutation=name,command=['python',*flags,'run_independent.py','--candidate',candidate],exit_code=r.returncode,stdout=r.stdout.decode(),stderr=r.stderr.decode(),mutant_bytes=len(raw),mutant_sha256=hashlib.sha256(raw).hexdigest(),expected_reason=reason,actual_permission_denials=probes))
   finally:
    td.chmod(0o755)
    for p in td.iterdir():p.chmod(0o644)
 need(all((root/n).read_bytes()==original[n] for n in names),'original checkers changed')
 print(json.dumps(dict(schema=1,problem_id=30005082,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,source_sha256=hashlib.sha256(original['check_math.py']).hexdigest(),mutations=rows,mutation_count=len(rows),originals_unchanged=True,scope='Actual code mutation guards, not stale-hash failures or a global proof'),indent=2,sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,subprocess.TimeoutExpired) as e:print('REJECT: semantic mutation runner: '+str(e),file=sys.stderr);sys.exit(1)
