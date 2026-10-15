# Independent literal-model and source-scope adversarial audit

Audit target: PR173, problem 30003677 / OWR-15962-003; supplied original head `eb68ee2ecda39a8ec2748796d716c7a7598b7bc6`.

**Finding.** The candidate provides a mathematically sufficient affirmative answer to the literal possibility question in the growing-seed regime expressly allowed by the primary sources. Its theorem is qualified: it concerns iid unbounded-support finite-second-moment degrees, a growing but vanishing-density set of degree-selected seeds, arbitrary fixed positive speed disadvantage, and one fixed-degree competitor chosen without inspecting matching or weights. It does not resolve the full strategic-start research program, fixed-hub budgets, optimal schedules, or all finite-variance degree laws. The fixed edge/type exponential-weight model matches the original model exactly. No historic-novelty verdict is made.

## Independence, inputs, and seal

The exact candidate and source record were read first and copied byte-for-byte into private storage. No original `review/`, readiness/verification verdict, ROOT file, or other-agent conclusion was read at any point. All substantive deductions below were made before communicating a verdict. At 2026-10-12T14:18:32.942210Z the first derivation and assessment, all then-retained inputs, extraction/render artifacts, and runtime inventory were sealed 0444. The first manifest hash is `a1301be315cdc989784955d077d47279bcca09f046865987c1a27670803862f9`. Its 28 inventoried files were rehashed after the boundary checks and remain unchanged. The original-head identifier is a supplied provenance claim, not independently checked through Git; no Git commands were run.

Exact initial input SHA256 hashes:

| Input | Bytes | SHA256 |
|---|---:|---|
| CANDIDATE.md | 16137 | `588cc7063ba7e44bddd7fefafac7369d467ad52e70effd304a69d3dca95ba783` |
| source_record.json | 4117 | `e6594fcdc48b70e1eeffabc3a094319d1f02ab66f57e4d9bbb13a48eaeb14cd5` |

## Decisive primary-source facts

The full [Deijfen OWR contribution](https://ems.press/content/serial-article-files/46721) is the body on printed 3442 / PDF 16 and references on printed 3443 / PDF 17. The complete 16-page [ADJ preprint](https://arxiv.org/pdf/1711.02902) was read; its model and assumptions are p.2, the fixed/uniform-start theorem and remarks p.3, the finite-time branching construction Section 2 pp.5-7, and the strategic-seed question Section 5 p.15. Decisive source pages were also visually checked.

Both questions place growing initial sets next to degree-based choices. Neither specifies a fixed count, polynomial budget, or degree-growth scale. Consequently the candidate's growing-seed construction is a permitted literal existential answer. It is not evidence for every stronger interpretation of the question. The candidate is candid about those restrictions.

ADJ p.2 assigns independent Exp(lambda1) and Exp(lambda2) weights to each edge; traversal begins at the infected endpoint and only an uninfected endpoint can change state. The candidate follows that convention. Section 2's active-half-edge clocks are a memoryless exploration representation. Parallel edges are separate channels and loops do not infect new vertices. The abstract's neighbor-rate shorthand does not replace the complete per-edge specification.

[EMS metadata](https://ems.press/journals/owr/articles/15962) establishes report 57/2017, workshop 10-16 December 2017, publication 19 December 2018. The curation's label OWR 57/2019 is incorrect; its use of 2018 as publication year is compatible with 2017 report numbering. [arXiv metadata](https://arxiv.org/abs/1711.02902) establishes v1, 8 November 2017. [Publisher-deposited Crossref metadata](https://api.crossref.org/works/10.1002/rsa.20846) gives journal online 5 March 2019 and print October 2019, RSA 55(3), 545-559. The journal DOI's web open failed; the decisive full preprint and date metadata were successfully retrieved separately.

## Claim and probability quantifiers checked

For any integer-valued unbounded-support law D with P(D>=2)=1 and E[D^2]<infinity, any fixed atom d0, and any fixed 0<lambda1<lambda2<infinity, the construction asserts deterministic thresholds k_n->infinity and times t_n->infinity with t_n=o(log n). Type1 starts at every vertex of actual repaired degree at least k_n; type2 starts at a degree-d0 vertex uniformly within that class, independently of matching and weights. The result is

    |S_n|/n -> 0,  |S_n| -> infinity,
    sum_{v in S_n}d_v / sum_v d_v -> 0,
    N1(n,t_n)/n -> 1,

all in probability over degrees, matching, weights, and the degree-conditioned root. This implies terminal fraction 1-o_P(1), stronger than any fixed positive-fraction success with probability tending to 1. It is not a simultaneous guarantee for every graph/weight realization or a uniform quenched theorem over all degree sequences.

Unbounded support is an additional restriction beyond ADJ(A1)-(A2), deliberately needed for diverging seed degrees. It still yields an existence answer within the finite-variance class. No claim is made that every finite-variance distribution permits diverging seed degrees. The concrete even law P(D=2m)=2^-m is a valid witness.

## Independent mathematical reconstruction

The following is my deduction, not a quotation or an invocation of the candidate's claimed conclusion.

Write mu=E[D], P(D*=d)=dP(D=d)/mu, and nu=E[D*-1]<infinity. A degree-d0 root's unopposed fast infection converges locally to a continuous-time branching tree with d0 active edges, each reproducing at rate lambda2 into D*-1 forward edges. For fixed T its expected active population is

    d0 exp(lambda2(nu-1)t),

and its expected event count through T is

    d0 lambda2 integral_0^T exp(lambda2(nu-1)s) ds < infinity.

These formulas can first be obtained with offspring truncation and then with the finite-mean branching-process limit, preventing circular reliance on nonexplosion. The process has only finitely many events by fixed T almost surely, and each event reveals a finite degree. Thus its total incident-half-edge exposure is a.s. finite.

For any fixed R, a uniform test vertex U admits a nonbacktracking path whose nonroot total degrees are iid D* in the limiting tree. Since minD>=2, a forward half-edge always exists. For fixed k>d0, set p_k=P(D*>=k)>0. The probability no nonroot path vertex has degree at least k is (1-p_k)^R. The path's type1 passage sum G_R has mean R/lambda1, hence P(G_R>T)<=R/(lambda1 T). A marked vertex is a weak seed, and reversing the intervening undirected path gives a weak route to U. Its length and weights are chosen only as a proof witness; the initial seed rule still uses only degrees.

For fixed R,T, couple that path and the fast ball. Given a cutoff M on all incident half-edges exposed in the two limiting explorations, matching queries are size-biased sampling without replacement. Their independent-sampling approximation error and the O(M^2/n) collision probability vanish. The degree-d0 class has positive asymptotic vertex density, so choosing the other root within that class adds only O(M/n) overlap probability. The empirical degree law and first two moments converge for iid samples. A single +1 repair changes the second-moment average by at most (2maxD_i+1)/n=o_P(1), and does not disrupt the law or degree-class density. Let n->infinity at fixed M, then M->infinity. The whole weak path avoids the whole fixed-time unopposed fast ball with probability 1-o(1).

This local comparison is legitimate for static fixed weights: on a tree, each frontier edge first becomes usable from one endpoint, and its independent exponential delay becomes that frontier clock. Irrelevant later attempts between already infected endpoints have no effect. There is no need to identify a two-type winner through two unopposed distance fields.

Define B2(T) by static X2 metric distance from the fast root. Every actual fast infection by T has an ancestor path of X2 sum at most T, hence lies in B2(T). If a weak-seed-to-U path has X1 sum at most T and all its vertices avoid B2(T), induction along the path proves U is weak by T: at each step the target cannot be fast by T; if already weak it is harmless, otherwise the weak traversal infects it by the cumulative path sum. This proves path protection on the actual competing process.

We therefore get the annealed, fixed-parameter bound

    limsup_n P(U not weak by T) <= (1-p_k)^R + R/(lambda1 T).   (*).

No growing parameter is inserted into this fixed-parameter limit. Instead take K_j=d0+j, p_j=P(D*>=K_j), q_j=P(D>=K_j), R_j=ceil(j^2/p_j), and increasing finite T_j>=j^2R_j/lambda1. Then the two terms in(*) are at most1/j^2. Choose increasing deterministic N_j large enough that every n>=N_j has failure probability <=3/j^2 for those fixed parameters, N_jq_j>=4j^2, and logN_j>=jT_j. This choice is possible because p_j,q_j are positive and the limit is fixed-parameter. With J(n)=max{j:N_j<=n}, k_n=K_J and t_n=T_J, one has J,k_n,t_n->infinity and t_n/logn<=1/J->0.

For the realized infection Z_n=1-N1(n,t_n)/n, an independent uniform test vertex gives E[Z_n]=P(U not weak by t_n)<=3/J^2. Markov yields P(Z_n>1/J)<=3/J. This proves the macroscopic claim without any false independence assertion for vertex indicators.

The original seed count is binomial(n,q_J), with at most one extra seed from parity repair. Thus its density has expectation<=q_J+1/n->0, whereas mean >=4J^2 and variance <=mean give a diverging count in probability. The expected original seed degree mass/n is E[D1_{D>=k_n}]->0. If repair crosses threshold, its extra degree contribution is at most D_repair+1, with expected normalized contribution<=(mu+1)/n. Since total degree>=2n, the seed half-edge fraction vanishes. The degree-d0 class remains nonempty with probability tending to 1 and is disjoint from the seed set once k_n>d0. Every arbitrary fallback on the exceptional event is negligible.

This establishes the claimed theorem. It does not transfer the central difficulty to a stronger unsupported logarithmic-time coupling or to a fixed-seed competition theorem.

## Adversarial checks and exact remaining gaps

| Attack or boundary | Finding and mechanism |
|---|---|
| Fixed edge weights versus transmission clocks | Match. Fixed exponential delays and memorylessness give the source's infection-state clock law. Path reversal uses the source's undirected fixed edge weights. |
| Fictitious Voronoi characterization | Rejected as invalid. A checked four-vertex weighted tree has weak unopposed arrival at v=3 and fast=101, but actual v becomes fast at101 because the intermediate vertex becomes fast at1. The candidate's path-protection premise excludes this obstruction. |
| Hidden growing-time coupling | Absent. Every local limit is at fixed k,R,T; only afterward are deterministic cutoffs diagonalized. |
| Unbounded maximum degree during local exposure | Handled by finite random exposure followed by cutoff M. No finite third moment or uniform deterministic degree bound is used. |
| Dependence among infection indicators | Handled by the uniform-test-vertex expectation identity and Markov; no concentration assumption is needed. |
| Seed-selection information | Degree-list-only, before matching and weights. Conditional matching exchangeability even extends the uniform degree-d0 root to any degree-list-only rule selecting a degree-d0 vertex. This is an additional deduction, not a graph-aware extension. |
| Arbitrary fixed speed disadvantage | Covered because any fixed T fast ball remains finite, regardless of finite lambda2/lambda1. Schedules may depend on those rates. |
| Varying rates with n | Not covered; finite-time tightness need not be uniform if lambda2 grows. Route remains outside theorem. |
| Fixed or polynomially constrained hub budget | Not established. The proof relies on diagonal freedom and n q_J growing; recovering a specified budget needs quantitative estimates absent here. |
| Bounded-support or minimum-degree<2 laws | Outside asserted theorem. Bounded support prevents k_n->infinity seeds; degree1 allows path termination, while isolated/finite components can prevent near-total capture. |
| Fast root selected using graph or weights | Not covered; independence/exchangeability used in the two-root exploration then fails. |
| General passage distributions | Not asserted. Source exponential model is the theorem under audit. |
| Marginal strategic benefit from high degree | Not isolated against equal-size uniform seeds. The theorem verifies an allowed construction, not an optimal strategy or causal comparison. |
| Historic priority | Unassessed. ADJ itself notes known growing-initial-set results on regular graphs; no exhaustive novelty search has been conducted here. |

The deterministic-degree-sequence scope of ADJ(A1)-(A2) is broader than the iid candidate. Its fixed/uniform-start Theorem 1.1 does not settle the present degree-selected growing-set claim. Its p.3 fixed-number remark is not used as a theorem for strategically selected degrees diverging with n. No contradiction is inferred from that informal remark.

The exact checks retained privately use rational arithmetic in a fixed-weight event simulation for the four-vertex counterexample, derive ED=4 and ED^2=24 for the concrete law, check its size-biased tail (j+1)/2^j at 99 thresholds, and check 48 diagonal arithmetic cases. They corroborate the finite arithmetic and attack a plausible incorrect shortcut. The stochastic convergence rests on the derivation above, not on simulations.

## Resolution wording and strongest verified result

A defensible resolution statement is: **An affirmative existence answer in the source-permitted growing-seed regime: for every iid unbounded-support degree law with minimum degree 2 and finite second moment and every fixed speed disadvantage, there are degree-only seed thresholds of vanishing vertex and half-edge density that let the weaker infection capture 1-o_P(1) of the graph by deterministic sublogarithmic times, against a fixed-degree strong root selected using degrees only.**

A defensible caveat is: **The construction does not solve the single-hub or fixed-hub threshold problem, give an optimal or prescribed seed budget, cover all finite-variance degree laws, or establish historical novelty.** These limitations should accompany any publication-level claim that problem 30003677 has been answered; claiming an entire strategic-start theory is solved would be inaccurate. The literal unqualified possibility question has no stated fixed-seed quantifier whose omission would invalidate this construction.

## Source access and retained-file controls

The public source-access ledger gives successful complete-body retrievals, hashes, page/range consumption, failed-access information, and external URLs. Complete original PDF/HTML/API bodies, source headers, input copies, extraction text, rendered pixels, code execution outputs, and runtime details remain in `private/`; none is included in the public allowlist. No source was unavailable in a way that leaves the decisive model/question unverified. All external access was read-only; no individual was contacted and no outreach was prepared.

The explicit public allowlist enumerates only the report, clean ledger, own logs and seal notes, first assessment, and hash manifests. The final recursive manifest includes every retained own file except itself; its own digest is delivered separately because a file cannot contain its own noncircular cryptographic hash. All final retained files are sealed 0444. No file outside the assigned folder, Git index/ref/checkout, PR, package, publication state, or release was modified.
