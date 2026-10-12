# A sharp finite obstruction for binary-digit-multiplicative signs in every factor

## Exact statement and limitations

Work in \(\mathbb Z[[q]]\), keeping every original unrestricted-partition factor. Suppose every factor has the form
\[
F_m(q)=\prod_{j\ge0}(1+\sigma_{m,j}q^{m2^j}),
\qquad \sigma_{m,j}\in\{-1,1\}. \tag{1}
\]
All digit signs \(\sigma_{m,j}\) are independent across both indices, and infinitely many factors may be changed. Unique binary expansion gives
\[
F_m(q)=1+\sum_{r\ge1}\epsilon_{m,r}q^{mr},\qquad
\epsilon_{m,r}=\prod_{j:\text{the }j\text{-th binary digit of }r\text{ is }1}\sigma_{m,j}\in\{-1,1\}. \tag{2}
\]
Thus (1) is an admissible but restricted sign family for the original problem. For example, it requires \(\epsilon_{m,3}=\epsilon_{m,1}\epsilon_{m,2}\), a condition absent from the original independently signed question.

**Theorem (computer-assisted, sharp within (1)).** For every assignment of all the signs in (1), at least one coefficient of
\[
P(q)=\prod_{m\ge1}F_m(q)
\]
of degree between 1 and 76 lies outside \(\{-1,0,1\}\). There is an assignment for which every coefficient through degree 75 belongs to that set. Therefore 76 is the exact first unavoidable obstruction degree for this class.

The result permits all even factors and all digit-sign freedoms in (1). It does not prove an obstruction for arbitrary independently signed coefficients \(\epsilon_{m,r}\), and it does not solve the original unrestricted problem. It is also distinct from the obstruction for at most two arbitrary active factors. No novelty or general finite-search record is claimed.

## 1. Exact grouping of all sign freedoms

Define
\[
d_n=1+v_2(n),\qquad n\ge1.
\]
The pairs \((m,j)\) with \(m2^j=n\) are exactly
\[
(m,j)=(n/2^j,j),\qquad 0\le j\le v_2(n).
\]
There are \(d_n\) of them. Let \(c_n\) be the number having positive digit sign. Then
\[
0\le c_n\le d_n,\qquad
P(q)=\prod_{n\ge1}G_{n,c_n}(q),
\quad
G_{n,c}(q)=(1+q^n)^c(1-q^n)^{d_n-c}. \tag{3}
\]
Regrouping is legitimate formally: only finitely many pairs \((m,j)\) satisfy \(m2^j\le N\), for any fixed degree \(N\).

Conversely, **every** sequence of integers \(c_n\in\{0,\ldots,d_n\}\) occurs. A canonical realization is
\[
\sigma_{m,j}=\begin{cases}+1,&j<c_{m2^j},\\-1,&j\ge c_{m2^j}.\end{cases} \tag{4}
\]
For fixed \(n\), precisely the indices \(0\le j<c_n\) among its \(d_n\) representations are positive. Every digit-sign variable belongs to exactly one group, so (4) creates no consistency conflict between groups.

The group count loses only labels of identical commuting binomials. It loses no possible product and makes no heuristic identification of different count sequences. In particular, \(c_n\) is not constrained by count choices at other exponents.

## 2. The complete finite recurrence

For \(c=(c_1,\ldots,c_N)\), let
\[
Q_c(q)=\prod_{n=1}^NG_{n,c_n}(q).
\]
Call \(c\) feasible if all coefficients of \(Q_c\) through degree \(N\) lie in \(\{-1,0,1\}\). Future groups start in higher degree, so they cannot change these coefficients.

Start with the unique empty vector at degree zero, with polynomial 1. From every feasible vector \(c=(c_1,\ldots,c_{N-1})\), compute
\[
A_N=[q^N]Q_c(q).
\]
For each integer \(b\in\{0,\ldots,d_N\}\), retain the child \((c_1,\ldots,c_{N-1},b)\) exactly when
\[
|A_N+2b-d_N|\le1. \tag{5}
\]
This is an exact test because
\[
G_{N,b}(q)=1+(2b-d_N)q^N+O(q^{2N}).
\]
Multiplying by that group changes no lower coefficient and adds exactly \(2b-d_N\) to degree \(N\).

By induction, every retained child is feasible. Conversely, restricting any feasible vector to its first \(N-1\) entries gives a feasible parent; its last entry is one of the explicitly tested integers, and it passes (5). Thus the procedure enumerates **all** feasible count vectors. No count choice is discarded except by the exact coefficient condition.

### Two independent coefficient computations

The certificate producer forms the truncated product directly, inserting the \(d_N\) binomials \(1\pm q^N\) one at a time. Multiplication by \(1+s q^N\) replaces each coefficient \(u_i\) with \(u_i+s u_{i-N}\), reading the old coefficients by updating downward in degree.

A separate verifier uses formal logarithmic derivatives instead. For a known vector \(c_1,\ldots,c_M\), define
\[
h_k=\sum_{\substack{m\mid k\\m\le M}}m\begin{cases}
2c_m-d_m,& k/m\text{ odd},\\
-d_m,& k/m\text{ even}.
\end{cases} \tag{6}
\]
Indeed, the contribution of group \(m\) to \(qQ'_c/Q_c\) is
\[
mc_m\frac{q^m}{1+q^m}-m(d_m-c_m)\frac{q^m}{1-q^m}.
\]
Expanding the two geometric series gives precisely (6). Therefore the coefficients \(u_n=[q^n]Q_c\) satisfy
\[
u_0=1,\qquad nu_n=\sum_{k=1}^nh_ku_{n-k}. \tag{7}
\]
This recurrence independently reconstructs \(A_N\), using exact integers and checking divisibility by \(n\), without invoking the producer's multiplication routine.

## 3. Exhaustive certificate and terminal obstruction

The number of feasible count vectors at degrees 0 through 76 is

```
1,2,2,4,8,12,24,32,32,26,26,16,30,36,64,40,78,82,136,74,
140,74,68,78,150,74,70,36,36,36,32,22,42,50,44,64,104,144,
180,228,154,166,100,106,142,62,42,24,34,30,24,20,38,50,86,
44,80,30,26,14,26,20,16,22,22,14,14,8,14,18,14,8,16,16,
4,2,0.
```

There are 3,903 nonempty count-vector states altogether, including the root. The largest frontier has 228 states at degree 39. The recurrence ends with exactly two feasible vectors at degree 75 and none at degree 76. There is no search budget or unresolved branch in this calculation.

One of the two degree-75 vectors, in increasing exponent order \(c_1,\ldots,c_{75}\), is

```
0,1,1,2,1,1,0,2,0,1,1,2,1,1,0,3,0,1,1,2,1,1,0,2,0,
1,1,2,1,1,0,4,0,1,1,2,1,1,0,2,0,1,1,2,1,1,0,3,0,1,
1,2,1,1,0,2,0,1,1,2,1,1,0,4,0,1,1,1,1,0,0,1,1,0,1.
```

The other vector keeps every even-indexed entry unchanged and replaces each odd-indexed entry \(c_n\) by \(1-c_n\). This is the transformation \(q\mapsto-q\) in (3), since \(d_n=1\) for odd \(n\). The exhaustive enumeration retains both vectors; the symmetry was not used to prune the search.

For the displayed vector, exact multiplication gives the coefficients of degrees 0 through 75 as follows:

```
1,-1,0,1,-1,1,-1,-1,0,0,0,0,-1,1,1,0,1,-1,1,0,-1,0,0,-1,
1,0,0,0,0,1,0,0,1,-1,0,1,-1,1,-1,-1,0,-1,0,1,-1,0,0,0,
1,-1,0,1,-1,1,-1,0,1,0,0,0,-1,1,0,-1,0,0,0,-1,-1,1,0,1,
1,-1,0,0.
```

Its coefficient of degree 76 before adding group 76 is
\[
A_{76}=6.
\]
The reflected vector has the same residual because 76 is even. Since \(d_{76}=1+v_2(76)=3\), the possible new coefficients are exactly
\[
6+2b-3\in\{3,5,7,9\},\qquad b=0,1,2,3.
\]
None is allowed. This proves the degree-76 obstruction for all vectors, and hence, by the exact grouping argument, for every binary-digit-multiplicative sign array (1).

For sharpness, extend the displayed vector by any legal counts beyond 75, for example \(c_n=0\) for \(n\ge76\), and use (4). This defines all infinitely many original digit signs and therefore every coefficient sign in every original factor. Future groups cannot affect the verified prefix through degree 75.

The retained complete machine certificate contains every count vector at every level, not just the displayed counts. Its verifier checks the unique root, integer domains \(0\le c_n\le d_n\), state lengths, absence of duplicates, all child sets from (5), every first-empty condition, all terminal coefficients, and the complete witness. It uses (6)–(7), separately from the producer's direct multiplication. Omitting a feasible state, inserting an infeasible state, or using an invalid group count is rejected. Normal Python and optimization levels 1 and 2 give identical verification results. The tests use explicit conditions rather than removable assertions.

## 4. Relationship to prior identities and to the unrestricted problem

[Andrews and Newman, *Binary Representations and Theta Function*, Integers 18 (2018), A34](https://math.colgate.edu/~integers/s34/s34.pdf), use binary sign series in identities over prescribed sets of dilates. This theorem keeps every positive integer \(m\) in the original unrestricted product; it neither substitutes an odd-only product nor deletes even factors.

The [2013 MathOverflow discussion of the unrestricted problem](https://mathoverflow.net/questions/146359/a-product-related-to-unrestricted-partitions) includes a proposed sufficient route using one signed binomial at each odd exponent and a degree-28 obstruction to that smaller model. Here the exact groups at exponent \(n\) have \(1+v_2(n)\) independently signed binomials, including all even exponents, with every allowable count retained. The degree-28 observation is not used as the present certificate.

[Newman's September 2017 numerator/denominator variant](https://mathoverflow.net/questions/282057/yet-another-question-about-unrestricted-partitions) and Alekseyev's reported degree-121 endpoint impose a different pattern of restrictions. That source's exhaustive maximality claim is not invoked here, and its program was not executed.

The conclusion for the original unrestricted problem is only this: any successful unrestricted array would have to violate binary-digit multiplicativity in at least one factor, already among the coefficients relevant through degree 76. There is no implication that general independent signs fail at degree 76, at degree 86, or at any finite degree. No claim about arbitrary three-factor signings or arbitrary finite active sets follows from this certificate.
