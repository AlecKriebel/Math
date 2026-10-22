# Frozen independent mathematical audit

Review: note_math_review_01, PR885 / PID9700042. Captured 2026-10-16 04:28:36 UTC after the independent assessment was frozen and sent to the parent. Completion estimate: **100% of this assigned note-level proof audit**. This is validation, not additional central proof search; the original immutable 5/5 effort is unchanged.

**Decision: no blocking mathematical defect found in the operative note.** Its exact Aldous-Lenderman asymptotic follows from the stated BGT strict-site scaling input and the numerical weighted-list majorant after the note's directed-model comparison. This is not whole-package clearance, a novelty finding, a status-of-literature finding, a default replay/build receipt, or human peer review.

## Independence and source identity

First read canonical_pair.json completely, then the exact Aldous model HTML completely, then note.tex completely. Only afterwards consulted the operative BGT primary and its extracted text. Did not read other agent verdicts, parent dispositions, or older proof files under source. No other PR was inspected, no Git invoked, and no outside individuals or project chats contacted.

Verified SHA256 values:

* canonical_pair.json: fef71ca1603c57d1335d95fdd80a4e3d8dad6e0ed454e92fd60b3945e229ca06
* note.tex: 493e7b3756487bd47c2eb0f804e5bf253082b63e86f54c661c0ffbf40b7d39ea
* BGT_2106.12266_root.pdf: 9d78c8dd86aaa62dbaa7bfcaf40195c901c3cc9dee025bffd4a6e29af64339ba

Read relevant BGT sections 2.2-2.5 and 3.1-3.4; inspected existing page images 16, 23 and 24; directly extracted actual PDF pages 23-24, 9-12 and 25 to stdout. In particular, the negative-part quantity in (19), Lemma 19 and (33) is the **sum of individual negative increments**, as used by the note. No source body is copied into this review folder.

## Exact model and finite reduction

The note's source set is exactly the left/bottom boundary excluding the northwest and southeast corner sinks. The sink set is the top/right boundary. Sources and sinks are disjoint, so no zero-edge path convention intrudes. Shared vertices are permitted, as Aldous requires.

For N=n-2, the only boundary label changes for any feasible cut are e_L and e_B. The directed interface with source side on its physical right has balanced indegree/outdegree at each bounded face, including the degree-four checkerboard case. Its two exterior endpoints have balances +1 and -1. Reachability therefore supplies a directed route between them. Loop erasure leaves a simple route; forward dual crossings are outward primal cut edges, reverse crossings are inward and cost zero. Nonnegative capacities give the lower bound V_n >= c_L+c_B+T_N. Conversely, a simple dual corner path extended through e_L,e_B is a simple crosscut avoiding every primal vertex; its source-side component contains the entire source boundary arc, and its outward crossings have exactly that cost. Hence equality holds for arbitrary finite nonnegative capacities. At n=2, source=(0,0), both outgoing edges end at sinks, and V_2=c_L+c_B exactly.

For any corner walk, forward count minus backward count is 2N. Cost is therefore 2N+b-k and deficit k-b. A cycle has equally many forward and backward steps and k<=forward count, hence nonpositive reward. This validates restriction to simple paths and 0<=D_N<=2N.

Translated consecutive diagonal boxes intersect only at their corner vertex. Concatenating their optimizing paths proves expectation superadditivity; stationarity suffices and no independence between optimal paths is needed. The boundary correction is bounded and N/n tends to one. Thus g(q)=lim E[D_N]/(2N), with the Aldous L1 existence statement identifying the same v. There is no use of Aldous's heuristic complement identity.

## Strict chains and endpoints

The two outgoing edge variables at each site are disjoint from the variables belonging to every other site. The independent site parameter is exactly r=2q-q^2. BGT's site model, rather than its bond score, is the applicable strict-chain model. It allows a weak initial comparison with the origin and strict subsequent comparisons, exactly matching chains in [0,M)^2 that may include an open origin. Lemmas 5, 10 and 13 and the planar identification in section 3.4/page 25 give sigma_r/sqrt(r) -> 2.

For the lower bound, every site in [0,N)^2 has both outgoing edges inside Q_N. Strict coordinate increases leave room to take either marked edge before the next chain site and before the final endpoint. Consequently D_N>=A_r(N).

For the upper bound, set M=N+1 and exclude the actual terminal (N,N) from the path's open-site list. That terminal has no departure and hence cannot account for a marked forward traversal. The artificial terminal (M,M) is strictly above every real visited site and need not be reached by a physical competitor. Extra open boundary sites from extension may enlarge the upper chain score, which is favorable.

Every marked traversal has a distinct starting vertex on a simple path, even when both outgoing edges are marked. Thus k<=p+I_0. Selected internal anchors plus the open origin give A_r(M)>=a-1+I_0, and p=a-1+L yields D_N-A_r(M)<=L-b. The origin cancels without a missing additive constant. The actual terminal's state can only increase A_r(M).

## Local comparison and variation

For any nonlast gap s strictly below t, both outgoing edges from s lie in Q_N and either can initiate a monotone route to t. If s is open, its marked first edge gives competitor cost at most ||t-s||_1-I_s. The actual segment costs ||t-s||_1+b_j-k_j, with k_j<=ell_j+I_s. A cheaper replacement would lower the global walk cost; subsequent loop removal cannot increase cost. Hence b_j<=ell_j. Any coordinate overshoot of the last intervening site beyond t forces at least that many backward steps, proving Item 4, even with ell_j instead of 2(ell_j+1). For the last gap the auxiliary terminal dominates all real sites, so Item 4 holds directly. No competitor leaves the box.

For each gap prefix through its last intervening site, the distinguished coordinate has nonpositive net displacement. Its sampled absolute variation is at most actual variation, at most twice the actual backward variation in that coordinate. In the other coordinate, the sum of individual negative sampled increments is at most actual backward variation. Prefixes are disjoint in path time. Therefore the note's exact X satisfies X<=2b. Replacing the sum of negative parts by the negative part of a sum would be invalid; the note does not do so.

The bad event D_N>A_r(M)+delta*M*sqrt(r) gives L-b>delta*M*sqrt(r), hence -X+2L>2delta*M*sqrt(r). Thus it supplies a list satisfying numerical Item 5 with tau=2delta. All list sites are distinct, nonzero and strictly below the auxiliary terminal; every chosen coordinate exists by the first-subsequent rule.

## Independent numerical-majorant derivation

This check does not equate the directed dual with ordinary FPP. Put s=sqrt(r), beta=2gamma and p=a-1+L. For each list, bound the three numerical predicates using exponential multipliers

    exp[beta*s*(2M-sum_j ||h(j)||_1)],
    exp[gamma*s*sum_j (2(ell_j+1)+h(j)_other-sum_i u(j,i)_other)],
    exp[alpha*(1+2L-X-tau*M*s)].

The harmless factor exp[2(p+1)] may also be inserted; it is at least one and corresponds to the vacuous d2=0 form of Item 2. Recovering sites from anchor and prefix increments is injective before enlarging the summation domain. Sum over enlarged independent integer increment domains. The distinguished h-coordinate contributes at most K(beta*s); the other h-coordinate contributes at most K(gamma*s), since -2gamma*s*|h|+gamma*s*h <= -gamma*s*|h|. The distinguished u-coordinate contributes K(alpha). For the other u-coordinate,

    sum_{u in Z} exp[-gamma*s*u-alpha*(u)_-]
        <= K(gamma*s)+K(alpha-gamma*s),

provided alpha>gamma*s. These give the note's exact B0^a B1^L factors. The direct derivation actually permits prefactor r^-1 exp[alpha]; its written prefactor r^-1 exp[2+alpha] is a harmless enlargement. The exponential M-factor is exp[(2beta-alpha*tau)M*s]. Since B0 -> 4e^2/(beta*gamma) and B1 -> 0, choose gamma large, alpha*tau>2beta+1, then r small. Summing the 2^a coordinate choices and ell-vectors yields sum_{a>=1}[2B0/(1-B1)]^a<=1, exactly as in the note. This establishes the claimed C_tau*r^-1*exp[-M*sqrt(r)] bound uniformly for M>=2.

The BGT displayed estimate uses the barred site parameter in its numerical factors. The note explicitly fixes its predicate to tau*M*sqrt(r); the derivation above checks this normalization directly and avoids any silent identification of epsilon with the barred epsilon.

The m=0 specialization is a specialization of a **positive numerical counting sum**. It does not require that the actual path have no doubly-open sites. Asking that any fixed distinct list of p sites is open has probability r^p, independently of how many outgoing marks each site has. The union bound ignores the origin state and does not condition on a selected geodesic. Thus no missing double-open probability or model-event equivalence is needed.

## Ordered limits and dependency boundary

For each fixed delta>0 and sufficiently small fixed q>0, the tail bound is exponentially small as N tends to infinity. Since 0<=D_N<=2N and A_r>=0, expectation truncation gives

    sigma_r/2 <= g(q) <= sigma_r/2 + delta*sqrt(r)/2.

Only afterwards let q tend to zero, using sigma_r/sqrt(r)->2 and r/(2q)->1, and finally delta tend to zero. No uniform-in-q finite-volume convergence is asserted or needed. This proves the exact target asymptotic.

Remaining mathematical dependencies are explicitly attributed classical inputs: existence/normalization of Aldous's v (with independent expectation-limit existence supplied), BGT strict-chain scaling and the classical planar Poisson constant 2. The numerical list estimate has also been independently rederived above. No central unsupported replacement claim remains. No historical firstness, current openness or novelty conclusion was audited or inferred.

## Actual finite diagnostics and limitations

The two captured checker bodies were first executed entirely in memory in functions.exec while disk writes were prohibited. Their files and stdout receipts were created only after capacity restoration was reported and the parent authorized this dedicated folder. They were **not preregistered**, and no local/default package replay is claimed. No exact clock was sampled for either original execution; receipt.json records honest timestamp bounds.

Finite cut checker enumerated every source-side labeling and every assignment to the edges that can contribute to a cut: primal n=2,3,4 had respectively 4,64,16384 relevant binary assignments and 1,2,16 cuts. All identities matched. Other primal edges connect fixed equal-side boundary labels and cannot contribute, so omitting their irrelevant capacities loses no case in these binary checks.

Path checker enumerated all simple dual corner paths, every forward mark pattern, and all possible added open flags on the nonterminal top/right boundary. At N=1: 16 patterns x4 boundary extensions, 2 simple paths, 88 minimizing-path cases. At N=2: 4096 patterns x16 extensions, 12 simple paths, 176032 minimizing-path cases and 164448 nonlast-segment checks. It checked the lower-chain comparison, both origin-aware counting inequalities and cancellation, local b_j<=ell_j, Item 4 and exact per-increment X<=2b. No failure occurred. The terminal's additional flag is unnecessary for these checks because it has no outgoing traversal and changing it to open only increases the chain score.

These computations supplement the analytic proof; they do not prove the infinite-volume asymptotic. Actual assembled-package verification, two new whole-package reviews, and integration remain outside this note-level decision.
