# Independent review of SIRSN traffic turns2–3

2026-10-02. **PASS_SCOPED_TURNS_2_3**, no mandatory mathematical revision. This is a fresh audit of the strengthened arguments, not an automatic extension of the earlier turn1 verdict. No final unrestricted-problem disposition is made.

Bound proofs: TURN_2.md SHA1338040f1716063c6560eb6365f22e8b3011d5d7c81184151e1137e8657339cc; TURN_3.md SHA720dc5da698aadef9e903aeab02a549997ae0ef848742037fdf4e47b476a3e81. All entries of the two frozen manifests matched. Both author receipts replayed exactly (2,077 and9,215 assertions). A separate checker passes8,224 exact controls. These are scalar/combinatorial support; the continuum arguments were reviewed analytically.

## Exact accepted scope

Turn2 proves full-interval local finiteness under a stated uniform local route-confinement modulus whose weighted square is integrable. It also proves a locally bounded traffic density relative to each major-road length measure, with a bound independent of the cutoff. That extra modulus is not derived from the ordinary SIRSN axioms.

Turn3 proves the critical beta=3 conclusion under the explicitly added jointly measurable continuum realization(JM), using only the ordinary finite first route-length moment and finite major-road intensity. Traffic restricted to any positive major-road cutoff is almost surely locally finite, has every positive moment of order less than one on bounded windows, and has infinite first moment on bounded sets of positive area. Combined with turn1, the accepted unconditional-moment range is2<beta<=3, still conditional on JM. The range3<beta<4 and automatic JM construction remain unresolved.

The primary source and renumbering were rechecked in the preceding review: Aldous2012 Problem31 versus2014 Problem5, §8.3. Relevant primary source: https://www.maths.tcd.ie/EMIS/journals/EJP-ECP/article/download/2920/2920-16115-1-PB.pdf . Major roads are endpoint-truncated route unions, not speed-threshold networks. The present report does not convert a conditional continuum theorem into a theorem from bare finite-dimensional laws.

## Turn2 checks

The earlier far-endpoint cutoff gives one bounded endpoint for any contributing typical pair; a sufficiently short displacement then bounds both endpoints in the same deterministic-index ball. The random local modulus applies to that ball on a countable probability-one event.

The translated-ball inequality is pathwise. For each fixed road point, the set of possible starting centers has area pi*omega(t)^2. Tonelli therefore bounds short-pair traffic by road length times2*pi² times the modulus integral. No independence of the random modulus and the road set is assumed. Pair-null exceptional sets become negligible for almost every displacement by Fubini, which is all the integral requires.

The large-pair contribution is controlled by the earlier endpoint cutoff and beta>2. Both density constants are independent of r, as asserted. Major-road length itself need not have a finite limit as r tends to zero, so no ambient local-finiteness statement follows. The Holder and logarithmic exponent tests are correct, including the explicit impossibility of an eventually sublinear-radius bound smaller than the endpoint distance when alpha=1. A qualitative modulus tending to zero alone is correctly distinguished from the required integrability.

The alternate first-turn short-length bound is also valid: restricting to routes of length<=tK places their intersection inside the ball centered at their start, and the road-length integral can be enlarged before averaging. It is not a false factorization of correlated events.

## Turn3: random finite road-size cutoff

If a sampled major-road point lies in B_R with witnessing endpoints at distance at least M, the route reaches outside B_(2R), since M>6R. The connector from the point to its first exit has length at least R and stays within3R of the witness point. Thus it lies in E_(M/2), with strict margin, and consumes at least R of length in B_(2R). The intensity/Markov bound8*pi*p*R/M is correct. Dyadic Borel–Cantelli and nestedness then imply eventual emptiness of E_M on the entire bounded window, not merely vanishing length. The witnessed sampled-set definition is essential here and is respected.

Hitting events can be treated in the completed probability space through the countably many measurable rectifiable route images; strict cutoffs are countable unions of closed larger cutoffs. The already explicit JM assumption is sufficient for the length integrals used throughout.

## Planted route and band partition

The support argument from turn1 holds for almost every endpoint pair on almost every realization. The major-road union and the sampled coupling are translation/rotation covariant and scale covariant in distribution: dilating the independent space-time Poisson sample only reparametrizes its time intensity, and its infinite union is unaffected. Together with the prescribed finite-dimensional route laws, this gives the same joint covariance with any fixed planted endpoint pair.

Consequently the expected omitted length outside the positive-road-size union is a constant times endpoint distance. It is finite by E[D]<infinity and vanishes for almost every pair by the Campbell support argument, so the constant is zero. This proves planted-unit-route support directly. Source equation(6.4) discusses one planted point; relying on it alone without this extension would be less explicit, but the candidate supplies the complete alternative argument.

The road-size cutoff is a global bounded-window event, hence applies also to the compact image of the planted finite-length route. Its length is therefore partitioned by F_(2^j u), j over all integers, for any fixed u>0. Nestedness gives disjointness and telescoping coverage. Integrating the resulting sum ell(2^j u)=d on1<=u<2 yields integral ell(u)du/u=d*log2 by Tonelli. No D-log-D moment is hidden in this step.

## Critical band expectation and almost-sure assembly

Mass transport must translate the joint route and major-road environment, not one while fixing the other. The proof does this correctly. Scaling yields expected rooted band length t*ell(r/t). With polar measure t*dt and kernel t^(-3), the resulting integral is ell(r/t)dt/t. The substitution u=r/t therefore gives the exact finite constant2*pi*|A|*d*log2 for every fixed band.

Each fixed band has finite traffic mass almost surely. In a bounded window only finitely many bands above any given cutoff are present, by the random road-size bound. Their sum is therefore finite pathwise; it does not require independence or a finite expected number of active bands. Countable windows/cutoffs and monotonicity justify all r>0.

On the other hand, the expectation of that sum is infinite because every band has the same positive expected mass. Tonelli allows the divergent sum. This is fully compatible with pathwise finite assembly and is not contradicted by the earlier first-turn large-trip estimate, whose random endpoint bound was never claimed integrable.

The tail split at J0+ceil(log2x) gives at most J terms on the complement of the high-road event. Markov controls their sum by JC/x; the high-road event is bounded by a constant/x. The resulting O((1+logx)/x) bound yields all subunit moments and does not yield the first moment, exactly as stated.

## Intrinsic-mark formula and remaining gap

Define the road-size mark using the supremum over rational positive cutoffs; nestedness makes this equivalent to the stated supremum and ensures measurability. Except for irrelevant interval endpoints, membership of a point in E_u is the interval0<u<S(point). For beta>3 the nonnegative integral of u^(beta−4) over that interval is S^(beta−3)/(beta−3). Combining this with the radial scaling change of variables proves the exact displayed annealed identity, including the power r^(3−beta) and constant2*pi*|A|/(beta−3).

A finite positive mark moment is therefore an exact finite-expectation criterion and sufficient for almost-sure local finiteness. It is not necessary for the latter; the critical case explicitly demonstrates why expectation and almost-sure conclusions must remain separate. No positive intrinsic-mark moment is proved from the ordinary first moment in these turns.

## Final assessment

The critical theorem and the separate confinement-modulus theorem pass in their stated scopes. Preserve JM, all cutoff conventions, the fixed-band versus whole-road distinction, infinite first moment and the unclosed beta>3 range in every later summary. Future turns need their own audit. This is independent AI-assisted review, without a historical-priority, human-referee or formal-certification claim. No author proof bytes were changed.
