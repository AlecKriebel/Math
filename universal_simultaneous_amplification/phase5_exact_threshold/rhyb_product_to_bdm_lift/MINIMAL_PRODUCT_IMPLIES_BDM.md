# From the minimal stationary product to BDM by a weak-core lift

Date: 2026-08-13 (America/Los_Angeles)

No literature search, graph search, or external communication was used.

## 1. Status and theorem

**PROVED, within the already proved separated first-exit normal form.**
Assume at `r=R_hyb` the portal-general minimal stationary product inequality

\[
 q_B(H,x)q_D(H,x)\ge r^3[\rho_{Bd}(H,r)-p]_+
                         [\rho_{dB}(H,r)-p]_+,
 \qquad p={r-1\over r},                                  \tag{MP}
\]

for every finite connected weighted graph `H` and every positive portal
vector `x`.  Then every bounded separated module satisfies BDM, equivalently

\[
                         D+(r-1)B\le0                     \tag{1}
\]

at every gate scale.

The implication uses no graph classification.  If (1) failed, the exact
leaf/strong-pair convexification would make a *paired* positive response.
Realize that finite response packet around a large complete core, put the
next portal on the core, and send the cut clock to zero.  The original-fitness
response survives because the separated gate trace depends on conditional
first-exit probabilities, not on its common clock.  The reciprocal-fitness
Bd core singleton output does not: a core mutant must reproduce across the
weak cut before local core absorption in order to acquire a module refuge.
This contradicts (MP) at the first response scale.  No separate control of
the dB singleton output is needed, since it is at most one.

This closes an important logical loop.  BDM is stronger than the one-module
gate disjunction, but it is not an additional stationary conjecture once
(MP) is known universally: a strict BDM violation manufactures a connected
compound graph that violates (MP).

The result is not a compactness theorem for arbitrary graph sequences and
does not prove (MP).  Its only dynamical input is the existing separated
first-exit realization, including its common physical mixing coefficient.

## 2. Why four local coordinates do not compose by themselves

For a bounded module write

\[
 b=\rho_{Bd}(H,r),\quad d=\rho_{dB}(H,r),\quad
 q_B=\sum_i\gamma_iq_{Bd,i},\quad
 q_D=\sum_i\alpha_iq_{dB,i}.                            \tag{2}
\]

At Bd gate odds `z`, with

\[
 K={r(r-1)^2\over q_Bq_D},                              \tag{3}
\]

the paired response is

\[
 B=s\left\{{rb\over r-1}{z\over1+z}-1\right\},\qquad
 D=s\left\{{rd\over r-1}{K\over K+z}-1\right\}.       \tag{4}
\]

The four numbers in (2) determine (4), but they do **not** determine the
reciprocal singleton output of a compound graph.  That output also depends
on

1. where the next portal is supported;
2. the absolute clock on the cut between the core and the modules; and
3. the core excursion law before its first cut crossing.

Indeed, multiply every core--module conductance by `tau`.  For every module
with positive internal conductance, the two leading first-exit currents have
the same cut-clock factor, so their gate odds are unchanged.  The ordinary
leaf is a row-normalization boundary: its two literal rates do not share a
clock, but its exact limiting response `(1/(r-1),-1)` is itself independent
of the leaf-edge weight.  Thus every response packet used below survives the
weak-cut limit.

For Bd at reciprocal fitness, a mutant started in the core can enter *any*
module only by reproducing across a core row.  Since the core degree is
dominated by its complete-core edges, the total mutant-export rate is
proportional to `tau`, including when the target module is an ordinary leaf.
Resident-module reproduction into the core can only remove core mutants and
therefore cannot invalidate the upper bound below.

Thus there is no closed transformation

\[
                 (b,d,q_B,q_D)\longmapsto(q_B^{out},q_D^{out})
\]

without extra macro data.  The useful fact is that the missing cut-clock
datum can be sent to zero while all original-fitness response coordinates
stay fixed.

## 3. The exact weak-cut reciprocal bound

Fix a finite core order `C` and finitely many module copies.  Let `G_tau` be
the connected graph obtained by multiplying every core--module conductance
by `tau>0`.  Start a Bd mutant at a core vertex at fitness `1/r`.  Let

* `T_C` be the absorption time of the isolated core chain, and
* `E_tau` be the event that a core mutant reproduces into a module before
  the isolated core mutant population is absorbed.

For fixed `C` and a fixed finite number of modules,

\[
                         \Pr(E_\tau)\longrightarrow0
                         \qquad(\tau\downarrow0).          \tag{5}
\]

This is a direct finite-state clock statement.  Conditional on the isolated
core path, `T_C<infinity` almost surely and the integrated mutant-export
intensity is `tau` times a finite random variable.  Extra reproduction from
resident modules into the core only removes mutants, so the actual core
mutant set is dominated until `E_tau` by the isolated complete-core chain.
Dominated convergence proves (5).

Here the modules use the uniform-bundle realization of the separated normal
form: every core row sees the same total module load.  Consequently the
internal complete-core Bd chain is changed only by a common clock factor;
the additional resident-module arrows are adverse.  This is the precise
coupling behind the word “dominated.”

On `E_tau^c`, global mutant fixation is impossible if the dominating
isolated core mutant becomes extinct.  If the isolated core fixes, the
conditional chance of later global fixation is at most one.  Therefore,
uniformly over the core starting vertex,

\[
 \limsup_{\tau\downarrow0}
 \phi^{Bd}_{G_\tau,i}(1/r)
 \le \rho_{Bd}(K_C,1/r).                               \tag{6}
\]

The two exact complete-core values are

\[
 \rho_{Bd}(K_C,1/r)={r-1\over r^C-1},\qquad
 \rho_{dB}(K_C,1/r)
 ={(r-1)(1-C^{-1})\over r^{C-1}-1}.                    \tag{7}
\]

Both are `O_r(r^{-C})`.

Now choose the outer portal load to be one on the core and `eta>0` on the
module vertices.  Letting `eta downarrow 0` conditions the Bd portal law on
the core.  The singleton averages are continuous in `eta`, so (MP), assumed
for positive portals, also holds in this limiting portal direction.  Equations
(5)--(7) make the Bd outer singleton factor arbitrarily close to an
exponentially small complete-core term.  The dB outer singleton factor needs
no estimate beyond the universal bound `0<=q_D^{out}<=1`.

Equivalently, one may keep every portal entry strictly positive.  After
choosing `C` and `tau`, choose the module leakage `eta` so small that its
contribution to `q_B^{out}` is below any prescribed tolerance.  This is the
finite positive-portal version used on the diagonal below.

The order of limits is essential and legitimate.  For a fixed core and a
fixed finite packet, let

\[
 R^{\rm tr}_{U}(C,\mathbf q)
       :=\lim_{\tau\downarrow0}\rho_U(G_{C,\mathbf q,\tau},r). \tag{7a}
\]

This is the finite Schur-trace limit: eliminate each locally absorbing
component before retaining the next cross-component jump.  It exists for
every fixed finite datum because the fixation probabilities are rational
functions of the positive edge weights, and the first nonzero common power
of `tau` in each retained row gives the finite embedded exit kernel.  The
ordinary-leaf row is retained at its first nonzero (order-zero) boundary
power.  Thus the already proved separated normal form is precisely an
asymptotic statement about the values in (7a), not an estimate required to
hold uniformly over small `tau`.

The diagonal therefore has the following order:

1. choose a large but finite `C` and finite module counts;
2. use the separated theorem for the sequence of finite trace values
   `R_U^{tr}(C,mathbf q)`;
3. for that fixed finite graph, choose positive `tau` so its two
   original-fitness fixation probabilities are as close to (7a) as desired
   and (6) has the required reciprocal-fitness error;
4. only then advance to the next large-core/dilute stage.

Every graph to which (MP) is applied still has `tau>0` and is connected.

## 4. First-order compound transformation

Let `v_j=(B_j,D_j)` be a finite menu of physical module responses and let
`lambda_j>=0` be fixed common coefficients.  The common-coefficient
first-exit lemma gives

\[
                         V=\sum_j\lambda_jv_j.            \tag{8}
\]

The `v_j` are closed trace rays.  Because the final inequalities are strict,
first choose finite positive graph approximants and rational coefficients
whose packet still has the same strict coordinate signs.  All approximation
errors are fixed and absorbed before `delta`, `tau`, and the outer portal
leakage are chosen.

Choose core orders `C_k to infinity`, module counts tending to infinity but
of total density `delta_k to 0`, and with type proportions converging to the
`lambda_j`.  Take, for example, a rational approximation to the coefficients
and a common count of order `sqrt(C_k)`.  Then `C_k^{-1}=o(delta_k)`.

Write `R_{U,k}^{tr}` for (7a) at the `k`th finite core and packet.  The exact
separated normal form and the complete-graph baselines give

\[
 R_{Bd,k}^{tr}=p+p\delta_kV_B+o(\delta_k),\qquad
 R_{dB,k}^{tr}=p+p\delta_kV_D+o(\delta_k).              \tag{9}
\]

Here `delta_k` is the common multiplicity/core scale; the fixed orders of
the finitely many packet types have already been absorbed into their response
vectors.  For each finite `k`, continuity toward its own trace value permits
choosing `tau_k>0` so that

\[
 |\rho_U(G_{k,\tau_k},r)-R_{U,k}^{tr}|=o(\delta_k)
 \quad(U=Bd,dB),                                      \tag{9a}
\]

while the probability in (5) is `o(delta_k^2)`.  These are finitely many
pointwise requirements at stage `k`; no common modulus in `k` is invoked.
Choose the positive outer-portal leakage `eta_k` so its Bd singleton
contribution is also `o(delta_k^2)`.  Choose `C_k` sufficiently fast that
the complete-core term in (7) is `o(delta_k^2)`.  Then

\[
 q_{B,k}^{out}=o(\delta_k^2),\qquad
                         0\le q_{D,k}^{out}\le1.        \tag{10}
\]

Equations (9)--(10) are the exact controlled projection needed here:

\[
 \boxed{
 \begin{aligned}
 \rho_{Bd}^{out}&=p+p\delta V_B+o(\delta),&
 \rho_{dB}^{out}&=p+p\delta V_D+o(\delta),\\
 q_B^{out}&=o(\delta^2),&0\le q_D^{out}&\le1.
 \end{aligned}}                                        \tag{11}
\]

The one-sided nature of (11) is important.  For example, a dB update at a
degree-one leaf is insensitive to a common rescaling of its only edge, so a
claim that both reciprocal outputs vanish would be false without additional
macro assumptions.  The product theorem needs only the Bd factor.

No uniform-in-`k` singular-perturbation estimate is assumed.  Equation (9)
belongs to the trace sequence; (9a) transfers it to connected positive-cut
graphs one finite stage at a time.  The cut clock `tau_k` is selected only
after `C_k` and all finite module counts have been fixed.  This iterated
choice is exactly the usual diagonal realization of the separated response
cone.

If `V_B,V_D>0`, applying (MP) to `G_k` gives, on the one hand,

\[
 q_{B,k}^{out}q_{D,k}^{out}=o(\delta_k^2),              \tag{12}
\]

and, on the other,

\[
 r^3[\rho_{Bd}(G_k,r)-p]_+
     [\rho_{dB}(G_k,r)-p]_+
 =r^3p^2\delta_k^2V_BV_D+o(\delta_k^2).                \tag{13}
\]

This is a contradiction.  Hence universal (MP) implies

\[
 \boxed{\text{the closed paired separated response cone does not meet }
                         (0,\infty)^2.}                 \tag{14}
\]

## 5. Exact convexification of a BDM violation

Put `c=r-1` and

\[
                         L(B,D)=D+cB.                    \tag{15}
\]

At `r=R_hyb`, the ordinary leaf and the tangent strong-pair response are

\[
 \ell=(1/c,-1),\qquad k=(-\eta/c,\eta),\quad\eta>0,     \tag{16}
\]

and both have `L=0`.  Suppose a physical module has response `v=(B,D)`
with `L(v)>0`.

The rays in (16) are closure rays of finite positive constructions.  The
leaf is obtained by the standard uniform-bundle satellite limit, and the
tangent `K_2` ray by the hybrid gate scale.  In each use below, choose a
finite approximant close enough that the strict positive margin survives;
then fix that approximant before forming the outer weak-core diagonal.

* If `B<0`, put `lambda_0=-cB`.  Then

  \[
  v+\lambda_0\ell=(0,L(v)).                              \tag{17}
  \]

  Increasing `lambda_0` by a sufficiently small positive amount makes both
  coordinates positive.
* If `B>=0,D<=0`, put `lambda_0=-D/eta`.  Then

  \[
  v+\lambda_0k=(L(v)/c,0).                               \tag{18}
  \]

  Again, a sufficiently small positive increase makes both coordinates
  positive.
* If the response is already in the positive quadrant there is nothing to
  add.  The boundary case `B=0<D` is made strict by an arbitrarily small leaf
  coefficient.

All coefficients are common physical module multiplicities by the proved
first-exit lemma.  Thus a strict BDM violation produces a finite paired
packet `V` with `V_B,V_D>0`, contradicting (14).  This proves (1).

## 6. Consequence and remaining theorem

The matching-upper proof order can now be shortened:

1. prove the portal-general minimal product inequality (MP), equivalently
   the two-copy MPER/Schur-trace sign;
2. invoke the weak-core lift above to obtain BDM automatically for every
   bounded separated module;
3. use the already proved paired first-exit cone lift.

The local Hellinger inequality no longer needs an independent stationary
proof if (MP) is established.  The open stationary theorem is the genuinely
minimal two-copy product sign.  The global bulk/compactness alternative
remains separate.

## 7. Exact replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python -B \
  verify_product_to_bdm_lift.py
```

The replay verifies the convexification identities, the complete-core
reciprocal formulas, the response-scale product contradiction, and the
invariance of a two-rate gate under a common cut-clock rescaling.  It is an
algebraic replay of the proved reduction, not a graph screen and not a proof
of (MP).
