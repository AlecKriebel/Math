# The Exact Antipodal Bound in Dimension Five

This note proves a restricted but exact theorem:

\[
\max\{|C|:C\subset S^4,\ C=-C,\ 
             \langle x,y\rangle\leq\tfrac12\ (x\ne y)\}=40.
\]

It does **not** assume that a maximum kissing configuration is antipodal and
does not prove an upper bound for general 5-dimensional spherical codes.

## From antipodal points to unoriented lines

Let \(C=-C\) be a kissing configuration.  No point equals its antipode, so
\(C\) is the disjoint union of \(M=|C|/2\) pairs
\(\{u_i,-u_i\}\).  Choose one representative \(u_i\) from each pair.  For
\(i\ne j\), both \(u_j\) and \(-u_j\) belong to \(C\).  Applying the kissing
inequality to \(u_i,u_j\) and to \(u_i,-u_j\) gives

\[
\langle u_i,u_j\rangle\leq\tfrac12,\qquad
-\langle u_i,u_j\rangle\leq\tfrac12.
\]

Consequently

\[
|\langle u_i,u_j\rangle|\leq\tfrac12.                 \tag{1}
\]

Conversely, any \(M\) unit vectors satisfying (1) yield an antipodal
\(2M\)-point kissing configuration by adjoining both signs.  It therefore
suffices to prove that at most 20 unoriented lines satisfy (1).

## A projective linear-programming bound

Use the normalized dimension-five Gegenbauer polynomials

\[
P_0(t)=1,\qquad P_1(t)=t,\qquad
(k+2)P_k(t)=(2k+1)tP_{k-1}(t)-(k-1)P_{k-2}(t).
\]

In particular,

\[
P_2(t)=\frac{5t^2-1}{4},\qquad
P_4(t)=\frac{21t^4-14t^2+1}{8}.
\]

The auxiliary polynomial

\[
f(t)=t^2\left(t^2-\frac14\right)
    =\frac1{28}P_0(t)+\frac13P_2(t)+\frac8{21}P_4(t)       \tag{2}
\]

has nonnegative Gegenbauer coefficients, has positive constant coefficient
\(f_0=1/28\), and satisfies \(f(t)\leq0\) throughout
\([-1/2,1/2]\).  Also \(f(1)=3/4\).

For completeness, the positive-definite part of the Delsarte argument is
spelled out.  By the spherical-harmonic addition formula, for every \(k\)
there are evaluation vectors \(\Phi_k(u)\) such that

\[
P_k(\langle u,v\rangle)
 =\langle\Phi_k(u),\Phi_k(v)\rangle .
\]

Thus

\[
\sum_{i,j=1}^{M}P_k(\langle u_i,u_j\rangle)
 =\left\|\sum_{i=1}^{M}\Phi_k(u_i)\right\|^2\geq0.        \tag{3}
\]

Applying (2), (3), and the sign of \(f\) on the off-diagonal interval gives

\[
\frac1{28}M^2
\leq\sum_{i,j=1}^{M}f(\langle u_i,u_j\rangle)
\leq M f(1)=\frac34M.
\]

Hence \(M\leq21\).

## The equality case \(M=21\) is impossible

Suppose \(M=21\).  The two ends of the preceding inequality chain are then
equal.  Equality in the upper inequality forces

\[
f(\langle u_i,u_j\rangle)=0\qquad(i\ne j),
\]

because every one of those summands is nonpositive.  Therefore every
off-diagonal inner product lies in

\[
\left\{-\frac12,0,\frac12\right\}.                       \tag{4}
\]

Equality in the lower inequality also forces the \(P_2\) contribution in
(3) to vanish, since its coefficient \(1/3\) in (2) is strictly positive.
This is stronger than merely knowing a scalar total is zero: (3) says

\[
\left\|\sum_j\Phi_2(u_j)\right\|^2=0,
\]

so \(\sum_j\Phi_2(u_j)=0\).  Taking its inner product with
\(\Phi_2(u_i)\) proves the rowwise identity

\[
\sum_{j=1}^{21}P_2(\langle u_i,u_j\rangle)=0
\qquad\text{for every }i.                                \tag{5}
\]

Fix \(i\), and let \(b_i\) be the number of the other 20 lines whose
representatives have inner product of absolute value \(1/2\) with \(u_i\).
Using

\[
P_2(1)=1,\qquad P_2(0)=-\frac14,\qquad
P_2(\pm\tfrac12)=\frac1{16}
\]

in (4)--(5) gives

\[
0=1+\frac{b_i}{16}-\frac{20-b_i}{4}
  =-4+\frac{5b_i}{16}.
\]

This would require \(b_i=64/5\), impossible because \(b_i\) is an integer.
Thus \(M\leq20\).

## Sharpness

For each \(1\leq i<j\leq5\) and
\(\sigma\in\{-1,+1\}\), take the line represented by

\[
u_{ij}^{\sigma}=\frac{e_i+\sigma e_j}{\sqrt2}.
\]

These are 20 distinct unoriented lines.  Two representatives have absolute
inner product at most \(1/2\): their supports are disjoint, overlap in one
coordinate, or coincide as a coordinate pair with opposite choices of
\(\sigma\).  Adjoining both signs gives precisely the normalized \(D_5\)
root system of 40 points.  Therefore the antipodal maximum is exactly 40.

## Boundary and scope audit

- Condition (1) uses both signs in \(C\), so neither the \(+1/2\) nor
  \(-1/2\) boundary is discarded.
- The polynomial is nonpositive on the entire closed interval
  \([-1/2,1/2]\); equality cases are retained and then eliminated exactly.
- No rationality, rigidity, contact-graph, or lattice assumption is imposed
  on the hypothetical 21 lines.
- The conclusion applies only to antipodal configurations.  A general
  41--44 point code need not determine a projective code satisfying (1).

## Reproduction

Run:

```sh
python3 verifiers/verify_antipodal_bound.py
python3 -m unittest tests.test_antipodal_bound -v
```
