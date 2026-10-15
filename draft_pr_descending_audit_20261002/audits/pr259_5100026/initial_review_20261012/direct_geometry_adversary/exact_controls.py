#!/usr/bin/env python3
"""Exact Cartesian witnesses derived before reading submitted proof.

Triangle computations use quotient-ring reduction; bounds fixing the intended
real root and nonzero denominators are documented in EXACT_WITNESSES.md.
"""
import hashlib
import json
import platform
import sys
from datetime import datetime,timezone
from pathlib import Path
import sympy as S

HERE=Path(__file__).resolve().parent


def solve2(u,v,h,k):
    d=u[0]*v[1]-u[1]*v[0]
    return [(h*v[1]-u[1]*k)/d,(u[0]*k-h*v[0])/d]


def dot(u,v):
    return sum(x*y for x,y in zip(u,v))


def constructed(points,a,b,c):
    tangent=[[x/(a*a),y/(b*b)] for x,y in points]
    outer=[solve2(tangent[i],tangent[(i+1)%len(points)],1,1) for i in range(len(points))]
    normals=[[r[0]-c,r[1]] for r in outer]
    heights=[dot(n,r) for n,r in zip(normals,outer)]
    anti=[solve2(normals[i],normals[(i+1)%len(points)],heights[i],heights[(i+1)%len(points)]) for i in range(len(points))]
    return outer,anti,[S.factor(sum(u[k] for u in anti)/len(points)) for k in (0,1)]


def main():
    a,b,c=map(S.Integer,(5,3,4))
    diamond=[[a,0],[0,b],[-a,0],[0,-b]]
    outer,anti,mean=constructed(diamond,a,b,c)
    assert mean==[0,0]
    assert outer==[[5,3],[-5,3],[-5,-3],[5,-3]]
    assert anti==[[-4,6],[-6,0],[-4,-6],[14,0]]
    t,s=S.symbols('t s')
    basis=S.groebner([16*t*t+18*t-25,s*s+t*t-1],s,t)
    def residual(f):
        numerator=S.fraction(S.cancel(f))[0]
        return S.factor(basis.reduce(S.expand(numerator))[1])
    triangles=[]
    for sign in (1,-1):
        points=[[sign*a,0],[-sign*a*t,sign*b*s],[-sign*a*t,-sign*b*s]]
        ro,ua,gm=constructed(points,a,b,c)
        # Positive-root chord-length witness. Its square equals actual length.
        length=s*(25+16*t)/(3*t)
        lengths=[length,6*s,length]
        outgoing=[]
        line_caustic=[]
        reflection=[]
        for i,p in enumerate(points):
            q=points[(i+1)%3]
            d=[(q[k]-p[k])/lengths[i] for k in (0,1)]
            outgoing.append(d)
            n=[-d[1],d[0]]
            lam=25*n[0]**2+9*n[1]**2-dot(n,p)**2
            line_caustic.append(residual(lam-25*(1-t*t)))
        for i,p in enumerate(points):
            incoming=outgoing[(i-1)%3]
            n=[p[0]/25,p[1]/9]
            reflected=[incoming[k]-2*dot(incoming,n)*n[k]/dot(n,n) for k in (0,1)]
            reflection.extend(residual(reflected[k]-outgoing[i][k]) for k in (0,1))
        unit=[residual(dot(d,d)-1) for d in outgoing]
        boundary=[residual(p[0]**2/25+p[1]**2/9-1) for p in points]
        expected=(a + (a+c)*(1+t)/(1-t)-2*a/t)/3 if sign==1 else (-a-(a-c)*(1+t)/(1-t)+2*a/t)/3
        centroid_residual=[residual(gm[0]-expected),residual(gm[1])]
        _,_,repeat_mean=constructed(points+points,a,b,c)
        repeat_residual=[residual(repeat_mean[k]-gm[k]) for k in (0,1)]
        all_res=unit+boundary+line_caustic+reflection+centroid_residual+repeat_residual
        assert all(z==0 for z in all_res)
        actual_t=(S.sqrt(481)-9)/16
        triangles.append({'sign':sign,'points':points,'outer':ro,'antipedal':ua,
                          'mean':[expected,0],'mean_decimal':[S.N(expected.subs(t,actual_t),40),0],
                          'unit_residual':unit,'boundary_residual':boundary,
                          'caustic_residual':line_caustic,'reflection_residual':reflection,
                          'centroid_residual':centroid_residual,'repeat_mean_residual':repeat_residual})
    difference=4*a*(2*t-1)/(3*t*(1-t))
    assert residual(triangles[0]['mean'][0]-triangles[1]['mean'][0]-difference)==0
    output={'receipt':{'created_utc':datetime.now(timezone.utc).isoformat(),'python':sys.executable,
                       'python_version':platform.python_version(),'sympy_version':S.__version__,
                       'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                       'method':'Exact Cartesian intersections and rational quotient-ring identities; no submitted helpers.'},
            'diamond':{'a':a,'b':b,'c':c,'lambda':S.Rational(225,34),'points':diamond,'outer':outer,'antipedal':anti,'mean':mean},
            'triangle_parameter':{'t':(S.sqrt(481)-9)/16,'s':'positive sqrt(1-t^2)',
                                  'lambda':225*(S.sqrt(481)-17)/128,
                                  'polynomial':16*t*t+18*t-25,'quotient_basis':[str(g) for g in basis.polys]},
            'triangles':triangles,'phase_mean_difference':difference,
            'scope':'Exact counterexample to extending the even theorem to twice-repeated odd least-period lists; no counterexample to primitive even theorem.'}
    (HERE/'exact_cartesian_witnesses.json').write_text(json.dumps(output,default=str,indent=2)+'\n')
    print('All quotient-ring residuals zero. Two repeated-triangle mean x values:')
    for row in triangles:
        print(row['sign'],row['mean_decimal'])


if __name__=='__main__':
    main()
