# Independent review: minimal virtual-knot realizations

**Verdict: PASS_SCOPED_PARTIAL_RESULTS.** The conditional compression-circle test is valid with its nonsplit-link hypothesis retained. The homological obstruction and the stated source distinctions are correct. The original universal realization problem remains unresolved after two substantive approaches. No mandatory mathematical correction is requested.

This separate adversarial AI review was completed on 2026-09-30 using gpt-6-astra at xhigh reasoning. It is not human peer review, and it establishes no historical priority.

## Snapshot and reproduction

- Reviewed OBSTRUCTION.md: 3f7cd405177c44d8d26064f6643d8847a9ecd86c17db22b32c1b024ac3292345
- Submitted verifier: 074e128e5d47199463301e99a0b60e41bbdef07161cc1fbb5b022083b019941c
- Submitted receipt: 6de073fa15027b7dfc9e8c952d86eeb3f278dede1245626016ca27e426b0656c
- All **2,121 submitted exact assertions** reproduced with byte-identical output in an isolated copy
- **724 independent exact diagnostics** passed

No author mathematical file was edited. The finite computations do not decide whether a link is split, locate a disk, certify minimal supporting genus, or prove the universal existence statement.

## 1. Exact original question and allowed equivalence

I checked the complete published item 20, printed p. 32, of [Fenn–Ilyutko–Kauffman–Manturov's survey](https://www.impan.pl/shop/publication/transaction/download/product/86155), including visual inspection. The problem requires a nontrivial virtual knot, a **minimal** realization in a thickened closed oriented surface, and an **unknotted** embedding of that thickening in three-dimensional space producing a nontrivial classical knot. The text explicitly credits Dye with partial progress.

The artifact preserves all three requirements. A standard genus-$g$ Heegaard surface in $S^3$, together with a product neighborhood, gives an admissible unknotted model; removing a point outside that compact neighborhood gives the required $\mathbb R^3$ realization. Applying an orientation-preserving homeomorphism to the abstract supporting surface is allowed in virtual equivalence. It need not extend over both complementary handlebodies of this fixed unknotted embedding. Thus it can change the classical knot type without changing the virtual knot or the supporting genus.

I read the complete [Kuperberg paper](https://arxiv.org/abs/math/0208039v2), particularly the topologically vertical annulus definition and Theorem 1 with its proof. Its irreducibility and uniqueness statements concern the thickened-surface complement. They do not move arbitrary ambient disks through the complementary handlebodies into the product. The artifact correctly refuses that inference.

## 2. Credited Dye result and zero homology

I checked [Dye's complete author preprint](https://arxiv.org/abs/math/0502477v1), including the definitions of intersection pairs, Theorems 4.1–4.2, the examples, and Conjecture 5.1. Theorem 4.1 on printed p. 12 was also visually inspected.

Its nonzero intersection-pair hypothesis matches the artifact. For a single knot, all meridian/longitude intersection coordinates vanish exactly when its class in $H_1(\Sigma_g;\mathbb Z)$ is zero, because the surface intersection pairing is nondegenerate. The product deformation retraction identifies this group with $H_1(\Sigma_g\times I;\mathbb Z)$. Every surface homeomorphism induces a group automorphism, so zero remains zero. No choice of symplectic basis or sequence of Dehn twists can create a nonzero algebraic intersection certificate from this class.

This does not say that geometric intersection vanishes or that classical knot type is fixed. The distinction is essential and is maintained.

The source's outstanding all-zero-pair case is correctly identified with Dye's Conjecture 5.1, restricted to the original nontrivial-knot question. The genus-zero case is already classical; Kuperberg's theorem preserves the distinction between a nontrivial classical knot and the unknot under virtual equivalence.

The torus control is valid: any embedded essential simple curve on a torus destabilizes to a simple curve on a sphere by cutting along a disjoint parallel curve and capping. Its virtual class is therefore the unknot. On the standard unknotted torus, the primitive slope $(2,3)$ is nevertheless a trefoil. The displayed determinant-one matrix and Alexander polynomial are correct. This tests the necessity of the minimal-genus restriction and supplies no counterexample to it.

Dye's fixed-diagram crossing-assignment theorem does not maintain minimal supporting genus automatically. The Kishino discussion is also faithful to the preprint: the standard diagram's trivial crossing realizations do not exhaust the allowed minimal-surface representatives. The artifact credits these results and does not relabel them as campaign discoveries. The published Dye version was not independently compared in full; the precise theorem audit uses the openly available author version.

## 3. Compression circle, framing, and the product marking

The conditional test begins with an unknotted product $N=\Sigma_g\times[-1,1]$, a null-homologous knot inside it whose image $U$ is an unknot, and an essential curve $c$ compressible in the positive-side handlebody. The surgery curve $C$ is a parallel copy on the **opposite**, negative side.

Let $D_+$ be the compressing disk. Adjoining the annulus tracing $c$ through the product and a short outer collar gives an embedded spanning disk $D$ for $C$. Its interior may intersect $U$; the proof neither removes nor ignores these intersections. The surface framing agrees with the zero framing: a parallel of the boundary can be pushed to the compressing-disk side and bounded by a parallel disk. Transport through the product annulus preserves that framing. This applies to separating as well as nonseparating compression curves; no primitive homology assumption on $c$ is needed.

I checked the delicate surgery identification directly. In an annular neighborhood of $c$, write a surface Dehn twist as
\[
(\theta,u)\longmapsto(\theta+n\rho(u),u),
\]
where $\theta$ is a circle coordinate and $\rho$ is zero near one annular boundary and one near the other. Its product extension leaves the thickening coordinate unchanged. The full disk twist across $D$ restricts to this formula throughout $D\cap N=c\times I$: the angular rotation depends on the transverse annular coordinate, not on the product coordinate. This is why the opposite-side push-off is the appropriate surgery curve.

Equivalently, surgery on the boundary-parallel copy $C$ with meridian slope $\mu+n\lambda$ changes the negative-side collar marking by the $n$-fold surface twist. The surgered negative handlebody is identified with the original one with this boundary marking. Use the product twist on $N$ and extend that same boundary twist over the positive handlebody using $D_+$. These maps agree on the boundary identifications and give a homeomorphism of the filled pair to the original standard pair, carrying the knot to $(\tau_c^{\pm n}\times\mathrm{id})(K)$. The sign depends on conventions and is immaterial to a statement for every nonzero integer power.

This supplies the required conclusion about the **pair** consisting of ambient manifold and supporting product, rather than merely observing that surgery on an unknot yields $S^3$. The complementary handlebodies and the standard unknotted product are restored under the described marking. No handle is added to the supporting surface.

Since a surface homeomorphism preserves virtual equivalence and genus, minimal genus is preserved if it held at the start. This assertion does not depend on an ambient extension over both original handlebodies before surgery.

## 4. Gabai's theorem and all of its hypotheses

The original theorem used is [Gabai, *Foliations and the topology of 3-manifolds II*](https://doi.org/10.4310/jdg/1214441487), Corollary 2.5, printed pp. 462 and 471. I independently read the exact statement, its proof, and the relevant preceding Corollary 2.4 in the [indexed full primary PDF](https://scispace.com/pdf/foliations-and-the-topology-of-3-manifolds-ii-4bywlfmfgl.pdf).

The statement excludes a solid-torus result for **every nontrivial surgery** on a winding-zero knot in a solid torus that is not contained in a three-cell. Its proof uses a norm-minimizing surface with outer meridional boundary and the exceptional-filling result. There is no additional hyperbolicity hypothesis to impose on the present conditional application.

All hypotheses are satisfied:

1. $V=S^3\setminus\operatorname{int}\nu U$ is a solid torus because the starting image $U$ is an unknot.
2. $C$ is disjoint from $N$. A bounding integral two-chain for $K$ inside $N$ is therefore disjoint from $C$, so $\operatorname{lk}(U,C)=0$. This is the winding number of $C$ in $V$.
3. If $C$ lay in a three-ball in $V$, its boundary sphere would separate $C$ from $U$ in $S^3$. The assumed nonsplit link rules this out.
4. For $n\ne0$, the primitive slope $\mu+n\lambda$ differs from the meridian; their intersection number has absolute value $|n|$. The zero-framing identification above makes it exactly the stated $1/n$ filling.

Gabai therefore shows that the exterior of the image of $U$ after surgery is not a solid torus. The ambient filled manifold is $S^3$, and an unknot there has solid-torus exterior, so the resulting knot is nontrivial. This applies to every nonzero integer $n$, including negative powers. Nothing is asserted for $n=0$.

The deep foliation result is a credited import, not independently reconstructed. A PDF screenshot request for the Gabai mirror failed with a cache error, and I did not obtain a usable local PDF for visual verification. This access limitation is accurately disclosed in the author's sources and remains explicit in this review. The indexed primary text does give the precise corollary and proof.

## 5. The unresolved step is genuinely geometric

The artifact does not prove that a nonsplit compression-circle link exists for every nontrivial null-homologous minimal representative. It also correctly explains why the apparent converse from minimality is unsupported.

Minimality forbids a suitable disjoint essential vertical annulus **inside** the product complement. A disk or splitting sphere for a curve in the ambient knot exterior may travel outside the product. Separate disks for separate curves need not be compatible or movable into the product. No source theorem read in this audit bridges that gap, and the conditional proof does not use such a bridge.

The first-homology calculation cannot replace the geometric hypothesis. The relation imposed by filling is $(n\ell,1)$ in the meridian basis, where $\ell=\operatorname{lk}(U,C)$. It is primitive, so the quotient is always infinite cyclic. When $\ell=0$, it only kills the $C$ meridian. Both trivial and nontrivial classical knot exteriors share this first homology. The artifact states this limit correctly.

## 6. Checks and final disposition

The independent controls use matrix transvections and their products, nondegeneracy of intersection coordinates, explicit determinant-one surgery markings, the local product-annulus twist, an integral quotient map for the filling relation, and a Seifert-matrix derivation of the trefoil Alexander polynomial. They are independent algebraic diagnostics, not tests of the missing topology.

From this directory:

    python3 independent_checks.py
    python3 author_replay/verify_obstruction.py > author_replay/replayed_verification.json
    cmp author_replay/verification.json author_replay/replayed_verification.json

The independent checker uses SymPy; the submitted checker uses the Python standard library. Both retain the reviewed snapshot as a sibling dependency.

Recommended campaign disposition: **unsolved, 2/5**, with the conditional compression-circle result and all source-access qualifications preserved. No mandatory correction remains. This pass approves the scoped partial assertions and the honest gap; it is not a full resolution or a novelty certificate.
