# Normalizer-free two-root renewal criterion for universal MP

Date: 2026-08-13 (America/Los_Angeles)

No external communication, graph enumeration, or kernel search was used.

## Status

**EXACT REDUCTION AND PROOF-ROUTE OBSTRUCTION.**  This note does not prove
the universal minimal stationary product `(MP)`.  It applies the already
proved orientation-preserving portal minimax to the singleton Schur/renewal
variables and obtains a normalizer-free full-excursion criterion.  The
criterion has three equivalent forms:

1. an all-portal product of the two root-occupation fields;
2. one diagonal and one copositive inequality for each pair of roots; and
3. a two-scalar interval/minimax inequality with quantifiers
   `for every z, there exists t`.

The note then proves that no fixed rank prefix of the two stationary dual
equations can establish even the diagonal part of this criterion.  This is
a theorem for every fixed prefix depth and for both duals simultaneously,
not a first- or second-level example.  A proof must use an unbounded/full
return identity, or another invariant which encodes that information.

Finally, the exact pair margin is split into its Hellinger core and its
swapped-root orientation square.  A rational positive-data example proves
that ordinary rootwise Cauchy, which drops this square, can fail while the
exact pair test holds strictly.  Thus a surviving two-source argument must
retain orientation.  The full-chain sign of that orientation-preserving
criterion remains open.

## 1. Singleton Schur variables

Fix a connected loopless weighted module, fitness `1<r<2`, and one of the
two recurrent duals `U in {Bd,dB}`.  Partition its state space into the
singleton roots `S` and their complement `R`, and write

\[
 Q_U=\begin{pmatrix}Q^U_{SS}&Q^U_{SR}\\
                     Q^U_{RS}&Q^U_{RR}\end{pmatrix},
 \qquad \pi_U=(u_U,w_U).                              \tag{1}
\]

The killed complement is transient, so

\[
 G_U=(-Q^U_{RR})^{-1}\ge0.                            \tag{2}
\]

For the density-excess reward

\[
 g(A)=\frac{|A|}{s}-p,\qquad p=1-\frac1r,             \tag{3}
\]

define the singleton trace reward

\[
 \phi_U=g_S+Q^U_{SR}G_Ug_R.                           \tag{4}
\]

If

\[
 c_U=u_U\mathbf1,qquad
 \lambda_U=\frac{u_U}{c_U},qquad
 \overline\phi_U=\lambda_U\phi_U,                   \tag{5}
\]

then block stationarity gives exactly

\[
 \rho_U-p=c_U\overline\phi_U.                        \tag{6}
\]

Let `e_i=1/d_i` be inverse weighted degree.  For a nonzero physical portal
load `x>=0`, the Bd and dB portal laws are

\[
 \gamma_i=\frac{x_i}{x\mathbin\cdot\mathbf1},
 \qquad
 \alpha_i=\frac{e_ix_i}{x\mathbin\cdot e}.           \tag{7}
\]

After cancellation of the positive singleton masses, `(MP)` is exactly

\[
 (x\mathbin\cdot\lambda_B)
 (x\mathbin\cdot(e\lambda_D))
 \ge Q_0(x\mathbin\cdot\mathbf1)(x\mathbin\cdot e), \tag{8}
\]

where

\[
 Q_0=r^3[\overline\phi_B]_+[\overline\phi_D]_+.      \tag{9}
\]

This is the singleton-root Schur form.  Every rank at least two is still
present through the two killed Green kernels in (2)--(4).

## 2. Honest renewal cancellation

Suppose first that the recurrent dual makes a nondegenerate low/high trace;
this includes the finite-prefix regime in Section 5, whose orders are at
least six.  Split it into the low sector `1<=|A|<=2` and the high sector
`|A|>=3`.  Let `nu_U^-` be the stationary entrance law of a low excursion,
let `G_U^-` be its killed low Green kernel, and put

\[
 h_U=\nu_U^-G_U^-.                                    \tag{10}
\]

Write

\[
 B_i=h_B(\{i\}),\qquad D_i=h_D(\{i\}),
 \qquad H_B=\sum_iB_i,\qquad H_D=\sum_iD_i.           \tag{11}
\]

Let `T_U` and `M_U` be the time and rank reward of one complete alternating
low-plus-high cycle, and set

\[
 X_U=\frac{M_U}{s}-pT_U.                              \tag{12}
\]

The renewal current multiplies every stationary occupation and cancels in
the normalized trace quantities.  Hence

\[
 \lambda_{B,i}=\frac{B_i}{H_B},\qquad
 \lambda_{D,i}=\frac{D_i}{H_D},\qquad
 \overline\phi_B=\frac{X_B}{H_B},\qquad
 \overline\phi_D=\frac{X_D}{H_D}.                   \tag{13}
\]

Define the full-cycle target

\[
 \boxed{Z=r^3[X_B]_+[X_D]_+.}                        \tag{14}
\]

Since `H_B,H_D>0`, equations (9), (13), and positivity of the normalizers
give

\[
 Q_0=\frac{Z}{H_BH_D}.                               \tag{15}
\]

Multiplying (8) by `H_BH_D` proves the normalizer-free renewal form

\[
 \boxed{
 (x\mathbin\cdot B)(x\mathbin\cdot(eD))
 \ge Z(x\mathbin\cdot\mathbf1)(x\mathbin\cdot e)
 \quad\hbox{for every }x\ge0.}                      \tag{RMP}
\]

This cancellation is new only as a change to honest renewal variables.
The portal theorem applied below is the already proved theorem in
`../rhyb_mp_orientation_minimax/ORIENTATION_PRESERVING_PORTAL_MINIMAX.md`;
it is not reproved or claimed as a second discovery here.
If one dual has no high crossing (a degenerate small-order case), its
singleton Schur form (8) remains exact, but the alternating-cycle notation
(10)--(15) is simply not used.

## 3. Exact one-root and two-root criterion

Apply that portal theorem to

\[
 U_i=B_i,\qquad V_i=D_i,\qquad W_i=e_iD_i,
 \qquad Q=Z.                                         \tag{16}
\]

For each root define

\[
 \boxed{\mathfrak d_i=e_i(B_iD_i-Z),}                \tag{17}
\]

and, for `i!=j`, define

\[
 \boxed{
 \mathfrak k_{ij}
 =B_ie_jD_j+B_je_iD_i-Z(e_i+e_j).}                   \tag{18}
\]

Then `(RMP)` is equivalent to the finite family

\[
 \boxed{
 \mathfrak d_i\ge0\quad(i\in V),\qquad
 \mathfrak k_{ij}+2\sqrt{\mathfrak d_i\mathfrak d_j}\ge0
 \quad(i\ne j).}                                    \tag{19}
\]

Indeed, on a portal supported on `{i,j}`, the homogeneous gap is

\[
 \mathfrak d_ix_i^2+\mathfrak k_{ij}x_ix_j
 +\mathfrak d_jx_j^2,                                \tag{20}
\]

and (19) is the exact two-by-two copositivity criterion.  The support-two
theorem says that these tests are also sufficient for every portal load.
The factor `2` in (19) belongs to the coefficient convention (18); if the
cross coefficient in (20) is written as `2c_ij`, the same test is
`c_ij+sqrt(d_i d_j)>=0`.

The same theorem gives an exact normalizer-free positive-diagonal minimax.
When `Z>0`, `(RMP)` is equivalent to

\[
 \boxed{
 \text{for every }z>0\text{ there exists }t>0\text{ such that}
 \quad
 zB_i+z^{-1}e_iD_i
 \ge\sqrt Z\,(t+e_i/t)\quad\hbox{for every }i.}     \tag{21}
\]

For `Z=0`, `(RMP)` is automatic.  Formula (21) can also be obtained from
the normalized singleton minimax by setting
`z=lambda sqrt(H_D/H_B)` and multiplying by `sqrt(H_BH_D)`.  Thus both
singleton normalizers disappear, while the two global scalars and their
quantifier order remain unchanged.

For fixed `z`, define the interval

\[
 I_i(z;Z)=\left[
 {c_i(z)-\sqrt{c_i(z)^2-4Ze_i}\over2\sqrt Z},
 {c_i(z)+\sqrt{c_i(z)^2-4Ze_i}\over2\sqrt Z}
 \right],
 \quad c_i(z)=zB_i+z^{-1}e_iD_i,                    \tag{22}
\]

and declare it empty if the discriminant is negative.  Then (21) says
that `intersection_i I_i(z;Z)` is nonempty for every `z`.  Pairwise
intersection is sufficient by one-dimensional Helly.  This is the exact
two-source renewal target; it does not estimate either dual separately.

## 4. The orientation square that Cauchy must retain

Put `m_i=B_iD_i`.  The cross assignment in (18) has the exact split

\[
 B_ie_jD_j+B_je_iD_i
 =2\sqrt{e_ie_jm_im_j}+\Omega_{ij},                  \tag{23}
\]

where

\[
 \boxed{
 \Omega_{ij}=
 (\sqrt{B_ie_jD_j}-\sqrt{B_je_iD_i})^2\ge0.}         \tag{24}
\]

Consequently the exact pair margin is

\[
\begin{split}
 \mathfrak k_{ij}+2\sqrt{\mathfrak d_i\mathfrak d_j}
 ={}&\Omega_{ij}\\
 &+2\sqrt{e_ie_j}\left[
  \sqrt{m_im_j}+\sqrt{(m_i-Z)(m_j-Z)}
  -{Z(e_i+e_j)\over2\sqrt{e_ie_j}}
 \right].                                           \tag{25}
\end{split}
\]

Ordinary rootwise Hellinger/Cauchy drops `Omega_ij` and asks that the square
bracket in (25) be nonnegative.  That is a genuine strengthening, not an
equivalent proof of (19).  The distinction is exact even on positive
rational data.  Take

\[
 (e_i,e_j)=(100,1),\qquad
 (B_i,B_j)=(100,1),\qquad
 (D_i,D_j)=(1/50,2),\qquad Z=1.                      \tag{26}
\]

Then `m_i=m_j=2`,

\[
 \mathfrak d_i=100,qquad \mathfrak d_j=1,qquad
 \mathfrak k_{ij}=101,                               \tag{27}
\]

so the exact margin is `121>0`.  But the Hellinger bracket, before its
positive factor, is

\[
 2+1-\frac{101}{20}=-\frac{41}{20}<0.                \tag{28}
\]

The missing square is `Omega_ij=162` and repays the deficit exactly:
`162-41=121`.  This is an abstract algebraic route audit, not a claim that
(26) is generated by a physical module.  It proves precisely that a
two-source Cauchy derivation which replaces the two swapped assignments by
their geometric mean cannot establish the exact pair theorem from
positivity alone.  A physical proof may still use Cauchy, but it must retain
or separately repay (24).

## 5. No fixed rank prefix can prove even the diagonals

The obstruction below applies simultaneously to the Bd and dB duals.
Their one-step maps have the common support property

\[
 |A'|\ge |A|-1.                                      \tag{29}
\]

For Bd, a neutral arrow replaces one occupied target by one source and a
selective arrow only adds a source.  For dB, an occupied target is removed
and replaced by a nonempty sampled union.  In either case one update can
delete at most the named target.

Fix any integer `m>=1`, let `s=2(m+2)`, and take a complete regular module
of order `s`.  Let `pi_U` be the genuine stationary law of dual `U`, put

\[
 \Lambda_{m,U}=\sum_{1\le |A|\le m+1}\pi_U(A),       \tag{30}
\]

and choose a set `R_U` of rank `m+2`.  For `0<epsilon<1`, define

\[
 \widetilde\pi_{U,\epsilon}(A)=
 \begin{cases}
  \epsilon\pi_U(A),&1\le |A|\le m+1,\\
  1-\epsilon\Lambda_{m,U},&A=R_U,\\
  0,&\text{otherwise}.
 \end{cases}                                         \tag{31}
\]

This is a nonnegative normalized law.  If `|A|<=m`, property (29) gives
`Q_U(B,A)=0` whenever `|B|>=m+2`.  Hence every coordinate stationarity
equation through rank `m` remains exact:

\[
\begin{split}
 (\widetilde\pi_{U,\epsilon}Q_U)(A)
 &=\epsilon\sum_{1\le|B|\le m+1}\pi_U(B)Q_U(B,A)\\
 &=\epsilon(\pi_UQ_U)(A)=0.                          \tag{32}
\end{split}
\]

This holds separately for both duals, including all nonsymmetric labelled
coordinate equations.  The complete module is used only to give one
canonical genuine starting law at every depth; no family of kernels is
searched.

Let `rho_tilde_U,epsilon` be the mean density of (31).  Directly,

\[
 \widetilde\rho_{U,\epsilon}
 ={\epsilon\sum_{1\le|A|\le m+1}|A|\pi_U(A)
 +(m+2)(1-\epsilon\Lambda_{m,U})\over s}
 \longrightarrow\frac12.                            \tag{33}
\]

Meanwhile every singleton atom and the total singleton mass scale as

\[
 \widetilde u_{U,i}=\epsilon u_{U,i},\qquad
 \widetilde c_U=\epsilon c_U,                        \tag{34}
\]

so the normalized root laws `lambda_U` are unchanged.  Since

\[
 \frac12-p=\frac{2-r}{2r}>0\qquad(1<r<2),            \tag{35}
\]

both pseudo-laws are on the active branch for all sufficiently small
`epsilon`.  Define the divided raw-MP target for these relaxed laws by

\[
 \widetilde Q_0=
 {r^3[\widetilde\rho_{B,\epsilon}-p]_+
       [\widetilde\rho_{D,\epsilon}-p]_+
  \over\widetilde c_B\widetilde c_D}.                \tag{36}
\]

This is an algebraic normalization of the raw target, not a claim that the
nonstationary pseudo-laws possess the honest Green reward (4).  It satisfies

\[
 \lim_{\epsilon\downarrow0}\epsilon^2\widetilde Q_0
 ={r^3(1/2-p)^2\over c_Bc_D}>0.                      \tag{37}
\]

Thus `Q_tilde_0` tends to infinity while every
`lambda_B,i lambda_D,i` stays fixed.  For all sufficiently small
`epsilon`, every one-root diagonal

\[
 e_i(\lambda_{B,i}\lambda_{D,i}-\widetilde Q_0)      \tag{38}
\]

is strictly negative.  Equivalently, at a portal supported only on root
`i`, the raw singleton product is `O(epsilon^2)` while

\[
 r^3(\widetilde\rho_{B,\epsilon}-p)
    (\widetilde\rho_{D,\epsilon}-p)
 \longrightarrow r^3(1/2-p)^2>0.                    \tag{39}
\]

The pseudo-laws are unconstrained at the first omitted rank and are not
stationary graph laws, so they do not refute `(MP)`.  The exact `m=2`
replay verifies a nonzero rank-three residual for each dual.  What
(29)--(39)
prove is the following uniform logical obstruction:

> Positivity, normalization, and every coordinate stationary equation
> through any fixed rank `m` cannot prove the universal minimal product,
> even after its portal quantifier has been reduced exactly to one- and
> two-root tests.

The construction works throughout `1<r<2`, hence at the algebraic
`R_hyb`.  A bounded-rank Cauchy or renewal closure is therefore exhausted.
Any surviving proof must use the full high return, an order-dependent depth
which tends to infinity, or a global Green/tree identity encoding that
return.

## 6. Exact remaining theorem

The portal variable and every stationary/renewal normalizer have now been
removed.  The unresolved physical theorem is exactly this:

> For the two honest full dual excursions of every module with a
> nondegenerate low/high trace at `r=R_hyb`, their positive excess-reward
> product `Z` and root occupation fields `B,D` satisfy (17)--(19),
> equivalently (21).  Degenerate low-only cases are read directly in the
> singleton Schur variables (8)--(9).

The diagonal part is

\[
 B_iD_i\ge r^3[X_B]_+[X_D]_+\qquad(i\in V),          \tag{40}
\]

and the pair part must retain the orientation square (24).  Neither follows
from a fixed rank prefix.  Ordinary rootwise Cauchy is also not exact
because it discards (24).  This leaves a sharply specified full-rank,
orientation-preserving Green/renewal comparison; no graph search or
finite-prefix coefficient search remains on this route.

## 7. Exact replay

From the repository root run

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
rhyb_two_root_mp_criterion/verify_two_root_renewal.py
```

The replay checks the normalizer cancellation, the two-root polynomial and
orientation split, the strict rational separation (26)--(28), and an
independent exact `m=2`, `s=8` complete-kernel pseudo-law for both duals.
It checks every labelled singleton and doubleton stationarity equation and
then verifies strict failure of the one-root product.  It performs no graph
enumeration and makes no claim that the pseudo-laws are stationary.
