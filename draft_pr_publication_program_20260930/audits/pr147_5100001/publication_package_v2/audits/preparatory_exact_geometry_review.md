# PR147: independent exact geometry adversarial review

**Verdict:** the submitted counterexample to the literal printed k107 assertion is mathematically valid. I found no mandatory mathematical repair. Preparatory mathematical audit: **100% complete**. Historical priority, editorial intent, a corrected all-period invariant, and publication readiness are outside this verdict.

## Independence and exact target

I initially read only the frozen `COUNTEREXAMPLE.md` and `source_record.json`. I did not read or run the submitted `verify.py`, inherited reviews, inherited results, or imported report. I independently reconstructed two rational geometric certificates, a nonsymmetric quadratic-field phase certificate, and a polynomial check of the continuous-family mechanism. The report's proofs supply the analytic sign and branch arguments that symbolic identities alone cannot supply.

The proposition under review says that, for a fixed noncircular outer ellipse and fixed confocal elliptical caustic supporting an N-periodic billiard family, `(A'/A) product sin(theta_i/2)` is constant if N is divisible by four. A universal assertion of this form is refuted by two admissible primitive four-period representatives in the same family with distinct values. No claim about all larger N is needed for that refutation.

I opened the primary arXiv v11 and journal PDFs, independently downloaded them, extracted their definitions, and rendered and visually inspected both Table 2 pages. The journal table really gives k103 as A'/A, k105 as the half-angle sine product, and k107 as their product for N congruent to zero modulo four. The preprint gives the same entry. The relevant definitions use the outer tangents at orbit vertices, signed areas, and the angles of the orbit polygon. I found no exclusion of N=4 in these definitions or this row. This source check establishes fidelity to the literal printed statement; it does not establish that the defect was previously unknown. [Journal primary PDF](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), [arXiv v11 primary PDF](https://arxiv.org/pdf/2004.12497v11).

The local copies of full primary PDFs and extracted/rendered material are inspection evidence, not a proposed licensed public supplement.

## Independent finite certificate

Use E: x²/16 + y²/9 = 1 and C: x²/(256/25) + y²/(81/25) = 1. The common confocal parameter is 144/25: subtracting either caustic semiaxis square from its outer counterpart gives 144/25. It lies strictly between zero and 9, so the caustic is a strictly nested nondegenerate ellipse with the same focal distance.

The counterclockwise vertices are

- D: (4,0), (0,3), (-4,0), (0,-3).
- R: (16/5,9/5), (-16/5,9/5), (-16/5,-9/5), (16/5,-9/5).

Every vertex satisfies the ellipse equation exactly. Each turn determinant is strictly positive. All four vertices are distinct, and a return to the original oriented state is impossible before four collisions because the initial position is not revisited earlier. Neither polygon self-intersects.

For every chord I reconstructed its line `n·X=h`, checked `h²=(256/25)n_x²+(81/25)n_y²`, reconstructed its caustic contact `((256/25)n_x/h,(81/25)n_y/h)`, and checked that the chord coordinate of this contact lies strictly between zero and one. For example, D's first contact is (64/25,27/25), at chord coordinate 9/25. R's first contact is (0,9/5), at chord coordinate 1/2. Axis symmetries yield the other contacts; the executable certificate checks each separately.

The physical reflection check uses unit velocities, rather than equal-length unnormalized chords or only visual angle bisectors. At a vertex p, the outward normal is `N=(p_x/16,p_y/9)` and the reflected incoming unit velocity is

`v_in - 2(v_in·N)/(N·N) N`.

This equals the outgoing unit velocity in all eight cases. Incoming normal projections are positive and outgoing ones negative. In particular, both trajectories have Joachimsthal constant 1/5. D's edges all have length 5; R has alternating lengths 32/5 and 18/5. Their common perimeter is 20.

Intersecting successive exact outer tangent lines gives D's outer vertices (4,3), (-4,3), (-4,-3), (4,-3). R's outer vertices are (0,5), (-5,0), (0,-5), (5,0). All intersections are finite. Exact signed shoelace areas and half-angle quantities are:

| Quantity | D | R |
|---|---:|---:|
| A | 24 | 576/25 |
| A' | 48 | 50 |
| A'/A | 2 | 625/288 |
| Product of sin(theta_i/2) | 144/625 | 1/4 |
| Printed k107 | 288/625 | 625/1152 |
| A A' | 1152 | 1152 |
| k103/k105 | 625/72 | 625/72 |

The strict exact difference is `625/1152 - 288/625 = 58849/720000 > 0`. This is enough to disprove the universal printed assertion once membership in the same family is established below.

## General noncircular ellipse and strict inequality

Let a>b>0, S=a²+b², s=sqrt(S), and lambda=a²b²/S. Define the caustic squared semiaxes as a⁴/S and b⁴/S. Then a²-a⁴/S=b²-b⁴/S=lambda, and `0<lambda<b²`. This is a strictly nested confocal ellipse for every allowed axis ratio.

The two polygons are the axis diamond `(a,0),(0,b),(-a,0),(0,-b)` and the rectangle with vertices `(±a²/s,±b²/s)` in counterclockwise order. Their points lie on the outer ellipse. A diamond side has line x/a+y/b=1 and caustic support square `a²/S+b²/S=1`. Its unique contact is `(a³/S,b³/S)`, strictly within the side. Rectangle sides are axis tangents of the same caustic and their contacts are their midpoints. These are direct tangency calculations, not an assumption that an arbitrary rectangle is a billiard.

At diamond vertices the ellipse normal bisects the two inward adjacent rays. At rectangle vertices that normal is proportional to `(±1,±1)` and bisects the adjacent horizontal and vertical inward rays. Reversing the previous inward ray gives physical incoming velocity, and reflection in the tangent line gives the next inward ray. Thus these are genuine billiards even though R's adjacent chord lengths differ.

D has areas `A=2ab`, `A'=4ab`, with successive half-angle sines b/s and a/s. Hence

`k_D = 2a²b²/(a²+b²)²`.

R has `A=4a²b²/S`, `A'=2S`, and all angles equal to pi/2. Hence

`k_R = S²/(8a²b²)`.

Writing A=a² and B=b² only for the following algebra, the independently checked difference factorizes as

`k_R-k_D = (A-B)²(A²+6AB+B²) / [8AB(A+B)²]`.

It is strictly positive because A>B>0. Also `k_D<1/2<k_R`. Equality occurs only in the circular limit, where both become 1/2. The caustic's singular limit b=0 lies outside the stated assumptions; no such limiting degeneration is used to manufacture the difference.

## Same oriented continuous family: a complete analytic check

Let c²+d²=1 and

`Delta = sqrt(a⁴d²+b⁴c²)`,
`P=(ac,bd)`,
`Q=(-a³d/Delta,b³c/Delta)`.

Delta is positive everywhere on the unit circle: its square is a positive definite quadratic form. Consequently the map

`T(c,d)=(-a²d,b²c)/Delta`

is continuous. Its new normalization denominator is `a²b²/Delta`; taking the positive square root is justified by a,b,Delta>0. Thus `T²(c,d)=(-c,-d)` and `T⁴(c,d)=(c,d)`. The four orbit vertices are P,Q,-P,-Q. They all lie on the outer ellipse because Q's normalized squared coordinates sum to `(a⁴d²+b⁴c²)/Delta²=1`.

Moreover

`det(P,Q) = ab(a²d²+b²c²)/Delta > 0`.

This implies four distinct vertices, a strictly convex counterclockwise centrally symmetric quadrilateral, and primitive period four. The map is a single orientation-preserving map of the whole circle: it comes from the linear map with matrix `[[0,-a²],[b²,0]]`, whose determinant is positive, followed by radial normalization. Since its successive angular displacements lie strictly between zero and pi, it follows the same orientation and winding branch throughout.

Here is an independently checked tangency identity without trigonometric numerics. Put U=a²d²+b²c². A normal to PQ after multiplying by Delta is

`n=(b(Delta*d-b²c), -a(Delta*c+a²d))`.

Its line value is `h=n·P=-abU`, so it never vanishes. Its caustic support square equals h² because

`a²(Delta*d-b²c)² + b²(Delta*c+a²d)² = (a²+b²)U²`.

Expansion first gives `U(Delta²+a²b²)`, and then `Delta²+a²b²=(a²+b²)U` by c²+d²=1. These are independently checked polynomial identities. Applying T gives every other chord, all tangent to the same fixed caustic.

Each caustic contact lies strictly inside its chord. Indeed, every point of the caustic lies strictly inside the outer ellipse. A line tangent to that caustic contains a contact in this strict interior. Its intersections with the outer ellipse are precisely its chord endpoints P,Q, so the contact is between these endpoints. This rules out tangency only to a remote extension.

Tangency by itself must not be confused with the physical reflection law; the following sign argument completes it. For an outer boundary point p=(x,y) and a unit direction v tangent to the caustic line through p, expansion gives

`(p_x*v_x/a² + p_y*v_y/b²)² = lambda/(a²b²) = 1/S`.

The polynomial checker verifies this reduction from the line tangency equation and the two constraints that p lies on the outer ellipse and v has unit length. The two inward chord directions from p towards its adjacent vertices are distinct. Strict convexity of the outer ellipse makes each of their projections on its outward normal strictly negative. Therefore both projections equal `-1/s`; the common absolute value cannot conceal a wrong outgoing branch.

Two distinct unit vectors in a plane with the same projection on a fixed nonzero normal have opposite tangential projections. They are reflections of each other in the normal line. The physical incoming vector is the negative of the previous inward vector, so reflection of that incoming vector in the tangent line gives the next inward vector. This is exactly the ordinary specular law. It holds throughout the continuous family, not only at D and R.

At (c,d)=(1,0), the vertices are D. At `(c,d)=(a/s,b/s)`, Delta=ab and the vertices are R. The intervening arc is continuous, uses the same caustic, never changes orientation or period, and has no singular chord or contact. This directly resolves the possible objection that two symmetric orbits with the same numerical caustic parameter might inhabit different oriented Poncelet families.

The extra pointwise certificate uses `(c,d)=(3/5,4/5)` at a=4,b=3. It lives exactly in Q(sqrt(193)). Its alternating positive edge lengths are `5 ± 84/(5sqrt(193))`. It checks all four ordinary normalized reflections, all four caustic tangencies, the common perimeter 20, and both normal-projection signs. Thirty exact identities pass. This phase is not either symmetric representative and supports the branch argument; it is not a substitute for the preceding general proof.

## Adversarial alternatives and claim limits

1. **Wrong orbit angle convention.** Replacing each interior theta by its supplement interchanges half-angle sine and cosine. D has supplementary opposite angle pairs, so the four-factor product is unchanged; R has four right angles. The same unequal k107 values remain. Source theta is the original polygon's angle, so an incidence angle relative to the normal would be a different quantity, not an alternative interpretation of this table row.
2. **Signed areas and orientation.** Both displayed trajectories and both outer tangent polygons have positive signed area. Reversing the traversal negates both A and A' and keeps their ratio. Reordering the starting index cyclically also changes nothing. Thus an orientation convention cannot explain the discrepancy.
3. **Tangents to the wrong ellipse.** I constructed tangents to the outer ellipse, as the source specifies, not the caustic or side-line intersections. Tangency points on the inner ellipse were used only to verify the caustic.
4. **Repetition, self-intersection, or singularity.** Distinct four-vertex convex polygons and distinct incoming states establish primitive period four. The caustic is a strict ellipse, both areas are positive, tangent intersections are finite, and all contacts are strictly inside their chords.
5. **Different conserved family data.** The exact caustic, perimeter, Joachimsthal constant, rotation orientation, and explicit connecting continuous family all agree. No numerical fitting of a caustic is involved.
6. **Known adjacent invariant.** The two area products agree exactly. The diagnostic corrected quotient also agrees for these two representatives. Neither consistency check turns the printed product into an invariant. Agreement of two representatives is not proof of a corrected quotient for every phase or every N.
7. **A possibly intended corrected theorem.** The result resolves the literal assertion by refutation. It does not establish what the authors intended, exclude a later correction, or prove the N≡2 mod4 sibling statement.
8. **Historical novelty.** No novelty conclusion follows from the correctness audit. A later paper, erratum, source update, or explicit earlier nonconstancy formula could settle priority and change publication disposition. This report makes no search-completeness or independent-discovery claim.

The negative controls in the rational program reject an incorrectly changed caustic and an off-ellipse vertex. Explicit runtime checks remain active under optimization; the independent certificate contains no assertion-based safety shortcut.

## Reproduction and remaining gaps

Run `independent_rational_certificate.py` with Python's standard library; both ordinary and `-O` executions completed 175 exact runtime checks, including two expected negative-control rejections. Run `independent_polynomial_identities.py` and `independent_nonsymmetric_certificate.py` with SymPy 1.14.0; they passed six polynomial identities and thirty nonsymmetric exact identities. The machine outputs are `RATIONAL_CERTIFICATE.json`, `POLYNOMIAL_IDENTITIES.json`, and `NONSYMMETRIC_CERTIFICATE.json`. Full local primary-source hashes and URLs are in `primary_sources/SOURCE_RECEIPT.json`.

`ACTUAL_REPRODUCTION_RECEIPT.json` records a dedicated final replay supervised by actual PID 73412. The four actual child PIDs 73420–73423 all exited zero, were reaped, and had empty process groups. Full stdout and stderr bodies are retained under `reproduction_raw/`. The exact source and output hashes are pinned in that receipt. It is an actual preparatory audit replay, not a synthetic publication fixture or an authorization to alter provider state.

**Strongest independently verified conclusion:** for every a>b>0, one explicitly fixed four-period confocal billiard family contains the two stated admissible representatives with different printed k107 values; in particular the rational axes 4,3 example disproves the literal universal k107 assertion. **Exact mathematical gap:** none found in this conclusion. **Remaining nonmathematical gap:** priority has not been established by this geometry review. No original file, repository metadata, Git control, provider state, or external person was modified or contacted.
