import ast,json,os,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parent
p=R/'helper_controls.py';tree=ast.parse(p.read_text())
class Explicit(ast.NodeTransformer):
 def visit_Assert(self,n):return ast.copy_location(ast.If(test=ast.UnaryOp(op=ast.Not(),operand=n.test),body=[ast.Raise(exc=ast.Call(func=ast.Name(id='RuntimeError',ctx=ast.Load()),args=[ast.Constant('Reviewer harness expectation failed: '+ast.unparse(n.test))],keywords=[]),cause=None)],orelse=[]),n)
# Keep the human-authored source; execute its assertion-equivalent explicit checks.
tree=ast.fix_missing_locations(Explicit().visit(tree));q=R/'private/helper_explicit.py';q.write_text(ast.unparse(tree)+'\n')
# __file__ must identify the public harness so all fixture paths stay correct.
runner=R/'private/helper_launcher.py';runner.write_text('import pathlib,sys\np=pathlib.Path(sys.argv.pop(1));sys.argv[0]=str(p)\nexec(compile(pathlib.Path('+repr(str(q))+').read_text(),str(p),"exec"),{"__file__":str(p),"__name__":"__main__"})\n')
rows=[]
for mode,flags,opt in [('normal',[],None),('O',['-O'],None),('OO',['-OO'],None),('env2',[],'2')]:
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
 if opt:env['PYTHONOPTIMIZE']=opt
 r=subprocess.run([sys.executable,*flags,'-B',str(runner),str(p),mode],env=env,capture_output=True,text=True,timeout=60)
 if r.returncode:raise RuntimeError(r.stderr)
 rows.append(json.loads(r.stdout));print(mode,r.stdout.strip(),flush=True)
(R/'HELPER_MODE_SUMMARY.json').write_text(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS_WITH_R6',modes=rows),indent=2)+'\n')
