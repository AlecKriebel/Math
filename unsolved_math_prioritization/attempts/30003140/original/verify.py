#!/usr/bin/env python3
"""Exact bounded arithmetic and pinned-packet verification; not a modularity proof."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import warnings
import sympy as sp
from sympy.utilities.exceptions import SymPyDeprecationWarning
warnings.filterwarnings('ignore', category=SymPyDeprecationWarning)

class VerificationError(Exception):
    pass

def need(condition, message):
    if not condition:
        raise VerificationError(message)

X = sp.Symbol('x')
F = {713: [1,-4,2,2,1,-2,1], 893: [1,-2,-3,-2,-2,0,1]}
H = {713: [1,0,-1,1], 893: [1,1,0,1]}
PRIMES = [3,5,7,11,13,17,29,37,41]

def poly(c):
    return sum(a*X**i for i,a in enumerate(c))

def coefficients(f):
    return [int(a) for a in reversed(sp.Poly(f, X).all_coeffs())]

def field(p):
    need(p >= 3 and bool(sp.isprime(p)), 'field requires an odd prime')
    return next(d for d in range(1,p) if pow(d,(p-1)//2,p) == p-1)

def mul(z,w,p,d):
    return ((z[0]*w[0]+d*z[1]*w[1])%p, (z[0]*w[1]+z[1]*w[0])%p)

def evaluate(c,z,p,d):
    r=(0,0)
    for a in reversed(c):
        r=mul(r,z,p,d)
        r=((r[0]+a)%p,r[1])
    return r

def count_odd(c,p,degree):
    d=field(p)
    need(degree in (1,2), 'unsupported field degree')
    elements=[(a,b) for a in range(p) for b in (range(p) if degree==2 else [0])]
    # Independent character/norm and square-fiber counts on the same field.
    square_fibers={}
    for z in elements:
        z2=mul(z,z,p,d)
        square_fibers[z2]=square_fibers.get(z2,0)+1
    character_total=2
    fiber_total=2
    for z in elements:
        value=evaluate(c,z,p,d)
        fiber_total += square_fibers.get(value,0)
        if value == (0,0):
            character_total += 1
        else:
            norm=value[0] if degree==1 else (value[0]**2-d*value[1]**2)%p
            character_total += 2*int(pow(norm,(p-1)//2,p)==1)
    need(character_total==fiber_total, 'character versus square-fiber mismatch')
    return character_total

def mul4(a,b):
    c=0
    for j in range(2):
        if (b>>j)&1:
            c ^= a<<j
    if c&4:
        c ^= 7
    return c

def eval4(c,z):
    r=0
    for a in reversed(c):
        r=mul4(r,z) ^ (a%2)
    return r

def count_two(h,g,degree):
    need(degree in (1,2), 'unsupported binary field degree')
    q=2**degree
    # Two nonsingular points at infinity, since h has leading coefficient one.
    return 2+sum((mul4(y,y)^mul4(eval4(h,z),y))==eval4(g,z)
                 for z in range(q) for y in range(q))

def local_row(p,n1,n2):
    a=p+1-n1
    numerator=a*a-p*p-1+n2
    need(numerator%2==0, 'nonintegral middle coefficient')
    b=numerator//2
    return {'p':p,'count_p':n1,'count_p2':n2,'a':a,'b':b,
            'euler_ascending':[1,-a,b,-p*a,p*p], 'ordinary':b%p!=0}

def f1(a,b):
    return [b,2*b,b+a,b-a,2*b+a,2*a,a,4*b,3*b+2*a,3*b+a,
            3*b,3*b-a,2*b+2*a,2*b,2*b-a,2*b-2*a,b+2*a,
            b+a,b,b-a,b-2*a,a,0,0]

def irreducible_quartic_integer(c):
    # Monic quartic: a rational factor is integral. Check linear and quadratic factors.
    need(len(c)==5 and c[-1]==1 and c[0]!=0, 'quartic format')
    div=[int(d)*sign for d in sp.divisors(abs(c[0])) for sign in (-1,1)]
    for r in div:
        if sum(a*r**i for i,a in enumerate(c))==0:
            return False
    for a in div:
        if c[0]%a:
            continue
        b=c[0]//a
        # (x^2+u*x+a)(x^2+v*x+b): u+v=c3; ub+va=c1.
        if a!=b:
            num=c[1]-c[3]*a
            if num%(b-a):
                continue
            u=num//(b-a); v=c[3]-u
            if u*v+a+b==c[2]:
                return False
        elif c[1]==a*c[3]:
            delta=c[3]**2-4*(c[2]-a-b)
            if delta>=0 and math.isqrt(delta)**2==delta and (c[3]+math.isqrt(delta))%2==0:
                return False
    return True

def calculate():
    out={'problem_id':30003140,'status':'UNSOLVED','approaches_used':5,
         'scope':'bounded arithmetic partials; no Hecke matching or global modularity proof',
         'curves':{},'borcherds_inputs':[]}
    for N,c in F.items():
        f=poly(c); h=poly(H[N]); g=sp.expand((f-h*h)/4)
        gc=coefficients(g)
        need(sp.expand(h*h+4*g-f)==0, 'integral-model identity')
        smooth=sp.gcd(sp.Poly(h,X,modulus=2),
                      sp.Poly(sp.diff(g,X)**2+sp.diff(h,X)**2*g,X,modulus=2))
        need(smooth.degree()==0, 'singular characteristic-two model')
        disc=int(sp.discriminant(f,X))
        need(disc==4096*N, 'unexpected discriminant')
        rows=[local_row(2,count_two(H[N],gc,1),count_two(H[N],gc,2))]
        for p in PRIMES:
            need(disc%p!=0,'bad prime in good-prime list')
            rows.append(local_row(p,count_odd(c,p,1),count_odd(c,p,2)))
        bad=[]
        for p in sp.factorint(N):
            p=int(p)
            common=sp.gcd(sp.Poly(f,X,modulus=p),sp.Poly(sp.diff(f,X),X,modulus=p))
            need(common.degree()==1, 'not exactly one double root')
            r=(-int(common.all_coeffs()[1]))%p
            quartic,remainder=sp.div(sp.Poly(f,X,modulus=p),sp.Poly((X-r)**2,X,modulus=p))
            need(remainder.is_zero,'node normalization division')
            need(sp.gcd(quartic,quartic.diff()).degree()==0, 'singular normalization')
            value=int(quartic.eval(r))%p
            need(value!=0,'not an ordinary node')
            epsilon=1 if pow(value,(p-1)//2,p)==1 else -1
            ec=2+sum(1 if (v:=int(quartic.eval(a))%p)==0 else
                     2*int(pow(v,(p-1)//2,p)==1) for a in range(p))
            ae=p+1-ec
            bad.append({'p':p,'double_root':r,'normalization_ascending':coefficients(quartic.as_expr()),
                        'node_value':value,'epsilon':epsilon,'elliptic_count':ec,'elliptic_trace':ae,
                        'euler_ascending':coefficients((1-epsilon*X)*(1-ae*X+p*X*X))})
        out['curves'][str(N)]={'sextic_ascending':c,'h_ascending':H[N],
             'g_ascending':gc,'discriminant':disc,'good_factors':rows,'bad_factors':bad,
             'local_root_number_product':math.prod(-b['epsilon'] for b in bad)}
    # The two proposed parameterizations at level 713 produce identical inputs.
    inflation=[5,3,3,3,2,2,2]+[1]*17
    for a,b in [(1,4),(-5,3),(5,3)]:
        d=list(map(abs,f1(a,b))); e=[c*t for c,t in zip(inflation,d)]
        need(len(d)==24 and d.count(0)==2,'theta-block weight')
        out['borcherds_inputs'].append({'parameters':[a,b],'weight':2,
            'index':sum(t*t for t in d)//2,'inflated_index':sum(t*t for t in e)//2,
            'phi_entries':sorted(t for t in d if t),'xi_entries':sorted(t for t in e if t),
            'm':math.prod(c for c,t in zip(inflation,d) if t==0),'q_order':2})
    aa,bb,_=out['borcherds_inputs']
    need(aa['phi_entries']==bb['phi_entries'] and aa['xi_entries']==bb['xi_entries'],
         'duplicate 713 Borcherds input mismatch')
    u=X**3+X**2-1; v=X**3-3*X**2+4*X-1
    need(sp.expand(u*v-poly(F[713]))==0,'cubic factorization')
    need(all(z.subs(X,r)!=0 for z in (u,v) for r in (-1,1)), 'reducible cubic')
    out['residual']={'713':{'factor_degrees':[3,3],'cubic_discriminants':[int(sp.discriminant(u,X)),int(sp.discriminant(v,X))],
        'resultant':int(sp.resultant(u,v,X)),'group':'S3 x S3','representation':'reducible 2+2'},
        '893':{'frobenius_factorizations':[],'group':'S6','representation':'absolutely irreducible'}}
    for p in (3,7,349):
        fac=sp.factor_list(poly(F[893]),modulus=p)[1]
        need(all(m==1 for _,m in fac),'ramified factorization witness')
        out['residual']['893']['frobenius_factorizations'].append({'p':p,
            'factors_ascending':[coefficients(g) for g,m in fac],
            'degrees':sorted(int(sp.degree(g)) for g,m in fac)})
    need([r['degrees'] for r in out['residual']['893']['frobenius_factorizations']]==[[6],[1,5],[1,1,1,1,2]],
         'S6 witnesses missing')
    # Rational simplicity certificates used with the cited semistable/nonsquare-conductor lemma.
    q713=[121,-22,-6,-2,1]; q893=[25,20,11,4,1]
    need(bool(sp.Poly(poly(q713),X,modulus=3).is_irreducible),'713 simple-reduction certificate')
    need(irreducible_quartic_integer(q893),'893 simple-reduction certificate')
    out['simplicity']={'713':{'prime':11,'characteristic_ascending':q713,'irreducible_modulus':3},
                       '893':{'prime':5,'characteristic_ascending':q893,'method':'all possible integral factors excluded'}}
    twist=120121
    need(bool(sp.isprime(twist)) and twist%(8*3*5*7*11*13)==1,'twist witness')
    out['finite_match_control']={'twist_prime':twist,'matching_primes':[2,3,5,7,11,13],
        'new_conductor_multiplier':twist**4,'warning':'changes conductor; not a counterexample at fixed level'}
    return out

def validate_certificate(c):
    need(type(c) is dict, 'certificate object required')
    actual=calculate()
    # Canonical serialization rejects type substitutions such as true for 1.
    need(json.dumps(c,sort_keys=True,separators=(',',':'))==
         json.dumps(actual,sort_keys=True,separators=(',',':')), 'arithmetic certificate mismatch')
    return {'curves':2,'good_prime_factors':20,'bad_prime_factors':4,
            'theta_parameterizations':3,'galois_witness_primes':3,
            'status':'PASS_BOUNDED_ARITHMETIC_ONLY'}

def verify_inventory(root, expected):
    manifest_path=root/'MANIFEST.json'
    data=manifest_path.read_bytes()
    need(hashlib.sha256(data).hexdigest()==expected,'manifest pin mismatch')
    manifest=json.loads(data)
    need(type(manifest) is dict and set(manifest)=={'files','exceptions'},'manifest schema')
    need(manifest['exceptions']==['MANIFEST.json is externally pinned and excludes itself'], 'manifest exceptions')
    wanted=set(manifest['files'])|{'MANIFEST.json'}
    entries=list(root.rglob('*'))
    need(not any(p.is_symlink() for p in entries),'symlink forbidden')
    seen={p.relative_to(root).as_posix() for p in entries if p.is_file()}
    need(seen==wanted,'packet inventory mismatch')
    for name,meta in manifest['files'].items():
        need(not Path(name).is_absolute() and '..' not in Path(name).parts,'unsafe manifest path')
        raw=(root/name).read_bytes()
        need(len(raw)==meta['bytes'] and hashlib.sha256(raw).hexdigest()==meta['sha256'], 'file hash mismatch: '+name)
    return len(manifest['files'])

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--manifest-sha',required=True)
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    n=verify_inventory(root,args.manifest_sha)
    result=validate_certificate(json.loads((root/'certificate.json').read_text()))
    result.update({'manifest_files':n,'external_sources':'NOT_REPLAYED_METADATA_ONLY',
        'global_modularity':'NOT_PROVED','optimization':sys.flags.optimize})
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':
    try:
        main()
    except Exception as error:
        print('VERIFICATION_ERROR: '+str(error),file=sys.stderr)
        raise SystemExit(2)
