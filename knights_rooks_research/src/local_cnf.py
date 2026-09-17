#!/usr/bin/env python3
"""Generate a NECESSARY local relaxation, not a bounded-board model.

Window x=-3..0, y=-3..3, arbitrary continuation outside except x>0 empty.
A=(0,0) is a knight. Four distinguished locations, when knights, must
attack >=4 rooks. Their full possible knight neighborhoods in x<=0 are
inside the window. Every local rook has <=2 locally occupied rays and no
unblocked local rook. Extra constraints on other knights, or lower bounds
on rook degree, are deliberately omitted. These omissions RELAX the target.
"""
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class CNF:
    def __init__(self):self.names={};self.clauses=[];self.reasons=[]
    def var(self,name):
        if name not in self.names:self.names[name]=len(self.names)+1
        return self.names[name]
    def add(self,clause,reason):
        self.clauses.append(list(clause));self.reasons.append(reason)

def build():
    c=CNF();P=[(x,y) for x in range(-3,1) for y in range(-3,4)]
    N={p:c.var(f'K({p[0]},{p[1]})') for p in P}
    R={p:c.var(f'R({p[0]},{p[1]})') for p in P}
    O={p:c.var(f'O({p[0]},{p[1]})') for p in P}
    for p in P:
        c.add([-N[p],-R[p]],f'disjoint {p}')
        c.add([-N[p],O[p]],f'K implies occupied {p}')
        c.add([-R[p],O[p]],f'R implies occupied {p}')
        c.add([-O[p],N[p],R[p]],f'occupied implies K or R {p}')
    directions=[(1,0),(-1,0),(0,1),(0,-1)]
    for p in P:
        rays=[]
        for dx,dy in directions:
            qs=[q for q in P if (q[0]-p[0])*dy==(q[1]-p[1])*dx
                and (q[0]-p[0])*dx+(q[1]-p[1])*dy>0]
            if not qs:continue
            ray=c.var(f'V({p[0]},{p[1]};{dx},{dy})');rays.append(ray)
            for q in qs:c.add([-O[q],ray],f'occupied {q} implies ray from {p} dir {(dx,dy)}')
            c.add([-ray]+[O[q] for q in qs],f'ray presence has local witness from {p} dir {(dx,dy)}')
        for triple in itertools.combinations(rays,3):
            c.add([-R[p]]+[-v for v in triple],f'rook has at most 2 locally occupied rays at {p}')
    for p,q in itertools.combinations(P,2):
        if p[0]==q[0]:between=[s for s in P if s[0]==p[0] and min(p[1],q[1])<s[1]<max(p[1],q[1])]
        elif p[1]==q[1]:between=[s for s in P if s[1]==p[1] and min(p[0],q[0])<s[0]<max(p[0],q[0])]
        else:continue
        c.add([-R[p],-R[q]]+[N[s] for s in between],f'rooks {p},{q} need intervening knight')
    distinguished=[(0,0),(-1,0),(-1,1),(-1,-1)]
    for p in distinguished:
        neighbors=[q for q in P if (abs(p[0]-q[0]),abs(p[1]-q[1])) in [(1,2),(2,1)]]
        rs=[R[q] for q in neighbors]
        # >=4 among t candidates means each (t-3)-subset contains a true bit.
        for sub in itertools.combinations(rs,len(rs)-3):
            c.add([-N[p]]+list(sub),f'knight at {p} has at least 4 rook targets')
    c.add([N[(0,0)]],'rightmost knight at origin')
    return c

def main():
    c=build();path=ROOT/'certificates/local_relaxation.cnf'
    path.write_text(f'p cnf {len(c.names)} {len(c.clauses)}\n'+''.join(' '.join(map(str,a))+' 0\n' for a in c.clauses))
    (ROOT/'certificates/local_variables.json').write_text(json.dumps(c.names,indent=2)+'\n')
    (ROOT/'certificates/local_clause_reasons.json').write_text(json.dumps(c.reasons,indent=2)+'\n')
    print(f'Wrote {path}: {len(c.names)} variables, {len(c.clauses)} clauses')
if __name__=='__main__':main()
