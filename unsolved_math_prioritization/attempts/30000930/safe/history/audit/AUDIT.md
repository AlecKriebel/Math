# Independent audit of the unweighted convolution obstruction

## Verdict and scope

**PASS for a known obstruction to the literal unweighted, complex-oriented product.** The frozen packet's Jordan-type (2,2) calculation is correct. The associator is 4t in the AB block and is nonzero over C. This excludes an algebra isomorphism from any associative Yoneda Ext algebra to that particular multiplication. It does not resolve the coherent-sheaf Yoneda comparison with a weighted or sign-adjusted convolution, nor establish the current global status of that comparison. No novelty claim is supported or made.

The appropriate disposition is `SOURCE_FORMULATION_CORRECTION_KNOWN_UNWEIGHTED_OBSTRUCTION`, with the multiplication and scope spelled out. An unqualified label such as "Ext/arc conjecture refuted" would be misleading. Early stopping is justified for verifying this prior obstruction and the literal f=1 reading; it is not evidence that the intended weighted comparison has been solved.

This audit is bound to `author-packet.zip`, 18,021 bytes, SHA256 `ae7427fca8dc6414d40b0a499fa58e2cd7056151f3c5a781170a96df72c0a3a1`. The original archive and source packet were not modified. The accompanying binding records the complete member list and audit-file checksums.

## Source formulation and a convention warning

The [2008 Oberwolfach report](https://ems.press/content/serial-article-files/46153), printed p.438, prescribes pullback to the triple intersection, cup product, and pushforward without an inserted weighting class. Conjecture 8 on p.440 refers back to that convolution. The report does not explicitly fix orientation signs at that definition. The literal refutation therefore must retain the packet's qualification that these are ordinary complex-oriented Gysin maps. Its printed shift n-c is inconsistent with n as the number of points; that issue is unnecessary for the associativity argument.

The [final Stroppel--Webster article](https://ems.press/content/serial-article-files/43290), p.500, uses a class f and fixes complex orientations; it explicitly states that f=1 is nonassociative. Theorem 35 on p.501 supplies a suitable associative weighted product. Page 507 independently identifies ordinary complex-oriented convolution as nonassociative. Conjecture 42 and Remark 43 on p.511 leave the Yoneda-product identification unsettled there and do not unambiguously pin it to a specified f.

An additional source warning was found: the alpha labels in Section 4.3 are internally inconsistent. Page 504 calls alpha=+1 the natural orientation, whereas p.505 identifies alpha=-1 with the nonassociative product and alpha=+1 with the arc algebra. The audit does not use those labels to set signs. The geometry and the unambiguous statements on pp.500 and 507 suffice. This inconsistency does not overturn the packet's result.

Both primary PDFs were independently retrieved from the official URLs and matched the packet's byte counts and SHA256 values. Relevant printed pages were visually inspected. No source PDF, source passage, or extracted text is included in this portable audit.

## Independent geometry check

Write V=W plus W', with N identifying W' with W and vanishing on W. Every flag satisfies F1 subset W subset F3. The locus F2=W is A=P(W) times P(V/W), hence P1 times P1. If F2 differs from W, then F2 intersect W=F1, forcing N(F3)=F1 and F3=N inverse(F1). This is the other component B. Over L in P(W), its middle-plane choices form the projective bundle of lines in (W/L) plus L, namely P(O(1) plus O(-1))=F2. Both are smooth irreducible surfaces and cover the Springer fiber.

The intersection C consists of F1=L, F2=W, F3=N inverse(L). It is a P1, diagonal in A and the section selecting O(1) in the lines convention for B. The two normal bundles are consequently O(2) and Hom(O(1),O(-1))=O(-2). The sign in the second normal degree has not been replaced by the quotient-convention sign.

A local check also makes the reduced and clean intersection explicit. In an affine neighborhood of any point of C after a simultaneous basis change in W and W', set

- F1=span(e1+z f1)
- F3=W plus span(e2+w f2)
- F2/F1=span(f1+q(e2+w f2)) modulo F1.

The nilpotent incidence equations reduce to q(w-z)=0. The two components are q=0 and w-z=0; their intersection is defined by q=w-z=0. Thus the scheme-theoretic intersection is reduced and their common tangent space is the tangent of C. These charts cover C by changing the base-line chart.

With t positively normalized by integral_C(t)=1, the complex-oriented self-intersection formula gives a-star a-push(1)=2t and b-star b-push(1)=-2t. Taking the two distinct off-diagonal unit classes u in H_AB and v in H_BA yields

    (u*v)*u = 2t,    u*(v*u) = -2t.

These elements lie in the same AB summand. Their difference is 4t. The reversed triple has difference -4t in BA. Associative graded Yoneda composition is associative without a sign in its associativity axiom; merely shifting vector-space degrees cannot remove this defect. Multiplication-preserving bijections need not preserve the component idempotents for this obstruction to apply.

## Independent exact computation

The author's verifier was replayed from a separate extraction of the frozen archive. Its manifest check passed for all 12 listed payload files, and its emitted JSON matched `CONTROL_RESULTS.json` byte for byte.

The new `independent_check.py` does not import the author's code or reuse its monomial-reduction algorithm. It starts from the two divisor intersection matrices

    A: [[0,1],[1,0]],    B: [[0,1],[1,-2]]

and the restriction vectors (1,1) and (1,-2). It derives both Gysin maps as adjoints of restriction under Poincare duality by solving exact linear systems. Those derived maps give a-push(1)=x+y, a-push(t)=xy, b-push(1)=s, and b-push(t)=hs.

It then constructs a symbolic structure tensor over Q[lambda_A,lambda_B] and contracts both associations for all 12^3=1,728 ordered basis triples. Exactly two symbolic associators are nonzero:

    (u,v,u):  2(lambda_A+lambda_B) tu
    (v,u,v): -2(lambda_A+lambda_B) tv.

All other basis triples have zero symbolic associator. In particular, natural weights (1,1) give the asserted two defects; weights (1,-1) and (0,0) give associative products. The table is associative over characteristic 2, and still fails over characteristics 3 and 5. The two-sided unit and every product's codimension-shifted degree were checked. Comparison with the frozen author's implementation agrees on all 144 basis products at each of four exact parameter pairs, including a nonintegral pair, for 576 comparisons total.

This establishes the claimed iff condition lambda_A+lambda_B=0 over C by an exact symbolic computation, independently of the author's finite parameter grid. Trilinearity makes basis-triple checking exhaustive for this 12-dimensional model. As a conceptual check, triples with two off-diagonal factors satisfy the projection formula, while the alternating three-factor triples compare the two self-intersection classes.

For the sign repair, p=h and q=-s-h obey p squared=q squared=0, both restrict to t, and -b-push(1)=p+q, -b-push(t)=pq. Thus the claimed two-matching arc multiplication is consistent. This is a changed product and is not a calculation of coherent-sheaf composition.

## Other claims and boundaries

The general clean-intersection associator is the difference of the two normal first Chern classes. For Lagrangian surfaces in a holomorphic symplectic fourfold, the cross-pairing of their tangent bundles has radical TC on both sides. It descends to a nondegenerate pairing of their normal lines along C, making those lines dual. The packet's general formula follows.

The k=1 calculation is correct: the zero section P1 in T*P1 has normal bundle O(-2); the divisor resolution gives global self-Ext only in degrees 0 and 2, with the degree-2 generator square zero. The stated k=2 Hilbert polynomial is also correct. Neither calculation fixes mixed Yoneda compositions.

The [Mladenov article](https://link.springer.com/article/10.1007/s00029-023-00894-3), Theorems 0.1.8 and 0.1.12, gives a single-object algebra-formality result and a pairwise module-formality result. The collection-level question remains separately conjectural in that article, Conjecture 0.3.4. These assertions do not supply simultaneous compatibility of the entire mixed composition algebra. No exhaustive contemporary literature search or global-open-status claim is certified by this audit.

The audit does not independently certify repository duplicate checks, prior personal history, the live problem-page content, or campaign accounting policy. Those are separate from the mathematical result. No remote writes or helper reviewers were used.

## Reproduction

Keep this directory's files together and provide the exact author archive:

    python3 replay_audit.py /path/to/author-packet.zip

The replay verifies both bindings, the author's manifest and exact output, the independently generated output, and all 576 product comparisons. Python 3 and its standard library suffice.

## Publication wording

A suitable concise description is: "A source-formulation correction: the unweighted complex-oriented convolution in the 2008 formulation has a nonzero associator already for Jordan type (2,2). The final 2012 paper already records this obstruction and constructs a weighted repair. The explicit witness and verification do not settle the weighted coherent-sheaf Yoneda comparison."

No blocking mathematical error was found. The orientation qualification, known-prior attribution, alpha-label warning, and exclusion of the weighted Yoneda comparison should travel with any public status record.
