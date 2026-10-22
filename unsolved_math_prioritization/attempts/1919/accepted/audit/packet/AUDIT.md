# Independent audit: cycle-set counting, problem 1919 / EP-84

Audit date: 8 October 2026 (UTC). Queue rank: 1017.

## Verdict and exact accepted scope

**Accepted as a source-free, independently reviewed report of five partial approaches and their limitations. The full problem remains unsolved here.** The first asymptotic assertion is prior literature; the diverging-factor lower bound and the existence/value of the exponential growth-rate limit are not established by this work. No novelty, peer review of this packet, or formal certification is claimed.

The mathematical subject is the number f(n) of distinct sets of lengths of all simple cycles of finite simple undirected n-vertex graphs. It is not a graph count, an isomorphism-class count, an induced-cycle count, or a multiset count. Empty spectra and isolated vertices are included. The natural asymptotic domain is positive integer n, through both parities. The separate computational convention f(0)=1 does not extend the cactus formula with right side n-1 to n=0.

I read the complete corrected mathematical report, all executable code, the proof-turn ledger, status and source metadata, and the imported primary-source passages described below. I independently rederived all five restricted arguments. The conclusions below rely on those derivations; successful finite tests alone are insufficient.

### Subject and correction chain

The author revision2 manifest is 4a68c2510b717b1e6e4afcf267fdc0b40bf97a8156eab1c4c44c51f65e7410da. Its report hash is 86428f2fd218f8d6ebb54a9e6d6a0a9e8643ef8d2d99fb532fc524319bcd7083. The first seal's seven files still match its manifest, 6bcedfd3969ac78cb318f32a819486a4848c7c18d6ace163afe3f764eec7ca97. The actual earlier CORRECTION.patch applies cleanly to disposable first-seal copies and produces the revision2 report, proof-check code and verifier exactly.

This audit additionally found an exact-integer validation gap: direct invocation of revision2's verifier with a newly chosen manifest accepted a Boolean or floating-point first ledger turn, and did not validate its three non-proof-activity counters. The fixed, independently pinned bootstrap always rejected these altered manifests. This was a limited semantic-validation flaw, not a bypass of the original authenticity boundary.

The final accepted public slice incorporates the separate actual **LEDGER_VALIDATION.patch**: two validation lines require exact integer approach turns and exact integer zero for the source-lookup, duplicate-gate and audit/packaging proof-turn counters. Only verify.py changes among the nine author packet files; all eight other files, including every mathematical byte, remain unchanged. The externally rebound accepted pins are:

- Manifest: af6631e1537a26720df4234f41974a8de54185e5bd625bc24d6997f3174c1958
- Verifier: 5603afacfc7d8754eb5a94b61097863b01776dcca023210e46e6e96090695945
- Bootstrap: 714afb752a56c50c447f778a2ffbf301b5c5f28b4fd99b54a1768151e5863304

Neither original author seal is edited. The original status saying independent review was pending is a preserved historical statement; this separate audit supplies the subsequent acceptance and identifies the final accepted slice.

## Mathematical review

### 1. One hub, high-band recovery, and a genuine collision

Removing the sole hub from a cycle leaves exactly one path between two distinct hub neighbors. Conversely each pair of such neighbors closes the unique path into a simple cycle. Hence the spectrum is precisely D(A)+2, also when A has fewer than two elements. This accounts for all cycles, not only a selected family.

For the Faudree construction on 2m vertices, m>=2, the original path neighbor 2 is distinct from every chosen b>=m+1. The hub-to-path-neighbor cycle has length b. A cycle between two selected b-values has length b'-b+2, at most m+1; equality requires b=m+1 and b'=2m. Thus every extra length above m is already a selected value. Intersecting the complete spectrum with {m+1,...,2m} recovers B, proving the 2^m lower bound for this domain. At m=1 the proposed extra edge is the existing path edge; no 2-cycle exists and f(2)=1. The earlier correction is essential and correct. The constructor now rejects m=1.

The two displayed neighbor sets have different cardinalities, so equality of their distance sets is not explained by reflection or translation. Direct pair differences give every distance from 1 to 6 for each set. Their eight-vertex one-hub graphs therefore collide. With an integer widening parameter 0<=s<=m, selected-selected distances can reach m+s, so only the m-s positions above that threshold retain the original uncontaminated decoder. This is a limitation of that decoder, not a theorem that no other decoder or image estimate can work. The report makes the correct distinction.

Isolated-vertex padding extends any even-order bound to the next odd order, losing the fixed factor sqrt(2). It cannot turn a constant-factor lower bound into a divergent-factor one. A genuinely divergent bound on all sufficiently large even orders would transfer to all orders; an arbitrary sparse subsequence would not automatically suffice.

### 2. Uniform sampling and concentration of distance sets

For a fixed d, the distance-d graph is a disjoint union of residue-class paths. An e-edge path has a matching of size ceil(e/2), so the combined matching has at least (N-d)/2 edges. A uniformly sampled subset chooses its vertices independently with probability 1/2. The disjoint matching edges therefore fail to have both endpoints selected independently, with probability 3/4 each. The missing-distance event is a subset of their joint failure event. This establishes the stated bound, including its inequality direction.

For d<=N-t, the matching has size at least t/2. A union bound over at most N distances gives N(3/4)^(t/2). With t=ceil(6 log N/log(4/3)), this is at most N^-2. For sufficiently large N, 1<=t<N. There are exactly t-1 remaining potential distances above N-t, giving at most 2^(t-1), hence polynomially many outputs for at least a 1-N^-2 fraction of all inputs.

No polynomial upper bound for all distance sets follows: the exceptional fraction still contains exponentially many subsets. The report does not turn a statement about typical inputs into a statement about the entire image or use it to refute the requested lower bound.

Independently, writing N=qd+r gives d-r residue paths on q vertices and r on q+1 vertices. Independent subsets of a k-vertex path number F_(k+2), yielding the displayed product for the exact missing-distance count. The indexing and both residue cases are correct.

### 3. Cactus spectra and the vertex budget

For a graph with c connected components, the block decomposition gives n-c as the sum of |V(block)|-1 over its nontrivial blocks. In a cactus, every cycle is one cycle block. Selecting a representative block for each distinct required length gives sum(ell-1)<=n-c<=n-1 when the spectrum is nonempty. Repeated lengths, bridges and disconnected components cannot reduce this cost. For n>=1 the empty spectrum also satisfies the criterion and is realizable.

Conversely, one cycle of each required length, all joined at a common vertex, has 1+sum(ell-1) vertices and no cross-block simple cycles. Padding supplies exactly n vertices. Thus the criterion is both necessary and sufficient for positive n.

The generating-product bound counts an even larger class of distinct positive weights, so permitting weight 1 only increases the count. For t>0, log product(1+e^-tj)<=sum e^-tj=1/(e^t-1)<=1/t. Optimizing tM+1/t at t=1/sqrt(M) gives exp(2sqrt(M)) for M>0; M=0 has one spectrum. The logarithm of the ratio to 2^(n/2) tends to minus infinity. This excludes the entire cactus family, with unboundedly many blocks allowed. It does not exclude arbitrary unions involving non-cactus cores.

### 4. One generalized theta and partition counting

The internally disjoint paths share only their two terminals. Internal vertices have degree two in this component; a simple cycle must traverse two entire terminal paths and cannot traverse a third without revisiting a terminal. Every pair gives a cycle. A simple graph permits at most one length-one path. Consequently no forbidden 2-cycle is hidden in the pairwise-sum formula.

The positive weights l_i-1 form an unordered integer partition of total s<=n-2; the one optional direct edge contributes zero and gives at most an additional factor two. Zero paths, one path and one direct edge only produce harmless overcounting of the empty spectrum. The bound applies for n>=2, with the stated analytic optimization used when n>=3.

For t>0, expanding the logarithm of the partition product and summing the nonnegative terms gives sum_(r>=1) 1/[r(e^(tr)-1)]<=t^-1 sum r^-2<=2/t. Optimizing tM+2/t gives exp(2sqrt(2M)). Multiplication by two remains negligible compared with 2^(n/2). The argument permits the number of paths to grow with n and still bounds all spectra in this single-network class. It makes no statement about networks with several branching locations.

### 5. Two nonadjacent hubs and the translated-copy failure

There are no cycles entirely inside the base path. Removing one hub from a cycle that uses only that hub leaves a path, giving D(A)+2 or D(B)+2. A cycle using both hubs splits, after their removal, into two vertex-disjoint path intervals. Each joins an A-neighbor to a B-neighbor and may be a singleton common neighbor. Restoring the four incident hub edges adds four to the total interval lengths. Conversely such intervals create a simple cycle. Vertex disjointness, including the singleton case, is essential; edge disjointness alone would overcount.

For the specialized family, x has neighbors 0,t and y has neighbors 0 and B, with 0<t<m<=b. If the interval incident with x-neighbor 0 ends at a positive b, it contains t and cannot coexist with the other cross interval. Therefore the interval at 0 must be the singleton, while the other is [t,b]. This proves the complete four-term specialization, including B empty. There is no missing case using a hub-hub edge because the hubs are nonadjacent by definition.

For m=6,t=5, both displayed B choices have exactly the listed ten cycle lengths on fourteen vertices. The shift t-2=3 satisfies the proposed separated-shift threshold ceil(m/2), and the two extremes are fixed, so this is a counterexample within the tempting decoder's own regime. Without the selected-selected difference contribution, a chain of length at most two is decoded by its two endpoint output bits. The actual difference contribution can hide an endpoint and introduce a smaller cycle, invalidating that reasoning for the complete spectrum.

The symmetric-family counts are correctly described as counts of this construction's image, not exact values of f(2m+2). Finite ratios and unproved recurrences imply no asymptotic lower bound. The remaining gap is accurately identified as a uniform complete-spectrum image bound with a multiplicative factor tending to infinity.

## Source imports and current-status limits

The scope matches the [official indexed history](https://www.erdosproblems.com/history/84) and [LaTeX page](https://www.erdosproblems.com/latex/84). An independent direct attempt to open the problem again returned 403; the indexed pages were several months old. This is not a full live discussion inspection or an exhaustive guarantee of current openness.

I visually inspected page 2 of Verstraete's author PDF because its text extraction is corrupt. Its Theorem 1.2 supplies a positive power saving in the exponent, sufficient for the upper little-o assertion. I inspected Nenadov's published introduction, theorem and lower-bound discussion, and separately checked the arXiv v2 stamp and corresponding introduction. The published bound has a positive constant times sqrt(n)/(log n)^(3/2) as an exponent saving. That quantity tends to infinity for all integer n, so the ratio to 2^n tends to zero. None of these upper bounds proves the lower assertion. Credit remains with the cited literature. [Verstraete PDF](https://mathweb.ucsd.edu/~jverstra/numcyc.pdf); [Nenadov publication](https://doi.org/10.5070/C66165704); [arXiv v2](https://arxiv.org/abs/2501.09904v2).

I inspected Dunas's title page, abstract, introduction and complete lower-bound section. The distance-set reduction, parity-dependent constant improvements and Fibonacci product are accurately identified. Dividing the two parity bounds by 2^(n/2) leaves fixed constants, not a quantity shown to diverge. The work is a June 2026 master's thesis; this audit does not relabel it as a peer-reviewed journal paper. The report's nonresolution wording is consistent with that primary source. [Thesis PDF](https://uu.diva-portal.org/smash/get/diva2%3A2077189/FULLTEXT01.pdf).

All four retained PDF byte counts and SHA-256 values match the author's public metadata. The audit accepts these sources for the specified theorem statements and attributions; it does not certify their full proofs. It does not independently reproduce the entire campaign duplicate gate or corpus download history. Those remain bounded provenance claims rather than mathematical premises.

## Executable evidence and trust boundary

The independently authored checker uses subset dynamic programming for cycle detection, unlike the author's DFS and cycle-edge-mask methods. For a fixed least vertex, a state records which endpoints can be reached by a simple path using precisely a given vertex subset. Extending to an unused neighbor is complete by induction on subset size, and a closing edge to the root detects a cycle. Only subsets of size at least three count. Thus the detector has an independent completeness argument.

In each of normal, -O and -OO, the checker processes all 33,868 labeled graphs of orders 0 through 6, obtaining f(n)=1,1,1,2,4,6,11. A separate Tarjan edge-block test identifies cactus graphs and verifies their entire finite spectrum image against the vertex-budget criterion. Additional checks cover 2,047 one-hub cases, 508 Faudree cases through m=8, distance images through N=16, 91 exact missing-distance cases, 544 theta cases, 5,461 two-hub cases through path order 6, all 516 specialized cases through m=6, and the fourteen-vertex collision. The three modes return identical mathematical results. The total 732,874 checks includes routine graph-validity checks and must not be advertised as that many independent mathematical propositions.

The author's complete matrix was independently rerun on revision2 and again on the corrected public slice: each has 5,668 finite checks per mode, 34 hostile cases in all three modes, four actual write-denial probes as effective UID 1000, and three read-only relocated successes under a hostile working directory and Python environment. Frozen bytes and modes remain unchanged. The extra parser tests supply eight additional malformed cases in all three modes; the original fixed bootstrap rejects their caller-repinned variants.

The semantic-correction matrix demonstrates 14 precisely targeted old/new cases in normal, -O and -OO: revision2 accepts all 42 direct caller-repinned variants, the corrected verifier rejects all 42, and both fixed bootstraps reject all 84 changed manifests. The check also verifies byte identity of all eight nonverifier packet files.

Trust starts with independently delivered manifest, verifier and bootstrap hashes and trusted isolated Python/stdlib. A replacement self-authored manifest is not evidence of authenticity. The static, read-only threat model does not promise protection against a privileged attacker changing files between checks or a compromised Python runtime. Neither the verifier nor this audit is a general mathematical theorem prover or a complete arbitrary-metadata schema validator.

## Publication scope

Only the explicit final allowlist is suitable for publication: authored mathematical text and code, actual correction patches, public citations and verification metadata. It excludes source PDFs, extracted text, rendered source pages, corpus contents, private coordination and absolute private paths. No publication, queue modification or external communication is performed by this audit. The accepted disposition is **unsolved; five approaches used; independently reviewed scoped partial results**, with the upper assertion credited to prior work.
