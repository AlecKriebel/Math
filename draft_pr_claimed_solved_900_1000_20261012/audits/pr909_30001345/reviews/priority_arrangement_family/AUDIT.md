# Primary priority audit: classical arrangements and their contraction

Audit target: claimed-solved PR909, problem30001345, original head d186dea31791cd3e8acf6829e0b65d01849623b8. This is an independent priority family, begun after the root mathematical gate PASS. The other priority family was neither read nor contacted. This audit makes no change to the original packet and performs no publication action.

## Verdict

**Priority is not cleared as a new research result.** Affirmative primary evidence shows that the arrangement, its delta-constant deformation mechanism, and the ordinary-point rough-invariant calculation predate the candidate. The exact accepted assertion is an elementary corollary of those ingredients. In particular, the dual Hesse configuration already appears as a picture deformation in de Jong-van Straten (1998), and the identical scaling-of-constant-terms mechanism is explicitly described by Plamenevskaya-Starkston (2023).

This is **not** a finding that an earlier author explicitly announced the numerical inequality 7<12 as an answer to Oberwolfach Question3. I did not locate that stated conclusion. Nor is the absence of such a hit evidence of firstness. The defensible publication route, if desired, is an attributed clarification or worked corollary, with a candid statement that the link to the literal unrestricted summed question is the observation being presented. The current packet's precise mathematics remains supported; this audit found no mathematical contradiction requiring repair.

## Exact hypothesis under review

The accepted claim concerns only the sum of local **rough** invariants bar-M=K(K+D), D=C'+E_red, for unrestricted reduced multibranch plane-curve deformations in a common transverse ball. The central ordinary ninefold point has delta36 and bar-M7. Every small nonzero fiber has twelve ordinary triples with total delta36 and total bar-M12, and its simultaneous normalization has nine disks. The optional classical 3n-line arrangement yields excess n^2-4 for every n>=3.

This does not settle a marked-section property or the published 2014 parametric Conjecture3.8. Definition2.1 of that paper requires a rational deformation **and a unibranched central fiber**. Nine disks have total geometric genus zero but do not satisfy that second requirement. The 2009 arXiv v3 and 2014 journal body are different versions; the journal conjecture is absent from v3.

## Affirmative primary evidence and exact implication

| Primary source | What its body actually supplies | What this audit infers |
|---|---|---|
| Hirzebruch, 1983, pp119,121,133 | The arrangements A_3^0(n) have 3n lines, n^2 ordinary triples and three n-fold points, with the n=3 collision of categories explicitly resolved as twelve triples. The nine-point flex configuration is dualized; the quadratic arrangement polynomial is evaluated. | The candidate incidence data, including the universal family, are classical. |
| Hirzebruch, 1985, p138 | The same counts and the explicit equation (z0^n-z1^n)(z1^n-z2^n)(z2^n-z0^n)=0, including n=3. | The optional all-n equation and combinatorics were explicitly published decades before the candidate. |
| de Jong-van Straten, 1998, Def4.2 p476, Theorem4.4 pp477-478, Def4.6/Lemma4.7 p480, Ex6.6 pp503-504 | Decorated-curve deformations are delta-constant, with product normalization in Def4.2; picture fibers have ordinary multiple points. Ex6.6 uses exactly the dual Hesse nine lines and twelve triples, with a complete incidence list and no other intersections, to construct a smoothing with infinite fundamental group. | The exact underlying nine-to-twelve configuration occurs inside the published delta-constant picture-deformation framework, rather than merely in a static arrangement table. That paper does not evaluate the later rough invariant or identify OWR Question3. |
| Borodzik-Zoladek, 2007-dated author preprint of the 2008 paper, Ex2.14 p6, Prop4.1/Remark4.2 pp20-23 | Pairwise transverse smooth branches impose r-2 external conditions; the rough invariant equals K(K+D). A multibranch shift from Orevkov's convention is explained. The full relevant proof, not just the statement, was inspected. | Ordinary r-fold bar-M=r-2 was available independently of this candidate. The retrieved author version is not falsely labeled the journal PDF. |
| Borodzik, published 2014, pp575-578 | The deformation model, the exact rough definition, branch-convention warning, the parametric conjecture, and a projective-curve contraction argument retaining all singularities in a small transverse ball. The ordinary d-fold rough value d-2 is explicitly used on p578. | The candidate's contraction strategy and ordinary-point evaluation have a direct published precedent in the target author's own paper. The high-genus Hirano example used there does not itself settle the delta-constant target. |
| Plamenevskaya-Starkston, 2023, Def2.7 p1109, Ex7.2 p1157, Lemma7.5/proof pp1159-1161, Ex8.7 p1194 | The definition includes delta constancy and simultaneous normalization. Distinct affine slopes/no intersection at infinity are discussed. Ex8.7 explicitly obtains a pencil from any straight-line arrangement by scaling constant terms of the line equations to zero. | This is the same algebraic mechanism as the candidate, already explicitly stated before October7, 2026. |
| Roulleau-Urzua, 2015, Prop3.1 and full proof pp291-292 | The nine-line equation and twelve triples occur through an elliptic-quotient construction. The p290 acknowledgement attributes the proposition to Comessatti through Catanese-Ciliberto1993 Section2. | This is a useful modern proof and attribution, not evidence that the arrangement or deformation first appeared in 2015. |

The inference in the last column is the audit's reasoning, not a historical quotation.

### Checkable contraction lemma

Let A be a reduced arrangement of d>=2 projective lines. Choose an infinity line avoiding every pair intersection. This is possible because there are finitely many intersections. The affine lines ell_i=a_i x+b_i y+c_i=0 then have distinct directions: parallelism would place their projective intersection at infinity. Define

F(x,y,t)=product_i(a_i x+b_i y+t c_i).

For t!=0, the fiber is t times the affine arrangement. At t=0 it is an ordinary d-fold point with **its own** distinct tangent directions. No analytic equivalence to the special polynomial x^d-y^d is required or asserted. Ordinary multiple points of fixed multiplicity have tangent-direction moduli; the rough and delta calculations depend only on the ordinary type.

After a generic linear coordinate change all a_i are nonzero. F, divided by a constant, is monic in x, so the family is algebraically flat. Its component planes are graphs over (y,t). Their disjoint union is finite over the reduced total space, is normal, and restricts fiberwise to the disjoint smooth line normalizations. It is therefore a simultaneous normalization.

All finitely many intersection points scale by t. In one fixed ball, for sufficiently small complex |t|, all are inside half the radius. The distances of the affine lines from the origin are O(|t|). Each restricted line is a disk and meets the sphere transversely; the boundary circles are disjoint because all intersections lie in the interior. The same statement holds at zero, whose central curve is a cone. Thus one retains all singularities without losing delta through infinity or the boundary.

If t_r denotes the number of ordinary r-fold intersections of A, pair counting gives

sum_{r>=2} binom(r,2)t_r=binom(d,2).

This proves delta constancy directly, including the reducible case. On the one-blowup embedded resolution of an ordinary r-fold point (r>=3), E^2=-1, K=E and D.E=r-1, hence K(K+D)=r-2. A node has rough value zero, consistent with the same expression. Consequently the summed excess in this classical contraction is

sum_{r>=2}(r-2)t_r-(d-2).

For dual Hesse, d=9 and t3=12, giving delta36 on both sides and excess12-7=5. For the classical 3n-line arrangement, with the n=3 overlap counted only once, the moving sum is n^2+3(n-2), the central value is 3n-2, and the excess is n^2-4. Its delta identity is

3 binom(n,2)+3n^2=binom(3n,2).

This is a universal algebraic deduction, not an inference from finitely many numerical tests. At n=2 the same incidence family gives zero excess; the claimed strict range n>=3 is correct. The central tangent directions are arrangement dependent throughout.

These calculations show that the exact accepted counterexample is immediately supplied by classical incidence data plus the published ordinary-point value and standard scaling. No new deformation or invariant technology is needed. The candidate's explicit unit-ball constants and reproducibility packet are useful verification details, but no primary source evidence supports calling their underlying mechanism new.

## Why related global inequalities do not rescue a novelty claim

Hirzebruch1983 Section3.1 pp132-133 defines f0=sum t_r and f1=sum r t_r. Its arrangement polynomial has coefficient f1-2f0, exactly sum(r-2)t_r. Thus even the weighted incidence sum underlying this audit is a classical numerical arrangement quantity. For dual Hesse, the polynomial is 3(x-4)^2. The log-Chern method accepts this example; it does not imply the false bound sum(r-2)t_r<=d-2.

Langer's current arXiv math/0012180v1 (submitted2000, retrieved complete) Section11.3 pp35-36 derives incidence inequalities from orbifold BMY and explicitly reuses the 3n-line family as an equality example. Its hypotheses exclude overly large pencils and its quantities are incidence sums. It is a strong independent pre-candidate confirmation of the all-n combinatorics, not a source asserting rough semicontinuity. The published article is Proc London Math Soc86(2003)358-396, DOI10.1112/S0024611502013874; this audit inspected the arXiv mathematical version, not a claimed byte-identical journal body.

Orevkov2002 Sections1-2, and the Borodzik-Zoladek body, concern rational cuspidal or parametrized irreducible curves when deriving their global degree/codimension bounds. A reducible union of many lines is not licensed by the phrase rational curve in those theorems. Also, Orevkov's multibranch extension of mu+(K+D)^2 differs by r-1 from the target K(K+D), as the 2014 Remark3.4 explicitly warns. Transferring a theorem by name alone would mix hypotheses and conventions.

For context, blowing up all r>=3 intersections of a line arrangement in P2 gives K_Y=-3H+sum E_p and K_Y+D=(d-3)H-sum(r_p-2)E_p. Therefore

K_Y(K_Y+D)=9-3d+sum(r-2)t_r.

This is a separate global intersection number; its relation to the local sum explains why these quantities occur in log-Chern/codimension literature. It is not itself an upper-semicontinuity theorem.

Borodzik2014 p578 already disproves an extension with a genus allowance via Hirano's high-cusp curves. That example has a genus/delta deficit and cannot simply be relabeled delta-constant. The line-arrangement specialization supplies the missing delta constancy because it keeps every pair intersection and every component normalization disk. Hence the Hirano passage is a direct mechanism precedent but not, by itself, a prior complete proof of the exact accepted delta-constant assertion.

## Historical attribution and version limits

The 2015 Comessatti acknowledgement concerns Proposition3.1, including the elliptic-quotient identification. Bauer-Harbourne-Roe-Szemberg's 2016 postprint also attributes the degree-three rational map T x T --> P2 to Comessatti and points to Catanese-Ciliberto. It separately calls the nine-line configuration classical. These should not be conflated into a claim that Comessatti first discovered the numerical arrangement or the present rough-invariant counterexample.

I followed the chain to the official Catanese bibliography. It lists Catanese-Ciliberto1993, pp89-115; the commented PDF link and the corresponding older author-directory path both return404. The Comessatti1911 DOI resolves to Springer metadata for volume31 pp369-386, but its PDF request returns an HTML article/cookie page, not the body. Some secondary and later bibliography entries contain conflicting volume or page data. The official DOI metadata is preferred for bibliographic identity; the underlying 1911 theorem was not directly checked. No earliest-history claim is made.

The 1983 and 1985 published Hirzebruch bodies independently establish the exact equation/count history relevant here, without relying on that incomplete older attribution chain. Their collection records distinguish publication dates from later archive deposits. Modern web indexing dates are not publication dates.

The 2014 journal paper was read in full. Its Assumption5.1 explicitly requires a cuspidal central fiber and cusps/nodes on nearby fibers for its knot-signature bound. That result does not apply to the candidate's ordinary-nine central point and twelve triples. The 2009v3 body was read in full as well; it permits a bunch of central disks in its general model but defines parametric as rational plus unibranched, and has no Conjecture3.8. No assertion about current openness follows from either old text.

## Adversarial checks and remaining gap

- A generic infinity line is essential. Using the standard chart of the homogeneous Fermat equation would discard some high-multiplicity intersections and would not prove the same delta count. The candidate's chosen infinity passes this test.
- The relevant central object is an ordinary topological type with its own tangent moduli. Neither this audit nor the candidate needs all ordinary d-fold analytic germs to be equivalent.
- Normalization genus zero and central unibranchedness are distinct. The former cannot remove the latter from the 2014 conjecture.
- Delta constancy is proved by the pair identity and retained finite normalization, rather than a genus formula silently assuming irreducibility.
- The unrestricted sum over all moving singularities is indispensable. No result for a distinguished section is inferred.
- The all-n family was already published explicitly. Proving the arithmetic consequence n^2-4 adds no new construction mechanism.
- The precise previously stated answer to OWR Question3 remains unlocated. This is an attribution/priority gap, not a reason to certify novelty.

Searches covered exact numeric and phrase variants, dual-Hesse/Ceva/Fermat degeneration, rough M/codimension semicontinuity, picture deformation and projective contraction, and citation chains through the critical primary bodies. Many exact phrase searches were empty or noisy because mathematical symbols and M-number tokenize poorly. Secondary snippets were used only to find primary texts. No exhaustive citation graph, paywalled MathSciNet review search, archived private preprint search, or complete older-language corpus search was performed. Source/access and search manifests preserve these limits. No author or other individual was contacted.

The strongest verified result is therefore: **the accepted mathematics is correct within its declared scope, but its construction, deformation method and numerical ingredients are preexisting; the exact counterexample is an elementary corollary.** A new-problem-solution priority claim should not be promoted from this audit. An attributed explicit note can be evaluated on its expository value, with firstness and current-openness claims omitted unless new evidence establishes them.

## Primary links

1. [Hirzebruch1983, published chapter and archive record](https://hirzebruch.mpim-bonn.mpg.de/id/eprint/244/), DOI10.1007/978-1-4757-9286-7_7.
2. [Hirzebruch1985, published article and archive record](https://hirzebruch.mpim-bonn.mpg.de/id/eprint/137/).
3. [de Jong-van Straten1998, complete published body from author archive](https://download.uni-mainz.de/mathematik/Algebraische%20Geometrie/DvS-Publikationen/Deformation%20theory%20of%20sandwiched%20singularities%20-%201998.pdf), DOI10.1215/S0012-7094-98-09513-8.
4. [Borodzik-Zoladek, 2007-dated author preprint](https://www.mimuw.edu.pl/~mcboro/pliki/artykuly/curv4.pdf), journal DOI10.1215/KJM/1250271383.
5. [Borodzik2014, complete published body](https://ir.library.osaka-u.ac.jp/repo/ouka/all/50809/ojm51_03_573.pdf), DOI10.18910/50809.
6. [Borodzik2009v3 and version record](https://arxiv.org/abs/0907.4129).
7. [Plamenevskaya-Starkston2023, complete published body](https://msp.org/gt/2023/27-3/gt-v27-n3-p04-p.pdf), DOI10.2140/gt.2023.27.1083.
8. [Langer2000v1 and version record](https://arxiv.org/abs/math/0012180).
9. [Orevkov, author body of the 2002 paper](https://www.math.univ-toulouse.fr/~orevkov/cusp.pdf).
10. [Roulleau-Urzua2015, publisher record](https://annals.math.princeton.edu/2015/182-1/p06), DOI10.4007/annals.2015.182.1.6.
11. [OWR2009 target report](https://ems.press/journals/owr/articles/4086), DOI10.4171/OWR/2009/43.
12. [Bauer-Harbourne-Roe-Szemberg2016, author postprint](https://ddd.uab.cat/pub/artpub/2016/175900/Halphen-cubics-Revision.pdf), DOI10.1007/s13348-016-0172-4.
13. [Comessatti1911, bibliographic record only](https://doi.org/10.1007/BF03018810); [Catanese bibliography](https://www.mathe8.uni-bayreuth.de/de/team/prof-fabrizio-catanese/pdf/index.html).
