"""Independent literal Theorem 3.1 rate-domain falsification; no source repair."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
import sympy as s

root=Path(__file__).resolve().parent
old=root.parent
x,y,z=s.symbols('x y z')
eta=s.sqrt(2)/10
complexes=[(0,0,0),(0,0,1),(0,0,3),(0,1,1),(0,3,0),(1,0,1),(1,1,0),(1,1,1),(2,1,0),(3,0,0)]
pairs=[(0,1),(0,4),(0,6),(1,7),(2,4),(2,7),(2,9),(3,4),(5,9),(8,9)]
arcs=[p for edge in pairs for p in (edge,edge[::-1])]
clean=list(map(s.Integer,[1160,10296,976,23,560,5977,1800,25,1629,1237,1,9152,653,1214,5368,1,5368,70,6039,915]))
modified=clean.copy()
increments={(2,4):eta,(2,7):-3*eta,(2,9):eta}
for edge,change in increments.items(): modified[arcs.index(edge)]+=change
units=[s.Matrix([complexes[v][j]-complexes[u][j] for j in range(3)])*
       x**complexes[u][0]*y**complexes[u][1]*z**complexes[u][2] for u,v in arcs]
F0=sum((k*u for k,u in zip(clean,units)),s.zeros(3,1)).applyfunc(s.expand)
F1=sum((k*u for k,u in zip(modified,units)),s.zeros(3,1)).applyfunc(s.expand)
delta=(F1-F0).applyfunc(s.simplify)
assert delta==s.zeros(3,1)
assert all(s.Poly(f,x,y,z,domain=s.QQ) for f in F1)
L=z-x-y+1
Q=7*x*x-2*x*y-16*x+7*y*y-16*y+16
G=s.groebner([L,Q],z,y,x,domain=s.QQ)
reductions=[G.reduce(f)[1] for f in F1]
assert reductions==[0,0,0]
assert s.simplify(eta**2)==s.Rational(1,50)
# 0<sqrt(2)<2 gives 0<eta<1/5 and k27>2/5; all other changes increase a positive rate.
assert eta.is_positive and (s.Rational(1,5)-eta).is_positive
assert all(k.is_positive for k in modified)
assert modified[12]==653+eta and modified[12].is_rational is False
frozen=json.loads((root/'frozen-inputs.json').read_text())
for name,expected in frozen['existing_review_files'].items():
    assert hashlib.sha256((old/name).read_bytes()).hexdigest()==expected
out={
 'checked_utc':datetime.now(timezone.utc).isoformat(),
 'status':'LITERAL_COUNTEREXAMPLE_CONFIRMED',
 'eta':str(eta),'eta_squared':str(eta**2),'eta_irrational':eta.is_rational is False,
 'changed_rates':{str(e):str(modified[arcs.index(e)]) for e in increments},
 'reaction_vectors':{str(e):list(map(int,s.Matrix(complexes[e[1]])-s.Matrix(complexes[e[0]]))) for e in increments},
 'delta_field':list(map(str,delta)),
 'unchanged_rational_field':list(map(str,F1)),
 'rational_ideal_normal_forms':list(map(str,reductions)),
 'all_twenty_rates_positive':True,
 'smallest_changed_rate_lower_bound':'k27 = 1-3sqrt(2)/10 > 2/5',
 'forced_free_coordinate':'a = k29 = 653+sqrt(2)/10 is irrational',
 'no_rational_parameter_tuple_can_reproduce_modified_rates':True,
 'frozen_review_files_unchanged':True,
 'scope':'Counterexample to rational-parameter necessity under the published unrestricted positive-rate model; not a counterexample to the integer examples or the rational-input classification.'
}
(root/'result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','changed_rates','delta_field','rational_ideal_normal_forms','all_twenty_rates_positive','forced_free_coordinate','frozen_review_files_unchanged']}))
