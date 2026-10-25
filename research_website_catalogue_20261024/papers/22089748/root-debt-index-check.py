"""Exact check of published phase-note equation35; no submitted code imported."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import datetime, hashlib, json

HERE=Path(__file__).resolve().parent
note=HERE/'sources/published-source/complete_graph_extremality_db_source_and_certificates/universal_simultaneous_amplification/phase5_exact_threshold/r2_determinant/TRUE_INVERSE_RANK_SYMMETRIC_PHASE_CONTRACTION.md'
assert hashlib.sha256(note.read_bytes()).hexdigest() == '0f1e270ecf696f350b8e1917c80238ca3a7f161415bebdcdf594355acaf0ce8a'
results=[]
for n in (3,4,5,24,40,288):
    omega=lambda j:F(comb(n-2,j-1),2**(n-1)*(n+1))
    q=lambda k:F(comb(n-3,k-2),2**(n-2)*(n+1))
    y=lambda k:F(2*(k+1),3*k*(k-1))
    coefficient=lambda j:F(4*(j+2),3*(j+1)*(n-2))
    actual=sum((y(k)*q(k) for k in range(2,n)),F(0))
    printed=sum((coefficient(j)*omega(j) for j in range(1,n-1)),F(0))
    shifted=sum((coefficient(j)*omega(j+1) for j in range(1,n-1)),F(0))
    assert actual==shifted
    if n==40:assert actual-printed==F(549755813107,501063941451939840)
    results.append({'N':n,'Yq':str(actual),'printed_sum':str(printed),'difference':str(actual-printed)})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'status':'PUBLISHED_IDENTITY_FALSE', 'checks':results,
     'main_theorem_disproved':False,'A31_disproved':False,
     'scope':'The phase-note equality and its stated debt-bound deduction fail; the already-published forward-subset proof independently supports the curvature sign. No repair is supplied.'}
(HERE/'root-debt-index-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'N40_difference':results[4]['difference'],'main_theorem_disproved':False}))
