#!/usr/bin/env python3
"""Independent rational reconstruction; never imports or executes author code.
Finite checks supplement the proof audit. They certify neither topology nor a knot.
All guards remain active under python -O.
"""
import json
from fractions import Fraction as Q
from itertools import combinations, product
from collections import Counter


def demand(value, label, counts):
    if not value:
        raise RuntimeError('Independent check failed: ' + label)
    counts[label] += 1


def classify(k, p, q, area, target):
    if type(k) is not int or k < 1:
        raise ValueError('Intersection must be a positive integer')
    p,q,area,target = [Q(x) for x in (p,q,area,target)]
    if any(x <= 0 for x in (p,q,area,target)):
        raise ValueError('Lengths and area must be positive')
    determinant = k * area
    if determinant > p*q:
        return 'inconsistent_inputs'
    half_gap = (k*k*target*target-p*p-q*q)/2
    if half_gap < 0:
        return 'inconclusive'
    comparison = half_gap*half_gap - ((p*q)**2-determinant**2)
    return ('strict' if comparison > 0 else
            'at_most' if comparison == 0 else 'inconclusive')


def pair_optimum(slopes, caps):
    choices = [(Q(caps[i]+caps[j])/abs(slopes[i]-slopes[j]), i, j)
               for i in range(len(slopes)) for j in range(i+1,len(slopes))
               if slopes[i] != slopes[j]]
    if not choices or len(slopes) != len(caps) or min(caps) <= 0:
        raise ValueError('Invalid pair problem')
    return sorted(choices)[0]


def integer_cap(square):
    # Independent monotone integer construction, avoiding the author's isqrt helper.
    p = 1
    while p*p < square:
        p += 1
    return Q(p)


def dot(u,v):
    return sum(a*b for a,b in zip(u,v))


def determinant(u,v):
    return u[0]*v[1]-u[1]*v[0]


def rebuild():
    counts=Counter()
    check=lambda v,k:demand(v,k,counts)
    examples=[((8,18,18,36,4),'strict'),((2,5,5,12,4),'at_most'),
              ((2,5,5,12,Q(399,100)),'inconclusive'),
              ((2,5,5,13,4),'inconsistent_inputs'),
              ((1,1,1,1,1),'inconclusive'),((8,18,18,1,4),'inconclusive')]
    for args,want in examples: check(classify(*args)==want,'cap_examples')
    for args in [(0,1,1,1,1),(-1,1,1,1,1),(True,1,1,1,1),
                 (Q(1,2),1,1,1,1),(1,0,1,1,1),(1,1,-1,1,1),
                 (1,1,1,0,1),(1,1,1,1,0)]:
        rejected=False
        try: classify(*args)
        except ValueError: rejected=True
        check(rejected,'invalid_input_rejection')
    for m,h,shear in product((Q(1),Q(7,3),Q(5)),(Q(1,2),Q(6,5),Q(3)),
                              (Q(-4),Q(-1,3),Q(0),Q(9,2))):
        for a,b in combinations(range(-3,4),2):
            u=(shear+a*m,h);v=(shear+b*m,h)
            uu,vv,uv=dot(u,u),dot(v,v),dot(u,v)
            distance=dot(tuple(x-y for x,y in zip(u,v)),tuple(x-y for x,y in zip(u,v)))
            n=abs(a-b);area=m*h;p=integer_cap(uu);q=integer_cap(vv)
            check(uu*vv-uv*uv==determinant(u,v)**2==n*n*area*area,'gram_identity')
            check(distance==n*n*m*m,'difference_identity')
            r=p*p*q*q-n*n*area*area
            check(r>=0,'cap_discriminant')
            excess=distance-p*p-q*q
            check(excess<=0 or (excess/2)**2<=r,'upper_bound_control')
            check(distance<(p+q)**2,'strict_triangle_control')
            check(classify(n,p,q,area,m-Q(1,100))=='inconclusive',
                  'no_false_positive_below_actual_length')
            status=classify(n,p,q,area,4)
            check(status not in ('strict','at_most') or m<=4,'four_certificate_sound_on_controls')
            check(status!='strict' or m<4,'strict_certificate_sound_on_controls')
    lists=[((-4,-1,2,5),(3,8,4,9)),((0,0,2,8),(4,3,6,18)),
           ((-3,0,7,20),(12,6,9,24)),((1,2,3,4),(6,6,6,6))]
    for slopes,caps in lists:
        optimum,i,j=pair_optimum(slopes,caps)
        t=[Q(0) for _ in slopes];t[i]=Q(1,slopes[i]-slopes[j]);t[j]=-t[i]
        check(sum(t)==0 and dot(slopes,t)==1,'pair_attainment_constraints')
        check(dot(caps,[abs(x) for x in t])==optimum,'pair_attainment_cost')
        for r in product(range(-2,3),repeat=4):
            moment=dot(slopes,r)
            if sum(r) or not moment: continue
            weights=[Q(x,moment) for x in r]
            positives=[i for i in range(4) if weights[i]>0]
            negatives=[j for j in range(4) if weights[j]<0]
            mass=sum(weights[i] for i in positives)
            edges=[(i,j,-weights[i]*weights[j]/mass) for i in positives for j in negatives]
            check(sum(w*(slopes[i]-slopes[j]) for i,j,w in edges)==1,'coupling_moment')
            cost=dot(caps,[abs(x) for x in weights])
            check(sum(w*(caps[i]+caps[j]) for i,j,w in edges)==cost,'coupling_cost')
            check(cost>=optimum,'pair_optimality_controls')
        check(pair_optimum([x+7 for x in slopes],caps)[0]==optimum,'slope_shift_invariance')
        check(pair_optimum([-x for x in slopes],caps)[0]==optimum,'slope_sign_invariance')
    m=Q(5);h=Q(6,5);c=8
    check(4<m<=6-Q(7,c),'numerical_model')
    check(c*m+h<=6*(c-1),'numerical_model')
    check(h<=5*c-6 and m*h<=9*c*(1-Q(1,c))**2,'numerical_model')
    for p,q in product(range(-10,11),repeat=2):
        if p or q:check(dot((m*p,h*q),(m*p,h*q))>=h*h,'finite_systole_controls')
    for c in range(1,101):check((6-Q(7,c)<=4)==(c<=3),'crossing_threshold')
    for c,g in product(range(1,101),range(31)):
        check((3+Q(6*g-6,c)<=4)==(c>=6*g-6),'adequate_threshold')
    for n in range(2,101):
        below,at,above=[4-Q(1,n)+Q(1,k) for k in (n-1,n,n+1)]
        check(below>4 and at==4 and above<4,'limit_quantifier_controls')
    # Six independently evaluated witnesses against the author's six corrupted formulas.
    check((-1)**2>=0 and classify(1,1,1,1,1)=='inconclusive','rejected_corruptions')
    check(dot((1,-1),(1,-1))>1,'rejected_corruptions')
    check(5**4-2**4*12**2<0 and classify(2,5,5,12,4)=='at_most','rejected_corruptions')
    check(pair_optimum((0,1),(1,1))[0]>1,'rejected_corruptions')
    check(dot((4,0),(4,0))==16 and classify(2,5,5,12,4)=='at_most','rejected_corruptions')
    check(4-Q(1,10)+Q(1,9)>4,'rejected_corruptions')
    if sum(counts.values())!=10768: raise RuntimeError('Unexpected reconstructed count')
    return dict(sorted(counts.items()))


def supplementary():
    counts=Counter();check=lambda v,k:demand(v,k,counts)
    # Independent LP-dual feasibility witnesses over rational, repeated and unsorted slopes.
    for slopes in product((Q(-2),Q(0),Q(1,2),Q(3)),repeat=3):
        if len(set(slopes))<2:continue
        for caps in product((Q(1,3),Q(2),Q(5)),repeat=3):
            bound,_,_=pair_optimum(slopes,caps)
            lower=max(-p-bound*a for a,p in zip(slopes,caps))
            upper=min(p-bound*a for a,p in zip(slopes,caps))
            check(lower<=upper,'lp_dual_interval_feasibility')
            intercept=(lower+upper)/2
            check(all(abs(intercept+bound*a)<=p for a,p in zip(slopes,caps)),
                  'lp_dual_cap_constraints')
    # R=0 and negative/zero/positive target comparison, with exact Pythagorean examples.
    for p,q,hyp in ((3,4,5),(5,12,13),(8,15,17),(7,24,25)):
        for n in range(1,10):
            check(classify(n,p,q,Q(p*q,n),Q(hyp,n))=='at_most','orthogonal_equality')
            check(classify(n,p,q,Q(p*q,n),Q(hyp,n)-Q(1,100))=='inconclusive','orthogonal_below')
            check(classify(n,p,q,Q(p*q,n),Q(hyp,n)+Q(1,100))=='strict','orthogonal_above')
    check(classify(2,5,5,12,4)=='at_most','nonorthogonal_sharp_example')
    check(Q(376)**2>4*22032 and Q(7929,25)<324,'published_area_example')
    for n in range(1,50):
        check(classify(n,1,1,Q(1,n)+Q(1,100),4)=='inconsistent_inputs','area_inconsistency')
    return dict(sorted(counts.items()))


def run():
    original=rebuild();extra=supplementary()
    return {'problem_id':2809,'status':'PASS','author_domain_rebuilt_checks':sum(original.values()),
            'author_domain_counts':original,'supplementary_checks':sum(extra.values()),
            'supplementary_counts':extra,'author_code_imported':False,
            'optimized_mode_disables_checks':False,'target_resolved':False,
            'scope':'Finite rational algebra and independent dual witnesses; no topology certification.'}

if __name__=='__main__': print(json.dumps(run(),indent=2,sort_keys=True))
