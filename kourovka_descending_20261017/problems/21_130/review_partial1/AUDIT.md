# Independent adversarial audit of partial results

Completed 2026-10-24, 19:47 UTC. **Assigned audit completion: 100%.** This is not an estimate that the full conjecture is complete. No full resolution or originality is asserted. No external communication, commits, pushes, or releases were performed.

## Verdict and precise accepted scope

No substantive mathematical or certificate error was found in the frozen sources listed in `REVIEWED_MANIFEST.json`. Later edits are outside the original freeze; `SOURCE_DELTAS_AT_COMPLETION.json` identifies two such files. Small reviewed sources are preserved under `snapshot/`; large witness and DAG files are represented by hashes and were read without duplication.

The strongest accepted universal bounded-cardinality conclusion is: **every subset of size 3 through 7 in every finite odd-order abelian group has a cyclic ordering with distinct adjacent sums**. The size-7 statement has both a fresh independent completed search and a completely checked finite obstruction DAG. Sizes 5 and 6 received independently reproduced exact searches as well. These are finite symbolic conclusions, not a proof for arbitrary cardinality.

Other accepted partial results are the stated sparse-collision first-moment and local-lemma criteria, the large least-prime-factor rectification proposition, the listed elementary-abelian finite-field coefficient criteria, all subsets in odd abelian groups of order at most 15, and the explicitly hypothesized shared-edge fiber/product construction. Local-switch barriers and invariant cancellations are valid obstructions to particular proof routes.

The full target remains existence for **arbitrary** cardinality and **arbitrary** subsets of finite odd-order abelian groups. The accepted results leave that gap open. In particular, none establishes a general local improvement, general compatible fiber cycles, a universal coefficient nonvanishing theorem, or a general collision-cover obstruction theorem. The historically stopped unsaturated `relation_cover/result_n7.json` remains incomplete; it is separate from the completed saturated n=7 searches and DAG.

## First moment and local lemma

I checked the graph model and cancellation assumption: equal-colored simple edges sharing a vertex coincide, so every genuine repeated color is represented by disjoint edges.

The probability that a fixed disjoint edge pair lies in a uniform unoriented Hamilton cycle is exactly `4/((n-1)(n-2))`. The exceptional-looking contraction at n=4 is harmless: direct enumeration gives 2 of 3 cycles. Independent cycle enumeration through n=8 agrees with the formula. The expectation and strict first-moment sufficient condition follow. The formula for A=G of odd size also agrees with `m_s=(n-1)/2`.

For the injection local lemma, I independently enumerated the eight edge-respecting maps for each template/target pair and the domain/image support counts in examples n=4 through 7. The counts in the frozen proof are correct: `Q=n(n-3)/2`, a fixed template vertex lies in `2(n-3)` disjoint template pairs, and the number of target collision pairs incident to a is `R_a`. Summing four domain and four image support bounds gives the stated closed-neighborhood bound. Enlarging a negative-dependency graph is valid because it only reduces the collections of nonneighbors for which its condition is required. The reduction to `32 e (r-1)<n-2` is correct, including the case with no bad events.

I also read Theorem 1 and Lemma 3 in the [primary Lu–Székely paper](https://people.math.sc.edu/lu/papers/randinj.pdf). They provide precisely the canonical injection-event graph and negative-dependency local lemma required here. This is an imported theorem, not an independently proved new result.

## Rectification and local barriers

The rational rectification proof survives adversarial inspection. A nontrivial pair-sum relation has four distinct indices, norm 2, and coordinate sum zero. If a vertex difference lies in the rational row span, solve for its row coefficients on an invertible q-column minor. Cramer's rule makes `d(e_i-e_j)` an integer combination of the selected rows, with `0<|d|<=2^q<=2^(n-1)` by Hadamard. The large-prime hypothesis makes multiplication by d injective on G. The nullspace therefore avoids each coordinate-equality hyperplane. The sorted-coordinate parity-chain graph is indeed one cycle, including n=3 and n=4, and its sums are strictly increasing in the displayed edge order. Preserving original relations in the rational image has the correct implication direction.

Two-successor swaps have the stated convention: they exchange the images of two vertices of a permutation. Their two replacement colors are disjoint from the two removed colors, by cancellation and injectivity, whether or not fixed points or loops are allowed in the permutation. A full-group rainbow permutation already uses every group color, so such a swap cannot remain rainbow. Exhausting all rainbow permutations of C3, C5 and C7 checked 9, 150 and 2,793 such swaps respectively; all failed.

The insertion barrier is sound: in an odd group the total group sum is zero, so the omitted color from a rainbow cycle on G minus x is 2x. Both inserted colors differ from the removed color and from 2x. There is no spare pair of colors. This is an obstruction to extending an existing cycle by one insertion, not an obstruction to finding another cycle on G.

For the identity-trade barrier, the directed graph is balanced, including loops and parallel arcs. Its condensation has no edges: a source component has no incoming arcs, and degree balance forces no outgoing arcs. On each strongly connected block the outgoing Laplacian has positive principal cofactors counting trees directed toward the root. A nonroot has only two outgoing arc choices, so the cofactor lies between 1 and `2^(m-1)`. Subtracting the root value and applying the integer adjugate is valid for any finite abelian group. If all prime factors of the group order were coprime to that cofactor, the block values would coincide, contradicting distinctness.

I independently tested every pair of permutations pi,sigma through support k=5. All **71,382** nontrivial-block principal cofactors matched explicit outgoing-arc spanning-tree enumeration, including loops and doubled arcs. The maxima were 2,4,8,16 for k=2,3,4,5. The minimum connected cycle-trade supports for p=3,5,7,11,13 independently reproduce as 3,4,5,5,6. These minima concern connected cycle trades preserving the doubled color set; they are not a universal existence assertion.

## Polynomial claims

The two Vandermondes enforce distinct vertices and distinct sums on exactly the fixed single cycle. The grid coefficient identity is valid under the stated total-degree bound, including characteristics smaller than n: each unwanted monomial has a variable exponent below n-1, and the actual interpolation denominators are nonzero for a set of distinct field elements. The additive field representation applies to elementary abelian p-groups. It does not apply to arbitrary groups of exponent p^k or mixtures of characteristics.

I checked the antisymmetrization identity and its sign independently. The integer alternating polynomial has degree equal to that of V, so it is an integer multiple of V. Complementary Vandermonde exponent permutations give the central coefficient `(-1)^N n!`, hence `C_n=(-1)^N kappa_n`. Integer division must precede reduction modulo p; the source states this correctly.

An independent evaluation at the **different grid** `x_i=i^2+i`, summing unoriented cycles and restoring their 2n odd-n dihedral orbit multiplicities, gives exactly:

| n | C_n |
|---:|---:|
| 3 | 6 |
| 5 | 980 |
| 7 | 2,292,864 |
| 9 | 87,215,071,680 |

This reproduces the integers using a distinct grid and fewer independently constructed summands. It is not claimed to be a direct n=9 monomial expansion. The original direct-expansion code was inspected and its exponent truncation is safe because later multiplications cannot lower exponents.

The reflection sign is `(-1)^(n-1)`, so all even-n central coefficients vanish as integer identities, including after reduction to characteristic two. The exterior rotation and reversal cancellations have the claimed orbit sizes and signs. The determinant's squarefree terms can encode disconnected cycle covers. The full squarefree vertex coefficient of the trace counts exactly 2n rooted/oriented copies per Hamilton cycle for n>2; color nilpotence discards repeated colors and positive coefficients over Q prevent cancellation. The trace/log identity is valid in the stated commutative nilpotent Q-algebra. Its nonvanishing remains an exact reformulation of the missing existence claim.

## Finite witness domain and two-opt convention

I rechecked every one of the **22,028** zero-containing witness subsets of C3,C5,C7,C9,C3²,C11,C13,C15 without importing any search or verifier module. The arithmetic used direct encoded-coordinate addition. Every cycle is a permutation of precisely its subset, including its closing edge, and every adjacent sum is distinct. Exact membership, absence of duplicate masks, the size distribution `binom(q-1,n-1)`, and the total count `2^(q-1)-q` establish full normalized coverage. Translation shifts every edge sum by the same element, so it extends the result to all subsets in these groups. The listed groups exhaust odd abelian groups of order at most 15 up to isomorphism; order 1 has no eligible subset.

For the strict two-opt trap, I reconstructed neighbors by deleting each disjoint edge pair and checking both reconnections as undirected edge sets. I retained only connected 2-regular graphs. This yields exactly the same nine neighbors as the stored reversal convention, with score histogram `{3:2,4:1,5:6}`. The original cycle has score 5 and a valid rainbow cycle on the same subset exists. Thus the example falsifies strict one-move score improvement, not plateau moves or the original conjecture.

## Localized collision-cover equivalence and finite searches

The forward equivalence is sound because all actual relation rows vanish in G, and multiplication by two is invertible in a finite odd group. For the reverse, split a finitely generated quotient into its free part and its 2-primary and odd torsion. Survival after inverting two is precisely survival in the free plus odd-torsion part. A single odd modulus exceeding all absolute nonzero free difference coordinates preserves all marked differences; differences without a free component survive in the retained odd torsion. This constructs an actual finite odd group with distinct marked vertices. Extra collisions do not hurt the counterexample construction.

The torsion-order bound uses the gcd of full-rank minors of the original norm-2 generators, not arbitrary HNF rows. That gcd is at most a nonzero minor, hence at most `2^(n-1)`. A difference vanishes after localization exactly when its class is 2-primary torsion, whose order is a power of two at most that bound. Therefore the single exact membership test `2^(n-1)d in L` is valid. The same reasoning applies to collision rows. The empty lattice causes no exception.

The unsaturated branch/cache search is exhaustive: for a still-uncovered Hamilton cycle any counterexample must realize one of its listed disjoint-edge collisions, so branching on all those rows is necessary and sufficient. A forced vertex equality eliminates a branch. An exact canonical lattice cache loses no future choices. I independently implemented integer Euclidean row-Hermite reduction and back substitution in n-1 coordinates, with no SymPy or author imports. It reproduces all n=5 and n=6 states, collapsed branches, and cache counts exactly. Six hundred tests under integer elementary row operations and row permutation also checked normal-form invariance.

For n=5 an even simpler independent finite incidence check exhausts all `4^5=1024` possible four-tuple patterns. Odd-group cancellation allows at most one of the three collision relations on each four-tuple. No pattern covers all 12 Hamilton cycles; the maximum is 11. No lattice arithmetic is needed for this small case.

The saturated author's code also passes inspection. A nonzero dependence of an independent lattice basis modulo two yields an even sum; adjoining its half is an exact index-two enlargement and imposes no new relation on maps into odd groups. Repetition terminates when the basis is independent modulo two, which is equivalent to absence of 2-primary quotient torsion. The result is the unique localization saturation. The author's memo pruning is sound: every child strictly enlarges its parent lattice, so a seen ancestor cannot recur as a child; other seen states have already been exhausted in single-threaded depth-first traversal.

My independently coded saturation uses exhaustive binary row-subset enumeration instead of binary Gaussian elimination. With first-uncovered-cycle branching and no author's child heuristic, it **completes n=7** in 19,028 states, with 11,183 collapsed states, 90,803 cached revisits, and no surviving modules. This independently confirms the bounded result despite the different state counts.

Finally, I independently reconstructed and checked the complete obstruction DAG, using my own lattice and saturation routines. Certificate SHA-256 is `dff8a58679e5060b1a5254a13dc58d689fb3f1e7bbc32fb0042ff589c9fa6e30`. All **1,632 nodes, 2,304 child branches, and 20,544 forced-equality leaves** pass. At each node its cycle's 14 possible disjoint-edge collisions are covered exactly once; these account for all 22,848 branches. Every child equals the exact saturated augmented lattice, every leaf proves a marked vertex equality, all nodes are reachable from the empty root, and an independent topological check proves acyclicity. The certificate file was hash-checked again after reading.

## Fiber and product construction

The common-edge hypothesis is sufficient exactly as stated. Cutting that edge gives paths with first-coordinate internal colors avoiding c=u+v. Joins have first coordinate c; within-row colors are distinct, between-row internal colors are separated by injectivity of doubling in H, and join colors are separated by the rainbow row cycle. The construction enumerates every point once.

The punctured-fiber corollary handles H of order 1 separately, and otherwise uses the full-group mixed-radix rainbow cycle. The mixed-radix proof correctly recovers each starting coordinate from `2x_j+e_j`, including wraparound, and hence recovers the edge's starting index. The given C5 and C3² base cycles and common-edge paths are valid. I checked every D in the stated sample constructions C5×C5 (32 choices) and C3²×C3 (8 choices), plus natural mixed-radix cycles in eight groups through order 105.

The C5 prescribed-edge boundary is correct: the two eligible unoriented cycles on `{0,1,2,4}` containing `{0,1}` both repeat color 1. Thus the proof does not justify silently choosing compatible edge-containing fiber cycles. The affine-subspace corollaries follow by affine changes of coordinates, whose sum map is a common translate followed by an invertible linear map. They remain restricted structured families.

## Reproduction artifacts

Run the following from this folder with standard Python; no external packages are needed:

- `independent_audit.py`: first-moment/event counts, directed cofactors, alternate-grid coefficients, all order≤15 witnesses, and the two-opt neighbor set.
- `lattice_n5_independent.py`: all 1,024 four-tuple patterns and the explicit coverage histogram.
- `lattice_row_reproduction.py`: independent unsaturated n=5,6 searches and normal-form checks.
- `dag_certificate_audit.py`: the complete n=7 obstruction DAG, with independent arithmetic and explicit graph checks.
- `local_product_checks.py`: connected trade minima, successor swaps, product examples, and prescribed-edge boundary.

Each has a corresponding JSON result here. `lattice_n7_independent_results.json` records the additional completed saturated n=7 search made by calling `explore(7,saturate=True,time_limit=50)` from the independent lattice implementation. The code and exact certificates, rather than the descriptive percentages or completion flags alone, are the basis for acceptance.
