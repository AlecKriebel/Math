"""Stdlib-only fail-closed independent check. No assertions or numerical libraries.
Input is untrusted rational root brackets; ignores all saved PASS/display fields.
"""
from fractions import Fraction as Q
from math import comb, factorial
from pathlib import Path
import argparse, json


def require(test, message):
    if not test:
        raise ValueError(message)


def f(d, x):
    require(d >= 2, 'density dimension')
    x = Q(x)
    if x <= 0 or x >= d:
        return Q(0)
    # Reflection reduces both cancellation and computation; exact throughout.
    x = min(x, d-x)
    p, q = x.numerator, x.denominator
    numerator = 0
    for j in range(p//q+1):
        numerator += (-1 if j % 2 else 1)*comb(d,j)*(p-q*j)**(d-1)
    result = Q(numerator, factorial(d-1)*q**(d-1))
    require(result > 0, 'interior density positivity')
    return result


def enclose(d, a, b):
    require(a <= b, 'ordered interval')
    ends = [f(d,a), f(d,b)]
    return min(ends), max(ends+[f(d,Q(d,2))] if a<=Q(d,2)<=b else ends)


def check_bracket(d, a, b):
    require(Q(d,4) <= a < b <= Q(d,2), f'd={d}: bracket domain')
    require(f(d,a) < 2*f(d,2*a), f'd={d}: left sign')
    require(f(d,b) > 2*f(d,2*b), f'd={d}: right sign')
    lu, hu = enclose(d-1,a,b)
    lm, hm = enclose(d-1,a-1,b-1)
    l2, h2 = enclose(d-1,2*a,2*b)
    l2m, h2m = enclose(d-1,2*a-1,2*b-1)
    require(lm>0, f'd={d}: positive denominator')
    require(100*l2m >= 201*hm, f'd={d}: first margin')
    require(99*lu >= 100*(2*hm+4*h2), f'd={d}: second margin')
    return {'d':d, 'bracket':[str(a),str(b)], 'A_lower_display':float(l2m/hm),
            'B_lower_display':float(lu/(2*hm+4*h2))}


def exact_bisect(d, steps=40):
    a,b=Q(d,4),Q(d,2)
    for _ in range(steps):
        m=(a+b)/2
        g=f(d,m)-2*f(d,2*m)
        require(g != 0, 'exact rational root found: handle separately')
        if g<0: a=m
        else: b=m
    return a,b


def exponential(x, n=80):
    require(0<=x<n+2,'exponential tail domain')
    total=term=Q(1)
    for k in range(1,n+1):
        term *= x/k
        total += term
    return total, total+term*x/(n+1)/(1-x/(n+2))


def check_tail():
    output=[]
    for lam in [Q(3),Q(8,5)]:
        lower,upper=exponential(lam)
        mu_low=1/lam-1/(lower-1)
        mu_high=1/lam-1/(upper-1)
        var_high=1/lam**2-upper/(upper-1)**2
        delta=Q(1,3)-mu_high if lam==3 else mu_low-Q(1,3)
        require(delta>0 and var_high>0,'tilted moments')
        require(200*delta>1,'window sign')
        require((200*delta-1)**2>600*var_high,'dimension-200 mode window')
        output.append({'lambda':str(lam), 'window_pass':True})
    amin,amax=Q(77,1000),Q(145,1000)
    require(exponential(9*amin)[1]<2,'alpha lower')
    require(exponential(Q(24,5)*amax)[0]>2,'alpha upper')
    # The initial alpha bootstrap uses x=d/3-1, y=d/3+1/2.
    require(exponential(Q(12,5))[0]>2,'alpha bootstrap')
    offsets=[Q(1,3)+amin,Q(1,3)+amax,amin-Q(2,3),amax-Q(2,3),
             Q(1,3)-2*amin,Q(1,3)-2*amax,-Q(2,3)-2*amin,-Q(2,3)-2*amax]
    require(all(-1<=x<=1 for x in offsets),'all reflected evaluation points in mode window')
    require(1-3*amax>Q(1,2),'first ratio distance')
    require(exponential(Q(4,5))[0]>Q(201,100),'first tail ratio')
    ratio=2/exponential(Q(8,5))[0]+4/exponential(Q(8,5)*(1+3*amin))[0]
    require(ratio<Q(99,100),'second tail ratio')
    return {'mode_windows':output,'ratio_upper_display':float(ratio)}


def check_hubs():
    checked=0
    for d in range(3,13):
        for n in range(1,31):
            for r in range(d*n+1):
                lo,hi=max(0,r-(d-1)*n),min(n,r)
                h=0 if r<=n else max(0,r-(d-2)*n) if r<=(d-1)*n else n
                require(lo<=h<=hi,'hub membership')
                require(0<=r-hi-h and r-lo-h<=(d-2)*n,'all hub edges')
                checked+=1
    return checked


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--brackets',type=Path,default=Path(__file__).with_name('EXACT_SLICE_RESULTS.json'))
    args=parser.parse_args()
    records=json.loads(args.brackets.read_text())['dimensions']
    require(len(records)==197,'exactly 197 bracket records required')
    require([r['d'] for r in records]==list(range(4,201)),'dimension sequence must be exactly 4..200')
    checked=[check_bracket(r['d'],*[Q(x) for x in r['bracket']]) for r in records]
    # Fresh exact search independently tests the two transition dimensions.
    endpoints=[check_bracket(d,*exact_bisect(d)) for d in [3,200,201]]
    # Cross-check the density against the correct B-spline recurrence,
    # including integer knots and support endpoints (base d=2 is triangular).
    for d in range(3,13):
        for j in range(-1,3*d+2):
            x=Q(j,3)
            require((d-1)*f(d,x)==x*f(d-1,x)+(d-x)*f(d-1,x-1),'density recurrence')
    result={'all_pass':True,'saved_brackets_verified':len(checked),'fresh_endpoint_checks':endpoints,
            'tail':check_tail(),'hub_cases':check_hubs(),
            'smallest_A_d':min(checked,key=lambda r:r['A_lower_display'])['d'],
            'smallest_B_d':min(checked,key=lambda r:r['B_lower_display'])['d']}
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
