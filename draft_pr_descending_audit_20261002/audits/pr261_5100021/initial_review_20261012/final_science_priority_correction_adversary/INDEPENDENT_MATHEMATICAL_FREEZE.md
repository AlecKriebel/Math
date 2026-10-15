# Independent mathematical freeze

Recorded 2026-10-12T10:40:17.065575+00:00, after reading only submitted TARGET.json and PROOF.md and writing/running my own controls. Root and prior-review verdicts not yet read. Best-guess review completion: 35% (mathematical reconstruction done; priority and candidate audit outstanding).

## Exact domain provisionally accepted
A noncircular real ellipse, strict nested nondegenerate confocal elliptical caustic, primitive real orbit of least period N divisible by 4, and any primitive winding tau with 0<tau<N/2. Either original focus; actual feet from that focus to original chord lines and actual intersections of consecutive perpendicular-at-original-vertex lines; ordered signed shoelace areas. Reversal permitted, unsigned lobe area and hyperbolic/degenerate caustics excluded. The focal area factors need not be nonzero: A_F>0 for positive traversal; B may be zero and product theorem uses no division. This corrects the draft plan's preliminary nonzero-factors wording. Repeated traversals do not change the least-period target; their areas scale with traversal multiplicity and cannot be used to manufacture qualifying parity.

## Independent deductions
Normalize caustic semiaxes to (1,k'), so a=d/c,b=k'/c with v in (0,K). Then a^2-b^2=k^2; a>1,b>k'; focus k is interior to the caustic. N=2m, m even, primitive tau odd ensures shift m delta=2K tau and area period gcd(2K,delta)=h=2K/m. Stachel's parametrization still requires later primary-source check; the deductions thereafter are internally valid.

My independent symbolic control clears denominators of both original line incidences and of the claimed determinant, reducing modulo C^2=1-S^2,D^2=1-k^2 S^2,c^2=1-s^2,d^2=1-k^2s^2,k'^2=1-k^2. All remainders are zero. The pedal projection formula also independently reduces to zero. On the real domain the determinant has positive nonzero factors, so all antipedal intersections are finite.

Pole completeness: sn^2 on (2K,2iK') has one double pole and degree two. L=1-k^2s^2 sn^2 has exactly two simple zeros, at iK' +/- v, because sn=+/-1/(ks) gives nonzero cn,dn. Common sn,cn poles cancel in each R component (order at most two upstairs/downstairs), so there are no additional poles. R has order at most one; area has order at most two. Real h-periodicity puts all possible B poles on the two reduced rows iK',3iK'. Central inversion gives equal focal areas; reflection plus reversed index order gives B(-w)=B(w); imaginary 2iK' shift reflects across x-axis and gives anti-periodicity. Therefore B(iK'+z)=-B(iK'-z), eliminating even Laurent powers and all double coefficients. This explicitly works for N=4 even when every R is simultaneously singular; no separated-index assumption is needed.

T=sum dn(w+jdelta) has two simple reduced-torus poles: at iK', j=0,m have equal residues and add, and no other j has that same real class before quotient. Anti-periodicity reverses the second-row residue. Matching B's residue to T leaves a holomorphic torus function; anti-periodicity makes the residual constant zero, including the possibility B=0.

Pedal q has a possible double pole only where sn=1/k; common Jacobi poles cancel. At r=K+iK', both sn(r+z) and cn(r+z) are even, so q(r+z) is even. The adjacent q values remain regular (0<delta<2K) and their difference is odd; paired incident area edges have only a simple pole. This proves pedal area is p_F T(w+K+v), without divisions by area. Since K+v=(m+tau)h/2 and m+tau odd, this is p_F T(w+h/2).

Evenness and anti-periodicity force T to vanish at h/2+iK' and h/2+3iK'. Exactly two poles imply exactly two zero multiplicities on the compact torus, so both zeros are simple and T(w)T(w+h/2) has no poles. It is constant and positive on the real locus. This completes all-period analytic invariance on the exact domain.

Signed positivity follows because q-F is a positive outward-normal multiple and its consecutive normal-angle increment is strictly between 0 and pi for every admissible star step delta<2K. Reversal negates both areas. The claim does not assert antipedal positivity or nonzero area; circular limits and degenerate caustics are excluded. Nothing here establishes a novel first resolution.

## Independent computational corroboration
Own independent_controls.py imports no existing checker. Its direct endpoint-line Cramer construction and side projections test 36 (N,tau,k) cases, 4 phases each, N=4,8,12,20, including stars and k=.05,.4,.85,.99. Product and both trace proportionalities vary only at about 3.3e-69 or lower; focal areas agree. These are diagnostics, not the proof. N=4 traversed twice gives double areas and quadruple product, illustrating repeated-traversal scaling. Three-period products differ across phases, verifying that I did not silently generalize to all N.

## Challenges requiring later review
The source's short row is ambiguous on signed versus geometric area and primitive versus repeated traversal; accepted theorem must state those assumptions. Primary-source parametrization and classical alternative resolution still need source checks. Candidate status, credit and archive clocks are untouched at this freeze.
