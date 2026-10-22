import ast,datetime,hashlib,json,pathlib,sys
sys.dont_write_bytecode=True
B=pathlib.Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1031_30002816');O=B/'reviews/package_04';X=O/'extracted/grassmann_calibrations_v1'
old=B/'reviews/package_03/extracted/grassmann_calibrations_v1/run_checks.py';new=X/'run_checks.py'
s=old.read_text();n=new.read_text();replacements={'References must be exactly48unique executed cases':'References must contain exactly 48 unique executed cases','Exactly15actualcertificatefaultfamilies required':'Exactly 15 actual certificate fault families required'}
for a,b in replacements.items():assert s.count(a)==1;s=s.replace(a,b)
assert s==n and ast.dump(ast.parse(s),include_attributes=False)==ast.dump(ast.parse(n),include_attributes=False)
t=ast.parse((X/'evidence/submitted/run_finite_checks.py').read_text());fun=[f for f in t.body if isinstance(f,ast.FunctionDef) and f.name=='mutations'];assert len(fun)==1
calls=sorted({ast.unparse(c.func) for c in ast.walk(fun[0]) if isinstance(c,ast.Call)})
assert calls==['Fraction','deepcopy','fresh',"obj['columns'].pop","obj['columns'][0]['entries'].append",'out.append','str']
constants={f.targets[0].id:ast.literal_eval(f.value) for f in t.body if isinstance(f,ast.Assign) and len(f.targets)==1 and isinstance(f.targets[0],ast.Name) and f.targets[0].id in ('POSITIVES','EXPECTED_MUTATIONS')}
assert len(constants['EXPECTED_MUTATIONS'])==15
refs=json.loads((X/'expected/ROOT_FINITE_REPRODUCTION.json').read_text());replay=json.loads((O/'PORTABLE_REPLAY.json').read_text());assert len(replay['runs'])==48
reference_map={(r['mode'],r['case']):r for r in refs['runs']}
def eq(a,b):
 if type(a)!=type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys() and all(eq(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(eq(x,y) for x,y in zip(a,b))
 return a==b
summary=[]
for r in replay['runs']:
 f=reference_map[r['mode'],r['case']]
 assert r['exit_code']==f['exit_code'] and r['stdout']==f['stdout'] and r['stderr']==f['stderr'] and r['certificate_sha256']==f['certificate_sha256'] and eq(json.loads(r['stdout']),json.loads(f['stdout']))
 summary.append({'mode':r['mode'],'case':r['case'],'exit':r['exit_code'],'error':json.loads(r['stdout']).get('error'),'before_projector_minor':r['case']!='baseline'})
for a,b in [(True,1),(1,1.0),({'x':[False]}, {'x':[0]})]:assert not eq(a,b)
static=[]
for p in sorted(X.rglob('*.py')):
 text=p.read_text();tree=ast.parse(text)
 static.append({'path':str(p.relative_to(X)),'bytes':len(p.read_bytes()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'all_functions':[f.name for f in ast.walk(tree) if isinstance(f,(ast.FunctionDef,ast.AsyncFunctionDef))],'imports':[ast.unparse(v) for v in ast.walk(tree) if isinstance(v,(ast.Import,ast.ImportFrom))],'asserts':sum(isinstance(v,ast.Assert) for v in ast.walk(tree)),'write_or_exec_calls':[ast.unparse(v)[:240] for v in ast.walk(tree) if isinstance(v,ast.Call) and any(s in ast.unparse(v.func) for s in ('write','exec','subprocess','open','chmod','chown','unlink','mkdir'))],'diagnostic_string_literals':[v.value for v in ast.walk(tree) if isinstance(v,ast.Constant) and isinstance(v.value,str) and (' ' in v.value or 'FAIL' in v.value)]})
obj={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','round3_actual_old_and_new_source_match_exact_two_replacements':True,'old_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),'new_sha256':hashlib.sha256(new.read_bytes()).hexdigest(),'mutations_AST_calls':calls,'mutations_pure_literal_inputs_only':True,'historical_module_or_UID_harness_executed_or_simulated':False,'recursive_type_counterexamples_rejected':True,'portable_cases_independently_compared':summary,'all_python_sources_read_as_AST':static}
(O/'CODE_AND_REPLAY_INSPECTION.json').write_text(json.dumps(obj,indent=2)+'\n')
print(json.dumps({k:v for k,v in obj.items() if k not in ('portable_cases_independently_compared','all_python_sources_read_as_AST')},indent=2));print('All Python sources',len(static))
