#!/usr/bin/env python3
from fractions import Fraction as F
from polycode import hull, exact_code
Q=[(F(-3),F(-3)),(F(3),F(-3)),(F(3),F(3)),(F(-3),F(3))]
P2=hull([(F(0),F(-1)),(F(1),F(1,10)),(F(2),F(1,10)),(F(2),F(-1,10))])
P3=hull([(F(-2),F(-1,10)),(F(2),F(-1,10)),(F(2),F(1,10)),(F(-2),F(1,10))])
P1=hull([(F(-2),F(-1,10)),(F(2),F(-1,10)),(F(2),F(1,10)),(F(0),F(1)),(F(-2),F(1,10))])
H=hull(P1+P2)
D0,_=exact_code(Q,{1:P1,2:P2,3:P3})
assert {'13','123','1','2'} <= D0
Dfirst,_=exact_code(Q,{1:P1,2:P2,3:P1})
assert '1' not in Dfirst and '12' not in Dfirst
Dseq,wseq=exact_code(Q,{1:H,2:P2,3:P1})
assert '1' in Dseq
Dsync,_=exact_code(H,{1:H,2:P2,3:H})
assert Dsync=={'13','123'},Dsync
print('PROTECTED TARGET WITNESSES PASS: 13 AND 123')
print('SEQUENTIAL REPAIR RECREATES WORD 1')
print('SYNCHRONIZED REPAIR EXACT CODE PASS')
