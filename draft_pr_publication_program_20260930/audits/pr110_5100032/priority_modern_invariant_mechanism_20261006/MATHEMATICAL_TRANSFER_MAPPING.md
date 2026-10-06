# Exact observable mapping for the closest modern prior

This is an audit of a proposed transfer from earlier inverse-perimeter theorems, not a new central proof search. It assumes the root's pinned k603 definition and mathematical gate. All distances below are ordinary positive Euclidean distances; there is no signed replacement.

Translate the chosen focus to the origin. For consecutive noncollinear nonzero vertex vectors u,v, put r=|u|, s=|v|, ell=|v-u| and h=distance(0,line(u,v)). Unit inversion sends u to U=u/r² and v to V=v/s².

The antipedal line at u is x·u=r². Equivalently it is x·U=1. The antipedal intersection Q therefore satisfies Q·U=Q·V=1. Consequently the antipedal polygon of the original vertex polygon is the unit-polar polygon of its focus-inverse vertex polygon. Its ordinary radial distance is the reciprocal of the inverse sideline's distance to the focus.

Expansion of |V-U|² gives ell²/(r²s²). Also det(U,V)=det(u,v)/(r²s²). The squared sideline distance is det(u,v)²/ell²; it follows that

    inverse_edge_length = ell/(rs)
    inverse_sideline_height = h/(rs)
    antipedal_radial_distance = rs/h = 1/inverse_sideline_height.

Roitman–Garcia–Reznik's Corollary1 proves constancy of the sum of inverse edge lengths. Its Theorem2 proves perimeter constancy for limiting-point pedal polygons of the corresponding bicentric family. Figure4 explicitly has an antipedal arrow from the inverse polygon to the bicentric family. Neither that arrow nor the perimeter theorem supplies the sum of reciprocal inverse sideline heights required here. Applying the antipedal operation to the original polygon and to its inverse uses different input polygons.

The focus-inverse perimeter sum also is not the sum of inverse vertex radii studied in the low-period inverse-triangle paper. Those radii are 1/r; the target terms involve two consecutive vertex radii and their sideline height, rs/h.

## Exact local negative control

At a=5,b=3, focus f=(4,0), caustic parameter lambda=19/4, consider two tangent chords of the same strictly nested confocal pair.

The vertical chord has x=9/2 and endpoints y=±3sqrt(19)/10. Here rs=49/25, h=1/2, ell²=171/25, so Q's radial norm squared is 9604/625 and the inverse edge squared is 4275/2401.

The horizontal chord has y=sqrt(17)/2 and endpoints x=±5sqrt(19)/6. Here rs=149/9, h²=17/4, ell²=475/9, so Q's radial norm squared is 88804/1377 and the inverse edge squared is 4275/22201.

The quotient of these two squared metrics is different on the two chords. Thus a fixed-pair constant per-edge scaling cannot turn the earlier inverse-perimeter statement into the target ordinary radial-sum statement. This control is deliberately local: it does not assume this selected parameter closes, does not disprove a possible nonlocal relation on closed polygons, and does not establish novelty by itself.

The checker independently solves both antipedal supporting-line equations for seven rational pairs, verifies the inverse-polar equations and both metric transformations, and evaluates the same-caustic controls by exact fractions. It uses explicit exception checks, not removable assertions. Normal and Python-O executions are preserved with actual PID/UTC/process outputs; both perform49 checks. See TRANSFER_NORMAL.json and TRANSFER_OPTIMIZED.json.

## Other mechanism transfer limits

The Bialy–Tabachnikov support/generating-function identities supply length-action relations and the known product h_plus*h_minus=b²−lambda. A finite closed-cycle coboundary sums to zero. Identifying the specific ordinary norm difference q_plus−q_minus with a constant multiple of a coordinate increment is the additional observable-specific step verified in the original proof. The general telescoping principle alone is not a previously stated k603 theorem.

Complexifying a Poncelet family gives an elliptic curve, but a generic meromorphic function can have poles. Akopyan–Schwartz–Tabachnikov and the bicentric paper cancel poles for their particular expressions; they do not give blanket constancy of every norm sum. Schwartz's monodromy theorem likewise names particular projective cross-ratio polynomials. A metric identification for the present focal antipedal norm is still necessary.

Harmonic-polygon polarity uses homothetic ellipse pairs. For a noncircular outer ellipse a>b and a homothety factor0<t<1, the inner focal separation squared is t²(a²−b²), which differs from a²−b². The strictly nested noncircular pair cannot simultaneously be homothetic and confocal. The published harmonic family cannot simply replace the confocal billiard family in k603.

Finally, positive radial sums cannot be replaced by signed areas, squared norms, or signed hyperbolic-billiard perimeter identities. Equality of squared-norm sums generally does not imply equality of ordinary-norm sums; for example positive radius lists (1,3) and (sqrt(5),sqrt(5)) have equal square sums and unequal sums. Such distinctions are checked before classifying any prior as covering.
