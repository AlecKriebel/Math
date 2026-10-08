# Independent mathematical and source-scope audit

## Decision

**Accept the corrected packet as an unsolved, five-approach research result. Do not accept it as a proof or counterexample to Problem 1C.** The original frozen packet is preserved. The corrected packet fixes one false topological justification and makes two necessary analytic/path hypotheses explicit. None of these repairs changes the unsolved conclusion or the five-turn count.

Target: rank 1011, problem 10800003, catalog AMR-107-0003. Review date: 2026-10-08 UTC. This is an independent AI-assisted audit, not human peer review, formal verification, an exhaustive literature search, or a novelty certification.

The corrected proof is `corrected/author/PROOF_AND_STATUS.md`. `CORRECTIONS.patch` reconstructs all changed bytes from the original packet, including the corrected manifest and bootstrap anchor. Only the mathematical proof changes among the ten payload files.

## 1. Controlling question and source scope

The published target was checked in V. A. Vassiliev, *A Few Problems on Monodromy and Discriminants*, Arnold Mathematical Journal 1 (2015), pp.202–203, especially Problem 1C and its immediately preceding paragraph. The collision is in a fixed small miniversal parameter neighborhood, from a specified morsification, along the specified two vanishing paths, with the other critical values fixed. A global family realizing an abstract surgery or the same topological component does not automatically realize this path from this lift. The original source itself distinguishes local continuation from unrestricted travel in a canonical parabolic parameter space. [Official article](https://amj.math.stonybrook.edu/html-articles/Files-2015-2024/15-11/), [published PDF](https://armj.math.stonybrook.edu/pdf-Springer-final/015-0011-9.pdf).

The packet preserves these quantifiers. Its conclusion is that its own methods leave the problem unresolved. It does not establish worldwide current openness.

The following contemporary primary statements were separately inspected:

- **Quartic/X9.** Proposition 2 and its proof in *Isotopy classification of Morse polynomials of degree four on R²*, arXiv:2311.11113v12, pp.12–14, do realize the allowed real elementary surgeries. The proof explicitly holds seven values fixed, works in `(C minus {−1,1}) × C^8`, and invokes Jaworski's Proposition 2 to prevent the modulus reaching the excluded boundary. This is substantial positive evidence, not merely an experimental claim. The conclusion is a global parameter-space path; the compact modulus region is not asserted to be an arbitrary neighborhood of the original modulus. [Versioned primary paper](https://arxiv.org/abs/2311.11113v12).
- **J10.** Remark 4, pp.8–9, and Proposition 7, p.10, in *Complements of caustics of the real J10 singularities*, arXiv:2510.03883v5, attribute realizability to the parabolic theory and transfer the quartic argument to the canonical complex J10 family. The stated output is a real elementary-surgery path in the polynomial spaces Φ1 or Φ3. Neither the proposition nor the inspected argument supplies the general small-neighborhood complex conclusion of Problem 1C. [Versioned primary paper](https://arxiv.org/abs/2510.03883v5).
- **Parabolic discriminants.** Section 1.2, pp.4–5, in *Complements of discriminants of real parabolic function singularities. II*, arXiv:2512.12738v6, explains why global component classifications represent local components near every member of the parabolic class: dilations shrink lower-weight terms, and equisingularity transfers the component description along the modulus. This is a component-realization statement. It need not preserve a particular starting lift, its numerical fixed values, or its prescribed collision path. [Versioned primary paper](https://arxiv.org/abs/2512.12738v6).

The weighted-scaling objection is correct: a coefficient of weight q changes by ρ^(d−q). The X9 monomial x²y² has weight 4=d; the J10 monomial xy⁴ has weight 6=d for weights (2,1). Such coefficients are unchanged. Scaling alone therefore cannot shrink a modulus excursion back to its initial modulus. This rejects a proposed proof transfer, not the existence of a lift.

All six supplied external source files were independently byte-checked against the frozen source metadata. Target p.203, quartic p.13, and J10 Proposition 7 p.10 were also visually inspected; the other cited sections were read as extracted text. Live retrieval independently confirmed the official target HTML and the quartic v12 version page. The J10 v5 and parabolic v6 abstract fetches returned cache misses; their local PDF version labels and byte pins were checked. No stronger independent latest-version claim is made. The original Jaworski 1988 proof was not independently inspected. Its theorem remains an attributed dependency rather than a theorem reproved by this audit.

## 2. Route-by-route mathematical assessment

### Route 1: local endpoint classification

**Accepted with the stated endpoint and representative hypotheses.** The critical scheme must be finite over the chosen small parameter representative and conserve total length μ. A path on which precisely two of the μ critical values coalesce has collision multiplicity two. All other values have multiplicity one. The collision fiber therefore has either two length-one Morse points or one length-two local Jacobian algebra.

For the latter, its maximal ideal has cotangent dimension equal to Hessian corank. Corank at least two would give algebra length at least three. The splitting lemma reduces corank one to a one-variable germ whose derivative has a zero of order two, hence an A2 singularity. This gives the claimed A1+A1/A2 alternatives.

The product-versality step is valid after shrinking the representative so that the Kodaira–Spencer basis remains a basis of the finite flat critical algebra. It is not justified by dimension counting alone. The written basis-persistence explanation supplies the missing reason. At the two endpoints the value coordinates or the A2 parameters are independent of the other Morse value coordinates, so those other values can be kept exactly fixed locally.

In the A2 model, critical points ±s at a=s² have values b∓2s³ and squared difference 16a³. A branch along a punctured collision interval extends continuously to a=0. Maxwell ordered value coordinates are regular, while passage to the unordered pair introduces the square. Both local calculations are correct. They provide no path from an arbitrary initial lift to these endpoint charts.

### Route 2: symmetric rank-two reflections

**Accepted in precisely the normalized symmetric convention stated.** From `(a,a)=(b,b)=−2` and `(a,b)=m`, the two reflection matrices and their product are correct. The determinant, trace and characteristic-polynomial computations imply:

- m=0: product −I, order 2;
- |m|=1: nonidentity product satisfying P²+P+I=0, order 3;
- |m|=2: P=I+N, N nonzero and N²=0, so P^k=I+kN;
- |m|≥3: real reciprocal eigenvalues, one greater than 1.

Thus finite order occurs exactly for |m|≤1. The corresponding Gram form is negative definite exactly in these cases. The written all-integer proof is stronger than the finite test range. Independent tests include |m| up to 25 and 10^6, but the all-integer conclusion comes from the proof, not sampling.

This is a complete calculation for this displayed pair. It is not a classification of actual singularity deformations, a geometric realization theorem, or a proof of nonescape. The parity warning matters: plane-curve first-homology intersection is alternating and its Picard–Lefschetz operators are transvections. No unsupported suspension/parity substitution is used in the geometric route. Infinite order with a nontrivial unipotent part is also not, by itself, excluded by quasi-unipotence.

### Route 3: plane-curve geometric intersection

**Accepted as a conditional endpoint obstruction after the path clarification and topological repair.** A valid identification must use the originally specified pair of vanishing paths, continued compatibly with the allowed collision. Near the endpoint these paths have the two local pieces inside a collision disk and a common continuation to a regular reference fiber. Pulling the pair back by a common fiber diffeomorphism preserves their simultaneous isotopy classes and geometric intersection. An independent Hurwitz move around another critical value would change this identification and is excluded.

The Maxwell pair can be represented in disjoint Morse balls, giving geometric intersection zero. The local A2 pair has one intersection in its punctured-torus fiber. After embedding in the ambient fiber, the intersection cannot be reduced below one because its algebraic intersection has absolute value one. Thus the two stated necessary conditions follow for collision-compatible paths. This does not prove the compatibility or accessibility of an arbitrary pair after changing its paths.

The original text incorrectly asserted that every separating curve on the bordered surface is null-homologous. A separating curve can be homologous to a nonzero sum of boundary curves. The correct statement is that its homology class has zero algebraic intersection with every closed class. The Dehn-twist transvection therefore acts trivially on H1. The patch makes this correction explicitly.

Consequently `[T_c(a)]=[a]` is still true. The standard single-twist geometric formula `i(a,T_c(a))=i(a,c)^2` supplies the advertised positive geometric intersection when a meets c. Its annulus/bigon proof is an ordinary surface-topology argument, not something established by a homology matrix calculation. The packet openly treats this as a foundational geometric input.

Most importantly, the equal homology classes are dependent. They cannot be two members of the distinguished μ-element basis of Milnor homology. The proposed example remains correctly rejected. No actual isolated germ with an admissible distinguished pair violating the geometric condition is supplied.

### Route 4: inverse critical-value flow

**Accepted after stating the regularity and initial-value hypotheses explicitly.** At a Morse fiber, differentiation of `F(p_i(λ),λ)` leaves only parameter derivatives because the spatial gradient vanishes. Evaluation at the μ reduced critical points identifies the Jacobian algebra with C^μ. The local miniversal Kodaira–Spencer map is an isomorphism, so the evaluation matrix is invertible and gives the local differential equation.

The corrected theorem requires a continuous labelled value path on [0,1], C1 on each compact subinterval of [0,1), beginning at the critical values of λ0. It also requires r>0 and a nonnegative Lebesgue-integrable dominating speed function with integral strictly less than r. For the target specialization, the other μ−2 coordinates are constant. Merely mentioning a derivative without path regularity is insufficient for the integral argument; singular continuous motion is not controlled by an almost-everywhere zero derivative.

Under the corrected hypotheses, integrating on each compact interval bounds displacement strictly inside the ball. Integrability makes the lift Cauchy at any finite maximal time. At a maximal time less than 1 the limiting critical values are distinct; conservation of total multiplicity then makes the limit Morse, and local invertibility extends the lift. At time 1 the Cauchy limit is still inside the ball and realizes the prescribed limiting multiset. These are the claimed conclusions.

The A2 inverse derivative has the correct |d|^(−1/3) singularity for linear value-difference approach, hence integrable speed. The bound is a conditional nonescape criterion. Nothing in the packet derives it from the integer intersection number.

### Route 5: separable X9 slice and its repair

**Accepted, including the rejection of the slice as a target counterexample.** In the separable family, the nine values are `P_i+Q_j`. If only two labelled entries change while seven stay fixed, one of the three rows is unchanged. This forces all column increments to agree, so a nonzero changed row has three nonzero entries, contradicting support at most two. This is an exact path restriction while the three-by-three Morse labeling persists.

The size assumption is real: a two-by-two additive matrix can have exactly two nonzero entries. An independent positive scope control checks this rather than extrapolating the three-by-three argument indiscriminately.

For the displayed depressed quartics, the critical equations, nonzero Hessians, and nine distinct values are correct. The tensor evaluation matrix for monomials x^r y^s, 0≤r,s≤2, has exact determinant 34,012,224,000. Tensor Lagrange coefficients give its exact inverse. Thus the full miniversal tangent space permits an arbitrary infinitesimal velocity of the nine values, including changing just the selected two with seven zeros. The restricted-slice obstruction vanishes already at first order.

This is a valid nonsimple test, not a proof of continuation. The original unscaled fixture need not lie near the original germ; weighted scaling can place such a fixture nearby but does not prove that an unknown collision path remains nearby. The packet states both limitations.

## 3. Executable verification and adversarial controls

The original author verifier remains unchanged. Its authenticated diagnostic output reports 390 exact finite/scope checks. It runs without `assert`, third-party packages, or source-file access in portable mode. The bootstrap authenticates the ten-file inventory and expected output before accepting. The independently supplied original manifest and bootstrap pins both matched.

The independent audit code does not import the author's verifier or mathematical helper functions. It uses a separate Bareiss determinant implementation, basis-action reflection construction, exact Gaussian-rational cubic cases, tensor interpolation coefficients, sparse-support minors, a nonzero boundary-radical model, and exact dyadic cusp-approach identities. It performs **405 exact checks**, identically in normal, `-O`, and `-OO` modes.

`INDEPENDENT_CONTROLS.json` records **115 passing matrix cases** across those three modes. Coverage includes original and corrected direct verifiers and bootstraps; disposable semantic mutations; duplicate keys, nonfinite/overflow numbers, invalid UTF-8, booleans masquerading as integers, wrong catalog/rank/turn/mechanism fields, repeated rational inputs and wrong weights; symlinks, FIFOs, unexpected directories and writable modes; altered verifier, forged manifest and substituted bootstrap; and exact patch reconstruction.

The read-only tests run as actual UID 1000. Both creating a new file and appending to an existing payload file are denied in complete mode-0555/0444 copies. Both original and corrected bootstraps succeed there. All frozen original and corrected bytes and modes remain unchanged, and no hostile sentinel is created.

A deliberate boundary control alters a source-narrative field. The direct portable verifier accepts it, as expected; the authenticated bootstrap rejects the changed bytes. Therefore neither direct diagnostics nor JSON syntax validation proves source-description truth. Manual source review and byte authentication have separate roles. The audit does not claim race resistance, a network-isolated sandbox, or safety for arbitrary untrusted code.

The author's separately reported terminal matrix contains 120 cases, with 6 expected acceptances and 114 expected rejections, across the same optimization modes. Its source-byte run reports 396 checks, including six external byte comparisons. These corroborate but do not replace this audit's independent controls. The audit independently repeated the six source comparisons in `SOURCE_CHECK.json`.

## 4. Corrections and trust anchors

Three narrow proof changes were applied to a separate corrected packet:

1. Collision-compatible common path transport is explicit; independent Hurwitz changes are excluded.
2. The separating-curve justification uses the intersection radical, not a false blanket assertion of null homology on bordered surfaces.
3. The continuation theorem states regularity, initial matching, positive radius, integrable domination, and fixed-other-values specialization.

Original manifest SHA-256:
`90f41824fce3c028993e1dcd12651dbeb86c8b2728527e61052da9b54c2e33a7`

Original bootstrap SHA-256:
`747e0a67d88e4adb8818077394a132f80b0c8f30ed5c5b1877ea536708ab624f`

Corrected manifest SHA-256:
`9ddef9ad585717ca652952fddceef1d3cf0f753f2e23c59a5cdc581ff92e5850`

Corrected bootstrap SHA-256:
`e75b15d966850e2097412032b18c243cd068aa7750d20191121236671802a161`

Corrected proof SHA-256:
`23c088a87ef91827d94ca2aee040892c46a2492166901810586d75c49669df41`

The patch was applied to a disposable original copy and reproduced every corrected payload and freeze file byte-for-byte. Original trust anchors were never rewritten.

## 5. Final acceptance boundary

The five routes use distinct mathematical mechanisms and each reaches a concrete result or a specifically located obstruction to the attempted proof. Retrieval, software tests, freezing and this review are not additional mathematical turns. Accept **unsolved, 5/5** for this packet.

The unresolved target step is still either an a priori nonescape/access theorem for every permitted actual distinguished pair in the prescribed neighborhood, or a genuine isolated singularity and specified pair/path providing a counterexample. The packet provides neither. The rejected homologous surface pair and nonversal separable slice do not fill that gap.

This audit does not independently rerun the remote duplicate-search gate or authenticate the full external catalog datasets; their retained metadata is byte-bound but remains outside this mathematical/source audit. No source PDFs, extracted source text, screenshots, dataset contents, or private coordination material are included in the audit deliverables. No remote write was performed.
