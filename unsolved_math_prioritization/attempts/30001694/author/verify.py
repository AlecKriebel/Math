#!/usr/bin/env python3
"""Independent exact replay using complement flood fill, DP and diagonals."""
import csv,json,hashlib
from pathlib import Path
from collections import Counter

def reach(region):
    if not region:return set()
    seen={min(region)};q=list(seen)
    while q:
        x,y=q.pop()
        for a,b in [(x,y+1),(x,y-1),(x+1,y),(x-1,y)]:
            if (a,b) in region and (a,b) not in seen:seen.add((a,b));q.append((a,b))
    return seen

def admissible(c):
    if not c or len(reach(c))!=len(c):return False
    free={(x,y) for x in range(-1,5) for y in range(-1,5)}-c
    if len(reach(free))!=len(free):return False
    for x in range(5):
        for y in range(5):
            b=[(x-1,y-1) in c,(x,y-1) in c,(x,y) in c,(x-1,y) in c]
            if b in [[True,False,True,False],[False,True,False,True]]:return False
    return True

def params(c):
    # A point is interior iff its four incident cells are all occupied.
    vertices=set()
    for x in range(5):
        for y in range(5):
            k=sum(q in c for q in [(x-1,y-1),(x,y-1),(x,y),(x-1,y)])
            if 0<k<4:vertices.add((x,y))
    dp={};s=0
    for y in range(4):
        for x in range(4):
            dp[x,y]=1+min(dp.get((x-1,y),0),dp.get((x,y-1),0),dp.get((x-1,y-1),0)) if (x,y) in c else 0
            s=max(s,dp[x,y])
    sq=set();best=0
    for p in vertices:
        for r in vertices:
            if p>=r:continue
            x,y=p;X,Y=r
            bn=(x+X-y+Y,y+Y+x-X);dn=(x+X+y-Y,y+Y-x+X)
            if any(z%2 for z in (*bn,*dn)):continue
            b=(bn[0]//2,bn[1]//2);d=(dn[0]//2,dn[1]//2)
            if b in vertices and d in vertices:
                q=tuple(sorted((p,r,b,d)))
                if len(set(q))!=4:continue
                sq.add(q);diag=(X-x)**2+(Y-y)**2
                assert diag%2==0;best=max(best,diag//2)
    return s,best,vertices,sq

def check_certificate(path):
    with path.open() as f: rows=list(csv.DictReader(f))
    lookup={int(r['mask']):r for r in rows}
    assert len(lookup)==len(rows),'duplicate certificate mask'
    count=0;by=Counter()
    for mask in range(1,65536):
        c={(x,y) for y in range(4) for x in range(4) if mask&(1<<(4*y+x))}
        ok=admissible(c)
        assert (mask in lookup)==ok,('admissibility/missing row',mask)
        if not ok:continue
        row=lookup[mask];s,m,B,sq=params(c);count+=1;by[s]+=1
        assert int(row['s'])==s and int(row['max_side_squared'])==m,('parameters',mask)
        w=tuple(sorted((int(row['x'+str(i)]),int(row['y'+str(i)])) for i in range(4)))
        assert w in sq,('square witness',mask)
        ds=sorted((w[i][0]-w[j][0])**2+(w[i][1]-w[j][1])**2 for i in range(4) for j in range(i))
        assert ds==[m,m,m,m,2*m,2*m],('maximal witness',mask)
        ox,oy=int(row['block_x']),int(row['block_y'])
        assert all((ox+i,oy+j) in c for i in range(s) for j in range(s)),('block',mask)
        assert 2*m>=s*s,('target',mask)
    assert count==9349 and by=={1:2932,2:6034,3:382,4:1}
    return {'admissible':count,'by_s':dict(sorted(by.items())),'complete_mask_range':[1,65535],'passed':True}

def controls():
    cases={'unit':({(0,0)},True),'rectangle':({(x,y) for x in range(3) for y in range(2)},True),'disconnected':({(0,0),(2,2)},False),'ring':({(x,y) for x in range(3) for y in range(3)}-{(1,1)},False),'pinched':({(0,1),(0,0),(1,0),(2,0),(2,1),(2,2),(1,2)},False)}
    out={}
    for name,(c,want) in cases.items():
        got=admissible(c);assert got==want,(name,got);out[name]={'admissible':got}
    c={(i%4,i//4) for i in range(16) if 886>>i&1};s,m,B,sq=params(c)
    assert admissible(c) and s==2 and m==5
    axis=[q for q in sq if len({x for x,y in q})==2 and len({y for x,y in q})==2]
    assert not axis
    out['axis_only_restriction']={'mask':886,'cells':sorted(c),'s':s,'maximum_squared_side':m,'axis_aligned_square_count':len(axis),'all_lattice_squares':[list(q) for q in sorted(sq)]}
    # The maximum 2-square at (1,1) has (1,1) strictly interior.
    c={(1,1),(2,1),(1,2),(2,2),(0,0),(0,1),(1,0)}
    assert admissible(c);s,m,B,sq=params(c);assert s==2 and (1,1) not in B
    out['maximal_block_corner_not_boundary']={'cells':sorted(c),'s':2,'block_origin':[1,1],'interior_block_corner':[1,1]}
    # A real boundary square need not be contained inside the polyomino.
    c={(0,0),(1,0),(2,0),(0,1),(2,1),(0,2),(2,2)}
    assert admissible(c);s,m,B,sq=params(c)
    q=tuple(sorted(((0,0),(3,0),(3,3),(0,3))))
    assert q in sq and (1,1) not in c
    out['boundary_vertices_do_not_force_interior_containment']={'cells':sorted(c),'boundary_square':q,'missing_interior_cell':[1,1]}
    return out

if __name__=='__main__':
    root=Path(__file__).resolve().parent
    results=check_certificate(root/'computation/certificate.csv')
    results['negative_controls']=controls()
    (root/'computation/verification.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))
