# Rank-three renewal reduction for the bounded dual-moment lemma

## Status

This note proves an exact stationary-flow reduction for the bounded
dual-moment lemma (BDM).  It does **not** prove BDM.  Its purpose is to replace
the false rank-one/rank-two relaxation by the smallest legal higher-rank
object: the Palm law of entrances from rank three into rank two, followed by
the two killed excursion Green operators.

The main conclusions are:

1. the singleton equations are only the first block row of an exact
   rank-one/rank-two Schur system;
2. the missing second block row is a nonnegative rank-three entrance current;
3. alternating low/high excursions give exact renewal coordinates for all
   four BDM observables;
4. the full three-copy BDM forcing has an exact Schur trace on the
   singleton/doubleton sectors; and
5. BDM is equivalent to one fitness-resolved cross-rule inequality between
   the cycle rewards, displayed in (24).

Thus the earlier pseudo-law obstruction is completely removed for every
fixed module.  The remaining problem is a genuine comparison of the Bd and
dB excursion laws induced by the same undirected conductances.

## 1. Set chains and the rank-two cut

Let `H=(V,w)` be a finite connected loopless weighted graph of order `s`, let
`r>1`, and put

\[
 d_i=\sum_jw_{ij},\qquad P_{ij}=w_{ij}/d_i,
 \qquad g_r(x)={x\over r-(r-1)x}.                       \tag{1}
\]

For `U in {Bd,dB}`, let `Q_U` be the row generator of the exact stationary
OR dual at fitness `r`, and let `pi_U` be its stationary law.  We work on the
recurrent support of `pi_U`.  For Bd this is the set of all nonempty subsets.
For loopless dB, the full set has no incoming transition and is omitted.

Split the recurrent state space into

\[
 \mathcal L=\{A:1\le |A|\le2\},\qquad
 \mathcal H=\{A:|A|\ge3\}.                             \tag{2}
\]

The alternating-renewal reduction in Sections 2--5 applies only when both
blocks are nonempty for the rule under consideration.  Thus it does not give
a two-rule RTER statement for **any** order-three module: the dB high block is
empty even though the Bd full-set state is recurrent.  These are genuine
mixed boundary cases.  The exact `K_2` equality calculation handles order
two, and the separate direct weighted-path theorem proves BDM for the path
subclass of order three.  Arbitrary positive triangles still require a
separate BDM theorem.  The low-sector trace in Section 6 does extend to all
of these mixed boundary cases.

Use superscripts `-` and `+` for restrictions to `mathcal L` and
`mathcal H`.  In block form,

\[
 Q_U=\begin{pmatrix}Q_U^{--}&Q_U^{-+}\\
                     Q_U^{+-}&Q_U^{++}\end{pmatrix},
 \qquad \pi_U=(\pi_U^-,\pi_U^+).                       \tag{3}
\]

Whenever both blocks are nonempty, irreducibility on the recurrent support
implies that each block is left almost surely.  Both killed blocks are
therefore transient, hence

\[
 G_U^-=(-Q_U^{--})^{-1},\qquad
 G_U^+=(-Q_U^{++})^{-1}                                \tag{4}
\]

exist and are entrywise nonnegative.

## 2. The exact rank-three entrance current

Define the stationary entrance and exit currents

\[
 \eta_U=\pi_U^+Q_U^{+-},\qquad
 \xi_U=\pi_U^-Q_U^{-+}.                                \tag{5}
\]

Every dual update can lower the rank by at most one.  Consequently `eta_U`
is supported on doubletons, and only triples contribute to it.  For a
doubleton `C` its two rule-specific formulas are

\[
 \boxed{\eta_{Bd}(C)=
 \sum_{k\notin C}\pi_{Bd}(C\cup\{k\})
              \sum_{u\in C}P_{uk},}                   \tag{6}
\]

\[
 \boxed{\eta_{dB}(C)=
 \sum_{k\notin C}\pi_{dB}(C\cup\{k\})
              g_r(P_{kC}),\qquad
 P_{kC}=\sum_{u\in C}P_{ku}.}                         \tag{7}
\]

Indeed, a Bd triple `C union {k}` falls to `C` exactly when a neutral arrow
replaces occupied `k` by one of the two occupied vertices in `C`.  A dB
triple falls to `C` exactly when target `k` is removed and every member of
the geometric row-`k` burst lies in `C`; this has probability
`E[P_{kC}^K]=g_r(P_{kC})`.

The two stationary block equations give

\[
 \boxed{\pi_U^-=\eta_UG_U^-,\qquad
        \pi_U^+=\xi_UG_U^+.}                           \tag{8}
\]

Moreover the common crossing current

\[
 J_U:=\eta_U\mathbf1=\xi_U\mathbf1                    \tag{9}
\]

is positive.  Equation (8), rather than normalization alone, is the first
missing higher-rank constraint in the singleton relaxation.

### Proof

Stationarity in the low block reads

\[
 \pi_U^-Q_U^{--}+\pi_U^+Q_U^{+-}=0.
\]

Right multiplication by `G_U^-` proves the first identity in (8); the high
block is identical.  Since
`Q_U^{--}1=-Q_U^{-+}1`, the first identity gives

\[
 \eta_U1=-\pi_U^-Q_U^{--}1=\pi_U^-Q_U^{-+}1=\xi_U1.
\]

This proves (8)--(9).  Formulae (6)--(7) follow directly from the two update
maps as described above.  QED.

## 3. The missing doubleton equation as a Schur repayment

Order the low states by rank and put

\[
 M_U=-Q_U^{--}
 =\begin{pmatrix}M_{11}^U&M_{12}^U\\
                  M_{21}^U&M_{22}^U\end{pmatrix},
 \qquad \pi_U^-=(q_U,p_U),\qquad \eta_U=(0,\eta_U^{(2)}), \tag{10}
\]

where `q_U` is the row of singleton atoms and `p_U` the row of doubleton
atoms.  Equation (8) is equivalent to the two block equations

\[
 q_UM_{11}^U+p_UM_{21}^U=0,                            \tag{11}
\]

\[
 q_UM_{12}^U+p_UM_{22}^U=\eta_U^{(2)}.                 \tag{12}
\]

The previously used singleton-state balances are exactly (11).  They leave
`p_U` free.  The missing doubleton equation (12) forces the repayment current
from rank three.

Define the killed rank-two Schur complement

\[
 \mathcal S_U=M_{22}^U-M_{21}^U(M_{11}^U)^{-1}M_{12}^U. \tag{13}
\]

Then

\[
 \boxed{p_U=\eta_U^{(2)}\mathcal S_U^{-1},\qquad
 q_U=-\eta_U^{(2)}\mathcal S_U^{-1}
                 M_{21}^U(M_{11}^U)^{-1}.}             \tag{14}
\]

All displayed Green/Schur transfer matrices have the signs dictated by a
killed Markov chain; in particular the map from `eta_U^(2)` to `q_U` in
(14) is nonnegative.

This gives a precise diagnosis of the first-level pseudo-law.  Multiplying
all rank-one/rank-two masses by `lambda` while retaining order-one mass at
rank three preserves (11), but violates (12) unless the true entrance
current is also `O(lambda)`.  Even if a selected triple has zero immediate
downward rate, the high-block equation in (8) forces its eventual return
current.  For a fixed module,

\[
 \pi_U^-=O(\lambda)
 \Longrightarrow \xi_U=O(\lambda)
 \Longrightarrow \pi_U^+=\xi_UG_U^+=O(\lambda),       \tag{15}
\]

contradicting normalization.  A pseudo-law scaling can arise along a
degenerating sequence only if the high-excursion Green norm diverges.  This
is exactly the Green-uniformity issue that a global compactness theorem must
retain rather than discard.

## 4. Alternating-excursion Palm law

Normalize the two boundary currents:

\[
 \nu_U^-={\eta_U\over J_U},\qquad
 \nu_U^+={\xi_U\over J_U}.                             \tag{16}
\]

Thus `nu_U^-` is supported on doubletons.  The killed exit kernels

\[
 K_U^-=G_U^-Q_U^{-+},\qquad K_U^+=G_U^+Q_U^{+-}         \tag{17}
\]

are stochastic, and

\[
 \nu_U^+=\nu_U^-K_U^-,\qquad
 \nu_U^-=\nu_U^+K_U^+.                                \tag{18}
\]

They describe one low excursion followed by one high excursion.  Hence
`nu_U^-` is stationary for the honest return kernel `K_U^-K_U^+` on the
rank-two entrance boundary.

Let `k(A)=|A|`.  For a portal probability vector `omega`, put

\[
 f_\omega(A)=
 \begin{cases}\omega_i,&A=\{i\},\\0,&|A|\ne1.\end{cases} \tag{19}
\]

Define the cycle rewards

\[
 \begin{aligned}
 T_U^-&=\nu_U^-G_U^-\mathbf1,&
 T_U^+&=\nu_U^+G_U^+\mathbf1,& T_U&=T_U^-+T_U^+,\\
 M_U^-&=\nu_U^-G_U^-k,&
 M_U^+&=\nu_U^+G_U^+k,& M_U&=M_U^-+M_U^+,\\
 S_U^\omega&=\nu_U^-G_U^-f_\omega.
 \end{aligned}                                        \tag{20}
\]

Equations (8)--(9) and normalization now give the exact renewal identities

\[
 \boxed{J_U={1\over T_U},\qquad
        m_U={M_U\over T_U},\qquad
        q_U^\omega={S_U^\omega\over T_U}.}             \tag{21}
\]

No reversibility of either set chain is used.

## 5. The rank-three excursion repayment inequality

Take `omega=gamma` for Bd and `omega=alpha` for dB, with the portal laws from
the bounded-module reduction.  Abbreviate

\[
 \mathsf A={M_{dB}\over s(r-1)},\qquad
 \mathsf B={M_{Bd}\over s}.                            \tag{22}
\]

Then the separate dB density condition `a<=1` is exactly

\[
 \boxed{\mathsf A\le T_{dB}.}                          \tag{23}
\]

After substituting (21) into BDM and multiplying by
`T_Bd T_dB`, the square roots homogenize.  BDM is therefore exactly
equivalent to (23) and

\[
 \boxed{
 S_{Bd}^{\gamma}S_{dB}^{\alpha}
 \ \ge\ r(r-1)^2
 \left[
   \sqrt{\mathsf A\mathsf B}
   -\sqrt{(T_{dB}-\mathsf A)(T_{Bd}-\mathsf B)}
 \right]_+^2.}                                        \tag{24}
\]

Call (24) the **rank-three excursion repayment inequality (RTER)**.  It is a
sufficient theorem for BDM and, with (23), an equivalent one.  Unlike the
first-level relaxation, every variable in RTER is generated by an honest
alternating excursion, its boundary laws obey (18), and the two rule-specific
rank-three entrance rates are the explicit conductance expressions (6)--(7).

For comparison with the product-chain forcing, put `C=r(r-1)^2` and let
`z>0`.  If `G_z` denotes the denominator-cleared BDM gap

\[
 G_z=C\{(1+z)(1-a)-zb\}
       +zq_Bq_D\{1+z(1-b)\},                           \tag{25}
\]

then its cycle form is

\[
 \begin{split}
 T_{Bd}^2T_{dB}G_z={}&
 C T_{Bd}\{(1+z)T_{Bd}(T_{dB}-\mathsf A)
                  -z\mathsf B T_{dB}\}\\
 &+zS_{Bd}^{\gamma}S_{dB}^{\alpha}
             \{(1+z)T_{Bd}-z\mathsf B\}.              \tag{26}
 \end{split}
\]

Thus the positive singleton product in the product-chain certificate is
literally the repayment furnished during the two low excursions; all rank
three and higher occupation is carried in the paired high-excursion rewards.

## 6. Exact low-sector trace of the product-chain forcing

There is also a pointwise certificate formulation that retains the full
higher-rank correction while moving the unknown potential onto ranks one and
two.  Define the stochastic Schur trace generator

\[
 \widehat Q_U
 =Q_U^{--}+Q_U^{-+}G_U^+Q_U^{+-}.                     \tag{27}
\]

It has nonnegative off-diagonal entries and zero row sums.  Moreover

\[
                         \pi_U^-\widehat Q_U=0.          \tag{28}
\]

For any full-state reward `f=(f^-,f^+)`, define its occupation trace

\[
 \mathcal T_Uf=f^-+Q_U^{-+}G_U^+f^+.                   \tag{29}
\]

The stationary reward is preserved exactly:

\[
                         \pi_Uf=\pi_U^-\mathcal T_Uf.   \tag{30}
\]

In particular, with

\[
 \tau_U=\mathcal T_U\mathbf1,\qquad
 \kappa_U=\mathcal T_Uk,                               \tag{31}
\]

one has

\[
 \pi_U^-\tau_U=1,\qquad
 \pi_U^-\kappa_U=m_U,\qquad
 \pi_U^-f_\omega=q_U^\omega.                          \tag{32}
\]

The measure `pi_U^-` is intentionally not normalized; `tau_U` carries the
high-excursion normalization exactly.

Unlike the alternating-renewal representation, this trace formulation also
extends to a low-only chain.  With the zero-dimensional convention for the
empty high block, the correction terms vanish,
`widehat Q_U=Q_U`, `tau_U=1`, and `kappa_U=k`.  Thus (27)--(34) include the
`K_2` boundary and the dB factor of every order-three module without assigning
them a fictitious crossing current.

Let `ell,ell'` be two Bd low states and `d` one dB low state.  Put
`C=r(r-1)^2`, `u=f_gamma`, and `v=f_alpha`.  The exact Schur-traced forcing is

\[
\begin{split}
 \widehat F_z(\ell,\ell',d)={}&
 C(1+z)\tau_B(\ell)\tau_B(\ell')
       \left\{\tau_D(d)-{\kappa_D(d)\over s(r-1)}\right\}\\
 &-{Cz\over s}\tau_B(\ell)\kappa_B(\ell')\tau_D(d)\\
 &+z u(\ell)v(d)
       \left\{(1+z)\tau_B(\ell')
                    -{z\over s}\kappa_B(\ell')\right\}.
                                                               \tag{33}
\end{split}
\]

By (32), its mean under the stationary, generally unnormalized product
measure
`pi_B^- tensor pi_B^- tensor pi_D^-` is exactly the mean of the original
full-state forcing (35) in the bounded-module note.  Hence BDM follows if,
for every `z>0`, there is a potential on the low product space satisfying

\[
 \boxed{
 \widehat F_z+
 (\widehat Q_{Bd}^{\ell}+\widehat Q_{Bd}^{\ell'}
                  +\widehat Q_{dB}^{d})\Phi_z\ge0.}     \tag{34}
\]

This is the promised rank-two/three stationary-flow correction to the old
product-chain program.  The state variables in (34) have ranks only one and
two.  All higher ranks occur through the positive occupation corrections
`Q^{-+}G^+` and the return term `Q^{-+}G^+Q^{+-}`.  Since `Q^{+-}` is supported
only on triple-to-doubleton transitions, (6)--(7) identify its exact boundary
law.

### Proof of the trace identities

The second identity in (8) may be written

\[
 \pi_U^+=\pi_U^-Q_U^{-+}G_U^+.
\]

Substitution into `pi_U f` proves (30), while substitution into the low
stationarity equation proves (28).  Finally, high-block transience
(equivalently, almost-sure return to the nonempty low block) gives

\[
 G_U^+Q_U^{+-}\mathbf1
 =G_U^+(-Q_U^{++})\mathbf1=\mathbf1,
\]

so (27) has zero row sums; its off-diagonal rates are visibly nonnegative.
Equation (33) follows by applying (30) independently to each factor of every
monomial in the original three-copy forcing.  Stationary averaging kills the
generator term in (34), proving sufficiency.  QED.

## 7. What remains

The reduction proves the exact higher-rank compatibility omitted by the
pseudo-law, but it does not supply the sign of (23)--(24).  Treating RTER as
proved would merely transfer the central difficulty, so it remains explicitly
OPEN.

The smallest structural theorem now visible is:

> At `r=R_hyb`, for the two alternating excursion systems induced by the same
> undirected conductances, prove (23) and RTER (24), with equality rigidity at
> the `K_2` boundary degeneration.

The path and complete-module theorems verify this statement in their exact
classes.  Any general proof must compare the two rule-specific return
kernels, not just their marginal rank profiles.  Formulae (6)--(7) show the
precise local bridge on the common rank-three boundary.

## 8. Exact replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python -B \
  verify_rank_three_renewal.py
```

The replay first checks the low-only `K_2` boundary symbolically, including
the two portal singleton sources, both mean-rank normalizations, and the
hybrid discriminant.  It then builds the two exact dual generators on a
hostile rational weighted four-path and checks, over the rationals,
(6)--(18), the Schur repayment (14), all renewal rewards (21), the cycle form
(26), and the trace identities (27)--(33).  It is an audit of the proved
identities, not evidence for the still-open sign (24).
