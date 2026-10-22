# Independent adversarial audit: QCI stable-Morita rigidity

Target: rank 668, ID 30001222, OWR-3400-006. Audit date: 4 October 2026.

## Verdict

**Accept the disposition UNRESOLVED_AFTER_FIVE_APPROACHES (5/5), with the scope conventions and minor clarifications below.** No substantive mathematical error was found in Propositions 1–6. The five approaches contain meaningful distinct work and correctly identify their stopping obstructions. This is not an affirmative solution, a counterexample, or certification of global open status or novelty.

The 36-dimensional examples are nonisomorphic, but neither the author nor this audit has established or excluded a stable equivalence of Morita type between them. The 9-dimensional deformation pair is positively excluded from such an equivalence by unequal HH1 dimensions. These two conclusions must not be compressed into the same phrase.

The exact audited input is `rank668-30001222-authored-packet.zip`, 23,282 bytes, SHA-256 `4fc5af73089e545434dbb7020c197edb070066208122ad03237879da58bb01fa`. Its ten members, including the manifest, were preserved. The manifest's nine payload records match their bytes and hashes. The original verifier passed all 204,097 assertions and produced a byte-identical result file. `AUDIT_BINDING.json` binds this verdict to the exact input and records the reproduction evidence.

## Independent computation, beyond replay

`independent_checks.py` neither imports nor uses the author's verifier. It builds products by rewriting strings in x and y, using two reduction orders. It then computes derivations from the complete Hochschild 1-cocycle equations for arbitrary linear endomorphisms, rather than by differentiating the presentation's three relations.

The resulting dimensions are:

| Algebra | dim A | Der | inner Der | HH1 | center | projective center | stable center |
|---|---:|---:|---:|---:|---:|---:|---:|
| A3 over F11 | 36 | 36 | 24 | 12 | 12 | 1 | 11 |
| A9 over F11 | 36 | 36 | 24 | 12 | 12 | 1 | 11 |
| C0 over F3 | 9 | 11 | 3 | 8 | 6 | 0 | 6 |
| C1 over F3 | 9 | 10 | 3 | 7 | 6 | 0 | 6 |

For each 36-dimensional example there are 46,656 basis-pair/output cocycle equations on 1,296 coefficients; their rank is 1,260. For C0 and C1 there are 729 equations on 81 coefficients, with ranks 70 and 71. All 46,656 multiplication-associativity triples per 36-dimensional algebra and 729 per 9-dimensional algebra pass independently. Leftmost and rightmost word reduction agree on all 16,383 words of lengths 0–13 per 36-dimensional algebra and all 2,047 words of lengths 0–10 per 9-dimensional algebra. These finite controls supplement the critical-pair reasoning; they do not replace universal proofs.

The independent checker derives the centers from all commutators and verifies the stated matching multiplication tables. It reproduces every radical-power dimension. For the deformation pair, it also expands the cube of a fully symbolic radical element: coefficients are polynomial monomials in eight commuting variables, reduced modulo three. Thus the independence from all J² coefficients is checked as a polynomial identity, not merely as a finite-field function. Restricting the full cocycle kernels to the generator images verifies precisely the six common zero conditions and the one or two additional equations in Proposition 6.

The stable-center computation uses the symmetrizing Gram matrix to find dual bases and evaluates the Higman map a ↦ Σ b_i a b_i*. The F11 image is the line spanned by the top monomial, with τ(1)=3x⁵y⁵; the F3 Higman maps vanish. The standard identification of this image with the projective center is reviewed in [Zhou–Zimmermann, Propositions 1.4–1.5](https://math.ecnu.edu.cn/~gdzhou/JPAA2011.pdf). The computation uses the dual-basis formula directly and does not extrapolate an algebraically-closed-field Cartan-rank theorem to an unspecified field.

## Proof audit

### 1. Commutative reconstruction

Proposition 1 is complete: the center isomorphism identifies dim Z(Y) with dim X, and equal algebra dimensions imply Z(Y)=Y. The given k-algebra isomorphism of centers is then the algebra isomorphism. Stable equivalence, locality, and symmetry are unnecessary. The prime-dimensional consequence uses the expressly imposed exponents a_i≥2, so a prime product has a single factor. No claim is made for the proper-center case.

### 2. Ranks and failure of simple preservation

Over split local A and B, all finite projectives on either side are free. Equal algebra dimensions force the two one-sided ranks of each bimodule to agree. The radical-sum ideal in A⊗Aop is nilpotent and has quotient k, so the enveloping algebra is local. Consequently the projective bimodule error term is free, and taking dimensions yields rs=1+td. This proves that r and s are reciprocal units modulo d, not that either is one and not, without additional information, that r²=1 modulo d.

The split assumption is correctly retained. An arbitrary local algebra can have a larger residue division algebra; it is not legitimate to infer that its enveloping algebra is local by the same argument.

The syzygy example is valid under the stated nonsemisimple symmetric split-local hypotheses. Here are details checking the stronger bimodule definition, beyond a mere equivalence of stable module categories. Put R=Ae and M=ker(R→A). Since R is symmetric, choose a finite projective-injective bimodule I and an injection A→I, with cokernel N. The two sequences split after restriction to either A-side, since A is projective and injective over itself, so both M and N are projective on both sides. Tensoring 0→M→R→A→0 with N and comparing with 0→A→I→N→0 by Schanuel gives

(M⊗A N) ⊕ I ≅ A ⊕ (R⊗A N).

The added terms are projective R-modules. A is an indecomposable, nonprojective R-module: its endomorphism ring is the local center, and its dimension d lies strictly between 0 and d². Krull–Schmidt cancellation gives M⊗A N ≅ A⊕P for a projective bimodule P. The other tensor order is analogous. This supplies stable equivalence of Morita type in the exact sense used by the packet.

Moreover M⊗A k is exactly J(A), since tensoring the split-on-the-right multiplication sequence yields the usual augmentation sequence. Stable isomorphism with k would force d−1≡1 modulo d, impossible for d>2. Thus the proposed simple-preservation shortcut genuinely fails, even for an algebra's self-equivalence.

### 3. Local derived-equivalence strengthening

The minimal tilting-complex proof is correct when derived equivalence is understood to be k-linear. The asserted endpoint map really is a chain map: all possibly offending adjacent components vanish outside the endpoints. At the initial degree, a null-homotopy factors through one or both endpoint-adjacent minimal differentials; its entries lie in J(A). A unit matrix entry cannot occur. Hence the complex has one degree only. The endomorphism algebra of a free right module A^r is M_r(A), and locality of B forces r=1.

No separability or algebraic closedness is required for this argument. No lifting from stable equivalence is supplied, and the packet never uses this strengthening to claim a solution. An explicit k-linearity convention is recommended below to exclude abstract semilinear equivalences from the statement's intended meaning.

### 4. Parameter variation

For e>2, order(q)=e ensures q≠1 and the only degree-two relation is xy−qyx: the truncation degree e+1 is larger than two. The commuting-monomial test yields exactly the displayed 2e+2 central monomials. Boundary truncation makes their only nontrivial radical product x^e·y^e=y^e·x^e; its scalar is q^(−e²)=1. Complementary monomials have equal forward/reverse top coefficients and nonzero pairing, proving symmetry.

The nonisomorphism proof is valid over any field containing the indicated roots, and after any common field extension. Any algebra isomorphism induces an invertible degree-one map on the radical associated graded algebra. The equations ac=bd=0 and ad−bc≠0 force either a diagonal or antidiagonal matrix. Substitution gives r=q or r=q⁻¹, respectively. Higher-degree corrections to generator images cannot alter the quadratic relation. For F11, 3 and 9 both have order five and 9 is neither 3 nor 3⁻¹=4. The matrix enumeration is a control, not a substitute for this argument.

For Proposition 5, differentiating each power relation eliminates the e+1 variables whose corresponding generator exponent is zero, provided char(k) does not divide e+1. Nontrivial geometric sums are one; the two endpoint sums are e+1. After these eliminations, the commutation derivative gives e²−1 independent equations on disjoint variable pairs. The only zero equation is at (r,s)=(1,1). Thus the derivation and HH1 dimensions are correct. The characteristic condition cannot simply be dropped: the characteristic-three e=2 example is outside this proposition, consistently with its different derivation dimension.

### 5. Socle deformation

The reduction system is terminating using weight(x)=3, weight(y)=1 and a within-weight order with yx larger than xy. Its critical overlaps are the two self-overlaps of x³, the two self-overlaps of y³, and the mixed words yx³ and y³x. Both paths in each case agree. In particular x⁴ and x⁵ reduce to zero, and yx³ reduces to a multiple of x²y³ from either path. Hence the nine normal monomials are justified, independently of the finite table controls.

The radical filtration and center multiplication are correct. The top-coefficient form is symmetric; the extra x·x² term for β=1 does not destroy the nonsingular complementary-degree blocks. Both algebras are therefore self-injective.

The universal cube formula gives the stated zero loci over every field of characteristic three. In C0 the locus is the union of two distinct hyperplanes and is not a vector subspace (x and y lie in it, while x+y does not); in C1 it is the single hyperplane a=0. This proves nonisomorphism without cardinality reasoning or algebraic closedness.

The independent full Hochschild calculation agrees with every displayed derivation constraint. Those matrices have coefficients in F3, so their ranks are unchanged by extending scalars to any field of characteristic three. The unequal HH1 dimensions therefore apply in the full stated field scope.

[Briggs–Rubio y Degrassi, Theorem 1](https://arxiv.org/abs/2006.13871) concerns positive-degree Hochschild cohomology of finite-dimensional self-injective algebras over a field of positive characteristic. Its stated assumptions do not require an algebraically closed field or an extra separable-semismiple-quotient hypothesis. In any event these examples have quotient k, which is separable over itself. Their characteristic-three HH1 mismatch is a valid stable-Morita obstruction.

## Source, scope, and invariant audit

All six cited public PDFs were freshly downloaded; their byte counts and SHA-256 hashes exactly match the author's metadata. Metadata only is included in `source_retrieval.json`; PDF bytes and extracted source text are excluded. The original question on printed p.941 and Kessar's theorem across printed pp.1–2 were also inspected visually using freshly rendered pages. The HH-invariance theorem on printed p.2 was visually inspected. The unsuccessful web-screenshot fetches were replaced by local rendering of the successfully retrieved public PDFs.

The original [Oberwolfach report](https://doi.org/10.4171/owr/2009/17) asks the exact center/dimension/local-symmetric/stable-Morita question. Its contribution has previously fixed a residue field of prime characteristic, and the question itself does not expressly impose algebraic closedness. The packet's distinction between this context and the catalogue's arbitrary-field wording is appropriate.

[Kessar, Theorem 1.2](https://arxiv.org/abs/1012.0534) requires an algebraically closed field of characteristic three and the particular presentation x³=y³=0, xy+yx=0, as well as a local symmetric partner of dimension nine with isomorphic center and stable equivalence of Morita type. The author's account is accurate. This theorem does not resolve the general question or an arbitrary-field nine-dimensional version.

[Benson–Kessar–Linckelmann, Corollary 1.3](https://arxiv.org/abs/1604.04437) gives the 2e bound under the split-local symmetric partner hypothesis, for the p-power truncation family and e≥2 dividing p−1. The inverse parameter convention is handled correctly. The bound does not say that the partner has two generators. The packet's short prose summary should explicitly retain e≥2 to match the cited theorem. Within the target's additional equal-dimension and center-isomorphism hypotheses, the e=1 case is covered separately by commutative reconstruction. That separate argument should not be presented as a proof of the cited corollary for arbitrary stable-Morita partners.

[Bergh, Lemma 3.1](https://arxiv.org/abs/0811.4309) supports Frobenius structure and the diagonal Nakayama automorphism; Frobenius has not been confused with symmetric. The [September 2026 preprint](https://arxiv.org/abs/2609.24007) exists with the title and submitted date stated. Its displayed projectivity criterion concerns modules with vanishing self-extensions, not algebra reconstruction from stable Morita equivalence. Its proof was not independently re-proved and it is unnecessary for the packet's partial results.

Ordinary center isomorphism is an independent hypothesis of the target. Stable center is the quotient by projective bimodule-factorization maps, and it is not legitimate to use its invariance to assert ordinary-center invariance in general. The packet makes no such inference. The separate Higman computations above make the distinction concrete: the F11 ordinary centers have dimension 12 and their stable centers dimension 11, while the F3 centers agree with their stable centers.

The bounded literature check did not locate a general resolution. That is not an exhaustive absence certificate. Dataset hashes and catalogue-match claims remain the author's provenance claims: this audit did not reopen or redistribute the datasets, and it does not recertify their full-file searches. The primary mathematical target was independently verified.

## Publication boundaries and suggested clarifications

1. State explicitly that derived equivalences and all algebra isomorphisms are k-linear. This makes Proposition 3's intended convention unambiguous.
2. Preserve the exact distinction: the F11 pair has **no stable equivalence established**, whereas the characteristic-three deformation pair has **no stable equivalence of Morita type**, proved by an obstruction.
3. Include e≥2 when summarizing the precise Benson–Kessar–Linckelmann theorem. The target's e=1 case, with all its center and dimension hypotheses, follows separately from commutative reconstruction.
4. Keep the ordinary-center hypothesis separate from stable-center invariance. No correction to the existing argument is required, but the distinction is worth retaining in shortened summaries.
5. Do not present exact assertion counts as proof counts, a finite matrix search as arbitrary-field classification, matching invariants as an equivalence, or a bounded search as a proof of novelty.

These are precision safeguards, not repairs to a false claimed resolution. No original file was changed. No remote repository action was taken. The portable audit contains authored analysis, verification code and results, public-source metadata, and byte/hash bindings only.
