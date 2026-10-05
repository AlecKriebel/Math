#!/usr/bin/env python3
"""Independent exact audit of KOU-21.90. Standard library only.

Reconstructs distance multiplication from intersection recurrences and spectral
idempotents by Lagrange interpolation, without importing any author verifier or
inverting the displayed eigenmatrix. Certificates are authored input, not new.
"""
from fractions import Fraction as R
from itertools import product, permutations
from math import comb
from pathlib import Path
import collections, copy, hashlib, json

ROOT = Path(__file__).resolve().parent
N = 4
INDICES = tuple(product(range(N), repeat=3))
CHECKS = collections.Counter()

def require(condition, label):
    CHECKS[label] += 1
    if not condition:
        raise AssertionError(label)

def matmul(A, B):
    return [[sum(A[i][r] * B[r][j] for r in range(N)) for j in range(N)] for i in range(N)]

def apply(A, x):
    return [sum(a * b for a, b in zip(row, x)) for row in A]

def shifted(A, x):
    return [[A[i][j] - x * (i == j) for j in range(N)] for i in range(N)]

def reconstruct(t, c, a):
    t, c, a = map(R, (t, c, a))
    k = t * (c + 1) + a
    b = [k, t*c, a+1, R(0)]
    cs = [R(0), R(1), c, t*(c+1)]
    local = [k-b[i]-cs[i] for i in range(N)]
    L = [[R(0) for j in range(N)] for i in range(N)]
    for j in range(N):
        L[j][j] = local[j]
        if j: L[j-1][j] = b[j-1]
        if j+1 < N: L[j+1][j] = cs[j+1]
    I = [[R(i==j) for j in range(N)] for i in range(N)]
    M = [I, L]
    for i in (1, 2):
        prod = matmul(shifted(L, local[i]), M[i])
        M.append([[(prod[h][j]-b[i-1]*M[i-1][h][j])/cs[i+1] for j in range(N)] for h in range(N)])
    p = [[[M[i][h][j] for h in range(N)] for j in range(N)] for i in range(N)]
    val = [R(1)]
    for i in range(3): val.append(val[-1]*b[i]/cs[i+1])
    v = sum(val)
    theta = [k, a+t, R(-1), -c-1]
    P = []
    Q = [[R(0) for j in range(N)] for i in range(N)]
    for j, th in enumerate(theta):
        pol = [R(1), th]
        for i in (1, 2):
            pol.append(((th-local[i])*pol[-1]-b[i-1]*pol[-2])/cs[i+1])
        P.append(pol)
        require((th-local[3])*pol[3] == b[2]*pol[2], 'endpoint_recurrence')
        projector = [R(1), R(0), R(0), R(0)]
        for other in theta:
            if other != th:
                projector = [z/(th-other) for z in apply(shifted(L, other), projector)]
        for r in range(N): Q[r][j] = v*projector[r]
    require(P[0] == val, 'valency_recurrence')
    require(matmul(P, Q) == [[v*(i==j) for j in range(N)] for i in range(N)], 'PQ_orthogonality')
    require(sum(Q[0]) == v, 'multiplicity_sum')
    require(all(p[i][j][h] == p[j][i][h] for i,j,h in INDICES), 'intersection_commutativity')
    q = [[[sum(Q[r][i]*Q[r][j]*P[h][r] for r in range(N))/v for h in range(N)] for j in range(N)] for i in range(N)]
    return P, Q, p, q, v

def q_orders(q):
    # The off-diagonal Krein support must be one connected path beginning at 0.
    result = []
    for generator in (1, 2, 3):
        adjacent = [{h for h in range(N) if h != j and q[generator][j][h] != 0} for j in range(N)]
        if adjacent[0] != {generator}: continue
        order = [0]
        while len(order) < N:
            options = adjacent[order[-1]] - set(order)
            if len(options) != 1: break
            order.append(next(iter(options)))
        if len(order) != N: continue
        if any(adjacent[j] != {order[r] for r in (order.index(j)-1, order.index(j)+1) if 0<=r<N} for j in range(N)): continue
        if any(q[generator][j][h] <= 0 for j in range(N) for h in adjacent[j]): continue
        result.append(tuple(order))
    return result

def int_nonnegative(seq):
    return all(z >= 0 and z.denominator == 1 for z in seq)

def sieve():
    rows = []
    for t in range(2, 31):
        for a in range(1, t*t-1):
            den = t*t-a-1
            quotient, rem = divmod(a*(a+1), den)
            if rem or quotient < 2: continue
            c = quotient-1
            P,Q,p,q,v = reconstruct(t,c,a)
            k = t*(c+1)+a
            reasons = set()
            if not int_nonnegative(P[0]+Q[0]): reasons.add('nonintegral_valency_or_multiplicity')
            if not int_nonnegative(z for i in p for j in i for z in j): reasons.add('intersection_number')
            if any(z<0 for i in q for j in i for z in j): reasons.add('negative_Krein')
            if not q_orders(q): reasons.add('not_Q_polynomial')
            if not (k>=t*c>=a+1 and 1<=c<=t*(c+1)): reasons.add('intersection_array_monotonicity')
            for shell in (1,2,3):
                for relation in (1,2,3):
                    ends = P[0][shell]*p[shell][relation][shell]
                    if ends.denominator==1 and ends.numerator%2: reasons.add('shell_edge_parity')
            alpha = -(-k//(a+t))
            if k < alpha*(a+t)-comb(alpha,2)*(c-1): reasons.add('local_claw_bound')
            for rel in (2,3):
                eigenspaces = {}
                for j in (1,2,3): eigenspaces[P[j][rel]] = eigenspaces.get(P[j][rel],R(0))+Q[0][j]
                require(len(eigenspaces)==2, 'fusion_two_restricted_eigenvalues')
                for m in eigenspaces.values():
                    if 2*v>m*(m+3): reasons.add('SRG_absolute_bound_distance_'+str(rel))
            rows.append(dict(t=t,c=c,a=a,array=[k,t*c,a+1,1,c,t*(c+1)],v=int(v) if v.denominator==1 else str(v),rejections=sorted(reasons)))
    return rows

def equation_system(parameters, triangle):
    P,Q,p,q,v = reconstruct(*parameters)
    xy,xz,yz = triangle
    equations = []
    # Sparse coordinate dictionaries; ordering matches the certificate schema.
    for i,j in product(range(N),repeat=2):
        for left,right,dist in ((0,1,xy),(0,2,xz),(1,2,yz)):
            equations.append(({x:R(1) for x in INDICES if x[left]==i and x[right]==j},p[i][j][dist]))
    for x in INDICES:
        if 0 in x:
            value = int(x in ((0,xy,xz),(xy,0,yz),(xz,yz,0)))
            equations.append(({x:R(1)},R(value)))
    for r,s,u in product((1,2,3),repeat=3):
        if q[r][s][u]==0:
            row = {x:Q[x[0]][r]*Q[x[1]][s]*Q[x[2]][u] for x in INDICES}
            equations.append(({x:z for x,z in row.items() if z},R(0)))
    return equations, p

def certify(cert):
    eq,p = equation_system((cert['t'],cert['c'],cert['a']),cert['triangle'])
    d,e,f = cert['triangle']
    require(all(1<=x<=3 for x in (d,e,f)), 'distinct_base_vertices')
    require(p[e][f][d]>0, 'base_triangle_occurs')
    require(len(eq)==cert['equation_count'], 'certificate_equation_count')
    y = {}
    for index, val in cert['multipliers']:
        require(index not in y and 0<=index<len(eq), 'unique_valid_multiplier_index')
        y[index] = R(val)
    lhs = {x:R(0) for x in INDICES}
    rhs = R(0)
    for index, multiplier in y.items():
        row,b = eq[index]
        rhs += multiplier*b
        for x,z in row.items(): lhs[x] += multiplier*z
    expected = {x:R(0) for x in INDICES}
    seen = set()
    for index, val in cert['nonnegative_lhs']:
        index = tuple(index)
        require(index not in seen and index in expected, 'unique_valid_lhs_index')
        seen.add(index); expected[index] = R(val)
    require(lhs==expected, 'certificate_every_coefficient')
    require(rhs==R(cert['negative_rhs']), 'certificate_rhs')
    require(all(z>=0 for z in lhs.values()) and rhs<0, 'certificate_contradiction')
    return {'parameters':[cert['t'],cert['c'],cert['a']],'triangle':list(cert['triangle']),'base_triangle_multiplicity':str(p[e][f][d]),'equations':len(eq),'negative_rhs':str(rhs),'positive_coefficients':[[list(x),str(z)] for x,z in lhs.items() if z]}

def crown(n, equations=False):
    vertices = list(product(range(2),range(n)))
    neighbors = [[j for j,v in enumerate(vertices) if u[0]!=v[0] and u[1]!=v[1]] for u in vertices]
    distances = []
    for x in range(2*n):
        d = {x:0}; queue=collections.deque([x])
        while queue:
            y=queue.popleft()
            for z in neighbors[y]:
                if z not in d: d[z]=d[y]+1;queue.append(z)
        require(len(d)==2*n and max(d.values())==3,'crown_connected_diameter_three')
        distances.append([d[y] for y in range(2*n)])
    P,Q,p,q,v = reconstruct(1,n-2,0)
    for x,y in product(range(2*n),repeat=2):
        observed = collections.Counter((distances[x][z],distances[y][z]) for z in range(2*n))
        for i,j in product(range(N),repeat=2):
            require(observed[i,j]==p[i][j][distances[x][y]],'crown_actual_intersection_numbers')
    require((0,1,2,3) in q_orders(q),'crown_Q_order')
    require(p[2][2][1]==p[2][2][3]==0,'crown_distance_two_mu_zero')
    require(p[3][3][1]==p[3][3][2]==0,'crown_distance_three_mu_zero')
    tested=0
    if equations:
        systems={}
        for x,y,z in permutations(range(2*n),3):
            tri=(distances[x][y],distances[x][z],distances[y][z])
            if tri not in systems: systems[tri]=equation_system((1,n-2,0),tri)[0]
            counts=collections.Counter((distances[x][w],distances[y][w],distances[z][w]) for w in range(2*n))
            for row,b in systems[tri]:
                require(sum(row.get(index,0)*count for index,count in counts.items())==b,'crown_actual_triple_equation')
            tested+=1
    return {'n':n,'ordered_distinct_base_triples_tested':tested}

def canonical_hash(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
    rows=sieve()
    survivors=[row for row in rows if not row['rejections']]
    require(len(rows)==959,'parameter_count_959')
    require(len(survivors)==159,'basic_survivors_159')
    require(canonical_hash(rows)==EXPECTED_ROW_HASH,'every_author_sieve_row_matches')
    certs=json.loads((ROOT/'TRIPLE_CERTIFICATES.json').read_text())
    require(len(certs)==5,'five_certificates')
    certificates=[certify(c) for c in certs]
    excluded={tuple(c['parameters']) for c in certificates}
    require(len(excluded)==5,'distinct_exclusions')
    require(excluded.issubset({(r['t'],r['c'],r['a']) for r in survivors}),'all_five_pass_basic_sieve')
    remaining=[r for r in survivors if (r['t'],r['c'],r['a']) not in excluded]
    require(len(remaining)==154,'remaining_154')
    controls=[]
    for name,mutator in [
        ('rhs_sign',lambda x:x.update(negative_rhs=str(-R(x['negative_rhs'])))),
        ('first_multiplier',lambda x:x['multipliers'][0].__setitem__(1,str(R(x['multipliers'][0][1])+1))),
        ('lhs_coefficient',lambda x:x['nonnegative_lhs'][0].__setitem__(1,str(R(x['nonnegative_lhs'][0][1])+1))),
        ('parameter',lambda x:x.update(a=x['a']+1)),
        ('triangle',lambda x:x.update(triangle=[1,1,1])),
        ('equation_count',lambda x:x.update(equation_count=x['equation_count']+1)),
    ]:
        altered=copy.deepcopy(certs[0]);mutator(altered)
        try: certify(altered)
        except (AssertionError,ZeroDivisionError): controls.append(name)
        else: raise AssertionError('mutation not rejected: '+name)
    P,Q,p,q,v=reconstruct(3,5,3)
    require(not q_orders(q),'wrong_relation_Q_control')
    crowns=[crown(n,equations=n<=5) for n in range(3,11)]
    require(all(row['t']>=4 and row['c']>=2 for row in remaining),'bounded_primitive_small_exclusions')
    result={'status':'PASS_SCOPED_PARTIALS','problem_id':2599,'problem_number':'KOU-21.90','general_connected_nondegenerate_problem':'unresolved','approaches_completed':5,'parameter_count':len(rows),'basic_survivors':len(survivors),'post_certificate_survivors':len(remaining),'all_sieve_rows_canonical_sha256':canonical_hash(rows),'sieve_survivors_after_certificates':remaining,'certificates':certificates,'crown_controls':crowns,'certificate_mutations_rejected':controls,'checks':dict(sorted(CHECKS.items())),'total_checks':sum(CHECKS.values()),'limitations':['Necessary-parameter sieve only, t <= 30.','No primitive graph is constructed.','Five certificates do not prove general nonexistence.','No novelty claim; no external paper proof imported as independently proved.']}
    encoded=json.dumps(result,indent=2)+'\n'
    (ROOT/'AUDIT_RESULTS.json').write_text(encoded)
    print(json.dumps({k:result[k] for k in ('status','parameter_count','basic_survivors','post_certificate_survivors','total_checks')},indent=2))

EXPECTED_ROW_HASH = 'b3d6584ebd23a4ab4053a1b2287b82bc2e267df26b57ecc48149e2c9ecd38a45'
if __name__=='__main__': main()
