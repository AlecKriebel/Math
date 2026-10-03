# Independent network-measure and exterior-tail audit of PR41

**Scientific disposition: PASS for the unconditional interior law/full-length lower bound and for the explicitly conditional full-length law. The indexed full SIRSN target remains UNSOLVED.** No mandatory correction to the candidate mathematical body was found. This is an independent adversarial audit with finite diagnostic support, not a proof by computation, an exhaustive novelty certificate, or external peer review.

## Independence, source priority, and the exact functional

`INITIAL_PRIMARY_TARGET_SEAL.md` and `INITIAL_SEAL_RECEIPT.json` were written before opening any proposed proof, old review, code, saved diagnostic JSON, PR body, root conclusion, or other PR41 family. The draft-title exposure (“SIRSN spanning law extra-tail”) was disclosed. I first read the complete original flat source/prior/provenance and snapshot, then directly acquired Aldous's live author page and the 2012 and 2014 PDFs. Both PDF hashes match the original provenance. I read the whole operative definitions/discussion, published major-road scaling/proofs, and both target passages, and visually checked published page38/41.

Aldous's 2012 Open Problem35 asks for the full expected-length asymptotic. Published 2014 Open Problem9 expressly asks which extra assumptions, if any, make that same law true; the paper says it supersedes arXiv1204.0817. The published definition has priority for the precise current question. The imported prior's Steiner-minimum wording is wrong: span is the **union of all prescribed pair routes**, with overlapping road length counted once. The original imported records are provenance and must stay byte-exact; corrected current interpretation must be recorded separately. The candidate already makes both distinctions correctly. Its finite fourth-order little-o tail answers a sufficient-assumptions question; it does not prove automatic applicability under all SIRSN axioms.

Full SIRSN assumptions relevant here are finite, simple, measurable compatible prescribed routes; consistent finite-dimensional distributions; translation/rotation and Euclidean scale invariance; independent PPP sampling; finite unit-distance mean route length; and finite limiting major-road intensity p(1). Ell is the intensity of S(1), not p(1) or a Steiner constant. A weak SIRSN does not automatically supply finite p(1). The candidate interior argument actually needs only the locally integrable sampled-network measure and finite mean pair length; its exterior bound uses the full major-road hypothesis.

## Checkable random-measure justification

Every feasible route is a countable union of straight segments together with at most countably many endpoint/vertex points. For the countable PPP endpoint configuration, every route union is a Borel set and its geometric edge length is restriction of one-dimensional Hausdorff length; compatible overlaps have multiplicity one. Endpoint sets have zero one-dimensional length. The random-network/measurability assumptions in the primary supply measurable local length evaluations; no uncountable all-continuum route union is constructed by the candidate. The primary outlines, rather than gives every technical step of, the random-subnetwork measurable-space construction; this audit relies only on the standard local random-measure assertions that are part of the stated SIRSN setup.

Let M_lambda(A)=len(S(lambda) intersect A). Its mean is ell sqrt(lambda) area(A), a locally finite deterministic intensity measure. For a fixed unit cell C, finite spans from increasingly large endpoint windows form an increasing sequence of Borel sets whose union is S(lambda): every ordered or unordered pair of PPP endpoints occurs in a sufficiently large window. Thus continuity from below of length, followed by monotone convergence in expectation, proves a_lambda(r) increases to ell sqrt(lambda). Moreover each local random mass is bounded by the integrable M_lambda(C), so it also converges in L1. No closure of a geometric network is taken; no spurious edges are inserted; endpoint continuity of routes in an infinitely dense binomial sequence is unnecessary.

For fixed r, admissible integer-centered unit tiles have their centered side-r endpoint windows within Q_n. Their number is n^2+O_r(n), including noninteger n. Local route inclusion and translation invariance give the lower bound by this count times a_lambda(r); the entire sampled network gives the upper bound ell sqrt(lambda)n^2. Deterministic tile boundaries have zero expected M_lambda mass by zero planar area, so sums do not double-count positive expected length. Taking n to infinity before r proves the interior coefficient. Stationarity suffices; no mixing or ergodicity is used or inferred.

Ell>0 follows as stated: ell=0 would imply almost surely zero length in each square of a countable covering, hence zero S(1) length globally, contradicting a positive-length route between distinct PPP endpoints. A stationary mixture with different random conditional intensities would still have a deterministic mean intensity; an expectation law does not assert an ergodic samplewise law.

## Near, middle, and far exterior regions

The first expanded-square strip has area4n+4 and is bounded by the S(lambda) random measure, giving ell sqrt(lambda)(4n+4). For r=2^j, every point of Q_n^(2r) minus Q_n^r is strictly farther than r from every endpoint in Q_n; its finite-span edge lies in E(lambda,r). The annular area is (n+4r)^2−(n+2r)^2=4nr+12r^2. The mean major-road measure therefore gives p(4n+12r). This is pointwise set inclusion then an expectation bound, not multiplication of a network-mass expectation by an unrelated or correlated event probability.

With J=floor(log2 R), the unit strip and j=0,…,J annuli cover the exterior buffer through R≥1, sometimes beyond it. Both overcoverage and geometric overlaps preserve an upper bound. J+1≤1+log2 R and sum2^j≤2R give exactly

    E nearby exterior length ≤ ell sqrt(lambda)(4n+4)
                              +4pn(1+log2 R)+24pR.

The far exterior is treated separately. If a finite simple route with both endpoints in Q_n visits outside Q_n^R, the two endpoint-to-visited-point subpaths each have length at least R, so its full length L≥2R. Its outside contribution is at most L times1{L≥2R}. Conditioned on independent sampled endpoints x,y, invariance gives L distributed as cD with c=|x−y|≤sqrt(2)n. The function cD1{cD≥2R} is increasing in c pointwise, yielding the uniform bound sqrt(2)n h(sqrt(2)R/n), h(t)=E[D1{D≥t}]. Expected unordered PPP pair count is lambda^2 n^4/2, not (lambda n^2)(lambda n^2−1)/2. Linearity of expectation, without route independence, gives the exact constant/exponent

    E far exterior length ≤ lambda^2 n^5 / sqrt(2)
                            times h(sqrt(2)R/n).

All nonnegative geometric lengths have the right scaling: pair count depends on the dimensionless lambda n^2, each route contributes length of order n, and p/r is length per area. R=delta n^2 is an asymptotic choice in the fixed sampling length units; restoring a reference length L0 gives R=delta n^2/L0. It is not a simultaneous Euclidean-rescaling assertion.

The source removes closed endpoint disks while the candidate informally says distance at least r. Its operative annuli are strictly farther than r, which alone resolves the inclusion. Additionally, a countable straight-segment route has zero length on an endpoint circle, so either radius convention has the same length intensity in the stated feasible-route class. No arbitrary rectifiable-curve circle argument is assumed.

## Tail integral, critical exponent, and limit order

For the strict cutoff, layer cake gives

    E[D1{D>t}] = t P(D>t) + integral_t^infinity P(D>s) ds.

The hypothesis t^4 P(D>t)→0 yields, for any eta>0 and every sufficiently large t, an upper bound (4eta/3)t^(−3). The nonstrict h is bounded by the strict truncated expectation at t/2, handling all atoms. Thus h(t)=o(t^(−3)). Finite ED^4 is sufficient because t^4P(D>t)≤E[D^4 1{D>t}]→0. It is not necessary: a scalar tail t^(−4)/log t for t≥e satisfies the hypothesis but has divergent fourth moment, while h(t)≤4/(3 t^3 log t). This is a scalar boundary diagnostic, not an asserted realizable SIRSN.

For each **fixed** delta>0 take R=delta n^2. The normalized far term is lambda^2/sqrt(2) times n^3 h(sqrt(2)delta n), tending to0. The normalized near-strip/log terms tend to0 and its remaining limsup is ≤24p delta. Nonnegativity then permits delta↓0. Under the extra tail, normalized expected exterior length tends to0; any needed exterior L1 control is a deduction of these bounds, not a hidden assumed global major-road dominator.

The distinction from big-O is essential. For a scalar Pareto exponent alpha, h(t)=alpha/(alpha−1)t^(1−alpha); the normalized far term at R=delta n^2 is proportional to n^(4−alpha). Alpha=4 leaves a positive constant proportional to delta^(−3), so this bound cannot be closed by delta↓0. Alpha=2 has finite mean yet fails badly. Likewise the valid little-o tail t^(−4)/log t does not justify replacing fixed delta by delta(n)=n^(−1/2): n^3 h(delta(n)n) has a divergent lower bound of order n^(3/2)/log n. The candidate takes the proper ordered limits.

## Poisson to binomial transfer

For an independent auxiliary count N and a coupled uniform endpoint sequence, prescribed-route consistency makes F_m(n) nondecreasing in m. The argument never asserts that its infinitely dense endpoint sequence is a feasible locally finite network. All finite F_m expectations are bounded by sqrt(2)n Delta binom(m,2), including full exterior length. The upper-count inequality is E F_N ≥ P(N≥k)E F_k, using independence of N from the endpoints/routes. A route-dependent count would invalidate that factorization.

For the lower count, split at N≤k and bound the excess by the pair-length polynomial. The exact identity is E[N(N−1)1{N>k}]=mu^2P(Pois(mu)>k−2). With mu=(1−epsilon)k and theta=−log(1−epsilon), the exponential rate epsilon+log(1−epsilon)<0; the two-unit shift contributes a fixed factor. Its error is negligible after dividing by n^2=k. The upper probability tends to1. First k→infinity and then epsilon↓0 proves the interior binomial law. For full length, only the upper sandwich at1+epsilon and the already established interior lower bound are needed. No second independent exterior lower limit is missing.

## Generic shortcut counterexamples and controls

The authored controls give concrete checks independent of the reviewed scripts:

* Three prescribed line routes on endpoints0,1,2 have union length2 and sum length4. A 3-4-5 triangle has all-pair prescribed union length12, but a connected competitor of length7; a minimum connecting functional cannot silently replace span.
* An event A of probability1/m^2 with random mass m^2 1_A has E mass=E[mass1_A]=1, while the false product E mass P(A)=1/m^2. Holder would require an additional useful random-mass moment or a justified conditional bound. The candidate does not take this shortcut.
* Y_m=m on an event of probability1/m tends to0 in probability but has mean1, showing why vanishing excursion probability alone is insufficient for expected length. This can be represented by a generic escaping random measure; it is not a stationary compatible SIRSN construction.
* The exterior major-road bound has annular terms at least12pr, whose infinite dyadic sum diverges. Local intensity does not give a finite global exterior dominator. Divergence of an upper bound does not prove that actual SIRSN exterior length diverges.
* Atoms, power-law exponents, a slowly varying fourth-order tail, and a route-dependent count test the cutoff and ordered-limit requirements directly.

All generic examples are explicitly NOT admissible SIRSN counterexamples. They falsify generic inference rules only; they do not prove the tail condition fails for any full SIRSN, prove its necessity, or resolve the unconditional target.

122 own finite/exact controls actually passed. Four actual source corruptions were rejected with full stderr: wrong annular coefficient, counting overlap multiplicity, replacing nonstrict cutoff by strict at an atom, and promoting fourth-order big-O to the required vanishing bound. These diagnostics supplement the analytic argument; none samples a SIRSN or certifies every infinite-dimensional assumption. Full executed sources, argv/cwd, UTC clocks, streams, exits, and failure bodies are retained under executions/.

## Imported primary model applicability: precise qualification

The candidate's applicability observations use existing results, not new model estimates. Directly read Aldous Proposition3.1 statement, its continuum-limit usage and final bounded Euclidean-stretch verification: D≤sqrt(2)K_gamma almost surely for the binary hierarchy. Directly acquired Kahn v3 (hash matching original provenance), read whole Theorem5.1 proof and Remark5.1: the proven exponent range is delta<gamma−1, giving a fourth moment for gamma>5. The subsequent better exponent is explicitly conjectural, and gamma=5 is outside the proven fourth-moment claim.

There is a printed-proof qualification in Kahn that must not be hidden. Displayed(18)/(21)/(22) bound a conditional probability given Txy≤Tn by unconditioned geometric-event probabilities, although the conditioning is dependent. The moment deduction can instead use the valid event inclusion

    P(Lxy>r_m, Txy≤Tn) ≤ sum P(B0 intersect … intersect A_k),

then add P(Txy>Tn). The same geometric calculation bounds the first sum by2^(−n−1), and the time tail by2^(−n−1), obtaining P(Lxy>r_m)≤2^(−n). Also floor m gives r_m≤the stated upper envelope rather than literal equality; a correctly shifted quantile-moment sum has the same convergent geometric exponent for delta<kappa<gamma−1. These are elementary credited source-import qualifications, not a novel SIRSN result and not a correction needed in the candidate's main proof. This audit does not claim that every literal line of Kahn's printed proof is correct or independently certify its entire SIRSN construction. Other later geodesic-literature statements in SOURCE_AUDIT remain bounded imported bibliography observations, not independently whole-paper-certified here.

## Exact package/accounting truth and action

Every original16 file was read as complete bytes and matched its frozen size/SHA. All mathematical prose and both reviewed source programs were read without importing/executing them. Every field and all211/3809 saved check names/values in all eight original JSON documents were parsed with duplicate-key rejection and retained as complete objects in ORIGINAL_READ_LEDGER.json. Saved diagnostic PASS records are not actual replays by this family. The entire201709-byte/4919-line original diff was inspected structurally: all16 newly added payloads reconstruct the original bytes, and its seventeenth queue block changes only the target row's status/turns/findings, queued0/5→unsolved2/5. This is frozen-diff truth; no current native/Git or shared-state claim is inferred from it.

Original attempt.json and turns.json coherently record two authored substantive attempts of five: interior partial, then scoped conditional candidate. Original model gpt-6-astra/xhigh and the expired deadline are archival facts. The original proof and author receipt carry final SHA464af6…; the old review's earlier hash is explicitly extended by its final hash addendum and review_summary. No native/shared state, Git, remote branch, canonical tracker, DOI, or human outreach was changed. Every PR39 closure was preserved.

Actionable disposition: retain the extra-tail assumption prominently, retain full target UNSOLVED and local2/5, preserve complete upstream source/prior/proof/code/ledger, and distinguish saved diagnostics from future actual original-helper reproductions. If imported model moment proofs are discussed, include the source qualification above rather than claiming all printed conditional estimates were directly valid. Do not infer a general solution from the conditional result or a qualified absence-of-literature finding from a nonexistent exhaustive search.

Exact remaining unconditional gap: prove o(k) expected total exterior route-union length from the ordinary SIRSN axioms, by deriving this tail rate or a materially different valid geometric/integrability bound; alternatively an admissible full-SIRSN counterexample would settle failure. Scalar tails, generic random measures, extra moment assumptions, and an unintegrable major-road bound transfer rather than solve that difficulty. No new substantive route to that target was attempted during this audit.
