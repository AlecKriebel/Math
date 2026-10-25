#!/usr/bin/env python3
"""Exact p-primary Smith valuations for p^2 times the lattice derivation map.
Elementary row/column operations take place in Z/(p^precision). Only units
are inverted; division by p^v occurs only when divisibility is checked.
"""
from __future__ import annotations
from itertools import combinations
from pathlib import Path
from collections import Counter
import argparse,json,time
import numpy as np
from lie31 import D

def coefficient_table(p:int,Ca,weights):
    table={}
    for i,j in combinations(range(D),2):
        for k in np.flatnonzero(Ca[i,j]):
            exponent=2+int(weights[i])+int(weights[j])-int(weights[k])
            assert exponent>=0
            table[i,j,int(k)]=int(Ca[i,j,k])*p**exponent
            table[j,i,int(k)]=-table[i,j,int(k)]
    return table

def derivation_rows(C):
    for i,j in combinations(range(D),2):
        for k in range(D):
            row={}
            def add(j,a):
                value=row.get(j,0)+a
                if value: row[j]=value
                else: row.pop(j,None)
            for a in range(D):
                if (v:=C.get((i,j,a),0)): add(k*D+a,v)
                if (v:=C.get((a,j,k),0)): add(a*D+i,-v)
                if (v:=C.get((i,a,k),0)): add(a*D+j,-v)
            yield row

def valuation(a,p,precision):
    if not a: return precision
    v=0
    while a%p==0: a//=p; v+=1
    return v

def smith(rows,p,precision,plan=None):
    modulus=p**precision
    rows={i:{j:a%modulus for j,a in row.items() if a%modulus}
          for i,row in enumerate(rows) if row}
    rows={i:r for i,r in rows.items() if r}
    cols={}
    for i,row in rows.items():
        for j in row: cols.setdefault(j,set()).add(i)
    pivots=[]; start=time.perf_counter(); plan_iter=iter(plan) if plan is not None else None
    while rows:
        if plan_iter is not None:
            item=next(plan_iter); i,j,want=item['row'],item['col'],item['valuation']
            v=valuation(rows[i][j],p,precision)
            assert v==want
            # Independent verification also checks global minimal valuation.
            assert all(a%(p**v)==0 for row in rows.values() for a in row.values())
        else:
            best=None
            for ii,row in rows.items():
                rowlength=len(row)
                for jj,a in row.items():
                    vv=valuation(a,p,precision)
                    key=(vv,(rowlength-1)*(len(cols[jj])-1),rowlength+len(cols[jj]),ii,jj)
                    if best is None or key<best: best=key
            assert best is not None
            v,_,_,i,j=best
        row=rows[i]; power=p**v; unit=row[j]//power
        inverse=pow(unit,-1,modulus)
        row={k:a*inverse%modulus for k,a in row.items()}
        assert row[j]==power
        assert all(a%power==0 for a in row.values())
        affected=list(cols[j]-{i})
        for ii in affected:
            target=rows[ii]
            assert target[j]%power==0
            factor=target[j]//power
            for k,a in row.items():
                old=target.get(k,0); new=(old-factor*a)%modulus
                if new:
                    target[k]=new
                    if not old: cols.setdefault(k,set()).add(ii)
                elif old:
                    target.pop(k); cols[k].remove(ii)
                    if not cols[k]: cols.pop(k)
            assert j not in target
            if not target: rows.pop(ii)
        # Once column j has been cleared, clearing the other entries in the
        # pivot row by column operations changes no other row.
        for k in row:
            cols[k].remove(i)
            if not cols[k]: cols.pop(k)
        rows.pop(i)
        pivots.append({'row':i,'col':j,'valuation':v})
        if len(pivots)%100==0:
            print(json.dumps({'pivots':len(pivots),'last_valuation':v,'remaining_rows':len(rows),
                              'remaining_nnz':sum(map(len,rows.values())), 'seconds':time.perf_counter()-start}),flush=True)
    if plan_iter is not None: assert next(plan_iter,None) is None
    return pivots

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--precision',type=int,default=12)
    parser.add_argument('--verify-plan',action='store_true'); args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]; data=np.load(root/'data/lie31_tables.npz')
    p=1009; start=time.perf_counter()
    C=coefficient_table(p,data['Ca'],data['weights'])
    rows=list(derivation_rows(C))
    plan=json.loads((root/'data/smith_pivot_plan.json').read_text()) if args.verify_plan else None
    pivots=smith(rows,p,args.precision,plan)
    assert len(pivots)==931
    val=[q['valuation'] for q in pivots]; counts=dict(sorted(Counter(val).items()))
    # Divide the matrix by p^2 to return to delta_A.
    Csum=sum(val)-2*931
    result={'prime':p,'precision':args.precision,'rank':len(val),'scaled_smith_valuation_multiplicities':counts,
        'unscaled_smith_valuation_multiplicities':{v-2:n for v,n in counts.items()},
        'sum_unscaled_smith_valuations':Csum,'maximum_unscaled_smith_valuation':max(val)-2,
        'elapsed_seconds':time.perf_counter()-start,'mode':'verify_plan' if args.verify_plan else 'construct_plan'}
    if not args.verify_plan:
        (root/'data/smith_pivot_plan.json').write_text(json.dumps(pivots,indent=2)+'\n')
    name=f'smith_{"verify" if args.verify_plan else "compute"}_precision_{args.precision}.json'
    (root/'logs'/name).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
