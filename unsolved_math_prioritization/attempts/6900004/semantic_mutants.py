#!/usr/bin/env python3
"""Run six real source mutations of the independent checker in temporary copies."""
import hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path
SPECS=[
 ('reverse_ratio','(p[v][0]-p[u][0])/(q[v][0]-q[u][0])','(q[v][0]-q[u][0])/(p[v][0]-p[u][0])','transported vector not equilibrium'),
 ('omit_ratio','(p[v][0]-p[u][0])/(q[v][0]-q[u][0])','Q(1)','transported vector not equilibrium'),
 ('negative_ratio','(p[v][0]-p[u][0])/(q[v][0]-q[u][0])','-(p[v][0]-p[u][0])/(q[v][0]-q[u][0])','sign-preserving invertibility'),
 ('erase_zero_sign','return (x > 0) - (x < 0)','return 1 if x == 0 else (x > 0) - (x < 0)','accepted semantic mutant: allow zero-to-positive coordinate'),
 ('zero_singleton_witness','unit=tuple(Q(k==j) for k in range(len(edges)))','unit=tuple(Q(0) for k in range(len(edges)))','separated singleton retained'),
 ('same_force_both_endpoints','p[u][r]-p[i][r] if i==v else Q(0)','p[i][r]-p[u][r] if i==v else Q(0)','cycle-space nullity'),
]
def need(ok,label):
 if not ok:raise ValueError(label)
def main():
 need(len(sys.argv)==1,'no arguments');need(os.getuid()==os.geteuid()==1000,'UID 1000');need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'isolated no-site no-bytecode')
 root=Path(__file__).absolute().parent; original=(root/'independent_kernel_check.py').read_bytes(); source=original.decode(); rows=[]; flags=['-I','-S','-B']+([] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize])
 for name,old,new,reason in SPECS:
  need(source.count(old)==1,'unique mutation site');raw=source.replace(old,new).encode()
  with tempfile.TemporaryDirectory(prefix='tensegrity-mutation-') as tmp:
   td=Path(tmp);n='mutant_'+name+'.py';p=td/n;p.write_bytes(raw);p.chmod(0o444);td.chmod(0o555)
   try:
    probes=[]
    for target,op in [(td/'FORBIDDEN_CREATE','create'),(p,'append')]:
     try:fd=os.open(target,os.O_WRONLY|(os.O_CREAT|os.O_EXCL if op=='create' else os.O_APPEND),0o600)
     except PermissionError as e:need(e.errno==13,'EACCES');probes.append({'operation':op,'denied':True,'errno':13})
     else:os.close(fd);raise ValueError('write allowed')
    command=[sys.executable,*flags,n];r=subprocess.run(command,cwd=td,env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C'),capture_output=True,timeout=120)
    need(r.returncode==1 and r.stderr==b'','mutation process did not reject');need(json.loads(r.stdout)=={'status':'FAIL','reason':reason},'specific mutation reason');need(p.read_bytes()==raw,'mutant unchanged')
    rows.append({'mutation':name,'command':command,'exit_code':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode(),'mutant_bytes':len(raw),'mutant_sha256':hashlib.sha256(raw).hexdigest(),'expected_reason':reason,'actual_permission_denials':probes})
   finally:td.chmod(0o755);p.chmod(0o644)
 need((root/'independent_kernel_check.py').read_bytes()==original,'original checker changed')
 print(json.dumps({'schema':1,'status':'PASS','uid':os.getuid(),'euid':os.geteuid(),'optimization':sys.flags.optimize,'source_sha256':hashlib.sha256(original).hexdigest(),'mutations':rows,'mutation_count':len(rows),'original_unchanged':True,'scope':'Mutation guards only, not universal proof or author intent'},indent=2,sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,subprocess.TimeoutExpired) as e:print('REJECT: semantic mutation runner: '+str(e),file=sys.stderr);sys.exit(1)
