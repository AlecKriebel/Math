# Research and validation log

Date: 14 September 2026. This is a record of work actually performed in this
session, not a proposed search itinerary.

1. Inspected the primary definition, the two-row example, the attribution,
   and the separate unsolved list. Executed the source/later-result queries
   recorded in `references/source_audit.md`.
2. Recomputed the original 2-by-10 control: row sums 840, column products
   840, 20 distinct entries, total reciprocal sum exactly 2.
3. Normalized the sums by the common product. For three rows this gives a
   sum of pairwise reciprocal products. The elementary inequality
   1/(xy)+1/(xz)+1/(yz) <= 1/x^2+1/y^2+1/z^2 bounds it by a convergent
   distinct-integer reciprocal-square sum, yielding a contradiction.
4. Initial all-row generalization: AM-GM gives
   sum_i prod_{k!=i}(1/a_k) <= sum_i a_i^{-(m-1)}. For m>=3,
   summing over distinct integer entries also gives a bound below 2.
   This route is valid, but it was replaced in the main note by the simpler
   first-three-row reduction, which uses only an explicit sum of squares.
5. The first-three-row reduction proves the claim for *every* m>=3, because
   every omitted integer factor is at least 1. It is not a restriction of
   the investigation to m=3. Wrote an immediate source checkpoint.
6. Independently derived a cyclic-pair proof for all rows, giving the
   stronger ordinary-SP inequality m*S/P < 2. This is a second argument,
   not a claim of an independent human/AI review.
7. Implemented an independent matrix checker with default minimum m=3 and
   explicit --min-rows 2 support for the original control. Implemented
   regression tests, a coefficient-wise polynomial identity check, exact
   rational/integer probes, and a one-command reproducer.
8. Executed `python3 src/reproduce.py`; all 33 checker tests and all exact
   audits passed. Inspected the emitted summary, symbolic certificate,
   exact counts, and unittest result. See `logs/` for actual outputs.
9. Prepared the self-contained note and preserved code, numerical controls,
   references, exact test limits, program versions, and status metadata.

## Deliberately rejected approaches and controls

- No factorization or matrix search was attempted after the general proof
  was found. Therefore there is no hidden finite-search limit being used
  to assert nonexistence, and no failed construction run is being omitted.
- Uniformly doubling the source control preserves ordinary SP structure
  but gives sum 1680 and product 3360. It is deliberately rejected.
- The all-2 3-by-4 matrix has sum=product=8 but violates distinctness. It is
  deliberately rejected even though every required arithmetic equality
  holds. Its reciprocal-square sum, with multiplicity, is 3 rather than <2.
- The source's ordinary 3-by-2 and 2-by-3 examples are rejected for the
  equal-value target, despite satisfying ordinary SP conditions.
- Extending the inverse-square column bound to m=2 is invalid: the source
  column (2,420) is an exact counterexample to that incorrect extension.

## Scope of completion

The mathematical nonexistence result is complete. Finite diagnostics do not
replace the proof. No proof-assistant execution, external independent review,
or exhaustive novelty certification was performed. None is silently claimed.
The remaining optional checks concern provenance/review, not an unproved
mathematical case. No person was contacted and nothing was published.
