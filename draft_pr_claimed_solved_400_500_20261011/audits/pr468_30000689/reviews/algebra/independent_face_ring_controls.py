#!/usr/bin/env python3
"""Independent exact finite controls for PR468 Sections 1-2.

No author code/results imported. Work over a fixed prime field, eliminate the
ambient linear parameters, then compute quotient dimensions from polynomial
ideal generators. These controls check finite examples, not the general theorem.
"""
import hashlib
import itertools
import json
import pathlib
import random

P = 1009
ROOT = pathlib.Path(__file__).resolve().parent


def rank(rows, width):
    pivots = {}
    for original in rows:
        row = [x % P for x in original]
        for col in sorted(pivots):
            if row[col]:
                scale = row[col]
                other = pivots[col]
                row = [(a-scale*b) % P for a,b in zip(row,other)]
        nonzero = next((i for i,x in enumerate(row) if x),None)
        if nonzero is not None:
            scale = pow(row[nonzero], -1, P)
            pivots[nonzero] = [(scale*x) % P for x in row]
    return len(pivots)


def rref(matrix):
    rows = [[x % P for x in row] for row in matrix]
    pivots = []
    k = 0
    for col in range(len(rows[0])):
        candidate = next((i for i in range(k,len(rows)) if rows[i][col]),None)
        if candidate is None:
            continue
        rows[k],rows[candidate] = rows[candidate],rows[k]
        scale = pow(rows[k][col],-1,P)
        rows[k] = [(scale*x)%P for x in rows[k]]
        for i in range(len(rows)):
            if i != k and rows[i][col]:
                scale = rows[i][col]
                rows[i] = [(a-scale*b)%P for a,b in zip(rows[i],rows[k])]
        pivots.append(col)
        k += 1
        if k == len(rows):
            break
    return rows,pivots


def monomials(count,degree):
    if count == 0:
        return [()] if degree == 0 else []
    if count == 1:
        return [(degree,)]
    return [(k,)+tail for k in range(degree+1)
            for tail in monomials(count-1,degree-k)]


def multiply(poly,other):
    result = {}
    for a,ca in poly.items():
        for b,cb in other.items():
            key = tuple(x+y for x,y in zip(a,b))
            result[key] = (result.get(key,0)+ca*cb)%P
    return {a:c for a,c in result.items() if c}


def closure(facets):
    return {frozenset(face) for facet in facets
            for size in range(len(facet)+1)
            for face in itertools.combinations(sorted(facet),size)}


def join_boundary(d):
    left = set(range(d+1))
    right = set(range(d+1,2*d+3))
    facets = [frozenset((left-{a}) | (right-{b}))
              for a in left for b in right]
    return facets,frozenset(left)


def stellar_facet(facets):
    selected = facets[0]
    vertex = max(itertools.chain.from_iterable(facets))+1
    return [f for f in facets if f != selected] + [
        (selected-{v}) | frozenset({vertex}) for v in selected]


def parameters(facets,seed):
    count = max(itertools.chain.from_iterable(facets))+1
    ambient = len(facets[0])
    rng = random.Random(seed)
    for attempt in range(100):
        matrix = [[rng.randrange(P) for _ in range(count)]
                  for _ in range(ambient)]
        if all(rank([[row[v] for v in sorted(facet)] for row in matrix],ambient)
               == ambient for facet in facets):
            return matrix,attempt+1
    raise RuntimeError('No certified l.s.o.p. found')


def linear_images(matrix):
    reduced,pivots = rref(matrix)
    vertices = len(matrix[0])
    free = [v for v in range(vertices) if v not in pivots]
    images = []
    for vertex in range(vertices):
        coefficients = [0]*len(free)
        if vertex in free:
            coefficients[free.index(vertex)] = 1
        else:
            row = reduced[pivots.index(vertex)]
            coefficients = [(-row[v])%P for v in free]
        poly = {}
        for i,c in enumerate(coefficients):
            if c:
                exponent = [0]*len(free)
                exponent[i] = 1
                poly[tuple(exponent)] = c
        images.append(poly)
    return images,len(free)


def minimal_nonfaces(faces,vertices,degree):
    result = []
    for size in range(1,degree+1):
        for items in itertools.combinations(range(vertices),size):
            face = frozenset(items)
            if face not in faces and all(face-{v} in faces for v in face):
                result.append(face)
    return result


def quotient_dimension(faces,matrix,degree):
    images,free_count = linear_images(matrix)
    basis = monomials(free_count,degree)
    relations = []
    for nonface in minimal_nonfaces(faces,len(images),degree):
        poly = {(0,)*free_count:1}
        for vertex in sorted(nonface):
            poly = multiply(poly,images[vertex])
        for extra in monomials(free_count,degree-len(nonface)):
            relation = {tuple(x+y for x,y in zip(exponent,extra)):coefficient
                        for exponent,coefficient in poly.items()}
            relations.append([relation.get(exponent,0) for exponent in basis])
    relation_rank = rank(relations,len(basis))
    return len(basis)-relation_rank


def h_vector(faces,ambient):
    # Expand sum_{F in S} t^{|F|}(1-t)^{r-|F|} using integer binomial coefficients.
    import math
    result = [0]*(ambient+1)
    for face in faces:
        size = len(face)
        for extra in range(ambient-size+1):
            result[size+extra] += (-1)**extra*math.comb(ambient-size,extra)
    return result


def ring_monomials(faces,vertices,degree):
    return [m for m in monomials(vertices,degree)
            if frozenset(i for i,e in enumerate(m) if e) in faces]


def koszul_h1(faces,matrix,total_degree):
    vertices = len(matrix[0]); ambient = len(matrix)
    b0 = ring_monomials(faces,vertices,total_degree)
    b1 = ring_monomials(faces,vertices,total_degree-1)
    b2 = ring_monomials(faces,vertices,total_degree-2)
    ix0 = {m:i for i,m in enumerate(b0)}
    ix1 = {(m,j):i for i,(m,j) in enumerate(itertools.product(b1,range(ambient)))}
    d1_columns = []
    for m,j in itertools.product(b1,range(ambient)):
        row = [0]*len(b0)
        for v,c in enumerate(matrix[j]):
            target = list(m); target[v] += 1; target = tuple(target)
            if target in ix0:
                row[ix0[target]] = c
        d1_columns.append(row)
    d2_columns = []
    for m,(i,j) in itertools.product(b2,itertools.combinations(range(ambient),2)):
        row = [0]*len(ix1)
        # d(e_i wedge e_j) = theta_i e_j - theta_j e_i.
        for v in range(vertices):
            target = list(m); target[v] += 1; target = tuple(target)
            if (target,j) in ix1:
                row[ix1[target,j]] = matrix[i][v]
            if (target,i) in ix1:
                row[ix1[target,i]] = (-matrix[j][v])%P
        d2_columns.append(row)
    r1 = rank(d1_columns,len(b0))
    r2 = rank(d2_columns,len(ix1))
    return {'H1_dimension':len(ix1)-r1-r2,
            'C0_dimension':len(b0),'C1_dimension':len(ix1),
            'C2_dimension':len(d2_columns),'d1_rank':r1,'d2_rank':r2}


def require(condition,message):
    if not condition:
        raise RuntimeError(message)


def main():
    cases = []
    for d in range(1,5):
        original,T = join_boundary(d)
        for modified in (False,True):
            facets = stellar_facet(original) if modified else original
            A = closure(facets)
            require(T not in A and all(T-{v} in A for v in T),'Missing-face gate failed')
            C = {f for f in A if len(f)<=d+1}
            B = C | {T}
            h = h_vector(A,2*d+1)
            for seed in (468,9468):
                matrix,trials = parameters(facets,seed)
                dims = {name:[quotient_dimension(faces,matrix,j) for j in (d,d+1)]
                        for name,faces in [('A',A),('C',C),('B',B)]}
                require(h[d] == h[d+1],'h symmetry failed')
                require(dims['A']==[h[d],h[d+1]],'Source quotient wrong')
                require(dims['C']==dims['A'],'Skeleton low-degree agreement failed')
                require(dims['B']==[h[d],h[d+1]+1],'Exact jump failed')
                entry = {'d':d,'stellar_facet':modified,'seed':seed,
                         'vertices':len(matrix[0]),'parameter_trials':trials,
                         'parameter_matrix':matrix,'h_vector':h,'dimensions':dims}
                if d<=2:
                    entry['koszul_C_degree_d_plus_1'] = koszul_h1(C,matrix,d+1)
                    require(entry['koszul_C_degree_d_plus_1']['H1_dimension']==0,
                            'H1 not zero for certified parameters')
                cases.append(entry)
    facets,T = join_boundary(1)
    A = closure(facets); C = {f for f in A if len(f)<=2}; B = C | {T}
    bad_matrix = [[int(v==i) for v in range(5)] for i in range(3)]
    bad = {'matrix':bad_matrix,
           'facet_parameter_ranks':[rank([[row[v] for v in sorted(f)] for row in bad_matrix],3)
                                     for f in facets],
           'C_dimension_degree2':quotient_dimension(C,bad_matrix,2),
           'B_dimension_degree2':quotient_dimension(B,bad_matrix,2),
           'koszul_C_degree2':koszul_h1(C,bad_matrix,2)}
    require(bad['C_dimension_degree2']==bad['B_dimension_degree2'],
            'Nonregular countercontrol should kill restored monomial')
    require(bad['koszul_C_degree2']['H1_dimension']>0,
            'Nonregular countercontrol should have nonzero H1')
    require(min(bad['facet_parameter_ranks'])<3,'Countercontrol unexpectedly parameters')
    # Under the alternative convention allowing a missing singleton outside
    # V(S), use one ghost variable for A=C and restore it in B.
    zero_A = {frozenset(),frozenset({0}),frozenset({1})}
    zero_B = zero_A | {frozenset({2})}
    zero_matrix = [[2,3,5]]
    zero = {'A_dimensions':[quotient_dimension(zero_A,zero_matrix,j) for j in (0,1)],
            'B_dimensions':[quotient_dimension(zero_B,zero_matrix,j) for j in (0,1)]}
    require(zero['A_dimensions']==[1,1] and zero['B_dimensions']==[1,2],
            'External missing singleton control failed')
    output = {'status':'PASS','field_prime':P,'valid_cases':cases,
              'nonregular_parameter_countercontrol':bad,
              'd0_external_singleton_control':zero,
              'limitations':'Finite exact controls do not prove generic theorem or topology.'}
    (ROOT/'independent_face_ring_results.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'status':output['status'],'valid_cases':len(cases),
                      'koszul_cases':sum('koszul_C_degree_d_plus_1' in c for c in cases),
                      'bad_H1':bad['koszul_C_degree2']['H1_dimension']}))


if __name__=='__main__':
    main()
