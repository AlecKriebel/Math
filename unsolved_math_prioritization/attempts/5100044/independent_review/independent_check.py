#!/usr/bin/env python3
"""Finite high-precision Euclidean diagnostics; not interval or universal proof.

Jacobi functions choose a known closed confocal pair. After the first point,
vertices are generated only by line/ellipse intersection and specular reflection.
No result file is read as an acceptance oracle. All checks survive Python -O.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import mpmath as mp


class VerificationError(Exception):
    pass


def require(condition, message):
    if condition is not True:
        raise VerificationError(message)


def finite(value, label='sample'):
    try:
        result=mp.mpf(value)
    except (TypeError, ValueError, OverflowError) as error:
        raise VerificationError(label+': not a real scalar') from error
    require(bool(mp.isfinite(result)),label+': nonfinite scalar')
    return result


def vector(value, label='point'):
    require(len(value)==2,label+': expected two coordinates')
    return (finite(value[0],label+' x'),finite(value[1],label+' y'))


def dot(p,q):
    return p[0]*q[0]+p[1]*q[1]


def det(p,q):
    return p[0]*q[1]-p[1]*q[0]


def add(p,q):
    return (p[0]+q[0],p[1]+q[1])


def sub(p,q):
    return (p[0]-q[0],p[1]-q[1])


def scale(p,factor):
    return (p[0]*factor,p[1]*factor)


def unit(p):
    p=vector(p)
    squared=finite(dot(p,p),'squared vector length')
    require(bool(squared>0),'zero vector')
    return scale(p,1/mp.sqrt(squared))


def area(points):
    require(len(points)>=3,'area needs at least three listed vertices')
    points=[vector(p,'area vertex') for p in points]
    return finite(mp.fsum(det(p,points[(j+1)%len(points)])
                          for j,p in enumerate(points))/2,'shoelace area')


def focal_area(points,focus):
    focus=finite(focus,'focus')
    inverse=[]
    for p in points:
        p=vector(p,'inverse vertex')
        z=(p[0]-focus,p[1])
        squared=finite(dot(z,z),'inversion denominator')
        require(bool(squared>0),'vertex coincides with inversion center')
        inverse.append(vector(scale(z,1/squared),'inverse point'))
    return area(inverse)


def relative_error(actual,expected):
    actual=finite(actual,'actual value')
    expected=finite(expected,'expected value')
    return finite(abs(actual-expected)/max(mp.mpf(1),abs(expected)),'relative error')


def small(value,tolerance,label):
    value=finite(value,label)
    require(bool(value>=0 and value<=tolerance),
            label+': '+mp.nstr(value,12)+' exceeds '+mp.nstr(tolerance,8))


def geometry(k,N,tau):
    k=finite(k,'modulus')
    require(bool(0<k<1),'modulus must lie strictly between zero and one')
    require(type(N) is int and N>=3,'N must be an integer at least three')
    require(type(tau) is int and 0<2*tau<N,'turning number outside forward range')
    require(math.gcd(N,tau)==1,'N must be the least period: gcd(N,tau) must equal one')
    k2=k*k
    kp=mp.sqrt((1-k)*(1+k))
    K=mp.ellipk(k2)
    v=2*K*tau/N
    h=mp.ellipfun('sn',v,k2)
    cv=mp.ellipfun('cn',v,k2)
    dv=mp.ellipfun('dn',v,k2)
    require(bool(h>0 and cv>0 and dv>0),'nonpositive canonical coordinate')
    g={'k':k,'kp':kp,'K':K,'v':v,'h':h,'cv':cv,'dv':dv,
       'a':dv/cv,'b':kp/cv,'N':N,'tau':tau}
    for name,value in g.items():
        finite(value,'geometry '+name)
    require(bool(g['a']>1 and g['b']>kp),'caustic not strictly nested')
    return g


def orbit(g,angle):
    a,b,beta=g['a'],g['b'],g['kp']
    p=(a*mp.cos(angle),b*mp.sin(angle))
    start=p
    # The caustic alpha=1, beta=kp maps to the unit circle.
    z=(p[0],p[1]/beta)
    zz=finite(dot(z,z),'external-point squared radius')
    require(bool(zz>1),'initial point is not outside caustic')
    foot=scale(z,1/zz)
    offset=scale((-z[1],z[0]),mp.sqrt(zz-1)/zz)
    candidates=[]
    for sign in (-1,1):
        t=add(foot,scale(offset,sign))
        contact=(t[0],beta*t[1])
        direction=unit(sub(contact,p))
        if finite(det(p,direction),'initial orientation')>0:
            candidates.append(direction)
    require(len(candidates)==1,'forward tangent branch not unique')
    direction=candidates[0]
    initial_direction=direction
    points=[]
    metrics={key:mp.mpf(0) for key in
             ('outer_residual','tangency_residual','unit_direction_residual')}
    winding=mp.mpf(0)
    minimum_return=mp.inf
    for index in range(g['N']):
        points.append(vector(p))
        metrics['outer_residual']=max(metrics['outer_residual'],
            abs(finite((p[0]/a)**2+(p[1]/b)**2-1,'outer residual')))
        normal=(-direction[1],direction[0])
        support=dot(normal,p)
        caustic_support=normal[0]**2+beta**2*normal[1]**2
        require(bool(finite(caustic_support)>0),'zero caustic support')
        metrics['tangency_residual']=max(metrics['tangency_residual'],
            abs(finite((support**2-caustic_support)/caustic_support,'tangency residual')))
        denominator=finite((direction[0]/a)**2+(direction[1]/b)**2,'intersection denominator')
        require(bool(denominator>0),'zero line/ellipse intersection denominator')
        step=finite(-2*(p[0]*direction[0]/a**2+p[1]*direction[1]/b**2)/denominator,'forward step')
        require(bool(step>0),'nonpositive collision step')
        q=vector(add(p,scale(direction,step)),'next collision')
        normalized_p=(p[0]/a,p[1]/b)
        normalized_q=(q[0]/a,q[1]/b)
        turn=finite(mp.atan2(det(normalized_p,normalized_q),dot(normalized_p,normalized_q)),'angular advance')
        require(bool(0<turn<mp.pi),'lost forward nested-caustic branch')
        winding+=turn
        if index+1<g['N']:
            distance=mp.sqrt(((q[0]-start[0])/a)**2+((q[1]-start[1])/b)**2)
            minimum_return=min(minimum_return,finite(distance,'earlier return distance'))
        outer_normal=(q[0]/a**2,q[1]/b**2)
        squared=finite(dot(outer_normal,outer_normal),'reflection normal squared')
        require(bool(squared>0),'zero reflection normal')
        direction=sub(direction,scale(outer_normal,2*dot(direction,outer_normal)/squared))
        metrics['unit_direction_residual']=max(metrics['unit_direction_residual'],
            abs(finite(dot(direction,direction)-1,'reflection norm residual')))
        # Renormalization only controls roundoff; the norm error is measured first.
        direction=unit(direction)
        p=q
    metrics['closure']=finite(mp.sqrt(((p[0]-start[0])/a)**2+((p[1]-start[1])/b)**2),'closure')
    metrics['direction_closure']=finite(mp.sqrt(dot(sub(direction,initial_direction),sub(direction,initial_direction))),'direction closure')
    metrics['winding_error']=finite(abs(winding/(2*mp.pi)-g['tau']),'winding error')
    metrics['minimum_earlier_return']=finite(minimum_return,'minimum earlier return')
    return points,metrics


def explicit_constant(g):
    k,kp,K,h,cv,dv=g['k'],g['kp'],g['K'],g['h'],g['cv'],g['dv']
    t=h*h
    q=cv*cv
    U=kp*kp+k*k*q*q
    W=kp*kp+k*k*q*(2-q)
    bracket=2*kp**4+5*k*k*kp*kp*q+k**4*q*q*(4-q)
    Lambda=U*bracket/(2*kp**4*W**3)
    C=g['b']*h*dv*cv**4
    CA=g['a']*g['b']*h*cv/dv
    nome=mp.exp(-mp.pi*mp.ellipk(kp*kp)/K)
    Q=nome**(g['N']//2)
    theta3=mp.jtheta(3,0,Q)
    theta4=mp.jtheta(4,0,Q)
    landenc=(g['N']//2*mp.pi/(2*K))**2*theta3**2*theta4**2
    return finite(4*CA*C*Lambda*landenc/kp,'explicit Fourier/Landen product')


def family(k,N,tau,phases,tolerance,target):
    g=geometry(k,N,tau)
    require(type(target) is bool,'target flag must be Boolean')
    if target:
        require(N%4==0,'target theorem requires least period divisible by four')
    products=[]
    sample_data=[]
    maxima={key:mp.mpf(0) for key in
            ('closure','direction_closure','outer_residual','tangency_residual',
             'unit_direction_residual','winding_error','reversal_error')}
    if target:
        maxima.update({'focus_equality_error':mp.mpf(0),'explicit_constant_error':mp.mpf(0)})
        expected=explicit_constant(g)
    else:
        expected=None
    for phase in phases:
        points,metrics=orbit(g,mp.pi*finite(phase,'phase'))
        for key,value in metrics.items():
            if key!='minimum_earlier_return':
                small(value,tolerance,key)
                maxima[key]=max(maxima[key],value)
        require(bool(metrics['minimum_earlier_return']>1000*tolerance),
                'finite diagnostic cannot resolve an earlier return')
        A=area(points)
        Ip=focal_area(points,g['k'])
        Im=focal_area(points,-g['k'])
        product=finite(A*Ip,'area product')
        require(bool(A>0 and Ip>0),'forward area unexpectedly nonpositive')
        products.append(product)
        reversed_points=list(reversed(points))
        reversal=max(relative_error(area(reversed_points),-A),
                     relative_error(focal_area(reversed_points,g['k']),-Ip),
                     relative_error(area(reversed_points)*focal_area(reversed_points,g['k']),product))
        small(reversal,tolerance,'reversal error')
        maxima['reversal_error']=max(maxima['reversal_error'],reversal)
        if target:
            focus=relative_error(Ip,Im)
            formula=relative_error(product,expected)
            small(focus,tolerance,'two focal inverse areas')
            small(formula,tolerance,'explicit product')
            maxima['focus_equality_error']=max(maxima['focus_equality_error'],focus)
            maxima['explicit_constant_error']=max(maxima['explicit_constant_error'],formula)
        # A dimension check at one sample in each target family.
        if target and not sample_data:
            for ratio in (mp.mpf('0.000001'),mp.mpf('1000000')):
                scaled=[scale(p,ratio) for p in points]
                small(relative_error(area(scaled),A*ratio**2),tolerance,'similarity ordinary area')
                small(relative_error(focal_area(scaled,g['k']*ratio),Ip/ratio**2),tolerance,'similarity inverse area')
                small(relative_error(area(scaled)*focal_area(scaled,g['k']*ratio),product),tolerance,'similarity product')
        sample_data.append({'phase_over_pi':str(phase),'product':product,
                            'minimum_earlier_return':metrics['minimum_earlier_return']})
    spread=finite((max(products)-min(products))/max(abs(p) for p in products),'relative product spread')
    if target:
        small(spread,tolerance,'target product spread')
        if N==4:
            small(max(abs(product-4) for product in products),tolerance,'four-period value')
    else:
        require(bool(spread>mp.mpf('1e-10')),'excluded-parity diagnostic did not resolve product variation')
    return {'k':mp.nstr(g['k'],35),'least_N':N,'turning_number':tau,
            'target':target,'samples':sample_data,'maxima':maxima,
            'relative_product_spread':spread,'explicit_constant':expected}


def repeated_label_control(tolerance):
    g=geometry(mp.mpf('0.8'),6,1)
    products=[]
    for phase in ('0','0.137','0.333','0.731'):
        points,metrics=orbit(g,mp.pi*mp.mpf(phase))
        small(metrics['closure'],tolerance,'negative-control closure')
        original=area(points)*focal_area(points,g['k'])
        repeated=points*2
        product=area(repeated)*focal_area(repeated,g['k'])
        small(relative_error(product,4*original),tolerance,'repeat-area product scaling')
        products.append(product)
    spread=finite((max(products)-min(products))/max(abs(p) for p in products),'repeated-label spread')
    require(bool(spread>mp.mpf('1e-10')),'repeated period-six control did not resolve variation')
    return {'least_period':6,'listed_vertices':12,'repetitions':2,
            'relative_product_spread':spread,
            'limitation':'Length twelve does not imply least period twelve.'}


def serialize(value):
    if isinstance(value,dict):
        return {key:serialize(item) for key,item in value.items()}
    if isinstance(value,list):
        return [serialize(item) for item in value]
    if isinstance(value,(mp.mpf,mp.mpc)):
        return mp.nstr(finite(value,'serialized value'),35)
    return value


def run(dps=90,stress=False):
    require(type(dps) is int and 60<=dps<=500,'dps must be between 60 and 500')
    require(type(stress) is bool,'stress flag must be Boolean')
    require(not stress or dps>=130,'--stress requires --dps at least 130')
    mp.mp.dps=dps
    tolerance=mp.power(10,-dps//2)
    cases=[('0.2',4,1),('0.8',4,1),('0.8',8,1),('0.8',8,3),
           ('0.2',12,5),('0.98',12,1),('0.8',16,7),('0.98',20,3)]
    if stress:
        cases += [('0.9999999999999999',12,5),
                  ('0.0000000000000001',12,5),('0.8',128,1),('0.8',128,63)]
    phases=['0','0.137','0.333','0.731']
    targets=[family(mp.mpf(k),N,tau,phases,tolerance,True) for k,N,tau in cases]
    excluded=[family(mp.mpf('0.8'),N,tau,phases,tolerance,False)
              for N,tau in ((3,1),(6,1),(10,3))]
    return serialize({'schema':'pr207-portable-geometric-diagnostic-v1','status':'PASS',
          'mpmath_version':mp.__version__,'precision_dps':dps,
          'optimization_level':sys.flags.optimize,'tolerance':tolerance,
          'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'target_families':targets,'wrong_parity_controls':excluded,
          'repeated_label_control':repeated_label_control(tolerance),
          'scope':'Finite floating-point diagnostics only; no interval enclosure, '
                  'universal proof, uniform conditioning as k tends to one or v '
                  'tends to zero, or novelty/priority conclusion. Output is '
                  'computed from identities and geometric propagation, never '
                  'accepted by loading stored PASS records.'})


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dps',type=int,default=90)
    parser.add_argument('--stress',action='store_true',help='optional thin-caustic/large-period diagnostics; needs dps>=130')
    parser.add_argument('--output',metavar='NEW_FILE',help='exclusive creation; default stdout')
    args=parser.parse_args()
    try:
        text=json.dumps(run(args.dps,args.stress),indent=2,allow_nan=False)+'\n'
        if args.output is None:
            sys.stdout.write(text)
        else:
            with Path(args.output).open('x',encoding='utf-8') as stream:
                stream.write(text)
    except Exception as error:
        sys.stderr.write(json.dumps({'status':'FAIL','error_type':type(error).__name__,
                                     'error':str(error)},allow_nan=False)+'\n')
        return 1
    return 0


if __name__=='__main__':
    sys.exit(main())
