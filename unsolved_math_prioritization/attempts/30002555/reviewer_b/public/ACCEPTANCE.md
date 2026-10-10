# Independent mathematical audit: prescribed-end Veech obstruction

Problem 30002555 / OWR-12875-003, rank 987. Review date: 7 October 2026.

## Verdict

**ACCEPT AS WRITTEN: the frozen candidate proves a complete negative answer to the universal, prescribed-matrix-group question. No mathematical correction patch is required.**

The accepted counterexample is the closed Cantor subset

\[
X=\{0,2/3,1\},\qquad
G=\left\langle\frac15\begin{pmatrix}3&-4\\4&3\end{pmatrix}\right\rangle.
\]

The group is countably infinite and noncontracting. No translation structure on an infinite-genus surface with precisely three ends, all accumulated by genus, has this matrix group as its Veech group. Indeed its Veech group cannot contain the displayed matrix. The argument covers tame structures because it establishes the obstruction without a flat-completeness or tameness assumption.

This verdict applies to author manifest SHA-256

`f7b959531c352611c5c9b9d0c2cb57bcb865de9399d65dbd66c4fabef3a88e59`.

The complete eight-file author inventory was verified. The author packet was preserved. This is an independent AI-assisted mathematical audit, not human peer review, formal proof-assistant certification, a priority determination, or a general Veech-group classification.

## 1. Exact target and source fit

I inspected Valdez's whole contribution on printed pages 885–888, with visual inspection of Question 4 on page 887. The requested object is a subgroup of positive-determinant real matrices, realized as the derivative image. The end space is prescribed up to homeomorphism; infinite genus, tameness, and absence of planar ends are explicit. Surrounding results distinguish equality from conjugacy and do not replace matrices by an abstract isomorphism class. The finite-area lattice question is separate. The apparent contraction-sign error in the displayed classification does not change Question 4's noncontracting hypothesis. [OWR](https://ems.press/content/serial-article-files/46504)

The 2017 journal paper confirms the matrix-image convention and the topology used in the candidate. I checked its introduction, Theorem 1.2, and Section 1.4, including Definition 1.14. The positive theorems cover specified end spaces, not arbitrary closed Cantor subsets. In particular the finite three-point case is not licensed by a theorem for characteristic system `(k,1)`. Its cone definition allows finite and infinite cyclic completion models. [RMV](https://msp.org/agt/2017/17-1/agt-v17-n1-p15-s.pdf)

ARSVW v2 supplies an independent source-level crosscheck: Theorem 1.8 gives the nondisplaceable-subsurface finiteness obstruction, Corollary 2.19 gives proper discontinuity, Definition 3.1 has no flat-completeness requirement, and Section 3.1 defines the isometry subgroup by rotational derivatives. I inspected these statements, the proof of Theorem 1.8, and rendered pages 13–14. This matches the candidate's attribution. Its self-similar and virtually-cyclic realization statements retain their topological hypotheses. [ARSVW v2](https://arxiv.org/html/2311.00158v2)

The v2 submission date is 23 February 2026; the PDF's internal manuscript date is 20 February 2026. These are different dates for different purposes, not a discrepancy. The author's page currently describes the work as forthcoming in Algebraic & Geometric Topology. The candidate accurately avoids claiming inspection of a final journal version. [Version record](https://arxiv.org/abs/2311.00158v2), [author publication page](https://m-artigiani.github.io/research/papers/)

The original Loch Ness monster paper's public abstract additionally confirms that the relevant forbidden contractions have operator norm less than one. No contraction ambiguity affects an orthogonal witness. [PSV](https://numdam.org/articles/10.5802/aif.2625/)

## 2. Surface, singularity, and conformal audit

The topological object used for the end condition is consistently the underlying surface, not its metric completion. This is essential and is handled correctly.

1. On the regular locus, translation charts immediately define a complex atlas and a holomorphic one-form.
2. At a finite cone of angle `2*pi*k` that belongs to the underlying surface, a root coordinate `w` gives developing coordinate proportional to `w^k`. Thus the complex atlas extends over the cone.
3. If a convention omits finite cone points from its underlying surface, there is already a complex atlas on that exact surface. Adding completion points could change ends, but the proof does not add them.
4. Infinite-angle completion points are not ordinary manifold points and are not silently added. Their local completion behavior is irrelevant to uniformization of the original Riemann surface.
5. A rotational affine map is locally `z -> lambda*z+b`, with `|lambda|=1`, and is holomorphic on the regular locus. At an included finite cone, continuity in a local target root coordinate gives a bounded punctured holomorphic map. The removable-singularity theorem extends it, and the same argument extends the inverse. The result is a biholomorphism, not merely a continuous map.
6. Rotational affine maps preserve path lengths and hence intrinsic distances; the inverse supplies the opposite inequality. Completeness of the flat metric is not used.

Consequently `I(S)=D^{-1}(SO(2))` lies in the conformal automorphism group and its derivative image is exactly `Gamma(S) intersect SO(2)`. The candidate never treats a quotient derivative group as if it automatically acted on the surface, never assumes a trivial translation kernel, and never needs a homomorphic section of the derivative map.

## 3. Uniformization and proper discontinuity audit

I checked every step of Lemma 1 rather than relying solely on the later finiteness theorem.

### Hyperbolic universal cover

An infinite-genus orientable surface has nonabelian fundamental group. By uniformization its simply connected conformal cover is the sphere, plane, or disk. Every nonidentity spherical Möbius transformation has a fixed point, so a free deck group on the sphere is trivial. In the plane, a fixed-point-free holomorphic automorphism is a nonzero translation; a deck group consisting of translations is abelian. Both possibilities are excluded. Passing between disk and upper half-plane models gives `R=H/Lambda`, with a nonabelian, discrete, free deck group in `PSL(2,R)`.

The imported deep theorem is uniformization. No assertion that the original flat metric is complete is needed: the complete hyperbolic metric comes from the conformal covering description.

### Discreteness of the normalizer

Every biholomorphism lifts through the universal cover, so the conformal automorphism group is `N(Lambda)/Lambda`. If the normalizer were nondiscrete, there would be nonidentity `n_j` converging to the identity. Choose noncommuting `a,b` in `Lambda`. The conjugates `n_j a n_j^{-1}` and `n_j b n_j^{-1}` remain in the discrete deck group and converge to `a,b`; each is therefore eventually constant. Thus every sufficiently late `n_j` centralizes both.

The centralizer in `PSL(2,R)` of a nonidentity elliptic, hyperbolic, or parabolic element is respectively a conjugate of the rotation, diagonal, or unipotent one-parameter subgroup. In each case it is abelian. The noncommuting pair cannot both centralize a nonidentity `n_j`. This proves the claimed discreteness. Torsion in the normalizer creates no exception: finite rotation stabilizers still have the stated centralizer property.

### Compact transporters in the cover and quotient

The `PSL(2,R)` action on the hyperbolic plane is proper: the stabilizer of a point is compact, and restricting source and target to compact subsets gives a compact transporter. A discrete subgroup of a Lie group is closed, so its intersection with this transporter is finite. These facts justify the candidate's compact-set form of proper discontinuity, stronger than merely asserting locally separated orbits.

For compact `K` downstairs, choose finitely many relatively compact evenly covered neighborhoods whose closures lift into compact sets upstairs. Their union is a compact `L` with projection covering `K`; there is no claim that the full inverse image of `K` is compact. For any coset `[n]` moving a point of `K` back into `K`, choose witnessing lifts `u,v` in `L`. Some deck transformation `lambda` satisfies `n u=lambda v`, so `lambda^{-1}n` lies in the finite `L`-transporter. Finitely many transporter elements represent only finitely many quotient cosets. The lift argument is correct even for infinitely generated deck groups and infinitely sheeted covers.

## 4. Nondisplaceable-core audit

The classification theorem applies to the given orientable, boundaryless surfaces using genus and the nested end/genus-end spaces. The explicit model consisting of a compact genus-zero surface with `n` boundary circles and one one-ended infinite-genus piece attached to each boundary has exactly the required invariants. Classification therefore transports its central compact connected core `K` to any surface in question. There is no extra finite-genus parameter left unspecified.

If a homeomorphism displaced `K`, its connected image would lie in one component `U_i` of `S\K`. The union of `K` with the other `U_j` is connected: each such complementary component has boundary on `K`. This union avoids the displaced core and so lies in a single component of its complement. It contains end-neighborhoods for at least `n-1` distinct global ends. For `n>=3`, that is at least two ends. But the homeomorphism carries the original `n` complementary components, each containing exactly one global end, to the complementary components of its image core. Contradiction.

This reasoning neither assumes that all compact subsurfaces are nondisplaceable nor tries to apply the same contradiction to one or two ends. The explicit negative control `n=2` correctly stops at one remaining end and produces no contradiction.

Proper discontinuity now gives only finitely many conformal automorphisms that move `K` to meet itself, while nondisplaceability says every element of `I(S)` does exactly that. Hence `I(S)` and its rotational derivative image are finite. All quantifiers needed in Proposition 3 are satisfied.

## 5. Exact matrix and admissibility audit

The witness satisfies `A^T A=I` and `det(A)=1` exactly. Every positive or negative power is orthogonal, so no element strictly shortens every nonzero vector. The group generated by one matrix is countable. The author's Cayley–Hamilton recurrence is correct:

\[
B^2-6B+25I=0,\qquad
u_0=2,\quad u_1=6,\quad u_{n+1}=6u_n-25u_{n-1}.
\]

For every positive `n`, reduction modulo five gives `u_n=1 mod 5`, whereas `A^n=I` would imply `u_n=2*5^n=0 mod 5`. This is an all-exponents induction, not an inference from bounded tests.

As an independent algebraic check, write `(3+4i)^n=a_n+i b_n`. Over the field with five elements, the two roots of `i^2+1` are `2` and `-2`. The two conjugate factors evaluate to `1` and `0`, so

\[
2a_n=(3+4i)^n+(3-4i)^n\equiv1^n+0^n=1\pmod5
\]

for every `n>=1`. Equality with `5^n` on the real axis is therefore impossible. This independently recovers infinite order using Gaussian-integer arithmetic.

The set `X` is finite, nonempty, and closed. Its three points have ternary expansions using only zero and two: `0.000...`, `0.2000...`, and `0.222...`. Thus it is an admissible three-point closed subset of the middle-thirds Cantor set. Any realizing surface would have the core above. Containment of `A` in the derivative image would force containment of its whole infinite cyclic group in a finite rotational image. This is the required contradiction.

An abstract infinite cyclic group generated by a hyperbolic or other nonorthogonal matrix is not excluded. Replacing matrix realization by abstract isomorphism would not be a valid interpretation of this verdict.

## 6. Linear-conjugacy and tameness audit

The final conjugacy remark is valid and contains the geometric step that bare bilipschitz equivalence would omit.

Postcomposing charts by `T` gives derivative group `T Gamma(S) T^{-1}`. Its metric is globally bilipschitz equivalent to the old one, so completion points are identified. Near a tame singularity, the old punctured local model is a finite-degree cyclic cover or universal cyclic cover of a punctured disk. The new developing map is the old one composed with `T`; it covers a punctured ellipse. A sufficiently small round disk centered at the origin lies inside that ellipse. Inclusion of this disk's punctured version induces an isomorphism on fundamental groups, so restricting the covering keeps it connected and preserves its degree, including infinite degree. The pullback of the new Euclidean metric on the restricted cover is the standard cone metric. Adding its completion vertex gives the appropriate finite or infinite cone neighborhood. Shrinking the neighborhood as needed rules out metric shortcuts through its exterior.

Regular completion points use the same argument with degree one. Thus no new wild completion behavior appears. This proves tameness preservation by the specific linear coordinate change; arbitrary bilipschitz changes would not prove an exact cone model.

Equivalently, a conjugate rotational group preserves the positive-definite form `Q=T^{-T}T^{-1}`. The exact independent checks include a nonorthogonal conjugate that preserves `Q` but fails ordinary Euclidean orthogonality, preventing the two notions from being conflated. The central negative answer does not depend on this optional strengthening.

## 7. Reproduction and adversarial controls

The author verifier passed with the independently supplied anchor and its exact eight-member inventory. Both ordinary and optimized Python reproduced the frozen output of 1,996 exact arithmetic checks.

The independent reviewer program imports no author arithmetic functions. It performs 3,055 checks, including Gaussian powers through exponent 1,000, exact norm and residue identities, independent binary-exponentiation checks, negative powers, a nonorthogonal conjugate preserving a positive-definite form, a finite-order rational rotation, and a determinant-one nonisometry. Its output is byte-identical under ordinary and optimized Python.

Eleven disposable-packet mutations were each rejected under ordinary and optimized verification: changed manifest bytes, changed proof bytes, missing member, extra member, linked member, linked manifest, duplicate JSON key, unsafe path, duplicate member, a false receipt with consistently rebound hashes, and a failing arithmetic program with consistently rebound hashes. The original author packet remained unchanged. The tests characterize integrity and arithmetic controls, not a security boundary against an attacker allowed to replace both the verifier and trusted external anchor.

The all-exponents, topological, and conformal conclusions rest on the written proofs, not these finite runs. No assertion about author chronology or an exhaustive novelty search was inferred from a timestamp or checksum.

## 8. Source-byte verification and limits

The three primary PDFs were independently retrieved directly from their public URLs. Their byte counts and SHA-256 hashes match the frozen source metadata exactly:

- OWR: 784,906 bytes, `b7440e2e232089cc3b69bceec50065c7af13b79b05e9a322b2d576458d29cb3c`
- RMV: 545,672 bytes, `b1f3446ea593fe99880ef6d73c4eb56376cbee6987fdb479f6f4464cb8a7675a`
- ARSVW v2: 615,894 bytes, `a8ef5ea5f5e4172e6b93db90c40aa6032b9aab828ef7589a6be02fa200faa96f`

Their page counts are respectively 74, 32, and 29. The author publication page also matches the frozen 8,219-byte record and hash. The independently retrieved arXiv abstract HTML is dynamic and is not asserted to match an earlier HTML snapshot; its version history was read directly.

The public review materials contain authored audit text, a control program, results, and public source metadata. They exclude the retrieved PDFs, extracted source text, rendered source images, and private coordination. The accepted proof appropriately credits the known finiteness principle and its classical foundations. No priority claim is certified.

## Final disposition

**Complete negative answer accepted for the exact frozen candidate; zero required proof patches; author approach count remains one.** The conclusion is limited to the stated matrix-group realization question and its proved conjugacy strengthening. It does not solve the separate Jacob's-ladder lattice or finite-area questions.
