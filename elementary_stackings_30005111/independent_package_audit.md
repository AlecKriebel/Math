# Independent package audit: immersed theorem and construction

Verdict: ACCEPTED within the primitive immersed-loop scope. The unrestricted-walk counterexample and its mathematical correctness have a separate independent reviewer and are not incorporated into this verdict.

The final proof was reread after its orientation, absolute-degree and compactness clarifications. The complete mathematical audit is in independent_elementary_audit.md. The proof is elementary and self-contained; it does not depend on Howie or maximal-cyclic-tower results.

The original research checker contained ten optimization-sensitive assertions. I independently reconstructed the Assert-to-explicit-if/raise AST transformation and compared it to the publication checker: the ASTs match exactly, and the publication checker contains no Assert nodes. The transformation preserves all check conditions and control flow. Both normal and optimized publication executions byte-match cochain_results.json.

The independently authored check_cochain_independent.py is copied verbatim from its latest research version and contains no assertions. Normal and optimized package executions byte-match cochain_independent_results.json: 3,292 rose cases, 372 subdivisions, six additional bridge/barbell and theta graph cases, four rejected corrupt certificates, and four rejected invalid input classes. In particular, the independent verifier checks reverse-edge endpoint ordering, loops, exact rational heights, terminal covering degree, strict bounded vertex-count growth, and all affine strand separations. Its malformed-input boundary is explicit; the construction itself is not presented as a general parser for arbitrary malformed walks.

I also replayed verify_certificates.py in normal and optimized modes after installing the final independent checker. Both modes agree and reject all five listed real mutations, including a height collision and a reversed-edge orientation corruption. This replay verifies the executable result, not an additional independent mathematical review of the backtracking counterexample.

Audited content hashes and byte counts are in independent_package_hashes.json. Package-wide manifest, publication, and final repository status remain the assembling worker’s responsibility. These finite tests corroborate, rather than replace, the mathematical proof.
