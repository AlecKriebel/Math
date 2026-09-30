# Independent review: KP 1.63 / 2722

**Verdict: PASS for the credited structural obstructions and source-scope audit. The fixed-knot infinitude problem remains unresolved. No mandatory correction was identified.**

Reviewed September 30, 2026 by a separate gpt-6-astra agent using xhigh reasoning. The frozen `OBSTRUCTION.md` has SHA-256 `335a802ffaab7625ca227597a83121e31b6d6128d08d9c75fff01df414c36827`. This is independent AI review, not external refereeing or a novelty certificate.

## 1. Exact target, both stabilization signs, and the source wording

I requested the live problem page, which was unavailable to the reader, and read the complete pinned record. I then checked [K3](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf), printed pp. 61–62, and [Etnyre–Ng's original Question 44](https://etnyre.math.gatech.edu/preprints/papers/problems.pdf), printed p. 12, together with its surrounding definitions. The ambient contact structure is the standard tight structure on the three-sphere, equivalently standard contact three-space. The smooth knot type is fixed while Legendrian isotopy classes vary.

The author's peak set excludes the images of both positive and negative stabilization, after arbitrary Legendrian isotopy. This is the right definition; having no immediately removable zigzag in a particular front is weaker. Stabilizing in either sign decreases tb by one. Orientation reversal interchanges the relevant conventions but has only finitely many choices and leaves tb unchanged, so it cannot affect existence of an infinite family or an unbounded-below family.

The K3 p. 62 sentence beginning “This has been proved” really does follow the infinitude equivalence and precede references to classified families including the unknot. Reading it as a proof of fixed-type infinitude is incompatible with those classifications. The submitted package appropriately identifies the antecedent problem without treating it as a mathematical resolution or alleging anything about the authors. The original Question 44 and the current Dynnikov–Prasolov conjecture remove any ambiguity about the target.

## 2. Fixed-level finiteness and termination at a peak

I read the exact French statement of [Colin–Giroux–Honda, Theorem 10](https://www.numdam.org/article/PMIHES_2009__109__245_0.pdf), printed p. 248, and its proof in Section 5, pp. 291–292; the theorem page was also visually inspected. It specifies a fixed smooth knot type and fixed Thurston–Bennequin invariant in standard contact S³, with finitely many Legendrian isotopy classes. It does not impose an additional fixed rotation number. The proof is a consequence of their deep contact-structure finiteness theorem, which is an imported result rather than re-proved in this review.

For a fixed smooth type, the Bennequin inequality supplies an upper bound on tb. Successive destabilizations raise that integer strictly, so every such process terminates. Consequently every Legendrian class is a finite stabilization of some peak, and every smooth knot type has at least one peak. No uniqueness of the terminal peak is assumed.

The three equivalent formulations in Section 2 are correct. In particular, a lower bound on peak tb combines with the upper bound and fixed-level finiteness to give a finite peak set. Conversely, a peak obtained from a finite generating list cannot require a nonempty stabilization word. This equivalence does not supply the missing lower bound.

## 3. Connected-sum reduction

I checked [Etnyre–Honda's Theorem 3.4 and Lemma 3.3](https://arxiv.org/abs/math/0205310) and [An's author preprint, Theorem 5 and Corollaries 7–8](https://arxiv.org/abs/1503.01188). An's paper was published in Topology and its Applications 204 (2016), 175–184, [DOI 10.1016/j.topol.2016.03.011](https://doi.org/10.1016/j.topol.2016.03.011). The explicit corollaries used here do not require the prime factors to be Legendrian simple; that condition appears in other results of An's paper and must not be imported into or omitted from the wrong theorem.

The full quotient relation allows a stabilization of either sign to move between factors, and allows permutations only among identical oriented prime types. Every endpoint of a stabilization-transfer move has at least one stabilized factor. Hence an all-peak tuple admits no such move in either direction. Permutations cannot change that fact. Its entire equivalence class consists only of the allowed permutations. Conversely, a tuple with a stabilized factor gives a stabilized connected sum. This verifies the peak restriction rigorously, including the possibility of arbitrary finite sequences of equivalence moves.

It follows that the peak set is the product of the symmetric powers of the prime-factor peak sets. For finite nonempty sets, the binomial counting formula is correct and counts Legendrian classes, not merely pairs of classical invariants. Distinct peaks having the same tb remain distinct entries. The minimum-tb formula has the correct `m−1` correction from repeated application of `tb(L#L')=tb(L)+tb(L')+1`; repetition of a factor's minimizing class is permitted in a symmetric power.

For a nonempty set P, a positive finite symmetric power is infinite exactly when P is infinite. Holding all other factor entries fixed proves the necessary direction even after quotienting by identical-factor permutations. Therefore an infinite peak set for a composite fixed type requires an infinite peak set for one fixed prime factor. Coupling this with the fixed-level equivalence proves the claimed prime-knot reduction. Increasing the number of connected-sum factors changes the smooth type and cannot substitute for this conclusion.

## 4. Finite-dimensional DGA representations and framing

I read the published [Ng–Rutherford paper](https://msp.org/agt/2013/13-5/agt-v13-n5-p16-s.pdf), especially Definition 2.27, Theorem 1.2, Corollary 3.11, and Theorems 4.8–4.9. Printed p. 3082 was visually inspected. The exact imported assertion covers finite-dimensional ungraded representations of the based Chekanov–Eliashberg DGA over F₂. It implies that the Legendrian representative maximizes tb in its smooth knot type.

The package states the necessary conventions correctly:

- The representation is unital and satisfies `φ∂=0`
- Its vector-space dimension is a positive finite integer; the zero vector space is excluded
- The basepoint generator t is invertible, but its image is not required to be the identity
- “Ungraded” is the source's 1-graded convention
- No unverified extension to arbitrary coefficient fields or infinite-dimensional modules is claimed

The satellite used in the source's introductory representation theorem has n strands, with smooth parallel framing coefficient `tb(L)+1`. I verified that convention. The submitted proof does not attempt to identify satellites having different smooth framings merely because the companions have the same smooth type. It invokes the established type-and-tb invariance theorem directly, which avoids this framing pitfall.

The certificate-ceiling lemma is correct. A maximum tb is attained because the nonempty set of integer tb values is bounded above. If a class lies below it, stabilizing a maximizer the required number of times produces a stabilized representative with that same smooth type and tb. A property invariant under these two data and excluded for stabilizations cannot hold below the maximum. The argument uses no bound on matrix dimension, so increasing a finite dimension cannot evade the obstruction.

The DGA obstruction for a stabilization is the presence of a chain whose differential is the unit; a positive-dimensional unital representation cannot annihilate that differential. No assertion that absence of such representations forces stabilization is made.

## 5. The Leavitt diagnostic and credited examples

The algebraic example is valid in characteristic two. On the algebraic direct sum with countable basis, the even/odd inclusion and projection operators satisfy every displayed relation and give a nonzero identity operator. Each basis vector has finite support throughout, so no analytic completion is involved.

In finite positive dimension, the resulting maps between V and V⊕V would be mutually inverse. Their dimensions cannot agree. This is a rank/dimension contradiction over any field, not a trace computation modulo the characteristic. The package explicitly avoids claiming a Legendrian realization of this algebra.

The source checks for the additional topology examples also match. Ng–Rutherford Remark 4.10 credits the nonmaximal-tb examples and the absence of finite-dimensional representations. [Sivek's theorem](https://arxiv.org/abs/1012.5038), published in J. Symplectic Geometry 11 (2013), 167–178, supplies a maximal-tb representative of the mirror of 10₁₃₂ with trivial contact homology. Maximal tb alone precludes either destabilization. These are credited literature controls; this review does not independently recompute their full diagrammatic DGAs or identify all coefficient variants with one another. The artifact does not claim those computations were revalidated.

## 6. Grid and algorithm distinction

The current [Dynnikov–Prasolov arXiv record](https://arxiv.org/abs/2309.05087) shows v1, September 10, 2023. I read the introduction, Conjectures 1.1 and 1.3, and Theorem 1.4 in the complete PDF. The algorithm compares two given Legendrian links. It does not output a uniform bound on all peaks of one smooth type.

The source's nonsimplifiability excludes a sequence of allowed elementary moves that contains a destabilization and no stabilization, rather than only an immediately removable corner. The submitted package preserves this distinction and does not promote a finite search to a finiteness proof.

## 7. Reproduction and disposition

All 2,045 submitted exact assertions were replayed outside the author's directory, using an unchanged copy of the frozen artifact. The resulting receipt is byte-for-byte identical to the author's recorded JSON. No author file was modified.

The independent standard-library script passes 512 exact controls. It checks symmetric-product counts with equal-tb distinct classes, both signs of stabilization transfer, the fixed-level unknot model, an independently implemented bit-mask realization of the infinite Leavitt module, and the finite positive-dimension obstruction. These are bounded algebraic diagnostics, not actual Legendrian enumeration or proof of the imported contact-topological theorems.

The review files preserve the exact reviewed snapshot and checker in `author_replay/`. Run `python3 independent_checks.py` for the independent receipt, or `python3 author_replay/verify.py` for the submitted replay.

**Final disposition:** the obstruction package is correct within its explicitly limited scope. The original problem remains unsolved. Preserve both attempted-route accounting, prior attribution, the positive finite-dimensional F₂ convention, the absence of an actual new Legendrian example, and the lack of a novelty claim. No mandatory correction is required before a draft PR describing this as unresolved research.

## Final status-only snapshot coverage

On 2026-09-30, the sole change in `OBSTRUCTION.md` replaced the pending-review sentence with a link to the completed separate AI review. An exact full-file comparison confirms no mathematical changes. This verdict also covers SHA-256 `f49157b6c24222c30c796dfdfbff4da2bd2bec693a535bdfcfc83c0a37e32336`. The verifier is byte-identical. The retained author replay deliberately records the originally reviewed snapshot.
