# Full-excursion form of the root Green repayment target

Date: 2026-08-13 (America/Los_Angeles)

No external communication or graph search was used.

## Status

This note rewrites the root-Hellinger Green bound in honest alternating
excursion coordinates.  The rewrite proves two things.

1. The apparent singleton normalizers cancel completely.  The remaining
   sufficient inequality compares a doubleton-fed base-graph Green potential
   directly with the two signed full-excursion rewards.
2. No proof using only the normalized root laws and normalized doubleton
   atoms can establish that inequality.  The exact rank-three pseudo-law
   scaling leaves all such data fixed while making the normalized excursion
   target arbitrarily large.  A rank-three return equation or an equivalent
   full killed Green/tree functional is logically indispensable.

The final full-excursion inequality remains open.  This is a reduction and a
proof-route obstruction, not a proof of the minimal stationary product.

## 1. Honest alternating excursions

Fix one of the exact recurrent duals `U in {Bd,dB}` on a module of order
`s>=3`, and split its state space into

\[
 \mathcal L=\{A:1\le |A|\le2\},\qquad
 \mathcal H=\{A:|A|\ge3\}.
\]

Let `nu_U^-` be the stationary entrance law on the low boundary and
`G_U^-=(-Q_U^{--})^{-1}` its killed Green kernel.  Put

\[
 h_U=\nu_U^-G_U^- .                                    \tag{1}
\]

Thus `h_U(A)` is the expected occupation time of the low state `A` during
one low excursion.  Write

\[
 H_U=\sum_i h_U(\{i\}),\qquad
 X_U={M_U\over s}-pT_U,\qquad p=1-{1\over r},          \tag{2}
\]

where `T_U` and `M_U` are the full low-plus-high cycle time and rank reward.
If `J_U` is the stationary crossing current, the renewal identities give

\[
 \pi_U=J_U\,h_U\quad\hbox{on }\mathcal L,qquad
 c_U=J_UH_U,qquad
 \rho_U-p=J_UX_U.                                     \tag{3}
\]

Consequently

\[
 \boxed{
 \lambda_{U,i}={h_U(\{i\})\over H_U},\qquad
 \eta^U_{ij}={h_U(\{i,j\})\over H_U},\qquad
 \overline\phi_U={X_U\over H_U}.}                    \tag{4}
\]

All singleton normalizers have now been represented by honest occupation
times of one alternating excursion.

## 2. Rescaled doubleton rebate

For a base edge `ij`, define the cycle-level rebate

\[
 \widehat\Delta_{ij}=
 \sqrt{\{h_B(\{j\})+h_B(\{i,j\})\}
       \{h_D(\{j\})+h_D(\{i,j\})\}}
 -\sqrt{h_B(\{j\})h_D(\{j\})}.                       \tag{5}
\]

By (4), the normalized rebate in the singleton balance proof is

\[
 \Delta_{ij}={\widehat\Delta_{ij}\over\sqrt{H_BH_D}}. \tag{6}
\]

Retain the exact base-graph kernel

\[
 L_{ij}={P_{ij}\over
 \sqrt{rt_i}\sqrt{r-(r-1)P_{ji}}},                   \tag{7}
\]

and put

\[
 \widehat\beta_i={\sqrt{e_i}\over\sqrt{rt_i}}
 \sum_j\sqrt{P_{ij}g_r(P_{ji})}\,
             \widehat\Delta_{ij},                    \tag{8}
\]

where `e_i=1/d_i` and `g_r(z)=z/[r-(r-1)z]`.  Equations
(6)--(8) give

\[
 \beta={\widehat\beta\over\sqrt{H_BH_D}}.           \tag{9}
\]

Since `rho(L)<1`, define the full-excursion Green potential

\[
 \boxed{y=(I-L)^{-1}\widehat\beta.}                  \tag{10}
\]

The coordinatewise root-path theorem is equivalently

\[
 \sqrt{e_i h_B(\{i\})h_D(\{i\})}\ge y_i.            \tag{11}
\]

## 3. Exact sufficient target after cancellation

For a physical portal load `x>=0`, the root-Hellinger repayment condition is

\[
 (x\cdot a)^2\ge
 r^3[\overline\phi_B]_+[\overline\phi_D]_+
 (x\cdot\mathbf1)(x\cdot e).                         \tag{12}
\]

Substitute (4), (9), and the coordinatewise lower bound (10)--(11).  The
positive factor `H_BH_D` cancels from both sides.  Therefore the following
is a sufficient full-excursion theorem for `(RHR)`, hence for `(SRR)` and
the minimal stationary product:

\[
 \boxed{
 (x\cdot y)^2\ge r^3[X_B]_+[X_D]_+
 (x\cdot\mathbf1)(x\cdot e)
 \quad\hbox{for every }x\ge0.}                        \tag{FER}
\]

This is the same sharp pairwise copositivity problem as before, but with no
singleton mass or cycle current left.  Set

\[
 Q_X=r^3[X_B]_+[X_D]_+ .                              \tag{13}
\]

Then `(FER)` is equivalent to

\[
 y_i^2\ge Q_Xe_i                                      \tag{14}
\]

for every `i`, and, for every `i != j`,

\[
 y_iy_j-{Q_X\over2}(e_i+e_j)
 +\sqrt{(y_i^2-Q_Xe_i)(y_j^2-Q_Xe_j)}\ge0.           \tag{15}
\]

Thus the remaining universal gap is exact: the doubleton-fed Green
potential `y` must repay the product of the two signed full-cycle rewards
`X_B,X_D`.

## 4. Why the higher-rank return equation is indispensable

The rank-three pseudo-law gives a rigorous logical obstruction to any proof
of `(FER)` that uses only

\[
 (\lambda_B,\lambda_D,\eta^B,\eta^D)
\]

and the singleton balance equations.  Start from any positive rank-one and
rank-two arrays satisfying those balances.  For `epsilon in (0,1)`, multiply
every rank-one and rank-two atom in both putative laws by `epsilon` and put
the residual probability on a rank-three state.

The singleton equations are homogeneous, so they remain true.  Moreover

\[
 \lambda_U={\pi_{U,1}\over c_U},\qquad
 \eta^U={\pi_{U,2}\over c_U}                          \tag{16}
\]

are unchanged, because both numerator and denominator scale by `epsilon`.
Hence `L`, `Delta`, `beta`, and the normalized Green lower bound
`(I-L)^{-1}beta` are all unchanged.

For order `s=8`, however, both mean densities tend to `3/8`.  Throughout the
isolating interval containing `R_hyb`, `3/8-p>0`.  Since
`c_U=O(epsilon)`,

\[
 \overline\phi_U={\rho_U-p\over c_U}=\Theta(\epsilon^{-1}),
 \qquad
 Q_0=r^3\overline\phi_B\overline\phi_D
      =\Theta(\epsilon^{-2}).                          \tag{17}
\]

Thus `(RHR)` cannot follow from the normalized low data and singleton
balances alone.  This does not refute `(RHR)` for genuine stationary duals:
the scaled pseudo-law violates the doubleton/rank-three stationarity
equation.  It proves that any successful comparison of `y` with `X_BX_D`
must use that missing return equation, or an equivalent full killed Green
or marked-tree identity.

## 5. A boundary trace of the full reward

There is one exact way to expose that missing information without returning
to all singleton roots.  For either rule, take `E` to be the entire
doubleton sector and `R` its complement in the recurrent state space.  The
irreducible finite chain hits `E` almost surely, so the killed `R` block is
transient.  Let

\[
 G_E=(-Q_{RR})^{-1},\qquad
 \Psi_U=g_E+Q_{ER}G_Eg_R,qquad
 g(A)={|A|\over s}-p.                                 \tag{18}
\]

Stationarity gives

\[
 \pi_R=\pi_EQ_{ER}G_E,
\]

and therefore, after division by `c_U`,

\[
 \boxed{
 \overline\phi_U=\sum_{D\in E}\eta^U_D\Psi_U(D).}   \tag{19}
\]

In particular,

\[
 [\overline\phi_U]_+
 \le\sum_{D\in E}\eta^U_D[\Psi_U(D)]_+.            \tag{20}
\]

Formula (19) is the exact bridge sought by a doubleton proof: it pairs the
same normalized doubleton atoms appearing in the rebate with a full
killed-excursion coefficient.  It also shows why rank drift alone does not
finish the argument.  The coefficient `Psi_U(D)` contains the entire killed
Green lifetime in `R`; it cannot in general be replaced by a constant
depending only on `r` or by the immediate doubleton drift.

The remaining proof-first target is therefore not a marginal estimate.  It
is a paired comparison showing that the two full coefficients `Psi_B,Psi_D`
are jointly repaid by the nonlinear edge rebates (5) propagated through
`(I-L)^{-1}`.
