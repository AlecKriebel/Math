"""Fresh audit of frozen certificates; never starts an unresolved author search.

Independence: tree replay uses immutable sets and reconstruction of admissibility
from the entire selected family; normal forms use multisets rather than the
builder's recursion or checker Cartesian product; private covers include every
size 0..3. The trace replay uses vertex bitmasks. No author module is imported.
"""
from pathlib import Path
from itertools import combinations, combinations_with_replacement, product
from collections import Counter
from math import comb
from fractions import Fraction
import gzip, hashlib, json, copy

SOURCE = Path(__file__).resolve().parent.parent
OUT = Path(__file__).parent

def require(ok, why):
    if not ok: raise ValueError(why)

def unpack(mask, n):
    return frozenset(i for i in range(n) if mask & 2**i)

def encode(values):
    return sum(2**i for i in values)

def admissible(supports, n, tau, capacity=3):
    # A k-vertex set covering n-(tau-1-k) edges would give a (tau-1)-cover.
    for k in range(1, tau):
        for selected in combinations(supports, k):
            if len(frozenset().union(*selected)) > n - tau + k:
                return False
    rows = [frozenset(j for j, a in enumerate(supports) if i in a) for i in range(n)]
    if any(len(row) > capacity for row in rows): return False
    full = [row for row in rows if len(row) == capacity]
    return len(full) == len(set(full))

def replay_case(case, tau):
    n,d = case['edges'], case['maximum_degree']
    universe = frozenset(range(n))
    candidates = frozenset(frozenset(a) for size in range(4,d+1) for a in combinations(range(n),size))
    initial = frozenset(range(d))
    require(admissible((initial,),n,tau),'illegal fixed support')
    nodes = case['nodes']; visited = set(); leaves=0
    def visit(index, chosen, excluded):
        nonlocal leaves
        require(type(index) is int and 0<=index<len(nodes),'invalid node index')
        require(index not in visited,'reused tree node')
        visited.add(index)
        target_raw, branches = nodes[index]
        require(type(target_raw) is int and 0<=target_raw<2**n,'invalid target mask')
        target=unpack(target_raw,n)
        require(len(target)==tau+2,'wrong target size')
        require(all(len(a&target)<4 for a in chosen),'target already covered')
        possible = {a for a in candidates.difference(chosen).difference(excluded)
                    if len(a&target)>=4 and admissible(chosen+(a,),n,tau)}
        received=[]
        for raw,child in branches:
            require(type(raw) is int and 0<raw<2**n,'invalid support mask')
            a=unpack(raw,n);received.append(a)
        require(len(set(received))==len(received) and set(received)==possible,'incomplete/excess branches')
        if not branches: leaves+=1
        forbidden=set(excluded)
        for a,(_,child) in zip(received,branches):
            require(child>index,'non-forward child')
            visit(child,chosen+(a,),frozenset(forbidden))
            forbidden.add(a)
    visit(case['root'],(initial,),frozenset())
    require(len(visited)==len(nodes),'unvisited nodes')
    return {'pair':[n,d],'nodes':len(nodes),'leaves':leaves}

def audit_trees():
    summaries=[]; raw_cases={}
    expected3={(n,d) for n in range(6,11) for d in range(4,n-1)}
    expected4={(7,4),(8,4),(8,5),(9,5),(10,5),(9,6),(10,6),(10,7),(11,7)}
    for tau,name,expected in [(3,'turn3_tau3_certificate.json.gz',expected3),(4,'turn5_tau4_partial_certificate.json.gz',expected4)]:
        data=json.loads(gzip.decompress((SOURCE/name).read_bytes())); cases=data['cases']
        pairs=[(c['edges'],c['maximum_degree']) for c in cases]
        require(len(pairs)==len(set(pairs)) and set(pairs)==expected,'wrong final claimed cases')
        stats=[replay_case(c,tau) for c in cases]
        summaries.append({'tau':tau,'cases':stats,'total_nodes':sum(s['nodes'] for s in stats),'total_leaves':sum(s['leaves'] for s in stats)})
        raw_cases[tau]=cases
    controls=[]
    def reject(label,case,tau):
        try: replay_case(case,tau)
        except (ValueError,IndexError,TypeError): controls.append(label)
        else: raise ValueError('bad certificate accepted: '+label)
    for tau in (3,4):
        original=raw_cases[tau][0]
        bad=copy.deepcopy(original);bad['nodes'][0][0]=0;reject(f'tau{tau} wrong target',bad,tau)
        bad=copy.deepcopy(original);bad['nodes'][0][1].pop();reject(f'tau{tau} omitted branch',bad,tau)
        bad=copy.deepcopy(original);bad['nodes'][0][1]=[];reject(f'tau{tau} forged impossible leaf',bad,tau)
        bad=copy.deepcopy(original);bad['nodes'][0][1][0][1]=0;reject(f'tau{tau} cycle',bad,tau)
    # Planted nearby SAT system: complements of the five edges of K1,5.
    # All 5-row targets contain four rows of a support, tau>=3, but row capacity 4.
    sat=tuple(frozenset(range(6))-{0,i} for i in range(1,6))
    require(admissible(sat,6,3,4),'positive nearby model rejected')
    require(not admissible(sat,6,3,3),'capacity-3 negative control accepted')
    require(all(any(len(a&frozenset(t))>=4 for a in sat) for t in combinations(range(6),5)),'positive target coverage')
    controls += ['planted covering system passes capacity 4','same system fails capacity 3']
    return summaries,controls

def normal_forms(edge_count):
    # Enumerate unordered lists of outside-neighborhood types, at most E-1
    # entries because each such vertex contributes at least one graph edge.
    profiles=[]
    for k in range(edge_count):
        for seq in combinations_with_replacement(range(1,8),k):
            counts=Counter(seq)
            degree=tuple(sum(bool(mask&2**i) for mask in seq) for i in range(3))
            if max(degree,default=0)<=3:
                profiles.append((tuple(counts[i] for i in range(1,8)),seq,degree))
    endpoints=[mask for mask in range(8) if mask.bit_count()<=2]
    for internal in range(11-edge_count):
        inside=[frozenset(e) for e in ((0,1),(0,2))[:internal]]
        for u,v in product(endpoints,repeat=2):
            for counts,seq,degree in profiles:
                if internal+1+u.bit_count()+v.bit_count()+sum(degree)!=edge_count:continue
                edges={frozenset((3,4)),*inside}
                for vertex,pattern in enumerate((u,v)+seq,3):
                    edges.update(frozenset((i,vertex)) for i in range(3) if pattern&2**i)
                n=5+len(seq)
                require(len(edges)==edge_count,'constructed edge multiplicity')
                if any(sum(i in edge for edge in edges)>3 for i in range(n)):continue
                yield (internal,u,v,counts),n,edges

def small_covers(edges,n,avoid,maxsize):
    allowed=set(range(n))-set(avoid)
    return [frozenset(c) for k in range(maxsize+1) for c in combinations(sorted(allowed),k)
            if all(set(c)&e for e in edges)]

def audit_graphs():
    diamond={frozenset(e) for e in ((0,1),(0,2),(0,3),(1,2),(1,3),(2,4),(4,5),(3,5))}
    summary=[]; data8=None
    for num,name,field in [(9,'turn4_link_certificate.json','records'),(8,'turn5_degree8_certificate.json','link_records')]:
        data=json.loads((SOURCE/name).read_text());received={}
        if num==8:data8=data
        for internal,u,v,counts,witness in data[field]:
            key=(internal,u,v,tuple(counts));require(key not in received,'duplicate normal form');received[key]=witness
        visited=set(); rejected=classified=0;cover_candidates=0
        for key,n,graph in normal_forms(num):
            require(key in received,'omitted normal form');visited.add(key);w=received[key]
            if num==9 or 'bad_edge' in w:
                bad=frozenset(w if num==9 else w['bad_edge']);require(bad in graph and len(bad)==2,'invalid offending edge')
                require(not small_covers(graph-{bad},n,bad,3),'false no-cover witness')
                rejected+=1;cover_candidates+=sum(comb(n-2,k) for k in range(4))
            else:
                require(set(w)=={'diamond_image'},'invalid graph witness type')
                p=w['diamond_image'];require(n==6 and sorted(p)==list(range(6)),'invalid permutation')
                require({frozenset(p[x] for x in e) for e in diamond}==graph,'false isomorphism');classified+=1
        require(set(received)==visited,'extra normal forms')
        summary.append({'edges':num,'forms':len(visited),'rejected':rejected,'classified':classified,'cover_candidates_sizes_0_to_3':cover_candidates})
    # Independent positive/negative tests for graph predicate.
    require(all(small_covers(diamond-{e},6,e,3) for e in diamond),'diamond positive private-cover control')
    star={frozenset((0,i)) for i in range(1,6)}
    require(not small_covers(star-{frozenset((0,1))},6,{0,1},3),'degree-five star negative control')
    return summary,data8

def audit_traces(data):
    graphs={
      'k5_disjoint':[e for e in combinations(range(5),2) if e not in ((0,1),(2,3))],
      'k5_adjacent':[e for e in combinations(range(5),2) if e not in ((0,1),(0,2))],
      'diamond_path':[(0,1),(0,2),(0,3),(1,2),(1,3),(2,4),(4,5),(3,5)]}
    received={}
    for record in data['trace_cases']:
        key=(record['link'],tuple(encode(c) for c in record['private_covers']))
        require(key not in received,'duplicate trace system');received[key]=record
    visited=set();families=witnesses=0;systems=[]
    for name,es in graphs.items():
        n=1+max(max(e) for e in es); gm=[encode(e) for e in es]; full=2**n-1
        constrained=[];choices=[]
        for j,e in enumerate(gm):
            allowed=full^e
            covers=[s for s in range(2**n) if s&~allowed==0 and s.bit_count()<=3 and all(s&f for k,f in enumerate(gm) if k!=j)]
            if any(s.bit_count()<=2 for s in covers):continue
            constrained.append(j);choices.append([s for s in covers if s.bit_count()==3])
        for system in product(*choices):
            key=(name,tuple(system));require(key in received,'omitted cover system');visited.add(key)
            record=received[key]
            require(record['constrained_edges']==constrained,'wrong constrained edges')
            # Canonical trace order is increasing cardinality, then lexicographic vertices.
            traces=[encode(t) for k in (1,2,3) for t in combinations(range(n),k) if all(encode(t)&c for c in system)]
            require(record['traces']==[sorted(unpack(t,n)) for t in traces],'wrong eligible traces')
            rows={}
            for mask,a,b in record['witnesses']:
                require(mask not in rows,'duplicate packing witness');rows[mask]=(a,b)
            necessary=set();pairs=[encode(p) for p in combinations(range(n),2)]
            for mask in range(2**len(traces)):
                families+=1
                selected=[t for j,t in enumerate(traces) if mask&2**j]
                if any(all(p&t for t in selected) for p in pairs):continue
                necessary.add(mask);require(mask in rows,'omitted packing witness');a,b=rows[mask]
                require(len(a)==len(set(a))==3 and all(type(j)is int and 0<=j<len(traces) and mask&2**j for j in a),'invalid trace indices')
                require(len(b)==len(set(b))==3 and all(type(j)is int and 0<=j<8 for j in b),'invalid star indices')
                require(all(sum(bool(traces[j]&2**x) for j in a)+sum(bool(gm[j]&2**x) for j in b)<=3 for x in range(n)),'invalid packing capacity')
                witnesses+=1
            require(necessary==set(rows),'extra trace witnesses')
            systems.append({'link':name,'constrained_edges':constrained,'traces':len(traces),'witnesses':len(rows)})
    require(visited==set(received),'extra cover system')
    return {'systems':systems,'families':families,'witnesses':witnesses}

def audit_counting():
    rows=json.loads((SOURCE/'turn5_counting_bounds.json').read_text())['rows'];survived=[]
    for row in rows:
        h,d=row['edges'],row['maximum_degree']
        counts={i:sum(len(set(t)&set(range(i)))>=4 for t in combinations(range(h),6)) for i in range(4,d+1)}
        ratio=max(Fraction(v,k) for k,v in counts.items()); upper=(ratio*3*h).__floor__()
        require({int(k):v for k,v in row['per_vertex_counts'].items()}==counts,'bad combinatorial count')
        require(row['maximum_count_per_incidence']==[ratio.numerator,ratio.denominator],'bad ratio')
        require(row['coverage_upper_bound']==upper and row['six_subsets']==comb(h,6),'bad counting bound')
        require(row['survives_counting']==(upper>=comb(h,6)),'bad disposition')
        if upper>=comb(h,6):survived.append((h,d))
    expected={(h,d) for d in range(4,8) for h in range(max(7,d+3),20)}
    require({(r['edges'],r['maximum_degree']) for r in rows}==expected and len(rows)==len(expected),'incomplete arithmetic domain')
    return {'rows':len(rows),'surviving_pairs':sorted(survived)}

def main():
    result={}
    result['trees'],result['tree_controls']=audit_trees()
    result['graphs'],data=audit_graphs()
    result['traces']=audit_traces(data)
    result['counting']=audit_counting()
    result['passed']=True
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
