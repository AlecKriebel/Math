#!/usr/bin/env python3
"""Reproducible finite checks, not an asymptotic proof. Standard library only."""
import itertools,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parent

def sidon(A,mod=None):
    sums=[(a+b) if mod is None else (a+b)%mod for a,b in itertools.combinations_with_replacement(A,2)]
    return len(sums)==len(set(sums))
def blockers(A,N):
    A=set(A); out={}
    for a,b in itertools.combinations_with_replacement(sorted(A),2):
        for c in A:
            x=a+b-c
            if c not in (a,b) and 1<=x<=N and x not in A:
                out.setdefault(x,{'kind':'triple','a':a,'b':b,'c':c})
        if a<b and (a+b)%2==0:
            x=(a+b)//2
            if 1<=x<=N and x not in A: out.setdefault(x,{'kind':'midpoint','a':a,'b':b})
    return out

def main():
    checks=0; maximal_checks=0; exact=[]
    for N in range(1,17):
        best=N+1; witness=None
        for mask in range(1<<N):
            A=[i+1 for i in range(N) if mask>>i&1]
            if not sidon(A):continue
            B=blockers(A,N)
            for x in range(1,N+1):
                if x not in A:
                    assert (x in B)==(not sidon(A+[x]));checks+=1
            if len(A)+len(B)==N:
                maximal_checks+=1;k=len(A);e=sum(a%2==0 for a in A);o=k-e
                assert 2*N<=k**3+k-2*e*o
                # Every seed subset: absolute cross-differences for distinct new points
                # cannot collide, irrespective of each point's chosen seed anchor.
                for seedmask in range(1<<k):
                    S=[A[i] for i in range(k) if seedmask>>i&1];T=set(A)-set(S)
                    distance_owners={}
                    for x in T:
                        for a in S:
                            d=abs(x-a)
                            assert d not in distance_owners or distance_owners[d]==x
                            distance_owners[d]=x
                if k<best:best=k;witness=A
        exact.append({'N':N,'g_N':best,'example':witness})
    A=[8,48,68,69,71,75,104,120];N=144
    assert sidon(A)
    B=blockers(A,N);assert set(B)==set(range(1,N+1))-set(A)
    # Recheck witness equations without trusting blocker generation.
    for x,w in B.items():
        if w['kind']=='triple':
            assert all(w[t] in A for t in ['a','b','c'])
            assert x==w['a']+w['b']-w['c'] and w['c'] not in [w['a'],w['b']]
        else:assert w['a'] in A and w['b'] in A and w['a']<w['b'] and 2*x==w['a']+w['b']
        assert not sidon(A+[x])
    cert={'N':N,'A':A,'pair_sums':sorted(a+b for a,b in itertools.combinations_with_replacement(A,2)),
          'witnesses':{str(x):w for x,w in sorted(B.items())},'claim':'existence only; no eight-mark optimality claim'}
    (ROOT/'certificate_N144.json').write_text(json.dumps(cert,indent=2)+'\n')
    # Negative controls are necessary: midpoint and repeated-summand obstructions.
    assert sidon([1,3]) and not sidon([1,2,3])
    assert 2 not in {a+b-c for a in [1,3] for b in [1,3] for c in [1,3]}
    assert not sidon([1,2,3]) # distinct-pair-only check would miss 1+3=2+2.
    base=[0,1,3];lift=[1,9,18];q=7
    assert sidon(base,q) and sidon(lift)
    assert all(not sidon(base+[x],q) for x in range(q) if x not in base)
    holes=[x for x in range(1,22) if x not in lift and sidon(lift+[x])]
    assert holes
    assert not sidon([1,3,11,13]) # translated copies duplicate a difference.
    output={'exhaustive_domain':'all subsets of [1,N], 1<=N<=16','blocker_checks':checks,
            'maximal_sets_checked':maximal_checks,'exact_finite_values':exact,
            'modular_lift_counterexample':{'q':q,'modular_base':base,'integer_lift':lift,'N':21,'unblocked':holes},
            'N144_certificate_verified':True,'asymptotic_solution':False}
    (ROOT/'checks_results.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))
if __name__=='__main__':main()
