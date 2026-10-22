#!/usr/bin/env python3
"""Read-only independent exact oracles and corruption controls. No source code imports."""
import check_certificate as c
from fractions import Fraction as F
import json,hashlib,pathlib,copy,math
P=pathlib.Path(__file__).resolve().parent
count=0
def need(b,m):
    global count
    count+=1
    if not b:raise RuntimeError(m)
def contains(x,a,b=None):
    b=a if b is None else b
    need(F(x.l,c.S)<=a<=b<=F(x.h,c.S),'oracle containment')
rejected=0
def reject(f):
    global rejected
    try:f()
    except (ValueError,RuntimeError):rejected+=1
    else:raise RuntimeError('corruption escaped')
def main():
    for a in [F(-7,3),F(-1,10),F(0),F(1,7),F(11,3)]:
        for b in [F(-5,4),F(0),F(2,9),F(6,5)]:
            x,y=c.I(a),c.I(b);contains(x+y,a+b);contains(x-y,a-b);contains(x*y,a*b)
            if b:contains(x/y,a/b)
    for a in [F(1,3),F(1),F(2),F(7,2),F(10)]:
        x=c.I(a);rt=x.sqrt();need(rt.l*rt.l<=a*c.S*c.S<=rt.h*rt.h,'sqrt oracle')
        j=c.J(x,1).inv();contains(j.d,-1/(a*a));contains(j.dd,2/(a*a*a))
    t=F(1,3);v=2*sum((t**(2*j+1)/F(2*j+1) for j in range(150)),F(0));r=2*t**301/(301*(1-t*t));contains(c.LN2,v,v+r)
    v=sum((F(1,math.factorial(j)) for j in range(101)),F(0));r=F(1,math.factorial(101))/(1-F(1,102));contains(c.I(1).exp(),v,v+r)
    family=json.loads((P/'family_result.json').read_text());blocks=json.loads((P/'block_result.json').read_text())
    for kind,a,b in [('negative',F(1,50),F(27,100)),('convex',F(27,100),F(28,100)),('positive',F(28,100),F(87,200)),('soft',F(1,10),F(6181,50000)),('soft_last',F(6181,50000),F('.123630684649384'))]:c.cover(family['family_cover'],kind,a,b)
    s=-1/c.I(F(26631,10**6)).log();cap=-1/c.I(F(41542,10**6)).log()
    for kind,a,b in [('affine',F(36,25),F(21,10)),('constant',F(21,10),F(21,5)),('simple',F(1,50),F(s.h,c.S)),('refined',F(s.l,c.S),F(cap.h,c.S))]:c.cover(blocks['records'],kind,a,b)
    original=[{'what':'positive','a':'0','b':'1','bound':['1','2']},{'what':'positive','a':'1','b':'2','bound':['1','2']}]
    def corrupted(fn):
        r=copy.deepcopy(original);fn(r);c.cover(r,'positive',F(0),F(2))
    for fn in [lambda r:r.pop(),lambda r:r[0].update(a='1/10'),lambda r:r[1].update(a='11/10'),lambda r:r[1].update(a='9/10'),lambda r:r[0].update(b='-1'),lambda r:r[0].update(bound=['-1','1']),lambda r:r[0].update(bound=['2','1']),lambda r:r[0].update(what='wrong')]:reject(lambda:corrupted(fn))
    reject(lambda:c.need(F(family['isolation']['width'][0])>F('1.9'),'false L lower'))
    reject(lambda:c.need(F(family['isolation']['q'][0])>F('.026'),'false q lower'))
    reject(lambda:c.need(F(family['isolation']['width'][1])<F('1.8344'),'false L upper'))
    need(F(family['isolation']['width'][1])<F('1.83443047576266171109075363512901884952989750747'),'exact target bridge')
    need(rejected==11,'rejection count');arithmetic_controls=c.controls();need(arithmetic_controls==7,'arithmetic guards')
    print(json.dumps({'schema':'ep1038-independent-controls/v1','exact_oracle_checks':count,'corruption_rejections':rejected,'arithmetic_rejections':arithmetic_controls,'family_slabs':len(family['family_cover']),'block_slabs':len(blocks['records'])},sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
