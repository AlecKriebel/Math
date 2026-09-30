# Minimal virtual-knot realizations: homology and a conditional surgery test

**Original target unresolved; two substantive approaches used.** This package identifies the remaining source scope and proves a conditional test using a classical theorem of Gabai. It does not establish the missing geometric hypothesis for every virtual knot. Separate adversarial review is pending. No novelty or human peer review is claimed.

## 1. Exact question and ambient category

Item 20 on printed p.32 of Fenn–Ilyutko–Kauffman–Manturov, [*Unsolved Problems in Virtual Knot Theory and Combinatorial Knot Theory*](https://www.impan.pl/shop/publication/transaction/download/product/86155), asks whether each nontrivial virtual knot has a **minimal-genus** representative in `N=Sigma_g x I` whose image under an **unknotted embedding of N into R^3** is a nontrivial classical knot. The arXiv version is [1409.2823v1](https://arxiv.org/abs/1409.2823v1). Its truncated parenthetical reference in the imported record is restored by the published item: Dye is credited with a partial result.

Here `Sigma_g` is a closed oriented surface. The curves are tame knots in a three-dimensional thickening; this is not an embedding problem for knotted surfaces in dimension four. An unknotted thickening can be taken to be a product neighborhood of a standard genus-g Heegaard surface in `S^3`. Choosing a point outside this compact neighborhood converts the construction to `R^3`.

Surface isotopy and orientation-preserving surface homeomorphisms are allowed in representing the same virtual knot. Empty-handle stabilization and destabilization enter virtual equivalence, but the final supporting genus must be the least possible genus. The allowed homeomorphisms of the abstract surface need not extend to ambient homeomorphisms of the original `R^3` embedding. That distinction is what permits the classical knot type to change.

[Kuperberg's Theorem 1](https://arxiv.org/abs/math/0208039v2) gives the unique irreducible representative, up to the appropriate surface equivalence. Its destabilizing annuli must lie in the **thickened-surface complement** and be topologically vertical. It gives no theorem saying that every disk found later in a classical knot exterior can be moved into that product.

## 2. Prior result and the remaining homological case

The full [Dye preprint, math/0502477v1](https://arxiv.org/abs/math/0502477v1), was read, including the statements, proofs and examples. Its journal version is *J. Knot Theory Ramifications* 15 (2006), 963–981, [DOI 10.1142/S0218216506004890](https://doi.org/10.1142/S0218216506004890); the detailed theorem numbering used here is from the accessible preprint.

Dye's Theorem 4.1 supplies a knotted realization when a component has a nonzero oriented intersection pair with a handle's meridian and longitude. For a knot, the collection of these pairs is the coordinate data of its homology class in `H1(Sigma_g;Z)`, using the nondegenerate intersection pairing. Thus the source's remaining case is a positive-genus minimal representative with

`[K]=0 in H1(Sigma_g x I;Z)`.

This is the all-zero-pair case explicitly left as Conjecture 5.1 in Dye's preprint, restricted here to the original question's nontrivial knots. The nonzero-pair theorem and Dye's explicit examples are prior work, not results of this attempt. In genus zero, a nontrivial virtual knot represented there is already a nontrivial classical knot.

**Elementary obstruction to homological amplification.** If `h:Sigma_g -> Sigma_g` is any homeomorphism, then

`[(h x id)(K)] = h_*[K]`.

Consequently zero remains zero under every sequence of Dehn twists, changes of symplectic basis and isotopies. In particular one cannot bring the remaining case into Dye's nonzero-pair hypothesis merely by choosing better meridians or applying more twists. For a twist about a curve c, this is also immediate from the transvection formula `x -> x +/- <x,[c]>[c]`. The sign convention is immaterial when x=0.

This does not say that those twists preserve classical knot type. It says only that this particular **homological certificate** stays unavailable.

## 3. Why arbitrary diagram realizations are insufficient

Dye distinguishes a realization obtained by assigning over/under data to a fixed diagram's virtual crossings from the minimal-surface condition. A crossing assignment can be realized by attaching one handle at each virtual crossing, but that construction need not have minimal genus. Its later reduction can change the classical knot type. Dye's Theorem 4.2 and the examples are therefore not an automatic proof of the full item 20; the required preservation of a minimal unknotted surface must still be checked.

A simple control shows why minimality cannot be omitted. An embedded essential simple curve on a torus represents the virtual unknot: cut along a parallel disjoint essential curve and cap to obtain a sphere. On a standard unknotted torus in `S^3`, however, the simple slope `(2,3)` is a trefoil. The determinant-one matrix

`[[2,1],[3,2]]`

sends the meridional vector `(1,0)` to `(2,3)`. Thus a surface homeomorphism on a nonminimal supporting torus can turn this virtually trivial example into a knotted classical realization. The usual torus-knot Alexander polynomial is `t^2-t+1`, confirming its nontriviality. This is a control against a weakened formulation, not a counterexample to the source.

Likewise, Dye's standard Kishino diagram has only unknot crossing realizations, but Dye explicitly gives a different minimal-surface realization with a trefoil image. A finite list of trivial realizations of one diagram does not refute the existential question.

## 4. A conditional test in the null-homologous case

The following implication is useful because it separates a known surgery obstruction from the still-missing surface geometry.

**Compression-circle test.** Let `N=Sigma_g x [-1,1]` be unknotted in `S^3`, let `K` lie in its interior, and suppose `[K]=0` in `H1(N;Z)`. Assume the image U of K is an unknot. Let c be an essential simple curve on `Sigma_g` that bounds a compressing disk in the handlebody on the `+1` side. Let C be the parallel copy of c just outside N on the `-1` side. If the link `U union C` is nonsplit, then every nonzero integral power of the surface Dehn twist about c gives a nontrivial classical realization. The same statement holds with the two sides interchanged. If the starting genus is minimal, all these representatives still have that minimal genus and an unknotted supporting thickening.

Here nonsplit is a genuinely geometric hypothesis: there is no embedded sphere separating the two components. Algebraic linking zero alone is not enough.

### Proof

First C is an unknot. Indeed, the compressing disk on the `+1` side, together with the product annulus tracing c across N and a short boundary collar, gives an embedded disk with boundary C. That disk may intersect U, which is precisely the relevant issue.

The surface framing of C is its zero framing. A parallel of c can be pushed onto the compressing disk side; it then has zero linking with the original curve. The framing is transported unchanged along the product annulus to C.

The standard boundary-surgery description of a Dehn twist says that `1/n` surgery on C, relative to this surface framing, changes the boundary parameterization of the adjacent handlebody by an n-fold Dehn twist about c, with a sign depending on the orientation convention. One way to verify this local description is to cut a collar along the annulus carrying c to C. Filling with slope `mu+n lambda` reglues the collar after n full rotations; away from that annulus the identification is unchanged. The resulting collar is again a product, with its two boundary markings differing by the indicated twist.

Since c bounds a disk on the opposite handlebody, the twist extends over that handlebody by a disk twist. It follows that the filled ambient manifold is again `S^3`, its two complementary handlebodies still give the same standard unknotted thickening, and the resulting knot is the image of `(tau_c^{+/-n} x id)(K)` in the original standard model. No handle is added or removed. This is also the usual full-twist, or Rolfsen-twist, description along the spanning disk of C.

Next, `lk(U,C)=0`. The null-homology of K supplies an integral bounding 2-chain in N, whereas C is outside N. Their intersection is zero. This argument needs no claim that the geometric intersections of a spanning disk of C with U can be cancelled.

Because U is an unknot, its exterior `V=S^3 minus int(nu U)` is a solid torus. The winding number of C in V is `lk(C,U)=0`. Moreover C is not contained in a 3-ball in V: such a ball would give a splitting sphere for `U union C`, contrary to the hypothesis.

Apply [Gabai, *Foliations and the topology of 3-manifolds II*, Corollary 2.5](https://doi.org/10.4310/jdg/1214441487). For a winding-zero knot in a solid torus that is not contained in a 3-ball, every nonmeridional surgery produces a manifold that is not a solid torus. For n nonzero, the slope `mu+n lambda` is distinct from the original meridian mu. Thus the exterior of the image of U after that surgery is not a solid torus. An unknot would have solid-torus exterior, so the image knot is nontrivial.

The boundary-surgery identification gives the promised surface representative. A surface homeomorphism preserves its virtual class and its supporting genus, so a minimal starting representative stays minimal. This proves the conditional test. The only substantial surgery theorem invoked is Gabai's existing result; no new surgery theorem or priority is claimed.

## 5. The exact geometric gap

To use Section 4 to settle the source, one still needs the following existence statement:

> For every nontrivial null-homologous minimal representative, either some allowed unknotted surface embedding already gives a nontrivial classical knot, or some such unknot realization has a compression-circle push-off C whose link with that unknot is nonsplit.

This statement is **not proved here**. Minimality excludes a disjoint essential vertical annulus inside `N minus K`. In contrast, a splitting sphere or a disk witnessing that C is split can move through the complementary handlebodies, outside N. No argument here relocates such disks into N, makes disks for different curves compatible, or produces a destabilizing annulus from their separate existence. Doing so would be a substantive new geometric theorem, rather than an application of Kuperberg's uniqueness statement.

Thus even a proof that all the tested compression circles split would not by itself show that the virtual knot is trivial. Conversely, testing finitely many circles and obtaining only split links does not exclude another mapping-class representative or another compression curve. The current work constructs neither a universal nonsplit-circle certificate nor a counterexample having only trivial classical realizations.

Ordinary first homology cannot close this gap. In the exterior of `U union C`, let the meridians be `mu_U,mu_C` and put `ell=lk(U,C)`. The preferred longitude of C represents `ell mu_U`. Filling C along `mu_C+n lambda_C` therefore imposes only

`mu_C+n ell mu_U=0`.

This is a primitive relation, and the filled exterior still has first homology Z. When ell=0, it simply kills `mu_C` for every n. Both unknot and nontrivial-knot exteriors have that same first homology. Gabai's geometric hypothesis cannot be replaced by this homological calculation.

## 6. Checks, source limits and stopping point

The checker verifies exact symplectic-transvection identities, preservation of the zero class, the torus-slope control, the trefoil polynomial identity and the primitive surgery relation. It does not recognize any link as split, construct a disk, certify a minimal genus, or verify the hypotheses of Gabai's theorem for an arbitrary K. The proof of the conditional implication is in Section 4, and its missing universal hypothesis is isolated in Section 5.

The original published survey and complete Dye and Kuperberg author texts were recovered. Gabai's exact corollary and its proof were read in the indexed primary PDF; a local full-PDF download and screenshot were unavailable, as recorded in `SOURCES.md`. Current targeted searches did not locate a later full resolution, but this is not a comprehensive proof of literature status. No claim of novelty is made.

The homological route stops at the invariant zero class. The surgery route stops at the nonsplit-circle existence and disk-location problem. The original target remains **unsolved after 2/5 approaches**.
