"""Execute only each sealed family's explicit guard on a false claim."""
from pathlib import Path
import ast,json,sys,os
A=Path(__file__).resolve().parent
families=[
("ideal_hypotheses_adversary_20261006","independent_ideal_controls.py","check","AuditFailure"),
("polytope_fiber_adversary_20261006","independent_polytope_audit.py","require","RuntimeError"),
("primary_source_scope_adversary_20261006","source_scope_controls.py","require","ValueError")]
results=[]
for folder,name,function,expected in families:
 p=A/folder/name
 tree=ast.parse(p.read_text())
 if any(isinstance(n,ast.Assert) for n in ast.walk(tree)):raise ValueError("Unexpected assert guard")
 nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==function]
 nodes=[n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=="AuditFailure"]+nodes
 namespace={"COUNTS":{},"CHECKS":0,"checks":0}
 exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p)+":false-guard-only","exec"),namespace)
 try:namespace[function](False,"root deliberately false claim")
 except Exception as error:
  if type(error).__name__!=expected:raise
  results.append({"family":folder,"false_claim_rejected":True,"exception":expected})
 else:raise ValueError("False claim accepted: "+folder)
print(json.dumps({"actual_PID":os.getpid(),"optimized":bool(sys.flags.optimize),"status":"PASS","results":results},indent=2,sort_keys=True))

