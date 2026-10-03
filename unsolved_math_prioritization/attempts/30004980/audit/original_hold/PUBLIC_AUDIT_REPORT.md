# Independent audit of maximum twin width research record

Date: 2026-10-03 UTC. Problem 30004980 / OWR-9790352-030. Research author: Alec Kriebel. This is an adversarial review of a five-attempt partial research record, not research authorship or a resolution of the problem.

## Verdict

**HOLD on the frozen wording, with one localized mathematical definition correction required.** All reported computations reproduce, and the intended partial results pass independent mathematical review. The exact maximum problem remains unsolved by this work after five attempts out of five. A correction and a fresh freeze are required before a full PASS can apply to a revised package.

The audited package is the 17-file record at commit `ab502620095141f19e983d835c5ca3ac885ed21c` in `AlecKriebel/Math`. Its MANIFEST.json SHA-256 is `67aa8bdbea3c4991d4206978fd5944dc3ae822b47b8198f615adc872e2383756`. All 16 manifest-listed files match their byte counts and SHA-256 values. All 17 files, including the manifest itself, were fetched independently from that commit and matched the local frozen bytes. No original file was modified. `frozen_sha256.txt` records the complete freeze.

## Required correction and nonblocking improvements

### H1 Endpoint exclusion in Attempt 2

In `attempts/turn_02.md`, line 6, D_i is defined as the original vertices seeing exactly one endpoint of P_i. Read literally in a simple graph, this includes both endpoints whenever the pair is adjacent. The asserted exact identity on line 10 is then false.

Smallest counterexample: let G=K2 and P_1={0,1}. Both original vertices are adjacent to exactly one member of P_1, so the stated definition gives |D_1|=2. The only contraction has red degree 0. The claimed identity gives 2 instead of 0.

Required replacement: `D_i = {v in V(G) minus P_i : v is adjacent to exactly one of a_i,b_i}`. This agrees with the implementation, which explicitly clears both endpoint bits, and with the proof's intended meaning. There is no algorithmic correction needed for this defect. Independent tests below verify the identity with this corrected definition.

Recommended edits to bundle with the correction:

- Credit Ahn et al., Lemma 4.3, directly for the additive pair-scheduling identity, not only their Paley theorem for the later symmetry argument.
- Define the empty maximum over pair-orbits to be 0 if the one-vertex case is included. Alternatively restrict the involution proposition to nontrivial involutions and state n=1 separately. This is a minor convention issue, not a false positive computational result.
- Rename the scalar b_i to avoid reusing the same notation for a vertex and a number.
- Cite the existing six-vertex result of Kajal Das described below. The package already disclaims novelty for small maxima, so this is bibliographic improvement rather than a separate correctness blocker.

## Source scope and prior work

The original [Oberwolfach report](https://ems.press/content/serial-article-files/46939?nt=1), printed page 66, PDF page index 61, asks for the maximum twin-width of an n-vertex graph and already lists Paley equality and an asymptotic n/2 upper bound. The package correctly targets finite simple undirected graphs with initially black edges, arbitrary binary contractions, and maximum red degree. It does not substitute sparse, linear, directed, or initially red variants. The live [problem page](https://www.unsolvedmath.com/problems/30004980) was inaccessible in this review; its present body and numeric catalog mapping were not independently recovered from that page.

[Ahn, Hendrey, Kim, and Oum, v2](https://arxiv.org/abs/2110.03957v2): Theorem 1.1 gives the strict upper bound stated in the README; Theorem 1.3 gives the random-graph lower bound; Theorem 1.4 proves Paley equality. Conference lower bounds are developed in Section 3. Corollary 4.2 supplies the first-contraction bound. Lemma 4.3 supplies the same additive pair-update formulation used here. Thus the leading asymptotic and pair-scheduling mechanism are established prior work. The README's grouped theorem reference is substantively correct; adding the precise Section 3 and Lemma 4.3 locations would improve it.

[Heinrich, Ihringer, Raßmann, and Volk, v2](https://arxiv.org/html/2504.02342v2): Theorem 4.1 provides the first-step equality characterization; Lemma 4.2 gives early pair structure; Theorem 4.7 covers self-complementary vertex- and edge-transitive graphs. Conjecture 5.2 is a conjecture, including conference equality, not a proved universal upper bound. The arXiv version remains v2 and the record lists a 2026 journal publication. Trivial-order conventions should not be silently inferred from its equality wording.

Additional relevant primary literature checked: [Kajal Das, 2309.05297](https://arxiv.org/abs/2309.05297), explicitly proves the six-vertex upper bound 2; [Ahn et al., random graphs, v2](https://arxiv.org/abs/2212.07880v2), refines the typical random-graph value; and [Biedl, LaGrange, and Spirkl, 2606.21640v1](https://arxiv.org/html/2606.21640v1), concerns bounded VC-dimension and related restricted classes. None of these supplies an exact formula for unrestricted M(n). Searches on maximum twin-width, conference-graph twin-width, universal n/2 bounds, and the small-order literature did not identify a resolution. This is a dated bounded literature search, not proof that no later or unindexed result exists. Local source PDF bytes match all three source-manifest hashes; source PDFs and extracted text are excluded from this audit packet.

## Mathematical review of every attempt

### Attempt 1

PASS. Counting, for each third vertex w, unordered pairs containing one neighbor and one nonneighbor yields the claimed sum of d(w)(n-1-d(w)). Completing the square gives the defect identity. Since the minimum is no larger than the average, the near-equality variance estimate follows with the stated direction. Equality forces both regularity and equal pair distances; solving the adjacent and nonadjacent common-neighbor equations gives the conference parameters. The hypothesis n>=2 avoids division by zero. These statements do not upper-bound later contraction widths.

The C5 example is valid: every first merge has red degree 2, so an invariant imposing the four-vertex all-black ceiling 1 on its quotient is false. The quotient has existing red edges; applying the original graph induction hypothesis to it would be invalid.

### Attempt 2

HOLD as literally defined, PASS for the intended endpoint-excluded formulation. A merged pair's interaction with another merged pair replaces its two singleton indicators by one mixed-rectangle indicator. Summing those replacements proves the formula, independent of merge order. Unmerged singletons have red degree at most the number of merged pairs. After all pairs are merged, there are ceil(n/2) parts and the trivial maximum red degree is ceil(n/2)-1=floor((n-1)/2). The even and odd singleton bounds are correct. This is a sufficient restricted search, not an equivalence to unrestricted contraction sequences.

For an involutory automorphism, cross-orbit rectangles are [[a,b],[b,a]]. Their increments are 0 or -1, and a fixed vertex is uniform to each orbit. This proves the displayed sufficient bound after correcting D_i and specifying the empty maximum if needed. No claim for arbitrary graphs follows.

### Attempt 3

PASS. The six edges define the net graph. For the specified matching the base sizes are all 2 and the update matrix has the stated cyclic signs. All six orders have successive pair-phase widths [2,3,2]. Every first merge has width at least 2; the supplied alternative pair sequence completes at width 2. The graph therefore has twin-width exactly 2. The example refutes only the arbitrary-good-matching scheduling strengthening, not the existence of another suitable matching or the original extremal problem.

### Attempt 4

PASS within the explicitly finite scope. Counts 1,2,8,64,1024,32768 sum to 33,867 labeled graphs. Exhaustive upper certificates, with the named P4, C5, and C5-plus-isolate lower witnesses, establish maxima 0,0,0,1,2,2. The n<=3 bound is correctly tightened to 0 in the second verifier. The first script's looser bound 1 at n=3 is not misreported as the exact maximum.

The seed-481 stream has exactly 250 samples at each n=7,...,12. All 1,500 returned certificates pass. Sampling with replacement is permitted and is not an exhaustive or statistical proof of a universal claim. Certificate widths need not be optimal.

### Attempt 5

PASS. In a conference graph of order 4k+1, summing the three pair disagreements over a triple gives 6k. Each mixed external neighborhood contributes 2, while the internal contribution is 2 exactly when the triple has one or two edges. Thus the stated values 3k-1 and 3k follow. For k>=2 both exceed 2k, forcing a disjoint second merge at that ceiling. The k=1 case is correctly excluded from this obstruction.

The four neighborhood classes have sizes k-1,k,k,k. Exhausting the sixteen 2-by-2 rectangles gives ten updates (0,0), two (-1,-1), two (+1,-1), and two (-1,+1). Hence precisely the listed same-C, same-E, or A-B choices are forbidden. Their total is 2k(k-1); subtracting from choose(4k-1,2) gives 6k^2-4k+1 safe disjoint second contractions after every first pair. Other singleton red degrees are at most 2. Safe second moves do not guarantee a complete bounded-width sequence.

## Independent implementation and reproduced evidence

The four README commands were run using Python 3.12.14 with normal assertions enabled, in an isolated copy. Each exited 0. The four generated JSON files were byte-for-byte identical to the frozen files. Approximate runtimes were 0.95s, 1.96s, 16.10s, and 0.04s in README order. Timing is machine-dependent.

A third implementation, `independent_verify.py`, uses explicit 0/1/red trigraph matrices and threshold feasibility search. It does not use the author's partition-red function to determine exact values. It computed exact twin-width for every labeled graph through six, compared all 33,867 values with the author's exact dynamic program, and independently verified their complete certificates. Exact counts by width were:

- n=1: width 0, 1 graph
- n=2: width 0, 2 graphs
- n=3: width 0, 8 graphs
- n=4: width 0, 52; width 1, 12
- n=5: width 0, 472; width 1, 540; width 2, 12
- n=6: width 0, 5,504; width 1, 24,240; width 2, 3,024

The independent run also checks the corrected pair identity for every subset of a fixed full matching on every labeled graph through six, the defect identity throughout, 599 qualifying involution-invariant graphs, all 1,500 sampled certificates, all sixteen rectangle types, all six bad net orders, and the three explicit lower witnesses. The matching reduction is adequate for these finite identity controls because arbitrary labelings are enumerated. The original certificate-stream hash also reproduces: `78d3bd0cf3c79e0a95b2343035ed9b6e4b58ca5f22f50b00e353a21a9f6a1d8b`.

`independent_conference.py` imports no author code. It independently verifies all first pairs, disjoint second pairs, and triples at Paley orders 5,9,13,17,29. Order 9 uses the field F3[t]/(t^2+1), rather than incorrect arithmetic modulo 9. Safe counts per first pair are 3,17,43,81,267. This adds the important k=2 boundary absent from the author's prime-only controls. At order 9, 72 triples have red degree 5 and 12 have red degree 6, both above the ceiling 4.

Code review validates the quotient recurrence, canonical partition memoization, and early stopping when a child attains the current state's unavoidable width. The pair-only search memoizes only decreasing-size states and correctly supplies partial certificates at the ceiling used here. Its base case is not a general-purpose decision procedure at an arbitrary smaller bound; supplied certificates are therefore independently completed and checked. The exact routine's initial numerical sentinel 100 is harmless in the documented small-graph domain, but should be replaced by an order-derived bound before advertising an unrestricted solver. Assertions must remain enabled in the author's scripts. These implementation scope notes do not invalidate any reported experiment.

## Portable reproduction and stopping boundary

With Python 3.10+ and only its standard library, run:

```text
python verify_readme.py /path/to/frozen/package
python independent_verify.py /path/to/frozen/package --full
python independent_conference.py
```

The first command runs all four README scripts in a temporary copy and checks output identity. The second checks the source manifest, performs the independent exhaustive audit, and confirms the source bytes are unchanged. The third is self-contained. Result JSON files are written beside the audit scripts. The public packet includes scripts, concise result files, the freeze, remote-byte verification, and this report; it contains no source PDFs, screenshots, private reports, or external account data.

Five substantive attempts remain five. Verification does not count as a new attempt. The task has not determined M(n) for every n, proved the proposed universal sharp bound, proved equality for all conference graphs, or established novelty for the partial lemmas. The only release-blocking defect found in the frozen record is H1. A full PASS requires an explicitly corrected and rehashed record, with the unresolved status retained.
