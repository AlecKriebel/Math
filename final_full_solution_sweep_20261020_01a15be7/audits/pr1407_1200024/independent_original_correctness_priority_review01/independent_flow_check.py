"""New read-only exact reconstruction; certificate is inert JSON, author code unused."""
from pathlib import Path
from collections import deque
from fractions import Fraction as Q
import gzip,json,hashlib

def need(p,msg):
    if not p:raise RuntimeError(msg)
def words(R):
    out=[()];todo=deque([()])
    while todo:
        s=todo.popleft()
        if len(s)<R:
            for a in range(3 if not s else 2):
                t=s+(a,);out.append(t);todo.append(t)
    return out
def parent(s):
    return s+(0,) if all(a==0 for a in s) else s[:-1]
def tree_neighbors(s):
    # The root-coordinate tree has3 forward choices at root and2 thereafter.
    return ([s[:-1]] if s else [])+[s+(a,) for a in range(3 if not s else 2)]
def grand_neighbors(s):
    p=parent(s);p2=parent(p)
    children=[z for z in tree_neighbors(s) if z!=p]
    grandchildren=[z for c in children for z in tree_neighbors(c) if z!=s]
    return set([p,p2]+children+grandchildren)
def graph(R):
    W=words(R);ix={s:i for i,s in enumerate(W)};adj=[set() for s in W]
    # Construct by the complete infinite neighbor relation, then restrict endpoints.
    for i,s in enumerate(W):
        for t in grand_neighbors(s):
            if t in ix:adj[i].add(ix[t])
    need(all(i in adj[j] for i,a in enumerate(adj) for j in a),'undirected G restriction')
    sq=[(set(a)|set().union(*(adj[j] for j in a)))-{i} for i,a in enumerate(adj)]
    edges=sorted((i,j) for i,a in enumerate(sq) for j in a if i<j)
    return W,ix,adj,sq,edges

def flow_check(values,edges,n,source,D):
    need(len(values)==len(edges),'flow length')
    div=[0]*n;energy=0
    for (i,j),v in zip(edges,values):
        need(type(v) is int,'integer numerator')
        div[i]+=v;div[j]-=v;energy+=v*v
    target=[0]*n;target[source]=D;target[0]=-D
    need(div==target,'all vertex divergences')
    return energy

def main():
    here=Path(__file__).resolve().parent;f=here/'PRIVATE_INPUT/unsolved_math_prioritization/attempts/1200024_graph_square_20261021/square_flow_certificate.json.gz';raw=f.read_bytes();c=json.loads(gzip.decompress(raw))
    need(hashlib.sha256(raw).hexdigest()=='6573c55f2998f4576a050a0757ca74f1cae9cadfa96ec61c69b181c530f79c4f','certificate input pin')
    W,ix,adj,sq,edges=graph(10)
    need(len(W)==3070 and len(edges)==19931,'finite graph counts')
    need(c['q']==2 and c['radius']==10 and c['vertices']==len(W),'certificate graph parameters')
    need(c['edge_order']==[list(e) for e in edges],'every edge and its order')
    # Infinite G^2 root neighbors are generated without a ball boundary.
    N=grand_neighbors(());infinite=(N|set().union(*(grand_neighbors(t) for t in N)))-{()}
    need(len(N)==8 and len(infinite)==40,'actual G and G-square root degrees')
    need({W[i] for i in sq[0]}==infinite,'complete infinite root neighborhood')
    need(max(map(len,infinite))==4,'root square tree-distance guard')
    need(sorted(sq[0])==c['root_neighbors'] and len(c['flows'])==40,'all40 targets')
    D=c['denominator'];need(type(D) is int and D==10**9,'denominator')
    energies=[]
    for v,flow in zip(c['root_neighbors'],c['flows']):energies.append(flow_check(flow,edges,len(W),v,D))
    need(energies==c['energy_numerators'],'every supplied energy numerator')
    total=sum(energies);need(total==c['total_energy_numerator'] and D*D==c['total_energy_denominator'],'total exact energy')
    need(total==3208526010913748780 and Q(total,D*D)<Q(321,100),'strict upper bound')
    need(Q(73,50)**2>2 and (Q(24)-Q(73,50))/7==Q(161,50),'radical-free strict lower bound')
    need((Q(161,50)-Q(321,100))/2==Q(1,200),'strict bF-gap transfer')
    # Root-local triangle counts also reconstruct the oriented tree inside G.
    W4,ix4,a4,s4,e4=graph(4);tri={len(a4[0]&a4[j]) for j in a4[0]};need(tri=={1,3},'edge triangle types')
    for j in a4[0]:need(len(a4[0]&a4[j])==(3 if W4[j] in set(tree_neighbors(())) else 1),'tree-vs-grandparent triangles')
    Ts=set(tree_neighbors(()));induced={z:len((grand_neighbors(z)&Ts)) for z in Ts};need(induced[(0,)]==2 and sorted(induced.values())==[1,1,2],'parent uniquely recovered')
    # Mathematical corruptions affect feasibility, incidence or energy and must fail.
    mutants=0
    bad=c['flows'][0].copy();bad[0]+=1
    try:flow_check(bad,edges,len(W),c['root_neighbors'][0],D)
    except RuntimeError:mutants+=1
    else:raise RuntimeError('changed flow escaped')
    try:flow_check(c['flows'][0],edges,len(W),c['root_neighbors'][1],D)
    except RuntimeError:mutants+=1
    else:raise RuntimeError('wrong target escaped')
    need(c['edge_order'][:-1]!=[list(e) for e in edges],'missing-edge mutant');mutants+=1
    need(total+1!=c['total_energy_numerator'],'energy mutation');mutants+=1
    return dict(status='PASS',author_programs_executed=False,certificate_sha256=hashlib.sha256(raw).hexdigest(),vertices=len(W),edges=len(edges),full_root_degree_G=len(N),full_root_degree_Gsquare=len(infinite),flow_count=len(energies),divergence_equations=len(W)*len(energies),denominator=D,energy_numerators=energies,total_energy_numerator=total,total_energy_denominator=D*D,strict_upper='321/100',strict_lower_original='161/50',strict_bF_gap='1/200',mathematical_mutants_rejected=mutants,triangle_types=sorted(tri),infinite_scope='Finite exact flows become infinite FREE-resistance upper bounds only by the separate written Thomson/Rayleigh/exhaustion proof.')
if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))
