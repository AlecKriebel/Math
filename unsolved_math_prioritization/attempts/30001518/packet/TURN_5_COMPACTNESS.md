# Turn 5: attempting to pass to a perfect limiting body

The fifth substantive approach tried to obtain existence from a limit of asymptotically perfect shapes. A conditional scattering-continuity lemma is available, but the required geometric stability is not supplied by compactness. An explicit ordinary polygonal counterexample shows why Hausdorff convergence alone is insufficient.

## Stable finite itineraries

Fix a ray with a finite billiard itinerary in a limiting body B. Suppose each collision is at a regular C² boundary arc and transverse; the intervening segments have no other contacts; the incoming and outgoing half-rays have no other contacts; and corresponding boundary graphs of B_n converge locally in C¹ to those of B. Also require strict clearance from all other boundary pieces away from the collision neighborhoods, uniformly for large n, including the incoming and outgoing portions in a common bounded enclosing region. Outside that region all bodies are absent.

Under these hypotheses the corresponding B_n trajectories have the same finite itinerary for all sufficiently large n, their collision points converge, and their final velocities converge to that for B. Proof: the first transverse line/graph intersection persists and converges by the implicit-function theorem (or its elementary monotone-intersection form); C¹ convergence gives convergence of the normal and reflected direction. Induct over the fixed finite number of collisions. The strict-clearance assumptions exclude unwanted earlier collisions and further collisions on exit. ∎

If these hypotheses hold for almost every ray in one fixed incident probability space, then dominated convergence applies to the bounded scattering integrand (1−v·w_n)/2. Thus r(B_n)→r(B). In that particularly stable setting, r(B_n)→1 would prove B perfect. A common phase space and normalization must be specified; this statement does not compare arbitrarily changing incident measures without identification.

## An explicit Hausdorff counterexample

Let B=[0,1]×[−1,0]. For every positive integer n define the continuous triangular-wave function

    g_n(x)=−min({nx},1−{nx})/n,  0≤x≤1,
    B_n={(x,y):0≤x≤1, −1≤y≤g_n(x)}.

Here {nx} denotes fractional part, and at cell endpoints g_n=0. Each B_n is a connected finite simple polygonal body. The Hausdorff distance d_H(B_n,B) is at most 1/(2n), and tends to zero.

Consider the incoming ray at (x,0) with velocity (a,−1), where 0<a<1. Unit-speed normalization divides all velocities below by sqrt(1+a²) and does not alter any itinerary. Let r={nx} be its entrance coordinate in its width-1/n notch. Scaling the cell reduces it to the triangle with vertices (0,0),(1,0),(1/2,−1/2), whose two reflecting sides have slopes −1 and +1.

Away from the finitely many singular entrance coordinates for this n and a, the ray makes:

* Two reflections if 0<r<1−a. Its outgoing velocity is (−a,1), and its exit coordinate within the cell is 1−a−r.
* One reflection if 1−a<r<1. Its outgoing velocity is (−1,a), and its exit coordinate is (r+a−1)/a.

For completeness, the switch between which side is hit first is r=(1−a)/2. If r<(1−a)/2, the first hit is on y=−x at abscissa r/(1−a), with reflected velocity (1,−a); the second hit is on y=x−1 and produces (−a,1). If r>(1−a)/2, the first hit is on y=x−1 at abscissa (r+a)/(1+a), with reflected velocity (−1,a). It exits before the left side precisely when r>1−a; otherwise the second reflection gives (−a,1). The displayed exit coordinates follow by solving y=0. Each exit lies in the same cell and points upward, so the ray then escapes all of B_n.

For the limiting flat body B, the outgoing velocity is (a,1). Both possible outgoing velocities for B_n have negative horizontal component and differ from this limit. On any closed angular band 0<a₀≤a≤a₁<1 the normalized horizontal components are separated from that of the flat body by a positive constant. Therefore the scattering maps do not even converge in measure to the scattering map of B on the common top-aperture phase strip, despite Hausdorff convergence of the bodies. Excluding the countable union of singular entrance sets leaves a full-measure set; no simulation is involved in this conclusion.

The exact retroreflected fraction at a fixed a is 1−a under uniform entrance position. In particular this example is not asserted to be asymptotically perfect. Its purpose is to refute the proposed Hausdorff-continuity step by a genuine ordinary billiard construction.

## Remaining gap and stopping point

No compactness class containing a known asymptotically perfect family has been established here in which the required almost-everywhere regular itinerary stability survives. A limit may lose admissible boundary regularity or the scattering map may be discontinuous under geometric convergence. The conditional lemma cannot be applied to the cited constructions without proving those missing hypotheses. Five substantive approaches have now been made; the full bounded-body existence problem remains unresolved by this packet.
