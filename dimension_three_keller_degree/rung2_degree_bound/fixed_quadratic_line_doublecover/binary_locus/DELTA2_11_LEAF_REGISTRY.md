# Exact-\(\delta=2,\{1,1\}\) incidence-leaf registry

**Updated (UTC):** 2026-07-25T19:15:08Z.

This registry is grouped by geometric incidence mechanism.  “Closed”
below means only that a provisional exact proof and dual-CAS certificate
exist; hostile mathematical audit is still required.  A routed mutation
is not silently included in an exact-\(\delta=2\) theorem.

## Closed provisionally

| Fixed divisor | Exact-\(\delta=2\) leaf | Status |
|---|---|---|
| \(h=p^2\) | \(R=p(Ap^2+Bpq+Cq^2),\ BC\ne0\) | Closed through \(E_6/E_5\); `DELTA2_11_P2_SIMPLE_FIXED_EXCLUSION.md` |
| \(h=p^2\) | \(R=Ap^3+Cpq^2+Dq^3,\ D\ne0\) | Closed through \(E_6/E_5/E_4\); `DELTA2_11_P2_BRANCH_CONTACT_EXCLUSION.md` |
| \(h=pq\) | \(R=p^2(Ap+Bq),\ AB\ne0\), up to swap | Closed at \(E_6\) by the all-binary exit; `DELTA2_11_PQ_DOUBLE_EXCLUSION.md` |
| \(h=pq\) | \(R=pq(Ap+Bq),\ AB\ne0\) | Closed at \(E_6\) by a rank-four/Veronese obstruction; `DELTA2_11_PQ_TWO_SIMPLE_EXCLUSION.md` |
| \(h=p(p+q)\) | \(R=p^2(Ap+Bq)\), on its exact open | Closed at \(E_6\) by the all-binary exit; `DELTA2_11_PELL_DOUBLE_P_EXCLUSION.md` |
| \(h=p(p+q)\) | \(R=(p+q)^2(Ap+Bq)\), on its exact open | Closed at \(E_6\) by a two-minor contact cover and the all-binary exit; `DELTA2_11_PELL_DOUBLE_L_EXCLUSION.md` |
| \(h=p(p+q)\) | \(R=p(p+q)(Ap+Bq)\), on its exact open | Closed at \(E_6\) by a rank-four/Veronese obstruction; `DELTA2_11_PELL_TWO_FIXED_EXCLUSION.md` |
| \(h=p(p+q)\) | \(R=p(4Tp^2+3Tpq+Cq^2)\), on its exact open | Closed at \(E_6\) by a three-chart contact atlas; `DELTA2_11_PELL_P_CONTACT_EXCLUSION.md` |
| \(h=p(p+q)\) | \(R=(p+q)(-4Bp^2+Bpq+Cq^2)\), on its exact open | Closed at \(E_6\) by an independent three-chart contact atlas; `DELTA2_11_PELL_L_CONTACT_EXCLUSION.md` |
| squarefree interior \(h=LM\) | \(L^2\mid R\), with no additional incidence | Closed at \(E_6\) by a projective resultant cover and fresh \(R=L^3\) pivot; `DELTA2_11_INTERIOR_DOUBLE_FIXED_EXCLUSION.md` |
| squarefree interior \(h=LM\) | \(LM\mid R\), with no additional incidence | Closed at \(E_6\) by a rank-four/Veronese obstruction; `DELTA2_11_INTERIOR_TWO_FIXED_EXCLUSION.md` |
| squarefree interior \(h=LM\) | One fixed-root incidence plus one ramification contact | Closed through \(E_6/E_5\) by a two-chart contact atlas, a primitive quartic-field obstruction, and four fresh pivots; `DELTA2_11_INTERIOR_FIXED_CONTACT_EXCLUSION.md` |
| squarefree interior \(h=LM\) | Two ramification contacts | Closed through \(E_6/E_5/E_4\) and the constant term by a generic/alternate contact atlas; the sole full-lower lift forces a singular linear part; `DELTA2_11_INTERIOR_TWO_CONTACTS_EXCLUSION.md` |
| doubled nonbranch \(h=(p+q)^2\) | One simple fixed-root incidence | Closed at \(E_6\) by generic and fresh \(\Delta=0\) full-rank contact charts plus the all-binary exit; `DELTA2_11_DOUBLED_NONBRANCH_SIMPLE_FIXED_EXCLUSION.md` |

The mutations \(B=0\) or \(C=0\) in the first row, and \(D=0\) in the
second row, have gcd degree at least three and are routed to the future
\(\delta\ge3\) analysis.  The internal pivot divisors
\(4AC-B^2=0\) and \(27AD^2+4C^3=0\) were recomputed and remain inside
the closed exact-\(\delta=2\) leaves.

## Open leaves

### Doubled nonbranch fixed divisor \(h=(p+q)^2\)

1. Baseline doubled-root contribution plus one ramification contact:
    \[
    R=ap^3+bp^2q+\frac32d\,pq^2+dq^3,
    \]
    on
    \((3a-2b)(2a-2b+d)(6a-5b+3d)\ne0\).
    The final factor removes the \(\{2,0\}\) sublocus.

## Separate, not counted as an open \(\{1,1\}\) leaf

- The three exact-\(\delta=2,\{2,0\}\) loci are provisionally excluded
  by `DELTA2_K20_UMBRELLA.md`.
- Every \(\delta\ge3\) mutation remains open in its own future stratum.
- The constant-dependent power fibre \(h=p^2,R=p^3\) remains separate.

The active next experiment is the final open leaf, the baseline
doubled-root contribution plus one ramification contact.

This registry was prepared with AI assistance.  It is not peer
reviewed.
