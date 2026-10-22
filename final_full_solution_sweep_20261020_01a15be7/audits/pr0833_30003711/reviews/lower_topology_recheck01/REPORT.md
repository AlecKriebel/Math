# PR833 lower-bound topology recheck

Completed 2026-10-21T19:21:35.448338+00:00. Review scope: original PR head `0e6e23213494ecb4a7208f920d25d7b49502a5cb`, problem30003711. This is an independent mathematical audit, not a claim of conventional human peer review or a formal proof-assistant certificate.

**Conclusion.** The original equality certification remains unsupported by its cited lower-bound proof. For exactly the cover and map appearing in Chen–Wan arXiv:2306.17303v2 Proposition4.2(1), the asserted degree-seven map is identically zero. This is a falsification of that detector, not a disproof that the genus is8. No new proof of lower bound8 was found, and no evidence from this recheck reopens equality certification. The separate upper-bound construction is not affected by this failure.

## Claim and dependency

The original author proof defines X as smooth homogeneous ternary complex cubic equations modulo nonzero scalar, namely CP9 minus the discriminant; Y chooses one flex. Its target is ordinary, unnormalized section Schwarz genus g(Y/X)=8. It imports its entire lower bound from Chen–Wan Theorems1.2/4.1. This is the same base, cover and section convention as the inspected primary paper; normalization or replacing the coefficient space by moduli does not explain the failure.

The cited proof takes K=C3×C3 generated projectively by the coordinate cycle A and B=diag(1,omega,omega²), and uses the Fermat orbit map M=PU(3)/K -> X. Its pullback is the principal nine-sheet cover PU(3)->M, since K acts regularly on the nine flexes. Those reductions are valid. The crucial assertion is that its classifying map c:M->BK induces a nonzero map in H7 with constant trivial F3 coefficients. The subsequent genus≥8 inference is conditional on that assertion.

## Checkable independent derivation

Use omega³=1, omega≠1. The actual inverse image of K under SU(3)->PU(3) is

    P = {omega^t A^a B^b : a,b,t in F3},
    (a,b,t)(d,e,s) = (a+d,b+e,t+s+bd).

Here BA=omega AB. The27 matrices are distinct and determinant1; P has exponent3, center and commutator subgroup {(0,0,t)}, and P_ab=K. Thus M=SU(3)/P has pi1(M)=P, while the nine-sheet cover is the quotient of the universal P-cover by the central C3. Its classifying map c induces exactly P->K. In particular,

    c*:H1(BK;F3) -> H1(M;F3)

is an isomorphism of two-dimensional vector spaces.

Write u(a,b)=a and v(a,b)=b for the degree-one coordinate classes on K. On P the normalized one-cochain f(a,b,t)=t-ab satisfies, for trivial coefficients,

    delta f(g,h) = f(h)-f(gh)+f(g) = a(g)b(h).

So the inflation of uv is zero in H2(BP;F3). Since c factors through the classifying map of the universal P-cover, c*(uv)=0 on M.

The standard cohomology algebra is

    H*(BK;F3) = Lambda(u,v) tensor F3[x,y],
    deg(u)=deg(v)=1, deg(x)=deg(y)=2.

Every alpha in H7(BK;F3) has the form u P3(x,y)+v Q3(x,y). Its product with u or v is zero or a multiple of uv, hence its pullback pairs to zero with both generators of H1(M;F3). The manifold M is closed, connected, oriented, of real dimension8: right translations preserve the orientation of the connected Lie group SU(3). Poincare duality over F3 makes the H7 by H1 pairing nondegenerate. Consequently

    c*:H7(BK;F3) -> H7(M;F3) = 0.

This contradicts precisely Proposition4.2(1). The target H7 itself has dimension2 by the same duality; the conclusion is not caused by a zero target. The argument uses neither Leary's full ring presentation nor a spectral-sequence edge-kernel assumption.

## Adversarial checks and repairs

The projective order9 group is not the fundamental group of M. Substituting it for the order27 central extension is an invalid repair. The Poincare-duality argument takes place on compact M, not noncompact X. Its map factorization is forced by the actual universal cover, not an arbitrary group map. Constant F3 coefficients are exactly those in Proposition4.2; no claim is made that this proves vanishing with every twisted module.

Changing the displayed degree7 candidate cannot help, because the entire map in that degree is zero. Leary's original Theorem2 has the primed relation c2 y'=-x'² y'; CWv2 prints an inconsistent unprimed x² in its summary and later uses the primed version. Correcting this typographic inconsistency does not change the independent contradiction above. The assertion that naturality of the Chern transgressions alone identifies the full edge-kernel with the Chern ideal is not a general spectral-sequence theorem; additional differentials require verification. This recheck does not claim a new independent calculation of the precise omitted higher differential.

A verified degree7 detector with another coefficient system, another geometric restriction, or a direct obstruction argument could still prove g(Y/X)≥8. Merely positing such a detector transfers the missing proof to an unsupported equivalent claim and remains blocked. The truth of genus8 is unresolved by this audit. The elementary baseline g(Y/X)≥2 follows already because its Fermat pullback PU(3)->M is connected and nontrivial and therefore has no global section. No sharper numerical lower bound is certified here.

## Independence, sources, and reproducibility

`INDEPENDENT_RECONSTRUCTION.md` was saved and hashed before reading any integrated/root/other-auditor findings. Its SHA256 is `7cfe682f57fc34e65d78e16ce523d0c89c9fd7688f1741b473dc42d6f8b416e7` (3464bytes). `PRE_CORRECTION_RECONSTRUCTION_HASHES.json` freezes that checkpoint. Only afterward was the permitted integrated audit at Git98ee5482 read; it independently contains the same obstruction. The initial log bytes are retained in `checkpoint01/RESEARCH_LOG.md` so the pre-correction log digest remains checkable after continuation.

Primary [CWv2](https://arxiv.org/pdf/2306.17303v2) pages5–7 were inspected from the fixed-version PDF and matching HTML. The current [arXiv version record](https://arxiv.org/abs/2306.17303v2) identifies July21,2023v2 as its latest revision. Primary [Leary](https://arxiv.org/pdf/0711.4831) Theorem2 was inspected to test the typo repair. The 2025 journal body was not inspected; its correctness or changes are not inferred from the2023 preprint. Raw third-party copies and extraction files remain private with source receipts.

`check_extension_controls.py` uses exact Eisenstein arithmetic for the actual matrices and exact F3 elimination. Normal and optimized runs both verify27 distinct SU3 matrices,729 matrix products,19683 associativity triples,729 cup-coboundary pairs, and H1 equation rank25/dimension2. Both reject six deliberate corruptions: wrong commutator, abelian substitution, swapped cocycle, wrong cochain sign, wrong H1 dimension, and falsely nonzero inflated uv. Results are in the two `CONTROL_RESULTS_*.json` files. The finite computations validate algebraic inputs; orientability, factorization and duality are the explicit mathematical deductions above.

All work is confined to this assigned review folder. No original or previously sealed program was executed or modified. No external communication, outreach draft, PR/ledger/Zenodo mutation, publication or branch/commit/remote-state change was made. Duplicate-publication screening was supplied by the parent task and was not rerun or represented as a new check here. Best estimate: assigned recheck100% complete; the exact lower-bound8 proof remains an unfilled research gap. SHA256/size manifests and private reading receipts seal the outputs.
