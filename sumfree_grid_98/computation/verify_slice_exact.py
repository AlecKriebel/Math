from pathlib import Path
"""Independent exact-rational certificate for Keevash-Lim Lemma 3.1, d=4..200.
SciPy supplies candidate locations only. Every accepted bracket and inequality is
checked with Python integers/Fraction; numerical root guesses are not trusted.
"""
from fractions import Fraction as F
from math import comb, factorial
import json, time
from scipy.optimize import brentq
from scipy.stats import irwinhall

def density(d,x):
    if x <= 0 or x >= d: return F(0)
    p,q=x.numerator,x.denominator
    total=sum((-1)**j*comb(d,j)*(p-j*q)**(d-1) for j in range(min(d,p//q)+1))
    return F(total, factorial(d-1)*q**(d-1))

def interval_density(d,a,b):
    vals=[density(d,a),density(d,b)]
    low=min(vals); high=max(vals)
    if a<=F(d,2)<=b: high=density(d,F(d,2))
    return low,high

def verify(d):
    guess=brentq(lambda u: irwinhall.pdf(u,d)-2*irwinhall.pdf(2*u,d),d/4,d/2)
    q=2**35; p=int(guess*q); radius=1
    while True:
        a,b=F(p-radius,q),F(p+1+radius,q)
        ga=density(d,a)-2*density(d,2*a)
        gb=density(d,b)-2*density(d,2*b)
        if ga<0<gb: break
        radius*=2
        if radius>q: raise RuntimeError('Root bracket failed')
    # Unimodality gives enclosures at every point in each interval.
    low_u,high_u=interval_density(d-1,a,b)
    low_um,high_um=interval_density(d-1,a-1,b-1)
    low_2u,high_2u=interval_density(d-1,2*a,2*b)
    low_2um,high_2um=interval_density(d-1,2*a-1,2*b-1)
    assert low_um>0
    A=low_2um/high_um
    B=low_u/(2*high_um+4*high_2u)
    assert A>=F(201,100), (d,'A')
    assert B>=F(100,99), (d,'B')
    return dict(d=d, bracket=[str(a),str(b)], exact_endpoint_signs=[-1,1],
                A_lower_display=float(A), B_lower_display=float(B),
                lemma_3_1_exact_comparisons_pass=True)

if __name__=='__main__':
    start=time.time(); rows=[]
    for d in range(4,201):
        row=verify(d); rows.append(row)
        if d%20==0: print(d, row['A_lower_display'], row['B_lower_display'],flush=True)
    result={'method':'Exact rational density formula, strict endpoint signs and unimodality bounds',
            'dimensions':rows, 'all_pass':True, 'seconds':time.time()-start}
    with open(Path(__file__).with_name('EXACT_SLICE_RESULTS.json'),'w') as f: json.dump(result,f,indent=2)
    print('PASS',len(rows),'dimensions',result['seconds'])

# Auxiliary certification of the few real-number inequalities used in the
# analytic tail, avoiding reliance on printed decimal approximations.
def exp_bounds(x,terms=100):
    assert x>=0
    term=F(1); total=term
    for k in range(1,terms+1):
        term=term*x/k; total+=term
    next_term=term*x/(terms+1)
    ratio=x/(terms+2)
    assert ratio<1
    return total,total+next_term/(1-ratio)

def verify_analytic_tail():
    records=[]
    for lam in [F(3),F(8,5)]:
        elo,ehi=exp_bounds(lam)
        # h(E)=E/(E-1)^2 is decreasing for E>1.
        mu_lo=1/lam-1/(elo-1); mu_hi=1/lam-1/(ehi-1)
        var_hi=1/(lam*lam)-ehi/(ehi-1)**2
        delta=F(1,3)-mu_hi if lam==3 else mu_lo-F(1,3)
        assert delta>0
        assert 200*delta-1>0
        assert (200*delta-1)**2 > 600*var_hi
        records.append({'tilt_magnitude':str(lam),'dimension_200_window_pass':True})
    assert exp_bounds(9*F(77,1000))[1]<2
    assert exp_bounds(F(24,5)*F(145,1000))[0]>2
    assert exp_bounds(F(4,5))[0]>F(201,100)
    upper=2/exp_bounds(F(8,5))[0]+4/exp_bounds(F(8,5)*(1+3*F(77,1000)))[0]
    assert upper<F(99,100)
    # d=3: root is within [1.11,1.12]; bounds are deliberately coarse.
    a,b=F(111,100),F(28,25)
    assert density(3,a)-2*density(3,2*a)<0
    assert density(3,b)-2*density(3,2*b)>0
    assert (3-2*b)>=F(201,100)*(b-1)
    assert F(99,100)*(2-b)>=2*(b-1)
    return {'analytic_tail_d_ge_201_pass':True,'dimension_3_pass':True,
            'tilt_checks':records,'ratio_sum_upper_display':float(upper)}

if __name__=='__main__':
    analytic=verify_analytic_tail()
    with open(Path(__file__).with_name('ANALYTIC_CONSTANTS_RESULTS.json'),'w') as f: json.dump(analytic,f,indent=2)
    print(analytic)
