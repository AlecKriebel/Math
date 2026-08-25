# D3+ simplex and single-minor audit

This directory independently audits the proposed product-of-simplexes sign
certificate for the 24 unresolved one-active cross-bridge directions.

## Result

The homogeneous coefficient-sign argument is mathematically sound as a
sufficient certificate.  It does not close the residue.  More strongly, exact
rational witnesses show that every individual candidate minor changes sign:

- 24 target directions;
- 144 Fourier-block 2x2 minors per direction;
- 3,456 minors with exact opposite-sign witness pairs;
- 6,912 exact nonzero rational evaluations.

Consequently, a universal strictly signed **single minor** cannot prove the
remaining cross-bridge exclusions.  This does not decide whether all minors
can vanish at one physical point.

A six-equation refinement using all six principal minors *within the
zero-character block* also fails.  For target 117 / record 39, an exact strict
rational point makes those six minors vanish.  At that point every complete
Fourier block has exact rank 4, so this construction refutes only that precise
zero-block shortcut—not pointwise cut recovery.

A different cyclic six-minor certificate succeeds for target 117.  It uses
three zero-block minors `F_C,F_G,F_T` and three carefully selected minors from
other character-sum blocks `H_C,H_G,H_T`.  Independent sparse replay proves

```text
y*z*F - x*H
= a*b*d^2*lambda*(1-lambda)*(y-x*z)*(x*y-z).
```

Vanishing the cyclic six forces each of three numbers in `(0,1)` to be a ratio
of the other two, which is impossible.  The zero-block counterexample has all
three cyclic `H` values nonzero and therefore does not challenge this proof.

Target 174 / record 60 has a separate exact cyclic certificate.  Nine minors
from its zero-character block reduce to three polynomials `F_s` and six
ordered polynomials `E_st`.  Exact elimination gives, for every cyclic
`{r,s,t}={C,G,T}`,

```text
b_r*C_r + b_s*b_t*F_r
= d_r^2*p*(1-p)*a_r*c_r*(b_t-b_s*b_r)*(b_t*b_r-b_s),
```

where `C_r` is itself an explicit polynomial combination of
`F_s,F_t,E_st,E_ts`.  The prefactor is strictly positive on D3+.  Joint
vanishing would force `b_r` to be a ratio of `b_s,b_t` for all three sectors,
again contradicting the maximal negative logarithm.  This proves pointwise
rank greater than four for target 174 throughout the strict principal domain.

Target 127 / record 43 transports that nine-minor eliminant exactly.  After
positive-monomial removal, each of its nine zero-block minors is exactly
divisible by the additional strict factor `1-lambda_0`, with zero remainder.
The quotients use `p=lambda_1`, edge roles `a=1,b=4,c=8,d=9`, and the ordered
cross minor `(s,t)` maps to `E_ts`.  The same cyclic factorization and maximal
negative-log contradiction therefore prove pointwise rank greater than four
for target 127 as well.

## Replay

From the project root, run:

```text
.venv/bin/python cut_recovery/strong_crossbridge/audit_simplex/verify_single_minor_sign_changes.py --mutations
```

The verifier rebuilds the graph-derived K3P maps, checks the domain inequalities
exactly, recomputes every stored value, and rejects eight adversarial mutations.

The six-equation construction has a separate replay:

```text
.venv/bin/python cut_recovery/strong_crossbridge/audit_simplex/verify_record39_six_diagonal_counterexample.py --mutations
```

The successful cyclic certificate replay is:

```text
.venv/bin/python cut_recovery/strong_crossbridge/audit_simplex/verify_record39_cyclic_certificate.py
```

The target-174 / record-60 replay is:

```text
.venv/bin/python cut_recovery/strong_crossbridge/audit_simplex/verify_record60_cyclic_certificate.py
```

Its human-readable derivation is `RECORD60_CYCLIC_CERTIFICATE.md`, and its
machine audit is `RECORD60_CYCLIC_CERTIFICATE_AUDIT.json`.

The target-127 / record-43 transport replay is:

```text
.venv/bin/python cut_recovery/strong_crossbridge/audit_simplex/verify_record43_cyclic_transport.py
```

Its derivation and audit are `RECORD43_CYCLIC_CERTIFICATE.md` and
`RECORD43_CYCLIC_TRANSPORT_AUDIT.json`.
