#!/usr/bin/env python3
"""Reproducible numerical stress checks, not a proof or validated interval numerics.
Only NumPy is required. Run from anywhere; output stays in this family root.
"""
import datetime, json, math, pathlib
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent

def composite_gauss(a, b, panels, order=16):
    z, w = np.polynomial.legendre.leggauss(order)
    cuts = np.linspace(a, b, panels + 1)
    mid = (cuts[:-1] + cuts[1:]) / 2
    half = (cuts[1:] - cuts[:-1]) / 2
    return (mid[:, None] + half[:, None] * z).ravel(), (half[:, None] * w).ravel()

def phi(x, kind):
    if kind == 'flat_face':
        return np.zeros_like(x)
    if kind == 'log_cusp':
        return x / np.log(np.e / x)
    return x ** float(kind)

def endpoint_density(t, kind):
    # K={(x,y): |x|<=1, phi(|x|)<=y<=1}; h=y+x^2+y^2.
    lo = np.zeros_like(t)
    hi = np.ones_like(t)
    for _ in range(64):
        mid = (lo + hi) / 2
        v = phi(mid, kind)
        below = v + mid * mid + v * v < t
        lo = np.where(below, mid, lo)
        hi = np.where(below, hi, mid)
    upper = (lo + hi) / 2
    lower = np.sqrt(np.maximum(t - 2, 0))
    scale = np.sqrt(1 + 4*t)
    return np.maximum(0, np.arcsin(2*upper/scale) - np.arcsin(2*lower/scale))

def quadrature(kind, panels):
    # Split at t=2, and smooth the cap transition with endpoint substitutions.
    theta, wtheta = composite_gauss(0, np.pi/2, panels)
    tleft = 2*np.sin(theta)**2
    wleft = wtheta * 4*np.sin(theta)*np.cos(theta)
    u, wu = composite_gauss(0, 1, panels)
    tright = 2 + u*u
    wright = 2*u*wu
    t = np.concatenate([tleft, tright])
    weights = np.concatenate([wleft, wright]) * endpoint_density(t, kind)
    return t, weights

def reference_moments(kind):
    x, wx = composite_gauss(0, 1, 512)
    a = phi(x, kind)
    def mon(i, j):
        return 2*np.dot(wx, x**i * (1-a**(j+1))/(j+1))
    v = mon(0, 0)
    h1 = mon(0, 1) + mon(2, 0) + mon(0, 2)
    h2 = mon(0, 2) + mon(4, 0) + mon(0, 4) + 2*mon(2, 1) + 2*mon(0, 3) + 2*mon(2, 2)
    return np.array([v, h1, h2])

def spectral_values(t, w, degrees=(4, 8, 16, 32, 64)):
    w = w / np.sum(w)
    v = np.sqrt(w)
    basis = []
    for j in range(max(degrees)+1):
        if j:
            v = t*basis[-1]
            # Full double reorthogonalization prevents misleading monomial Gram failures.
            for _ in range(2):
                for old in basis:
                    v -= np.dot(old, v)*old
            v /= np.linalg.norm(v)
        basis.append(v.copy())
    Q = np.array(basis).T
    orth_error = np.max(np.abs(Q.T@Q - np.eye(Q.shape[1])))
    J = Q.T@(t[:,None]*Q)
    answer = {}
    for m in degrees:
        val = float(np.linalg.eigvalsh(J[:m+1,:m+1])[0])
        answer[str(m)] = {'smallest_zero_approx': val, 'm_squared_times_value': m*m*val,
                         'global_density_degree': 4*m}
    return answer, float(orth_error)

def nesting_check():
    # Nonsimple 3D apex: square pyramid, four extremal rays in dimension three.
    rng = np.random.default_rng(30003990)
    e = np.array([0.,0.,.5])
    def h(x): return x[2]+np.dot(x,x)
    max_h_error = 0.
    min_slack = math.inf
    cases = 0
    for _ in range(500):
        x = rng.uniform(-1,1,3)
        x[2] = rng.uniform(.000001,.002)
        x[:2] *= x[2]
        s = h(x)
        target = s + rng.uniform(.000001,.002)
        u_s = x[2]/e[2]
        z = (x-u_s*e)/(1-u_s)
        lo, hi = u_s, .1
        for __ in range(60):
            mid = (lo+hi)/2
            v = (1-mid)*z+mid*e
            if h(v)<target: lo=mid
            else: hi=mid
        u_t=(lo+hi)/2
        xt=(1-u_t)*z+u_t*e
        min_slack=min(min_slack,float(xt[2]-max(abs(xt[0]),abs(xt[1]))),float(1-xt[2]))
        max_h_error=max(max_h_error,abs(h(xt)-target))
        assert min_slack >= -1e-14
        assert u_t >= u_s
        cases += 1
    return {'cases':cases,'minimum_membership_slack':min_slack,'maximum_level_residual':max_h_error}

def radial_jacobi_check():
    # h=||x||^2 on a unit n-ball: its normalized push-forward is
    # (alpha+1)t^alpha dt, alpha=n/2-1. These are exact recurrence coefficients.
    answer={}
    for n in (1,2,3,7):
        alpha=n/2-1
        k=np.arange(65,dtype=float)
        diag=np.empty_like(k)
        diag[0]=(alpha+1)/(alpha+2)
        diag[1:]=(1+alpha*alpha/((2*k[1:]+alpha)*(2*k[1:]+alpha+2)))/2
        j=np.arange(64,dtype=float)
        off=np.sqrt((j+1)**2*(j+alpha+1)**2/((2*j+alpha+1)*(2*j+alpha+3)))/(2*j+alpha+2)
        J=np.diag(diag)+np.diag(off,1)+np.diag(off,-1)
        variance=(alpha+1)/((alpha+2)**2*(alpha+3))
        assert abs(off[0]**2-variance)<1e-14
        values={str(m):float(np.linalg.eigvalsh(J[:m+1,:m+1])[0]) for m in (4,8,16,32,64)}
        assert all(v>0 for v in values.values())
        answer[str(n)]={'alpha':alpha,'values':values,'m64_squared_times_value':4096*values['64'],
                        'exact_mean_residual':float(abs(diag[0]-(alpha+1)/(alpha+2))),
                        'exact_variance_residual':float(abs(off[0]**2-variance))}
    return answer

def main():
    results = {'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'status':'Empirical floating-point stress checks only; analytic proof is in report.md.',
               'numpy_version':np.__version__, 'cases':{}}
    for kind in ('flat_face','1','1.25','2','4','16','log_cusp'):
        rows=[]
        ref=reference_moments(kind)
        for panels in (64,128):
            t,w=quadrature(kind,panels)
            vals,oe=spectral_values(t,w)
            mom=np.array([np.dot(w,t**j) for j in range(3)])
            rows.append({'panels':panels,'nodes':len(t),'moment_relative_error':(np.abs(mom-ref)/ref).tolist(),
                         'orthogonality_error':oe,'spectral':vals})
        a,b=rows
        stability=max(abs(a['spectral'][str(m)]['smallest_zero_approx']/b['spectral'][str(m)]['smallest_zero_approx']-1) for m in (4,8,16,32,64))
        tt=np.geomspace(1e-10,1e-3,400)
        ww=endpoint_density(tt,kind)
        # In dimension two the proof gives w(t)<= (t/s) w(s), and w(t)>=c*w(s).
        growth_violation=float(np.max((ww[1:]/ww[:-1])/(tt[1:]/tt[:-1])))
        local_drop=float(np.min(ww[1:]/ww[:-1]))
        results['cases'][kind]={'quadratures':rows,'max_relative_value_change':stability,
                                  'adjacent_density_growth_ratio_bound':growth_violation,
                                  'minimum_adjacent_density_ratio':local_drop}
    # Falsifiable numerical sanity conditions, deliberately much looser than observed errors.
    for case in results['cases'].values():
        assert case['max_relative_value_change'] < 1e-8
        assert max(case['quadratures'][-1]['moment_relative_error']) < 1e-9
        assert case['quadratures'][-1]['orthogonality_error'] < 1e-11
        assert case['adjacent_density_growth_ratio_bound'] <= 1+1e-8
        assert case['minimum_adjacent_density_ratio'] >= .25-1e-8
        vals=[v['smallest_zero_approx'] for v in case['quadratures'][-1]['spectral'].values()]
        assert all(v>0 for v in vals)
        assert all(a>b for a,b in zip(vals,vals[1:]))
    results['radial_zero_gradient_jacobi']=radial_jacobi_check()
    results['nonsimple_cone_nesting']=nesting_check()
    results['sanity_assertions']='PASS'
    (ROOT/'numerical_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({'cases':{k:{'max_relative_value_change':v['max_relative_value_change'],
                  'm64_scaled':v['quadratures'][-1]['spectral']['64']['m_squared_times_value']}
                  for k,v in results['cases'].items()},'nesting':results['nonsimple_cone_nesting']},indent=2))
if __name__=='__main__':main()
