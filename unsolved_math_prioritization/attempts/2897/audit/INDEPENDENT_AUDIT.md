# Independent mathematical audit: Kirby Problem 4.21

Problem ID 2897. Audit date: 2026-10-03.

## Verdict

**The substantive partial results pass. The general problem remains unresolved. One localized mathematical overstatement requires correction; it does not invalidate the sufficient criterion or any claimed positive class or obstruction.**

The eight audited authored artifacts are identified, without modification, by `AUDITED_ARTIFACTS.json`. Their embedded seven-file checksum list also verifies. The original verification program reproduces its recorded output byte-for-byte. An independently written cyclic-shift/block-matrix calculation agrees with every recorded lattice field for n = 1,...,12.

This is an audit of a partial-results investigation, not a proof of the full problem, a claim of mathematical novelty, or a formal verification of four-dimensional topology. Five substantive approaches are present, and none is misrepresented as a general solution. The descriptive status `partial_progress`, together with `full_problem_resolved: false`, is appropriate.

### Correction C1: the puncture's generator condition is automatic

In `PROOF.md`, §4, the sentence asserting that the linking-sphere generator condition is essential to the converse is false under that paragraph's stated manifold hypotheses. The condition is redundant. Here is a proof, using only the same standard tools already employed in the artifact.

Let Z be a compact topological 4-manifold with nonempty boundary, p an interior point, and E = Z minus {p}. Suppose E has the integral homology of S³. Then Z is connected. Excision identifies H_i(Z,E) with the local homology at p, which is Z in degree 4 and zero in every other degree. Thus H₁(Z) = H₂(Z) = 0. The universal coefficient theorem gives H¹(Z; Z/2) = 0, so Z is orientable. Also H₄(Z) = 0 because Z is connected, compact, and has nonempty boundary.

The pair sequence therefore gives

    0 → Z → H₃(E) = Z → H₃(Z) → 0.

The first nonzero arrow is induced by a small linking sphere; it is multiplication by a nonzero integer k. Consequently H₃(Z) is finite. But Poincaré–Lefschetz duality and the universal coefficient theorem give

    H₃(Z) ≅ H¹(Z, ∂Z) ≅ Hom(H₁(Z, ∂Z), Z),

because H₀(Z, ∂Z) = 0. Hence H₃(Z) is torsion-free. It must vanish, and k = ±1. Z is acyclic and the linking sphere is automatically a generator. Its boundary is consequently an integral homology 3-sphere.

**Recommended correction:** replace the claim of essentiality by this automatic-generator observation. The sufficient missing statement can be simplified to finding a compact smooth complement whose punctured other side has the integral homology of S³. The condition is not an independent additional obstruction in this compact-manifold setting.

**Impact:** minor and non-blocking for the substantive results. The artifact's stronger hypothesis still implies its stated conclusion. Quinn's theorem still does not supply the needed finite smooth cross-section or the end-side homology. This correction does not solve the general problem.

### Simplification S1: the compact obstruction already embeds in S⁴

The proof by doubling and surgery in Proposition 6 is valid, but more machinery than necessary. Its X was defined as the exterior of a locally flat slice disk in B⁴. Thus X is already a codimension-zero topological submanifold of B⁴, and hence of the standard closed smooth S⁴. Local flatness and the usual corner rounding give the relevant collared boundary.

Since S⁴ has the desired decomposition, this directly proves the failure of the proposed inheritance argument, in an even simpler positive ambient example. Being a topological codimension-zero submanifold of a smooth manifold does not imply smoothability when its boundary is merely locally flat. No new result or novelty claim is needed for this observation.

## 1. Exact problem and source gate

The full April 2026 author preliminary version of Baykur–Kirby–Ruberman, *K3: A New Problem List in Low-Dimensional Topology*, was checked at printed pp. 206–207. Problem 4.21 asks about a closed topological 4-manifold decomposed into a smoothable submanifold and an acyclic submanifold with common homology-sphere boundary. It does not restrict the question to orientable or simply connected manifolds. Its remarks identify the old number as Kirby 1997 Problem 4.74, record the simply connected positive construction, and give the compact slice-disk-exterior obstruction.

The audit does not replace this primary source by the catalogue page or the short AIM workshop report. The source gate candidly records that the catalogue returned HTTP 403 and the 1997 scan was not retrieved. Those limitations do not prevent checking the exact current problem. The old numbering is properly attributed to K3 rather than asserted from an independent examination of the old scan.

A fresh bounded search for the current number and the defining smoothable/acyclic/homology-sphere phrase returned the 2026 primary question and related work, but no verified later resolution. Search results are not used as a proof of an open-problem status. No stronger completeness claim is justified.

Primary links:

- [K3 author preliminary version, pp. 206–207](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf)
- [Freedman, The topology of four-dimensional manifolds](https://doi.org/10.4310/jdg/1214437136)
- [Quinn, Ends of maps III](https://doi.org/10.4310/jdg/1214437139)
- [Friedl–Hambleton–Melvin–Teichner, version 2](https://arxiv.org/abs/math/0611077v2)
- [Ruberman–Stern, A fake smooth CP² # RP⁴](https://doi.org/10.4310/MRL.1997.v4.n3.a6)

The mathematical source checks used the full relevant statements and proof sections, not only abstracts or search snippets:

- Freedman: pp. 366–371, including Theorem 1.4′ and the complete existence/uniqueness discussion for Theorem 1.5, including the odd-form Arf modification on p. 371.
- Quinn: the handle-straightening statements and argument in §2.2, pp. 505–508, through Corollary 2.2.3. The result supplies a smoothing off a point, including the boundary-relative statement.
- FHMT: Theorem 1.2 and its full §2 proof, and Corollary 1.4 with the full §4 proof/construction on pp. 9–11. The knot figure and the framed-link discussion were also inspected.
- Ruberman–Stern: all four pages, including the displayed star-RP⁴ construction on p. 376, Lemma 2.1, and its Brieskorn-sphere construction on pp. 377–378.

Established deep results used inside these papers remain imported mathematical theorems. The audit does not claim to reconstruct every underlying disc-embedding, classification, smoothing, or gauge-theoretic proof from first principles.

## 2. Positive classes and category checks

### Smoothable manifolds and integral homology 4-spheres

Proposition 1 is correct. In the homology-sphere case, H₄(M; Z) = Z supplies orientation, and the local orientation map to H₄(B⁴,S³) is an isomorphism. The long exact sequence gives an acyclic complement. The chosen ball has a genuine locally flat boundary and the ball, rather than its potentially nonsmoothable complement, is the smoothable piece. Neither simple connectivity nor global smoothability of M is assumed.

### Connected sums

Proposition 2 is correct. The connected sum is performed in smooth coordinate balls on the smoothable sides. Transferring a smooth arc neighborhood attaches a single 1-handle between two distinct components of the acyclic side. This joins components without creating a new first homology class. Mayer–Vietoris, or a homotopy-equivalent union joined by an interval, establishes acyclicity. The boundary is the connected sum of the two integral homology spheres. Boundary collars permit the attachment and corner rounding in the required categories. There is no hidden orientability assumption on the whole ambient manifolds.

### S³ interface

Proposition 3 is correct. The cap on the smoothable side is legitimate because three-dimensional smoothing uniqueness permits a compatible smooth boundary identification; the topological side needs only a topological ball. Mayer–Vietoris gives the homology sphere H. Conversely, puncturing H supplies the acyclic side. In the simply connected case, the free-product fundamental group of N # H forces both summands simply connected, and the topological Poincaré theorem gives H homeomorphic to S⁴. The E₈ example correctly shows why an S³ interface cannot be imposed in general.

### Freedman's scope

The simply connected construction is supported by the actual existence proof, not merely by matching the ordinary intersection form. The smooth 0/2-handlebody has boundary an integral homology sphere because its linking matrix is unimodular. A contractible topological cap kills no unwanted second homology. The odd-form construction really must realize both Kirby–Siebenmann types; the cited Arf-one modification supplies this. Quinn's almost-smoothability removes the historical almost-smooth hypothesis in the quoted classification theorem. There is no extension here to arbitrary fundamental groups or arbitrary equivariant forms.

### Nonorientable example

The star-RP⁴ construction is correctly quoted. The quotient of a smooth homology sphere by a free smooth orientation-preserving involution is a smooth 3-manifold. Its associated nontrivial interval bundle is smooth with boundary the original sphere. A contractible topological cap completes the cited nonorientable manifold. The orientation-preserving involution and the orientation-reversing interval action are consistent with nonorientability of the total space. This establishes the displayed example only.

## 3. Punctured smoothing and homological restrictions

Lemma 4's forward direction is correct: acyclicity forces orientability, duality gives a homology-sphere boundary, local excision gives punctured homology S³, and the relative fundamental class identifies the two degree-three generators. The converse is valid, with the redundant generator assumption corrected as in C1.

Quinn's theorem is not a finite compact-complement theorem. A smooth exhaustion produces smooth boundary levels but no asserted control of the end-side H₁ or H₂. A topological coordinate sphere has the right homology but need not be smooth for the chosen punctured smoothing. The remaining gap is genuine after removal of the redundant condition.

Lemma 5 is correct. Mayer–Vietoris gives the H₁ and H₂ isomorphisms without orientability of M. In the orientable case the fundamental-class boundary map H₄(M) → H₃(Σ) is an isomorphism, giving the H₃ statement. Intersection forms on the free second homology agree under capping by a homology ball. The Euler-characteristic identity is valid, and in fact also follows without orientability. The artifact correctly refuses to infer trivial fundamental group from acyclicity.

## 4. Cyclic covers and the lattice calculation

The displayed matrix matches FHMT. The basis norms are 7, 5, 3 for the first two generator types when n is 1, 2, at least 3 respectively, and 2 for the last two types. Pairing the norm-sum vector w with a basis element gives 5 or 2, exactly the required parity. Its norm is 4n. Therefore w minus 2e₁ is characteristic, of norm 4n minus 8 for n at least 3. Such a norm is impossible in the positive standard diagonal lattice of rank 4n.

The argument is symbolic for all n at least 3. The finite computations are supplements. The independent check uses T = S + Sᵀ, with S the cyclic-shift permutation matrix. In the resulting block matrix

    Lₙ = [ A  B ]
         [ B  2I],

it verifies the integer identity 2A − B² = I. Thus the Schur complement is I/2, certifying positive definiteness and determinant one exactly. This uses a different construction and certificate from the authored Laurent-polynomial expansion and rational elimination.

The cover discussion is also correct. Any homomorphism from π₁(Z) to a finite cyclic group factors through its zero abelianization, so the cover over Z is trivial. The same holds over Σ. Surjectivity from H₁(Y) to H₁(M_L) ensures the lifted complement is connected. Its intersection form is Lₙ, but it has n boundary components. The argument supplies topological acyclic caps, not smooth acyclic caps. Closed smooth diagonalization cannot be applied as though those caps were smooth. Consequently the nonsmoothability theorem is not a counterexample to the decomposition property.

## 5. Compact slice-disk obstruction and closed embedding

FHMT Corollary 1.4 provides a published knot theorem stronger than required: the knots are topologically slice and do not bound smooth disks in any smooth rational homology 4-ball. An integral homology ball would be such a rational ball. The proof does not rely on an inaccessible unpublished construction.

A locally flat proper slice disk has the topological normal-neighborhood and collared-boundary setup needed for its exterior. The zero-framing is the slice-disk framing; the exterior has the integral homology of a circle, with meridian generator, and boundary zero surgery on the knot.

Assuming the compact decomposition, the three-dimensional smoothing compatibility allows the dual handle to be attached in the chosen smoothing of A without changing the relevant knot or surgery slope. This must be the dual handle that reverses the specified zero surgery, not an arbitrary framing of a homologically primitive curve. Its outgoing boundary is S³, and its cocore boundary, after reversal, is the original knot (up to the harmless orientation conventions).

The first relative handle map is multiplication by ±1 on H₁, so it kills H₁ and creates no H₂. The H₃ class persists until the S³ cap kills it. This yields A′ acyclic. The sign reversal in A glued to −A′ is correct: it supplies the orientation-compatible gluing along Σ. In the second gluing, the H₃(Σ) map is an isomorphism, leaving a homology circle. The second dual handle produces a smooth integral homology ball, with a smooth slice cocore, contradicting FHMT. All necessary integral, rather than merely rational, homology statements are valid.

The double-and-surgery proof also survives the audit. The double has H₁ = H₃ = Z and H₂ = 0. Inclusion of the second copy surjects on H₁, so a loop representing the primitive generator can be chosen there. Quinn smoothing away from a point and general position provide a smooth loop and a trivial oriented rank-three normal bundle. Its surgery is disjoint from the first copy. Removing a codimension-three loop does not change the fundamental group, and surgery imposes the loop's normal relation. Thus the new H₁ is zero. The Euler characteristic increases from zero to two. Oriented duality and the universal coefficient theorem force H₃ = 0 and H₂ torsion-free, and Euler characteristic forces its rank to vanish. The result is an integral homology 4-sphere. The simpler direct embedding into S⁴ noted in S1 gives the same conclusion without these steps.

No decomposition of an ambient closed manifold is required to restrict to the selected compact submanifold. Its interface can cross that submanifold's boundary. This is the decisive failure of the inheritance shortcut.

## 6. Reproduction and integrity

- All eight original authored-file SHA-256 values match `AUDITED_ARTIFACTS.json`.
- The original `SHA256SUMS` checks all seven of its listed files successfully.
- Running the original `verify.py` reproduces `verification.json` byte-for-byte; the result is also supplied as `verification.reproduced.json`.
- Running `verify_independently.py` reproduces `independent_verification.json`.
- The two programs agree on all twelve lattice records, including rank, determinant, exact positivity, characteristic parity, both vector norms, and the nonstandardness flag.
- No topology is certified by the numerical checks. The assertions about a primitive chain map and Euler characteristic in the authored program are only arithmetic consistency checks; their geometric inputs require the proofs audited above.

Source-edition SHA-256 fingerprints also match the source gate:

| Source | SHA-256 |
| --- | --- |
| K3 April 2026 author PDF | ae56518166fe38aaaf555c58614329228afe734e743b111badec4060877fa12f |
| Freedman scan | e1f8fa0954129889038b709a41e5583488e8527831351558af176b8326a713c7 |
| Quinn scan | 53791846508aa8b81c218b314522c0209b482af3f62d46d54b6b7ed003d92b29 |
| FHMT v2 | 9f439ae9fd56bfd9d5b984a95c68901bf9bdd7ac3983b7859bdaaefc9c859334 |
| Ruberman–Stern | 5b3151e2cb37c21898e99c371a92f30bc0cf819c145b71c7ddee3538649e0018 |

The source PDFs, whole-book extractions, and page images are not part of this audit deliverable. Bibliographic links and fingerprints identify the primary evidence.

## Final disposition

Accept the substantive partial-result scope, with C1 explicitly attached as a mathematical correction. Do not relabel the closed problem solved, do not infer a closed counterexample from the compact obstruction, and do not treat source access or finite computation as a replacement for the missing general argument. S1 is an optional simplification. The audited authored files remain unchanged.
