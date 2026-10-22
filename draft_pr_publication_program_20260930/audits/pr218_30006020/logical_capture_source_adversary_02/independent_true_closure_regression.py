"""Actual guard/row-assignment lexical regression. Never executes run or an API."""
from pathlib import Path
import ast,copy,datetime,hashlib,json,sys,tempfile,types
HERE=Path(__file__).absolute().parent
CASE=HERE.parent
RESULTS=[]
def need(x,m):
 if type(x) is not bool or not x:raise RuntimeError(m)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(j):return (json.dumps(j,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def put(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:need(f.write(b)==len(b),'Owned full write')
 p.chmod(0o444)
def module(p,n):
 m=types.ModuleType(n);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def run_node(raw):return next(n for n in ast.parse(raw).body if isinstance(n,ast.FunctionDef) and n.name=='run')
def module_run_code(raw):
 top=compile(raw,'inspected_capture_source','exec')
 return next(c for c in top.co_consts if isinstance(c,types.CodeType) and c.co_name=='run')
def binding_inventory(raw):
 run=run_node(raw);code=module_run_code(raw);children={c.co_name:c for c in code.co_consts if isinstance(c,types.CodeType)};stores={}
 def record(name,line,kind):stores.setdefault(name,[]).append({'line':line,'kind':kind})
 def walk(n):
  if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
   record(n.name,n.lineno,'nested_definition');return
  if isinstance(n,(ast.ListComp,ast.DictComp,ast.SetComp,ast.GeneratorExp)):return
  if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Store):record(n.id,n.lineno,'outer_store')
  if isinstance(n,ast.ExceptHandler) and n.name:record(n.name,n.lineno,'exception_target')
  for child in ast.iter_child_nodes(n):walk(child)
 for n in run.body:walk(n)
 for arg in run.args.args:record(arg.arg,run.lineno,'parameter')
 out=[]
 for n in run.body:
  if isinstance(n,ast.FunctionDef):
   child=children[n.name];bindings=[]
   for name in child.co_freevars:
    sites=stores.get(name,[]);bindings.append({'name':name,'outer_binding_sites':sites,'outer_stores_after_closure_definition':[p for p in sites if p['line']>n.lineno]})
   out.append({'closure':n.name,'definition_line':n.lineno,'actual_compiled_freevars':list(child.co_freevars),'bindings':bindings})
 nested=[]
 def code_walk(parent):
  for index,child in enumerate(parent.co_consts):
   if isinstance(child,types.CodeType):
    nested.append({'qualname':child.co_qualname,'constant_index':index,'first_line':child.co_firstlineno,'freevars':list(child.co_freevars),'cellvars':list(child.co_cellvars),'kind':'comprehension_or_generator' if child.co_name.startswith('<') else 'named_function'})
    code_walk(child)
 code_walk(code)
 return {'named_nested_closures':out,'run_cellvars':list(code.co_cellvars),'all_nested_code_including_each_comprehension':nested}
def actual_fragment_factory(cap,h,source,engine_raw,own_raw,acceptance_ref,acceptance_raw,qb):
 run=run_node(source);guard=next(n for n in run.body if isinstance(n,ast.FunctionDef) and n.name=='guard')
 decodes=[n for n in run.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('engine','own')]
 need({n.targets[0].id for n in decodes}=={'engine','own'},'Actual engine/source manifest decode bindings')
 queue_assignments=[n for n in ast.walk(run) if isinstance(n,ast.Assign) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr=='own_queue_row']
 need(len(queue_assignments)==1,'Single actual source queue-row assignment');row_assignment=queue_assignments[0];row_name=row_assignment.targets[0].elts[0].id
 arguments=ast.parse('def f(h,source,source_pin,engine_raw,own_raw,acceptance_ref,acceptance_raw,qb):\n pass').body[0].args
 tail=ast.parse('guard()\n'+row_name+'\n').body
 # The actual nested guard and row binding share one compiler-created cell.
 body=[copy.deepcopy(n) for n in decodes]+[copy.deepcopy(guard),tail[0],copy.deepcopy(row_assignment)]
 body+=ast.parse('return guard, type(own).__name__, type('+row_name+').__name__').body
 factory=ast.FunctionDef(name='owned_actual_guard_row_factory',args=arguments,body=body,decorator_list=[])
 tree=ast.Module(body=[factory],type_ignores=[]);ast.fix_missing_locations(tree);environment=dict(cap.__dict__)
 exec(compile(tree,'actual_guard_and_queue_binding_in_one_owned_closure','exec'),environment)
 guard,manifest_type,row_type=environment[factory.name](h,source,pin(source),engine_raw,own_raw,acceptance_ref,acceptance_raw,qb)
 closure_cells={name:cell for name,cell in zip(guard.__code__.co_freevars,guard.__closure__)}
 need('own' in closure_cells,'True lexical source-manifest closure cell')
 failure=None
 try:guard()
 except BaseException as error:failure={'type':type(error).__name__,'message':str(error)}
 return {'guard_freevars':list(guard.__code__.co_freevars),'manifest_type_after_actual_row_binding':manifest_type,'row_type':row_type,'manifest_cell_type':type(closure_cells['own'].cell_contents).__name__,'guard_after_actual_row_binding_failure':failure,'row_assignment':ast.unparse(row_assignment),'actual_guard_AST_pin':pin(ast.dump(guard_node:=next(n for n in run.body if isinstance(n,ast.FunctionDef) and n.name=='guard'),include_attributes=False).encode())}
def main():
 def deny(event,args):
  if event in ('subprocess.Popen','os.system','os.exec','socket.connect','socket.connect_ex','socket.bind'):raise RuntimeError('No API/transport/subprocess in closure regression')
 sys.addaudithook(deny)
 bindings=json.loads((HERE/'REVIEWED_SOURCE_BINDINGS.json').read_text());sources={}
 for label in ('01','02'):
  p=CASE/('logical_capture_source_preparation_'+label)/'capture_logical_packet.py';raw=p.read_bytes();need(pin(raw)==bindings['source'+label+'_pin'],'Exact source'+label);sources[label]=raw
 with tempfile.TemporaryDirectory(prefix='_synthetic_true_closure_',dir=HERE) as temp:
  checkout=Path(temp)/'checkout';case=checkout/'draft_pr_publication_program_20260930/audits/pr218_30006020';engine=case/'native_completion_preparation_01';realengine=CASE/'native_completion_preparation_01';eraw=(realengine/'SOURCE_MANIFEST.json').read_bytes();em=json.loads(eraw)
  for row in em['files']:
   raw=(realengine/row['path']).read_bytes();need(pin(raw)=={k:row[k] for k in ('bytes','sha256')},'Exact engine file');put(engine/row['path'],raw)
  put(engine/'SOURCE_MANIFEST.json',eraw);h=module(engine/'native218_model.py','owned_h')
  context=CASE/'native_source_custody_preparation_02/capture_native_custody.py';put(case/'native_source_custody_preparation_02/capture_native_custody.py',context.read_bytes())
  gate=case/'_synthetic_gate.json';gate_raw=enc({'scope':'OWNED_SOURCE_CLOSURE_ONLY_NOT_ACTUAL_ACCEPTANCE'});put(gate,gate_raw);gate_ref={'path':str(gate),**pin(gate_raw)}
  qb=b'|218|30006020 / OWR-14298589-005|a|b|c|d|e|claimed_solved|1/5|f|g|h|\n';results={}
  for label in ('01','02'):
   real=CASE/('logical_capture_source_preparation_'+label);target=case/real.name;raw=(real/'SOURCE_MANIFEST.json').read_bytes();manifest=json.loads(raw)
   for row in manifest['files']:
    data=(real/row['path']).read_bytes();need(pin(data)=={k:row[k] for k in ('bytes','sha256')},'Exact'+label+' payload');put(target/row['path'],data)
   put(target/'SOURCE_MANIFEST.json',raw);cap=module(target/'capture_logical_packet.py','owned_capture_'+label)
   need(cap.CHECKOUT==checkout,'Owned source paths only')
   results[label]=actual_fragment_factory(cap,h,sources[label],eraw,raw,gate_ref,gate_raw,qb)
  need(results['01']['manifest_cell_type']=='bytes' and results['01']['guard_after_actual_row_binding_failure']['type']=='AttributeError','Actual01 shadow reproduced in true closure')
  need(results['02']['manifest_cell_type']=='dict' and results['02']['row_type']=='bytes' and results['02']['guard_after_actual_row_binding_failure'] is None,'Actual02 guard survives row extraction')
  need(results['01']['actual_guard_AST_pin']==results['02']['actual_guard_AST_pin'],'Guard mechanism unchanged byte-for-AST')
  inv={label:binding_inventory(raw) for label,raw in sources.items()};hazards={}
  for label,value in inv.items():
   hazards[label]=[{'closure':c['closure'],'binding':r['name'],'later_outer_stores':r['outer_stores_after_closure_definition']} for c in value['named_nested_closures'] for r in c['bindings'] if r['outer_stores_after_closure_definition']]
  need(any(h['closure']=='guard' and h['binding']=='own' for h in hazards['01']),'Static scan independently identifies source01 hazard')
  need(hazards['02']==[],'No later outer rebinding of any named nested closure free binding in02')
 return {'schema':'pr218-independent-actual-closure-repair-regression-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'ACTUAL_AST_GUARD_AND_ROW_ASSIGNMENT_IN_ONE_OWNED_FACTORY_ONLY','source01_failure_reproduced':True,'source02_true_closure_passed':True,'guard_AST_unchanged':True,'results':results,'all_named_nested_closure_binding_inventory':inv,'postdefinition_outer_rebindings':hazards,'explicit_dependencies':['Exact owned source/engine/manifest copies, real readonly source/closure readers, actual pure own_queue_row.','Synthetic gate bytes used only by the actual guard byte reread, no typed Root acceptance created.','No actual run/main/API/Seed/Runtime/original lock/private packet stage or native effect.'],'actual_capture_or_source02_operational_success_proved':False}
if __name__=='__main__':print(json.dumps(main(),sort_keys=True,indent=2))
