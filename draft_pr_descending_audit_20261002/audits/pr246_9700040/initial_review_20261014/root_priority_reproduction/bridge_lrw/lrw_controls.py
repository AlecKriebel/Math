"""Independent finite controls for the LRW no-jump/rotation bridge.

Pathwise controls use direct finite-k updates and a separate longest-increasing-
subsequence routine. Coefficient controls enumerate permutations and Poisson
strip counts; they do not use Schur or Young-tableau dimensions.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
from itertools import permutations
from math import factorial
from pathlib import Path
import json


def lis(word):
    best = []
    for i,x in enumerate(word):
        best.append(1+max((best[j] for j in range(i) if word[j]<x),default=0))
    return max(best,default=0)


def finite_update(initial,word):
    tops = list(initial)
    for x in word:
        for i,y in enumerate(tops):
            if y>x:
                tops[i]=x
                break
    return tuple(tops)


def pathwise():
    cases = 0
    for k in range(1,6):
        y = tuple(3*j*(j+1)//2 for j in range(1,k+1))
        a = y[-1]
        coords = []
        low = 0
        for j,high in enumerate(y,1):
            coords += [low+j,low+2*j]
            low=high
        coords += [a+1,a+2]  # Deliberate outside-strip points.
        x = tuple(a-v for v in (y[:-1][::-1]+(0,)))
        for n in range(0,min(5,len(coords))+1):
            for word in permutations(coords,n):
                actual = finite_update(y,word)[-1] == a
                in_strip = tuple(v for v in word if v<a)
                assert finite_update(y,word) == finite_update(y,in_strip)
                augmented_lis = lis(y[:-1]+in_strip)
                finite_count = sum(v<a for v in finite_update(y,word))
                assert finite_count == min(k,augmented_lis)
                variational = max(j+lis([v for v in in_strip if v>yj])
                                  for j,yj in enumerate((0,)+y[:-1]))
                assert augmented_lis == variational
                rotated = tuple(a-v for v in in_strip[::-1])
                survival = all(lis([v for v in rotated if v<xr]) <= r-1
                               for r,xr in enumerate(x,1))
                assert actual == (augmented_lis < k) == survival,(k,word)
                cases+=1
    # Explicitly reject an invalid intermediate equality. Appending unrestricted
    # piles remains possible even when all event values lie below initial a.
    negative = dict(initial=(2,),events=(F(1,2),F(1)))
    negative['unrestricted_below_a_count'] = lis(negative['events'])
    negative['finite_below_a_count'] = sum(v<2 for v in finite_update((2,),negative['events']))
    assert negative['unrestricted_below_a_count']==2
    assert negative['finite_below_a_count']==1
    negative['events'] = [str(v) for v in negative['events']]
    return dict(pathwise_histories=cases,maximum_particles=5,maximum_events=5,
                includes_outside_strip_points=True,
                false_finite_unrestricted_count_equality_control=negative)


def compositions(n,k):
    if k==1:
        yield (n,)
    else:
        for j in range(n+1):
            for tail in compositions(n-j,k-1):
                yield (j,)+tail


def pmul(a,b,N):
    out=[F(0)]*(N+1)
    for i,x in enumerate(a):
        for j,y in enumerate(b[:N+1-i]):
            out[i+j]+=x*y
    return out


def parity(p):
    return -1 if sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2 else 1


def bessel_determinant_coefficients(y,N):
    m=len(y)
    matrix=[]
    for i in range(m):
        row=[]
        for j in range(m):
            theta=i-j
            row.append([F(y[j]**p,factorial(p)*factorial(p-theta))
                        if p>=max(theta,0) else F(0) for p in range(N+1)])
        matrix.append(row)
    result=[F(0)]*(N+1)
    for perm in permutations(range(m)):
        poly=[F(1)]+[F(0)]*N
        for i,j in enumerate(perm):
            poly=pmul(poly,matrix[i][j],N)
        for i,v in enumerate(poly):
            result[i]+=parity(perm)*v
    return result


def enumerated_coefficients(x,N):
    k=len(x)
    delta=tuple(x[i]-(x[i-1] if i else 0) for i in range(k))
    results=[]
    for n in range(N+1):
        specs=[]
        for d in compositions(n,k):
            total=0
            cut=[]
            weight=F(1,factorial(n))
            for dt,count in zip(delta,d):
                total+=count
                cut.append(total)
                weight*=F(dt**count,factorial(count))
            specs.append((cut,weight))
        coefficient=F(0)
        for word in permutations(range(1,n+1)):
            lengths=[lis(word[:j]) for j in range(n+1)]
            for cuts,weight in specs:
                if all(lengths[cut]<=r-1 for r,cut in enumerate(cuts,1)):
                    coefficient+=weight
        results.append(coefficient)
    return results


def series():
    result=[]
    for k in range(2,6):
        x=tuple(j*(j+1)//2 for j in range(1,k+1))  # unequal gaps
        a=x[-1]
        y=tuple(a-x[k-j-1] for j in range(1,k))
        observed=enumerated_coefficients(x,7)
        determinant=bessel_determinant_coefficients(y,7)
        assert observed==determinant,(k,observed,determinant)
        result.append(dict(k=k,x=x,y=y,coefficients=[str(v) for v in observed]))
    return dict(maximum_degree=7,cases=result)


if __name__=='__main__':
    result=dict(started_utc=datetime.now(timezone.utc).isoformat(),
                pathwise=pathwise(),formal_series=series())
    result['finished_utc']=datetime.now(timezone.utc).isoformat()
    result['status']='all exact assertions passed'
    Path(__file__).with_name('LRW_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
