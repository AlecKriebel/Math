from pathlib import Path
import subprocess,hashlib,json,datetime
D=Path(__file__).resolve().parent;A=D.parent;X=D/'extracted_supplement/controls';M=D/'mutants';M.mkdir(exist_ok=True)
py=str(A/'gv_algebra_reproduction_adversary/private/control_env/bin/python')
mutants=[
 ('polynomial_false','verify_forms.py','for k in range(120):','check(False)\nfor k in range(120):'),
 ('polynomial_wrong_GV_sign','verify_forms.py','density=add(mul(qz,der(pz,2)),scale(mul(pz,der(qz,2)),-1))','density=scale(add(mul(qz,der(pz,2)),scale(mul(pz,der(qz,2)),-1)),-1)'),
 ('polynomial_missing_Jacobian','verify_forms.py','scale(subz(density,a,l),1/l)','subz(density,a,l)'),
 ('symbolic_false','independent_symbolic_checks.py','x,y,z,t = s.symbols','check("injected_false",False)\nx,y,z,t = s.symbols'),
 ('symbolic_wrong_GV_sign','independent_symbolic_checks.py','G=s.diff(q,z)*s.diff(p,z,2)-s.diff(p,z)*s.diff(q,z,2)','G=-(s.diff(q,z)*s.diff(p,z,2)-s.diff(p,z)*s.diff(q,z,2))'),
 ('symbolic_missing_Jacobian','independent_symbolic_checks.py','g.subs(sub)/length','g.subs(sub)'),
 ('jet_false','independent_integrable_controls.py','for xv in [Q(0),Q(1,4)]:','check("injected_false",False)\nfor xv in [Q(0),Q(1,4)]:'),
 ('jet_wrong_GV_sign','independent_integrable_controls.py','rho=(-6*zv**2','rho=-(-6*zv**2'),
 ('sampling_wrong_value','finite_sampling_counterexample.py','negative!=Q(-62,63)','negative!=Q(-61,63)'),
]
records=[]
for label,src,old,new in mutants:
 text=(X/src).read_text();count=text.count(old)
 if not count:raise RuntimeError(label+' missing mutation target')
 p=M/(label+'.py');p.write_text(text.replace(old,new));
 for opt in [False,True]:
  cmd=[py,'-E','-B','-P']+(['-O'] if opt else [])+[str(p)];utc=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run(cmd,cwd=D,capture_output=True,text=True,timeout=45)
  stream=D/(label+('_optimized' if opt else '_normal'));stream.with_suffix('.stdout.txt').write_text(r.stdout);stream.with_suffix('.stderr.txt').write_text(r.stderr)
  row={'label':label,'source':src,'replacement_occurrences':count,'old':old,'new':new,'utc':utc,'optimized':opt,'argv':cmd,'mutant_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'exit_code':r.returncode,'rejected':r.returncode!=0,'stdout':stream.with_suffix('.stdout.txt').name,'stderr':stream.with_suffix('.stderr.txt').name};records.append(row)
  print(label,opt,r.returncode,flush=True)
(D/'NEGATIVE_CONTROL_RESULTS.json').write_text(json.dumps(records,indent=2)+'\n')
if not all(r['rejected'] for r in records):raise RuntimeError('A deliberately false variant survived')
