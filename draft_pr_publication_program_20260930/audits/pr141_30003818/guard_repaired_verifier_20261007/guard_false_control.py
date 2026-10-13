import ast,sys
from pathlib import Path
p=Path(sys.argv[1]);tree=ast.parse(p.read_bytes());f=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='ck');env={'N':0,'counts':{}};exec(compile(ast.Module(body=[f],type_ignores=[]),str(p),'exec'),env);env['ck'](False,'intentional_false_diagnostic')
