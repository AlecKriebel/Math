#!/usr/bin/env python3
"""Count unchanged authored diagnostics and reject intended mathematical mutants.

No downloaded companion is read or executed. Finite checks are not a proof.
"""
import collections,contextlib,hashlib,io,json,os,runpy,subprocess,sys
from pathlib import Path
EXPECTED_COUNTS={f'exact_check_{i:03d}':1 for i in range(1,36)}
EXPECTED_COUNTS.update(exact_check_008=40,exact_check_022=176,exact_check_023=176,exact_check_024=6,exact_check_025=6,exact_check_026=6,exact_check_027=3,**{f'exact_check_{i:03d}':12 for i in range(28,33)})
EMBEDDED_CONTROLS=['exact_check_009','exact_check_010','exact_check_011','exact_check_012','exact_check_020','exact_check_021']
INPUT_NAMES=['AUDIT.md','AUDIT_MANIFEST.json','EXACT_CHECK_RESULTS.json','README.md','SOURCE_METADATA.json','STATIC_FORMAL_INSPECTION.json','VERIFICATION_RECEIPT.json','independent_exact_checks.py','verify_audit_packet.py']
MUTANTS=[
 ('wrong_active_determinant','check(determinant(minor) == 64,','check(determinant(minor) == 65,','exact_check_003'),
 ('wrong_scale','check(feasible(v, x, 5, 3) and not in_lattice(x, 3),','check(feasible(v, x, 3, 3) and not in_lattice(x, 3),','exact_check_004'),
 ('hole_falsely_decomposable','check(not any(tuple(hj-xj for hj, xj in zip(h, x)) in lattice for x in lattice),','check(any(tuple(hj-xj for hj, xj in zip(h, x)) in lattice for x in lattice),','exact_check_015'),
 ('wrong_face_cardinality','== T and len(face) == 4,','== T and len(face) == 5,','exact_check_016'),
 ('wrong_fixed_contribution','check(fixed == [8, -4,','check(fixed == [7, -4,','exact_check_018'),
 ('neighbor_falsely_nondecomposable','check(any(tuple(hj-xj for hj, xj in zip(changed, x)) in lattice for x in lattice),','check(not any(tuple(hj-xj for hj, xj in zip(changed, x)) in lattice for x in lattice),','exact_check_020'),
 ('wrong_sharpness_determinant','check(abs(det) == 16,','check(abs(det) == 15,','exact_check_032'),
 ('wrong_resonance_row','check(tight == [0],','check(tight == [1],','exact_check_034')]
sha=lambda b:hashlib.sha256(b).hexdigest()
def need(ok,label):
 if not ok:raise ValueError(label)
def same(a,b):
 if type(a) is not type(b):return False
 if type(b) is dict:return set(a)==set(b) and all(same(a[k],v) for k,v in b.items())
 if type(b) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
def main():
 root=Path(__file__).resolve().parent
 need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000')
 need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'require -I -S -B')
 need(sorted(p.name for p in (root/'current').iterdir())==INPUT_NAMES,'exact nine input identities')
 def snapshot():return {n:dict(bytes=len(raw),sha256=sha(raw)) for n in INPUT_NAMES for raw in [(root/'current'/n).read_bytes()]}
 before=snapshot();physical=[]
 for p,label,create in [(root/'current','current',True),(root/'current/independent_exact_checks.py','current/independent_exact_checks.py',False)]:
  need(not p.stat().st_mode&0o222 and not os.access(p,os.W_OK),'read-only input mode')
  try:fd=os.open(p/'DENIED' if create else p,os.O_WRONLY|(os.O_CREAT|os.O_EXCL if create else os.O_APPEND),0o600)
  except PermissionError as exc:need(exc.errno==13,'EACCES required');physical.append(dict(path=label,operation='create' if create else 'append_open',errno=13,denied=True))
  else:os.close(fd);raise ValueError('physical write denial missing')
 script=root/'current/independent_exact_checks.py';counts=collections.Counter();output=io.StringIO();errors=io.StringIO()
 with contextlib.redirect_stdout(output),contextlib.redirect_stderr(errors):
  ns=runpy.run_path(str(script),run_name='authored_diagnostics');original=ns['check']
  def counted(condition,label):
   need(type(label) is str and label in EXPECTED_COUNTS,'unknown diagnostic identity')
   original(condition,label);counts[label]+=1
  ns['paley'].__globals__['check']=counted
  report={'status':'PASS','arithmetic':'exact integers and fractions only','external_companion_executed':False,'paley':ns['paley'](),'hole':ns['hole'](),'small_sign_matrix_classes':ns['small_signs'](),'sylvester_sharpness_samples':ns['sharp_examples'](),'smoothness_resonance':ns['resonance']()}
 need(output.getvalue()==errors.getvalue()=='','unexpected instrumented suite output')
 need(same(dict(counts),EXPECTED_COUNTS) and sum(counts.values())==496 and len(counts)==35,'exact positive diagnostic identities/counts')
 expected=(root/'current/EXACT_CHECK_RESULTS.json').read_bytes();raw=(json.dumps(report,indent=2)+'\n').encode()
 need(raw==expected and same(json.loads(raw),json.loads(expected)),'complete unchanged authored report and recursive types')
 source=script.read_text();mode=[] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize];env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C');runs=[]
 def run_program(program):return subprocess.run([sys.executable,'-I','-S','-B',*mode,'-c',program],cwd=root,env=env,capture_output=True,timeout=60)
 for label,old,new,identity in MUTANTS:
  need(source.count(old)==1,'unique mathematical mutation anchor '+label)
  program="from pathlib import Path\nimport sys\ns=Path('current/independent_exact_checks.py').read_text()\nold="+repr(old)+"\nnew="+repr(new)+"\nif s.count(old)!=1:raise SystemExit('REJECT: invalid mutation anchor')\ntry:\n exec(compile(s.replace(old,new,1),'<authored-mathematical-mutant>','exec'),{'__name__':'__main__'})\nexcept RuntimeError as exc:\n print('REJECT: '+str(exc),file=sys.stderr);sys.exit(1)\n"
  r=run_program(program);error=('REJECT: FAILED: '+identity+'\n').encode()
  need(type(r.returncode) is int and r.returncode==1 and r.stdout==b'' and r.stderr==error,'intended mathematical rejection '+label)
  runs.append(dict(control=label,category='finite_mathematics_mutation',condition=identity,exit_code=r.returncode,stdout=r.stdout.decode(),stderr=r.stderr.decode(),intended_rejection_verified=True))
 need(len(runs)==8 and len({x['control'] for x in runs})==8,'exact eight mathematical mutation identities')
 program="import runpy,sys\nns=runpy.run_path('current/independent_exact_checks.py')\ntry:\n ns['check'](False,'deliberate_false_condition')\nexcept RuntimeError as exc:\n print('REJECT: '+str(exc),file=sys.stderr);sys.exit(1)\n"
 r=run_program(program);need(r.returncode==1 and r.stdout==b'' and r.stderr==b'REJECT: FAILED: deliberate_false_condition\n','injected false-condition rejection')
 injected=dict(category='injected_failure_control',control='forced_false_condition',exit_code=r.returncode,stdout=r.stdout.decode(),stderr=r.stderr.decode())
 after=snapshot();need(after==before,'accepted inputs changed')
 print(json.dumps(dict(schema=1,problem_id=30000813,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,check_identities=35,check_invocations=496,check_counts=dict(counts),embedded_negative_predicate_controls=EMBEDDED_CONTROLS,semantic_mutants=8,finite_mathematics_mutants=8,injected_failure_controls=1,injected_failure=injected,runs=runs,physical_denials=physical,positive_report_bytes=len(raw),positive_report_sha256=sha(raw),whole_mathematics_unchanged=True,before=before,after=after,external_companion_executed=False,lean_build='NOT_RUN',limits='Finite diagnostics only; seventeen written arguments accepted separately. No downloaded companion execution.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,RuntimeError,subprocess.TimeoutExpired) as exc:print('REJECT: mathematical controls failed: '+str(exc),file=sys.stderr);sys.exit(1)
