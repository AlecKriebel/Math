#!/usr/bin/env python3
"""Independent coordinate formulas; no imports from the enumeration program."""
import itertools
import json

V=list(itertools.product(range(2),repeat=3))
ZERO=(0,0,0);ONE=(1,0,0);E=(0,1,0);F=(0,0,1)
def mul(x,y,symmetric=False):
    a,b,c=x;p,q,r=y
    return ((a*p+c*q+(b*r if symmetric else 0))%2,
            (a*q+b*p)%2,(a*r+c*p)%2)
def test(symmetric):
    m=lambda x,y:mul(x,y,symmetric)
    units=[]
    for a in V:
        if any(all(m(a,m(b,z))==z==m(b,m(a,z)) and
                       m(m(z,a),b)==z==m(m(z,b),a) for z in V) for b in V):
            units.append(a)
    assert units==[ONE]
    assert all(m(m(a,y),m(z,a))==m(m(a,m(y,z)),a) and
               m(a,m(y,m(a,z)))==m(m(a,m(y,a)),z) and
               m(m(m(z,a),y),a)==m(z,m(m(a,y),a))
               for a in units for y in V for z in V)
    bad=None
    for a,b,c,t in itertools.product(V,repeat=4):
        if m(a,b)==ZERO==m(c,a):
            d=m(b,c)
            values=(m(d,m(a,t)),m(m(t,a),d),m(a,m(d,t)),m(m(t,d),a))
            if any(v!=ZERO for v in values):
                bad={'a':a,'b':b,'c':c,'t':t,'values':values};break
    if symmetric:
        assert bad is None
        assert m(m(E,E),F)==ZERO and m(E,m(E,F))==E
    else:
        assert bad is not None
        assert m(m(F,F),E)==ZERO and m(F,m(F,E))==F
    return {'strong_units':units,'opposite_root_obstruction':bad,
            'nonalternative':True}
print(json.dumps({'one_sided_pair':test(False),'symmetric_pair':test(True)},
                 indent=2,sort_keys=True))
