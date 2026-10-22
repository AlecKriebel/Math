# Independent audit: a six-vertex pressing-sequence normalization obstruction

## Verdict and exact accepted scope

**PASS, restricted to the explicitly normalized mathematical statement.** The graph below has precisely two successful pressing sequences. Their insertion/deletion distance is eight. Consequently its successful-sequence graph is disconnected at either a total-four or a total-six insertion/deletion threshold.

**This is not a refutation of Bixby–Flint–Miklós Conjecture 6.** That conjecture explicitly permits four removals and four additions. The two words are adjacent at its threshold. They are also adjacent if four unit-cost substitutions are permitted. The literal state space of all legal finite prefixes is connected by deletion to the empty word. The source-list wording therefore cannot be declared resolved without specifying both the state space and metric.

No novelty, comprehensive literature coverage, or independent minimality claim is made. The source ambiguity is a blocker to attributing the normalized disproof to the intended original conjecture. The obstruction itself is unconditional and fully proved below.

## Independent proof

Let the vertex set be `{0,1,2,3,4,5}`. Take simple edges

`{03,04,05,12,14,23}`

and black vertices `{1,2}`. This is the five-cycle `0,4,1,2,3,0` with a leaf `5` attached at `0`. It is connected and initially has a black vertex. With a black diagonal entry equal to one, its binary augmented adjacency matrix is

```
0 0 0 1 1 1
0 1 1 0 1 0
0 1 1 1 0 0
1 0 1 0 0 0
1 1 0 0 0 0
1 0 0 0 0 0
```

The row masks, with bit `j` representing column `j`, are `[56,22,14,5,3,1]`. Symmetry is immediate. From `Ax=0`, rows 5, 4, and 3 give respectively `x0=x1=x2=0`; rows 1 and 2 then give `x4=x3=0`; row 0 gives `x5=0`. Thus `rank(A)=6`.

For a legal press at `v`, let `c` be the current column `v`. Toggling the closed neighborhood and its induced edges replaces the matrix by `A+ccᵀ` over the binary field. The diagonal at `v` must be one. Its row and column become zero, and stay zero under every later press. A vertex cannot be pressed twice. If the pivot is moved first, the matrix has block form `[1 bᵀ; b C]`; invertible simultaneous row/column operations give `diag(1,C+bbᵀ)`, whereas pressing gives `diag(0,C+bbᵀ)`. Every legal press therefore drops rank by one.

Here is the **entire** legal-prefix tree, independently reconstructed without the discoverer's code. Each row lists all legal next presses; hence every legal branch is included. A nonzero state with no available press is an unsuccessful terminal state, not a successful sequence.

| Prefix | Current row masks | Legal next |
|---|---|---|
| empty | 56,22,14,5,3,1 | 1,2 |
| 1 | 56,0,24,5,21,1 | 4 |
| 1,4 | 45,0,13,5,0,1 | 0,2 |
| 1,4,0 | 0,0,32,40,0,44 | 3,5 |
| 1,4,0,3 | 0,0,32,0,0,4 | none, nonzero |
| 1,4,0,5 | 0,0,12,4,0,0 | 2 |
| 1,4,0,5,2 | 0,0,0,8,0,0 | 3 |
| 1,4,0,5,2,3 | 0,0,0,0,0,0 | success |
| 1,4,2 | 32,0,0,8,0,1 | 3 |
| 1,4,2,3 | 32,0,0,0,0,1 | none, nonzero |
| 2 | 56,24,0,11,3,1 | 3 |
| 2,3 | 51,19,0,0,3,1 | 0,1 |
| 2,3,0 | 0,32,0,0,48,50 | 4,5 |
| 2,3,0,4 | 0,32,0,0,0,2 | none, nonzero |
| 2,3,0,5 | 0,18,0,0,2,0 | 1 |
| 2,3,0,5,1 | 0,0,0,0,16,0 | 4 |
| 2,3,0,5,1,4 | 0,0,0,0,0,0 | success |
| 2,3,1 | 32,0,0,0,16,1 | 4 |
| 2,3,1,4 | 32,0,0,0,0,1 | none, nonzero |

The color-preserving automorphism `(1 2)(3 4)` interchanges the two halves. The 19 nodes comprise six terminal branches: four failures and two successes. Therefore all successful words are exactly

`s=(1,4,0,5,2,3)` and `t=(2,3,0,5,1,4)`.

Write `P=(1,4)`, `Q=(0,5)`, and `R=(2,3)`. Then `s=PQR` and `t=RQP`. The order of any two distinct blocks is reversed, so a common subsequence cannot take letters from more than one block. Each block itself is a common subsequence. Hence the longest common subsequence has length two, and the three longest common subsequences are exactly `P,Q,R`.

For equal-length words of length `r`, insertion/deletion distance is `2(r-L)`, where `L` is longest-common-subsequence length. In any edit script, retained original letters appear in order in both words; at most `L` can survive. Thus at least `r-L` deletions are necessary, and equal final length requires equally many insertions. Conversely, retain a longest common subsequence, delete the other letters, and insert the needed letters. For these words this gives distance `2(6-2)=8`.

There are only two successful states, so no intermediate successful state can connect them at total budget four or six. At total budget eight there is a direct edge. Four substitutions also suffice, at the first, second, fifth, and sixth positions; a separate dynamic-programming check finds exact unit-substitution Levenshtein distance four. Intermediate character edits need not themselves be successful states for the distance of a single edge; only edge endpoints are states of the reconfiguration graph.

If every legal finite prefix is instead a state, deleting the final letter of any nonempty legal word leaves a legal word. Repetition reaches the empty word, proving connectivity with single-deletion edges for every graph, independently of this example.

## Source normalization and historical status

1. **Bixby–Flint–Miklós, 2013 preprint and 2016 publication.** Conjecture 6 in the published paper, printed p.47, uses `LCS ≥ r−4`; its explanation gives separate budgets of four deletions and four insertions. Theorem 7, printed p.48, proves `LCS ≥ r−2` for linear graphs. These thresholds differ by a factor of two in total insertion/deletion cost. The preprint has the same bounds. The present graph contains a cycle and a degree-three vertex, so it is outside the linear-graph theorem. [Published paper](https://msp.org/involve/2016/9-1/involve-v9-n1-p03-s.pdf), [preprint](https://arxiv.org/abs/1303.6799).

2. **Cooper–Davis, author-hosted June 2015 manuscript and latest arXiv v5.** Conjecture 1 on printed p.3 uses “at most four deletions or insertions,” and attributes the statement to Bixby–Flint–Miklós. The adjoining text repeats this wording, without a separate formal distance or LCS definition. A combined-budget interpretation is the precisely normalized statement refuted above, but the attribution to the larger-budget original means intended equivalence cannot be assumed. Latest v5 retains the same wording and explicitly expresses doubt for general graphs. The internal typeset date of a regenerated PDF is not an arXiv revision date. [Author-hosted manuscript](https://people.math.sc.edu/cooper/pressing.pdf), [v5 PDF](https://arxiv.org/pdf/1502.07450v5).

3. **An important superseded claim.** Version 1 claimed a two-edit theorem and, in Theorem 10, connectivity by adjacent transpositions. Version 2's public notice says it was withdrawn to verify a proof. Version 5 omits the general connectivity theorem. In the v1 argument, permutation conjugation is claimed to preserve triangularity, which is false in general: swapping both coordinates of `[[1,0],[1,1]]` produces `[[1,1],[0,1]]`. This is an independently identified flaw, not an asserted explanation from the authors for withdrawal. The older claimed theorem is not a valid prior resolution and supplies no established novelty conclusion. [v1 PDF](https://arxiv.org/pdf/1502.07450v1), [withdrawal notice](https://arxiv.org/abs/1502.07450v2), [version history](https://arxiv.org/abs/1502.07450).

4. **Cooper's problem list.** The page says valid sequences and leaves its one-letter edit operations undefined. Literal legal-prefix states yield the elementary positive result above; successful states with insertion/deletion-only cost yield the negative result; allowing substitutions does not give a counterexample from this graph. These alternatives must remain separate. [Problem list](https://people.math.sc.edu/cooper/combprob.html).

5. **Later primary-source check.** Miklós's June 2022 doctoral thesis, Chapter 9, Conjecture 2 on printed pp.169–170, again uses `LCS ≥ r−4`. Its selected text was inspected through the web PDF service, while local download failed; no local PDF hash or complete-thesis review is claimed. The published Cooper–Davis article is bibliographically verified as *Linear Algebra and its Applications* 490 (2016), 162–173; its publisher full-text page was blocked, so this audit does not assert that its exact conjecture wording was inspected. [Thesis](https://real-d.mtak.hu/1570/7/dc_2046_22_doktori_mu.pdf), [published article](https://doi.org/10.1016/j.laa.2015.11.001).

## Prior-result search and limits

A bounded search on 11 October 2026 used pressing-sequence/game queries combined with counterexample, connectivity, six, two sequences, cycle, pendant, and pan graph. Primary material checked included the sources above, selected introduction/conclusion sections of *Uniquely Pressable Graphs*, and selected definitions, figures, and concluding questions of *A New Characterization of V-Posets*. Figure 2 of the latter was visually inspected: it has four vertices and is not the present six-vertex graph. No inspected source or search result identified this exact graph or result. This is **not evidence sufficient to claim novelty or absence from all prior literature**. [Uniquely Pressable Graphs](https://arxiv.org/abs/1706.07468), [V-Posets](https://arxiv.org/abs/1810.07276).

## Verification design and reproducibility

The independent verifier has explicit exception-based checks, with no reliance on Python assertions. It checks:

- the graph, colors, symmetry, connectedness, full rank, and automorphism;
- every branch by dense entrywise rank-one matrix updates;
- the same entire tree by a separately written edge-set/color-set symmetric-difference implementation;
- all 720 vertex permutations using full rank of every leading principal submatrix, without pressing updates;
- common subsequences by direct subset enumeration, and insertion/deletion and substitution distances by dynamic programming;
- all four metric/state-space conventions;
- nine negative controls, including missing branches, wrong transitions, wrong LCS, false original-conjecture refutation, and false novelty claims;
- exact byte counts and SHA-256 hashes of seven locally inspected PDFs when supplied privately.

Runs under normal Python, `-O`, and `-OO` all pass, including the negative controls. Third-party source code and the discoverer's implementation were not executed. The mathematical proof does not depend on the computational cross-checks. Smaller-order exhaustive searches reported by other work were not independently rerun here and are not part of this acceptance.

The reviewed proof was 7,337 bytes with SHA-256 `290d1fbf73dd17543204039648693f28afbd2d75dcd393aeae731c6b5ab9208a`. This audit accepts its core theorem and its explicit scope restrictions. Publication or status labels must retain those restrictions.
