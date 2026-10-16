"""Exact rational tail bound used only for the fixed Haar-instrument comparison.
The analytic integral and chain-rule argument are given in REPORT.md.
This is not a general LOCC capacity converse.
"""
from fractions import Fraction as Q
import json
N=10
lower=2*sum((Q(1,(2*k+1)*3**(2*k+1)) for k in range(N)),Q(0))
tail=Q(9,4*(2*N+1)*3**(2*N+1))
upper=lower+tail
if not (Q(13,24)<lower<upper<Q(52,75)):
 raise AssertionError('rational ln(2) certificate failed')
print(json.dumps({'status':'PASS_RATIONAL_HAAR_COMPARISON_TAIL_BOUND','ln2_lower':str(lower),'ln2_upper':str(upper),'ln2_upper_less_than_52_over_75':True,'two_c4_equals':'4-13/(6*ln(2))','two_c4_less_than_7_over_8':True,'instrument_scope':'independent local Haar POVMs on 4 by 4; not general LOCC'},indent=2))
