#!/usr/bin/env python3
"""Exact finite-rectangle Boolean search, with OPTIONAL symmetry restrictions.

Per cell: K,R mutually exclusive. Per open ray: first K / first R Booleans,
defined by neighbor recursion and false beyond board boundary. Knight jump
constraints and directed rook visibility constraints are imposed separately.
No attack-incidence equality is used. Unsat applies only to this rectangle
and any specified restrictions, never to all finite placements.
"""
import argparse,json,re,time
from pathlib import Path
from z3shim import Solver
ROOT=Path(__file__).resolve().parents[1]

def op(name,args):
    args=list(args)
    if not args:return 'true' if name=='and' else 'false'
    if len(args)==1:return args[0]
    return '('+name+' '+' '.join(args)+')'
def eqcount(xs,n):
    if len(xs)<n:return 'false'
    if not xs:return 'true' if n==0 else 'false'
    return f'((_ pbeq {n} '+' '.join('1' for _ in xs)+') '+' '.join(xs)+')'

def model(w,h,n=4,m=2,sym='none',parity=False,min_k=1,max_k=None):
    lines=[];declared=set()
    def var(kind,p,d=None):
        v=f'{kind}_{p[0]}_{p[1]}' + (f'_{d}' if d is not None else '')
        if v not in declared:
            lines.append(f'(declare-const {v} Bool)');declared.add(v)
        return v
    def ast(s):lines.append('(assert '+s+')')
    cells=[(x,y) for y in range(h) for x in range(w)]
    K={p:var('K',p) for p in cells};R={p:var('R',p) for p in cells}
    dirs=[(1,0),(-1,0),(0,1),(0,-1)]
    jumps=[(a,b) for a in [-2,-1,1,2] for b in [-2,-1,1,2] if abs(a)+abs(b)==3]
    for p in cells:
        x,y=p
        ast(f'(not (and {K[p]} {R[p]}))')
        ns=[(x+a,y+b) for a,b in jumps if (x+a,y+b) in K]
        ast(f'(=> {K[p]} '+eqcount([R[q] for q in ns],n)+')')
        for q in ns:
            if p<q:ast(f'(not (and {K[p]} {K[q]}))')
        FK=[];FR=[]
        for d,(dx,dy) in enumerate(dirs):
            q=(x+dx,y+dy)
            fk=var('FK',p,d);fr=var('FR',p,d);FK.append(fk);FR.append(fr)
            if q not in K:
                ast(f'(not {fk})');ast(f'(not {fr})')
            else:
                empty=f'(not (or {K[q]} {R[q]}))'
                ast(f'(= {fk} (or {K[q]} (and {empty} {var("FK",q,d)})))')
                ast(f'(= {fr} (or {R[q]} (and {empty} {var("FR",q,d)})))')
        ast(f'(=> {R[p]} '+eqcount(FK,m)+')')
        ast(f'(=> {R[p]} (not '+op('or',FR)+'))')
        if parity and (x+y)%2:ast(f'(not {K[p]})')
    if min_k==1:ast(op('or',K.values()))
    else:ast(f'((_ pbge {min_k} '+' '.join('1' for _ in K)+') '+' '.join(K.values())+')')
    ast(op('or',R.values()))
    if max_k is not None:ast(f'((_ pble {max_k} '+' '.join('1' for _ in K)+') '+' '.join(K.values())+')')
    for p in cells:
        x,y=p
        qs=[]
        if sym in ['rot180','rot90','d4','xy']:qs.append((w-1-x,h-1-y))
        if sym in ['rot90','d4']:
            if w!=h:raise ValueError('rot90 and d4 require square')
            qs.append((w-1-y,x))
        if sym in ['xy','d4']:qs.extend([(w-1-x,y),(x,h-1-y)])
        for q in qs:
            if p!=q:
                ast(f'(= {K[p]} {K[q]})');ast(f'(= {R[p]} {R[q]})')
    return '\n'.join(lines),list(K.values())+list(R.values())

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--width',type=int,default=8);p.add_argument('--height',type=int)
    p.add_argument('--knight-degree',type=int,default=4);p.add_argument('--rook-degree',type=int,default=2)
    p.add_argument('--symmetry',choices=['none','rot180','rot90','d4','xy'],default='none')
    p.add_argument('--parity',action='store_true');p.add_argument('--min-knights',type=int,default=1)
    p.add_argument('--max-knights',type=int);p.add_argument('--timeout',type=float,default=30)
    p.add_argument('--seed',type=int,default=1);p.add_argument('--name')
    a=p.parse_args();a.height=a.height or a.width
    name=a.name or f'{a.width}x{a.height}_N{a.knight_degree}R{a.rook_degree}_{a.symmetry}_p{int(a.parity)}_s{a.seed}'
    text,vs=model(a.width,a.height,a.knight_degree,a.rook_degree,a.symmetry,a.parity,a.min_knights,a.max_knights)
    prefix=f'(set-option :timeout {int(a.timeout*1000)})\n(set-option :sat.random_seed {a.seed})\n(set-option :smt.random_seed {a.seed})\n'
    path=ROOT/'data'/f'{name}.smt2';path.write_text(prefix+text+'\n(check-sat)\n')
    s=Solver();print('Z3',s.version(),'problem',name,'bytes',len(text),flush=True)
    st=time.time();out=s.eval(prefix+text+'\n(check-sat)\n');elapsed=time.time()-st
    print(out,'elapsed',elapsed,flush=True)
    meta={'name':name,'arguments':vars(a),'z3_version':s.version(),'elapsed':elapsed,'status':out.strip()}
    if out.strip()=='sat':
        vals=s.eval('(get-value ('+' '.join(vs)+'))')
        (ROOT/'logs'/f'{name}_raw_model.txt').write_text(vals)
        true=re.findall(r'\(([KR])_(\d+)_(\d+)\s+true\)',vals)
        data={'knights':[[int(x),int(y)] for k,x,y in true if k=='K'],
              'rooks':[[int(x),int(y)] for k,x,y in true if k=='R'],'search':meta}
        wp=ROOT/'data'/f'{name}_candidate.json';wp.write_text(json.dumps(data,indent=2)+'\n')
        print('CANDIDATE',len(data['knights']),'knights',len(data['rooks']),'rooks at',wp,flush=True)
    else:
        print(s.eval('(get-info :reason-unknown)'),flush=True)
    stats=s.eval('(get-info :all-statistics)')
    (ROOT/'logs'/f'{name}.json').write_text(json.dumps(meta,indent=2)+'\n')
    (ROOT/'logs'/f'{name}_stats.txt').write_text(stats)
    s.close()
if __name__=='__main__':main()
