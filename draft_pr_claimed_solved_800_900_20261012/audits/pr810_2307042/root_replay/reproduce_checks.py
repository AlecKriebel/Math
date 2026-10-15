#!/usr/bin/env python3
"""Independent PR810 formula/falsification checks; Python standard library only.

Run in any working directory. Writes CHECK_RESULTS.json beside this script.
The analytic proof is INDEPENDENT_DERIVATION.md. Mesh checks are empirical.
Decimal/image/Fourier agreement is reported with conservative analytic tails.
"""
from decimal import Decimal as D, localcontext
from pathlib import Path
from datetime import datetime, timezone
import json
import math

PRECISION = 100
N_IMAGES = 10
N_FOURIER = 2400
results = {"precision_digits": PRECISION, "image_half_width": N_IMAGES,
           "fourier_terms": N_FOURIER, "scope": "independent diagnostic checks; not a replacement proof"}

with localcontext() as ctx:
    ctx.prec = PRECISION
    one = D(1)
    two = D(2)
    a, b, t, m = one, one/two.sqrt(), D('0.25'), one
    for _ in range(9):
        aa = (a+b)/2
        b = (a*b).sqrt()
        t -= m*(a-aa)**2
        a, m = aa, m*2
    pi = (a+b)**2/(4*t)
    tau = 2*pi

    def sincos(z):
        z = z % tau
        if z > pi:
            z -= tau
        if z < -pi:
            z += tau
        if z == 0:
            return D(0), one
        if z == pi or z == -pi:
            return D(0), D(-1)
        zz = z*z
        si, co, ts, tc = z, one, z, one
        for n in range(1, 250):
            ts *= -zz / ((2*n)*(2*n+1))
            tc *= -zz / ((2*n-1)*(2*n))
            si2, co2 = si+ts, co+tc
            if si2 == si and co2 == co:
                return si, co
            si, co = si2, co2
        raise AssertionError("trigonometric series did not converge")

    def cosh(z):
        e = z.exp()
        return (e+one/e)/2

    def log1p(z):
        if abs(z) >= D('0.05'):
            return (1+z).ln()
        # This avoids catastrophic cancellation on highly tangential paths.
        term, acc = z, z
        for n in range(2, 400):
            term *= -z
            new = acc + term/n
            if new == acc:
                return acc
            acc = new
        raise AssertionError("log1p series did not converge")

    def poisson(x, y, eta=pi):
        sx, cx = sincos(pi*x)
        return sum((sx/(2*(cosh(pi*(y-eta+tau*k))-cx))
                    for k in range(-N_IMAGES, N_IMAGES+2)), D(0))

    def green(x, y, s, eta):
        sx, _ = sincos(pi*x)
        ss, _ = sincos(pi*s)
        _, cm = sincos(pi*(x-s))
        return sum((log1p(2*sx*ss/(cosh(pi*(y-eta+tau*k))-cm))/2
                    for k in range(-N_IMAGES, N_IMAGES+2)), D(0))

    def p_fourier(x, y, derivative_x=False):
        theta = y-pi
        st, ct = sincos(theta)
        sn, cn = D(0), one
        q, r, v = (-x).exp(), (-(2-x)).exp(), D(-2).exp()
        qn, rn, vn = one, one, one
        acc = D(-1)/(2*pi) if derivative_x else (1-x)/(2*pi)
        for n in range(1, N_FOURIER+1):
            sn, cn = sn*ct+cn*st, cn*ct-sn*st
            qn, rn, vn = qn*q, rn*r, vn*v
            coef = -n*(qn+rn)/(1-vn) if derivative_x else (qn-rn)/(1-vn)
            acc += coef*cn/pi
        return acc

    def g_fourier(x, y, s, eta):
        lo, hi = min(x,s), max(x,s)
        st, ct = sincos(y-eta)
        sn, cn = D(0), one
        q, r, v, j = (-(hi-lo)).exp(), (-2*lo).exp(), (-2*(1-hi)).exp(), D(-2).exp()
        qn, rn, vn, jn = one, one, one, one
        acc = lo*(1-hi)
        for n in range(1, N_FOURIER+1):
            sn, cn = sn*ct+cn*st, cn*ct-sn*st
            qn, rn, vn, jn = qn*q, rn*r, vn*v, jn*j
            acc += qn*(1-rn)*(1-vn)*cn/(n*(1-jn))
        return acc

    def image_tail(y, eta=pi):
        B = abs(y-eta)
        # p <= 2 exp(-pi |d|) when pi|d| >= log 4;
        # |d| >= tau |k| - B. The actual asymmetric image set is larger
        # than [-N_IMAGES,N_IMAGES], so this bound is conservative.
        return 4*(pi*B-2*pi*pi*(N_IMAGES+1)).exp()/(1-(-2*pi*pi).exp())

    def p_fourier_tail(x, derivative_x=False):
        q = (-x).exp()
        # (q^n-r^n)/(1-e^-2n) <= q^n/(1-e^-2).
        if derivative_x:
            # n(q^n+r^n) <= 2nq^n, sum n q^n explicitly.
            z = q**(N_FOURIER+1)
            total = z*((N_FOURIER+1)/(1-q)+q/(1-q)**2)
            return 2*total/(pi*(1-D(-2).exp()))
        return q**(N_FOURIER+1)/(pi*(1-D(-2).exp())*(1-q))

    def g_fourier_tail(x, s):
        q = (-abs(x-s)).exp()
        return q**(N_FOURIER+1)/((N_FOURIER+1)*(1-D(-2).exp())*(1-q))

    p0 = poisson(D('0.5'), D(0))
    qs = [1/cosh((2*k-1)*pi*pi) for k in range(-N_IMAGES, N_IMAGES+2)]
    S1, S2 = sum(qs,D(0)), sum((q*q for q in qs),D(0))
    c = pi*S2/S1
    bp = 1/(2*cosh(D('0.5')))
    exact_min_slope = (1-c)*bp/(1+bp*bp).sqrt()
    results['constants'] = {"pi": str(pi), "P_a": str(p0), "c": str(c),
        "b": str(bp), "exact_directional_minimum": str(exact_min_slope),
        "proof_lower_bound": "1/10", "c_rational_bound": "8/83"}
    assert 0<c<D(8)/83<D('0.1') and D('0.25')<bp<1
    assert exact_min_slope>D('0.1')

    points = [('0.1','-2.0'),('0.25','0.3'),('0.5','0'),('0.7','-0.4'),('0.9','2.0')]
    poisson_agreement = []
    for xs, ys in points:
        x,y = D(xs),D(ys)
        ip, fp = poisson(x,y), p_fourier(x,y)
        err = abs(ip-fp)
        tail = image_tail(y)+p_fourier_tail(x)
        assert err < tail + D('1e-90')
        poisson_agreement.append({"x":xs,"y":ys,"image_value":str(ip),
            "absolute_discrepancy":str(err),"analytic_truncation_bound":str(tail)})
    results['poisson_image_vs_fourier'] = poisson_agreement
    grad_fourier = p_fourier(D('0.5'),D(0),True)/p0
    assert abs(grad_fourier+c)<D('1e-80')
    results['gradient_independent_fourier_discrepancy']=str(abs(grad_fourier+c))

    green_agreement=[]
    for xs,ys,ss,es in [('0.4','0.2','0.1','2.8'),('0.7','-0.4','0.2','3.0'),
                        ('0.9','2.0','0.1','0.7')]:
        x,y,s,eta=map(D,(xs,ys,ss,es))
        ig,fg=green(x,y,s,eta),g_fourier(x,y,s,eta)
        err=abs(ig-fg)
        # For small z, (1/2)log(1+z)<=z/2. Green summand <=
        # 4 exp(-pi|d|), and this safely bounds the omitted positive terms.
        tail=2*image_tail(y,eta)+g_fourier_tail(x,s)
        assert ig>0 and abs(ig-green(s,eta,x,y))<D('1e-80')
        assert err<tail+D('1e-90')
        green_agreement.append({"x":xs,"y":ys,"s":ss,"eta":es,
            "image_value":str(ig),"absolute_discrepancy":str(err),
            "analytic_truncation_bound":str(tail)})
    results['green_image_vs_fourier']=green_agreement

    approaches=[]
    for mode in ['normal','slanted','extremely_tangential']:
        rows=[]
        for exponent in [1,2,3,4,6]:
            eps=D(10)**(-exponent)
            s=eps if mode!='extremely_tangential' else eps**20
            eta=pi if mode=='normal' else pi+(s if mode=='slanted' else eps)
            row={"epsilon":str(eps),"normal_distance":str(s),
                 "tangential_offset":str(eta-pi),"test_points":[]}
            for xs,ys in [('0.25','0.3'),('0.7','-0.4')]:
                x,y=D(xs),D(ys)
                ratio=green(x,y,s,eta)/green(D('0.5'),D(0),s,eta)
                expected=poisson(x,y)/p0
                row['test_points'].append({"x":xs,"y":ys,"ratio":str(ratio),
                    "limit":str(expected),"absolute_error":str(abs(ratio-expected))})
            rows.append(row)
        final=max(D(z['absolute_error']) for z in rows[-1]['test_points'])
        first=max(D(z['absolute_error']) for z in rows[0]['test_points'])
        assert final<first*D('0.0001')
        approaches.append({"mode":mode,"rows":rows})
    results['boundary_approach_stress']=approaches

    singularity=[]
    for scale in [D('0.1'),D('0.01'),D('0.001'),D('0.0001')]:
        for x,t in [(scale,scale),(scale**4,scale),(scale,D(0))]:
            difference=poisson(x,pi+t)-x/(pi*(x*x+t*t))
            normalized=difference/x
            assert abs(normalized)<1
            singularity.append({"x":str(x),"t":str(t),
                 "(P-leading_dipole)/x":str(normalized)})
    results['uniform_O_x_singularity_stress']=singularity

# This separate finite-precision mesh intentionally tests an actual punctured
# neighborhood, not just the first derivatives. It includes the switching
# directions exactly. Its role is to hunt counterexamples, not certify radii.
def p_float(x,y):
    return sum(math.sin(math.pi*x)/(2*(math.cosh(math.pi*(y-math.pi+2*math.pi*k))
               -math.cos(math.pi*x))) for k in range(-5,7))

p0f=p_float(.5,0.0)
bf=1/(2*math.cosh(.5))
switch=math.atan(1/bf)
angles=[2*math.pi*j/4096 for j in range(4096)]
angles += [switch,math.pi-switch,math.pi+switch,2*math.pi-switch]
mesh=[]
for radius in [.05,.025,.01,.001,1e-4,1e-5,1e-6,1e-7,1e-8]:
    min_gap=math.inf
    argmin=None
    for angle in angles:
        u,v=radius*math.cos(angle),radius*math.sin(angle)
        kval=p_float(.5+u,v)/p0f
        hmax=1+max(abs(u),bf*abs(math.sin(v))*math.cosh(u))
        gap=hmax-kval
        if gap<min_gap:
            min_gap,argmin=gap,angle
    assert min_gap>0
    mesh.append({"radius":radius,"directions":len(angles),
                 "minimum_sampled_gap":min_gap,"gap_over_radius":min_gap/radius,
                 "minimum_angle_radians":argmin})
results['finite_direction_mesh']=mesh
results['status']='all checks passed'
results['timestamp_utc']=datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
out=Path(__file__).with_name('CHECK_RESULTS.json')
out.write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({"status":results['status'],"output":str(out),
                 "c":results['constants']['c'],"b":results['constants']['b'],
                 "exact_directional_minimum":results['constants']['exact_directional_minimum'],
                 "mesh_min_gap_over_radius":min(z['gap_over_radius'] for z in mesh)},indent=2))
