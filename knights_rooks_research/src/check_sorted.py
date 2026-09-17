#!/usr/bin/env python3
"""Second attack reconstruction: explicit jumps and sorted row/column neighbors.
Independent of check.py and all search / certificate modules.
"""
import argparse,json
from collections import defaultdict
from pathlib import Path

def reconstruct(data,n=4,m=2):
    positions={}
    for label,key in [('K','knights'),('R','rooks')]:
        coords=data[key]
        if not isinstance(coords,list) or not coords:raise ValueError('nonempty lists required')
        for p in coords:
            if len(p)!=2 or any(type(v)!=int for v in p):raise ValueError('integer pair required')
            q=tuple(p)
            if q in positions:raise ValueError('repeated or overlapping square')
            positions[q]=label
    rows=defaultdict(list);cols=defaultdict(list)
    for x,y in positions:rows[y].append(x);cols[x].append(y)
    visible=defaultdict(dict)
    for y,xs in rows.items():
        xs.sort()
        for i,x in enumerate(xs):
            visible[x,y]['W']=(xs[i-1],y) if i else None
            visible[x,y]['E']=(xs[i+1],y) if i+1<len(xs) else None
    for x,ys in cols.items():
        ys.sort()
        for i,y in enumerate(ys):
            visible[x,y]['S']=(x,ys[i-1]) if i else None
            visible[x,y]['N']=(x,ys[i+1]) if i+1<len(ys) else None
    attacks=[];valid=True
    for piece in ('K','R'):
        for x,y in sorted(p for p,t in positions.items() if t==piece):
            p=(x,y)
            if piece=='K':
                candidates=[(x+2,y+1),(x+2,y-1),(x-2,y+1),(x-2,y-1),
                            (x+1,y+2),(x+1,y-2),(x-1,y+2),(x-1,y-2)]
                targets=[q for q in candidates if q in positions]
            else:targets=[q for q in visible[p].values() if q is not None]
            ks=sorted(q for q in targets if positions[q]=='K')
            rs=sorted(q for q in targets if positions[q]=='R')
            rec={'piece':piece,'at':p,'attacks_knights':ks,'attacks_rooks':rs}
            if piece=='K':valid &= (not ks and len(rs)==n)
            else:
                valid &= (not rs and len(ks)==m)
                rec['rays']=visible[p]
            attacks.append(rec)
    return {'valid':bool(valid),'attacks':attacks}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('coordinates',type=Path)
    p.add_argument('--knight-degree',type=int,default=4);p.add_argument('--rook-degree',type=int,default=2)
    a=p.parse_args();r=reconstruct(json.loads(a.coordinates.read_text()),a.knight_degree,a.rook_degree)
    print(json.dumps(r,indent=2));raise SystemExit(0 if r['valid'] else 1)
