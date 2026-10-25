# Independent adversarial review: logarithmic Bray sampling

Record: Zenodo 23577484, *Logarithmic Bray sampling in symplectic and orthogonal groups*, published version 1.0.0, 22 October 2026.

Reviewed 2026-10-24. Verdict: **no substantive defect found within this review's scope**. This is an AI-assisted adversarial review, not formal proof certification or independent human peer review.

## Exact scope and sources

Read all eleven pages of the published manuscript, the corresponding `main.tex`, `DEPENDENCIES.md`, and the complete published `exact_checks.py`. Earlier favorable review conclusions were not used as premises. The main task was to attempt to falsify the chart parametrization and probability law, four orthogonal character sectors, the 192-class generation bound, and the passage from separate marginal successes to the actual centraliser's second derived group.

Source identities:

- PDF SHA-256: `2384d12cb9335141d01e0093297e2d6e7efa6e1e9e7ddc6f6e7af4b40b4287a4`.
- Source archive SHA-256: `7a23be70751bafac555e10cbeac1ea07bfe1281e8eaab3719a83dc353dbfec84`.
- `main.tex` SHA-256: `a875aa501657f38c0086a4353abd7555e140c2acf5b4e69bfb560482e04f6da7`.

The exact assertions being reviewed concern actual involutions, odd characteristic, natural matrix groups, independent exactly uniform samples, sufficiently large dimensions, and sample count. They do not assert a practical running-time bound, a certified stopping algorithm, simultaneous strong components, or a result for every dimension.

## Mathematical attacks and outcome

### Graph chart and unconditional probability

The graph of `F:A→B` gives the claimed conjugate involution only after requiring nondegeneracy of `K=F*F` and `1+K`, together with the determinant condition in the orthogonal case. The graph map is injective, so counting distinct `F` does not overcount conjugates. The denominator is the full conjugacy-class size, not the chart size. This distinction is correctly retained.

The orthogonal codimension-zero constraint is essential. For positive codimension either complementary discriminant exists; for zero codimension it must be the trivial zero-space discriminant. The paper imposes exactly that restriction. Both one-dimensional full orthogonal orders and `|O(0)|=1` occur correctly. The scalar `|O(A)|/2` count for each squarefree `f` follows from the equal orbit sizes of the `2^(s−1)` coefficient-type assignments with prescribed total discriminant. The embedding fiber depends on the total complementary form, not on the individual coefficient-type assignment, so the subsequent equal-weight argument is valid.

Direct enumeration of maps, using separate code, checked twenty combinations over F3, F5 and F7, both orthogonal types of A and B, and codimensions zero and one. Every observed polynomial fiber equals `|O(A)||O(B)|/(2|O(C)|)`, and every observed set of K has size `|O(A)|/2`. The cases with no permitted polynomial are correctly empty; these small cases are not mistaken for evidence of the asymptotic lower bound.

The symplectic exponent in the mass formula is `−a`: the group-order exponents cancel against `∑3d=3a`. Its uniform lower bound follows from four numerator factors at least `7/8` and denominator factors at most one. The orthogonal normalized mass bound has been checked algebraically and with exact rational arithmetic for q in {3,5,7,9,11}, `1≤a≤24`, `a≤b≤2a`, and all compatible discriminant sectors. The smallest sampled normalized mass is `32/65`, above the stated `1/8`; this numerical minimum is not claimed globally optimal.

### Distinguished 2-part and all four sectors

The degree-preservation argument in Lemma 4.1 survives the important possible collapse from k to k/2: that collapse would put λ in the norm-one torus of order `q^(k/2)+1`, whose 2-part is two, while the chosen λ has larger 2-part. The `λ↦κ` map has exactly the inverse-pair fibers used in the count. Maximal 2-part forces λ nonsquare; because k is divisible by four, the resulting κ and `1+κ` have characters +1 and −1. Norm transfers these characters correctly to the base field. The dominance comparison covers both split and nonsplit quadratic tori and all factor degrees not divisible by d.

An independently constructed finite-field implementation tested the entire distinguished set in F(3^4), F(5^4), F(7^4), and F(3^8). It checked degree preservation, the Cayley identity, inverse-pair fibers, character signs, Frobenius orbit sizes, the lower factor count, and the order-2-part comparison through degree 128. The resulting irreducible-factor orbit counts are 5, 39, 150, and 205, respectively. All exceed the claimed lower bounds.

The squarefree character generating function follows by dividing the ordinary character Euler product by its squared-character product at `u²`. Extending each character by zero at both forbidden roots is crucial and is done in the manuscript. The displayed coefficient error is linear `qr/2`, not exponential `q^(r/2)`; the typeset source confirms this. Fourier inversion yields the stated uniform sector lower bound when r≥8. No sector is discarded for q=3.

Separate exhaustive polynomial enumeration extends beyond the release checker: F3 degrees 9 and 10, F5 degree 6, and F7 degree 5. All three character sums agree exactly with the generating-function coefficients. The degree-9 F3 sector counts are 1848, 1841, 1848, 1848; the degree-10 counts are 5537, 5537, 5537, 5528. The r≥8 lower bound holds in both tested cases.

The orthogonal square-spinor refinement does not presume independence of determinant and spinor norm. A residual primary factor exists, so toggling its coefficient type together with the distinguished type preserves the total discriminant and flips the distinguished discriminant. Equal fibers make the resulting half-mass exact. Since k is divisible by four, the distinguished involution has determinant one and spinor character equal to the selected discriminant character. Enumeration of all sign assignments for 2–12 factors confirmed this balancing interface.

### The 192-class bound

For a fixed strong involution, an invariant subspace splits across its two eigenspaces. Nondegenerate intersections remain nondegenerate; totally singular intersections satisfy the required dimension restrictions. The exponent losses `ib+ja−2ij` and `ib+ja−3ij` have the claimed lower bound `ek/12`. Exact enumeration checked 462,937 feasible dimension/intersection cases up to dimension 80, including unbalanced strong endpoints. The proof itself supplies the general inequality.

There is no hidden assumption that an orthogonal subspace orbit stays a single Ω orbit: the involution's full O class is a single Ω class, which is enough for its fixed-subspace probability to be constant on the full O subspace orbit. Reducible subgroups have either an invariant totally singular radical or an invariant nondegenerate subspace of dimension at most e/2. Thus the two subspace families cover the reducible case.

The absorption `128(k+1)≤256^k≤3^(8k)≤q^(ek/48)` at e≥384 gives the stated `q^(−ek/16)` bound. Raising it to 192 and summing at most `12q^(ek)` candidate subspaces gives the displayed reducibility tail. The class-size estimate loses at most a factor two on passing to the projective simple quotient, and a strong involution cannot become identity there.

I independently inspected [Burness's author-hosted paper](https://seis.bristol.ac.uk/~tb13602/docs/fpr1.pdf), specifically Definitions 1–2, Theorem 1, Corollary 1 and the correction table. The non-subspace action theorem applies to prime-order images in the sufficiently large symplectic/orthogonal simple groups used here; its dimension convention and listed corrections agree with the manuscript's use. I also inspected [Liebeck–Pyber–Shalev's author-hosted paper](https://www.ma.imperial.ac.uk/~mwl/WALL.PDF), Theorem 1.1, which bounds the total number of maximal subgroups, not merely conjugacy classes. Those inputs support the union bound. Their classification-based proofs were not independently re-proved.

The finite threshold `e0` is existential because the imported maximal-subgroup constant is unspecified. That limitation is stated in the paper. The perfectness argument `KZ(J)=J ⇒ J=(KZ(J))'=K'≤K` correctly lifts generation from the simple quotient to the natural central cover.

### Conditioning and diagonal escape

This is the most important interface to test: marginal success alone would not yield generation of the product, and repeated outputs could in principle remain in a diagonal graph.

The paper proves the required stronger conditional law. Full product conjugation classes remain single centraliser conjugation classes, because reflections in one joint eigenspace of dimension at least three cover the total determinant/spinor quotient. Therefore fixing the two actual component classes gives an independent uniform product law. This is conditional independence; it does not assert unconditional independence of the components.

Selection of the first success in each finite block preserves the law conditioned on the target event. Disjoint blocks conditioned on their own successes remain independent. Explicit enumeration of every sequence for block lengths 1–5 under a nonuniform four-outcome law independently confirms this selection identity. The main proof establishes it for arbitrary length and law.

After the first 384 successful blocks, the generated subgroup projects onto both perfect factors. Goursat's alternatives in the simple quotient are precisely the full product or one graph of a quotient isomorphism. The graph is fixed by the already-generated subgroup before drawing the last independent output, so no union bound over isomorphisms is needed. The proof does not incorrectly lift a projective isomorphism to the central covers.

The kernel bound for `D_U→Aut(L_U/Z(L_U))` is sound in the large dimensions under discussion. Perfectness first reduces its kernel to the natural representation centraliser. The transvection argument handles Sp; the common fixed lines of the Siegel transformations handle Ω. Preserving all singular lines forces the same scalar on a Witt basis and the remaining anisotropic space. Consequently there are at most two compatible B components for each A component. Conditional uniformity on the large strong B class gives the claimed diagonal escape bound.

Finally, retaining all outputs means the procedure need not recognize the selected good outputs. A successful trial supplies a subgroup of the full generated group. Independent trial amplification has failure at most δ and the stated order `log n (1+log(1/δ))`. The 385-block constants are large but absolute. No efficient total-time or stopping guarantee follows, and none is claimed.

## Reproducible artifacts and result

- `independent_checks.py` and `independent_results.json`: exact polynomial, graph-map, mass, dimension, threshold, and selection checks described above.
- `field_checks.py` and `field_results.json`: independently constructed finite fields and the complete distinguished-factor tests.
- `release_replay.json`: the published standard-library checker was replayed successfully against its archived expected results.

All three executions passed. No observed assertion failure was suppressed and no published source was edited. These checks are bounded interface diagnostics, not proofs by exhaustive verification of the universal result.

**Disposition:** pass this adversarial review, subject to synthesis with the independent mathematical/literature review. No substantive defect to defer was identified. Remaining limitations are the paper's stated large-dimension, exact-uniformity and sample-count scope, reliance on established structural and maximal-subgroup theorems, and the absence of human peer review or formal certification. This review does not establish worldwide novelty or journal acceptance.
