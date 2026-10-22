# WIP checkpoint: k804,a focal-inverse signed-area product

**5100044 / AMR-050-0044. Unreviewed mathematical work in progress. Author turn1 is active. No complete-result or novelty claim is being published at this checkpoint.**

## Exact source and gate

Pinned source_record.json and full prior_imported_report.json recover A*A_j^dagger for primitive N divisible by4, where only the ORIGINAL orbit vertices are inverted in a unit circle centered at an original ellipse focus. Areas are signed shoelace areas; the sides after inversion are the straight segments between inverted vertices, not the circular images of whole original sides. The source begins with nondegenerate nested confocal ellipses. Primitive stars are to be included; no hyperbolic/degenerate extension or parity by repeated traversal is assumed.

Edition defect: arXiv2004.12497v11 Table9 printedp11 has k804,a for this product, k804,b for its N4 value4, and k805 for a2mod4 ratio. The published Fifty New Invariants Table9 has k804 as an unrelated inverse-angle cosine sum and omits this area-product row. Follow the arXiv literal formula, not the published label. Later Garcia-Reznik Exploring self-intersected N-periodics uses k805,a for the corresponding area product; its precise general-proof status remains to be checked. No exact prior general-N resolution has been verified.

Live all-state PR searches5100044/k804, target branch search, and default-branch attempt-path commit history found no campaign attempt. No historical counter reset is intended.

## Turn1 mathematical reduction

Use Stachel's published canonical coordinates, with caustic semiaxes alpha,beta, k=c/alpha, k'=beta/alpha, K,K':

P(w)=(-a sn w,b cn w), a=alpha dn(v)/cn(v), b=beta/cn(v), delta=2v=4K tau/N.

Let h=sn(v), q=cn^2(v), t=h^2, U=1-2k^2t+k^2t^2, V=1-2t+k^2t^2, W=1-k^2t^2. Then U=dn(delta)W, V=cn(delta)W, U+V=2q dn^2(v), and U^2-k^2V^2=k'^2W^2>0.

For focus f=(c,0), its ordinary distance from P(w) is a+c sn(w)>0. Translating the inverted polygon by -f does not alter its signed area, so its vertices may be written (P(w)-f)/(a+c sn(w))^2.

For one side with midpoint phase u and endpoints P(u-v),P(u+v), let E_+(u) be its signed half-cross-product after inversion. Addition formulas reduce it to

E_+(u)=C dn(u)D(u)/[(1+k sn(u))(U+kV sn(u))^2],
C=b h dn(v)q^2/alpha^3,
D(u)=1-k^2t sn^2(u).

This was checked against direct Euclidean inversion in preliminary65-digit calculations, but still requires exact algebra verification. The intermediate denominator identity is

(a+c sn(u-v))(a+c sn(u+v))
=alpha^2(1+k sn(u))(U+kV sn(u))/(q D(u)).

Antipodal pairing is available for even leastN. Put m=N/2 and define B(u)=E_+(u)+E_+(u+2K). Algebra gives

B(u)=2C D(u)[U^2+k^2 V(V+2U)sn^2(u)]
       /[dn(u)(U^2-k^2 V^2 sn^2(u))^2].

Then inverse signed area is sum_(j=0)^(m-1) B(w+v+j delta). This is equal for the two foci by central symmetry.

## Proposed complete pole mechanism, still under author checking

For V nonzero, B is periodic2K, anti-periodic2iK', and odd about r=K+iK'. Its candidate poles are a simple pole at r and at most double poles at r±delta, plus imaginary translates. At the ordinary Jacobi poles p=iK', the displayed expression is removable. The two double-pole principal coefficients are opposite by oddness about r; when summed over the cyclic delta orbit, they cancel at the same reduced-torus location. The reduced real period is ell=2K/m. The inverse-area sum should therefore have only two simple poles at r and r+2iK' modulo (ell,4iK'). Residue matching and anti-periodicity force it proportional to S(u+K), S(u)=sum_(j=0)^(m-1)dn(u+j delta).

For N4, delta=K and V=0, the summand reduces to

B(u)=2C/U^2 [q/dn(u)+t dn(u)].

It has only simple poles at r and p. Since ell=K, these are the same reduced real class. This case needs its own pole accounting, not the generic formula.

As derived for the origin-pedal problem, the full orbit area is 2ab sn(v)cn(v)/dn(v) times S(w). The cyclic dn sum has two simple poles and zeros shifted by ell/2; S(w)S(w+ell/2) is constant. For N=4n, (K+v)/ell=(m+tau)/2 is a half-integer, so the claimed inverse-area product follows if every summand and pole assertion above is confirmed. This analytic mechanism reuses the author's work on k203,b and must be credited as related work, not counted as independent verification.

Preliminary direct inversions give phase-independent products at N4,8,12, including stars; the N4 value is4. N6/N10 controls vary, while the predicted area ratio stays constant. These are numerical probes only.

## Next checks and completion estimate

Verify the rational edge identities symbolically, full pole locations/multiplicities and residue cancellation (including all primitive stars and N4). Check the later primary source for known general results. Write a complete frozen proof with exact controls, then obtain review by an uninvolved agent before any claimed-result PR. Five substantive turns remain the maximum budget if unresolved; only the current first turn has begun. Completion estimate:65% of a full proof-and-review deliverable, not a success probability.
