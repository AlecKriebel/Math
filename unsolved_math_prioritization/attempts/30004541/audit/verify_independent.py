#!/usr/bin/env python3
"""Independent finite controls and frozen-byte verification, not a proof checker.

No networking, no writes, no simulations. Requires Python 3 and SymPy.
Usage: python verify_independent.py [--author-dir DIR] [--archive ZIP]
"""
import argparse
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import zipfile
import sympy as S

parser = argparse.ArgumentParser()
parser.add_argument('--author-dir', type=Path, default=Path(__file__).resolve().parent.parent/'derrida_30004541')
parser.add_argument('--archive', type=Path, default=Path(__file__).resolve().parent.parent/'DERRIDA_30004541_AUTHOR_SAFE_FREEZE.zip')
args = parser.parse_args()
records = []
def check(name, ok):
    if not ok:
        raise AssertionError(name)
    records.append({'name': name, 'status': 'PASS'})
def identity(name, value):
    check(name, S.simplify(value) == 0)
def meta(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

# Reproduce, but do not treat the author's finite checks as the mathematical audit.
author = args.author_dir
manifest = json.loads((author/'AUTHOR_MANIFEST.json').read_text())
check('exact author allowlist', set(p.name for p in author.iterdir()) == set(manifest['files']) | {'AUTHOR_MANIFEST.json'})
for name, expected in manifest['files'].items():
    check('author bytes '+name, meta((author/name).read_bytes()) == expected)
archive = args.archive.read_bytes()
check('frozen archive identity', meta(archive) == {'bytes': 24145, 'sha256': '87523ba565a385498b3f779924373a20e3fc0b6c75d596e8d1aa91f4de33b750'})
with zipfile.ZipFile(args.archive) as z:
    check('archive exact member list', set(z.namelist()) == {'derrida_30004541/'+p.name for p in author.iterdir()})
    for name in z.namelist():
        check('archive member '+name, z.read(name) == (author/Path(name).name).read_bytes())
run = lambda script: json.loads(subprocess.check_output([sys.executable, str(author/script)], text=True))
author_controls = run('verify_controls.py')
check('author control output equals frozen output', author_controls == json.loads((author/'EXACT_CHECKS.json').read_text()))
check('author checks 27 PASS', author_controls['status'] == 'PASS' and author_controls['check_count'] == 27)
author_integrity = run('verify_manifest.py')
check('author integrity validator', author_integrity['status'] == 'PASS' and author_integrity['files_checked'] == 9)

# Independent algebra from the jump generator, not imported from the author script.
x, y, theta, rate, p, g, h, j = S.symbols('x y theta rate p g h j')
q = 1-p
pg = q*(rate-p)
rg = -q*rate
identity('density x coefficient', -q*rate*rg - q*q*rate*rate)
identity('density constant coefficient', -pg*rate+q*rg - (-q*rate*rate+(2*p-1)*q*rate))
identity('atom flux balance', pg-(q*rate+p*p-p))
identity('first moment family generator', S.diff(q/rate,p)*pg+S.diff(q/rate,rate)*rg-(q/rate-q))
identity('invariant from direct chain rule', pg/rate + (-p/rate**2+1/rate)*rg)
for n in range(1,5):
    # The jump polynomial separates into mixed moments under independence.
    identity('jump binomial degree '+str(n), (x+y)**n-x**n-sum(S.binomial(n,k)*x**k*y**(n-k) for k in range(n)))

lam = S.Rational(5,2)
moment = lambda k, a: lam*S.factorial(k)/(lam-a)**(k+1)
check('pinned second moment exact', moment(2,0) == S.Rational(8,25))
check('pinned endpoint difference exact', moment(0,1)-moment(1,1) == S.Rational(5,9))
poly = S.expand((lam-theta)**2-theta*(lam-theta)-4*(1-theta))
identity('whole open theta interval square identity', poly-2*(theta-S.Rational(7,8))**2-S.Rational(23,32))
identity('whole theta family integral', moment(0,theta)-theta*moment(1,theta)-2*(1-theta)*moment(2,theta)-lam*poly/(lam-theta)**3)
check('positive all-theta residual and denominator margin', S.Rational(23,32)>0 and lam-1>0)
partial_e = sum(Q(1,S.factorial(k)) for k in range(4))
check('strict e bound relies on positive omitted terms', partial_e == Q(8,3))
check('global p maximum bound', Q(5,2)/partial_e == Q(15,16))
check('integral bound exponent', 16*Q(5,2) == 40)

dg = g*g-(1+theta)*g+theta*p
dh = (2*g-1-theta)*h-g+p
dj = (2*g-1-theta)*j+2*h*h-2*h
b = 2*(1-theta)
phi = g-theta*h-b*j
identity('necessary inequality integrating-factor identity', dg-theta*dh-b*dj-(2*g-1-theta)*phi-2*b*(h-h*h)+g*g-theta*g)
check('sign boundary is not invariant', (dg-dh).subs({theta:1,g:2,h:2,p:0}) == -2)
identity('capped moment scalar majorant', g*g-(1+theta)*g+theta-(g-1)*(g-theta))
a, t, c = S.symbols('a t c', positive=True)
identity('critical q quadratic coefficient', S.limit((1-(1+a)+(1+a)*S.log(1+a))/a**2,a,0)-S.Rational(1,2))
identity('deterministic threshold stationary point', S.diff(S.log(theta)/theta,theta).subs(theta,S.E))
identity('geometric leaf mgf at zero time', (S.exp(-t)*g/(1-(1-S.exp(-t))*g)).subs(t,0)-g)
identity('geometric leaf mgf denominator at blowup threshold', (1-(1-S.exp(-t))*g).subs(t,S.log(g/(g-1))))

z = S.symbols('z')
D = (1+z)**2-4*z*p
identity('stationary root squared identity', D-(1+2*(1-2*p)*z+z*z))
identity('discriminant has nonreal distinct roots', S.discriminant(D,z)+16*p*(1-p))
identity('positive real point remains regular', D.subs(z,1)-4*(1-p))

# Deterministic rational tree controls. Each edge/tree has total height one.
# They stress the implementation; the all-tree assertion is an induction in the audit.
leaf = lambda edge: ('leaf', edge)
node = lambda edge,l,r: ('node',edge,l,r)
trees = [leaf(Q(1)), node(Q(1,3),leaf(Q(2,3)),leaf(Q(2,3))),
         node(Q(1,3),node(Q(1,3),leaf(Q(1,3)),leaf(Q(1,3))),leaf(Q(2,3))),
         node(Q(1,3),node(Q(1,3),leaf(Q(1,3)),leaf(Q(1,3))),node(Q(1,3),leaf(Q(1,3)),leaf(Q(1,3))))]
def count(tree):
    return 1 if tree[0]=='leaf' else count(tree[2])+count(tree[3])
def evaluate(tree, values, cap=None):
    it=iter(values)
    def descend(v):
        amount=next(it) if v[0]=='leaf' else descend(v[2])+descend(v[3])
        if cap is not None:
            amount=min(amount,cap)
        return max(Q(0),amount-v[1])
    return descend(tree)
amounts=[Q(0),Q(1,4),Q(1,2),Q(1),Q(2)]
caps=[Q(1,4),Q(1,2),Q(1),Q(2),Q(4),Q(8)]
tree_cases=0
for tree in trees:
    for values in product(amounts,repeat=count(tree)):
        exact=evaluate(tree,values)
        assert exact>=sum(max(Q(0),v-1) for v in values)
        capped=[evaluate(tree,values,k) for k in caps]
        assert capped==sorted(capped) and all(v<=exact for v in capped)
        assert evaluate(tree,values,sum(values))==exact
        alternate=tuple(v+Q(1,4) for v in values)
        other=evaluate(tree,alternate)
        assert exact<=other and other-exact<=sum(abs(u-v) for u,v in zip(values,alternate))
        tree_cases+=1
check('rational tree cap, lower bound, coupling controls', tree_cases == 780)

# Finite moment obstructions are negative controls only; they do not replace
# the all-p analytic radius/positive-coefficient argument.
obstructions=[]
for atom in [Q(1,100),Q(1,10),Q(1,4),Q(1,2),Q(3,4),Q(9,10),Q(99,100)]:
    coeff=[Q(1),1-atom]
    for n in range(2,513):
        coeff.append(coeff[-1]-sum(coeff[k]*coeff[n-k] for k in range(1,n)))
        if coeff[-1]<0:
            obstructions.append({'atom':str(atom),'first_negative_degree':n,'coefficient':str(coeff[-1])})
            break
    else:
        raise AssertionError('No finite obstruction found for '+str(atom))
check('stationary moment negative controls',len(obstructions)==7)

print(json.dumps({'status':'PASS','named_check_count':len(records),'rational_tree_cases':tree_cases,
                 'stationary_negative_controls':obstructions,'checks':records,
                 'author_controls_reproduced':27,'sympy_version':S.__version__,
                 'simulation_used':False,
                 'limitations':'Finite symbolic/rational/integrity controls only. They do not prove arbitrary-law extinction, establish the infinite theta family without its algebraic argument, or replace the analytic audit.'},indent=2))
