"""Authored audit controls; all output goes to this audit directory.

Exact controls refute generic transfers. Numerical controls diagnose a target
family and classical elliptic model; they are not a proof or a novelty test.
"""
from pathlib import Path
import json
import sympy as s
import mpmath as mp

BASE = Path(__file__).resolve().parent

def area(poly):
    return s.simplify(sum(s.det(s.Matrix.hstack(poly[j], poly[(j+1)%len(poly)])) for j in range(len(poly)))/2)

def invert(poly, f):
    return [s.simplify((p-f)/((p-f).dot(p-f))) for p in poly]

def exact_controls():
    rt = s.sqrt(3)
    # Affine images of regular triangles on the unit circle. Their sides
    # envelope the same homothetic ellipse with semiaxes (1,1/2).
    phases = [
        [s.Matrix([2,0]),s.Matrix([-1,rt/2]),s.Matrix([-1,-rt/2])],
        [s.Matrix([rt,s.Rational(1,2)]),s.Matrix([-rt,s.Rational(1,2)]),s.Matrix([0,-1])],
    ]
    f=s.Matrix([rt/2,0]) # the INNER ellipse's focus
    records=[]
    for poly in phases:
        bp=area(invert(poly,f)); bm=area(invert(poly,-f))
        records.append(dict(area=str(area(poly)),Bplus=str(bp),Bminus=str(bm),product=str(s.simplify(bp*bm))))
    difference=s.simplify(s.sympify(records[0]['product'])-s.sympify(records[1]['product']))
    assert difference != 0
    # A second example has four distinct complex intersections (general
    # position), so homothety is not responsible for the transfer failure.
    generic=[
        [s.Matrix([2,0]),s.Matrix([-s.Rational(4,3),s.sqrt(5)/3]),s.Matrix([-s.Rational(4,3),-s.sqrt(5)/3])],
        [s.Matrix([4*s.sqrt(2)/3,s.Rational(1,3)]),s.Matrix([-4*s.sqrt(2)/3,s.Rational(1,3)]),s.Matrix([0,-1])],
    ]
    g=s.Matrix([s.sqrt(15)/3,0]); gen_records=[]
    inner=s.diag(s.Rational(16,9),s.Rational(1,9))
    for poly in generic:
        assert all(s.simplify(p[0]**2/4+p[1]**2-1)==0 for p in poly)
        # For line n dot x=h, tangency is h²=n^T diag(a²,b²)n;
        # reconstruct contact and check its segment parameter lies in [0,1].
        contacts=[]
        for j,p in enumerate(poly):
            q=poly[(j+1)%3]; d=q-p; n=s.Matrix([d[1],-d[0]]); h=s.simplify(n.dot(p))
            assert s.simplify(h*h-(n.T*inner*n)[0])==0
            contact=s.simplify(inner*n/h)
            t=s.simplify((contact-p).dot(d)/d.dot(d))
            assert 0<t<1
            contacts.append(str(t))
        bp=area(invert(poly,g)); bm=area(invert(poly,-g))
        gen_records.append(dict(area=str(area(poly)),Bplus=str(bp),Bminus=str(bm),product=str(s.simplify(bp*bm)),contact_parameters=contacts))
    gen_difference=s.simplify(s.sympify(gen_records[0]['product'])-s.sympify(gen_records[1]['product']))
    assert gen_difference==s.Rational(243,12544)
    X2,Y2=s.symbols('X2 Y2')
    intersections=s.solve([X2/4+Y2-1,s.Rational(9,16)*X2+9*Y2-1],[X2,Y2])
    assert intersections=={X2:s.Rational(128,27),Y2:-s.Rational(5,27)}
    # The tangent-gradient determinant is (27/4)xy, hence nonzero.
    transverse_det_square=s.simplify((s.Rational(27,4)**2*X2*Y2).subs(intersections))
    assert transverse_det_square != 0
    # Exact inversion-versus-affine failure on the ellipse itself.
    # I_0(T(1,0))=(1/2,0), whereas T(I_0(1,0))=(2,0).
    return {'generic_concentric_inner_focus_counterexample':records,
            'exact_product_difference':str(difference),
            'general_position_counterexample':gen_records,
            'general_position_product_difference':str(gen_difference),
            'complex_intersection_x_squared':str(intersections[X2]),
            'complex_intersection_y_squared':str(intersections[Y2]),
            'tangent_gradient_determinant_squared':str(transverse_det_square),
            'meaning':'Refutes the all-concentric-Poncelet inner-focus inversion product extension, including at N=3; does not refute the billiard target.'}

def numeric_family(kstr,N,tau):
    mp.mp.dps=80
    k=mp.mpf(kstr); m=k*k; K=mp.ellipk(m); Kp=mp.ellipk(1-m)
    sn=lambda z:mp.ellipfun('sn',z,m); cn=lambda z:mp.ellipfun('cn',z,m); dn=lambda z:mp.ellipfun('dn',z,m)
    v=2*K*tau/N; alpha=mp.mpf(1); beta=mp.sqrt(1-m)
    a=dn(v)/cn(v); b=beta/cn(v); c=k
    Ao=dn(v)**2/cn(v)**2; Bo=beta/cn(v)**2
    P=lambda u:(-a*sn(u),b*cn(u))
    Q=lambda u:(-Ao*sn(u),Bo*cn(u))
    def ar(poly):
        return mp.fsum(poly[j][0]*poly[(j+1)%len(poly)][1]-poly[j][1]*poly[(j+1)%len(poly)][0] for j in range(len(poly)))/2
    def inv(poly,center):
        return [((x-center)/((x-center)**2+y*y),y/((x-center)**2+y*y)) for x,y in poly]
    phases=[]
    for frac in ['0','0.173','0.381']:
        w=mp.mpf(frac)*K
        pp=[P(w+4*K*tau*j/N) for j in range(N)]
        qq=[Q(w+v+4*K*tau*j/N) for j in range(N)]
        bp=ar(inv(qq,c));bm=ar(inv(qq,-c))
        ap=ar(inv(pp,c));am=ar(inv(pp,-c))
        phases.append(dict(phase_over_K=frac,Bplus=mp.nstr(bp,60),Bminus=mp.nstr(bm,60),product=mp.nstr(bp*bm,60),outer_original_inverse_area_ratio=mp.nstr(bp/ap,60),original_inverse_product=mp.nstr(ap*am,60),area_ratio=mp.nstr(ar(qq)/ar(pp),60)))
    return dict(k=kstr,N=N,tau=tau,a=mp.nstr(a,60),b=mp.nstr(b,60),Ao=mp.nstr(Ao,60),Bo=mp.nstr(Bo,60),original_focal_square=mp.nstr(c*c,60),outer_axis_square_difference=mp.nstr(Ao*Ao-Bo*Bo,60),phases=phases)

def cs_control():
    mp.mp.dps=80
    m=mp.mpf('0.37'); K=mp.ellipk(m); Kp=mp.ellipk(1-m)
    cs=lambda z:mp.ellipfun('cn',z,m)/mp.ellipfun('sn',z,m)
    z=mp.mpc('0.41','0.28')
    err=abs(cs(z)*cs(z+K)+mp.sqrt(1-m))
    assert err<mp.mpf('1e-70')
    # Generic periodic traces are not constant: no pole cancellation premise.
    values=[mp.fsum(mp.ellipfun('dn',mp.mpf(x)+4*K*j/5,m) for j in range(5)) for x in ['0','0.2']]
    return dict(cs_half_period_expected=mp.nstr(-mp.sqrt(1-m),60),residual=mp.nstr(err,8),generic_dn_trace_values=[mp.nstr(x,60) for x in values],generic_dn_trace_difference=mp.nstr(values[0]-values[1],20))

if __name__=='__main__':
    result={'exact':exact_controls(),'target_diagnostics':[numeric_family('0.6',3,1),numeric_family('0.6',5,1),numeric_family('0.6',5,2)],'classical_model':cs_control(),
            'limits':'Exact symbolic counterexample is a proof of transfer failure. Finite high-precision target/model diagnostics are not proofs; no interval arithmetic is claimed.'}
    (BASE/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
