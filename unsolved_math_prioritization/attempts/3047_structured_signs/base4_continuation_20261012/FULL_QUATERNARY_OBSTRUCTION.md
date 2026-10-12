# No base-four digit-multiplicative solution: binomial pools and a parity-refined zero bound

**Public evidence note (12 October 2026).** This proof uses computer-assisted exhaustive enumeration. The complete mathematical argument, exact domains and transitions, all frontier cardinalities, abstract depth-first encoding and full substantive independent review are distributed in prose. The executable programs, raw tree and detailed machine reports used in the historical verification are not distributed in this appendix. This is not an executable public replay package. Degree 77 is the empty level of the combined coefficient-plus-global-Jensen search, not a claimed sharp coefficient-only threshold.


## Theorem and precise scope

Keep every original factor of the unrestricted-partition product. Suppose its signs are base-four digit multiplicative:
\[
F_m(q)=\prod_{j\ge0}
\left(1+a_{m,j}q^{m4^j}+b_{m,j}q^{2m4^j}+c_{m,j}q^{3m4^j}\right),
\qquad a_{m,j},b_{m,j},c_{m,j}\in\{-1,1\}. \tag{1}
\]
All three signs in every block are independent. Unique base-four expansion makes every original coefficient of \(F_m\) exactly \(+1\) or \(-1\).

**Theorem (computer-assisted).** No assignment of the signs in (1) makes every Taylor coefficient of \(P(q)=\prod_{m\ge1}F_m(q)\) lie in \(\{-1,0,1\}\).

The class (1) contains the binary-digit-multiplicative class: pair adjacent binary digit factors. It also permits cubic coefficient signs inconsistent with such a pairing. There is no restriction on how many of those inconsistencies occur. This theorem remains a partial result for Newman's original problem, which has independently assignable signs on every coefficient, with no digit-product assumption. No novelty or priority claim is made.

The proof assumes the desired coefficient alphabet at **all degrees**, derives finitely many exact necessary analytic inequalities, and combines them with exact coefficient tests. The combined search becomes empty at degree 77. This is not asserted to be a sharp unconditional coefficient-prefix obstruction: an analytically rejected prefix can still have good coefficients through degree 77 or later.

## 1. Exact classification of the eight cubic blocks

For \(a,b\in\{-1,1\}\), define
\[
C_{a,b}(z)=1+az+bz^2+abz^3=(1+az)(1+bz^2),
\]
\[
D_{a,b}(z)=1+az+bz^2-abz^3.
\]
The four \(C\)-blocks have only unit-circle roots. They are exactly the four blocks whose cubic sign equals the product of their first two signs. Call each of the four remaining \(D\)-blocks a defect.

Let \(T\) be the unique real root greater than 1 of
\[
h(x)=x^3-x^2-x-1.
\]
Indeed, \(h'(x)=(3x+1)(x-1)\), its two critical values are
\(h(-1/3)=-22/27\) and \(h(1)=-2\), and \(h(2)=1\). Both critical values are negative, so \(h\) has exactly one real root \(T\), with \(1<T<2\). Its other two roots form a nonreal conjugate pair. The product of all three roots is 1, so each nonreal root has modulus \(T^{-1/2}\).

If \(b=+1\), then
\[
D_{+,+}(z)=-h(z),\qquad D_{-,+}(z)=D_{+,+}(-z).
\]
These blocks have two inner roots of modulus \(T^{-1/2}\) and one outer root of modulus \(T\).

If \(b=-1\), then
\[
D_{-,-}(z)=z^3h(1/z),\qquad D_{+,-}(z)=D_{-,-}(-z).
\]
These blocks have one inner root of modulus \(T^{-1}\) and two outer roots of modulus \(T^{1/2}\). In particular, none of the four \(D\)-blocks is cyclotomic. No general classification theorem for Littlewood polynomials is being assumed.

At a radius \(r=e^{-t}\), the Jensen contribution of a defect at exponent \(n\) is therefore exactly
\[
\begin{cases}
(\log T-nt)_+,&b=-1,\\
(\log T-2nt)_+,&b=+1.
\end{cases} \tag{2}
\]
For the second case the two inner roots are both counted: after substituting \(z=q^n\), their total contribution is \(2n(\log r+\log T/(2n))_+\). Thus equality of the four Mahler measures is not being confused with equality of their radial zero distributions.

For purely rational arithmetic we use
\[
R=1839/1000<T. \tag{3}
\]
The numerator of \(h(1839/1000)\), over denominator \(10^9\), is \(-1568281\). Since \(h\) is strictly increasing above 1, (3) follows. Replacing \(T\) by this lower bound weakens the necessary zero inequalities and can never discard a genuine solution.

## 2. A parity-refined Jensen upper bound

Every factor in (1), viewed in its original variable, has coefficients \(\pm1\). Reducing the full product modulo 2 therefore gives the ordinary unrestricted-partition product. If
\[
P(q)=\sum_{n\ge0}A_nq^n,
\]
then \(A_n\equiv p(n)\pmod2\), where \(p(n)\) is the number of unrestricted partitions. Put \(\pi_n=p(n)\bmod2\in\{0,1\}\). Under the desired alphabet,
\[
|A_n|^2=\pi_n \quad\text{for every }n. \tag{4}
\]
Thus the squared magnitudes are known even though their signs are not.

The infinite digit-block product converges locally uniformly in \(|q|<1\), because \(\sum_{m,j}r^{m4^j}<\infty\) for every \(r<1\). A sufficiently late tail is a nonvanishing exponential of uniformly convergent analytic logarithms. Its zeros are therefore exactly the block zeros, with multiplicities added, including coincidences. Jensen's formula, concavity of logarithm, Parseval's identity, and (4) yield
\[
J_P(r):=\frac1{2\pi}\int_0^{2\pi}\log|P(re^{i\theta})|\,d\theta
\le\frac12\log\sum_{n\ge0}\pi_n r^{2n}. \tag{5}
\]
Boundary-root radii follow by a limit and contribute zero at those roots. The elementary convergence and Jensen arguments are detailed in the companion [interior-zero proof](../continuation_20261012/INTERIOR_ZERO_BOUND.md); no real-radius lower bound is used here.

Only the finite parity prefix through \(J=512\) is needed. Since \(0\le\pi_n\le1\),
\[
\sum_{n\ge0}\pi_nr^{2n}
\le U_r:=\sum_{n=0}^{512}\pi_nr^{2n}
+\frac{r^{1026}}{1-r^2}. \tag{6}
\]
This uses no assertion about the density or distribution of partition parity.

The bits \(\pi_0,\ldots,\pi_{512}\) are computed by an exact partition update modulo 2. Start with \(v_0=1,v_n=0\) for \(n>0\). For each part \(m=1,\ldots,512\), update \(v_n\leftarrow v_n+v_{n-m}\pmod2\) for increasing \(n=m,\ldots,512\). After part \(m\), the array is the coefficient sequence modulo 2 of \(\prod_{i=1}^m(1-q^i)^{-1}\): the increasing update sums all possible numbers of copies of the new part. This induction proves the computation without a parity conjecture. A separate pentagonal-number recurrence gives the same 513 bits as a check.

## 3. Finite, entirely rational pruning inequalities

Use the rational radii
\[
r=\frac{b-1}{b},\qquad
b\in\{2,3,4,6,8,12,16,24,32,48,64,96,128,192,256,384,512,768,1024,1536,2048\}. \tag{7}
\]
For any known defect, assign it a weight \(w=n\) if its quadratic sign is negative, and \(w=2n\) if that sign is positive. By (2)–(3), its exact zero contribution is at least
\((\log R+w\log r)_+\).

For each radius, retain just the known defects satisfying \(Rr^w>1\). Let \(K\) count these defects with multiplicity, and let \(S\) be the sum of their weights with multiplicity. Unknown defects contribute nonnegatively and may be omitted. Equations (5)–(6) imply the necessary condition
\[
R^{2K}r^{2S}\le U_r. \tag{8}
\]
All parts of this test are rational.

More explicitly, set \(a=b-1\), \(X=a^2\), \(Y=b^2\), and
\[
H=\sum_{n=0}^{512}\pi_nX^nY^{512-n},
\quad U_{\rm num}=(Y-X)H+X^{513},
\quad U_{\rm den}=Y^{512}(Y-X).
\]
Then \(U_r=U_{\rm num}/U_{\rm den}\). A weight contributes precisely when
\[
1839a^w>1000b^w.
\]
Reject a candidate precisely when, for some radius in (7),
\[
\boxed{\quad
1839^{2K}a^{2S}U_{\rm den}
>1000^{2K}b^{2S}U_{\rm num}.
\quad} \tag{9}
\]
These are arbitrary-precision integer comparisons. No floating-point root approximation, logarithm, tolerance, or density estimate enters a pruning decision. Repeated weighted defect profiles can reuse their exact result.

## 4. Binomial pools remove irrelevant pairings

There are \(d_n=1+v_4(n)\) original base-four blocks at exponent \(n\), one for each pair \((m,j)\) with \(m4^j=n\). A nondefective block splits into a binomial at exponent \(n\) and a binomial at exponent \(2n\). View these as a pair of slots belonging to an edge from pool \(n\) to pool \(2n\).

The pool at exponent \(n\) contains \(d_n\) first slots of edges at \(n\), and, when \(n\) is even, \(d_{n/2}\) second slots of edges at \(n/2\). Its total size is
\[
D_n=d_n+\mathbf1_{2\mid n}d_{n/2}=1+v_2(n). \tag{10}
\]
To check (10), write \(v_2(n)=2h\) or \(2h+1\) and evaluate the two floor divisions by 2. Let \(C_n\in\{0,\ldots,D_n\}\) count positive-sign binomials in this pool. The cyclotomic baseline is
\[
\prod_{n\ge1}(1+q^n)^{C_n}(1-q^n)^{D_n-C_n}. \tag{11}
\]
Individual allocations of the signs in a pool to its two edge groups are not needed until a defect uses those slots.

At edge \(l\), let \(k_0,k_1,k_2,k_3\) count defects of types
\[
(a,b)=(-1,-1),\ (-1,+1),\ (+1,-1),\ (+1,+1),
\]
respectively. Require
\[
k_i\ge0,\qquad k_0+k_1+k_2+k_3\le d_l. \tag{12}
\]
A defect consumes one first slot of sign \(a\) from pool \(l\) and one second slot of sign \(b\) from pool \(2l\), replacing their \(C_{a,b}\)-block by \(D_{a,b}\).

When edge \(l\) is finalized, edge \(l/2\), if present, has already been finalized. Let \(p_-\) and \(p_+\) count its consumed second slots of negative and positive sign; they are zero for odd \(l\). The complete pool-capacity restrictions needed now are
\[
\begin{aligned}
k_0+k_1+p_-&\le D_l-C_l,&
 k_2+k_3+p_+&\le C_l,\\
k_0+k_2&\le D_{2l}-C_{2l},&
 k_1+k_3&\le C_{2l}.
\end{aligned} \tag{13}
\]
Here \(p_-=k_0^{(l/2)}+k_2^{(l/2)}\) and
\(p_+=k_1^{(l/2)}+k_3^{(l/2)}\).
The later edge \(2l\) will check its own first-slot consumption against the second-slot consumption already recorded at pool \(2l\).

### Why this representation preserves all freedoms

Every actual base-four array supplies counts satisfying (10)–(13): each defect consumes exactly the indicated original slots. Conversely the slot restrictions also suffice for simultaneous realization of any prescribed finite defect data and pool counts. At one pool, each of its two components has a fixed capacity. The number of already consumed slots in each component does not exceed that capacity, by (12). Their total positive and negative consumptions fit the pool's available positive and negative signs, by (13). Assign the remaining positive signs to any remaining slots, then the remaining negative signs. This is possible because both remaining counts are nonnegative and sum to the number of free slots. Pools may be completed independently.

At one edge, first pair the designated consumed first and second slots to realize its four specified defect counts. Pair its remaining first and second slots arbitrarily; these are nondefective blocks and their product depends only on the two margins, because \(C_{a,b}=(1+az)(1+bz^2)\). Assign the resulting blocks to the distinct original labels \((m,j)\) with \(m4^j=l\). Different edges use disjoint block labels, so this is a consistent original digit assignment. Slots or pools beyond a finite truncation may be filled arbitrarily. This construction also explains why choosing the internal pairings earlier would enumerate redundant histories.

For the obstruction itself, the necessity direction alone would suffice: every hypothetical infinite solution must map to a retained state. No possible original sign array is excluded merely because its pool allocation was not explicitly recorded.

## 5. Exact deferred recurrence

A degree-\(N\) state records:

- all pool counts \(C_1,\ldots,C_N\);
- all four defect counts for edges \(l\le\lfloor N/3\rfloor\).

Before its cubic degree \(3l\), edge \(l\)'s defect choice cannot change a coefficient: the ratio
\[
D_{a,b}(q^l)/C_{a,b}(q^l)=1-2abq^{3l}+O(q^{4l}). \tag{14}
\]
Represent a state by the truncated polynomial formed from its known baseline pools and all its finalized defect ratios. The capacity restrictions guarantee that each denominator binomial can be canceled against a remaining baseline slot, so this rational notation represents a polynomial. Future pools and future defect ratios cannot affect the already checked coefficient prefix.

From a state through degree \(N-1\), let \(A_N\) be the degree-\(N\) residual of this polynomial.

- If \(3\mid N\), set \(l=N/3\) and enumerate every quadruple satisfying (12)–(13), using the already known pools \(l\) and \(2l<N\). Otherwise use the zero quadruple and finalize no edge.
- Enumerate every \(C\in\{0,\ldots,D_N\}\) for the fresh pool.
- Test all newly known defects by (9).
- Retain precisely the children satisfying
\[
\boxed{\quad
\left|A_N+2C-D_N-2(k_0-k_1-k_2+k_3)\right|\le1.
\quad} \tag{15}
\]
The signs in the last term are the four values of \(ab\), in the stated order. Equation (14) and the fresh pool's first term \((2C-D_N)q^N\) prove (15). All changes begin in degree \(N\), so previously checked coefficients remain unchanged.

Assume an infinite solution exists. Its pool counts and finalized defect counts occur in every enumerated domain, its coefficient satisfies (15), and all its known defects satisfy (9) by the global bound. Restricting it degree by degree therefore places its state in every retained frontier. This is a complete necessary-condition search, not a heuristic search for promising candidates.

The producer updates the polynomial by truncated multiplication with the ratios (14) and the new signed binomials. It checks every polynomial multiply-and-add for signed 64-bit overflow with a 128-bit intermediate and aborts upon overflow; the verified run does not overflow. All rational-bound computations use GMP arbitrary-precision integers. Every ratio denominator has constant 1. A separately reconstructed product or logarithmic-derivative calculation can verify the coefficient residuals without this update routine.

## 6. Complete finite computation and abstract tree encoding

The frontier cardinalities from degree 0 through degree 77 are

```
1,2,2,8,16,20,112,154,144,180,142,90,594,714,1142,1150,
2156,2238,7150,3806,5758,5372,4584,5674,29476,13318,11000,
8180,7264,8146,12972,8400,15206,26464,23360,28706,73168,
98652,136190,212164,142444,144528,158604,163204,195886,
120014,74666,39822,133318,126584,100146,119696,207648,
269572,710118,348552,557414,284010,226614,143066,418034,
325708,276732,404918,391572,278924,358832,252246,430532,
659692,447398,209804,631594,656356,244958,141300,2708,0.
```

There are 11,151,089 nonempty states, including the root. The peak is 710,118 states at degree 54. The final nonempty frontier has 2,708 states at degree 76, and degree 77 is empty. The exact run records 9,107,474 attempted defect choices rejected by (9), 26,095,524 coefficient-test rejections, and 70,639 rejected versus 15,992 accepted distinct weighted defect profiles. These diagnostic counts do not substitute for checking all transitions.

The historical verification retained every state as a path in the complete depth-first prefix tree, not merely as a count or checksum. That raw tree is not distributed in this appendix. Its full abstract encoding is specified here: the root is implicit. At a node of depth \(L\), a child for step \(n=L+1\) is encoded as follows:

1. One byte gives \(C_n\), between 0 and 7 in this computation.
2. If \(3\mid n\), the next byte is \(k_0+4k_1+16k_2+64k_3\). Each digit is at most 3 since \(l=n/3\le25\) at all nonempty levels.
3. The child's complete subtree follows immediately.
4. A byte of value 255 where a child-count byte would appear closes the current node. It cannot be confused with a legal \(C_n\).

The byte after a cubic-step count is always interpreted as a defect code, never as a terminator. The file must end exactly when the root closes. This representation retains the full path of every state while avoiding repetition of its prefixes. The uncompressed tree has 26,819,297 bytes.

The producer enumerates defect quadruples lexicographically in \((k_0,k_1,k_2,k_3)\), then fresh pool counts in increasing order. A verifier can consume the tree in precisely that order while independently enumerating every legal transition. A missing child, extra child, changed domain value, premature terminator, or trailing data must be rejected. It must also recompute the parity bits and all rational pruning bounds, verify coefficient residuals by a distinct arithmetic method, and check the entire tree rather than only its cardinalities.

The historical verification checked the exact counts, encoding, rational constants and radii, and all 513 exact parity bits with their two-method comparison. The final original computation truncates at 78, above the empty level. A preliminary truncation-100 run gave the same complete counts. The fixed-limit-78 run and the independently verified complete prefix tree are the finite computation supporting this result. The full substantive [independent review](REVIEW_FULL_QUATERNARY.md) describes the verification; the raw tree and machine reports are not distributed here.

Since a hypothetical infinite solution would contribute a state at every level, the empty degree-77 frontier contradicts its existence. This proves the stated restricted-family theorem once the retained exact computation is verified. The subsequent full [independent review](REVIEW_FULL_QUATERNARY.md) completed that verification within the stated scope.

## 7. Context and boundaries

[David Newman's unrestricted question](https://www.openproblemgarden.org/op/dividing_up_the_unrestricted_partitions) allows independent coefficient signs across and within all original factors. The base-four digit rule (1) still imposes relations within a factor, so it is a genuine restriction.

[Andrews and Newman, *Binary Representations and Theta Function*, Integers 18 (2018), A34](https://math.colgate.edu/~integers/s34/s34.pdf), motivates digit-product identities on specified dilates. Here all positive integer dilates remain present. The proof neither deletes even factors nor substitutes an identity for a different product.

No claim is made about arbitrary sign arrays, the sharp longest base-four finite prefix, or any partition-parity density. The parity refinement uses only exact finitely computed bits and the trivial tail bound. The complex-zero restrictions are compatible with the fact that arbitrary finite collections of signed factors can suppress the positive real radius.
