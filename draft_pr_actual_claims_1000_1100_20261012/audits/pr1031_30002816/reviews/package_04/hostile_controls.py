"""Fresh intended-reason malformed certificate and mathematical code-fault controls."""
import ast,copy,datetime,hashlib,json,pathlib,subprocess,sys
sys.dont_write_bytecode=True
O=pathlib.Path(__file__).resolve().parent;X=O/'extracted/grassmann_calibrations_v1';H=O/'hostile';H.mkdir(exist_ok=True)
checker=X/'checks/audit_exact_embedding.py';certificate=X/'checks/EMBEDDING_CERTIFICATE.json';original=json.loads(certificate.read_text());code=checker.read_text()
cases=[]
def certcase(label,mutate,reason):
 value=copy.deepcopy(original);mutate(value);p=H/(label+'.json');p.write_text(json.dumps(value,sort_keys=True)+'\n');cases.append((label,checker,p,reason,'fresh_certificate_fault'))
certcase('boolean_exterior_index',lambda o:o['columns'][0]['entries'][0][0].__setitem__(0,False),'ENTRY_INDEX')
certcase('boolean_coordinate_value',lambda o:o['columns'][0]['entries'][0].__setitem__(1,True),'ENTRY_VALUE_TYPE')
certcase('noncanonical_fraction',lambda o:o['columns'][0]['entries'][0].__setitem__(1,'1/1'),'ENTRY_VALUE_CANONICAL')
certcase('wrong_canonical_denominator',lambda o:o['columns'][0]['entries'][0].__setitem__(1,'1/3'),'ENTRY_DENOMINATOR')
certcase('zero_coordinate',lambda o:o['columns'][0]['entries'][0].__setitem__(1,'0'),'ENTRY_VALUE_CANONICAL')
# These are newly executed defective SOURCE expectations, explicitly outside portable48 certificate-only scope.
def codecase(label,before,after,reason):
 assert code.count(before)==1
 altered=code.replace(before,after);ast.parse(altered);p=H/(label+'.py');p.write_text(altered);cases.append((label,p,certificate,reason,'fresh_defective_source_expectation'))
codecase('projector_expected_factor', 'image[quad] == {key: 4*value for key, value in plane[quad].items()}', 'image[quad] == {key: 3*value for key, value in plane[quad].items()}', 'GENERAL_PROJECTOR_IDENTITY:')
codecase('projector_trace_expected_factor','expected_trace = poly_add(expected_trace, coordinate, 4)','expected_trace = poly_add(expected_trace, coordinate, 8)','GENERAL_PROJECTOR_PHI')
codecase('projector_pure_expected_factor','expected_q = poly_add(expected_q, coordinate, 4)','expected_q = poly_add(expected_q, coordinate, 8)','GENERAL_PROJECTOR_Q')
codecase('mixed_minor_expected_count','require(count == 9, "MIXED_MINOR_COUNT")','require(count == 8, "MIXED_MINOR_COUNT")','MIXED_MINOR_COUNT')
codecase('mixed_minor_expected_sign','3*a+c-3, 3*b+d-3))), -2)','3*a+c-3, 3*b+d-3))), 2)','MIXED_PLUCKER_MINORS')
rows=[]
for mode in (0,1,2):
 for label,program,cert,reason,category in cases:
  command=[sys.executable,'-I','-S','-B']+([] if mode==0 else ['-'+'O'*mode])+[str(program),'--certificate',str(cert)]
  result=subprocess.run(command,capture_output=True,timeout=120)
  parsed=json.loads(result.stdout);assert result.returncode==1 and result.stderr==b'' and parsed['status']=='FAIL' and parsed['error'].startswith(reason)
  rows.append({'case':label,'mode':mode,'category':category,'exit':result.returncode,'stdout':result.stdout.decode(),'stderr':result.stderr.decode(),'source_sha256':hashlib.sha256(program.read_bytes()).hexdigest(),'certificate_sha256':hashlib.sha256(cert.read_bytes()).hexdigest(),'intended_failure':reason,'matched':True})
obj={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','executions':len(rows),'case_families':len(cases),'portable48_scope_extended':False,'rows':rows}
(O/'HOSTILE_CONTROLS.json').write_text(json.dumps(obj,indent=2)+'\n');print(json.dumps({k:v for k,v in obj.items() if k!='rows'},indent=2))
