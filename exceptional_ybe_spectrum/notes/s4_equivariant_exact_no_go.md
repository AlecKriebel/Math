# Exact exclusion of the \(S_4\)-equivariant heterogeneous \(d=6\) branch

**Date:** 2026-07-29 PDT

**Status:** `PROVED` (exact finite computation plus a human-readable real
case split)

**Scope:** the heterogeneous spectator ansatz with
\[
 A=V_2,\qquad B=V_3,
\]
where \(V_2\) is the two-dimensional irreducible representation of
\(S_4\), \(V_3\) is its standard three-dimensional representation, and
the active operator on \(A\otimes B\otimes A\) commutes with the diagonal
\(S_4\)-action.

This note does **not** exclude arbitrary \(d=6\) exceptional Yang--Baxter
matrices, arbitrary heterogeneous operators, or operators with a
different symmetry.

## 1. Result

Let
\[
 H\in\operatorname{End}(A\otimes B\otimes A)
\]
be a Hermitian involution of trace zero which commutes with the diagonal
\(S_4\)-action.  On
\[
 A\otimes B\otimes A\otimes B\otimes A
\]
put
\[
 H_1=H\otimes I_{B\otimes A},
 \qquad
 H_2=I_{A\otimes B}\otimes H.
\]

> **Theorem.**  There is no such \(H\) satisfying
> \[
> H_1H_2H_1-H_2H_1H_2=\frac13(H_1-H_2).
> \]

The two central rank-six equivariant choices were already rejected
exactly in `scripts/verify_track_additive_s4_central.py`.  The proof below
closes the remaining noncentral \(S^2\times S^2\) branch.  Consequently,
there is no rank-six \(S_4\)-equivariant solution in this heterogeneous
\((2,3,2)\) ansatz.

## 2. Exact multiplicity-space Pauli basis

Use the rational sum-zero bases
\[
 a_1=e_1-e_3,\quad a_2=e_2-e_3
\]
for the permutation action on the three perfect matchings, and
\[
 b_1=e_1-e_4,\quad b_2=e_2-e_4,\quad b_3=e_3-e_4
\]
for the standard representation.  Their Gram matrices are
\[
 G_A=
 \begin{pmatrix}2&1\\1&2\end{pmatrix},
 \qquad
 G_B=
 \begin{pmatrix}2&1&1\\1&2&1\\1&1&2\end{pmatrix}.
\]
Thus the product-basis metric on \(A\otimes B\otimes A\) is
\[
 G=G_A\otimes G_B\otimes G_A.
\]
Write \(X^\sharp=G^{-1}X^*G\) for the metric adjoint.

Character decomposition gives
\[
 A\otimes B\otimes A\cong 2V_3\oplus2V_{3'},
\]
and hence
\[
 \operatorname{End}_{S_4}(A\otimes B\otimes A)
 \cong M_2(\mathbb C)\oplus M_2(\mathbb C).
\]
The following construction fixes an exact Pauli basis in both summands.

Let \(\rho\) be the product representation, let
\(\chi_3(g)=\#\operatorname{Fix}(g)-1\), and put
\[
 P_s=\frac18\sum_{g\in S_4}\chi_3(g)\rho(g),
 \qquad
 P_t=\frac18\sum_{g\in S_4}\operatorname{sgn}(g)\chi_3(g)\rho(g).
\]
On \(A\otimes A\), define
\[
 \pi_1=\frac1{24}\sum_{g\in S_4}\rho_A(g)\otimes\rho_A(g),
\qquad
 \pi_\epsilon=\frac1{24}\sum_{g\in S_4}
 \operatorname{sgn}(g)\rho_A(g)\otimes\rho_A(g).
\]
After inserting the unchanged \(B\)-factor, call the resulting rank-three
projections \(Q_s\) and \(Q_t\).  They satisfy
\[
 Q_s\le P_s,\qquad Q_t\le P_t.
\]

Let \(E_{01}\) be the \(12\times12\) elementary matrix in the rational
product basis and average it into the commutant:
\[
 C=\frac1{24}\sum_{g\in S_4}\rho(g)E_{01}\rho(g)^{-1}.
\]
Set
\[
 T_s=36(P_s-Q_s)CQ_s,\qquad
 T_t=12(P_t-Q_t)CQ_t.
\]
Exact rational multiplication gives
\[
 T_s^\sharp T_s=Q_s,\quad
 T_sT_s^\sharp=P_s-Q_s,
\]
and the analogous identities for \(t\).  Therefore
\[
\begin{aligned}
 X_s&=T_s+T_s^\sharp,&
 Y_s&=-i(T_s-T_s^\sharp),&
 Z_s&=P_s-2Q_s,\\
 X_t&=T_t+T_t^\sharp,&
 Y_t&=-i(T_t-T_t^\sharp),&
 Z_t&=P_t-2Q_t
\end{aligned}
\]
are exact metric-Hermitian Pauli triples.  In each central summand they
square to its identity and obey the usual Pauli multiplication rules.

A noncentral trace-zero equivariant Hermitian involution is consequently
exactly
\[
 H=xX_s+yY_s+zZ_s+uX_t+vY_t+wZ_t,
 \tag{2.1}
\]
where
\[
 x^2+y^2+z^2=1,\qquad u^2+v^2+w^2=1.
 \tag{2.2}
\]
This proves that the parametrization covers the entire
\(S^2\times S^2\) branch; it is not an ansatz within that branch.

## 3. Sparse exact cubic certificate

Let
\[
 D=H_1H_2H_1-H_2H_1H_2-\frac13(H_1-H_2).
\]
Rows and columns below use the lexicographic product basis of
\(A,B,A,B,A\), indexed from zero.  Multiplying the Pauli matrices by
\(12\) makes them Gaussian-integer matrices.  Hence \(1728D\) has
Gaussian-integer polynomial coefficients.

Twenty particularly sparse normalized real or imaginary coordinates of
\(1728D\) are:
\[
\begin{array}{c|c|l}
j&(r,c;\text{part})&f_j\\ \hline
0&(6,51;i)&vx(z-w)\\
1&(6,65;i)&uy(z-w)\\
2&(2,55;i)&-uvw-uvz+2xyz\\
3&(2,45;i)&2uvz-3wxy+xyz\\
4&(20,51;i)&-4uwy+vwx+3vxz\\
5&(34,65;i)&-uwy-3uyz+4vxz\\
6&(0,51;r)&-uv^2+uwz-uz^2+vxy\\
7&(0,57;i)&(z-w)(-uy+vx)\\
8&(2,0;i)&-uvz-uwy+vxz+xyz\\
9&(12,0;i)&-uvz+uwy-vxz+xyz\\
10&(14,0;r)&(z-w)(ux-vy)\\
11&(14,0;i)&-uxy+vwz+vx^2-vz^2\\
12&(20,37;i)&(z-w)(uy+vx)\\
13&(0,0;r)&3uwx+5uxz+5vwy+3vyz\\
14&(0,0;i)&5uxy-5vwz+3vx^2-3vz^2\\
15&(0,43;i)&-11uwy+3uyz+3vwx+5vxz\\
16&(6,37;i)&-13uwy-3uyz+3vwx+13vxz\\
17&(14,51;r)&3uv^2+13uwz+3uz^2+13vxy\\
18&(2,55;r)&-u^2x-2uvy+v^2x+x^3+xy^2\\
19&(3,1;i)&uvz-2uwy+2vxz-3wxy+2xyz
\end{array}
\tag{3.1}
\]
Each table entry differs from the indicated coordinate only by a
nonzero integer factor.  Thus \(D=0\) implies \(f_j=0\) for all \(j\).

Exact Buchberger reduction of (3.1) together with the two equations
(2.2) gives the following seven consequences:
\[
\begin{aligned}
u(v^2+w^2)&=0,& u(z-w)&=0,& xy-uv&=0,\\
w(w^2-1)&=0,& v(z-w)&=0,&
v(uy-vx)&=0,\\
x(z^2-w^2)&=0.&&&&
\end{aligned}
\tag{3.2}
\]
The verifier reconstructs the matrices from the group action, extracts
the coordinates independently using exact Gaussian-integer arithmetic,
and checks that every polynomial in (3.2) reduces to zero modulo the
ideal generated by (2.2) and (3.1).

Three further normalized coordinates will eliminate the branches:
\[
\begin{aligned}
k_1={}&9uvw-3uvz+24v^2y-24w^2y+9wxy+24x^2y
       -15xyz-8y,\\
k_2={}&6u^3-2uvy+2uwz+2u-3v^2x+2vxy-3w^2x
       +xy^2-xz^2,\\
k_3={}&9u^2w+9u^2z-9v^2w+39v^2z-9w^3-21w^2z
       +27wx^2+9wy^2\\
     &\hspace{3em}-27wz^2+3x^2z+9y^2z+9z^3-16z.
\end{aligned}
\tag{3.3}
\]
They are respectively the imaginary \((17,17)\), real \((8,6)\), and
real \((1,1)\) coordinates, again after nonzero integer normalization.

## 4. Human-readable real case split

All six parameters are real because (2.1) is Hermitian.

### Case A: \(u\ne0\)

The first equation of (3.2) gives \(v=w=0\), and \(u(z-w)=0\) gives
\(z=0\).  The sphere equations give
\[
 u^2=1,\qquad x^2+y^2=1,
\]
while \(xy=uv\) gives \(xy=0\).  On this branch,
\[
 k_2=8u\ne0.
\]
So Case A is impossible.

### Case B: \(u=0,w=0\)

The second sphere gives \(v^2=1\).  From \(v(z-w)=0\) and
\(v(uy-vx)=0\), one obtains \(z=x=0\).  The first sphere then gives
\(y^2=1\).  But
\[
 k_1=16y\ne0.
\]
So Case B is impossible.

### Case C: \(u=0,w\ne0\)

The equation \(w(w^2-1)=0\) gives \(w^2=1\), and the second sphere then
gives \(v=0\).  Hence \(xy=0\).  If \(x\ne0\), the last equation of
(3.2) gives \(z^2=1\), contradicting
\(x^2+y^2+z^2=1\).  Therefore
\[
 x=0,\qquad y^2+z^2=1.
\]
Now \(k_1=-32y\), so \(y=0\) and \(z^2=1\).  Finally
\[
 k_3=-36w-28z.
\]
For \(w,z\in\{-1,1\}\), this is one of
\(\{-64,-8,8,64\}\), never zero.  So Case C is impossible.

The cases exhaust the real product of spheres.  This proves the theorem.
As a separate exact check, the verifier confirms that the ideal generated
by the two sphere equations and the 23 selected residual coordinates is
the unit ideal over \(\mathbb Q\); thus those selected equations actually
have no common complex solution either.

## 5. Verification and precise conclusion

Run:

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_s4_equivariant_noncentral_no_go.py
```

The verifier checks:

1. the rational \(S_4\) representations and Gram metrics;
2. the two central projectors and exact Pauli triples;
3. metric Hermiticity, Pauli multiplication, and zero traces;
4. all 23 selected coordinates using bounded Gaussian-integer arithmetic;
5. the seven ideal-membership reductions (3.2);
6. the full unit-ideal certificate;
7. the three real branch evaluations used in Section 4.

The result is a complete no-go only for the stated
\(S_4\)-equivariant heterogeneous branch.  It supplies no obstruction to
a genuinely non-\(S_4\)-equivariant \(d=6\) witness.
