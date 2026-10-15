#!/usr/bin/env python3
"""Independent ray tracing; no submitted helpers or elliptic parametrization.

All inputs/outputs live beside this script. mpmath is used only for arithmetic.
Numerical diagnostics are empirical checks, not interval or universal proofs.
"""
import argparse
import hashlib
import json
import math
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
import mpmath as mp

HERE = Path(__file__).resolve().parent


def now():
    return datetime.now(timezone.utc).isoformat()


def dot(x, y):
    return x[0] * y[0] + x[1] * y[1]


def sub(x, y):
    return x[0] - y[0], x[1] - y[1]


def norm(x):
    return mp.sqrt(dot(x, x))


def initial_ray(a, b, lam, theta):
    co, si = mp.cos(theta), mp.sin(theta)
    g2 = a*a*si*si + b*b*co*co
    sl, sg = mp.sqrt(lam), mp.sqrt(g2-lam)
    return ((-a*si*sg-b*co*sl)/g2,
            (b*co*sg-a*si*sl)/g2)


def boundary_second(a, b, p, d):
    travel = -2*(p[0]*d[0]/(a*a)+p[1]*d[1]/(b*b)) / (
        d[0]*d[0]/(a*a)+d[1]*d[1]/(b*b))
    return (p[0]+travel*d[0], p[1]+travel*d[1]), travel


def reflect(a, b, q, d):
    n = q[0]/(a*a), q[1]/(b*b)
    factor = 2*dot(d, n)/dot(n, n)
    return d[0]-factor*n[0], d[1]-factor*n[1]


def tangent_lambda(a, b, p, d):
    n = -d[1], d[0]
    return (a*a*n[0]*n[0]+b*b*n[1]*n[1]-dot(n, p)**2)/dot(n,n)


def shoot(a, b, lam, theta, count, diagnostics=False):
    p = a*mp.cos(theta), b*mp.sin(theta)
    d = initial_ray(a, b, lam, theta)
    start, start_d = p, d
    vertices, turns = [], mp.mpf(0)
    residuals = {'boundary': mp.mpf(0), 'caustic': mp.mpf(0),
                 'unit_ray': mp.mpf(0), 'reflection_vs_regenerated': mp.mpf(0),
                 'minimum_travel': mp.inf, 'max_step_angle': mp.mpf(0)}
    for i in range(count):
        vertices.append(p)
        q, travel = boundary_second(a, b, p, d)
        cp, sp, cq, sq = p[0]/a, p[1]/b, q[0]/a, q[1]/b
        increment = mp.atan2(cp*sq-sp*cq, cp*cq+sp*sq)
        if increment <= 0:
            increment += 2*mp.pi
        turns += increment
        new_d = reflect(a, b, q, d)
        if diagnostics:
            residuals['boundary'] = max(residuals['boundary'], abs(cq*cq+sq*sq-1))
            residuals['caustic'] = max(residuals['caustic'], abs(tangent_lambda(a,b,p,d)-lam)/(b*b))
            residuals['unit_ray'] = max(residuals['unit_ray'], abs(dot(d,d)-1))
            regenerated = initial_ray(a,b,lam,mp.atan2(sq,cq))
            residuals['reflection_vs_regenerated'] = max(residuals['reflection_vs_regenerated'], norm(sub(new_d,regenerated)))
            residuals['minimum_travel'] = min(residuals['minimum_travel'], travel)
            residuals['max_step_angle'] = max(residuals['max_step_angle'], increment)
        p, d = q, new_d
    residuals['closure'] = norm(sub(p,start))/a
    residuals['direction_closure'] = norm(sub(d,start_d))
    return vertices, turns, residuals


def periodic_lambda(a, b, n, winding):
    target = 2*mp.pi*winding
    lo = mp.mpf(0)
    hi = b*b*(1-mp.power(10,-mp.mp.dps//2))
    _, angle, _ = shoot(a,b,hi,mp.mpf(0),n)
    if angle < target:
        raise ArithmeticError('Unbracketed winding; increase precision')
    for i in range(int(mp.mp.dps*math.log2(10))+12):
        mid = (lo+hi)/2
        _, angle, _ = shoot(a,b,mid,mp.mpf(0),n)
        if angle < target:
            lo = mid
        else:
            hi = mid
    return (lo+hi)/2


def solve2(u, v, h, k):
    det = u[0]*v[1]-u[1]*v[0]
    if det == 0:
        raise ArithmeticError('Parallel/coincident consecutive lines')
    return ((h*v[1]-u[1]*k)/det, (u[0]*k-h*v[0])/det), det


def construct(a,b,vertices,focus_sign=1,focus_override=None):
    tangent_normals = [(p[0]/(a*a),p[1]/(b*b)) for p in vertices]
    outer, tangent_dets = [], []
    n = len(vertices)
    for i in range(n):
        r, det = solve2(tangent_normals[i],tangent_normals[(i+1)%n],1,1)
        outer.append(r)
        tangent_dets.append(abs(det)/(norm(tangent_normals[i])*norm(tangent_normals[(i+1)%n])))
    m = (focus_sign*mp.sqrt(a*a-b*b),mp.mpf(0)) if focus_override is None else focus_override
    lines = [sub(r,m) for r in outer]
    heights = [dot(lines[i],outer[i]) for i in range(n)]
    anti, normal_dets = [], []
    for i in range(n):
        u, det = solve2(lines[i],lines[(i+1)%n],heights[i],heights[(i+1)%n])
        anti.append(u)
        normal_dets.append(abs(det)/(norm(lines[i])*norm(lines[(i+1)%n])))
    mean = tuple(mp.fsum(u[k] for u in anti)/n for k in (0,1))
    return mean, outer, anti, min(tangent_dets), min(normal_dets)


def serial(x):
    if isinstance(x,mp.mpf):
        return mp.nstr(x,mp.mp.dps)
    if isinstance(x,dict):
        return {k:serial(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):
        return [serial(v) for v in x]
    return x


def run_case(a_text,b_text,n,winding,phases):
    a,b = mp.mpf(a_text),mp.mpf(b_text)
    lam = periodic_lambda(a,b,n,winding)
    means, records = [], []
    for phase in phases:
        vertices,angle,residuals = shoot(a,b,lam,phase,n,True)
        mean,outer,anti,td,nd = construct(a,b,vertices)
        other_mean,*_ = construct(a,b,vertices,-1)
        reverse_mean,*_ = construct(a,b,list(reversed(vertices)))
        means.append(mean)
        records.append({'phase': phase,'mean':mean,
                        'other_focus_mean': other_mean,
                        'reversal_mean_residual': norm(sub(mean,reverse_mean)),
                        'angle_closure_residual':abs(angle-2*mp.pi*winding),
                        'min_scaled_tangent_determinant':td,
                        'min_scaled_normal_determinant':nd,
                        'max_antipedal_vertex_norm_over_a':max(norm(u) for u in anti)/a,
                        'residuals':residuals})
    phase_variation=max(norm(sub(mean,means[0])) for mean in means)/a
    return {'a':a,'b':b,'N':n,'winding':winding,'primitive':math.gcd(n,winding)==1,
            'lambda':lam,'lambda_over_b_squared':lam/(b*b),
            'phase_variation_over_a':phase_variation,
            'all_positive_focus_mean_x_negative':all(mean[0]<0 for mean in means),
            'max_abs_mean_y_over_a':max(abs(mean[1]) for mean in means)/a,
            'records':records}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dps',type=int,default=70)
    parser.add_argument('--mode',choices=['broad','stability','odd'],default='broad')
    parser.add_argument('--output',default=None)
    args = parser.parse_args()
    mp.mp.dps=args.dps
    output=HERE/(args.output or f'{args.mode}_{args.dps}_digits.json')
    phases=[mp.mpf(0),mp.mpf(1)/7,mp.pi/8,mp.mpf('1.123456789'),mp.pi/2,
            mp.mpf('2.718281828')]
    if args.mode=='broad':
        aspects=[('1.0001','1'),('1.2','1'),('5','3'),('3','1'),('10','1')]
        pairs=[(4,1),(6,1),(8,1),(8,3),(10,1),(10,3),(12,1),(12,5),(14,1),(14,3),(14,5),(16,7),(20,3),(24,5),(30,13)]
    elif args.mode=='stability':
        aspects=[('1.0001','1'),('10','1'),('100','1')]
        pairs=[(4,1),(12,5),(30,13)]
    else:
        aspects=[('5','3'),('3','1')]
        pairs=[(3,1),(5,1),(5,2),(7,3)]
    receipt={'started_utc':now(),'python':sys.executable,'python_version':platform.python_version(),
             'mpmath_version':mp.__version__,'precision_decimal_digits':args.dps,
             'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             'argv':sys.argv,'independence':'No submitted source/helper imported. Physical reflection propagation.',
             'validation_class':'High-precision diagnostics, not interval-certified universal proof.'}
    cases,failures=[],[]
    progress=output.with_suffix('.progress.jsonl')
    with progress.open('w') as log:
        for a,b in aspects:
            for n,p in pairs:
                try:
                    row=run_case(a,b,n,p,phases)
                    if args.mode=='odd':
                        # Repeating the odd orbit twice has nominally even count.
                        lam=mp.mpf(row['lambda'])
                        repeated=[]
                        for phase in phases:
                            verts,_,_=shoot(mp.mpf(a),mp.mpf(b),lam,phase,n)
                            oddmean,*_=construct(mp.mpf(a),mp.mpf(b),verts)
                            repeatedmean,*_=construct(mp.mpf(a),mp.mpf(b),verts+verts)
                            repeated.append({'phase':phase,'mean':repeatedmean,'repeat_residual':norm(sub(oddmean,repeatedmean))})
                        row['nominal_even_2N_repeat']=repeated
                    cases.append(serial(row))
                    log.write(json.dumps({'utc':now(),'a':a,'b':b,'N':n,'winding':p,'phase_variation_over_a':serial(row['phase_variation_over_a']),
                                          'min_normal_det':serial(min(x['min_scaled_normal_determinant'] for x in row['records']))})+'\n')
                    log.flush()
                except Exception as ex:
                    failures.append({'a':a,'b':b,'N':n,'winding':p,'exception':repr(ex)})
                    log.write(json.dumps({'utc':now(),'failure':failures[-1]})+'\n')
                    log.flush()
    receipt['finished_utc']=now()
    receipt['case_count']=len(cases)
    receipt['failure_count']=len(failures)
    output.write_text(json.dumps({'receipt':receipt,'cases':cases,'failures':failures},indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
    print('Largest phase variation:',max((mp.mpf(c['phase_variation_over_a']) for c in cases),default=mp.nan))
    print('Failures:',failures)


if __name__=='__main__':
    main()
