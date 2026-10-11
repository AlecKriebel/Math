# Distance-count spectra: two construction obstructions

**Erdős Problem 653 remains unresolved.** This note records why two selected construction routes do not establish the conjecture. The elementary statements below carry no novelty claim. Separate adversarial review is pending.

## 1. Exact target and notation

For a set \(P\) of \(n\ge2\) **distinct** points in the Euclidean plane, put
\[
r_P(p)=\#\{\lVert p-q\rVert:q\in P\setminus\{p\}\},\qquad
\sigma(P)=\#\{r_P(p):p\in P\}.
\]
The target is
\[
g(n):=\max_{|P|=n}\sigma(P)=(1-o(1))n.
\tag{1}
\]
Thus we count the different integer values of the pinned-distance counts, not the distances themselves. The maximum possible pinned count is \(n-1\).

The exact asymptotic question occurs in Erdős's 1995 article, section III.1, on manuscript pp.14–15 [E95]. The tracker cites the later 1997 article [E97]. The 1995 full manuscript was available and its question was visually checked; the cited 1997 full text was not recovered. These source versions are distinguished in the accompanying source audit.

Define the **deficit** at a point by
\[
d_P(p)=n-1-r_P(p),\qquad D(P)=\{d_P(p):p\in P\}.
\]
For a singleton, use \(r_P(p)=d_P(p)=0\). For any fixed set, \(|D(P)|=\sigma(P)\). When \(n\ge2\), its deficits are integers in \([0,n-2]\).

## 2. Generic gluing preserves the deficit spectrum

Let \(P_1,\ldots,P_k\) be nonempty finite planar sets, of sizes \(m_1,\ldots,m_k\). Translate them independently, writing \(Q_i=P_i+t_i\) and \(Q=\bigcup_iQ_i\), of size \(n=\sum_i m_i\).

Call these translations admissible if the translated sets are disjoint and, for every pin \(p\in Q_i\), the distances from \(p\) to the points outside \(Q_i\) are mutually distinct and different from all its distances to points of \(Q_i\setminus\{p\}\).

**Lemma 1.** Admissible translation tuples form an open dense subset of \((\mathbb R^2)^k\). For every admissible tuple,
\[
r_Q(p+t_i)=n-m_i+r_{P_i}(p),\qquad
d_Q(p+t_i)=d_{P_i}(p),
\tag{2}
\]
and consequently
\[
D(Q)=\bigcup_{i=1}^kD(P_i).
\tag{3}
\]

**Proof.** The forbidden point coincidences and distance equalities are a finite collection of polynomial equations in the translations. None is an identity. For example, if two comparison points are in the same block outside the pin's block, their squared-distance difference is a nonconstant affine function of the relative translation, with nonzero linear coefficient equal, up to a factor, to their difference vector. If they are in distinct blocks and at least one block differs from the pin's block, varying that latter block's translation alone gives a nonconstant quadratic polynomial. This also treats one comparison point inside the pin's block. Point coincidence is plainly a proper condition. No equality between two points within the pin's own block is forbidden.

A nonzero real polynomial has a zero set with empty interior. The complement of the finite union of these zero sets is therefore open and dense. At an admissible tuple, each of the \(n-m_i\) external points supplies one new distance at a pin of block \(i\); the internal distance count is unchanged by translation. This proves (2), and then (3). \(\square\)

Several exact consequences rule out a generic amplification of small examples.

1. If all blocks are translated copies of the same seed \(P\), then \(D(Q)=D(P)\) and \(\sigma(Q)=\sigma(P)\), regardless of the number of copies.
2. If the largest block has size \(M\ge2\), then \(D(Q)\subseteq\{0,\ldots,M-2\}\), so \(\sigma(Q)\le M-1\). If all blocks are singletons, the spectrum has size one.
3. Adding any positive number of generic singleton points to a fixed set changes its deficit spectrum to \(D(P)\cup\{0\}\); it adds at most one distinct count value, however many points are added.
4. The same statements apply inductively to a finite hierarchy in which every gluing step is admissible. The final deficit spectrum is the union of the leaf spectra. In particular, a family built from leaves of maximum size \(M(n)=o(n)\) has \(\sigma(Q)=o(n)\), not the required asymptotic size in (1).

These conclusions concern the stated admissibility condition. They do not apply to constructions that deliberately create equal distances across blocks. For instance, two horizontal unit segments translated into opposite sides of a unit square have internal deficits zero but union deficits one, so (2) fails when cross-block coincidences are allowed. The obstruction identifies exactly where a useful gluing construction must depart from the generic route.

## 3. Concentration on one line or circle has a one-half barrier

**Lemma 2.** If all \(n\ge2\) points lie on a line or on a circle of positive radius, then
\[
\sigma(P)\le\left\lceil\frac n2\right\rceil.
\tag{4}
\]
This bound is attained in both restricted classes for every \(n\ge2\).

**Proof.** For a pin on a line, a positive distance sphere meets the line in at most two points. For a pin on the supporting circle, its positive distance sphere is a different circle and also meets the supporting circle in at most two points: the pin cannot be the supporting circle's center because it lies on that circle of positive radius. Hence
\[
\left\lceil\frac{n-1}{2}\right\rceil\le r_P(p)\le n-1.
\]
The number of integers in this interval is \(\lceil n/2\rceil\).

For equality on a line use \(P=\{(j,0):0\le j<n\}\). The count at index \(i\) is \(\max(i,n-1-i)\), giving exactly \(\lceil n/2\rceil\) values. For equality on a circle choose points at angles \(j\theta\), \(0\le j<n\), with \(0<(n-1)\theta<\pi\). Their chord length for index difference \(a\) is \(2R\sin(a\theta/2)\), strictly increasing for \(1\le a\le n-1\). The same pinned counts result. \(\square\)

The obstruction survives a sublinear number of exceptional points.

**Lemma 3.** Suppose \(m=n-t\ge2\) of the points lie on one line or one positive-radius circle. The other \(t\) points are unrestricted. Then
\[
\sigma(P)\le
\min\left\{n-1,\ n+t-\left\lceil\frac{n-t-1}{2}\right\rceil\right\}.
\tag{5}
\]
In particular, if \(t=o(n)\), then \(\sigma(P)\le(1/2+o(1))n\).

**Proof.** At each of the \(m\) supported pins, its distances to the other supported points already take at least \(a=\lceil(m-1)/2\rceil\) different values. Adding the exceptional points cannot reduce that count. These pins therefore contribute at most \(n-a\) count values from the integer interval \([a,n-1]\). The exceptional pins add at most \(t\) values. Finally all counts lie in \(\{1,\ldots,n-1\}\), giving the additional trivial bound in (5). \(\square\)

Thus a construction concentrated on a single simple support, even with sublinear repairs, does not yield (1). The lemma does not bound arbitrary planar configurations or configurations supported on a growing family of curves.

## 4. A classical upper-bound check

The following elementary estimate is included for orientation and is already implicit in the Erdős–Saldanha observation recorded in [E95]; it is not a new result.

For two distinct pins \(p,q\), each other point lies on the intersection of a distance circle centered at \(p\) and one centered at \(q\). The centers differ, so each pair of circles intersects in at most two points. Therefore
\[
n-2\le 2r_P(p)r_P(q).
\tag{6}
\]
If \(s=\sigma(P)\ge2\), set \(h=n-s\) and write the different counts increasingly as \(a_1<\cdots<a_s\). Since these are integers at most \(n-1\),
\[
a_j\le n-s+j-1=h+j-1.
\]
Choosing pins realizing \(a_1,a_2\) in (6) gives
\[
n-2\le2h(h+1),\qquad
h\ge\frac{\sqrt{2n-3}-1}{2}.
\tag{7}
\]
If \(s=1\), the same final inequality holds directly because \(h=n-1\). Hence (7) applies to every configuration. Later reported upper bounds are stronger, as described with source qualifications in the audit. Any bound of the form \(g(n)\le n-c n^\alpha\) with fixed \(\alpha<1\) is compatible with (1).

## 5. Exact gap and scope of this attempt

The two substantive approaches were generic hierarchical gluing and configurations concentrated on a line or circle. The first cannot enlarge the range of seed deficits; the second has a one-half asymptotic barrier. Neither provides a lower bound with coefficient approaching one, nor a universal upper bound separated from one by a fixed positive proportion.

The remaining problem is still (1) in full. A successful construction would have to control many nongeneric equalities across its components, or use a different mechanism. No scalable realization of such equalities has been proved here. Finite examples, including previously posted exact small configurations, do not settle this missing asymptotic step. Work stops at this precise gap after two attempts, rather than relabeling a restricted-family obstruction as an answer to the original problem.

The accompanying exact checker validates small examples, both generic and deliberately nongeneric unions, restricted-support bounds, and the elementary inequality (7). Its finite scope does not certify either an asymptotic solution or historical priority.

## References

- **[E95]** P. Erdős, *Some of my favourite problems in number theory, combinatorics, and geometry*, Resenhas **2**(2) (1995), 165–186. [Publisher record](https://revistas.usp.br/resenhasimeusp/en/article/view/74798), [full author manuscript](https://www.ime.usp.br/~yoshi/resenhas/abstracts/Erdos.pdf), section III.1, manuscript pp.14–15.
- **[E97]** P. Erdős, *Some of my favourite unsolved problems*, Math. Japonica **46**(3) (1997), 527–537. [Publisher contents](https://www.jams.jp/notice/mj/46-3.html). Full text not recovered in this attempt.
- **[Tracker]** T. F. Bloom, [Erdős Problem 653](https://www.erdosproblems.com/653). The current direct page was blocked; search-index evidence and the pinned dataset were distinguished from a live read.

Further bibliography, current preprint claims, and access limitations are recorded in [SOURCE_AUDIT.md](SOURCE_AUDIT.md).
