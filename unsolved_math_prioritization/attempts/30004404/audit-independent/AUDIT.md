# Independent adversarial audit: figure-eight surgery counterexample

Problem 30004404, catalogue label OWR-17471-010, queue rank 611.
Audit date: 4 October 2026 (UTC).

## Verdict and binding

**PASS: the frozen candidate gives a correct negative answer to the literal universal question. No mathematical correction is required.**

This verdict binds only to the package whose `FROZEN_MANIFEST.json` has SHA-256

`4f6575af14a3e8b72e61202c45e411b4febcaa7770c3e7e8af45576eda6218f8`.

All ten listed file lengths and SHA-256 hashes were independently checked. The directory contains exactly those ten files and the manifest. No frozen candidate file was changed. This audit is an independent reasoning and source-verification pass; it is not formal proof-assistant verification or human peer review.

The accepted conclusion is: there exists a hyperbolic knot with no finite nonmeridional surgery for which no rank-two free subgroup injects under every rational filling. The witness is the figure-eight knot, and the obstruction already occurs at slope zero. This does not establish novelty or answer whether some other hyperbolic knot has a persistent rank-two free subgroup.

## 1. Claim and source quantifiers

Let `G = pi_1(E(K))` and let `N_r` be the normal closure of the primitive peripheral element `mu^p lambda^q`, for `r=p/q`. The assertion being refuted is

`For every eligible K, there exists H <= G, H isomorphic to F_2, such that H intersect (union over r in Q of N_r) = {1}.`

The independent visual inspection of [S1], printed pp.491-493 (PDF pages 27-29), confirms standard meridian-longitude coordinates, the filling-kernel exact sequence, the hyperbolicity/no-finite-surgery hypotheses, and a union indexed by all rational slopes. The final question has no all-but-finitely-many qualification. Zero is included; infinity is excluded. The surrounding discussion is consistent with nonmeridional surgery throughout. [S1](https://ems.press/content/serial-article-files/46844)

Set-theoretically, `H intersect union_r N_r = union_r (H intersect N_r)`. Thus the target requires `q_r|H` to be injective for every `r`. It does not merely require injection into a product of filling groups. A nontrivial element killed by one filling is sufficient to defeat a candidate subgroup. The killed element may depend on that subgroup and its chosen free basis; a single uniform ambient word is unnecessary.

The proof refutes the universal claim with one eligible knot. It neither replaces the target by a special-case theorem nor needs to show that every eligible knot fails.

## 2. Source verification and topology inputs

All six source PDFs were independently downloaded from the recorded URLs. Every downloaded byte length and SHA-256 matched `SOURCE_RECEIPTS.json`; see `SOURCE_RECHECK.json`. Relevant pages were independently rendered and visually inspected. Source PDFs, screenshots, extracted full texts, and imported corpus files are excluded from this audit deliverable.

### Hyperbolicity and the complementary slope class

Thurston's Chapter 4, especially Section 4.3, constructs the complete figure-eight hyperbolic structure. Theorem 4.7, printed p.61 (PDF page 19), gives hyperbolicity outside the meridional and nine rational exceptions. Its presentation identifies opposite signs through an orientation-reversing symmetry, so the number of listed homeomorphism types must not be mistaken for the number of rational slopes. The result applies to all rational coefficients, including nonintegral ones. The same page explicitly supplies the sign symmetry used for the negative exceptional coefficients. [S2](https://library.slmath.org/nonmsri/gt3m/PDF/4.pdf)

Brittenham-Wu, Theorem 1.1(4), PDF pages 1-2, independently lists precisely the rational exceptional set `{0, +/-1, +/-2, +/-3, +/-4}`, with `0,+/-4` toroidal and the remaining six Seifert fibered. The paper's introduction fixes ordinary rational meridian-longitude slopes and omits infinity. The author PDF is an older preprint, identified as such in the candidate; the classification is not being inferred from numerical software. [S3](https://homepage.math.uiowa.edu/~wu/papers/p32.pdf)

### Seifert exceptional slopes

Gukov-Manolescu, Section 9.4, printed/PDF p.71, displays Seifert data with cone orders `(2,3,7)`, `(2,4,5)`, and `(3,3,4)` at positive slopes `1,2,3`. The candidate correctly avoids the erroneous negative-slope subscript in the middle displayed equality. The negative-slope groups have the same relevant properties by the sign symmetry already checked in S2. [S5](https://web.stanford.edu/~cm5/surgeries.pdf)

For a Seifert fibration with base `S^2(a,b,c)`, killing the regular fiber yields the orbifold presentation

`<u,v,z | u^a = v^b = z^c = uvz = 1>`.

Therefore the manifold group surjects onto the triangle group. The exact orbifold Euler characteristics are, respectively, `-1/42`, `-1/20`, and `-1/12`. A hyperbolic triangle with the specified angles has an infinite discrete reflection group; its index-two orientation-preserving subgroup realizes this triangle group. Hence each of the six filled manifold groups is infinite. The proof does not wrongly infer infinitude from the phrase "Seifert fibered" alone: spherical Seifert bases would fail that inference.

### Zero filling

Khoi, Section 3.1, printed p.524 (PDF page 6), unambiguously identifies figure-eight zero surgery as a torus bundle. [S4](https://math.ac.vn/public/uploads/files/0803519.pdf)

Thurston, printed p.70 (PDF page 28), gives the mapping-torus model with matrix `[[2,1],[1,1]]`. The first surgery-coordinate glyph really is D-shaped in the inspected edition, followed by an explicit discussion of coordinates `(0,1)` and `(0,-1)`. The candidate's warning is accurate. Its identification does not rest on silently interpreting that glyph: S4 directly supplies zero surgery. No particular monodromy matrix is needed for the obstruction. [S2](https://library.slmath.org/nonmsri/gt3m/PDF/4.pdf)

### Exhaustion of all rational finite-surgery possibilities

The exhaustive deduction is valid:

1. If `r` is outside the nine exceptional rational slopes, the closed filling is hyperbolic. Its fundamental group is infinite: a finite-sheeted universal cover of a compact manifold is compact, whereas hyperbolic three-space is not.
2. For `r=0,+/-4`, the toroidal classification supplies an incompressible torus and hence an injected `Z^2`, so the group is infinite. Zero also has an independent infinite cyclic quotient from its bundle structure.
3. For `r=+/-1,+/-2,+/-3`, the infinite triangle-group quotient above proves infinitude.

These mutually exclusive cases cover `Q`. The meridional `S^3` filling has finite group but is outside the hypothesis and the union. The candidate has verified the no-finite-surgery premise, rather than merely checking that zero surgery is infinite.

## 3. Independent algebraic proof

A torus bundle over a circle has the exact sequence

`1 -> Z^2 -> pi_1(M) -> Z -> 1`.

The injection on the left follows from the homotopy exact sequence and `pi_2(S^1)=0`. Exactness puts the commutator subgroup inside the abelian kernel. Consequently `pi_1(M)''=1`; equivalently it is metabelian. A lift of the generator of `Z` splits the extension, although splitting is not needed for the commutator argument. In particular, the group is infinite because it surjects onto `Z`.

Now let `H <= G` be any subgroup isomorphic to `F_2`, with free basis `a,b`. Write `[s,t]=s t s^-1 t^-1`, and put

`c=[a,b], d=a c a^-1, w=[c,d]`.

Both `c` and `d` belong to `H'`. Under a homomorphism to a metabelian group their images belong to an abelian commutator subgroup, so the image of `w` is the identity.

In the free alphabet `x,y,X=x^-1,Y=y^-1`, independently cancelling the expanded word gives

`xyXYxxyXYXyxxYXX`.

It has 16 letters and no adjacent inverse pair. It is nonempty, so it represents a nonidentity element in the free group. By the free-basis isomorphism it remains nonidentity in `H`, and because `H` is a subgroup it remains nonidentity in `G`. Thus `w` lies in `H''` and is a nontrivial element of `H intersect ker(q_0)`.

The candidate's stronger assertion `H'' <= ker(q_0|H)` is also valid: homomorphisms carry derived subgroups into the corresponding derived subgroups of the codomain. The displayed word is used only to show that `H''` is nontrivial.

Combining this with the verified topology gives

`{1} != H intersect N_0 <= H intersect (union over r in Q of N_r)`

for every rank-two free subgroup `H` of the figure-eight group. This is exactly the required counterexample. There is no circularity, unproved injection from a quotient, or reliance on a finite enumeration of subgroups.

## 4. Reproduction and independently implemented controls

Run from this directory:

`python3 independent_checks.py`

An optional first argument selects the frozen package directory. The script requires only the Python standard library and reads the candidate without changing it. Compare its standard output byte-for-byte with `independent_results.json`.

Checks performed:

- Manifest binding, all ten file sizes and hashes, and exact package inventory.
- The original author control script reproduces `controls/expected.json` byte-for-byte: 30,625 ordered pairs, 29,464 noncommuting pairs, and the reported exact word/arithmetic results.
- Independent free-word reduction uses repeated string erasure, not the author's stack implementation.
- Independent group tests use full three-by-three homogeneous integer matrices and cofactor inverses, not the author's `(vector, exponent)` multiplication implementation.
- Five monodromies are tested: the figure-eight hyperbolic matrix, identity, a unipotent matrix, a reflection of determinant minus one, and a rotation. All 10,125 ordered parameter pairs satisfy the witness identity. Each nonidentity model has noncommuting examples, while the identity model is abelian.
- Negative powers and two-sided inverses are checked. The formal derivation, rather than these bounded model cases, proves the group law for every torus bundle.
- A non-metabelian matrix evaluation of the same word is nonidentity: its upper-left block is `[[22145,-100992],[8448,-38527]]`. This rejects an implementation that accidentally forces the word to vanish in every ambient group. It also supplies an independent certificate that the formal word is nontrivial, without needing to assert freeness of the matrix generators.
- Orbifold characteristics are recomputed using common-denominator numerators. The Euclidean `(2,3,6)` and spherical `(2,3,5)` controls give `0` and `1/30`.
- The exceptional partition and rational-slope boundary controls pass. These are consistency checks against cited classification, not a computation proving that classification.

For finite-order monodromy the matrix model identifies some different exponent parameters. The results are therefore accurately labeled parameter pairs; no faithfulness or exhaustive group enumeration is claimed. This limitation does not affect the independently proved universal law.

## 5. Adversarial alternatives and failure conditions

The following plausible misreadings were specifically challenged and rejected:

- **Replace union by intersection:** that would be a different, much weaker assertion. The printed source has a union.
- **Remove zero as a trivial surgery:** in the source convention infinity is the meridian; zero is longitude filling and remains admissible.
- **Equate infinite with containing a free subgroup:** the zero group is an explicit infinite metabelian counterexample to that inference.
- **Check only generators:** injectivity on two chosen elements is insufficient; the second-derived word necessarily dies.
- **Treat all exceptional fillings as finite:** their types and infinite-group arguments were checked separately.
- **Check only integer slopes:** the complementary hyperbolicity theorem covers every remaining rational slope.
- **Infer negative-slope bases from the mistyped middle equality:** the candidate instead uses independently documented sign symmetry.
- **Require one ambient word for all subgroups:** the negated existential statement permits a basis-dependent witness for each subgroup. The slope zero is fixed for all of them.
- **Rely on abelianization or numerical testing:** the topological group is metabelian, generally nonabelian. Exact negative controls confirm this distinction; the universal conclusion is proved symbolically.

Any modified question excluding zero, allowing finitely many exceptional fillings to be ignored, or imposing additional hypotheses on all filling groups needs separate analysis. This audit does not promote such a modification to solved status.

## 6. Later literature and priority

The April 2026 preprint's definition requires every nonidentity subgroup element to survive all nonmeridional fillings. Section 7.1 says that no hyperbolic examples are known to the authors, then Question 7.1 is formally worded with an arbitrary hyperbolic `K`. It is not literally an existential quantifier over `K`, and it does not print a no-finite-surgery qualification. The frozen candidate correctly separates the literal universal reading from the independently meaningful question of whether at least one hyperbolic knot admits a persistent `F_2`. The present negative example leaves that existence question unresolved. [S6](https://arxiv.org/html/2604.01697v1)

The 2024 cyclic-persistent paper's publisher abstract concerns cyclic subgroups and does not assert the rank-two result. Its full text remains subscription-restricted in this audit and was not used. [Publisher record](https://link.springer.com/article/10.1007/s40590-024-00674-9)

Independent bounded searches used exact title/identifier terms and combinations of persistent subgroups, figure-eight, solvable/metabelian, and finite surgery. They did not locate a directly stated prior negative answer to the exact OWR formulation. This is not evidence sufficient to establish historical novelty: terminology differs across papers, search indexing is incomplete, and the 2024 full text was not inspected. The ingredients are classical and the deduction is short. A correct counterexample can justify a qualified queue disposition without implying a new theorem of substantial novelty.

## 7. Required corrections, recommendations, and stopping condition

Required mathematical corrections: **none**.

Required scope restrictions are already present in the frozen package and must be preserved in any publication or queue summary:

1. Identify the solved target as the **literal universal OWR statement**.
2. Do not claim that no hyperbolic knot has a persistent free subgroup.
3. Do not claim a first solution or novel topological classification.
4. Do not describe finite controls as a formal proof or an all-slope computation.
5. Do not characterize the printed 2026 question itself as formally existential; refer instead to the separate existential problem motivated by its context.

A `claimed_solved` disposition at the recorded `1/5` attempt count is mathematically supported for this exact target, subject to the repository's separate current-state/publication gate. This audit did not check current remote conflicts, write to GitHub, create a release, contact an individual, or authorize those actions. It does not alter historical source assessments.

Audit stopping condition reached: all essential logical steps, source quantifiers, topology dependencies, exceptional cases, explicit word, original controls, independently implemented controls, manifest binding, and stated scope/novelty qualifications have been checked. No mathematical blocker remains for the literal claim.
