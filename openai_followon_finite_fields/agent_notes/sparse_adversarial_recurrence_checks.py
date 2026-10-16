"""Independent all-multiplicity Cartier recurrence test, prime coefficients.

Uses only existing dense factorization as a small-field oracle. Sparse U is never
expanded in the main recurrence. Exact denominator recovery and quotient-root
valuations are independent implementations from the proposed production code.
"""
import hashlib
import itertools
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'code'))
sys.path.insert(0,str(ROOT/'agent_notes'))
from finite_fields import FiniteField,factor,exhaustive_prime_split_oracle
from sparse_adversarial_checks import trie,trim,mul,divide,gcd,solve,sparse_mul


def sparse_derivative(U,p):
    return {n-1:n*a%p for n,a in U.items() if n and n*a%p}


def sparse_dense(U,A,p):
    return sparse_mul(U,{i:a for i,a in enumerate(A) if a},p)


def sparse_pade(U,p,B):
    fp=sparse_derivative(U,p)
    inv=pow(U[0],-1,p);s=[]
    for k in range(2*B):
        z=fp.get(k,0)
        for j in range(1,k+1):z-=U.get(j,0)*s[k-j]
        s.append(z*inv%p)
    matrix=[];rhs=[]
    for k in range(2*B):
        row=[s[k-j] if j<=k else 0 for j in range(1,B+1)]
        row += [-int(k==j)%p for j in range(B)]
        matrix.append(row);rhs.append(-s[k]%p)
    v=solve(matrix,rhs,p)
    if v is None:return None
    Q=trim([1]+v[:B],p);A=trim(v[B:],p)
    if sparse_dense(fp,Q,p)!=sparse_dense(U,A,p):return None
    common=gcd(A,Q,p) if A else Q
    G=divide(Q,common,p)[0]
    return [x*pow(G[-1],-1,p)%p for x in G]


def visible(U,p):
    B=1
    while True:
        g=sparse_pade(U,p,B)
        if g is not None:return g,B
        B*=2


def dense_factor(p,f):
    K=FiniteField(p,(0,1))
    answer=factor(K,K.poly(f),exhaustive_prime_split_oracle)
    return [(tuple(a[0] for a in g),e) for g,e in answer.factors]


def multiplicity(U,p,g):
    if len(g)==2:
        E=FiniteField(p,(0,1));alpha=E.element(-g[0])
    else:
        E=FiniteField(p,g);alpha=E.element((0,1))
    return trie(E,[(n,E.element(a)) for n,a in U.items()],alpha)[0][0]


def dense_power(a,e,p):
    ans=[1]
    while e:
        if e&1:ans=mul(ans,a,p)
        e//=2
        if e:a=mul(a,a,p)
    return ans


def recurrence(original,p):
    U=dict(original);V=[1];weight=1;counts={};trace=[]
    # This fixture family always has a nonzero constant coefficient.
    assert U[0]
    while max(U)>0:
        G,B=visible(U,p)
        AU=[1];visiblefacts=[]
        for g,_ in dense_factor(p,G):
            e=multiplicity(U,p,g);r=e%p
            assert r and r<=len(U)-1
            AU=mul(AU,dense_power(list(g),r,p),p)
            counts[g]=counts.get(g,0)+weight*r
            visiblefacts.append((g,e,r))
        AV=[1]
        for g,e in dense_factor(p,V):
            r=e%p
            AV=mul(AV,dense_power(list(g),r,p),p)
            counts[g]=counts.get(g,0)-weight*r
        quotient,remainder=divide(V,AV,p)
        assert not remainder
        assert all(not a or i%p==0 for i,a in enumerate(quotient))
        HV=quotient[::p] # coefficient inverse Frobenius is identity over F_p.
        W=AU[::p]
        assert W[0]
        Unext={n//p:a for n,a in U.items() if n%p==0}
        Vnext=mul(W,HV,p)
        assert Unext[0] and Vnext[0]
        trace.append({'U_terms':len(U),'U_exponent_bits':max(U).bit_length(),
                      'V_degree':len(V)-1,'visible_degree':len(G)-1,
                      'AU_degree':len(AU)-1,'next_V_degree':len(Vnext)-1,
                      'pade_bound':B})
        U,V,weight=Unext,Vnext,weight*p
    assert len(V)==1
    counts={g:e for g,e in counts.items() if e}
    assert all(e>0 for e in counts.values())
    # Independent valuations in the ORIGINAL input, not the intermediate U.
    for g,e in counts.items():assert multiplicity(original,p,g)==e
    assert sum((len(g)-1)*e for g,e in counts.items())==max(original)
    D=sum(len(g)-1 for g in counts)
    for j,row in enumerate(trace):
        assert row['V_degree']<=j*D
        assert row['next_V_degree']<=(j+1)*D
    return counts,trace


def run():
    out={'scope':'finite tests of all-multiplicity Cartier recurrence; not a proof or priority audit',
         'dense_cross_checks':{},'huge_cases':[]}
    for p,length in [(2,9),(3,6)]:
        count=0;max_v=0;max_levels=0
        for coeffs in itertools.product(range(p),repeat=length):
            if not coeffs[0]:continue
            f=trim(coeffs,p)
            if not f:continue
            U={n:a for n,a in enumerate(f) if a}
            answer,trace=recurrence(U,p)
            assert answer==dict(dense_factor(p,f))
            count+=1
            max_levels=max(max_levels,len(trace))
            max_v=max([max_v]+[r['V_degree'] for r in trace])
        out['dense_cross_checks'][f'F{p}_length{length}']={
            'cases':count,'maximum_V_degree':max_v,'maximum_levels':max_levels}
    fixtures=[(2,[(tuple([1,1]),2**160),(tuple([1,1,1]),2**87+1)]),
              (2,[(tuple([1,0,1,1]),2**120+1)]),
              (3,[(tuple([1,0,1]),3**60+1),(tuple([1,1]),3**33)])]
    for p,factors in fixtures:
        U={0:1}
        for g,e in factors:
            # Exponents supplied in their base-p Frobenius decomposition.
            power=1;remaining=e
            while remaining:
                r=remaining%p
                for _ in range(r):
                    U=sparse_mul(U,{i*power:a for i,a in enumerate(g) if a},p)
                power*=p;remaining//=p
        answer,trace=recurrence(U,p)
        assert answer==dict(factors)
        out['huge_cases'].append({'p':p,'input_terms':len(U),
            'maximum_exponent_bits':max(U).bit_length(),'distinct_output_degree':sum(len(g)-1 for g,_ in factors),
            'levels':len(trace),'maximum_V_degree':max(r['V_degree'] for r in trace),
            'factor_multiplicity_bits':[e.bit_length() for g,e in sorted(answer.items())],
            'trace_sha256':hashlib.sha256(json.dumps(trace,sort_keys=True).encode()).hexdigest()})
    artifact={0:1,2:1,3:1}
    answer,trace=recurrence(artifact,2)
    assert answer=={(1,0,1,1):1}
    assert trace[0]['next_V_degree']==1
    out['artifact_factor_cancellation']={'input':'X^3+X^2+1 over F2',
        'next_U':'X+1','next_V':'X+1','output_contains_X_plus_1':False,'trace':trace}
    out['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    return out

if __name__=='__main__':
    out=run()
    (ROOT/'agent_notes'/'sparse_adversarial_recurrence_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
