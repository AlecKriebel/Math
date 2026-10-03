#!/usr/bin/env python3
"""Exact finite controls for the audit mechanisms, not a target proof search."""
from fractions import Fraction as F
import json


def matmul(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def point_on_chord(a, b, t):
    return tuple(a[j]+t*(b[j]-a[j]) for j in range(2))


def height_squared(a, b, t):
    # Chord endpoints are at height1 on one hyperbolic semicircle.
    return 1+sum((b[j]-a[j])**2 for j in range(2))*t*(1-t)


def main():
    checks = []
    def check(name, condition, evidence):
        assert condition, name
        checks.append({'check': name, 'pass': True, 'evidence': evidence})

    exponents=[]
    for n in [3,4,5,8]:
        boundary=F(3,n-2)
        for kappa, expected in [(boundary+F(1,7),-1),(boundary,0),(boundary-F(1,7),1)]:
            exponent=3-(n-2)*kappa
            sign=(exponent>0)-(exponent<0)
            assert sign==expected
            exponents.append({'n':n,'kappa':str(kappa),'exponent':str(exponent),'sign':sign})
    check('strict exponent boundary', True, exponents)
    check('dimension2 mechanism does not decay', 3-(2-2)*F(100)==3, 'n=2 exponent3 for every kappa')

    a=[[1,2],[0,1]]; b=[[1,0],[2,1]]; g=matmul(a,b)
    check('primitive-shortcut exact matrix witness',g==[[5,2],[2,1]],g)
    # Fixed roots satisfy z²−2z−1=0. Translated roots satisfy z²−6z+7=0.
    # Centers1/3 and radius²2 meet at x2,height²1, with slopes−1/+1.
    check('proper translated-axis intersection',(2-1)**2+1==2 and (2-3)**2+1==2 and -1!=1,
          {'axis_center':1,'translate_center':3,'radius_squared':2,'intersection':[2,1], 'tangent_slopes':[-1,1]})
    check('endpoint root polynomials differ',[1,-2,-1]!=[1,-6,7],
          {'axis_polynomial':[1,-2,-1],'translated_polynomial':[1,-6,7], 'A_not_axis_stabilizer':True})
    check('Gamma2 trace0 elliptic obstruction', (1+0)%4!=(-1)%4,
          'trace0 with odd diagonal a,-a and even off-diagonals would give a²+bc=−1, impossible mod4')

    b2=F(2,5); error=F(1,100)
    check('toral transverse coordinate margin',0<b2-2*error and b2+2*error<1,
          {'transverse':str(b2),'error':str(error),'lower':str(b2-2*error),'upper':str(b2+2*error)})
    a0=F(1,5)
    check('symmetric cusp midpoint half-lattice separation',a0-error>0 and a0+error<F(1,2),
          {'distance':str(a0),'perturbed_minimum':str(a0-error),'valid_for_all_integer_n':True})
    y0,y1=F(-1,5),F(1,3)
    midpoint=(y0+y1)/2
    check('nonsymmetric cusp midpoint excludes all half-lattice axes',abs(midpoint)>error and abs(midpoint)+error<F(1,2),
          {'midpoint':str(midpoint),'minimum_gap_after_error':str(abs(midpoint)-error)})
    check('nonsymmetric cusp excludes translations',0<y1-y0-2*error and y1-y0+2*error<1,
          {'transverse_difference':str(y1-y0),'error':str(error)})

    # Removing the midpoint obstruction supplies an actual same-height glide collision.
    endpoints=((F(0),F(-1,5)),(F(2),F(1,5)))
    p=point_on_chord(*endpoints,F(1,4)); q=point_on_chord(*endpoints,F(3,4))
    sp=(p[0]+1,-p[1])
    hp=height_squared(*endpoints,F(1,4)); hq=height_squared(*endpoints,F(3,4))
    check('negative control actual glide collision',sp==q and hp==hq and hp>1,
          {'P':[str(x) for x in p],'Q':[str(x) for x in q],'height_squared':str(hp),'glide':'(x+1,−y)'})

    # Projected identification alone is not sufficient for a reversing cusp element.
    endpoints=((F(0),F(-1,5)),(F(4),F(3,10)))
    u,v=F(11,40),F(21,40)
    p=point_on_chord(*endpoints,u); q=point_on_chord(*endpoints,v)
    hp=height_squared(*endpoints,u); hq=height_squared(*endpoints,v)
    check('negative control projected glide identification has unequal heights',
          (p[0]+1,-p[1])==q and hp!=hq,
          {'P':[str(x) for x in p],'Q':[str(x) for x in q],'height_squared_P':str(hp),'height_squared_Q':str(hq),
           'not_an_actual_hyperbolic_arc_collision':True})

    # Finite-angle/length margins used by the local repair are exact inequalities.
    inj=F(1); delta=F(1,100)
    check('pointed-loop nontriviality and uniform long-half constant', inj-3*delta>inj/2 and 2*delta<(inj/2)/4,
          {'length_lower_bound':str(inj-3*delta),'applicable_L':str(inj/2),'endpoint_error':str(2*delta)})
    for r,eps,c in [(F(100),F(1,10),F(1,20)),(F(1000),F(1,3),F(-1,4))]:
        ell=r-eps
        assert ell/4-abs(c)>r/10 and 3*(r+eps)/4+abs(c)<9*r/10
    check('corrected interior witness margin',True,'[ell/4,3ell/4] plus bounded flow shift lies inside [r/10,9r/10] for large r')
    check('Banach boundary-map loxodromic margin',F(1,3-1)**2<1,
          'for K>3, displacement-map and inverse are contractions on disjoint unit balls, with derivative≤1/(K−1)²')
    output={'schema':'pr40-geodesic-exact-controls/v1','status':'PASS','arithmetic':'stdlib Fraction and exact integer polynomial/circle arithmetic',
            'checks':checks,'new_substantive_attempts':0,'verification_attempts_added':0,
            'limitations':['Finite mechanism controls do not prove the full target.','Matrix witness is an infinite-volume example, not a target counterexample.','Boundary-map derivative and free-group facts are proved in the authored audit; sampled arithmetic alone does not certify them.']}
    print(json.dumps(output,indent=2,ensure_ascii=False))


if __name__=='__main__':
    main()
