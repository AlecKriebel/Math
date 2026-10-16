# PR173 / 30003677 / OWR-15962-003: independent priority and source-lineage audit

Audit family: source and citation lineage. This family used only the authorized repaired candidate and original source record as its initial local scientific inputs. It did not read ROOT material, other-family work, original readiness/review conclusions, or previous package verdicts. The supplied original head `eb68ee2ecda39a8ec2748796d716c7a7598b7bc6` is a task identifier; this audit does not independently authenticate a GitHub head or claim that its repaired candidate is the original-head blob. The exact consumed candidate is SHA256 `abe51c0360499d3dbd3da392bad37650b10e29a843654dd7e76260ab69c06c7e`, 17,713 bytes. The first substantive comparison was sealed before findings were sent to the parent; its external identity is recorded below.

## Finding and promotion criterion

The complete primary problem does permit growing initial populations and degree-based initial choices. The candidate is a legitimate affirmative result in that broad existential regime if its mathematical proof is accepted. It does not settle a fixed number of strategically selected hubs, any prescribed seed budget, or sharp rate/degree thresholds.

The generic phenomenon that a sufficiently large sublinear weak population defeats a fixed stronger competitor predates the candidate. ADMP gives a precise regular-graph theorem for that phenomenon. Its literal theorem does **not** imply all the candidate's simultaneous requirements. However, the candidate's much weaker, arbitrarily slow existence schedules are a transparent consequence of established finite-time local-exploration machinery: the marked-ray reduction given below uses the mechanism explicitly proved in ADJ Section 2 plus elementary tail estimates and diagonalization. Under this task's criterion that rigorous transparent corollaries count against novelty, I would **not promote this exact existence statement as a substantial new research contribution without a materially stronger result or a defensible explanation of what exceeds that corollary**.

This is not a claim to have located a published sentence identical to the candidate. No exact earlier theorem with the entire tuple was found. Historical priority remains **unestablished**, both because bounded searches cannot prove novelty and because the primary body of ADJ's cited Cooper--Elsässer--Ogierman--Radzik preprint could not be located. The candidate itself correctly states that historical priority is unestablished; this audit supplies a concrete mathematical reason for caution rather than treating its cautious wording as a false claim.

## Primary problem and citation corrections

The retrieved [OWR primary report](https://ems.press/content/serial-article-files/46721) is Report No. 57/2017, DOI 10.4171/OWR/2017/57, for the meeting on 10--16 December 2017. The complete Deijfen contribution occupies printed p.3442 and its two references at the start of p.3443, PDF pp.16--17. Its joint-work attribution includes Ahlberg, van der Hofstad and Janson. It describes iid degrees, uniform pairing, permanent infection types, and per-edge infection intensities. Its final paragraph puts growing seed numbers and degree-based choices together before asking about a weak infection from high-degree starts against a small-degree start. No numerical seed cap is stated there.

The original database record's label “OWR Report 57/2019” is incorrect. “2018” in the report citation is not the workshop/report number; the downloaded PDF was created in December 2018. The problem's 2017 provenance is supported by the report itself. Its abbreviated title for the ADJ paper omits “with finite variance degrees.” These are bibliographic corrections, not changes to the mathematical question. The record's dated “open” status is not accepted as proof of current openness. [ADJ v1](https://arxiv.org/pdf/1711.02902v1), Section 5 p.15, repeats the same further-work question and points to ADMP's growing initial sets.

ADJ is by Ahlberg, Deijfen and Janson; its journal DOI is [10.1002/rsa.20846](https://doi.org/10.1002/rsa.20846). [ADMP](https://arxiv.org/pdf/1109.2575v2) is by Antunović, Dekel, Mossel and Peres, journal DOI [10.1002/rsa.20699](https://doi.org/10.1002/rsa.20699). ADMP v1 was submitted 12 September 2011; v2 was submitted 4 August 2014. **Theorem 2.6 belongs to v2**, which is the complete 49-page primary text deeply read here. The separately obtained v1 has a different numbering and was read pp.1--5. Publisher access returned 403; the version-of-record body was not independently compared with v2. The v2 theorem is already an antecedent regardless of later journal wording.

## Exact target reconstructed

The target is a configuration multigraph with an iid integer degree law satisfying D≥2, unbounded support and E[D²]<∞, plus the stated single-degree parity repair. Every supported fixed d0 and every fixed 0<λ1<λ2 are allowed. There must exist deterministic kn→∞ and tn→∞ with tn/log n→0. Type 1 initially occupies exactly all vertices of repaired degree at least kn; selection precedes matching and weights. Type 2 starts from an independent uniform member of the degree-d0 class. The seed count must diverge while both its vertex fraction and its fraction of all incident stubs vanish. By tn, the type-1 fraction must tend to one in probability.

Unbounded support supplies positive probability above every fixed threshold. Minimum degree two supplies an indefinitely continuing nonbacktracking limiting ray. Finite second moment makes size-biased exploration nonexplosive. Fixed d0 makes the competitor's initial local exposure tight. The freedom to choose arbitrarily slow schedules does most of the work: the claim asks for no useful quantitative degree threshold, number of seeds, or time scale as a function of n.

## ADMP theorem-level comparison

Definitions 2.1--2.3 and the preamble to Theorems 2.4--2.7 require a fixed d≥3 regular graph and admissible initial sets: uniform disjoint sets, or a set grown from a small uniform center followed by uniform opponent placement. Theorem 2.4 handles both populations growing; Theorem 2.5 handles both fixed; Theorem 2.6 handles a fixed B0 and R0=m(N)→∞ with m(N)/N→0. They concern final sizes.

Put β=λ2, ρ=λ1, B0=1, and call R the initially numerous weak infection. Write r=ρ/β∈(0,1). The two strict asymptotic regimes in Theorem 2.6 are:

| Seed regime | Prior consequence | Comparison |
|---|---|---|
| m(N)≪N^(1−r) | The weak final population has scale m(N)N^r=o(N). | A diverging sublinear population is not automatically enough at a specified scale. |
| m(N)≫N^(1−r) | The fast final population has scale (N/m(N))^(1/r)=o(N). | The weak infection occupies N−oP(N). |
| m(N) comparable to N^(1−r) | The displayed strict regimes do not alone give the above all-but-vanishing conclusion. | Do not silently use a boundary formula outside its conditions. |

These are deductions from the theorem with the colors and rates assigned as above. For example m(N)=N^a, 1−r<a<1, already has diverging count and vanishing vertex/stub fractions and beats any fixed rate disadvantage on a fixed regular graph. The algebra is checked with exact rational arithmetic in the standalone controls. Reversing the color assignment would give the wrong threshold.

The proof chain is important. Theorem 2.6 restarts at the stopping time of Lemma 4.13. Corollary 4.14 and diagonal urn growth give the Gamma limit for the small population relative to the large one. Theorem 3.1 then converts active-stub proportions to final vertex sizes. The transition table in Section 3 has fixed jumps d−2, −2 and −d; Lemma 4.5 and Theorem 4.6 use a fixed replacement matrix; Section 5 estimates a corrected ratio involving Xn and Yn and the fixed-d depletion curve. Constants and Taylor bounds depend on d. This is not a hidden variable-degree theorem.

| Candidate requirement | Literal ADMP coverage |
|---|---|
| Any fixed speed disadvantage | Yes. |
| Diverging weak count, vanishing vertex and stub fractions | Yes, for appropriate admissible regular-graph populations. |
| Bounded-degree strong root | Yes, all degrees equal fixed d. |
| Fixed unbounded finite-second-moment degree law | No: constant d. |
| Seeds selected solely by a diverging degree threshold | No: all degrees are d, so this set is eventually empty. |
| Deterministic sublogarithmic time of near-total occupation | No: a final-size statement and primarily discrete pairing analysis. |

Replacing d by d(N), replacing m(N) with total seed stubs, or treating degree-threshold sets as uniform regular-graph seeds does not satisfy the literal hypotheses. Generalizing the urn proof would require a new degree-dependent transition and depletion analysis. That route is **blocked as an automatic transfer**, not reopened merely because the physical phenomenon is similar.

## ADJ: literal theorem versus transparent reduction

ADJ Theorem 1.1 assumes convergence of empirical degrees with uniformly integrable squared degrees and minimum degree two with P(D>2)>0. Its infections initially start from two uniform vertices. The fixed-finite-start remark must not be read as a uniform theorem for roots whose degrees diverge: Section 2's proof conditions on fixed initial stub counts and its fixed-time tightness depends on that condition. The theorem's unequal-rate conclusion that the weak fraction vanishes is not a contradiction to the candidate's growing seed set.

ADJ Section 2, pp.6--7, proves the finite-time exposure mechanism needed here directly. Size-biased offspring converge, their finite mean prevents explosion, and replacement sampling differs from the uniform pairing exploration only with vanishing probability on a fixed time interval. Its Proposition 2.1 treats the proportions from fixed starts; the following reduction uses the underlying finite-exposure argument, rather than substituting growing starts into that proposition.

### Standalone reduction certificate

1. Fix k>d0, R and T before taking n→∞. Expose a nonbacktracking ray of R edges from an independent uniform test vertex U, and the unopposed λ2 first-passage ball through T from the independently chosen degree-d0 root W. The limiting ray's subsequent degrees are independent copies of D*, with P(D*=d)=dP(D=d)/E[D]. Its continuation is guaranteed by D*−1≥1.

2. The fixed-time fast tree has finitely many birth events almost surely. One elementary nonexplosion proof starts with d0 active edges and writes ν=E[D*−1]<∞. The expected number of generation-r birth events by T is bounded by d0 ν^(r−1)(λ2T)^r/r!. Summing over r is finite, so Tonelli excludes infinitely many events before T. Each reached degree is finite almost surely. The fixed ray, current frontier targets and all their incident stubs also form a finite exposure almost surely. This enlarged count avoids assuming a third moment or omitting boundary collisions.

3. Cut off both limiting exposures at a total of M incident stubs. Choose M so that exceeding it has probability below ε. Under empirical first-moment convergence, the empirical size-biased law converges in total variation to D*. Until M stubs have been exposed, uniform pairing and independent size-biased sampling differ by a vanishing error; collision/intersection probabilities are O(M²/n). The degree-d0 class has positive limiting density, so selecting W from that class changes the bounded-exposure collision estimate only by a constant. Let n→∞ for fixed M and then ε→0. This is the finite-exposure modification of ADJ's argument needed for the extra auxiliary ray. It requires no growing-time approximation.

4. Set p=P(D*≥k)>0. The ray misses all initial seeds in its first R non-root vertices with probability (1−p)^R. Its independent type-1 edge costs sum to a Gamma variable G_R of mean R/λ1; hence P(G_R>T)≤R/(λ1T). The limiting finite exposures are disjoint. Reverse the ray segment from its first marked vertex to U. Every vertex on it avoids the entire unopposed fast ball through T. Any actual type-2 vertex by T belongs to that unopposed ball, by following infection ancestors. Induction along the path therefore infects U with type 1 by T. This uses path protection, not a false two-distance Voronoi equivalence. Consequently

   limsup P(U is not type 1 by T) ≤ (1−p)^R + R/(λ1T).

5. For j≥2 choose K_j=d0+j, p_j=P(D*≥K_j), q_j=P(D≥K_j), R_j≥j²/p_j, and increasing T_j≥j²R_j/λ1, T_j≥j. The preceding bound is at most 2/j². Choose deterministic increasing N_j so that for every n≥N_j the actual failure is at most 3/j², N_j q_j≥4j², and log N_j≥jT_j. Define J(n)=max{j:N_j≤n}, kn=K_J(n), tn=T_J(n). Then all schedules diverge and tn/log n≤1/J(n)→0. The uniform-test-vertex identity bounds the expected missing fraction by 3/J(n)²; Markov gives convergence in probability.

6. The pre-repair seed count is binomial with mean n q_J(n)≥4J(n)² and variance at most its mean, so it diverges in probability. Its expected vertex fraction is q_J(n)→0. Its expected stub mass divided by n is E[D 1(D≥kn)]→0 by integrability, while the total stubs are at least 2n. The single upward parity repair changes the relevant expected normalized mass by O(1/n), including a possible threshold crossing. Thus it does not disturb either vanishing mass or diverging count. The conditioned root exists with probability tending to one.

This recovers the exact combination being audited. Steps 1--3 are established local exploration with a bounded auxiliary path and a positive-density root conditioning; steps 4--6 are elementary marking, path protection and diagonal estimates. Their deductions are explicit rather than an unsupported demand for a stronger theorem. This is the substantive transparent-corollary objection; it is stronger evidence against substantial novelty than any unsuccessful search.

The same argument works for independent Bernoulli seed marks of any fixed positive density, then for sufficiently slowly vanishing densities by another diagonal construction. That observation is an independent inference, not a claimed literature theorem. It shows that diverging degree is used to make the marks qualifying high-degree starts, rather than to demonstrate a quantitatively strategic degree advantage. A fixed number of hubs does not result from this argument: its diagonal construction deliberately enforces diverging seed count.

### Boundary checks and exact limits of the reduction

Bounded degree support makes a diverging threshold eventually empty. Degree-one leaves can terminate the selected ray and finite components prevent a near-total occupation conclusion without additional hypotheses. Infinite-variance exploration can explode, destroying the finite-time fast-ball separation argument. Rates depending on n are outside the fixed-rate argument. A competitor chosen after inspecting matching or edge weights need not behave like an independent bounded-degree root. A specified polynomial budget is not obtained by choosing N_j arbitrarily large. These are real boundaries, not claims that those other problems have been settled.

## Direct citation and citing extensions

The complete primary bodies were downloaded where available, but only the relevant models/theorem pages of the following extensions were read; their exact limits are in SOURCE_ACCESS_LEDGER.json. Model mismatch is sufficient to reject literal application; it is not a claim to have verified all their proofs.

| Primary source and locus | Exact comparison |
|---|---|
| [Antunović, arXiv:1408.0559](https://arxiv.org/pdf/1408.0559), pp.1--3, Theorem 1.1 | ADMP's cited depletion estimate has a fixed (a,b) urn, specializing to fixed d regular graphs. Its general urn parameters do not make the offspring or degrees random. |
| [Deijfen--van der Hofstad, 2016](https://doi.org/10.1214/15-AAP1151), Theorems 1.1 and 1.2 | Power-law exponent τ∈(2,3), hence infinite variance. Multiple starting points are fixed before n→∞; a subsequent large-k limit is not the candidate's finite-variance threshold theorem. |
| [Baroni--van der Hofstad--Komjáthy, arXiv:1408.0475](https://arxiv.org/pdf/1408.0475), Theorem 1.2 | Infinite variance, single uniform sources and deterministic unequal passage times. The speed-versus-neighborhood exponent is not an exponential finite-variance growing-seed theorem. |
| [van der Hofstad--Komjáthy, arXiv:1503.09046](https://arxiv.org/pdf/1503.09046), Theorems 1.2 and 1.5 | Infinite variance and equal deterministic speeds; coexistence depends on local growth variables and an explicit technical absolute-continuity assumption. Cannot be rebranded as any-fixed-rate weak victory. |
| [Antunović--Mossel--Rácz, arXiv:1307.2893](https://arxiv.org/pdf/1307.2893), Section 1.1 and Theorems 1.1--1.5 | The graph grows by preferential attachment; a new vertex adopts its type at birth based on existing neighbor types. This is not infection of a pre-existing uniformly paired graph. ADJ's informal description of this as competition on preferential attachment should not obscure the model difference. |
| [Deijfen--van der Hofstad--Sfragara, arXiv:2204.04125](https://arxiv.org/pdf/2204.04125), Theorem 1.1 | Infinite mean, τ∈(1,2), uniform finite starts. The model's giant-degree structure differs from finite second moment. |
| [van der Hofstad, arXiv:2307.09911](https://arxiv.org/pdf/2307.09911), Theorem 1.1 and Remark 1.2 | A directly indexed citing extension requires infinite variance and at least one explosive passage distribution. The candidate's finite-mean size-biased exponential growth is nonexplosive. |
| [Karrer--Newman, arXiv:1105.3424](https://arxiv.org/pdf/1105.3424), model pp.1--2 | Reed--Frost SIR with recovery after one time step and transmissibility. Its coexistence phase cannot be substituted for permanent exponential nearest-neighbor infection. |
| [van Santvoort thesis](https://pure.tue.nl/ws/portalfiles/portal/197525945/Santvoort_Mike.pdf), model/abstract and bibliography | Stochastic SIR on metapopulations, not the target competing SI process. A search snippet was misleading because its bibliography misnames ADMP as a finite-variance-degree paper. No theorem match was inferred from that label. |
| Cooper--Elsässer--Ogierman--Radzik, cited ADJ reference 10 | **Unresolved access gap.** No primary body located after exact-title and author searches. ADJ characterizes it as a different constant-time process; that summary is not an independent theorem-level exclusion. |

OpenAlex's returned citation sets contained only two ADJ citing records and ten ADMP citing records. Both were completely scanned as discovery metadata, then relevant primary papers were inspected. This index is not complete and does not contain every known citation. Search snippets' crawl or “published” dates were not taken as paper publication dates. Unrelated SIS, dormant-seed hostile-environment, random-walk-location and general influence-ranking hits were not used as proof evidence; no title-based novelty exclusion is claimed.

## Authentication, reading limits and remaining uncertainty

The first seal was created at 2026-10-12T14:42:26.723679Z after actual mathematical comparison. FIRST_SEAL.json: 6,192 bytes, SHA256 `655a17cfec66d36384307fea485afa352967ede6e5439a61ebe3ed2581caf211`. FIRST_SUBSTANTIVE_ASSESSMENT.md SHA256 `cc95e79e2414c205ae0f677f2b3d1682e7ad04d409dd2cccc0303a05548098fd`. It includes every then-retained own file and all consumed scientific-source identities; all were set to mode0444. Later findings are additive.

The final seal inventories **every retained own file recursively**, including private bodies, raw headers, extracts, renders, private API data, own code, clean ledgers, reports and receipts. Its self-hash is delivered externally to avoid a cycle. The explicit PUBLIC_ALLOWLIST.json is the only release list. A file's presence under this family folder is not permission to publish it. All primary-source bodies and private source artifacts are excluded from that allowlist.

The standalone audit_controls.py runs ordinary and optimized Python checks. Negative controls reject an omitted retained source, same-size source corruption, writeable retained file, unsafe external path, and a private source added to the public list; these are real executions with receipts. Exact rational checks reject the misleading reversal of ADMP's winning/losing regime. These controls authenticate evidence and elementary algebra; they do not computationally prove the stochastic theorem.

Family completion estimate at the final checkpoint: **90% toward a complete priority determination**. The requested primary OWR contribution, complete ADJ v1, and complete ADMP v2 have been read; direct relevant extensions and a rigorous local-corollary reduction have been checked. The remaining 10% is not a missing algebra calculation: it is historical coverage, the inaccessible cited preprint, and unverified journal-version changes. Absolute novelty cannot be certified from this finite audit. No external outreach, outreach draft, Git/index/ref/checkout mutation, PR action, upload or publication occurred.
