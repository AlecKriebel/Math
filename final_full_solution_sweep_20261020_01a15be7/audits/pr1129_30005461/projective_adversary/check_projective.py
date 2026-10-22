"""Finite exact interface checks. Not an SOS certificate or theorem prover."""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb, gcd
import json

class CheckFailure(ValueError):
    pass

def require(condition, message):
    if not condition:
        raise CheckFailure(message)

def rank(a):
    if not a:
        return 0
    b = [[Q(x) for x in r] for r in a]
    nr, nc, piv = len(b), len(b[0]), 0
    for col in range(nc):
        row = next((i for i in range(piv, nr) if b[i][col]), None)
        if row is None:
            continue
        b[piv], b[row] = b[row], b[piv]
        v = b[piv][col]
        b[piv] = [x/v for x in b[piv]]
        for i in range(nr):
            if i != piv and b[i][col]:
                v = b[i][col]
                b[i] = [x-v*y for x,y in zip(b[i], b[piv])]
        piv += 1
        if piv == nr:
            break
    return piv

def exponents(n, d):
    if n == 1:
        yield (d,)
        return
    for a in range(d+1):
        for tail in exponents(n-1, d-a):
            yield (a,)+tail

def image(e, mapping):
    return tuple(sum(e[j]*mapping[j][i] for j in range(4)) for i in range(3))

def check_mapping(mapping):
    require(len(mapping) == 4 and all(len(v) == 3 for v in mapping), 'map shape')
    require(all(type(x) is int and x >= 0 for v in mapping for x in v), 'map exponents')
    require(all(sum(v) == 3 for v in mapping), 'map is not cubic')
    require(image((1,1,1,0), mapping) == image((0,0,0,3), mapping), 'ABC-D^3 does not vanish')
    require(image((2,0,0,0),mapping) == (4,2,0), 'A square wrong')
    require(image((0,2,0,0),mapping) == (2,4,0), 'B square wrong')
    require(image((0,0,2,0),mapping) == (0,0,6), 'C square wrong')
    require(image((0,0,0,2),mapping) == (2,2,2), 'D square wrong')
    require(rank(list(zip(*mapping))) == 3, 'map rank is not three')

def check_bookkeeping(N, root_degree):
    require(type(N) is int and N >= 0 and N % 2 == 0, 'N must be even')
    m = N+1
    require(m % 2 == 1, 'power is not odd')
    require(root_degree == m, 'global root degree wrong')
    require(2*root_degree == 2*m, 'squared section degree wrong')
    return m

def qvalue(a,b,c,d,t):
    return a*a+b*b+c*c-t*d*d

def run_math():
    mapping = ((2,1,0),(1,2,0),(0,0,3),(1,1,1))
    check_mapping(mapping)
    counts = {'signed_q_values':0,'boundary_q_values':0,'chart_sign_checks':0,
              'root_monomials':0,'relation_multiples':0,'hilbert_degrees':0,
              'cech_support_patterns':0,'parity_cases':0,'adverse_controls':0}
    v=(1,1,1,-3)
    require(gcd(gcd(v[0],v[1]),gcd(v[2],v[3])) == 1, 'kernel vector not primitive')
    require(all(sum(v[j]*mapping[j][i] for j in range(4)) == 0 for i in range(3)), 'kernel vector wrong')
    vals=[Q(s)*a for s in [-1,1] for a in [Q(1,3),Q(1),Q(2),Q(5)]]
    cs=[Q(-7),Q(-1,2),Q(0),Q(1),Q(2),Q(2999,1000)]
    for a,b,t,scale in product(vals,vals,cs,[Q(1),Q(-2)]):
        c=1/(a*b)
        A,B,C,D=[scale*x for x in [a,b,c,Q(1)]]
        require(A*B*C == D**3, 'signed chart off surface')
        q=qvalue(A,B,C,D,t)
        require(q >= (3-t)*D*D and q > 0, 'signed positivity failed')
        counts['signed_q_values']+=1
        for T in [A,B,C,D]:
            if T:
                require(q/(T*T) > 0, 'square trivialization sign failed')
                counts['chart_sign_checks']+=1
    for A,B,C in product(range(-2,3),repeat=3):
        if (A or B or C) and A*B*C == 0:
            for t in cs:
                require(qvalue(A,B,C,0,t) > 0, 'boundary positivity failed')
                counts['boundary_q_values']+=1
    require(qvalue(1,1,1,1,Q(3)) == 0, 'endpoint must fail strict positivity')
    require(qvalue(1,1,1,1,Q(3001,1000)) < 0, 'above cutoff negative witness missing')
    singular=[]
    for A,B,C,D in product(range(-1,2),repeat=4):
        if not (A or B or C or D):
            continue
        if A*B*C == D**3 and (B*C,A*C,A*B,-3*D*D)==(0,0,0,0):
            require(D==0 and sum(x != 0 for x in [A,B,C])==1, 'unexpected singular sample')
            singular.append((A,B,C,D))
    require(len(singular)==6,'three real projective singular vertices not witnessed')
    for m in range(31):
        normal=sum(1 for A,B,C,D in exponents(4,m) if not(A and B and C))
        expected=comb(m+3,3)-(comb(m,3) if m>=3 else 0)
        require(normal==expected,'hypersurface Hilbert count mismatch')
        counts['hilbert_degrees']+=1
        if m<=18:
            for e in exponents(4,m):
                require(sum(image(e,mapping))==3*m,'substituted degree mismatch')
                counts['root_monomials']+=1
                lhs=image(tuple(e[i]+[1,1,1,0][i] for i in range(4)),mapping)
                rhs=image(tuple(e[i]+[0,0,0,3][i] for i in range(4)),mapping)
                require(lhs==rhs,'multiple of relation survives substitution')
                counts['relation_multiples']+=1
    for N in range(0,102,2):
        m=check_bookkeeping(N,N+1)
        require(m+2==N+3,'odd successor failed')
        counts['parity_cases']+=1
    # Exact Cech matrices: one weight's negative-exponent index set determines it.
    for mask in range(16):
        neg={i for i in range(4) if mask & (1<<i)}
        terms=[[I for I in combinations(range(4),q+1) if neg.issubset(I)] for q in range(4)]
        ds=[]
        for q in range(3):
            mat=[]
            for J in terms[q+1]:
                row=[]
                for I in terms[q]:
                    row.append(sum((-1)**i for i in range(len(J)) if J[:i]+J[i+1:]==I))
                mat.append(row)
            ds.append(mat)
        ranks=[rank(d) for d in ds]
        for q in [1,2]:
            require(len(terms[q])-ranks[q-1]-ranks[q]==0,'intermediate Cech cohomology nonzero')
        h0=len(terms[0])-ranks[0]
        h3=len(terms[3])-ranks[2]
        require(h0==int(not neg) and h3==int(len(neg)==4),'end Cech cohomology mismatch')
        for q in [0,1]:
            for row in ds[q+1]:
                for j in range(len(terms[q])):
                    require(sum(row[k]*ds[q][k][j] for k in range(len(terms[q+1])))==0,'Cech d squared nonzero')
        counts['cech_support_patterns']+=1
    wrong_maps=[((2,1,0),(1,2,0),(0,0,3),(1,1,0)),
                ((2,1,0),(1,2,0),(0,0,2),(1,1,1)),
                ((1,2,0),(2,1,0),(0,0,3),(1,1,1))]
    for bad in wrong_maps:
        try:
            check_mapping(bad)
        except CheckFailure:
            counts['adverse_controls']+=1
        else:
            raise CheckFailure('wrong mapping control accepted')
    for N,degree in [(1,2),(3,4),(2,2),(4,6)]:
        try:
            check_bookkeeping(N,degree)
        except CheckFailure:
            counts['adverse_controls']+=1
        else:
            raise CheckFailure('bad parity/degree control accepted')
    # Wrong q sign disagrees already at an exact surface point.
    require(qvalue(1,1,1,1,Q(2)) != 1+1+1+2,'coefficient-sign mutation undetected')
    counts['adverse_controls']+=1
    require(counts['adverse_controls']==8,'adverse-control count changed')
    return {'status':'pass','scope':'finite exact interfaces only; universal proof is written in REVIEW.md',
            'counts':counts,'singular_representatives':singular}

if __name__=='__main__':
    print(json.dumps(run_math(),sort_keys=True))
