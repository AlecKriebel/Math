# PR885 / PID9700042: independent stochastic mechanism audit

**PASS, within the scope below.** The pinned revised C4 stochastic argument proves the sharp asymptotic from its explicit finite primal/dual identity and the primary problem's fixed-q flow-density limit, together with the verified classical Poisson-chain and Bernoulli-product BK inputs. I found no unresolved stochastic, asymptotic, or parameter-order blocker. This is an initial mechanism audit, not whole-package approval, a priority certificate, human review, formal verification, or permission to publish.

The strongest checked implication is

\[
\bigl[V_n=c_L+c_B+2(n-2)-D_{n-2},\quad V_n/(2n)\to v(1-q)\text{ in }L^1\bigr]
\quad\Longrightarrow\quad
\lim_{q\downarrow0}\frac{1-v(1-q)}{\sqrt{2q}}=1.
\]

The finite identity is an explicit dependency here; its independent whole-model validation belongs to the separate finite geometry family, whose findings I neither read nor received. The C1 marked-list count, all stochastic transitions, and their normalization were checked here. No new central proof search was attempted; the original CL 5/5 budget remains 5/5.

## Scope, input pins, independence and timing

The primary model was read before the candidate. SOURCE_CONTRACT was saved at 2026-10-15T13:52:11.974366Z, before candidate reading. The analytic memo was successfully saved at 2026-10-15T13:59:30.819153Z, before author clarification or prior-audit reading. Its opening 13:58 minute is drafting-time shorthand; the ledger records the exact successful save timestamp. An earlier save failed because the shared disk filled. I deleted only my already-inspected private renders/extracted text and did not read other assessments during recovery.

The analytic memo is unchanged after the freeze: SHA256 `911cafc5886d8714589a1b6968f6a772bb1b962ff41af5de13793a6d07e7cd03`. It contains the detailed independent derivations supporting this report. SOURCE_READING_LEDGER records exact sizes, hashes, reading order, and visual inspection pages.

| Input | Bytes | SHA256 |
|---|---:|---|
| C4 revised candidate | 20646 | `8da7cf366948e8d4fc63e3399cc4fe804ed786ea99b01479619efbdbacfedf3a` |
| C1 original prerequisite | 9957 | `f38d6ac74d3abad6f7675a13429f09e0bc6fc8151c137284e4655e8fc0c39120` |
| Frozen source manifest | — | `6b1d1281848190f616f6759f40454183c937b65e65219b893202254be6c3617d` |

No candidate, prior-audit, or author-checker code was executed. No other current independent family's findings were read. The only task communication was to the parent agent. No Git/ref/index/config mutations, publishing, DOI actions, sheets, outreach, or communication with individuals occurred. All authored work stayed in the assigned folder.

## Exact target and mathematical inputs

The target is the near-one deficit constant for the finite north/east independent Bernoulli-capacity square, with source/sink sets and denominator 2n exactly as on [Aldous's primary page](https://www.stat.berkeley.edu/~aldous/Research/OP/hammersley_flow.html). Its asserted fixed-p deterministic L1 limit is used as a premise. Its later continuum discussion is expressly heuristic and supplies no theorem used here. The boundary relation N=n-2 and the two bounded special-edge capacities are kept through the normalization.

The [Deuschel-Zeitouni author-hosted PDF](https://www.wisdom.weizmann.ac.il/~zeitouni/pdf/ccp.pdf) was visually inspected on complete pages 1, 2, and 9 because extracted characters are corrupted. Its geometric strict-chain probability limit has constant 2; Theorem 2 gives a positive upper-tail rate at speed sqrt(n) for any fixed positive excess. I derived the Poisson random-count and moment consequences rather than assuming them.

The [van den Berg-Jonasson primary-author restatement](https://arxiv.org/pdf/1105.3862) was visually inspected on complete pages 2 and 3. Theorem 1.1 is the product-measure disjoint-occurrence theorem, with coordinate certificates defined immediately before it. The subsequent fixed-size theorem is not used. Finite-many BK follows by iteration with unions of disjoint positive certificates. Primary body pins match ROOT_PRIMARY_RETRIEVAL.

## Mechanism checks and exact disposition

| Step | Result and reason |
|---|---|
| Mark budget and C1 use | PASS. The enumeration requires only b<=k, so it bounds K_N^+, not merely net reward. Distinct valid marked-edge lists have probability q^k; repeated/invalid lists enlarge only the count. The two numerical bases are 0.1643866545 and 0.0085121926, both <1/4. |
| Simple paths and rough moments | PASS. A cycle has nonpositive reward. An optimum can be simple and nonnegative. Tail summation at theta<log 4 gives uniform rough square moments; monotone padding yields the deliberately weaker rectangle bound. |
| Sparse finite-box Poisson limit | PASS. Two orientation opportunities give intensity two, and boundary expectation vanishes. The Laplace functional converges. Total mark count is exponentially tight; the probability of a close row/column pair is O_M(sqrt(q)). |
| Strict versus weak order, ties and orientation | PASS. On at most M marks separated by more than M in both coordinates, b<=k<=M forbids any decreasing ordered mark pair; every strict chain fits its one-step oriented edges. Away from ties and the boundary, chain length is locally constant in finite point configurations. Ties are controlled before the limit. |
| Moment and mean convergence | PASS. D<=Z and uniformly bounded E exp(aZ), with a>theta, give exponential uniform integrability. Weak convergence alone is not used to infer expectations. |
| Random-count Poissonization | PASS. Couple with one iid sequence independent of a Poisson(s^2) count; sandwich at floor((1-delta)s^2), ceil((1+delta)s^2). Chernoff errors have speed s^2, and the chain upper-tail error has speed s. |
| Sharp Poisson exponential moment | PASS. Split at (2+a)s and Ms. Choose theta M<c_a/2 for the middle part; factorial counting controls the unbounded upper part by a geometric series. This proves the fixed-theta bound, while the same factorial tail proves mean uniform integrability. |
| Slicing, rounding and rectangle positivity | PASS. There are ceil(2N/L) segments; last increment lies in (0,L]. Each side is at least 2a-b+1>h. Width plus height is exactly tau+2h+4a. The finite shape list may harmlessly contain unused shapes. |
| Bad rectangles and entropy | PASS. Nonlast bad segments use (m+10) times their actual backward budget; the last costs <=L+6h+4b_last. Endpoint records contribute (m+5)^J exp(K); the s-vector count is binom(J+K,K), with K/J->16m sqrt(q). No log(1/q) entropy is missing. |
| Overlap and BK certificates | PASS. Original segment marks alone force local reward under every completion; padding adds no negative reward and its edges are not certificate coordinates. Global simplicity makes certificates disjoint even when rectangles overlap. Independent extension can be made on one deterministic finite ambient box. |
| Union bounds and exponential normalization | PASS. Union over nonnegative reward vectors, the tail-generating identity, skeleton counting and marginal moments give (46). Dividing by 2sqrt(q)N gives exactly (47), including the coefficient 512 in the bad-size term. |
| Quantifiers and limits | PASS. Choose epsilon,m, then theta, then large fixed R, then sufficiently small fixed q, then N->infinity. Thresholds on q are independent of N. The final small-q conclusion follows from this family of fixed-q estimates. |
| Lower bound and matching constant | PASS. Diagonal block paths concatenate, with adjacent squares sharing only a vertex. Expectations and the fixed-q density limit yield (51). For each fixed R, the sparse mean limit gives E Lambda_(sqrt(2)R)/(2sqrt(2)R); then R->infinity gives one. No missing historical lower-bound proof is used. |

The upper bound passes from a probability tail to the density by boundedness 0<=D_N/(2N)<=1 and the input limit (22). The lower bound separately uses mean convergence already supplied by uniform integrability. Both constants therefore match for the correct rate-two lattice scaling and denominator 2N. There is no unsupported interchange of large volume with small q.

The parameter boundary cases relevant to these deductions were checked: q is positive and ultimately <=10^-6; h,L are positive integers after choosing q small; good shapes have positive fixed limiting sides; all rectangle statements allow external translations and a short final increment; K=0 uses F(0)=0; J=1 remains valid; zero local reward has an empty certificate. N=0 is confined to the finite n=2 identity and is not used in the asymptotic estimates. Empty and singleton sparse configurations are included. Degenerate limiting rectangles are excluded explicitly by w,h>0 and are never required.

## Independent finite falsification controls

The independently authored checker was fully read before execution and imports no source code. Actual command role: `python3 -I -S -B AUDIT/check_controls.py`, assertions active, no optimization. One run completed with exit code zero; the raw execution receipt is private, while CONTROL_RESULTS records the public role and actual counts. Nothing was simulated or promoted from computation to proof.

| Exhaustive control | Actual executed coverage |
|---|---:|
| Simple paths on Q_1,Q_2,Q_3 | 198 |
| Path/scale cases, h in {1,2,3}, m in {1,2,3,4} | 2376 |
| Geometric segment cases | 4854 |
| Negative endpoint-displacement cases / short final segments | 114 / 1022 |
| Q_2 mark configurations, all 12 paths, four scale choices | 4096 configurations; 196608 path/configuration/scale cases |
| Segment certificate tests | 442368, including 264960 positive certificates and 18816 negative segment rewards |
| Nonnegative-path negative-variation tests | 47744 |
| Separated mark sets, at most two marks, 6 by 6 rectangle | 581 |
| All increasing events on three coordinates, ordered triples | 20 events; 8000 triples |
| Rational triple BK inequalities, q=1/7,1/2,3/4 | 24000 |
| Coordinate-count parameter pairs | 30 |

All passed. A deliberately tied pair of horizontal edges has reward 2 and strict-chain length 1; it confirms why an unqualified finite-lattice strict-chain identification would fail. The revised proof instead uses a vanishing close-pair event and is not contradicted by this control.

These checks cannot prove BK in arbitrary dimension, the classical chain theorem, or an infinite-volume assertion. Their role is to falsify errors in the explicit finite constructions and constants; the analytical arguments are in ANALYTIC_MEMO_FROZEN.

## Post-freeze comparison with author clarification and earlier audits

Only after the frozen memo was saved did I read the complete author clarification, Audit A, Audit B, C1 audit, and clarified C1 proof. No conclusion in the frozen memo was changed.

The author's two precision corrections are valid: a<=b+h must be weak when h divides b, and positive rectangle sides for a short last segment require the actual endpoint displacements. The revised candidate already contains both. Audits A/B additionally note the corrected nonlast indexing and the explicit Poisson mean-uniform-integrability step. These are the same local issues independently handled here; no additional stochastic assumption or central lemma is introduced by the corrections. The acceptance target is the revised SHA, not the original candidate's literal wording.

Audits A/B accept the revised full asymptotic under the same external premises. This agrees with the frozen stochastic verdict, while their finite geometry acceptance is not substituted for this audit's explicit finite-identity dependency.

The C1 audit accepts only limsup <=e/2 and explicitly does not certify a separate lower bound or later C2 work. That limitation is correct for C1; it does not contradict C4's later argument. C4 needs C1's finite identity/count, then supplies a fresh lower bound and the sharp BK block upper bound. The strongest result supported by this mechanism review is therefore (T) conditional on the finite identity and source flow limit; it is not restricted to e/2 merely because the older C1 audit was partial. Neither unavailable historical artifacts nor C2/C3 are necessary inputs.

## Remaining gap and release boundary

**No unresolved stochastic proof gap was found.** The exact remaining scope condition is independent validation of the finite source-to-dual identity in the canonical boundary model; this review does not claim to close that separate family's task. The fixed-q flow existence/L1 statement is an explicit accepted model input, not independently reproved. Priority, novelty, author metadata, complete package consistency, safe publication selection and broader code integrity remain outside this initial mechanism verdict.

The public selection is the exact authored allowlist in PUBLIC_MANIFEST, relative to this audit folder. It excludes raw primary bodies, source copies, private receipts, removed renders and any other folder. A local file hash identifies inspected bytes; it does not certify an unchanged future download. Nothing is recursively authorized for publication. The parent should fully read REPORT, ANALYTIC_MEMO_FROZEN and check_controls before integrating the result.
