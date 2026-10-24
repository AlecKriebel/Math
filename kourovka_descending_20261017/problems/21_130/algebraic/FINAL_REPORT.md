# Algebraic / probabilistic family report

2026-10-24. **Full problem unresolved.** Best-guess completion toward the unrestricted discovery goal: **22%**. No novelty assertion, external outreach, Git action, upload, or publication is made by this family.

## Strongest independently checked result

For every odd prime `p`, every subset `A` of cardinality `3≤|A|≤11` of every finite abelian `p`-group admits a cyclic enumeration with all neighboring sums distinct. At cardinality eleven, the same result holds for abelian `2`-groups as well.

This follows from two checkable ingredients:

1. Exact sparse-polynomial coefficient certificates for `Q_n=V(vertices) prod_(disjoint cycle edges)(difference of neighboring sums)`, truncated modulo `(x_1^n,...,x_n^n)`. Cardinalities `3,...,9` use complete expansions plus independently checked coefficient witnesses. Cardinalities ten and eleven use signed-permutation formulas, with independent actual-polynomial grid-sum reproduction. Their witness gcds are respectively `2` and `1`.
2. The integral analytic transfer lemma of `FORMAL_GROUP_TRANSFER.md`, independently adversarially audited, and the original Lubin–Tate Theorem 2(b). This realizes arbitrary-rank, arbitrary-exponent finite abelian `p`-groups as torsion of an integral one-dimensional formal group and transfers the characteristic-`p` coefficient nonvanishing to it.

Primary artifacts:

- `FORMAL_GROUP_TRANSFER.md`: complete analytic transfer proof and exact primary theorem citation; frozen while root's additional fresh audit proceeds.
- `COEFFICIENT_EXTENSION.md`: full n10–11 formula derivation and witnesses.
- `polynomial/SLACK_RESULTS.md`, `polynomial/FINAL_AUDIT.md`: n3–9 proofs, independently reproduced n10–11 values, and audit scope.
- `polynomial/fixed_zero_audit.py`: independently recomputes the actual-polynomial n10–11 witnesses.
- `verify_extension_consistency.py`: all 151 new-formula coefficient values n3–9 agree with separate complete expansions.

## Other proved partial statements

`PARTIAL_RESULTS.md` contains:

- Exact first-moment sufficient condition `4T(A)<(n−1)(n−2)`, where `T=sum_s binom(m_s,2)` counts disjoint equal-sum edge pairs.
- A standard random-injection local-lemma sufficient condition `32e(max_s m_s−1)<n−2`, with complete event count and primary theorem citation.
- An elementary determinant/Hadamard rectification theorem for all finite abelian groups satisfying `p_min(|G|)>2^(n−1)`.

These are independently audited restricted cases; none supplies the full conclusion.

## Mechanisms and exact gaps

| Family | Evidence | Status / exact gap |
|---|---|---|
| Full Vandermonde / central CN | Exact coefficients; dihedral cancellation proofs | Blocked universally: every even n central coefficient vanishes, and odd n has obstructing odd characteristic divisors |
| Exterior color trace | Rotation/reversal cancellation proof | Blocked for large congruence classes; avoiding cancellations would require a new invariant |
| Reduced CN polynomial | Explicit nonzero certificates through n11 | Successful bounded-cardinality primary case; no all-n coefficient-content proof |
| Formal-group transfer | Complete convergent remainder proof; original LT theorem checked; independent audits | Successful transfer to all p-groups; does not embed mixed-prime torsion in one maximal ideal |
| Random first moment / LLL | Exact proofs and finite formula checks | Blocked in unrestricted high-multiplicity regime |
| Rational rectification | Cramer's rule, norm2 rows, Hadamard bound | Successful large-prime regime; arbitrary small-prime torsion remains |
| Single-primary Freiman model | Explicit seven-point C15 (root) and nine-point C3×C5 annihilator constructions | Blocked by exact obstruction, not merely lack of a proof |

`MIXED_PRIME_MODEL_OBSTRUCTION.md` gives an independently derived nine-point subset of `C_3×C_5` and the root family’s sharper seven-point subset of `C_15` for which every sum-equality-preserving map to any abelian `p`-group identifies two vertices. The nine-point construction proves integral annihilators `3f(a)=0` and `5f(b)=0`; the seven-point construction forces `15f(1)=0` and displays the collapsing vertex pair in every primary target. Both subsets have explicitly displayed rainbow cycles, so these constructions block only that reduction and are not negative answers to the problem.

No all-n or mixed-prime step is promoted by analogy, by a central coefficient, or by the success of the primary cases. The exact remaining target is arbitrary cardinality in arbitrary finite abelian groups of odd order.
