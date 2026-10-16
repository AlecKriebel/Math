from pathlib import Path
import json,subprocess,sys,datetime,hashlib,copy,importlib.util
R=Path(__file__).resolve().parent;P=R.parent.parent/'publication';D=R/'hostile';D.mkdir(exist_ok=True)
original=(P/'checks/audit_exact_embedding.py').read_text();cert=P/'checks/EMBEDDING_CERTIFICATE.json';rows=[]
mutations=[('projector_factor_sign','image[quad] == {key: 4*value','image[quad] == {key: -4*value','GENERAL_PROJECTOR_IDENTITY'),('minor_reference_sign','tuple(sorted((3*a+c-3, 3*b+d-3))), -2','tuple(sorted((3*a+c-3, 3*b+d-3))), 2','MIXED_PLUCKER_MINORS'),('phi_trace_factor','phi(col) == (4 if kind','phi(col) == (8 if kind','PHI_TRACE')]
for label,old,new,wanted in mutations:
 if original.count(old)!=1:raise RuntimeError('unique source control '+label)
 path=D/(label+'.py');path.write_text(original.replace(old,new))
 for mode in ('','-O','-OO'):
  cmd=[sys.executable,'-I','-S','-B']+([mode] if mode else [])+[str(path),'--certificate',str(cert)]
  r=subprocess.run(cmd,capture_output=True,timeout=120);obj=json.loads(r.stdout)
  if r.returncode!=1 or r.stderr!=b'' or not obj.get('error','').startswith(wanted):raise RuntimeError('source control outcome '+label)
  rows.append({'case':label,'mode':mode or 'normal','expected_error':wanted,'exit':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode(),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
obj=json.loads(cert.read_text())
for label,mutate,error in [('boolean_index',lambda o:o['columns'][0]['entries'][0][0].__setitem__(0,False),'ENTRY_INDEX'),('boolean_coordinate',lambda o:o['columns'][0]['entries'][0].__setitem__(1,True),'ENTRY_VALUE_TYPE'),('noncanonical_rational',lambda o:o['columns'][0]['entries'][0].__setitem__(1,'2/2'),'ENTRY_VALUE_CANONICAL')]:
 o=copy.deepcopy(obj);mutate(o);path=D/(label+'.json');path.write_text(json.dumps(o)+'\n');r=subprocess.run([sys.executable,'-I','-S','-B',str(P/'checks/audit_exact_embedding.py'),'--certificate',str(path)],capture_output=True,timeout=120)
 if r.returncode!=1 or json.loads(r.stdout).get('error')!=error:raise RuntimeError(label)
 rows.append({'case':label,'mode':'normal','exit':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode(),'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
# Directly test the reviewed recursive JSON comparator in isolation.
spec=importlib.util.spec_from_file_location('portable_runner',P/'run_checks.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
type_controls=[mod.exact_types({'n':[0,1]}, {'n':[False,1]}),mod.exact_types({'n':1}, {'n':1.0}),mod.exact_types({'n':[1]}, {'n':(1,)}),mod.exact_types({'n':[1,True]}, {'n':[1,True]})]
if type_controls!=[False,False,False,True]:raise RuntimeError('recursive JSON exact types')
# Count all existing15negative outcome sites: each fails before projector/minors.
replay=json.loads((R/'receipts/EXTRACTED_REPLAY.json').read_text());faults=[x for x in replay['runs'] if x['case']!='baseline']
early_codes={'COORDINATE_MISMATCH','HERMITIAN_BASIS_ORDER','REAL_BASIS_ORDER','COMPLEX_BASIS_ORDER','ENTRY_ORDER_OR_DUPLICATE','ENTRY_VALUE_PARSE','GRAM_METADATA','INVERSE_METADATA','COLUMN_COUNT','SCHEMA_KEYS'}
if not all(json.loads(x['stdout'])['error'].split(':')[0] in early_codes for x in faults):raise RuntimeError('unexpected fault path')
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','source_mutation_executions':9,'new_certificate_fault_executions':3,'complete_stream_rows':rows,'recursive_type_controls':type_controls,'portable45faults_reject_before_projector_or_minor_verification':True,'portable45fault_reasons':sorted({json.loads(x['stdout'])['error'].split(':')[0] for x in faults}),'candidate_source_unchanged':True,'old_UID_harness_executed':False,'claim_boundary':'New defective-source controls are reviewer checks only; portable48runs are unchanged3baselines+45certificatefaults.'}
(R/'receipts/HOSTILE_CONTROLS.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k!='complete_stream_rows'},indent=2))
