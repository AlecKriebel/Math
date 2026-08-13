# Adversarial review brief

Review only `reviews/bounded_directed_relation_cleanroom/**` and the inert input
artifacts named by its certificates.  Do not open or import the primary
relation compiler, merger, canonicalizer, separator selector, crosswalk code,
or any other review implementation.

Do not launch `verify_all.sh`, `verify_n3.sh`, `cleanroom_verify.py`, or any
other long-running/full replay.  The caller has already produced the exact
certificates sequentially.  Restrict execution to static file inspection and
small read-only probes that finish in seconds; never run two probes
concurrently.  Do not edit any file.

Try to falsify the scoped verdict.  In particular:

1. check the zero-sum split-complement identity and whether the positive
   path-product normal form is an exact image reduction rather than a diagonal
   specialization;
2. inspect direct displayed-switching, descendant-mask, inheritance-weight,
   and invariant-orbit reconstruction;
3. attempt to find a false positive in polynomial equality up to variable
   permutation/product zipping or in exact Bernstein strict-sign checking;
4. check that the directed retention predicate has the correct orientation for
   source-relative containment;
5. challenge every source-support reconstruction and the claimed exhaustive,
   disjoint source-core partition;
6. challenge the 5,344-to-5,344 pending/fixed-full key and final crosswalk;
7. test whether the mixed-graph isomorphism / ordinary-T reduction erases too
   many arrowheads or confuses rooted presentations with labelled
   semi-directed topology;
8. inspect every mutation and confirm that rejection occurs at the intended
   load-bearing check, not merely at an unrelated stale checksum;
9. confirm that incomplete n4 inputs cannot yield a complete verdict and that
   no global theorem is promoted.

Return a concise report with exact file/line references and one of:

- `ADVERSARIALLY VERIFIED`;
- `VERIFIED AFTER CORRECTION`;
- `FAILED`, with a concrete counterexample or reproducible defect;
- `UNRESOLVED`, with the exact missing evidence.

For an interim n3-only invocation, audit the hash-pinned n3 verdict and state
n4 as outside that interim verdict.  For the final invocation, require both n3
and n4 certificates and challenge the combined status.  Do not edit any file;
return the report as your final response for the caller to preserve.
