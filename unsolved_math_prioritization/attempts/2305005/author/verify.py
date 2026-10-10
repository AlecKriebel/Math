#!/usr/bin/env python3
"""Data integrity and exact finite controls. This does not prove the open claim."""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

class Invalid(ValueError):
    pass

def need(condition, message):
    if not condition:
        raise Invalid(message)

def integer(x, minimum=0):
    need(type(x) is int and x >= minimum, 'invalid exact integer')
    return x

def keys(obj, expected):
    need(type(obj) is dict and set(obj) == set(expected), 'invalid object schema')

def pairs(xs):
    out = {}
    for k, v in xs:
        need(k not in out, 'duplicate JSON key')
        out[k] = v
    return out

def no_constant(x):
    raise Invalid('non-finite JSON number')

def finite_tree(x):
    # No floats are used anywhere in this exact packet, finite or otherwise.
    need(type(x) in (dict, list, str, int, bool, type(None)), 'inexact or unsupported JSON type')
    if type(x) is dict:
        for k, v in x.items():
            need(type(k) is str, 'nonstring key')
            finite_tree(v)
    elif type(x) is list:
        for v in x:
            finite_tree(v)

def decode(b):
    x = json.loads(b.decode('utf-8'), object_pairs_hook=pairs, parse_constant=no_constant)
    finite_tree(x)
    return x

def digest(b):
    return hashlib.sha256(b).hexdigest()

def hex64(x):
    need(type(x) is str and re.fullmatch('[0-9a-f]{64}', x) is not None, 'invalid digest')
    return x

def validate_inventory(root, pin):
    need(root.is_dir() and not root.is_symlink(), 'root must be a real directory')
    mp = root / 'MANIFEST.json'
    need(mp.is_file() and not mp.is_symlink(), 'manifest must be a regular file')
    b = mp.read_bytes()
    need(digest(b) == hex64(pin), 'external manifest pin mismatch')
    man = decode(b)
    keys(man, ['schema', 'problem_id', 'files'])
    need(type(man['schema']) is int and man['schema'] == 1, 'manifest version')
    need(type(man['problem_id']) is int and man['problem_id'] == 2305005, 'manifest problem')
    need(type(man['files']) is list and man['files'], 'empty manifest')
    paths = set()
    for ent in man['files']:
        keys(ent, ['path', 'bytes', 'sha256'])
        s = ent['path']
        need(type(s) is str and s != 'MANIFEST.json', 'invalid path')
        p = PurePosixPath(s)
        need(not p.is_absolute() and str(p) == s and all(t not in ('', '.', '..') for t in s.split('/')) and '\\' not in s, 'unsafe path')
        need(s not in paths, 'duplicate path')
        paths.add(s)
        size = integer(ent['bytes'])
        h = hex64(ent['sha256'])
        q = root
        for component in p.parts:
            q = q / component
            need(not q.is_symlink(), 'symlink forbidden')
        need(q.is_file(), 'payload missing')
        data = q.read_bytes()
        need(len(data) == size and digest(data) == h, 'payload hash/size mismatch')
    actual = set()
    for p in root.rglob('*'):
        need(not p.is_symlink(), 'inventory symlink')
        if p.is_file():
            actual.add(p.relative_to(root).as_posix())
        else:
            need(p.is_dir(), 'special file')
    need(actual == paths | {'MANIFEST.json'}, 'inventory mismatch')
    return len(paths)

def ceiling(x):
    return -((-x.numerator) // x.denominator)

def nearest(x):
    # Either choice at a half-integer is mathematically valid.
    return (x + Q(1,2)).numerator // (x + Q(1,2)).denominator

def height(x):
    need(type(x) is Q and x >= 0, 'height domain')
    k = 0
    while Q((1 << (k+1))-1) <= x:
        k += 1
    left = Q((1 << k)-1)
    return Q(4)+Q(k,16)+(x-left)/Q(16*(1 << k))

def verify_math(root):
    f = decode((root/'FIXTURES.json').read_bytes())
    keys(f, ['schema','problem_id','log_square_coefficients','geometry','lacunary','parabola_identity_parameters'])
    need(type(f['schema']) is int and f['schema']==1, 'fixture schema')
    need(type(f['problem_id']) is int and f['problem_id']==2305005, 'fixture problem')
    coeff = f['log_square_coefficients']
    need(type(coeff) is list and len(coeff)==64, 'coefficient inventory')
    counts = {'coefficient_identities':0,'lattice_upper_cases':0,'lattice_lower_cases':0,'height_lipschitz_cases':0,'parabola_identities':0,'lacunary_inequalities':0,'bernoulli_coefficient_bounds':0}
    for expected_n, rec in enumerate(coeff,1):
        keys(rec,['n','numerator','denominator'])
        n = integer(rec['n'],1)
        need(n == expected_n, 'coefficient index')
        val = Q(integer(rec['numerator']),integer(rec['denominator'],1))
        if n%2:
            derived = Q(0)
        else:
            m = n//2
            derived = Q(4,m)*sum((Q(1,2*j-1) for j in range(1,m+1)),Q(0))
        # Independent direct convolution, compared to the harmonic identity.
        convolution = sum((Q(4,j*(n-j)) for j in range(1,n) if j%2 and (n-j)%2),Q(0))
        need(val == derived == convolution, 'coefficient identity failure')
        counts['coefficient_identities'] += 1
    g = f['geometry']
    keys(g,['radius_denominator','maximum_radius_numerator','directions'])
    denom=integer(g['radius_denominator'],1); maximum=integer(g['maximum_radius_numerator'],1)
    need(denom==4 and maximum==256, 'geometry coverage changed')
    need(type(g['directions']) is list and len(g['directions'])==12, 'directions coverage')
    for v in g['directions']:
        need(type(v) is list and len(v)==3 and all(type(t) is int for t in v), 'direction types')
        x,y,d=v;need(d>0 and x*x+y*y==d*d, 'not a unit rational direction')
    for j in range(maximum+1):
        r=Q(j,denom);h=height(r)
        need(h>=4,'height positivity')
        for dx,dy,d in g['directions']:
            x=r*Q(dx,d);y=r*Q(dy,d)
            m=nearest(x);hm=height(abs(Q(m)));q=ceiling(hm)
            n=max(q,nearest(abs(y))) * (-1 if y<0 else 1)
            need(abs(Q(n))>=hm,'chosen puncture membership')
            need(abs(Q(m)-x)<=Q(1,2),'rounding error')
            need(hm<=h+Q(1,8),'height monotonic/Lipschitz upper bound')
            need(abs(Q(m)-x)+abs(Q(n)-y)<=h+Q(13,8),'lattice upper bound')
            counts['lattice_upper_cases']+=1
        start=(r-h/2).numerator//(r-h/2).denominator-1
        end=ceiling(r+h/2)+1
        for m in range(start,end+1):
            hm=height(abs(Q(m)));q=ceiling(hm)
            need((Q(m)-r)**2+q*q>=(h/2)**2,'lattice lower bound')
            counts['lattice_lower_cases']+=1
        for s in [r+Q(1,2), r+Q(3,2), max(Q(0),r-Q(1,2))]:
            need(abs(height(s)-h)<=abs(s-r)/4,'height Lipschitz bound')
            counts['height_lipschitz_cases']+=1
    ps=f['parabola_identity_parameters']
    need(type(ps) is list and len(ps)==384,'parabola coverage')
    for rec in ps:
        keys(rec,['a2','r','t2']);a=integer(rec['a2'],1);r=integer(rec['r'],a);t=integer(rec['t2'])
        need((r+a-t)**2+4*a*t == (t-(r-a))**2+4*a*r,'parabola identity')
        counts['parabola_identities']+=1
    la=f['lacunary']
    keys(la,['coefficient_base','exponent_base','tail_numerator','tail_denominator','margin_numerator','margin_denominator','checked_index_maximum'])
    for v in la.values():integer(v,1)
    need(la['coefficient_base']==4 and la['exponent_base']==8 and la['checked_index_maximum']==128,'lacunary scope')
    tail=Q(la['tail_numerator'],la['tail_denominator']);margin=Q(la['margin_numerator'],la['margin_denominator'])
    need(tail == Q(1,64)/(1-Q(1,64)), 'tail geometric sum')
    need(margin == Q(1,2)-Q(1,3)-tail and margin>0,'Rouche margin')
    for j in range(1,129):
        need(8**j>=8*j,'tail exponent inequality')
        need(sum(4**i for i in range(1,j))<Q(4**j,3),'earlier term bound')
        counts['lacunary_inequalities']+=2
        t=1-Q(1,2*j)
        need(t**(j-1)>=Q(1,2) and j*(1-t*t)>=Q(3,4),'Bloch/Cauchy scalar estimates')
        counts['bernoulli_coefficient_bounds']+=1
    claims=decode((root/'CLAIMS.json').read_bytes())
    need(type(claims['mathematical_routes']) is int and claims['mathematical_routes']==5,'route count')
    need(claims['literal_limit_status']=='unresolved_in_this_investigation','status overclaim')
    need(claims['full_solution_claimed'] is False and claims['unconditional_new_counterexample_claimed'] is False,'proof overclaim')
    sources=decode((root/'SOURCES.json').read_bytes())
    need(sources['scholarly_sources'][1]['original_full_theorem_inspected'] is False,'source overclaim')
    return counts

def verify_sources(root, problems, research, pdf):
    src=decode((root/'SOURCES.json').read_bytes())
    out=[]
    for input_path, ent in zip([problems,research],src['dataset_pins']):
        if input_path is None:
            continue
        p=Path(input_path);need(p.is_file() and not p.is_symlink(),'source input invalid')
        b=p.read_bytes();need(len(b)==ent['bytes'] and digest(b)==ent['sha256'],'source dataset mismatch')
        # External datasets can contain finite JSON floats. Their exact whole-file
        # pins authenticate every byte; only the selected object is canonicalized.
        d=json.loads(b,object_pairs_hook=pairs,parse_constant=no_constant)
        if ent['name']=='problems.json':
            found=[v for v in d if type(v) is dict and type(v.get('id')) is int and v['id']==2305005]
            need(len(found)==1,'source selection not unique');rec=found[0]
        else:
            need(type(d) is dict and 'AMR-022-5005' in d,'review key missing');rec=d['AMR-022-5005']
        c=json.dumps(rec,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
        need(digest(c)==ent['record_sha256'],'selected record mismatch')
        out.append(ent['name'])
    if pdf is not None:
        p=Path(pdf);need(p.is_file() and not p.is_symlink(),'PDF input invalid');b=p.read_bytes();e=src['scholarly_sources'][0]
        need(b.startswith(b'%PDF') and len(b)==e['pdf_bytes'] and digest(b)==e['pdf_sha256'],'PDF mismatch');out.append('scholarly_pdf')
    return out

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,required=True)
    ap.add_argument('--manifest-sha256',required=True)
    ap.add_argument('--problems');ap.add_argument('--research');ap.add_argument('--pdf')
    a=ap.parse_args()
    n=validate_inventory(a.root,a.manifest_sha256)
    counts=verify_math(a.root)
    source_checks=verify_sources(a.root,a.problems,a.research,a.pdf)
    print(json.dumps({'integrity':'pass','payload_files':n,'exact_finite_checks':counts,'source_inputs_rehashed':source_checks,'literal_limit_status':'unresolved_in_this_investigation','analytic_existence_proof_computed':False},sort_keys=True,separators=(',',':')))

if __name__=='__main__':
    try:
        main()
    except (Invalid,ValueError,KeyError,TypeError,OSError,ZeroDivisionError) as e:
        print('REJECT: '+str(e),file=sys.stderr)
        sys.exit(1)
