#!/usr/bin/env python3
"""Independent high-precision diagnostics; not certified zero counts or proofs."""
import json
import mpmath as mp

mp.mp.dps = 70

def require(ok, label):
    if not ok:
        raise ValueError(label)

def F(n, z):
    a = mp.mpf(1)/(2*n)
    return z*mp.hyper([a], [mp.mpf('1.5'), a+1], -z**(2*n)/4)

def A(n):
    return mp.gamma(mp.mpf(1)/n)*mp.cos(mp.pi/(2*n))/(n-1)

checks = 0
sector_results = []
for n in (2, 3, 5, 10):
    for j in range(1, 25):
        x = (j*mp.pi)**(mp.mpf(1)/n)
        f = F(n, x)
        require(f > 0, 'positive critical value')
        require((-1)**j*(A(n)-f) > 0, 'strict alternating tail')
        checks += 2
    for fraction in (mp.mpf('0.2'), mp.mpf('0.5'), mp.mpf('0.8')):
        for q in (40, 80, 160):
            z = mp.mpf(q)**(mp.mpf(1)/n)*mp.exp(1j*mp.pi*fraction/n)
            leading = -z**(1-2*n)*mp.exp(-1j*z**n)/(2*n)
            error = abs(F(n, z)/leading-1)
            require(q*error < 5, 'sector leading coefficient or remainder scale')
            checks += 1
            sector_results.append({'n': n, 'sector_fraction': float(fraction),
                                   'radius_power_n': q, 'scaled_relative_error': float(q*error)})
    for z in (mp.mpc('0.3', '0.2'), mp.mpc('1.1', '-0.4')):
        radial = z*mp.quad(lambda t: mp.sin((z*t)**n)/(z*t)**n if t else 1, [0, 1])
        require(abs(F(n, z)-radial) < mp.mpf('1e-60'), 'hypergeometric versus radial quadrature')
        checks += 1

def winding(n, q, samples):
    r = mp.mpf(q)**(mp.mpf(1)/n)
    a = A(n)
    values = [F(n, r*mp.exp(2j*mp.pi*j/samples))-a for j in range(samples)]
    increments = [mp.arg(values[(j+1)%samples]/values[j]) for j in range(samples)]
    total = mp.fsum(increments)/(2*mp.pi)
    rounded = int(mp.nint(total))
    require(abs(total-rounded) < mp.mpf('1e-60'), 'winding integer consistency')
    return rounded, float(max(map(abs, increments)))

winding_results = []
for n in (2, 3, 5):
    for q in ('20.3', '40.7', '80.9'):
        samples = 512*n
        history = []
        while True:
            count1, max1 = winding(n, q, samples)
            count2, max2 = winding(n, q, 2*samples)
            history.append({'samples': samples, 'counts': [count1,count2], 'phase_steps': [max1,max2]})
            if max(max1,max2) < float(mp.pi/2) and count1 == count2:
                break
            samples *= 2
            require(samples <= 65536*n, 'adaptive sampling limit')
        require(count1 == count2, 'mesh refinement winding count')
        require(max1 < float(mp.pi/2), 'coarse sampled phase increments')
        require(max2 < float(mp.pi/2), 'fine sampled phase increments')
        prediction = 2*n*mp.mpf(q)/mp.pi
        require(abs(count2/prediction-1) < mp.mpf('0.30'), 'finite-radius count scaling')
        checks += 6
        winding_results.append({'n': n, 'radius_power_n': q,
                                'samples': [samples, 2*samples], 'approximate_count': count2,
                                'predicted_leading_count': float(prediction),
                                'count_over_prediction': float(count2/prediction),
                                'maximum_sampled_phase_steps': [max1, max2],
                                'refinement_history': history})

print(json.dumps({'result': 'PASS', 'precision_decimal_digits': mp.mp.dps,
                  'diagnostic_checks': checks, 'certified': False,
                  'warning': 'Finite floating-point diagnostics cannot establish asymptotic limits or certify winding counts between samples.',
                  'sector_checks': sector_results, 'winding_checks': winding_results}, indent=2))
