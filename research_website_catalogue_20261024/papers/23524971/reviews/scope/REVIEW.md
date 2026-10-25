# Acquisition and scope review — Zenodo 23524971

Disposition: **SCOPE_COMPLETE; no mathematical verdict and no publication clearance.** This review authenticates and maps the deposited edition, its exact model, attribution and proof interfaces. The separate mathematical reviewers and root must decide correctness and promotion.

## Identity and custody

The exact queue item is row 65, record 23524971, concept/work identity Z-23524970: *All-load stability of a deterministic-first-chunk file-sharing chain*, Alec Kriebel, Zenodo version **1.0**, publication date **2026-10-20**. The six-page manuscript prints “20 October 2026” and “Unrefereed preprint draft”; it does not print a numbered version. Metadata version 1.0 is not an inferred manuscript version.

Both public assets were freshly downloaded from the record's actual API file links and checked against its byte sizes and MD5 checksums. The immutable local custody receipt additionally records SHA-256:

| Asset | Bytes | SHA-256 |
| --- | ---: | --- |
| dfc_stability.pdf | 75,006 | bee5abffcfdb1ce8bc50f706480c81c4a80e8d609bec2a9d99c6aa4e9b805036 |
| dfc_stability_verification.zip | 251,455 | 38664f12e8d2e74fa46b3f11363a071ec100aad62ece713b578293a6593d9a0e |

ZIP CRC, safe relative paths, duplicate names, file types, extracted sizes and extracted hashes were checked. There are 92 regular members. Its `paper.pdf` is byte-identical to the public six-page PDF; there is no extra reader PDF. The doubled extraction prefix is intentional: `sources/published-source/dfc_stability_verification/dfc_stability_verification/`. `sources/reader-pdf-map.json` maps both reader occurrences. The final custody check covers all public assets and all 92 extracted members, including opaque assessment files, without using their contents as mathematical evidence.

## Reading and independence

I read all six current PDF pages, the complete 417-line `main.tex`, the complete original proof in `original/TURN_4.md`, the current `reproduce.py`, and `original/checks/turn4_checks.py`. These suffice to map the stated all-state proof and its computational interface. I inspected the rendering of current pages 1 and 5, the retained NRE Figure 2, and Meyn–Tweedie printed page 529 to disambiguate formulas and source versions. Other original failed/intermediate routes and dedicated historical review bodies were not needed and were not read. `support-map.json` distinguishes inspected support from opaque historical material.

**Incidental historical-status exposure:** while looking for the full original proof, I opened `original/RESULT_ACCEPTED.md`, which turned out to be a historical disposition summary rather than the proof. It states that a historical adversarial review passed and lists old finite-control counts. I then read `TURN_4.md` itself. The summary, current manuscript/record, wrapper, and original proof also contain status or expected-count text. This was disclosed to root immediately and is recorded in `independence.json`. None of those statuses/counts is evidence for this scope disposition. This work is not described as strictly blind. No current sibling review or dedicated historical reviewer verdict body was inspected.

No submitted mathematical program was executed in this scope role. Reading a checker or its expected count is not reproduction. Fresh integrity checks and source/abstract comparisons are acquisition/editorial checks only. Mathematical reproduction belongs to the separately assigned reviews.

## Exact theorem and model

Theorem 1 concerns a countable-state continuous-time Markov chain on **N₀⁴**, from any finite initial state `(a,b,x,y)`. An arriving peer independently chooses each first chunk with probability 1/2, fixes that choice, and leaves immediately after its second download. The two empty waiting-room counts are `a,b`; one-chunk holders are `x,y`. One permanent seed remains. Empty waiting rooms are excluded from the contact denominator **D=x+y+1**.

The six increments and rates are exactly:

| Increment | Rate |
| --- | --- |
| (1,0,0,0) | λ/2 |
| (0,1,0,0) | λ/2 |
| (−1,0,1,0) | a(x+1)/D |
| (0,−1,0,1) | b(y+1)/D |
| (0,0,−1,0) | x(y+1)/D |
| (0,0,0,−1) | y(x+1)/D |

A transition decrementing a zero coordinate has rate zero. The service/contact time scale is fixed by these formulas; no independent service-rate parameter or separate capped seed-upload server is in the theorem. In particular, at `(a,b,0,0)` the seed-mediated first-download rate is `a+b`, which is unbounded over states. “One permanent seed” must not be turned into “one seed of fixed aggregate upload capacity.”

For **every fixed finite real λ>0**, the claim is nonexplosion, irreducibility and positive recurrence, hence a unique stationary probability distribution. Constants may depend arbitrarily on λ. No stationary population moment, finite mean completion time, geometric ergodicity, convergence rate, uniform-in-λ estimate, deterministic path bound, many-chunk extension or different policy is claimed. A random finite initial state with an unbounded distribution is not a promise of a finite unconditional expected hitting time. At λ=0 the zero state is absorbing and the chain is not irreducible on N₀⁴; this boundary is explicitly outside the theorem. Negative rates, seed deletion, nonuniform first choices, empty-visible denominators and infinite initial populations are also outside scope.

“Stable” has the stochastic meaning of irreducibility and positive recurrence. It is not global asymptotic stability of the associated deterministic limit. Existing small-load stability follows from the displayed workload drift for 0<λ<1/2; the claimed addition is extension to every positive λ, including λ=1/2 and larger loads.

## Proof and support interfaces to be independently checked

1. The workload `W=2a+2b+x+y` and signed cohort imbalance `Z=a+x−b−y` have the two generator identities in (3). First downloads preserve Z. A rounded absolute value has a global Lipschitz derivative, including its joining points.
2. For each fixed λ the paper chooses finite constants and a reflected finite birth–death chain with geometric weights. A finite Poisson solution is nonnegative/decreasing, is zero from R onward, satisfies the terminal equation at R, and has zero successor increments at R+1. This is an explicitly constructed finite auxiliary object, not a stationary averaging assumption for the original chain.
3. A single global `V=W+c h_m(Z)+f(b/D)g(y)+f(a/D)g(x)` is coercive. The exact product identity evaluates the second factor after the jump. First-download cutoff errors have the favorable sign even with unbounded empty waiting rooms. Arrival/departure errors are bounded pointwise. The D=1 case has no departures; both cutoff endpoints and the whole linear ramp are included.
4. The three regions cover both large holder counts, one large/one bounded holder count (and its symmetric case), and bounded visible population with unbounded empty waiting rooms. The paper derives `LV≤−1` outside a finite F without switching among unaccounted functions.
5. Section 5 explicitly supplies nonexplosion, finite-path irreducibility, localized Dynkin, Fatou/monotone limits, and a finite-mean regeneration construction. Its linear bound on V and Poisson arrival bound control the finite-time expectations needed for the repeated-trial step. Correctness of these all-state arguments is a mathematical gate; finite examples cannot substitute for it.

The original `TURN_4.md` develops the same certificate. The published Section 5 expands its finite-set recurrence step into a concrete trial/regeneration argument. The rational checker implements selected loads, finite boundary/ramp/large-empty states and exact identities. `reproduce.py` also orchestrates other historical mathematical programs, output comparison, a finite-horizon simulation and a deliberately rejected protocol-identity control. Those are useful replay entry points, not universal all-real-λ or all-state proofs, nor proof-assistant certification. Its Python≥3.11/no-optimization requirements and temporary-copy behavior are explicit. This scope review does not import any historical “PASS” result from them.

## Primary bodies and attribution

**Norros, Reittu and Eirola, arXiv:0910.5577v1 (2009).** Fresh PDF acquired. Section 3.2, Figure 2, Proposition 3.3 and Conjecture 3.4 were read. Figure 2 gives the same six-rate model and D=x+y+1. The conjecture in this version is high-load *instability*. It must not be quoted as the later positive-stability conjecture. The primary displayed ODE and its divergent open set supply background, not a stochastic-recurrence implication.

**Norros, OWR 48/2010, printed pp.2782–2783.** Fresh 68-page publisher report acquired; the complete two-page Norros contribution was read. It describes the two-chunk permanent-seed setting and states the deterministic-first-chunk stochastic-stability conjecture despite unstable large-system dynamics. The surrounding introduction frames the goal as any input rate. This is directly checked evidence for the historical question; it does not certify its status in 2026. Its different Enforced Friedman question must remain separate.

**NRE January 5, 2011 author proof, HAL 00781341.** Fresh public HAL endpoints returned non-PDF responses; the Springer content URL also returned HTML. A retained raw primary PDF was copied without adjacent review material. Its HAL cover identifies hal-00781341v1, and the manuscript headers read `QUES9209_source.tex; 5/01/2011; 11:31`. I independently read the opening model context, Section 2 stability definitions and all of Section 3.2 (printed pp.10–12, PDF pp.11–13). Figure 2 and the explicit invisible-waiting-room paragraph match the manuscript model. Conjecture 3.6 states stability. This is a checked retained author-proof body, **not newly downloaded/authenticated final-publisher bytes**. Its abstract/bibliographic cover alone does not establish final-edition identity.

**Meyn and Tweedie, Stability of Markovian processes III (1993), pp.518–548.** Fresh author-hosted scan of the published article acquired. Read §§1.2–1.3 (right-process/nonexplosion, stopped extended-generator domain, Dynkin) and the full §4.1 statement/proof interface through Theorem 4.3. Theorem 4.2 requires a nonexplosive right process, drift condition CD2 for truncated generators, a closed petite C, and V bounded on C. In the present discrete locally finite setting finite sets and positive finite paths supply the relevant finite-set smallness; finite-valued stopped V belongs to the local generator domain. With f≡1 this yields recurrence, not a stationary population moment. The manuscript also gives its own localized hitting-time/regeneration derivation, so it does not merely cite a criterion while assuming a stationary law. No exponential-ergodicity criterion is imported.

**Oguz, Anantharam and Norros, Allerton 2012, pp.915–919.** Fresh CiteSeer PDF requests failed (429/403); search exposed publisher-style primary first-page text. A retained raw five-page primary conference PDF was copied and read completely, including §§II–IV, Theorems 3.3/4.3, the m-sampling extension and the closing conjecture. The model samples up to three peers from the *entire* population with replacement, includes self-sampling, and protects departures by requiring repeated observations of the chunks a departing peer already owns. It is not the DFC generator. Its rare-chunk conjecture concerns that other algorithm. The 7/8 versus 1/2 example in the current manuscript follows the two definitions, and arrival rates already fixed at λ preclude identifying both chains by a state-dependent clock change. This source provides a comparison, not a load-bearing DFC stability theorem. The retained copy has not been newly authenticated against publisher bytes.

The freshly acquired Berkeley UCB/EECS-2012-6 technical report is a distinct longer work. Only its title/front matter was inspected; it is **not** silently substituted for the conference paper, nor listed as fully read. No final 2011 publisher body or final 2015 journal extension was acquired/read. No comprehensive worldwide-priority, current-openness or exclusion-of-all-later-results claim is made. Primary receipts list successful acquisitions, failures and retained copies separately.

## Conditional publication content

`content.json` contains the complete original abstract, preserved against actual `main.tex`, and a conditional explanatory candidate. It uses the exact DFC name, state/rate restrictions, all-fixed-positive-λ quantifier, stochastic meaning of stability and explicit limits. It credits the original model/conjecture and classical Foster–Lyapunov tools, labels the work unrefereed and extensively AI-assisted, offers substantive collaboration without outreach, and links the exact main PDF plus ZIP. It does not replay dated audit steps or old test counts. The follow-up is null: this scope work has not justified an unusually strong, paper-worthy new question.

The candidate is not permission to publish and no page, promotion file, spreadsheet, redirect, Git state or remote service was changed. Final `verdict.json` binds all source hashes, report/content/primary interfaces and remaining mathematical gates. This is acquisition/scope completion, not human peer review or novelty certification.
