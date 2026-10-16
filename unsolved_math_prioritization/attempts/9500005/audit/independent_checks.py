#!/usr/bin/env python3
"""Independent finite exact checks of the retained partials; never a stochastic proof."""
from fractions import Fraction as F
from math import factorial, comb
import json
import os


def need(ok, label):
    if not ok:
        raise RuntimeError(label)


def dot(v, w):
    return sum((a*b for a,b in zip(v,w)), F(0))


def sub(v, w):
    return tuple(a-b for a,b in zip(v,w))


def circle(r, t):
    return (r*(1-t*t)/(1+t*t), r*2*t/(1+t*t))


def cmul(v, w):
    return (v[0]*w[0]-v[1]*w[1], v[0]*w[1]+v[1]*w[0])


def inv(z):
    q=dot(z,z)
    need(q>0,'inverse domain')
    return (z[0]/q,-z[1]/q)


def disk_moment(i, j):
    if i%2 or j%2:
        return F(0)
    a,b=i//2,j//2
    return F(factorial(2*a)*factorial(2*b),4**(a+b)*factorial(a)*factorial(b)*factorial(a+b+1))


def derivative(p, axis):
    q={}
    for power,c in p.items():
        if power[axis]:
            k=list(power); k[axis]-=1; k=tuple(k)
            q[k]=q.get(k,F(0))+power[axis]*c
    return q


def expectation(p):
    return sum((c*disk_moment(*k) for k,c in p.items()), F(0))


def main():
    counts={'boundary_pairs':0,'radial_coefficients':0,'inversion_covariances':0,
            'harmonic_log_traces':0,'controlled_times':0,'even_power_moments':0,
            'finite_state_stationarity_checks':0,'semantic_witnesses':0}
    for r in map(F, ['1/3','2/5','1','7/3']):
        xs=[circle(r,F(k,5)) for k in range(-4,5)]+[(-r,F(0))]
        for x in xs:
            for s in map(F,['1','6/5','2','5']):
                for t in [F(k,7) for k in range(-3,4)]+[None]:
                    y=tuple(s*v for v in (circle(r,t) if t is not None else (-r,F(0))))
                    z=sub(x,y); d2=dot(z,z)
                    if not d2: continue
                    yy=dot(y,y); n=tuple(v/r for v in x)
                    actual=dot(z,n)
                    need(2*r*actual==d2+r*r-yy,'distance boundary polarization')
                    need(actual<=d2/(2*r),'uniform exterior ball inequality')
                    counts['boundary_pairs']+=1
                    for a in map(F,['-1','0','1/4','1/2','3/4','2']):
                        lhs=actual/d2-a/r
                        rhs=F(1,2)/r-a/r+(r*r-yy)/(2*r*d2)
                        need(lhs==rhs,'radial correction coefficient')
                        if a>=F(1,2): need(lhs<=0,'radial sign')
                        if yy==r*r: need((lhs<=0)==(a>=F(1,2)),'sharp radial threshold')
                        counts['radial_coefficients']+=1
                    # Use the two real Jacobian columns, rather than a modulus-only calculation.
                    ix2=cmul(inv(x),inv(x)); iy2=cmul(inv(y),inv(y))
                    h=tuple(r*r*(b-a) for a,b in zip(ix2,iy2))
                    col1=h; col2=(-h[1],h[0])
                    covariance=(col1[0]**2+col2[0]**2,col1[1]**2+col2[1]**2,
                                col1[0]*col1[1]+col2[0]*col2[1])
                    total=tuple(a+b for a,b in zip(x,y))
                    factored=r**4*d2*dot(total,total)/(dot(x,x)**2*yy**2)
                    need(covariance==(factored,factored,F(0)),'inverted covariance matrix')
                    counts['inversion_covariances']+=1
                    for v in (x,y):
                        q=dot(v,v)
                        trace=sum((F(1)/q-2*w*w/q**2 for w in v),F(0))
                        need(trace==0,'two-dimensional logarithm harmonicity')
                        counts['harmonic_log_traces']+=1
    for k in range(101):
        t=F(k,100)
        X=(F(1),F(0)); Y=(-2-t,F(0)); B=(-t,F(0))
        need(X==(1+B[0]+t,B[1]),'expanding X equation')
        need(Y==(-2+B[0],B[1]),'expanding Y equation')
        need(dot(sub(X,Y),sub(X,Y))==(3+t)**2,'expansion separation')
        for p in (X,Y):
            need(1<=dot(p,p)<=100 and dot(sub(p,(F(4),F(4))),sub(p,(F(4),F(4))))>=F(1,4),'two-hole membership')
        Ly=max(F(0),t-F(1,2)); Y=(F(3,2)-t+Ly,F(0))
        need(Y[0]==max(F(1),F(3,2)-t),'contracting equation')
        need(Ly==0 or Y==(F(1),F(0)),'boundary support')
        need(dot(sub(X,Y),sub(X,Y))==max(F(0),F(1,2)-t)**2,'contracting distance')
        counts['controlled_times']+=1
    # Normalized cos^{2m} integral is b_m = binomial(2m,m)/4^m.
    # Independently obtain b_m by the integration-by-parts recurrence.
    b=F(1); cumulative=F(0)
    for m in range(1,129):
        cumulative+=b
        b*=F(2*m-1,2*m)
        need(b==F(comb(2*m,m),4**m),'cosine moment recurrence')
        need(cumulative==2*m*b,'J(2m) telescoping identity')
        counts['even_power_moments']+=1
    u={(1,0):F(3),(3,0):F(-1),(1,2):F(-1)}
    dx=derivative(u,0); dy=derivative(u,1)
    need(expectation(u)==0,'disk mean u')
    need((expectation(dx),expectation(dy))==(2,0),'disk mean gradient')
    lap_mean=expectation(derivative(dx,0))+expectation(derivative(dy,1))
    product_generator=lap_mean*expectation(u)+expectation(dx)**2+expectation(dy)**2
    need(product_generator==4,'product uniform is not invariant')
    # Verify the Neumann polynomial identity coefficientwise.
    radial={}
    for axis,p in enumerate((dx,dy)):
        for k,c in p.items():
            kk=list(k);kk[axis]+=1;kk=tuple(kk)
            radial[kk]=radial.get(kk,F(0))+c
    need(radial=={(1,0):F(3),(3,0):F(-3),(1,2):F(-3)},'Neumann factor 3*x*(1-r^2)')
    # Finite-state model tests the measure telescoping algebra, not the Brownian criterion.
    matrix=((F(1,2),F(1,2)),(F(1,4),F(3,4)))
    law=(F(1),F(0)); f=(F(-2),F(3)); initial=law; summed=(F(0),F(0))
    for T in range(1,65):
        summed=tuple(a+b for a,b in zip(summed,law))
        law=tuple(sum((initial_value*matrix[i][j] for i,initial_value in enumerate(law)),F(0)) for j in range(2))
        avg=tuple(v/T for v in summed)
        pf=tuple(dot(row,f) for row in matrix)
        lhs=dot(avg,sub(pf,f)); rhs=(dot(law,f)-dot(initial,f))/T
        need(lhs==rhs,'occupation telescoping identity')
        need(abs(lhs)<=2*max(map(abs,f))/T,'occupation endpoint bound')
        counts['finite_state_stationarity_checks']+=1
    # Exact witnesses rejecting shortcuts rather than claims about Brownian trajectories.
    need(F(1,2)-F(1,4)>0,'a=1/4 fails sign threshold');counts['semantic_witnesses']+=1
    need((F(1,4)-F(1,9))**2==F(25,1296)>0,'inversion has nonzero difference covariance');counts['semantic_witnesses']+=1
    need(F(1,16)!=F(1,81),'individual inverted clocks differ');counts['semantic_witnesses']+=1
    need(product_generator!=0,'uniform marginals do not imply product invariance');counts['semantic_witnesses']+=1
    for n in (2,10,100,1000):
        need(-F(n,n*n)==-F(1,n),'zero-rate decaying scalar model')
        need(F(0,n*n)==0,'zero-rate constant scalar model')
    counts['semantic_witnesses']+=1
    partial=F(0)
    for n in range(1,101):
        partial+=F(2,3)*F(1,2**(n+3))
        need(partial<F(1,12),'sparse peak total squared integral bound')
    counts['semantic_witnesses']+=1
    print(json.dumps({'result':'PASS','uid':os.getuid(),'counts':counts,
      'arithmetic':'exact rational, independent implementation',
      'scope':'finite algebra and logical counter-witnesses; no simulation or infinite-horizon proof'},sort_keys=True))


if __name__=='__main__':
    main()
