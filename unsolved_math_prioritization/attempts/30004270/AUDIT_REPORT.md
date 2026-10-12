# Independent audit: arbitrary-degree Hasse-semigroup obstruction

**Verdict: accept the explicit normalized calculation; require a scope correction before treating it as a historical refutation.**

Candidate audited: SHA-256 `fc4036224e6291c60ba39cb3c54b7dad8982d518f2136561f496e15d8f5ad5f3`, 3,846 bytes. The candidate was not edited. The accompanying `PROOF.md` is a standalone, qualified replacement exposition.

## Checks completed

- **Primary-source formula:** Visually checked the complete 2019 contribution, printed pp. 2905–2907. Its root equation is `eta^b=f_p/f_q` in the function field of the affine cone. Its one-chain LS formula contains the unweighted integral-total condition.
- **Geometric hypotheses:** Independently checked the poset, cover relation, projective normality, set-theoretic zero loci, nonvanishing, and positive homogeneous degrees. The example meets all these hypotheses.
- **Coordinate ring:** The counterexample uses the standard embedding and the full ring `C[x,y]`. In particular `x` is an eligible nonzero homogeneous input.
- **Root condition and bonds:** Verified `eta=x/y`, upper bond two, and modern terminal bond two.
- **Valuation:** Recomputed the defining recursion, obtaining `(i/2,(d-i)/2)` for a degree-`d` homogeneous polynomial with smallest `x` exponent `i`. This proves the complete semigroup, not only one test value.
- **Contradiction:** `(1/2,0)` belongs to the normalized value semigroup and fails the unweighted integral-total requirement.
- **Weighted interpretation:** Proved the exact weighted description for this example and distinguished it from a general necessary degree identity. No sufficiency claim for general stratifications is made.
- **Degree-one controls:** Checked both linear extremal functions in `C[x,y]` and quadratic extremal sections in the regraded quadratic-Veronese ring. The respective LS formulas hold. In the latter ring the putative witness `x` does not exist.
- **Modern scope:** Checked Definition 2.9 in arXiv:2206.13171v2, which explicitly requires degree one for LS-type.

## Material qualification

The candidate imports `V_C(f_s)=e_s` from the later fully specified construction. That is a valid convention and yields a genuine counterexample to the arbitrary-degree application of the LS formula. However, the 2019 report only announces a modified valuation using asymptotic ideas. It supplies no construction or explicit extremal-function normalization for arbitrary degrees. The audit found no explicit source statement identifying every arbitrary-degree convention in that report with the later construction.

For comparison, the cited predecessor by Fang–Littelmann, arXiv:1709.09734v1, Section 6, pp. 10–11, uses an injection into `R_1` in its different lattice-governed setup. It does not supply the missing arbitrary-degree identification. This predecessor was inspected only for that limited purpose.

Accordingly, the historical target is not certified as refuted. Nor is it certified that degree one was silently assumed everywhere in the 2019 report. Those are separate interpretive claims, and neither follows from the inspected source text.

## Acceptance boundary

The accepted statement is: the specified geometric and rational-root assumptions allow the degree-two example, and the displayed unweighted LS semigroup is false for its explicitly modern-normalized valuation on `C[x,y]`.

The rejected overstatement is: this audit has disproved the flag-variety theorem, current LS-type theory, or all intended formulations of the 2019 conjecture.

No source-author code was executed. No publication, repository update, queue edit, or external outreach was performed. No claim of novelty or comprehensive literature status is made. Source verification is bounded to the sources and versions listed in `SOURCE_MANIFEST.json` as checked on 11 October 2026.
