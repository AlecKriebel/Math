# Independent adversarial review: 5100017 / k307

Verdict: **PASS_COMPLETE_SOURCE_TARGET_ON_NATURAL_CENTROID_DOMAIN**. No mandatory mathematical or source correction was identified. The frozen candidate supplies the area centroid of the outer-side pedal polygon, for even least-period elliptic-caustic billiards and arbitrary fixed pedal point wherever that signed-area centroid is defined. It also identifies the complete exceptional domain. This verdict does not certify historical novelty or external acceptance.

## Frozen inputs and independence

The reviewed PROOF.md has SHA-256 d072c6ecf0f398753382603bbd00b4a950e50881d1fd3aa70526fc8889c12584. Its FROZEN_MANIFEST.json has SHA-256 057830409d710b7e0bb52ed2c3d8ffa71e268633729dbdc3d110509030b7739e. All twelve listed author files and all three pinned primary PDFs match. No author file was changed. The reviewer did not develop this candidate and independently reconstructed its support-number, signed-moment and exact-star calculations. Related earlier campaign work is not treated as an independent proof of this target.

## Source and object gate

Both the arXiv v11 Table 4 and final printed page 346 identify k307 as C2 prime, the signed **area** centroid of the pedal of the outer tangent polygon. The feet lie on the original ellipse's tangent lines at the original orbit vertices. This is neither the vertex centroid k306 nor the pedal of the original chord polygon. The source permits self-intersecting trajectories and defines area centroids by signed shoelace moments. Its formula itself requires nonzero signed area. Section 2 assumes a>b>0 and a strict confocal elliptic caustic. The candidate's least-period and star qualifications preserve this model.

Bialy–Tabachnikov Theorem 4.1 proves the neighboring vertex-centroid assertion, not k307. The candidate does not replace the requested area centroid with that theorem. Their Theorem 4.3 and its proof support the known even symmetry and four-period geometry. All source PDFs were read locally, and both table images were inspected. Source hashes and locators are recorded separately.

## Analytic and algebraic attacks

1. **Antipodal pairing.** The chosen Poncelet map has exact finite order N and commutes with the half-turn. The finite group it generates together with that half-turn is cyclic: an orientation-preserving finite circle action is free, and its faithful action on one finite orbit preserves cyclic order. For even N its unique involution is the half-turn. This proves the pairing for primitive stars as well as convex orbits. An odd orbit traversed twice does not supply this hypothesis and is explicitly excluded from an unjustified extension.

2. **Real geometry and positivity.** Consecutive chord endpoints advance by less than a half-turn around the ellipse because their chord supports an inner ellipse containing the origin. The strictly increasing Gauss map commutes with the half-turn. Thus successive outward normal angles differ by a number in (0,pi), and all tangent intersections are finite. Each term in the origin-pedal signed area is positive, even for stars. No assumption of simple winding is used here.

3. **Bilinear support identity.** I derived the chord tangency equation in the eccentric-angle coordinates and recovered d h_i h_j = F cos(Delta)+e d cos(psi_i+psi_j). The factors F+ed and F-ed are respectively a²-lambda(a²/b²-1)>b² and b²+lambda(1-b²/a²)>0. Hence all denominators F and F²-e²d² in the final formula are controlled. When d=0, every normal advances by pi/2, so the least period is exactly four. A direct unrestricted-point shoelace calculation gives area 2AB and centroid M/3 in that case.

4. **Doubled-normal moment.** Squaring the bilinear identity and substituting h_i²=H+e cos(2psi_i) gives precisely the stated affine relation for cos(2Delta). The unit-circle identity used to telescope the first moment is valid without simplicity or nonzero area. Its real and imaginary telescoping terms yield T_Z=2v S_Z, with the factor two and sign as written. Separately, S(0)=D S_Z/2. The prior strict positivity therefore proves S_Z is nonzero whenever d is nonzero; division by it is legitimate for star polygons too.

5. **Cubic signed moment.** I independently expanded the full edge expression (conjugate(V_i)V_j-V_i conjugate(V_j))(V_i+V_j), averaged the antipodal edges and extracted its linear and cubic terms. The exact checker verifies the two Laurent coboundaries, not just a numerical specialization. Their cyclic sums are D R2+(3e/2)R1 and (D/2+H)R1+(e/2)R2; the cubic term has the negative sign -|t|²t T_Z. Substituting R1=-4iS_Z and R2=-4ivS_Z, dividing by 6S and translating by z/2 gives the displayed formula. The area expression follows independently by antipodal cancellation. The factors 2, 3 and 6 and conjugations are consistent.

6. **Exact domain and convex subcase.** Since S(0)>0, the formula S(M)=S(0)(2F+d|M|²)/(2F) proves that the only undefined signed-centroid locus is the stated circle when d<0. If d>=0 it is empty. For winding one and N>=6, the first half of the doubled normals is a convex cyclic polygon in order; the full list traverses it twice, so S_Z>0 and therefore d>0. The four-period case was already handled. This proves the literal all-M assertion for simple families without asserting it for star families on the zero circle.

7. **Actual exceptional star.** Independent rational scaled-coordinate calculations verify all eight original vertices, confocal tangency, the reflection law with the correct forward sign, exact least period and winding three. I reconstructed the outer tangent feet for 221 rational pedal-point queries, checking both tangent incidence and perpendicularity before area/moment comparisons. The parameters d=-120/221, F=2795/1728, v=7/13 and radius squared 123539/20736 are correct. An exact quadratic area-polynomial calculation confirms the zero circle without numerical square roots. This is a domain demonstration, not a counterexample to the invariant on its defined locus.

## Reproducibility and limitations

The author's receipt replays byte-for-byte: 63 exact assertions, 1,984 defined-centroid diagnostics and 224 zero-circle diagnostics. The independent exact checker passes 4,355 assertions, including formal Laurent identities, 221 actual rational star queries and 27 rectangle controls. A separate 85-digit mpmath script provides phase/primitive-star diagnostics; its receipt reports the precise counts and residuals. Neither finite checks nor high precision replaces the written all-period proof.

Run `python independent_checks.py` and `python independent_numeric.py` from any directory; neither uses an absolute checkout path or imports author code. SymPy and mpmath are the only nonstandard dependencies. The source PDFs are reading copies, not required for replaying these computations.

## Disposition

A claimed_solved first-turn disposition is mathematically supported with the source's natural signed-centroid domain prominently retained. State that simple even families cover every M, while primitive stars can have the explicitly certified common zero-area circle. Preserve the exact object, least-period qualification and known-input credits. The proof is not an unconditional assertion that a zero-over-zero area centroid exists, and no priority claim is certified.
