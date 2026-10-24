#!/usr/bin/env python3
"""Independent small exact checks of local barriers and product constructions."""
from itertools import combinations,permutations
from math import prod
from pathlib import Path
import json,datetime
from independent_audit import encoded_sum,need

HERE=Path(__file__).resolve().parent

def local_trades():
    reports=[]
    for p in (3,5,7,11,13):
        tested=0;found=None
        for k in range(3,p+1):
            for B in combinations(range(1,p),k-1):
                target={(2*a)%p for a in (0,)+B}
                for tail in permutations(B):
                    if tail[0]>tail[-1]:continue
                    c=(0,)+tail;tested+=1
                    colors={(c[i]+c[(i+1)%k])%p for i in range(k)}
                    if colors==target:found=c;break
                if found:break
            if found:break
        need(len(found)=={3:3,5:4,7:5,11:5,13:6}[p],'trade minimum disagreement')
        reports.append({'prime':p,'minimum_connected_cycle_support':len(found),'witness':found,'smaller_candidates_exhausted':True,'cycles_examined':tested})
    return reports

def successor_switches():
    out=[]
    for p in (3,5,7):
        rainbow=swaps=0
        for pi in permutations(range(p)):
            colors=[(a+pi[a])%p for a in range(p)]
            if len(set(colors))!=p:continue
            rainbow+=1
            for a,b in combinations(range(p),2):
                sigma=list(pi);sigma[a],sigma[b]=sigma[b],sigma[a]
                need(len({(x+sigma[x])%p for x in range(p)})<p,'rainbow two-successor switch')
                swaps+=1
        out.append({'group_order':p,'rainbow_permutations':rainbow,'successor_swaps_falsified':swaps})
    return out

def product_checks():
    bases=[((5,),[0,1,2,3,4],[1,2,4,3],[1,0,4,3,2],[1,3,4,2],5),
           ((3,3),[0,1,2,3,4,5,6,7,8],[2,5,4,6,1,7,8,3],[4,3,2,1,0,8,7,6,5],[4,6,1,7,8,3,2,5],3)]
    records=[]
    for mods,full,punctured,path_full,path_punctured,hsize in bases:
        for c in (full,punctured):
            need(len({encoded_sum(c[i],c[(i+1)%len(c)],mods) for i in range(len(c))})==len(c),'base rainbow cycle')
        need(path_full[0]==path_punctured[0] and path_full[-1]==path_punctured[-1],'different common edge endpoints')
        for mask in range(2**hsize):
            c=[(a,h) for h in range(hsize) for a in (path_punctured if mask>>h&1 else path_full)]
            expected={(a,h) for h in range(hsize) for a in range(prod(mods)) if a or not(mask>>h&1)}
            need(set(c)==expected and len(c)==len(expected),'product vertices')
            colors={(encoded_sum(c[i][0],c[(i+1)%len(c)][0],mods),(c[i][1]+c[(i+1)%len(c)][1])%hsize) for i in range(len(c))}
            need(len(colors)==len(c),'product repeated color')
        records.append({'base_moduli':mods,'H_order':hsize,'all_D_checked':2**hsize})
    natural=[]
    for mods in ((3,),(5,),(3,3),(3,5),(3,3,3),(5,5),(3,7),(3,5,7)):
        q=prod(mods);need(len({encoded_sum(i,(i+1)%q,mods) for i in range(q)})==q,'mixed radix cycle')
        natural.append({'moduli':mods,'order':q})
    bad=[]
    for tail in permutations((1,2,4)):
        c=(0,)+tail
        if c[1]>c[-1]:continue
        E={frozenset((c[i],c[(i+1)%4])) for i in range(4)}
        if frozenset((0,1)) not in E:continue
        colors=[(c[i]+c[(i+1)%4])%5 for i in range(4)]
        need(len(set(colors))<4,'unexpected prescribed-edge witness')
        bad.append({'cycle':c,'colors':colors})
    need(len(bad)==2,'prescribed-edge enumeration')
    return {'punctured_fibers':records,'mixed_radix_examples':natural,'prescribed_edge_failure':bad}

if __name__=='__main__':
    r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'connected_trade_minima':local_trades(),
       'successor_switches':successor_switches(),'product':product_checks(),'passed':True}
    (HERE/'local_product_results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
