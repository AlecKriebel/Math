"""Adversarial domain tests of actual packaged callback AST bodies."""
import ast, json, hashlib, datetime
from pathlib import Path
from flint import arb, acb

out = Path(__file__).resolve().parent
p = out / 'extracted/target_b/independent_validated_integrals.py'
s = p.read_text()
tree = ast.parse(s)
scope = {}
exec(compile(ast.parse(s[:s.index('start=time.monotonic()')]), str(p), 'exec'), scope)
for name in ('table_density', 'bern_factor', 'quotient_factor'):
    node = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == name)
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(p), 'exec'), scope)
scope['tab'] = []
for i in range(2):
    pairs = {r[0]: (arb(r[1+2*i])/10**10, arb(r[2+2*i])/10**10)
             for r in scope['data']['tables']['coefficients']['rows']}
    pairs[0] = (arb(1), arb(44)/100) if i == 0 else (arb(0), -arb(368)/1000)
    scope['tab'].append(pairs)
scope.update(C=[-arb(13)/1000, arb(17)/1000], kindout=1, kindin=0,
             m=1, n=1, j=1, i=1, index=0, derivative=1,
             y=-arb(1)/2, nu=2, k=28)
boxes = {
    'exact_singularity': acb(0, -arb(2)/5),
    'containing_ball': acb(arb(0, '.01'), arb(-arb(2)/5, '.01')),
    'regular_ball': acb(arb('.5', '.001'), arb(0, '.001')),
}
checks = []
for node in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == 'callback']:
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(p), 'exec'), scope)
    for label, t in boxes.items():
        for analytic in (False, True):
            value = scope['callback'](t, analytic)
            finite = value.is_finite()
            assert finite == (label == 'regular_ball'), (node.lineno, label, analytic, str(value))
            checks.append({'callback_line': node.lineno, 'ball': label,
                           'analytic': analytic, 'is_finite': finite})
record = {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'script_sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
    'method': 'Execute actual AST callback bodies on singular, containing, and regular complex balls.',
    'status': 'PASS', 'tests': checks, 'callback_definitions': len(checks)//6,
    'coverage_limit': 'Representative parameters and balls; global holomorphy follows rational/entire syntax off -2i/5.',
}
(out/'CALLBACK_ADVERSARY.json').write_text(json.dumps(record, indent=2)+'\n')
print(json.dumps({k: v for k, v in record.items() if k != 'tests'}, indent=2))
