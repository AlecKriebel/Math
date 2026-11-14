UTC: 2026-11-14T23:36:51.780201+00:00

# Exact adversarial derivations

The equations below are a resumed reconstruction after the primary read and predecessor-lane exposure declared in RESUME_RECONSTRUCTION.md. No other review lane was read. No sampled simulations are used.

## 1. Atomic local chains, clocks and normalization

For a state S, list each ordered parent u / target v pair with different types. Deleting the Bd common positive factor F(S) does not change harmonic absorption probabilities. Its rate is fitness(u) w_uv/d_u. Deleting the dB common factor n likewise leaves fitness(u) w_uv / sum_x fitness(x) w_xv. The active component in an otherwise isolated global chain is lazy, but both clocks preserve these internal harmonic probabilities. Inverting relative fitness gives beta_v(r)=f_v(1/r).

The independent verifier rebuilds all six nonabsorbing triangle states under each rule. It solves the actual Dirichlet system, substitutes every solution back into all 12 equations, and establishes the five printed aggregate rational functions (16),(17),(19),(20),(23) by identities, not examples. It also checks neutral uniform averaging, the equal-edge triangle baseline, the singular singleton limits (Bd: 0,1,0; dB: 1/2,0,1/2), the complete dB telescoping adjacent ratio and the endpoint arithmetic. These checks pass. The disconnected graph at delta=0 is not substituted as a valid population graph.

## 2. Rare-edge error

Let a<=w_internal<=b and w_outer<=epsilon<=b. Each vertex has positive internal degree at least a. A desired discordant directed internal replacement has probability at least a/(r n² b) per global update under either rule. A monotone spanning-tree sequence of at most s replacements therefore yields absorption in s steps with probability at least p^s, p=a/(C_r n²b). In the isolated lazy chain E[tau]<=s p^-s. The per-update chance of any outer replacement, and the total-variation cost of deleting outer choices, are at most C_r n epsilon/a. Couple only until the first discrepant/outer event. A stopped union bound is at most C_r n epsilon/a E[tau], so this avoids estimating an original chain after uncontrolled external disturbances. The printed eta is a larger dimensionless bound. Long monomorphic waiting times incur no accumulated discrepancy: the next type-changing outer event is drawn from its exact competing rates.

For n<=4N²,s=N,a=N^-4,b=1,epsilon=N^(-N³), log eta=-N³ log N+O_r(N log N). Thus N^K eta->0 for every fixed K. All constants may depend on fixed r. No uniformity as r approaches 1 is used.

## 3. Exact macro raw rates and success budgets

Put c=N,M=N²,Z=(N-1)N^-3,Dc=Z+3M epsilon, d_v=(1+delta,2delta,1+delta), and Xeps=sum_v 1/(d_v+c epsilon). Keep isolated marks Q_U, Qbar_U, f_v^U and beta_v^U.

With a single mutant module and resident center, Bd rates after deleting F are

    seed_raw = r c epsilon Xeps,
    erase_raw = 3 c epsilon/Dc,
    seed_success = seed_raw Q_B,
    erase_success = c epsilon sum_v beta_v^Bd / Dc.

Therefore the successful ratio is exactly r Dc Xeps Q_B/Y_B in the marked chain. Its leading value is (r-1)N²/2. The raw seed/erase ratio grows like r N²/6, and Q_B is bounded below for each fixed r>1, so success per raw introduction is bounded below by a positive r-dependent constant.

For dB with one mutant module, the exact marked rates are the manuscript's (33),(34). At leading order,

    seed_success ~ 3 c r epsilon Q_D/(n Z),
    erase_success ~ c epsilon I_D/(n r),

so their ratio is 3r(r-1)/(Z I_D)~6r²(r-1)N²/(2r+1). Raw erase rates contain X~1/(2delta); success per raw introduction is at least c_r delta (indeed the seeding term alone gives a stronger bound at the selected scales). No illicit switch from all introductions to successful jumps is needed.

With mutant center and R resident modules, Bd rates after deleting F are

    good_raw = 3 R r c epsilon / Dc,
    good_success = R r c epsilon sum_v f_v^Bd / Dc,
    bad_raw = R c epsilon Xeps,
    bad_success = bad_raw Qbar_B.

Hence bad_success/good_success = Dc Xeps Qbar_B/[r sum f_B] = O_r(N² r^-N), uniformly in R. Moreover good_success/(good_raw+bad_raw) >= c_r N^-2. The factor R cancels exactly.

For dB, write Dcenter(R)=rZ+3r(M-R)epsilon+3R epsilon. Then

    bad_raw = (c/n) 3R epsilon/Dcenter(R),
    bad_success = bad_raw Qbar_D,
    good_raw = (R/n) sum_v c r epsilon/(d_v+c r epsilon),
    good_success = (R/n) sum_v c r epsilon f_v^dB/(d_v+c r epsilon).

Since epsilon is superpolynomially smaller than every internal scale, uniformly for 1<=R<=M,

    bad_success/good_success = O_r(Z^-1 Qbar_D)=O_r(N² r^(2-N)),
    good_success/(good_raw+bad_raw) >= c_r delta.

The forward weighted sum tends to (r+2)/2>0, while X is O(delta^-1). Thus N² module conversions cost expected O_r(N^6) raw excursions. At cutoff N^10, Markov costs O_r(N^-4); the first stage costs O_r(N^-6). Multiplying the reversal bounds by M costs only O_r(N^4 r^-N). Together with N^10 eta these are o(N^-2), not just o(1). This independently supports the main theorem and its endpoint error scale.

## 4. Endpoint averaging and fixed-r quantifiers

At r=3/2, alpha=1/3+O(N^-4), A_B~N²/4,A_D~27N²/16. Thus module-start deficits are 4/(3N²) and 16/(81N²). A center start has Q_B=1/3+exponentially small and Q_D=(1-1/N)/3+exponentially small. Its mass is exactly h=1/(3N+1). Therefore the graph dB coefficient is -(16/81+1/9)=-25/81; subtracting the complete dB coefficient -1/9 gives -16/81. The Bd coefficient is -4/3. All errors above are o(N^-2).

For each fixed 1<r<3/2, 1/3-(1-1/r)=(3-2r)/(3r)>0. Separate convergence of graph and complete probabilities gives an eventual threshold depending on r; the same graph sequence is independent of r. For each fixed r>3/2 the sign reverses. At r=1 the neutral uniform mean is 1/n; this does not contradict a limit whose r is fixed greater than 1 before N tends to infinity. No claim of a universal endpoint obstruction follows.

## 5. Exact obstruction to the advertised growing-type diffuse derivation

The deposited detailed diffuse source note specifies Q_s->infinity,Q_s=o(s), equal portal-network row sum H>0, max portal edge->0, exchangeable portal incidence lambda_t/s, fixed B=2 sum pi_t lambda_t>0, and max lambda_t=o(s) for growing types. It claims (lines158–163) external intervention during a fast heterotypic blade resolution is O(Q_s/s). That estimate fails under its stated domain.

For integer K>=2 choose s=K²,Q=K,H=1 and a complete portal network of edge weight1/(K-1). Take K high-load blades with lambda_H=K and K(K-1) low-load blades with lambda_L=K/(K-1). Then B=4 exactly. If growing T is desired, split the low blades into K nominal types, each with K-1 blades and identical lambda_L, giving T=K+1. This relabelling changes no graph. All incidences are positive, every endpoint has the same incidence to every portal, graph data are independent of fitness, Q/s=1/K->0, max lambda/s=1/K->0 and max portal edge=1/(K-1)->0. Both B and H are constant. But a high-blade endpoint has total outer incident weight Q lambda_H/s=1, as large as its internal edge.

Start with one mutant endpoint u of a high blade, all other vertices resident. Under dB in n-time units: u is erased at rate1, its resident blade neighbor turns mutant at rate r/(r+1), and mutant introductions into all portals total r/[5+(r-1)/K]. The labelled resident-portal-parent erasure of u alone has rate1/2. Therefore the probability that the first type-changing event is that outer erasure is exactly

    (1/2)/[1+r/(r+1)+r/(5+(r-1)/K)].

At r=3/2 this tends to5/19, rather than zero. Under Bd after removing the common F denominator, the same outer erasure has rate1/5, internal erasure rate1/2 and total mutant births rate r. Its first-event probability is 2/(10r+7), exactly1/11 at r=3/2. These are rational event calculations; they require no simulation or limiting chain approximation.

The failure cannot be dismissed solely as a uniformly rare initialization type. A mutant portal directs half of its Bd blade-target edge mass to high blades. For dB with a single mutant portal and resident blades, the exact total n-time raw introduction rate into blades tends to3r: the high and low classes contribute r and2r. The dilute-blade approximation used by the source would give rB=4r. The actual high-class raw target fraction tends to1/3, whereas its asserted size-biased distribution f_H=2 pi_H lambda_H/B is1/2. Thus even the raw coefficients in the putative uniform episode-to-blade derivation have a nonvanishing discrepancy.

This is a falsification of a load-bearing vanishing-error estimate and its advertised uniform supporting limit; it is not a graph that simultaneously amplifies and does not falsify the main center–triangle theorem. The final no-overlap inequality could still hold on this broader class for a different reason. No repair or expanded hypothesis is supplied here. The exact gap is a valid derivation on the detailed advertised growing-type domain, or an unambiguous original scope restriction excluding it. Manuscript Section11 item3 says singular load scaling is outside its scope; its detailed source explicitly excludes only singular B,H scaling, and our B,H are fixed. This discrepancy prevents full auxiliary-claim clearance on the current archive. It must be reported with this scope qualification.

## 6. Other auxiliary checks and limits of this lane

Theorem6's finite rates, hub-occupation drift and killed quadratic are algebraically consistent; their exact polynomial checks do not establish the polynomial-time post-establishment uniformity. The source supplies a longer multiregion argument. I inspected it in full, including endpoint deficits and cutoff removal, and found no definition-level counterexample. Its phrasing that the ratio is r-o(1) is stronger than necessary for h=1 and bounded i; a uniform lower comparison is the meaningful quantity. I do not treat that wording alone as a substantive defect.

For Proposition8, before hub activation all leaves are resident. Its rates are correct. On 1<=i<floor(c/2), the up/down ratio is bounded between any fixed s<r and r for sufficiently large c, independently of leaf weights. For 1<z<s, the denominator 1-(s/z+z)/(s+1)>0 because(z-1)(z-s)<0. The decreasing potential z^-i has a uniform geometric drift. It bounds the expected extinction-weighted occupation sum, which is the correct quantity for marks that add fixation probability. The leaf activation-first bound and sum over leaves are exact and uniform. I found no counterexample to this argument.

Once the diffuse supporting gap was identified, I stopped expanding that route. I have not represented a finite certificate replay, archived PASS label, or a narrowed main-theorem check as clearance of every auxiliary assertion. No source modifications, repairs, promotion, outreach, site or inventory mutations were performed.
