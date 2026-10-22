# Exact obstruction thresholds for at most two noncyclotomic ternary blocks

**Later accepted result (12 October 2026).** This note retains the earlier argument and its original mathematical scope. A separate, subsequently accepted [full-ternary theorem](FULL_TERNARY_OBSTRUCTION.md), with [complete independent review](REVIEW_FULL_TERNARY.md), combines coefficient conditions with global Jensen inequalities to exclude the entire ternary-digit family. The earlier statements that these zero-sparsity or finite-budget arguments alone do not do so remain accurate. The unrestricted independent-coefficient problem remains unresolved.


**Public evidence note.** The finite obstruction below uses computer-assisted exhaustive enumeration. The complete recurrence, state domains, counts, explicit sharpness witnesses and substantive independent review are distributed in prose. The programs and raw frontier certificates used in the historical verification are not distributed in this appendix. This is not an executable public replay package; independent reimplementation is possible from the mathematical specification.


## Family and theorem

Retain every original partition factor and put
\[
F_m(q)=\prod_{j\ge0}
(1+u_{m,j}q^{m3^j}+v_{m,j}q^{2m3^j}),\qquad u_{m,j},v_{m,j}\in\{-1,1\}.
\]
Unique ternary representation makes every coefficient in each original factor \(F_m\) exactly \(+1\) or \(-1\). All displayed block signs are independent. The class is still narrower than arbitrary independent signs on the original factor coefficients.

Call a block a defect if \(v_{m,j}=-1\). Its exponent is \(n=m3^j\). The two nondefective block polynomials \(1\pm z+z^2\) have only unit-circle roots; each defective polynomial \(1\pm z-z^2\) has an interior root of modulus \(\varphi^{-1}\). The companion interior-zero note proves the relevant global necessary zero inequality.

**Theorem (exact computer-assisted thresholds).** If there are at most \(K\) defective blocks in the entire product, the first unavoidable coefficient outside \(\{-1,0,1\}\) occurs at the following sharp universal degrees:

| Allowed defects \(K\) | First unavoidable degree | Good prefix achieved | Total nonempty states | Largest frontier |
|---|---:|---:|---:|---:|
| 0 | 31 | 30 | 563 | 60 |
| 1 | 42 | 41 | 11,481 | 1,242 |
| 2 | 55 | 54 | 132,203 | 12,448 |

This does **not** exclude unrestricted ternary-digit arrays with more defects. It is an authored partial result with no novelty claim.

A consequence for any successful array in this ternary family is that it must have at least one defective block of exponent at most 15, at least two of exponent at most 21, and at least three of exponent at most 27. These are lower requirements on a hypothetical infinite solution, not a construction of one.

## 1. Grouping and realizability

For each \(n\), the pairs \((m,j)\) with \(m3^j=n\) are precisely
\[
(m,j)=(n/3^j,j),\quad 0\le j\le v_3(n).
\]
Their number is \(d_n=1+v_3(n)\). Index the four possible block polynomials by
\[
B_0(z)=1-z+z^2,\quad B_1(z)=1+z+z^2,
\quad B_2(z)=1-z-z^2,\quad B_3(z)=1+z-z^2.
\]
A group is a sorted tuple \(g=(g_1,\ldots,g_{d_n})\) with entries in \(\{0,1,2,3\}\), representing
\[
G_g(q)=\prod_{i=1}^{d_n}B_{g_i}(q^n).
\]
Sorting removes only labels of commuting identical blocks, not any possible product. Conversely every group tuple can be realized by assigning its entries in order to the pairs \((n/3^j,j)\). Different exponents use disjoint pairs, so all group choices are simultaneously realizable.

Define
\[
D(g)=\#\{i:g_i\in\{2,3\}\},\qquad
L(g)=\#\{i:g_i\in\{1,3\}\}-\#\{i:g_i\in\{0,2\}\}.
\]
Then \(D(g)\) is its defect count and \(G_g(q)=1+L(g)q^n+O(q^{2n})\).

## 2. Exhaustive recurrence

A state at degree \(N\) is the complete sequence of group tuples \((g_1,\ldots,g_N)\). It is feasible for cap \(K\) if its total defect count is at most \(K\), and every coefficient of \(\prod_{n=1}^NG_{g_n}(q)\) through degree \(N\) has absolute value at most 1.

Start with the unique empty state. For every feasible state through \(N-1\), compute the degree-\(N\) residual \(A_N\) of its product. Enumerate **every** sorted group tuple of length \(d_N\). Retain it exactly if
\[
D(g_1)+\cdots+D(g_{N-1})+D(g_N)\le K,
\qquad |A_N+L(g_N)|\le1. \tag{1}
\]
The fresh group starts at degree \(N\), so this is the exact new coefficient condition and changes no previous coefficient. Restricting a feasible state gives a feasible parent. Thus induction proves that the recurrence retains every feasible state, with no heuristic exclusions.

The producer uses integer polynomial convolution, with a truncation limit of 60, which exceeds all three terminal degrees. The historical review retained and compared every complete frontier. Those raw frontiers are not distributed here. The following abstract encoding specifies the displayed mathematical witnesses: a state is encoded by one character per exponent: list the sorted tuples of length \(d_n\) in lexicographic order, then encode the tuple's zero-based index with alphabet

```
0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
```

The indices occurring through degree 55 fit this alphabet. The tuple rule and alphabet above completely specify the witness encoding, independently of a storage format.

An independent enumeration can recover coefficients without convolution: for each polynomial block use its formal logarithmic derivative, sum the dilated logarithmic derivatives of all blocks, and recover product coefficients by \(na_n=\sum_{k=1}^nh_ka_{n-k}\). This is the separate arithmetic route used in the independent audit. Counts alone are diagnostic; comparison of complete state sets is required.

## 3. Witnesses and sharpness

The selected final feasible state strings, in the encoding just specified, are:

- \(K=0\), degree 30: `001000001000111000114110114001`
- \(K=1\), degree 41: `00101110100200101110400000101410000000400`
- \(K=2\), degree 54: `001011101002001011106000001014100000004010104004110011`

They use respectively 0, 1, and 2 defects. The coefficient arrays are determined exactly by the displayed group assignments and direct multiplication; the historical independent review checked those full arrays and the final residuals. Their final residuals before adding the terminal group are respectively \(-3\), \(6\), and \(5\). The exhaustive transition test (1) gives no terminal child for any state at the preceding degree, not only these selected witnesses.

Extend each witness by arbitrary nondefective groups beyond its last degree. The realization in Section 1 defines all the original factor signs and keeps the global defect cap. Higher groups cannot change the already verified prefix, proving sharpness.

For the lower requirements on a hypothetical unrestricted ternary solution, observe that changing \(v\) from \(-1\) to \(+1\) in a block of exponent \(n\) first changes the product at degree \(2n\). If at most \(K\) defects have \(n\le\lfloor N/2\rfloor\), all later defects can be removed without altering the product through degree \(N\). Taking \((K,N)=(0,31),(1,42),(2,55)\) would contradict the corresponding obstruction. This proves the exponents 15, 21, and 27 stated above.

## Limits

There is no conclusion here about arbitrary original factor signs, more than two ternary defects, or the existence of an infinite successful sequence. In particular, the companion upper bound \(B(N)=O(\log N)\) and these first three lower bounds do not contradict each other. Any future search using analytic inequalities must certify its numerical enclosures rather than prune from unchecked floating-point estimates.
