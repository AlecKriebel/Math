# The nonvertical nontriple companion is impossible

**Status:** exact standalone lemma; the complete nonvertical-companion
hostile audit passed in `audit_nonvertical_companion/REPORT.md`.  This is
not peer reviewed.

**Recorded:** 2026-07-25T11:36:16Z.

## Statement

Let the triple-vertical leading part and its nonvertical cubic companion
be
\[
H_4=(z^4,zq,0)^T,\qquad (H_3)_3=q,                     \tag{1}
\]
where \((z^3,q)\) is a coprime minimal cubic pencil.  Put
\[
q_0=q|_{z=0}.
\]
If \(q_0\) has either three distinct roots or one double and one simple
root, then no total-degree-four Keller map has (1).

Equivalently, a Keller map on the nonvertical companion must lie on the
triple-root divisor
\[
\boxed{q_0=L^3.}                                       \tag{2}
\]

## Proof

Write
\[
H_3=(U,V,q)^T,\qquad H_2=(A,B,W)^T.
\]
The exact \(E_7\) solve, modulo legal additions of the third target
component to the first two, is
\[
U=dz^3,\qquad V=zW+fz^3.                               \tag{3}
\]

For a binary cubic \(q_0\) that is not a cube, the restrictions of
\(E_6,E_5,E_4\) to \(z=0\) successively give
\[
A_0=0,\qquad \bar L_1=0,\qquad
A=\alpha z^2\ \text{or}\ B_0=0.                        \tag{4}
\]
Here \(A_0=A|_{z=0}\), \(B_0=B|_{z=0}\), and \(\bar L_i\) is the
\((x,y)\)-part of the \(i\)-th row of the linear matrix.  These statements
come from
\[
\begin{aligned}
E_6|_{z=0}&=-q_0\{A_0,q_0\},\\
E_5|_{z=0}&=-q_0\{\bar L_1,q_0\},\\
E_4|_{z=0}&=A_1\{B_0,q_0\},
\end{aligned}                                          \tag{5}
\]
where \(A=zA_1+\alpha z^2\).  The binary kernel
\(\{K_0,q_0\}=0\) in degrees two and one is zero when \(q_0\) is not a
cube.

It remains to solve both branches in (4) without losing rank loci.

### Branch 1: \(A=\alpha z^2\)

Keep every lower coefficient of \(q\), every coefficient of \(W\), and
the scalars \(d,f,\alpha\) symbolic.  The full \(E_6,E_5\) coefficient
matrix in the coefficients of \(B,L\) has the literal pivot minor
\[
\boxed{-524288=-2^{19}.}                               \tag{6}
\]
It forces
\[
B_0=0,\qquad
B=z(\ell_{31}x+\ell_{32}y+\beta z),\qquad
\bar L_2=0,                                             \tag{7}
\]
with \((\ell_{31},\ell_{32})=\bar L_3\).

### Branch 2: \(B_0=0\)

Initially allow
\[
A=z(a_1x+a_2y+\alpha z).
\]
The full \(E_6,E_5\) matrix now has the literal pivot minor
\[
\boxed{-2048=-2^{11}.}                                 \tag{8}
\]
It forces \(a_1=a_2=0\), and then gives exactly (7).

The same two constant minors work for both normal forms
\[
q_0=xy(x-y),\qquad q_0=x^2y.                            \tag{9}
\]
They contain no lower coefficient of \(q\) and no coefficient of \(W\);
there is therefore no hidden internal rank divisor.

In both branches, (4) and (7) make the first and second rows of \(L\)
multiples of \(dz\).  Hence \(\det L=0\), contradicting the invertibility
of the linear part.  This proves the lemma.

## Verification and disclosure

`verify_nonvertical_nontriple_e4_sympy.py` reconstructs both complete
coefficient systems, checks the literal minors (6), (8), solves their
pivot equations over the full symbolic parameter rings, checks every
residual equation, and verifies \(\det L=0\).

`test_nonvertical_nontriple_mutations.sh` changes each \(E_4\) branch
outside its certified hypothesis and requires the exact verifier to fail.
The strict runner also rejects a missing success sentinel.

These exact checks are evidence about the encoded algebra, not peer
review.  AI systems materially assisted the derivation, computation, and
exposition.
