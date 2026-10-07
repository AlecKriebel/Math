# A credited subquadratic algorithm for all shortest exact-count intervals

Status: complete known-algorithm resolution in the standard real-RAM model, pending separate adversarial review. One validation/reconstruction family is recorded. The bound is \(O(n^2/\log(2+n))=o(n^2)\); no \(O(n^{2-\varepsilon})\) bound, superlinear lower bound, bit-model speedup, or novelty is claimed.

## 1. Exact source and computational model

Jeff Erickson's original [algorithmic problem page](https://jeffe.cs.illinois.edu/open/algo.html), under “A dynamic programming problem” attributed to David Eppstein, gives a sorted list of \(n\) real numbers and asks for the smallest interval containing exactly \(k\) elements for every \(1\le k\le n\). It asks for an algorithm faster than quadratic time **or** a lower bound larger than linear in a reasonable model. It does not demand a fixed polynomial saving \(n^\varepsilon\). The index page explicitly warns that its problems have not been systematically updated since2001.

We use exact arithmetic, comparison and ordinary array/index operations at unit cost on the standard real RAM. This is the model of the credited convolution theorem below. There is no assumption that coordinates are small integers, and no pseudopolynomial dependence on their magnitude. Arbitrary real inputs do not have a finite bit encoding; a separate bit-model claim cannot silently be read into this operation count.

For distinct sorted entries \(a_0<\cdots<a_{n-1}\), the answer is the familiar consecutive-window minimum
\[
L_k=\min_{0\le j\le n-k}(a_{j+k-1}-a_j).
\tag{1}
\]
We output an attaining pair of endpoints, not just its length. Closed intervals suffice: an interval containing finitely many entries can be replaced by the closed interval from its smallest included value to its largest without becoming longer or changing its included multiset.

The source does not explicitly discuss repeated values. We do not pretend that every count is then feasible. Our algorithm handles a nondecreasing list with multiplicities and reports infeasibility where necessary; e.g. for \((0,0)\), no interval contains exactly one entry. This extension agrees with (1) when the input is strictly increasing. An interpretation requiring intervals to be open only, with no attained minimum, is not imposed on the source.

## 2. Credited prior algorithm

Bremner, Chan, Demaine, Erickson, Hurtado, Iacono, Langerman, Pătraşcu and Taslakian, *Necklaces, Convolutions, and X+Y*, give a worst-case \(O(n^2/\log n)\) real-RAM algorithm for min-plus convolution. It appears as Theorem11 in the retrieved full author version, arXiv:1212.4771v1, Section4.3; the paper was published in Algorithmica69(2)(2014),294–314, following an ESA2006 version. Plus and minus formulations are equivalent by negating the second input.

The method uses Chan's high-dimensional dominance reporting lemma, Lemma2.1 of his2005 author manuscript *All-pairs shortest paths with real weights in O(n³/log n) time*, later Algorithmica50(2008),236–243. We read the relevant complete proofs, including tie treatment and the reported winning indices. The stronger matrix-product bound elsewhere in the necklace paper is unnecessary here and is not used.

Sections3–5 spell out the reduction, witnesses and a simple exact implementation of this credited method. They also avoid relying on the old problem page's obsolete open-status label. The full final publisher-layout necklace PDF was not compared with the retrieved author version; the publication venue and year are confirmed on the authors' institutional publication pages.

## 3. One masked convolution handles duplicates and endpoints

Assume \(n\ge1\). Shift all coordinates by \(a_0\), writing \(t_j=a_j-a_0\), and let
\[
R=t_{n-1}\ge0,\qquad M=3R+1,\qquad N=2n.
\]
Call \(j\) a run start if \(j=0\) or \(a_{j-1}<a_j\), and a run end if \(j=n-1\) or \(a_j<a_{j+1}\).

Build two length-\(N\) arrays, initially filled with \(M\):
\[
A_i=t_i\quad\text{if }i<n\text{ is a run end},
\qquad
B_{n-1-j}=-t_j\quad\text{if }j<n\text{ is a run start}.
\tag{2}
\]
Compute the first \(N\) min-plus coefficients, retaining the smallest minimizing first index:
\[
(C_h,i_h)=\min_{0\le i\le h}^{\rm lex}(A_i+B_{h-i},i),\qquad0\le h<N.
\tag{3}
\]
All array indices in (3) are below \(N\). For each requested count \(k\), inspect \(h=n+k-2\).

If a term in (3) uses two non-sentinel entries, write the index of the second one as \(n-1-j\). Then
\[
i+(n-1-j)=n+k-2\quad\Longleftrightarrow\quad i-j+1=k,
\]
and its value is \(a_i-a_j\). The run-start/run-end conditions ensure that \([a_j,a_i]\) contains exactly the chosen \(k\) entries, including all copies of either endpoint. Conversely, every shortest feasible interval can have endpoints at input values and must include whole runs, so every feasible optimum appears this way.

Every genuine interval length lies in \([0,R]\). A term using an \(M\) sentinel has value at least \(M-R=2R+1>R\). Thus:

- if \(C_h>R\), no interval contains exactly \(k\) entries;
- otherwise let \(i=i_h\), \(j=i-k+1\), and return \([a_j,a_i]\) of length \(C_h\).

The reduction and reconstruction take \(O(n)\) time. It works for \(n=1\), all-equal inputs, negative coordinates and multiple optimal windows. No numerical infinity or coordinate discretization is required.

## 4. Explicit witness-preserving block implementation

Here we reconstruct the credited dominance method for the finite arrays (2). All entries lie in \([-M,M]\). For out-of-range indices only, use the larger sentinel \(S=10M\). Every true coefficient (3) has a term at most \(2M\); every term involving an out-of-range index is at least \(S-M=9M>2M\). Thus the latter cannot change any answer or witness.

Let
\[
d=\max\{1,\lfloor\log_2N/16\rfloor\},
\]
and divide the first array into blocks with starting indices \(r=0,d,2d,\ldots<N\), padding the last block with \(S\). Fix an offset \(\delta\in\{0,\ldots,d-1\}\). Construct red points labeled by block starts and blue points labeled by integers \(-(N-1)\le s\le N-1\), with coordinates indexed by \(t=0,\ldots,d-1\):
\[
p_{\delta,r}[t]=(A_{r+\delta}-A_{r+t},\ \delta-t),
\qquad
q_{\delta,s}[t]=(B_{s-t}-B_{s-\delta},\ 0).
\tag{4}
\]
Each coordinate is an ordered pair compared lexicographically. The second component is merely an integer tie-breaker, not an infinitesimal real whose magnitude must be chosen.

Report all pairs with \(p_{\delta,r}[t]\le q_{\delta,s}[t]\) in every coordinate. Rearranging the first components shows that this condition means
\[
(A_{r+\delta}+B_{s-\delta},\delta)
\le_{\rm lex}(A_{r+t}+B_{s-t},t)
\quad\text{for every }t.
\tag{5}
\]
Consequently, for each pair \((r,s)\), exactly one offset \(\delta\) is reported over all \(d\) passes: the smallest-index minimizer in that block. For a report, put \(h=r+s\). If \(0\le h<N\), compare its candidate value and first index against the currently stored pair for coefficient \(h\). This returns exactly (3), with consistent leftmost witnesses.

The number of reported pairs over all passes is
\[
\lceil N/d\rceil(2N-1)=O(N^2/d+N).
\tag{6}
\]
This remains true when many real candidate values coincide: the offset tie-breaker is essential to the output-sensitive bound. Reports with \(h\) outside the desired coefficient range are discarded but are already included in (6).

## 5. Dominance routine and a complete running-time bound

For completeness, the supplied reference code implements the elementary divide-and-conquer underlying Chan's lemma. Given red and blue points in dimension \(d\), it reports all red–blue pairs satisfying coordinatewise red≤blue.

If there are no points of one color, stop. In dimension zero, output the red–blue Cartesian product. For a bounded number of points, compare all pairs directly. Otherwise sort by the last remaining coordinate, placing red before blue when that coordinate is equal, and split the sorted list in half. Recurse on each half at the same dimension, and recurse on the lower-half red points together with the upper-half blue points at dimension one smaller. The omitted cross-color direction cannot dominate. These three pair classes are disjoint, so every qualifying pair is output exactly once. Lexicographic coordinates in (4) form a total order and obey the same argument.

Here is a deliberately conservative bound that also covers sorting afresh at each recursive node. Excluding output, the recurrence has the form
\[
T_d(m)\le T_d(\lfloor m/2\rfloor)+T_d(\lceil m/2\rceil)+T_{d-1}(m)+O(m\log(2+m)).
\]
A bound
\[
T_d(m)=O(16^d m^{5/4})
\tag{7}
\]
follows by induction. Handle \(m\le16\) directly, with its \(O(dm^2)\) cost absorbed by \(16^d\). For \(m>16\), both half sizes are at most \(17m/32\), and
\[
2(17/32)^{5/4}+1/16<1.
\]
For example, the strict inequality follows from \(17^5<32\cdot15^4\). The resulting constant slack absorbs \(O(m\log(2+m))\), since \(\log(2+m)=O(m^{1/4})\). The dimension-zero and empty-color costs satisfy the same bound. Output adds \(O(P)\), because no pair is repeated.

There are \(O(N)\) points in each of \(d\) passes in Section4. Constructing their coordinates costs \(O(Nd^2)\). The dimension choice gives \(16^d=O(N^{1/4})\), so (7) and (6) bound the total by
\[
O(Nd^2+dN^{3/2}+N^2/d)=O(N^2/\log(2+N)).
\tag{8}
\]
For small \(N\), choosing \(d=1\) is absorbed by the asymptotic constant. Witness bookkeeping and endpoint recovery cost no additional asymptotic factor.

Together, (2)–(8) give the requested faster algorithm. This is a reconstruction of the established method, not a new asymptotic discovery. No fast matrix multiplication, randomization, table of nonuniform advice, or word-level operations on the input coordinates are required.

## 6. Bit complexity and verification limits

The reference implementation uses exact integer or rational arithmetic when passed those Python types. Its Python runtime is not asserted to equal a real-RAM operation count. For \(L\)-bit rational inputs, each coordinate comparison reduces to arithmetic on a bounded number of input rationals, together with \(O(\log n)\)-bit indices. This yields a polynomial-in-\(L+\log n\) overhead per real-RAM operation. We do not claim that (8) is a subquadratic bit-time bound when \(L\) grows with \(n\). The absence of a dependence on the numerical magnitude as an iteration count distinguishes this from a pseudopolynomial algorithm.

The checker compares the actual block/dominance implementation with exhaustive exact interval enumeration on small sorted inputs, including repeated values, infeasible counts and rational shifts. It also tests generic min-plus values and tie-broken witnesses against a quadratic oracle, and the dominance reporter against direct pair checks. Small overridden block sizes exercise all paths without pretending that a benchmark proves (8); the asymptotic claim is the analytic bound above.

The old alternatives were disjunctive: a faster algorithm is enough. A superlinear lower bound, a genuinely polynomial subquadratic bound and the optimal present-day min-plus-convolution complexity are not resolved or claimed here.

## Sources

1. J. Erickson, [A dynamic programming problem](https://jeffe.cs.illinois.edu/open/algo.html), original page dated5September1997; [index warning](https://jeffe.cs.illinois.edu/open/) on its non-updated status. Full relevant original text read.
2. D. Bremner et al., [Necklaces, Convolutions, and X+Y](https://tmc.web.engr.illinois.edu/convol.pdf), author version arXiv:1212.4771v1, Section4.3, Lemma10 and Theorem11. [Erickson's publication record](https://jeffe.cs.illinois.edu/pubs/necklace.html) records Algorithmica69(2)(2014),294–314 and the2006 conference version. Full author PDF retrieved; the convolution and witness proof read.
3. T. M. Chan, [All-pairs shortest paths with real weights in O(n³/log n) time](https://tmc.web.engr.illinois.edu/apsp.pdf), author manuscript dated10May2005, Lemma2.1 and Section3; later Algorithmica50(2008),236–243. The complete dominance proof was read. This is the credited divide-and-conquer dependency.
