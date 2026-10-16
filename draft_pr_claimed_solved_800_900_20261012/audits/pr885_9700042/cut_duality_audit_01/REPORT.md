# PR 885 / problem 9700042: independent finite directed-cut audit

Audit date: 2026-10-15. Role: universal finite geometry and its exact connection to the asymptotic target. Author metadata supplied for the project: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X.

## Decision

**PASS within this role.** The exact finite directed-flow/dual-path prerequisite is correct for the primary model. It covers arbitrary cuts, four-valent faces, backward dual steps, the two forced corner crossings, and n=2. The marked-list prerequisite, local completion geometry, original-mark witnesses, and lower-bound concatenation also withstand independent checks. No substantive gap remains in these finite mechanisms.

The strongest verified statement is the exact identity, valid for every assignment of finite nonnegative primal capacities when V_n denotes the ordinary maximum-flow value (the path count in the Bernoulli case),

V_n=c_L+c_B+T_{n-2}.

For Bernoulli capacities, D_N=2N-T_N=max_P(k(P)-b(P)) and

(2n-2)-V_n=2-c_L-c_B+D_{n-2}.

Using the primary source's stated fixed-q L1 limit, this gives exactly

g(q):=1-v(1-q)=lim(N->infinity) E[D_N]/(2N).

**Scope boundary:** this report does not approve the entire sharp asymptotic, novelty, current priority, formal verification, publication, or DOI creation. The remaining full-theorem dependencies are the external Poisson-chain law and tail, the exponential-moment consequence, BK, and C4's probability/entropy/parameter argument. Finite enumeration cannot establish those. There is no blocked route or unsupported restatement inside the finite mechanism audited here. The original central proof-search count remains **5/5**; this work is validation.

## Independence and authenticated inputs

The [actual Aldous primary model](https://www.stat.berkeley.edu/~aldous/Research/OP/hammersley_flow.html) was browser-retrieved before candidate inspection. Its downloaded 3,576-byte HTML was separately read and authenticated: SHA256 `1c3078bb05b25554b7ab7bc12e6d8567b777407b6c6ad24fecfc89715088a301`, agreeing with the parent HTTP-200 retrieval receipt. SOURCE_CONTRACT.md was frozen at 13:51:35Z, before candidate or previous-audit reading. FROZEN_ANALYTIC_VERDICT.md was frozen at 13:56:10Z, before earlier audits, author clarification, or README inspection. README was never needed.

The immutable source manifest SHA256 is `6b1d1281848190f616f6759f40454183c937b65e65219b893202254be6c3617d`. The parent live-gate receipt identifies head `4b1ef9bbeb723a4171949a6c3934db98962ac615`, PR 885, original count 5/5. I authenticated these receipt bytes but did not independently query GitHub or mutate Git.

Candidate inputs read in full and hashed:

- TURN_C1_MARKED_DEFECT_BOUND.md: 9,957 bytes; SHA256 `f38d6ac74d3abad6f7675a13429f09e0bc6fc8151c137284e4655e8fc0c39120`.
- TURN_C4_BK_POISSON_REVISED.md: 20,646 bytes; SHA256 `8da7cf366948e8d4fc63e3399cc4fe804ed786ea99b01479619efbdbacfedf3a`.

No original checker was imported or executed. Both fresh checkers were fully read and hashed before execution. All writes remained in this audit folder. No other researcher, chat, shard agent, or individual was contacted; only the assigning parent received coordination updates.

## Exact source contract

For n>=2, primal vertices are {0,...,n-1}^2, with north/east nearest-neighbor edges. Capacities are independent Bernoulli(p), and paths are edge-disjoint, with shared vertices allowed. Sources are the left/bottom boundary excluding (0,n-1) and (n-1,0); sinks are all top/right boundary vertices. The origin is a source and the upper-right corner a sink. Auxiliary terminal arcs have unrestricted capacity. The source-stated limit uses V_n/(2n), n->infinity at fixed p. The target is g(q)/sqrt(2q)->1 as q->0 after that limit. The source's covering-path/continuum heuristic was not used as an exact finite identity.

## Independent proof of the finite prerequisite

Put N=n-2. Represent the primal face with lower-left corner (x,N-y) by dual vertex (x,y). A dual east step crosses ((x+1,N-y),(x+1,N-y+1)); a dual north step crosses ((x,N-y),(x+1,N-y)). Forward cost is that primal capacity; reverse cost is zero. These are exactly the interior primal edges. Only two boundary edges can cross an allowed cut: e_L=((0,n-2),(0,n-1)) and e_B=((n-2,0),(n-1,0)). Both point outward and contribute c_L+c_B.

For any allowed primal cut, draw all bichromatic edge crossings, oriented with the source side on the right in the physical embedding. Cyclic binary color transitions around every bounded face give equal incoming and outgoing degrees. An alternating face has two of each; it requires no assumed noncrossing pairing. The e_L exterior endpoint has excess outgoing degree one, and e_B has excess incoming degree one. The second endpoint must be reachable from the first: otherwise summing degree balances over the reachable set contradicts its absence of outward arcs. Loop erasure gives a simple corner-to-corner dual path. Its forward crossings are outward primal cut edges, while reverse crossings are inward and cost zero. Its cost plus the forced terms is at most the cut cost. Islands, holes, and extra components do not affect this inequality.

Conversely, a vertex-simple dual path, appended through the two forced crossings, is an embedded simple crosscut avoiding primal vertices. Jordan separation puts exactly the prescribed source boundary arc on its right and the sink arc on its left. Source-side primal vertices define an allowed cut whose outward crossings are precisely the forward dual steps plus e_L,e_B. Nonnegative costs permit deleting cycles from any shortest walk. Integral max-flow/min-cut now gives the claimed equality. For n=2 the dual path has zero steps and the equality reads V_2=c_L+c_B.

For a corner path, forward count minus backward count is 2N; its cost is 2N+b-k. Every closed walk has equal forward/backward counts and reward at most zero, so deleting cycles does not lower reward. Thus simple maximizers exist and their marked edges are distinct. A monotone path gives nonnegative reward; nonnegative cost gives D_N<=2N. The all-open flow is 2n-2, and the all-closed flow is zero. The bounded forced terms and N/n->1 establish the fixed-q expectation limit above without exchanging limits.

The complete checkable derivation is INDEPENDENT_DERIVATION.md; it also gives the stars-and-bars count, cycle accounting, local completion proof, and diagonal concatenation.

## Marked lists and C4 completions

For a nonnegative-reward simple path, b<=k. Taking its k marked forward starts in path order and appending the corners cannot increase either coordinate's negative variation, since (a-c)_+<=(a-b)_++(b-c)_+. Choosing t negative increments and their positive magnitudes, then the remaining nonnegative increments, proves C1's coordinate count. Orientation bits and two coordinate lists identify a marked-edge list. Full-path injectivity is unnecessary: the union is over valid distinct-edge lists, and each such list has closure probability q^k. Invalid/repeated lists are discarded before probabilities are assigned. Thus C4's stronger K_N^+ use is valid, rather than an inference about k from D_N alone.

For a sliced segment, every coordinate stays above its start minus b_j and below its end plus b_j. The quantized rectangle contains the entire segment; both corner-to-end padding paths are monotone and exist. Width and height exceed 2a_j-b_j>=h, even for a short last segment. Their sum is tau_j+2h+4a_j. Nonlast bad rectangles cost at most (m+10)b_j; the last costs at most L+6h+4b_last, giving exactly the candidate's total bad-perimeter bound.

Keeping only the segment's original marked forward edges makes its reward no smaller under every other mark assignment. Padding adds nonnegative reward and loop erasure cannot decrease reward. Hence these original marks alone certify the local positive-reward threshold. Zero threshold has the empty witness. Distinct segments of the simple global path have disjoint original marked-edge sets. This establishes the deterministic event inclusion used by BK; it does not replace proof of BK itself.

For the sparse stability step, a total mark count <=M and coordinate separation greater than M force all marks visited by a nonnegative-reward path into strict coordinate order. Conversely, that separation permits monotone connections through every selected oriented edge. The finite deterministic statement is sound. Its high-probability and moment consequences remain probability arguments.

Diagonal side-ell squares meet only at a corner, so their optimal paths concatenate to a simple large-square path. D_{k ell}>=sum D_ell^(j) holds pathwise. Expectations and the fixed-q limit give g(q)>=E[D_ell]/(2ell), without needing independence.

## Finite diagnostics and reproducibility

The normal and optimized isolated finite-checker runs both exited 0 with identical saved stdout SHA256 `c020d03dac30e16aaed019a997523dbbccd64161d2c1734e9d26a476a36afb86`. Explicit exceptions preserve every check under optimization.

| Diagnostic | Exact coverage |
|---|---:|
| Arbitrary cut colorings, n=2..6 | 66,067 |
| Those with four-valent faces | 41,870 |
| Four-valent face occurrences | 73,986 |
| Essential capacity patterns, n=2..4 | 16,452 |
| Simple dual paths, N=0..4 | 8,711 |
| Those using backward steps | 8,612 |
| Coordinate lists, 25 (N,k) pairs | 5,699 |

The capacity checker enumerates primal cuts independently of dual shortest paths. Omitted outer-boundary capacities never cross any allowed cut; the enumeration therefore covers every full capacity assignment modulo provably irrelevant states. Every simple dual path is converted back into a cut by undirected primal reachability after removing crossing edges, verifying the exact outward/inward crossing sets.

The supplemental completion checker ran normally and with optimization, each exit 0 and identical tool stdout. It checked all simple paths for N=1..3 and 12 (h,m) choices: 2,376 path/scale cases, 4,854 segments (2,748 bad; 1,022 short-last), 25,192 mark-only witness completions, and 1,096 marked subsequences. Mark patterns are exhaustive on each path for N<=2; four deterministic patterns are used at N=3. All other marks are absent during each local completion test. No diagnostic failure occurred.

A first attempt to redirect the supplemental stdout failed before Python started because the shared filesystem reported no space (shell exit 1). Re-running without redirection succeeded; the exact tool stdout was subsequently saved as COMPLETION_CHECK_RESULTS.json, SHA256 `cfbf826576da2623dfc07f7d329544e42683e1c45ec35ee702bd1766fc097259`. The private raw execution receipts preserve this failure and the actual successful exits. Public EXECUTION_SUMMARY.json uses normalized command roles. No claimed test count includes the failed launch.

## Comparison after freezing independence

Only after the independent verdict was frozen did I read TURN_C1_CLARIFIED.md, C4_AUTHOR_CLARIFICATION_1.md, and the C1/A/B audit reports. The clarified C1 supplies the same directed balance proof reconstructed here; it addresses exposition in the original compressed interface paragraph, not a false identity. The C4 clarification replaces an invalid strict inequality by a weak one when h divides b_j and proves rectangle positivity from actual endpoint displacements. The pinned revision already contains these corrections; the independent completion analysis agrees. The earlier reports' full-theorem acceptances are recorded as prior opinions and are not premises of this verdict.

## Final status

This finite audit is complete. No repair to immutable candidate inputs was necessary. The exact remaining approval gap is the full-theorem probability/source/entropy audit, plus separate priority review if requested. Passing this report alone must not be promoted into an unconditional whole-paper or firstness acceptance.
