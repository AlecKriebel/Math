#!/usr/bin/env python3
"""Fresh counterchecks of explicitly unclaimed global-OPT and B=1 extensions."""
from pathlib import Path
from itertools import product
from collections import Counter
import ast,datetime,hashlib,json,os
O=Path(__file__).resolve().parent
p=O/'independent_diagnostics.py';tree=ast.parse(p.read_text())
# Reuse our freshly written construction/distance evaluator only; no packaged or
# historical checker is imported and none of its top-level tests runs here.
names={'ck','make','distances','trees','value'}
body=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom)) or isinstance(n,ast.FunctionDef) and n.name in names]
ns={'checks':Counter()};exec(compile(ast.Module(body=body,type_ignores=[]),str(p),'exec'),ns)
results=[]
for cs,B in [(((1,2),(2,),(-2,)),1),(((1,2),(2,),(2,),(2,),(-2,),(-2,),(-2,)),2),(((1,2),(2,),(2,),(2,),(-2,),(-2,),(-2,)),3)]:
 I=ns['make'](cs,B);vals=[];structured=[];witness=None
 for es,d in ns['trees'](I['N'],I['edges']):
  F=sum(ns['value'](I,es,d));vals.append(F)
  if (0,1) in es and sum(v>=I['n']+2 for u,v in es)==I['m']:structured.append(F)
  if F<=I['K']:witness=es
 unsat=min(sum(not any(a[abs(l)-1]==(l>0) for l in c) for c in cs) for a in product((False,True),repeat=I['n']))
 if B==1:ns['ck'](unsat>0 and witness is not None and min(vals)==I['K']==5,'unclaimed_B1_extension_falsified')
 else:ns['ck'](min(vals)<min(structured)==I['K']+unsat,'unclaimed_global_OPT_identity_falsified')
 results.append(dict(clauses=cs,B=B,N=I['N'],tree_count=len(vals),K=I['K'],global_minimum=min(vals),structured_minimum=min(structured),minimum_unsatisfied=unsat,threshold_witness=witness))
r=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_PID=os.getpid(),first_party_evaluator_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),results=results,all_pass=True,scope='Counterexamples concern extensions explicitly unclaimed by current note; not counterexamples to theorem.')
(O/'BOUNDARY_DIAGNOSTICS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
