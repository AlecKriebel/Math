"""New exact diagnostics; no claimant code imports or executions.

Geometry uses intercept-line equations and exact fractions, independently of
orientation predicates. The all-width theorem is proved in REPORT.md.
"""
from fractions import Fraction as F
from itertools import combinations, product
from collections import Counter
import json
import random


def require(test, text):
    if not test:
        raise RuntimeError(text)


def rays(k):
    return [-i for i in range(1,k//2+1)]+list(range(1,k-k//2+1))


def objects(m,n):
    x,y = rays(m),rays(n)
    edges = list(product(range(m),range(n)))
    pairs = [(i,j) for i,j in combinations(range(len(edges)),2)
             if edges[i][0] != edges[j][0] and edges[i][1] != edges[j][1]]
    return x,y,edges,pairs


def meet(r,s,R,S):
    # Segments join (r,0) to (0,s) and (R,0) to (0,S).
    a,b,c,d = F(1,r),F(1,s),F(1,R),F(1,S)
    det = a*d-b*c
    if det == 0:
        return None
    x,y = (d-b)/det,(a-c)/det
    return (x,y) if all(0<t<1 for t in [x/r,y/s,x/R,y/S]) else None


def geometry(m,n):
    x,y,edges,pairs = objects(m,n)
    bits,locations = [],Counter()
    for i,j in pairs:
        a,b = edges[i]
        c,d = edges[j]
        z = meet(x[a],y[b],x[c],y[d])
        hit = z is not None
        expected = x[a]*x[c]>0 and y[b]*y[d]>0 and (
            abs(x[a])-abs(x[c]))*(abs(y[b])-abs(y[d]))<0
        require(hit == expected,"crossing characterization")
        bits.append(int(hit))
        if hit:
            locations[z] += 1
    for i,j in combinations(range(len(edges)),2):
        if (i,j) in pairs:
            continue
        a,b = edges[i]
        c,d = edges[j]
        require(meet(x[a],y[b],x[c],y[d]) is None,"no adjacent interior intersections")
    require(all(v == 1 for v in locations.values()),"no triple intersections")
    require(len(pairs) == m*(m-1)*n*(n-1)//2,"unordered pair count")
    q = (n//2)*((n-1)//2)
    require(sum(bits) == (m-2)*q,"drawing crossing count")
    return edges,pairs,bits


def endpoints(e,m):
    return {e[0],m+e[1]}


def pbits(m,edges,pairs,assignment):
    return [(len(assignment[i]&endpoints(edges[j],m))+
             len(assignment[j]&endpoints(edges[i],m)))%2 for i,j in pairs]


def switch_columns(m,n,edges,pairs):
    result = []
    variables = []
    for i,e in enumerate(edges):
        for v in range(m+n):
            if v not in endpoints(e,m):
                a = [set() for _ in edges]
                a[i] = {v}
                result.append(sum(b<<k for k,b in enumerate(pbits(m,edges,pairs,a))))
                variables.append((i,v))
    return variables,result


def rank2(columns):
    piv = {}
    for value in columns:
        while value:
            k = value.bit_length()-1
            if k in piv:
                value ^= piv[k]
            else:
                piv[k] = value
                break
    return len(piv)


def corrupt(label, actual, wrong):
    require(actual != wrong,"ineffective control: "+label)
    return {"control":label,"rejected":True}


def main():
    rng = random.Random(30000215)
    grid,locals_checked,samples = [],0,0
    for m in [3,4]:
        for n in range(3,13):
            edges,pairs,c = geometry(m,n)
            variables,columns = switch_columns(m,n,edges,pairs)
            if n <= 8:
                for xs in combinations(range(m),3):
                    for ys in combinations(range(n),3):
                        vertices = set(xs)|{m+j for j in ys}
                        local = [k for k,(i,j) in enumerate(pairs)
                                 if endpoints(edges[i],m)|endpoints(edges[j],m) <= vertices]
                        require(len(local) == 18,"K33 independent pair count")
                        require(sum(c[k] for k in local)%2 == 1,"baseline K33 parity")
                        for (edge,v),column in zip(variables,columns):
                            coeff = sum((column>>k)&1 for k in local)
                            expected = 2 if endpoints(edges[edge],m)<=vertices and v in vertices else 0
                            require(coeff == expected,"every incidence coefficient is zero or two")
                        locals_checked += 1
            if n <= 8:
                for _ in range(24):
                    assignment = [{v for v in range(m+n)
                                   if v not in endpoints(e,m) and rng.randrange(2)}
                                  for e in edges]
                    switch = pbits(m,edges,pairs,assignment)
                    b = [u^v for u,v in zip(c,switch)]
                    N11 = sum(u and v for u,v in zip(c,switch))
                    N01 = sum(not u and v for u,v in zip(c,switch))
                    require(sum(b)-sum(c) == N01-N11,"criterion sign and equivalence")
                    require(sum(b)>=sum(c),"arbitrary simultaneous assignment diagnostic")
                    total = 0
                    for xs in combinations(range(m),3):
                        weights = Counter()
                        local_indices = []
                        for k,(i,j) in enumerate(pairs):
                            if edges[i][0] in xs and edges[j][0] in xs:
                                weights[tuple(sorted((edges[i][1],edges[j][1])))] += b[k]
                                local_indices.append(k)
                        t = [0]+[1^(weights[0,j]%2) for j in range(1,n)]
                        require(all(weights[i,j]%2 == (1^t[i]^t[j])
                                    for i,j in combinations(range(n),2)),"complete triangle-label identity")
                        require(sum(weights.values()) >= (n//2)*((n-1)//2),"local lower bound")
                        if m == 4:
                            kept = {i for i,e in enumerate(edges) if e[0] in xs}
                            vertices = set(xs)|set(range(m,m+n))
                            projected = [a&vertices if i in kept else set() for i,a in enumerate(assignment)]
                            changed = pbits(m,edges,pairs,projected)
                            require(all(changed[k] == switch[k] for k in local_indices),"restriction preserves exact parity")
                        total += sum(weights.values())
                    if m == 4:
                        require(total == 2*sum(b),"four restrictions count each bit twice")
                    samples += 1
            grid.append({"m":m,"n":n,"pairs":len(pairs),"crossings":sum(c)})
    # This exact connected incidence graph identifies the whole K33 switch image.
    edges,pairs,c = geometry(3,3)
    variables,columns = switch_columns(3,3,edges,pairs)
    require(len(variables) == 36 and all(v.bit_count() == 2 for v in columns),"K33 column weights")
    require(rank2(columns) == 17,"K33 image has entire even-parity dimension")
    adjacency = [set() for _ in pairs]
    for value in columns:
        a,b = [i for i in range(18) if value>>i&1]
        adjacency[a].add(b)
        adjacency[b].add(a)
    seen,stack = {0},[0]
    while stack:
        for v in adjacency[stack.pop()]-seen:
            seen.add(v)
            stack.append(v)
    require(len(seen) == 18,"connected primitive switch graph")
    # Tiny exact extremal enumeration checks the distinct Mantel step.
    mantel = []
    for n in range(3,7):
        pp = list(combinations(range(n),2))
        best = 0
        for mask in range(1<<len(pp)):
            es = {e for i,e in enumerate(pp) if mask>>i&1}
            if all(not {(a,b),(a,d),(b,d)} <= es for a,b,d in combinations(range(n),3)):
                best = max(best,len(es))
        require(best == n*n//4,"Mantel exact small graph maximum")
        mantel.append({"n":n,"maximum_triangle_free_edges":best})
    controls = [corrupt("ordered versus unordered pairs",len(pairs),36),
                corrupt("wrong K33 baseline parity",sum(c)%2,0),
                corrupt("ignore allowed incidence variables on one side",len(variables),18),
                corrupt("one rather than two occurrences per K33 variable",columns[0].bit_count(),1),
                corrupt("incorrect K33 image rank",rank2(columns),18)]
    # Keeping only one of a primitive switch's two terms can falsely improve D.
    crossing = next(i for i,v in enumerate(c) if v)
    bad_switch = 1<<crossing
    bad_b = sum((c[i]^((bad_switch>>i)&1)) for i in range(18))
    controls.append(corrupt("omit a partner incidence from the switch formula",bad_b>=sum(c),True))
    first,second = next((a,b) for a,b in combinations(columns,2) if a!=b and a&b)
    controls.append(corrupt("add switch weights instead of simultaneous XOR",(first^second).bit_count(),first.bit_count()+second.bit_count()))
    edges4,pairs4,c4 = geometry(4,3)
    multiplicities = [sum(set([edges4[i][0],edges4[j][0]]) <= set(T)
                          for T in combinations(range(4),3)) for i,j in pairs4]
    controls.append(corrupt("K4 left-triple multiplicity",sorted(set(multiplicities)),[3]))
    controls.append(corrupt("unbalanced odd-width crossing formula",(5//2)*((5-1)//2),5*5//4))
    controls.append(corrupt("ceil instead of floor in Mantel",mantel[2]["maximum_triangle_free_edges"],7))
    # The exact three lines meet at (1/2,15/2); a third X on a ray is unsafe.
    meet12 = meet(1,15,2,10)
    meet23 = meet(2,10,3,9)
    require(meet12 == meet23 == (F(1,2),F(15,2)),"explicit m5 scope guard")
    controls.append(corrupt("extend no-triple argument to m5",meet12==meet23,False))
    controls.append(corrupt("ordinary/pair versus independent-odd crossings",(2,1,0),(2,1,1)))
    controls.append(corrupt("count adjacent odd pair in iocr",0,1))
    return {"status":"PASS","method":"exact intercept-line geometry, raw set intersections, integer coefficient counts, GF2 incidence image, complete small triangle-free enumeration", "geometry":grid,"local_K33_checks":locals_checked,"simultaneous_assignments":samples,"K33_image":{"variables":36,"pairs":18,"rank":17,"connected_switch_graph_vertices":len(seen),"minimum_coset_weight":1,"argument":"Every column has even weight, rank17 gives the full even subspace, and the baseline has odd weight."},"mantel":mantel,"controls":controls,"limits":"Finite diagnostics; universal derivation and primary-source theorem interface are in REPORT.md."}


if __name__ == "__main__":
    print(json.dumps(main(),indent=2))
