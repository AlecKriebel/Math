"""Own alternative certificate: Machin identity and alternating range reduction.

Authored after the independent early seal and before supplied checker reads.
Only exact integers/Fractions; no source programs or foreign code imported.
The all-time analytic argument is in DERIVATION.md, not inferred from samples.
"""
from fractions import Fraction as F
from math import factorial, isqrt
import argparse
import json
import sys


def require(ok, tag):
    if not ok:
        raise ValueError(tag)


def atan_bounds(q):
    partial=sum(((-1)**j*q**(2*j+1)/F(2*j+1) for j in range(24)), F(0))
    return partial,partial+q**49/F(49)


def exp_negative_bounds(x):
    require(x>=0, 'nonnegative exponential argument')
    q=x/32
    require(q<=1, 'alternating terms decrease')
    upper=sum(((-q)**j/F(factorial(j)) for j in range(13)), F(0))
    lower=upper-q**13/F(factorial(13))
    require(0<lower<=upper, 'positive alternating enclosure')
    return lower**32,upper**32


def sqrt_upper(x):
    scale=2**40
    floor=isqrt((x.numerator*scale*scale)//x.denominator)
    require(F(floor*floor,scale*scale)<=x<F((floor+1)**2,scale*scale),
            'integer square-root bracket')
    return F(floor+1,scale)


def coarse_upper(x,scale=10**12):
    ceiling=(x.numerator*scale+x.denominator-1)//x.denominator
    y=F(ceiling,scale)
    require(x<=y, 'outward rational rounding')
    return {'numerator':y.numerator,'denominator':y.denominator}


def verify(mutant):
    al,au=atan_bounds(F(1,5));bl,bu=atan_bounds(F(1,239))
    pi_lo,pi_hi=16*al-4*bu,16*au-4*bl
    # tan(4atan(1/5))=120/119; subtraction of atan(1/239) has tangent1.
    tangent=(F(120,119)-F(1,239))/(1+F(120,119)*F(1,239))
    require(tangent==1, 'Machin exact tangent identity')
    require(F(1772,1000)**2<pi_lo and pi_hi<F(1773,1000)**2,
            'strict square-root-pi brackets')
    eminuse_lo,eminuse_hi=exp_negative_bounds(F(1))
    e_lo,e_hi=1/eminuse_hi,1/eminuse_lo
    require(e_hi<F(2719,1000), 'strict e upper bound')
    require(1+F(8,3)/(e_lo**3)<2, 'each cap radial integral below two')
    # Unitary conjugation and volume normalization are exact exponent algebra.
    U=F(1,2) if mutant=='unitary_exponent' else F(3,4)
    require(U-F(5,4)==-F(1,2) and F(1,4)-U==-F(1,2),
            'exact weighted-operator conjugation')
    normalization_power=F(3,2) if mutant=='normalization' else F(2,3)
    require(F(3,2)*normalization_power==1, 'volume normalization exponent')
    time_power=-1 if mutant=='time_rescale' else 1
    require(time_power-1==0, 'time cancels constant metric rescaling')
    require(4*2*2==16, 'time and volume prefactor')
    lower=F(1772,2719)*F(10000000-7092,10004000)
    require(lower==F(1106714561,1700054750), 'literal finite lower fraction')
    threshold=F(2,3) if mutant=='lower_threshold' else F(13,20)
    require(lower>threshold, 'strict weighted lower gap')
    require(lower-F(13,20)==F(3357947,3400109500), 'literal weighted margin')
    small_end=F(25) if mutant=='smalltime_sign' else F(7,5)
    require(small_end<2*pi_lo*pi_lo, 'small-time Poisson correction sign')
    small_bound=F(1773,4000)/exp_negative_bounds(F(7,20))[0]
    require(small_bound<F(629002,10**6), 'literal small-time table ceiling')
    endpoints=[F(7,5),F(3,2),F(8,5),F(17,10),F(9,5),F(19,10),F(2)]
    ceilings=[631338,636143,639464,641172,641202,639541]
    rows=[]
    tail_factor=9 if mutant=='tail_factor' else 18
    for a,b,ceiling in zip(endpoints,endpoints[1:],ceilings):
        r=F(16,9)*exp_negative_bounds(7*a)[1]
        require(r<F(1,2), 'Gaussian multiplicity tail ratio')
        require(tail_factor>=F(9)/(1-r), 'valid infinite geometric tail factor')
        aterm=b*sqrt_upper(b)*exp_negative_bounds(F(3,4)*b)[1]
        bterm=a*sqrt_upper(a)*(4*exp_negative_bounds(F(15,4)*a)[1]
                  +tail_factor*exp_negative_bounds(F(35,4)*a)[1])
        bound=aterm+bterm
        ceiling=630000 if mutant=='round_ceiling' else ceiling
        require(bound<F(ceiling,10**6), 'literal interval table ceiling')
        rows.append({'a':str(a),'b':str(b),'independent_upper':coarse_upper(bound),
                     'literal_table_ceiling':{'numerator':ceiling,'denominator':10**6}})
    require(F(641202,10**6)<F(321,500)<F(129,200), 'literal round gap')
    require(F(128)>pi_hi*e_hi**3, 'round interior value exceeds zero-time limit')
    require(F(13,20)>F(1773,4000), 'weighted value exceeds zero-time limit')
    return {'status':'PASS','optimization':sys.flags.optimize,'mutant':mutant,
        'method':'Machin16atan(1/5)-4atan(1/239), alternating13/12 degree exp(-x/32) then32nd powers, 2^40 square-root brackets',
        'small_time_upper':coarse_upper(small_bound),'intervals':rows,
        'weighted_lower':str(lower),'weighted_margin':str(lower-F(13,20)),
        'round_upper':str(F(641202,10**6)),
        'separation_lower_minus_round_upper':str(lower-F(641202,10**6)),
        'finite_certificate_not_geometry_or_spectral_proof':True}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--mutant',default='none',choices=['none','unitary_exponent',
      'normalization','time_rescale','lower_threshold','smalltime_sign',
      'tail_factor','round_ceiling'])
    args=parser.parse_args()
    try:
        answer=verify(args.mutant)
    except ValueError as error:
        print(json.dumps({'status':'REJECT','optimization':sys.flags.optimize,
                         'mutant':args.mutant,'tag':str(error)}))
        sys.exit(1)
    print(json.dumps(answer,indent=2))
