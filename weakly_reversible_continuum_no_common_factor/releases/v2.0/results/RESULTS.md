# Frozen verification results

All eight executable gates passed under CPython with `sympy==1.14.0` and
`mpmath==1.3.0`.  The exact result frozen by the independent v2 audit is
`../audit_v2/audit_results.json`.

| Gate | Frozen result |
|---|---|
| Release-package integrity | Final PDF/source byte anchors, source/data rate tables, family formulas, frozen JSON, and no-false-DOI state agree |
| Original construction | 10 complexes; 20 directed reactions; one connected reversible linkage class; stoichiometric rank 3; gcd 1; radical dimension-one steady ideal equal geometrically to the conic plus 15 reduced points |
| Frozen-v1 clean room | Exact checks 1--17 passed; structural proof audits 18--20 recorded in `../cleanroom/PROOF_AUDIT.md` |
| Four-parameter family | Canonical matrix 21 by 20; rank/nullity 16/4; positive orthant coordinates exact; original affine and homogenized gcds 1 |
| Clean rates and stability | Primitive clean maximum 10296 and sum 52464; same radical conic-plus-15-points ideal; two exact transverse stability transitions |
| Minimality arithmetic | The only numerical case with at most four complexes reduces to `(m,l,s,delta)=(4,1,2,1)`, which the accompanying proof excludes |
| Independent v2 audit | Both gcds, both radicals, both integral optima, the family, and Sturm counts passed using alternative algorithms |
| Integrated manuscript gate | Rate tables, family coordinates, both gcds, degree-15 modular irreducibility, family, optimality, radical, and Sturm assertions passed |

No floating-point value is used to establish any entry in this table.
