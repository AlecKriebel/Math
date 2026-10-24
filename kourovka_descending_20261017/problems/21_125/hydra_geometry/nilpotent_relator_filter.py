#!/usr/bin/env python3
"""Lazard Lie quotient by the actual Hydra relator, all arithmetic mod101.
Finite-computation family test only, no statement about all nilpotent quotients.
"""
from nilpotent_lie_filter import P,add,scalar,prod,exp,log,inverse,bracket,Span
from pathlib import Path
import json

def run(m,c):
    x={'x':1};y={'y':1};s=exp(x,c);t=exp(y,c)
    aa=[s]+[None]*m;aa[m]=t
    for i in range(m,1,-1):aa[i-1]=prod(prod(inverse(aa[i],c),s,c),aa[i],c)
    relation=log(prod(prod(prod(inverse(s,c),inverse(aa[1],c),c),s,c),aa[1],c),c)
    ideal=Span();todo=[]
    b=ideal.insert(relation)
    if b:todo.append(b)
    for b in todo:
        for g in (x,y):
            k=ideal.insert(bracket(g,b,c))
            if k:todo.append(k)
    gens=[log(aa[1],c)]+[log(prod(prod(aa[i],s,c),inverse(aa[i],c),c),c) for i in range(2,m+1)]
    span=Span()
    for b in todo:span.insert(b)
    queue=[]
    for g in gens:
        b=span.insert(g)
        if b:queue.append(b)
    for b in queue:
        for g in gens:
            k=span.insert(bracket(g,b,c))
            if k:queue.append(k)
    members=[]
    for i in range(m+1):
        rem=span.reduce(log(aa[i],c));members.append({'label':'s' if i==0 else 'alpha_'+str(i),'in_L_plus_relation_ideal':not rem,'remainder':rem})
    return {'rank':m,'class':c,'prime':P,'relator_ideal_dimension':len(ideal.rows),'L_plus_ideal_dimension':len(span.rows),'membership':members}
if __name__=='__main__':
    rows=[]
    for m in range(3,7):
        for c in range(m,10):
            r=run(m,c);rows.append(r);print(m,c,r['relator_ideal_dimension'],r['L_plus_ideal_dimension'],[(i['label'],i['in_L_plus_relation_ideal']) for i in r['membership']],flush=True)
    Path(__file__).with_name('nilpotent_relator_filter_results.json').write_text(json.dumps({'scope':'exact F101 Lie arithmetic in specified classes<=9 only; no all-class conclusion or virtual specialness conclusion','rows':rows},indent=2)+'\n')
