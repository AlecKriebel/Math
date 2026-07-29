# Independent hostile audit: the codimension-two cut-down obstruction

**Date:** 2026-07-29

**Audited files:**

- `notes/no_rank_six_subspace_of_d8_amplification.md`
- `verifiers/verify_no_rank_six_subspace_of_d8.py`

**Verdict:** **INDEPENDENTLY REPRODUCED.**  The theorem is valid for every
identity amplification \(H^{(4)}\boxtimes I_m\), \(m\ge2\), at its stated
scope.  I found no tensor-order, real/complex-span, rank-bound, or
generated-algebra gap.  It excludes codimension-two square restrictions
of these specific amplifications; it does not exclude genuinely new
solutions in dimensions \(4m-2\).

## Independent derivation

I reconstructed the published five-word \(H^{(4)}\), grouped its first
site by the Hermitian Pauli basis on the active \(a\)-qubit, and obtained
exactly
\[
H^{(4m)}=\sum_{\nu=X,Y,Z}A_\nu\otimes B_\nu
\]
in the local order
\((a_1,b_1,c_1\,|\,a_2,b_2,c_2)\), where \(\dim c_i=m\), with the three
\(B_\nu\)'s displayed in the audited note.  Thus the spectator and
operator-Schmidt tensor orders are correct.

Let \(Q\) have rank \(4m-2\) and \(E=I-Q\).  Commutation with
\(Q\otimes Q\) gives
\[
\sum_\nu (EA_\nu Q)\otimes(QB_\nu Q)=0. \tag{A}
\]
If the real span of the Hermitian compressions \(QB_\nu Q\) had dimension
at most one, its coefficient map would have a real kernel of dimension at
least two.  For a real coefficient vector in this kernel, the corresponding
Hermitian \(B\) has block form
\[
\begin{pmatrix}0&C\\ C^*&D\end{pmatrix}
\quad\text{on }QV_m\oplus EV_m.
\]
The columns from \(QV_m\) have image in the two-dimensional space \(EV_m\),
and the columns from \(EV_m\) have rank at most two.  Hence
\(\operatorname{rank}B\le4\).  Since \(B=\widetilde B\otimes I_c\), this
forces
\[
m\operatorname{rank}\widetilde B\le4. \tag{B}
\]

In the Bell basis, the two blocks of \(\widetilde B(x,y,z)\) have
determinants
\[
\frac{z^2-2x^2}{3},\qquad \frac{z^2-2y^2}{3}.
\]
If \(z=0\), rank at most two occurs only on the \(x\)- or \(y\)-axis.  If
\(z\ne0\), neither block is zero, so both must have rank one; this gives
\[
x=\pm z/\sqrt2,\qquad y=\pm z/\sqrt2.
\]
Thus the real rank-at-most-two cone is exactly the union of the six stated
lines and contains no real plane.  Also, every nonzero pencil element has
rank at least two: if one Bell block vanishes, the other nonzero block has
rank two, while if neither vanishes their ranks add to at least two.
For \(m=2\), (B) would put a kernel plane in the six-line cone.  For
\(m\ge3\), (B) would make every member of the kernel plane have rank at
most one, hence zero.  Both are contradictions.  The compression span
therefore has real dimension at least two for every \(m\ge2\).

Choose a real basis for that span.  Hermitian matrices independent over
\(\mathbb R\) are also independent over \(\mathbb C\), so coefficient
comparison in (A) is legitimate despite the generally complex matrices
\(EA_\nu Q\).  It yields two independent **real** Pauli directions
\(u,v\) with
\[
EA(u)Q=EA(v)Q=0.
\]
Adjoints kill the opposite off-diagonal corners.  Hence \(Q\) commutes
with \(A(u)\) and \(A(v)\).  Two independent real Pauli directions have
nonzero cross product and generate \(M_2(\mathbb C)_a\), so
\[
Q=I_a\otimes Q_{bc}. \tag{C}
\]
This explicitly resolves the only plausible real-versus-complex span
concern.

Substituting (C) into the full commutator gives
\[
\sum_\nu A_\nu Q\otimes[B_\nu,Q]=0.
\]
Now \(A_\nu Q=A_\nu\otimes Q_{bc}\) are linearly independent because
\(Q_{bc}\ne0\), so \(Q\) commutes with every \(B_\nu\).
The \(A_\nu\)'s give \(M_2\) on \(a\);
\(A_XB_X\) gives \(I_a\otimes X_b\); and
\(A_X[A_Z,B_Z]\) gives a nonzero scalar multiple of
\(I_a\otimes Y_b\).  Their product gives \(I_a\otimes Z_b\).
Consequently the generated active algebra is \(M_4(\mathbb C)_{ab}\),
whose commutant on \(V_m\) is \(I_{ab}\otimes M_m(\mathbb C)_c\).
Projection ranks in this commutant are divisible by four, contradicting
rank \(4m-2\).

## Verifier audit

The primary verifier completed successfully.  I also wrote
`verifiers/verify_no_rank_six_subspace_of_d8_independent.py`, which uses
two deliberately different checks:

1. it extracts the three second-site Schmidt coefficients from the
   published \(16\times16\) matrix by exact partial contraction rather
   than reconstructing the amplified matrix from hard-coded coefficients;
2. it solves the generic \(4\times4\) commutant equations and obtains
   linear rank \(15\), hence a one-dimensional active commutant, rather
   than closing the generated algebra by word multiplication.

Both routes reproduce the claimed tensor ordering, Bell blocks, minimum
nonzero pencil rank, and full active algebra.  The all-\(m\) step is then
the exact integer rank inequality (B).

## Minor exposition corrections applied

The audit initially flagged two presentation issues: the independence of
\(A_\nu Q\) should be attributed to (C), not merely to \(Q\ne0\), and
equation (7) needed \(H^{(4m)}\) rather than \(H^{(8)}\).  Both corrections
have now been made in the primary note.
