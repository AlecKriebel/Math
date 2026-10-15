# Parameter-robust transfer of the signed impulse proof

Checkpoint: 2026-10-06 (America/Los_Angeles). Mathematical resolution of full
project: 25% estimated; publication package: 3% estimated. The percentages
are estimates, not evidence.

This is a reusable proof of the **extension step**. Its hypotheses refer to
the actual analytic arguments in pinned family 362; they do not follow merely
from its headline theorem. The algebraic and transport inputs were checked
directly in `SUPPLEMENT_PAIR_IDENTITY.md`. The remaining scalar dyadic inequalities and
their uses must pass the independent upstream audit before this lemma can
support an unconditional global theorem. No Lean build or global
formalization is certified here.

**Lemma (fixed finite species transfer).** Fix `N<infinity`, masses `m_a>0`
and real charges `e_a`. Let (1) of `SUPPLEMENT_PAIR_IDENTITY.md` be a smooth classical
solution on `[0,t_*]`, with compact phase support there, nonnegative compactly
supported initial distributions, compatible Maxwell fields of the stated
finite-energy `C_b^infinity` class, and `t_*<=T_0<infinity`. Suppose the analytic
arguments in the upstream occupation.tex, direct.tex, direction.tex and
selection.tex are valid with exactly the hypotheses and estimates listed
below. Then there exist `M,A>=1` and `P_0`, depending on this datum, `T_0`,
`N`, masses and charges, such that for every common dyadic

\[
 P\ge P_0,\qquad P\ge1024\max_{a,t,z}q(V_a(t,z)),
\]

every supported receiver of every species `a`, every dyad `w=2^k`, `k>=0`,
and every interval `[t_1,t_2]` on which `w/8<=q(V_a(t))<=8w`, one has

\[
 |V_a(t_2)-V_a(t_1)|\le MP\sqrt{t_2-t_1}
     +A(t_2-t_1)\frac{P^2\log(2+P)}w.\tag{T}
\]

The constants are independent of `t_*` and of the chosen `P`, and are shared
by all species. They are not uniform in varying masses, charges or `N`.

**Proof.** Put `lambda_a=e_a/m_a`, `c_ab=lambda_a e_b`, `L=log(2+P)` and
`S(w)=P^2L/w`. All constants written `C` below may depend on the fixed data,
`T_0`, species parameters and decomposition, but not on `M,A,P,t_*`. To make
this dependence explicit, one may include

\[
 N,\quad H_0,\quad\max_b\|f_{b,0}\|_\infty,
 \quad\max_bm_b^{-1},\quad\max_b|\lambda_b|,
 \quad\max_{a,b}|c_{ab}|,\quad\max_{a,b}|c_{ab}\lambda_b|
\]

and the initial support sizes and finitely many bounded field derivatives.
No inverse charge occurs. Maximum constants over empty source species may
be replaced by one.

Fix a bootstrap endpoint `tau<=t_*` and assume (T) for **all species,
supported labels, dyads and eligible intervals in `[0,tau]`**. Every source
stability argument below is therefore authorized by this same hypothesis,
including when the source and receiver species differ. This is the only
bootstrap assumption; in particular an uncoupled species theorem is not
used.

For a receiver of species `a`, the exact retarded force is

\[
 K_a=K_a^{\rm data}+(4\pi)^{-1}\sum_b c_{ab}\int(T_b+S_b)\,dy\,dv.
\]

The pair kernels, measure changes and signed identity are proved in
`SUPPLEMENT_PAIR_IDENTITY.md`, (5)--(11). Their assumptions are satisfied because each
species' phase flow preserves volume, all normalized velocities are
strictly timelike, and `lambda_b` is constant. The energy density is positive
and mass weighted; every source density has the bounds

\[
 0\le f_b\le\|f_{b,0}\|_\infty,\quad
 \int qf_b\,dy\,dv\le H_0/m_b,\quad
 \int_{\mathrm{cone}}r^2qd f_b\le H_0/m_b.
\]

The good field cone budget is `<=4H_0`, independent of source species.
The following list supplies all changed hypotheses of the upstream chain.

1. **Occupation geometry and stability.** The exact identities
   `2d=|n-u_b|^2+q_b^{-2}`, `2D=|n-alpha|^2+q_X^{-2}` and
   `2epsilon=|alpha-u_b|^2+q_b^{-2}+q_X^{-2}` are unchanged. Thus all dyadic
   ranges, caps and deficit/actual classifications are unchanged. The source
   density bound `N_b<=C_b p^3 nu^2` uses its nonnegative transported density.
   The retarded Jacobians depend only on velocities and are unchanged.
   The crude energy and time-change occupation bounds follow specieswise.
   Stability on length
   `lambda=[C_1(P/m)(M/omega+sqrt(AL/omega))]^{-2}` follows from (T) for
   source `b` and receiver `a`, with one common `C_1`; it does not require
   `lambda_a=lambda_b`. The monotone relative-velocity crossing is purely
   kinematic. Averaging its label mass over cells uses the above energy bound.
   For each source, the two occupation energy indicators have uniformly
   bounded overlap, so `sum_{p,phi} E_{p phi}^{(b)}<=C_b`. Every parameter
   remains uniform in `M,A`; any finite species sum of budgets is bounded by
   a fixed constant.

2. **Direct-force table and its sums.** The two transport majorants for a
   pair are multiplied by `|c_ab|`. Both source-force majorants, the good
   field term and magnetic remainder, are multiplied by `|c_ab lambda_b|`.
   This follows from the actual source acceleration (5), including its sign
   before absolute values are taken. Field budgets `G_phi,F_phi` are exactly
   those for the common Maxwell field; finite overlap and positive energy
   still bound their sums. The near/far table is therefore multiplied only
   by fixed exterior constants. The scalar dyadic radius, angle and momentum
   sums do not contain an acceleration coefficient. Applying those sums
   specieswise and then summing the finite source set proves

   \[
   \mathcal B=P\sqrt I+(M+\sqrt A)IS(w),\qquad
   \int_J|K_a|\,dt\le C\sqrt w\,\mathcal B,\tag{A}
   \]

   and bounds the transport, magnetic remainder and remaining-sector good
   field terms by `C B`. `C` is uniform over all receiver species and
   independent of `M,A`. This is a proof transfer of the scalar estimates,
   rather than an application of a one-species solution theorem.

3. **Signed weighted formula and all derivative factors.** The physical
   pair multiplier `c_ab` is fixed and factors out of integration by parts.
   The derivative of a selected sum is canceled only within this same pair
   after its common physical multiplier is factored out. Source-cutoff
   derivatives have exactly `|c_ab lambda_b|` times the direct source-force
   majorants; geometric cutoff, time weight and initial-boundary terms have
   `|c_ab|` times the corresponding geometric majorants. Receiver terms and
   receiver-cutoff terms use
   `alpha_t=(I-alpha tensor alpha)K_a/q_X` and hence have `|c_ab|` times
   `f_b theta |K_a|/(wr phi^2)`. They acquire no new `lambda_a`. For the
   moving projector `Pi=w P_X/|V_a|`, direct differentiation gives
   `|Pi_t k|<=C theta |K_a|/(w phi)`. This again uses the full normalized
   `K_a`, without dividing by or multiplying by the charge. Labelwise
   integration and cone-tip removal use only compact classical bounds, and
   collision-label exclusion works specieswise. Such bounds justify the
   identities but are not put into the final uniform constants. The initial
   boundary cost is fixed data times the integral of the time weight and
   receives only the same fixed exterior `|c_ab|`.

4. **Direction-change argument, before enhanced occupation.** Use the same
   fixed narrow-sector selection `p theta sqrt(h)<=1`. At each complete
   first exit of chordal size `delta`, the signed bootstrap gives a minimum
   interval length `c ell`, where
   `ell=min[(w delta/(MP))^2,w delta/(A S(w))]`; it also bounds the endpoint
   ramps and gives `|int psi w xi_t|>=w delta/2`. This reasoning applies to
   any receiver species. Apply the weighted formula of item 3 to the full
   source sum. Its projected receiver/projector coefficient is at most
   `C L^2/w`, its weight coefficient at most `C L^2`, and (A) bounds the
   receiver cost by `C(M,A) w^{1/2}L^3`. Complementary-bin good field terms,
   source/spatial cutoffs and central terms have the same baseline occupation
   and geometric dyadic estimates as upstream, multiplied by fixed factors
   from items 1--3. They total at most `C(M,A)w L^6`; no enhanced occupation
   is used in this step. Summing the complete first exits yields

   \[
   \tfrac12 N_c w\delta\le C(M,A)wL^6+CL^2N_c.
   \]

   For `w>=P^{3/5}`, `w^{-3/5}<=delta<=w^{-1/10}`, the bound
   `w delta>=P^{6/25}` absorbs the last term at a threshold allowed to
   depend on the fixed species parameters and `M,A`. This proves the same
   direction count `N_c+1<=C(M,A)L^6/delta`, uniformly over all species.

5. **Enhanced occupation for a particular pair.** In the exact window
   `p,w>=P^{7/10}` and `j^{-49/100}<=phi<=j^{-4/25}` for `j=p,w`, put
   `I_m^0=(m/P)^2`, `Q_0=C_2(M^2+AL)`, `lambda_0=I_m^0/Q_0` with one common
   fixed `C_2`. The bootstrap stops source `b` and receiver `a` energies
   before their first exit from comparable ranges on an enlarged cell;
   (T) supplies both bounds. Direction partitions in item 4 apply to both
   species with `delta=c_2 phi`. Their common refinement has the sum of the
   two cell counts, rather than their product. Bad hits are within source
   time `C_T h` before a receiver direction boundary, and hence have duration
   at most `C(M,A)hL^6/phi`. At a good hit, `s,t` lie in one receiver
   direction cell and `|Y_b(s)-X_a(s)|<=Ch phi`. Each combined direction
   interval has a fixed relative-velocity projection at least `c phi`;
   its good-hit duration is at most `Ch`. The positive source energy bounds
   the common-cell label mass by `C_b/p`. Cell summation gives

   \[
   \mathsf M_b\le C(M,A)\frac hp\phi^{-1}L^7
        \max(1,I/I_m^0,h/I_m^0).
   \]

   In the stated window `phi<=P^{-14/125}`, so
   `phi^{-(29/25-1)}>=P^{56/3125}` absorbs the fixed `C(M,A)L^7`.
   Thus the final constant in enhanced occupation is independent of `M,A`,
   with a common threshold `P_*(M,A)` over finitely many pairs. This explicitly
   verifies that species-dependent direction constants do not leak into
   the selected-range exponent argument as bootstrap-dependent constants.

6. **Pure selection and the receiver coefficient.** Let `M_*` be the minimum
   of the applicable *exact representative quantities* in upstream
   `sel:pure`. Items 1 and 5 prove `M_b<=C_b M_*`. Choose the same fixed set
   of indices using `sel:selection`, and
   `W=(P theta)^{-epsilon}phi^epsilon h^epsilon`, `epsilon=10^{-5}`. The
   selection is independent of the trajectory variables subsequently
   differentiated. For a pair, density and positive cone flux give the
   receiver coefficient

   \[
   C_{ab}^{\rm data}U,\qquad
   U=w^{-1}\min[h^2(p\theta)^3,(p\theta h\phi^2)^{-1}].
   \]

   All `C_ab^data` are independent of `M,A,P`. The exact selection exponent
   argument uses only `M_*`, the common `lambda` and representative powers
   of `P`. Its contradiction therefore still proves
   `U<=w^{-1/2}W` for every selected index. Exterior species constants do
   not change that pure inequality, and need not be made small. Summing
   the finite source set and the summable weights gives coefficient
   `C w^{-1/2}`. Multiplying by (A) yields `C B`.

7. **Spatial transition and time weights.** For each source use
   `R_b=1+sqrt(I/lambda)sqrt(E_{p phi}^{(b)})`. Its budget is uniform and
   independent of `theta,h`. The spatial near/far bounds and the
   `h_0` crossing sum in upstream `sel:spatial-sum` are scalar; their
   `D_0=sqrt(I) R_b p phi` has the same theta independence. Pair prefactors
   multiply the estimates without changing the geometric sums or adding
   logarithms. Source derivatives on unselected neighbors have the
   coefficients in item 3; they are bounded by the direct table in item 2.
   The geometric residual uses the same `f_b/r^2` near/far estimates.
   For endpoint-zero time weights with ramps of length `eta I`, the
   `h<=I` and `h>I` estimates in `sel:time-weight` remain valid specieswise;
   their constants depend on `eta` and fixed species parameters only.
   Summing all sources proves the simultaneous weighted signed bound

   \[
   \left|\int_J\psi K_a\,dt\right|
     \le C_\eta[P\sqrt I+(M+\sqrt A)IS(w)].\tag{W}
   \]

This list accounts for every occurrence of an acceleration law in the
upstream proof. All other operations are scalar dyadic sums, strictly
timelike geometry, nonnegative energy/density estimates, or finite sums.
In particular it proves why fixed charge signs and fixed mass ratios
introduce no new exponent loss in this route.

It remains to remove the simultaneous bootstrap. Fix one common `C_eta`
covering every species. If `MP sqrt(I)+AI S(w)>=32w`, the endpoint energies
bound the increment by `16w`, giving an immediate strict improvement.
Otherwise `M>=32` implies `I<=(w/P)^2`, so (W) applies. Each removed endpoint
ramp is bounded by (T) on its own shortened interval, giving

\[
 |\Delta V_a|\le(C_\eta+2M\sqrt\eta)P\sqrt I
     +[C_\eta(M+\sqrt A)+2A\eta]IS(w).
\]

Choose `eta` with `2sqrt(eta)<=1/8`, `2eta<=1/8`, then
`M>=max(32,8C_eta)`, then
`A>=max(1,16C_eta M,256C_eta^2)`. The displayed estimate is at most one
quarter of the bootstrap bound. All threshold conditions can then be met
by one `P_0`, taking maxima over finitely many sources and receivers.

For this fixed `P`, define the set of `tau` where (T) holds for **all**
species, supported labels, dyads and eligible intervals in `[0,tau]`.
It is an initial interval and contains zero. If its increasing endpoints
approach `tau`, truncate any nontrivial eligible interval at those endpoints;
the range condition is preserved and continuity proves closedness. On the
fixed compact classical interval there is a common finite bound `C_*` for
the full `|K_a|` over the finite disjoint union of compact initial supports.
Thus some `ell_0>0` makes every interval of length at most `ell_0` satisfy
(T) directly. A longer eligible interval ending within `varepsilon` after
a bootstrap endpoint has a prefix satisfying the strict improvement and
a suffix bounded by `C_* varepsilon`. The full bootstrap bound is uniformly
at least `MP sqrt(ell_0)`, so choose a common `varepsilon` making the suffix
smaller than its remaining margin. An interval starting after the endpoint
is short. This proves relative openness and hence (T) throughout `[0,t_*]`.
`C_*` is used only in this continuity argument and never enters `M,A,P_0`.
∎

## Exact upstream analytic dependency table

The source root for every row is
`sources/upstream_pinned/preprints/Global-classical-solutions-of-the-three-dimensional-relativistic-Vlasov-Maxwell-system-September-23-2026/build/sections/`.
Hashes are recorded in the associated agent-note source manifest.

| Source and exact label | Needed statement | Changed hypotheses checked above |
|---|---|---|
| retarded.tex `ret:energy` | positive energy and cone flux | rederived with positive masses, signed work and source weights |
| retarded.tex `ret:phase-change`, `ret:receiver-time` | retarded phase and receiver Jacobians; null collision labels | specieswise phase preservation and strict timelikeness; no charge in determinant |
| retarded.tex `ret:representation`, `ret:direct-bounds` | field kernels and source pointwise majorants | Maxwell linear source `e_b`; actual acceleration `lambda_b`; receiver `lambda_a` |
| occupation.tex `occ:crude-lemma` | energy/time-change occupation | source nonnegative `f_b`; number and mass-weighted energy |
| occupation.tex `occ:cell-lemma` | stable-cell occupation | simultaneous source/receiver bootstrap, common normalized velocity law |
| occupation.tex `occ:refined-proposition` | joint-budget refined occupation | sourcewise indicators, bounded overlap and `H_0/m_b` |
| direct.tex `dir:direct` and proof tables `dir:near-far`, `dir:balanced` | baseline and full absolute-force estimates | only fixed pair coefficients in table; shared field budgets |
| cancellation.tex `can:identity` | exact signed kernel identity | proved afresh for arbitrary source/receiver accelerations |
| cancellation.tex `can:cutoff-cancellation` | selected derivative moved to unselected support | common fixed `c_ab` factored first; cancellation only within a pair |
| cancellation.tex `can:weighted-formula` | labelwise weighted integration by parts | sourcewise null collision set, same cone-tip estimates, fixed pair scalar |
| cancellation.tex `can:receiver-coefficient` | two-sided coefficient `C U` | source density and specieswise positive cone flux; normalized full `K_a` |
| direction.tex `ang:direction` | `C(M,A)L^6/delta` direction count | full source sum; baseline occupation only; species constants are fixed |
| direction.tex `ang:improved-hit` | `C h/p phi^{-29/25}` occupation in exact window | both direction counts uniform; source positive energy; fixed constants absorbed only into threshold |
| selection.tex `sel:weight-sum`, `sel:exponents` | weight summability and exact selected `U<=w^{-1/2}W` | unchanged pure representatives; all pair constants exterior and independent of `M,A` |
| selection.tex `sel:spatial-sum` | spatial transition without an extra logarithm | sourcewise joint budget; pure crossing calculation unchanged |
| selection.tex `sel:time-weight`, `sel:bulk-impulse` | endpoint-zero weighted impulse | finite sum of fixed factors; common `C_eta` |
| closure.tex `eq:closure-improvement`, continuity proof | strict improvement and bootstrap removal | universal quantification over finite species; compact union and common force bound |

The local existence/continuation theorem is a separate dependency. The
lemma proves (T) on already-existing compact classical intervals. If that
exact multispecies continuation theorem is established, the usual first
doubling of `Q(t)=max_{a,z}q(V_a(t,z))` excludes finite-time breakdown with
the same shared constants. This lemma does not independently establish
the cited continuation theorem or the public priority of the result.
