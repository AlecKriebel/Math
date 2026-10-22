#!/usr/bin/env python3
"""Independent exact iterated polynomial quadrature of defining discrepancy.

No supplied verification module is imported. Split z at k/m for m<=n-1;
within each strip the Delta wrap endpoints are affine with fixed order. Between
consecutive Delta cuts, sorted points are affine. The x antiderivative has
total degree p+1, and Delta integration raises the possible z degree to p+2.
Interior rational interpolation quadrature evaluates both integrals exactly.
"""
from fractions import Fraction as Q
from math import comb, factorial
import argparse, json

def require(condition, message):
    if not condition:
        raise ValueError(message)

def mul(a,b):
    c=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return c

def weights(count):
    nodes=[Q(2*i+1,2*count) for i in range(count)]
    out=[]
    for i,x in enumerate(nodes):
        polynomial=[Q(1)];denominator=Q(1)
        for j,y in enumerate(nodes):
            if j==i:continue
            polynomial=mul(polynomial,[-y,Q(1)]);denominator*=x-y
        out.append(sum(c/Q(k+1) for k,c in enumerate(polynomial))/denominator)
    for degree in range(count):
        require(sum(w*x**degree for x,w in zip(nodes,out))==Q(1,degree+1),'quadrature moments')
    return tuple(zip(nodes,out))

def segment_integral(n,p,z,delta):
    points=sorted((j*z+delta)%1 for j in range(n))
    ends=[Q(0)]+points+[Q(1)]
    return sum(((ends[k+1]-Q(k,n))**(p+1)-(ends[k]-Q(k,n))**(p+1))/Q(p+1) for k in range(n+1))

def shifted_integral(n,p,z,quadrature):
    cuts=sorted({Q(0),Q(1)}|{(1-j*z)%1 for j in range(n)})
    return sum((b-a)*sum(w*segment_integral(n,p,z,a+(b-a)*t) for t,w in quadrature) for a,b in zip(cuts,cuts[1:]))

def exact_moment(n,p):
    require(n>=1 and p>=2 and p%2==0,'valid model parameters')
    inner=weights(p+2);outer=weights(p+3)
    cuts=sorted({Q(0),Q(1)}|{Q(k,m) for m in range(1,n) for k in range(1,m)})
    value=sum((b-a)*sum(w*shifted_integral(n,p,a+(b-a)*t,inner) for t,w in outer) for a,b in zip(cuts,cuts[1:]))
    return value,len(cuts)-1

def iid_moment(n,p):
    value=Q(0)
    for k in range(n+1):
        for a in range(n-k+1):
            for b in range(p+1):
                value+=Q(comb(n,k)*comb(n-k,a)*(-1)**(a+b)*comb(p,b),k+a+b+1)*Q(k,n)**(p-b)
    return value

def energy_lattice(n):
    return sum(1 for a in range(n) for b in range(n) for c in range(n) for d in range(n) if a+b==c+d)

def energy_iid(n):
    count=0
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    exponents=[0]*n
                    for i in (a,b):exponents[i]+=1
                    for i in (c,d):exponents[i]-=1
                    count+=all(v==0 for v in exponents)
    return count

def run(force_wrong_identity=False):
    checks=0;values={};partitions={}
    def check(got,expected,label):
        nonlocal checks
        require(got==expected,label+': '+str(got)+' != '+str(expected));checks+=1
    expected={(1,2):Q(1,6),(2,2):Q(1,12),(3,2):Q(1,18),(4,2):Q(1,24),
              (1,4):Q(1,15),(2,4):Q(1,48),(3,4):Q(19,1620),(4,4):Q(139,17280)}
    if force_wrong_identity:expected[(3,4)]=Q(4,405)
    for (n,p),target in expected.items():
        value,cells=exact_moment(n,p);check(value,target,'direct defining moment '+str((n,p)))
        values[str((n,p))]=str(value);partitions[str((n,p))]=cells
        if n<=2 or p==2:check(value,iid_moment(n,p),'iid law/variance consistency '+str((n,p)))
    check(iid_moment(3,4),Q(4,405),'direct binomial n3')
    check(Q(values['(3, 4)'])-iid_moment(3,4),Q(1,540),'strict gap')
    check(Q(values['(3, 4)'])/iid_moment(3,4),Q(19,16),'ratio')
    for n in range(1,18):
        check(iid_moment(n,4),Q(3*n-1,30*n**3),'iid general fourth formula')
        check(iid_moment(n,2),Q(1,6*n),'iid general variance')
    for n in (1,2,3,4,5,7,12):
        check(energy_lattice(n),Q(2*n**3+n,3),'lattice Fourier energy')
        check(energy_iid(n),2*n*n-n,'iid Fourier energy')
    check(energy_lattice(3),19,'lattice energy n3');check(energy_iid(3),15,'iid energy n3')
    coefficient=Q(4,5)*Q(factorial(5)*factorial(0),factorial(7))
    check(coefficient,Q(2,105),'two-triangle coefficient')
    check(coefficient/Q(3)-iid_moment(4,4),Q(5,8064),'n4 lower-bound gap')
    for t in (Q(0),Q(1,7),Q(1),Q(19),Q(100000)):
        n=4+t
        check(4*n**3-21*n**2+28*n-7,25+52*t+27*t*t+4*t**3,'universal tail shifted polynomial')
    pi_upper=Q(22,7)
    c0=60*234**2+30-48*pi_upper**4*(3*234-1)
    c1=120*234-144*pi_upper**4;c2=Q(60)
    check(c0,Q(5975502,2401),'Fourier threshold certificate constant')
    require(min(c0,c1,c2)>0,'all-n Fourier polynomial positive');checks+=1
    check(segment_integral(3,4,Q(0),Q(0)),Q(1,5),'complete collision at zero')
    check(segment_integral(3,4,Q(0),Q(1,2)),Q(1,80),'complete collision at half')
    adverse={}
    for label,got,wrong in [('iid triple replacement',Q(values['(3, 4)']),Q(4,405)),
                            ('wrong full n4',Q(values['(4, 4)']),Q(2,315)),
                            ('false iid Fourier energy',energy_iid(3),energy_lattice(3)),
                            ('tail falsely sufficient at n3',coefficient/Q(2)>iid_moment(3,4),True),
                            ('n2 p4 false reversal',Q(values['(2, 4)'])>iid_moment(2,4),True),
                            ('dropped orientation',coefficient,Q(1,105))]:
        try:require(got==wrong,'deliberately false: '+label)
        except ValueError:adverse[label]='rejected'
        else:raise RuntimeError('ineffective adverse identity '+label)
    return {'status':'PASS','checks':checks,'adverse_checks':adverse,'exact_moments':values,'generator_intervals':partitions,
            'method':'Independent iterated exact interpolation quadrature; direct sorted-point definition; explicit exceptions',
            'fourier_energies_n3':{'lattice':energy_lattice(3),'iid':energy_iid(3)},
            'tail_coefficient':str(coefficient),'fourier_threshold_coefficients':[str(c0),str(c1),str(c2)],
            'finite_checks_supplement_explicit_universal_arguments':True}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--force-wrong-identity',action='store_true');args=parser.parse_args()
    print(json.dumps(run(args.force_wrong_identity),indent=2,sort_keys=True))
