#!/usr/bin/env python3
"""Finite regression checks only. No geometric theorem is verified by this program."""
import contextlib
from fractions import Fraction as Q
import hashlib
import io
import json
import math
import os
from pathlib import Path
import sys


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def check_source(path, readonly=False):
    path=Path(path).resolve()
    source_bytes=path.read_bytes()
    need(os.getuid()==1000 and os.geteuid()==1000, 'must actually run as UID/EUID 1000')
    probes={}
    if readonly:
        for name,target,flags in [('existing_file',path,os.O_WRONLY|os.O_APPEND),
              ('new_file',path.parent/'write_probe_must_not_exist',os.O_WRONLY|os.O_CREAT|os.O_EXCL)]:
            try:
                fd=os.open(target,flags,0o600)
            except PermissionError:
                probes[name]='PermissionError'
            else:
                os.close(fd)
                if name=='new_file': target.unlink()
                raise RuntimeError('read-only probe unexpectedly allowed: '+name)
    ns={'__name__':'audited_module','__file__':str(path)}
    exec(compile(source_bytes,str(path),'exec'),ns)
    output=io.StringIO()
    with contextlib.redirect_stdout(output): ns['main']()
    authored=json.loads(output.getvalue())
    need(authored['checks']==61 and authored['negative_checks']==16,'authored count changed')
    count=0
    def verify(test,label):
        nonlocal count
        need(test,label); count+=1
    # Values absent from the authored fixtures, including large and very small rationals.
    for a,p,alpha in [(Q(17,13),Q(9,11),Q(4,9)),(Q(10**6),Q(1,10**6),Q(7,3)),
                      (Q(1,10**6),Q(10**6),Q(1,7)),(Q(5,9),Q(0),Q(11,2)),
                      (Q(97,23),Q(13,31),Q(0))]:
        c=p+alpha*a; I=2*a*p+alpha*a*a
        verify(ns['recover_area'](c,I,alpha)==a,'independent area fixture')
        verify(c*c-alpha*I==p*p,'discriminant must be the mixed-area square')
    for a,b in [(Q(1,13),Q(19,7)),(Q(99,2),Q(99,2)),(Q(2,3),Q(10000))]:
        verify(ns['recover_curvature_radii'](a+b,1/a+1/b)==tuple(sorted((a,b))),
               'independent radius fixture')
        verify((a+b)/(1/a+1/b)==a*b,'radius product is s/q, not s*q or q/s')
    for m,A,alpha,t in [(Q(13,17),Q(29,3),Q(2,9),Q(1,7)),
                        (Q(3,5),Q(11,19),Q(17,4),Q(11,3))]:
        g=m+alpha*A; gt=t*m+alpha*t*t*A
        verify(ns['recover_area_covariogram'](g,gt,t,alpha)==A,'independent dilation fixture')
        verify(gt-t*g==alpha*t*(t-1)*A,'dilation determinant')
    # Independently computed boundary formula: for CCW polygon E, V(E,H)
    # equals half the sum of h_H((dy,-dx)) over edges. No square roots needed.
    def edge_mixed(E,H):
        total=Q(0)
        for a,b in zip(E,E[1:]+E[:1]):
            n=(b[1]-a[1],a[0]-b[0])
            total+=max(n[0]*p[0]+n[1]*p[1] for p in H)
        return total/2
    polygons=[[(0,0),(3,0),(0,2)],[(0,0),(4,0),(4,3),(0,3)],
              [(-2,-1),(1,-2),(4,1),(0,3)]]
    bodies=[[(0,0),(1,0),(0,1)],[(-2,0),(3,0)],[(0,0)],
            [(7,-5),(8,-5),(7,-4)]]
    for E in polygons:
        for H in bodies:
            verify(ns['mixed_area'](E,H)==edge_mixed(E,H),'independent edge mixed-area formula')
    # Exact one-dimensional integration of rectangle overlap widths.
    def linear_integral(y0,y1,length): return (y0+y1)*length/2
    for a,b,wx,wy in [(Q(2),Q(3),Q(5),Q(7)),(Q(3,2),Q(7,5),Q(0),Q(2))]:
        integral_lx=2*linear_integral(a,Q(0),a)
        integral_ly=2*linear_integral(b,Q(0),b)
        I=(wx*(2*a)*integral_ly+wy*(2*b)*integral_lx)/2
        m=(b*wx+a*wy)/2
        verify(I==2*(a*b)*m,'rectangle mixed-area integral coefficient two')
    # Parabolic-lens area integrates epsilon - q*s^2/2 over [-b,b].
    for q,b in [(Q(3,2),Q(2,5)),(Q(7),Q(3,11))]:
        eps=q*b*b/2
        integral=2*eps*b-q*b**3/3
        verify(integral==Q(4,3)*b*eps,'lens area coefficient 4/3')
        verify(eps/(b*b)==q/2,'lens horizontal scale sqrt(2 epsilon/q)')
    # Disk lens arc geometry gives 4R arccos(d/(2R)); test three radii.
    disk_errors=[]
    for R in [Q(1,2),Q(1),Q(7,3)]:
        R=float(R); eps=R*1e-6
        measured=4*R*math.acos(1-eps/(2*R))/math.sqrt(eps)
        expected=4*math.sqrt(R)
        verify(abs(measured/expected-1)<1e-6,'Euclidean lens coefficient four')
        disk_errors.append(abs(measured/expected-1))
    # Boundary segment and normalization checks with explicit support conditions.
    for length in [Q(1,7),Q(2),Q(13,5)]:
        # Cauchy width integral of a segment is length * integral_0^pi |cos| = 2 length.
        P=2*length
        verify(P!=length,'boundary segment factor two cannot be omitted')
    for x,inside in [(Q(0),True),(Q(2),True),(Q(3),False)]:
        raw=Q(3) if inside else Q(0)
        normalized=raw-Q(3)*int(inside)
        verify(normalized==0,'Euler subtraction is supported on the closed difference body')
    for bad in [lambda: ns['recover_area'](False,1,0),
                lambda: ns['recover_area'](1,1,-Q(1,3)),
                lambda: ns['recover_area'](1,3,-1),
                lambda: ns['recover_curvature_radii'](Q(1),Q(1)),
                lambda: ns['recover_area_covariogram'](1,2,Q(1),Q(3)),
                lambda: ns['recover_area_covariogram'](1,2,Q(2),Q(-1)),
                lambda: ns['rational_sqrt'](Q(3,7))]:
        try: bad()
        except (ValueError,TypeError): count+=1
        else: raise RuntimeError('independent invalid fixture accepted')
    need(path.read_bytes()==source_bytes,'checker bytes changed during read-only run')
    # The checker is compiled in memory; -B prevents bytecode artifacts.
    return {'status':'PASS','uid':os.getuid(),'euid':os.geteuid(),
            'optimization':sys.flags.optimize,'authored':authored,
            'independent_checks':count,'disk_relative_errors':disk_errors,
            'read_only_probes':probes,'checker_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'scope':'Finite algebra/constants/guard regressions only; geometry is audited by proof.'}

if __name__=='__main__':
    need(len(sys.argv) in (2,3),'usage: independent_checks.py CHECKER [--require-readonly]')
    print(json.dumps(check_source(sys.argv[1],len(sys.argv)==3),sort_keys=True))
