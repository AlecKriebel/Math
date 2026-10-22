# A sharp obstruction for one arbitrary factor beyond the first two

**Public evidence note.** The finite obstruction below uses computer-assisted exhaustive enumeration. The complete recurrence, state domains, counts, explicit sharpness witnesses and substantive independent review are distributed in prose. The programs and raw frontier certificates used in the historical verification are not distributed in this appendix. This is not an executable public replay package; independent reimplementation is possible from the mathematical specification.


## Statement and scope

For the unrestricted partition-sign problem, write
\[
P(q)=\prod_{m\ge1}F_m(q),\qquad
F_m(q)=1+\sum_{j\ge1}\epsilon_{m,j}q^{mj},\quad
\epsilon_{m,j}\in\{-1,1\}.
\]
Call factor \(m\) **binary-digit multiplicative** when
\[
F_m(q)=\prod_{r\ge0}(1+\sigma_{m,r}q^{m2^r}),\qquad
\sigma_{m,r}\in\{-1,1\}. \tag{1}
\]
Unique binary expansion shows that (1) is admissible: every coefficient in that factor is a sign. It also imposes genuine restrictions, for example
\(\epsilon_{m,3}=\epsilon_{m,1}\epsilon_{m,2}\).

**Theorem (computer-assisted, sharp).** Suppose all factors are binary-digit multiplicative except possibly one factor with index \(a\ge3\), whose coefficients may be signed completely independently. Then some coefficient of degree at most 94 lies outside \(\{-1,0,1\}\). There is such a product, with exceptional factor \(a=3\), satisfying all coefficient bounds through degree 93.

All factors remain present, all their digit signs are independent, and infinitely many factors may be changed. The arbitrary exceptional factor can have infinitely many nonbinary coefficients. This is a strict enlargement of the all-binary class, and is different from allowing only finitely many active factors while leaving the rest positive.

**Consequence for the original unrestricted problem.** Any successful unrestricted sign array must either have a nonbinary factor of index 1 or 2, or have nonbinary coefficients in at least two different factors. The same finite-prefix statement holds through degree 94: the signs relevant by that degree cannot all be compatible with the stated hybrid class.

The theorem does not cover an arbitrary exceptional factor 1 or 2, two or more arbitrary factors, or unrestricted independent signs in all factors. These unresolved cases must not be inferred from the finite obstructions below. No novelty or finite-search record claim is made.

## 1. Exact grouping of the binary factors

Fix \(a\), and write the arbitrary factor as
\[
A_a(q)=1+\sum_{j\ge1}\alpha_jq^{aj},\qquad \alpha_j\in\{-1,1\}.
\]
For each \(n\ge1\), there are \(1+v_2(n)\) pairs \((m,r)\) with \(m2^r=n\). Excluding factor \(a\) leaves
\[
d_n^{(a)}=1+v_2(n)-\mathbf1_{\{n=a2^r\text{ for some }r\ge0\}}. \tag{2}
\]
If \(c_n\) of these digit signs are positive, then
\[
P(q)=A_a(q)B(q),\quad
B(q)=\prod_{n\ge1}(1+q^n)^{c_n}(1-q^n)^{d_n^{(a)}-c_n},
\quad0\le c_n\le d_n^{(a)}. \tag{3}
\]
Every legal count sequence occurs: at each exponent, order the finitely many representations \((m,r)\) with \(m\ne a\) by increasing \(r\), choose the first \(c_n\) positive, and choose the rest negative. Each digit-sign variable belongs to exactly one such exponent group. There is no consistency constraint between different counts.

The grouping only forgets labels of identical commuting binomials outside factor \(a\). It does not identify arbitrary-factor sign choices or different count sequences. Formal regrouping is valid since only finitely many factors can contribute below any fixed degree.

## 2. Exact finite recurrence and completeness

At level \(N\), the state consists of
\[
(\alpha_1,\ldots,\alpha_{\lfloor N/a\rfloor});
(c_1,\ldots,c_N).
\]
Use the corresponding truncated factors in (3), with \(\alpha_0=1\). Start with the unique root. For a level-\(N-1\) state, compute
\[
R_N=[q^N]\left(\sum_{j=0}^{\lfloor(N-1)/a\rfloor}\alpha_jq^{aj}\right)
\prod_{n=1}^{N-1}(1+q^n)^{c_n}(1-q^n)^{d_n^{(a)}-c_n}. \tag{4}
\]
For every \(b\in\{0,\ldots,d_N^{(a)}\}\), and for every
\[
e\in E_N=\begin{cases}\{-1,1\},&a\mid N,\\\{0\},&a\nmid N,\end{cases}
\]
retain the child exactly when
\[
|R_N+2b-d_N^{(a)}+e|\le1. \tag{5}
\]
Append \(b\) to the count vector, and append \(e\) to the arbitrary-factor sign vector only if \(a\mid N\).

A new arbitrary coefficient has degree \(N\), and the new binary group equals
\(1+(2b-d_N^{(a)})q^N+O(q^{2N})\). Thus (5) is exactly the new coefficient condition and cannot change earlier coefficients. Conversely, restricting any feasible level-\(N\) state gives a feasible parent, and its final choices occur among those in (5). Induction proves that every feasible state, and only feasible states, is retained. No beam width, random choice, symmetry reduction, numerical tolerance, or search-time cutoff is used in any completed case stated in this note.

## 3. Reduction to 23 finite cases

The previously established all-binary obstruction has first empty degree 76. For \(a\ge26\), the arbitrary factor has at most its first two nonconstant coefficients visible through degree 76. Every pair of signs \((\alpha_1,\alpha_2)\) extends to a binary-digit-multiplicative factor by setting the first two digit signs accordingly. If only one or neither coefficient is visible, the statement is even more immediate. The first coefficient at which binary multiplicativity can fail is multiplicity 3, of degree \(3a\ge78>76\).

Consequently a hybrid with \(a\ge26\) agrees, through degree 76, with some all-binary product, which is impossible. The remaining exceptional indices for this theorem are exactly \(a=3,4,\ldots,25\). The case where no factor is exceptional is already included in the all-binary obstruction. This reduction does not apply to \(a=1,2\), which are deliberately outside the theorem.

## 4. Exhaustive finite results

The recurrence (2)–(5) gives these first empty levels:

| Exceptional factor | First empty degree | Total nonempty states, including root | Maximum frontier |
|---|---:|---:|---:|
| 3 | 94 | 1,709,525 | 108,684 |
| 4 | 78 | 2,887,957 | 182,540 |
| 5 | 76 | 120,297 | 7,846 |
| 6 | 76 | 263,551 | 16,872 |
| 7 | 76 | 42,041 | 2,952 |
| 8 | 76 | 108,881 | 7,224 |
| 9 | 76 | 21,093 | 1,154 |
| 10 | 76 | 44,015 | 2,176 |
| 11 | 76 | 13,567 | 784 |
| 12 | 76 | 30,311 | 1,712 |
| 13 | 76 | 9,455 | 642 |
| 14 | 76 | 19,623 | 1,048 |
| 15 | 76 | 7,469 | 402 |
| 16 | 76 | 16,043 | 880 |
| 17 | 76 | 6,639 | 370 |
| 18 | 76 | 12,675 | 796 |
| 19 | 76 | 5,707 | 328 |
| 20 | 76 | 10,375 | 540 |
| 21 | 76 | 4,945 | 228 |
| 22 | 76 | 8,741 | 454 |
| 23 | 76 | 4,699 | 228 |
| 24 | 76 | 8,111 | 456 |
| 25 | 76 | 4,483 | 228 |

The original exhaustive computation multiplies the binary group polynomials directly, keeping every sign vector and count vector. The historical review compared every complete frontier with independently generated states. Aggregate cardinalities and integrity checks were not substitutes for arithmetic and complete-state verification. The raw frontiers and programs are not distributed here.

An independently written C++ enumeration uses logarithmic derivatives instead of direct group multiplication. Given an already chosen binary cofactor, its logarithmic derivative has coefficients
\[
h_k=\sum_{\substack{n\mid k\\n\text{ already chosen}}}n
\begin{cases}
2c_n-d_n^{(a)},&k/n\text{ odd},\\
-d_n^{(a)},&k/n\text{ even}.
\end{cases} \tag{6}
\]
Its coefficients \(b_n\) satisfy
\[
b_0=1,\qquad nb_n=\sum_{k=1}^nh_kb_{n-k}. \tag{7}
\]
These follow by expanding the formal logarithmic derivatives of \(1+q^n\) and \(1-q^n\). Formula (4) is then \(R_N=\sum_j\alpha_jb_{N-aj}\). The independent enumeration reproduces every stated frontier cardinality. Its detailed report records further certificate and mutation checks separately; checks not listed as completed in that report are not claimed here.

## 5. Sharpness witness and terminal obstruction

For \(a=3\), give factor 3 the positive signs precisely at multiplicities
\[
1,2,6,7,8,10,15,19,20,21,23,25,26,27,30
\]
among \(1\le j\le31\), and give every other sign in that interval the value \(-1\). The following count sequence \((c_1,\ldots,c_{93})\), interpreted using (2)–(3), completes the witness:

```
0,1,0,2,1,1,1,3,1,1,0,1,0,1,0,4,1,1,1,2,1,1,0,1,0,1,0,2,1,2,1,
5,1,1,0,2,0,1,0,3,1,2,1,2,1,1,0,3,0,1,0,2,1,2,1,3,1,1,0,0,0,1,
1,6,1,1,1,1,0,0,0,3,0,2,0,3,0,2,0,3,0,0,1,1,1,0,0,1,0,2,0,0,0.
```

Exact multiplication gives these coefficients from degree 0 through 93:

```
1,-1,0,1,-1,1,1,-1,0,0,0,0,1,-1,-1,0,-1,1,-1,0,-1,0,0,-1,
1,0,0,0,0,1,0,0,-1,1,0,1,1,-1,1,-1,0,1,0,1,-1,0,0,0,
-1,-1,0,1,-1,-1,1,0,1,0,0,0,1,-1,0,1,0,0,0,-1,-1,-1,0,-1,
1,-1,0,0,-1,-1,0,0,0,1,1,1,0,1,0,1,-1,-1,-1,1,1,1.
```

All entries have absolute value at most 1. Extending the remaining signs and counts arbitrarily defines a full infinite product without changing this prefix, proving finite sharpness.

There are exactly four feasible states at degree 93 for \(a=3\). In each, (4) gives \(R_{94}=-6\). Since \(3\nmid94\) and \(d_{94}^{(3)}=2\), the only possible degree-94 coefficients are
\[
-6+2b-2\in\{-8,-6,-4\},\qquad b=0,1,2.
\]
Thus all four states fail. The historical independent review checked their entire sign/count vectors, not just their counts or residuals, and separately checked both displayed witness arrays. The displayed assignment and coefficient list are the public mathematical witness.

Combining the finite cases with the reduction in Section 3 proves the obstruction by degree 94, and the witness proves sharpness for the stated union of hybrid classes.

## Source and limitation notes

The motivating unrestricted question is [David Newman, *Dividing up the unrestricted partitions*, Open Problem Garden](https://www.openproblemgarden.org/op/dividing_up_the_unrestricted_partitions). Its historical discussion reports unrestricted searches to approximately degree 110, so the present degree-93 witness is not claimed as an unrestricted record. Newman's [2013 MathOverflow formulation](https://mathoverflow.net/questions/146359/a-product-related-to-unrestricted-partitions) also makes clear that the original signs are not restricted to (1).

The degree-76 all-binary theorem used for the index reduction is the prior authored [all-binary proof](../BINARY_CLASS_OBSTRUCTION.md), whose exact finite computation was independently checked. Its proof and scope are not enlarged by assumption here. The present theorem is a separate exact extension permitting one arbitrary factor of index at least 3. No result for arbitrary exception index 1 or 2 is proved, and nothing in this note establishes nonexistence in the unrestricted problem.
