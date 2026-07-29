# A no-go theorem for rank-one Bloch-controlled \(d=6\) solutions

**Date:** 2026-07-28

**Status:** PROVED within the stated ansatz
**Scope:** this excludes one exact, non-scalar color/face mechanism at
\(d=6\); it is not a nonexistence theorem for arbitrary exceptional
solutions.

## 1. Statement

Let
\[
V=\mathbb C^2\otimes\mathbb C^m,\qquad d=2m,
\]
let \(\psi_1,\ldots,\psi_d\) be an orthonormal basis of \(V\), and put
\(\Pi_j=|\psi_j\rangle\langle\psi_j|\).  For unit vectors
\(n_j\in\mathbb R^3\), define
\[
A_j=(n_j\cdot\sigma)\otimes I_m
\]
and
\[
H=\sum_{j=1}^{d} A_j\otimes\Pi_j.
\tag{1}
\]
Thus \(H\) is a rank-one controlled reflection.  It is automatically
Hermitian, satisfies \(H^2=I\), and has trace zero.

### Theorem

If \(m\leq 3\) and (1) satisfies
\[
H_{12}H_{23}H_{12}-H_{23}H_{12}H_{23}
=\frac13(H_{12}-H_{23}),
\tag{2}
\]
then \(m=2\).  In particular, no operator of the form (1) is an
exceptional solution in base dimension \(d=6\).

The proof does not assume scalar partial traces, Markov standardness,
faithfulness, or any representation-theoretic quotient.  Consequently it
also covers nonstandard solutions inside this ansatz.

## 2. The compressed cubic equations

Write
\[
e_{rs}=|\psi_r\rangle\langle\psi_s|,\qquad
a^{(k)}_{rs}=\langle\psi_r,A_k\psi_s\rangle,
\]
and let
\[
G_{rs}=n_r\cdot n_s,\qquad
C_{rs}=n_r\times n_s.
\]
Compress (2) on the third site by \(\Pi_k\).  Direct multiplication gives
\[
\begin{aligned}
&\sum_{r,s}a^{(k)}_{rs}A_rA_s\otimes e_{rs}
-\sum_r A_r\otimes A_k\Pi_rA_k\\
&\qquad =
\frac13\left(\sum_r A_r\otimes\Pi_r-I\otimes A_k\right).
\end{aligned}
\tag{3}
\]
The Pauli product rule
\[
(n_r\cdot\sigma)(n_s\cdot\sigma)
=(n_r\cdot n_s)I+i(n_r\times n_s)\cdot\sigma
\tag{4}
\]
separates (3) into its scalar and Pauli-vector coefficients on the qubit
factor of the first site.

The scalar coefficient is
\[
\boxed{G\circ[A_k]_\psi=-\frac13[A_k]_\psi,}
\tag{5}
\]
where \(\circ\) is entrywise multiplication and \([A_k]_\psi\) is the
matrix of \(A_k\) in the control basis.

For \(u\in\mathbb R^3\), put
\[
D_u=\sum_r (u\cdot n_r)\Pi_r,\qquad
(C_u)_{rs}=u\cdot(n_r\times n_s).
\]
The Pauli coefficient in direction \(u\) is
\[
\boxed{
i\,C_u\circ[A_k]_\psi-A_kD_uA_k=\frac13D_u.
}
\tag{6}
\]

Equation (5) is also what follows from the canonical-channel identity.
Indeed, for \(P=(I-H)/2\), the channel
\[
\mathcal E_L(X)=\frac2d\operatorname{Tr}_1
\bigl(P(I\otimes X)P\bigr)
\]
is, in the \(\psi\)-basis, the Schur multiplier with symbol
\[
s_{rs}=\frac{1+n_r\cdot n_s}{2}.
\tag{7}
\]
Taking the first partial trace of the projection form of (2) gives
\[
(\mathcal E_L\otimes\mathrm{id})(H)=\frac13H.
\]
Since the \(\Pi_k\) are linearly independent, this says
\(\mathcal E_L(A_k)=A_k/3\), which is equivalent to (5).
This confirms the suggested channel argument, with the important
orientation that \(\mathcal E_L\) traces the first leg of \(P\) and then
acts on the first leg of \(H\).

## 3. The Bloch vectors must span \(\mathbb R^3\)

Let
\[
S=\operatorname{span}_{\mathbb R}\{n_1,\ldots,n_d\}.
\]
Suppose \(\dim S\leq2\).  Choose a nonzero \(u\in S\).  Every cross product
\(n_r\times n_s\) is perpendicular to \(S\), so \(C_u=0\).  Equation (6)
then becomes
\[
A_kD_uA_k=-\frac13D_u.
\tag{8}
\]
The diagonal operator \(D_u\) is nonzero: otherwise \(u\) would be
orthogonal to every \(n_r\), hence to \(S\), while also belonging to \(S\).
But \(A_k\) is unitary, so conjugation by \(A_k\) preserves the
Hilbert--Schmidt norm.  Taking norms in (8) gives
\[
\|D_u\|_2=\frac13\|D_u\|_2,
\]
a contradiction.  Therefore
\[
\boxed{S=\mathbb R^3.}
\tag{9}
\]

This disposes of the lower-span branch directly.  The scalar channel
identity alone would not do so; the vector part (6) of the cubic relation is
essential.

## 4. The control basis is maximally entangled

Since \(G_{rr}=1\), the diagonal entries of (5) satisfy
\[
\langle\psi_r,A_k\psi_r\rangle=0
\qquad\text{for every }r,k.
\tag{10}
\]
The \(n_k\) span \(\mathbb R^3\), so (10) says that all three components of
the reduced-qubit Bloch vector of every \(\psi_r\) vanish.  Hence
\[
\operatorname{Tr}_{\mathbb C^m}
|\psi_r\rangle\langle\psi_r|=\frac12I_2.
\tag{11}
\]
Every control vector is therefore maximally entangled across
\(\mathbb C^2\otimes\mathbb C^m\).

Represent \(\psi_r\) by its \(2\times m\) coefficient matrix \(T_r\).
Equation (11) is
\[
T_rT_r^*=\frac12I_2,
\tag{12}
\]
so the row space of every \(T_r\) has dimension two.

## 5. Small multiplicity forces a complete Bloch graph

For \(r\neq s\), (5) gives
\[
\left(n_r\cdot n_s+\frac13\right)
\langle\psi_r,A_k\psi_s\rangle=0
\qquad\text{for every }k.
\tag{13}
\]
Suppose \(n_r\cdot n_s\neq-1/3\).  Then all the matrix elements in
(13) vanish.  Because the \(n_k\) span \(\mathbb R^3\),
\[
\langle\psi_r,(\sigma_a\otimes I_m)\psi_s\rangle=0
\qquad(a=x,y,z).
\tag{14}
\]
Orthonormality supplies the same equation for \(\sigma_0=I_2\).
The four Pauli matrices span \(M_2(\mathbb C)\), so
\[
\langle\psi_r,(B\otimes I_m)\psi_s\rangle=0
\qquad\text{for every }B\in M_2(\mathbb C).
\tag{15}
\]
In coefficient-matrix form, (15) is
\[
T_sT_r^*=0.
\tag{16}
\]
Thus the two-dimensional row spaces of \(T_r\) and \(T_s\) are orthogonal
subspaces of \(\mathbb C^m\).

When \(m\leq3\), two two-dimensional subspaces of \(\mathbb C^m\) cannot be
orthogonal.  Therefore no such pair \(r,s\) exists, and
\[
\boxed{n_r\cdot n_s=-\frac13\quad(r\neq s).}
\tag{17}
\]

## 6. The final Gram obstruction

There are \(d=2m\) Bloch vectors.  Under (17), their Gram matrix is
\[
G=\frac43I_d-\frac13J_d.
\tag{18}
\]
Its eigenvalues are
\[
\frac43\quad\text{with multiplicity }d-1,\qquad
\frac{4-d}{3}\quad\text{with multiplicity }1.
\tag{19}
\]
A Gram matrix must be positive semidefinite, so \(d\leq4\).  On the other
hand, (9) requires at least three vectors.  Since \(d=2m\) is even and
\(m\leq3\), the only remaining possibility is \(d=4\), or \(m=2\).
For \(m=3\), the last eigenvalue in (19) is \(-2/3\), proving the claimed
\(d=6\) no-go.

The \(d=4\) boundary is sharp at the level of this argument: (18) is then
the positive semidefinite rank-three Gram matrix of a regular tetrahedron.

## 7. What this does and does not prove

This theorem rigorously eliminates a broad-looking but still special
rank-one controlled construction on
\(\mathbb C^6=\mathbb C^2\otimes\mathbb C^3\).  It improves on a numerical
failure because it covers all control bases and all choices of six Bloch
vectors exactly.

It does **not** eliminate:

- higher-rank control projections;
- reflections \(A_j\) acting nontrivially on the \(\mathbb C^m\) factor;
- operator-valued face blocks;
- crossed-factor models;
- arbitrary \(36\times36\) exceptional solutions.

Thus it is a rigorous ansatz-level obstruction, not evidence that
\(4\mid d\) is forced in the full class.

## 8. Replay

The exact companion check is:

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_face_rank_one_control_no_go.py
```

It checks the symbolic Pauli product, the exceptional Schur eigenvalue,
the unitary-conjugation norm obstruction, and the exact Gram spectra at
\(d=4\) and \(d=6\).
