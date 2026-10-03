# Independent AI mathematical audit: ID 2580 / KOU-21.71

Audit date: 3 October 2026 UTC.

## Decision

**PASS as an unsolved partial-results package, with five substantive attempts and no claimed resolution.** No mandatory mathematical repair was found in the frozen author files. The unrestricted existence question is still unanswered by this work. This audit is not a sixth attempt, an originality certificate, or external human peer review.

The correct publication classification, if publication is separately authorized, remains **unsolved, 5/5**. Any presentation as a solution, counterexample satisfying both FL hypotheses, or proof of universal equality would be **HOLD / unsupported**.

The ten original author files were unchanged during review. Their SHA-256 hashes are recorded in `AUTHOR_MANIFEST.json`. The mathematical report and independent verification controls are included here.

## Scope and primary identity

The inspected source is the October 2026 Kourovka Notebook, printed page 187 and one-based PDF page 187. I visually inspected the supplied page image and independently extracted the same page from the supplied complete PDF. Its SHA-256 is:

`31baec1b36ec3a956e787355eccfffa2e89df5b1fe31b22a3123377d8103baab`.

Problem 21.71 is D. Kielak's question about a group admitting finite, finitely generated **free** resolutions over two fields and having different ordinary homological Euler characteristics. The neighboring 21.70 is the Poincaré-duality-over-all-fields question; it has not been substituted here. The inspected 21.71 entry is unmarked and has no attached solution comment.

The official October revision announcement was checked live. The primary PDF could not be freshly retrieved during review, so the page-level verification used the previously downloaded primary PDF. Dated source status and bounded literature searches do not certify absence of unindexed or later work.

Primary links:
- https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt.pdf
- https://kourovkanotebookorg.wordpress.com/2026/09/30/october-2026-update-for-the-21st-edition/

## Attempt 1: coefficient comparison — PASS

1. The identity between ordinary homological Euler characteristic and alternating free ranks is valid. Applying the trivial right module to a finite free resolution produces a bounded finite-dimensional vector-space complex. It computes group homology; it is not asserted to remain an exact resolution after augmentation. Euler–Poincaré supplies the equality.
2. Same-characteristic invariance is correctly proved at the bar-complex level over the prime field. Field extension is exact and faithful and preserves the dimension of a vector space when dimension is measured over the corresponding fields, even before finiteness is known. The FL hypothesis supplies finite support and finite dimensions. There is no FL descent claim.
3. The cited non-descent example is real. Leary's 2002 publisher abstract expressly states that the paper constructs groups FL over the complex numbers but not over the rationals. The citation is relevant even though its title concerns a different Euler-class subject; it is used only for non-descent, not to substitute the adjacent Notebook problem.
4. A common bounded finite-free complex whose two fibers resolve the trivial modules forces equality. This is conditional, and the missing common complex is not assumed into existence.
5. Integral FL base change is justified: the augmented resolution splits as abelian groups. Equivalently, its successive kernels are free abelian, so tensoring with arbitrary fields preserves the required short exact sequences. The finite free, cocompact, finite-dimensional cellular model is likewise a valid sufficient common model when it is acyclic over each field.
6. Restriction to a subgroup of order p gives a valid obstruction to FL in characteristic p. Finite generation of the restricted terms is unnecessary for the finite-projective-dimension contradiction. The text correctly stops short of claiming torsion-freeness.

Source verified: Leary, *The Euler class of a Poincaré duality group*, DOI 10.1017/S0013091500001164, publisher abstract at https://www.cambridge.org/core/journals/proceedings-of-the-edinburgh-mathematical-society/article/euler-class-of-a-poincare-duality-group/297EAAF2F9D4ED283EDB57ABD657DB9A .

## Attempt 2: universal coefficients and localization — PASS

Write A_i = H_i(G; Z). The universal-coefficient short exact sequence used in the text is correct for the free integral bar complex:

0 → A_i/pA_i → H_i(G; F_p) → A_{i-1}[p] → 0.

The finiteness argument handles a potentially serious endpoint issue correctly. Finite-dimensional, finitely supported mod-p homology bounds A_i/pA_i through H_i and A_i[p] through H_{i+1}. Hence both families are eventually zero and finite dimensional. Reindexing the Tor term is therefore legitimate and gives the stated alternating defect with the correct minus sign. No infinite alternating series is silently manipulated.

The positive-positive formula requires no rational rank. The rational-comparison formula is explicitly conditioned on finite-dimensional, finitely supported rational homology. The warning that two modular characteristics need not see rational-vector-space summands is appropriate.

If every A_i is finitely generated, the torsion summands in A_i/pA_i and A_i[p] have equal dimensions, leaving only integral free rank. Eventual vanishing of field homology forces eventual vanishing of those ranks. Thus equality follows without a finite integral resolution. Integral FP-infinity is a sufficient source of degreewise finite generation, not an inferred consequence of two-field FL.

The necessity of non-finitely-generated integral homology in some degree at least 2 is valid. The augmentation-ideal argument establishes FP1 over a nonzero field implies finite generation of G: finite supports generate a subgroup H; I = FG I_H implies the coset permutation module FG/FG I_H has dimension one, hence H = G. Consequently H_0 and H_1 over Z are finitely generated. This is a necessary obstruction, not a sufficiency claim or a realization theorem.

The additive group Z[1/p] is an authentic near-counterexample. Group homology commutes with its filtered direct limit of cyclic groups. H_1 is the direct limit under multiplication by p, equal to Q in rational characteristic and zero in characteristic p, while higher homology vanishes. Therefore the ordinary Euler values 0 and 1 are correct. The group is not finitely generated and fails FP1 over every nonzero field, so it cannot answer the target question.

Kropholler's cited examples really are FP2 over Q and every prime field but not FP2 over Z. The frozen notes make only the warranted cautionary use of that result and do not upgrade it to FL. Source: https://arxiv.org/abs/2102.13509 , Theorem 1.3 / 6.1 in the supplied full text.

## Attempt 3: cyclic repair — PASS

For p prime, multiplication by p is an automorphism of Z[1/p], and the semidirect product with Z has the displayed BS(1,p) presentation. The finite graph-of-spaces presentation complex is aspherical, with injective edge maps, so its cellular universal-cover chains give integral FL.

The trivial-coefficient boundary is the relator exponent-sum column (1-p, 0). Its rank is one unless the positive characteristic divides p-1. The two Betti vectors are consequently (1,1,0) and (1,2,1), both of Euler characteristic zero. The integral H_2 statement and the mod-q H_2 Tor explanation agree. In particular, characteristic p itself does not divide p-1.

For 1 → N → G → Z → 1, the extension splits because a lift of the generator defines a section. The two-column homological LHS spectral sequence collapses; there are no higher differentials that can land in another nonzero column. Its filtration gives the displayed kernel/cokernel dimension formula. Finite-dimensionality equates kernel and cokernel dimensions; bounded homological support makes the alternating sum finite. Both hypotheses are present. The conclusion is correctly applied separately in each field and does not need FL for N.

The product and free-product observations are also correct. The former obeys the field Künneth Euler formula under the stated homological finiteness, and projection/retraction obstructs using either operation to repair finite generation of Z[1/p]. No conclusion about arbitrary embeddings is inferred.

## Attempt 4: ordinary Bestvina–Brady groups — PASS

The finite, nonempty, flag hypothesis is stated before the computation. Flagness is essential for identifying the cyclic cover of the Salvetti complex with a classifying space for the kernel. Nonemptiness handles H_0 and the augmented degree -1 term.

The chain complex and attribution agree with Leary–Saadetoglu Proposition 6 and Corollary 7 in the supplied full text. Splitting the augmented simplicial chain complex over a field gives boundary, reduced-homology, and complementary summands. Multiplication by 1-t is injective in F[t,t^{-1}], has quotient F, and the reduced-homology summands retain a full Laurent-polynomial factor. This yields exactly the text's vector-space decomposition, including H_0 = F.

Thus nonzero reduced link homology forces infinite-dimensional ordinary group homology one degree higher. This proves the necessary implication FL(F) ⇒ F-acyclicity. No converse finiteness theorem is needed or silently used. When L is F-acyclic, the finite boundary ranks satisfy f_j = z_j + z_{j-1}, with z_{-1}=1 and z_d=0. The stated face-count Euler formula follows, with the correct indexing and sign. It excludes the stated ordinary finite-link family, not all constructions with Bestvina–Brady terminology.

Independent checks confirm the six-vertex input has ten triangles, all fifteen edges, and the expected integral 2-torsion: the nonzero Smith invariants of its d_2 are nine 1s and one 2. Its barycentric subdivision is flag with face vector (31,90,60). Its reduced Betti vectors are zero in characteristics 0,3,5 and (0,1,1) in characteristic 2. Accordingly the kernel has finite ordinary Betti vector (1,30,60), Euler value 31 in the first fields, and infinite-dimensional H_2 and H_3 in characteristic 2. The latter fails FL; it is not a positive example.

Attribution nuance: the cited paper's Corollary 9 states its Euler formula over Q. The frozen notes validly extend the calculation to an arbitrary acyclic field using their own displayed field-linear argument; they do not need a stronger quoted Corollary 9. Source: https://arxiv.org/abs/0711.5018 .

## Attempt 5: product-ring synchronization — PASS

Let S=(F_1×F_2)G ≅ F_1G×F_2G. Modules over S are pairs; exactness and finite generation are componentwise. The paired resolution has terms (F_1G)^{a_i}×(F_2G)^{b_i}, each a finite sum of the two central-idempotent projectives. It therefore gives a finite resolution by finitely generated projectives.

It does not by itself give a free resolution. The rank obstruction is genuine: augmenting a hypothetical isomorphism of a paired term with S^n gives an isomorphism F_1^{a_i}×F_2^{b_i} ≅ F_1^n×F_2^n, forcing a_i=b_i=n. This also supplies the required invariant-basis-number justification; no unproved group-ring rank or cancellation property is used.

Necessity of equality follows by taking exact factor projections of a free S-resolution. For sufficiency, set δ_i=a_i-b_i and s_i=δ_i-s_{i-1}, with s_{-1}=0. Equality of Euler sums is exactly s_N=0. Adding max(-s_i,0) identity disks to P and max(s_i,0) identity disks to Q changes the degree-i rank difference by -s_i-s_{i-1}. The result is zero in every degree, including the bottom and top endpoints. Negative s_i causes no negative rank, since each side receives a nonnegative number of disks. The degree-(1,0) disk has zero augmentation on its new degree-zero summand and remains contractible as an augmented addition. The paired differential on synchronized modules is a free S-resolution. Unequal lengths are harmless after zero-padding; the N=0 case needs no disks.

This is constructive sufficiency from two existing resolutions and equality of their Euler sums. It assumes neither a chain map across characteristics nor a common resolution in advance. Separate FL plus unequal Euler sums would instead yield a finite projective resolution with nonzero free-rank obstruction. Establishing that this situation cannot occur for trivial group modules is precisely what has not been proved.

The Euler class expression and augmentation detection are correct in K_0(S)/Z[S]. Under augmentation, the class maps to (χ_1,χ_2) modulo the diagonal in K_0(F_1×F_2) ≅ Z², which is nonzero exactly when χ_1≠χ_2. There is no hidden inference that every projective with vanishing rank difference is free: the constructive disk argument only pairs originally free component modules.

The connected-coefficient-ring paragraph is a valid conditional statement. Augmentation takes finitely generated projectives over AG to finitely generated projectives over A. Their ranks are locally constant, hence constant on a connected spectrum. Applicable exact fiber resolutions then have equal Euler characteristics. No such connected-ring resolution is obtained from the original assumptions.

## Exact computational controls

The author's script was rerun unchanged and produced JSON semantically identical to the frozen `verification.json`:

- 6 simplicial examples, each over Q, F_2, F_3, F_5;
- 35 Baumslag–Solitar parameter/characteristic cases;
- 8,092 ordered pairs of length-four rank vectors with entries in {0,1,2,3} and equal alternating sums.

An independent audit script separately reconstructed barycentric chains as vertex < edge < face, checked every integer boundary composition equals zero, computed rational/modular ranks with SymPy DomainMatrix over QQ/GF(p), checked the flag condition, and calculated the original Smith invariants. The rank-pair count was independently recovered as the sum of squares of the Euler-value histogram; disk stabilization was checked using the closed alternating-prefix formula rather than the author's recurrence. BS outcomes were checked by divisibility rather than Gaussian elimination.

All controls passed. They validate these explicit examples and algebraic bookkeeping. They do not prove FL of arbitrary groups, certify an unrestricted comparison theorem, or constitute an exhaustive counterexample search.

Reproduce the supplemental controls with:

`python3 audit/independent_field_euler_checks.py`

The supplemental script requires SymPy; the frozen author's script still requires only the Python standard library.

## Repairs, cautions, and remaining gap

Mandatory mathematical repairs: **none**.

Optional clarity improvements, not blockers:
1. Define FP(R) at its first use in attempt 5 as a finite resolution by finitely generated projectives, to avoid readers using FP as shorthand for FP-infinity.
2. If later calling the displayed obstruction a “reduced K_0” class, specify K_0(S)/Z[S]. Do not replace this by the relative quotient modulo the entire image of K_0(F_1×F_2), which would kill both idempotent classes and lose the obstruction.
3. Keep the finite-support hypothesis whenever abbreviating the cyclic-extension result as “finite homology,” and retain the finite/nonempty/flag scope of the ordinary Bestvina–Brady exclusion.
4. Preserve the distinction between finite ordinary Betti numbers and FL, particularly in discussing the localization and torsion-sensitive examples.

The substantive open gap remains exactly as stated in the frozen package: either construct a group with both field-FL hypotheses and a nonzero higher integral-homology Euler defect, or prove a comparison principle forbidding that defect. The five attempts provide neither. No sixth attempt was undertaken during this audit.
