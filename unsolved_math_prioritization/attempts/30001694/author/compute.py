#!/usr/bin/env python3
"""Exact exhaustive 4 by 4 cell-subset check; Python standard library only."""
from collections import defaultdict, Counter
from pathlib import Path
import json, hashlib, itertools, argparse

def boundary(cells):
    edges=set()
    for x,y in cells:
        v=[(x,y),(x+1,y),(x+1,y+1),(x,y+1)]
        for a,b in zip(v,v[1:]+v[:1]):
            e=tuple(sorted((a,b)))
            if e in edges: edges.remove(e)
            else: edges.add(e)
    graph=defaultdict(set)
    for a,b in edges: graph[a].add(b);graph[b].add(a)
    return edges,graph

def connected(points,neighbors):
    if not points:return False
    start=next(iter(points));seen={start};todo=[start]
    while todo:
        for q in neighbors(todo.pop()):
            if q in points and q not in seen:seen.add(q);todo.append(q)
    return len(seen)==len(points)

def valid(cells):
    if not connected(cells,lambda p:((p[0]+1,p[1]),(p[0]-1,p[1]),(p[0],p[1]+1),(p[0],p[1]-1))):return False
    e,g=boundary(cells)
    return bool(g) and all(len(v)==2 for v in g.values()) and connected(g,lambda p:g[p])

def max_block(cells):
    if not cells:return 0,None
    best=0;w=None
    for x,y in sorted(cells):
        n=1
        while all((x+i,y+j) in cells for i in range(n) for j in range(n)):
            if n>best:best=n;w=(x,y)
            n+=1
    return best,w

def squares(vertices):
    pts=set(vertices);out=set()
    for x,y in pts:
        for a,b in pts:
            u,v=a-x,b-y
            if u==v==0:continue
            r=(a-v,b+u);t=(x-v,y+u)
            if r in pts and t in pts:out.add(tuple(sorted(((x,y),(a,b),r,t))))
    return out

def square_side2(q):
    a=q[0];return min((x-a[0])**2+(y-a[1])**2 for x,y in q[1:])

def analyze(cells):
    _,g=boundary(cells);sq=squares(g);s,origin=max_block(cells)
    ranked=sorted((square_side2(q),q) for q in sq)
    best,w=ranked[-1] if ranked else (0,())
    ax=max([n for n,q in ranked if len({x for x,y in q})==2 and len({y for x,y in q})==2]+[0])
    return s,best,w,origin,ax

def run(out):
    out.mkdir(parents=True,exist_ok=True)
    counts=Counter(); bys=Counter();certificate=[];best_ratio=None;minrow=None;axisbad=None
    n=4
    for mask in range(1,1<<(n*n)):
        cells={(i%n,i//n) for i in range(n*n) if mask>>i&1}
        if not valid(cells):counts['rejected']+=1;continue
        counts['jordan_polyominoes']+=1
        s,m,w,origin,axis=analyze(cells);bys[s]+=1
        if 2*m<s*s:raise AssertionError(('counterexample',mask,s,m,w))
        if best_ratio is None or m*best_ratio[1]<best_ratio[0]*s*s:best_ratio=(m,s*s);minrow=(mask,s,m,w)
        if 2*axis<s*s and axisbad is None:axisbad=(mask,s,m,axis)
        fields=[mask,s,m,origin[0],origin[1],*[z for q in w for z in q]]
        certificate.append(','.join(map(str,fields))+'\n')
    header='mask,s,max_side_squared,block_x,block_y,x0,y0,x1,y1,x2,y2,x3,y3\n'
    raw=(header+''.join(certificate)).encode();(out/'certificate.csv').write_bytes(raw)
    summary={'grid_cells':[4,4],'masks_examined':65535,'empty_mask_excluded':True,'counts':dict(counts),'by_s':dict(sorted(bys.items())),'minimum_max_side_squared_over_s_squared':best_ratio,'minimum_witness':minrow,'axis_only_failure_first':axisbad,'certificate_sha256':hashlib.sha256(raw).hexdigest(),'certificate_bytes':len(raw),'claim':'All nonempty subsets of the 4 by 4 cell box whose edge graph is connected and whose exposed-edge boundary is one simple cycle satisfy 2*M^2 >= s^2. No claim beyond this range.'}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'computation');a=p.parse_args();run(a.out)
