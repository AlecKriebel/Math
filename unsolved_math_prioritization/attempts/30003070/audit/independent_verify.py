#!/usr/bin/env python3
"""Independent exact finite controls for an explicitly unsolved research packet.
Standard library only. No imports of author code, network access, or assert statements.
Finite experiments supplement the written all-degree proof audit; they do not prove
any universal plabic realization theorem. Output is deterministic in all Python modes.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, permutations, product
from math import comb, factorial
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

COUNT = 0
PINNED_MANIFEST = '6dc7b5dc2209ed8ef3285b4b7da123df2285d328236b907fd7bad4ff17098c9e'
PINNED_ARCHIVE = '4ae7e2309f630c0008eed27ebdc297dee0817e23669eae5f5cefa35e595013fe'

def need(condition, why):
    global COUNT
    COUNT += 1
    if not condition:
        raise ValueError(why)


def determinant(M):
    """Fraction-free Bareiss elimination, distinct from author rational elimination."""
    A = [list(row) for row in M]
    n = len(A)
    if any(len(row) != n for row in A):
        raise ValueError('nonsquare matrix')
    if n == 0:
        return 1
    sign, last = 1, 1
    for k in range(n-1):
        if A[k][k] == 0:
            pivot = next((j for j in range(k+1,n) if A[j][k]), None)
            if pivot is None:
                return 0
            A[k], A[pivot] = A[pivot], A[k]
            sign = -sign
        pivot = A[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                num = A[i][j]*pivot-A[i][k]*A[k][j]
                if isinstance(num, int) and isinstance(last, int):
                    if num % last:
                        raise ValueError('nonexact Bareiss division')
                    A[i][j] = num//last
                else:
                    A[i][j] = F(num)/last
            A[i][k] = 0
        last = pivot
    return sign*A[-1][-1]


def inverse(M):
    n = len(M)
    A = [[F(x) for x in row]+[F(i==j) for j in range(n)] for i,row in enumerate(M)]
    for k in range(n):
        p = next((j for j in range(k,n) if A[j][k]), None)
        if p is None:
            raise ValueError('singular inverse')
        A[k],A[p] = A[p],A[k]
        v = A[k][k]
        A[k] = [x/v for x in A[k]]
        for i in range(n):
            if i != k:
                v = A[i][k]
                A[i] = [x-v*y for x,y in zip(A[i],A[k])]
    return [row[n:] for row in A]


def mv(M,v):
    return tuple(sum(a*b for a,b in zip(row,v)) for row in M)


def padd(P,Q,scale=1):
    ans = dict(P)
    for e,c in Q.items():
        ans[e] = ans.get(e,0)+scale*c
        if not ans[e]:
            del ans[e]
    return ans


def pmul(P,Q):
    ans = {}
    for e,c in P.items():
        for f,d in Q.items():
            a = tuple(x+y for x,y in zip(e,f))
            ans[a] = ans.get(a,0)+c*d
    return {a:c for a,c in ans.items() if c}


def ppow(P,r,d):
    out = {(0,)*d:1}
    for _ in range(r):
        out = pmul(out,P)
    return out


def monomial(d,index):
    e = [0]*d
    e[index] = 1
    return {tuple(e):1}


def signed_perms(k):
    for p in permutations(range(k)):
        inversions = sum(p[i]>p[j] for i in range(k) for j in range(i+1,k))
        yield p,(-1)**inversions


def matrix_chart(k,n,sequence):
    """Independent implementation through n-by-k matrices and their determinants."""
    d = len(sequence)
    A = [[{(0,)*d:1} if i==j else {} for j in range(k)] for i in range(n)]
    for position in reversed(range(d)):
        i,j = sequence[position]
        t = monomial(d,position)
        A[j-1] = [padd(x,pmul(t,y)) for x,y in zip(A[j-1],A[i-1])]
    minors = {}
    for rows in combinations(range(n),k):
        q = {}
        for perm,sign in signed_perms(k):
            term = {(0,)*d:1}
            for i,col in enumerate(perm):
                term = pmul(term,A[rows[i]][col])
            q = padd(q,term,sign)
        minors[tuple(i+1 for i in rows)] = q
    return A,minors


def root_controls():
    cases = [
        (2,4,[(1,3),(1,4),(2,3),(2,4)]),
        (3,6,[(1,6),(4,6),(5,6),(1,5),(2,5),(4,5),(1,4),(2,4),(3,4)]),
        # Repeated (2,3) root; inverse checked separately below.
        (2,4,[(2,3),(1,2),(3,4),(2,3)]),
    ]
    reports = []
    for k,n,S in cases:
        d = len(S)
        A,P = matrix_chart(k,n,S)
        need(d==k*(n-k), 'chart dimension')
        need(P[tuple(range(1,k+1))]=={(0,)*d:1}, 'reference determinant')
        terms = 0
        for I,p in P.items():
            need(bool(p), 'identically vanishing Plucker coordinate')
            for a in p:
                terms += 1
                need(all(x in (0,1) for x in a), 'nonmultiaffine minor')
                weight = tuple(sum(a[h]*((j==i)-(j==l)) for h,(i,l) in enumerate(S)) for j in range(1,n+1))
                need(weight==tuple((j<=k)-(j in I) for j in range(1,n+1)), 'weight mismatch')
                need(sum(a[h]*(l-i) for h,(i,l) in enumerate(S))==sum(I)-k*(k+1)//2, 'height mismatch')
        # Fully expand products in degrees 2 and 3, including all coefficient cancellation.
        product_counts = []
        for r in (2,3):
            products = []
            for chosen in combinations_with_replacement(list(P),r):
                p = {(0,)*d:1}
                for I in chosen:
                    p = pmul(p,P[I])
                need(all(all(0<=x<=r for x in a) for a in p), 'higher-degree box escape')
                products.append(p)
            combined = {}
            for h,p in enumerate(products):
                combined = padd(combined,p,(-1)**h)
            need(all(all(0<=x<=r for x in a) for a in combined), 'sum box escape')
            product_counts.append([r,len(products)])
        reports.append({'k':k,'n':n,'repeated_roots':len(set(S))<d,'plucker_coordinates':len(P),
                        'nonzero_terms':terms,'expanded_products':product_counts})
    # Every ordering of the Gr(2,4) PBW roots remains the same canonical matrix
    # after identifying parameter positions with their root labels.
    checked = 0
    for S in permutations(cases[0][2]):
        A,_ = matrix_chart(2,4,S)
        for position,(i,j) in enumerate(S):
            need(A[j-1][i-1]==monomial(4,position), 'PBW row coordinate mismatch')
        checked += 1
    # Repeated-root chart canonical lower block = (-bd,a+d;-bcd,cd).
    repeated_inverse = 0
    for a,b,c,d in product(range(1,4),repeat=4):
        u,v,w,z = -b*d,a+d,-b*c*d,c*d
        bb,dd,cc = -F(w,z),F(u*z,w),F(w,u)
        aa = v-dd
        need((aa,bb,cc,dd)==(a,b,c,d), 'repeated-root rational inverse')
        repeated_inverse += 1
    # Row extension for every row subset of exact Vandermonde representatives.
    extensions = 0
    for k in (1,2,3):
        for n in range(k+1,7):
            A = [[i**j for j in range(k)] for i in range(1,n+1)]
            for rows in combinations(range(n),k):
                B = [A[i] for i in rows]
                need(determinant(B)!=0, 'chosen row minor is zero')
                z = [F((-1)**j*(j+2),j+1) for j in range(k)]
                inv = inverse(B)
                y = [sum(z[j]*inv[j][h] for j in range(k)) for h in range(k)]
                need([sum(y[h]*B[h][j] for h in range(k)) for j in range(k)]==z,
                     'row-extension inverse mismatch')
                extensions += 1
    return {'charts':reports,'PBW_orderings':checked,'repeated_root_inverse_samples':repeated_inverse,
            'row_extension_samples':extensions}


def semigroup_controls():
    q = [{(0,0,0,0):1},{(0,1,0,0):1},{(0,0,0,1):1},
         {(1,0,0,0):1},{(0,0,1,0):1},{(0,1,1,0):1,(1,0,0,1):-1}]
    values = [min(p) for p in q]
    degree_counts, normal_total = [],0
    for r in range(15):
        distinct = set()
        for chosen in combinations_with_replacement(range(6),r):
            m = Counter(chosen)
            if m[0] and m[5]:
                continue
            leading = tuple(sum(values[i][j] for i in chosen) for j in range(4))
            need(leading not in distinct, 'normal-value collision')
            distinct.add(leading)
            # Independently reconstruct full (bc-ad)^m5 coefficient expansion.
            p = {}
            for j in range(m[5]+1):
                exponent = (m[3]+j,m[1]+m[5]-j,m[4]+m[5]-j,m[2]+j)
                p[exponent] = (-1)**j*comb(m[5],j)
            need(min(p)==leading, 'binomial leading exponent')
            need(all(max(a,default=0)<=r for a in p), 'normal product degree bound')
        h = (r+1)*(r+2)**2*(r+3)//12
        need(len(distinct)==h==comb(r+5,5)-(comb(r+3,5) if r>=2 else 0), 'Hilbert count')
        degree_counts.append([r,len(distinct)])
        normal_total += len(distinct)
    # Row reduction obtains every possible leading term of the whole vector space,
    # including those exposed by cancellations; not just generator leading terms.
    span_checks = []
    for r in range(6):
        echelon = {}
        semigroup_values = set()
        for chosen in combinations_with_replacement(range(6),r):
            p = {(0,0,0,0):F(1)}
            for i in chosen:
                p = pmul(p,q[i])
            semigroup_values.add(tuple(sum(values[i][j] for i in chosen) for j in range(4)))
            while p:
                pivot = min(p)
                if pivot not in echelon:
                    coeff = p[pivot]
                    echelon[pivot] = {a:F(c)/coeff for a,c in p.items()}
                    break
                p = padd(p,echelon[pivot],-p[pivot])
        need(set(echelon)==semigroup_values, 'full span exposes new nongenerator values')
        need(len(echelon)==(r+1)*(r+2)**2*(r+3)//12, 'whole-space rank')
        span_checks.append([r,len(echelon)])
    relation = padd(padd(pmul(q[0],q[5]),pmul(q[1],q[4]),-1),pmul(q[2],q[3]))
    need(relation=={}, 'Plucker relation')
    cancellation = padd(q[5],pmul(q[1],q[4]),-1)
    need(cancellation=={(1,0,0,1):-1}, 'Plucker cancellation control')
    # Birational-but-nonmonomial transport failure.
    y1 = {(1,0):1}; y2 = {(1,0):1,(1,1):1}
    need(min(y1)==min(y2), 'chart leading collision')
    need(min(padd(y2,y1,-1))==(1,1), 'chart cancellation exposed term')
    # Positive compatible monomial transport on Laurent supports, including negatives.
    M = ((1,0),(2,1))
    need(determinant(M)==1, 'transport unimodularity')
    samples = 0
    points = list(product(range(-3,4),repeat=2))
    for a,b in combinations(points,2):
        need((a<b)==(mv(M,a)<mv(M,b)), 'transport order compatibility')
        need(min(mv(M,a),mv(M,b))==mv(M,min(a,b)), 'transport minimum')
        samples += 1
    return {'normal_monomials':normal_total,'degree_counts':degree_counts,
            'full_vector_space_echelon':span_checks,'monomial_transport_pairs':samples}


MU = ((3,3,3),(3,3,2),(2,2,2),(1,1,1),(3,3,0),(2,1,0),(1,1,0),(3,0,0),(2,0,0))
U = ((0,1,0,0,-1,-1,0,0,1),(0,0,0,0,1,0,0,-1,-1),
     (0,1,-1,0,0,-1,1,0,0),(0,0,1,0,0,-1,-1,0,0),
     (0,0,0,0,0,1,0,0,-1),(0,0,1,-1,0,0,-1,0,0),
     (0,0,0,1,0,0,-1,0,0),(1,-1,0,0,0,0,0,0,0),
     (0,0,0,0,0,-1,1,0,1))
C = tuple(F(i,2) for i in (3,3,2,1,2,1,1,1,1))


def cube_controls(mu=MU,matrix=U,vertex=C):
    def boxes(lam):
        return {(r,c) for r in range(1,4) for c in range(1,lam[r-1]+1)}
    def entry(m,lam):
        skew = boxes(m)-boxes(lam)
        # Enumerate complete NW-SE diagonals rather than count stored differences.
        return max((sum(r-c==d for r,c in skew) for d in range(-2,3)),default=0)
    partitions = sorted((c-3,b-2,a-1) for a,b,c in combinations(range(1,7),3))
    V = [tuple(entry(m,lam) for m in mu) for lam in partitions]
    need(len(set(V))==20, 'twenty distinct diagram valuations')
    need(determinant(matrix)==1, 'cube determinant not one')
    inv = inverse(matrix)
    need(all(x.denominator==1 for row in inv for x in row), 'cube inverse not integral')
    for col in range(9):
        need(mv(matrix,[inv[row][col] for row in range(9)])==tuple(int(i==col) for i in range(9)),
             'cube inverse verification')
    transformed = [mv(matrix,v) for v in V]
    for v in transformed:
        need(set(v)<=set((0,1)), 'integer vertex outside unit cube')
    vc = mv(matrix,vertex)
    need(vc==tuple(F(i,2) for i in (1,0,1,0,0,0,0,0,1)), 'extra vertex transformed incorrectly')
    w = (0,-1,1,0,1,0,-1,0,-1)
    scalar = lambda a,b:sum(x*y for x,y in zip(a,b))
    need({scalar(w,v) for v in V}=={0,1}, 'separator integer values')
    need(scalar(w,vertex)==F(-1,2), 'separator misses extra vertex')
    columns = (0,1,2,3,4,5,9,10,16)
    need(determinant([[V[j][i] for j in columns] for i in range(9)])==-1, 'ambient lattice basis')
    return {'degree_one_points':len(V),'cube_determinant':determinant(matrix),
            'cube_inverse':[[int(x) for x in row] for row in inv],
            'transformed_points':[list(v) for v in transformed],
            'extra_vertex_image':[str(x) for x in vc],'separator_value':str(scalar(w,vertex))}


def braid_controls():
    # Rational functions as polynomial numerator/denominator pairs; equality by cross product.
    one = {(0,0,0):1}; zero = {}
    def add(x,y):return padd(pmul(x[0],y[1]),pmul(y[0],x[1])),pmul(x[1],y[1])
    def mul(x,y):return pmul(x[0],y[0]),pmul(x[1],y[1])
    def eq(x,y):return pmul(x[0],y[1])==pmul(y[0],x[1])
    def mm(A,B):
        rows=[]
        for i in range(3):
            row=[]
            for k in range(3):
                cell=(zero,one)
                for j in range(3):cell=add(cell,mul(A[i][j],B[j][k]))
                row.append(cell)
            rows.append(row)
        return rows
    def root(i,t):
        M=[[(one if j==k else zero,one) for k in range(3)] for j in range(3)]
        M[i][i-1]=t
        return M
    a,b,c = [monomial(3,i) for i in range(3)]
    den = padd(a,c)
    lhs=mm(mm(root(1,(a,one)),root(2,(b,one))),root(1,(c,one)))
    rhs=mm(mm(root(2,(pmul(b,c),den)),root(1,(den,one))),root(2,(pmul(a,b),den)))
    for i,j in product(range(3),repeat=2):need(eq(lhs[i][j],rhs[i][j]), 'symbolic braid matrix identity')
    left=((-1,1,1),(1,0,0),(0,1,0));right=((0,1,0),(0,0,1),(1,1,-1))
    need(determinant(left)==determinant(right)==1, 'tropical chamber determinant')
    def tau(v):
        a,b,c=v;m=min(a,c)
        return b+c-m,m,a+b-m
    total=0
    for v in product(range(-5,6),repeat=3):
        M=left if v[0]<=v[2] else right
        need(mv(M,v)==tau(v), 'chamber formula')
        need(tau(tau(v))==v, 'tropical inverse')
        total+=1
    p=(1,1,2);q=(2,1,1)
    image_sum=tau(tuple(a+b for a,b in zip(p,q)))
    sum_images=tuple(a+b for a,b in zip(tau(p),tau(q)))
    need(image_sum==(2,3,2) and sum_images==(3,2,3) and image_sum!=sum_images, 'nonlinearity witness')
    return {'symbolic_matrix_entries':9,'tropical_lattice_points':total,
            'sum_of_images':sum_images,'image_of_sum':image_sum,
            'rational_inverse_dense_open':'a+c != 0 and b != 0'}


def freeze_controls(author,archive):
    mpath=author/'MANIFEST.json'
    need(not mpath.is_symlink(), 'manifest symlink')
    need(hashlib.sha256(mpath.read_bytes()).hexdigest()==PINNED_MANIFEST, 'frozen manifest pin')
    metadata=json.loads(mpath.read_text())
    need(metadata['problem_id']=='30003070','target identity')
    members={x['name']:x for x in metadata['files']}
    need(len(members)==10==len(metadata['files']), 'manifest duplicates or count')
    need(set(x.name for x in author.iterdir())==set(members)|{'MANIFEST.json'}, 'freeze inventory')
    for p in author.iterdir():
        need(p.is_file() and not p.is_symlink(), 'nonregular freeze member')
        if p.name!='MANIFEST.json':
            b=p.read_bytes();e=members[p.name]
            need(len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'], 'frozen member digest')
    b=archive.read_bytes()
    need(len(b)==24377 and hashlib.sha256(b).hexdigest()==PINNED_ARCHIVE,'frozen archive pin')
    with zipfile.ZipFile(archive) as z:
        names=z.namelist()
        need(len(names)==len(set(names))==11,'archive duplicate/member count')
        need(set(names)==set(members)|{'MANIFEST.json'},'archive inventory')
        for name in names:need(z.read(name)==(author/name).read_bytes(),'archive differs from frozen tree')
    status=json.loads((author/'STATUS.json').read_text())
    need(status['status']=='unsolved' and status['approaches_used']==status['approach_limit']==5,'scope mismatch')
    for flag in ('full_solution','full_counterexample','verified_full_prior_resolution','novelty_claim','global_current_openness_claim','remote_changes_performed'):
        need(status[flag] is False,'unsupported status '+flag)
    return {'members':11,'manifest_sha256':PINNED_MANIFEST,'archive_bytes':len(b),'archive_sha256':PINNED_ARCHIVE}


def source_controls(author,sources):
    data=json.loads((author/'SOURCE_VERIFICATION.json').read_text())
    report=[]
    for s in data['sources']:
        p=sources/s['filename_for_optional_private_verification']
        b=p.read_bytes()
        need(b.startswith(b'%PDF-'), 'not a PDF')
        need(len(b)==s['bytes'],'source byte length')
        sha=hashlib.sha256(b).hexdigest()
        need(sha==s['sha256'],'source SHA256')
        report.append({'id':s['id'],'bytes':len(b),'sha256':sha,'match':True})
    need(len(report)==6,'source count')
    return report


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--author-dir',type=Path)
    parser.add_argument('--archive',type=Path)
    parser.add_argument('--source-dir',type=Path)
    args=parser.parse_args()
    result={'disposition':'unsolved; five approaches; finite checks supplement audited proofs',
            'roots':root_controls(),'semigroup':semigroup_controls(),
            'cube':cube_controls(),'braid':braid_controls()}
    if bool(args.author_dir)!=bool(args.archive):raise ValueError('author directory and archive must be paired')
    if args.author_dir:result['freeze']=freeze_controls(args.author_dir,args.archive)
    if args.source_dir:
        if not args.author_dir:raise ValueError('source check needs author metadata')
        result['sources']=source_controls(args.author_dir,args.source_dir)
    result['checks']=COUNT
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
