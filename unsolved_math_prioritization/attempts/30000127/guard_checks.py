#!/usr/bin/env python3
"""Intended mathematical rejection controls, distinct from successful baselines."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
EXPECTED_ERRORS = {'current/verify_algebra.py': {'alter_collision_rate': 'ValueError: microscopic signed-spin flux: nonzero residual -(-rho + u + 1)*(rho + u - 1)/2\n', 'reverse_entropy_flux': 'ValueError: affine entropy flux: nonzero residual -2*c*(-c**2 + c*u + rho)\n', 'omit_mixed_derivative': 'ValueError: viscous weighted derivative equation: nonzero residual 2*nu*p*(-a*bp + b*bp + p*q - q**2)/(a - b)**3\n'}, 'current/audit_checks.py': {'wrong_face_flux': 'ValueError: face flux: residual -k + u\n', 'reverse_cone': 'ValueError: backward cone sign\n', 'drop_viscous_cross': 'ValueError: weighted physical viscosity: residual 2*nu*p*(-a*bp + b*bp + p*q - q**2)/(a - b)**3\n', 'wrong_third_jet': 'ValueError: jet second derivative: residual -1\n', 'assume_kernel_exact': 'ValueError: discrete kernel mass: residual (14*ell**2 - 5)/(96*ell**6)\n'}}
EXPECTED_POSITIVE = {'current/audit_checks.py': {'checks': ['equilibrium_currents_from_three_transitions', 'global_coordinate_polynomial_certificates', 'full_entropy_branches_scalar_faces_and_zero_limit', 'rectangle_signs_and_cone_orientation', 'independent_physical_viscosity_Riccati_and_strict_jet', 'non_attractiveness_rings', 'source_kernel_nonunit_mass_and_uniform_bound_controls', 'Hopf_Lax_order_truncations_and_sharp_fan_slope'], 'count': 8, 'limitations': 'Symbolic identities and finite witnesses only; analytic and probabilistic proofs are audited in INDEPENDENT_AUDIT.md.', 'mutation': 'none', 'status': 'passed'}, 'current/verify_algebra.py': {'checks': ['microscopic_expected_fluxes', 'coordinates_speeds_and_boundary_grid', 'affine_entropies_and_scalar_face_reductions', 'natural_order_non_attractiveness_witness', 'reachable_block_rectangle_obstruction', 'inviscid_weighted_Riccati_identities', 'viscous_cross_term_and_positive_maximum_jet', 'initial_entropy_non_continuity_witness'], 'count': 8, 'mutation': 'none', 'status': 'passed', 'stirring_path_length': 30}}
INPUT_PINS = {'current/ACCEPTANCE.json': {'bytes': 3902, 'sha256': '702bc9c75cbb55d2d59523687d2708a6bfc900c724110dd43560a8f3f47076a1'}, 'current/APPROACHES.json': {'bytes': 3976, 'sha256': 'dee4c6d0e181d02279925fb9968eabfd320e88f719ff2e735e591323c6304f71'}, 'current/AUDIT_EVIDENCE.json': {'bytes': 28731, 'sha256': 'f7408237ea4dff08b21117f25edbc63eee271f9358d45c78a992929912b3fed2'}, 'current/CORRECTION.patch': {'bytes': 7110, 'sha256': '7145e10ffc547e3c148b38103647189e6a6cdc1349e0c07162ddb7e92c2cd9bf'}, 'current/EXACT_TARGET.md': {'bytes': 7177, 'sha256': '4d68e2b5df373bee73640e2f6f2980f0f68b7370df21aaf89e65c5229ed6a281'}, 'current/INDEPENDENT_AUDIT.md': {'bytes': 21289, 'sha256': '7db1ab882c3002d06d8e2cf02b005b073a8bf34e8f12b6c02d876c72d247c70a'}, 'current/MANIFEST.json': {'bytes': 2912, 'sha256': '640fe655455a60ef1c6e4238a55582da437d8ee9445053968a1ebc88b4f88004'}, 'current/ORIGINAL_MANIFEST.json': {'bytes': 1550, 'sha256': '6e5176946e05030e4ef98dd96123036e57433c080c3e7b9207bda7812a82cc31'}, 'current/README.md': {'bytes': 2162, 'sha256': '6e01660aaf644aa0759534b0d2355a443a95a17997440657a4794dc1c7584391'}, 'current/REPORT.md': {'bytes': 18069, 'sha256': '8319890368d954d25e4aa30c9e2cbd87703bb54f74c304b2c0bfa5c3b2a1a399'}, 'current/SOURCE_INSPECTION.json': {'bytes': 4854, 'sha256': 'a8b47df269c1ebab869a245b5560de321ec029f2628df2760d32606a9798edbb'}, 'current/SOURCE_METADATA.json': {'bytes': 4551, 'sha256': '939831f7bd525f4d6490bf9d076d798476cdb893dfc14d3337ef150c015641c1'}, 'current/SOURCE_SCOPE_AUDIT.md': {'bytes': 3418, 'sha256': '240d898eeafb413f021353c15544f87ab6363ac93f2fe4a1e779252c494b90e3'}, 'current/VERIFICATION.json': {'bytes': 4793, 'sha256': '249bb3f6a726a2ef192dfc602344cfe33faa3a1c31cda65946b360fe42c804d9'}, 'current/audit_checks.py': {'bytes': 8446, 'sha256': 'dc727896589733947e62048df2f05fb788c1acd286282bb8571a5e725f22581e'}, 'current/run_audit.py': {'bytes': 5761, 'sha256': 'a1575fabfed84f8bc05b9d76677855a14128ea413caa2ba26a793ed5dabb9290'}, 'current/verify_algebra.py': {'bytes': 6860, 'sha256': '187d369f0482bc021e3a2d7bb85f89e36854ff98b2d9281648d1dd76c23b5dbd'}}
REFERENCE_PIN = {'bytes': 10137, 'sha256': 'a44a66e352e2d1db0899cd146fe46c7858074e10ff3ee1028ca6942cffd7dae1'}
sha=lambda b:hashlib.sha256(b).hexdigest()
def need(ok,message):
 if not ok:raise ValueError(message)
def same(a,b):
 if type(a) is not type(b):return False
 if type(b) is dict:return set(a)==set(b) and all(same(a[k],v) for k,v in b.items())
 if type(b) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
def main():
 root=Path(__file__).resolve().parent
 need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000')
 need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'-I -S -B')
 files=sorted(str(p.relative_to(root)) for p in (root/'current').iterdir())
 need(files==sorted(INPUT_PINS) and len(files)==17,'exact accepted input identities')
 def snapshot():return {n:dict(bytes=len(b),sha256=sha(b)) for n in files for b in [(root/n).read_bytes()]}
 before=snapshot();need(same(before,INPUT_PINS),'accepted input pins');physical=[]
 for p,label,create in [(root/'current','current',True),(root/'current/audit_checks.py','current/audit_checks.py',False)]:
  need(not p.stat().st_mode&0o222 and not os.access(p,os.W_OK),'read-only mode')
  try:fd=os.open(p/'DENIED' if create else p,os.O_WRONLY|(os.O_CREAT|os.O_EXCL if create else os.O_APPEND),0o600)
  except PermissionError as exc:need(exc.errno==13,'EACCES required');physical.append(dict(path=label,operation='create' if create else 'append_open',errno=13,denied=True))
  else:os.close(fd);raise ValueError('physical denial missing')
 raw=(root/'CHECKER_REFERENCES.json').read_bytes();need(same(dict(bytes=len(raw),sha256=sha(raw)),REFERENCE_PIN),'fixed raw checker references')
 references=json.loads(raw);need(set(references)=={'schema','problem_id','stage','modes'} and type(references['schema']) is int and references['schema']==1 and type(references['problem_id']) is int and references['problem_id']==30000127 and set(references['modes'])=={'0','1','2'},'reference schema')
 expected_ids=[(s,m) for s in ('current/verify_algebra.py','current/audit_checks.py') for m in ['none',*EXPECTED_ERRORS[s]]]
 for rows in references['modes'].values():
  need(type(rows) is list and [(r['script'],r['mutation']) for r in rows]==expected_ids and len(rows)==10,'exact reference identities/counts')
  for r in rows:
   need(set(r)=={'script','mutation','exit_code','stdout','stderr'} and type(r['exit_code']) is int and type(r['stdout']) is str and type(r['stderr']) is str,'reference row exact types')
   if r['mutation']=='none':need(r['exit_code']==0 and r['stderr']=='' and same(json.loads(r['stdout']),EXPECTED_POSITIVE[r['script']]),'exact positive family identity/count')
   else:need(r['exit_code']==1 and r['stdout']=='' and r['stderr']==EXPECTED_ERRORS[r['script']][r['mutation']],'intended rejection reference')
 mode=[] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize];env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C');runs=[]
 for ref in references['modes'][str(sys.flags.optimize)]:
  if ref['mutation']=='none':continue
  r=subprocess.run([sys.executable,'-I','-S','-B',*mode,'NO_SITE_RUNNER.py',ref['script'],'--mutation',ref['mutation']],cwd=root,env=env,capture_output=True,timeout=150)
  need(type(r.returncode) is int and r.returncode==1 and r.stdout==ref['stdout'].encode() and r.stderr==ref['stderr'].encode(),'full raw intended rejection equality '+ref['mutation'])
  need(r.stderr.decode()==EXPECTED_ERRORS[ref['script']][ref['mutation']],'intended mathematical reason')
  record=dict(script=ref['script'],mutation=ref['mutation'],exit_code=r.returncode,stdout=r.stdout.decode(),stderr=r.stderr.decode())
  need(same(record,ref),'recursive exact rejection types/values')
  runs.append(dict(control=ref['script']+':'+ref['mutation'],category='finite_mathematics',**record,intended_rejection_verified=True,full_raw_output_equal=True,recursive_exact_json_equal=True))
 need([(r['script'],r['mutation']) for r in runs]==[(s,m) for s,m in expected_ids if m!='none'] and len(runs)==8,'exact eight rejection identities')
 after=snapshot();need(same(after,before),'protected mathematics changed')
 print(json.dumps(dict(schema=1,problem_id=30000127,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,semantic_mutants=8,physical_denials=physical,runs=runs,before=before,after=after,whole_mathematics_unchanged=True,limitations='Eight named finite-mathematics rejections only; successful checker suites are reported separately. Analytic and stochastic proofs require written review.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired) as exc:print('REJECT: semantic controls failed: '+str(exc),file=sys.stderr);sys.exit(1)
