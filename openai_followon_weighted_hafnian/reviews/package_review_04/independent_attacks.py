"""Bounded independent falsification mechanisms for package review 04.

Own enumerator and DAG-to-graph assembly, mixed gluing orientations, and
full symbolic adaptive sampler laws with nonzero failed estimates. Finite
evidence is not an upstream-FPRAS or all-input proof certificate.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations, product
from collections import Counter
import hashlib, json, sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'extracted/code'))
import gadget as g
import sampling as s

def own_matchings(vertices, edges):
    vertices = frozenset(vertices)
    edges = set(tuple(sorted(e)) for e in edges)
    def rec(vs):
        if not vs:
            return [()]
        u = min(vs)
        out = []
        for v in sorted(vs - {u}):
            if (u, v) in edges:
                for tail in rec(vs - {u, v}):
                    out.append(tuple(sorted(((u, v),) + tail)))
        return out
    return rec(vertices)

def split(arcs, n):
    left = {0: 0}; right = {n-1: 1}; edges=[]; k=2
    for i in range(1,n-1):
        left[i],right[i]=k,k+1;edges.append((k,k+1));k+=2
    for a,b in arcs:
        edges.append(tuple(sorted((left[a],right[b]))))
    return k,edges

def dag_checks():
    cases=0
    # All labelled forward-edge DAGs on 2..5 vertices, including zero paths,
    # disconnected identity components, and direct source/sink edges.
    for n in range(2,6):
        choices=list(combinations(range(n),2))
        for mask in range(1 << len(choices)):
            arcs=[e for i,e in enumerate(choices) if mask & (1<<i)]
            paths=[0]*n;paths[0]=1
            for a in range(n):
                for u,v in arcs:
                    if u==a:paths[v]+=paths[u]
            order,edges=split(arcs,n)
            observed=[len(own_matchings(set(range(order))-set(r),edges)) for r in ((),(0,1),(0,),(1,))]
            assert observed == [paths[-1],1,0,0]
            cases+=1
    # Negative control: a disjoint internal directed two-cycle causes the
    # terminal-deleted count to exceed one. The acyclicity premise is essential.
    order,edges=split([(0,3),(1,2),(2,1)],4)
    cycle_sig=[len(own_matchings(set(range(order))-set(r),edges)) for r in ((),(0,1),(0,),(1,))]
    assert cycle_sig == [2,2,0,0]
    return {'acyclic_dag_instances':cases,'cycle_negative_control':cycle_sig}

def orientation_checks():
    pairs=list(combinations(range(4),2));weights=[1,2,3,1,2,1]
    expected={m:__import__('math').prod(weights[pairs.index(e)] for e in m)
              for m in own_matchings(range(4),pairs)}
    for orientation in product((0,1),repeat=len(pairs)):
        k=4;edges=[];owners={}
        for e,w,flip in zip(pairs,weights,orientation):
            dag=g.path_dag(w);order,local=split(dag.arcs,dag.order)
            rename={0:e[flip],1:e[1-flip]}
            for i in range(2,order):rename[i]=k;k+=1
            for a,b in local:
                edge=tuple(sorted((rename[a],rename[b])))
                assert edge not in owners
                owners[edge]=e;edges.append(edge)
        fibers=Counter()
        for pm in own_matchings(range(k),edges):
            used={e:set() for e in pairs}
            for edge in pm:used[owners[edge]].update(v for v in edge if v<4)
            assert all(not x or x==set(e) for e,x in used.items())
            image=tuple(e for e,x in used.items() if x)
            fibers[image]+=1
        assert dict(fibers)==expected
    return {'mixed_orientation_instances':64,'fibers':{str(k):v for k,v in expected.items()}}

def floor_law(weights,b):
    total=sum(weights,F(0));c=F(0);previous=0;out=[]
    for w in weights:
        c+=w;num=(c/total)*(1<<b);end=num.numerator//num.denominator
        out.append(F(end-previous,1<<b));previous=end
    assert sum(out)==1
    assert tuple(out)==s.rounded_probabilities(tuple(weights),b)
    return out

def adaptive_law(graph,eta,mode):
    par=s.parameters(len(graph.vertices),eta)
    def rec(residual,prefix):
        true=own_matchings(residual.vertices,residual.edges)
        if not residual.vertices:return {tuple(sorted(prefix)):F(1)}
        u=residual.vertices[0];children=[]
        for v in residual.neighbors(u):
            child=residual.without(u,v)
            z=len(own_matchings(child.vertices,child.edges))
            if z:children.append((v,child,z))
        assert children
        if len(children)==1:
            v,child,z=children[0]
            return rec(child,prefix+((u,v),))
        law={};j=len(children)
        for pattern in product((0,1),repeat=j):
            f=sum(pattern);prob=par.call_failure**f*(1-par.call_failure)**(j-f)
            estimates=[]
            for index,((v,child,z),failed) in enumerate(zip(children,pattern)):
                sign=1 if (v+sum(a+b for a,b in prefix)+len(child.edges))%2 else -1
                if failed:
                    estimate=(F(0) if mode=='zero' else
                              F(1<<256) if (index+len(prefix))%2 else F(1,1<<256))
                else:estimate=z*(1+sign*par.relative_error)
                estimates.append(estimate)
            if not sum(estimates):
                pm=tuple(sorted(prefix+true[0]));law[pm]=law.get(pm,F(0))+prob
                continue
            for (v,child,z),branch in zip(children,floor_law(estimates,par.bits_per_draw)):
                if branch:
                    for pm,p in rec(child,prefix+((u,v),)).items():
                        law[pm]=law.get(pm,F(0))+prob*branch*p
        return law
    return rec(graph,())

def sampler_checks():
    cases=[]
    for n in (4,6):
        graph=s.Graph.make(range(n),combinations(range(n),2))
        matchings=own_matchings(graph.vertices,graph.edges)
        target={m:F(1,len(matchings)) for m in matchings}
        for eta in (F(1,2),F(1,10)):
            par=s.parameters(n,eta)
            bound=par.pairs*par.relative_error/(1-par.relative_error)+par.call_cap*par.call_failure+F(par.call_cap,1<<par.bits_per_draw)
            for mode in ('zero','huge_and_tiny'):
                law=adaptive_law(graph,eta,mode)
                assert sum(law.values())==1 and set(law)<=set(target)
                tv=sum(abs(law.get(m,F(0))-p) for m,p in target.items())/2
                assert tv<=bound<eta
                cases.append({'n':n,'eta':str(eta),'failed_estimates':mode,'tv':str(tv),'theorem_bound':str(bound)})
    # Fully integrate the imperative executable's first categorical draw under
    # huge, zero and tiny failed values on K4 (its later choices are forced).
    graph=s.Graph.make(range(4),combinations(range(4),2));eta=F(1,10);par=s.parameters(4,eta)
    weights=(F(1<<256),F(0),F(1,1<<256));expected=floor_law(weights,par.bits_per_draw)
    tally=Counter()
    for r in range(1<<par.bits_per_draw):
        calls=iter(weights);stats=s.Stats()
        pm=s.sample_perfect_matching(graph,eta,lambda *_:next(calls),s.exact_witness,lambda b:r,stats)
        assert pm in own_matchings(graph.vertices,graph.edges)
        first=next(v for u,v in pm if u==0);tally[first]+=1
        assert stats.count_calls<=par.call_cap and stats.random_bits<=par.pairs*par.bits_per_draw
    observed=[F(tally[i],1<<par.bits_per_draw) for i in (1,2,3)]
    assert observed==expected
    return {'adaptive_symbolic_laws':cases,'imperative_draws':1<<par.bits_per_draw,'imperative_branch_law':list(map(str,observed))}

if __name__=='__main__':
    report={'status':'passed','scope':'bounded finite corroboration only','dag':dag_checks(),'orientation':orientation_checks(),'sampler':sampler_checks(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'INDEPENDENT_ATTACKS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
