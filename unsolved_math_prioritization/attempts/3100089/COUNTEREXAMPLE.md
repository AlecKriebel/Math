# A six-vertex obstruction to total-four pressing-sequence edit connectivity

## Scope

This note proves that the following **precisely normalized statement is false**:

> For every successfully pressable bicolored graph, the graph on its successful pressing sequences, joining two sequences when their insertion/deletion distance is at most four in total, is connected.

The counterexample also fails the total-six bound. It **does not** disprove the original Bixby–Flint–Miklós conjecture, whose formal bound is four deletions **and** four insertions, or equivalently longest-common-subsequence length at least the common sequence length minus four. It also does not disprove a convention allowing unit-cost substitutions. Attribution of the total-four normalization to the authors' intended conjecture is not established here. No novelty claim is made.

## 1. The graph

Take vertices 0,1,2,3,4,5 and edges

\[
E=\{03,04,05,12,14,23\}.
\]

Only vertices 1 and 2 are initially black. Thus the underlying graph is the five-cycle
\(0,4,1,2,3,0\), with a leaf 5 attached at 0. It is connected. Its symmetric augmented adjacency matrix over \(\mathbb F_2\) is

\[
A=\begin{pmatrix}
0&0&0&1&1&1\\
0&1&1&0&1&0\\
0&1&1&1&0&0\\
1&0&1&0&0&0\\
1&1&0&0&0&0\\
1&0&0&0&0&0
\end{pmatrix}.
\]

The row bitmasks, with column \(j\) represented by \(2^j\), are
\((56,22,14,5,3,1)\).

The matrix is nonsingular: if \(Ax=0\), rows 5,4,3 imply successively
\(x_0=x_1=x_2=0\); rows 1,2 imply \(x_4=x_3=0\); and row 0 implies \(x_5=0\). Therefore \(\operatorname{rank}A=6\).

## 2. Complete successful-sequence classification

A press at a currently black vertex \(i\) acts by
\[
B\longmapsto B+(Be_i)(Be_i)^T
\]
over \(\mathbb F_2\). It clears row and column \(i\), so that vertex cannot be pressed again. All legal continuations can be listed by reading the diagonal after each operation.

The color-preserving automorphism \(\tau=(1\ 2)(3\ 4)\) fixes 0 and 5. Initially only 1 and 2 are black, so it suffices to classify all legal sequences starting with 1; the other half is obtained by applying \(\tau\).

Here is the complete branch tree for that half, including the common root. Every matrix entry can be recovered from the displayed row bitmasks. A nonzero matrix with empty legal-next set cannot be successfully continued.

| Legal prefix | Current row bitmasks in vertex order 0,...,5 | All possible next presses |
|---|---|---|
| empty | (56,22,14,5,3,1) | 1,2 |
| (1) | (56,0,24,5,21,1) | 4 |
| (1,4) | (45,0,13,5,0,1) | 0,2 |
| (1,4,0) | (0,0,32,40,0,44) | 3,5 |
| (1,4,0,3) | (0,0,32,0,0,4) | none; nonzero white edge 25 |
| (1,4,0,5) | (0,0,12,4,0,0) | 2 |
| (1,4,0,5,2) | (0,0,0,8,0,0) | 3 |
| (1,4,0,5,2,3) | (0,0,0,0,0,0) | success |
| (1,4,2) | (32,0,0,8,0,1) | 3 |
| (1,4,2,3) | (32,0,0,0,0,1) | none; nonzero white edge 05 |

Consequently the **entire** successful-sequence set is
\[
s=(1,4,0,5,2,3),\qquad t=(2,3,0,5,1,4).
\]
There are no other successful sequences, including shorter ones: the table and its automorphic image exhaust every legal branch, and only the two displayed branches reach zero. The full tree has 19 nodes, two successful leaves, and four nonzero all-white dead ends.

## 3. Their exact edit distance

Partition the letters into ordered two-letter blocks
\[
P=(1,4),\qquad Q=(0,5),\qquad R=(2,3).
\]
Then \(s=PQR\) and \(t=RQP\). The internal order within each block agrees, but the order of every pair of distinct blocks is reversed. A common subsequence cannot use letters from two different blocks. Thus its length is at most two, and each of \(P,Q,R\) is a common subsequence of length two. Hence
\[
\operatorname{LCS}(s,t)=2.
\]

For words of common length \(r\), their insertion/deletion distance is
\(2(r-\operatorname{LCS})\): the letters retained by any edit script form a common subsequence, giving the lower bound, and retaining a longest common subsequence attains it. Here the distance is exactly
\[
2(6-2)=8.
\]

Therefore the graph on successful sequences using at most four total insertions/deletions consists of two isolated vertices. The same is true with a total-six threshold. At the original Bixby–Flint–Miklós threshold of eight total, its two vertices are adjacent.

If a single-letter substitution costs one, four substitutions transform \(s\) into \(t\), since their positions 3 and 4 agree and the other four positions differ. Hence this example cannot be used to refute that edit convention.

## 4. What the sources actually specify

- Joshua Cooper and Jeffrey Davis, *Successful Pressing Sequences for a Bicolored Graph and Binary Matrices*, June 20, 2015, Conjecture 1, printed p.3, uses the phrase “at most four deletions or insertions” and attributes the conjecture to Bixby–Flint–Miklós. The following paragraph repeats the same prose. The inspected manuscript provides no separate formal metric or longest-common-subsequence normalization clarifying whether four is a combined budget or a budget of each kind. A literal combined-budget interpretation is refuted above; intended-author attribution remains uncertain. [Author-hosted manuscript](https://people.math.sc.edu/cooper/pressing.pdf)
- Eliot Bixby, Toby Flint and István Miklós, *Proving the pressing game conjecture on linear graphs*, Involve 9 (2016), 41–56, Conjecture 6, printed p.47, explicitly requires longest-common-subsequence length at least the common length minus four. Its immediately following explanation specifies removing up to four vertices and adding up to four. Theorem 7, printed p.48, proves the stronger minus-two bound for linear graphs. The counterexample here is not linear. [Published paper](https://msp.org/involve/2016/9-1/involve-v9-n1-p03-s.pdf)
- Cooper's author-maintained problem list says “at most 4 one-letter edits,” without defining the edit operations there, and says “valid” rather than “successful.” Accordingly the unqualified list wording must not silently be identified with the normalized statement refuted in this note. [Problem list](https://people.math.sc.edu/cooper/combprob.html)

## 5. Exact computational cross-checks

The proof above is independent of software. Two independently authored implementations provide checks:

1. A C++ bitmask rank-one-update search found the matrix and enumerated its two successful words.
2. A separate Python dense-entry update implementation enumerated every node of the complete legal tree. It additionally tested all 720 permutations using a different criterion: every leading principal determinant equals one. Those determinants were computed directly by the Leibniz sum modulo two, without using the pressing update or Gaussian-elimination determinant calculation. Exactly the same two permutations pass.

The Python certificate also computes common subsequences directly and verifies nonsingularity by binary row reduction. The checked results are summarized in `AGGREGATE_CHECKS.json`. Independently rerunning all symmetric binary matrices on one through five vertices in the new C++ implementation finds no total-four counterexample, agreeing with the prior bounded screen. No minimum-order claim is accepted here; the independent audit did not rerun those smaller-order searches.

The original eight-total conjecture remains unresolved by this work.
