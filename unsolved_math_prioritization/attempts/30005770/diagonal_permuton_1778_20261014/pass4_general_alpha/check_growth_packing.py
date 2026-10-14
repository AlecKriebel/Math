#!/usr/bin/env python3
"""Exact finite regressions for the PASS4 general-alpha note, not an asymptotic proof."""
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations
from math import comb
from pathlib import Path
import hashlib,json,sys,time

HERE=Path(__file__).resolve().parent
PROOF_HASH='c0e18d22fbda449f7303cf9688a66f10269d417e2687e2766ae7cd72e5632465'

def require(ok,detail):
    if not ok: raise RuntimeError(detail)

def rank(seq):
    ranks={x:i+1 for i,x in enumerate(sorted(seq))}
    return tuple(ranks[x] for x in seq)

@lru_cache(None)
def perms(n): return tuple(permutations(range(1,n+1)))

@lru_cache(None)
def occurrences(p,m):
    out={}
    for ids in combinations(range(len(p)),m):
        q=rank(tuple(p[i] for i in ids))
        out.setdefault(q,[]).append(sum(1<<i for i in ids))
    return {q:tuple(v) for q,v in out.items()}

@lru_cache(None)
def class_count(q,n):
    return sum(q not in occurrences(p,len(q)) for p in perms(n))

@lru_cache(None)
def packing_and_deletion(n,occs):
    @lru_cache(None)
    def packing(available):
        return max((1+packing(available^o) for o in occs if available&o==o),default=0)
    P=packing((1<<n)-1)
    for h in range(n+1):
        for ids in combinations(range(n),h):
            removed=sum(1<<i for i in ids)
            if all(removed&o for o in occs): return P,h,ids
    raise RuntimeError('No deletion witness')


def reconstruct(p,ids):
    n=len(p);I=set(ids);V=tuple(sorted(p[i] for i in ids))
    sigma=rank(tuple(p[i] for i in ids))
    eta=rank(tuple(p[i] for i in range(n) if i not in I))
    comp_pos=tuple(i for i in range(n) if i not in I)
    comp_val=tuple(sorted(set(p)-set(V)))
    result=[0]*n
    for i,r in zip(ids,sigma): result[i]=V[r-1]
    for i,r in zip(comp_pos,eta): result[i]=comp_val[r-1]
    require(tuple(result)==p,('deletion inverse',p,ids))
    return (tuple(ids),V,sigma,eta)


def exhaustive_small():
    rows=[]
    for m in (2,3,4):
        limit=7 if m<=3 else 6
        for alpha in perms(m):
            tau=tuple(x+1 for x in alpha)+(1,)
            for n in range(1,limit+1):
                ds=Counter(); encodings=set(); tested=0; crossing_checks=0
                for p in perms(n):
                    if tau in occurrences(p,m+1): continue
                    tested+=1
                    P,D,ids=packing_and_deletion(n,occurrences(p,m).get(alpha,()))
                    require(P<=D<=m*P,('packing/deletion inequality',alpha,p,P,D))
                    encoding=reconstruct(p,ids)
                    require(encoding not in encodings,('encoding collision',alpha,p,ids))
                    encodings.add(encoding)
                    require(tau not in occurrences(encoding[2],m+1),('deleted pattern not in C',alpha,p,ids))
                    require(alpha not in occurrences(encoding[3],m),('retained pattern not alpha-free',alpha,p,ids))
                    ds[D]+=1
                    for r in range(n+1):
                        crossing=tuple(x for x in p[:r] if x>r)
                        opposite=sum(x<=r for x in p[r:])
                        require(len(crossing)==opposite,('crossing cardinality',alpha,p,r))
                        require(alpha not in occurrences(rank(crossing),m),('crossing contains alpha',alpha,p,r))
                        crossing_checks+=1
                require(tested==class_count(tau,n),('actual class count',alpha,n))
                for h in range(n+1):
                    actual=sum(v for d,v in ds.items() if d<=h)
                    upper=comb(n,h)**2*class_count(tau,h)*class_count(alpha,n-h)
                    require(actual<=upper,('exact deletion count',alpha,n,h,actual,upper))
                rows.append({'alpha':list(alpha),'n':n,'actual_avoiders':tested,
                             'crossing_rectangles_checked':crossing_checks,
                             'deletion_distance_histogram':dict(sorted(ds.items()))})
    return rows


def direct_sum(parts):
    p=[];offset=0
    for q in parts:
        p.extend(x+offset for x in q);offset+=len(q)
    return tuple(p)


def contains_brute(p,q):
    m=len(q)
    checks=tuple((i,j,q[i]<q[j]) for i in range(m) for j in range(i+1,m))
    for ids in combinations(range(len(p)),m):
        if all((p[ids[i]]<p[ids[j]])==sense for i,j,sense in checks): return True
    return False


def inv(p): return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))
def desc(p): return sum(p[i]>p[i+1] for i in range(len(p)-1))


def perfect_packing_constructions():
    rows=[]
    for m in (2,3,4):
        for alpha in perms(m):
            tau=tuple(x+1 for x in alpha)+(1,)
            for k in (1,2,3):
                if alpha==tuple(range(1,m+1)):
                    p=tuple(range(1,(m-1)*k+1))+tuple(range(m*k,(m-1)*k,-1))
                    partition=[tuple(range(r*(m-1),(r+1)*(m-1)))+((m-1)*k+r,) for r in range(k)]
                    shield=(m-1)*k
                    r=shield+k//2
                    crossing_expected=k//2
                    inversion_expected=k*(k-1)//2
                else:
                    prefix=direct_sum([alpha]*k)
                    Q=tuple((x-1)*k+r for x in alpha for r in range(1,k+1))
                    require(desc(Q)==desc(alpha) and desc(tau)==desc(alpha)+1,('descent count',alpha,k))
                    p=direct_sum([prefix,Q])
                    partition=[tuple(range(j*m,(j+1)*m)) for j in range(k)]
                    partition += [tuple(m*k+j*k+r for j in range(m)) for r in range(k)]
                    shield=m*k
                    ell=next(j for j in range(1,m) if any(x>j for x in alpha[:j]))
                    r=m*k+ell*k
                    crossing_expected=k*sum(x>ell for x in alpha[:ell])
                    inversion_expected=(k+k*k)*inv(alpha)
                n=len(p)
                require(sorted(p)==list(range(1,n+1)),('not permutation',alpha,k))
                require(not contains_brute(p,tau),('construction forbidden pattern',alpha,k,p))
                require(sorted(i for group in partition for i in group)==list(range(n)),('packing not partition',alpha,k))
                require(all(rank(tuple(p[i] for i in group))==alpha for group in partition),('wrong packing pattern',alpha,k))
                require(rank(p[:m])==alpha,('first frontier',alpha,k))
                positions={v:i+1 for i,v in enumerate(p)}
                for s in range(1,shield+1):
                    bound=s if alpha==tuple(range(1,m+1)) else s+m-1
                    require(max(positions[v] for v in range(1,s+1))<=bound,('small values',alpha,k,s))
                crossing=sum(x>r for x in p[:r])
                require(crossing==crossing_expected,('cut mass',alpha,k,r,crossing,crossing_expected))
                require(inv(p)==inversion_expected,('inversion formula',alpha,k))
                rows.append({'alpha':list(alpha),'k':k,'n':n,'packing_size':len(partition),
                             'cut':r,'crossing_count':crossing,'inversions':inversion_expected})
    return rows


def main():
    start=time.time()
    proof=HERE/'GROWTH_PACKING_AND_SPATIAL_BARRIER.md'
    require(hashlib.sha256(proof.read_bytes()).hexdigest()==PROOF_HASH,'Frozen proof changed')
    small=exhaustive_small()
    print('Exact deletion, packing, and crossing-rectangle checks passed.',flush=True)
    constructions=perfect_packing_constructions()
    print('Every explicit perfect-packing construction passed.',flush=True)
    result={'status':'PASS','interpretation':'Finite regressions only; the all-size argument is in the pinned proof.',
            'proof_sha256':PROOF_HASH,'python':sys.version,'optimization_level':sys.flags.optimize,
            'small_case_rows':small,'small_cases_total':sum(r['actual_avoiders'] for r in small),
            'crossing_rectangles_total':sum(r['crossing_rectangles_checked'] for r in small),
            'construction_rows':constructions,'constructions_total':len(constructions),
            'elapsed_seconds':round(time.time()-start,3)}
    path=HERE/f'CHECK_OPTIMIZATION_{sys.flags.optimize}.json'
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','small_cases_total','crossing_rectangles_total','constructions_total','elapsed_seconds')}))

if __name__=='__main__':main()
