"""Validated n=2 entropy midpoint integral using real mpmath interval operations.

The analytic error bound is proved in PASS3_VALIDATED_ENTROPY_QUADRATURE.md.
All inputs are exact decimal/rational strings; output enclosures are outward
rounded exact rational endpoints. No optimizer number is promoted to a proof.
"""
import argparse,json,math,time
from fractions import Fraction
from mpmath import iv
from pathlib import Path
iv.dps=45

def rational(s):
    q=Fraction(s);return iv.mpf(q.numerator)/q.denominator

def conj(z):return iv.mpc(z.real,-z.imag)
def nonnegative(v):return iv.mpf([max(0,v.a),max(0,v.b)])
def hull(x,y):return iv.mpf([min(x.a,y.a),max(x.b,y.b)])
def complex_hull(x,y):return iv.mpc(hull(x.real,y.real),hull(x.imag,y.imag))
def csqrt(z):
    """Rectangle enclosing a square root; ± suffices since both are used."""
    az=abs(z)
    x=iv.sqrt(nonnegative((az+z.real)/2))
    y=iv.sqrt(nonnegative((az-z.real)/2))
    if z.imag.a>=0:return iv.mpc(x,y)
    if z.imag.b<=0:return iv.mpc(x,-y)
    return iv.mpc(x,iv.mpf([-y.b,y.b]))

def phase(w,a,b):
    d=csqrt(w*w-4*a*b)
    roots=[(-w+d)/(2*a),(-w-d)/(2*a)]
    q0=a*a+b*b+w.real*w.real+w.imag*w.imag
    q1=a*conj(w)+b*w
    out=q0*iv.log(a)
    for r in roots:
        mag=abs(r)
        l0=iv.log(iv.mpf([max(1,mag.a),max(1,mag.b)]))
        if mag.b<=1:t=r
        elif mag.a>=1:t=1/conj(r)
        else:t=complex_hull(r,1/conj(r))
        out+=q0*l0-(q1*t).real-a*b/2*(t*t).real
    return out

def fraction_mpf(x):
    sign,man,exponent,bits=x
    return Fraction((-1 if sign else 1)*man)*(Fraction(2)**exponent)

def enclosure(v,digits=24):
    lo,hi=map(fraction_mpf,v._mpi_);den=10**digits
    l=lo.numerator*den//lo.denominator
    h=-((-hi.numerator*den)//hi.denominator)
    return {'lower':str(Fraction(l,den)),'upper':str(Fraction(h,den)),
            'decimal_lower':f'{l/den:.16g}','decimal_upper':f'{h/den:.16g}'}

def certify(c,a,b,signs,N):
    # Input values remain rational throughout normalization, avoiding sqrt.
    R=c+sum(a)+sum(b)
    cn=rational(str(c/R));an=[rational(str(v/R)) for v in a];bn=[rational(str(v/R)) for v in b]
    # Integrate the larger positive endpoint to improve the derivative bound.
    j=max(range(2),key=lambda k:a[k]);k=1-j
    L=an[k]+bn[k]
    M=L*L*(3-2*iv.log(an[j]))+L
    error=M*iv.pi**2/(3*N*N)
    acc=iv.mpf(0)
    for q in range(N):
        t=2*iv.pi*(iv.mpf(q)+rational('1/2'))/N
        z=iv.mpc(iv.cos(t),iv.sin(t));zi=conj(z)
        wp=cn+an[k]*z+bn[k]*zi
        wm=cn+an[k]*z+signs[k]*bn[k]*zi
        acc+=phase(wp,an[j],bn[j])-phase(wm,an[j],signs[j]*bn[j])
    quadrature=acc/N
    result=quadrature+iv.mpf([-error.b,error.b])
    return {'support_bound':str(R),'integrated_pair':j,'N':N,'interval_dps':iv.dps,
            'derivative_bound_each_sign':enclosure(M),
            'midpoint_average':enclosure(quadrature),'quadrature_error_upper':enclosure(error),
            'normalized_entropy_gap':enclosure(result),'unnormalized_entropy_gap':enclosure(result*rational(str(R*R))),
            'positive_certified':bool(result.a>0),'negative_certified':bool(result.b<0)}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--N',type=int,default=256)
    parser.add_argument('--output',default='quadrature_certificates.json');args=parser.parse_args()
    cases=[{'name':'intermediate_center_mixed_roots','c':'9/10','a':['1','4/5'],'b':['2/5','3/10'],'signs':[-1,1]},
           {'name':'dominant_endpoint_exact_crosscheck','c':'1','a':['4','1'],'b':['1','1/2'],'signs':[-1,1]},
           {'name':'unequal_ellipse_mixed_roots','c':'2/5','a':['1','7/8'],'b':['7/10','1/5'],'signs':[-1,1]}]
    output=[]
    for case in cases:
        t=time.time();res=certify(Fraction(case['c']),list(map(Fraction,case['a'])),list(map(Fraction,case['b'])),case['signs'],args.N)
        rec={'case':case,**res,'seconds':time.time()-t};output.append(rec);print(json.dumps(rec),flush=True)
    path=Path(__file__).parent/args.output;path.write_text(json.dumps(output,indent=2)+'\n')
