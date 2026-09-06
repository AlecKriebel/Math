#!/usr/bin/env python3
"""Root reviewer checks preserved bytes and independently inverts Bernstein bases.

The interval reconstruction checks the separate referee's cubic/crossing sign
evidence. It is an audit of that mechanism, not another full PDE proof.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import sympy as S

HERE = Path(__file__).resolve().parent


def require(value, message):
    if not value:
        raise RuntimeError(message)


inventory = json.loads((HERE / 'SOURCE_INVENTORY.json').read_text())
snapshot = HERE / 'source_snapshot'
for row in inventory['files']:
    data = (snapshot / row['path']).read_bytes()
    require(len(data) == row['bytes'], row['path'] + ': size changed')
    require(hashlib.sha256(data).hexdigest() == row['sha256'],
            row['path'] + ': hash changed')
require({str(p.relative_to(snapshot)) for p in snapshot.rglob('*') if p.is_file()}
        == {row['path'] for row in inventory['files']}, 'Snapshot file set changed')

pde = json.loads((HERE / 'pde/INDEPENDENT_RESULTS.json').read_text())
near = next(c for c in pde['checks'] if c['name'].startswith('near_threshold'))
epsilon = S.Symbol('epsilon')
results = []
for field in ('cubic', 'eta'):
    expression = S.sympify(near[field], locals={'epsilon': epsilon})
    numerator, denominator = S.fraction(S.cancel(expression))
    if denominator.subs(epsilon, S.Rational(1, 2000)) < 0:
        numerator, denominator = -numerator, -denominator
    for part_name, part in (('numerator', numerator), ('denominator', denominator)):
        polynomial = S.Poly(part, epsilon)
        power = min(m[0] for m, _ in polynomial.terms())
        reduced = S.Poly(S.cancel(part / epsilon**power), epsilon)
        degree = reduced.degree()
        # Solve for coefficients from the basis polynomials themselves,
        # independently of the other referee's closed conversion formula.
        basis = [S.Poly(S.binomial(degree, k) * (1000*epsilon)**k
                        * (1-1000*epsilon)**(degree-k), epsilon)
                 for k in range(degree+1)]
        matrix = S.Matrix([[basis[k].nth(j) for k in range(degree+1)]
                           for j in range(degree+1)])
        rhs = S.Matrix([reduced.nth(j) for j in range(degree+1)])
        coefficients = matrix.inv()*rhs
        require(all(c > 0 for c in coefficients), field + ': nonpositive coefficient')
        recovered = sum(c*b.as_expr() for c, b in zip(coefficients, basis))
        require(S.expand(recovered-reduced.as_expr()) == 0,
                field + ': reconstruction failed')
        results.append({'field': field, 'part': part_name,
                        'epsilon_power': power, 'degree': degree,
                        'positive_bernstein_coefficients': len(coefficients),
                        'minimum_coefficient': str(min(coefficients))})

pdfs = json.loads((HERE / 'documents/PDF_INVENTORY.json').read_text())
require(sum(p['pages'] for p in pdfs) == 96, 'Page count')
notation = json.loads((HERE / 'documents/NOTATION_WITNESS.json').read_text())
require(notation['affected_rows'] == len(notation['rows']) == 50, 'Notation count')
assets = json.loads((HERE / 'software/RELEASE_ASSET_INTEGRITY.json').read_text())
require(len(assets) == 9 and all(a['matches_snapshot'] and a['matches_github_digest']
                               for a in assets), 'Release asset evidence')

out = {'status': 'PASS', 'completed_utc': datetime.now(timezone.utc).isoformat(),
       'source_files_unchanged': len(inventory['files']),
       'total_source_bytes': sum(r['bytes'] for r in inventory['files']),
       'bernstein_basis_inversions': results, 'pdf_pages': 96,
       'ambiguous_notation_rows': 50, 'matching_release_assets': 9}
(HERE / 'ROOT_EVIDENCE_CHECK.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out, indent=2))
