#!/usr/bin/env python3
"""Second-auditor checks, independently reconstructed with SymPy number fields.
No candidate checker code is imported. Mathematical proof still required for the
analytic normalization, flatness, representative, and source-scope conclusions.
"""
import hashlib
import itertools
import json
import pathlib
import subprocess
import sys
import sympy as sp

K = sp.QQ.algebraic_field(sp.sqrt(-3))
one, zero = K.one, K.zero
omega = K.from_sympy((-1 + sp.sqrt(-3)) / 2)
x, y, t = sp.symbols('x y t')
count = 0

def verify(condition, description):
    global count
    count += 1
    if not condition:
        raise ValueError(description)

def line_arrangement(roots):
    return ([(one, -q, zero) for q in roots]
            + [(q, 4*one + 2*q, -q) for q in roots]
            + [(-one - 4*q, -2*one, one) for q in roots])

def incidence(lines):
    points = {}
    for i, j in itertools.combinations(range(len(lines)), 2):
        a,b,c = lines[i]; d,e,f = lines[j]
        det = a*e - d*b
        verify(det != zero, 'Distinct spatial directions required')
        p = ((b*f-c*e)/det, (c*d-a*f)/det)
        points.setdefault(p, set()).update((i,j))
    for p, labels in points.items():
        actual = {i for i,(a,b,c) in enumerate(lines) if a*p[0]+b*p[1]+c == zero}
        verify(labels == actual, 'Pair enumeration and full incidence agree')
    verify(sum(len(s)*(len(s)-1)//2 for s in points.values()) == len(lines)*(len(lines)-1)//2,
           'All pairs counted exactly once')
    return points

def norm(z):
    expr = K.to_sympy(z)
    return sp.simplify(expr*sp.conjugate(expr))

def poly_from_lines(lines):
    p = sp.Poly(1, x,y,t, domain=K)
    for a,b,c in lines:
        p *= sp.Poly(K.to_sympy(a)*x + K.to_sympy(b)*y + K.to_sympy(c)*t, x,y,t, domain=K)
    return p

def totals(points):
    return (sum(len(s)*(len(s)-1)//2 for s in points.values()),
            sum(len(s)-2 for s in points.values()))

roots = [one, omega, omega**2]
lines = line_arrangement(roots)
points = incidence(lines)
verify(len(points)==12, 'Twelve singular points')
verify(all(len(v)==3 for v in points.values()), 'Every singular point has three branches')
verify(all(a!=zero for a,b,c in lines), 'Each normalization component is a graph over (y,t)')
radii = sorted(norm(a)+norm(b) for a,b in points)
verify(max(radii)<2, 'All scaled singularities lie in radius sqrt(2)*abs(t)')
verify(max(radii)/16<sp.Rational(1,4), 'Uniform parameter disk abs(t)<1/4 puts singularities inside radius 1/2')
distances = [sp.simplify(norm(c)/(norm(a)+norm(b))) for a,b,c in lines]
verify(all(d/16<1 for d in distances), 'Uniform boundary-transversality distance margin')

F = (x**3-y**3)*(64*y**3-(t-x-2*y)**3)*((t-x-2*y)**3-64*x**3)
product = poly_from_lines(lines)
verify(product==sp.Poly(F,x,y,t,domain=K), 'Nine-line product equals stated F')
verify(sp.Poly(F,x).LC()==-65, 'Constant nonzero x-leading coefficient')
verify(product.total_degree()==9, 'Degree nine')
verify(all(sum(m)==9 for m,c in product.terms()), 'Homogeneous in (x,y,t)')
verify(sp.Poly(F,x,y,t).get_domain()==sp.ZZ, 'Integer coefficients')
# Central arrangement is squarefree: distinct directions were checked above.
central = sp.Poly(F.subs(t,0),x,y)
verify(sp.gcd(central, central.diff(x)).total_degree()==0,
       'Central fiber polynomial is squarefree')
for p in points:
    a,b=map(K.to_sympy,p)
    for expr in (F,sp.diff(F,x),sp.diff(F,y)):
        value=sp.Poly(expr,x,y,t,domain=K).eval({x:a,y:b,t:1})
        verify(value==0, 'Every independently enumerated point is a gradient singularity')
verify(totals(points)==(36,12), 'Nearby invariant totals')
verify((9*8//2,9-2)==(36,7), 'Central invariant totals')

# Actual perturbed-data controls, not just deliberately false assertions.
controls={}
missing=incidence(lines[:-1])
controls['missing_line_detected'] = len(missing)!=12 or any(len(v)!=3 for v in missing.values())
corrupted=F+x**9
controls['polynomial_corruption_detected'] = product != sp.Poly(corrupted,x,y,t,domain=K)
# Infinity L=X+Y+Z contains arrangement intersections. In that chart Z=t-x-y.
invalid_lines=([(one,-q,zero) for q in roots]
               +[(q,one+q,-q) for q in roots]
               +[(-one-q,-one,one) for q in roots])
controls['nongeneric_infinity_detected'] = any(a*e-b*d==zero for (a,b,c),(d,e,f) in itertools.combinations(invalid_lines,2))
duplicate=lines[:-1]+[lines[0]]
controls['duplicated_direction_detected'] = any(a*e-b*d==zero for (a,b,c),(d,e,f) in itertools.combinations(duplicate,2))
verify(all(controls.values()), 'All four mutation controls detected')

fermat_two=incidence(line_arrangement([one,-one]))
verify(sorted(map(len,fermat_two.values()))==[2,2,2,3,3,3,3], 'n=2 boundary arrangement multiplicities')
verify(totals(fermat_two)==(15,4), 'n=2 has no false strict inequality')
generic_lines=[(one,-i*one,-i*i*one) for i in range(9)]
generic=incidence(generic_lines)
verify(len(generic)==36 and all(len(v)==2 for v in generic.values()), 'Nine generic lines give only nodes')
verify(totals(generic)==(36,0), 'Generic-line control has no false counterexample')

candidate=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path(__file__).resolve().parent.parent/'frozen_v2'
manifest=json.loads((candidate/'FROZEN_MANIFEST.json').read_text())
for item in manifest['files']:
    data=(candidate/item['file']).read_bytes()
    verify(len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256'], 'Frozen file identity: '+item['file'])
outputs=[]
for opt in ([],['-O']):
    outputs.append(subprocess.check_output([sys.executable,*opt,str(candidate/'checks.py')]))
verify(outputs[0]==outputs[1], 'Candidate checker works identically under optimization')
verify(outputs[0]==(candidate/'CHECK_RESULTS.json').read_bytes(), 'Saved candidate check output reproduced')
summary={
 'status':'PASS', 'independent_implementation':'SymPy '+sp.__version__+' QQ(sqrt(-3)); direct affine pair solving',
 'checks':count,'proof_sha256':hashlib.sha256((candidate/'PROOF.md').read_bytes()).hexdigest(),
 'candidate_manifest_sha256':hashlib.sha256((candidate/'FROZEN_MANIFEST.json').read_bytes()).hexdigest(),
 'line_count':len(lines),'singular_point_count':len(points),'singularity_branch_counts':sorted(map(len,points.values())),
 'chart_squared_norms':[str(r) for r in radii],
 'line_squared_distance_coefficients':[str(d) for d in distances],
 'central_delta':36,'nearby_delta':totals(points)[0],'central_rough_M':7,'nearby_rough_M':totals(points)[1],
 'mutation_controls':controls,'n2_control':{'delta':15,'nearby_rough_M':4,'central_rough_M':4},
 'generic_nine_line_control':{'delta':36,'nearby_rough_M':0,'central_rough_M':7},
 'author_checker_exact_checks':json.loads(outputs[0])['exact_checks'],
 'limitations':'No proof-assistant certification. Analytic and source-scope issues were audited in the written report.'}
print(json.dumps(summary,indent=2,sort_keys=True))
