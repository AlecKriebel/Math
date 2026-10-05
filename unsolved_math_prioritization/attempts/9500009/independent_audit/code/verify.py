#!/usr/bin/env python3
"""Independent finite audit. No network and no writes unless --write is passed."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations
from math import comb, factorial, prod
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]

def require(condition, message):
    if not condition:
        raise ValueError(message)

def read(path):
    return json.loads((ROOT/path).read_text())

def graph(n):
    return [tuple(w for w in range(n*n)
                  if abs(v//n-w//n)+abs(v%n-w%n)==1) for v in range(n*n)]

def peak_set(labels, adj, vertices=None):
    vertices=set(range(len(labels))) if vertices is None else set(vertices)
    return tuple(v for v in sorted(vertices)
                 if all(labels[v]>labels[w] for w in adj[v] if w in vertices))

def direct_enumeration(adj):
    result=Counter()
    for labels in permutations(range(1,len(adj)+1)):
        result[peak_set(labels,adj)]+=1
    return result

def orientation_enumeration(adj):
    """Partition labelings by lower-to-higher edge orientations, then count
    topological orders. Cyclic orientations have zero topological orders."""
    N=len(adj); edges=[(u,v) for u in range(N) for v in adj[u] if u<v]
    result=Counter(); acyclic=0
    for mask in range(1<<len(edges)):
        pred=[0]*N; out=[0]*N
        for i,(u,v) in enumerate(edges):
            if mask>>i&1: u,v=v,u
            pred[v]|=1<<u; out[u]|=1<<v
        f=[0]*(1<<N);f[0]=1
        for S in range(1<<N):
            if not f[S]:continue
            for v in range(N):
                if not S>>v&1 and pred[v]&~S==0:f[S|1<<v]+=f[S]
        if f[-1]:
            acyclic+=1
            result[tuple(v for v in range(N) if not out[v])]+=f[-1]
    return result,acyclic

def check_forest(c,weights):
    n=c['n'];N=n*n;adj=graph(n);roots=set(c['roots']);parent=c['parent']
    require(len(roots)==2 and len(parent)==N,'forest dimensions')
    require(not any(b in adj[a] for a in roots for b in roots),'root adjacency')
    sizes=[0]*N
    for v in range(N):
        seen=set();w=v
        while True:
            require(w not in seen,'forest cycle');seen.add(w);sizes[w]+=1
            if parent[w]==-1:
                require(w in roots,'wrong forest root');break
            require(w not in roots and parent[w] in adj[w],'bad forest parent')
            w=parent[w]
    require(sizes==c['subtree_sizes'],'subtree sizes')
    labels=c['certified_two_peak_labels']
    require(sorted(labels)==list(range(1,N+1)),'certificate not bijection')
    require(set(peak_set(labels,adj))==roots,'certificate peaks')
    require(set(labels[v] for v in roots)=={N,N-1},'top two root labels')
    for v in range(N):
        if v not in roots: require(labels[parent[v]]>labels[v],'parent order')
    nonroots=[v for v in range(N) if v not in roots];index={v:i for i,v in enumerate(nonroots)}
    prereq=[0 if parent[v] in roots else 1<<index[parent[v]] for v in nonroots]
    f=[0]*(1<<len(nonroots));f[0]=1
    for S in range(len(f)):
        if not f[S]:continue
        for v,p in enumerate(prereq):
            if not S>>v&1 and p&~S==0:f[S|1<<v]+=f[S]
    denom=prod(sizes[v] for v in nonroots)
    require(factorial(N-2)%denom==0,'nonintegral hook count')
    lower=2*factorial(N-2)//denom
    require(lower==2*f[-1]==c['top_two_root_labeling_lower_bound'],'hook/poset mismatch')
    require(lower<=weights[tuple(sorted(roots))],'lower bound exceeded exact count')

def check_general_admissibility():
    graph_counts=[];rootsets=0
    for N in range(1,6):
        edges=list(combinations(range(N),2));count=0
        for mask in range(1<<len(edges)):
            adj=[[] for _ in range(N)]
            for i,(u,v) in enumerate(edges):
                if mask>>i&1:adj[u].append(v);adj[v].append(u)
            visited={0};todo=[0]
            while todo:
                for w in adj[todo.pop()]:
                    if w not in visited:visited.add(w);todo.append(w)
            if len(visited)!=N:continue
            count+=1;seen=direct_enumeration(adj)
            independent={tuple(v for v in range(N) if S>>v&1) for S in range(1,1<<N)
                         if all(not(S>>u&1 and S>>v&1) for u,v in edges if v in adj[u])}
            require(set(seen)==independent,'general admissibility mismatch')
            rootsets+=len(independent)
        graph_counts.append(count)
    return dict(connected_labeled_graph_counts=graph_counts,
                vertex_sizes=list(range(1,6)),independent_root_sets_checked=rootsets)

def main(write=False,negative=False):
    expected=read('reference/exact_counts.json')
    if negative:expected['squares'][0]['pair_counts'][0][2]+=1
    with tempfile.TemporaryDirectory() as tmp:
        exe=str(Path(tmp)/'count')
        subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Werror','-pedantic',
                        str(ROOT/'code/ascending_count.cpp'),'-o',exe],check=True)
        actual=json.loads(subprocess.check_output([exe],text=True))
    pair_weights={};summaries=[];brutes={};orientation_results=[]
    for got,want in zip(actual['squares'],expected['squares']):
        for k in ['n','pair_counts','single_peak_counts','peak_histogram']:
            require(got[k]==want[k],f"n={got['n']} mismatch in {k}")
        n=got['n'];N=n*n;adj=graph(n)
        pairs={(a,b):c for a,b,c in got['pair_counts']};pair_weights[n]=pairs
        require(len(pairs)==comb(N,2),'pair coverage')
        dist=[0]*(2*n-1)
        for (a,b),c in pairs.items():
            d=abs(a//n-b//n)+abs(a%n-b%n);dist[d]+=c
            require((c>0)==(b not in adj[a]),'admissibility support')
        h=got['peak_histogram'];z=sum(pairs.values())
        require(sum(h)==factorial(N) and h[2]==z,'total histogram')
        require(dist==want['two_peak_distance_counts'],'distance distribution')
        mean=Fraction(sum(d*c for d,c in enumerate(dist)),n*z)
        mean_peaks=sum(Fraction(k*c,factorial(N)) for k,c in enumerate(h))
        require(mean_peaks==Fraction(4,3)+(n-2)+Fraction((n-2)**2,5),'expected peaks')
        summaries.append(dict(n=n,two_peak_total=z,distance_counts=dist,
            mean_distance_over_n=str(mean),mean_raw_distance=str(n*mean),
            tail_distance_at_least_n=str(Fraction(sum(dist[n:]),z)),
            unconditioned_two_peak_probability=str(Fraction(z,factorial(N))),
            expected_total_peaks=str(mean_peaks),positive_pair_count=sum(c>0 for c in pairs.values())))
        if n<=3:
            brute=direct_enumeration(adj);brutes[n]=brute
            bh=[0]*(N+1)
            for peaks,c in brute.items():bh[len(peaks)]+=c
            require(bh==h,'brute histogram')
            require(all(brute[(a,b)]==c for (a,b),c in pairs.items()),'brute pairs')
            require([brute[(v,)] for v in range(N)]==got['single_peak_counts'],'brute singles')
            orient,acyclic=orientation_enumeration(adj)
            require(orient==brute,'orientation partition')
            orientation_results.append(dict(n=n,edge_orientations=1<<(sum(map(len,adj))//2),
                                            acyclic_orientations=acyclic,all_peak_sets_agree=True))
    forests=read('reference/forest_certificates.json')
    require(len(forests)==122,'forest count')
    certificate_keys={(c['n'],*c['roots']) for c in forests}
    required_keys={(n,a,b) for n,pairs in pair_weights.items() for (a,b),c in pairs.items() if c}
    require(certificate_keys==required_keys and len(certificate_keys)==len(forests),'forest coverage')
    for c in forests:check_forest(c,pair_weights[c['n']])
    b=brutes[3];z=sum(c for peaks,c in b.items() if len(peaks)==2)
    ma=sum(c for peaks,c in b.items() if len(peaks)==2 and 0 in peaks)
    mb=sum(c for peaks,c in b.items() if len(peaks)==2 and 8 in peaks)
    joint=Fraction(b[(0,8)],z);mp=Fraction(ma*mb,z*z)
    require(joint-mp==Fraction(-7485,2244004),'conditional covariance')
    adj=graph(3)
    require(not(set(adj[0])|{0})&(set(adj[8])|{8}),'disjoint neighborhoods')
    # Directly complete all 7! orders after the fixed descending prefix.
    completions=Counter()
    for suffix in permutations(range(2,9)):
        order=(0,1)+suffix;labels=[0]*9
        for i,v in enumerate(order):labels[v]=9-i
        if peak_set(labels,adj)==(0,):completions[suffix[0]]+=1
    require(completions=={2:156,3:180,4:336},'boundary growth')
    v=read('reference/verification.json');block=v['block_restriction_counterexample'];labels=block['labels_row_major']
    full=peak_set(labels,graph(4));restricted=peak_set(labels,graph(4),[4*i+j for i in range(3) for j in range(3)])
    require(full==(7,8) and restricted==(2,8,10),'restriction counterexample')
    for n in range(2,51):
        centers=[(i,j) for i in range(1,n-1,3) for j in range(1,n-1,3)]
        m=len(centers);require(m==(n//3)**2,'packed centers count')
        neighborhoods=[{(i,j),(i-1,j),(i+1,j),(i,j-1),(i,j+1)} for i,j in centers]
        require(len(set().union(*neighborhoods))==5*m,'neighborhood packing')
        bound=Fraction(4,5)**m*(1+Fraction(m,4)+Fraction(m*(m-1),32))
        direct=sum(Fraction(comb(m,j)*4**(m-j),5**m) for j in range(min(m,2)+1))
        require(bound==direct,'binomial tail algebra')
    out=dict(status='PASS',asymptotic_status='UNRESOLVED',new_solution_claim=False,
        pair_counts_checked=162,singleton_counts_checked=29,forest_certificates_checked=122,
        forest_hook_counts_independently_matched_poset_counts=True,
        summaries=summaries,brute_force_sizes=[2,3],orientation_crosschecks=orientation_results,
        general_graph_admissibility=check_general_admissibility(),
        conditioned_independence=dict(joint=str(joint),marginal_product=str(mp),covariance=str(joint-mp)),
        boundary_completions={str(k):c for k,c in sorted(completions.items())},
        restriction_peaks=dict(full=list(full),restricted=list(restricted)),
        rare_bound_packing_algebra_sizes=list(range(2,51)),
        arithmetic='exact integers and rational fractions; finite tests do not prove asymptotics')
    if write:
        (ROOT/'results/ascending_counts.json').write_text(json.dumps(actual,indent=2)+'\n')
        (ROOT/'results/independent_verification.json').write_text(json.dumps(out,indent=2)+'\n')
    else:
        require(actual==read('results/ascending_counts.json'),'saved independent counts')
        require(out==read('results/independent_verification.json'),'saved verification report')
        if (ROOT/'MANIFEST.json').exists():
            for entry in read('MANIFEST.json')['files']:
                data=(ROOT/entry['path']).read_bytes()
                require(len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256'],
                        'manifest mismatch: '+entry['path'])
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true')
    parser.add_argument('--negative-control',action='store_true')
    args=parser.parse_args();main(args.write,args.negative_control)
