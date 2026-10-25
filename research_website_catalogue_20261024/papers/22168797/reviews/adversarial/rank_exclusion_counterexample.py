"""Reproduce false raw4 rank exclusion 137124, without repairing any source.

The mathematical graphs are constructed from the article's core table, using
independent_controls.py and rank_gauge_controls.py, both written before reading
published mathematical reviewer reports. Published code is used only to check
the raw row's source/target numbering against its primitive generator.
"""
import json,gzip,hashlib,sys,itertools as it
from pathlib import Path
from datetime import datetime,timezone
import sympy as S
import networkx as nx
from rank_gauge_controls import build,mixed
from independent_controls import rootings,fourier
O=Path(__file__).parent;P=O/'cache/replay';F=S.Rational
checks=[]
def ck(name,value,detail=None):
    checks.append({'name':name,'pass':bool(value),'detail':detail})
    if not value:raise AssertionError((name,detail))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
es,leaves=build('theta1',(2,3));et,_=build('theta0',(2,3))
perm=[2,0,1,3];relabel={f'L{i}':f'L{j}' for i,j in enumerate(perm)}
etp=[(relabel.get(u,u),relabel.get(v,v)) for u,v in et]
GS,GT=mixed(es,leaves),mixed(etp,leaves)
# Target-to-source explicit map; all labels already aligned to raw-row order.
m={'S':'P3','U':'U','V':'V','X':'X','P2':'S','P3':'P2',**{x:x for x in leaves}}
ck('bijection',set(m)==set(GT) and set(m.values())==set(GS))
mapped=[]
for u,v,d in GT.edges(data=True):
    a,b=m[u],m[v];ck('edge '+str((u,v)),GS.has_edge(a,b))
    head=m[d['head']] if d['head'] else ''
    ck('retained head '+str((u,v)),GS.edges[a,b]['head']==head)
    mapped.append({'target_edge':[u,v],'target_head':d['head'],'source_edge':[a,b],'source_head':head})
ck('label preservation',all(m[x]==x for x in leaves))
for name,edges in [('source',es),('target',etp)]:
    graph,rs=rootings(edges,leaves)
    ck(name+' all admissible rootings tree-child',len(rs)>0 and all(r['tree_child'] for r in rs),{'admissible_rootings':len(rs)})
    ck(name+' simple graph',len(graph)==len({tuple(sorted((u,v))) for u,v,_ in graph}) and all(u!=v for u,v,_ in graph))
    ck(name+' local no-omnian criterion',all(sum(1 for a,b,h in graph if not h and t in (a,b))==2 for u,v,h in graph if h for t in ([v if h==u else u])))
# Strict-CT common physical tensor: assign distinct rational pairs to every
# mixed edge; split the root edge with (7/8,7/8) and an interior residual.
sectors={frozenset(e): (F(10+i,70+2*i),F(13+i,65+3*i)) for i,e in enumerate(sorted(tuple(sorted(e)) for e in GS.edges()))}
ck('every common mixed edge strict CT',all(0<s<1 and s*s<g<1 for s,g in sectors.values()))
cw={'V':{'U':F(2,5),'P3':F(3,5)},'X':{'S':F(3,7),'P2':F(4,7)}}
def rooted_params(edges,mapto):
    rc=[v for u,v in edges if u=='r'];pair=sectors[frozenset(mapto[v] for v in rc)]
    par={}
    for u,v in edges:
        if u=='r':par[(u,v)]=(F(7,8),F(7,8)) if v==rc[0] else tuple(x/F(7,8) for x in pair)
        else:par[(u,v)]=sectors[frozenset([mapto[u],mapto[v]])]
    weights={v:{u:cw[mapto[v]][mapto[u]] for u,w in edges if w==v} for v in ['V','X']}
    return par,weights
ps,ws=rooted_params(es,{v:v for v in GS});pt,wt=rooted_params(etp,m)
ck('all rooted edges strict CT',all(0<s<1 and s*s<g<1 for s,g in list(ps.values())+list(pt.values())))
qs=[h for h in it.product(range(4),repeat=4) if h[0]^h[1]^h[2]^h[3]==0]
vs=[fourier(es,leaves,ps,ws,h) for h in qs];vt=[fourier(etp,leaves,pt,wt,h) for h in qs]
ck('64 exact full Fourier coordinates coincide',vs==vt)
# Bind the independently written diagrams to the publication's numbering.
sys.path.insert(0,str(P/'package/referee/k2p_offline_sweep_portable/atlas'))
import k2p_atlas_core as a
src=a.source_supports()[2];tar=(a.target_completions(4,True)+a.target_completions(4,False))[85]
def decode_graph(rec):
    G=rec.graph
    names={}
    for n,d in G.nodes(data=True):
        if d['role']=='root': names[n]='r'
        elif d['role']=='leaf': names[n]='L'+str(d['label'])
        elif n[0]=='core':names[n]=n[1]
        elif n[0]=='sub':names[n]='P'+str(n[1])
        else:raise AssertionError(n)
    return {(names[u],names[v]) for u,v in G.edges()}
ck('printed source binds published source2',decode_graph(src)==set(es))
ck('printed target binds published target85',decode_graph(tar)==set(et))
ledger=P/'work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_ledger.jsonl.gz'
with gzip.open(ledger,'rt') as f:
    rows=[json.loads(line) for line in f if '"raw_id":137124,' in line]
ck('exactly one raw row',len(rows)==1)
r=rows[0]
ck('row identity',r['source_index']==2 and r['target_index']==85 and r['port_permutation']==perm)
ck('published row claims false exclusion',r['corrected_category']=='exact_rank_exclusion' and r['evidence_binding']['source_exact_rank']==14 and r['evidence_binding']['target_exact_rank']==13)
result={'utc':datetime.now(timezone.utc).isoformat(),'status':'COUNTEREXAMPLE_CONFIRMED','scope':'False certificate, not a counterexample to the classification theorem itself','checks':checks,'mapping_target_to_source':m,'edge_transport':mapped,'source_rooted_edges':es,'target_rooted_edges_relabelled':etp,'published_row':r,'source_hashes':{'ledger_sha256':sha(ledger),'atlas_sha256':sha(P/'package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py')},'common_tensor_exact':{'character_order':qs,'coordinates':[str(x) for x in vs]},'full_rank_controls':'rank-gauge-controls.json','proof':'Labelled head-preserving isomorphism, admissible rerooting, and strict serial subdivision give local analytic physical parameter transport. The quotient relation therefore exists; raw arm-fixed ranks cannot exclude it.'}
O.joinpath('rank-exclusion-counterexample.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'checks':len(checks),'all_pass':all(c['pass'] for c in checks),'ledger_sha256':sha(ledger)},indent=2))
