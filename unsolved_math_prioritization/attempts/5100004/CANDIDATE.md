# k110 follows from the published even-Poncelet area-product theorem

**5100004 / AMR-050-0004. Complete credited consequence, author turn 1. Independent review pending.**

## 1. Exact claim and conventions

Let

    E: x²/a² + y²/b² = 1,          a > b > 0,
    C: x²/alpha² + y²/beta² = 1,  alpha² = a² − lambda,
                                  beta² = b² − lambda,
                                  0 < lambda < b².

Fix a Poncelet billiard family between E and C with even least period N. In traversal order let P=(P_i), let T_i be the intersection of the tangents to E at P_i and P_(i+1), and let S_i be the contact of the side P_i P_(i+1) with C. Thus T is the outer polygon P' and S is the contact polygon P'', up to a harmless cyclic indexing shift. Areas here mean the signed shoelace areas

    area(W) = (1/2) sum_i det(W_i,W_(i+1)).                 (1)

Then

    A A'' = (alpha² beta² / (a² b²)) A A'                 (2)

is constant as P varies. This includes simple and star polygons in the source's nondegenerate confocal-ellipse setting. No unsigned union-of-lobes area is substituted for (1).

The source is Reznik–Garcia–Koiller, *Eighty New Invariants of N-Periodics in the Elliptic Billiard*, arXiv:2004.12497v11, Table 2, k110, printed p.5. The published companion, *Fifty New Invariants*, Arnold Mathematical Journal 7 (2021), 341–355, Table 2 on p.345, has the same k110 assertion. Its Sections 1–2 specify the confocal ellipse pair and signed areas. The imported statement omits these conventions; we restore them rather than extend to hyperbolic or degenerate caustics.

Here “N-periodic polygon” uses primitive period. Traversing an odd-period orbit twice does not make the underlying polygon primitive even. A repeated traversal of an even primitive orbit also has constant product, since both areas multiply by the repetition count. We make no inference for repeated odd primitive orbits. N=2 is impossible with a strictly interior nondegenerate elliptical caustic: a two-bounce billiard chord is a diameter through the center, and cannot be tangent to C. Angle conventions in the source (theta_i at P_i, theta'_i at T_i) do not enter this proof.

## 2. Fixed linear map between the derived polygons

Put

    B = diag(a^(-2), b^(-2)),   D = diag(alpha^(-2), beta^(-2)).

The tangents defining T_i are

    P_i^t B T_i = 1,   P_(i+1)^t B T_i = 1.

They meet at a finite point: distinct points of a centered ellipse have parallel tangent lines only when antipodal, whereas an antipodal chord through the center cannot be tangent to the strictly nested C. Consecutive vertices are distinct for a nondegenerate billiard orbit.

Since B is symmetric, the line

    x^t B T_i = 1                                             (3)

contains both endpoints P_i and P_(i+1); it is precisely the side line. The tangent to C at S_i is

    x^t D S_i = 1.                                            (4)

Equations (3) and (4) define the same affine line. Their nonzero constant terms have both been normalized to 1, so their coefficient vectors are equal:

    D S_i = B T_i,
    S_i = D^(-1) B T_i
        = diag(alpha²/a², beta²/b²) T_i.                       (5)

Thus the whole contact polygon is the image of the outer polygon under one fixed, orientation-preserving linear map. It is important that vertices remain in traversal order, rather than being re-sorted spatially. Applying (1) term by term gives

    A'' = det(D^(-1)B) A' = (alpha² beta² / a² b²) A'.          (6)

This argument has no parity requirement, no division by polygon area, and no convexity requirement for the polygon. It remains an identity if a signed area is zero. Only the two centered conics and the specified incidence/tangency constructions are used.

## 3. Published theorem and exact hypothesis check

Theorem 3 of Ana C. Chavez-Caliz, *More About Areas and Centers of Poncelet Polygons*, Arnold Mathematical Journal 7 (2021), 91–106, DOI 10.1007/s40598-020-00154-8, states that for two concentric ellipses in general position admitting a Poncelet n-gon family, the product of the area of the inscribed polygon and the area of its outer tangent polygon is constant when n is even. It is repeated as Theorem 6 and proved in Section 5, p.104. The paper uses algebraic area (equation (5), p.93), so simple and star traversals are covered. Its flag-curve proof uses the Poncelet translation of order n; this is the primitive-period interpretation used above. It does not require ordinary convex polygon area.

In this theorem “general position” means transverse intersection of the two complex projective conics (definition on p.94). That condition is not merely assumed here. Set c²=a²−b²>0. The common points of E and C have finite affine coordinates satisfying

    x² = a² alpha²/c²,   y² = −b² beta²/c².                    (7)

They are four distinct points over C, with both coordinates nonzero. There is no common point at infinity: the determinant of the two homogeneous equations in x²,y² is

    1/(a² beta²) − 1/(b² alpha²)
      = lambda c² / (a² b² alpha² beta²) > 0.                 (8)

At each common affine point the determinant of the gradients of the two conic equations is four times x y times the nonzero expression (8). Hence all four intersections are transverse. Strict nesting, concentricity, a Poncelet family, and even primitive period are already hypotheses of the claim. The theorem therefore applies to precisely the polygons P and T used in Section 2 and yields

    A(P) A(T) = K(E,C,N),                                    (9)

independent of the initial vertex. Multiplication of (9) by the fixed determinant in (6) proves (2), and settles the stated k110 constancy.

No numerical approximation, conjectural area identity, or private communication is required for this deduction. The complex flag-curve theorem is the published input, not a new theorem claimed here.

## 4. Attribution, source discrepancies, and limits

This is a classical consequence of Chavez-Caliz's published area-product theorem and elementary conic polarity. It should be credited as `already_solved`, with one substantive author turn, rather than described as a novel resolution of a long-open conjecture. The source's k110 row still has a question mark; that historical label is not evidence against the deduction.

The v11 table itself gives the area-ratio identity A'/A'' = (ab/(alpha beta))² as k113, credited to H. Stachel's private communication. Equation (5) supplies a complete public derivation of the needed identity, avoiding reliance on the inaccessible communication. The published companion changes the neighboring numbering and prints a product where the v11 ratio appears; it must not be silently quoted as though it printed the ratio. The k110 target is unchanged. See SOURCE_AUDIT.md.

A separate normalization check finds a factor-four discrepancy in the low-N formula printed in Garcia–Reznik's *Exploring self-intersected N-periodics in the elliptic billiard*, Proposition 4.9. Under the explicitly specified contact-polygon/shoelace conventions, the axis quadrilateral gives AA'' = 8a⁴b⁴/(a²+b²)², whereas that proposition prints coefficient 2. This does not affect constancy and is not an input to our proof. Exact coordinates and checks are in SOURCE_AUDIT.md and verify.py.

Hyperbolic caustics, degenerate caustics, and unsigned filled-region area are outside this source-corrected claim. A circular outer boundary is not required by the source (which assumes a>b); if desired it is a separate immediate case: fixed-step regular star polygons and all their derived polygons rotate rigidly. No practical computation of K is claimed or needed.

## References

- A. C. Chavez-Caliz, *More About Areas and Centers of Poncelet Polygons*, Arnold Math. J. 7 (2021), 91–106; online 14 August 2020. https://doi.org/10.1007/s40598-020-00154-8 . Complete publisher PDF: https://armj.math.stonybrook.edu/pdf-Springer-final/020-0154.pdf . Theorems 3 and 6; Sections 2 and 5.
- D. Reznik, R. Garcia, J. Koiller, *Eighty New Invariants of N-Periodics in the Elliptic Billiard*, arXiv:2004.12497v11. https://arxiv.org/pdf/2004.12497v11 . Sections 1–3; Table 2; bibliography.
- D. Reznik, R. Garcia, J. Koiller, *Fifty New Invariants of N-Periodics in the Elliptic Billiard*, Arnold Math. J. 7 (2021), 341–355. https://doi.org/10.1007/s40598-021-00174-y . Complete publisher PDF: https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf . Sections 1–3; Table 2.
- R. Garcia, D. Reznik, *Exploring self-intersected N-periodics in the elliptic billiard*, DOI 10.33039/ami.2022.02.001, accepted manuscript published online 22 February 2022. https://ami.uni-eszterhazy.hu/uploads/papers/finalpdf/AMI_online_1216.pdf . Proposition 4.9, p.10, for the normalization audit only.
