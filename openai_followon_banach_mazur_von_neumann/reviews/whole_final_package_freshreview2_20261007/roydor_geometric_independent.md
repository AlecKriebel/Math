# Fresh independent Roydor and geometric review

Completed 2026-10-07 15:06 UTC. Internal AI subagent review for the second complete-package review. This is a geometric/dependency support report, not an independent audit of the entire upstream cohomology proof, a priority verdict, or publication clearance. No outside individual was contacted; no Git or publication operation was performed. Only this owned report and the assigned ignored temporary directory were written.

## Finding

**No substantive gap was found in the current manuscript's geometric argument, conditional on its attributed all-algebra bounded-cohomology input.** The fixed-source construction really avoids constants depending on a comparison-dependent corner. The carrier proof, odd finite type-I reconstruction, normality/order argument, arbitrary centers, arbitrary infinite cardinal dimensions, and canonical-predual deduction check out.

Roydor's literal Theorem 1.2 is restricted to a fixed algebra with separable predual. The manuscript accurately states that limitation and proves the additional scope rather than deleting a source hypothesis. His Theorem 3.2 is available without separability but requires a halving source; the manuscript applies it only to sources that meet that condition. The proof does not use his problematic compressed invocation in Lemma 4.3.

I found additional false intermediate scalar inequalities in the supplied proof of Lemma 3.1. They **do not refute any compression bound consumed by this manuscript**: a direct sharper estimate establishes those bounds throughout the lemma's stated parameter range. Details and the distinction are below. No manuscript repair is required to preserve its existential conclusion.

Completion estimate for the delegated review: 100%. This does not assign a percentage to the entire mathematical/publication objective. Publication clearance from this report: none.

## Exact material reviewed and independence

Before reading previous supporting audit records, I read the original project brief, all 449 lines of the current manuscript, and the supplied Roydor article's complete 26-page reading text. I independently reconstructed the main geometric proof and challenged its carrier and rank steps. I did not read either earlier final-review report or use a previous verdict as a premise.

At the parent reviewer's later request, after that reconstruction I read **both entire records from the actual intended ZIP**, not just their findings: `research/roydor_full_conventions_20261007.md` (415 lines) and `research/roydor_full_proof_scope_attack_20261007.md` (305 lines). Their geometric/source claims and cautions were checked against the primary source and my independent reconstruction. I did not rely on their upstream proof verdicts.

| Material | SHA-256 / exact version |
| --- | --- |
| `research/PROJECT_BRIEF.txt` | `496e4cf36100a785f53ea8015835231063cb73ec3c53dcda0d4b149f8fa81ca2` |
| Current `manuscript/main.tex`, and same entry extracted from the ZIP | `46a02c0cd03f798459a9cfd8fb1cd5e03c4e599208a2a53750d3b218b7e96dc4` |
| Actual user source `/Users/alec/Downloads/roydor2020.pdf` | `2320e92723841bd9414c4d846a489bbe78d01a03403b8078ca43354407cfacb4`; 26 pages |
| Complete `sources/roydor/roydor2020_reading_text.txt` | `66cd604671be8249af91b4009fb1d8c13a4f47f9448552d239aa5a44dba5342b`; physical page markers 1--26 |
| `sources/roydor/roydor_slides.pdf` | `b9202a2b4b3b50efc84a3430c593823f8c15404e83a2987be80083dc9028c36a`; 87 PDF pages |
| Intended `publication/upload-kit/source-and-verification.zip` | `4dc0129f59789e279318bc2e1ba53a1c3e414fda8a7ba32c8dd1d7f221aee9fc` |
| ZIP conventions report | `18f305e072e390cf327ea34c783c141b416bfdfd9d9dc8fff89cdd3946dd8b0d` |
| ZIP full-proof scope attack | `399a86004e38f81325b4c29a3ab8e68ed9c8d113082f7b90c9fae555686544a2` |

The actual supplied PDF has DOI `10.1142/S1793525321500151`, the December 9, 2020 production header, internal printed pagination 1--26, and a first-page publication date of December 11, 2020. This is the complete supplied publisher-formatted version, not evidence of a new byte comparison to a final 2022 issue PDF. I visually inspected the actual rendered printed pages 2, 7, 10--15, 19--23. I also inspected primary-author slide PDF pages 28--29 in pixels. Other Roydor pages, including the ending references, were read in the complete extraction; this report does not claim that every page received pixel inspection.

For an additional primary check of the standard projection facts, I fetched the authors' [Anantharaman--Popa notes](https://www.math.ucla.edu/~popa/Books/IIun.pdf), SHA-256 `a8cfb540a4d9154a4f6e662dfad6f0ecdf5e92a34130e3b5b81b51ce674b1726`, and read/viewed printed pp. 77--79 (physical PDF pp. 83--85). Proposition 5.5.2 states equivalence of abelian projections with the same central support; Definition 5.5.3 gives the full-abelian characterization of type I; Remark 5.5.6 supplies the product structure; Proposition 5.5.8 proves halving for any algebra without abelian projections. These passages have no separability assumption. I did not read the full cited Takesaki proof.

## Primary-source hypotheses, conventions, and attribution

1. Roydor printed p. 2, Theorem 1.2: fixed `M` has **separable predual**, ordinary `H^2(M,M)=0`, and `B^3(M,M)` closed in `Z^3(M,M)`. The comparison `N` is a von Neumann algebra; the threshold depends a priori on `M`; both distance conditions are strict. No separate separability assumption is imposed on `N`.
2. Printed p. 2 defines multiplicative ordinary Banach--Mazur distance through bounded linear isomorphisms and the product of the two ordinary operator norms. The complex field is the conventional complex C*-algebra setting, confirmed by the complex-scalar numerical-radius proof on p. 5. The manuscript explicitly states it and supplies the empty-infimum and zero-space conventions.
3. Printed p. 20 defines all bounded multilinear cochains, with their ordinary norm and the original algebra as its coefficient bimodule. The quotient uses the actual image, not a closure. Standard actual-image `H^3=0` gives `B^3=Z^3`, and `Z^3` is a closed kernel, so it supplies Roydor's weaker degree-three hypothesis.
4. The differential displayed on p. 20 is genuinely misprinted: its merge sum ends at `k-1` and its final sign is `(-1)^k`. The manuscript's corrected standard formula is appropriate. For example, the literal degree-one formula composed with degree zero at `(a,1)` gives `xa-ax`; `x=e11,a=e12` contradicts the asserted complex identity. Thus this is a printed error, not matching literal formulas.
5. Corollary 2.4 (p. 6), Lemma 2.5 (p. 7), Proposition 2.13 (pp. 10--11), Lemma 3.1 (pp. 11--13), and Theorem 3.2 (pp. 13--17) have no separability assumption. Their proofs use norm, order, functional calculus, projection, and a finite matrix-unit computation. Theorem 3.2 explicitly requires only even degrees in the finite type-I source part; its operative hypothesis is that the unit halves.
6. Claim 4's heading on printed p. 15 has the stated off-diagonal index error. The preceding p. 15 line and Claim 7 use `gij+hji`. For the exact transpose on `M2`, `g12=0`, `h12=e12`, `h21=e21`, whereas `T(e12)=e21`; this falsifies the literal heading at zero error and verifies the corrected index.
7. Lemma 4.3(2), printed p. 19, applies its earlier equivalence statement to a compressed map without ensuring its parameter and halving-source prerequisites. A corner of `M6` can be `M3`; an infinite projection in `M6 direct-product B(H)` can have such an odd finite part in its corner. Its inverse argument also needs hypotheses checked. The current manuscript bypasses both Lemma 4.3 and Theorem 1.1, so this does not enter its proof.
8. Printed pp. 22--23 write the type-I decomposition with labels in `N union {infinity}` and use a rank-`j-1` comparison. That presentation does not itself handle arbitrary infinite Hilbert cardinalities. The manuscript accurately identifies this limitation and replaces that step.
9. The unrestricted cohomological conditional implication is already printed in the primary-author slides, PDF pp. 28--29, with `H^2=H^3=0`. The manuscript's attribution to that prior announcement is accurate. This review makes no independent priority/firstness claim.

## Lemma 3.1: false printed intermediate bounds versus valid conclusions

Let `u=sqrt(t)`. The supplied proof on printed p. 12 asserts

`(1-140u)^(-1) <= 1+141u`,

and pp. 12--13 infer

`((1+t)^(-1)-986u)^(-1) <= 1+988u`.

Neither follows over the full stated `t<10^-8`. For instance `t=9.9*10^-9` gives approximately `1.014126605 > 1.014029323` in the first comparison and `1.108777469 > 1.098304759` in the second. Both are valid for sufficiently small `t`, including `t<=10^-12`. This alone would already suffice for the manuscript's existential use.

More strongly, the lemma's *consumed conclusions* have a direct repair throughout `u<=10^-4`, without these intermediate steps. Write `Ttilde(x)=qT(x)q` and `C=qT(p)q`. The forward compression estimate in the source yields

`||Ttilde^-1|| <= (1+t)/[1-742(1+t)u]`.

The positive compressed unit has `||C||<=1+t`, while unitization is `Tp(x)=C^(-1/2)Ttilde(x)C^(-1/2)`. Therefore

`||Tp^-1|| <= (1+t)^2/[1-742(1+t)u] <= 1+988u`.

After clearing the positive denominator, the last comparison is precisely positivity of

`u[246-733098u-742u^2-733097u^3]`,

which is positive for `0<u<=10^-4`. Likewise,

`||Tp|| <= (1+t)/(1-140u) <= 1+142u`

reduces to `u[2-19881u]>=0`. Spectral calculus for `C`, whose spectrum is within `140u` of the corner identity and at most `1+t`, gives

`||Tp-Ttilde|| <= (1+t)140u/(1-140u) <=244u`.

Combined with the source's `742u` compression closeness, this gives the consumed `986u` closeness. This independently verifies the sharper calculation sent by the parent reviewer. It is important to distinguish a bad displayed inference from a false theorem: the former is present here, while the latter was not established and the needed bounds survive.

The compression surjectivity mechanism also survives: inverse Jordan triple approximation shows that `T^-1(y)` is within `O(u)||y||` of `pT^-1(y)p` for `y in qNq`; hence the composed compression differs from the identity by a norm less than one for small `t`. Closed range from the forward lower bound and the resulting approximation/geometric series give onto. No normality of `T` is needed.

## Independent reconstruction of the manuscript argument

### Fixed halving source and central opposite product (lines 187--234)

Roydor supplies central orientation projections `p,q` and a unital, self-adjoint block isomorphism `F`. The direct products have their maximum norm, so the inverse bound is the maximum of the two inverse block bounds, and the total bilinear defect is the maximum of the block defects. There is no missing sum over an unbounded family of corners.

On the same target normed star space put `y diamond z=qyz+(1-q)zy`. Cross terms vanish by centrality. Each central block has its usual product or its opposite product, so associativity, unit, star symmetry, and the C*-norm identity all hold. For example `x* diamond x=q x*x+(1-q)xx*`, with norm `||x||^2` under the maximum central-product norm.

Pulling this product back through `F` yields an associative, star-compatible, original-unit product on the **same fixed source**. Its distance from the old source multiplication is bounded by the inverse norm times the block defect. Applying the self-contained multiplication correction on that source gives `F Phi^-1`, with the correct conjugacy direction. It is a star isomorphism to the changed product and a Jordan star isomorphism to the original target product. The source cohomology constants never depend on `p`, `q`, or the comparison algebra.

I checked the correction's algebraic orientation and the cochain symmetry in lines 130--184 while reading the full manuscript, but this report does not replace the independently assigned detailed deformation review.

### Full carrier order argument (lines 236--263)

The inverse map is unital and self-adjoint with the same norm bound. For `k<=w=c_D(k)`, Roydor's order estimate contributes `gamma(t)||k-w|| <= gamma(t)`. The distances from `h` to `T^-1(k)` and from `T^-1(w)` to the corresponding central `z` are each at most `(1+t)r(t)`; the latter follows already from the forward center-rounding bound by applying `T^-1`. Therefore the manuscript's bracket bound on `h-z` is conservative and correct.

Since `z` is central, `h(1-z)` is a projection. Compressing by `1-z` puts that projection below a scalar strictly less than one times the corner identity. A nonzero projection has norm/eigenvalue one, so it must vanish. Thus `h<=z`, and full carrier forces `z=1,w=1`. Applying the same argument to complements is legitimate because `T` is unital. No inverse-rounding equality at exactly the same radius is silently assumed.

### Odd finite type-I reconstruction (lines 265--317)

For arbitrary centers, finite homogeneous degree `n` has matrix form `Mn(Zn)`. The fixed projection of rank `n-1` leaves a full rank-one abelian complement. Both projections have full carrier. The fixed corner `E=eOe` consists of even finite degrees and halves, including a product of unboundedly many finite degrees. One application of fixed-source rigidity supplies a Jordan isomorphism to `qDq`; a separate compression of the complement supplies an abelian target complement with full carrier.

A full abelian projection implies that `D` is type I. Because `q` and `e` are full, center compression identifies their corner centers with the ambient centers. Restricting the exact Jordan map to the centers yields the map `beta` used in the manuscript; it need not agree with the original approximate map's center correspondence. The proof only needs this exact center map.

Both directions of a Jordan star isomorphism are positive: a positive element is a square of a self-adjoint element. They are consequently order isomorphisms, hence preserve least upper bounds of arbitrary bounded increasing positive nets. This proves normality and preserves the joins of central projections. In particular, the target projections `wn=beta(zn)` exhaust the target identity.

On `wn`, the corner has degree `n-1`; the usual homomorphism/anti-homomorphism split of a Jordan star isomorphism preserves finite homogeneous degree on each central piece. Its `n-1` equivalent abelian corner projections remain abelian and equivalent in `D`, with ambient central carrier `wn`. The complementary `wn(1-q)` is abelian with the same carrier. Equivalence of abelian projections with the same carrier therefore provides `n` orthogonal equivalent abelian projections summing to `wn`. Matrix units give `wnD=Mn(Z(wnD))`; `beta` identifies its center with the source center. This proves the asserted star isomorphism of each odd block and the bounded product isomorphism.

This check specifically excludes hidden target infinite-degree blocks, a zero complementary projection, loss of a central component, and unjustified finite-cardinal cancellation. It does not use a measurable-fiber decomposition or assumptions that the centers are separable.

### Three fixed summands, quantifiers, and infinite cardinals (lines 319--354)

The center correspondence is a star isomorphism and sends the three fixed central units to an orthogonal partition of the target unit. Compression thresholds apply uniformly to those finitely many maps. Only the at most two fixed nonzero sources `P` and `E` require cohomology/deformation constants. The corner `E` is noncentral in `O`; the manuscript correctly uses universal vanishing directly for it instead of a central-cut cohomology argument.

The type-II/type-III part has no abelian projections and halves without a countability assumption. An infinite homogeneous type-I Hilbert space splits into two equivalent halves at every infinite cardinal dimension; finite even degrees halve by matrix units. These choices assemble in the bounded central product. All infinite type-I degrees stay inside the single fixed `P`. No enumeration or comparison of arbitrary cardinal labels is required.

The finite sequence of square-root parameter changes still tends to zero with the original distortion. Its numerical geometric restrictions and the two fixed deformation thresholds can therefore be satisfied by one positive number depending on `M`, fixed before choosing `N`. Strict distance bounds allow a map below the threshold without requiring an attained infimum. Zero summands are omitted. No universal epsilon is extracted from qualitative vanishing.

### Canonical preduals and boundaries (lines 356--368)

For any bounded complex-linear predual isomorphism, the Banach adjoint between the algebras has the same norm and inverse norm. Inversion if needed puts its direction in the algebra argument, so `d_BM(M,N)<=d_BM(M_*,N_*)` is correct. It needs no normality of an arbitrary intermediate near-isomorphism. The same fixed algebra threshold therefore gives the predual conclusion.

The final exact Jordan map is normal by the order/net argument above and induces an isometric canonical-predual map. Conversely, an exact predual isometry adjoints to an algebra-space isometry; Kadison's theorem gives a Jordan star isomorphism after the possible unitary multiplier. The statement asserts existence of a Jordan map, not that every isometry is itself Jordan. Zero algebra, absent Banach isomorphism, ordinary rather than completely bounded norms, comparison restricted to von Neumann algebras, and opposite-algebra orientation all have the correct treatment.

## Assessment of the two complete ZIP audit records

The conventions record accurately distinguishes its separable-predual direct consequence from an additional extension. Its ordinary/complex/self-module/actual-image bridge, source differential warning, canonical-predual deductions, and cautions about all infinite degrees compressed to a single infinity label agree with the supplied primary source. Its central extension/restriction maps are contractive chain maps and supply uniform bounds on central corners. That mechanism is an alternative to the current fixed-source choice, not a missing requirement of the current proof.

The full-proof scope-attack record's broader closed-`B3` conditional proof is coherent: closed range yields the fixed-algebra approximation constant, central cuts pass the cohomology conditions to `P`, and the noncentral type-I `E` requires the explicitly named classical type-I input (or universal family 295). It does not silently deduce noncentral cohomology by a central-cut argument. Its product, carrier equality, reconstruction, and single-threshold arguments agree with the reconstruction above. Its caution against deducing norm-one primitives or universal numerical thresholds from qualitative all-algebra vanishing is appropriate. The current manuscript uses stronger `H2=H3=0` on its two sources and does not rely on the auxiliary classical-type-I version of that record.

The records are appropriately limited and historical: their remaining-work statements do not certify the whole package, and this review does not adopt any asserted upstream validation as a mathematical premise. The additional Lemma 3.1 intermediate-inference observation in this report expands their source audit but does not expose a substantive error in their consumed geometric argument.

## Exact remaining scope

The strongest result independently checked here is the full arbitrary-von-Neumann-algebra geometric implication from the manuscript's attributed bounded-cohomology input, including the same-threshold canonical-predual implication. No additional geometric gap remains known to this reviewer. The actual validity of the upstream all-algebra cohomology theorem, novelty/priority conclusions, complete metadata/archive consistency, production publication, and tracker operations remain outside this assigned report and must be assessed by their responsible reviewers. No publication clearance is issued.
