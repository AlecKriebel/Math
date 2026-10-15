# Independent adversarial review of the printed k107 assertion

**Verdict: PASS_COMPLETE_LITERAL_COUNTEREXAMPLE.** No mandatory mathematical correction. The frozen package gives two genuine primitive four-period billiard orbits in one fixed confocal-ellipse Poncelet family with different values of the exact product printed as k107. Recommended status: **claimed_solved, 2/5 approaches**, specifically by counterexample to the literal source.

Reviewed 2026-09-30 by a separate GPT-6 Astra agent at xhigh reasoning. This is an independent AI audit, not human peer review or a novelty certificate.

## 1. Frozen artifacts and source statement

The reviewed `COUNTEREXAMPLE.md` has SHA-256
`d34e4347358f54b20c9cea7d974e2c6a2308a5e69c7abf46de16132d83f9edbd`.
The submitted verifier and receipt hashes are respectively
`005647d99a679fd48556aec8951f237e32b7fbd90374212dff1233d2a564d671` and
`039acbc4f04ce42c5e9f1f983fbc9c4817edbb7829d5a00673a3d1caa9396692`.

I checked the full definitions and the rendered Table 2 in both [arXiv:2004.12497v11, p.5](https://arxiv.org/abs/2004.12497v11) and [the published companion, p.345](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf). Both print k107 as **k103*k105**, with N divisible by four. The component expressions are A'/A and the product of the original orbit's half-angle sines. P' is the polygon of intersections of consecutive tangent lines to the outer ellipse at the orbit vertices. The area convention is signed.

The target is therefore genuinely the product, rather than a quotient inferred from another table row. The counterexample uses convex counterclockwise polygons, so signed areas and ordinary positive areas agree. There is no angle, area-sign, parity or repeated-period convention that rescues the printed expression for these examples.

## 2. Direct verification of the two orbits

For a>b>0, let s=sqrt(a^2+b^2) and lambda=a^2*b^2/s^2. The proposed caustic has squared semiaxes a^4/s^2 and b^4/s^2. Their differences from the outer squared semiaxes both equal lambda, and 0<lambda<b^2. Thus the caustic is nondegenerate, strictly nested and confocal.

The axis diamond has vertices (a,0),(0,b),(-a,0),(0,-b). Each vertex lies on the ellipse. Its first side has equation x/a+y/b=1. The caustic support-square in that normal direction is a^2/s^2+b^2/s^2=1. The tangency point (a^3/s^2,b^3/s^2) has strictly positive barycentric weights a^2/s^2 and b^2/s^2 on that side. Axis reflections handle all sides. At the vertices the normal axes bisect the two incident rays, verifying the physical reflection law directly.

The second polygon has coordinates (±a^2/s,±b^2/s) in rectangular order. Substitution verifies the outer ellipse equation. Its horizontal and vertical sides are precisely axis tangents of the same caustic, with contact points in their interiors. The outer normal at a vertex is proportional to (±1,±1), so it bisects the right angle between the incident rays. This is again a genuine billiard orbit. Both polygons have four distinct successive vertices, and therefore primitive period four.

## 3. Continuous same-family claim

Let v=(c,d) lie on the unit circle, and let L be the linear map

    L(c,d)=(-a^2*d,b^2*c).

Its determinant is positive and L^2=-a^2*b^2*Id. Radial normalization gives the submitted map T(v)=L(v)/|L(v)|. Therefore T is a continuous orientation-preserving circle map and T^2=-Id. Its denominator Delta=sqrt(a^4*d^2+b^4*c^2) is bounded below by b^2>0.

In the ellipse coordinates, P=(a*c,b*d) and Q=(-a^3*d/Delta,b^3*c/Delta). Their determinant is

    det(P,Q)=a*b*(a^2*d^2+b^2*c^2)/Delta>0.

Hence (P,Q,-P,-Q) is always a nondegenerate convex counterclockwise parallelogram with four distinct vertices. The submitted support-square calculation for the line PQ is correct after using c^2+d^2=1 and Delta^2+a^2*b^2=(a^2+b^2)(a^2*d^2+b^2*c^2). It makes every such side tangent to the same caustic. The contact is automatically in the chord interior: the whole caustic lies strictly inside the outer ellipse, and its contact point lies on the chord's line.

The general reflection implication was also checked independently. For a point P=(x,y) on the outer ellipse and a unit vector v, the identity

    a^2*b^2*(x*v_x/a^2+y*v_y/b^2)^2
      =a^2*v_y^2+b^2*v_x^2-(P cross v)^2

turns the confocal tangency condition into equation (6). The two distinct inward chord directions have negative projection on the outward normal and equal absolute projection. Their tangential projections have opposite signs; they are normal reflections of one another. Reversing the incoming inward ray gives the usual reflection of velocity across the tangent line. Thus the full continuous family consists of actual billiard trajectories, rather than just inscribed quadrilaterals.

At (c,d)=(1,0) it is the diamond. At (c,d)=(a/s,b/s), Delta=ab and it is exactly the stated rectangle, in the stated order. This supplies an explicit continuous connection within a single oriented family. No appeal to a numerically matched caustic is needed.

## 4. Areas, half angles and nonzero denominators

For the diamond, the orbit area is 2ab and the outer tangent polygon is the rectangle with area 4ab. The half-angle sines alternate b/s,a/s,b/s,a/s. Hence

    k107(D)=2a^2*b^2/(a^2+b^2)^2.

For the rectangle, the orbit area is 4a^2*b^2/s^2 and the outer tangent lines are ±x±y=s. Their consecutive intersections form the axis diamond of area 2s^2. All four half-angle sines are 1/sqrt(2), so

    k107(R)=(a^2+b^2)^2/(8a^2*b^2).

The inequality (a^2+b^2)^2>4a^2*b^2 gives k107(D)<1/2<k107(R) for every a>b. At a=4,b=3 the values are 288/625 and 625/1152, with positive difference 58849/720000. The caustic semiaxes are 16/5 and 9/5, exactly as claimed. Both perimeters equal 20 and both Joachimsthal constants equal 1/5.

There are no hidden tangent-polygon singularities along the connecting family. The determinant of two consecutive outer-ellipse normals is det(P,Q)/(a^2*b^2)>0. The four tangent lines are the inverse linear image of the four sides of a square. Their area is 4a^2*b^2/det(P,Q), while the orbit area is 2det(P,Q). Both are strictly positive and finite. Their product is 8a^2*b^2, consistent with the cited even-period area-product theorem.

## 5. Prior results and exact claim boundary

I checked [Chavez-Caliz, Theorem 6](https://armj.math.stonybrook.edu/pdf-Springer-final/020-0154.pdf) and [Akopyan–Schwartz–Tabachnikov, Corollary 6.4](https://par.nsf.gov/servlets/purl/10408491) in their full primary texts. The former concerns the area product for even periods; the latter's half-angle product invariance has an odd-period hypothesis. Neither asserts constancy of the product under review at period four. The counterexample is independently elementary and does not depend on either theorem.

The equality of the quotient k103/k105 at the two displayed representatives is a useful table diagnostic, but it is not a proof of a corrected all-period theorem. The submitted package correctly refrains from that claim. The neighboring k108 problem and earlier focal-antipedal k603/k405 packages are different targets and were not used as verification evidence here.

## 6. Reproducibility

The submitted standard-library verifier passes all **10,073 assertions** and reproduces its receipt byte for byte. Its 228 family samples include exact quadratic-field arithmetic, contact locations and normalized reflection checks.

The separate `independent_checks.py` uses direct rational line intersections, shoelace areas, and square-root-free half-angle-product recovery for **66 Pythagorean-axis pairs**, testing both complete orbits in each ellipse. It additionally performs symbolic polynomial reductions for the all-parameter continuous-family identities, including T^2=-Id, tangency, exact side lengths, normalized reflection and the normal-projection identity. **All 8,397 independent assertions pass.** The checker uses SymPy for the symbolic reductions; no numerical orbit fitting is involved.

The exact finite controls supplement the explicit proof. The full literal assertion is refuted by the two rational four-orbits alone, with continuous family membership justified analytically. Preserve the source-product wording, two-approach count, unconfirmed historical priority and absence of a corrected-invariant claim when publishing.
