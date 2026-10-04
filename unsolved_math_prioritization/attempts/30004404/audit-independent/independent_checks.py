#!/usr/bin/env python3
"""Independent exact controls for 30004404. No topology/novelty certification.

Uses string erasure rather than the author's word stack, and homogeneous
integer matrices rather than the author's semidirect-product pair arithmetic.
Run: python3 independent_checks.py [path/to/frozen/package]
"""
from pathlib import Path
from fractions import Fraction
from itertools import product
from functools import lru_cache
import hashlib
import json
import subprocess
import sys

PACKAGE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'package'
BINDING = '4f6575af14a3e8b72e61202c45e411b4febcaa7770c3e7e8af45576eda6218f8'
manifest_bytes = (PACKAGE / 'FROZEN_MANIFEST.json').read_bytes()
assert hashlib.sha256(manifest_bytes).hexdigest() == BINDING
manifest = json.loads(manifest_bytes)
listed = {x['path'] for x in manifest['files']}
actual = {str(x.relative_to(PACKAGE)) for x in PACKAGE.rglob('*') if x.is_file()}
assert actual == listed | {'FROZEN_MANIFEST.json'}
for entry in manifest['files']:
    data = (PACKAGE / entry['path']).read_bytes()
    assert len(data) == entry['bytes']
    assert hashlib.sha256(data).hexdigest() == entry['sha256']

def invword(s):
    return s[::-1].swapcase()

def erase(s):
    while True:
        t = s
        for pair in ('xX', 'Xx', 'yY', 'Yy'):
            s = s.replace(pair, '')
        if s == t:
            return s

def commword(s, t):
    return s + t + invword(s) + invword(t)

c = commword('x', 'y')
d = 'x' + c + 'X'
w = erase(commword(c, d))
assert w == 'xyXYxxyXYXyxxYXX' and len(w) == 16
assert erase(w + invword(w)) == ''
assert erase('xyYX') == ''
assert erase(commword('x', 'x')) == ''
assert w != ''

I = ((1,0,0),(0,1,0),(0,0,1))
def mm(a, b):
    # Independent row/column dot products on full homogeneous matrices.
    return tuple(tuple(sum(x*y for x,y in zip(row,col)) for col in zip(*b)) for row in a)

def determinant(a):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
            -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
            +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))

@lru_cache(None)
def inverse(a):
    det = determinant(a)
    assert det in (-1,1)
    cof = []
    for i in range(3):
        row=[]
        for j in range(3):
            minor = [[a[r][s] for s in range(3) if s != j] for r in range(3) if r != i]
            row.append(((-1)**(i+j))*(minor[0][0]*minor[1][1]-minor[0][1]*minor[1][0]))
        cof.append(row)
    answer=tuple(tuple(cof[j][i]//det for j in range(3)) for i in range(3))
    assert mm(a,answer) == mm(answer,a) == I
    return answer

def mpow(a,n):
    if n < 0:
        a, n = inverse(a), -n
    result=I
    for _ in range(n):
        result=mm(result,a)
    return result

def ev(s,x,y):
    letters={'x':x,'X':inverse(x),'y':y,'Y':inverse(y)}
    z=I
    for letter in s:
        z=mm(z,letters[letter])
    return z

matrices = {
    'hyperbolic': ((2,1),(1,1)),
    'identity': ((1,0),(0,1)),
    'unipotent': ((1,1),(0,1)),
    'reflection': ((1,0),(0,-1)),
    'rotation': ((0,-1),(1,0)),
}
model_results=[]
for name,A in matrices.items():
    T=((A[0][0],A[0][1],0),(A[1][0],A[1][1],0),(0,0,1))
    cases=[]
    for n,u,v in product(range(-2,3),range(-1,2),range(-1,2)):
        P=mpow(T,n)
        cases.append(((P[0][0],P[0][1],u),(P[1][0],P[1][1],v),(0,0,1)))
    count=0
    noncommuting=0
    for X,Y in product(cases,repeat=2):
        C=ev(c,X,Y)
        assert C[0][:2]==(1,0) and C[1][:2]==(0,1) and C[2]==(0,0,1)
        assert ev(w,X,Y)==I
        noncommuting += (C != I)
        count+=1
    if name=='identity':
        assert noncommuting==0
    else:
        assert noncommuting>0
    model_results.append({'monodromy':name,'ordered_parameter_pairs':count,'noncommuting_pairs':noncommuting,'witness_identity_pairs':count})

# A non-metabelian ambient test rejects a script that forces w to be trivial everywhere.
X=((1,2,0),(0,1,0),(0,0,1))
Y=((1,0,0),(2,1,0),(0,0,1))
nonmetabelian_w=ev(w,X,Y)
assert nonmetabelian_w != I
assert ev('x',X,Y)==X and ev('y',X,Y)==Y

bases=((2,3,7),(2,4,5),(3,3,4))
# Calculate orbifold chi using an independent common-denominator numerator.
chis=[]
for a,b,c_ in bases:
    chis.append(Fraction(b*c_+a*c_+a*b-a*b*c_,a*b*c_))
assert chis == [Fraction(-1,42),Fraction(-1,20),Fraction(-1,12)]
assert Fraction(3*6+2*6+2*3-2*3*6,2*3*6)==0
assert Fraction(3*5+2*5+2*3-2*3*5,2*3*5)==Fraction(1,30)
exceptional={Fraction(p,1) for p in range(-4,5)}
toroidal={Fraction(0),Fraction(-4),Fraction(4)}
seifert={Fraction(s*i) for s in (-1,1) for i in (1,2,3)}
assert toroidal.isdisjoint(seifert) and toroidal|seifert==exceptional
# Rational-slope convention guards; they do not prove the classification.
assert Fraction(0,1) in toroidal
assert Fraction(1,2) not in exceptional and Fraction(5,1) not in exceptional

run = subprocess.run([sys.executable,str(PACKAGE/'controls/check.py')],capture_output=True,check=True)
assert not run.stderr
assert run.stdout == (PACKAGE/'controls/expected.json').read_bytes()
print(json.dumps({
    'result':'PASS',
    'frozen_manifest_sha256':BINDING,
    'frozen_files_verified':len(listed),
    'author_output_byte_identical':True,
    'free_reduced_word':w,
    'free_reduced_word_length':len(w),
    'independent_affine_matrix_models':model_results,
    'all_independent_witness_identity_pairs':sum(x['ordered_parameter_pairs'] for x in model_results),
    'nonmetabelian_negative_control_word_matrix':nonmetabelian_w,
    'orbifold_euler_characteristics':list(map(str,chis)),
    'exceptional_partition_from_cited_classification':sorted(map(int,exceptional)),
    'limits':['Finite checks do not establish topology, all-slope classification, or novelty.',
              'Generic metabelian proof and source inspection are in AUDIT.md.',
              'The matrix parameterization need not be faithful for finite-order monodromy.'],
},indent=2,sort_keys=True))
