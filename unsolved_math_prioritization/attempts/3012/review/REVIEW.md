# Independent adversarial review: connected sums of topological manifold pairs

**Verdict: PASS_CONDITIONAL_LEMMA_AND_OBSTRUCTION.** The all-codimension fiber-preserving isotopy and its compactly supported collar extension are valid under the displayed hypotheses. The original higher-codimension connected-sum problem remains unsolved. No mathematical correction is required.

Reviewed on 2026-09-30 by a separate AI reviewer, gpt-6-astra with xhigh reasoning. This is not human peer review.

## Frozen artifact and source scope

- Problem 3012 / KP-5.5
- OBSTRUCTION.md SHA256 **eb6986ba77d7639e6f4df4d41cc2d89b23865d5040be01454ea832b4c2d73bd3**
- Recommended original-target status: **unsolved, 2/5 substantive approaches**
- No historical novelty or counterexample is established
- No author source was changed during this review

The reviewer read the complete mathematical artifact, its source notes and manifests, Livingston's complete published paper and relevant earlier-version appendices, and visually checked the original K3 page 304. Bounded current-source searches found no verified general resolution; this is not an exhaustive literature certificate.

The [original K3 source](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf) distinguishes codimensions one and two from the range of codimension greater than two and ambient dimension greater than four. Its suggested pairwise surgery route is not a theorem supplied by the artifact.

[Livingston's published paper](https://doi.org/10.1017/prm.2022.87), *Proceedings of the Royal Society of Edinburgh A* 154 (2024), 1937–1944, was published online on 16 January 2023. Its page 1938 conventions specify oriented topological manifolds and locally flat submanifolds; interior sums may also be considered for manifolds with boundary. Its Theorem 3.2 is the credited codimension-two result. Problem 4.1 explicitly retains the general higher-codimension problem, and Problem 4.2 states the Relative Annulus Conjecture.

The artifact's connected, oriented, interior-sum conventions are appropriate. In particular, compatibility with the orientation of the distinguished submanifold is substantive. Merely preserving ambient orientation would not imply that the base map in the conditional lemma preserves orientation. The artifact explicitly includes the required base and fiber orientation hypotheses and does not exploit ambiguities in the abbreviated source question.

## 1. Pointed disk homeomorphisms: the all-dimensional input is valid

The earlier version [arXiv:2104.03930v1](https://arxiv.org/abs/2104.03930), Theorem 1 on printed page 2, recalls the ordinary topological fact that orientation-preserving self-homeomorphisms of every sphere are isotopic to the identity. Its proof and Appendix A identify the stable-homeomorphism and annulus inputs, including dimension four. The published proof of Theorem 2.2 uses the same ordinary result. This review imports that established topological theorem; it does not reprove its deep foundations or replace it with a smooth analogue.

For a disk self-homeomorphism fixing zero, let c be the cone on its boundary map. The residual map c⁻¹h fixes both boundary and zero. The Alexander isotopy of that residual map fixes both: each scaled interior value at zero is zero, and the boundary seam is fixed. Composing with c joins h to c. Coning a boundary isotopy then joins c to the identity while keeping zero fixed. In dimension one the orientation-compatible boundary map is the identity, so the argument still applies.

Thus the pointed group is path-connected in precisely the sense needed. No stronger assertion about a deformation retraction onto an orthogonal group is required. In particular, the proof does not extrapolate the special two-dimensional homotopy-type theorem to arbitrary codimension.

## 2. Fiber contraction and its inverses

Write the given map as g(x,y) = (a(x),b_x(y)). If a_t is a path from a to the identity, the first stage can explicitly be taken as (a_t(x),b_x(y)). Its inverse first applies a_t⁻¹ to the base coordinate and then the corresponding b_x⁻¹ to the fiber. Thus this stage really consists of homeomorphisms; it does not require a_t to fix the base origin.

Once the base map is the identity, replacing x by (1−t)x in the fiber parameter is legitimate because the base disk is convex. At the endpoint the fiber is b_0 everywhere. A pointed path from b_0 to the identity completes the isotopy.

The family x ↦ b_x is continuous in the compact-open topology: joint continuity on a compact product gives uniform continuity in the fiber variable. Inversion is continuous in the homeomorphism group of the compact disk. Alternatively, the parameterized map (t,x,y) ↦ (t,x,b_(1−t)x(y)) is a continuous bijection of a compact space to itself, so its inverse is continuous. This verifies joint inverse continuity, rather than only invertibility for each parameter.

The contraction need not fix the boundary of the product ball. The lemma only promises an isotopy of pairs, and the next collar construction handles precisely that boundary motion.

## 3. Compact collar extension, including both seams

Let h_s run from the identity to g on P. Any homeomorphism of the topological ball P preserves its boundary. With the product gauge p, every nonzero point has a unique radial decomposition ru with u on that boundary.

On the shell 1 ≤ r ≤ 2, the proposed extension is r h_(s(2−r))(u). Since the boundary image again has gauge one, this preserves the radial coordinate r. Its inverse is obtained by substituting the inverse boundary homeomorphism at the same parameter. The parameter remains in [0,1].

At r = 1 the shell agrees exactly with h_s; at r = 2 it agrees exactly with the identity. The inverse formulas satisfy the same matching. The inside formula handles the origin. Joint continuity in s follows from the given isotopy and its continuous inverse. Therefore these are global homeomorphisms of Euclidean space, not merely continuous shell maps.

Each h_s preserves the zero section as a set, hence also its intersection with the boundary. The extension and inverse consequently preserve the entire distinguished linear subspace. It is the identity outside 2P and starts at the identity. The isotopy therefore has all the compact support and pair-preservation properties claimed.

This construction is conditional on already having the product-pair isotopy. It provides no isotopy for an arbitrary unaligned pair germ.

## 4. Descent to connected sums

When the chart images already agree on P and g = φ⁻¹φ′ satisfies the fiber hypothesis, the transported extension E has Eφ = φ′ on P. Its support lies in the chart image of the compact set 2P, so setting it equal to the identity elsewhere is continuous.

Using E⁻¹ on the punctured changed summand sends φ′(u) to φ(u) for every boundary coordinate u. The identity on the other summand therefore respects the two gluing equivalence relations. The inverse descends in the reverse direction. Both maps preserve the distinguished submanifolds, and orientation preservation follows from the ambient pair isotopy.

Matching the ball images alone is insufficient for this argument. Matching their parametrizations through the indicated E is the exact fact used. The artifact makes that distinction.

## 5. The unresolved alignment and annulus issues are not bypassed

Published Lemma 3.4 on pages 1940–1941 performs the preceding codimension-two normal-bundle alignment. Lemma 3.5 then removes the fiber automorphism. The artifact generalizes the latter elementary step, not the former deep one.

The published paper explicitly notes that normal bundles need not exist in general in higher codimension. This is an obstruction to copying that proof; it is not itself a counterexample to connected-sum independence. Local flatness supplies charts, but no general compatible global normal-bundle uniqueness or fiber-preserving transition map is silently inferred.

The pair Alexander formula in Section 4 is correct for a boundary-fixing self-homeomorphism of one product ball. The seam agrees because the boundary is fixed, and the product-gauge displacement is at most 2t, so joint continuity at t = 0 is uniform. Its inverse uses the same formula with the inverse map. These hypotheses are absent for a general chart change. The ordinary sphere-isotopy theorem gives no equator-preserving boundary isotopy by itself.

Similarly, a product description of an ambient annulus does not supply the simultaneous product structure on its distinguished submanifold. Coning a boundary-pair homeomorphism fills a disk; it does not automatically extend over the punctured original summand. The artifact correctly leaves these relative localization and compatibility assertions unresolved.

No smooth derivative argument, PL tameness assumption, or pairwise isotopy-extension theorem stronger than the stated hypotheses is introduced.

## 6. Bibliographic correction

Published reference [17] gives the connected-sum title but the identifier arXiv:2110.03502v1. The [actual record for that identifier](https://arxiv.org/abs/2110.03502) is Livingston's *Intrinsic symmetry groups of links*. The title-matched earlier connected-sum paper is arXiv:2104.03930v1, whose Appendix C contains the higher-codimension discussion. This correction is verified and has no bearing on the validity of the published codimension-two theorem.

Checked PDF hashes:

- Published paper: **0b0e1037b6c086853ada5247834c7e67b3f1aed542574c0e668ef16a841b21f6**
- Earlier connected-sum paper: **da0a11efbaa7daffdbabbab26dbc97f0b2f8d6bbe69e85c76428ce81a9e07c5c**

## 7. Independent bounded controls and final recommendation

There is no submitted numerical checker to reproduce. The reviewer independently wrote a standard-library exact rational checker for nonlinear interval-fiber examples, using b_c(y) = y/(1+c−c|y|) and its explicit inverse. It tests product inverses, contraction endpoints, boundary preservation, zero-section preservation, both collar seams, radial-shell preservation, compact support and the identity endpoint.

All **19,435** assertions passed. These controls cover explicit n = k = 1 examples and the formulas' algebra. They cannot certify a general topological straightening theorem or answer the original question. The all-dimensional conditional proof was checked mathematically above.

Recommended status remains **unsolved, 2/5**, with the conditional lemma and the precise missing relative-straightening step preserved. There is no required correction and no basis for claiming an unrestricted solution, a counterexample, or historical novelty.
