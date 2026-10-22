# Independent direct geometry: verified lemmas and exact gap

Author/family: independent physical/geometry family 01. Frozen plan: research_log.md, 2026-10-16 15:54:41 UTC. No submitted PR205 proof, checker, review, or other family report has been opened. This note supplies partial exact geometry and physical numerical reproduction, not a universal proof of k601.

## Complete-line focal distance lemma

Let a caustic tangent be n·X=h, with ||n||=1 and h>0. Its support equation is

    h² = alpha² n_x² + beta² n_y².

Since c²=alpha²-beta²,

    h²-c²n_x² = beta² > 0.

Both foci are strictly on the inner side of the line, and their ordinary perpendicular distances to the complete line are therefore

    q+ = h-c n_x,   q− = h+c n_x,
    q+ q− = beta².

This conclusion is valid for every caustic tangent, without periodicity, winding, a billiard reflection assumption, or use of a segment endpoint. It also implies

    I = beta² (sum_i t_i)(sum_i 1/t_i),  t_i=q+,i/beta > 0.

The local product identity alone does not make I constant: the positive triples t=(1,1,1) and t=(2,1,1) give I/beta² equal to 9 and 10. These arbitrary triples are not claimed to be billiard orbits. They demonstrate why a proof must still exploit the full outer-ellipse/reflection/closure constraints.

## Optical reflection identity

At an outer-ellipse vertex P, write d±=|P-F±| and e±=(P-F±)/d±. The normal bisects e+ and e−, so reflection R across the tangent sends e+ to -e−. Specular reflection sends incoming unit direction v_in to outgoing direction v_out. Orthogonal reflection preserves absolute cross products. Consequently

    |cross(v_in,e+)| = |cross(v_out,e−)|,
    q+,i−1/d+,i = q−,i/d−,i,
    q+,i−1 q+,i = beta² d+,i/d−,i.

This is exact local geometry. The checker independently recomputes it from propagated vertices. It gives a cyclic multiplicative relation, but does not by itself establish the target product of SUMS. Solving an odd cyclic system of multiplicative relations merely replaces the target by an equivalent vertex-distance sum identity. Without a new identity proving that final expression constant, this direct local-elimination route is blocked. It must not be promoted as a proof.

## Exact three-period calibration

An isosceles triangle has vertices P0=(a,0), P1=(-alpha,y), P2=(-alpha,-y), with y=b sqrt(a²-alpha²)/a. The vertical side is tangent to the caustic. Tangency of P0P1 gives

    (a²-b²) alpha² + 2 a b² alpha - a⁴ = 0.

The positive solution is alpha=a(delta-b²)/(a²-b²), with delta=sqrt(a⁴-a²b²+b⁴); beta=b(a²-delta)/(a²-b²). These formulas are derived here by tangency, not imported as a closing configuration. The two oblique sides have distances q±=beta(a∓c)/b, while the vertical side has q+=alpha+c and q−=alpha-c. Thus

    S+ = alpha+c+2 beta(a-c)/b,
    S− = alpha-c+2 beta(a+c)/b.

For a=sqrt(2), b=1, c=1, alpha=sqrt(2)(sqrt(3)-1), beta=2-sqrt(3),

    I = [sqrt(2)(3-sqrt(3))]² - [2sqrt(3)-3]² = 3.

The triangle is a valid billiard because its adjacent sides are the two caustic tangents through each outer-ellipse vertex; their angle bisectors coincide with the confocal-coordinate normal/tangent directions. The physical checker separately verifies specular reflection, tangency, closure, and I=3. This verifies one exact orbit and validates conventions; it is not a proof of invariance over the three-period family.

## Exact even-period calibration and parity distinction

For the four-vertex diamond (a,0),(0,b),(-a,0),(0,-b), take

    lambda = a²b²/(a²+b²),
    alpha = a²/sqrt(a²+b²), beta=b²/sqrt(a²+b²).

Every side has positive support h=ab/sqrt(a²+b²). Opposite normals cancel in each focal sum, yielding

    I = 16 a²b²/(a²+b²).

The exact diamond value is checked numerically at a=2,b=1, giving 12.8. Physically propagated other phases in the SAME four-period family show a substantial variation of I. Thus an even-period extension of the odd target is false, and the physical procedure does distinguish parity.

## Reversal, repetition, and physical scaling

Reversal permutes original support lines, so it preserves both sums exactly. Traversing any closed orbit r times repeats every line r times, so S± becomes r S± and I becomes r² I. This counting argument holds for all positive integer r; testing odd r=3,5 is calibration rather than a new universal difficulty. Scaling every axis and coordinate by k>0 multiplies each q by k and I by k². The checker tests k=10^-20 and 10^20.

## Strongest exact result and remaining universal gap

The exact independently established results are the complete-line local product, the optical adjacent-distance relation, the exact triangle and diamond calibrations, and reversal/repetition/scaling rules. The missing result is a proof that the target product of sums is independent of starting phase for EVERY proper confocal pair supporting an odd primitive orbit, for all admissible coprime winding classes. High-precision noninterval propagation cannot fill this gap.

Primary-source semantic exposure only: Reznik–Garcia–Koiller, *Fifty New Invariants of N-Periodics in the Elliptic Billiard*, published Table 7 p349, k601 and §3.7: https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf . The source was opened after plan freeze to confirm that q denotes distance to original supporting sides. No published elliptic parametrization or closing formula was used in physical root shooting.
