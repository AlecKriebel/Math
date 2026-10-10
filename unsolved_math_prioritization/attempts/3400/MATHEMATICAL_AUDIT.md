# Independent audit: stable ternary circuits (3400 / OPG-474)

Public proof-only edition. Recorded audit date: 10 October 2026. This AI-assisted audit is unrefereed; acceptance does not mean external human peer review, journal acceptance, or formal proof-assistant certification.

## Decision

**ACCEPTED AS PROVED PARTIAL.** No mathematical correction to the sealed proof is required. The original linear-size general bounded-fan-in circuit question remains unresolved by this work. The unconditional bounds established here are Omega(n) and O(n log n). The matching Omega(n log n) lower bound is conditional on the undirected k-pairs conjecture used by AFKL. Neither the conjecture nor an unconditional superlinear lower bound has been proved.

This audit accepts the explicit construction, the two shift reductions, the balanced-promise equivalence with output masking, and the specific source counterexample. It does not claim that these ideas are new. In particular, the conditional stable-compaction barrier is already discussed in Asharov–Lin–Shi. The audit made no changes to the source package and performed no publication or queue edit.

This edition binds the distributed [PROOF.md](PROOF.md): 18,333 bytes, SHA-256 `e72de7fbb3c65d3875a3fa804e46af7699897b7964d4286bf36cf989e9311f3e`. The complete mathematical sections, constructions, reductions, gate accounting, source counterexample and scope qualifications are preserved from the accepted proof. Public edits reconcile completed review status, explicitly credit the prior conditional barrier, and distinguish recorded supplementary checks from distributed analytic arguments. No mathematical proof correction is introduced here.

## Mathematical review

### Canonical Boolean model and unconditional lower bound

Representing each symbol by a live bit and value bit correctly distinguishes the two live symbols and garbage. Canonicalizing by live AND value gives the claimed extension to the fourth two-bit code. Each fixed finite, constant-arity gate can be replaced by a constant-size Boolean circuit; this does not license unit-cost arithmetic on growing words.

For each position i, fix the live mask to have its only live bit at i. Toggling that position's value bit changes the first output's value while keeping both inputs valid. Thus one output cone has n essential distinct value sources. Its connected underlying graph has at most bt incoming edges from its t computational gates, and at least t+r-1 edges when r distinct sources are present. Consequently r <= 1+(b-1)t. For any fixed b >= 2 this yields the claimed Omega(n) lower bound. Extra live-bit sources only strengthen the inequality.

### Rank-parity construction and cost

The pair formulas correctly produce its first and second live symbols, with canonical garbage fields when they do not exist. If the number of live symbols before the pair is odd, exchanging these two fields sends the first live symbol to the odd-rank channel and the second to the even-rank channel. A singleton therefore goes to the correct channel as well. Within each channel the surviving symbols retain their order. There are ceil(m/2) even-ranked and floor(m/2) odd-ranked live symbols when the input has m live entries, so recursive compaction followed by fixed interleaving yields exactly the desired prefix and only garbage afterward. This gives a complete induction, independently of finite tests.

There are six local field gates, two parity gates, and thirteen shared-control mux gates per pair. A two-pass complete-tree exclusive scan uses 2(m-1) XOR macros, each costing four basis gates. The recurrence is therefore valid. For n=2^L, the unsimplified implementation has the sharper exact count

    n + (29/2)nL - 8(n-1),

including initial canonicalization. This is at most 15nL+n. A stage adds O(L) depth and the recursion has L stages. For example, the conservative bound 3L^2+8L+1 suffices for the independently built circuit. Padding to the next power of two preserves the live subsequence and changes the size by a constant factor. No address tags, input-dependent wiring, or growing-word gates are hidden in this reasoning.

### Fan-out conversion, including terminals

For a bounded-fan-in circuit of S gates, the total number of operand uses plus output taps is at most bS+M. Split each source's uses through a binary distribution tree. This accounting includes original inputs, constants, computed bits, and repeated output taps. Two NOT gates implement each identity copy, so the additional size is O(bS+M). If a formal circuit definition requires separate output sink vertices, add M one-input identity gates. Constants can likewise be fixed locally or distributed through the counted tree. All node degrees are then bounded and the additional terminal cost is O(n). AFKL's degree restriction is satisfied; there is no free high-degree input exception.

The audit records that its independent checker built the conversion explicitly, added deliberately repeated input, constant and output taps, checked every resulting out-degree, and verified truth-table equivalence. This is supplemental implementation evidence, not the proof of the general conversion.

### Shift restrictions and balanced reduction

For each n-bit x and each 0 <= k < n, compacting `0^k 2^(n-k) x` yields `0^k x 2^(n-k)`. Taking value bits is exactly the zero-padded 2n-bit shift. The threshold decoder uses O(n) gates: a full binary decision tree has O(n) leaves and its suffix OR scan has O(n) gates. A literal change between zero-based and one-based binary indices, if needed, costs O(log n), already absorbed in this overhead. The input contains a single garbage run.

The balanced input `0^k 2^(n-k) x 0^(n-k) 2^k 2^n` has length 4n, precisely 2n live and 2n garbage symbols, and at most two garbage runs. For power-of-two n its length is a power of two. The first 2n output value bits are the same shift. Thus all independent payload bits and all shifts are represented, including k=0 and k=n-1. This is not a fixed-permutation argument.

In Regan's general-to-balanced reduction, choose m as the least power of two at least n, let c count garbage, and let g=n-c. Both padding exponents are nonnegative and the result has exactly m garbage symbols among 2m symbols. The compacted output consists of the original live subsequence, then m-g padding ones, then m garbage symbols. Retaining only indices j<g and replacing the rest by garbage recovers the exact original task. The mask is necessary: for x=(2), the padded input is (2,1), whose first unmasked compacted output is 1. Counting and threshold generation have the claimed O(n) Boolean cost.

### Conditional lower bound and its precise source

[AFKL, ICALP 2019](https://doi.org/10.4230/LIPIcs.ICALP.2019.10), Theorem 2 on physical PDF page 3, addresses the actual n-bit shift function with arbitrary Boolean gates and bounded in- and out-degrees. Its premise is Conjecture 1, equality of coding and fractional multicommodity-flow rates in undirected networks. The definitions on pages 5–6 and Section 4 on pages 7–8 were checked, including the zero-filled output convention. There is no large-payload requirement.

Applying the preceding reductions and fan-out conversion therefore gives O(S(2n)+n) >= c n log n, and hence S(2n)=Omega(n log n). For arbitrary m, n=floor(m/2) and trailing garbage padding give the same bound at length m. The balanced reduction gives it at all sufficiently large power-of-two lengths. These implications remain conditional throughout.

### Regan's Theorem 1 and the surviving comparator lower bound

The complete two-page [Regan note](https://www.cse.buffalo.edu/~regan/InfoFlow.pdf) was inspected, including its definition of the locally stable comparator. Its stated extension from binary-correct networks to stable sorting of arbitrary partial orders is false as written.

The network (1,3), (1,2), (2,3), with smaller entries directed to the lower-index wire, sorts all eight binary triples and all six distinct total-order permutations. Under the partial order 0,1<2, its locally stable comparators send (2,0,1) first to (1,0,2), then leave it unchanged. The correct stable output is (0,1,2). This disproves exactly the stability assertion, without depending on a broader interpretation of arbitrary posets. Nonadjacent exchanges may pass an item over incomparable elements that never meet it at a comparator.

The source's index-completed relation also fails for some general posets: take a<b with c incomparable to both and original order b,c,a. The resulting relation contains a<b<c<a. This additional observation is not needed for the explicit ternary counterexample.

The comparator lower bound remains valid. Restriction to {0,2} yields a binary sorting network; the ordinary total-order 0–1 principle then yields a sorting network for distinct items. A fixed pattern of comparator outcomes determines one input permutation leading to sorted distinct output, so n! orders require at least n! such patterns. Thus 2^s >= n!, giving s >= log_2(n!) = n log_2 n-O(n). This does not apply to unrestricted Boolean computation.

## Source scope and novelty

The audit recorded exact byte matches for four previously retrieved public sources: the originating problem page, the Regan note, Asharov–Lin–Shi, and Holmgren–Rothblum. The fifth source is the pinned official AFKL paper. [SOURCE_METADATA.json](SOURCE_METADATA.json) preserves the public source identities and recorded retrieval and inspection scope. These descriptions concern the proof review and audit, not a new scholarly inspection during edition preparation.

[Asharov–Lin–Shi](https://arxiv.org/abs/2010.09884), arXiv v2, explicitly discusses the conditional barrier to stable compaction; Theorem 1.2 is a nonstable construction and does not settle this target. [Holmgren–Rothblum, CCC 2024](https://doi.org/10.4230/LIPIcs.CCC.2024.11), gives O(n+q log^3 n) for supplied multiselection query indices. Substituting dense output counts and deriving the indices are not free operations. These scope distinctions are correct. The audit does not certify priority of the parity construction or counterexample, and does not claim an exhaustive new literature survey.

## Verification and limitations

The audit records that the author's normal and optimized checks both passed and matched the saved results. A genuinely independent implementation used an array-indexed scan tree, a bit-parallel Boolean evaluator, and an ordinary sequence-filter oracle, with no import of the author's checker. The recorded coverage was:

- All 349,524 Boolean encodings across lengths 1–9, including invalid-code normalization
- Exact unsimplified gate counts and a quadratic-logarithmic depth bound through n=4096
- Explicit all-terminal fan-out conversion through length 7
- 2,046 decoder inputs and 131,070 population-count inputs
- 18,434 ordinary shifts and 18,434 balanced shifts, covering every n<=10 and all x,k
- 29,523 balanced extraction cases, the source counterexample, and 2,080 essential-variable witnesses
- Six independently rejected negative controls

The audit records that normal and optimized independent results matched exactly. These tests support implementation correctness only; the asymptotic claims are accepted on the mathematical arguments above. No proof of the network-coding conjecture or unconditional circuit lower bound is inferred from testing. The analytic acceptance requires no omitted executable or raw output. Edition preparation rechecked frozen byte identities and publication integrity, but did not rerun these mathematical computations or perform new scholarly retrieval, source-text inspection, or literature search.

There are no blocking mathematical defects. This publication edition has a freshly authored status record and a precise eight-file manifest. Its distribution boundary is proof, mathematical audit, acceptance, status, source review and public metadata. Programs, raw outputs, datasets, copied third-party source bodies, PDFs, images and private coordination material are excluded. The analytic verdict does not depend on any omitted file.
