from pathlib import Path
import json,hashlib,subprocess,sys,copy,importlib.util,datetime
R=Path(__file__).resolve().parent;P=R.parent.parent/'publication';H=R/'hostile';H.mkdir(exist_ok=True)
checker=P/'checks/audit_exact_embedding.py';cert=P/'checks/EMBEDDING_CERTIFICATE.json';source=checker.read_text()
def req(c,m):
 if not c:raise RuntimeError(m)
original=json.loads(cert.read_text());cases=[]
for name,modify,err in [
 ('boolean_exterior_index',lambda o:o['columns'][0]['entries'][0][0].__setitem__(0,False),'ENTRY_INDEX'),
 ('boolean_coordinate',lambda o:o['columns'][0]['entries'][0].__setitem__(1,True),'ENTRY_VALUE_TYPE'),
 ('noncanonical_fraction',lambda o:o['columns'][0]['entries'][0].__setitem__(1,'2/2'),'ENTRY_VALUE_CANONICAL'),
 ('zero_entry',lambda o:o['columns'][0]['entries'][0].__setitem__(1,'0'),'ENTRY_VALUE_CANONICAL'),
 ('wrong_exact_denominator',lambda o:o['columns'][0]['entries'][0].__setitem__(1,'1/3'),'ENTRY_DENOMINATOR')]:
 o=copy.deepcopy(original);modify(o);p=H/(name+'.json');p.write_text(json.dumps(o,sort_keys=True)+'\n');cases.append((name,checker,p,err))
for name,old,new,err in [
 ('projector_expected_sign','{key: 4*value for key, value in plane[quad].items()}','{key: -4*value for key, value in plane[quad].items()}','GENERAL_PROJECTOR_IDENTITY'),
 ('phi_trace_expected_scale','phi(col) == (4 if kind == "diag" else 0)','phi(col) == (8 if kind == "diag" else 0)','PHI_TRACE'),
 ('pure_trace_expected_scale','phi(col, pure=True) == (4 if kind == "diag" and','phi(col, pure=True) == (8 if kind == "diag" and','Q_PURE_TRACE'),
 ('mixed_minor_expected_sign','3*a+c-3, 3*b+d-3))), -2)','3*a+c-3, 3*b+d-3))), 2)','MIXED_PLUCKER_MINORS')]:
 req(source.count(old)==1,'mutation locator '+name);p=H/(name+'.py');p.write_text(source.replace(old,new));cases.append((name,p,cert,err))
rows=[]
for mode in (0,1,2):
 for name,script,inputpath,expected in cases:
  command=[sys.executable,'-I','-S','-B']+(['-'+'O'*mode] if mode else [])+[str(script),'--certificate',str(inputpath)]
  z=subprocess.run(command,capture_output=True,timeout=120)
  obj=json.loads(z.stdout);req(z.returncode==1 and z.stderr==b'' and obj['status']=='FAIL' and obj['error'].startswith(expected),name+' reason')
  rows.append({'mode':mode,'case':name,'exit_code':z.returncode,'stdout':z.stdout.decode(),'stderr':z.stderr.decode(),'expected_error':expected,'checker_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'certificate_sha256':hashlib.sha256(inputpath.read_bytes()).hexdigest()})
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('reviewed_current_runner',P/'run_checks.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
comp=[('same_nested',{'x':[1,True,2.0]},{'x':[1,True,2.0]},True),('bool_int',{'x':[True]},{'x':[1]},False),('int_float',{'x':[1]},{'x':[1.0]},False),('list_tuple',[1],(1,),False),('extra_key',{'x':1,'y':2},{'x':1},False)]
for name,a,b,wanted in comp:req(mod.exact_types(a,b) is wanted,'recursive comparator '+name)
# Reader-facing current diagnostic strings, separate from immutable historical evidence.
texts=[n for n in source.splitlines() if False]
diagnostics=[]
for n,line in enumerate((P/'run_checks.py').read_text().splitlines(),1):
 if 'exactly48unique' in line or 'Exactly15actualcertificatefaultfamilies' in line:diagnostics.append({'line':n,'text':line.strip()})
d={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fresh_actual_runs':len(rows),'certificate_fault_families':5,'defective_source_families':4,'runs':rows,'recursive_comparator':[{ 'case':a,'expected':d} for a,b,c,d in comp],'current_diagnostic_spacing_candidates':diagnostics,'no_historical_harness_run':True,'scope':'Reviewer controls separate from portable 48-run claim.'}
(R/'HOSTILE_CONTROLS.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps({k:v for k,v in d.items() if k!='runs'},indent=2))
