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
to all singleton roots.  For either rule, take

\[
 E=\{\{i,j\}:w_{ij}>0\}                               \tag{18}
\]

to be precisely the base-edge doubletons and take `R` to be their complement
in the recurrent state space.  This is exactly the collection used in the
rebate (5); nonedge doubletons remain inside the killed excursion.  Since the
finite recurrent dual is irreducible and `E` is nonempty, it hits `E` almost
surely, so the killed `R` block is transient.  Let

\[
 G_E=(-Q_{RR})^{-1},\qquad
 \Psi_U=g_E+Q_{ER}G_Eg_R,qquad
 g(A)={|A|\over s}-p.                                 \tag{19}
\]

Stationarity gives

\[
 \pi_R=\pi_EQ_{ER}G_E,
\]

and therefore, after division by `c_U`,

\[
 \boxed{
 \overline\phi_U=\sum_{D\in E}\eta^U_D\Psi_U(D).}   \tag{20}
\]

In particular,

\[
 [\overline\phi_U]_+
 \le\sum_{D\in E}\eta^U_D[\Psi_U(D)]_+.            \tag{21}
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

## 6. Exact star obstruction to a separate reward bound

The killed coefficient in (20) cannot be replaced, rule by rule, by a
constant or even by a polynomial in the module order.  This already fails
for the Bd dual on the unit star with centre `0` and `L` leaves.

Let `H_B(q)` and `E_B(q)` be the Bd fixation probabilities at relative
fitness `q` from the centre and one leaf.  Put

\[
 \theta_q={L+q\over q(qL+1)},\qquad
 D_q={q\over L}+{1-\theta_q^L\over1-\theta_q}.        \tag{22}
\]

The exact star solution is

\[
 H_B(q)={q\over LD_q},\qquad
 E_B(q)={q^2\theta_q\over D_q}.                       \tag{23}
\]

By reciprocal-fitness duality, the Bd singleton atoms at fitness `r` are

\[
 u_0=H_B(1/r),\qquad u_\ell=E_B(1/r).                 \tag{24}
\]

If `b_{0ell}` is the centre-leaf doubleton atom, exact singleton balance at
a leaf gives

\[
 b_{0\ell}={r\over L}u_\ell-u_0.                     \tag{25}
\]

Writing `c=u_0+Lu_ell`, direct simplification yields

\[
 \boxed{
 \sum_{D\in E}\eta_D={Lb_{0\ell}\over c}
 ={L^2(r^2-1)\over
   (L+1)(rL^2-rL+L+r)}.}                              \tag{26}
\]

On the other hand,

\[
 \rho_{Bd}={H_B(r)+LE_B(r)\over L+1},\qquad
 \overline\phi_{Bd}={\rho_{Bd}-p\over c}.            \tag{27}
\]

For fixed `r>1`, the exact formulas give

\[
 \rho_{Bd}-p\longrightarrow {r-1\over r^2},\qquad
 c\sim L(r^2-1)e^{r-1/r}r^{-2L},                     \tag{28}
\]

while (26) is asymptotic to `(r^2-1)/(rL)`.  Therefore

\[
 \boxed{
 {\overline\phi_{Bd}\over\sum_{D\in E}\eta_D}
 \sim {r^{2L-1}\over
 (r-1)(r+1)^2e^{r-1/r}}\longrightarrow\infty.}       \tag{29}
\]

This rules out every separate per-rule estimate

\[
 [\overline\phi_{Bd}]_+
 \le C_r(s)\sum_{D\in E}\eta_D
\]

with `C_r(s)` constant or polynomial in `s=L+1`.  It does not refute a
genuinely paired bound: on large stars the dB excess is nonpositive, so the
positive-part product vanishes.  What (29) proves is that `Psi_B` cannot be
localized before the two rules are coupled.  A successful proof must retain
both full killed Green coefficients and exploit their cross-rule
compensation.

## 7. Exact paired-coefficient bottleneck

The boundary trace determines exactly what a paired coefficient proof would
have to control.  Put

\[
 A_D=h_B(D)[\Psi_B(D)]_+,qquad
 B_D=h_D(D)[\Psi_D(D)]_+ .                            \tag{30}
\]

Equations (20)--(21), in cycle coordinates, give

\[
 [X_B]_+\le\sum_DA_D,qquad [X_D]_+\le\sum_DB_D.      \tag{31}
\]

The boundary analogue of the root Cauchy split is the exact identity

\[
 \boxed{
 (\sum_DA_D)(\sum_DB_D)
 =\left(\sum_D\sqrt{A_DB_D}\right)^2
 +{1\over2}\sum_{D,F}
  (\sqrt{A_DB_F}-\sqrt{A_FB_D})^2.}                  \tag{32}
\]

Therefore a bound on the same-edge products
`[Psi_B(D)]_+[Psi_D(D)]_+` controls only the first term in (32).  The second
term is a nonnegative **reward-orientation square on the target side**.  It
cannot be discarded when proving `(FER)`.

This can be stated as an explicit cross-edge sufficient target.  Decompose
the nonnegative source in (8) by undirected base edges,

\[
 \widehat\beta=\sum_{D\in E}\widehat\beta^{,D},qquad
 y^D=(I-L)^{-1}\widehat\beta^{,D},qquad
 y=\sum_Dy^D.                                        \tag{33}
\]

For a fixed portal load, abbreviate

\[
 Y_D=x\cdot y^D,qquad
 W_x=(x\cdot\mathbf1)(x\cdot e).                    \tag{34}
\]

Then (31) and expansion of `(x.y)^2` show that `(FER)` would follow from
the coefficientwise paired inequalities

\[
 Y_D^2\ge r^3A_DB_DW_x                              \tag{35}
\]

and, for `D != F`,

\[
 \boxed{
 2Y_DY_F\ge r^3(A_DB_F+A_FB_D)W_x.}                  \tag{36}
\]

Condition (36) keeps both swapped edge assignments and is exactly the
arithmetic comparison demanded by the reward product.

The proved swapped cut-odds lemma does not supply (36).  It bounds the
*product* of the two assignments and therefore their geometric mean.  But

\[
 A_DB_F+A_FB_D
 =2\sqrt{A_DB_FA_FB_D}
  +(\sqrt{A_DB_F}-\sqrt{A_FB_D})^2,                  \tag{37}
\]

so the geometric-mean bound goes in the insufficient direction.  The last
square in (37) is exactly the corresponding term in (32).  Unsymmetrized
local cut-odds control is unavailable: it is already false on the
unweighted three-path.

Thus the killed coefficients do admit an exact paired formulation,
(35)--(36), but neither a same-edge product bound nor the sharp swapped
local odds envelope can prove it.  The remaining mechanism would have to
transport the reward-orientation square across different boundary edges.
In operator language this is a global multiplicity-labelled excursion or
paired-tree matching.  The canonical step-synchronous labelled matching is
already refuted by the non-telescoping repeated-source factor in the paired
root-tree note.

At this point no further scalar rank-drift, marginal Green, or same-edge
coefficient reduction remains.  Proving `(FER)` by this route is precisely
the unresolved global cross-edge path/tree transport problem.  Retaining
the original root-orientation square and attacking `(SRR)` directly may be
strictly more economical.
