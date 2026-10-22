# Independent adversarial topology audit: PR #1102

- Problem: 30006658 / OWR-14299915-021, Greenlees Question 2.2.
- Review checkpoint: 2026-10-17 16:31 UTC / 2026-10-17 09:31 America/Los_Angeles.
- Assigned review-family completion: **100%**. This percentage concerns this topology/mechanism audit, not the separate priority and publication program.
- Verdict: **PASS for the full stated mathematical theorem**, conditional only on the explicitly cited established primary results. No necessary mathematical repair, hidden orientability hypothesis, unsupported equivalent reformulation, or counterexample was found.
- Strongest verified result: for every compact Lie group G, field k of characteristic p, and X=(BG)^∧_p, if H_*(ΩX;k) has infinite total dimension then every R-linear map M→R from an object of Loc_R(k) induces zero on homology, where R=C_*(ΩX;k). Non-p-nilpotence of π_0G implies that infinite-dimensional hypothesis and gives precisely the original question's conclusion.
- Exact remaining gap in this review family: **none identified**. Novelty, present openness, authorship/metadata, final typesetting, and complete submission-package verification are outside this assignment and are not certified here.

## Independence and record integrity

The authored MATHEMATICAL_REPORT.md was read first. This reviewer then reconstructed the mechanism against original sources and wrote [INDEPENDENT_DERIVATION.md](INDEPENDENT_DERIVATION.md) before consulting any earlier mathematical audit. The earlier MATHEMATICAL_AUDIT.md, ACCEPTANCE.json, and SOURCE_REVIEW.md have **not been read at all** in this review. SOURCE_METADATA.json was opened for source URLs and bibliographic locators; it contains some earlier inspection summaries, a limited exposure recorded in the independent checkpoint. No earlier audit's proof reasoning or verdict was used.

Fresh primary-source downloads have byte counts, hashes, and retrieval timestamps in [sources/RECEIPTS.json](sources/RECEIPTS.json). Full downloaded source bodies and local text extractions are excluded by sources/.gitignore: they are reading copies, not original research artifacts to redistribute in a preprint package.

## 1. Exact target and conventions

The official [Oberwolfach Report 9/2026](https://ems.press/content/serial-article-files/53607?nt=1), printed pp. 592–595, was checked directly, including Question 2.2 on p. 594 and the notation paragraph on p. 593. It asks whether the map on all homotopy groups of Γ_k C_*(ΩBG_p)→C_*(ΩBG_p) vanishes for positive-dimensional compact Lie groups with non-p-nilpotent π_0G. The notation explicitly means the **Bousfield–Kan p-completion of BG before looping**, not chains on G or the ordinary group ring. Its coefficient convention is a field of characteristic p.

The surrounding duality theorem assumes an orientable adjoint representation, but Question 2.2 itself does not impose that restriction in its displayed wording. The submitted theorem handles the literal unrestricted question, and even handles dimension zero. Its proof does not identify the cellularization with an untwisted dual and therefore does not silently import the orientability assumption of the surrounding theorem.

The target is vanishing on homotopy groups, not nullhomotopy in D(R). The report makes that distinction correctly. No argument about vanishing homotopy is promoted to equality of morphisms.

## 2. Independent abstract reconstruction

Let A→k be an augmented differential graded k-algebra, k a field, and suppose K is a proxy in the following precise sense:

1. K∈thick_A(A), so K is compact in D(A).
2. K∈thick_A(k), so its underlying k-complex has finite-dimensional **total** homology.
3. k∈Loc_A(K), so Loc_A(K)=Loc_A(k).

The forgetful functor to D(k) preserves finite sums, shifts, cones, and retracts. Finite total homology is preserved by these operations. Thus every P∈thick_A(K), not merely K, has finite total homology. No boundedness assumption on A, on End_A(K), or on all of M is involved.

### 2.1 Compact approximation is valid

Put E=REnd_A(K). The compact-generator Morita equivalence is

D(E^op) ≃ Loc_A(K),    N ↦ N⊗_E^L K.

This is the small-generator theorem with K substituted for the generator denoted k in DGI. That substitution is legitimate for an arbitrary module K: DGI's proof of Theorem 4.10 itself applies Theorem 4.9 to the pair (R,K). It does not require K to be an augmented algebra or the original residue field to be compact.

For an arbitrary, possibly unbounded E-module N, take a semi-free resolution F. Choose a well-order of the semi-free generators such that the differential of a generator is a finite E-linear combination of earlier generators. For a finite selection of generators, form the closure under these finitely many differential dependencies. That closure is finite: otherwise its finite-branching dependency tree would have an infinite branch by König's lemma, contradicting strict descent in a well-order. The finite closed selections form a filtered poset under unions. They give finite semi-free submodules F_i, whose union is F. Every inclusion F_i→F_j has semi-free quotient: order the remaining finitely many generators by their original order. Thus the diagram is cofibrant in the relevant sense and its union computes its filtered homotopy colimit. Equivalently, filtered colimits of dg modules are exact, so this ordinary filtered union represents the derived colimit.

Every F_i is perfect over E. Tensoring with K preserves homotopy colimits and takes F_i into thick_A(K). Consequently every M∈Loc_A(k) admits

M ≃ hocolim_i P_i,    P_i∈thick_A(K).

There is an independent source cross-check: [Briggs–Iyengar–Stevenson, *Proxy-small objects present compactly generated categories*](https://sunsite3.icm.edu.pl/packages/EMIS/journals/NYJM/j/2025/31-26p.pdf), printed p. 703 (Ind-completion discussion after Definition 2.1) and p. 709 (proof of Lemma 4.1), uses exactly filtered-perfect approximation and tensoring. This verifies the relevant machinery; it does not establish novelty of the submitted result.

### 2.2 Individual homotopy classes factor through a finite stage

For x∈H_n(M), filtered colimits commute with homology, so x is the image of some y∈H_n(P_i). In module-spectrum language, Σ^n A is compact and its maps into a filtered homotopy colimit factor through a stage. This is a factorization of a **class**, which is exactly what is needed. No assertion is made that M or an arbitrary map out of M factors through one finite stage.

Given an A-linear f:M→A, the composite P_i→M→A has homology image I that is:

- a graded left ideal in H_*(A), by H_*(A)-linearity into the regular module;
- finite-dimensional over k, as the image of finite total H_*(P_i).

An infinite-dimensional graded Hopf algebra has no nonzero finite-dimensional graded one-sided ideal. Applying that fact gives I=0, hence f_*(x)=0. Since x and n were arbitrary, H_*(f)=0 in every degree.

The report's graded-sign repair is legitimate: in characteristic two the sign disappears; otherwise parity bosonization makes an ordinary Hopf algebra with a finite-dimensional ideal I#kC_2. No connectedness or bijective-antipode hypothesis is required for the finite-ideal theorem used here. This reviewer also checked the ordinary finite-ideal argument in the report: the coideal enlargement J is finite-dimensional, contains I, is a right ideal by the stated antipode identity, and is a Hopf submodule. The Hopf-module theorem forces a nonzero coinvariant and then finite dimension of the full algebra. The left-ideal conclusion follows through op/cop. The topology audit does not rest on falsely ignoring Koszul signs.

## 3. DGI hypotheses: all compact Lie groups, including nonnilpotent actions

The primary [Dwyer–Greenlees–Iyengar manuscript](https://arxiv.org/pdf/math/0510247), Definitions 4.6 and 4.14, Remark 4.8, Theorems 4.9–4.10, Proposition 4.17, and §§4.22, 5.5–5.7, was inspected directly. The [publisher-version mirror](https://www.maths.ed.ac.uk/~v1ranick/papers/dwgriy.pdf) was successfully downloaded and independently inspected at the same locators, especially Theorem 4.9 and the application to (R,K) in the proof of Theorem 4.10 (pp. 376–377), Proposition 4.17 (p. 378), §4.22 (p. 380), and §5.7 (p. 382). The downloaded publisher version has SHA-256 5d7c5ab3b5c354776f217c8cbcf9428f99ddafb6644b13a16828fbb92764c253; its detailed retrieval record is in the receipts. The important checks are these:

- §5.7 starts with **any compact Lie group G**, explicitly including finite groups, k=F_p, and X the Bousfield–Kan p-completion of BG.
- A faithful G→SU(n) gives the fibration SU(n)/G→BG→BSU(n). The homogeneous space is a finite complex; BSU(n) is simply connected. The cochain base-change construction therefore converges with the required finite fiber. This produces a compact proxy for F_p over cochains via Proposition 4.18.
- §5.7 establishes mod-p goodness of BG, cochain equivalence C^*(X;F_p)≃C^*(BG;F_p), and finite p-group π_1X. It does not suppose that π_0G itself is a p-group.
- The EM-type definition in §4.22 asks for finite-dimensional homology in each degree and either simple connectedness or a finite p-group fundamental group in characteristic p. X satisfies the latter alternative. It does **not** ask for a nilpotent action of the original π_0G on H^*(BG_e).
- That EM condition gives both double-centralizer equivalences, so Proposition 4.17 transfers proxy-smallness to C_*(ΩX;F_p). This completes the full hypothesis chain, not merely an assertion about uncompleted group chains.

No adjoint representation, orientation local system, Poincaré-duality shift, or spectral-sequence collapse is used here. Such hypotheses occur elsewhere in DGI and Greenlees for other results, and cannot be silently imported into §5.7. Conversely, nothing in this argument needs those stronger duality results.

## 4. Arbitrary characteristic-p fields

Every field k of characteristic p contains the prime field F_p. Singular chain complexes satisfy

C_*(ΩX;k) ≅ C_*(ΩX;F_p)⊗_{F_p}k

as augmented dg algebras (or the corresponding Hk-algebras), with the usual compatible product. Field extension is exact, so ordinary and derived tensor agree. If K_0 is the F_p proxy, its extension K inherits finite building from R, finite building from k, and building of k by preservation of finite constructions and coproducts. It is therefore a valid proxy over R.

This argument avoids the generally dangerous interchange between extension of scalars and an infinite cochain dual. It does not need a natural equivalence C^*(X;F_p)⊗k≃C^*(X;k). Infinite-dimensional k or infinite degree extension presents no difficulty.

Likewise H_*(ΩX;k)≅H_*(ΩX;F_p)⊗k. An infinite linearly independent F_p family remains linearly independent after extension, so total infinite dimension cannot disappear. The argument applies to finite fields, their algebraic closures, and transcendental characteristic-p fields equally.

## 5. Loop-space Hopf structure and disconnected loops

ΩX is grouplike. It admits the standard topological/simplicial group model. Multiplication, diagonal, constant loop, collapse to a point, and inversion induce the graded Hopf operations on H_*(ΩX;k). The bialgebra identity uses the Koszul sign in the symmetry of tensor factors. Künneth over a field identifies homology of products with the algebraic graded tensor product, without finite-dimensionality assumptions. Inversion supplies an antipode independently of connectedness.

X is connected; ΩX may be disconnected. Its component group is π_1X, a finite p-group by DGI, so H_0 is k[π_1X], not necessarily k. That is harmless: the finite-ideal lemma is a statement about arbitrary graded Hopf algebras and does not assume H_0=k. There is no mistaken replacement of all of ΩX by its identity component.

## 6. Ishiguro implication and completion compatibility

The official [Ishiguro 2007 article](https://msp.org/gtm/2007/10/gtm-2007-10-011p.pdf) was independently checked at printed p. 195 (definition) and p. 199, Proposition 1.3(a), with the surrounding discussion. It explicitly gives the necessary implication

BG p-compact ⇒ π_0G p-nilpotent.

The article means by BG p-compact that Ω((BG)^∧_p) is a p-compact group. Since the classifying space in this expression is already the specified completed X, the remaining finite condition is exactly finite total mod-p homology of ΩX. Thus, if the latter were finite, the necessary implication would contradict the theorem's non-p-nilpotence assumption.

This is the correct **contrapositive of a necessary condition**. The report does not assume its false converse. Indeed Ishiguro immediately discusses failures of sufficiency. The original 2001 proposition is credited, but the 2007 explicit restatement is itself a direct primary-author source and suffices for this dependency; the earlier paper was not independently obtained in this audit.

The completion convention is consistent between original question, DGI §5.7, and Ishiguro's article. Nothing in this step uses completion of G in place of completion of BG, or presumes they commute outside the allowed cases.

## 7. Adversarial and boundary checks

| Attempted failure | Check and outcome |
|---|---|
| Noncompact k invalidates approximation | The actual generator used for Morita theory is compact K; k compactness is never asserted. |
| Transfinite semi-free resolutions require an infinite dependency closure | Finite branching and well-founded descent force each finite dependency closure to be finite. No uniform bound over all generators is needed. |
| Unbounded M has classes inaccessible to finite stages | Filtered homology/compactness of the free rank-one module gives exactly class-by-class accessibility. |
| Image is only a finite subspace, not an ideal | A-linearity into A's regular module makes the entire homology image a graded left ideal. |
| Nonconnected ΩX violates Hopf theorem | Hopf theorem allows H_0=k[π_1X]; connectedness is unnecessary. |
| Odd p invalidates forgetting grading | Bosonization explicitly accounts for parity and preserves the finite ideal obstruction. |
| Nonorientable adjoint action | No duality shift or untwisted dual is used. For example G=O(2)×S_3 at p=3 has a nonorientable adjoint action and non-p-nilpotent component group; DGI and the abstract proof still apply. |
| Non-nilpotent component action | In that same example, the reflection acts by −1 on H^2(BSO(2);F_3), so its action is not unipotent/nilpotent. The proof does not invoke the nilpotent-action route. |
| Finite/positive-dimensional confusion | G=S_3,p=3 is included as a consistency check; products with S^1 produce positive dimension. The target only needs positive dimension, so the theorem is stronger in this harmless direction. |
| Connected compact Lie groups contradict vanishing | Their component group is p-nilpotent and they are outside the theorem; loop homology is finite after the relevant completion. No conclusion is asserted. |
| P-nilpotent finite group gives identity cellularization | Such boundary cases have finite loop homology; the infinite-Hopf hypothesis fails, consistently allowing a nonzero or identity map. |
| Ishiguro implication used backwards | Only necessary condition and contrapositive are used. P-nilpotence is not promoted to p-compactness. |
| Vanishing classes implies null morphism | The conclusion is restricted to homotopy groups throughout. |

## 8. Mechanism/evidence/status register

| Family | Mechanism | Evidence | Status | Exact gap |
|---|---|---|---|---|
| Compact approximation | Compact proxy replaces possibly noncompact k; Loc(K)=Ind(thick K) | Independent semi-free construction; DGI 4.9/4.10; BIS pp. 703,709 | Verified | None |
| Finite-image obstruction | Finite stage → A has finite-dimensional graded ideal image | Independent module-linearity calculation; graded finite-ideal proof checked | Verified | None |
| Topological proxy | SU(n)/G fibration + EM/double centralizer + proxy transfer | DGI §§4.17,4.22,5.7 directly inspected | Verified at full compact-Lie scope | None |
| Coefficients/components | Extend F_p proxy; retain disconnected Hopf algebra | Exact scalar extension; loop-group model; field Künneth | Verified | None |
| Infinite dimension | Contrapositive of p-compactness necessity | Ishiguro pp. 195,199, Prop.1.3(a) | Verified | None; original 2001 paper not separately inspected, but explicit 2007 author restatement is sufficient |
| Exact problem | Completion before looping; all homotopy degrees | Official OWR pp. 593–594 | Verified | None |
| Literature priority | Distinguish source machinery and special cases from new combination | No exhaustive priority search undertaken | Outside assignment | Parent must conduct required priority audit before publication |

## Final mathematical disposition

The independent reconstructed argument proves the report's full theorem and answers the original Question 2.2 affirmatively. No repair is required for the assigned topology, proxy-smallness, homotopy-class factorization, coefficient, component, or completion issues. This is a review judgment based on checkable arguments and cited literature, not formal certification or external human peer review. The separate priority audit and final fresh adversarial package reviews remain necessary under the user's process.
