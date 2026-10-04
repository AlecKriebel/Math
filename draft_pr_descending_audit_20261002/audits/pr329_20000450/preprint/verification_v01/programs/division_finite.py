#!/usr/bin/env python3
# Public export: optimization must not disable scientific assertions.
import sys
if sys.flags.optimize:
    raise SystemExit("Verification refuses Python optimization (-O/-OO).")
"""Independent general-Weierstrass finite controls; no candidate imports or writes."""
import json


def R_value(x,b,p):
    coefficients=[5,5*(b*b-5*b+1),b**4-7*b**3+44*b*b-38*b+1,
        b*(b**4+3*b**3-26*b*b+127*b-9),b*b*(b**4+3*b**3+19*b*b-248*b+36),
        b**3*(b**4+3*b**3-71*b*b+322*b-84),b**4*(b**4-12*b**3+94*b*b-293*b+126),
        5*b**5*(b**3-10*b*b+36*b-25),5*b**6*(2*b*b-13*b+16),10*b**7*(b-3),5*b**8]
    value=0
    for coefficient in coefficients:value=(value*x+coefficient)%p
    return value


def curve(p,b):
    a1,a2,a3=(1-b)%p,(-b)%p,(-b)%p
    def on(P):
        if P is None:return True
        x,y=P
        return (y*y+a1*x*y+a3*y-x**3-a2*x*x)%p==0
    def negative(P):
        if P is None:return None
        x,y=P
        return x,(-y-a1*x-a3)%p
    def add(P,Q):
        if P is None:return Q
        if Q is None:return P
        x1,y1=P;x2,y2=Q
        if Q==negative(P):return None
        if P==Q:
            numerator=3*x1*x1+2*a2*x1-a1*y1
            denominator=2*y1+a1*x1+a3
        else:
            numerator=y2-y1;denominator=x2-x1
        if denominator%p==0:raise ValueError('Uncovered vertical/tangent exception')
        slope=numerator*pow(denominator%p,-1,p)%p
        intercept=(y1-slope*x1)%p
        x3=(slope*slope+a1*slope-a2-x1-x2)%p
        y3=(-(slope+a1)*x3-intercept-a3)%p
        result=x3,y3
        if not on(result):raise ValueError('General-Weierstrass addition left curve')
        return result
    def multiple(n,P):
        answer=None
        while n:
            if n&1:answer=add(answer,P)
            P=add(P,P);n>>=1
        return answer
    return on,negative,add,multiple


def main():
    total_points=total_fibers=0;all25=[];edge_j=[];negative_counts={'wrong_ordinate_constant':0,'coefficient_mutant':0,'omitted_known_factor':0,'omitted_ordinate_branch':0}
    counts={}
    for p in (7,11,31,41,61):
        counts[p]={'fibers':0,'affine_points':0,'full25':0,'cyclic5':0}
        for b in range(p):
            Delta=b**5*(b*b-11*b-1)%p
            if Delta==0:continue
            on,negative,add,multiple=curve(p,b)
            points=[(x,y) for x in range(p) for y in range(p) if on((x,y))]
            torsion={P for P in points if multiple(5,P) is None}
            predicted={P for P in points if P[0]*(P[0]-b)*R_value(P[0],b,p)%p==0}
            if torsion!=predicted:raise ValueError('Independent torsion/kernel presentation differs')
            marked={(0,0),(0,b),(b,0),(b,b*b%p)}
            if not marked<=torsion or len(marked)!=4:raise ValueError('Marked order5 subgroup failed')
            if multiple(2,(0,0))!=(b,b*b%p) or multiple(3,(0,0))!=(b,0):raise ValueError('Direct marked-point signs failed')
            for P in torsion:
                if multiple(1,P) is None or add(P,negative(P)) is not None:raise ValueError('Exact order/negation failed')
                x,y=P;T=(2*y+(1-b)*x-b)**2%p
                if T==0:raise ValueError('Fifth torsion collided with branch ordinate')
            if len(torsion) not in (4,24):raise ValueError('Unexpected rational5-kernel size')
            omitted_factor={P for P in points if R_value(P[0],b,p)==0}
            if omitted_factor!=torsion:negative_counts['omitted_known_factor']+=1
            wrong_ordinates={(x,(-((1-b)*x+b)+(2*y+(1-b)*x-b))*pow(2,-1,p)%p) for x,y in torsion}
            negative_counts['wrong_ordinate_constant']+=int(any(not on(P) for P in wrong_ordinates))
            mutant={P for P in points if P[0]*(P[0]-b)*(R_value(P[0],b,p)+b*P[0]**8)%p==0}
            negative_counts['coefficient_mutant']+=int(mutant!=torsion)
            one_branch={(x,min(y for xx,y in torsion if xx==x)) for x,_ in torsion}
            negative_counts['omitted_ordinate_branch']+=int(one_branch!=torsion)
            counts[p]['fibers']+=1;counts[p]['affine_points']+=len(points)
            counts[p]['full25' if len(torsion)==24 else 'cyclic5']+=1
            if len(torsion)==24:all25.append({'p':p,'beta':b})
            b2=b*b-6*b+1;b4=b*b-b;c4=(b2*b2-24*b4)%p
            c6=(-b2**3+36*b2*b4-216*b*b)%p
            if c4==0 or c6==0:edge_j.append({'p':p,'beta':b,'j':'0' if c4==0 else '1728','geometric_point_count_claim':'25 in algebraic closure, rational count'+str(len(torsion)+1)})
            total_fibers+=1;total_points+=len(points)
    if not all(n>0 for n in negative_counts.values()):raise ValueError('A mathematical negative control was ineffective')
    on,negative,add,multiple=curve(5,1)
    points=[(x,y) for x in range(5) for y in range(5) if on((x,y))]
    characteristic5_kernel=1+sum(multiple(5,P) is None for P in points)
    if characteristic5_kernel==25:raise ValueError('Characteristic5 boundary not detected')
    print(json.dumps(dict(status='PASS',mechanism='Direct general-Weierstrass chord law on uncompleted Tate equation; binary multiplication by5',
        finite_field_fibers=total_fibers,enumerated_affine_points=total_points,per_prime=counts,
        all25_rational_fiber_examples=all25[:8],j_special_fibers=edge_j,
        mathematical_mutant_detection_counts=negative_counts,
        characteristic5_beta1_rational_kernel=characteristic5_kernel,
        scope='Finite controls support the independently proved characteristic-zero polynomial completeness; finite rational kernel counts are not all geometric point counts.'),indent=2))


if __name__=='__main__':main()
