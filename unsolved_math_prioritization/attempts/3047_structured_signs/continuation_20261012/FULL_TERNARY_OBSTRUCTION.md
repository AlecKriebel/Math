# No ternary-digit-multiplicative solution to the unrestricted partition sign problem

**Public evidence note.** The finite obstruction below uses computer-assisted exhaustive enumeration. The complete recurrence, state domains, counts, explicit sharpness witnesses and substantive independent review are distributed in prose. The programs and raw frontier certificates used in the historical verification are not distributed in this appendix. This is not an executable public replay package; independent reimplementation is possible from the mathematical specification.


## Exact scope

Let every original unrestricted-partition factor remain present, and suppose its signs are ternary-digit multiplicative:
\[
F_m(q)=\prod_{j\ge0}
\bigl(1+u_{m,j}q^{m3^j}+v_{m,j}q^{2m3^j}\bigr),
\qquad u_{m,j},v_{m,j}\in\{-1,1\}. \tag{1}
\]
All the displayed signs are independent, including signs in infinitely many factors and digit positions. Unique ternary expansion shows that every coefficient of each original factor \(F_m\) is exactly \(+1\) or \(-1\).

**Theorem (computer-assisted).** No assignment in (1) makes every coefficient of \(P(q)=\prod_{m\ge1}F_m(q)\) belong to \(\{-1,0,1\}\).

This excludes the entire ternary-digit-multiplicative class, with no bound on the number of changed signs or noncyclotomic blocks. It does **not** settle the original problem with arbitrary independently assigned factor coefficients. Binary-digit and ternary-digit multiplicative families are different and neither contains the other.

The proof combines exact coefficient restrictions through degree 59 with finitely many necessary inequalities derived from the **assumed bound on every coefficient**. In particular, 59 is not asserted to be the first unavoidable coefficient degree for arbitrary finite ternary prefixes. A prefix discarded by an analytic inequality might have admissible coefficients through degree 59 or beyond. The contradiction concerns an infinite solution.

No novelty or priority claim is made.

## 1. Group all digit blocks without losing freedoms

Put
\[
C_-(z)=1-z+z^2,\quad C_+(z)=1+z+z^2,
\qquad D_-(z)=1-z-z^2,\quad D_+(z)=1+z-z^2.
\]
Call a \(D\)-block a defect. At exponent \(n\) there are exactly
\[
d_n=1+v_3(n)
\]
blocks: their labels are \((m,j)=(n/3^j,j)\), for \(0\le j\le v_3(n)\). Every possible multiset of these four block types at every exponent can be realized simultaneously by assigning the blocks to these labels. Labels at different exponents are disjoint. Sorting or counting identical blocks therefore loses no possible product.

Let \(c_n\) be the number of blocks at exponent \(n\) whose linear sign is positive. For later use let \(k^-_n\) and \(k^+_n\) be the numbers of negative-quadratic-sign blocks among the negative-linear-sign and positive-linear-sign groups, respectively. Their domains are
\[
0\le c_n\le d_n,\quad
0\le k^-_n\le d_n-c_n,\quad
0\le k^+_n\le c_n. \tag{2}
\]
These give counts of the four types as
\[
\#C_-=d_n-c_n-k^-_n,\quad
\#C_+=c_n-k^+_n,\quad
\#D_-=k^-_n,\quad
\#D_+=k^+_n.
\]
The total defect count at exponent \(n\) is \(b_n=k^-_n+k^+_n\).

## 2. A finite set of exact necessary zero inequalities

Write \(\varphi=(1+\sqrt5)/2\), and \(\lambda=\log\varphi\). Each \(C\)-block has only unit-circle roots; each \(D\)-block has one inner root of modulus \(\varphi^{-1}\). A \(D(q^n)\)-block therefore contributes exactly \((\lambda+n\log r)_+\) to Jensen's zero sum at radius \(r\). Coincident roots add their multiplicities.

Here is the required analytic justification. For each \(0<r<1\), the full digit-block product converges locally uniformly, since
\[
\sum_{m,j}r^{m3^j}<\infty.
\]
A sufficiently late product tail is the exponential of a uniformly convergent series of analytic logarithms, hence is nonzero. Thus no zeros can cancel and no extra zeros arise from the tail. Jensen's formula and the Taylor-coefficient bound then give
\[
\sum_{n\ge1}b_n(\lambda+n\log r)_+
=\frac1{2\pi}\int_0^{2\pi}\log|P(re^{i\theta})|\,d\theta
\le\frac12\log\sum_{k\ge0}|[q^k]P|^2r^{2k}
\le-\frac12\log(1-r^2). \tag{3}
\]
For a radius meeting a zero, use a limiting radius; its boundary-root contribution is zero. The detailed elementary Jensen argument is also given in the companion interior-zero note. For (3), the global bound \(|[q^k]P|\le1\) is essential.

We use only the following finite list of rational radii:
\[
r=\frac{b-1}{b},\qquad
b\in\{2,3,4,6,8,12,16,24,32,48,64,96,128,192,256,384,512,768,1024,1536,2048\}. \tag{4}
\]
Given any known finite set of defects, retain just the exponents \(n\) for which \(\varphi r^n>1\). Let \(K\) be their number, counted with multiplicity, and let \(S\) be the sum of their exponents, also with multiplicity. Omitting all unknown defects only decreases the nonnegative left side of (3), so a necessary condition is
\[
K\log\varphi+S\log r\le-\tfrac12\log(1-r^2).
\]
With \(a=b-1\), this is equivalent to
\[
\boxed{\quad A\varphi^{2K}\le B,\qquad
A=a^{2S}(b^2-a^2),\quad B=b^{2S+2}.\quad} \tag{5}
\]
All numbers except \(\varphi\) in (5) are positive integers.

### Exact algebraic comparisons

No numerical logarithms, floating-point approximations, or tolerance tests are needed. To decide which exponents contribute, put \(U=a^n,V=b^n\). Since \(2V-U>0\),
\[
\varphi a^n>b^n\quad\Longleftrightarrow\quad
5U^2>(2V-U)^2. \tag{6}
\]
Let \(F_j\) and \(L_j\) be the Fibonacci and Lucas integers, with \(F_0=0,F_1=1,L_0=2,L_1=1\). The identity
\[
2\varphi^{2K}=L_{2K}+F_{2K}\sqrt5
\]
follows from the quadratic equation \(\varphi^2=\varphi+1\), or the usual two-term recurrences. Put \(D=2B-AL_{2K}\). The necessary inequality (5) is violated precisely when

- \(D<0\); or
- \(D\ge0\) and \(5A^2F_{2K}^2>D^2\).

Thus all pruning decisions are integer comparisons. Repeated defect profiles can reuse the already determined result because neither the signs of the inner roots nor the unassigned linear signs affect this calculation.

## 3. Defer the quadratic sign until it first matters

A state at degree \(N\) records:

- every \(c_n\) for \(1\le n\le N\);
- every pair \((k^-_n,k^+_n)\) for \(1\le n\le\lfloor N/2\rfloor\).

For the remaining exponents \(N/2<n\le N\), temporarily set the quadratic signs positive. Their actual quadratic signs first affect degree \(2n>N\), so this convention changes no coefficient through degree \(N\). Omit groups of exponent greater than \(N\), which also cannot affect that prefix. Let \(Q\) be this finite, provisional block product.

At the next degree \(N\), from a state through \(N-1\), perform the following exhaustive choices:

1. If \(N\) is even, put \(l=N/2\) and choose every pair
   \(0\le k^-\le d_l-c_l\), \(0\le k^+\le c_l\), finalizing the quadratic signs at exponent \(l\). If \(N\) is odd, put \(k^-=k^+=0\) and do not finalize a group.
2. Choose every \(c\in\{0,\ldots,d_N\}\) for the fresh group at exponent \(N\).
3. Reject if any exact inequality (5) fails for the defects now known.
4. Let \(A_N=[q^N]Q\). Retain the child exactly if
\[
\boxed{\quad |A_N-2(k^-+k^+)+2c-d_N|\le1.\quad} \tag{7}
\]

To justify (7), switching \(C_\pm(q^l)\) to \(D_\pm(q^l)\) first changes the product by \(-2q^{2l}\). Formally,
\[
D_\pm(q^l)/C_\pm(q^l)=1-2q^{2l}+O(q^{3l}).
\]
Every one of the \(k^-+k^+\) switches therefore contributes \(-2\) at degree \(N=2l\). The fresh group contributes \(2c-d_N\), and no fresh change affects a lower degree. This proves the exact extension condition.

The producer updates its truncated polynomial by the rational expression
\[
\left(\frac{D_-(q^l)}{C_-(q^l)}\right)^{k^-}
\left(\frac{D_+(q^l)}{C_+(q^l)}\right)^{k^+}
C_+(q^N)^cC_-(q^N)^{d_N-c}
\]
when \(N\) is even, omitting the ratios when \(N\) is odd. The denominators have constant 1, and the domains (2) ensure the chosen blocks actually occur in the old product. Formal truncated inverses therefore give exactly the new finite product. Every polynomial multiply-and-add in the C++ producer is checked for signed 64-bit overflow using a 128-bit intermediate; an overflow aborts the run. Algebraic zero tests use arbitrary-precision GMP integers.

### Why no hypothetical solution can be omitted

Assume an infinite solution exists. At each degree, restrict it to the state just defined. Its fresh counts occur in the listed domains. Its coefficient satisfies (7), and its known defects satisfy (5), because these are necessary consequences of (3). Induction therefore places its state in every retained frontier. This implication does not require extending arbitrary retained states to infinite solutions.

No beam truncation, random sampling, quotienting of genuinely different count histories, or heuristic pruning is used. Identical commuting blocks are represented by counts, and the exact quadratic-sign deferral is the only scheduling of undecided variables.

## 4. Complete finite enumeration and abstract state encoding

The resulting frontier cardinalities from degree 0 through degree 59 are

```
1,2,4,8,20,32,152,212,268,250,314,230,794,1042,2278,1730,
3076,3446,14968,8862,14756,9612,8966,10942,27676,16688,
19590,18090,14662,16532,20604,14304,23588,33500,32200,
30962,55244,68302,88138,101822,34810,51650,9008,9162,
12886,11134,9522,8660,1920,2516,2584,1144,2468,2236,
6670,774,116,108,136,0.
```

There are 831,371 nonempty states in total, including the root. The largest frontier contains 101,822 states at degree 39. The last nonempty frontier has 136 states at degree 58. The degree-59 frontier is empty. The exact run also records 461,708 attempts rejected by the zero inequalities, using 22,788 distinct rejected defect profiles and 9,420 accepted profiles; these are diagnostics, not substitutes for completeness.

The historical verification retained and compared every state at levels 1 through 60. The following abstract fixed-length encoding specifies the states independently of any archive: at level \(L\), each record has exactly \(L\) integer entries. At step \(n\), the entry equals
\[
c_n+5k^-+25k^+,
\]
where \(k^-,k^+\) are the newly finalized choices for exponent \(n/2\) if \(n\) is even, and are zero otherwise. Every digit is at most 4 in this computation, so base-5 decoding is unique. The root is the implicit empty record. Level 60 is also empty and is retained only as a truncation-margin diagnostic. No state is represented merely by a checksum.

The counts, record specification and rational radii are given above. Historical integrity checks covered every complete frontier, separately from the exact state comparisons. The producer truncates at degree 60, above the first empty level. Exploratory runs with limits 100 and 160 gave the same frontier counts; the frozen proof relies on the exact fixed-limit-60 producer and the independently checked certificate.

A verifier can check every complete transition without using the producer's rational-quotient update: decode a parent, reconstruct its actual \(C_-,C_+,D_-,D_+\) counts, multiply those polynomial blocks directly or use their logarithmic derivatives to recover \(A_N\), and enumerate all domain choices in (2), (5), and (7). The exact child set must equal the next certified frontier, with root, domains, uniqueness, and first-empty property checked. A certificate containing only the counts would not suffice.

Since a hypothetical infinite solution would survive every level, the empty degree-59 frontier contradicts its existence. This completes the restricted-family theorem once the exhaustive computation is verified. The accompanying [independent review](REVIEW_FULL_TERNARY.md) records that completed verification.

## 5. Relationship to the original problem and sources

[David Newman's Open Problem Garden question](https://www.openproblemgarden.org/op/dividing_up_the_unrestricted_partitions) permits all coefficient signs independently. Equation (1) still relates coefficients within each original factor through their ternary digits. The theorem therefore remains a partial result for that original question.

[Andrews and Newman, *Binary Representations and Theta Function*, Integers 18 (2018), A34](https://math.colgate.edu/~integers/s34/s34.pdf), motivates digit-product methods through identities on specified dilate sets. The present argument retains all original factors and makes no substitution of an odd-only identity for the full product.

The coefficient-plus-zero-bound obstruction is different from the earlier sharp, coefficient-only binary-digit obstruction and from finite-active-factor radial estimates. It uses the distribution and multiplicity of complex zeros, not merely decay or growth on the positive real radius. No general obstruction for arbitrary sign arrays follows.
