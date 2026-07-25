# A robust degree-11 enlarged-cap bound

## Theorem

Fix \(e\in S^4\).  Let \(C\subset S^4\) be a kissing code:
\(\langle x,y\rangle\leq1/2\) for distinct \(x,y\in C\).  If
\[
\langle e,x\rangle\geq-\frac1{300}\qquad(x\in C),
\]
then
\[
\boxed{|C|\leq34.}                                        \tag{1}
\]

This is an exact computer-assisted theorem.  It reuses the integer Gram
factors from the certified degree-11 hemisphere kernel, but audits them on a
strictly larger closed domain.  The verifier authenticates the source
certificate by SHA-256 and factor-payload hash.  It then uses only Python's
standard library and exact `Fraction` arithmetic.

## 1. The positive kernel

For \(u=\langle e,x\rangle\), \(v=\langle e,y\rangle\), and
\(t=\langle x,y\rangle\), let \(F(u,v,t)\) be the degree-11 polynomial
defined by the exact positive-semidefinite Gram blocks in
[`one_sided_cap_degree11_bound.md`](one_sided_cap_degree11_bound.md).
For every finite \(C\subset S^4\),
\[
\sum_{x,y\in C}F(u_x,u_y,\langle x,y\rangle)\geq0.          \tag{2}
\]
This follows from the homogeneous-harmonic addition formula and the exact
Gram decompositions \(F_k=L_kL_k^{\mathsf T}\).  No sign restriction on
\(u_x\) is needed for positivity, so the same kernel applies on the enlarged
cap.

## 2. Exact enlarged-domain inequalities

The new certificate
[`../certificates/one_sided_cap_degree11_robust_1_over_300.json`](../certificates/one_sided_cap_degree11_robust_1_over_300.json)
and verifier prove
\[
F(u,u,1)\leq\frac{3291}{100}
\quad\left(-\frac1{300}\leq u\leq1\right),                 \tag{3}
\]
and
\[
F(u,v,t)\leq-\frac{121}{125}                               \tag{4}
\]
on the complete closed domain
\[
\mathcal D_{1/300}=\left\{\begin{array}{l}
-1/300\leq u,v\leq1,\quad -1\leq t\leq1/2,\\
1+2uvt-u^2-v^2-t^2\geq0.
\end{array}\right.                                         \tag{5}
\]

The determinant inequality in (5) is exactly positive semidefiniteness of
the Gram matrix of \(e,x,y\); hence no geometrically feasible pair is
discarded.

## 3. Exact Bernstein audit

The verifier maps the enlarged box to the unit cube by
\[
u=-\frac1{300}+\frac{301}{300}a,\qquad
v=-\frac1{300}+\frac{301}{300}b,\qquad
t=-1+\frac32s.                                             \tag{6}
\]
It expands (6) exactly into the rational power basis and then converts to
the tensor Bernstein basis.

For (3), the degree-22 univariate margin
\(3291/100-F(u,u,1)\) is certified on five dyadic leaves, of maximum depth
three.

For (4), set \(H=-121/125-F\).  Starting from the full unit cube, the
verifier bisects \(a,b,s\) cyclically.  A leaf is accepted only when:

1. the maximum exact Bernstein coefficient of the transformed Gram
   determinant is strictly negative, so the whole box is infeasible; or
2. the minimum exact Bernstein coefficient of \(H\) is nonnegative.

The rebuilt tree has 6,053 leaves: 2,914 determinant-infeasible and 3,139
proved.  Its maximum depth is 30 and its ordered leaf digest is
```
8c61e175b7cd3b83e5140becb278c47a2c413bdf3e0cc034a0891f1e41b79eab
```
All endpoints, split points, coefficients, comparisons, and hashes are
exact.  No solver output or floating tolerance is used.

## 4. Summation

For \(n=|C|>0\), (2)--(4) give
\[
0\leq \frac{3291}{100}n-\frac{121}{125}n(n-1).
\]
Therefore
\[
n\leq1+\frac{3291/100}{121/125}
=\frac{16939}{484}
=35-\frac1{484}<35.                                       \tag{7}
\]
Since \(n\) is integral, \(n\leq34\), proving (1).

## 5. Consequences for a hypothetical 41-code

If \(C\) were a 41-point kissing code, apply (1) to every axis \(e\).
At most 34 points can satisfy
\(\langle e,x\rangle\geq-1/300\), so
\[
\boxed{\#\{x\in C:\langle e,x\rangle<-1/300\}\geq7}
\qquad(e\in S^4).                                         \tag{8}
\]
Applying the same statement to \(-e\) also gives
\[
\boxed{\#\{x\in C:\langle e,x\rangle>1/300\}\geq7}.         \tag{9}
\]
These are strict conclusions because points on the threshold belong to the
closed enlarged cap.

In particular, for each code point \(x\), at least seven of the other
40 points have inner product \(<-1/300\) with \(x\).  At least six of the
other points have inner product \(>1/300\): (9) counts at least seven points
including \(x\) itself.

This strengthens the quantitative separation of every hypothetical
41-code, but it does **not** improve the global bound
\(40\leq\tau(5)\leq44\), and it does not by itself rule out 41 points.

## 6. Boundary and numerical rigor

- The new faces \(u=-1/300\) and \(v=-1/300\) are included.
- The old equator, both poles when feasible, contacts \(t=1/2\), and every
  determinant-zero triple are included.
- Infeasible leaves require the strict exact test \(\max\Delta<0\).
- Proved leaves allow the non-strict exact test \(\min H\geq0\).
- Closed child boxes cover their parent, including split boundaries.
- The Gram blocks are PSD because they are exact Gram products; the verifier
  authenticates their entire source file and factor payload.
- Numerical degree-12/13 searches and enlarged-cap scans motivated the
  rational choice \(1/300\), but none is called or trusted by the verifier.
- Run verifiers without Python's `-O` flag because assertions are proof
  checks.

## 7. Reproduction and dependency map

From the project root:

```sh
python3 verifiers/verify_one_sided_cap_degree11_robust.py
python3 -m unittest tests.test_one_sided_cap_degree11_robust -v
```

The proof dependencies are
```text
degree-11 exact Gram factors + harmonic addition formula
                         |
                         v
             positive ordered-pair kernel
                    /              \
 enlarged diagonal audit      enlarged pair-domain tree
 F(u,u,1)<=3291/100           F<=-121/125
                    \              /
                     exact summation
                            |
                            v
               |C|<=16939/484<35
                            |
                            v
 seven points below -1/300 in every direction
```
