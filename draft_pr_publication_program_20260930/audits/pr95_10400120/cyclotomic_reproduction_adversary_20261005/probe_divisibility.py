import ast,sys,json
from pathlib import Path
script=Path(sys.argv[1]);mode=sys.argv[2]
source=ast.parse(script.read_text());selected=[]
for node in source.body:
 if isinstance(node,(ast.Import,ast.ImportFrom)):selected.append(node)
 if isinstance(node,ast.FunctionDef) and node.name in {'require','red','mul','shift','conj','snum'}:selected.append(node)
 if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id in {'MON','perms','signs'} for t in node.targets):selected.append(node)
ns={};exec(compile(ast.Module(body=selected,type_ignores=[]),str(script),'exec'),ns)
if mode=='S':
 ns['snum']((1,0,0,0,0),(1,0,0,0,0))
else:
 ns['X']=[(0,0,0,0,0),(1,0,0,0,0)]
 blocks=[]
 for node in source.body:
  if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='T' for t in node.targets):blocks.append(node)
  if isinstance(node,ast.For) and isinstance(node.target,ast.Name) and node.target.id=='x' and isinstance(node.iter,ast.Name) and node.iter.id=='X':blocks.append(node)
 exec(compile(ast.Module(body=blocks,type_ignores=[]),str(script),'exec'),ns)
print(json.dumps({'status':'INVALID_DIVISIBILITY_ACCEPTED','mode':mode,'source':str(script)}))
