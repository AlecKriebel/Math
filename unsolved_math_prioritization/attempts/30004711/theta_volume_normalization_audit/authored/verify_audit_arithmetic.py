from fractions import Fraction as Q
import json
from pathlib import Path
integral_c1 = -2 * (11*Q(1,24)**2 + Q(1,24)**2 + Q(1,2)*Q(1,24)*Q(1,2))
odd_c1=Q(1,4)*(-Q(1,24))-Q(1,2)*Q(1,2)*Q(1,12)
even_c1=integral_c1-odd_c1
raw=-integral_c1
theta=3*Q(1,24)
assert integral_c1 == -Q(1,16)
assert odd_c1 == even_c1 == -Q(1,32)
assert raw == Q(1,16) and theta == Q(1,8) and 2*raw == theta
assert (-odd_c1)-(-even_c1) == 0
for g in range(10):
    for n in range(10):
        if 2*g-2+n>0:
            r=2*g-2+n
            assert (-1)**r == (-1)**n
            assert (3*g-3+n)-r == g-1
out={'integral_c1_F':str(integral_c1),'integral_c1_F_odd':str(odd_c1),'integral_c1_F_even':str(even_c1),'W_1_1':str(raw),'T_1_1':str(theta),'N_1_1':str(2*raw),'naive_parity_weighted_W_1_1':'0','scope':'Exact rational verification; not a proof of the analytic extension theorem or a torsion-measure identification.'}
Path(__file__).with_name('AUDIT_ARITHMETIC.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
