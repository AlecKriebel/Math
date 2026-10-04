#!/usr/bin/env python3
"""Independent standard-library audit. Does not import or execute packet code.
Usage: python independent_verify.py /path/to/extracted/packet
Cycles: layered Hamilton-path counting, then explicit all-pairs mask testing.
Minors: quotient-edge construction and independent union-find connectivity.
"""
import sys, json, hashlib
from pathlib import Path
from itertools import combinations, product
from collections import defaultdict, Counter
P=Path(sys.argv[1])

def require(b, text):
    if not b: raise ValueError(text)

def edges_product(m,n):
    coords=[(i,j) for i in range(m) for j in range(n)]
    return { (u,v) for u,v in combinations(range(m*n),2)
        if ((coords[u][0]==coords[v][0] and (coords[u][1]-coords[v][1])%n in (1,n-1))
        or (coords[u][1]==coords[v][1] and (coords[u][0]-coords[v][0])%m in (1,m-1))) }

def adjacency(N,edges):
    a=[set() for _ in range(N)]
    for u,v in edges: a[u].add(v);a[v].add(u)
    return a

def cycles_dp(N,es):
    a=adjacency(N,es); oriented=Counter()
    for root in range(N):
        paths={(1<<root,root):1}
        for length in range(1,N-2):
            following=defaultdict(int)
            for (mask,last),multiplicity in paths.items():
                if length>=3 and root in a[last]: oriented[mask]+=multiplicity
                if length<N-3:
                    for v in a[last]:
                        if v>root and not mask&(1<<v): following[mask|(1<<v),v]+=multiplicity
            paths=following
    require(all(x%2==0 for x in oriented.values()),'oriented count parity')
    return {m:x//2 for m,x in oriented.items()}

def facet_member(mask,m,n):
    rows={i//n for i in range(m*n) if mask&(1<<i)}
    cols={i%n for i in range(m*n) if mask&(1<<i)}
    return any(rows<={r,(r+1)%m} for r in range(m)) or any(cols<={c,(c+1)%n} for c in range(n))

def cycle_audit(m,n):
    cs=cycles_dp(m*n,edges_product(m,n));nf={x for x in cs if not facet_member(x,m,n)}
    counts=Counter()
    for mask,num in cs.items():counts[mask.bit_count()]+=num
    bad=[];disjoint_mask_pairs=0;disjoint_cycle_pairs=0
    for a,b in combinations(sorted(cs),2):
        if not a&b:
            disjoint_mask_pairs+=1;disjoint_cycle_pairs+=cs[a]*cs[b]
            if a in nf and b in nf:bad.append([a,b])
    return {'cycle_counts':dict(sorted(counts.items())), 'total_cycles':sum(cs.values()),
      'distinct_cycle_vertex_masks':len(cs),'nonfacial_cycle_vertex_masks':len(nf),
      'disjoint_mask_pairs':disjoint_mask_pairs,'disjoint_cycle_pairs':disjoint_cycle_pairs,
      'uncovered_disjoint_mask_pairs':len(bad),'first_uncovered_masks':bad[:1],
      'all_disjoint_pairs_facially_covered':not bad}

def edge_set(es):return {tuple(sorted(e)) for e in es}

def family_audit(fam):
    results=[]
    for f in fam:
        E=set(combinations(range(6),2));V=set(range(6))
        for op in f['derivation']:
            if op['op']=='delta_y':
                t=op['triangle'];require(len(set(t))==3 and set(t)<=V,'invalid triangle')
                old=edge_set(combinations(t,2));require(old<=E,'missing triangle edge')
                z=max(V)+1;V.add(z);E=(E-old)|edge_set((z,v) for v in t)
            elif op['op']=='y_delta':
                v=op['vertex'];ns={y if x==v else x for x,y in E if v in (x,y)}
                require(len(ns)==3,'invalid Y');V.remove(v)
                E={e for e in E if v not in e}|edge_set(combinations(ns,2))
            else:raise ValueError('unknown transformation')
            relabel={v:i for i,v in enumerate(sorted(V))}
            E=edge_set((relabel[a],relabel[b]) for a,b in E);V=set(range(len(V)))
        require(len(V)==f['n'] and E==edge_set(f['edges']),'family mismatch')
        results.append({'n':len(V),'edges':len(E),'moves':len(f['derivation']),
          'delta_y_only':all(op['op']=='delta_y' for op in f['derivation'])})
    return results

def minor_audit(N,E,rec,fam):
    bs=rec['branch_sets'];f=fam[rec['family_index']]
    require(len(bs)==f['n'],'branch number');require(edge_set(rec['target_edges'])==edge_set(f['edges']),'target mismatch')
    owner={};trees=[]
    for i,b in enumerate(bs):
        require(len(b)>0 and len(b)==len(set(b)),'empty or repeated branch vertex')
        for v in b:
            require(type(v)==int and 0<=v<N and v not in owner,'overlap or invalid vertex');owner[v]=i
        component={v:v for v in b};tree=[]
        def find(x):
            while component[x]!=x:x=component[x]
            return x
        for u,v in sorted(E):
            if u in component and v in component and find(u)!=find(v):
                component[find(u)]=find(v);tree.append([u,v])
        require(len({find(v) for v in b})==1,'disconnected branch');trees.append(tree)
    quotient={};
    for u,v in sorted(E):
        if u in owner and v in owner and owner[u]!=owner[v]:
            quotient.setdefault(tuple(sorted((owner[u],owner[v]))),[u,v])
    target=edge_set(f['edges']);require(target<=set(quotient),'missing target adjacency')
    return {'valid':True,'source_vertices':N,'source_edges':len(E),'target_vertices':len(bs),
      'target_edges':len(target),'used_source_vertices':len(owner),'spanning_tree_edges':trees,
      'edge_witnesses':[{'target':list(e),'source':quotient[e]} for e in sorted(target)]}

def truncated_graph_from_inequalities():
    # A vertex of sum x_i=3, 0<=x_i<=2 has four coordinates at bounds.
    vertices=set()
    for free in range(5):
        for bounds in product((0,2),repeat=4):
            x=[];it=iter(bounds)
            for i in range(5):x.append(3-sum(bounds) if i==free else next(it))
            if all(0<=v<=2 for v in x):vertices.add(tuple(x))
    labels=[(i,j) for i in range(5) for j in range(5) if i!=j]
    ordered=[tuple(2*(k==i)+(k==j) for k in range(5)) for i,j in labels]
    require(vertices==set(ordered) and len(vertices)==20,'vertex enumeration mismatch')
    E=set()
    for a,b in combinations(range(20),2):
        common=[(k,ordered[a][k]) for k in range(5) if ordered[a][k]==ordered[b][k] and ordered[a][k] in (0,2)]
        face=[x for x in vertices if all(x[k]==v for k,v in common)]
        if len(face)==2:E.add((a,b))
    expected={(a,b) for a,b in combinations(range(20),2) if labels[a][0]==labels[b][0] or labels[a]==labels[b][::-1]}
    require(E==expected,'truncated-simplex adjacency mismatch')
    return E

def isomorphism(E,F,N):
    A=adjacency(N,E);B=adjacency(N,F);assign={};used=set()
    def visit():
        if len(assign)==N:return dict(assign)
        left=max((i for i in range(N) if i not in assign),key=lambda i:(len(A[i]&assign.keys()),len(A[i])))
        for right in range(N):
            if right not in used and len(A[left])==len(B[right]) and all((v in A[left])==(w in B[right]) for v,w in assign.items()):
                assign[left]=right;used.add(right);ans=visit()
                if ans is not None:return ans
                used.remove(right);del assign[left]
        return None
    return visit()

def rejects(fn):
    try:fn()
    except ValueError:return True
    return False

def main():
    fam=json.loads((P/'petersen_family_certificates.json').read_text());cert=json.loads((P/'minor_certificates.json').read_text())
    result={'family_derivations':family_audit(fam),'facial_covers':{},'minor_models':{},'negative_controls':{}}
    author=json.loads((P/'verification_results.json').read_text())
    for m,n in [(3,3),(3,4),(3,5),(4,4)]:
        q=cycle_audit(m,n);key=f'C{m}xC{n}';result['facial_covers'][key]=q
        expected=author['facial_covers'][key] if m==3 else author['negative_controls']['Q4_facial_test_rejects']
        for k in ['cycle_counts','distinct_cycle_vertex_masks','nonfacial_cycle_vertex_masks','all_disjoint_pairs_facially_covered']:
            require(json.loads(json.dumps(q[k]))==expected[k],f'{key} {k} differs')
    trunc=truncated_graph_from_inequalities()
    graphs={'Q4':(16,edges_product(4,4)),'triangle_hexagon':(18,edges_product(3,6)),'truncated_simplex':(20,trunc)}
    for name,(N,E) in graphs.items():
        require(all(x['op']=='delta_y' for x in fam[cert[name]['family_index']]['derivation']),'used family needs non-DeltaY move')
        result['minor_models'][name]=minor_audit(N,E,cert[name],fam)
    standard_petersen=edge_set([(i,(i+1)%5) for i in range(5)]+[(i,i+5) for i in range(5)]+[(i+5,(i+2)%5+5) for i in range(5)])
    iso=isomorphism(edge_set(fam[6]['edges']),standard_petersen,10);require(iso is not None,'target not Petersen')
    result['petersen_isomorphism']=iso
    from copy import deepcopy
    for damage in ['empty','overlap','out_of_range','disconnect','missing_adjacency']:
        rec=deepcopy(cert['Q4']);N,E=graphs['Q4'];E=set(E)
        if damage=='empty':rec['branch_sets'][0]=[]
        if damage=='overlap':rec['branch_sets'][0].append(rec['branch_sets'][1][0])
        if damage=='out_of_range':rec['branch_sets'][0].append(N)
        if damage=='disconnect':
            b=set(rec['branch_sets'][0]);E={e for e in E if not set(e)<=b}
        if damage=='missing_adjacency':
            a,b=rec['target_edges'][0];A=set(rec['branch_sets'][a]);B=set(rec['branch_sets'][b])
            E={e for e in E if not (e[0] in A and e[1] in B or e[1] in A and e[0] in B)}
        result['negative_controls'][damage]=rejects(lambda:minor_audit(N,E,rec,fam));require(result['negative_controls'][damage],damage+' accepted')
    broken=deepcopy(fam);broken[6]['edges'].pop()
    result['negative_controls']['family_damage']=rejects(lambda:family_audit(broken));require(result['negative_controls']['family_damage'],'family damage accepted')
    result['six_vertex_cases']={str(p):sum(1 for a,b in combinations(range(6),2) if 0<sum(i<p for i in range(6) if i not in (a,b))<4) for p in (2,3,4)}
    require(list(result['six_vertex_cases'].values())==[14,15,14],'six-vertex count')
    result['truncation_geometry']={'vertices':20,'edges':len(trunc),'degree_distribution':dict(Counter(len(a) for a in adjacency(20,trunc)))}
    result['status']='PASS: independently reproduced stated finite exclusions; full problem remains unresolved in the packet.'
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
