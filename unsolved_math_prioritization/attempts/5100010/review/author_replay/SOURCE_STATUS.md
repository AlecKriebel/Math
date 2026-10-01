# Focal-angle invariant k120 as a known bicentric consequence

**5100010 / AMR-050-0010. Source-status result: already implied by a published 2021 theorem in the intended confocal-ellipse setting. Separate review pending. No new-discovery claim.**

## 1. Exact source and prior result

Reznik–Garcia–Koiller, *Eighty New Invariants of N-Periodics in the Elliptic Billiard*, [arXiv:2004.12497v11](https://arxiv.org/abs/2004.12497v11), defines its billiard in Sections 1–2 using a pair of strictly nested confocal ellipses. Section 3.1 defines alpha_(j,i) as the angle P_i f_j P_(i+1). Table 2, p.5, labels the sum of cos(alpha_(1,i)) as k120, with all N, and credits its suggestion to A. Akopyan. The [published companion](https://amj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), *Arnold Mathematical Journal* 7 (2021), pp.341–355, retains this row on p.345.

Roitman–Garcia–Reznik, *New Invariants of Poncelet–Jacobi Bicentric Polygons*, [published version](https://amj.math.stonybrook.edu/pdf-Springer-final/021-0188.pdf), *Arnold Mathematical Journal* 7 (2021), pp.619–637, DOI [10.1007/s40598-021-00188-6](https://doi.org/10.1007/s40598-021-00188-6), **Theorem 1, pp.623–624**, proves that the sum of internal-angle cosines of a bicentric Poncelet family is invariant. Its Section 2 allows the periodic winding parameter, rather than restricting to triangles. Its **Appendix C, p.632**, identifies the focal polar image of a confocal ellipse pair as a nested circle pair. The elementary angle relation below makes k120 a direct consequence of those already published results.

The imported third-party literature triage did not identify this consequence. Its assertion that no general-N proof was found is therefore not used as a present mathematical status certificate. The source status here credits the published theorem, not a claimed discovery of a new invariant.

## 2. Precise theorem and domain

Let

    E: x^2/a^2+y^2/b^2=1, a>b>0, c=sqrt(a^2-b^2),
    E_lambda: x^2/(a^2-lambda)+y^2/(b^2-lambda)=1,
    0<lambda<b^2.

Fix a nondegenerate Poncelet family P_1,...,P_N between these two ellipses, N>=3, following one consistent tangent branch. The ordinary nonnegative angle alpha_i at either focus f between P_i-f and P_(i+1)-f has family-invariant cosine sum.

Both simple and star orbits are covered. Repeated traversal repeats the summands and preserves invariance. Hyperbolic or degenerate caustics are not the confocal-ellipse pair specified by the original source and are not added here. The source's outer tangent polygon P' is not the polar polygon used below; no identity between those constructions is assumed.

## 3. Explicit polar pair and nondegeneracy

Choose f=(c,0), translate f to the origin, and write p_i=P_i-f. Use polarity of a unit circle centered at f: the polar of p is the line

    ell_p: p dot q=1.

Set Q_i=ell_(p_i) intersect ell_(p_(i+1)). Then Q_i is the pole of the original billiard sideline. We now verify directly the circle pair stated in the published Appendix C.

In these translated coordinates, the ellipse with semiaxes A,B and focal distance c has equation

    (x+c)^2/A^2+y^2/B^2=1, A^2-B^2=c^2.

A line q dot (x,y)=1 is tangent to it precisely when

    -c q_x+sqrt(A^2 q_x^2+B^2 q_y^2)=1.

Squaring gives

    B^2 |q|^2-2c q_x-1=0,
    |q-(c/B^2,0)|^2=A^2/B^4.                         (1)

There is no extraneous branch on this circle: its minimum q_x is (c-A)/B^2=-1/(A+c), so 1+c q_x>=A/(A+c)>0. Thus (1) is exactly the polar envelope, with center C_B=(c/B^2,0) and radius A/B^2.

The dual of E is the inner circle, with center C=(c/b^2,0) and radius r=a/b^2. The dual of E_lambda is the outer circle, with center C'=(c/(b^2-lambda),0) and radius R=sqrt(a^2-lambda)/(b^2-lambda). These circles are strictly nested. Put A'=sqrt(a^2-lambda). Since A'<a and B'^2=b^2-lambda=(A'-c)(A'+c),

    R-r-|C'-C|=1/(A'+c)-1/(a+c)>0.                    (2)

Every ell_(p_i) is tangent to the fixed inner circle, and every Q_i belongs to the fixed outer circle by tangency of the original sideline to E_lambda. The focal distances |p_i| are positive because the focus lies strictly inside E. The focus also lies strictly inside E_lambda, so no original tangent sideline passes through it. Hence det(p_i,p_(i+1)) is nonzero, all Q_i are finite, and consecutive polar lines are distinct. The construction and its inverse depend continuously on the original orbit.

## 4. Ordinary angle signs, including star orbits

Orient the orbit so E_lambda is to the left of each directed side. The usual Poncelet tangent map preserves this choice; reversing the orbit handles the opposite branch. Since f is inside E_lambda,

    det(p_i,p_(i+1))>0.

Consequently the positively oriented increment delta_i between the unit vectors u_i=p_i/|p_i| and u_(i+1) lies strictly between zero and pi. Its cosine is precisely cos(alpha_i), independent of orientation convention for the ordinary angle.

Let J denote rotation through pi/2. The line ell_(p_i) can be written

    u_i dot(q-C)=r.

The positive sign is important. For P_i=(x_i,y_i), its focal distance is d_i=a-c*x_i/a; thus

    1-C dot p_i=(a^2-c*x_i)/b^2=r*d_i>0.

The inner-circle contact point is T_i=C+r*u_i. Intersecting neighboring tangent lines gives

    Q_i=T_i+r*tan(delta_i/2)*J*u_i,
    Q_(i-1)=T_i-r*tan(delta_(i-1)/2)*J*u_i.           (3)

Both tangent lengths are strictly positive. Therefore the actual polar side Q_(i-1)Q_i points along J*u_i, and its contact point is on the side segment, not merely its extension. At Q_i the two vectors defining the ordinary internal angle theta_i of the polar polygon point along -J*u_i and J*u_(i+1). Hence

    cos(theta_i)=-u_i dot u_(i+1)=-cos(alpha_i).      (4)

This is a local relation. It remains valid when the complete polygon is a star: the total winding may exceed one, but every delta_i and both positive tangent lengths in (3) retain the stated signs. No convex-hull reorder of the vertices is made.

## 5. Apply the published bicentric invariant

The Q_i form an N-periodic Poncelet polygon inscribed in the same fixed outer circle and circumscribed about the same fixed inner circle. Varying the original orbit gives members of this fixed bicentric family, with its order and winding retained. Roitman–Garcia–Reznik Theorem 1 applies. Summing (4) gives

    sum_i cos(angle P_i f P_(i+1))
      = -sum_i cos(theta_i),

which is constant on the original family. Reflection in the y-axis gives the identical conclusion for the other focus. No equality of the two focus-specific constants is needed for this argument.

In the circular limiting case the two foci coincide with the center and the Poncelet step is a fixed central angle, so the conclusion is also immediate. No parity restriction is introduced: the target asks for all nondegenerate periods.

## 6. Checks, attribution and limits

The exact verifier checks rational focal polar coordinates, the dual-circle equation, positive tangent-side orientation, and the cosine sign relation on many local configurations. These are controls on the elementary reduction; they do not replace the cited all-N bicentric theorem or assert that arbitrary sampled chords close into a billiard orbit.

The campaign's earlier k603 focal-antipedal distance and k405 antipedal-centroid packages concern different quantities. Their source restoration of the nested-confocal-ellipse setting is consistent with the present audit, but their proofs are not dependencies. The current k107, k108 and k114 investigations likewise do not establish k120. The proof here depends on the published bicentric invariant and the explicit polar-angle bridge only. Polar lines are not antipedal lines: their defining constants here are 1, rather than |p_i|^2.

The source requires constancy, not a requested elementary formula for the constant. This package does not claim a new explicit value, a new proof of the published bicentric theorem, or historical priority for this corollary. The intended original invariant is a known-theorem consequence; the broader hyperbolic-caustic wording sometimes inferred from the dataset has not been substituted for the original source.
