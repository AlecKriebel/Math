#!/usr/bin/env python3
"""Exhaustively count FULL automorphisms of three split metacyclic controls.
The group is <a,b | a^(p^2)=b^p=1, b a b^-1=a^(1+p)>.
All elements, all generator-image pairs, all relators and generation are checked.
"""
import json, platform, sys

def check(p:int)->dict:
    m=p*p; q=1+p
    assert pow(q,p,m)==1
    def mul(x,y): return ((x[0]+pow(q,x[1],m)*y[0])%m,(x[1]+y[1])%p)
    def power(x,n):
        z=(0,0)
        while n:
            if n&1:z=mul(z,x)
            x=mul(x,x);n//=2
        return z
    def inv(x):return ((-pow(q,-x[1],m)*x[0])%m,(-x[1])%p)
    E=[(i,j) for i in range(m) for j in range(p)]
    count=0;relator_pairs=0
    for x in E:
        for y in E:
            if power(x,m)!=(0,0) or power(y,p)!=(0,0):continue
            if mul(mul(y,x),inv(y))!=power(x,q):continue
            relator_pairs+=1
            # The Frattini quotient has basis a,b over F_p.
            if (x[0]*y[1]-x[1]*y[0])%p:count+=1
    assert count==(p-1)*p**3
    return {'prime':p,'group_order':len(E),'full_automorphism_order':count,
            'all_generator_image_pairs_examined':len(E)**2,'relator_satisfying_pairs':relator_pairs}
if __name__=='__main__':
    results=[check(p) for p in (3,5,7)]
    print(json.dumps({'python':sys.version,'platform':platform.platform(),'results':results},indent=2))
