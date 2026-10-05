# Independent source audit: 2725 / KP-1.66

**Verdict: PASS for the credited known negative answer. Antisymmetry fails for the exact relation asked in KP-1.66, already on knots. No mandatory correction is required.**

Reviewed on 2026-09-30 using gpt-6-astra with xhigh reasoning. The frozen KNOWN_RESULT.md has SHA-256:

af59561f9c977412d0e95c382cd36e6fb339f35baea777bc4dfd4d3d3afc6de1.

This is an independent source-match and theorem-to-target audit. It does not independently certify the full construction or its h-principle dependencies, and it gives no campaign discovery credit.

## Original target

I read and visually inspected [K3, printed p.63](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf), Problem 1.66, and read the remarks continuing onto p.64. The relation is existence of an **exact Lagrangian cobordism in the symplectization of standard contact three-space** between Legendrian links.

The conventional equivalence is Legendrian isotopy, as made explicit in the current result's formulation. The original source already distinguishes failure of symmetry from the question of being a partial order. The submitted note correctly targets antisymmetry.

No regularity, decomposability, absence of stabilizations, or higher-dimensional restriction is imposed on the original relation. A pair of knots is an admissible pair of one-component links.

## Exact current theorem

The inspected full source is the [versioned author manuscript arXiv:2409.00290v4](https://arxiv.org/pdf/2409.00290v4), by Georgios Dimitroglou Rizell and Roman Golovko. I checked Theorem 1.4, Corollary 1.5, the end conventions in Section 2.1, Theorem 5.7 and its proof, Example 5.8, and the relevant statements in Section 5 and Appendix A.

Theorem 1.4, restated as Theorem 5.7, requires a **decomposable Lagrangian disc filling**, not merely a filling of arbitrary genus. It gives an exact Lagrangian concordance in
$$
(\mathbb R_t\times\mathbb R^3,\ d(e^t\alpha_0))
$$
from the sufficiently stabilized knot to the standard unknot stabilized the same number of times, with stabilizations of both signs. Example 5.8 and Corollary 1.5 identify a disc-fillable representative of the **mirror of $9_{46}$** as an example. The overbar in this knot notation was visually checked.

Corollary 1.5 expressly supplies concordances in both directions for the same stabilized pair. The forward direction from the unknot comes from puncturing the disc filling and preserving concordance under simultaneous stabilization. The reverse direction is the new construction. This is not an inference from the paper's separate high-dimensional front-spinning isotopy.

The ends are the concave/negative and convex/positive Legendrian boundaries defined in Section 2.1. The cobordisms used here are cylinders, hence orientable; no nonorientable cobordism is substituted. The corollary's mutuality is already a statement about the same Legendrian endpoints. Distinct underlying unoriented smooth knot types also exclude isotopy regardless of any additional orientation labels.

## Antisymmetry and exactness

Let $A$ be the sufficiently both-sign-stabilized mirror-$9_{46}$ representative, and $B$ the correspondingly stabilized standard unknot. The cited concordances imply $A\preceq B$ and $B\preceq A$ for the question's more general cobordism relation.

Legendrian stabilization changes the Legendrian representative but preserves the smooth knot type. Therefore $A$ remains smoothly knotted and $B$ remains smoothly unknotted. They cannot be Legendrian isotopic. This is a failure of antisymmetry, and passing from knots to links cannot remove it.

The existence theorem explicitly asserts exactness. The note's supplementary cylinder argument is also correct: on a Lagrangian cylinder $L$, the restricted Liouville form is closed. Its period on a cylindrical Legendrian end circle is zero, and that circle generates $H_1(L;\mathbb Z)$. All periods therefore vanish, giving a smooth global primitive. The form vanishes on each cylindrical end, so the primitive is constant on each connected end. These constants need not equal each other; the standard exact-cobordism condition allows this. No stronger common-constant convention is silently imposed.

This cylinder observation does not make arbitrary positive-genus Lagrangian cobordisms automatically exact. The restriction to the cited concordances is essential.

## Version and publication status

The [arXiv record](https://arxiv.org/abs/2409.00290v4) reports first submission on 30 August 2024, v4 on 8 July 2026, and acceptance in *Advances in Mathematics*. The [author's publication list](https://sites.google.com/site/ragolovko/publications) gives volume 502 (2026), article 111133, DOI [10.1016/j.aim.2026.111133](https://doi.org/10.1016/j.aim.2026.111133). The publisher's indexed record and Crossref metadata corroborate those details.

The assigned print issue is October 2026, which is later than this audit date. Crossref's DOI creation date is 20 July 2026; it is not treated here as a separately verified online-publication date. “Accepted, with assigned journal bibliographic details” is the conservative current description. Direct publisher access returned 403, so no publisher-typeset full-text inspection is claimed.

I also checked the [arXiv record of the approximation input, 2408.16614v2](https://arxiv.org/abs/2408.16614v2). Its March 2025 correction preserves a smooth isotopy class rather than necessarily a totally real isotopy class. The audited v4 paper's Theorem 5.3 uses the corrected smooth-isotopy wording. This source check does not reconstruct that input's full proof.

## Integrity and limitations

Both cached primary PDF hashes match the source manifest. The packaged source record matches numeric ID 2725 in the pinned dataset, and the frozen note hash matches the handoff. No numerical experiment or symbolic identity is offered as a substitute for the cited existence theorem.

The report's exact-source conclusion requires no smallest stabilization count. It does not settle a different relation requiring regular or decomposable cobordisms. The submitted note preserves these limits and attributes the mathematical result to its authors.

**Disposition: already_solved, known negative answer, zero campaign proof attempts.** Keep the explicit limits on full-proof verification and publisher access. No author file was changed during this review.
