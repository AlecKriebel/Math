# Independent exact falsification of phase constancy

Analysis freeze UTC: 2026-10-04T23:05:30.687640+00:00

No candidate content or inherited review/results read before this analysis.

Let d=sqrt(13), c=sqrt(3), a=2,b=1, A=2(d−1)/3, B=(4−d)/3. Then A²−B²=3 and A,B>0, so C:x²/A²+y²/B²=1 is a genuine confocal elliptic caustic. Consider the positively oriented triangles

    T_x=((2,0), (−A,Y), (−A,−Y)),   Y²=1−A²/4,
    T_y=((0,1), (−X,−B), (X,−B)),   X²=4(1−B²).

Both have all vertices on the outer ellipse. Their three sides are tangent to C and obey the ellipse billiard reflection law, as verified by the following exact algebra. Write the generic horizontally symmetric triangle ((r,0),(−H,V),(−H,−V)) in an ellipse with axes r,s, V²=s²(1−H²/r²). If its caustic has axes H,K in these rotated coordinates, the vertical side x=−H is tangent, while each other side has equation ±Vx+(r+H)y=rV. Tangency is precisely

    r² V² = H² V² + K²(r+H)².                       (T)

At (−H,V), the two unit vectors toward its neighbors sum to ((r+H)/sqrt(D),−V/sqrt(D)−1), D=(r+H)²+V². This vector is parallel to the inward normal (H/r²,−V/s²) exactly when

    sqrt(D)=V [r²(r+H)/(H s²)−1].                   (R)

The quantities on both sides are positive. Squaring gives a rational expression in d, so no ambiguous squaring branch occurs. Substitute (r,s,H,K)=(2,1,A,B) for T_x or (1,2,B,A) in coordinates rotated by 90 degrees for T_y. In both substitutions (T) and the square of (R) reduce to zero using d²=13. The base vertices are symmetric, and the endpoint reflection law follows directly from symmetry. Thus these are legitimate three-periodic trajectories with the same outer ellipse and same elliptic caustic. Poncelet's porism identifies them as members of the same moving triangle family.

For T_x, focus f_s=(sc,0), s=±1. Its pedal feet to the upper side, vertical side and lower side are respectively (U_s,Z_s),(−A,0),(U_s,−Z_s), where

    D=(2+A)²+Y²,
    U_s=[sc(2+A)²+2Y²]/D,
    Z_s=Y(2+A)(2−sc)/D.

The signed shoelace area is Z_s(A+U_s). Hence the ratio from +c focus to −c focus is

    R_x = (2−c)/(2+c) · (t+c)/(t−c),
    t = (3A+2)/4 = d/2,
    R_x = (2−sqrt3)/(2+sqrt3) · (sqrt13+2sqrt3)/(sqrt13−2sqrt3).

This is strictly greater than 1: t>c because t²−c²=1/4, while 2>t; subtracting the two cross-multiplied numerator products gives 2c(2−t)>0. Both focus-pedal areas are positive and nonzero because Z_s>0 and A+U_s>0. For T_y, reflection across the y-axis swaps f_+ and f_− and reverses the cyclic vertex order, so the two signed pedal areas are equal and nonzero. Therefore R_y=1. The same family has R_x≠R_y: claim C (phase constancy) is false in a fully nondegenerate literal-source N=3 case.

Direct 85-digit Decimal controls independently checked both ellipse equations, billiard-normal bisectors, and tangency to the identical caustic, with maximum residual below 5e−84. They give R_x=3.5884019759959343412457523971432027957001184581565… and R_y=1. These finite-precision controls are empirical checks of the exact derivation, not its logical premise. Both phases also satisfy the displayed orbit-versus-outer ratio equality numerically to better than 1e−81. This does not prove E universally.

## Frozen independent conclusion

The source's literal displayed equality E and global invariant claim C are mathematically different. C fails. A valid proof of E can settle the displayed identity while necessarily correcting the source's implication that the ratio value itself is invariant. Calling that proof a complete proof of phase constancy would be incorrect. A candidate that acknowledges this distinction is not silently weakening the equality; its corrected statement must not be advertised as verifying the source's false constancy layer.

## Remaining independent controls before promotion

- Confirm candidate proves E for every permitted elliptic-caustic family and signed areas, including cyclic order and nonzero-ratio assumptions.
- Compare candidate's correction with this exact N=3 witness, not with an earlier verdict.
- Distinguish hyperbolic-caustic and circular-limit extensions from original ellipse-pair scope.
- Test all-zero pedal area examples and formulate cross-multiplied extension separately if candidate claims ratios exist everywhere.

Completion estimate: 45% of this source-fidelity audit. Candidate documents may be read after this file and its seal have been written.
