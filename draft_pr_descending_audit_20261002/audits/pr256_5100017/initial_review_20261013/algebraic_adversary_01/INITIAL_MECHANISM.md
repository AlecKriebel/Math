# Independent algebraic adversary mechanism

Timestamp: 2026-10-13 (UTC; exact checkpoint time to be recorded by verifier).
Completion estimate: 0% of assigned mathematical audit.

This note precedes reading the submitted proof or prior independent reviews.

I will express an outward tangent line as n dot x = h with |n|=1 and encode n by z on the unit circle. For a fixed M encoded by m, the projection is q=m+(h-Re(m conjugate(z)))z = (m-z^2 conjugate(m))/2+h z. Signed area comes from Im(conjugate(q_i)q_{i+1})/2, while signed first moment comes from the usual (q_i+q_{i+1}) times that cross product /6. For antipodal pairs z -> -z, h remains positive and unchanged: the projection splits into an even quadratic-normal contribution and an odd support-normal contribution. Pair sums will isolate area terms quadratic in M and centroid numerator terms linear/cubic in M. I will independently derive these pair contributions, then test whether billiard/caustic constraints make their aggregate phase invariant.

Proposed falsifiers: wrong antipodal edge bookkeeping; a missed cubic term in centroid numerator; reversed normal-angle branch causing a sign error; support-function scaling error; missing dependence on phase in one purported telescope; division by zero on an unreported locus; N=4 d=0 not accounted for; signed moment failing on stars; central inversion commuting with the map but not equal to the half-period on a primitive even orbit; endpoint or winding argument silently requiring simple polygons.

Exact controls: symbolic adjacent-normal identities; raw shoelace and raw moment for a noncircular even orbit; an exact zero-area locus point; N=4; nonzero rotation stars; orientation reversal; scaled ellipses. Proof failures will be logged and communicated without editing submitted sources.
