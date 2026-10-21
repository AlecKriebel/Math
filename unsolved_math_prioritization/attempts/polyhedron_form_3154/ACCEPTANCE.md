# Scoped acceptance: polyhedron form distribution

21 October 2026. Row 1875; ID 3154; OPG-36933.

Disposition: ACCEPT EXISTING SOLUTION, ATTRIBUTED; NO NOVELTY CLAIM.

For uniformly sampled unlabelled combinatorial types of convex three-dimensional polyhedra with e edges, beta=V/(e+2) converges in probability to 1/2 and sqrt(e)(beta−1/2) converges in distribution to N(0,1/32). In addition E[V]=(e+2)/2 exactly and Var(V)~e/32. Limits are through admissible edge counts.

The exact target is stated in Lachlan Bridges's September 2026 preprint, Theorem 1.1(vi), https://arxiv.org/abs/2609.22402v1. Its proof follows from classical published uniform rooted and unrooted enumeration/asymmetry results, independently verified here at the statement/application level. The authored proof audit and independent adversarial review both accept the target implication, including full-support tails, normalization, parity, uniform unrooting, and moment uniform integrability.

Acceptance is mathematical and scoped to the target CLT/concentration/variance conclusion. It does not assert journal acceptance of the preprint, novelty, or audit approval of all its stronger assertions. The source gate reports no journal reference at inspection. Classical theorem proofs are treated as published dependencies rather than fully reconstructed. The numerical weights used in the check script are asymptotic proxies, not exact enumeration.

One editorial caveat is recorded: the CLT and variance asymptotic are not logically equivalent in general. The manuscript separately proves uniform integrability and moment convergence, which supplies the needed variance conclusion. This is not a blocking gap.

Public-safe authored deliverables: CLT_PROOF_AUDIT.md, independent_clt_review.md, ACCEPTANCE.md, check_constants.py, check_results.json, verification_manifest.json. Publication must exclude the private subdirectory, downloaded source PDFs/text, dataset record/contents, and coordination material. No queue edit or publication was performed by this audit.
