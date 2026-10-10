# Independent audit: sparse low-rank zero-square bounds

Date: 2026-10-10 UTC. Target: rank 1213 / problem 30006403.

## Verdict

**ACCEPT the partial mathematical results; DO NOT classify the original real-matrix conjecture as solved.**

For an \(n\times n\) matrix \(M\) over any field, with \(n\ge1\), rank \(r\), and \(E\) nonzero entries, write \(z(M)\) for the largest integer side length of an all-zero submatrix, with independently chosen row and column sets. Put \(h=z(M)/n\). A zero square is not required to be principal. The following statements are correct:

1. \(z(M)\ge\max\{0,\lceil n-\sqrt{rE}\rceil\}\).
2. For \(E\le\varepsilon n^2\), \(0\le\varepsilon\le1\), and every integer \(k>r\),
   \[
   h\ge {k-r\over 2k-r}(1-\varepsilon)^k.
   \]
   In fact,
   \[
   (1-\varepsilon)^k\le h+{k\over k-r}h(1-h).
   \]
3. If \(0\le\varepsilon\le1/2\), then
   \[
   z(M)\ge\left\lceil n\exp\bigl(-6\max\{\sqrt{\varepsilon r},\varepsilon r\}\bigr)\right\rceil.
   \]
   In particular, the weaker constant 9 is valid too.
4. The elementary binary-field inner-product matrix demonstrates that a universal theorem over all fields cannot replace the large-\(\varepsilon r\) linear exponent by a square-root exponent. This is a limitation of field-independent arguments, not a counterexample to the real-matrix conjecture.

The exponential claim requires a density restriction such as the target's \(0<\varepsilon<1/2\). It is false without one: a fully nonzero rank-one matrix has no positive zero square. The discrete sampling statement itself remains valid for all \(0\le\varepsilon\le1\).

## 1. Sparse-row basis argument, including rounding

If \(E=0\), the matrix is zero, \(r=0\), and \(z=n\). Conversely, exact rank \(r=0\) implies \(E=0\). Assume \(E,r>0\). Set \(t=\sqrt{E/r}\), and let \(L\) be the rows with at most \(t\) nonzero entries.

Each excluded row has strictly more than \(t\) nonzero entries. Therefore
\[
 |[n]\setminus L|\,t<E,
 \qquad |L|>n-E/t=n-\sqrt{rE}.
\]
Choose a basis of the span of these rows consisting of rows from \(L\). Its size is at most \(r\). The union \(S\) of the supports of the basis rows has size at most \(rt=\sqrt{rE}\). Every row of \(L\), being a linear combination of the basis rows, is zero outside \(S\). Hence \(M[L,[n]\setminus S]\) is an all-zero rectangle and both its side lengths are at least \(n-\sqrt{rE}\).

When the real lower bound is positive, both integer side lengths are at least its ceiling; selecting equal-sized subsets gives the claimed square. When it is nonpositive the bound is read as zero. Empty \(L\) or an empty basis causes no problem. The proof uses only field-linear dependence and support containment, so it works over every field, not just over the reals.

The use of the ceiling is valid, not an off-by-one extrapolation. Equivalently, \(z\ge n-\lfloor\sqrt{rE}\rfloor\) when this is positive. A rank-one matrix whose support is an \(s\times s\) rectangle has \(E=s^2\) and \(z=n-s\), so equality can occur.

With \(E\le\varepsilon n^2\), this also gives \(h\ge1-\sqrt{\varepsilon r}\), understood as useful only when the right side is positive. In particular,
\(\varepsilon r\le1/4\) ensures a zero square of side at least \(\lceil n/2\rceil\).

## 2. Full sampling proof

The rank factorization in the proposed argument is legitimate over every field. An equivalent formulation avoids factorization altogether: let \(v_1,\ldots,v_n\in\mathbb F^n\) be the actual columns of \(M\), whose span has dimension \(r\).

Independently sample \(J_1,\ldots,J_k\) uniformly from \([n]\), **with replacement**. Let
\[
 H_j=\operatorname{span}\{v_{J_1},\ldots,v_{J_j}\},\qquad H_0=\{0\}.
\]
For any subspace \(H\), define
\[
 R(H)=\{i:w_i=0\text{ for every }w\in H\},\quad
 C(H)=\{\ell:v_\ell\in H\},\quad c(H)=|C(H)|/n.
\]
Then \(M[R(H),C(H)]\) is all zero. Put \(X=|R(H_k)|/n\) and \(A=\{X>h\}\).

### Expected surviving-row fraction

If row \(i\) has zero fraction \(q_i\), it survives precisely when all \(k\) independent selected entries in that row are zero. Thus its survival probability is \(q_i^k\). Consequently
\[
 \mathbb E X={1\over n}\sum_iq_i^k
 \ge\left({1\over n}\sum_iq_i\right)^k
 =\left(1-{E\over n^2}\right)^k
 \ge(1-\varepsilon)^k.
\]
The first inequality is Jensen's inequality for the convex real function \(x^k\) on \([0,1]\). It is applied to real probabilities, regardless of the matrix's field. The row events need not be independent of each other. Generally the expectation is **not equal** to the \(k\)-th power of the average zero density, so this inequality must not be replaced by an equality.

### The maximal-square implication

On \(A\), the integer row count \(|R(H_k)|\) is strictly greater than \(z\). Since \(H_j\subseteq H_k\), every \(R(H_j)\) contains \(R(H_k)\). If \(c(H_j)>h\), then also \(|C(H_j)|>z\); the corresponding zero rectangle would contain a \((z+1)\times(z+1)\) zero square. This contradicts the definition of \(z\). Therefore on \(A\),
\[
 c(H_j)\le h\quad(0\le j\le k).
\]
This is also correct for \(j=0\): \(C(H_0)\) is exactly the zero columns. If there are more than \(z\) zero columns, they and all rows already contradict maximality unless \(z=n\).

### Adapted dependence indicators

Let
\[
 D_j=\mathbf1\{v_{J_j}\in H_{j-1}\},\qquad
 I_j=\mathbf1\{c(H_{j-1})\le h\}D_j.
\]
Conditioned on \(J_1,\ldots,J_{j-1}\), the next index remains uniform, so
\[
 \mathbb E[I_j\mid J_1,\ldots,J_{j-1}]
 =\mathbf1\{c(H_{j-1})\le h\}c(H_{j-1})\le h.
\]
No independence between different \(D_j\), no conditioning on the future event \(A\), and no stopping-time theorem is being assumed.

Exactly \(\dim H_k\) samples increase the span dimension, so
\[
 \sum_{j=1}^kD_j=k-\dim H_k\ge k-r.
\]
On \(A\), all the truncating conditions in \(I_j\) hold. Therefore
\[
 (k-r)\mathbf1_A\le\sum_{j=1}^k I_j,
 \qquad (k-r)\mathbb P(A)\le kh.
\]
Finally \(0\le X\le1\), and \(X\le h\) outside \(A\), giving
\[
 \mathbb EX\le h+(1-h)\mathbb P(A)
 \le h+{k\over k-r}h(1-h).
\]
Dropping the factor \(1-h\le1\) proves
\[
 (1-\varepsilon)^k\le h\,{2k-r\over k-r}.
\]
The denominator is positive because \(k>r\). If \(kh/(k-r)>1\), the displayed probability bound is merely weak, not invalid. The proof covers zero rows, zero columns, repeated or proportional columns, \(k>n\), full rank, and finite fields.

For an integer side-length formulation, the lower bound is
\(
 z\ge\left\lceil n{(k-r)\over(2k-r)}(1-\varepsilon)^k\right\rceil.
\)
The rank-zero case may either be handled separately or left in this sampling proof; separate treatment preserves the exact answer \(z=n\).

## 3. Constant 6, with all parameter ranges

Assume \(r\ge1\), \(0\le\varepsilon\le1/2\), and put \(s=\varepsilon r\). The logarithmic inequality
\(\log(1-\varepsilon)\ge-2\varepsilon\)
holds throughout this interval. Taking \(k=2r\) gives
\[
 h\ge\tfrac13(1-\varepsilon)^{2r}\ge\tfrac13e^{-4s}.
\]

* If \(0\le s\le1/4\), put \(t=\sqrt s\le1/2\). The sparse-basis bound gives \(h\ge1-t\ge e^{-2t}\ge e^{-6t}\). The middle inequality follows from \(log(1-t)+2t\ge0\) on \([0,1/2]\).
* If \(1/4\le s\le1\), put \(t=\sqrt s\in[1/2,1]\). The convex polynomial \(4t^2-6t+\log3\) has value \(\log3-2<0\) at both endpoints, so it is nonpositive throughout the interval. Hence \(\tfrac13e^{-4s}\ge e^{-6\sqrt s}\).
* If \(s\ge1\), \(4s+\log3\le6s\), so \(\tfrac13e^{-4s}\ge e^{-6s}\).

For \(r=0\), \(h=1\), exactly matching the desired exponential lower bound. The case \(\varepsilon=0\) likewise forces \(M=0\).

This proves the claimed C=6 bound. It settles the target bound only in the bounded-\(\varepsilon r\) range. For unbounded \(\varepsilon r\), the exponent remains linear rather than the target square root, so the original conjecture remains unresolved by this argument.

## 4. Binary-field obstruction and real-rank safeguard

For an integer \(d\ge1\), take all \(x,y\in\mathbb F_2^d\), \(n=2^d\), and let \(M_{x,y}=x\cdot y\in\mathbb F_2\), represented by 0 or 1. Then
\[
 \operatorname{rank}_{\mathbb F_2}M=d,\qquad
 E=(n-1)n/2,\qquad \varepsilon=(n-1)/(2n)<1/2.
\]
The rank factorization gives the upper bound \(d\), while rows and columns indexed by coordinate vectors contain a \(d\times d\) identity submatrix.

If \(A\times B\) is a zero rectangle, \(U=\operatorname{span}A\) and \(V=\operatorname{span}B\) are orthogonal for the nondegenerate dot product. Thus \(\dim U+\dim V\le d\). In particular, one dimension is at most \(\lfloor d/2\rfloor\), so
\[
 \min\{|A|,|B|\}\le2^{\lfloor d/2\rfloor}.
\]
Complementary coordinate subspaces of dimensions \(\lfloor d/2\rfloor\) and \(\lceil d/2\rceil\) attain that balanced square size. Therefore
\[
 z=2^{\lfloor d/2\rfloor},\qquad h=2^{-\lceil d/2\rceil}=\exp(-\Theta(\varepsilon d)).
\]
This contradicts any field-uniform square-root-exponent conclusion with an absolute constant as \(d\to\infty\).

However, the same 0/1 array has real rank \(n-1\), not \(d\). For \(d\ge2\), the Gram matrix of its \(n-1\) nonzero rows over the reals is
\[
 {n\over4}(I_{n-1}+J_{n-1}),
\]
which is positive definite. A zero row gives the matching upper bound. For \(d=1\), the real rank is directly 1. Therefore this construction is not a counterexample to the target statement about real rank.

## 5. Attribution and literature scope

The sampling method has a clear antecedent in Singer and Sudan, *Point-hyperplane incidence geometry and the log-rank conjecture*, Section 3 / proof of Theorem 1.7. Their argument samples hyperplanes, retains a large expected fraction of points, and uses dimension drops to force a common containing family. The present proof uses more than \(r\) samples and counts all dependent steps to obtain an explicit balanced bound. Calling it an elementary adaptation or refinement is appropriate. An assertion of original discovery or comprehensive novelty is not justified by this audit. Primary record: https://arxiv.org/abs/2101.09592 .

Hunter, Milojević, Sudakov and Tomon, *Disjoint pairs in set systems and combinatorics of low rank matrices*, Conjecture 1.8, states the real-matrix target with \(0<\varepsilon<1/2\); Lemma 4.7(2) provides a prior small-density half-sized zero rectangle at density \(1/(16r)\). The sparse-basis proof gives \(1/(4r)\) for a half-square, but no priority claim is made. Their nonnegative-entry/average-entry theorem does not apply to arbitrary signed real matrices under only a support-density condition. Primary records: https://arxiv.org/abs/2411.13510 and https://people.math.ethz.ch/~sudakovb/disjoint-pairs-set-sytems-log-rank.pdf .

Version caution: in both inspected downloaded PDFs, the body of Theorem 1.12 includes an additive \(log r\) in the exponent, while the abstract omits it. Cite the exact body statement when relying on that theorem; do not silently use the stronger abstract wording. These observations do not establish the present-day global status beyond the searched/inspected sources.

## Scope and disposition

Accept the checked statements as partial results with the density domain and field distinction stated explicitly. Keep the original arbitrary-real-matrix square-root-exponent conjecture open.

## Reviewed mathematical scope

The complete authored report was read. Its sparse-basis, sampling, C=6, rank-one, binary-field and real set-intersection claims all pass this audit. No required mathematical correction was found. [APPROACH_1.md](APPROACH_1.md) preserves that report's complete substantive mathematics. [ACCEPTANCE.md](ACCEPTANCE.md) binds the distributed report and audit editions, and [PROVENANCE.md](PROVENANCE.md) records the editorial boundary. Subsequent substantive edits require their own review.
