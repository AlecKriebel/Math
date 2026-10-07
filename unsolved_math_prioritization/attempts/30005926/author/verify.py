#!/usr/bin/env python3
"""Finite controls for the scoped report; no random-map limit is certified here."""
import argparse
from collections import Counter, deque
from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import combinations, product
import json
from math import factorial
from pathlib import Path

COUNTS = Counter()
def check(condition, category):
    if not condition:
        raise RuntimeError('Failed control: ' + category)
    COUNTS[category] += 1

def distances(adj):
    ans = {}
    for start in adj:
        d = {start: 0}; todo = deque([start])
        while todo:
            u = todo.popleft()
            for v in adj[u]:
                if v not in d:
                    d[v] = d[u]+1; todo.append(v)
        if len(d) != len(adj):
            return None
        ans[start] = d
    return ans

def adj_from_edges(vertices, edges):
    adj = {v:set() for v in vertices}
    for x,y in edges:
        adj[x].add(y); adj[y].add(x)
    return adj

def parameter_checks():
    for b in range(2,41):
        for a in range(1,b):
            m = F(a,b); h = m/(1+m)**2; s = (1-m)/(1+m)
            check(s*s == 1-4*h, 'rational_parameter_identity')
            check((1-2*h-s)/(2*h) == m, 'rational_parameter_identity')
            q = m*m+10*m+1
            check(h*h/(1+8*h)**3 == m*m*(1+m)**2/q**3, 'rational_parameter_identity')
            check((1+m)**2 < q**3, 'lambda_less_than_m')
            check(6*h/((1+8*h)*s) == 6*m*(1+m)/((1-m)*q), 'rational_parameter_identity')
    N=9
    def divide(a,b):
        c=[F(0)]*N
        for i in range(N):
            c[i]=(a[i]-sum(b[j]*c[i-j] for j in range(1,i+1)))/b[0]
        return c
    cosh=[F(1,2**i*factorial(i)) if i%2==0 else F(0) for i in range(N)]
    sinh=[F(1,2**i*factorial(i+1)) if i%2==0 else F(0) for i in range(N)]
    num=[6*x for x in divide(cosh,sinh)]
    den=[F(1,factorial(i)) if i%2==0 else F(0) for i in range(N)]; den[0]+=5
    theta=[((1 if i==0 else 0)-x)/2 for i,x in enumerate(divide(num,den))]
    check(theta == [F(0)]*4+[F(1,240),F(0),F(-1,4032),F(0),F(-1,172800)], 'exact_taylor_coefficients')
    values=[]
    with localcontext() as ctx:
        ctx.prec=65
        one=Decimal(1)
        def theta_of_t(t):
            m=(-t).exp()
            return (one-6*m*(one+m)*t/((one-m)*(m*m+10*m+one)))/2
        for target in ['0.001','0.01','0.1','0.25','0.4','0.49']:
            th=Decimal(target); lo=Decimal('1e-10'); hi=Decimal(30)
            for _ in range(240):
                mid=(lo+hi)/2
                if theta_of_t(mid)<th:lo=mid
                else:hi=mid
            t=(lo+hi)/2; m=(-t).exp(); h=m/(one+m)**2
            lam=h/((one+8*h).sqrt()**3); s=(one-4*h).sqrt()
            original=(one-6*h*((one+s)/(one-s)).ln()/((one+8*h)*s))/2
            check(abs(original-th)<Decimal('1e-58'), 'decimal_parameter_diagnostic')
            D=one/t; tube=one/(3*(one/lam).ln())
            check(tube<D/3, 'decimal_parameter_diagnostic')
            values.append({'theta':target,'D_diagnostic':format(D,'.14f'),'rigid_tube_cutoff_diagnostic':format(tube,'.14f')})
    return values

def all_graph_checks():
    tested=0
    for n in range(1,6):
        edges=list(combinations(range(n),2))
        for mask in range(1<<len(edges)):
            adj=adj_from_edges(range(n), [e for i,e in enumerate(edges) if mask>>i&1])
            ds=distances(adj)
            if ds is None:continue
            tested+=1; diameter=max(max(row.values()) for row in ds.values())
            for r in range(diameter+1):
                Z=sum(d>r for row in ds.values() for d in row.values())
                for s in range(diameter+1):
                    check(not(diameter>r+2*s) or Z>=2*(s+1)**2, 'geodesic_witness_inequality')
                sizes={v:sum(d<=r for d in ds[v].values()) for v in adj}
                v=max(sizes,key=sizes.get); S=[w for w in adj if ds[v][w]<=r]
                check(n*len(S)>=n*n-Z, 'metric_subset_size')
                check(all(ds[x][y]<=2*r for x in S for y in S), 'metric_subset_diameter')
    return tested

def tube_patch(boundary,ell,next_id):
    cycles=[list(boundary)]
    for j in range(ell):
        cycles.append(list(range(next_id+3*j,next_id+3*j+3)))
    faces=[]
    for j in range(1,ell+1):
        a,b=cycles[j-1],cycles[j]
        for i in range(3):
            k=(i+1)%3
            faces += [(a[i],a[k],b[k]),(a[i],b[k],b[i])]
    faces.append(tuple(cycles[-1]))
    return faces,cycles

def graph_from_faces(faces):
    edges=[];vertices=set()
    for f in faces:
        vertices.update(f)
        edges.extend(zip(f,f[1:]+f[:1]))
    return adj_from_edges(vertices,edges)

def oriented_surface_check(faces):
    incidence=Counter()
    for f in faces:
        for a,b in zip(f,f[1:]+f[:1]):incidence[(a,b)]+=1
    check(all(incidence[(b,a)]==c==1 for (a,b),c in incidence.items()), 'oriented_surface_edge_incidence')

def tube_checks():
    tetra=[(0,1,2),(0,3,1),(1,3,2),(0,2,3)]
    bases=[tetra]
    for q in [3,4,5]:
        faces=[]
        v=lambda i,j:(i%q)*q+j%q
        for i,j in product(range(q),repeat=2):
            faces += [(v(i,j),v(i+1,j),v(i+1,j+1)),(v(i,j),v(i+1,j+1),v(i,j+1))]
        bases.append(faces)
    tested=0
    for base in bases:
        old=graph_from_faces(base); oldd=distances(old)
        E=sum(map(len,old.values()))//2
        chi=len(old)-E+len(base)
        for ell in range(1,31):
            patch,cyc=tube_patch(base[0],ell,max(old)+1)
            fs=base[1:]+patch; new=graph_from_faces(fs); ds=distances(new)
            oriented_surface_check(fs)
            check(len(fs)==len(base)+6*ell,'tube_counts')
            check(len(new)==len(old)+3*ell,'tube_counts')
            check(sum(map(len,new.values()))//2==E+9*ell,'tube_counts')
            check(len(new)-sum(map(len,new.values()))//2+len(fs)==chi,'tube_euler_characteristic')
            for x,y in product(old,repeat=2):check(ds[x][y]==oldd[x][y],'tube_old_distance_preservation')
            for layer,vs in enumerate(cyc):
                for x in vs:check(min(ds[x][y] for y in old)==layer,'tube_layer_distance')
            for n in [3*ell+1,6*ell+2,1000+3*ell]:
                # Rational root-dart correction and exact deletion prefactor.
                check(F(6*n-18*ell,6*n)==F(n-3*ell,n),'tube_reroot_prefactor')
                check(F(n,n-3*ell)*6*(n-3*ell)==6*n,'tube_reroot_prefactor')
            tested+=1
    return tested

def decoration_checks():
    tested=0
    for n in range(3,9):
        for kind in ['path','cycle','complete']:
            edges=[(i,i+1) for i in range(n-1)]
            if kind=='cycle':edges += [(n-1,0)]
            if kind=='complete':edges=list(combinations(range(n),2))
            C=adj_from_edges(range(n),edges); cd=distances(C)
            for heights in [(1,2,3),(3,1,4),(4,4,2)]:
                graph={v:set(ws) for v,ws in C.items()}; ints=[]; anchors=[]; nextv=n
                for i,height in enumerate(heights):
                    a=i; boundary=[a,a+1] if i+1<n else [a]
                    anchors.append(a); vertices=list(range(nextv,nextv+height));nextv+=height
                    for x in vertices:graph[x]=set()
                    for v in boundary:graph[v].add(vertices[0]);graph[vertices[0]].add(v)
                    for x,y in zip(vertices,vertices[1:]):graph[x].add(y);graph[y].add(x)
                    ints.append((vertices,boundary))
                ds=distances(graph)
                check(all(ds[x][y]==cd[x][y] for x,y in product(C,repeat=2)),'decoration_core_isometry')
                H=[]
                for vs,A in ints:H.append(max(min(ds[x][a] for a in A) for x in vs))
                for i,j in combinations(range(3),2):
                    for x,y in product(ints[i][0],ints[j][0]):
                        hx=min(ds[x][a] for a in ints[i][1]);hy=min(ds[y][a] for a in ints[j][1])
                        model=hx+hy+cd[anchors[i]][anchors[j]]
                        check(model-2<=ds[x][y]<=model+2,'decoration_two_sided_metric')
                check(max(max(row.values()) for row in ds.values())<=2*max(H)+max(max(row.values()) for row in cd.values())+2,'decoration_diameter_bound')
                tested+=1
    return tested

def negative_controls():
    # A shortcut through a decoration invalidates a putative non-isometric core proof.
    core=adj_from_edges(range(7),[(i,i+1) for i in range(6)]);cd=distances(core)
    G={v:set(ws) for v,ws in core.items()}
    for v in [7,8,9]:G[v]=set()
    for a,b in [(0,7),(6,7),(0,8),(6,9)]:G[a].add(b);G[b].add(a)
    ds=distances(G)
    check(ds[0][6]!=cd[0][6],'negative_nonisometric_core_rejected')
    check(ds[8][9]<1+cd[0][6]+1,'negative_nonisometric_lower_bound_fails')
    # Perfectly dependent rare heights satisfy a one-variable tail but not the pair condition.
    p=F(1,16);M=32
    check(p>p*p,'negative_correlated_extremes_rejected')
    check(M*p==2 and p<F(1,2),'negative_mean_does_not_imply_high_probability')
    # The exact log second ratio for the valley construction is 2 sqrt(j), not o(1).
    for j in [16,25,36,49,64,81,100]:
        s=int(j**0.5)
        check(s*s==j and F(s,j)<=F(1,4),'negative_ratio_increment_small')
        check(-2*(-s)==2*s and 2*s>=8,'negative_ratio_second_difference_large')
    # A deliberately collapsed tube layer creates a shortcut and fails the depth invariant.
    patch,cycles=tube_patch((0,1,2),5,3);G=graph_from_faces(patch)
    top=cycles[-1][0];G[0].add(top);G[top].add(0)
    ds=distances(G)
    check(min(ds[top][x] for x in (0,1,2))!=5,'negative_tube_shortcut_rejected')

def run():
    diagnostics=parameter_checks()
    graph_total=all_graph_checks();tube_total=tube_checks();decoration_total=decoration_checks();negative_controls()
    return {
        'scope':'finite exact controls and Decimal diagnostics only; not an asymptotic or full-target proof',
        'all_controls_passed':True,
        'counts':dict(sorted(COUNTS.items())),
        'total_control_checks':sum(COUNTS.values()),
        'connected_labeled_graphs_through_five_vertices':graph_total,
        'triangulated_tube_instances':tube_total,
        'decorated_graph_instances':decoration_total,
        'parameter_values':diagnostics,
        'full_target_solved':False,
        'typical_distance_result':'credited to Lions 2026, not re-proved',
        'diameter_ratio_three':'unresolved'
    }

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write-results',action='store_true');args=ap.parse_args()
    result=run();render=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.write_results:Path(__file__).with_name('RESULTS.json').write_text(render)
    else:
        expected=json.loads(Path(__file__).with_name('RESULTS.json').read_text())
        if expected!=result:raise RuntimeError('Recorded result mismatch')
    print(render,end='')
