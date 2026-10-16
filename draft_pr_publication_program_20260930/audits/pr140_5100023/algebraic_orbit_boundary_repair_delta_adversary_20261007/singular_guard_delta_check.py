import ast,json,sys,hashlib,os
from pathlib import Path
from datetime import datetime,timezone
A=Path(__file__).parent.parent
p=A/'repaired_candidate_v1'/'independent_checks.py'
source=p.read_bytes();tree=ast.parse(source)
wanted={'dot','det','sub','neg','anti'}
nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in wanted]
if {n.name for n in nodes}!=wanted:raise RuntimeError('function source scope')
env={};exec(compile(ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[])),str(p),'exec',optimize=sys.flags.optimize),env)
if env['anti']((1,0),(0,1),0)!=(1,1):raise RuntimeError('positive line solver')
try:env['anti']((1,0),(-1,0),0)
except RuntimeError as e:
 if str(e)!="Singular antipedal line system":raise
 rejected=True
else:raise RuntimeError('singular guard accepted')
r={'schema':'pr140-repair-singular-guard-production-method-control/v1','verdict':'PASS','actual_PID':os.getpid(),'UTC':datetime.now(timezone.utc).isoformat(),'optimized':sys.flags.optimize>0,'positive_line_solver':True,'singular_line_explicit_runtime_failure':rejected,'source_sha256':hashlib.sha256(source).hexdigest(),'full_verifier_loops_executed':False,'control_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(sys.argv[1]).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
