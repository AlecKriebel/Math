from pathlib import Path
import subprocess,json,hashlib,shutil
D=Path(__file__).absolute().parent;S=D/'private/source';P=S/'draft_pr_actual_claims_1100_1200_20261017/audits/pr1150_30003045/pr_repair_candidate';raw=D/'private/direct_runs';raw.mkdir(exist_ok=True)
wrong=['differentiate_square','wrong_h_frobenius','wrong_s_power','omit_exact_correction','gamma_kills_dz','a_belongs_R','wrong_quotient_derivative','slot_z_preserves_dz','invalid_exponent_one_base_dlog'];runs=[]
for tag,flags in [('normal',[]),('optimized',['-O'])]:
 for prog,base in [('verify_symbols.py','symbols_expected.json'),('diagnose_norm.py','norm_expected.json')]:
  r=subprocess.run(['python3','-B',*flags,str(P/prog)],cwd=P,capture_output=True);(raw/(tag+'-'+prog+'.stdout')).write_bytes(r.stdout);(raw/(tag+'-'+prog+'.stderr')).write_bytes(r.stderr)
  okay=r.returncode==0 and not r.stderr and r.stdout==(P/base).read_bytes();runs.append({'program':prog,'flags':flags,'exit':r.returncode,'bytes':len(r.stdout),'sha256':hashlib.sha256(r.stdout).hexdigest(),'complete_baseline_match':okay,'output':json.loads(r.stdout)})
  if not okay:raise ValueError((tag,prog))
 for mode in wrong:
  r=subprocess.run(['python3','-B',*flags,str(P/'verify_symbols.py'),'--wrong',mode],cwd=P,capture_output=True);(raw/(tag+'-'+mode+'.stderr')).write_bytes(r.stderr);last=r.stderr.decode().splitlines()[-1];okay=r.returncode!=0 and last.startswith('ValueError: CHECK FAILED:') and 'unexpectedly passed' not in last
  runs.append({'program':'verify_symbols.py','flags':flags,'wrong':mode,'exit':r.returncode,'stderr_bytes':len(r.stderr),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest(),'actual_computed_failure':okay,'diagnostic':last})
  if not okay:raise ValueError((tag,mode))
(D/'DIRECT_MATH_EXECUTIONS.json').write_text(json.dumps(runs,indent=2)+'\n');print('direct math: four exact positive outputs,18 actual computed ValueError failures')
# extra altered baseline/proof input checks exercise BOTH integrity entrypoints.
controls=[];outs=['output/mixed-kato-counterexample-source-and-verification.zip','output/zenodo-upload-kit.zip','PACKAGE_RECEIPT.json']
def fp(p):
 st=p.stat();return {'bytes':st.st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'inode':st.st_ino,'mtime_ns':st.st_mtime_ns}
for tag,flags in [('normal',[]),('optimized',['-O'])]:
 for prog in ['verification/verify_all.py','build_package.py']:
  for kind in ['proof','baseline']:
   root=D/'private'/('integrity-'+tag+'-'+prog.replace('/','_')+'-'+kind)
   if root.exists():shutil.rmtree(root)
   shutil.copytree(S,root);a=root/'draft_pr_actual_claims_1100_1200_20261017/audits/pr1150_30003045';p=a/'FINAL_PROOF.md' if kind=='proof' else a/'pr_repair_candidate/symbols_expected.json';p.write_bytes(p.read_bytes()+b'CORRUPTION\n');before={n:fp(root/n) for n in outs};r=subprocess.run(['python3','-B',*flags,str(root/prog)],cwd=root,capture_output=True);after={n:fp(root/n) for n in outs};okay=r.returncode!=0 and before==after
   controls.append({'mode':tag,'entrypoint':prog,'mutation':kind,'exit':r.returncode,'stderr':r.stderr.decode(),'other_outputs_exactly_preserved':before==after,'PASS':okay})
   if not okay:raise ValueError('integrity control')
(D/'EXTRA_INTEGRITY_CONTROLS.json').write_text(json.dumps(controls,indent=2)+'\n');print('extra integrity:',len(controls),'safe rejections')
