# General-theorem implication audit for PR 201 / k303,a

Audit date: 2026-10-16 UTC. This is a bounded priority audit, not an assertion of worldwide firstness. Mathematical acceptance in ROOT_MATHEMATICAL_GATE_01.json and the scope correction are accepted inputs. Publication and priority remain uncleared. No sibling priority-family reports were read.

## 1. Outcome and exact claim

No theorem-to-target substitution was found in the primary general-theorem sources audited here. Several results genuinely supply parts of the proof. In particular, Chavez-Caliz supplies the even-period product AA', while Bialy-Tabachnikov supplies arbitrary-point invariants for the *same outer-pedal feet*. Neither supplies their signed area. The distinction is substantive and can be checked exactly.

The exact accepted target is as follows. Let E be x²/a²+y²/b²=1 with a>b>0. Let the strictly nested caustic be x²/(a²-lambda)+y²/(b²-lambda)=1, with 0<lambda<b². Its Poncelet translation must have exact least order N=2 mod 4, N>=6. If P_i are its billiard vertices in orbit order, T_i the intersections of consecutive E-tangents, and Q_i(M) the perpendicular feet from any fixed finite real M to those tangents, then

    A'(t) B_M(t) is independent of t,

where A' is the signed shoelace area of T and B_M that of Q(M). Primitive star windings and reversal are included. The source table's N is interpreted as least period; it does not literally print that qualification. Hyperbolic or degenerate caustics, unrestricted repeated odd orbits, unsigned filled area, and an all-parity converse are outside the claim.

An independently derived reduction in Section 3 makes the unfilled bridge precise: after central symmetry, the every-M target is equivalent to constancy of **two scalar quantities**, A'B_0 and A'S, where S is defined there. Existing centroid, squared-distance, angle-product, and AA' laws do not fill this bridge by substitution. This does not rule out a future short derivation from those results plus additional geometry; it identifies exactly what such a derivation must establish.

Search also surfaced an exact-target 2026 preprint by Alper Ferudun, [Outer-Pedal Area Products in Elliptic Billiards](https://eulersolve.org/papers/amr-050-0014/), whose page reports 1 October 2026. This was promptly reported to root for the separate exact-history/later-literature family. Its proof, dating, and priority are not adjudicated here. Therefore this report **cannot support a novelty clearance**, even if the general-theorem route has no identified prior implication.

## 2. Primary theorem and section ledger

Entries distinguish a direct usable implication, a related mechanism, and a scope mismatch. The full retrieved PDFs and extracted texts are private reading aids, excluded from the authored-output manifest. Bibliographic URLs and hashes appear in SOURCE_LEDGER.json. Descriptions below are deliberately brief; the transfer analysis is independently derived in later sections.

### Akopyan-Schwartz-Tabachnikov

Source: [Billiards in ellipses revisited, arXiv:2001.02934v2](https://arxiv.org/pdf/2001.02934v2), dated 25 January 2020. Main statement/related derivations checked across pp. 2-11.

| Location | Result used or tested | Target status |
|---|---|---|
| Theorems 1, 4; Section 2 | Constant sum of billiard angle cosines; Joachimsthal/perimeter formula | Genuine background; no pedal-area assertion |
| Theorems 2, 6; Section 5 | Constant product of outer tangent polygon angle cosines | Same outer polygon; different observable |
| Lemma 3.1, Section 3; Section 4 | Dual Minkowski billiard and unit side-vector Poncelet polygon | Transfer exists for side directions, not automatically for tangent-normal pedal feet |
| Theorems 7, 8; Corollary 6.1 | Longer-angle cosine sums and squared diagonal lengths | Genuine angle/distance generalizations; no area product |
| Corollary 6.4 | Ellipse-circle angle formulation | Different observable |
| Corollaries 6.2-6.3; multidimensional variant | Odd half-angle sine product; ideal hyperbolic/dimensional reformulations | Different observable or geometry |
| Theorem 3, Section 7 | A'/A invariant for odd n between concentric ellipses | Odd-period hypothesis excludes the target |

The Section 7 affine/Poncelet-grid argument controls areas of two polygons related by a fixed affine map. The target's perpendicular-foot operation does not commute with that map (Section 4). The paper's holomorphic pole-cancellation proofs are credited mechanism, not a theorem that arbitrary rational polygon observables are constant.

### Bialy-Tabachnikov

Source: [Dan Reznik's identities and more, arXiv:2001.08469v2](https://arxiv.org/pdf/2001.08469v2), dated 5 May 2020. Sections 2-4, pp. 2-10, checked.

| Location | Result used or tested | Target status |
|---|---|---|
| Proposition 2.1; Theorem 2.2 | Support-function generating function; sums 2h sin(delta) and h' sin(delta) | General smooth-convex billiard identities |
| Corollary 3.2 | Elliptic support/angle moment identities | Supplies moments, not adjacent determinant traces |
| Theorem 3.3 | Product of outer angle cosines | Same angle law as AST |
| Theorem 4.1, pp. 6-7 | Fixed centroid and sum of squared distances for feet from every P to tangents at billiard vertices | **Exactly the target feet**, but not their area |
| Lemma 4.2; Theorem 4.3 | Focal-distance products for pedals to billiard *sides*; centered product when 4 divides n | Different sidelines and observable/parity |

Theorem 4.1 is the closest general result. Section 5 gives an exact check that its conserved data, even combined with AA', do not determine A'B_M across all even periods. Target parity still requires extra reasoning.

### Chavez-Caliz

Sources: [More about areas and centers of Poncelet polygons, arXiv:2004.05404](https://arxiv.org/pdf/2004.05404), and [journal final](https://armj.math.stonybrook.edu/pdf-Springer-final/020-0154.pdf), DOI [10.1007/s40598-020-00154-8](https://doi.org/10.1007/s40598-020-00154-8). Sections 2, 4, 5 and introduction checked; arXiv Theorem 6 at pp. 18-19 agrees with journal Theorem 6 and proof at p. 104.

| Location | Result used or tested | Target status |
|---|---|---|
| Theorem 3 in introduction; Theorem 6, Section 5 | AA' constant for even Poncelet polygons between concentric ellipses in general position | **Direct credited dependency** after E/C/P/T substitution |
| Section 2 | Genus-one flag curve, involutions, cyclic area trace, pole/zero method | Credited framework |
| Theorem 4 | A nondegenerate zero-area Poncelet member forces all members' areas to vanish | Requires actual Poncelet polygons on the conic pair |
| Theorems 2, 5; Sections 3-4 | Circumcenter-of-mass locus and degenerate-center analysis | Centers; no arbitrary-point pedal area |

For the accepted confocal scope, general position is checkable directly: with c²=a²-b², E and C meet at x²=a²(a²-lambda)/c² and y²=-b²(b²-lambda)/c², four distinct finite transverse complex intersections. Thus no target restriction is lost in the credited AA' substitution. The missing B_M/A relation is not printed as a consequence.

### Roitman-Garcia-Reznik: bicentric and focus-inversive transfer

Source: [New Invariants of Poncelet-Jacobi Bicentric Polygons, journal final](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0188.pdf), DOI [10.1007/s40598-021-00188-6](https://doi.org/10.1007/s40598-021-00188-6), 2021, pp. 619-637. Sections 3-5 and Appendices A-C checked.

Theorem 1 conserves the bicentric angle-cosine sum. Theorem 2 (p. 625) conserves pedal **perimeter** for the **two limiting points**. Corollary 1 (p. 627) gives focus-inversive elliptic-billiard perimeter. Appendix A proves the classical inversion/polarity/pedal relationship; Appendices B-C identify special polar conic pairs. These are real transfers, but neither perimeter nor limiting-point restriction is the target's every-M area product. Inversion has varying determinant weights (Section 4). The shared use of Jacobi functions and Liouville's theorem does not supply the missing area identity.

### Garcia-Reznik-Roitman: harmonic families

Source: [New Properties of Harmonic Polygons, journal final](https://www.heldermann-verlag.de/jgg/jgg26/j26h2alve.pdf), J. Geom. Graphics 26 (2022), 217-236. Sections 2-4, Table 2, pp. 225-228, checked.

Propositions 1-3 and Theorem 1 concern reciprocal squared lengths, Apollonius radii, and cotangent symmetric functions. Table 2 compares confocal, bicentric, inversive, homothetic and harmonic families. Propositions 4-5 and 7-9 construct polar/inversive links. Proposition 6 concerns reciprocal *lateral harmonic* areas for N=3,5; its all-odd extension is Conjecture 1. Conjecture 2 concerns a sine-of-double-angle sum divided by the *harmonic* polygon area. None supplies A'S or A'B_0 for target confocal outer pedals. Its labels must not be silently replaced by target geometry.

### Garcia-Reznik: self-intersected N-periodics

Sources: [arXiv:2011.06640](https://arxiv.org/pdf/2011.06640) and [2022 journal final](https://ami.uni-eszterhazy.hu/uploads/papers/finalpdf/AMI_55_from49to75.pdf), Ann. Math. Inform. 55 (2022), 49-75. Section 4/Table 1 and Section 5, including low-N qualifications, checked in both editions.

The table's area rows are k103, k106, k110 and focus-inversive k805-k807, with explicit low-N derivations and proof credits. It does not contain k303. Its N=4 and type-II N=6 failures concern another claimed focus-inversive angle law. This supports caution about meromorphic degeneracies, not a proof or disproof of our target. Some self-intersected cases use hyperbolic caustics and are outside the accepted scope. Primitive elliptic-caustic stars remain a separate quantifier to verify.

### Reznik-Garcia-Helman: inversive triangles

Source: [The Talented Mr. Inversive Triangle in the Elliptic Billiard, arXiv:2012.03020](https://arxiv.org/pdf/2012.03020). Section 3, Propositions 3-7 and Corollary 1, pp. 5-6, checked.

The fixed/perhaps moving billiard interpretation and proved area product concern N=3 focus-inversive triangles. Proposition 7 multiplies the two focus-inversive areas; Conjecture 1 extends that product to odd N. The pedals mentioned in Observation 1 are pedals of the inversive triangles at their respective foci. None is the outer-tangent every-M area product for least N=2 mod 4.

### Garcia-Odehnal-Reznik: general closure

Source: [Loci of Poncelet Triangles in the General Closure Case, arXiv:2108.05430](https://arxiv.org/pdf/2108.05430). Introduction/Theorem 1, main-result inventory, and Sections 4-6 checked.

Theorem 1 is the general multi-caustic closure statement. Theorems 2-3 and Propositions 1-6 concern triangle center loci/envelopes for modified bicentric/confocal families. The closure theorem supplies a family, not constancy of every geometric quantity on it. No pedal-area theorem or fixed-area multiplier is provided.

### Stachel: Poncelet grids and canonical coordinates

Sources: [The Geometry of Billiards in Ellipses and their Poncelet Grids, arXiv:2105.03362](https://arxiv.org/pdf/2105.03362), and [On the Motion of Billiards in Ellipses, arXiv:2105.03624](https://arxiv.org/pdf/2105.03624). Grid Sections 3-4 and Motion Sections 4-5 checked.

Grid Theorems 3.5-3.6 establish the grid/conjugate geometry; Corollary 4.2 explicitly treats even N with odd winding as centrally symmetric. Corollary 4.9 is a tangent-distance-square law. Motion Theorem 2 gives Jacobi coordinates with coprime N/winding. Its Theorem 6 is an alternating sine law; Theorems 8,10 and Corollary 9 concern tangent-contact segment lengths/products. These supply parametrization/symmetry and other invariants, but no theorem for outer-pedal signed area. In particular, tangent-contact lengths are not perpendicular-foot areas.

### General pedal-area geometry

Source: [Reznik-Garcia-Stachel, Area-Invariant Pedal-Like Curves Derived from the Ellipse, arXiv:2009.02581](https://arxiv.org/pdf/2009.02581), Section 2, Proposition 2 and Appendix B checked.

Section 2 recalls the Sturm-Steiner circle-isocurve theorem for pedal area of a *fixed* polygon, and its curve analogue. Proposition 2 gives the full continuous ellipse pedal area pi(a²+b²+|M|²)/2. Neither claims phase invariance for a finite Poncelet sample. The classical circle dependence explains the reduction below; it leaves phase dependence of its centered value and radial coefficient.

Theorems 1-3 address interpolated or other pedal-like **curves**, including special boundary-point isocurves; Appendix B's general formulas remain curve-area statements. A continuous area integral cannot simply replace the finite shoelace sum.

Source: [Hsu et al., Topics on Pedal Polygons, arXiv:2108.08293](https://arxiv.org/pdf/2108.08293), Definitions 2.1-2.3, Theorems 2.5,2.8,2.10 and Section 3 checked. Theorem 2.8 conserves the **sum** of inner/outer areas under a rotation parameter in their pair-of-polygons construction. Its V,W are fixed polygons; the target outer tangent polygon changes shape with billiard phase. No substitution identifying the varying Poncelet phase with that fixed-shape rotation is supplied.

### Recent general results screened by their exact hypotheses

[Garcia-Gheorghe, Poncelet Pairs via Isogonal Conjugacy](https://link.springer.com/article/10.1007/s00010-026-01274-w), published 16 March 2026: introduction, Theorems 3.1,4.2,5.1,6.1, and Corollary 6.3 checked on the publisher full-text page. These are circle/ellipse **3-Poncelet** and isogonal locus/envelope results. They do not state the target even-period pedal invariant.

[Murad, An Affine Approach to Metric Invariants of Poncelet Polygons](https://www.preprints.org/manuscript/202607.1243), July 2026: Sections 2.1-2.3, Lemmas 1-2 and Corollaries 1-5 checked on the author-submitted full-text page. The averaging lemma requires rotationally symmetric vectors; applications are odd polygons between **homothetic** ellipses. Distinct noncircular confocal ellipses are not homothetic. An affine transformation cannot change that homothety relation, and perpendicular projection additionally fails affine covariance.

### Explicit coverage gaps

The 250-page book *Discovering Poncelet Invariants in the Plane* (Garcia-Reznik, IMPA, 2021) was confirmed in the [publisher catalog](https://impa.br/editora/coloquios/) and [author bibliography](https://ronaldo.ime.ufg.br/p/2316-anos-2004-2021). Attempts to retrieve the presumed official PDF returned HTTP 400. No book full-text claim is made, and third-party Scribd copies were not used. This is a remaining bibliographic coverage gap, not evidence that the target is new. The source family's original table and its proof-question marks are historical evidence only.

## 3. A checkable reduction of the every-M quantifier

This derivation is independent of the candidate's quotient-divisor proof. It is classical pedal geometry in a convenient notation, and no novelty is claimed.

Represent the plane by complex numbers. Write consecutive tangent sidelines as

    Re(z conjugate(n_i)) = h_i,   |n_i|=1.

Here n_i is the outward unit normal, h_i the real support distance, and m is the fixed pedal point. Orthogonal projection gives

    q_i(m) = m + (h_i - Re(m conjugate(n_i))) n_i
           = m/2 + h_i n_i - conjugate(m) n_i²/2.

Set p_i=h_i n_i and v_i=n_i². Translation by m/2 does not affect area. Since signed area of a complex polygon z_i is (1/2) Im sum conjugate(z_i) z_(i+1), expansion yields

    B_m = B_0 + |m|² S/8
          - (1/4) Im sum [m conjugate(v_i) p_(i+1)
                         + conjugate(m) conjugate(p_i) v_(i+1)],

    S = Im sum conjugate(v_i) v_(i+1)
      = sum sin(2(psi_(i+1)-psi_i)).

For an even primitive elliptic-caustic billiard, central symmetry gives n_(i+N/2)=-n_i and h_(i+N/2)=h_i. Consequently p changes sign and v does not under the half shift. The two linear sums cancel in pairs, with no assumption about their numerical values. Therefore

    B_M(t) = B_0(t) + |M|² S(t)/8.                         (R)

The formula is valid for signed star polygons in orbit order and reversal. If some area or S vanishes, the identity still holds; there is no division. It also works for any centrally symmetric cyclic list of real sidelines, independently of a billiard.

Multiplying (R) by A'(t) proves the exact equivalence

    [A'B_M constant for every fixed M]
       iff [A'B_0 constant and A'S constant].              (E)

The forward implication follows by setting M=0 and then a unit vector. The backward implication is immediate. Combining with the credited AA'=K gives a sufficient form B_0=c_0 A and S=c_1 A. This is what the candidate proves in stronger all-M form B_M=c_M A. The centered identity alone is insufficient to infer the arbitrary-point identity; the radial coefficient also needs control.

The exact script independently checks (R) on a six-line central fixture with rational normals. It gives

    B_M = 1464/65 + (2688/4225)(x²+y²),
    S = 21504/4225.

That finite check corroborates the signs and factors in the derivation; it is not the proof of its generality.

## 4. Why the apparent transfer shortcuts stop

**Affine normalization.** Let L=diag(2,1), M=0, and the line be x+y=1. Its foot is (1/2,1/2), whose image is (1,1/2). The image line is x/2+y=1; its Euclidean foot is (2/5,4/5). Thus even a fixed affine normalization of a conic pair does not preserve target feet. It does preserve area ratios/products up to a constant multiplier for polygons actually mapped by L. These are different premises.

**Polarity and inversion.** For a line R_i dot z=1 and fixed M, the pole relative to the unit circle centered at M has displacement r_i=R_i/(1-R_i dot M). Inversion of that pole has displacement

    r_i/(r_i dot r_i) = (1-R_i dot M) R_i/(R_i dot R_i),

which is precisely the perpendicular-foot displacement. This establishes a geometric identification, but for a polygon r_i inversion changes its area into

    (1/2) sum det(r_i,r_(i+1)) /
                  [(r_i dot r_i)(r_(i+1) dot r_(i+1))].

The weights vary with vertex and phase. No fixed multiplier or perimeter-to-area implication follows. The special bicentric theorem controls limiting-point pedal perimeter; it supplies neither these weighted area traces nor arbitrary M.

**The pedal locus is generally not a conic.** At M=0 put R=diag(1/a²,1/b²)P. The pedal point q=R/(R dot R) lies on

    (q_x²+q_y²)² = a² q_x²+b² q_y².

For a>b this is the usual quartic pedal locus, not the original conic. For example, its axis points are (+/-a,0),(0,+/-b), while the diagonal-normal point is (sqrt(a²+b²)/2,sqrt(a²+b²)/2), which does not lie on the axis ellipse unless a=b. Hence a theorem about two Poncelet conics cannot simply be re-applied with the pedal vertices as a new Poncelet polygon. Special focal/circular degeneracies do not establish the every-M quantifier.

**Elliptic-function constancy.** Being a cyclic trace on a torsion elliptic curve does not make a meromorphic function constant. For any nonconstant elliptic f with a pole at x_0, the sum over the N translations typically still has poles on the orbit of x_0. The classical theorem says a holomorphic function on the compact curve is constant. Proving the requisite pole cancellation is the central target-specific step.

For the accepted candidate, the genuinely required checks are that the rational foot denominator's isotropic zeros are common-tangent contacts, their translation orbits meet the two billiard-area pole classes using 2k=1-N/2 mod N, and their adjacent residues cancel the possible double poles. Only then can genus-one Riemann-Roch and orientation reversal force B_M=c_M A. Calling Riemann-Roch or the Poncelet map a general theorem does not remove those checks. The congruence fails when 4 divides N, so it is not a dispensable parity decoration.

## 5. Exact counterlimitation to the moment shortcut

Use E: x²/4+y²=1 and caustic x²/(16/5)+y²/(1/5)=1. Two exact least-four-period members, in the indicated order, are

    P^(1) = ((2,0),(0,1),(-2,0),(0,-1));
    P^(2) = ((4,1),(-4,1),(-4,-1),(4,-1))/sqrt(5).

The script checks the boundary equations, caustic tangency, reflection law, and all area/moment statements with exact radicals. Both have four distinct vertices; neither is a padded two-period orbit.

| Quantity | First phase | Second phase |
|---|---:|---:|
| A | 4 | 16/5 |
| A' | 8 | 10 |
| AA' | 32 | 32 |
| Outer-pedal centroid | M/2 | M/2 |
| Sum squared foot distances from M | 10+2|M|² | 10+2|M|² |
| S | 0 | 0 |
| B_M, for every M | 4 | 5 |
| A'B_M | 32 | 50 |

Thus the exact BT foot moments and even-period AA' identity can coexist with variable outer-pedal products. This is **not a counterexample to the target**: N=4 is explicitly excluded. It falsifies the proposed theorem substitution without the additional N=2 mod 4 mechanism.

The exact controls use explicit exceptions, not Python assertions, and are run in ordinary and optimized modes. Existing SymPy 1.14.0/mpmath packages from the shared research runtime are read without installing or copying dependencies. The initial system and bundled Python attempts lacked SymPy; the successful commands use the already-recorded shared package directory and Python 3.14.6. No source executable was downloaded or run.

## 6. Editorial interpretation and remaining work

The strongest verified contribution that this family can support is an independently checkable exposition/proof package for the **previously tabulated** every-point outer-pedal invariant under an explicit least-period, nondegenerate elliptic-caustic convention, with primitive-star scope, signed-zero handling, exact controls, and clear dependency credit. A methodological novelty claim about elliptic complexification, pole cancellation, Poncelet translation, or genus-one Riemann-Roch is not supported: those are established mechanisms.

The relation B_M=c_M A is target-specific work in this package, but “not found as a corollary of the audited general theorems” is not “new to the literature.” The exact-target October 2026 preprint and the unread IMPA book prevent priority promotion on this family's evidence. Root's separate priority family must resolve the former and decide the appropriate bibliographic/editorial positioning. No claim that the source's historical question mark means currently open is permissible.

The all-M theorem should not be weakened to a focus-only, centered-only, convex-only, or sampled-N assertion. Conversely, no unrestricted traversal-count or hyperbolic extension follows from the inspected literature. The source correction must accompany any later manuscript and metadata.

Bounded-audit completion: 100% of the assigned general-theorem implication assessment, with the listed book/later-history coverage limitations retained. Priority/publication clearance: **false**. No publication, Git, PR, index, branch, or checkout mutation was performed.
