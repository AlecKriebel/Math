#!/usr/bin/env python3
"""Exact finite certificate for the attributed DJS counterexample; Python stdlib only.
No network, file writes, floating point, external CAS, or source text are needed.
"""
from fractions import Fraction as Q
from itertools import permutations
import json

COUNT = 0

def check(ok, label):
    global COUNT
    COUNT += 1
    if not ok:
        raise AssertionError(label)

def rref(A, ncols=None):
    A = [[Q(x) for x in r] for r in A]
    n = len(A[0]) if A else (ncols or 0)
    lead, piv = 0, []
    for c in range(n):
        p = next((r for r in range(lead, len(A)) if A[r][c]), None)
        if p is None:
            continue
        A[lead], A[p] = A[p], A[lead]
        q = A[lead][c]
        A[lead] = [x/q for x in A[lead]]
        for r in range(len(A)):
            if r != lead:
                q = A[r][c]
                A[r] = [x-q*y for x, y in zip(A[r], A[lead])]
        piv.append(c)
        lead += 1
        if lead == len(A):
            break
    return A, piv

def rank(A):
    return len(rref(A)[1])

def kernel(A, n=3):
    R, p = rref(A, n)
    out = []
    for c in range(n):
        if c not in p:
            v = [Q(0)]*n
            v[c] = Q(1)
            for i, b in enumerate(p):
                v[b] = -R[i][c]
            out.append(v)
    return out

def eye(n=3):
    return [[Q(i == j) for j in range(n)] for i in range(n)]

def inv(A):
    n = len(A)
    R, p = rref([list(r)+s for r, s in zip(A, eye(n))])
    if p[:n] != list(range(n)):
        raise ValueError('singular matrix')
    return [r[n:] for r in R]

def matmul(A, B):
    return [[sum(a*b for a, b in zip(row, col)) for col in zip(*B)] for row in A]

def mv(A, v):
    return [sum(a*b for a, b in zip(row, v)) for row in A]

def det(A):
    return sum(((-1)**sum(p[i] > p[j] for i in range(3) for j in range(i+1, 3)))
               * A[0][p[0]]*A[1][p[1]]*A[2][p[2]] for p in permutations(range(3)))

def dot(a, b):
    return sum(x*y for x, y in zip(a, b))

def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))

def p_add(a, b):
    c = dict(a)
    for m, v in b.items():
        c[m] = c.get(m, Q(0))+v
        if not c[m]:
            del c[m]
    return c

def p_mul(a, b):
    c = {}
    for m, v in a.items():
        for n, w in b.items():
            c = p_add(c, {tuple(x+y for x, y in zip(m,n)):v*w})
    return c

def pmul(A, B):
    C = [[{} for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                C[i][j] = p_add(C[i][j], p_mul(A[i][k],B[k][j]))
    return C

def peye():
    return [[{(0,0):Q(1)} if i == j else {} for j in range(3)] for i in range(3)]

V = [(1,0),(0,1),(-1,-1)]
CONES = [(1,2),(0,2),(0,1)]
B = [
    [[1,0,0],[-1,1,0],[0,-1,1]],
    [[1,1,0],[0,-1,1],[0,0,-1]],
    eye(),
]
U = [
    [(-1,-2),(-2,0),(-2,3)],
    [(4,-3),(0,-3),(-1,-1)],
    [(4,-2),(0,0),(-1,3)],
]

def transition(i, j, bases=B, weights=U):
    C = matmul(inv(bases[i]),bases[j])
    return [[{sub(weights[i][a],weights[j][b]):C[a][b]} if C[a][b] else {}
             for b in range(3)] for a in range(3)]

def compatible(bases, weights):
    for i, j in permutations(range(3),2):
        ray = next(iter(set(CONES[i]) & set(CONES[j])))
        for row in transition(i,j,bases,weights):
            for p in row:
                if any(dot(m,V[ray]) < 0 for m in p):
                    return False
    return True

def weightspace(u, bases=B, weights=U):
    equations = []
    for i in range(3):
        A = inv(bases[i])
        for j in range(3):
            if any(dot(sub(weights[i][j],u),V[r]) < 0 for r in CONES[i]):
                equations.append(A[j])
    return kernel(equations)

def sections(bases=B, weights=U):
    # Every nonzero weight obeys dot(u,v_r) <= max local ray height.
    H = []
    for r in range(3):
        i = next(i for i in range(3) if r in CONES[i])
        H.append(max(dot(u,V[r]) for u in weights[i]))
    amin, bmin = -H[2]-H[1], -H[2]-H[0]
    out = []
    for a in range(amin,H[0]+1):
        for b in range(bmin,H[1]+1):
            if a+b >= -H[2]:
                for v in weightspace((a,b),bases,weights):
                    out.append(((a,b),v))
    return H, out

def jet_matrix(i, k, sec, bases=B, weights=U):
    labels = [(j,a,b) for j in range(3)
              for a in range(k+1) for b in range(k+1-a)]
    out = [[] for _ in labels]
    for u, v in sec:
        c = mv(inv(bases[i]),v)
        for n, (j,a,b) in enumerate(labels):
            exp = tuple(dot(sub(weights[i][j],u),V[r]) for r in CONES[i])
            out[n].append(c[j] if exp == (a,b) else Q(0))
    return labels, out

def restriction(i, j, r, tangent):
    # Boundary restriction removes positive normal order terms.
    G = transition(i,j)
    remaining = []
    for a in range(3):
        for b in range(3):
            for m, c in G[a][b].items():
                h = dot(m,V[r])
                check(h >= 0,'regular transition on invariant divisor')
                if h == 0:
                    assert tangent[0] or tangent[1]
                    k = next(m[t]//tangent[t] for t in range(2) if tangent[t])
                    check(m == tuple(k*x for x in tangent),'primitive curve coordinate')
                    remaining.append((a,b,k,int(c)))
    check(sorted(a for a,b,k,c in remaining) == [0,1,2], 'one term each restriction row')
    check(sorted(b for a,b,k,c in remaining) == [0,1,2], 'one term each restriction column')
    return remaining


def main():
    for base in B:
        check(abs(det(base)) == 1,'unimodular constant frame')
    for c in CONES:
        check(abs(V[c[0]][0]*V[c[1]][1]-V[c[0]][1]*V[c[1]][0]) == 1,'smooth maximal cone')
    check(compatible(B,U),'all six overlap transitions are regular')
    for i,j in permutations(range(3),2):
        check(pmul(transition(i,j),transition(j,i)) == peye(),'transition inverse')
    for i,j,k in permutations(range(3),3):
        check(pmul(transition(i,j),transition(j,k)) == transition(i,k),'cocycle')
    restrictions = [restriction(2,1,0,(0,1)), restriction(2,0,1,(1,0)), restriction(1,0,2,(1,-1))]
    degrees = [sorted([k for a,b,k,c in R],reverse=True) for R in restrictions]
    check(degrees == [[4,3,1],[5,2,1],[6,1,1]],'three exact splitting types')
    check(min(k for row in degrees for k in row) == 1,'tau equals one')
    H, sec = sections()
    check(H == [4,3,3],'global finite-support bounds')
    check(len(sec) == 12,'dimension H0 equals twelve')
    expected = {
        (3,-2):(1,0,0),(4,-3):(1,0,0),(4,-2):(1,0,0),
        (-1,-2):(-1,1,0),(0,-3):(-1,1,0),(0,-2):(-1,1,0),
        (-2,0):(0,-1,1),(-1,-1):(0,-1,1),(-1,0):(0,-1,1),
        (-2,3):(0,0,1),(-1,2):(0,0,1),(-1,3):(0,0,1),
    }
    check({u:tuple(v) for u,v in sec} == expected,'entire global section basis')
    check(weightspace((0,0)) == [],'weight zero is absent')
    value_ranks, jet_ranks = [], []
    for i in range(3):
        _,M = jet_matrix(i,0,sec);value_ranks.append(rank(M))
        _,M = jet_matrix(i,1,sec);jet_ranks.append(rank(M))
    check(value_ranks == [3,3,2],'all fixed-point value ranks')
    check(jet_ranks == [9,9,7],'all fixed-point first-jet ranks')
    labels,J = jet_matrix(2,1,sec)
    for label in [(1,0,0),(1,0,1)]:
        check(not any(J[labels.index(label)]),'missing e2 value and y derivative')
    # Direct filtration constraints at zero: first two permit e2, third rejects it.
    check(kernel([[0,0,1],[1,0,0]]) == [[Q(0),Q(1),Q(0)]], 'two-ray false positive control')
    check(kernel([[0,0,1],[1,0,0],[1,1,1]]) == [],'third ray eliminates false section')
    # Source-consistent polygon vertex and deliberate synthetic sign flip: heights (0,-2,3) force b <= -2.
    check(dot((-1,-2),V[1]) <= -2,'source vertex respects second ray')
    check(not (dot((-1,2),V[1]) <= -2),'synthetic sign flip violates filtration')
    negatives = []
    bad = [[tuple(u) for u in row] for row in U]
    bad[0][2] = (-2,4)
    check(not compatible(B,bad),'incompatible altered local weight rejected')
    negatives.append('altered local weight fails overlap regularity')
    # Three copies of O: globally generated and nef, but tau=0 and no first jets.
    idbases = [eye(),eye(),eye()]
    trivial = [[(0,0)]*3 for _ in range(3)]
    check(compatible(idbases,trivial),'trivial control glues')
    _,S0 = sections(idbases,trivial)
    check(len(S0) == 3,'trivial H0')
    for i in range(3):
        check(rank(jet_matrix(i,0,S0,idbases,trivial)[1]) == 3,'trivial values generated')
        check(rank(jet_matrix(i,1,S0,idbases,trivial)[1]) == 3,'trivial first jets fail')
    negatives.append('nef and globally generated do not alone imply first jets')
    # Three copies of O(D3) = O(1): a genuinely jet-spanned positive control.
    positive = [[(-1,0)]*3,[(0,-1)]*3,[(0,0)]*3]
    check(compatible(idbases,positive),'positive line-bundle control glues')
    _,S1 = sections(idbases,positive)
    check(len(S1) == 9,'O(1)^3 H0')
    for i in range(3):
        check(rank(jet_matrix(i,1,S1,idbases,positive)[1]) == 9,'O(1)^3 first jets generated')
    # O(-1)^3 provides a sign-sensitive negative control.
    negative = [[tuple(-z for z in u) for u in row] for row in positive]
    check(compatible(idbases,negative),'negative line-bundle control glues')
    _,SN = sections(idbases,negative)
    check(SN == [],'O(-1)^3 has no sections')
    negatives.append('line-bundle sign reversal destroys global sections')
    print(json.dumps({
        'schema':'toric-jets-exact-checks-v1',
        'arithmetic':'Python fractions.Fraction and integer Laurent monomials',
        'assertions':COUNT,
        'splitting_degrees':degrees,
        'tau':1,
        'global_section_dimension':12,
        'value_ranks':value_ranks,
        'first_jet_ranks':jet_ranks,
        'first_jet_target_dimension':9,
        'bad_point_missing_rows':['e2 value','e2 y derivative'],
        'positive_control':'O(1)^3 has first-jet rank 9 at all three fixed points',
        'negative_controls':negatives,
        'synthetic_polygon_sign_control':'Synthetic (-1,2) rejected; source-consistent (-1,-2) satisfies the e1-e2 second-ray bound',
        'scope':'Finite exact certificate. Geometric nefness and the full source implication are proved in PROOF.md, not inferred from finite tests.',
        'result':'PASS'
    },indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
