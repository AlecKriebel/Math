"""Fresh arm-augmented ranks and mixed-graph isomorphisms from printed cores."""
import itertools as it,json,time
from pathlib import Path
import sympy as S
import networkx as nx
from independent_controls import fourier
F=S.Rational
out=Path(__file__).parent
cores={
'theta0':([('S','U'),('S','V'),('U','X'),('V','X'),('U','V')],['X'],[(2,3),(3,4)]),
'theta1':([('S','U'),('S','X'),('V','X'),('U','V'),('U','V')],['X'],[(2,3),(2,4)]),
'theta3':([('S','U'),('S','X0'),('V','X0'),('U','X1'),('V','X1'),('U','V')],['X0','X1'],[(2,),(4,)])}
def build(core,repair):
    seg,sinks,_=cores[core];es=[('r','S'),('r','L0')];k=1
    for i,(u,v) in enumerate(seg):
        if i in repair:
            n='P'+str(i);es.extend([(u,n),(n,v),(n,'L'+str(k))]);k+=1
        else:es.append((u,v))
    for s in sinks:es.append((s,'L'+str(k)));k+=1
    return es,['L'+str(i) for i in range(k)]
def mixed(es,leaves):
    G=nx.Graph();ret={v for u,v in es if sum(w==v for _,w in es)==2}
    for u,v in es:
        if u!='r':G.add_edge(u,v,head=v if v in ret else '')
    rc=[v for u,v in es if u=='r'];G.add_edge(*rc,head='')
    for v in G:G.nodes[v]['label']=leaves.index(v) if v in leaves else None
    return G
def iso(G,H):
    gm=nx.algorithms.isomorphism.GraphMatcher(G,H,node_match=lambda a,b:(a['label'] is None)==(b['label'] is None))
    for m in gm.isomorphisms_iter():
        if all((not d['head'] and not H.edges[m[u],m[v]]['head']) or (d['head'] and m[d['head']]==H.edges[m[u],m[v]]['head']) for u,v,d in G.edges(data=True)):return m
    return None
def run():
    results=[];graphs=[]
    chars=sorted({min(h,tuple(3 if a==1 else 1 if a==3 else a for a in h)) for h in it.product(range(4),repeat=4) if h[0]^h[1]^h[2]^h[3]==0})
    for core,(_,_,repairs) in cores.items():
        for repair in repairs:
            es,leaves=build(core,repair);graphs.append(mixed(es,leaves))
            ret={v:[u for u,w in es if w==v] for u,v in es if sum(w==v for _,w in es)==2}
            params={e:S.symbols('s'+str(i)+' g'+str(i)) for i,e in enumerate(es)}
            ls=S.symbols('l0:'+str(len(ret)))
            weights={v:{ps[0]:l,ps[1]:1-l} for (v,ps),l in zip(ret.items(),ls)}
            polys=[fourier(es,leaves,params,weights,h) for h in chars]
            variables=sum((list(p) for p in params.values()),[])+list(ls)
            point={v:F(2*i+3,7*i+13) for i,v in enumerate(variables)}
            jac=S.Matrix(polys).jacobian(variables).subs(point)
            internal=[2*i+j for i,e in enumerate(es) if e[1] not in leaves for j in range(2)]+list(range(2*len(es),len(variables)))
            rank_full=jac.rank();rank_internal=jac[:,internal].rank()
            results.append({'core':core,'repair':repair,'rank_internal':rank_internal,'rank_with_arms':rank_full,'rank_quotient':rank_full-8})
    isos=[]
    for i,j in it.combinations(range(6),2):
        m=iso(graphs[i],graphs[j])
        if m:isos.append({'source':i,'target':j,'mapping':m,'ranks':[results[i],results[j]]})
    return {'ranks':results,'isomorphisms_allowing_port_permutation':isos}
if __name__=='__main__':
    t=time.monotonic();r=run();r['wall_seconds']=time.monotonic()-t
    out.joinpath('rank-gauge-controls.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
