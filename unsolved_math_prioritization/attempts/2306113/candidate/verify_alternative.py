#!/usr/bin/env python3
"""Exact disk certificate for the explicitly described inner-|h| repair."""
import argparse,json,runpy,sys
from fractions import Fraction as Q
from pathlib import Path

V=runpy.run_path(str(Path(__file__).with_name('verify_counterexample.py')),run_name='certificate_library')
add,mul,scale,neg,norm2,unit,compose,koebe,slit,evalpoly,sqrt_upper,need=[V[k] for k in ('add','mul','scale','neg','norm2','unit','compose','koebe','slit','evalpoly','sqrt_upper','need')]
Z=V['Z']

def certify(data):
    keys={'degree','q1','q2','t1','t2','t3','radius','coefficients','norm_upper','grid_N','sqrt_scale','rho','convolution_lower'}
    need(type(data) is dict and set(data)==keys,'wrong schema keys')
    need(type(data['degree']) is int and type(data['grid_N']) is int and type(data['sqrt_scale']) is int,'integer parameter type')
    need(data['grid_N']==8192 and data['sqrt_scale']==10**9,'unsupported certificate settings')
    need([data['t'+str(j)] for j in (1,2,3)]==['0','7/200','-2/25'],'unsupported unit parameters')
    need(data['norm_upper']=='251/250' and data['convolution_lower']=='2517/2500','unsupported witness bounds')
    need(type(data['coefficients']) is list and len(data['coefficients'])==9,'coefficient count')
    for pair in data['coefficients']:
        need(type(pair) is list and len(pair)==2,'complex coefficient schema')
        for value in pair:V['rational'](value)
    # The analytic proof is fixed to these geometric parameters.
    need(data['degree']==10 and data['q1']=='63/80' and data['q2']=='2/25' and data['rho']=='1/1000' and data['radius']=='999/1000','unsupported witness parameters')
    d=10;q1=Q(data['q1']);q2=Q(data['q2']);r=Q(data['radius']);us=[unit(Q(data['t'+str(j)])) for j in (1,2,3)]
    a=[scale(x,1/(q1*q2)) for x in compose(koebe(us[2],d),compose(slit(q2,us[1],d),slit(q1,us[0],d),d),d)]
    c=[Z,Z]+[(Q(x),Q(y)) for x,y in data['coefficients']]
    L=Z
    for n in range(2,d+1):L=add(L,scale(mul(c[n],a[n]),r**(n-1)))
    need(norm2(L)>0,'zero L');factor=scale((-L[0],L[1]),1/norm2(L));c=[mul(x,factor) for x in c]
    deriv=[scale(c[n],Q(n)) for n in range(1,d+1)];quotient=c[1:]
    absupper=[abs(x)+abs(y) for x,y in c];ss=10**10;gamma=Q(1000000,1002001)
    def center_bound(r,t,sgn):
        v=scale(((1-t*t)/(1+t*t),2*t/(1+t*t)),Q(sgn));z=scale(v,r)
        der=evalpoly(deriv,z);q=evalpoly(quotient,z)
        first=add(der,neg(q));qabs=sqrt_upper(norm2(q),ss)
        # |q| lies in [qabs-1/ss,qabs]; replacing it by qabs costs <=1/ss.
        second=add(der,scale((v[0],-v[1]),qabs))
        return (sqrt_upper(norm2(first),ss)+sqrt_upper(norm2(second),ss)+Q(1,ss))/2
    stack=[(Q(0),Q(1),Q(-1),Q(1),sgn,0) for sgn in (1,-1)]
    visited=leaves=depthmax=0;largest=Q(0);smallest_margin=gamma
    while stack:
        r0,r1,t0,t1,sgn,depth=stack.pop();visited+=1;need(visited<=300000,'covering node budget exceeded')
        rm=(r0+r1)/2;tm=(t0+t1)/2
        Br=sum(Q(n*(n-1))*absupper[n]*r1**(n-2) for n in range(2,d+1))
        Bt=sum(Q(2*n*n-2*n+1)*absupper[n]*r1**(n-1) for n in range(2,d+1))
        er=Br*(r1-r0)/2;et=Bt*(t1-t0)/2
        bound=center_bound(rm,tm,sgn)+er+et
        if bound<gamma:
            leaves+=1;largest=max(largest,bound);smallest_margin=min(smallest_margin,gamma-bound);depthmax=max(depthmax,depth)
        else:
            need(depth<40,'covering did not certify')
            if er>=et:
                stack.extend([(r0,rm,t0,t1,sgn,depth+1),(rm,r1,t0,t1,sgn,depth+1)])
            else:
                stack.extend([(r0,r1,t0,tm,sgn,depth+1),(r0,r1,tm,t1,sgn,depth+1)])
    return {'status':'PASS','scope':'entire closed unit disk for inner-|h| repair','arithmetic':'exact rational bounds and integer square roots','visited_rectangles':visited,'certified_leaves':leaves,'maximum_depth':depthmax,'all_leaf_bounds_strictly_less_than_gamma':True,'gamma':str(gamma),'smallest_margin_numerator':str(smallest_margin.numerator),'smallest_margin_denominator':str(smallest_margin.denominator)}

def main():
    p=argparse.ArgumentParser();p.add_argument('certificate',type=Path);a=p.parse_args()
    try:
        raw=a.certificate.read_bytes();need(len(raw)<=10000,'input too large');data=json.loads(raw,object_pairs_hook=V['pairs'],parse_constant=lambda _:(_ for _ in ()).throw(ValueError('nonfinite JSON')))
        result=certify(data)
    except (V['Invalid'],ValueError,OSError,KeyError,TypeError,ZeroDivisionError,json.JSONDecodeError) as e:
        print(json.dumps({'status':'REJECT','reason':str(e)}));return 2
    print(json.dumps(result,indent=2,sort_keys=True));return 0
if __name__=='__main__':sys.exit(main())
