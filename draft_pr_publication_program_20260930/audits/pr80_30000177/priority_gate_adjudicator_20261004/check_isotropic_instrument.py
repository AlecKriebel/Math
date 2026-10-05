#!/usr/bin/env python3
"""Numerical check of an analytic, measurement-specific information bound."""
import json
import math

def c(d):
    return (math.log(d) + 1 - math.fsum(1/k for k in range(1,d+1))) / math.log(2)

def simpson(n):
    def f(t):
        return 0.0 if t in (0.0,1.0) else 12*t*(1-t)**2*math.log2(4*t)
    return math.fsum((4 if k%2 else 2)*f(k/n) for k in range(1,n))/(3*n)

analytic=c(4)
checks=[{'subintervals':n,'pure_output_relative_entropy_bits':simpson(n)} for n in (20000,40000)]
if any(abs(row['pure_output_relative_entropy_bits']-analytic)>5e-8 for row in checks):
    raise SystemExit('integral check failed')
print(json.dumps({
    'eq24_universal_max_bits':1/(306*math.log(2)),
    'single_lab_d4_max_information_bits':analytic,
    'two_labs_d4_product_Haar_information_upper_bound_bits':2*analytic,
    'quadrature_checks_not_interval_certificates':checks,
    'block_Haar_bounds':[{'copies':n,'local_dimension':4**n,'block_bits_upper_bound':2*c(4**n),'per_copy_bits_upper_bound':2*c(4**n)/n} for n in range(1,9)],
    'scope':'Specific independent local isotropic POVMs only; not a converse for general LOCC capacity.'
},indent=2))
