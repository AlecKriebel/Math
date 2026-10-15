# Primary-prior audit and conditional architecture certificate

UTC checkpoint: 2026-10-02T02:26:21Z. Audit completion estimate: 65%. This is an adversarial audit, not an extra research attempt or a repaired publication of the source theorem. No source PDF or TeX was edited.

## Primary receipts and exact attribution boundary

The fresh [Benjamini–Kozma primary record](https://arxiv.org/abs/2412.16600) lists only v1, submitted 2024-12-21 12:15:53 UTC; no journal reference is listed. Its 515,694-byte PDF and 73,808-byte `avoiding_coupling.tex` exactly match the old package hashes `2bf5c220f9bfee7b697482e1448bed5be268142bdb063861ba1f83aa005567f5` and `97650de9c6a65da504dfdce0825ce3aa4650b1f109f9cf215b6362c2ff1e28e7`. Thus none of the observed literal problems can be attributed to a different downloaded version. Full download/archive/version receipts are in SOURCE_RECEIPTS.json.

The source states the intended positive 4D full-trace theorem (printed p. 2), acknowledges its unresolved 3D case (p. 1), includes initial vertices (§1.2 pp. 2–3), and asks about a Markovian joint law separately. The final proof starts at 0 and a fixed x rather than restricting x to a neighbour (pp. 17–18). This supports attribution of the intended result for nonzero distance-ten starts. It does **not** independently certify every estimate or the general-fixed-x initialization: the quoted Lawler citation there is explicitly identified for neighbouring starts. This audit found no primary later arXiv version or posted correction that resolves the literal issues. That bounded observation is not a proof of present-day 3D openness or a claim about undiscovered publications.

## Dependency and location map

| Component | Exact source location | Assumptions / role | Audit status |
|---|---|---|---|
| Trace and initial-time convention | §1.2, pp. 2–3; TeX 299–329 | All times, full vertex traces, stopped paths retain prefix | Directly verified |
| Moment control | Lemma 2, pp. 4–7; TeX 357–634 | Independent 4D walks from radius n, separation > n/log n, stopped at radius m | Read in full; no full independent proof certificate |
| Good-time intersection control | Lemma 5, pp. 9–10; TeX 735–834 | Independent auxiliary walkers; lower intersection count following a hit; spatial boundary loss | Literal singular kernels falsified; trace versus temporal multiplicity conversion and killed-walk bounds require repair/checking |
| Rare hittability | Lemma 6, pp. 11–12; TeX 837–928 | Separation > n/log n; log^-1 n <= epsilon < 2/3; n <= m <= n exp(4 sqrt(log n)) | Conditional input below; depends on unrepaired Lemma 5 and appendix |
| Finite annular coupling | Lemma 8, pp. 12–14; TeX 939–1057 | m >= 2n; same separation; exceptional one-walk events; Hall matching | Bounded conditional repair proved below |
| Old-prefix hittability | Lemma 9, pp. 14–17; TeX 1060–1204 | Single stopped prefix, uniform over separated future start z | Conditional input below; literal statement/proof need systematic repair |
| Multiscale induction | pp. 17–18; TeX 1207–1278 | Radii 2^(n^2), prefix avoidance, endpoint separation, rare H events | Averaged induction repair proved below, conditional on corrected estimates and initialization |
| Hitting / harmonic measure | A.1, A.10, pp. 18, 21; TeX 1287–1306,1460–1470 | 4D SRW, away from diagonal; start deep inside larger ball | Correct scale and primary assumptions independently checked; inside/outside boundary convention needs explicit translation |

## Literal defects and bounded fixes

These are defects in the literal supplied argument. They do not prove the intended theorem false.

1. **Lemma 8 event polarity.** If both E_i are empty, its literal conclusion requires the empty event with probability tending to 1. Intended E_i are exceptional events and the conclusion must avoid them. In its proof, late exits τ>T must be added to E_i, `A_i'` must exclude E_i, and the removed hittable paths must have intersection probability **greater than**, rather than less than, 1-3µ. The first singleton-degree calculation must count disjointness. TeX 939–990 confirms all these are literal, not extraction artifacts.
2. **Finite normalization.** There are 8^T equally likely T-step 4D words, not 2^T. Every count, threshold and mass must use L=8^T (or a consistently defined equivalent encoding). TeX 973–1054. The missing factors of L in the large-set argument and complement coupling normalization must also be supplied.
3. **Hall proof exclusions and strict thresholds.** The printed degree calculation removes E_i and the endpoint loss but does not explicitly deduct the paths excluded for being hittable. Lemma 6 supplies that deduction after making n large. µ<1/6 is insufficient for epsilon+2µ<2/3 at epsilon=1/2; use µ<1/12, for example µ<1/24. For large B, degree equal to |A_1\B| need not meet B; use a strict greater-than criterion with a margin. The certificate below handles these details.
4. **Singular good-time kernels.** Lemma 5's second condition (p. 9, TeX 751), and Lemma 9's conditions (p. 15, TeX 1089–1090), use |R(t+s)-R(t)|^-2 without regularization. For √n>=2, a two-step return occurs with probability 1/8 in 4D. Its s_1=2,s_2=1 summand is infinite, contradicting the claimed failure probability tending to zero. A candidate repair is (|z|+1)^-2, consistent with Lemmas 3–4 and the hitting kernel. That substitution alone is not a verification of the subsequent distinct-trace count or killed-walk moment estimates.
5. **Lemma 9 finite-time definitions and polarity.** t<=ell-n still allows t+s_1+s_2>ell in condition (2), whose last argument also contains an undefined s (TeX 1085–1090). Near-exit indices need an explicit extension or boundary treatment. Good paths must belong to H^c, not H (TeX 1107 onward), and the final probability should be >=1-C/log²n rather than >=C/log²n (TeX 1202). Annular radii `2^n-i^i`, expectation symbols inside random Markov bounds, and the stated implication from bad paths to the extended bad set need consistent definitions (pp. 16–17).
6. **Lemma 9 logarithm parentheses.** The literal statement (TeX 1069–1071) has log(n log³n)/k; its derived bound and final use require log((n log³n)/k). These yield radically different thresholds. The intended corrected H event must be stated before using its complement as a prefix protection condition.
7. **False literal spatial logarithm in A.3.** It assumes spatial radius n>|x| but bounds the nonnegative expectation by C log(n/|x|²) (p. 18, TeX 1310–1315). x=(10,0,0,0), n=20 makes that bound negative, while the second walk follows a geodesic to x with probability 8^-10>0 and R_1 includes x at time zero. A spatial bound such as C[1+log(n/(|x|+1))] follows by regularized Green-kernel convolution, with suitable ball geometry. This is a genuine false literal statement, not a refutation of a logarithmic estimate with corrected variables.
8. **Other appendix convention defects.** A.2 equates distinct trace intersections to a sum over time pairs; the latter counts temporal multiplicity. A.6's displayed optional-stopping algebra uses Aα and aα where the stated limit requires A^-2α and a^-2α. A.9 allows a negative right side for some of its stated start/radius cases; use a nonnegative logarithm or restrict to the actual large annular ratio. A.10 calls an outside exit point an inner-boundary point. These must be reconciled if supplying a full proof certificate. Moment-tree Lemma 2 likewise needs its root at R_0(0), and an explicit stopped-to-unrestricted upper-bound argument before applying its infinite-walk hitting lemma.
9. **Final induction polarity and conditioning.** The p. 17 E_i event must mean hitting the other prefix, rather than avoiding it; its probability is bounded **above**, not below. The initial endpoint exception is small separation, not separation at least the threshold. `Cn_1^6` must be `C/n_1^6`. More substantially, Lemma 9's unconditional rare-H probability is not a uniform conditional bound given an arbitrary fixed joint prefix. Averaging, as below, repairs that step without assuming such a bound.

## Conditional Hall certificate (own checkable repair)

The endpoint loss used here has a direct primary-backed repair. Lawler–Limic Lemma 6.3.7 and Theorem 6.3.9 give outside-exit mass <=Cm^-3 for a 4D SRW started in B(m/2). For the first inner-boundary hit u, choose an outside neighbour w; the next step has probability 1/8 to exit at w, so the first-hit mass at u is <=8 times the outside-exit mass at w. A boundary cap of Euclidean radius m/log m has <=C(m/log m+1)^3 lattice vertices: split into the finitely many regions where one coordinate has magnitude >=m/3 for sufficiently large m, project to the other three coordinates, and note that the shell of bounded width permits only a bounded number of choices in the remaining coordinate. Consequently the close-endpoint loss is <=C/log³m. This explicitly reconciles the preprint's inner-boundary and exit conventions.

The negative literal A.3 logarithm also has a bounded kernel repair, rather than an unsupported replacement: with spatial radius R>|x|=D, distinct-trace expectation is at most the sum over z∈B(R) of C/[(1+|z|)^2(1+|z-x|)^2]. The regions |z|<=D/2 and |z-x|<=D/2 each contribute O(1) by the four-dimensional volume estimate. The remaining region with |z|<=2D contributes O(1), and each dyadic shell beyond 2D contributes O(1). Thus the sum is <=C[1+log(1+R/(D+1))]. For the separated annular use D>=n/log n and R<=Cm, this is <=C log(m log n/n) once n is large. This proves the corrected spatial convolution bound needed there. It does not justify replacing temporal counts by distinct traces elsewhere.

Assume the corrected rare-hittability estimate of Lemma 6 in both directions, and an endpoint-nearness loss b<=C/log³m. Give each T-step word mass 1/L, L=8^T. Let E_i include the late-exit exception, p_i=P(E_i), and µ=p_1+p_2+1/log n. We can assume µ<1/24; otherwise a sufficiently enlarged error constant makes the desired success bound vacuous. Define

    A_i = {word: E_i fails and its stopped trace has
           independent intersection probability <= 1-3µ}.

Lemma 6 directly gives a removed hittability mass h_i<=K(3µ)/log^(1/4)n. For n large, arrange h_i<=µ/4 and b<=µ/4. Therefore |A_i|>=L(1-Cµ). The edges between A_1 and A_2 require disjoint stopped traces and separated exit endpoints. Every γ∈A_i has degree in the opposite A at least

    L[3µ-p_(3-i)-h_(3-i)-b] > µL.

Assume |A_1|<=|A_2|. For B⊂A_1:

- If |B|<=µL, one γ∈B has degree>|B| (the empty case is trivial).
- If µL<|B|<=L/2, put epsilon=|B|/L. Having degree <epsilon L implies its independent disjointness probability is <epsilon+2µ. The two-direction hittability estimate bounds the number of such γ by K(epsilon+2µ)L/log^(1/4)n <epsilon L. Thus B contains a γ with degree >=|B| and Hall holds.
- If |B|>L/2, put r=|A_1|-|B|. For r<=µL every opposite vertex has degree>r and thus meets B. Otherwise epsilon=r/L is in (µ,1/2). Degree <=r in the opposite side implies independent disjointness probability <epsilon+2µ, with the strict margin provided by p_1+h_1+b<2µ. Fewer than epsilon L opposite vertices have degree <=r. All others meet B, giving |N(B)|>=|A_2|-epsilon L>=|B|.

Hall matches all of A_1. Complete this injection to a permutation of all L labeled words. The uniform permutation coupling has both exact full T-step marginal laws and good mass |A_1|/L>=1-Cµ. Extend tails with independent uniform increments and then stop at exit. Stopped finite paths form a countable discrete space, and their prescribed marginal laws are tight because exit is almost surely finite. The joint couplings are uniformly tight by those marginals; a subsequence converges pointwise and hence in total variation. Thus every stopped-path event, including arbitrary E_i, passes to the limit. Late-exit marginal mass tends to zero as T→∞. This gives the intended annular coupling, **conditional on the quantitative profile estimate**, and repairs normalization, exclusions, complements and strict-threshold issues without importing a 3D assertion.

## Conditional averaged-induction certificate (own checkable repair)

Assume a corrected Lemma 9 with H_{r,r/log r}, probability <=C/log²r, and the corrected annular certificate. Let r_n=2^(n²), and let G_n denote success of all prefix requirements through stage n. Its mass is p_n. From a successful joint prefix, the probability that continuation i hits the other old prefix is bounded pointwise by q_n<=C(log n)²/n² using H_old^c and endpoint separation. The annular range is valid:

    2r_n <= r_(n+1) = r_n 2^(2n+1)
         <= r_n exp(4 sqrt(log_2 r_n)).

The new H event depends on the entire continued prefix. Denote its conditional probability given the joint old prefix by h_i. It is not valid to claim h_i<=C/n^4 for each prefix. Instead, the retained full SRW marginal and the tower property give

    E[1_(G_n) h_i] <= P(H_new for marginal i) <= C/(n+1)^4.

Apply the annular coupling to each eligible prefix with bad event “hits the other prefix OR H_new.” On failed prefixes use any coupling with the correct SRW continuation marginals. Countably many finite prefixes allow these choices without a measurable-selection obstacle. Averaging gives

    p_(n+1) >= p_n(1-C(log n)²/n²) - C/(n+1)^4.

If initialization supplies p_(n_1)>=c_x/n_1, the product of the multiplicative factors is >=1/2 for n_1 sufficiently large, and the total additive loss is O(n_1^-3). Consequently inf_n p_n>=c_x/(2n_1)-O(n_1^-3)>0. This is the missing averaged justification. It depends on corrected Lemma 9 and a verified initialization lower bound for the desired fixed x; neither is silently assumed proved by this certificate. The concatenation preserves complete marginal SRW laws, including time zero. The within-annulus matching can use future paths and the joint coupling is not thereby proved Markovian or co-adapted.

## Required qualification and remaining verification gap

Accept the attribution **“Benjamini–Kozma v1 states the intended 4D full-trace result; this package does not certify its complete proof.”** Retain that qualification wherever the attribution is promoted. Do not convert the conditional certificates above into a new theorem claim. The exact unverified quantitative boundary is a systematically defined and proved rare-hittability Lemma 6 (including good-time/distinct-trace/killed-walk bounds and corrected appendix hypotheses), a corrected uniform old-prefix Lemma 9 (including near-exit definitions), and the arbitrary-fixed-x initialization estimate. No 3D uniform lower bound or universal impossibility result is supplied.
