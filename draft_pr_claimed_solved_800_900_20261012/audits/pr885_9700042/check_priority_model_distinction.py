#!/usr/bin/env python3
"""Finite diagnostic for the model comparison; no asymptotic inference."""
import json
N=2
marks={((0,0),(1,0)),((1,0),(1,1)),((0,1),(0,2)),((0,2),(1,2))}
paths=[]
def visit(path):
 x,y=path[-1]
 if (x,y)==(N,N):
  paths.append(path);return
 for u,v in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
  if 0<=u<=N and 0<=v<=N and (u,v) not in path:visit(path+[(u,v)])
visit([(0,0)])
rows=[]
for path in paths:
 b=kf=kb=0
 for u,v in zip(path,path[1:]):
  if sum(v)>sum(u):kf+=int((u,v) in marks)
  else:b+=1;kb+=int((v,u) in marks)
 target_cost=2*N+b-kf
 ordinary_cost=2*N+2*b-kf-kb
 if ordinary_cost-target_cost!=b-kb or kb>b or ordinary_cost<target_cost:raise SystemExit("pointwise comparison failed")
 rows.append({"path":path,"backward_steps":b,"marked_forward":kf,"marked_backward":kb,"target_cost":target_cost,"ordinary_cost":ordinary_cost})
target=min(r["target_cost"] for r in rows);ordinary=min(r["ordinary_cost"] for r in rows)
if (target,ordinary)!=(1,2):raise SystemExit("model distinction failed")
witness=next(r for r in rows if r["target_cost"]==target)
result={"scope":"Exact finite Q_2 model distinction only; does not disprove equal asymptotic constants or rule out a stronger prior corollary.","status":"PASS","simple_corner_paths_exhausted":len(rows),"marked_forward_edges":sorted(marks),"target_min_cost":target,"ordinary_confined_min_cost":ordinary,"target_max_defect":2*N-target,"ordinary_confined_max_defect":2*N-ordinary,"pointwise_identity":"ordinary_cost-target_cost=b-k_b >= 0","target_optimum_witness":witness,"all_path_scores":rows}
print(json.dumps(result,indent=2))
