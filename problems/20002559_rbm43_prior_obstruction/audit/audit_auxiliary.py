#!/usr/bin/env python3
"""Check auxiliary source data without importing or executing source code.

Inputs: public positive_controls.json and the separately supplied prior report.
Output: result metadata only; neither input is redistributed by this script.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from math import lcm,prod
from pathlib import Path
import re
import sys


def need(ok,msg):
    if not ok:
        raise ValueError(msg)


def bareiss(matrix):
    a=[list(row) for row in matrix]
    previous=1
    sign=1
    for k in range(len(a)-1):
        pivot=next((i for i in range(k,len(a)) if a[i][k]),None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k],a[pivot]=a[pivot],a[k]
            sign=-sign
        for i in range(k+1,len(a)):
            for j in range(k+1,len(a)):
                numerator=a[k][k]*a[i][j]-a[i][k]*a[k][j]
                need(numerator%previous == 0,'Bareiss nonexact division')
                a[i][j]=numerator//previous
            a[i][k]=0
        previous=a[k][k]
    return sign*a[-1][-1]


def audit_positive(data):
    p=data['parity_plus_one']
    theta=list(map(F,p['parameters']))
    need(len(theta) == 19,'parameter count')
    def stats(x,h):
        return (1,)+x+h+tuple(hj*xi for hj in h for xi in x)
    states=list(product(list(product((0,1),repeat=4)),list(product((0,1),repeat=3))))
    energies=[sum(a*b for a,b in zip(theta,stats(x,h)[1:])) for x,h in states]
    maximum=max(energies)
    face=[z for z,e in zip(states,energies) if e == maximum]
    expected_face=[(tuple(z['x']),tuple(z['h'])) for z in p['face']]
    need(set(face) == set(expected_face) and len(expected_face) == len(set(expected_face)) == 10,'exposed face')
    need(maximum == F(p['maximum']) == 4,'maximum')
    gap=maximum-max(e for e in energies if e < maximum)
    need(gap == F(1,4),'gap')
    visible={x for x,h in face}
    desired={x for x in product((0,1),repeat=4) if sum(x)%2 == 0}|{(0,0,0,1)}
    need(visible == desired,'parity-plus-one projection')
    cols=p['minor_columns_zero_based']
    need(len(set(cols)) == 10 and all(type(i) is int and 0 <= i < 20 for i in cols),'minor columns')
    minor=[[stats(x,h)[i] for i in cols] for x,h in expected_face]
    determinant=bareiss(minor)
    need(determinant == F(p['minor_determinant']) == 1,'minor determinant')
    inverse=[list(map(F,row)) for row in p['minor_inverse']]
    for a,b in [(minor,inverse),(inverse,minor)]:
        for i in range(10):
            for j in range(10):
                need(sum(a[i][k]*b[k][j] for k in range(10)) == int(i==j),'inverse')
    q=list(map(F,data['quantitative']['positive_counterexample']))
    support=data['quantitative']['uniform_support']
    need(len(q) == 16 and sum(q) == 1 and min(q) > 0,'positive target')
    need(sum(q[i] for i in range(16) if i not in support) < (min(q[i] for i in support)/8)**4,'positive inequality violation')
    return {'joint_states_checked':128,'maximum_energy':str(maximum),'next_energy_gap':str(gap),'exposed_joint_states':len(face),'visible_states':len(visible),'interpolation_minor_determinant':str(determinant),'both_inverse_products_identity':True,'published_positive_target_normalized_and_excluded':True}


def audit_chart(text):
    matrices=re.findall(r'\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}',text,re.S)
    need(len(matrices) == 1,'prior weight matrix ambiguity')
    weights=[[int(x.strip()) for x in row.strip().split('&')] for row in matrices[0].strip().split('\\\\')]
    need(len(weights) == 3 and all(len(row) == 4 for row in weights),'prior matrix shape')
    jacobian=[]
    for x in list(product((0,1),repeat=4))[1:]:
        sigmoids=[F(z,1+z) for z in [prod(w**b for w,b in zip(row,x)) for row in weights]]
        jacobian.append([F(b) for b in x]+[s-F(1,2) for s in sigmoids]+[b*s for s in sigmoids[:2] for b in x])
    scales=[lcm(*(z.denominator for z in row)) for row in jacobian]
    integers=[[int(z*s) for z in row] for row,s in zip(jacobian,scales)]
    det=F(bareiss(integers),prod(scales))
    match=re.search(r'-\\frac\{(429\d+)\}\s*\{(118\d+)\}',text)
    need(match is not None,'prior determinant location')
    stated=-F(int(match[1]),int(match[2]))
    need(det == stated and det != 0,'prior exact determinant')
    return {'rank':15,'determinant':str(det),'method':'row-denominator clearing followed by fraction-free Bareiss elimination','implication':'local full dimension only; not universality'}


def main():
    pb=Path(sys.argv[1]).read_bytes()
    rb=Path(sys.argv[2]).read_bytes()
    need(sha256(pb).hexdigest() == '913a06971f4fe41c7535aadb61b4733874e76d035c80d370a5770cae90feec68','positive controls hash pin')
    out={'status':'PASS','python_optimized':sys.flags.optimize,'positive_controls_sha256':sha256(pb).hexdigest(),'positive_controls_bytes':len(pb),'parity_plus_one':audit_positive(json.loads(pb)),'prior_local_chart':audit_chart(rb.decode())}
    print(json.dumps(out,sort_keys=True,indent=2))

if __name__ == '__main__':
    main()
