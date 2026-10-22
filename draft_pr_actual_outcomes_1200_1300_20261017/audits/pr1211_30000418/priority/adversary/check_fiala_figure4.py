"""Independent transcription check for Fiala--Skrekovski KAM2001-530 Fig.4.
This is a priority audit, not an enumeration/minimality claim about the submitted tree.
"""
from itertools import combinations
import json
from pathlib import Path
V = ['x','t0','t1','t2','t3','b0','b1','b2','b3','y']
E = [('t0','t1'),('t1','t2'),('t2','t3'),('b0','b1'),('b1','b2'),('b2','b3'),('t0','b0'),('t3','b3'),('x','t0'),('x','b0'),('y','t3'),('y','b3')]
A = set(range(1,6)); C = {1,2,4,5,6}
L = {v:C if v=='x' else A for v in V}
def solve(vertices,edges,lists):
    adj={v:set() for v in vertices}
    for u,v in edges: adj[u].add(v);adj[v].add(u)
    d2={v:set().union(*(adj[u] for u in adj[v]))-{v}-adj[v] for v in vertices}
    assigned={}
    def rec():
        if len(assigned)==len(vertices): return dict(assigned)
        poss={v:[a for a in sorted(lists[v]) if all(abs(a-assigned[w])>=2 for w in adj[v] if w in assigned) and all(a!=assigned[w] for w in d2[v] if w in assigned)] for v in vertices if v not in assigned}
        v=min(poss,key=lambda z:(len(poss[z]),-len(adj[z]),z))
        for a in poss[v]:
            assigned[v]=a
            ret=rec()
            if ret is not None: return ret
            del assigned[v]
        return None
    return rec()
def connected(vertices,edges):
    seen={vertices[0]}
    while True:
        old=len(seen)
        for u,v in edges:
            if u in seen:seen.add(v)
            if v in seen:seen.add(u)
        if len(seen)==old:return len(seen)==len(vertices)
ordinary={'x':3,'t0':1,'t1':4,'t2':2,'t3':5,'b0':5,'b1':2,'b2':4,'b3':1,'y':3}
def valid(vertices,edges,lists,f):
    if any(f[v] not in lists[v] for v in vertices):return False
    if any(abs(f[u]-f[v])<2 for u,v in edges):return False
    adj={v:set() for v in vertices}
    for u,v in edges:adj[u].add(v);adj[v].add(u)
    return all(len({f[w] for w in adj[v]})==len(adj[v]) for v in vertices)
if not valid(V,E,{v:A for v in V},ordinary):raise RuntimeError('Fig4 witness invalid')
full_bad=solve(V,E,L)
if full_bad is not None:raise RuntimeError('Fig4 alleged bad list is feasible')
spanning=[]
for ix in combinations(range(len(E)),len(V)-1):
    edges=[E[i] for i in ix]
    if connected(V,edges):
        f=solve(V,edges,L)
        if f is None:raise RuntimeError('Found an inherited tree obstruction')
        if not valid(V,edges,L,f):raise RuntimeError('invalid tree witness')
        spanning.append({'edge_indices':list(ix),'labeling':f})
summary={'source':'https://kam.mff.cuni.cz/kamserie/clanky/2001/s530.pdf','figure':4,'pdf_page':14,'vertices':V,'edges':E,'lists':{v:sorted(L[v]) for v in V},'ordinary_witness':ordinary,'full_figure_bad_assignment_infeasible':full_bad is None,'connected_spanning_trees':len(spanning),'all_inherited_tree_assignments_feasible':True,'spanning_tree_witnesses':spanning}
Path(__file__).with_suffix('.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ['spanning_tree_witnesses','lists','vertices','edges','ordinary_witness']},indent=2))
