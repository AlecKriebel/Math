import sympy as s, json
from pathlib import Path
x, T, G = s.symbols('x T G')
cat = T - x * (1 + T) ** 2
relation = (1 - x) * (1 - T * T) * G - 1
poly = (4 * x ** 3 - 9 * x * x + 6 * x - 1) * G * G + (4 * x * x - 5 * x + 1) * G + x * x
res = s.factor(s.resultant(cat, relation, T))
if not s.expand(res - poly) == 0:
    raise RuntimeError('check_4231.py:8: s.expand(res-poly)==0')
subnumer = s.together(poly.subs(G, 1 / ((1 - x) * (1 - T * T)))).as_numer_denom()[0]
if not s.rem(subnumer, cat, T) == 0:
    raise RuntimeError('check_4231.py:11: s.rem(subnumer,cat,T)==0')
D = s.factor(s.discriminant(poly, G))
if not s.expand(D - (1 - x) ** 2 * (1 - 2 * x) ** 2 * (1 - 4 * x)) == 0:
    raise RuntimeError('check_4231.py:12: s.expand(D-(1-x)**2*(1-2*x)**2*(1-4*x))==0')
c = (1 - 2 * x - s.sqrt(1 - 4 * x)) / (2 * x)
series = s.series(1 / ((1 - x) * (1 - c * c)), x, 0, 13).removeO().expand()
coeffs = [int(series.coeff(x, n)) for n in range(13)]
rows = json.loads((Path(__file__).parent / 'all_length4_results.json').read_text())
row = next((r for r in rows if r['basis'] == ['4231']))
if not coeffs == row['coefficients'][:13]:
    raise RuntimeError("check_4231.py:18: coeffs==row['coefficients'][:13]")
out = {'resultant': str(res), 'identity_mod_Catalan_polynomial': True, 'discriminant': str(D), 'formal_branch': 'T(0)=0, G(0)=1', 'coefficients': coeffs, 'comparison_matches': True}
(Path(__file__).parent / 'exact_4231_checks.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
