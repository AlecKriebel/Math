# Independent audit: obstruction to iterating unique-overlap moves

## Verdict and scope

**ACCEPTED.** The eight-vertex example has exactly four successful pressing words. Its graph under all eligible unique-overlap contiguous substitutions is exactly two disjoint edges. Its original four-deletion/four-insertion pressing-word graph is a connected four-cycle. The example therefore disproves connectivity of the specified restricted move system, even without an edit-budget bound on its moves. It does **not** disprove the original pressing-connectivity conjecture.

The authored [complete counterexample proof](UNIQUE_OVERLAP_OBSTRUCTION.md) is preserved byte-for-byte: 9,066 bytes, SHA-256 `3e811359c1080a0c31916ca8f32324120526653e6f8d4bb646aec2fd1e59afaa`. No mathematical correction was required. This audit is AI-assisted and unrefereed, not formal proof-assistant verification or a novelty assessment.

The accepted short-neighbor theorem and its full audit were read to check the exact relation between the move systems. That theorem chooses a minimum-length nonunique contiguous instructional-root interval; both one-end truncations are therefore unique. For intervals of length at most four it permits an arbitrary distinct successful replacement; for longer intervals it constructs a particular one. The present example allows **every** successful replacement on **every** interval with unique one-end truncations. Thus its move set contains the theorem's explicit minimal-interval moves. In this example the only nonunique eligible interval is the same length-two interval in each word, so both interpretations give exactly the same two edges.

The original threshold is LCS at least r−4, meaning at most four deletions and at most four insertions. Conjecture 6 on printed p.47 was independently read in Bixby, Flint and Miklós, [*Proving the pressing game conjecture on linear graphs*](https://msp.org/involve/2016/9-1/involve-v9-n1-p03-s.pdf), Involve 9 (2016), 41–56. No other external mathematical theorem is needed for this finite obstruction. In particular, it does not require the Cooper–Whitlatch characterization used in the earlier theorem.

## 1. Matrix convention, full-state success, and rank

Labels are 0 through 7; bit j in row mask i is the entry Aᵢⱼ. The matrix is

A = (248, 22, 14, 5, 3, 65, 33, 1).

Its simple edges are 03, 04, 05, 06, 07, 12, 14, 23, 56. Its only diagonal-one vertices are 1 and 2. It is symmetric and its underlying graph is connected.

All pressing arithmetic is over F₂. A legal press at a diagonal-one vertex v transforms the **entire** current matrix M to M+(Meᵥ)(Meᵥ)ᵀ. A successful word must reach the full zero matrix. An all-white but nonzero residual is a dead end, not a success. Pressed vertices become zero rows and columns and cannot be legally repeated.

Writing a legal pivot first, the current matrix is congruent to diag(1,C+bbᵀ), while the post-press matrix is congruent to diag(0,C+bbᵀ). Every press decreases rank by one. A length-eight successful word therefore proves rank eight. Independently, binary Gaussian elimination gives rank eight, and fraction-free integer determinant calculation gives det(A)=1, hence also determinant one over F₂.

## 2. Complete language and exhaustive branch proof

The complete language is

- S₀ = (1,4,0,5,6,7,2,3)
- S₁ = (1,4,0,6,5,7,2,3)
- T₀ = (2,3,0,5,6,7,1,4)
- T₁ = (2,3,0,6,5,7,1,4)

The permutations α=(1 2)(3 4) and β=(5 6) preserve every matrix entry, including the diagonal, and commute. The group they generate has four elements. The following reduced tree is complete up to that group. All listed row masks describe the full eight-by-eight state.

| Prefix | Full current row masks | Complete legal-next set |
|---|---|---|
| empty | (248,22,14,5,3,65,33,1) | 1,2 |
| 1 | (248,0,24,5,21,65,33,1) | 4 |
| 1,4 | (237,0,13,5,0,65,33,1) | 0,2 |
| 1,4,2 | (224,0,0,8,0,65,33,1) | 3 |
| 1,4,2,3 | (224,0,0,0,0,65,33,1) | none; nonzero dead end |
| 1,4,0 | (0,0,224,232,0,172,204,236) | 3,5,6,7 |
| 1,4,0,3 | (0,0,224,0,0,68,36,4) | none; nonzero dead end |
| 1,4,0,7 | (0,0,12,4,0,64,32,0) | 2 |
| 1,4,0,7,2 | (0,0,0,8,0,64,32,0) | 3 |
| 1,4,0,7,2,3 | (0,0,0,0,0,64,32,0) | none; nonzero dead end |
| 1,4,0,5 | (0,0,76,68,0,0,204,64) | 2,6 |
| 1,4,0,5,2 | (0,0,0,8,0,0,128,64) | 3 |
| 1,4,0,5,2,3 | (0,0,0,0,0,0,128,64) | none; nonzero dead end |
| 1,4,0,5,6 | (0,0,128,136,0,0,0,140) | 3,7 |
| 1,4,0,5,6,3 | (0,0,128,0,0,0,0,4) | none; nonzero dead end |
| 1,4,0,5,6,7 | (0,0,12,4,0,0,0,0) | 2 |
| 1,4,0,5,6,7,2 | (0,0,0,8,0,0,0,0) | 3 |
| 1,4,0,5,6,7,2,3 | (0,0,0,0,0,0,0,0) | success |

At the root α identifies the 1- and 2-branches. After (1,4,0), β identifies the 5- and 6-branches. Every other listed legal continuation is present in the table, with the sole displayed successful leaf S₀. Its orbit is exactly the four distinct words above. There are no unaccounted branches. Thus this is a complete elementary proof of the language, not a sampled list.

The independent literal search, without quotienting or caps, gives 51 nodes, four successful leaves, and 14 nonzero dead leaves. Taking the four-element symmetry group on prefixes yields exactly 18 orbits, and the displayed rows are precisely one representative of each. Every full state and every complete legal-next set in the author's hand table was independently verified.

## 3. Original pressing-word graph

Put P=(1,4), R=(2,3), Q₀=(0,5,6,7), Q₁=(0,6,5,7). Then Sᵢ=P Qᵢ R and Tᵢ=R Qᵢ P. The three blocks have disjoint alphabets. Their pairwise order reverses between an S-word and a T-word, so a common subsequence between the two sides lies in a single block.

Consequently the same-index cross pairs have LCS four, while the different-index cross pairs have LCS three. Within each side only adjacent letters 5 and 6 are swapped, so LCS is seven. In word order S₀,S₁,T₀,T₁ the exact matrix is

| | S₀ | S₁ | T₀ | T₁ |
|---|---:|---:|---:|---:|
| S₀ | 8 | 7 | 4 | 3 |
| S₁ | 7 | 8 | 3 | 4 |
| T₀ | 4 | 3 | 8 | 7 |
| T₁ | 3 | 4 | 7 | 8 |

At threshold 8−4=4 the edges are S₀S₁, S₀T₀, S₁T₁, T₀T₁. They form a connected four-cycle. At the stronger deficit-three threshold, only S₀S₁ and T₀T₁ remain, showing again that deficit three does not universally suffice.

The independent check computed each LCS by exhaustive intersection of subsequence sets, rather than the author's dynamic-programming implementation.

## 4. Exact restricted-move definition and full-state lifting

For a successful word W, write the matrix in W-order as UᵀU with U unit upper triangular. A source interval I of consecutive **positions** is eligible if both matrices obtained by deleting the first or the last row and column of U[I,I], then taking the corresponding Gram matrix, have exactly one successful word. The empty truncation has the sole empty word. Any successful permutation of U[I,I]ᵀU[I,I] may replace I; outside letters stay fixed and in order. Adjacency is undirected, allowing a substitution from either endpoint.

After pressing the prefix before I, the principal residual on I is precisely U[I,I]ᵀU[I,I]. If this block is B and the outside coupling is C, eliminating it leaves D+CᵀB⁻¹C. This full external Schur complement is independent of the successful internal scalar-pivot order. Thus replacement preserves every external coordinate, and the original suffix stays legal. Equality only on the chosen block would not suffice; the independent check compares the entire post-interval matrices and tests every prefix of every lifted replacement.

## 5. Proof that the restricted graph is two disjoint edges

An S-word and a T-word differ at both their first and last positions. Any contiguous substitution carrying one to the other must therefore use the whole eight-position interval.

For any of the four words, the trailing seven-by-seven root Gram matrix is the residual after its first press, restricted to the remaining coordinates. The full first coordinate is already zero. Its successful orders correspond bijectively to full words beginning with that first letter, of which there are exactly two.

The leading seven-by-seven root Gram matrix is the principal restriction of A obtained by deleting the current last letter. It is nonsingular. Any successful order of that restriction leaves a final scalar pivot equal to det(A)/det(A[restriction])=1, so appending the last letter gives a full successful word. Conversely a full word ending with that letter restricts to a successful word there. Exactly two full words have that last letter. Both one-end root truncations consequently have exactly two successful words, for every source word. The whole interval is ineligible from both sides, excluding every cross edge.

After prefix (1,4,0), the principal residual on labels 5 and 6 is I₂. Both one-coordinate root truncations are [1], uniquely pressable. Reversing the consecutive letters 5 and 6 therefore connects S₀ to S₁. The automorphism α gives the T₀–T₁ edge. These two edges exhaust the restricted graph.

For completeness the independent computation tested all 4×36=144 source-word intervals, including singletons and the whole word. Of these, 84 were eligible. Their 88 successful replacements, counting the identity replacement separately for each eligible source interval, contain precisely four nonidentity directed replacements. All four swap positions 4 and 5 (one-based positions), giving exactly the two undirected edges already proved. In each source word this is its unique minimum-length nonunique interval. There is no unseen longer eligible exchange.

## 6. Independent computation and adversarial checks

No author program was imported or executed. The independently written audit uses:

1. Complete full-matrix legal-press recursion, retaining every coordinate, and independent binary rank checks at every state.
2. Exact integer Bareiss determinants for all 256 principal submatrices, reduced modulo two. This is distinct from the author's binary permutation-expansion method. The nonsingular-principal-prefix criterion was checked on all 40,320 permutations; each of those permutations was also separately tested by direct full-state pressing.
3. Algebraic triangular-root reconstruction from A in each word order, followed by exact Gram verification. All local interval languages and both truncation languages were obtained by both direct pressing and determinant flags, without caps.
4. Full prefix legality, distinct letters, terminal zero, exact post-interval full-state equality, complete interval/replacement enumeration, and the six unordered pairwise LCS values.
5. Exact agreement with every original literal tree record, every principal-determinant parity, all four instructional roots, both end languages for all four words, both graphs, and the full nontrivial replacement list.

Fifteen negative controls were rejected: omitting a successful word; adding an illegal permutation; repeating a coordinate; confusing a locally successful proper principal block with full success; claiming rank seven; removing a reduced-tree row; omitting a legal-next vertex; altering a full-state entry; treating two truncation words as unique; changing a cross-diagonal LCS from three to four; claiming the original graph disconnected; claiming the restricted graph connected; dropping an original cross edge; changing a proof byte; and changing an initial diagonal bit.

The empty-matrix and nonsingular alternating-matrix controls also behaved correctly. All checks use explicit exceptions rather than removable assertions. Normal, `-O`, and `-OO` executions passed with certificates identical except for the recorded optimization flag.

## 7. Exact conclusion and limitations

Naïve iteration of the prior minimal unique-truncation substitutions need not leave a two-word component. This obstruction persists in the larger move system allowing arbitrary successful substitutions on all uniquely truncated intervals and no edit bound. An actual allowed original-threshold edge nevertheless crosses each restricted component.

The obstruction leaves the accepted short-neighbor theorem intact: every one of the four words still has a restricted neighbor. It does not classify four-word languages, prove general pressing connectivity, establish vertex minimality, or make a novelty claim. It does not show that all possible interval-based methods fail. A stronger argument may use nonunique end-truncation languages or other moves. The reviewed example itself satisfies the original conjecture.
