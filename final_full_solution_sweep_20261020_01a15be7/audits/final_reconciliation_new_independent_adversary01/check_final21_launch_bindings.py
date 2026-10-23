"""Pure AST launch-string equivalence check on final sealed SOURCE21 and inactive recipes."""
from pathlib import Path
import ast,hashlib,json
R=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7');A=R/'audits';E=A/'pr1131_30005455/known23592692_operations21_preparation01'
PINS={}
def read(p,h):
 assert not any(q.is_symlink()for q in[p,*p.parents]);b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==h
 PINS[str(p)]={'path':str(p),'bytes':len(b),'sha256':h};return b
def expr(raw,name):
 nodes=[n.value for n in ast.walk(ast.parse(raw))if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id==name for t in n.targets)]
 assert len(nodes)==1;node=nodes[0]
 permitted=(ast.BinOp,ast.Add,ast.Name,ast.Load,ast.Constant,ast.Call,ast.Subscript)
 assert all(isinstance(n,permitted)for n in ast.walk(node))
 assert all(isinstance(n.func,ast.Name)and n.func.id in{'repr','str'}for n in ast.walk(node)if isinstance(n,ast.Call))
 return compile(ast.Expression(node),'<inert source expression>','eval')
def main():
 mf=json.loads(read(E/'MANIFEST.json','f1a3c3b228228f7c8ecfef3d597f597d5b994d1fa85fbd0a07a6ed17395a426f'))
 controller=read(E/'native_step21.py','ca513166da9a72098891b90d44175d2a547c1a530e68595222e5ba8f426b9f7f')
 read(E/'entry21.py','694fb1692a0d30c5f4d7ea3e782887a88070ec3a980869717a8f5f025d8663ea')
 read(E/'source21/SOURCE_MANIFEST21.json','c64fae35c2ea0ebd7213e0791559f3cb5eba9f87a5b6fa8a0fc2038af2da9670')
 assert mf['controller21_sha256']==PINS[str(E/'native_step21.py')]['sha256']and mf['entry21_sha256']==PINS[str(E/'entry21.py')]['sha256']
 recipe=read(A/'ROOT_PR1131_KNOWN21_POST_ALL_ACTIONS_COMPLETION_PROSPECTIVE_TEMPLATE05.py','b78ddf07d7b42bbc614cbda1f090ca73b60426724f9c8129b4921798bdb01d46')
 parent=read(A/'ROOT_ACTUAL21_KNOWN_ONLY_SEPARATE_ACTION_FULL_NATIVE_PARENT_PROSPECTIVE_TEMPLATE03.py','0cd02ddf5cc23928aed3e2fc6ac98904512bd40369b25d01522902af33093771')
 ci=expr(controller,'program');ri=expr(recipe,'inner_program');ro=expr(recipe,'outer_program');po=expr(parent,'launch')
 results=[]
 for action in['stage-known','publish','verify-public','ledger']:
  # Synthetic digest strings exist only in memory; they are not actual authorities/receipts.
  root19='55eb5e5e8a62553bd342ee690a753d1f66b8d63fd8f9cfe56d9b7c7f8f403e79';root21='1'*64;compat='2'*64;contract='3'*64
  argv=[action,'--expected-pr-head','9601e1e768c94522bc8ad105db4dfae4770bad75','--deposit-id','23592692','--clearance-sha256',root19,'--root21-clearance-sha256',root21,'--compat20-clearance-sha256',compat]
  entrypin=mf['entry21_sha256'];helperpin=mf['controller21_sha256'];scope={'__builtins__':{'repr':repr,'str':str}}
  actual_inner=eval(ci,scope,{'ENTRY':E/'entry21.py','g':{'entry21_sha256':entrypin},'argv':argv})
  recipe_inner=eval(ri,scope,{'entryp':E/'entry21.py','ENTRY21_SHA':entrypin,'expected_argv':argv})
  actual_outer=eval(po,scope,{'p':E/'native_step21.py','h':helperpin,'action':action,'contractsha':contract})
  recipe_outer=eval(ro,scope,{'helperp':E/'native_step21.py','helperh':helperpin,'action':action,'CONTRACT_SHA':contract})
  assert actual_inner==recipe_inner and actual_outer==recipe_outer
  results.append({'action':action,'inner_launch_sha256':hashlib.sha256(actual_inner.encode()).hexdigest(),'outer_launch_sha256':hashlib.sha256(actual_outer.encode()).hexdigest()})
 return {'status':'PASS_FINAL_SEALED21_VS_COMPLETION05_EXACT_INERT_LAUNCH_EQUIVALENCE','comparisons':8,'actions':results,'external_inputs':list(PINS.values()),'synthetic_in_memory_digest_constants_only':True,'actual_receipts_or_authority_created':False,'actual_actions_executed':0,'scope':'Program-construction equivalence only; final actual full argv/interpreter/authority/physical stream/publication evidence still required.','final_clearance':False}
if __name__=='__main__':print(json.dumps(main(),sort_keys=True,indent=2))
