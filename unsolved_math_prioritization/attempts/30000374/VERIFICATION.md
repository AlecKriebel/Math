# Verification scope for the partial theorem

The following authored checks preceded the independent mathematical audit. That audit subsequently accepted the partial theorem without mathematical correction; its complete reconstruction is in AUDIT.md and its scope is recorded in ACCEPTANCE.json. The proof was checked against the source definition and checked internally for these obligations:

1. The product spaces are standard Borel, including the empty and singleton cases.
2. A witnessing rational map extends continuously across every irrational cut; continuity only on the rational subspace is not substituted.
3. The fixed source compact set has exactly its isolated markers as rational points. This is the condition allowing a branch embedding to be extended with rational preservation.
4. The rational target markers are globally distinct, and every output coordinate depends on at most one input tree membership test, giving a continuous coding map.
5. A closure point of a well founded target tree must stop at a finite node. Infinite descent through child intervals would exhibit an actual infinite branch.
6. A branch selects a full binary subtree with compact order structure matching the source, and all required marked rational points have marked rational images.
7. Compactness gives h(closure A) = closure h(A); hence injectivity contradicts countability of the closure in the well founded case.
8. These arguments use only the colors 0 and 1, so they apply unchanged to every ordinal α ≥ 2.
9. Analytic set completeness is kept distinct from universality of a preorder under one pair preserving Borel map.
10. The greatest class uses a single common interval for all color tails; an interval depending on the color is insufficient.

Exact rational arithmetic diagnostics checked 1,555 target nodes, 255 source nodes, 16 natural child labels per checked parent, and four selected branch patterns. They checked child interiors, strict separation, shrinking diameters, distinct markers, finite rational avoidance, and agreement of marker order. Two deliberately invalid local conditions were rejected. The same checks passed under normal, optimized, and doubly optimized Python execution. These are finite diagnostics; they do not replace any compactness, infinite branch, or descriptive set theoretic proof.

Primary source formulas were read as extracted text and checked on rendered pages where relevant. The current invariant universality PDF matched the supplied source copy exactly. Public source hash metadata accompanies this document.

The independently reviewed partial result is accepted internally. The proof is byte-identical to the frozen original, and all substantive audit reasoning is retained. The mathematical proof is standalone: no omitted finite diagnostic, program, generated certificate or source file is needed to complete an argument.

Edition preparation replayed the independently audited input verification and its exact-rational controls in normal, -O and -OO Python. These checks establish recorded identities and finite regression results, not infinite mathematical conclusions. The source-review and page-inspection statements above are inherited from the authored review and independent audit of 10 October 2026; no new literature search or source-page inspection was performed for this edition.

The public manifest covers exact bytes of all non-manifest members. The proposed draft-PR body separately pins every public file, including the manifest. Local verification checks the exact allowlist, complete editorial provenance, addition-only patch and complete native Git trees. These integrity checks are not a formal proof-assistant certificate. The proof and audit are AI-assisted and unrefereed; internal acceptance is not external human peer review or journal acceptance. There is no novelty, priority, global-openness or full-classification claim.
