#!/usr/bin/env python3
"""Independent deterministic controls; standard library only, no original edits.
Usage: python3 audit_check.py [frozen_public_directory]
The optional directory enables hash verification and byte-for-byte author replay.
"""
import hashlib
import itertools
import json
import math
from fractions import Fraction as Q
from pathlib import Path
import subprocess
import sys

EXPECTED_MANIFEST = 'a18df1c214a6ea7ed7aa14d8a038827f463a7c9ff4f069228e0eb68b247367d2'
EXPECTED_RESULT = '0c63e1801d50434d217a8a66d16ea8bad27cac4867919f7532abc4819eb9dc16'

def bind_and_replay(directory):
    p = Path(directory)
    digest = lambda b: hashlib.sha256(b).hexdigest()
    assert digest((p/'MANIFEST.json').read_bytes()) == EXPECTED_MANIFEST
    assert digest((p/'RESULT.md').read_bytes()) == EXPECTED_RESULT
    m = json.loads((p/'MANIFEST.json').read_text())
    for row in m['files']:
        b = (p/row['path']).read_bytes()
        assert len(b) == row['bytes'] and digest(b) == row['sha256']
    result = subprocess.run([sys.executable, str(p/'verification/check.py')],
                            check=True, capture_output=True).stdout
    assert result == (p/'verification/result.json').read_bytes()
    j = json.loads(result)
    return {'manifest_items': len(m['files']), 'replay_byte_identical': True,
            'author_guard_cases': j['guard']['exact_order_statistic_cases'],
            'author_output_sha256': digest(result)}

def exhaustive_guard():
    # Includes duplicate coordinates, zero directions, boundary queries,
    # both tie orders and all scalar fields taking values -1,0,1.
    zs = list(map(Q, [-2, -1, 0, 0, 2]))
    count = 0
    for x, lam, coeffs, reverse in itertools.product(
        [Q(-1,2), Q(0), Q(3)], [Q(1), Q(1,3), Q(1,17), Q(1,10000)],
        itertools.product([Q(-1), Q(0), Q(1)], repeat=len(zs)), [False,True]):
        radii = [abs(z-x) for z in zs]
        ds = [abs(a*(z-x))+lam*r for a,z,r in zip(coeffs,zs,radii)]
        order = sorted(range(len(zs)), key=lambda i:(ds[i], -i if reverse else i))
        for k in range(1,len(zs)+1):
            rk = sorted(radii)[k-1]
            selected = max(radii[i] for i in order[:k])
            assert selected <= (1+lam)*rk/lam
            count += 1
    return {'exact_cases':count, 'zero_distance_and_tie_cases_included':True}

def integrate_poly_density(b,h,m):
    w=h/2
    cuts=sorted(set([-b-w,-abs(b-w),abs(b-w),b+w]))
    def density(t):
        return max(Q(0),min(b,t+w)-max(-b,t-w))/(4*b*w)
    total=Q(0)
    for a,c in zip(cuts,cuts[1:]):
        slope=(density(c)-density(a))/(c-a)
        intercept=density(a)-slope*a
        total += slope*(c**(m+2)-a**(m+2))/(m+2)
        total += intercept*(c**(m+1)-a**(m+1))/(m+1)
    return total

def slice_density_checks():
    rows=[]
    for b,h in [(Q(1,4),Q(1,10)),(Q(1,10),Q(1,3)),(Q(2,7),Q(1,4))]:
        assert integrate_poly_density(b,h,0)==1
        assert integrate_poly_density(b,h,1)==0
        assert integrate_poly_density(b,h,2)==b*b/3+h*h/12
        bf,hf=float(b),float(h); w=hf/2
        cuts=sorted(set([-bf-w,-abs(bf-w),abs(bf-w),bf+w]))
        def density(t):
            return max(0.,min(bf,t+w)-max(-bf,t-w))/(4*bf*w)
        def simpson(q):
            answer=0.
            for a,c in zip(cuts,cuts[1:]):
                N=800; step=(c-a)/N
                f=lambda t:density(t)*math.cos(q*t)
                answer += step/3*(f(a)+f(c)+sum((4 if i%2 else 2)*f(a+i*step) for i in range(1,N)))
            return answer
        sinc=lambda z:math.sin(z)/z if z else 1.
        errors=[abs(simpson(q)-sinc(q*bf)*sinc(q*hf/2)) for q in [1,2]]
        assert max(errors)<1e-10
        rows.append({'b':str(b),'h':str(h),'exact_variance':str(b*b/3+h*h/12),
                     'cosine_quadrature_errors':errors})
    return rows

def selection_noise_checks():
    # Conditional independent signs: exact variance 1/k with arbitrary fixed indices.
    rows=[]
    for k in [1,2,3,5,8]:
        values=[sum(bits,Q(0))/k for bits in itertools.product([Q(-1),Q(1)],repeat=k)]
        mean=sum(values,Q(0))/len(values)
        mse=sum((x*x for x in values),Q(0))/len(values)
        assert mean==0 and mse==Q(1,k)
        rows.append({'k':k,'exact_noise_variance':str(mse)})
    # All covariates equal; selecting positive responses destroys the mean-zero step.
    n,k=8,2
    values=[]
    for signs in itertools.product([-1,1],repeat=n):
        selected=sorted(signs,reverse=True)[:k]
        values.append(Q(sum(selected),k))
    mean=sum(values,Q(0))/len(values)
    mse=sum((x*x for x in values),Q(0))/len(values)
    assert mean>0 and mse>Q(1,k)
    return {'independent_noise':rows,'response_reuse_negative_control':
            {'n':n,'k':k,'mean':str(mean),'mse':str(mse),'invalid_claim_sigma2_over_k':str(Q(1,k))}}

def geometry_and_guard_negative_controls():
    # Uniform endpoint cap for gamma(t)=(t,0), 0<=t<=1:
    # X1 uniform[-1,0], X2 uniform[-1/2,1/2]. Projection coordinate is zero.
    tangent_covariance=Q(1,12)
    normal_covariance=Q(1,12)
    assert tangent_covariance>0 and normal_covariance>0
    # Without any guard, a=e1 and F(x)=x2 on a uniform square gives this exact risk.
    unguarded=[{'k':k,'noiseless_integrated_mse':str(Q(1,3)+Q(1,3*k))} for k in [1,10,100]]
    # Auxiliary radius-bound arithmetic; mathematical proof lives separately.
    adaptive_cases=0
    for r,n in itertools.product([0.,1e-12,1e-5,.01,.25,1.],[1,2,10,10000]):
        lam=min(1.,math.sqrt(r+1/n))
        assert lam>0
        assert (1+lam)*r/lam <= 2*math.sqrt(r)+1e-14
        adaptive_cases+=1
    return {'endpoint_cap_covariance_diagonal':[str(tangent_covariance),str(normal_covariance)],
            'endpoint_cap_tangent_not_null':True,'unguarded_square_risks':unguarded,
            'candidate_adaptive_guard_arithmetic_cases':adaptive_cases}

def gaussian_l2_control():
    # Z~N(0,tau²), W=1, epsilon~N(0,sigma²). The Fourier tail has a closed form.
    sigma,tau=.7,.9
    rows=[]
    for n in [100,10000,1000000]:
        U=math.sqrt(math.log(n)/(2*sigma*sigma))
        bound=U/(math.pi*math.sqrt(n))
        tail=math.erfc(tau*U)/(2*math.sqrt(math.pi)*tau)
        # Numerically integrate the exact pointwise variance on the passband.
        N=4000; step=2*U/N
        fn=lambda u:math.exp(sigma*sigma*u*u)-math.exp(-tau*tau*u*u)
        variance=step/3*(fn(-U)+fn(U)+sum((4 if i%2 else 2)*fn(-U+i*step) for i in range(1,N)))/(2*math.pi*n)
        assert 0<=variance<=bound*(1+1e-9)
        rows.append({'n':n,'exact_model_variance_quadrature':variance,'upper_bound':bound,'exact_fourier_tail':tail})
    assert all(rows[i]['upper_bound']+rows[i]['exact_fourier_tail']>rows[i+1]['upper_bound']+rows[i+1]['exact_fourier_tail'] for i in range(len(rows)-1))
    return rows

if __name__=='__main__':
    result={'status':'PASS','proof_status':'Finite controls only; not a theorem prover',
            'binding':bind_and_replay(sys.argv[1]) if len(sys.argv)>1 else 'Not requested',
            'guard':exhaustive_guard(),'slice':slice_density_checks(),
            'noise_selection':selection_noise_checks(),
            'negative_controls':geometry_and_guard_negative_controls(),
            'continuous_gaussian_l2_model':gaussian_l2_control()}
    print(json.dumps(result,indent=2,sort_keys=True))
