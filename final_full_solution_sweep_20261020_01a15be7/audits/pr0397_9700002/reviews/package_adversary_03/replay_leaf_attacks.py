from pathlib import Path
import ast,json,copy,math,hashlib,datetime
home=Path(__file__).resolve().parent;p=home/'extracted/congestion-fragmentation-verification';tree=ast.parse((p/'replay.py').read_text());names={'AuditError','require','reject_constant','reject_duplicate_keys','finite_tree','strict_json','compare_records','compare_component'};env={'json':json,'math':math,'sha':lambda b:hashlib.sha256(b).hexdigest()};exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,(ast.FunctionDef,ast.ClassDef)) and x.name in names],type_ignores=[]),str(p/'replay.py'),'exec'),env)
policy=json.loads((p/'comparison-policy.json').read_text());runtime=json.loads((home/'replay_run/receipt.json').read_text())['runtime'];rows=[]
def leaves(v,path=()):
 if isinstance(v,dict):
  for k,x in v.items():yield from leaves(x,path+(k,))
 elif isinstance(v,list):
  for i,x in enumerate(v):yield from leaves(x,path+(i,))
 else:yield path,v
for name,old in [('turn1','candidate/turns/turn_01/CHECKS.json'),('turn2','candidate/turns/turn_02/CHECKS.json'),('portable','candidate/review/INDEPENDENT_CHECKS.json')]:
 exp=(p/old).read_bytes();act=json.loads((home/'replay_run'/name/'actual.json').read_text());allowed=set(policy['float_tolerances'].get(name,{}))
 if name=='portable':allowed|={'/python','/numpy','/scipy','/checks/0/name','/checks/0/files'}
 for path,value in leaves(act):
  ptr='/'+'/'.join(map(str,path))
  if ptr in allowed:continue
  changed=copy.deepcopy(act);node=changed
  for k in path[:-1]:node=node[k]
  if type(value) is bool:replacement=not value
  elif type(value) is int:replacement=value+1
  elif type(value) is float:replacement=value+max(0.01,abs(value)/7)
  elif type(value) is str:replacement=value+' altered'
  else:replacement='invalid type'
  node[path[-1]]=replacement;data=(json.dumps(changed,indent=2)+'\n').encode()
  try:env['compare_component'](exp,data,name,policy,runtime)
  except env['AuditError']:rows.append({'component':name,'path':ptr,'rejected':True})
  else:raise AssertionError(('Unapproved leaf mutation accepted',name,ptr))
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_assertions_passed':True,'independently_generated_unapproved_scalar_mutations':len(rows),'all_rejected':True,'cases':rows,'uses_actual_production_comparator':True}
(home/'REPLAY_LEAF_ATTACKS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='cases'}))
