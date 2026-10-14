# Independent mathematical reconstruction before prior verdicts

Recorded 2026-10-13 06:18 UTC. This derivation was formed from the current manuscript and algebra, before reading original/family proof reports or earlier verdicts. It treats the invariant as a hypothesis.

## Scope and exact claim

For a>b>0, a strict nested nondegenerate confocal elliptical caustic (alpha,beta), and each primitive odd N>=3 with gcd(N,tau)=1 and 0<tau<N/2, use the ordered original-side origin pedal and original-vertex origin antipedal P dot X=H(P). Areas mean ordered signed shoelace areas. Claim: their product is phase independent; consecutive real antipedal intersections are finite. This is an all-period analytic claim, not an inference from sampled trajectories. Reversals and repeats have the expected sign/scaling effects. Hyperbolic/collapsed/even extensions and unsigned area replacements are not inferred.

## Generic antipedal identity, independently derived

Let D_i=det(P_i,P_{i+1}), C_i=P_i dot P_{i+1}, H_i=P_i dot P_i, and J(x,y)=(-y,x). Solving the two named line equations gives R_i=P_i+[(H_{i+1}-C_i)/D_i]JP_i. The preceding intersection is R_{i-1}=P_i-[(H_{i-1}-C_{i-1})/D_{i-1}]JP_i. Since det(P_i,JP_i)=H_i, the triangle contribution is det(R_{i-1},R_i)/2=H_i(t_previous+t_next)/2. Collecting an edge's two contributions gives [H_i H_{i+1}-(H_i+H_{i+1})C_i/2]/D_i. This proves the actual signed-area formula F directly for any finite consecutive intersections. No convexity, nonzero norm, or new generic-F discovery is assumed.

## Complete determinant divisor

Canonical coordinates P(w)=(-a sn w,b cn w), a=alpha dn(v)/cn(v), b=beta/cn(v), v=2K tau/N, delta=2v give B(u)=2ab sn(v)cn(v)dn(u)/(1-k^2 sn^2(v)sn^2(u)). At u=p=iK', dn has pole order one and D has pole order two: B has a simple zero. At u=p+/-v, D has two simple zeros with D' equal respectively +2cd/s and -2cd/s; dn is regular nonzero, so B has simple poles. At r=K+p, dn has a simple zero and D=c^2>0, so B has a simple zero. sn^2 has degree two on C/(2K Z+2p Z); its one double pole and the displayed two simple preimages exhaust D. dn has no further divisor support. These are complete support and exact orders, even though B is antiperiodic under 2p.

The p-centered finite endpoints are opposite by the p-shift formulas. The r-centered endpoints coincide by P(2r-z)=P(z). A conflation of these two determinant zeros would invalidate the proof, but the current manuscript separates them correctly.

## Exhaustive antipedal poles

At coincident regular endpoints, the numerator equals ((H(P)+H(Q))H(P-Q)-(H(P)-H(Q))^2)/4. It is O(z^2), including isotropic complex normals, and division by B=O(z) is removable. At opposite regular endpoints the numerator is holomorphic, giving at most a simple pole. This contribution cannot be discarded.

At a pole vertex P(p+z), coordinates have pole order one, H pole order at most two, and the neighboring vertex is regular. The numerator of an incident F has pole order at most three and its determinant has pole order one, so F has order at most two. The preceding-plus-following terms are exactly G(z)-G(-z): P(p-z)=-P(p+z), the previous neighbor equals minus the forward neighbor evaluated at -z, F is antisymmetric under interchange and invariant under joint negation. Thus the possible z^-2 term cancels. Odd coprimality gives one singular vertex per phase modulo 2K; no edge has two pole endpoints. For N=3 the nonincident edge has opposite finite endpoints at the same phase and adds at most a simple pole, so the total bound remains valid.

Vertex singular phases are p-j delta, and opposite-midpoint phases are p-v-j delta. With ell=2K/N, delta=2tau ell, v=tau ell, and gcd(2tau,N)=1, both supports become p and 3p on the actual torus X=C/(ell Z+4p Z). The determinant-reflection character of F gives antiperiod 2p; real shifts and cyclic reindexing give period ell. Hence U has at most those two simple poles.

## Independent trace-space proof

S(w)=sum dn(w+j delta) is even, ell-periodic, and 2p-antiperiodic. At p only one summand is singular modulo 2K and has residue -i. At 3p the residue is +i. Thus there are exactly two simple poles on X, and S is not zero. Reflection followed by ell+2p fixes p+ell/2 and negates S, forcing a zero there; the same holds at 3p+ell/2. They are distinct nonpoles. On a compact torus zero order equals pole order, so they exhaust the zero divisor and are simple. The product S(w)S(w+ell/2) has all apparent poles canceled and is constant.

For any meromorphic antiperiodic function with only possible simple poles at p,3p, matching its residue at p to S also matches that at 3p. The difference is holomorphic and therefore constant on X; its antiperiod forces zero. This is a constructive one-dimensionality proof, not a circular restatement of the target area product. In particular U=c_star S, allowing c_star=0.

## Actual pedal and the half-period

The line normal n(u)=(-sn(u)/alpha,cn(u)/beta) obeys n dot n=dn^2(u)/beta^2. Thus Q=n/(n dot n)=(-alpha k'^2 sn(u)/dn^2(u),beta cn(u)/dn^2(u)) is the actual origin foot. At a common Jacobi pole its numerator has order one and denominator order two, so it is holomorphic and vanishes. Its only possible coordinate poles are double at dn zeros r and translates. Q(2r-z)=Q(z) implies the sum of the two incident determinants is det(Q(r+z),Q(r+delta+z)-Q(r-delta+z))/2. The neighbor difference is O(z), and neighbors are regular; thus the area trace T has only simple poles. Q's imaginary reflection makes T antiperiodic, and odd coprimality gives real period ell. Shifted residue uniqueness gives T(u)=c_p S(u+K). Actual chord midpoints are u=w+v, so A_O(w)=c_p S(w+v+K).

Since (v+K)/ell=tau+N/2 is half-integral, the actual product is c_p c_star S(w)S(w+ell/2), constant. This proof never divides by a derived area.

## Real domain, controls and dimensional checks

For real u, B>0 because s,c,dn(u)>0 and D>=1-k^2s^2>0. All consecutive radial vectors are linearly independent and each antipedal intersection is finite, including admitted stars. The primitive hypothesis and real line construction resolve the domain independently of complex norm zeros. Under reversal both derived area orders reverse; repeats multiply each area by r. Areas and constants c_p,c_star have units length squared; the product has units length fourth. Circle coordinates directly give pedal radius R cos(theta/2), antipedal radius R/cos(theta/2), and product N^2 R^4 sin^2(theta)/4, finite for 0<theta<pi.

For the N=4 control, set a^2=5,b^2=3. The diamond is (sqrt5,0),(0,sqrt3),(-sqrt5,0),(0,-sqrt3), with caustic alpha^2=25/8,beta^2=9/8. Its side lines are caustic tangents since alpha^2/a^2+beta^2/b^2=1. The axis vertices reflect by symmetry. The rectangle uses +/-alpha,+/-beta; its vertical/horizontal sides touch that same caustic, and alpha/a^2=beta/b^2 makes the normal bisect the incoming/outgoing axis directions. Direct signed line calculations must yield 225/4 and 289/4 and will be independently checked below. Thus evenness cannot be generalized.

## Mathematical verdict at this checkpoint

The complete analytic mechanism is sound in the stated domain. No unproved claim equivalent to the original target is introduced. No mandatory mathematical correction found. Remaining audit work is implementation reproduction, exact controls, primary-source attribution/priority, package integrity and actual PDF/readiness. Completion estimate: 35%.
