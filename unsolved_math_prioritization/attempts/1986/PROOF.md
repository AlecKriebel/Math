# EP195 / 1986: partial research on integer 4-AP avoidance

This is an AI-assisted, unrefereed research edition. The independent check described here is an internal AI audit, not external human peer review or formal proof-assistant certification. Source results retain their named attribution. No novelty claim is made. This prose-and-metadata edition is not a computational reproduction package: code, raw result files, copied source documents, source text, and images are not distributed. Historical execution and inspection statements describe the authenticated research and audit records; no mathematical code or formalization was rerun during publication preparation. Hashes authenticate bytes, not mathematical truth. The complete written mathematics is retained below, with the single safe-prefix orientation correction disclosed in ACCEPTANCE.md and nonmathematical publication edits.

## Outcome and exact scope

**Partial research, not a solution of EP195.** The target is a bijection from the nonnegative index set onto **all of Z**, avoiding subsequences `(a,a+d,a+2d,a+3d)` for both signs of `d != 0`. No such construction and no universal 4-AP forcing proof is established here. The remaining universally forced threshold for this target is **3 or 4**. No conclusion below is transferred to a doubly infinite permutation or an arbitrary linear order.

The main useful results of this pass are:

1. A material source update: Ho's September 2026 paper proves 4-AP avoidance on the **nonnegative/positive integers**, following the August density paper. The written proof has been read in full. It does not state the all-integer result.
2. A proof that Ho's **fixed reverse-binary tail invariant cannot exhaust Z**, together with an exact signed parity-splice criterion and an obstruction to repairing the proof merely by adding an absolute-value buffer.
3. Explicit finite-prefix obstruction certificates, a general residue-grouped shell obstruction, and an exact compactness formulation that identifies the missing uniformity in finite search.
4. A self-contained verification of the known bounds: an elementary 3-AP forcing proof and a corrected/streamlined proof of Adenwalla's 5-AP-avoiding construction. That construction contains an explicit infinite family of 4-APs.

These authored deductions are not accompanied by a novelty claim. There has been no independent expert review or formal verification. Source-author Python/Lean/build code has not been executed. The research phase made no public repository mutation or queue change.

## 1. Source authentication and source-status change

The research used authenticated source snapshots. Public scholarly-source identities and the historical inspection limits are recorded in SOURCES.json; byte authentication does not certify a theorem.

The following source distinctions matter:

- Sarosh Adenwalla, *Avoiding Monotone Arithmetic Progressions in Permutations of Integers*, arXiv:2211.04451v7 (23 July 2024), Theorem 1: an omega-permutation of Z avoiding 5-APs. The journal article is *Discrete Mathematics* 347 (2024), 114183, DOI 10.1016/j.disc.2024.114183. The arXiv proof on PDF pages 3–5 was inspected and is reconstructed in Section 7 below.
- Jesse Geneson, *Density bounds for permutations avoiding monotone arithmetic progressions*, arXiv:2608.12604v1 (12 August 2026): the density parameters for length four have supremum one. Its explicit statement after Corollary 1.3 says this does not produce a 4-AP-free omega-permutation of N or Z. The finite-parameter construction still has gaps. Section 5's avoidance mechanism was inspected; the entire paper was not audited.
- **Boon Suan Ho, *A 4AP-free permutation of the positive integers*, arXiv:2609.12780v1 (11 September 2026).** This newly found five-page manuscript gives an actual omega-permutation of N0 and hence N avoiding 4-APs, explicitly allowing negative common differences. The whole written proof, including Lemmas 1–2 and the exhaustion argument, was inspected. It does not prove the target over Z. The downloaded PDF is 404497 bytes, SHA-256 `42f3878948d2e26c5085cd36c2eb585174ba2ea85ee06cb87c1f9e29ce1e090b`.
- A later public repository, `coleski/erdos196`, gives a related adaptive binary-tree proof for N0 and reports a Lean formalization, while acknowledging Ho's priority. Its complete human proof was read. Its formalization/build claims were **not independently executed or certified here**.

Primary links:

- https://arxiv.org/abs/2211.04451v7
- https://doi.org/10.1016/j.disc.2024.114183
- https://arxiv.org/abs/2608.12604v1
- https://arxiv.org/abs/2609.12780v1
- https://github.com/boonsuan/4ap
- https://github.com/coleski/erdos196/blob/main/FINAL-HUMAN-PROOF.md

A fresh direct tracker open returned HTTP 403. Search-index material still describes EP195 as open, but its crawl predates Ho's paper. It is not used as proof of current completeness. Bounded fresh searches located the positive-integer result but no all-integer resolution. This is a limited literature search, not a claim that no such result exists anywhere.

## 2. Binary orders and the finite-to-omega distinction

At the least binary digit where two distinct integers differ, either prefer 0 or prefer 1. Binary digits of negative integers are understood 2-adically; any pair of distinct integers has a finite least differing digit. Allowing a separate preference at each residue-tree node also defines a strict total order. Comparisons are lexicographic on the infinite least-significant-first bit strings, so transitivity follows by the first differing coordinate argument.

For a nonconstant AP with difference `d`, put `v = v2(d)`. Its terms agree below bit `v` and alternate at bit `v`. Consequently the middle of a 3-AP is either before both endpoints or after both. Every such binary-tree order is 3-AP-free. Moreover, for four consecutive AP terms `(a,b,c,d)`, the pairs `(a,b)` and `(c,d)` have the same first differing node and orientation, because `c-a = d-b` is twice the common difference. Thus

`a <_T b` if and only if `c <_T d`.

If a finite set is ordered by `T`, followed by its complement in the reversed tree order, the resulting total order avoids 4-APs: neither part contains a 3-AP, and a potential 2+2 split contradicts the pair identity. **This total order need not have type omega.**

In particular every finite interval has a 3-AP-free permutation, but this alone supplies no 3-AP-free enumeration of Z. The relevant missing property is finite predecessor sets, not local absence of APs.

## 3. What the September N construction does, and why its literal Z transfer fails

Ho fixes the reverse binary order `triangleleft` that prefers bit 1 at every node, so odd numbers precede even numbers. A finite prefix is safe when appending all unused nonnegative integers in this fixed order produces a 4-AP-free total order. A finite set listed in the reverse of `triangleleft` is safe by the preceding two-order argument; listing it in the same order as the tail is not sufficient. His extension induction decreases the maximum old prefix entry under parity normalization. The new odd buffer is inserted before the new even suffix; crucial inequalities use nonnegativity of earlier AP terms. Nested safe prefixes cover every nonnegative integer, with each finite position fixed permanently.

This is a genuine one-sided construction on N0. It supersedes any statement that the positive-integer 4-AP question is still open. The proof's domain restriction cannot be removed silently: its bounds `d = 2c-b <= 2c` and `c = 2b-a <= 2b` use `a,b >= 0`.

### Proposition 3.1: no fixed reverse-binary safe exhaustion of Z

Extend Ho's same fixed order `triangleleft` to Z. There is no nested exhaustive sequence of finite words P for which every completion `P ; (Z minus P in triangleleft)` is 4-AP-free.

**Proof.** Suppose an exhaustive chain exists. After the finite position of `-1`, some positive integer larger than every value preceding `-1` must appear. Choose a stage containing such a value and let M be the largest value in that stage. Then `-1` precedes M. Both `2M+1` and `3M+2` are larger than M, so are in the tail. Put `t=M+1>0`, and `v=v2(t)`. The numbers `2M+1=2t-1` and `3M+2=3t-1` have identical bits below v; at bit v the former has 1 and the latter 0. Hence `2M+1 triangleleft 3M+2`. The completed order contains

`-1, M, 2M+1, 3M+2`,

a 4-AP of nonzero difference M+1. Contradiction. ∎

Already the safe singleton prefix `(-1)` has no safe finite extension, in this invariant, containing a nonnegative integer. The same record argument uses its maximum M. This is an obstruction to a specified proof invariant, **not** a proof that every integer permutation contains a 4-AP.

### Proposition 3.2: exact residual in a signed parity splice

Let P be a finite prefix with a 4-AP-free completed order on Z. Its old tail has all parity-A values before all parity-B values, where A and B are the two distinct parity classes. Let U be a finite list of new A values and V a finite list of new B values. Form

`P ; U ; V ; A-tail ; B-tail`,

where the tails are the unused values of their respective parity classes. Assume:

1. There are no repetitions, and each completed parity restriction is 4-AP-free.
2. The old completion of P was 4-AP-free and had the same root preference A before B.
3. With `M=max({|p|:p in P} union {0})` and `H=max({|v|:v in V} union {0})`, every A integer of absolute value at most `2H+M` is already in `P union U`.

Then the new completed order is 4-AP-free **if and only if** for every `u in U` and `v in V`,

`2v-u belongs to P union U`, or `3v-2u belongs to P union V`.       (R)

If (R) fails, the explicit forbidden progression is

`u, v, 2v-u, 3v-2u`.

**Proof.** An even-difference AP is excluded by a parity restriction. For an odd-difference AP `(a,b,c,d)`, the old-prefix entries form an initial segment. Three or four old entries contradict old safety. With exactly two old entries, the pattern ABAB already contradicts old tail order. The remaining pattern BABA has c in V (B-tail cannot be followed by A) and d in A-tail. But `|d|=|2c-b|<=2H+M`, contrary to the buffer.

With at most one old entry and pattern BABA, b must lie in U, c in V, and d in A-tail. The first term a must be old, since a new B cannot precede U. Hence `d=(3c-a)/2` has absolute value at most `(3H+M)/2<=2H+M`, again impossible.

With at most one old entry and pattern ABAB, b lies in V, c in A-tail, and d in B-tail. If a were old, `|c|=|2b-a|<=2H+M`; therefore a lies in U. This is exactly the failure of (R). Conversely failure of (R) puts the displayed four distinct AP terms in U, V, A-tail, B-tail in that order. The difference v-u is odd and nonzero. ∎

In the residual case, `|c|>2H+M`, while `a=2b-c` has the opposite sign to c and `d=2c-b` has the same sign as c. Thus it is specifically a cross-sign cancellation that the N proof does not encounter.

**Sharp tiny example.** P is empty, A is odd, U=(1), B is even, V=(0), and both tails use the reverse binary order. Both parity completions are safe (each is a singleton completion), and the absolute buffer for M=H=0 is vacuous. Nevertheless the full completion contains `(1,0,-1,-2)`.

### Proposition 3.3: a large absolute-value buffer cannot repair this merge

Under the same finite sets, suppose V has at least two distinct elements and `P union U` contains every A integer with absolute value at most `K=2H+M+2`. Then (R) is impossible, regardless of the within-parity orders.

**Proof.** Let `u_- = min U`, `u_+ = max U`, `v_- = min V`, `v_+ = max V`. The buffer and parity spacing imply

`u_- <= -2H-M-1`, and `u_+ >= 2H+M+1`.

For `(u_-,v_+)`, the number `3v_+-2u_-` exceeds both H and M, so it is outside P and V. Also `2v_+-u_->M`. Condition (R) therefore forces `2v_+-u_-` into U, giving `u_-+u_+ >= 2v_+`. Applying the same argument at the other extreme, `3v_--2u_+` is less than both `-H` and `-M`, and `2v_--u_+<-M`. Thus (R) forces `2v_--u_+` into U, giving `u_-+u_+ <= 2v_-`. This contradicts `v_-<v_+`. ∎

So adding a symmetric buffer to the N parity merge is not a missing routine estimate: for two new B values it is structurally incompatible with finite completion. A genuinely different invariant, splice, or extension scheme would be needed. This does not rule out adaptive binary-tree strategies generally.

## 4. Finite-prefix obstruction certificates

Let P be a finite word of distinct integers, and let S be its support. Necessary conditions for P to be an initial segment of a 4-AP-free permutation of all Z are:

- P itself contains no 4-AP.
- Every ordered 3-AP `(a,b,c)` in P has its continuation `2c-b` already in P, and that continuation cannot occur after c.
- For every ordered pair `(a,b)` in P whose continuations `c=2b-a`, `d=3b-2a` are both outside S, impose the directed requirement **d before c** on the future values. This finite directed graph must be acyclic.

These statements follow directly by placing the missing terms later. They are necessary, not claimed sufficient.

### Exact test when a fixed binary tail is specified

If the prospective tail is a specified 3-AP-free binary order T, the finite checks become sufficient as well: require no 4-AP inside P, no ordered triple in P whose fourth continuation lies outside P, and require every demand edge to agree with T. A putative 4-AP has 4, 3, 2, 1, or 0 entries in P; the first three cases are exactly those tests, and the last two would contain a 3-AP wholly in the tail. Thus safety relative to this fixed infinite completion is decidable by finitely many arithmetic/order checks. It still does not imply extendibility while exhausting Z, as Proposition 3.1 demonstrates.

### A two-cycle invisible to a 3-AP-free-prefix test

`P=(-2,-1,3,2)` is 3-AP-free. Its ordered pair `(-2,-1)` forces `1 before 0`; its ordered pair `(3,2)` forces `0 before 1`. Thus P cannot be extended to an avoiding enumeration containing both 0 and 1. Equivalently, one of `(-2,-1,0,1)` and `(3,2,1,0)` is unavoidable after that prefix.

Every two-cycle in this demand graph has this six-term geometry. If missing distinct values are x,y, the two forcing ordered pairs must be

`(3x-2y, 2x-y)` and `(3y-2x, 2y-x)`.

For `y=x+t`, the six values are `x-2t,x-t,x,x+t,x+2t,x+3t`; the two external pairs point inward. All four prefix values are distinct, so this type of certificate needs at least four prefix entries.

### Checking two-cycles alone is insufficient

`P=(-2,-3,-1,9,6)` is also 3-AP-free. The pairs `(-2,-1)`, `(-3,-1)`, `(9,6)` force respectively

`1 before 0`, `3 before 1`, `0 before 3`.

The complete demand graph has no two-cycle; its minimum cycle length is three. Thus a procedure checking only immediate missing endpoints and two-cycle obstructions still accepts dead prefixes. The complete graph, its edge certificates, and the finite verification were recorded in the historical research checks; those raw result files are not distributed in this prose edition. The independent audit retains the edge counts and cycle findings.

## 5. A general obstruction to residue-grouped geometric shells

Consider a block concatenation enumerating Z in radial shells. For one shell B, suppose the earlier shells contain all integers of absolute value below R, B contains the positive interval `[R,Rnext)`, the immediately preceding shell contains `[Rprev,R)`, and

`R >= 3 Rprev`, `Rnext >= 3 R`.

Suppose also that every integer in `[0,Rprev)` occurs before the immediately preceding shell. If B groups all its entries by residues modulo an integer `m` with `2<=m<=Rprev`, placing complete residue classes in some fixed order, then the whole permutation contains a 4-AP, independent of the within-residue orders.

**Proof.** Select two different residues r,s with the r-class earlier than the s-class. Set

`a = (3r-2s) mod m` in `[0,m)`, and choose `b congruent 2r-s (mod m)` with

`ceil((R+a)/2) <= b < R`.

Such a b exists: the interval has at least m integers, since `a<=m-1` and `R>=3m`. It is at least `R/2>=Rprev`, so b lies in the preceding shell, strictly after a. Put `c=2b-a` and `d=3b-2a`. Then `R<=c<d<3R<=Rnext`, while `c congruent r` and `d congruent s`. Consequently c precedes d in B. Hence `(a,b,c,d)` is a 4-AP in time order. ∎

This rules out a broad simple repair of the known shell construction, including fixed small moduli and many variable moduli. It does **not** apply to arbitrary block orders, arbitrary permutations, or the gapped density construction. The support and chronology hypotheses are indispensable.

## 6. An exact compactness target for future finite search

There is a 4-AP-free omega-permutation of Z **if and only if** there is a function `B:Z -> N0` such that, for every N, `[-N,N]` has a 4-AP-free finite ordering in which every x in that interval has at most B(x) predecessors.

**Proof.** Restricting an avoiding enumeration gives the forward direction, with B(x) its global position. Conversely, choose such finite orders for arbitrarily large N. Diagonalize over the countably many pairs of integers, retaining a subsequence on which each pair comparison stabilizes. The limit is a strict total order: transitivity and totality are finite conditions and hold in sufficiently late finite orders. No 4-AP can occur because its six pair comparisons would hold eventually. If x had B(x)+1 distinct predecessors, these finitely many comparisons would also hold eventually, contradicting the finite rank bound. Every element therefore has finitely many predecessors. The rank equal to its predecessor count is an order-preserving bijection to N0: its image is an infinite initial segment, since predecessors of an element of rank q have exactly ranks 0 through q-1. Thus the limiting order has type omega. ∎

The unknown is the existence of **one compatible family of uniform predecessor bounds**, not whether individual finite intervals admit avoiding orders. The same finite question for 3-APs always has a positive answer, while the omega version is impossible. For example, in any 3-AP-free order on `[0,N]` with 0 first, the ranks of `1,2,4,...,2^L` must strictly decrease, where `L=floor(log2 N)`. Hence the rank of 1 is at least L+1 and escapes every fixed bound.

## 7. Self-contained verification of the known 3/5 bounds

### 7.1 Every omega-permutation of Z contains 3-APs

Fix any value a and any nonzero q. The distinct values `a+2^j q` eventually all appear after a: only finitely many values precede a. Their positions cannot be eventually strictly decreasing, since positions are nonnegative integers. Thus there are infinitely many j with

`position(a) < position(a+2^j q) < position(a+2^(j+1) q)`.

Each such triple is a nonconstant AP. This establishes the lower bound 3 directly, without a finite-search or density inference.

The argument does not force length four through one anchor. In fact, there is an omega-permutation of Z with 0 first and `3x before 2x` for every nonzero x. Write `x=2^v u`, u odd, and group integers by the odd signed terminal value `t=3^v u`. Order fibers by increasing |t|, choosing the positive fiber before the negative one at each magnitude; each fiber is finite, with v from 0 to `v3(|t|)`. Inside a fiber order by increasing v. The values 3x and 2x have the same terminal value and valuations v and v+1, respectively. Each element has finitely many predecessors, and all integers occur. Therefore no AP `(0,x,2x,3x)` appears in order.

Imposing this same final-pair reversal for **both** anchors 0 and 1 is impossible. For x>=2 choose `a in {0,1}` of the same parity as x, and put `T(x)=(3x-a)/2>x`. The rule would require T(x) before x. Iterating gives an infinite strictly decreasing sequence of positions. This rules out that stronger sufficient strategy, not general anchored avoidance.

### 7.2 Adenwalla's explicit 5-AP-free permutation

Let

`A=(0,4,2,6,1,5,3,7)`,

`X1=(-8,-4,4,-6,2,-2,6,-7,1,-3,5,-5,3,7)`.

For i>=2 construct Xi by concatenating copies `8 X_(i-1)+r`, taking r in order A for odd i and in reverse A for even i. Define

`P = 0 ; X1 ; -1 ; X2 ; X3 ; ...`.

Induction gives the exact support of Xi as

`[-8^i,-8^(i-1)-1] union [8^(i-1),8^i-1]`.

These disjoint finite shells, together with 0 and -1, exhaust Z. Hence P is an omega-permutation.

**Binary residue identity.** For m a power of two, let rho be the bit-reversal rank with 0 preferred. If m does not divide d, the least nonzero bit of d proves simultaneously

`rho(a)<rho(a+d) iff rho(a+d)>rho(a+2d)`,

`rho(a)<rho(a+d) iff rho(a+2d)<rho(a+3d)`.

This includes repeated nonadjacent residues. It avoids reliance on a printed list of concatenated residues.

**Each Xi is 3-AP-free.** The finite base is checked directly. For a proposed AP in Xi, if 8 divides the difference, all entries lie in one residue subblock and normalize to an AP in X_(i-1). Otherwise, consecutive residues differ. A subsequence traverses subblocks in nondecreasing block order, whereas the first binary identity forces a strict change of direction across three residues. Contradiction.

**Adjacent shells have no 4-AP.** A possible AP spanning Xi and X_(i+1) must have two terms in each, since neither contains a 3-AP. If its difference is not divisible by 8, the second binary identity gives the same orientation to the first and final residue pairs under A, while adjacent shells use opposite orientations. This is impossible. If the difference is divisible by 8 and i>=2, all four entries have a common residue r; mapping them by `(x-r)/8` gives an AP of the same 2+2 type across X_(i-1),Xi, preserving the two internal pair orders. Induct down to i=1. In X1 the only same-residue ordered pairs are `(-4,4),(-6,2),(-2,6),(-7,1),(-3,5),(-5,3)`, each with difference 8. Their last two continuations in X2 normalize to the ordered-value pair (1,2); but 2 precedes 1 in X1. Thus the needed final pair is reversed. The base case and induction are complete.

**The exceptional initial portion.** The sixteen-term word `0 ; X1 ; -1` is 3-AP-free. One may check its 560 triples, or recognize that it is a bit-reversal order modulo 16 with independently chosen child orientations: even values come first, then odd values; inside either parity, the residue classes recursively remain grouped in a binary order. The explicit finite check is included.

**No 5-AP occurs in P.** Suppose `(a1,...,a5)` did. If a2 belongs to Xi and a3 to a later shell, then `|a1|,|a2|<=8^i` and `|a2-a1|<2*8^i`. Hence `|a3|<3*8^i`, `|a4|<5*8^i`, `|a5|<7*8^i`. Since they occur after Xi, all three must be in X_(i+1), contradicting its 3-AP-freeness.

If a2,a3 belong to the same Xi, a4 cannot belong to it. It also cannot be the intervening -1 when i=1, because that would be a 3-AP in the exceptional sixteen-term portion. Thus a4 belongs to a later shell. The bounds `|a4|<3*8^i`, `|a5|<5*8^i` put a4,a5 in X_(i+1), contrary to adjacent-shell 4-AP avoidance applied to a2,...,a5.

Neither a2 nor a3 can be 0, which is first. If a3=-1, then a1,a2,a3 is a 3-AP in the exceptional initial portion. If a2=-1, a1 is in that portion and the difference has absolute value at most 8. The last three terms have absolute values at most 9,17,25; since all occur after -1, they lie in X2 and form a forbidden 3-AP. These exhaust the possibilities. ∎

This is a verification and rewrite of the known construction, not a new upper bound. Two minor presentation issues in the arXiv proof were handled explicitly: the negative shell endpoint requires `<=8^i` rather than `<8^i`, and the displayed combined residue list on PDF page 4 contains a duplicated 4 where a 5 is expected. The binary identity proves the intended claim without that list. The possible intervening -1 in the same-shell case is also explicitly excluded above. None of these changes alters the construction or claimed theorem.

### 7.3 Why that construction does not settle four

For every n>=1 it contains

`0, -8^n, -2*8^n, -3*8^n`

in this order. The second value belongs to Xn. The last two belong to X_(n+1); repeated selection of the residue-zero subblock reduces their comparison to `-2 before -3` in X1. Thus these are infinitely many actual 4-APs, all with negative common difference. The first appears at zero-based positions `(0,1,119,123)`.

## 8. Reproducible checks and remaining gap

The historical research checker used only the Python standard library and authored code. Its checks did not rely on assertions that disappear under optimization. The checker is not distributed in this prose edition; the following run statements are historical records, and the independent audit used separately authored code.

The deterministic run verifies 86,870 binary modular cases, the base word and three shells, the absence of 4-APs across the first two adjacent-shell pairs, and absence of 5-APs in prefixes of lengths 16,128,1024. Their 4-AP counts are respectively 0,2,685. It also checks the explicit scaled 4-APs, all demand edges/cycles for the dead prefixes, 704,808 shell-obstruction witnesses, and the single-anchor order on a finite prefix. Supplemental tests check 145 eligible small signed splices, 27,360 extremal obstruction cases, 10,001 fixed-tail record comparisons, and the signed splice counterexample. Both scripts passed in normal, -O, and -OO Python modes with identical deterministic reports. Finite evidence is never used to infer an infinite avoiding construction.

The exact unsolved task left here is still whether an omega-permutation of all Z can avoid 4-APs. The September result removes N as a possible source of a forcing contradiction, but does not give Z. The signed parity-splice obstruction explains a concrete gap in the most immediate transfer; the predecessor-bound criterion gives an exact alternative target. Neither supplies the missing global construction or forcing theorem.
