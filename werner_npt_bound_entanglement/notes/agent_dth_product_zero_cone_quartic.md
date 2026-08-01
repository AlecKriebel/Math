# Complete product-corner zero cone and its quartic deficit

## Status

The degenerate product-corner theorem proves that every quadratic cluster
shift at \(z_0=|000\rangle\) is nonpositive.  This note classifies every
direction for which that quadratic bound is an equality and computes the
next nonzero coefficient along its straight ray.

After quotienting the infinitesimal local-unitary directions, the result is:

1. one active weight-two pair may be arbitrary;
2. if two or three pairs are active, every pair matrix must be a scaled
   unitary;
3. three active pairs obey one exact skew-holonomy equation;
4. every multi-pair zero-Hessian ray has a strictly negative quartic
   coefficient;
5. the only nonzero rays with both zero quadratic and zero quartic terms
   are the rank-one single-pair rays, which lie in the exact physical
   equality branches.

This settles the straight-ray quartic normal form.  A full neighborhood
theorem still has to control curved arcs and higher-order gauge corrections.

## 1. Pair effective spaces

Put \(V_i=e_0^\perp\cong\mathbb C^2\).  A weight-two component on the
pair \(ij\) is represented by a matrix

\[
 Z_{ij}\in\operatorname{Hom}(V_j,V_i).
\]

Let

\[
 n=\|Z\|_2^2,
 \qquad d=|\det Z|.
\]

The exact effective spectrum is

\[
 -{n\over8}^{(4)},\qquad +{d\over4}^{(2)},
 \qquad -{d\over4}^{(2)}.
\tag{1}

In singular coordinates \(Z=\operatorname{diag}(b,c)\), define the
matched plane

\[
 E_Z=\operatorname{span}\{|00\rangle,|11\rangle\}
 \subset V_i\otimes V_j.
\tag{2}

If \(2d<n\), the unique maximizing four-plane of the pair effective
operator is

\[
 \boxed{E_Z\otimes V_k.}
\tag{3}

If \(2d=n\), then \(Z=\alpha U\) is a scaled unitary.  Let
\(\beta_Z\in V_i\otimes V_j\) be its positive maximally entangled
eigenvector and put

\[
 A_Z=\mathbb C\beta_Z\otimes V_k.
\tag{4}

The effective operator is

\[
 {n\over8}(2P_{A_Z}-I),
\]

and a four-plane is maximizing exactly when it contains \(A_Z\).

## 2. Common-maximizer classification

Let \(\delta\) have no weight-one component; those directions are tangent
to the local-unitary orbit and their effective operator vanishes.  Write

\[
 \delta=\delta_{12}+\delta_{13}+\delta_{23}+\delta_{123}.
\]

The product-corner splitting and Ky--Fan equality condition show that the
quadratic coefficient vanishes only if \(\delta_{123}=0\) and all active
pair effective operators have a common maximizing four-plane.

### Theorem 1

For nonzero \(\delta\), the quadratic cluster coefficient is zero if and
only if one of the following holds.

1. Exactly one \(Z_{ij}\) is active; it is arbitrary.
2. Exactly two are active, and both are scaled unitaries.
3. All three are active, all are scaled unitaries, and their coefficient
   matrices satisfy

   \[
   \boxed{
   (Z_{12}^{-1})^{\mathsf T}Z_{23}Z_{13}^{-1}
   \ \text{is proportional to}\
   J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
   }
   \tag{5}
   \]

### Proof

If an active matrix is not a scaled unitary, its maximizing space (3) is
unique.  It cannot equal a maximizing space belonging to another pair.
Indeed, equality of

\[
 E_{12}\otimes V_3
 \quad\text{and}\quad
 E_{13}\otimes V_2
\]

would make the common space invariant under both
\(\operatorname{End}(V_2)\) and \(\operatorname{End}(V_3)\).  It would
therefore be \(L_1\otimes V_2\otimes V_3\), which is impossible because
the matched plane \(E_{12}\) has two-dimensional support on \(V_1\).
Likewise, a maximally entangled top space \(A_{13}\) cannot be contained
in \(E_{12}\otimes V_3\): its contractions over \(V_3\) span all of
\(V_1\otimes V_2\).  Thus multiple active pairs must all be scaled
unitaries.

For two scaled-unitary pairs, the two spaces (4) have zero intersection.
Their direct sum is a common maximizing four-plane.

For three pairs, use local unitaries to put

\[
 \beta_{12}=|00\rangle+|11\rangle,
 \qquad
 \beta_{13}=|00\rangle+|11\rangle.
\]

The sum \(A_{12}+A_{13}\) has dimension four.  A direct two-qubit
contraction gives

\[
 (A_{12}+A_{13})\cap(e_r\otimes V_2\otimes V_3)
 =\mathbb C e_r\otimes
   (|01\rangle-|10\rangle),
 \qquad r=0,1.
\tag{6}

Hence it contains \(A_{23}\) precisely when \(\beta_{23}\) is the
antisymmetric Bell vector.  Undoing the local bases gives (5).  This proves
the classification. \(\square\)

For real scaled orthogonal matrices, (5) is the angle relation observed in
the numerical zero cone.  In the orientation-preserving chart it reads

\[
 \theta_{12}-\theta_{13}+\theta_{23}=\pm{\pi\over2}pmod\pi.
\]

## 3. Quartic coefficient: one active pair

Suppose only \(Z_{12}\) is active.  The entire ray factors at the third
site, and local singular coordinates give

\[
\boxed{
 \mathcal F\left(
 {z_0+t\delta_{12}\over\sqrt{1+t^2\|Z_{12}\|^2}}
 \right)
 ={1\over2}-|\det Z_{12}|^2t^4+O(t^6).
}
\tag{7}

The coefficient vanishes exactly when \(\operatorname{rank}Z_{12}\le1\).
In that case the complementary \(3\times3\) coefficient matrix has rank at
most two for every \(t\), so the whole ray is an exact physical equality
ray.

To obtain (7), put \(Z=\operatorname{diag}(b,c)\).  The two leading local
double-Hodge singular values come from the diagonal block

\[
 {1\over2}\begin{pmatrix}
 0&tc&tb\\ tc&0&1\\ tb&1&0
 \end{pmatrix}.
\]

Its small eigenvalue is \(-bc\,t^2+O(t^4)\).  The sharp local identity is
one half of the squared Frobenius norm minus the square of this small
eigenvalue, proving (7).

## 4. Quartic coefficient: several active pairs

Suppose two or three pairs are active and satisfy Theorem 1.  Write

\[
 Z_e=\alpha_eU_e,
 \qquad \alpha_e>0,
\]

with \(U_e\) unitary, and let \(\mathcal E\) be the active edge set.

### Theorem 2

Along the normalized straight ray,

\[
\boxed{
 \mathcal F(z(t))
 ={1\over2}-\left[
 \sum_{e\in\mathcal E}\alpha_e^4
 +{1\over2}\sum_{e<f}\alpha_e^2\alpha_f^2
 \right]t^4+O(t^6).
}
\tag{8}

In particular, every nonzero multi-pair zero-Hessian direction has a
strictly negative quartic coefficient.

### Proof

Gauge two active Bell vectors to the standard symmetric Bell vector; if a
third is active, (5) gauges it to the antisymmetric Bell vector.  Put

\[
 s=\sum_e\alpha_e^2,
 \qquad p=\sum_{e<f}\alpha_e^2\alpha_f^2,
 \qquad u=t^2.
\]

The two identical high-spectral blocks have the exact quartic factor

\[
\begin{aligned}
q(\lambda,u)={}&
\lambda^2(\lambda-1)^2
+4su\lambda^2(1-\lambda)\\
&+u^2\left[(4s^2+6p)\lambda^2
            -(4s^2-6p)\lambda\right]\\
&-12spu^3\lambda+9p^2u^4.
\end{aligned}
\tag{9}

Let the two roots tending to one be

\[
 \lambda_\pm=1+A_\pm u+B_\pm u^2+O(u^3).
\]

Substitution in (9) gives

\[
 A_\pm^2-4sA_\pm+12p=0,
\]

and then

\[
 A_++A_-=4s,
 \qquad
 B_++B_-=-4s^2+6p.
\tag{10}

Each root occurs twice in the full squared spectrum.  The tensor norm is
\(1+2su\), so (10) yields

\[
 \mathcal F(z(t))
 ={\lambda_++\lambda_-\over4(1+2su)}
 ={1\over2}+{-4s^2+6p\over4}u^2+O(u^3).
\]

Since \(s^2=\sum_e\alpha_e^4+2p\), this is exactly (8). \(\square\)

## 5. Remaining local lemma

Modulo local-unitary tangent directions, Theorems 1--2 show that every
fixed ray leaving the product corner is either:

- quadratically decreasing;
- quartically decreasing; or
- an exact rank-one single-pair equality ray.

To turn this blow-up classification into a full neighborhood theorem, one
must control curved arcs whose first derivative lies in the last cone and
whose higher jets leave it.  That is now the sole product-corner local
lemma; no additional zero-Hessian ray remains unclassified.

The exact verifier

```text
python3 verification/verify_dth_product_zero_cone_quartic.py
```

checks the common-maximizer incidence spaces and the universal high-block
polynomial (9) by exact multivariate arithmetic.
