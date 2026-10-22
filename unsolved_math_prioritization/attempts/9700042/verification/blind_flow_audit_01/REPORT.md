# Source-first blind mathematical audit: PR885 / PID9700042

Final verdict: **PASS**, scoped to the mathematics of the exact current C1 prerequisite and revised C4 proof. No unsupported central step was found. The argument yields

    lim_(q downarrow 0) [1-v(1-q)]/sqrt(2q) = 1

for the canonical model on [Aldous's primary problem page](https://www.stat.berkeley.edu/~aldous/Research/OP/hammersley_flow.html), using its stated deterministic L1 flow-density existence. This audit does not certify novelty, firstness, human review, formal verification, the whole publication package, eligibility, or any remote action.

## Independence and exact inputs

The primary problem was read independently first, both through the web retrieval and the authenticated actual HTML. SOURCE_CONTRACT.md froze exact boundary sets, edge capacities, zero-length convention, normalization, ordered limits, and six falsification mechanisms before either proof body was read. INDEPENDENT_ANALYSIS_FREEZE.md then froze the complete analytic verdict before any older audit, disposition, clarification, or candidate checker was read. The subsequent comparison found agreement and did not change that verdict. No other researcher, chat, shard, or audit family was contacted.

Acceptance attaches to these exact source-role bytes:

| Role path | Bytes | SHA-256 |
|---|---:|---|
| source/TURN_C1_MARKED_DEFECT_BOUND.md | 9957 | f38d6ac74d3abad6f7675a13429f09e0bc6fc8151c137284e4655e8fc0c39120 |
| source/TURN_C4_BK_POISSON_REVISED.md | 20646 | 8da7cf366948e8d4fc63e3399cc4fe804ed786ea99b01479619efbdbacfedf3a |

The proof uses the actual source boundary convention: sources are the bottom/left arc excluding the two corners on the sink arc; sinks are the full top/right arc. The sets are disjoint, so no zero-length path contributes. Only edges have unit capacities. The all-open baseline is 2(n-1), and the limiting normalization is 2n.

## Decisive mathematical findings

The detailed checkable reconstruction is INDEPENDENT_ANALYSIS_FREEZE.md. Its nine steps verify the following chain.

1. Directed cut duality gives V_n=c_L+c_B+T_(n-2), including nonmonotone cuts. A simple reflected dual path has reward k-b, every cycle has nonpositive reward, and the two forced boundary edges give only a bounded correction. Thus g(q)=lim E[D_N]/(2N) is the correct deficit density. Checkerboard face interfaces can be resolved as balanced directed interface trails; simple crosscuts give the converse cut.
2. C1's marked-list count controls the total number k of distinct marks on any simple path with b<=k, not merely k-b. The negative-variation composition count and the two geometric ranges are valid. Consequently C4's K_N^+ budget and uniform rough rectangular exponential moments follow. C1 itself gives the nonsharp e/2 upper constant.
3. Fixed rescaled boxes converge to intensity-two Poisson marks. Coordinate separation forces an unrestricted nonnegative-reward path's marked starts to form a strict chain; separated chains can be traversed with their specified edge orientations. Total mark count supplies exponential uniform integrability.
4. The imported rate-one Poisson chain constant is 2. The positive-excess upper tail at speed s, together with factorial control of very high tails, yields the small fixed-theta moment estimate. The actual [Deuschel-Zeitouni primary PDF](https://www.wisdom.weizmann.ac.il/~zeitouni/pdf/ccp.pdf), pages 1 and 9, was visually inspected because text extraction is broken. Theorem 2 is used for the uniform strict-chain law at speed sqrt(n), with a positive rate for every positive excess; uniform density meets its hypotheses. Poissonization and the moment conversion are independently justified in the freeze.
5. First-hitting rectangles contain all excursions, including the final short segment. Their total side length is tau+2h+4a. Good shapes have L+6h total side length; bad total side length is at most (m+10)B_N+L+6h. The exact inequality and index corrections in the revision are adequate.
6. Skeleton entropy counts coarse coordinates only; no microscopic endpoint factor is missing. K/J tends to 16m sqrt(q). Overlapping local rectangles use mutually disjoint marked-edge witnesses from the original simple path. Padding is outside the witness and has nonnegative reward. Therefore the [primary-author BK restatement](https://arxiv.org/pdf/1105.3862), definition and product Theorem 1.1 on pages 2-3, applies. It is the finite Bernoulli product theorem, not the paper's later fixed-size result.
7. Parameters are fixed in the valid order epsilon,m; theta; R; then sufficiently small fixed q; then N->infinity. The rectangle moment thresholds are independent of N. The entropy cost is O(1/R), the extra backward entropy vanishes with q, and the bad-length error is 512 theta(m+10)sqrt(q). These are absorbed by fixed positive slack. This resolves the ordered-limit difficulty with uniform inequalities.
8. Diagonal block concatenation gives a fresh lower bound. First q->0 at fixed rescaled R; afterward R->infinity. The Poisson mean constant gives 1. No missing historical lower-bound proof is required.

## Source-derived falsification attempts and limitations

The source's explicitly heuristic scaling and continuum chain-count displays contain apparent dimensional/factor inconsistencies. C4 does not import them: it derives rate two and uses the correct constant-two chain law. The source's informal closed-edge-cover complementation is not an exact finite identity under the literal boundaries. At n=2, close only the top horizontal edge: V=2, its all-open deficit is zero, while one source-to-sink path is needed to cover that closed edge. This is a useful trap and does not refute this proof, which uses direct directed-cut duality.

Independent finite_boundary_check.py was authored and fully read before candidate checkers. Under isolated standard-library Python it passed all 16 full-primal n=2 and 4096 full-primal n=3 capacity configurations, 400 deterministic samples at n=4,5, and all-open/all-closed extremes through n=6. FINITE_BOUNDARY_RESULT.json records exact scope. These checks support finite conventions; they do not establish the universal duality or any asymptotic.

After the analytic freeze, both candidate diagnostic scripts were fully read, SHA-authenticated, and replayed with assertions active under python3 -I -S -B. A storage error prevented tiny copies and temporary files. The isolated process therefore captured only the scripts' declared JSON output write in memory; all tested code otherwise remained unchanged. The C1 result was byte-identical to its frozen 3971-byte JSON, SHA-256 022566a4288c89010aa15923c84cc802e9cb0627937eed44144e818905df3b08. The C4 result was byte-identical to its frozen 628-byte JSON, SHA-256 c6665c65efbab00cbda08a0b4151be5d076bdf89d6a453dc6a3997174c88c57f. This audit did not rerun the whole-package verifier or certify every older checker.

## Strongest result and exact remaining gap

Strongest verified result: the exact canonical square-root asymptotic follows from the two pinned current proof bodies and the explicitly checked classical inputs. Exact mathematical gap identified: none. Residual external dependencies are the source-stated L1 density limit, classical uniform-chain shape/upper-tail theorem, and finite-product BK theorem; each is used in its stated regime. The audit is fallible mathematical review and has no authority over novelty or package publication gates.

No new central proof search was launched beyond the original 5/5 attempts. No Git, branch, index, configuration, PR, publishing, release, DOI, spreadsheet, or outreach action occurred. Only this audit's dedicated folder was written. Private primary-source receipts remain inspection evidence and are excluded from the explicit public manifest.
