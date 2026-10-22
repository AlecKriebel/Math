# Independent audit of binary weighted directed cycle cactus halting

## Decision

Accept the restricted theorem in the candidate note. Its algorithm decides chip-firing halting on connected loopless directed-cycle block cacti with an independent positive integer weight on each cycle, in O(n²) integer arithmetic operations and polynomial bit complexity. The proof includes both directions and valid, compact certificates. No mathematical correction is required.

This acceptance does not resolve arbitrary Eulerian multigraph halting, establish priority or novelty, certify current literature-wide openness, or turn a signed stable certificate into a legally reachable endpoint. The one-vertex degree-zero case is separately excluded from the theorem and is nonhalting under the literal zero-threshold firing rule.

The exact candidate is identified by manifest SHA256 8291a163e9c39a5212987d51ea7b6f867cb3675e0f7d3edf48cd57e597f5a3b0 and proof-file SHA256 95c07b0c2b07ec2e9b19d1496b620aab369b536f3cbfdd34eedbac91b4ca581f. All 20 manifest members were independently authenticated by byte count, hash, and exact inventory. The candidate was not modified, imported, or executed in this audit.

This AI-assisted work is unrefereed. Acceptance means an independent internal AI audit. No external human peer review, journal acceptance, or formal proof-assistant certification is claimed. The general Eulerian-multigraph target remains unresolved by this work; no novelty, priority, or exhaustive current-literature claim is made.

This edition contains the complete self-contained mathematical proof and full analytical algorithm. It is not a computational reproduction package: executable programs, raw certificate contents, and copied source documents are not distributed. Historical finite checks are supporting validation only; no omitted computational premise is needed for the theorem. Edition preparation made no new mathematical test runs, scholarly-source retrieval, visual source inspection, or literature search.

## Least action and equivalence

For a loopless digraph, suppose f is a nonnegative integer vector and s=x−Δf is coordinatewise strictly below the outdegree. If a legal firing sequence first exceeds f at v, its pre-firing count h has h_v=f_v and h_u≤f_u for every u. Nonnegative incoming arc multiplicities then give the pre-firing chip count at v at most s_v, contradicting legality. There is no use of s≥0 in this comparison.

Consequently every legal sequence has at most the sum of the entries of f firings. A maximal one must finish at a genuinely nonnegative stable configuration, even when s itself is signed. The candidate consistently distinguishes this upper-bound certificate from a reachable stable endpoint.

For the equivalence lemma, if y=x−Δg and x terminates with firing count u and stable endpoint s, then s=y−Δ(u−g). On an Eulerian graph Δ1=0, so an integral all-ones shift makes u−g nonnegative without changing the image. The preceding least-action argument proves termination of y. Exchanging x and y proves the converse. Both configurations must be nonnegative for this statement; the candidate invokes it only in the nonhalting branch, where that condition holds.

## Elimination and exact lattice membership

Each nonroot vertex has exactly one parent block. For its weight w and threshold d, the normalization chooses the largest integer below d congruent to the working value modulo w. Thus d−w≤y_v≤d−1 and b_v−y_v is divisible by w. Because d≥w, every finalized nonroot value is nonnegative. Euclidean remainders in 0 through w−1, including on negative dividends, are essential and are correctly specified.

The potential assignment follows the directed order within each block. The difference between consecutive potentials is the corresponding transfer divided by w. Hence the block's Laplacian contribution is the recorded transfer at each nonanchor and minus their sum at its anchor. At a vertex shared by blocks, child-anchor contributions cancel exactly the child transfers previously added to its working value. What remains is x_v−y_v. The same identity holds at the root. This proves ΔF=x−y over the integers, not only over the rationals.

Subtracting the minimum of F makes the firing bound nonnegative. The Eulerian all-ones kernel identity preserves ΔF. No legal path from x to the normalized vector is asserted or needed.

## Both decision directions

When the root is below threshold, the entire normalized vector is strictly below threshold. Applying signed least action with the constructed nonnegative firing bound proves halting.

When the root is active, the normalized vector is nonnegative. Fire the root first and then process blocks outward, each in directed cycle order. Every nonroot vertex begins with at least d_v−w_parent chips; its parent-cycle predecessor has already fired and supplies the missing w_parent chips before its turn. Other incoming firings cannot hurt. Every vertex therefore fires legally once. The net change is −Δ1=0. Repetition gives an infinite legal play from y, and the established equivalence transfers nonhalting to x.

This covers both root-value possibilities and neither direction relies on a total-chip threshold alone.

## Recognition and arithmetic complexity

The undirected support of a graph in the stated class has biconnected blocks that are single edges or simple cycles. Conversely, if each edge block carries equal positive opposite multiplicities, and each larger block carries exactly one consistently oriented cycle of uniform weight, the ordinary block-cut incidence structure gives exactly the required directed-cycle block tree. Thus the proposed recognition criterion is exact.

The source implementation was read in full. Its iterative depth-first low-link traversal extracts undirected biconnected components. Internal outgoing and incoming tests require one successor and one predecessor at every vertex of a block, a common weight, and a single spanning directed cycle. These tests correctly reject bidirected triangles, several directed cycles in one block, and cycles sharing more than an articulation. The later incidence traversal separately guards tree consistency and connectivity.

The adjacency scan and Eulerian row/column checks take O(n²) operations. If block sizes are k_B, the connected block structure satisfies sum_B(k_B−1)=n−1 and each k_B≥2. Therefore sum_B k_B≤2n−2 and sum_B k_B²=O(n²). This bounds the implementation's pair scans, cycle-membership scans, and sorting work as well as the graph traversal. The numerical elimination and potential assignment use O(n) arithmetic operations. The dense Laplacian certificate check and a recurrence of n firings use O(n²). The recognizer therefore does not silently expand the encoded weights or require O(n³) block inspection.

Division/remainder is counted as one exact integer operation in the stated arithmetic model. With that convention, the strongly polynomial arithmetic claim is justified. No assertion is made that the expanded firing sequence or expanded multigraph has polynomial length.

## Intermediate bit lengths

Let N be the input chip total and C=sum_v(d_v−1). All degrees are positive for a connected member with n≥2, so C≥0. An unfinalized working vertex represents a disjoint rooted region: its value equals original chips in that region minus the nonnegative, already finalized values there. Thus its value is between −C and N.

Finalized coordinates instead lie between 0 and d_v−1. They can exceed N, as the signed-root examples demonstrate. The accepted original's phrase “current vertex value” meant an unfinalized aggregate, with finalized values separately bounded. This edition adopts the optional precision: each unfinalized aggregate lies between −C and N, finalized coordinates separately satisfy 0≤y_v≤d_v−1, and every stored coordinate lies in [−C,max(N,C)]. This is a wording clarification, not a required mathematical correction.

A transfer equals the region's original chip sum minus all finalized values after including the current vertex, so its absolute value is at most N+C. The same estimate applies to the sum transferred by an entire block. The predecessor relations inside blocks form a rooted spanning tree, hence each potential uses at most n−1 increments. Since w≥1, |F_v|≤n(N+C), and after shifting, 0≤f_v≤2n(N+C).

All degree, remainder, accumulated-transfer, potential, Laplacian-product, and recurrence-check integers therefore have O(log(n+1)+log(N+C+1)) bits, with constant-factor increases for products. The case N+C=0 causes no singularity because of the +1. These estimates yield polynomial bit running time in the full adjacency-and-chip encoding.

## Explanatory families and boundary case

For the bidirected triangle of common multiplicity q, the candidate's cycle (2q,q,0) → (0,2q,q) → (q,0,2q) → (2q,q,0) is legal. The comparison (q,q,q) is stable, with the same total and coordinate residues modulo q. For the unit triangle, Δf has each coordinate congruent to minus the sum of the entries of f modulo 3, whereas (1,0,−1) does not. This proves the claimed lattice obstruction. The example refutes only the proposed residue-and-total shortcut and is outside the theorem's graph class.

For the path with edge weights M and 1, starting from (0,0,M), vertex 2 is the unique active vertex until it has fired M times. The resulting (0,M,0) is stable because the middle degree is M+1. Thus the stated terminating play has length exactly M; choosing M=2^B makes it exponential in the binary parameter length. This is compatible with compressed decision and does not imply hardness.

For a singleton loopless graph, the literal rule permits a firing at every nonnegative chip count because d=0, and that firing is the identity. The note's nonhalting convention and its explicit n≥2 theorem domain agree. The supplied solver rejects n=1 rather than pretending to cover it.

## Historical independent exact controls

The audit wrote its own normalizer, columnwise Laplacian certificate checker, exhaustive state-graph classifier, reduced-Laplacian rational solver, and small recognition oracle. No candidate module was imported or executed. The audit scripts use only the standard library and explicit exceptions, so optimization cannot remove checks.

The exact graph-family specification was reproduced, but the dynamics oracle differs materially: it constructs every legal edge of each complete finite state space. Reverse reachability computes whether a stable endpoint exists; iterative removal of states whose successors all terminate computes whether every legal play is finite. Those two independently calculated sets agree throughout. The normalizer's decision agrees with both.

The recorded historical normal, -O, and -OO runs gave these exact results:

- 177 weighted cacti and 1,208 complete fixed-total state spaces
- 53,422 initial configurations and 71,257 legal transitions
- 15,693 halting and 37,729 nonhalting configurations
- 3,328 halting certificates with negative canonical roots
- 66,862 normalization occurrences with a negative remainder dividend
- 359 independent reduced-Laplacian rational solves giving precisely the integral shifted potential
- 18 root choices and 96 relabeling controls
- Five additional large-integer cases, reaching 24,001-bit inputs, plus the exponentially long-play family at a 24,001-bit parameter
- Three supplied raw certificates checked directly with the audit checker
- Ten rejecting certificate mutations, including false equations, flipped outcomes, empty/truncated/illegal recurrences, and a negative firing bound

The audit's finite-outcome digest is ad1748d7b9a105d30bbb312d2efe349b06615df39451be1cf7ce277b63b8035f. Its serialization and enumeration differ from the candidate's digest; the coverage and outcome totals agree exactly.

A separate recognition oracle computes biconnected blocks by exhaustive vertex-subset connectivity tests, rather than Tarjan traversal. It compares the block criterion against independently generated constructions on all 16 two-vertex matrices with entries 0–3, all 729 three-vertex matrices with entries 0–2, and all 4,096 four-vertex matrices with entries 0–1. All 4,841 comparisons agree, with 3, 16, and 46 recognized graphs respectively. Eight invalid controls are rejected, including an Eulerian union of overlapping directed cycles, and a mixed eight-vertex cactus is accepted. The recognition digest is 11fb751272b6184cb630b7414ed1d90d8d392b5889151b85983d387fceb712ef.

These tests corroborate the theorem and independently inspect the supplied certificate data. They do not purport to execute or reproduce every behavior of the supplied implementation; that implementation was reviewed statically. Universal acceptance rests on the written proof, not finite tests.

## Source scope

The retained statement identifies the broad question as halting for Eulerian digraphs with multiple edges. In the retained Hujter–Kiss–Tóthmérész paper, Theorem 11 concerns prescribed-endpoint reachability, Proposition 21 supplies the co-NP side, and Problem 22 asks the broader halting question. The paper's public v4 record identifies the 4 October 2016 revision and 2017 publication. [On the complexity of the chip-firing reachability problem](https://arxiv.org/abs/1507.03209v4)

The retained Björner–Lovász manuscript gives its multiplicity-dependent game bound in Theorem 4.8 and the Eulerian bound in Corollary 4.9, followed by the additional no-multiple-edges specialization. The candidate correctly avoids using this as a binary-weight-independent firing bound. [Chip-firing games on directed graphs](http://www.cs.elte.hu/~lovasz/morepapers/abacus.pdf)

The retained Farrell–Levine text, Theorem 1.2 and Proposition 2.13, supports the coEulerian distinction and the known unweighted directed-cactus case. Its public arXiv record confirms the v3 scope and authors. A two-vertex block of weight 2 has Laplacian image 2Z(1,−1), a proper sublattice, so the candidate's weighted class is genuinely larger than that unweighted coEulerian subclass. [CoEulerian graphs](https://arxiv.org/abs/1502.04690)

This audit read the relevant retained extracted sections and checked the two public arXiv records. It did not undertake a full independent visual audit of all source PDFs or a comprehensive search of subsequent literature. The restricted proof is self-contained, and no copied source text is part of the authored audit deliverable.

## Correction disposition and distribution

No required mathematical correction was found. The accepted proof is unchanged in its mathematical hypotheses, algorithm, lemmas, decision criteria, complexity claim, and examples. The public proof incorporates the optional unfinalized-aggregate clarification stated above. Historical implementation descriptions are identified as such, and executable instructions are replaced by supporting verification prose.

PROOF.md supplies the complete analytical proof, while this document retains the complete logical audit. VERIFICATION.json records aggregate historical checks and their identities; SOURCES.json records public-source metadata and inspection limits. The original candidate and audit documents remain unchanged. No new mathematical program execution or new source inspection is claimed by this edition.
