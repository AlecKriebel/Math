# Independent source and proof audit: focal-angle invariant k120

## Verdict

**PASS_COMPLETE_CREDITED_BICENTRIC_CONSEQUENCE. No mandatory correction to the frozen reduction.**

Reviewed `SOURCE_STATUS.md` SHA-256:
`46365cd0bb5e81459072d2c749aadd2e048af98d7ea7da4a98a29ff69e9d1445`.

The exact focal-angle sum is a consequence of the published 2021 bicentric cosine-sum theorem, with the polar-duality and ordinary-angle bridge proved in the submission. The result covers every nondegenerate period and star winding in the original nested-confocal-ellipse setting. It is appropriately recorded as **already_solved**, retaining the one reduction/validation family. It is not a new-discovery claim.

All **30,804 submitted assertions** reproduce byte for byte. The independent checker passes **43,158 exact controls**. The all-period conclusion rests on the written geometry and the published elliptic-function argument, not on a bounded set of sampled polygons.

This report includes an explicit winding-parity clarification for the published Jacobi parametrization. That clarification closes a convention issue in reading the source proof and must remain available with the public audit. No change to the mathematical conclusion is needed. This is independent adversarial AI review, not human peer review or historical-priority certification.

## 1. Exact statement and primary sources

I independently read the original arXiv v11 definitions and Table 2, printed p.5, and the corresponding published table on p.345. The original k120 is the sum of cosines of the ordinary focal angles between consecutive orbit vertices, for all periods. Its suggestion is credited there to A. Akopyan. The pair of confocal conics in this source is a pair of strictly nested ellipses. The proof does not import the distinct antipedal or outer-tangent constructions.

I read Theorem 1 and its full proof, pp.623--624, Section 2 pp.621--623, and Appendix C p.632 in Roitman--Garcia--Reznik, [*New Invariants of Poncelet--Jacobi Bicentric Polygons*](https://amj.math.stonybrook.edu/pdf-Springer-final/021-0188.pdf), Arnold Mathematical Journal 7 (2021), 619--637. The theorem and polar appendix were also visually inspected. The journal title, publication date of 18 August 2021, and theorem scope match the submission. The author preprint [arXiv:2103.11260](https://arxiv.org/abs/2103.11260) is secondary to that full published text in this audit.

The published theorem concerns the ordinary internal-angle cosine sum for bicentric Poncelet polygons, rather than a claim confined to triangles. The explicit argument below verifies the winding issue instead of relying on the word “all” alone. The published Appendix C gives the same polar-circle centers and radii as the submission, after translating to the chosen focus and reflecting the sign convention for the focus if necessary.

## 2. Polar circles and strict nesting

For a translated confocal ellipse with center (-c,0), semiaxes A,B and A²-B²=c², the support equation for a tangent line q dot p=1 is

\[
-cq_x+\sqrt{A^2q_x^2+B^2q_y^2}=1.
\]

Squaring yields B²|q|²-2cq_x-1=0. The resulting circle has center (c/B²,0) and radius A/B². On that circle the least possible value of 1+cq_x is A/(A+c)>0, so squaring has introduced no extraneous branch. This check is particularly important for distinguishing the intended compact ellipse from a hyperbolic polar configuration.

The outer billiard ellipse dualizes to the inner circle and the caustic to the outer circle. With A'=sqrt(a²-lambda), their strict separation is exactly

\[
R-r-|C'-C|=\frac1{A'+c}-\frac1{a+c}>0.
\]

Thus the inner circle lies strictly inside the outer one. Their center distance d is positive when a>b and lambda>0; the modulus used by the published theorem satisfies

\[
0<\frac{4Rd}{(R+d)^2-r^2}<1,
\]

because R-d>r. The circular limiting case is handled separately by the elementary constant-step argument.

The common focus lies strictly inside both original ellipses. No caustic tangent can therefore pass through it. Consequently consecutive focal position vectors are linearly independent, all polar intersections are finite, and the original-to-polar construction is nonsingular. The explicit positive side-length formula below also shows that neighboring polar vertices are distinct. These facts rule out all zero-denominator and collapsed-side concerns in the submitted reduction.

## 3. Orientation and ordinary angles, including stars

Choose the oriented billiard branch with the caustic on the left. The focus is on the same side, so det(p_i,p_(i+1))>0. The directed increment delta_i of their unit vectors lies strictly between zero and pi. In particular its cosine agrees with the ordinary nonnegative angle at the focus; there is no signed-angle substitution.

Writing u_i=p_i/|p_i|, the polar line is

\[
u_i\cdot(q-C)=r,
\]

with the **positive** support number r. This follows from the exact focal-distance identity

\[
1-C\cdot p_i=(a^2-cx_i)/b^2=r|p_i|>0.
\]

At its contact point T_i=C+r u_i, the neighboring tangent intersections are

\[
Q_i=T_i+r\tan(\delta_i/2)Ju_i,\qquad
Q_{i-1}=T_i-r\tan(\delta_{i-1}/2)Ju_i.
\]

Both tangent lengths are positive. Therefore the actual side Q_(i-1)Q_i points along Ju_i and contains T_i in its interior. At Q_i, the two rays defining the ordinary internal angle point along -Ju_i and Ju_(i+1). Their dot product is exactly -u_i dot u_(i+1). Hence the angle identity in the submission is correct, without an absolute-value or winding-dependent sign.

This argument is local and does not require convexity of the full polygon. For a star, the actual ordered vertices and contact points are retained; no convex-hull reorder is performed. Every directed polar side has the inner circle on its left. Polarity and its inverse preserve the cyclic orbit order, and repeated traversal repeats every summand. Thus the relevant bicentric family really has the required period and order.

As an independent diagnostic, I checked closed rational tangent polygons in both orientations, including winding-five twelve-vertex stars. Their ordinary side vectors, interior contact parameters and whole-polygon cosine bridge satisfy the formulas exactly. These auxiliary tangent polygons are not asserted to be bicentric, and are used only to test the sign and winding geometry.

## 4. The published cosine-sum proof and the winding-parity convention

There is a small issue one must not overlook in reading Section 2 of the cited paper. It writes

\[
p_j(u)=R(\cos(2\operatorname{am}(u+j\sigma)),
             \sin(2\operatorname{am}(u+j\sigma))),\qquad
\sigma=4\tau K/N.
\]

The geometric point p_j has real period 2K in its argument, whereas the vector v=(cn,sn) has period 4K and changes sign under a shift of 2K. Thus taking the printed positive integer tau at face value directly covers even winding, and does not by itself describe every primitive even-period family. The frozen submission invokes the theorem rather than this numerical parametrization, but an all-winding audit still has to address it.

Here is an explicit verification using the paper's own pole-cancellation mechanism. For a primitive period n>=3 and winding w, use the actual step

\[
\sigma=2wK/n,\qquad \gcd(w,n)=1.
\]

Choose the direction so that 0<sigma<2K. The lifted Jacobi amplitudes increase by an amount between zero and pi at each step. Therefore the elementary chord calculation gives the ordinary internal-angle cosine as

\[
-\,v(u+(j-1)\sigma)\cdot v(u+(j+1)\sigma).
\]

Now sum over **2n indices**, a doubled traversal. This has sigma=4wK/(2n), precisely the published period convention, and v(u+2n sigma)=v(u). Each dot-product summand repeats after n indices because both vector factors acquire the same sign (-1)^w. Hence the doubled sum is exactly twice the actual geometric sum.

The doubled sum is a meromorphic elliptic function of u. At a pole of v(u+j sigma), the only potentially singular terms involving that factor have coefficient

\[
-\,[v(u+(j-2)\sigma)+v(u+(j+2)\sigma)].
\]

The published odd symmetry about each Jacobi pole makes this coefficient zero at the pole. Both neighboring factors are regular: their shifts 2sigma cannot be an integer multiple of 2K, since that would say 2w/n is an integer, impossible for primitive n>2. This observation excludes the possible adjacent double-pole exception. Pole indices repeated n steps apart in the doubled list cause no difficulty; they are nonadjacent in this sense and the same cancellation applies to each occurrence.

Every apparent pole is therefore removable. The function is doubly periodic and entire, hence constant. Its half, the original ordinary-angle cosine sum, is constant too. Repeated orbits reduce to their primitive period. This verifies the full winding scope while preserving the credit to the published theorem and its analytic mechanism.

The common periods, simple poles and local odd symmetry are stated on the primary paper's p.623; their standard Jacobi setting is also consistent with [NIST DLMF Section 22.4](https://dlmf.nist.gov/22.4). No new all-period invariant theorem is claimed in this review. The clarification is about indexing the established proof without losing a parity class.

## 5. The final implication and attribution

The polar polygon lies on one fixed outer circle and is tangent to one fixed strictly interior circle. Its ordered family satisfies exactly the geometric assumptions just audited. Summing the local angle identity gives

\[
\sum_i\cos\angle(P_i f P_{i+1})=-\sum_i\cos\theta_i(Q).
\]

The right-hand side is constant by the published bicentric theorem, with the winding convention clarified above. The other focus follows by reflection. The source only asks for constancy, so no closed expression for that constant is missing from the target.

This result is independent of the campaign's k603/k405 and the concurrent k107/k108/k114 targets. In particular the printed-product counterexamples for other table rows do not invalidate this polar-angle consequence. The original source's strictly nested confocal ellipses, positive focal distances, nonsingular polar intersections and ordinary-angle convention are retained. Hyperbolic caustics and degenerate two-bounce cases are outside the audited scope.

The imported report's earlier failure to locate the bicentric consequence should not retain an open-status label for this exact target. The appropriate disposition is a credited known-result correction, with no historical-priority or new-discovery claim.

## 6. Verification and reproducibility

The submitted checker was copied with its frozen dependency and run outside the author's directory. It writes its receipt; the result is byte-identical to the submitted `verification.json`: **30,804 assertions**.

The independent checker uses only exact rational arithmetic and the Python standard library. Its **43,158 assertions** cover:

- 12 separately parameterized rational confocal pairs, dual-circle equations, the unsquared support branch, strict nesting and modulus range
- Exact polar contact points and focal distances
- 24 closed ordered tangent-polygon configurations, including stars and reversed orientations, with positive tangent lengths and ordinary-angle signs
- 3,042 primitive winding/period pairs through period 100, testing doubled traversal and exclusion of adjacent pole collisions

These are finite diagnostics, not a sampled proof of all-period closure or invariance. The written source and proof audit supplies that step. No author mathematics or public repository state was modified by this reviewer.

`review_summary.json` lists the publication files. Keep `author_replay/SOURCE_STATUS.md`, which the independent checker hashes. Exclude redundant replay files and all third-party full PDFs and rendered source images.
