# Fixed-variable Rado boundedness: accepted valuation-coloring partial

Problem 3100062 / AMR-030-0062; shared mathematical target with 153 / GREEN-065.

**Accepted partial only. The general fixed-arity target remains unresolved.**
For a nonzero active integer coefficient vector, let c(a) be its least
positive color count admitting an avoiding coloring of the positive integers,
or infinity if the equation is partition regular. Variables may repeat.
Zero coefficients are removed first, with the all-zero case treated separately.

## Results preserved in full

- The infinite greedy coloring of any finite positive distance set D uses at most |D|+1 colors.
- Pairwise distinct coefficient valuations at one prime give c(a) ≤ binom(n,2)+1, independently of the prime and valuation gaps.
- For nonzero coefficient subset sums, bounded p-adic cancellation depth kappa gives c(a) ≤ (p−1)p^(kappa−1)[kappa+binom(t,2)(2kappa−1)], where t is the number of valuation levels.
- The full strict near-minimum cluster proof and the kappa=1 layer corollary remain.
- A primitive two-variable family has arbitrarily large cancellation depth at every prime in a bounded range, yet has exact avoiding number two.
- Exact small arities M(1)=1 and M(2)=2 and the credited Alexeev–Tsimerman family c(a)=n are retained.

The obstruction does not disprove Rado's conjecture. The known exact-degree
family increases the variable count; it is not an unbounded family at one
fixed arity. There is no coefficient-independent bound for arbitrary fixed
arity and no fixed-arity counterexample sequence in this work. No novelty
or priority is claimed for the classical ingredients or auxiliary estimates.

## Files and review meaning

- [PROOF_PARTIAL.md](PROOF_PARTIAL.md): full analytic arguments, domain and zero-coefficient handling, examples and exact remaining gap
- [MATHEMATICAL_AUDIT.md](MATHEMATICAL_AUDIT.md): complete independent analytic audit and recorded supporting checks
- [ACCEPTANCE.json](ACCEPTANCE.json): public proof/audit identities, accepted claims, scope and aggregate check metadata
- [STATUS.json](STATUS.json): unresolved full target, shared identifier, partial results and review limits
- [SOURCE_REVIEW.md](SOURCE_REVIEW.md): credited sources, quantifier distinction and inspection limits
- [SOURCE_METADATA.json](SOURCE_METADATA.json): public bibliography, recorded source identity and retrieval/inspection metadata
- [MANIFEST.json](MANIFEST.json): exact eight-member inventory and seven non-manifest hashes

The manuscript and independent audit are AI-assisted and unrefereed.
Acceptance is a mathematical audit verdict; no external human peer review,
journal acceptance or formal proof-assistant certification is claimed.
Bibliographic priority and worldwide current openness are not certified.

## Editorial and distribution boundary

All analytic proof sections and mathematical qualifications are preserved.
Editorial changes reconcile acceptance, bind the public proof and audit,
remove private provenance and stale pending-review state, and identify
recorded computational and source observations as historical. The analytic
verdict depends on no omitted program, raw output, or dataset. Finite checks
are supporting aggregate metadata only.

Programs, raw outputs, dataset contents, copied source bodies/PDFs/images,
and private coordination material are excluded. Edition preparation made
no mathematical computation rerun or new scholarly-source retrieval,
source-file rehash, source inspection, or literature search.

QUEUE.md and all unrelated repository content remain unchanged. No merge,
release, DOI, journal submission, or external outreach is implied.
