import pathlib,json,datetime,subprocess,sys,shutil,importlib.util
R=pathlib.Path(__file__).resolve().parent
P=R/'private/fresh_external_copy'
M=R/'private/mutants_v02';M.mkdir(exist_ok=False)
cases=[
('missing_reverse_residual','verify_boundary.py','r[u][v] -= delta; r[v][u] += delta','r[u][v] -= delta; r[v][u] += 0'),
('overwrite_aggregate_coupling','verify_boundary.py','B[key] = B.get(key,0)+coefficient','B[key] = coefficient'),
('wrong_minimum_energy_shift','verify_boundary.py','pow2(-(energy-minimum))','pow2(-(energy+minimum))'),
('mtp2_check_always_true','verify_boundary.py','return False','return True')]
results=[]
for label,name,before,after in cases:
 text=(P/name).read_text();assert text.count(before)==1
 path=M/(label+'.py');path.write_text(text.replace(before,after))
 cmd=[sys.executable,str(R/'capture.py'),label,'--',sys.executable,str(path)]
 actual=subprocess.run(cmd,capture_output=True)
 if actual.returncode==0:raise ValueError('mutant was not detected: '+label)
 results.append({'case':label,'exit':actual.returncode,'caught':True,'stderr':actual.stderr.decode()[-1000:]})
# Tampered expected output must also fail the top-level runner.
tam=M/'tampered_expected_package';tam.mkdir()
for name in ['REPRODUCE.py','verify_boundary.py','verify_priority_examples.py','expected/boundary.json','expected/priority_laws.json']:
 dest=tam/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/name,dest)
expected=json.loads((tam/'expected/boundary.json').read_text());expected['networks']-=1
(tam/'expected/boundary.json').write_text(json.dumps(expected,indent=2)+'\n')
controls=[
('altered_expected_rejected',[sys.executable,str(tam/'REPRODUCE.py'),'--out-dir',str(M/'altered_expected_results')]),
('optimization_rejected',[sys.executable,'-O',str(P/'REPRODUCE.py'),'--out-dir',str(M/'forbidden_optimized_results')]),
('existing_output_rejected',[sys.executable,str(P/'REPRODUCE.py'),'--out-dir',str(R/'private/fresh_external_results')])]
for label,argv in controls:
 actual=subprocess.run([sys.executable,str(R/'capture.py'),label,'--']+argv,capture_output=True)
 if actual.returncode==0:raise ValueError('negative runner control not rejected: '+label)
 results.append({'case':label,'exit':actual.returncode,'caught':True,'stderr':actual.stderr.decode()[-1000:]})
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('boundary_released',P/'verify_boundary.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
density=[
(4,[(0,1),(2,3),(0,2),(1,3)],{},[(0,1),(1,0),(2,3),(3,2)],[2,-3,4,-1],[-7,6,-5,8]),
(4,[(0,1),(0,2),(1,3),(2,3),(1,2)],{},[(0,1),(0,2),(1,3),(2,3)],[-2,3,1,-4],[-5,7,-9,2,4]),
(5,[(0,1),(2,3)],{0:0,3:1},[],[3,-2,4,-5,6],[-8,-7]),
(3,[(0,1),(1,2)],{},[(0,1),(1,2)],[1,-5,3],[-4,-6]),
(3,[(0,1)],{},[(0,1),(1,0)],[3,-4,5],[-9])]
density_results=[module.density(*args) for args in density]
# This uniform lattice support is not feasible on the path, demonstrating why
# the supplementary lemma's facial assumption cannot be omitted.
X=module.cube(3);S=[x for x in X if x[0]==x[2]]
projections={e:{(x[e[0]],x[e[1]]) for x in S} for e in [(0,1),(1,2)]}
recovered=[x for x in X if all((x[e[0]],x[e[1]]) in projections[e] for e in projections)]
assert module.mtp2({x:int(x in S) for x in X}) and len(S)==4 and len(recovered)==8
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_MUTANT_NEGATIVE_AND_DENSITY_CONTROLS',
 'mutants_and_runner_negatives':results,'additional_density_cases':density_results,
 'facial_assumption_essential_control':{'lattice_support_size':len(S),'edge_projection_intersection_size':len(recovered)},
 'limitations':'Additional density examples invoke released density code and independently selected inputs. All finite controls remain illustrative.'}
(R/'MUTANT_AND_DENSITY_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
