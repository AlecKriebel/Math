# Independent reconstruction, frozen before reading audit verdicts

Reconstructed between the observed UTC bounds 2026-10-16T06:53:32Z and 2026-10-16T06:55:06Z from the final manuscript and direct primary texts, without consulting earlier favorable audit reports.

## Exact claim
Fix a>b>0 and 0<lambda<b². The pair E=(a,b), C=(sqrt(a²-lambda),sqrt(b²-lambda)) has an oriented Poncelet translation of exact order N=2m, m odd >=3. For every fixed finite real M, signed cyclic areas A'=area of intersections of successive boundary tangents and B_M=area of feet on those boundary tangents satisfy A' B_M independent of phase. Stars are traversal-order shoelace sums. The claim is neither a positive-area nor a face-area claim, and does not pad odd least periods to eligible list lengths.

## Curve and order
E and C intersect at x²=a²(a²-lambda)/(a²-b²), y²=-b²(b²-lambda)/(a²-b²), four distinct transverse points. The incidence curve X of boundary point and caustic tangent is the connected double cover of E with these four simple branch points, hence a smooth genus-one curve. The endpoint involution sigma and tangent-choice involution tau are branched degree-two deck involutions, so each acts by -1 on the one-dimensional differential space. T=tau sigma consequently has derivative +1 and is a translation. A single orbit's least period N forces its translation order to be N globally; this is stronger than merely listing N vertices.

Plane inversion I commutes with T and preserves each real directed component. That component is a circle, and the finite abelian group <I,T> can be made isometric by averaging a metric. Its orientation-preserving action consists of circle rotations; the nonidentity involutions I and T^m must be identical. Identity on the real circle extends to connected X, so I=T^m. This proof does not assume convex traversal: coprime winding for even N has odd numerator. T has no fixed points, and Y=X/<T> is an unramified genus-one quotient.

## Two poles of original area
P has simple coordinate poles at two infinity points e_±=[a:±ib:0], with two unramified flags over each. I exchanges the flags at each infinity, so quotient support S has at most two points. No adjacent P_i,P_{i+1} both diverge: distinct infinities would require L∞ tangent to C, and coincident infinity requires the E tangent there to be C tangent. Its dual C value is lambda(1/b²-1/a²), not zero. Thus A has at most simple poles in S.

For real orientation with C left of each chord, origin is strictly to the left of every chord and det(P_i,P_{i+1})>0. This includes stars because the support line separates origin from its right half-plane regardless of winding. A>0 and reversal tau negates A, so A is nonconstant. A nonconstant genus-one meromorphic function cannot have one simple pole. Therefore S has exactly two distinct points and both are actual simple poles. Riemann--Roch gives dim L(S)=2 and {1,A} is a basis.

## Pedal poles and exhaustive contact indices
Set R=(x/a²,y/b²), d=R.R (complex bilinear). Q=M+(1-R.M)R/d. At e_±, d has leading nonzero double pole because (1/a,±i/b) has norm 1/a²-1/b² !=0; Q is regular.

The only finite denominator zeros are x²=a⁴/(a²-b²), y²=-b⁴/(a²-b²). They are simple on E: substituting y²=b²(1-x²/a²) makes d affine in x² with nonzero coefficient and x,y both nonzero. The E tangent there is a C tangent because the difference of dual equations is lambda d. Conversely every common tangent contact has d=0. These contacts are not E∩C: C(P)-1=-lambda²/((a²-lambda)(b²-lambda)), so pi is unramified and each foot has order <=1.

At a common-tangent flag z, sigma z=z and tau z=Tz. Solve 2k=1-m modulo 2m (possible precisely because m is odd). Then tau T^k z=T^(1-k)z=T^(m+k)z=I T^k z; equal projections imply P(T^k z) is a fixed point of inversion, hence infinity. All pedal poles therefore project to S.

If T^j z is sigma fixed, sigma T^j z=T^-j z=T^j z, i.e. 2j=0 mod 2m, so j=0,m. A contact's two flags are z and Tz. Consequently the complete singular foot index set in this orbit is {0,1,m,m+1}. No additional contact can enter the orbit without another sigma fixed flag. For m>=3 the only adjacent singular pairs are (0,1),(m,m+1); m=3 produces no hidden wrap adjacency. In a common local parameter, residues at the first pair are each scalars times R(P), and at the second pair scalars times R(-P). Determinants of residue pairs vanish, so all t^-2 coefficients cancel term by term, without needing equal residues or nonzero residue assumptions. B_M has at most simple poles in S. Since descent is unramified, B_M belongs to L(S).

Thus B_M=c_M A+d_M. Reversal with M fixed negates both area traces, forcing d_M=0. No area division occurs. In particular c_M=0 and negative B_M create no exception.

## Independent verification of credited AA' law
The chord map rho:X->C* has deck sigma. Polarity with E sends L=[u:v:w] to W=[a²u:b²v:w], exactly the intersection of endpoint tangents. W has a coordinate pole only at w=0, the two origin-through tangents to C. Each meets E in distinct finite opposite points because its direction has nonzero E quadratic value lambda(1/a²-1/b²). Thus rho is unramified and W has only simple poles. Adjacent poles would require two such chord lines to meet at an E vertex: distinct lines meet at origin (not E); identical lines force an E point equal to their C contact at infinity (also not E). Hence A' has only possible simple poles on a support R0.

At original infinity tau x=Ix=T^m x, so sigma x=T^(m-1)x. A shift satisfying 2k=m-1 yields a sigma-fixed representative in each S orbit. At a W pole, opposite endpoints imply sigma x=Ix=T^m x, so tau x=T^(m+1)x. A shift satisfying 2k=m+1 yields a tau-fixed representative in each R0 orbit. Both congruences are soluble for odd m. An orbit with a sigma fixed representative cannot contain a tau fixed point: it would require 2j=1 mod even N. Hence S and R0 are disjoint.

At a tau-fixed representative, pi(T^j z)=pi(T^-j z); the finite vertex list is palindromic, so its signed area is zero by reversing the cycle. At a sigma-fixed representative, rho(T^j z)=rho(T^-j z); the finite W list is palindromic and its area is zero. Thus A zeros cancel all possible simple A' poles, and A' zeros cancel all actual A poles. AA' is holomorphic on compact Y and constant. Therefore A'B_M=c_M AA' is constant. This is a self-contained check of a credited known law, not a novelty argument.

## Boundary and interpretation checks
Real outer vertices are finite because parallel E tangents would be antipodal and the corresponding center-crossing chord cannot touch the proper inner ellipse. Real d>0. Reversal changes both factor signs. No positivity of B_M, no bounded side-foot condition, and no uncrossed polygon condition enters the proof. m even breaks the requisite congruences; a=b breaks the nonisotropic infinity argument; lambda=0 or b² breaks smoothness/nesting; hyperbolic/nonconfocal pairs and arbitrary repeated lists are excluded. Odd repetition of an eligible even primitive orbit scales each area by the repetition and preserves constancy, but is not needed to extend the stated least-period theorem.

## Primary-text comparison
Ferudun v1.0, sections 1 and 3–7, gives this exact theorem (Theorem 1), arbitrary M radial dependence, general six-period formula and an explicit repeated-three-period control. Its local analytic argument uses central pairing, isotropic projection poles, parallel residues and complementary reversal zeros. The current formulation moves through the quotient two-pole L(D) argument, but makes no theorem or mechanism novelty claim. Chavez-Caliz journal section 2 supplies the flag translation and section 5/Theorem 6 supplies AA' for even concentric Poncelet families. The present explicit odd-half-period palindrome check avoids importing unclear generic local assertions from that text.

Provisional mathematical conclusion: no substantive gap found. This is not yet the final whole-package verdict; execution, physical boundaries, PDF and archive remain to check.

## Additional real nonvanishing check for the positioning statement
The manuscript observes that the already-known product theorem together with nonzero real AA' implies proportionality, so proportionality alone is not theorem novelty. Nonzero AA' can also be checked directly: normalize P_i=(a cos theta_i,b sin theta_i), taking each forward increment delta_i in (0,pi) because the caustic contains the origin to the left of each chord. Then
V_i=diag(a,b) sec(delta_i/2) (cos(theta_i+delta_i/2),sin(theta_i+delta_i/2)).
Successive midpoint increments are (delta_i+delta_(i+1))/2 in (0,pi). Therefore every det(V_i,V_(i+1)) is positive, even for a star. Both A and A' are strictly positive in the chosen orientation; reversing changes both signs. Thus their constant product is nonzero on real phases. This fact is used only to validate the manuscript's honest-positioning observation, not to repair its proof.
