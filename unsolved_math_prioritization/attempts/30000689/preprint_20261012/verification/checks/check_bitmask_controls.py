#!/usr/bin/env python3
"""Independent finite controls: bitmask faces, dense ranks and rational circuits.

This program imports neither frozen checker. It proves no universal topology.
"""
from collections import Counter, deque
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
import json
import math
import random

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def vertices(mask):
    return tuple(i for i in range(mask.bit_length()) if mask & (1 << i))

def masks(items, size):
    return [sum(1 << i for i in c) for c in combinations(items, size)]

def submasks(mask):
    out = []
    sub = mask
    while True:
        out.append(sub)
        if not sub:
            return out
        sub = (sub-1) & mask

def boundary(mask):
    return [mask ^ (1 << v) for v in vertices(mask)]

def closure(facets):
    return set().union(*(set(submasks(f)) for f in facets))

def rank(rows, prime):
    if not rows:
        return 0
    matrix = [list(r) for r in rows]
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next((i for i in range(pivot_row, len(matrix)) if matrix[i][column] % prime), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column] % prime, -1, prime)
        matrix[pivot_row] = [(v*inverse) % prime for v in matrix[pivot_row]]
        for i in range(pivot_row+1, len(matrix)):
            factor = matrix[i][column] % prime
            if factor:
                matrix[i] = [(v-factor*w) % prime for v,w in zip(matrix[i],matrix[pivot_row])]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row

def exponents(n, degree):
    if n == 1:
        return [(degree,)]
    return [(first,)+rest for first in range(degree+1) for rest in exponents(n-1,degree-first)]

def quotient(faces, n, parameter_count, degree, prime):
    allowed = lambda exponent: sum(1 << i for i,x in enumerate(exponent) if x) in faces
    top = [e for e in exponents(n,degree) if allowed(e)]
    lower = [e for e in exponents(n,degree-1) if allowed(e)]
    index = {e:i for i,e in enumerate(top)}
    rows = []
    for lower_monomial in lower:
        for power in range(parameter_count):
            row = [0]*len(top)
            for vertex in range(n):
                product = list(lower_monomial)
                product[vertex] += 1
                if tuple(product) in index:
                    row[index[tuple(product)]] = (vertex+1)**power % prime
            rows.append(row)
    relation_rank = rank(rows,prime)
    return {"monomials":len(top),"relations_rank":relation_rank,"dimension":len(top)-relation_rank}

@lru_cache(None)
def circuit(union, ambient_dimension):
    points = vertices(union)
    require(len(points)==ambient_dimension+2,"Wrong circuit size")
    coefficients = tuple(Fraction(1,math.prod(x-y for y in points if y!=x)) for x in points)
    for power in range(ambient_dimension+1):
        require(sum(c*x**power for c,x in zip(coefficients,points))==0,"Circuit affine dependence fails")
    positive = sum(1 << x for x,c in zip(points,coefficients) if c>0)
    negative = union ^ positive
    require(positive and negative,"Circuit lacks a sign")
    return positive,negative

def intersects(a,b,ambient_dimension):
    require(not a&b,"Intersecting vertex supports")
    positive,negative = circuit(a|b,ambient_dimension)
    return (a==positive and b==negative) or (b==positive and a==negative)

def deleted_boundary(cells):
    result=set()
    for a,b in cells:
        for smaller,other in [(a,b),(b,a)]:
            for face in boundary(smaller):
                cell=tuple(sorted((face,other)))
                result.symmetric_difference_update({cell})
    return result

def stellar_controls():
    records=[]
    for d in range(1,5):
        size=2*d+2
        new=1 << size
        t=(1 << (d+1))-1
        complement=((1 << size)-1)^t
        # Direct face membership, rather than a closure of altered facets.
        faces={f for f in range(1 << (size+1))
               if ((not f&new and f&t!=t) or
                   (f&new and f&t!=t and f&complement!=complement))}
        require(t not in faces and all(f in faces for f in boundary(t)),"Missing face condition")
        lower={f for f in faces if f.bit_count()<=d+1}
        augmented=lower|{t}
        full=set().union(*(set(masks(range(size+1),j)) for j in range(d+2)))
        require(augmented==full,"Flores skeleton completion")
        counts=Counter(f.bit_count() for f in faces)
        r=2*d+1
        h=[sum(counts[j]*(-1)**(i-j)*math.comb(r-j,i-j) for j in range(i+1)) for i in range(r+1)]
        require(h==[min(i+1,r-i+1) for i in range(r+1)],"Unexpected h polynomial")
        top=masks(range(size+1),d+1)
        cells={tuple(sorted((a,b))) for a,b in combinations(top,2) if not a&b}
        require(not deleted_boundary(cells),"Flores chain not closed")
        crossings=sum(intersects(a,b,2*d) for a,b in cells)
        require(crossings==2*d+3 and crossings%2==1,"Rational moment-curve pairing")
        record={"d":d,"face_counts_including_empty":[counts[j] for j in range(r+1)],"h":h,
                "cycle_cells":len(cells),"rational_circuit_crossings":crossings,"quotients":[]}
        if d<=2:
            for prime in [7,101,103]:
                sq=[quotient(faces,size+1,r,k,prime) for k in [d,d+1]]
                aq=[quotient(augmented,size+1,r,k,prime) for k in [d,d+1]]
                require(sq[0]["dimension"]==sq[1]["dimension"]==aq[0]["dimension"]==h[d],"Source quotient dimensions")
                require(aq[1]["dimension"]==h[d]+1,"Added face quotient jump")
                record["quotients"].append({"prime":prime,"source":sq,"augmented":aq})
        if d==2:
            nonempty=sorted(faces-{0})
            chains=0
            for a,b,c in combinations(nonempty,3):
                ordered=sorted((a,b,c),key=int.bit_count)
                if ordered[0]&ordered[1]==ordered[0] and ordered[1]&ordered[2]==ordered[1]:
                    chains+=1
            require(chains==3084,"Barycentric triple-chain count")
            record["barycentric_vertices"]=len(nonempty)
            record["barycentric_three_chains"]=chains
        records.append(record)
    return records

def betti(faces):
    vs=sorted(f for f in faces if f.bit_count()==1)
    es=sorted(f for f in faces if f.bit_count()==2)
    ts=sorted(f for f in faces if f.bit_count()==3)
    r1=rank([[int(v in boundary(e)) for e in es] for v in vs],2)
    r2=rank([[int(e in boundary(t)) for t in ts] for e in es],2)
    return [len(vs)-r1-1,len(es)-r1-r2]

def missing(faces):
    support=0
    for f in faces:
        support|=f
    return {f for f in masks(vertices(support),3) if f not in faces and all(e in faces for e in boundary(f))}

def path_chain(faces,source,target,forbidden):
    es=[f for f in faces if f.bit_count()==2 and not f&forbidden]
    adjacency={v:[] for v in vertices(source|target)}
    for edge in es:
        u,v=vertices(edge)
        adjacency.setdefault(u,[]).append((v,edge))
        adjacency.setdefault(v,[]).append((u,edge))
    start=vertices(source)[0]
    end=vertices(target)[0]
    previous={start:None}
    todo=deque([start])
    while todo and end not in previous:
        current=todo.popleft()
        for nxt,edge in sorted(adjacency.get(current,[])):
            if nxt not in previous:
                previous[nxt]=(current,edge)
                todo.append(nxt)
    require(end in previous,"No independently found filling path")
    result=set()
    current=end
    while current!=start:
        prior,edge=previous[current]
        result.add(edge)
        current=prior
    return result

def triangle_filling(faces,target,forbidden):
    triangles=sorted(f for f in faces if f.bit_count()==3 and not f&forbidden)
    edges=sorted(set(target).union(*(set(boundary(t)) for t in triangles)))
    # Dense row reduction of the augmented boundary equation, rather than the
    # frozen audit's packed-column elimination with carried solution masks.
    matrix=[[int(e in boundary(t)) for t in triangles]+[int(e in target)] for e in edges]
    pivots=[]
    row=0
    for column in range(len(triangles)):
        pivot=next((i for i in range(row,len(matrix)) if matrix[i][column]),None)
        if pivot is None:
            continue
        matrix[row],matrix[pivot]=matrix[pivot],matrix[row]
        for i in range(len(matrix)):
            if i!=row and matrix[i][column]:
                matrix[i]=[x^y for x,y in zip(matrix[i],matrix[row])]
        pivots.append((row,column))
        row+=1
    require(all(any(r[:-1]) or not r[-1] for r in matrix),"No mod-2 triangle filling")
    result={triangles[col] for r,col in pivots if matrix[r][-1]}
    actual=set()
    for t in result:
        actual.symmetric_difference_update(boundary(t))
    require(actual==target,"Returned filling has wrong boundary")
    return result

def witness(faces,new_faces,a,b,v):
    U=a|b
    M=b|v
    V=U|v
    cones={}
    for w in vertices(U):
        point=1 << w
        edge=v|point
        cones[point]={edge} if edge in faces else path_chain(faces,v,point,U^point)
    for edge in sorted(f for f in faces if f.bit_count()==2 and f&U==f):
        triangle=edge|v
        if triangle in faces:
            cones[edge]={triangle}
        else:
            cycle={edge}
            for point in boundary(edge):
                cycle.symmetric_difference_update(cones[point])
            cones[edge]=triangle_filling(faces,cycle,U^edge)
    mapped=lambda triangle: {triangle} if not triangle&v or triangle==M else cones[triangle^v]
    triangles=masks(vertices(V),3)
    omega=set()
    for s,t in combinations(triangles,2):
        if s&t:
            continue
        for x in mapped(s):
            for y in mapped(t):
                require(not x&y,"Mapped supports overlap")
                require(x in new_faces|{M} and y in new_faces|{M},"Mapped triangle outside augmentation")
                omega.symmetric_difference_update({tuple(sorted((x,y)))})
    require(not deleted_boundary(omega),"Transferred deleted chain has boundary")
    paired={t if s==M else s for s,t in omega if s==M or t==M}
    require(paired==set(boundary(a)),"Wrong triangles paired with missing face")
    pairing=sum(intersects(s,t,4) for s,t in omega)%2
    require(pairing==1,"Transferred rational-circuit pairing vanished")
    return {"cells":len(omega),"pairing_mod2":pairing}

def bistellar_controls():
    rng=random.Random(202610120468)
    facets=set(masks(range(6),5))
    next_vertex=6
    counts=Counter()
    complements=common=new22=new31=0
    details=[]
    for step in range(100):
        faces=closure(facets)
        options=[]
        for a in sorted(faces-{0}):
            star={f for f in facets if f&a==a}
            if a.bit_count()==5:
                b=1 << next_vertex
            else:
                residues={f^a for f in star}
                b=0
                for residue in residues:
                    b|=residue
                if a.bit_count()+b.bit_count()!=6 or b in faces or residues!=set(boundary(b)):
                    continue
            replacement={b|face for face in boundary(a)}
            options.append((a,b,(facets-star)|replacement))
        require(options,"No bistellar option")
        vertex_count=len({v for f in faces for v in vertices(f)})
        weights=[]
        for a,b,_ in options:
            p=a.bit_count()-1
            weight=1/(1+counts[p])
            if p==4 and vertex_count>=9:
                weight*=0.02
            if p==0 and vertex_count>9:
                weight*=6
            weights.append(weight)
        a,b,new_facets=rng.choices(options,weights=weights)[0]
        new_faces=closure(new_facets)
        p=a.bit_count()-1
        q=b.bit_count()-1
        counts[p]+=1
        if q==0:
            next_vertex+=1
        U=a|b
        local_old={f for f in faces if f&U==f and f.bit_count()<=3}
        local_new={f for f in new_faces if f&U==f and f.bit_count()<=3}
        support=0
        for f in local_old:
            support|=f
        for rho in local_old&local_new:
            removed=support^rho
            induced={f for f in faces if f&removed==f}
            require(any(all(f|(1 << v) in induced for f in induced) for v in vertices(removed)),"Local induced cone fails")
            complement={f for f in faces if not f&removed and f.bit_count()<=3}
            require(betti(complement)==[0,0],"Complement mod-2 homology fails")
            complements+=1
        old_missing=missing(faces)
        new_missing=missing(new_faces)
        for M in old_missing&new_missing:
            require(M&support!=M and a&M!=a,"Persistent missing face entered support")
            common+=1
        for M in new_missing-old_missing:
            if M in faces:
                require(p==q==2 and M==a and b in old_missing,"Wrong middle move case")
                require({f for f in new_faces if f.bit_count()<=3}|{M}=={f for f in faces if f.bit_count()<=3}|{b},"Middle move augmentation identity")
                new22+=1
            else:
                require(p==3 and q==1 and M&b==b and (M&~U).bit_count()==1,"Wrong edge-created missing face case")
                details.append(witness(faces,new_faces,a,b,M&~U))
                new31+=1
        facets=new_facets
    require(set(counts)==set(range(5)) and common and new22 and new31,"Incomplete move coverage")
    return {"seed":202610120468,"transitions":100,"moves_by_p":dict(sorted(counts.items())),"complement_checks":complements,
            "persistent_missing_checks":common,"middle_move_augmentation_checks":new22,"edge_move_witnesses":new31,"witness_details":details}

def main():
    output={"scope":"Independently reformulated finite controls; no universal topology, sphere recognition or priority certification.",
            "stellar_and_flores":stellar_controls(),"bistellar":bistellar_controls(),"circuit_unions_verified":circuit.cache_info().currsize}
    print(json.dumps(output,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
