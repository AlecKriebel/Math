#!/usr/bin/env python3
"""Independent exact checks; polynomial convolution, incremental linear algebra.
No author code, third-party datasets, sources, or non-standard packages are read.
The all-rank result is a theorem audited separately, not a finite test claim.
"""
import json
from math import comb


def need(ok, message):
    if not ok:
        raise ValueError(message)


class Space:
    def __init__(self, p):
        self.p, self.rows = p, {}
    def add(self, vector):
        v = [x % self.p for x in vector]
        for pivot, row in sorted(self.rows.items()):
            c = v[pivot]
            if c:
                v = [(x-c*y) % self.p for x,y in zip(v,row)]
        pivot = next((i for i,x in enumerate(v) if x), None)
        if pivot is None:
            return False
        inv = pow(v[pivot], self.p-2, self.p)
        self.rows[pivot] = [(inv*x) % self.p for x in v]
        return True
    def rank(self):
        return len(self.rows)


def matrix_rank(rows, p):
    s = Space(p)
    for row in rows:
        s.add(row)
    return s.rank()


def polynomial_matrices(m, twist, p):
    # Repeated convolution of linear forms, independent of binomial expansion.
    # Key: (x degree, y degree, a,b,c,d degrees).
    n = m+1
    mats = {}
    for col in range(n):
        poly = {(0,0,0,0,0,0):1}
        factors = [[((1,0,1,0,0,0),1),((0,1,0,0,1,0),1)]]*(m-col)
        factors += [[((1,0,0,1,0,0),1),((0,1,0,0,0,1),1)]]*col
        factors += [[((0,0,1,0,0,1),1),((0,0,0,1,1,0),-1)]]*twist
        for factor in factors:
            new = {}
            for left, a in poly.items():
                for right, b in factor:
                    k = tuple(x+y for x,y in zip(left,right))
                    new[k] = (new.get(k,0)+a*b) % p
            poly = {k:v for k,v in new.items() if v}
        for key, value in poly.items():
            x,y,*exponent = key
            need(x+y == m, 'wrong polynomial degree')
            mat = mats.setdefault(tuple(exponent),[[0]*n for _ in range(n)])
            mat[y][col] = value
    return list(mats.values())


def flatten(a):
    return sum(a,[])


def multiply(a,b,p):
    return [[sum(x*y for x,y in zip(row,col)) % p for col in zip(*b)] for row in a]


def algebra_dimension(generators, p):
    n = len(generators[0]); identity = [[int(i==j) for j in range(n)] for i in range(n)]
    s, queue = Space(p), [identity]
    s.add(flatten(identity))
    pos = 0
    while pos < len(queue):
        a = queue[pos];pos += 1
        for g in generators:
            b = multiply(g,a,p)
            if s.add(flatten(b)):
                queue.append(b)
    return s.rank()


def commute_dimension(generators, p):
    n = len(generators[0]); eq = []
    for g in generators:
        # Columns are flattened commutators with the matrix-unit basis.
        columns=[]
        for a in range(n):
            for b in range(n):
                e=[[int(i==a and j==b) for j in range(n)] for i in range(n)]
                ge,eg=multiply(g,e,p),multiply(e,g,p)
                columns.append([x-y for x,y in zip(flatten(ge),flatten(eg))])
        eq += [list(row) for row in zip(*columns)]
    return n*n-matrix_rank(eq,p)


def extension_ranks(generators, p):
    # Reorder to (socle,quotient). An equivariant section has matrix (X;1).
    w,q=[0,3],[1,2]
    left,right=[],[]
    for g in generators:
        a=[[g[i][j] for j in w] for i in w]
        b=[[g[i][j] for j in q] for i in w]
        d=[[g[i][j] for j in q] for i in q]
        columns=[]
        for i in range(2):
            for j in range(2):
                e=[[int(k==i and l==j) for l in range(2)] for k in range(2)]
                ae,ed=multiply(a,e,p),multiply(e,d,p)
                columns.append([x-y for x,y in zip(flatten(ae),flatten(ed))])
        left += [list(row) for row in zip(*columns)]
        right += [-x for x in flatten(b)]
    return [matrix_rank(left,p),matrix_rank([row+[b] for row,b in zip(left,right)],p)]


def augmentation_generators(r,p):
    out=[]
    for s in range(r-1):
        perm=list(range(r));perm[s:s+2]=[s+1,s]
        a=[]
        for i in range(r-1):
            a.append([(int(i==perm[j])-int(i==perm[r-1])) % p for j in range(r-1)])
        out.append(a)
    return out


def main():
    p=3
    s5=polynomial_matrices(5,0,p)
    d3=polynomial_matrices(3,1,p)
    ranks=[matrix_rank([flatten(x) for x in ms],p) for ms in (s5,d3)]
    need(ranks==[36,12], 'polynomial coefficient spans differ')
    need(all(g[i][j]==0 for g in d3 for i in [1,2] for j in [0,3]),'socle not invariant')
    constituent_ranks=[]
    for coords in ([0,3],[1,2]):
        constituent_ranks.append(matrix_rank([flatten([[g[i][j] for j in coords] for i in coords]) for g in d3],p))
    need(constituent_ranks==[4,4], 'constituents not absolutely simple')
    splitting=extension_ranks(d3,p)
    need(splitting==[4,5], 'nonsplit extension test differs')
    end=commute_dimension(d3,p);need(end==1,'commutant is not scalar')
    augmentation=algebra_dimension(augmentation_generators(5,3),3)
    need(augmentation==16,'augmentation is not absolutely simple')
    dividing_control=algebra_dimension(augmentation_generators(3,3),3)
    need(dividing_control<4,'p-dividing-r negative control failed')
    family=[]
    for prime in [3,5,7,11,13,17,19,23,29,31]:
        support=[i for i in range(2*prime) if comb(2*prime-1,i)%prime]
        socle=[i for i in range(2*prime-2) if comb(2*prime-3,i)%prime]
        want=list(range(prime-2))+list(range(prime,2*prime-2))
        need(support==list(range(2*prime)), 'full-support binomial test failed')
        need(socle==want, 'socle support failed')
        family.append({'p':prime,'sym_r_dimension':len(support),'socle_dimension':len(socle),'quotient_dimension':2})
    print(json.dumps({'status':'PASS','coefficient_span_ranks':ranks,'constituent_span_ranks':constituent_ranks,
        'extension_ranks':splitting,'endomorphism_dimension':end,
        'augmentation_generated_algebra_dimension':augmentation,
        'p_divides_r_control_algebra_dimension':dividing_control,'finite_family_support_checks':family,
        'scope':'Finite exact checks. The all-odd-prime and all-rank assertions are proved in the authored mathematical audit.'},sort_keys=True,indent=2))

if __name__=='__main__':
    main()
