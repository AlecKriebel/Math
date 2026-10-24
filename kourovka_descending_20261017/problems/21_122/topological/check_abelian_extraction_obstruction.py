"""Exact checks of the class-two p-power construction; not a 21.122 solution."""

from datetime import datetime, timezone
from itertools import product
from math import comb
import json


def check(p=3, max_n=4):
    levels=[]
    for n in range(1,max_n+1):
        pairs=[(i,j) for i in range(n) for j in range(i+1,n)]
        def beta(a,b):
            return tuple(a[i]*b[j]%p for i,j in pairs)
        def mul(x,y):
            a,c=x
            b,d=y
            z=beta(a,b)
            return (tuple((u+v)%(p*p) for u,v in zip(a,b)),
                    tuple((u+v+t)%p for u,v,t in zip(c,d,z)))
        zero=((0,)*n,(0,)*len(pairs))
        outputs=set()
        for a in product(range(p*p),repeat=n):
            x=(a,(0,)*len(pairs))
            power=zero
            for _ in range(p):
                power=mul(power,x)
            expected=(tuple(p*(u%p) for u in a),(0,)*len(pairs))
            assert power==expected
            outputs.add(power)
        vectors=list(product(range(p),repeat=n))
        for a in vectors:
            for b in vectors:
                commute=beta(a,b)==beta(b,a)
                proportional=(not any(a) or any(
                    all(v==s*u%p for u,v in zip(a,b)) for s in range(p)))
                assert commute==proportional
        assert len(outputs)==p**n
        levels.append({'n':n,'p':p,'full_power_image_size':len(outputs),
                       'abelian_power_image_bound':p,
                       'checked_mod_p_vector_pairs':len(vectors)**2})
    return {'timestamp_utc':datetime.now(timezone.utc).isoformat(),
            'status':'passed','solves_21_122':False,'levels':levels}


if __name__=='__main__':
    print(json.dumps(check(),indent=2))
