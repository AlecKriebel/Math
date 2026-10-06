# Independent audit: KP-2.32, flat surface bundles

## Verdict

**ACCEPT the frozen author packet as a correctly scoped partial mathematical analysis. The full target remains UNSOLVED, with five of five approaches used. No mathematical correction is required.**

This is an independent AI mathematical review, not human peer review or formal verification. The accepted object is the six-file author archive with SHA-256 `438631e930255782b67ab90b2139255b223857a7d5cdb874496ff16f041f4f91` (12,700 bytes). Its immutable external manifest has SHA-256 `392de62a32bceb3d8aa7919d9021f7c9866731ce4d23a05f0cac323416bf60d1` (1,400 bytes). The author files are reproduced unchanged under `author/` in this audit packet. The author's historical “audit pending” statements remain unchanged; this report supplies the later acceptance.

The acceptance covers the genus-one boundary example; Propositions 2.1, 3.1, 4.1, 4.2 and Corollary 2.2; the diagonal-section example; and the stated limits on flux, Hofer, characteristic-class, symmetry, and bordism arguments. It does not accept a solution, novelty claim, universal lift, positive minimized obstruction, or proof of the current worldwide open status.

## 1. Statement and category checks

The complete problem record and complete associated report were read independently, including the entire literature-triage background. The associated report is empty. The complete-pair review hash and the statement hash match the author checkpoints. This establishes record identity, not the truth of the inherited literature assessment. No copied record contents are included here.

The primary K3 text was checked at Chapter 2's conventions (printed p. 84), the displayed problem (p. 111), and all three remarks (pp. 111–112). The problem requests transverse foliations for surface bundles over surfaces and over three-manifolds. The chapter fixes oriented surfaces and its notation S_g means a closed oriented surface; the displayed question itself omits a genus lower bound. Its lifting discussion uses the hyperbolic-fiber classification. The packet appropriately separates the literal lower-genus boundary from that intended target. The source's swapped fiber/base indices in part of Remark (3) are not propagated: throughout the packet g is fiber genus and h is base genus.

The accepted substantive results use closed, oriented, smooth fibers of genus g at least two, orientation-preserving structure group, and smooth holonomy. Neither a marked point nor a chosen section is part of the unrestricted target. Fixing an area form is an additional holonomy condition. No argument passes from failure in that smaller category to failure for all smooth diffeomorphisms.

K3 source: https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf

## 2. Hyperbolic classification and the lower-genus example

For g at least two, contractibility of Diff_0 implies that BDiff^+(S_g) is a K(Mod(S_g),1). On connected smooth manifold bases, maps into this classifying space are determined up to free homotopy by the induced fundamental-group homomorphism up to conjugacy. A suspension with the specified monodromy therefore has the same underlying bundle. This remains applicable to the non-aspherical three-manifold examples: it is the classifying space, not the base, that is aspherical. The Symp inclusion has the same homotopy type by the standard Moser argument, so the symplectic formulation also refers to the prescribed bundle.

The boundary example is a genuine torus bundle: multiply the Hopf circle bundle by a trivial circle. A smooth transverse foliation on a compact-fiber bundle has complete transport along finite paths; on a simply connected base its homotopy-invariant transport trivializes the bundle. Here this would imply S^3 × S^1 is a product S^2 × T^2, contradicted by their respective fundamental groups Z and Z^2. Pullback to S^2 × S^1 remains nonflat, since restriction to a slice would give a flat structure on the original example. Its mapping-class monodromy is trivial, illustrating exactly why the hyperbolic classification cannot be applied in genus one. This does not supply a genus-at-least-two counterexample.

Classification sources inspected: Kotschick–Morita, Remark 5; Bestvina–Church–Souto, pp. 2–3; Hillman, Section 3. https://arxiv.org/abs/math/0305182 ; https://arxiv.org/abs/0905.2360 ; https://msp.org/gtm/2015/19-1/gtm-v19-n1-p01-p.pdf

## 3. Flux inputs, action, and quotient splitting

The decisive published input is Kotschick–Morita, Theorem 2: for every g at least two, ordinary flux extends to an H^1-valued crossed homomorphism on the entire symplectomorphism group. Section 2 supplies the surjectivity and kernel facts and Hamiltonian perfectness; Lemma 6 uses the inverse-pullback left action. Theorem 2 and its Section 3 proof were inspected, rather than inferred from the abstract or confused with Theorem 1's g at least three condition. https://arxiv.org/abs/math/0305182

The following details independently check the applicability of those inputs.

- Ordinary flux is genuinely valued in V = H^1(S_g;R), not V modulo a nonzero flux lattice. Moser's comparison with the contractible Diff_0 gives trivial fundamental group of Symp_0, hence trivial flux group. Surjectivity can also be seen directly: for any closed one-form alpha, the vector field defined by contraction with omega equal to alpha is symplectic, is complete on the compact surface, and its time-one flow has flux [alpha].
- The smooth area form need not have total area 2g−2. If a proof normalizes it that way, rescaling omega rescales flux and the extended crossed map by the same positive constant and leaves G, N and H unchanged.
- Cohomology is contravariant, so m·v = (m^{-1})*v is the correct left action. This agrees with the conjugation action on flux. The semidirect product law in the packet therefore agrees with c(ab) = c(a) + q(a)·c(b).
- The algebraic argument requires no continuity of a chosen splitting and asserts only an abstract group isomorphism. Theorem 2's uniqueness is at the level of a cohomology class; the construction fixes one representative c. An N-coboundary vanishes because N acts trivially on V, so extending the flux class gives its exact restriction on N.

For Psi(a) = (c(a),q(a)), the crossed identity proves multiplicativity. A Psi-kernel element has q(a)=1, hence lies in N, where c is Flux. Its remaining condition is exactly membership in H. For surjectivity, choose a over m and n in N with Flux(n)=v−c(a); left multiplication gives c(na)=Flux(n)+c(a)=v. There is no missing m-action factor. Right multiplication would instead require Flux(n)=m^{-1}·(v−c(a)).

These checks prove G/H is V semidirect M and H is normal in G. Although c itself is generally not an ordinary homomorphism, its zero set K is a subgroup: zero is preserved by the crossed product law and by c(a^{-1})=−q(a)^{-1}·c(a). Surjectivity with v=0 proves K maps onto M with kernel H. Consequently K/H is M and the quotient extension splits. This does **not** split G→M or K→M. Its quotient section is canonical only after c is chosen.

## 4. Simultaneous relators and the nonabelian gap

Choose each presentation generator representative in K. Any relator is a finite word in K, so it remains in K. Its prescribed mapping class is the identity, so it lies in N and therefore in H. The same choice works simultaneously for all relators, including an arbitrary presentation. No finite presentation hypothesis is hidden. This establishes the full quantifier in Corollary 2.2, including the application to three-manifold groups.

The result says that every monodromy lifts after quotienting out H. It says neither that the generator choices satisfy the original relations in G nor that H can be removed. It is entirely consistent with a nontrivial Hamiltonian defect. If a representation into G already satisfies the relations, its composite with c can be a nonzero crossed cocycle of the base group. Normalizing separate generators into K need not preserve its relations. The packet expressly avoids that otherwise serious logical error.

## 5. Exact stabilization cost

For a fixed original lift tuple L, the old relator defect D(L) is in N because its mapping class is the identity. Trivial mapping classes on the added handles force their actual holonomies U_j,V_j to lie in N, rather than forcing those actual holonomies to equal the identity. The stabilized relation is exactly

    D(L) [U_1,V_1] ... [U_r,V_r] = 1.

Thus D(L)^{-1}, with the inverse in the correct position, must be a product of r N-commutators. Padding by identity commutators makes the “at most” and “exactly r allowed handles” formulations agree. Conversely, any such product defines a homomorphism from the stabilized surface group into G. Hyperbolic-fiber classification identifies its underlying bundle with the stipulated pinch-map pullback. No extra gluing invariant remains in Diff_0.

The abelian flux quotient gives [N,N] contained in H, and H's perfectness gives H=[H,H] contained in [N,N]. Hence [N,N]=H. At least one tuple has D(L) in H by Corollary 2.2, and each individual element of a perfect group is a **finite** product of commutators. Therefore the set of finite costs is a nonempty subset of the nonnegative integers. Its infimum is a minimum by well-ordering; no compactness, uniform bound, or minimizer in a function space is needed.

This proves the formula with the minimum over every original lift tuple and commutator length computed in N. Using commutator length in H instead would generally give only an upper bound. Restricting the original tuples to K would change the minimization. Neither replacement is made. Cost zero is exactly a relation-satisfying tuple on the original base. The genus-zero base is harmless: its empty tuple has identity defect and zero cost. Conjugating the prescribed monodromy cannot alter this minimum, since it can be implemented by a lift in G and N is normal.

Finite stabilization does not show zero stabilization, and perfectness does not imply uniform perfectness. No lower bound on the minimum or counterexample is accepted.

## 6. Hofer and actual flat subcases

The Hamiltonian-defect set is nonempty, and each of its elements has a finite Hofer norm. The infimum therefore exists as a finite nonnegative real number. A flat tuple contributes the identity and forces the infimum to be zero. A positive infimum excludes the identity; an infimum of zero does not place the identity in the set. Nondegeneracy of Hofer's norm applies to an individual element and does not supply attainment of an infimum over varying tuples. The packet imposes no nonexistent compactness theorem and takes the infimum over the full Hamiltonian-defect set, rather than only zero-extended-flux tuples.

The free-group argument correctly chooses lifts of a free basis and extends by the universal property. Composing with a factorization of the original monodromy gives a genuine representation into G and thus an area-preserving flat structure on the prescribed bundle. It is enough that monodromy factor through a free group; the base itself need not be aspherical or have a free fundamental group. The listed special cases follow: infinite cyclic image; compact connected oriented bases with nonempty boundary; and connected sums of S^1 × S^2, including S^3 as the zero-summand case.

For E→S_h and projection p:S_h×S^1→S_h, pullback carries a flat structure to p*E. The slice inclusion i satisfies p∘i=id, so restriction carries a flat structure on p*E back to E. This works for smooth and area-preserving holonomy. A counterexample over a surface therefore gives one over a three-manifold; universality over all three-manifolds implies universality over surfaces. The reverse universal implication is not established.

## 7. Nearby obstructions and current-source limits

For the product bundle projected onto its first factor, the constant-second-coordinate leaves explicitly exhibit flatness. The diagonal's normal bundle identifies with TS_g through (u,v)↦v−u, giving Euler number 2−2g up to orientation convention. If the diagonal were horizontal for a smooth flat connection, derivative holonomy would make its normal bundle a flat oriented rank-two real vector bundle. Milnor's bound is g−1 in this linear setting, not the circle-action bound 2g−2. Since 2g−2 exceeds g−1, that specified section cannot be horizontal. The contradiction concerns the prescribed section and is fully compatible with the product's ordinary flatness.

Bestvina–Church–Souto likewise require deck invariance in their Atiyah–Kodaira obstruction. Their theorem cannot be strengthened by omitting it. Their theorem statements, open-question discussion, and linear Euler bound were inspected. https://arxiv.org/abs/0905.2360

Degree-at-least-six MMM obstructions vanish upon pullback to bases of dimension two or three. This is only a dimensional observation; it does not produce a lift. Known area-preserving flat bundles with nonzero signature prevent signature alone from being a universal obstruction. Higher characteristic-class vanishing is not presented as a complete obstruction theory.

Nariman's 2024 paper distinguishes homological/bordism comparisons from a flat structure on the same base and same bundle. Its introduction and Section 1.1 were inspected; the arXiv record confirms version 3 dated 15 May 2024. The packet makes no fixed-base conclusion from these results and does not transfer conclusions between regularity categories. https://arxiv.org/abs/2202.00052

A bounded public search on 2026-10-06 revisited the primary K3 source, KM, BCS, Hillman and Nariman records and queried the general flatness question and recent flat-surface-bundle literature. No full resolution was identified in the material inspected. This search result is not an exhaustive current-status certificate. The original packet already states that limitation correctly.

## 8. Integrity, acceptance boundary, and disposition

The independent verifier checks pinned outer archive and manifest digests before interpreting any payload; exact six-member inventory; no duplicates, absolute paths, traversal names, links or executable modes; every member's bytes and digest; strict JSON without duplicate keys or nonfinite constants; the five-payload internal inventory; and the unsolved/five-approach status. It never imports or executes archive members.

Four positive runs passed: isolated normal and optimized runs, and normal/optimized relocation with hostile local import-shadow files and PYTHONPATH. Fifteen deliberately malformed controls were rejected. Internal controls recomputed only the explicitly recorded test trust layers so that structural and payload rejection was actually reached, rather than every result being merely an outer-hash mismatch. The separate two anchor tests rejected modified archive and manifest bytes. Details appear in INTEGRITY_REPLAY.json.

These replay runs exercise the independently authored external integrity utility; they are not code tests or CI for the author package, which contains no code. Import/optimization behavior of packaged code is inapplicable. No formal proof checker was run. All source PDFs, images, extracts, corpus records and working utilities remain outside the public data-only packet. No original author artifact was edited, no correction patch was necessary, and nothing was published as part of this review.

**Final disposition: accepted partial analysis; unrestricted KP-2.32 remains unsolved; five approaches exhausted; no mathematical patch required.**
