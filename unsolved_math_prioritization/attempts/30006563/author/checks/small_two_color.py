"""Exact bounded DPLL for K6/K7 with no disjoint equal-type triangles.
No third-party dependencies. Certificate verification uses separate replay logic.
Only two colors: a triangle type is its number of color-1 edges.
"""
from itertools import combinations, product
from collections import Counter
import json, signal, time
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def instance(n):
    edges=list(combinations(range(n),2)); eid={e:i for i,e in enumerate(edges)}
    triangles=[(set(t),[eid[e] for e in combinations(t,2)]) for t in combinations(range(n),3)]
    clauses=[]; pairs=0
    for (s,e),(t,f) in combinations(triangles,2):
        if s & t: continue
        pairs+=1
        for bits in product((0,1),repeat=6):
            if sum(bits[:3])!=sum(bits[3:]): continue
            pos=neg=0
            for v,b in zip(e+f,bits):
                if b: neg|=1<<v
                else: pos|=1<<v
            clauses.append((pos,neg))
    return edges,clauses,pairs

def solve(clauses,ones,zeros):
    units=[]
    while True:
        unit=None; shortest=[]; minlen=10**9
        for i,(p,m) in enumerate(clauses):
            if p & ones or m & zeros: continue
            pp=p & ~zeros; mm=m & ~ones; un=pp|mm
            if not un: return None,{'units':units,'conflict':i}
            k=un.bit_count()
            if k==1:
                var=un.bit_length()-1; val=int(bool(pp))
                unit=(var,val,i);break
            if k<minlen: shortest=[un];minlen=k
            elif k==minlen: shortest.append(un)
        if unit is None: break
        v,b,i=unit;units.append([v,b,i])
        if b:ones|=1<<v
        else:zeros|=1<<v
    if not shortest: return ones,{'units':units,'sat':True}
    counts=Counter(v for mask in shortest for v in range(mask.bit_length()) if mask>>v&1)
    v=max(counts,key=counts.get)
    answer,left=solve(clauses,ones,zeros|1<<v)
    if answer is not None:return answer,{}
    answer,right=solve(clauses,ones|1<<v,zeros)
    if answer is not None:return answer,{}
    return None,{'units':units,'branch':v,'zero':left,'one':right}

def verify(clauses,node,values):
    # Explicit literal-list evaluation independent of bitmask propagation.
    vals=dict(values);nodes=1
    def literals(i):
        p,m=clauses[i]
        return [(j,1) for j in range(p.bit_length()) if p>>j&1]+[(j,0) for j in range(m.bit_length()) if m>>j&1]
    def remaining(i):
        ls=literals(i)
        assert not any(v in vals and vals[v]==b for v,b in ls)
        return [(v,b) for v,b in ls if v not in vals]
    for v,b,i in node['units']:
        assert remaining(i)==[(v,b)]
        vals[v]=b
    if 'conflict' in node:
        assert remaining(node['conflict'])==[]
        return nodes
    v=node['branch'];assert v not in vals
    nodes+=verify(clauses,node['zero'],dict(vals,**{})|{v:0})
    nodes+=verify(clauses,node['one'],dict(vals,**{})|{v:1})
    return nodes

def witness_ok(n,edges,ones):
    groups={}
    for t in combinations(range(n),3):
        s=set(t); k=sum((ones>>edges.index(e))&1 for e in combinations(t,2))
        for old in groups.get(k,[]):
            assert old&s,('disjoint repeat',old,s,k)
        groups.setdefault(k,[]).append(s)

def run(n):
    start=time.monotonic(); edges,clauses,pairs=instance(n)
    # Global interchange of colors makes the first edge color 0 without loss.
    answer,cert=solve(clauses,0,1)
    r={'n':n,'q':2,'edges':len(edges),'disjoint_triangle_pairs':pairs,'clauses':len(clauses)}
    if answer is None:
        nodes=verify(clauses,cert,{0:0})
        path=ROOT/f'k{n}_two_color_unsat_certificate.json';path.write_text(json.dumps(cert,separators=(',',':'))+'\n')
        r.update(status='UNSAT',certificate_nodes=nodes,certificate_file=path.name,independent_replay='PASS')
    else:
        witness_ok(n,edges,answer)
        r.update(status='SAT',color1_edges=[e for i,e in enumerate(edges) if answer>>i&1],direct_all_pairs_check='PASS')
    r['elapsed_seconds']=round(time.monotonic()-start,3)
    return r

if __name__=='__main__':
    signal.alarm(30)
    results=[run(6),run(7),run(8)]
    (ROOT/'small_two_color_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))
