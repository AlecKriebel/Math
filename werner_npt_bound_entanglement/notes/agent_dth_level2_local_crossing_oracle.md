# Exact rational oracle for the local degree-three crossing

## Result

The numerical (2761\times2761) local Γ_A crossing now has an exact
matrix-free counterpart.  No dense rational crossing matrix and no
orthonormalizing square roots are required.

Let (R_\lambda(\pi)) be the exact integral polytabloid representation of
\(\pi\in S_7\) on the Specht multiplicity space of the holomorphic local
shape \(\lambda\).  If a holomorphic invariant operator has coordinate
blocks (X_\lambda), define

\[
a_\pi
=\frac1{7!}\sum_\lambda f^\lambda
\operatorname{Tr}\!\left(
R_\lambda(\pi^{-1})X_\lambda
\right).
\tag{1}
\]

Finite-group Fourier inversion gives

\[
X_\lambda=\sum_{\pi\in S_7}a_\pi R_\lambda(\pi).
\tag{2}
\]

The sum in (1) may include only the eight shapes with at most three rows;
the omitted Fourier blocks are set to zero.  This is the canonical group
algebra representative of the operator in the qutrit tensor
representation.

Let (H_\mu) be the exact rational highest-weight basis of a mixed type in

\[
\bar3^{\otimes2}\otimes3^{\otimes5},
\]

let (G_\mu=H_\mu^\dagger H_\mu), and define

\[
\Delta_\mu(\pi)
=G_\mu^{-1}H_\mu^\dagger
\Gamma_{01}(P_\pi)H_\mu.
\tag{3}
\]

Every entry in (3) is rational: Γ merely rearranges entries of the sparse
permutation diagram.  The exact crossed mixed blocks are

\[
\boxed{
Y_\mu=\sum_{\pi\in S_7}a_\pi\Delta_\mu(\pi).
}
\tag{4}
\]

Equations (1)--(4) are an exact local crossing oracle.  They also fix the
normalization used by the numerical cache.  For a raw holomorphic block
\(I_{d_\lambda}\otimes X_\lambda\), the coefficient in (1) is
\(f^\lambda/7!\); the extra (1/d_\lambda) in the discovery crossing appears
only because its columns are trace-normalized matrix units.

## Exact audits

`verification/verify_dth_level2_local_crossing_oracle.py` constructs the ten
mixed highest-weight bases over \(\mathbb Q\), evaluates (3) without forming
any dense (2187\times2187) diagram, and checks a generating collection of
eight diagrams.  In the nonorthogonal bases, the metric adjoint is

\[
Z^{\sharp}=G_\mu^{-1}Z^{\mathsf T}G_\mu.
\]

For every audited pair \(\pi,\sigma\), exact Fraction arithmetic verifies

\[
\sum_\mu d_\mu
\operatorname{Tr}\!\left(
\Delta_\mu(\pi)^\sharp\Delta_\mu(\sigma)
\right)
=3^{c(\pi^{-1}\sigma)},
\tag{5}
\]

and

\[
\sum_\mu d_\mu\operatorname{Tr}\Delta_\mu(\pi)
=3^{c(\pi)}.
\tag{6}
\]

These are respectively the Hilbert--Schmidt and trace invariance identities
for partial transpose.  They independently audit every conjugation,
nonorthogonal-Gram, and carrier normalization in (3).

## Scope

The oracle makes any rational local crossing exactly verifiable and is the
appropriate reconstruction layer for a future exact primal or dual
certificate.  It does not decide whether the complete degree-three fixed
marginal has a Γ_A-positive extension.  The current finite decision remains
a global cone problem, now being scanned with the orbit-streamed numerical
crossing.
