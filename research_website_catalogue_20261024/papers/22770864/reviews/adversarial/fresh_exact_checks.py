#!/usr/bin/env python3
"""Independent stdlib-only adversarial reconstruction; no archived code imported.

Rebuilds the manuscript's integer algebra and lattice, compares published data,
and replays a proposed Smith plan using unbounded integer arithmetic. Finite
checks do not replace the manuscript's lifting or logarithm arguments.
"""
from collections import Counter
from datetime import datetime, timezone
from itertools import combinations
from math import factorial, comb, isqrt
from pathlib import Path
import json
import time

OUT = Path(__file__).resolve().parent
SRC = OUT.parents[1] / 'sources/published-source/kourovka_16_63'
P, D = 1009, 31
START = time.monotonic()

def add(v, k, n):
    v[k] = v.get(k, 0) + n
    if not v[k]:
        del v[k]

def diff_monomial(x, y, dx, dy):
    if dx > x or dy > y:
        return 0
    return factorial(x) // factorial(x-dx) * factorial(y) // factorial(y-dy)

def trans(m, n, r, i, j):
    return sum((-1)**q * comb(r, q)
               * diff_monomial(m-i, i, r-q, q)
               * diff_monomial(n-j, j, q, r-q) for q in range(r+1))

def original():
    c = {}
    def put(i, j, k, n):
        if n:
            assert i != j
            assert c.get((i,j), {}).get(k, n) == n
            c.setdefault((i,j), {})[k] = n
            c.setdefault((j,i), {})[k] = -n
    put(0,1,1,2); put(0,2,2,-2); put(1,2,0,1)
    modules = [(6,3),(4,10),(6,15),(2,22),(4,25),(0,30)]
    for m,s in modules:
        for i in range(m+1):
            put(0,s+i,s+i,m-2*i)
            if i: put(1,s+i,s+i-1,i)
            if i<m: put(2,s+i,s+i+1,m-i)
    for aa,bb,cc,r in [(0,0,2,3),(0,1,3,4),(0,2,3,5),
                       (0,4,3,4),(1,1,3,3),(1,4,5,4),(4,4,3,3)]:
        m,a=modules[aa]; n,b=modules[bb]; _,target=modules[cc]
        for i in range(m+1):
            for j in range(n+1):
                if aa==bb and i>=j: continue
                q=trans(m,n,r,i,j)
                if q: put(a+i,b+j,target+i+j-r,q)
    return c

def bracket(c,x,y):
    z={}
    for i,a in x.items():
        for j,b in y.items():
            for k,t in c.get((i,j),{}).items(): add(z,k,a*b*t)
    return z

def jacobi(c):
    count=0
    for i,j,k in combinations(range(D),3):
        z={}
        for a,b,d in [(i,j,k),(j,k,i),(k,i,j)]:
            for l,n in bracket(c,{a:1},c.get((b,d),{})).items(): add(z,l,n)
        assert not z,(i,j,k,z)
        count+=1
    return count

def adapted(c):
    others=[i for i in range(D) if i not in (0,1,3)]
    base=[{0:1},{1:1,2:1,4:1,10:1,27:1},{3:1}]+[{i:1} for i in others]
    def inverse(z):
        ans={i:z[k] for i,k in [(0,0),(1,1),(2,3)] if z.get(k)}
        for i,k in enumerate(others,3):
            t=z.get(k,0)-(z.get(1,0) if k in (2,4,10,27) else 0)
            if t: ans[i]=t
        return ans
    for i,v in enumerate(base): assert inverse(v)=={i:1}
    return {(i,j):inverse(bracket(c,base[i],base[j])) for i in range(D) for j in range(D)}

def rank(rows, prime=P):
    pivots={}
    for r in rows:
        r={k:v%prime for k,v in r.items() if v%prime}
        while r:
            k=min(r)
            if k not in pivots:
                inv=pow(r[k],-1,prime)
                pivots[k]={j:v*inv%prime for j,v in r.items()}
                break
            f=r[k]
            for j,v in pivots[k].items():
                z=(r.get(j,0)-f*v)%prime
                if z: r[j]=z
                elif j in r: del r[j]
    return len(pivots)

def deriv_rows(c):
    rows=[]
    for i,j in combinations(range(D),2):
        for k in range(D):
            r={}
            for b,v in c.get((i,j),{}).items(): add(r,k*D+b,v)
            for a in range(D):
                add(r,a*D+i,-c.get((a,j),{}).get(k,0))
                add(r,a*D+j,-c.get((i,a),{}).get(k,0))
            rows.append(r)
    return rows

def smith_certificate(rows, plan, precision=6):
    modulus=P**precision
    a={i:{k:v%modulus for k,v in r.items() if v%modulus} for i,r in enumerate(rows)}
    a={i:r for i,r in a.items() if r}
    active_cols=set(range(D*D))
    counts=Counter()
    prev=-1
    for step,item in enumerate(plan):
        i,j,v=item['row'],item['col'],item['valuation']
        assert j in active_cols and i in a,('repeated pivot',step)
        assert prev<=v<precision,('valuation order',step)
        q=P**v; r=a[i]; pivot=r.get(j,0)
        assert pivot%q==0 and (pivot//q)%P,('pivot valuation',step)
        if v!=prev:
            assert all(n%q==0 for row in a.values() for n in row.values()),('minimality',step)
        inv=pow(pivot//q,-1,modulus)
        rr={k:n*inv%modulus for k,n in r.items()}
        assert rr[j]==q and all(n%q==0 for n in rr.values())
        for ii,row in list(a.items()):
            if ii==i or j not in row: continue
            assert row[j]%q==0
            factor=row[j]//q
            for k,n in rr.items():
                z=(row.get(k,0)-factor*n)%modulus
                if z: row[k]=z
                elif k in row: del row[k]
            assert j not in row
            if not row: del a[ii]
        del a[i]; active_cols.remove(j)
        counts[v]+=1; prev=v
        if (step+1)%200==0: print('fresh exact Smith pivots',step+1,flush=True)
    assert not a,('residual nonzero block',len(a))
    return dict(sorted(counts.items()))

def main():
    assert all(P%q for q in range(2,isqrt(P)+1))
    c=original(); ca=adapted(c)
    j0=jacobi(c); j1=jacobi(ca)
    terms=sorted([i,j,k,n] for (i,j),v in c.items() if i<j for k,n in v.items())
    archived=json.loads((SRC/'data/lie31_brackets.json').read_text())
    assert terms==sorted(archived['terms'])
    weights=[0,0,1]+[2]*28
    cl={(i,j):{k:n*P**(2+weights[i]+weights[j]-weights[k]) for k,n in v.items()}
        for (i,j),v in ca.items()}
    exported=json.loads((SRC/'data/group_lie_presentation.json').read_text())
    assert sorted(exported['bracket_terms_i_lt_j'])==sorted(
        [i,j,k,n] for (i,j),v in cl.items() if i<j for k,n in v.items())
    assert exported['coefficient_ring']['exponent']==1689
    print('integer brackets, Jacobi, adapted basis, exported presentation agree',flush=True)
    ir=rank([{j*D+k:c.get((a,j),{}).get(k,0) for j in range(D) for k in range(D)}
             for a in range(D)])
    pr=rank(list(c.values()))
    dr=rank(deriv_rows(c))
    assert (ir,pr,dr)==(30,31,931)
    # Direct finite-field closure, independent of Lie-word certificate.
    basis=[{0:1},{1:1}]
    old=0
    while len(basis)>old and len(basis)<D:
        old=len(basis)
        for i in range(old):
            for j in range(i):
                z=bracket(ca,basis[i],basis[j])
                if rank(basis+[z])>len(basis): basis.append(z)
                if len(basis)==D: break
            if len(basis)==D: break
    assert len(basis)==31
    # Linear flag equations applied to inner derivations, whose full dimension
    # has independently been obtained from the entire derivation matrix.
    flag=[{a:ca.get((a,j),{}).get(k,0) for a in range(D)}
          for j in range(3) for k in range(2 if j<2 else 3,D)]
    fr=rank(flag); assert fr==30
    # Enumerate all upper-Borel elements surviving the quotient-plane equation.
    # For s=(a,b;0,1), Ad_s(e-f) has matrix entries (-b/a, a+b*b/a;-1/a,b/a).
    survivors=[]
    for aa in range(1,P):
        inv=pow(aa,-1,P)
        for b in range(P):
            if b*inv%P==0 and (aa+(b*b-1)*inv)%P==0: survivors.append((aa,b))
    assert survivors==[(1,0),(P-1,0)]
    # For the four quotient/discrete-component choices, solve the necessary
    # modulo-N' flag equations on the weight-zero part of U+V+R.
    slots=list(range(3,10))+list(range(10,15))+list(range(25,30))
    zero=[6,12,27]
    sn=[bracket(c,{1:1,2:1},{z:1}) for z in zero]
    system=[{a:v.get(k,0) for a,v in enumerate(sn)} for k in slots]
    flag_cases=[]
    for sign in [1,-1]:
        for swap in [False,True]:
            transformed={4:1,25 if swap else 10:1,12 if swap else 27:1}
            target={k:sign*transformed.get(k,0)-{4:1,10:1,27:1}.get(k,0) for k in slots}
            aug=[dict(r,**{}) for r in system]
            for r,k in zip(aug,slots): r[3]=target[k]
            feasible=rank(aug)==rank(system)
            assert feasible==(sign==1 and not swap)
            flag_cases.append({'quotient_sign':sign,'swap':swap,'feasible_mod_Nprime':feasible})
    print('generation, inner/full derivations, infinitesimal and finite flag controls pass',flush=True)
    rows=deriv_rows(cl)
    plan=json.loads((SRC/'data/smith_pivot_plan.json').read_text())
    assert len(plan)==931
    counts=smith_certificate(rows,plan)
    assert counts=={0:87,1:55,2:758,3:6,4:25}
    assert sum(v*n for v,n in counts.items())==1689
    bad=[dict(item) for item in plan]; bad[0]['valuation']=5
    try:
        smith_certificate(rows,bad)
    except AssertionError as e:
        rejection=str(e)
    else:
        raise AssertionError('corrupted certificate accepted')
    # Additional adverse control: perturb a defining coefficient; Jacobi must
    # reject it instead of merely comparing against fixed expected dimensions.
    wrong={k:dict(v) for k,v in c.items()}
    wrong[(0,3)][3]+=1; wrong[(3,0)][3]-=1
    try:
        jacobi(wrong)
    except AssertionError as e:
        bracket_rejection=str(e)
    else:
        raise AssertionError('non-Lie perturbation accepted')
    # Check the arithmetic at the endpoints used in the analytic valuation
    # proof; its tail follows from the displayed linear Legendre bound.
    assert 2*847>=1689+4 and 846<P
    assert 31*1689==30*1689+1689==52359
    result={'timestamp_utc':datetime.now(timezone.utc).isoformat(),
            'implementation':'fresh Python standard library; no archived code imported',
            'prime':P,'original_jacobi_triples':j0,'adapted_jacobi_triples':j1,
            'published_coefficients_match':True,'group_presentation_match':True,
            'inner_rank':ir,'perfect_rank':pr,'unscaled_derivation_rank_mod_p':dr,
            'generated_rank':len(basis),'infinitesimal_flag_rank':fr,
            'upper_borel_survivors':survivors,'finite_flag_cases':flag_cases,
            'smith_precision':6,'smith_counts':counts,'smith_sum':1689,
            'corrupted_plan_rejected':rejection,'non_Lie_perturbation_rejected':bracket_rejection,
            'group_order_exponent':52359,'class_upper_bound':846,
            'elapsed_seconds':time.monotonic()-START,
            'limits':'No full group/automorphism enumeration; analytic classification, lifting, logarithm and Lazard steps independently reviewed in REVIEW.md.'}
    (OUT/'fresh_exact_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
