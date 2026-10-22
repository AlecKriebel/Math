#!/usr/bin/env python3
"""Fresh classified semantic controls; no source-body or old-report replay."""
import hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path
EXPECTED_ERRORS = {'wrong_corner_defect': 'REJECTED: corner defect 2pi minus three interior angles\n', 'wrong_Q_sign': 'REJECTED: signed Gauss-Bonnet coefficient identity F=3\n', 'wrong_edge_norm': 'REJECTED: two sheet conormal norm one\n', 'wrong_catenoid_scale': 'REJECTED: catenoid scale at junction\n', 'reverse_circle_curvature': 'REJECTED: circle curvature signed inward\n', 'duplicate_catenoid_sheet': 'REJECTED: inward sheet conormals from catenoid derivatives\n', 'nonminimal_ode': 'REJECTED: all-parameter catenoid ODE Laurent identity\n', 'discard_cell_transport': 'REJECTED: local example blocks a purely local nonpositive-sign inference\n', 'wrong_stellar_increment': 'REJECTED: stellar dual incidence increment\n', 'wrong_count_threshold': 'REJECTED: first single-insertion count threshold\n', 'wrong_decoration_count': 'REJECTED: full decoration global corner count\n', 'noncompact_dilation': 'REJECTED: dilation hypothesis guard\n', 'unproved_uniform_bound': 'REJECTED: uniform curvature estimate remains a hypothesis\n', 'claim_global_realization': 'REJECTED: no realization from local or counting checks\n', 'erase_simple_scope': 'REJECTED: restricted simple-cell scope and unresolved target\n', 'resolve_two_face_note': 'REJECTED: restricted simple-cell scope and unresolved target\n'}
SCOPE_GUARDS = {'discard_cell_transport','noncompact_dilation','unproved_uniform_bound','claim_global_realization','erase_simple_scope','resolve_two_face_note'}
sha=lambda b:hashlib.sha256(b).hexdigest()
def need(ok,message):
 if not ok:raise ValueError(message)
def main():
 root=Path(__file__).resolve().parent
 need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000')
 need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'-I -S -B')
 files=sorted(str(p.relative_to(root)) for d in ['current','audit'] for p in (root/d).iterdir())
 def snapshot():return {n:dict(bytes=len(b),sha256=sha(b)) for n in files for b in [(root/n).read_bytes()]}
 before=snapshot();physical=[]
 for d in ['current','audit']:
  for p,label,create in [(root/d,d,True),(root/d/('CLAIMS.json' if d=='current' else 'AUDIT.md'),d+'/sample',False)]:
   need(not p.stat().st_mode&0o222 and not os.access(p,os.W_OK),'read-only mode')
   try:fd=os.open(p/'DENIED' if create else p,os.O_WRONLY|(os.O_CREAT|os.O_EXCL if create else os.O_APPEND),0o600)
   except PermissionError as exc:need(exc.errno==13,'EACCES required');physical.append(dict(path=label,operation='create' if create else 'append_open',errno=13,denied=True))
   else:os.close(fd);raise ValueError('physical denial missing')
 mode=[] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize];env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C');runs=[]
 for mutant,error in EXPECTED_ERRORS.items():
  r=subprocess.run([sys.executable,'-I','-S','-B',*mode,'audit/check_independent.py','--require-readonly','--mutant',mutant],cwd=root,env=env,capture_output=True,timeout=100)
  need(r.returncode==1 and r.stdout==b'' and r.stderr==error.encode(),'wrong semantic rejection '+mutant)
  runs.append(dict(control=mutant,category='hypothesis_status_guard' if mutant in SCOPE_GUARDS else 'geometry_algebra',exit_code=r.returncode,stdout=r.stdout.decode(),stderr=r.stderr.decode(),intended_rejection_verified=True))
 after=snapshot();need(after==before,'protected mathematics changed')
 print(json.dumps(dict(schema=1,problem_id=5900021,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,semantic_mutants=16,geometry_algebra_mutants=10,hypothesis_status_guards=6,physical_denials=physical,runs=runs,before=before,after=after,whole_mathematics_unchanged=True,limitations='Ten geometric/algebraic rejections and six hypothesis/status guards; not a proof of analytic theorems or global realization.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired) as exc:print('REJECT: semantic controls failed: '+str(exc),file=sys.stderr);sys.exit(1)
