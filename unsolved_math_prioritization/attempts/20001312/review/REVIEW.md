# Independent review: the four-direction ridge-profile obstruction

**Verdict: PASS_COMPLETE_CREDITED_COUNTEREXAMPLE.** The sixteen-point certificate proves a negative answer to the recovered AIM Problem 22 for its stated four directions. The analytic, positively curved body and the almost-everywhere strengthening are valid consequences. No mandatory correction is required. Recommend **already_solved**, as recovery of a consequence of Gritzmann–Langfeld–Wiegelmann's published 2011 obstruction; retain the one validation/certificate approach actually recorded. No historical novelty or human peer review is certified.

Reviewed artifact: KNOWN_COUNTEREXAMPLE.md, SHA-256 cb3bbab9b132e181b214e40340f604daa2ae2be1d993ca03abb3fc86154ebfd0. All 548 submitted exact assertions reproduce their receipt byte-for-byte. The independently written checker passes 537 assertions.

## 1. The precise source question

I read the complete seven-page [official AIM list](https://aimath.org/WWN/fourierconvex/fourierconvex.pdf) and visually inspected page 6. Problem 22 is the ridge-function question by A. Daurat and R. Gardner. It asks whether every planar convex body is the nonnegative superlevel set of a sum of four real-valued measurable ridge functions, for the four listed directions. The slab discussion starts at the separate heading Problem 23. Its appearance in the imported record is extraction spillover and does not make it part of this target.

The written ridge formula uses a profile of an inner product with a direction vector. The actual linear forms in the candidate are therefore x, y, 2x+y, and −x+2y, up to nonzero scalar normalization. Replacing a normal by its unit multiple is absorbed into its unrestricted one-variable profile.

There is also a normal-versus-line convention in the tomography background. The perpendicular directions to these four normals are, up to nonzero scalar multiples,
\[
(0,1),\quad(1,0),\quad(-1,2),\quad(2,1).
\]
Thus a quarter-turn permutes the same four unoriented directions. The source's notational convention cannot change this particular obstruction.

The proof permits all finite-valued real profiles. The pointwise result even permits nonmeasurable profiles, so it cannot have lost examples through an unstated integrability, continuity, or polynomial restriction. The almost-everywhere statement retains measurability and uses no integration of the profiles.

## 2. Published prior work and its implication

I read the relevant definitions, Section 2, Remark 2.3, and Figure 1 in the complete [Gritzmann–Langfeld–Wiegelmann paper](https://mediatum.ub.tum.de/doc/1370776/document.pdf), and visually checked printed pages 1593–1594. The article is SIAM J. Discrete Math. 25 (2011), 1589–1599; its first page records electronic publication on 22 November 2011.

Remark 2.3 explicitly identifies the lattice points in the square with vertices (2,4), (−4,2), (−2,−4), (4,−2) as nonadditive for the same direction set. Figure 1 supplies a distinct tomographically equivalent finite set. This is prior work, not a new example found by the campaign.

The passage from that discrete statement to a continuous-body counterexample is legitimate. A hypothetical ridge score for the square would be nonnegative on the finite lattice set F and negative on the finite tomographic grid outside F. The finite collection of negative scores has a strict uniform gap from zero. Adding a sufficiently small positive constant to one profile and rescaling would give strict positive and negative separating weights on the grid, which is precisely discrete additivity. This contradicts the published nonadditivity. The article need not explicitly mention the AIM problem for this elementary implication to hold.

The candidate additionally provides its own exact finite certificate, so its conclusion does not depend on recovering coordinates from the figure or on a numerical optimizer. The smooth-body and null-set consequences are proved in the submitted artifact; their historical priority remains unconfirmed.

## 3. The finite certificate and its signs

I independently recalculated the four projected multisets of P and N. For x and y both are
\[
\{-4,-3,-2,-1,1,2,3,4\};
\]
for 2x+y and −x+2y both are
\[
\{-8,-7,-6,-1,1,6,7,8\}.
\]
The sets contain eight distinct points each and are disjoint.

For every choice of finite-valued profiles, finite regrouping therefore gives
\[
\sum_{p\in P}\sum_i g_i(\ell_i(p))
=\sum_{n\in N}\sum_i g_i(\ell_i(n)).
\]
This remains true after every common translation, since each of the four multisets is shifted by one common scalar. There is no interchange of an infinite sum or an integral.

For the square K_0, the invertible coordinate map (u,v)=(x−3y,3x+y) sends its vertices to the corners (±10,±10). Direct oriented-halfplane checks show that P lies in the square and N lies outside it. Some positive points lie on its boundary, which is allowed by the literal superlevel convention. Consequently the left finite sum would be nonnegative and the right finite sum strictly negative. That proves the pointwise contradiction.

The independent program also confirms the 45-point lattice count and a polynomial certificate. If
\[
H(X,Y)=\sum_{p\in P}X^{p_x+4}Y^{p_y+4}
       -\sum_{n\in N}X^{n_x+4}Y^{n_y+4},
\]
then exact multiplication verifies that H is divisible by
\[
(X-1)(Y-1)(X-Y^2)(X^2Y-1).
\]
These factors independently explain the four vanishing projected Laurent polynomials. The checker contains the full quotient and verifies every coefficient, rather than testing the factorization numerically.

## 4. The analytic convex body and its uniform margin

Write A for the displayed coordinate matrix. I checked \(A^TA=10I\), the polynomial expansion, and
\[
\nabla^2\Phi
=A^T\operatorname{diag}(56u^6+2,56v^6+2)A
\succeq20I.
\]
In particular, the level subbody is convex. Coercivity follows already from \(\Phi\ge u^2+v^2=10(x^2+y^2)\), and continuity at the origin gives nonempty interior. Since each coordinate derivative \(8u^7+2u\) vanishes only at zero and A is invertible, the positive level has no critical point. The real-analytic implicit-function theorem supplies its analytic boundary. On every nonzero tangent vector, the level's second fundamental form is the strictly positive Hessian quadratic form divided by the nonzero gradient norm. This proves positive curvature everywhere, rather than inferring it just from strict convexity.

Independent integer evaluation reproduces the positive values 100000100 and 200000200 and the negative values 214365572 and 220123852. The level 210000000 lies strictly between the two classes.

If \(\lVert h\rVert_\infty<1/1000\), both transformed coordinates change by less than 4/1000. Hence all positive translates have value at most
\[
2(2501/250)^8+2(2501/250)^2<210000000,
\]
whereas every negative translate has a coordinate of absolute value at least 2749/250 and therefore value at least
\[
(2749/250)^8>210000000.
\]
Both inequalities hold exactly as rational inequalities. They supply a uniform open neighborhood of admissible shifts, not a finite-grid approximation to one.

## 5. Arbitrary null-set changes and continuous X-rays

Suppose the ridge threshold set differed from K_* only in a planar null set Z. The shifts placing any one of the sixteen certificate points in Z form a translate of Z and are null. A finite union of these sets cannot cover the open square of admissible shifts. At a shift outside that union, all positive points receive nonnegative scores and all negative points strictly negative scores. The translated finite-sum identity is contradictory.

This proves the claimed almost-everywhere exclusion with no local integrability or essential-boundedness assumption. It neither evaluates a profile integral nor presumes that a pointwise exceptional set is absent before choosing the shift.

The patch replacement is also valid. The sixteen translated open squares are pairwise disjoint, because their centers are distinct integer points and their side length is 1/500. The uniform margin puts the positive patches inside K_* and the negative patches outside. Thus the indicator identity is pointwise correct and the modified bounded measurable set differs by positive area.

For a fixed linear form, two patch centers with the same value differ by a vector in its kernel. Translating along that kernel preserves every line-integral X-ray in that direction. Matching the multisets therefore cancels patch contributions on every line, including exceptional lines through patch boundaries. These are integrals of bounded indicators, not of the unrestricted profiles.

As an additional check, the independent program directly intersects each line with each open patch at all its section-function breakpoints and interval midpoints, treating boundary-parallel lines separately. It also exhibits endpoints of a segment retained in the body whose midpoint is removed, confirming that the competitor is not convex. Therefore no uniqueness theorem restricted to convex competitors is contradicted.

## 6. Validation and publication recommendation

The submitted 548 assertions reproduce exactly. The 537 independent assertions cover the polynomial factorization, oriented-halfplane membership, expanded Hessian and curvature numerator, strict rational margins, direct patch X-rays, and the nonconvex competitor.

Run:

    python author_replay/verify.py
    python independent_checks.py

The original Problem 22 is completely answered negatively, with **already_solved** recommended because its decisive obstruction is a published 2011 result. Preserve the actual one-family validation record instead of presenting this as a new open-problem discovery. The smooth and almost-everywhere corollaries are valid, but no priority is established for them. Problem 23's slab questions remain outside this artifact. This review is independent adversarial AI checking, not human peer review.
