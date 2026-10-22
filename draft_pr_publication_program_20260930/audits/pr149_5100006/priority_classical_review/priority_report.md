# Independent classical priority review of PR149 / k114

Prepared 2026-10-11. This review did not read sibling audit reports, execute existing research scripts, contact any individual, or mutate Git refs/index/remotes. All new artifacts and source copies are contained in this review folder.

## Verdict

**No direct earlier proof or exact least-period classification was located in the primary texts examined. Nevertheless, the full proposed classification is readily derived from Stachel's published canonical parametrization using standard Jacobi shifts and a short cyclic-divisor calculation.** The checkable derivation is in [classical_implication.md](classical_implication.md). A claim to a novel proof method is untenable. A carefully bounded claim to supplying a previously unstated focal-product corollary remains possible, but this audit does not certify novelty or absolute priority.

The key distinction is between the strongest *published statement actually found* and the strongest *consequence independently derived here*. The former is the explicit canonical parametrization and closure formula in Stachel 2022, Theorem 4.3, printed p. 1614. The latter is the entire noncircular least-period classification requested for PR149. It would be inaccurate to cite Stachel as directly proving `k114`; it would also be inaccurate to present the parametrization, Jacobi identities, cyclic products, or compact-torus pole-removal method as new.

## Exact target and prior statements

The target is `prod_i |P_i-F|`, where the `P_i` are the original boundary vertices and `F` is either fixed focus of the outer ellipse. The caustic is a strictly nested nondegenerate confocal ellipse. The least period and winding number must be coprime. No hyperbolic caustic, focal segment caustic, nonconfocal caustic, or degenerate limit is included.

| Primary source | Strongest relevant statement verified | Exact relationship and gap |
| --- | --- | --- |
| Reznik–Garcia–Koiller, *Fifty New Invariants of N-Periodics in the Elliptic Billiard*, Arnold Math. J. 7 (2021), 341–355; DOI [10.1007/s40598-021-00174-y](https://doi.org/10.1007/s40598-021-00174-y) | Section 3.1, p. 344, defines `d_{j,i}=|P_i-f_j|`; Table 2, p. 345, lists `k114=prod d_{1,i}`, `N≡2 mod4`, discovery date April 2020, proof column `?`. | Direct statement of the target as an experimentally observed invariant, explicitly unproved in that publication. It does not state the converse or classify repetitions. A table question mark is not evidence of absence of later proofs. |
| Stachel, *On the motion of billiards in ellipses*, Eur. J. Math. 8 (2022), 1602–1622; DOI [10.1007/s40879-021-00524-2](https://doi.org/10.1007/s40879-021-00524-2) | Theorem 4.3, p. 1614, explicitly parametrizes vertices by `(-a sn u,b cn u)` and gives the coprime closure relation and outer semiaxes. Lemma 5.3 and Theorem 5.4, p. 1620, give quarter-period pairing for tangent speeds/contact segments. Theorem 5.6, p. 1621, gives `prod r_i=prod l_i=lambda^(N/2)` for even `N`, and constant half-products for `N≡0 mod4`. | Theorem 5.6 directly settles `k117`, whose factors join a boundary vertex to a contact point. It does not mention `k114`. Theorem 4.3 plus standard Jacobi pole/shift facts readily yields the complete target classification; exact focal divisor identification is the missing target-specific calculation. |
| Stachel, *The geometry of billiards in ellipses and their Poncelet grids*, J. Geom. 112:40 (2021); DOI [10.1007/s00022-021-00606-2](https://doi.org/10.1007/s00022-021-00606-2) | Corollary 4.2, pp. 22–23 of 29, establishes central symmetry for even periods and odd winding, and describes conjugate billiards in the odd case. Section 4.2, pp. 24–27, proves other listed invariants. | Symmetry makes the two focal products equal for primitive even periods, but does not make either product constant. No target product is stated. |
| Bialy–Tabachnikov, *Dan Reznik's identities and more*, Eur. J. Math. 8 (2022), 1341–1354; DOI [10.1007/s40879-020-00428-7](https://doi.org/10.1007/s40879-020-00428-7) | Lemma 4.2, pp. 1349–1350, gives `dist(F_1,L) dist(F_2,L)=B^2` for each side line tangent to the caustic of minor semiaxis `B`. Theorem 4.3(a), p. 1350, proves the intended full focal-perpendicular-distance product `B^n` for even `n`. Part (b), pp. 1350–1353, proves the center-to-side product `(AB)^(n/2)` for `4|n`. | These are target Table 3's `k202` quantities. They are not original vertex distances. The published theorem contains a literal foot-notation error explained below; its intended statement and proof are clear. Neither invariant alone determines `k114`. |
| Akopyan–Schwartz–Tabachnikov, *Billiards in ellipses revisited*, Eur. J. Math. 8 (2022), 1313–1327; DOI [10.1007/s40879-020-00426-9](https://doi.org/10.1007/s40879-020-00426-9) | Published Theorem 4.1 and proof, pp. 1319–1320, establish an angular sum by complexification, boundedness, and Liouville. Published Theorem 5.1 and proof, pp. 1321–1322, establish an angular product by pole cancellation. The corresponding preprint numbers are Theorems 5 and 6. | Direct precedent for the proof mechanism. Their invariants are angular functions of a Poncelet family, not ordinary focal-distance products. The product theorem does not itself imply an arbitrary new product invariant without checking its zeros and poles. |
| Chavez-Caliz, *More About Areas and Centers of Poncelet Polygons*, Arnold Math. J. 7 (2021), 91–106; DOI [10.1007/s40598-020-00154-8](https://doi.org/10.1007/s40598-020-00154-8) | Section 2, pp. 97–98, constructs the elliptic flag curve, translates the Poncelet map on the torus, and studies cyclic meromorphic functions by zero/pole counts. Theorem 6, pp. 104–105, proves the even-period original/outer area product by pole cancellation. | Another explicit precedent for both elliptic-orbit sums/products and compact-torus arguments. The even area product is a distinct quantity; the article supplies no ordinary focal-product statement or converse. |
| Levi–Tabachnikov, *The Poncelet grid and billiards in ellipses*, Amer. Math. Monthly 114 (2007), 895–908; [2005 preprint](https://arxiv.org/abs/math/0511009) | Preprint Section 3, pp. 7–9, constructs a cyclic coordinate in which the billiard is translation; Section 4 gives the Poncelet-grid conics. | Classical dynamical and geometric infrastructure. These results by themselves do not force a general positive function's cyclic product to be constant. |
| Tabachnikov, *Geometry and Billiards* (AMS, 2005); DOI [10.1090/stml/030](https://doi.org/10.1090/stml/030) | Chapter 4, pp. 57–60, explains the invariant-curve affine coordinate and Poncelet closure. Chapter 4.2, pp. 70–72, explains the Arnold–Liouville context. | Supplies the established integrability framework; no exact focal-product theorem was found in the relevant sections. |

The published AST version was downloaded from the [NSF public repository](https://par.nsf.gov/servlets/purl/10408491), allowing exact version-of-record numbering rather than assuming that preprint theorem numbers persist.

## Short derivation and what it establishes about priority

Use caustic semiaxes `A>B>0`, focus coordinate `c=sqrt(A^2-B^2)>0`, modulus `k=c/A`, and `Delta=2 tau K/n`. Stachel gives `a=A dn(Delta)/cn(Delta)` and a vertex step `delta=2Delta`. The ordinary real focal distance is the positive factor

\[
 f(u)=a+c\operatorname{sn}u.
\]

On the `sn` torus with periods `4K,2iK'`, the two simple poles are `iK'` and `2K+iK'`. Standard half/quarter-period translations locate the two simple zeros at `3K±Delta+iK'`. The zeros differ by the billiard step `delta`, so their cyclic translates form one zero coset of multiplicity two. The poles form two cosets for odd `n`, and one pole coset of multiplicity two for even `n`. In the even case cancellation is equivalent to `3K+Delta` belonging to the orbit subgroup generated by `4K/n`, namely `(3n+2tau)/4` being integral. Coprimality forces `tau` odd and reduces this to `n≡2 mod4`. The compact-torus constancy criterion proves sufficiency; a surviving divisor and the identity theorem prove necessity on the real family. Repetitions are positive powers of the primitive product, and circles have identical focal radii.

This deduction needs no unproved geometric claim, numerical approximation, or PR149 research script. The classical steps are individually elementary once the published parametrization is supplied. The exact identification of the focal factor's divisor is useful but small. Therefore the result should be presented as a specific focal-distance application of established machinery, with its least-period converse if desired. It should not be promoted as a new invariant-discovery framework, a new uniformization, a new cyclic norm principle, or an independent new treatment of the Poncelet torus.

The identities are documented by [NIST DLMF Table 22.4.1](https://dlmf.nist.gov/22.4#T1), [Table 22.4.3](https://dlmf.nist.gov/22.4#T3), and [Eq. 22.6.1](https://dlmf.nist.gov/22.6#E1). DLMF itself points to older sources, including Whittaker–Watson and Lawden. Stachel's introduction, p. 1603, explicitly traces canonical elliptic parametrization to Jacobi (1828), King (1994), and Tabachnikov (2005), so crediting Stachel's convenient modern formula should not imply that the underlying parametrization originated there.

## Tested implications from the geometric product theorems

The numerical contact-segment invariant and perpendicular-distance invariant are insufficient to determine the ordinary focal-distance product. Here is an exact counterexample to that inference, entirely within the nondegenerate elliptical-caustic regime:

- Inner caustic: `x^2/4+y^2=1`, with `(A,B)=(2,1)` and focuses `(±sqrt(3),0)`.
- Outer ellipse: `x^2/6+y^2/3=1`, with `(a,b)=(sqrt(6),sqrt(3))` and `lambda=2`.
- Rectangular primitive 4-orbit: vertices `(2,1),(-2,1),(-2,-1),(2,-1)`. Its sides are `x=±2,y=±1` and are tangent to the caustic. At each corner the outer normal is diagonal and bisects the reflection angle.
- Diamond primitive 4-orbit: vertices `(sqrt(6),0),(0,sqrt(3)),(-sqrt(6),0),(0,-sqrt(3))`. Each side is a caustic tangent, since `4/6+1/3=1` in the dual tangency condition; the reflection law holds by axial symmetry.

For either focus the rectangle's ordinary vertex-distance product is `16`, and the diamond's is `18`. One can check this from the elementary formula `d_1d_2=a^2-(c^2/a^2)x^2` for opposite vertices. Yet both phases have `prod l_i=prod r_i=lambda^2=4` and corrected `prod dist(F,L_i)=B^4=1`.

This example does not contradict the target `n≡2 mod4` theorem. It demonstrates precisely why equality of the *other* geometric products cannot silently be substituted for the target quantity. Any successful implication needs an additional relation; the focal-divisor calculation supplies such a relation and simultaneously proves the exact residue condition.

There is also a useful local comparison. With `g(u)=A dn(u)` denoting Stachel's tangent-speed factor, paired opposite ordinary focal distances satisfy

\[
 d_F(u)d_F(u+2K)=a^2-c^2\operatorname{sn}^2u=g(u)^2+\lambda.
\]

The contact product controls products of `g` at vertex and contact parameters; it does not directly control products of `g^2+lambda`. Identifying the two functions merely by their appearance in the same elliptic parametrization would skip the exact issue.

### Bialy–Tabachnikov's printed foot notation

Printed p. 1350 defines `R_i` as the foot from the center `O` onto `M_iM_{i+1}`, then writes the factors `|F_jR_i|` in part (a). Those factors literally mean distances from a focus to the *center's* foot, which are not perpendicular distances from the focus to the line. The proof immediately invokes Lemma 4.2, whose factors are the latter, and the cited invariant `k202,a` in Reznik's table also uses the latter. The PDF page was rendered and inspected visually; this is not an extraction artifact. The same error appears in the cached May 2020 v2 preprint.

For the rectangular 4-orbit above, the center's feet are `(±2,0),(0,±1)`. Their ordinary distances to `F=(sqrt(3),0)` multiply to `(4-3)(3+1)=4`, while the printed theorem would give `B^4=1`. The correctly intended focal-perpendicular distances multiply to `1`. The report treats the intended claim as the genuine theorem supported by its proof and records the notation defect openly; it does not manufacture a focal-vertex theorem from that defect.

## Older method attribution and additional checked leads

Richard Schwartz's *The pentagram integrals for Poncelet families*, J. Geom. Phys. 87 (2015), 432–449, DOI [10.1016/j.geomphys.2014.07.024](https://doi.org/10.1016/j.geomphys.2014.07.024), already proves constancy of specified Poncelet functions by removing poles on a complex torus. The [author's February 2014 full manuscript](https://www.math.brown.edu/~res/Papers/poncelet_monodromy.pdf), pp. 5 and 12–14, makes that mechanism explicit. AST's published proof on p. 1319 directly credits Schwartz's approach. Schwartz proves monodromy invariant constancy, not arbitrary focal-product constancy; no identification of the target as one of his monodromy invariants was located. That missing identification cannot be presumed.

Jonathan King's [author-typeset full text of *Three Problems in Search of a Measure*](https://www.jonathanking.org/PDF/typeset.measures.pdf), Amer. Math. Monthly 101 (1994), 609–628, author-PDF p. 7, Eq. (1.10), explicitly gives the invariant-measure density for confocal ellipses. This corroborates the older origin of canonical coordinates. Its measure construction does not assert the target product. The PDF's text layer is garbled, so the relevant page was inspected as a rendered image.

Stachel's additional [full author preprint of *On the Diagonals of Billiards*](https://www.geometrie.tuwien.ac.at/stachel/SaoPaulo_Diagonals.pdf), DOI [10.1007/978-3-031-13588-0_2](https://doi.org/10.1007/978-3-031-13588-0_2), was downloaded and inspected. Theorems 1–3, author pp. 3–5, concern diagonal envelopes and polar lines; Theorem 7, pp. 10–11, concerns spatial focal-billiard diagonals. The final calculation explicitly reuses the canonical Jacobi parametrization of the motion paper. No ordinary vertex-to-focus product or exact period-residue classification occurs. These diagonal results do not supply a more direct implication than the published parametrization already audited. The [institutional record](https://repositum.tuwien.at/handle/20.500.12708/136175) identifies the 2022 conference and chapter pp. 19–33; the preprint cover describes a Springer volume edited in 2023, so those dates should not be conflated.

An additional lead, Dragović–Gajić, *Points with rotational ellipsoids of inertia, envelopes of hyperplanes which equally fit the system of points in R^k, and ellipsoidal billiards*, Physica D 451 (2023), 133776, DOI [10.1016/j.physd.2023.133776](https://doi.org/10.1016/j.physd.2023.133776), was checked at the public publisher preview. Its visible statements concern moments of inertia and confocal hyperplane envelopes. A complete lawful public text was not located in this audit. The separate arXiv regression paper by these authors is not a substitute. This lead remains an explicit full-text coverage gap, rather than being ruled out on its abstract alone.

The extra cached Garcia–Reznik 2021 book and their 2022 self-intersected-orbit paper were searched for focal/product leads. The relevant product discussions concern cosines and focus-inversive areas; no direct target theorem was located. This is supplementary bounded coverage, not an assertion that every formula in those works has been independently analyzed.

## Chronology, limits, and recommended wording

Verified chronology separates online publication from issue year:

1. Jacobi 1828: earlier elliptic-function Poncelet parametrization, as explicitly credited by Stachel; the original German full text was not independently audited here.
2. King 1994 and Tabachnikov 2005: invariant-measure/translation parametrization. Levi–Tabachnikov's grid preprint is dated November 2005 and its journal publication is 2007.
3. Schwartz's author manuscript is dated February 3, 2014; journal issue is January 2015: Poncelet torus pole-removal method.
4. AST: first arXiv posting January 9, 2020; published online September 9, 2020, journal issue 2022. Bialy–Tabachnikov: public v2 May 5, 2020; published online September 11, 2020, issue 2022.
5. The target table records the experimental `k114` discovery in April 2020. Its version of record was published online February 18, 2021, and leaves `k114` unproved.
6. Chavez-Caliz: published online August 14, 2020; journal issue 2021. Stachel geometry article: online October 18, 2021.
7. Stachel motion: published online January 24, 2022; issue 2022. Its exact parametrization is sufficient for the short target calculation preserved here.

The searches used primary papers, publisher pages, author-hosted texts, and institutional repositories. Absence of a keyword, dead website, table proof, catalog hit, or search result is not treated as exhaustive absence evidence. This audit did not prove that no classical general theorem is specialized to this product elsewhere, nor did it certify priority over all books, proceedings, or unindexed preprints. It also does not replace an independent adversarial proof review of the PR itself.

Suggested bounded publication positioning: **A focal-distance corollary of classical elliptic billiard parametrization, proving the experimentally recorded invariant `k114` in the primitive elliptical-caustic regime and establishing its exact least-period classification.** Credit Reznik–Garcia–Koiller for the observed invariant, Stachel for the convenient published parametrization, the older Jacobi/Poncelet literature for its origin, and Schwartz/AST/Chavez-Caliz for the established meromorphic Poncelet-invariant method. State that novelty of the specific formulation remains undetermined after this bounded primary-source audit.
