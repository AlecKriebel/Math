"""Formal Berezinian and exact genus-one stack arithmetic checks.
This does not verify the actual Goldman form is punctured-super-Kaehler.
"""
import json
from fractions import Fraction as F
from pathlib import Path
import sympy as s
z,zb=s.symbols('z zb')
h=s.Function('h')(z,zb)
g=s.symbols('g')
coefficient=s.diff(h,z,zb)/h-s.diff(h,z)*s.diff(h,zb)/h**2
assert s.simplify(coefficient-s.diff(s.log(h),z,zb))==0
# General local ratio between metrics:
k=s.Function('k')(z,zb)
assert s.simplify(s.diff(s.log(k),z,zb)-s.diff(s.log(h),z,zb)-s.diff(s.log(k/h),z,zb))==0
odd=F(3,2)*F(1,2)*F(1,24)
assert odd==F(1,32)
assert 2*odd==F(1,16)
report={'berezinian_odd_coefficient':'h_zbarz/h-h_z*h_barz/h^2 = partial_z partial_barz log h','berezinian_identity_passed':True,'log_metric_ratio_identity_passed':True,'odd_stack_integral_c1_F_dual':str(odd),'two_equal_parity_contributions':str(2*odd),'actual_punctured_super_kaehler_identification_verified':False,'all_checks_passed':True}
Path(__file__).with_name('SUPER_KAEHLER_LINE_CHECK.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
