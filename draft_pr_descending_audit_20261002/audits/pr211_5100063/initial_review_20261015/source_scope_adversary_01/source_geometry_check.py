#!/usr/bin/env python3
"""Independent finite source-scope diagnostics, no candidate E/pole formulas.

Uses Stachel Theorem 4.3 only to generate original billiard vertices.  All
subsequent tangency, reflection, outer intersections and focal inversions use
Cartesian geometry.  This is not an interval certificate or a universal proof.
"""
from pathlib import Path
from collections import Counter
from math import gcd
import json
import mpmath as m
m.mp.dps=80
counts=Counter()
maxerr=m.mpf(0)

def check(label, err, scale=1):
    global maxerr
    z=abs(err)/max(m.mpf(1),abs(scale))
    if z >= m.mpf('1e-60'):
        raise AssertionError((label,m.nstr(z,12)))
    counts[label]+=1
    maxerr=max(maxerr,z)

def det(p,q): return p[0]*q[1]-p[1]*q[0]
def sub(p,q): return (p[0]-q[0],p[1]-q[1])
def norm(p): return m.sqrt(p[0]**2+p[1]**2)
def area(p): return sum(det(p[i],p[(i+1)%len(p)]) for i in range(len(p)))/2

def inverse(p,f):
    d=sub(p,f); s=d[0]**2+d[1]**2
    if s<=0: raise AssertionError('real focal inversion undefined')
    counts['real_focal_inversion_defined']+=1
    return (f[0]+d[0]/s,f[1]+d[1]/s)

families=[]
for k0 in ('.03','.55','.97'):
    k=m.mpf(k0); par=k*k; K=m.ellipk(par)
    alpha=m.mpf('1.37'); beta=alpha*m.sqrt(1-par); c=alpha*k
    sn=lambda z:m.ellipfun('sn',z,par)
    cn=lambda z:m.ellipfun('cn',z,par)
    dn=lambda z:m.ellipfun('dn',z,par)
    for N in (3,5,7,9,11):
        for tau in range(1,N//2+1):
            if gcd(N,tau)!=1: continue
            v=2*K*tau/N; delta=2*v
            a=alpha*dn(v)/cn(v); b=beta/cn(v)
            check('original_foci_from_stachel_axes',a*a-b*b-c*c,a*a)
            products=[]
            for phase in (K/19,4*K/11,13*K/7):
                p=[(-a*sn(phase+j*delta),b*cn(phase+j*delta)) for j in range(N)]
                check('closure',norm(sub((-a*sn(phase+N*delta),b*cn(phase+N*delta)),p[0])),a)
                q=[]
                for j in range(N):
                    x,y=p[j]; xp,yp=p[(j+1)%N]
                    check('original_vertex_on_ellipse',x*x/(a*a)+y*y/(b*b)-1)
                    # Line through consecutive vertices: nx X + ny Y = ell.
                    nx,ny=yp-y,x-xp; ell=nx*x+ny*y
                    check('side_tangent_to_original_caustic',ell*ell-alpha*alpha*nx*nx-beta*beta*ny*ny,ell*ell)
                    incoming=sub(p[j],p[j-1]); outgoing=sub(p[(j+1)%N],p[j])
                    incoming=tuple(z/norm(incoming) for z in incoming)
                    outgoing=tuple(z/norm(outgoing) for z in outgoing)
                    normal=(x/(a*a),y/(b*b))
                    check('billiard_reflection_normal',det(sub(incoming,outgoing),normal),norm(normal))
                    # Independent solve of the actual tangent equations.
                    tx,ty=x/(a*a),y/(b*b); ux,uy=xp/(a*a),yp/(b*b)
                    denominator=tx*uy-ux*ty
                    if denominator==0: raise AssertionError('outer intersection at infinity')
                    counts['outer_intersection_finite']+=1
                    Q=((uy-ty)/denominator,(tx-ux)/denominator)
                    check('outer_intersection_tangent_1',tx*Q[0]+ty*Q[1]-1)
                    check('outer_intersection_tangent_2',ux*Q[0]+uy*Q[1]-1)
                    if Q[0]**2/a**2+Q[1]**2/b**2 <= 1:
                        raise AssertionError('outer vertex not outside billiard')
                    counts['outer_vertex_exterior_original_ellipse']+=1
                    q.append(Q)
                plus=[inverse(Q,(c,0)) for Q in q]
                minus=[inverse(Q,(-c,0)) for Q in q]
                ap,am=area(plus),area(minus)
                if ap<=0 or am<=0: raise AssertionError('positive oriented source area failed')
                counts['positive_source_signed_areas']+=2
                check('orientation_reversal_plus',area(list(reversed(plus)))+ap,ap)
                check('orientation_reversal_minus',area(list(reversed(minus)))+am,am)
                check('odd_repetition_plus',area(plus*3)-3*ap,ap)
                check('odd_repetition_minus',area(minus*3)-3*am,am)
                check('odd_repetition_product',area(plus*3)*area(minus*3)-9*ap*am,ap*am)
                products.append(ap*am)
            for product in products[1:]:
                check('source_target_phase_product',product-products[0],products[0])
            families.append({'k':k0,'N':N,'turning_number':tau})

out={'status':'finite_checks_passed','precision_digits':80,'threshold':'1e-60','families':families,'family_count':len(families),'assertions':sum(counts.values()),'categories':dict(counts),'max_scaled_error':m.nstr(maxerr,12),'limitations':'Finite uncertified high-precision source-object and theorem-applicability checks. No candidate edge, pole, or meromorphic formula is assumed or verified here; no universal proof or historical-priority claim.'}
root=Path(__file__).resolve().parent
(root/'source_geometry_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
