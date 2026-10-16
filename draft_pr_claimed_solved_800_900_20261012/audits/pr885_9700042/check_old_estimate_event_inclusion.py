#!/usr/bin/env python3
"""Exhaustive small-box diagnostics for the old-estimate event comparison.
All published-source bounds and unbounded-volume arguments remain analytic.
"""
import itertools,json
def require(ok,label):
 if not ok:raise RuntimeError(label)
counts={x:0 for x in ("full_mark_configurations","optimal_path_configurations","blocks","nonlast_local_comparisons","lower_comparisons","net_and_individual_negative_parts_differ")}
def run(N):
 vertices=list(itertools.product(range(N+1),repeat=2));M=N+1
 internal=[(u,v) for u in vertices for v in ((u[0]+1,u[1]),(u[0],u[1]+1)) if max(v)<=N]
 external=[(u,v) for u in vertices for v in ((u[0]+1,u[1]),(u[0],u[1]+1)) if max(v)>N]
 edges=internal+external;edge_idx={e:i for i,e in enumerate(edges)}
 paths=[]
 def visit(path):
  if path[-1]==(N,N):
   steps=[];fmask=0;b=0
   for u,v in zip(path,path[1:]):
    forward=sum(v)>sum(u);idx=edge_idx[(u,v)] if forward else None
    steps.append((forward,idx));b+=not forward
    if forward:fmask|=1<<idx
   paths.append((path,steps,fmask,b));return
  x,y=path[-1]
  for v in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
   if min(v)>=0 and max(v)<=N and v not in path:visit(path+[v])
 visit([(0,0)])
 outgoing=[(1<<edge_idx[(u,(u[0]+1,u[1]))])|(1<<edge_idx[(u,(u[0],u[1]+1))]) for u in vertices]
 def chain(open_sites):
  lengths=[]
  for j,w in enumerate(open_sites):
   lengths.append(1+max((lengths[i] for i,u in enumerate(open_sites[:j]) if u[0]<w[0] and u[1]<w[1]),default=0))
  return max(lengths,default=0)
 for imask in range(1<<len(internal)):
  rewards=[(imask&row[2]).bit_count()-row[3] for row in paths]
  D=max(rewards);require(0<=D<=2*N,"defect bounds")
  optimal=[row for row,r in zip(paths,rewards) if r==D]
  lower_sites=[u for u,om in zip(vertices,outgoing) if max(u)<N and imask&om]
  require(D>=chain(lower_sites),"strict-chain lower comparison");counts["lower_comparisons"]+=1
  for emask in range(1<<len(external)):
   mask=imask|(emask<<len(internal))
   opened={u for u,om in zip(vertices,outgoing) if mask&om}
   counts["full_mark_configurations"]+=1
   for path,steps,fmask,B in optimal:
    counts["optimal_path_configurations"]+=1
    selected=[u for u in path[1:-1] if u in opened]
    pts=[(0,0)]+selected+[(M,M)];p=len(selected);I0=int((0,0) in opened)
    k=(imask&fmask).bit_count()
    require(k<=p+I0,"forward reward tails")
    anchors=[0]
    while anchors[-1]<len(pts)-1:
     i=anchors[-1];anchors.append(next(j for j in range(i+1,len(pts)) if pts[i][0]<pts[j][0] and pts[i][1]<pts[j][1]))
    a=len(anchors)-1;L=0;G=H=Hnet=0
    pos={u:i for i,u in enumerate(path)}
    for block,(start,end) in enumerate(zip(anchors,anchors[1:])):
     counts["blocks"]+=1
     ell=end-start-1;L+=ell
     cur=pts[start:end]
     increments=[(v[0]-u[0],v[1]-u[1]) for u,v in zip(cur,cur[1:])]
     j=next((j for j in range(2) if cur[-1][j]<=cur[0][j]),0) if ell else 0
     require(sum(g[j] for g in increments)<=0,"distinguished coordinate")
     Gj=sum(abs(g[j]) for g in increments)
     Hj=sum(max(-g[1-j],0) for g in increments)
     Hnj=max(-sum(g[1-j] for g in increments),0)
     G+=Gj;H+=Hj;Hnet+=Hnj
     require(cur[-1][1-j]<=2*(ell+1)+pts[end][1-j],"source item4")
     if block<a-1:
      lo=pos[pts[start]];hi=pos[pts[end]]
      bseg=sum(not f for f,idx in steps[lo:hi])
      kseg=sum(f and bool(imask&(1<<idx)) for f,idx in steps[lo:hi])
      Istart=int(pts[start] in opened)
      require(kseg<=ell+Istart,"local tail count")
      require(bseg<=ell,"local monotone replacement")
      counts["nonlast_local_comparisons"]+=1
    require(p==a-1+L,"list identity")
    require(D-(a-1+I0)<=L-B,"anchor-score comparison")
    require(G+2*H<=2*B,"individual-negative-part variation bound")
    require(G+H<=2*B,"actual source item5 cost bound")
    if H!=Hnet:counts["net_and_individual_negative_parts_differ"]+=1
 return {"N":N,"simple_corner_paths":len(paths),"internal_edges":len(internal),"extra_outgoing_boundary_edges":len(external)}
boxes=[run(N) for N in (1,2)]
print(json.dumps({"status":"PASS","scope":"Exact finite diagnostics only; not a proof of BGT estimates, priority, or asymptotic result.","boxes":boxes,"counts":counts,"source_negative_part_convention":"sum of individual negative increments, not negative part of their sum","startup":"python3 -I -S -B; explicit RuntimeError checks survive optimization"},indent=2))
