# Status: partial obstruction, original question unresolved

Problem: can the positive integers be partitioned into two sets, each having an omega enumeration with no increasing or decreasing three-term arithmetic progression at arbitrary subsequence positions?

## Edition and review status

These AI-assisted authored documents and their independent internal AI audit are unrefereed. “Accepted” refers only to the corrected partial results in this edition. No external human peer review, journal acceptance, formal proof-assistant certification, novelty or exhaustive worldwide-status determination is claimed.

Both required domain/scope corrections have been applied to PROOF.md: Theorem 1 counts positive integer starts, and the affine extension treats finite and infinite intersections separately in positive coordinates. The original candidate is not accepted literally as written.

## Established in this packet

1. **Bounded-deficit interval obstruction.** For every 3-permutable set S and every fixed C>=0, only finitely many complete intervals [n,2n-C] are contained in S. The proof transplants Kasel's finite C3 obstruction and includes a self-contained proof of that finite lemma.
2. **Quantitative prefix pressure.** With two fixed adjacent anchors, k distinct shifted C3 intervals force at least k other distinct values before the later anchor. Its position is at least k+2.
3. **Partition consequence.** All bounded-additive-error dyadic run partitions fail, as does any two-color partition with infinitely many full monochromatic intervals whose doubling deficits stay bounded above.
4. **No universal divergence rate.** For any preassigned unbounded nondecreasing f, an adaptation of Geneson's construction gives a single 3-permutable set of upper density at least 2/3 containing full intervals with positive deficits at most f of their starting points. This is consistent with the deficits tending to infinity.
5. **Formulation correction.** The zero-based and positive-integer versions of the two-set existence question are equivalent by translation. This corrects Kasel's Remark 3 without using a claim about adjoining zero to one fixed set.

These results do not prove that every two-coloring fails or produce a valid two-set partition. There is no claim of novelty; the central finite lemma and the positive-density construction are explicitly attributed. Neither the older 1/2 density conjecture nor neighboring four-term results are used as evidence of a solution.

## Historically recorded verification

The universal results have hand proofs in PROOF.md. The following finite checks were recorded during candidate preparation and audit; their code, certificates and detailed outputs are omitted from this prose-only edition. Finite checking is corroboration only:

- All 16 exhaustive phase branches at M=16,24,32,40,48,56,64,80,96,128 have elementary AP-reflection/transitivity contradiction certificates.
- The checker is separate from the generator and verifies every proof step, every permitted hypothesis, exhaustive branch coverage, and the final reverse-edge contradiction.
- Twelve malformed-certificate controls are rejected.
- All 282 admissible orders of {1,...,8} pass the mirror-propagation checks.
- Increasing, decreasing, and nonconsecutive AP controls are explicitly checked.
- Rounding, guard arithmetic, block-separation arithmetic, and two logarithmic-deficit examples are checked.
- Normal, -O, and -OO runs give identical JSON results. No check relies on Python assert statements.

No third-party SAT solver, source code, or downloaded executable was run during the recorded checks. No new scholarly-source retrieval, inspection or mathematical search was performed during edition preparation.
