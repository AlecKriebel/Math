#!/usr/bin/env python3
"""Independent integer-lattice, symbolic, and finite-rank audit.

Builds the full list of quadratic generator types in the monomial lattice.
Smith normal form certifies that the degree-two relation subgroup is saturated.
This is independent of the producer's modular RREF quotient implementation.
"""
from itertools import combinations, combinations_with_replacement, permutations
from pathlib import Path
import argparse
import hashlib, json
import sympy as s
from sympy.matrices.normalforms import smith_normal_form


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def setup(n):
    mons = list(combinations_with_replacement(range(2*n), 2))
    ix = {m:k for k,m in enumerate(mons)}
    def mono(i,j):
        return ix[tuple(sorted((i,j)))]
    relations = []
    for i,j in combinations(range(n),2):
        relations.append({mono(i,j):1})
    for i,j in combinations_with_replacement(range(n),2):
        relations.append({mono(n+i,n+j):1})
    for i in range(n):
        relations.append({mono(i,n+i):1})
        for j,k in combinations([j for j in range(n) if j!=i],2):
            relations.append({mono(i,n+j):1,mono(i,n+k):-1})
    G = s.zeros(len(relations),len(mons))
    for r,row in enumerate(relations):
        for c,v in row.items():G[r,c]=v
    d2 = 1 if n==1 else 2*n
    P = s.zeros(d2,len(mons))
    for k,(i,j) in enumerate(mons):
        if i==j and i<n:P[i,k]=1
        elif i<n<=j and j-n!=i:P[n+i,k]=1
    require(P*G.T==s.zeros(d2,len(relations)), 'Independent check failed: P*G.T==s.zeros(d2,len(relations))')
    require(P.rank()==d2, 'Independent check failed: P.rank()==d2')
    return mons,G,P


def mult(mons,P,coeff):
    B=s.zeros(len(mons),len(coeff))
    for k,(i,j) in enumerate(mons):
        B[k,i]+=coeff[j]
        if j!=i:B[k,j]+=coeff[i]
    return P*B


def modrank(M,p):
    a=[[int(x)%p for x in row] for row in M.tolist()]
    r=0
    for c in range(M.cols):
        found=next((i for i in range(r,M.rows) if a[i][c]),None)
        if found is None:continue
        a[found],a[r]=a[r],a[found]
        f=pow(a[r][c],-1,p)
        a[r]=[(x*f)%p for x in a[r]]
        for i in range(r+1,M.rows):
            f=a[i][c]
            a[i]=[(x-f*y)%p for x,y in zip(a[i],a[r])]
        r+=1
        if r==M.rows:break
    return r


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Also create a new JSON result file; existing files are never overwritten.")
    args = parser.parse_args()
    smith=[]; symbolic=[]; grid=[]; inclusion=[]
    for n in range(1,8):
        mons,G,P=setup(n)
        D=smith_normal_form(G,domain=s.ZZ)
        inv=[abs(int(D[i,i])) for i in range(min(D.shape)) if D[i,i]]
        require(all(v==1 for v in inv), 'Independent check failed: all(v==1 for v in inv)')
        require(len(mons)-len(inv)==P.rows, 'Independent check failed: len(mons)-len(inv)==P.rows')
        smith.append({'n':n,'quadratic_monomials':len(mons),'generator_rows':G.rows,
                      'relation_rank':len(inv),'nonzero_smith_invariants':sorted(set(inv)),
                      'degree_two_dimension':P.rows})
        if n>=2 and n<=6:
            coeff=s.symbols('a1:'+str(n+1))+s.symbols('b1:'+str(n+1))
            M=mult(mons,P,coeff)
            expected=(-1)**(n-1)*(n-1)*s.prod(a*a for a in coeff[:n])
            det=s.factor(M.det())
            require(s.expand(det-expected)==0, 'Independent check failed: s.expand(det-expected)==0')
            symbolic.append({'n':n,'determinant':str(det)})
    for n in range(1,14):
        mons,G,P=setup(n)
        coeff=[1]*n+[0]*n
        M=mult(mons,P,coeff)
        square=M*s.Matrix(coeff)
        z=s.Matrix([0]*n+[1]*n)
        for p in (2,3,5,7,11):
            rank=modrank(M,p)
            expected=1 if n==1 else 2*n-int((n-1)%p==0)
            require(rank==expected, 'Independent check failed: rank==expected')
            require(any(int(v)%p for v in square), 'Independent check failed: any(int(v)%p for v in square)')
            if n>=2:require((all(int(v)%p==0 for v in M*z))==((n-1)%p==0), 'Independent check failed: (all(int(v)%p==0 for v in M*z))==((n-1)%p==0)')
            grid.append({'n':n,'p':p,'rank_sum_x':rank,'square_nonzero':True})
    for n in range(1,5):
        mons,G,P=setup(n)
        mons2,G2,P2=setup(n+1)
        ix2={m:k for k,m in enumerate(mons2)}
        checked=0
        for inj in permutations(range(n+1),n):
            def img(i):return inj[i] if i<n else (n+1)+inj[i-n]
            T=s.zeros(len(mons2),len(mons))
            for j,(a,b) in enumerate(mons):
                T[ix2[tuple(sorted((img(a),img(b))))],j]=1
            require(P2*T*G.T==s.zeros(P2.rows,G.rows), 'Independent check failed: P2*T*G.T==s.zeros(P2.rows,G.rows)')
            checked+=1
        inclusion.append({'source_n':n,'target_n':n+1,'all_column_injections_checked':checked})
    result={'status':'PASS','method':'Integer Smith normal form of all quadratic generator types; raw monomial multiplication projected only after relation verification; symbolic determinants and exact modular ranks.',
            'integer_quotients':smith,'symbolic_determinants':symbolic,'modular_grid':grid,
            'chain_inclusion':inclusion,
            'scope':'Finite checks support, but do not replace, the all-n proof in AUDIT.md.'}
    encoded = json.dumps(result,indent=2)+'\n'
    p=Path(__file__).with_name('results_independent.json')
    require(encoded.encode('utf-8') == p.read_bytes(), 'Computed results differ from historical results_independent.json')
    if args.output is not None:
        with args.output.open('x', encoding='utf-8', newline='') as stream:
            stream.write(encoded)
    print(json.dumps({'status':'PASS','smith_cases':len(smith),'symbolic_cases':len(symbolic),
                      'modular_cases':len(grid),'injection_cases':sum(x['all_column_injections_checked'] for x in inclusion),
                      'results_sha256':hashlib.sha256(p.read_bytes()).hexdigest()},indent=2))


if __name__=='__main__':main()
