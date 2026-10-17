#!/usr/bin/env python3
"""Independent exact-arithmetic checks; this does not prove infinite events."""
from fractions import Fraction as F
import json

def require(test, label):
    if not test:
        raise RuntimeError(label)

p0, p, length = F(9,10), F(19,20), 100
q = p**length
z = 3*(1-p0)
finite_cluster_upper = F(4,3)*(z/(1-z)**2-z)
survival_lower = 1-finite_cluster_upper
bridge_upper = F(8,3)*F(3,32)**4/(1-F(3,32))**2
joint_lower = survival_lower**2*(1-bridge_upper)
require(0 < p0 < p < 1, 'strict parameter ordering')
require(F(20,19)**20 > 2, 'binomial block')
require(q < F(1,32), 'effective weak probability')
require(finite_cluster_upper == F(102,245), 'quadrant series')
require(survival_lower == F(143,245), 'survival lower bound')
require(bridge_upper == F(27,107648) < F(1,1000), 'bridge upper bound')
require(joint_lower == F(2200741829,6461571200) > F(1,3), 'nonuniqueness lower bound')
require(joint_lower-F(1,3) == F(140654287,19384713600), 'strict one-third margin')
print(json.dumps({
    'status':'PASS: independent exact arithmetic',
    'p0':str(p0),'p':str(p),'replacement_length':length,
    'weak_probability_less_than_1_over_32': True,
    'quadrant_finite_cluster_upper':str(finite_cluster_upper),
    'quadrant_survival_lower':str(survival_lower),
    'bridge_strict_upper':str(bridge_upper),
    'nonuniqueness_strict_lower':str(joint_lower),
    'margin_above_one_third':str(joint_lower-F(1,3)),
    'mathematical_dependencies':'Finite dual-boundary parity, infinite-event path union bounds, and disjoint sigma-field independence are proved in the audited manuscript; arithmetic does not replace them.'
},indent=2)+'\n',end='')
