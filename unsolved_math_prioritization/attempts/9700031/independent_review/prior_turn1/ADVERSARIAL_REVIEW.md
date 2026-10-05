# Independent first-turn review: SIRSN traffic, 9700031

2026-10-02. Verdict: **PASS_SCOPED_FIRST_TURN**, with a harmless cutoff-convention clarification below. No mandatory mathematical revision. This review covers only the frozen first author turn, not future work or a final disposition of the unrestricted problem.

Bound author proof SHA256: 1cc1e6c27c111d3ad98c7dac9025aea5a316a0c2bddae9766b69c3aaf25acae1. All seven entries in TURN_1_MANIFEST.json matched, and the author checker reproduced its saved receipt exactly. A separate implementation supplies 133,334 exact arithmetic controls. These support exponent/constant bookkeeping; the analytic and geometric arguments were reviewed directly and are not formally certified by finite computation.

## Source and scope

The primary 2012 question page49 was inspected visually and in the full local source context: Open Problem31 permits additional regularity assumptions. The published 2014 question page37 is Open Problem5, §8.3, and asks the traffic sigma-finiteness/scaling conclusions. The source weights prescribed route length with the endpoint-pair density, not a newly chosen path and not a speed-threshold road subset.

Primary sources reopened: https://www.stat.berkeley.edu/~aldous/206-SNET/Papers/aldous_SIRSN_long.pdf and https://www.maths.tcd.ie/EMIS/journals/EJP-ECP/article/download/2920/2920-16115-1-PB.pdf . The published definitions and continuum discussion in §§2.2–2.3,6.3 were checked. The source's FDD formulation does not silently establish the candidate's jointly measurable continuum realization. The explicit JM hypothesis is therefore essential and correctly retained.

The result is conditional local finiteness for 2<beta<4-2/(s+1) given E[D^s]<infinity, s>=1, plus the logarithmic beta3 endpoint. It reaches every beta in(2,4) in the all-moments subclass. It does not settle the general first-moment case for beta>=3, and it does not prove JM from the basic FDD axioms. No final full-original disposition is authorized by this scoped review.

## Critical checks

1. **Major-road support.** Independent Poisson superposition preserves the infinite-sample distribution after time reparametrization. Inclusion and equality of finite expected length in bounded windows imply a zero-length difference. Campbell's factorial formula applies because the second point sample is independent of the environment and the first sample, while JM supplies measurable integrands. Countable endpoint-window/rational-cutoff exhaustion produces an environment-wise almost-every-pair assertion. This is stronger and better justified than applying a fixed-pair statement to an uncountable collection.

2. **Uniform far-endpoint cutoff.** The expectation of length in B(0,2R) at cutoff M/2 is8*pi*p*R^2/M. Markov and dyadic summability yield eventually length<R almost surely. A continuous route reaching B(0,R) from endpoints outside B(0,M), M>4R, contains length at leastR inside B(0,2R), entirely at strict distance>M/2 from both endpoints. Support up to length-null sets is sufficient for the contradiction. Thus the cutoff is genuinely uniform over typical endpoint pairs. There is no illicit use of an absence-of-bi-infinite-geodesics theorem.

3. **Large trips.** Non-self-intersecting image length in a fixed major-road window is at most that window's total length. The endpoint cutoff then leaves a finite area for at least one endpoint, and the other endpoint's tail integral converges exactly for beta>2. The coefficient4*pi^2*M^2*epsilon^(2-beta)/(beta-2) is correct. No expectation of the random cutoff is needed.

4. **Tube bound.** Each point of E_r in a small disk has a route connector to the doubled disk's boundary lying in E_(r/2), by the3r/8 displacement bound. Finitely many connectors plus the outer circle form a connected finite-length set. Disjoint delta/3 balls each consume at leastdelta/3 of its length, giving N<=3J/delta. Maximal separated sets exist for an arbitrary bounded subset by finite Euclidean packing, without closedness. The resulting area bound12*pi*J*delta does not assume a finite number of original road components or a smooth-network tube formula. J has finite expectation from the known intensity.

5. **Short trips and moments.** The short-route event implies the starting point belongs to a tube of widthtK and the route contributes at mosttK. No independence between the tube and route is assumed. Translation invariance and Tonelli give the complementary mass-transport identity. Balancing t^2*K^2 with t*K^(1-s), K=t^(-1/(s+1)), gives exponent2s/(s+1). Radial integration has exponent1-beta+2s/(s+1), hence exactly the stated strict threshold. At s=1 the estimate remains valid and yields beta<3.

6. **Logarithmic endpoint.** With beta3 and K=t^(-a),0<a<1/2, the low part is integrable and the high part is the truncated D-log-D integral by Tonelli. The source uses a positive-part logarithm, not an unsupported endpoint extrapolation of a strict moment inequality.

7. **Sigma-finiteness and scaling.** The rational truncations cover each typical route except endpoint singletons and length-null subsets. Consequently the unrestricted traffic measure is supported on their union and has a countable cover by finite-mass truncated bounded windows. This does not assert ordinary ambient local finiteness. Scaling contributes c^4 from endpoints, c^(-beta) from their separation kernel and c from length, leading to the displayed push-forward factor c^(beta-5). Restricted cutoffs must scale r to cr, as the proof states.

8. **Simultaneity.** Countable windows and rational cutoffs, followed by monotonicity, justify all r>0. A countable cofinal sequence of moments/exponents plus monotonicity for trips shorter than one justifies all beta in(2,4) in the all-moments subclass. Long trips are controlled separately, so reversed kernel monotonicity there is not overlooked.

## Nonfatal cutoff convention

Aldous's formulation removes endpoint disks and is conventionally expressed by distances at least r; the candidate uses distances greater than r. Results pass between them by nesting: E_closed(r) is contained in E_open(r') for every0<r'<r, while E_open(r) is contained in E_closed(r). Finite intensity for strict cutoffs also follows by monotone unions of closed cutoffs r+1/n and p(r)=p/r. Therefore the theorem's local-finiteness and support conclusions transfer unchanged to the exact source convention. It would be useful to state this short clarification in a later version; no frozen-proof rewrite is needed.

## Credited model comparisons

Aldous's binary-hierarchy Proposition3.1 is a bounded-stretch source input; the candidate only applies it with the separate JM realization condition. Kahn's Theorem5.1 proof gives all route-length moments strictly below gamma-1, while Remark5.1 describes stronger moments conjecturally. The candidate correctly derives only beta<4-2/gamma from the established range and does not promote the conjecture.

No new proof search, unrestricted theorem, implementation of a continuum SIRSN, historical-priority determination, human peer review or formal certification is claimed. Future author turns require their own review before final publication of a complete packet.
