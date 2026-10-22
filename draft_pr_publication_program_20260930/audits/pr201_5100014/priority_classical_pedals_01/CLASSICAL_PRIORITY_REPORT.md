# Classical pedal-area priority audit for PR2015100014 / k303,a

Independent family: classical Steiner/Sturm pedal area, curvature centroid, conic polarity, orthoptic/tangential identities, and elliptic addition/cyclic sums. Approach freeze: `APPROACH_FREEZE.md`, 2026-10-16 UTC, before reading any sibling new priority-family report. This report does not grant priority, publication, merge, or release clearance.

## 1. Exact claim and audit conclusion

The accepted mathematical gate is input, not a priority finding: outer ellipse E has a>b>0; the caustic has squared semiaxes a²−λ,b²−λ, with 0<λ<b²; the real Poncelet translation has **least** period N=2m≥6, m odd. In orbit order, P_i are the boundary vertices, ℓ_i their E-tangents, T_i=ℓ_i∩ℓ_(i+1), and Q_i(M) the perpendicular feet of a fixed real point M to ℓ_i. A,A′,B_M are the signed shoelace areas of P,T,Q(M). The target is phase constancy of A′B_M for every M, including primitive stars and reversal.

**Result of this bounded family audit:** the fixed-polygon dependence on M is directly classical, with an original Steiner proof and exact formula recovered. It must not be described as a new theorem. No inspected old primary theorem has been explicitly specialized to supply the two remaining phase-dependent coefficients for the noncircular confocal target. Therefore this family found **no exact classical priority knockout**, but it also provides **no proof of worldwide novelty or first-proof status**. The candidate's potentially creditable contribution is a particular proof/application of standard elliptic-function machinery to a previously recorded invariant, not discovery of that invariant, not discovery of the radial formula, and not a new general principle of pole cancellation.

## 2. Exact source/theorem ledger

The descriptions below refer to the inspected pages/sections, not to uninspected complete oeuvres. All old scans were obtained from ETH e-rara or Numdam/Gallica; no shadow-library fulltext was used. Search-result pages and modern secondary pages were discovery aids only.

### C1. Steiner's first general polygon theorem, dated November 1825

Primary inspected reproduction: Jacob Steiner, *Gesammelte Werke*, vol. I, Berlin: Reimer, 1881, **pp.15–16**, in *Einige geometrische Sätze*. The final line of p.16 dates the work Berlin, November 1825. The article is bibliographically J. reine angew. Math. 1 (1826), pp.38–52; the 1826 original itself was not downloaded. The claim/proof are directly visible in the collected-works primary reproduction.

Stable source: [ETH record, DOI10.3931/e-rara-76811](https://doi.org/10.3931/e-rara-76811). [Printed p.15](https://www.e-rara.ch/zut/content/zoom/21668475), [printed p.16](https://www.e-rara.ch/zut/content/zoom/21668476). Institution: ETH-Bibliothek Zürich, Rar22746. Private page images inspected, not proposed for redistribution.

**What it says:** for a fixed arbitrary polygon, the points whose perpendicular-foot polygon has fixed area form a concentric family of circles; the common center is the weighted centroid of its vertices with weights sin twice the vertex angles. Page16, equation(5), supplies the signed squared-distance area formula, with interior-angle convention. The triangle and regular-polygon predecessors are cited on p.15.

**Specialization/status:** central symmetry annihilates the weighted first moment, so the origin is the curvature center whenever the total weight is nonzero, and the polynomial remains radial even if the total weight is zero. This is a fixed-polygon theorem: its coefficients may depend on the billiard phase. It does not itself prove k303,a. A finite-center/degenerate-level-set qualification is necessary; see C4 and §4 below.

### C2. Steiner's explicit radial coefficient

Primary inspected: *Über den Krümmungs-Schwerpunkt ebener Curven*, read 5April1838, ETH offprint, [DOI10.3931/e-rara-3816](https://doi.org/10.3931/e-rara-3816), ETH-Bibliothek Zürich, Rar5481. The ETH record dates its collection1836–1841. We cite the **printed offprint pagination** and do not silently convert it to the journal pagination19–91 used by RGK.

Inspected sections: introduction **p.4**; §XIV–XV **pp.18–19**; §XVI **pp.20–22**; §XVII begins p.22. Page images: [p.19](https://www.e-rara.ch/zut/content/zoom/1188573), [p.20](https://www.e-rara.ch/zut/content/zoom/1188574), [p.21](https://www.e-rara.ch/zut/content/zoom/1188575), [p.22](https://www.e-rara.ch/zut/content/zoom/1188576).

**Exact inspected equations:** §XV eq.(26) is 4(2V−W)=Σd_i²sin(2δ_i), where W,V are original/pedal areas, d_i is distance to a vertex, and δ_i is the exterior angle. §XVI eqs.(27)–(29) give V−v=s²Σsin(2δ_i)/8 relative to the weighted center. This fixes the factor and the angle convention. Introductionp.4 points back to the1825 contribution in Crellevol.I p.51 and vol.II p.265.

**Specialization/status:** exactly the radial reduction in §3, already classical. No phase variation of a Poncelet family appears in the inspected theorem. Invoking it alone to claim A′B_M constant merely leaves the central coefficient difficulty unresolved.

### C3. Sturm's triangle predecessor, with explicit signed-area discussion

Ch. Sturm, *Autre démonstration du même théorème*, Annales de mathématiques pures et appliquées14(1823–1824), **pp.286–293**. [Primary scan](https://www.numdam.org/article/AMPA_1823-1824__14__286_0.pdf). The title metadata records the volume1823–1824; this audit does not resolve the exact issue date and does not convert it to an unsupported exact1823 publication date.

**Inspected result:** pp.286–289 derive concentric circular level sets of triangle pedal area; p.287 expressly retains the sign for the analytic interpretation; p.291 obtains the center value one quarter of the original triangle area. The last paragraph, pp.292–293, states a general second-degree level-set conclusion for arbitrary polygon area.

**Specialization/status:** a triangle theorem cannot be applied to the entire moving outer N-gon by replacing it with one triangle without proving compatibility of the decomposed coefficients. It establishes classical signed and zero/negative-area context, not the target confocal Poncelet coefficient identities.

### C4. Thébault's general fixed-polygon pedal/isopodal treatment and degenerate caveat

V. Thébault, *Sur les polygones podaires d'un polygone donné*, Nouvelles annales de mathématiques, series4, vol.14(1914), **pp.433–446**. [Primary scan](https://www.numdam.org/item/NAM_1914_4_14__433_0.pdf). Its first page identifies the Oct.–Nov.1914 issue.

**Inspected result:** §1 pp.433–434 treats isopodal similarity; §3 pp.437–438 states that the area level set is generally a circle but can be a line when the total double-angle sine vanishes; it retains algebraic area for crossed quadrilaterals. Page442 discusses trapezoid/cyclic exceptions. §2 p.436 relates the squared radii of two equal-absolute-area triangle level circles to the circumcircle orthoptic; this still concerns one fixed polygon. §4 p.444 extends the weighted-distance expression to arbitrary n and explicitly credits Steiner.

**Specialization/status:** confirms the old reduction and prevents overstating the finite curvature center or zero-area geometry. Nothing in the inspected treatment supplies target-family phase constancy. A later Thébault paper of similar title is bibliographically located in Tohoku Math.J.17(1920), pp.73–83, through the journal's official index; its full text was not obtained/checked and is an explicit remaining source-access gap, not a negative finding about its content.

### C5. Steiner on Poncelet conics and areas: a different construction

J. Steiner, *Teoremi sulle coniche inscritte e circoscritte*, Roma1844, **theoremIII p.3**, [ETH primary record DOI10.3931/e-rara-4469](https://doi.org/10.3931/e-rara-4469), ETH-Bibliothek Zürich, Rar5007; [p.3](https://www.e-rara.ch/zut/content/zoom/1371028).

**Inspected result:** given concentric conics admitting Poncelet triangles, construct the triangle whose sides through the original vertices are parallel to the opposite sides. The conics inscribed in these derived triangles with the same center have constant area. The surrounding §§I–II give conic-area formulas from a fixed triangle and a prescribed center.

**Specialization/status:** this is an old genuine Poncelet area theorem, but its derived object is an inscribed conic, with a triangle/parallel-line construction. It is neither the signed area of a polygon of feet nor an evenN assertion. No substitution establishing the target metric areas is recovered. Merely recognizing the words conic, Poncelet, and area is insufficient.

### C6. Jacobi's old additive-coordinate Poncelet mechanism

C.-G.-J. Jacobi, *Sur l'application des transcendantes elliptiques…*, Journal de mathématiques pures et appliquées, series1, vol.10(1845), **pp.435–444**, an explicitly shortened French translation by Terquem of the1828 German memoir. [Primary record](https://www.numdam.org/item/JMPA_1845_1_10__435_0/). The inspected primary scan is linked from that record.

**Inspected result:** §§IV–VI **pp.435–439** turn tangency between two circles into successive amplitudes am(u+jt), with the shift independent of the initial point. The footnote p.435 identifies the German source Crellevol.III p.376(1828). This audit checked the French source pages, not the full1828 original.

**Specialization/status:** closure/additive elliptic coordinates and addition theorems are old. The inspected equations do not identify the target Euclidean projection denominators or evaluate its signed area traces. A projective equivalence of conic pairs does not preserve perpendicular feet or affine signed area. See the exact metric obstruction in §5.

### C7. Poncelet-grid geometry and normal-distance invariants

H. Stachel, *The geometry of billiards in ellipses and their Poncelet grids*, J.Geometry112, article40(2021), [DOI10.1007/s00022-021-00606-2](https://doi.org/10.1007/s00022-021-00606-2). Primary publisher full text inspected by named sections rather than downloaded as a complete local PDF.

**Relevant exact results:** **Corollary4.2(i)**: evenN, odd turning number gives central symmetry. **Theorem4.7**, eqs.(4.4)–(4.5), concerns a constant sum of cosines. **Corollary4.9** gives a constant sum of squared center-to-tangent distances and of curvature^(2/3).

**Specialization/status:** the target primitive even stars have odd winding numerator; this supports the already known symmetry reduction. A sum of individual squared tangent distances is a one-index norm statistic, whereas B_0 and S involve adjacent pairs with oriented determinants and weights. No equality between those quantities is supplied in these results. Their invariants are useful background, not a replacement for the missing bridge.

### C8. The already credited original/outer area product

A.C. Chavez-Caliz, *More About Areas and Centers of Poncelet Polygons*, Arnold Math.J.7(2021),91–106, online14August2020, [primary journal PDF](https://armj.math.stonybrook.edu/pdf-Springer-final/020-0154.pdf), [DOI10.1007/s40598-020-00154-8](https://doi.org/10.1007/s40598-020-00154-8). **Theorem3 p.93** and **Theorem6 p.104** establish AA′ constant for even Poncelet polygons between concentric ellipses in general position. The genus-one translation framework is on p.98.

**Specialization/status:** this is an explicit dependency of the candidate, not its new contribution. Replacing B_M by A in this theorem is unjustified until B_M=c_M A is proved. The exact N4 boundary control in §4 shows why the replacement cannot be a parity-free consequence of Steiner plus this theorem. The accepted root gate supplies the target-parity applicability; this family does not replace the mathematical dependency audit.

### C9. Preexisting cyclic elliptic pole-cancellation/master identities

A. Khare, A. Lakshminarayan, U. Sukhatme, *Cyclic Identities Involving Jacobi Elliptic Functions.II*, [math-ph/0207019v2](https://arxiv.org/pdf/math-ph/0207019),24March2003. Primary manuscript inspected: **pp.3–8**, especially eq.(3) and its pole-cancellation explanation p.3, master identities eq.(20) p.6 and **eq.(26) p.8**. The page numbers here are the manuscript's printed page numbers (the PDF's first page is1).

**Inspected result:** equally spaced cyclic traces reduce to standard archetypal sums and derivatives, with coefficients read from principal parts. The constant adjacent-dn product and its rth-neighbor version are explicit examples. The required pole locations are specified before the master identity, p.5 eq.(11).

**Specialization/status:** standard elliptic principal-part cancellation is not a new method. To invoke these formulas here one must identify all poles of the metric projection trace, prove that its pole set falls into the allowed translated sampling grids, and cancel apparent higher-order terms. Those are precisely substantive steps of the candidate. Simply naming a master identity after assuming those coefficients vanish relocates the central difficulty; this shortcut route is **blocked** until an actual verified specialization is supplied.

Related primary source checked in limited part: their *Local Identities Involving Jacobi Elliptic Functions*, [math-ph/0306028](https://arxiv.org/pdf/math-ph/0306028), **§1 pp.2–4**, eqs.(1)–(8), gives local identities and cyclic summations with general weights. It supplies further standard machinery but no inspected pedal-area specialization.

### C10. Modern reference for the classical addition formulas

[NIST DLMF §22.8](https://dlmf.nist.gov/22.8), equations22.8.1–3, supplies the Jacobi addition formulas and cites Whittaker–Watson1927 pp.494–498, Lawden1989 pp.33–36, and Walker1996 pp.126–131. This official reference was checked to delimit the standard tool. Those three cited books were not inspected in this audit, so no priority verdict is based on their uninspected pages.

## 3. The exact classical reduction and its unsolved specialization

This section is an independent algebraic specialization of the inspected old formula; it is not claimed as a discovery.

Let R_i be any nonzero real normals, ℓ_i={z:R_i·z=1}, with det(R_i,R_(i+1))≠0. Put

    w_i = 2 det(R_i,R_(i+1)) (R_i·R_(i+1))
          / ((R_i·R_i)(R_(i+1)·R_(i+1))) = sin(2δ_i),
    S = Σ_i w_i,       L = Σ_i w_i T_i,       H = Σ_i w_i |T_i|².

Here δ_i is the oriented normal turn modulo π, not an unsigned angle. The expression w_i does not depend on the sign chosen for either normal. A′ and B_M use the fixed side-cycle order and signed shoelace area. With these conventions, Steiner's identity reads

    4(2 B_M − A′) = Σ_i |M−T_i|² w_i,
    B_M = A′/2 + H/8 − M·L/4 + |M|² S/8.                 (1)

For the target polygon, central inversion pairs T_i with −T_i and the weights agree. Thus L=0, and

    B_M = B_0 + |M|² S/8.                                 (2)

This deduction is valid for every centrally symmetric tangent polygon, without Poncelet closure and without N=2mod4. A direct determinant derivation extends the formula from the old convex drawings to arbitrary signed polygon order; star winding does not justify replacing signed area by unsigned filled area. Reversal changes the signs of A′,B_M,S together.

Consequently the **exact target bridge** is the pair

    C_0(phase) = A′(phase) B_0(phase) is constant,
    C_2(phase) = A′(phase) S(phase)   is constant.           (3)

These two conditions are equivalent to every-M constancy: evaluate at M=O and any one fixed point with |M|²≠0, then compare coefficients in(2). There is no division by a pedal area. Equivalently, a prior verified center result plus a verified result at one focus would imply everyM, since a>b makes each focus noncentral. A source does not need to print everyM to anticipate it in that situation. The two foci alone do not provide two independent radial values because they have the same distance to O. No such pair of verified results at distinct squared radii was recovered here.

For an entirely explicit metric form, put D=diag(1/a²,1/b²), R_i=DP_i, d_i=R_i·R_i, U_i=det(P_i,P_(i+1)). Then

    Q_i(0) = R_i/d_i,
    B_0 = (1/(2a²b²)) Σ_i U_i/(d_i d_(i+1)),
    S = (2/(a²b²)) Σ_i U_i (R_i·R_(i+1))/(d_i d_(i+1)).   (4)

The missing identities are weighted adjacent-pair trace identities, not the one-point statement that the curvature centroid is fixed or the sum of squared tangent distances is constant. When credited AA′ constancy is used, one still needs B_0=c_0 A and S=c_2 A (or another equivalent verification of(3)). The audited candidate's pole-divisor/parity calculation supplies such a bridge; the old fixed-polygon formulas alone do not.

A local determinant proof, independent of convexity, is recorded in `adversarial_01/REPORT.txt`: writing t_i=T_i−M and q_i=Q_i(M)−M, direct expansion gives 2det(q_i,q_(i+1))−w_i|t_i|²/2=det(q_i,t_i)−det(q_(i+1),t_i). Summation gives the right side2A′ because q_i,t_(i−1),t_i are collinear; rearrangement yields(1). This proves the signed-cycle extension without replacing the classical source attribution.

## 4. Exact controls and boundary cases

`exact_classical_controls.py` uses only rational arithmetic and explicit exceptions, with no external dependencies. It passes both normally and under `python3 -O`; the receipts agree. It verifies the signed formula and its1/8 factor at three pedal points for a rational centrally symmetric tangent hexagon, plus the following controls.

### Excluded N=4: Steiner and AA′ do not suffice

Use E:x²/4+y²=1 and proper confocal caustic x²/(16/5)+y²/(1/5)=1, so λ=4/5. Both sequences below are genuine least-period4 billiard polygons. Direct dual-conic tangency and physical reflection are verified exactly.

| Phase | P vertices in orbit order | A | A′ | B_0 | AA′ | A′B_0 | S |
|---|---|---:|---:|---:|---:|---:|---:|
| Axis | (2,0),(0,1),(−2,0),(0,−1) |4|8|4|32|32|0|
| Rectangle | (4,1),(−4,1),(−4,−1),(4,−1), all divided by √5 |16/5|10|5|32|50|0|

These examples satisfy central symmetry, a genuine common confocal caustic, and the credited constant AA′. Their pedal areas are independent of M because S=L=0, yet A′B_0 varies. They are **not counterexamples to the target**, which excludes N=4. They are a precise guard against a parity-free claimed implication from Steiner+AA′ and show where target parity must enter a successful proof.

### Zero total weight is not automatically a finite curvature center

For the noncentral trapezoid(0,0),(2,0),(1,1),(0,1), S=0 but L=(−1,1)≠0. Direct feet give B_(0,0)=1/2 and B_(1,0)=3/4. Thus its area level sets are lines, as Thébault discusses. The finite quotient K=L/S must not be used at S=0, and a blanket inference from S=0 to constant B_M is invalid without L=0. The target's central symmetry provides L=0, so this caveat does not invalidate the target.

## 5. Why conic polarity/orthoptic/circle routes do not automatically close the bridge

Polarity with respect to E sends an original chord line to a vertex of the outer tangent polygon. That is the appropriate projective geometry for AA′. It does not take the chord polygon to the Euclidean foot polygon. In coordinates, the foot is

    Q_i(M) = M + (1−R_i·M) R_i/(R_i·R_i).                (5)

The metric denominator is essential. Over the complexification it vanishes at isotropic normals. The target proof's identification of the corresponding common-tangent flags and their torsion orbits is a real additional geometric step; it cannot be erased by saying polarity or Poncelet porism.

An exact elementary check: the foot of O to x+y=1 is(1/2,1/2). The affine map(x,y)↦(2x,y) sends this to(1,1/2), while the foot to the mapped line x/2+y=1 is(2/5,4/5). Thus an affine change that simplifies a conic pair generally changes the pedal construction. A general projective change also changes the line at infinity and affine signed area.

Orthoptic conditions supply special right-angle/tangent-distance identities, but w_i is an adjacent double-angle sine, and H carries a metric vertex norm. A right angle makes w_i=0; it does not establish the required noncircular target coefficient identities. No inspected primary orthoptic theorem supplies(3). A proof for regular polygons on a circle has phase constancy by rotation, but transporting it affinely does not transport perpendicular feet, and homothetic conic pairs are not the target noncircular confocal pairs.

## 6. Route status and editorial contribution assessment

| Route/mechanism | Evidence | Status | Exact gap or consequence |
|---|---|---|---|
| Fixed-polygon Steiner/Sturm radial dependence | C1–C4, exact controls | Verified classical | Cannot count as novelty; leaves both quantities in(3) |
| Constant curvature center + AA′ | C1–C2,C7–C8 | Blocked as a shortcut | Still needs the two target coefficient identities; N4 guard rejects parity-free inference |
| Center + one focus implies everyM | Equation(2) | Verified conditional reduction | Need earlier proofs for both radial values; none recovered here |
| Conic polarity + classical Poncelet closure | C5–C6,C8, exact projection check | Blocked as a metric shortcut | Orthogonal projection denominators and signed area do not transport |
| Cosine/normal-distance invariants | C7 | Verified relevant background | No adjacent weighted determinant identity supplied |
| Addition/cyclic master identities | C6,C9–C10 | Standard machinery identified | Actual pole-grid/principal-part specialization needed; merely invoking it repeats the central difficulty |

The target invariant is already explicitly recorded by RGK in2020/2021; a new proof must credit that observation and the corrected least-period interpretation. If no exact earlier proof is established by the other independent priority families, this candidate may be presented as **a proof of the recorded outer-pedal product invariant**, using standard genus-one/Poncelet geometry and credited AA′. This audit alone does not justify first proof, new invariant, novel general method, or worldwide open problem claims.

The potentially substantive proof-specific point is the metric projection trace's pole-divisor reduction in odd half-period, including the apparent double-pole cancellation for arbitrary M. That is an editorial description of what the accepted proof adds beyond the inspected sources, not a certified historical novelty assertion. The accepted proof should retain separate credit for the general flag/translation framework, Riemann–Roch or equivalent classical elliptic-function theory, and Chavez-Caliz's product theorem.

## 7. Independent adversarial verification

The local adversarial verifier independently proves the signed determinant identity for real ordered line cycles and checks every polynomial coefficient in M on448 rational directed cycles, an explicit pentagram and reversal, origin-centered and translated symmetric hexagons, the exact N4 orbits including interior caustic-contact parameters and physical reflection, zero-weight trapezoid, affine projection, and invalid denominators. No algebraic defect was found. It confirms the necessary origin-centered ordered pairing and signed/oriented-angle conventions. See `adversarial_01/REPORT.txt` and its hash receipt.

All23 initial verifier assertions were replaced with explicit exception checks before sealing. The final normal and optimized runs agree on every mathematical field, and a deliberately false condition is rejected in both modes. This certifies the bounded algebraic controls only; it does not provide a second universal Poncelet proof or a historical priority verdict.

## 8. Search bounds, source limits, and custody

Focused searches covered Steiner/Sturm pedal theorem, curvature centroid/isopodal circles, Poncelet/pedal area, conic polarity/orthoptic/tangential area, German Fusspunkt/Krümmungs-Schwerpunkt and French polygones podaires, Jacobi1828/1845, and cyclic elliptic identities. Queries and exclusions are recorded separately in `SEARCH_AND_ACCESS_LIMITS.md`.

This is not a complete historical bibliography search. No complete19th-century oeuvre or journal-volume scan was performed. Direct books/papers not inspected are expressly identified above; inaccessible or metadata-only findings are not treated as negative fulltext evidence. Browser/search retrieval failures were worked around only through legitimate institutional source downloads. No contact, outreach, email, call, author request, or draft outreach was made. No private API output is part of the authored deliverables. Original submission files and all sibling new priority-family reports were left unread/unchanged by this family except the accepted root mathematical/source-scope documents supplied as task context.

Only files listed in `SAFE_AUTHORED_MANIFEST.json` are authored handoff material. `primary_private/` holds third-party primary scans, OCR and manifests for local audit only and is wholly excluded from that manifest. No PDF, full third-party text, dependency, browser cache, or private API dump is proposed for publication. No Git or publication action was performed.
