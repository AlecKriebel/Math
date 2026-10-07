# Uniform finite-species occupation-to-closure lemma chain

Prepared 2026-10-07T04:26:50Z. This supplements `SUPPLEMENT_OCCUPATION_AUDIT.md`. It proves the
uniformity and coupled quantifiers of the occupation-to-closure mechanism,
conditional only on the stated pointwise pair force identities/majorants and
on the classical solution/positive-energy inputs. It is not a citation to or
application of a completed one-species global theorem.

Throughout, the number of species `N` and masses `m_b>0`, charges `e_b` are
fixed. Normalize physical momentum by `W_b=p_b/m_b` and density by
`g_b=m_b^3 f_b(x,m_b W_b)`. Write `c_b=e_b/m_b`, `q=sqrt(1+|W|^2)` and `u=W/q`.
Fix a finite horizon `T0` and a compact classical interval `[0,t*]`.

## Exact input and constants

For every species, the flow preserves phase volume and transports its own
initial density. The positive energy and cone energy inputs are

\[
 \tfrac12\int(|E|^2+|B|^2)+\sum_bm_b\int qg_b=\mathcal H_0,
\]

\[
 \int_0^t\!\int_{S^2}r^2\left[G^2+
        \sum_bm_b\int qd\,g_b\,dW\right]dn\,ds\le C\mathcal H_0,
 \quad d=1-n\cdot u,
 \quad G=|E+n\times B|+|n\cdot B|.
\]

For a receiver of species `a`, put `a=u(W_a)`, `D=1-n.a`, `e=1-a.u`,
`K_a=W_a'`, `Q=D I+n tensor a`, `H=Q/D`, `k0=u-ne/D`. For each source species
`b`, assume the exact retarded force formula and signed identity

\[
 K_{ab}^{\rm lab}=c_ae_b\left[
 -\left(\frac{k_0}{rd}\right)' +
 \frac{e}{r^2D^2}\left(\frac{n}{q_a^2D}-a\right)
 +\frac{n(a_t\cdot k_0)}{rD^2}\right],
 \qquad a_t=q_a^{-1}(I-a\otimes a)K_a.
\]

Here prime is source time along its retarded branch; source acceleration is
`u_b'=c_b q_b^(-1)(I-u_b tensor u_b)(E+u_b x B)`. All initial boundary and
free-field contributions have bounded data cost, uniformly for supported
receivers on the fixed horizon. The source and transport pointwise majorants
are the family 362 ones, multiplied by `|c_a e_b|` for transport and by
`|c_a e_b c_b|` for source-field terms. Their projected versions have the extra
small-sector factor `phi`. The derivative versions are the same factors times
the bounds in cancellation.tex:196--267. These pointwise facts are the explicit
input needing independent verification in the paired-kernel audit.

Define the positive ensemble density and its budgets by

\[
 F=\sum_b g_b,\quad L_\infty=\sum_b\|g_{b,0}\|_\infty,\quad
 E_* =\mathcal H_0\sum_b m_b^{-1},\quad
 \Gamma=\max\left(1,\max_{a,b}|c_ae_b|,
                  \max_{a,b}|c_ae_bc_b|\right).
\]

Then `F<=L_infinity`, `integral qF<=E_*`. For every receiver, the sum of
absolute pairwise majorants is at most `Gamma` times the corresponding
unweighted `F` majorant. All subsequent constants may depend on
`N,{m_b,e_b}, H0,L_infinity,T0` and fixed partition parameters. They never
depend on `t*,P,M,A`; constants displayed as `C(M,A)` have that expressly
allowed bootstrap dependence. There is no assertion that `F` obeys one
Vlasov equation. Every argument involving flows is performed on the disjoint
union of species label spaces and then summed.

Assume one simultaneous bootstrap on `[0,tau]`:

\[
 |W_a(t_2)-W_a(t_1)|\le MP\sqrt{t_2-t_1}
       +A(t_2-t_1)\frac{P^2L}{w},\quad L=\log(2+P),
\]

for every supported label of every species, every receiver scale, and every
interval on which `q_a` remains in `[w/8,8w]`. Let
`P>=1024 max_{a,z,t<=t*} q(W_a(t,z))` be dyadic. All source and receiver
momentum scales are at most `P`.

## Lemma 1: ensemble occupation and shared angular energy

For a fixed receiver and any eligible measurable receiver times inside one
interval `J` of length at most `I<=(w/P)^2`, let `M_b` be the source occupation
measure from species `b`, and let `M=sum_b M_b`. Put `m=min(p,w)`, and set

\[
 \lambda^{-1/2}=C_1\frac Pm
      \left(\frac M\omega+\sqrt{\frac{AL}\omega}\right).
\]

Here the `M` in the stability length is the bootstrap constant; the occupation
measure is always written `mathsf M` in equations below. In the small sector
`theta<kappa phi`, take `omega=phi,k1=1,nu=theta`; in the remaining sector
take `omega=sigma,k1=1+phi/sigma,nu=min(theta,sigma)`.

Then

\[
 \mathsf M\le C\max(I,h)/p,\qquad
 \mathsf M\le CI\phi^2/\theta^2,
\]

and actual bins `omega>C0/m` satisfy

\[
 \mathsf M\le C(hk_1/p)\max(1,I/\lambda,h/\lambda).
\]

For the small sector there are nonnegative angular budgets `E_{p,phi}` with
`sum_{p,phi} E_{p,phi}<=C`, such that outside deficit bins
`omega<=C0/m, h<=min(I,lambda)` one has

\[
 \mathsf M\le C(hk_1/p)R^2,
 \quad R=1+\sqrt{I/\lambda}\sqrt{\mathcal E},\quad
 \mathcal E=\begin{cases}E_{p,\phi}&\text{small sector},\\1&\text{remaining}.
 \end{cases}
\]

Proof. For each species, `(t,n)->X_a(t)-(t-s)n` has injective Jacobian `r²D`,
and its own phase-flow change has determinant one. On the disjoint label
union, the label mass at any common time for a source shell is bounded by
`C E_*/p`, exactly as for one positive density. The time-change `ds/dt=D/d`
gives the second crude bound using total ensemble mass. The simultaneous
bootstrap gives `|Delta W|<=epsilon m omega` and `|Delta u|<=epsilon omega`
on source and receiver cells of size `C*lambda`, with one fixed `C1`.
Monotone projected equal-time separation gives residence at most `Chk1`
for each component label, while mass per cell is at most `C/p`. Summing cells
proves the actual-bin estimate.

Use the upstream two indicators `H1,H2` with the fixed receiver but integrate
`qF(H1+H2)` over `J*` and divide by `I`. At any phase point the count over
`p,phi` is bounded, so their sum is at most `C E_* |J*|/I<=C`. Labels hitting
a stable cell remain in `H1` throughout that cell, source by source; summing
their cell averages gives the same refined bound. For `lambda<h<=I`, the
injective spatial map puts each hit into `H2` and bounds its mass by
`(CI/p)E_{p,phi}`. For `h>I`, crude energy gives `Ch/p`. All constants are
independent of bootstrap parameters. No new species count is incurred in a
dyadic sum because the species sum has already been included in `F` and `E_*`.

## Lemma 2: shared field budgets and direct bounds

For this fixed receiver define

\[
 \mathcal G_\phi=I^{-1}\int_{\rm eligible}dt\int_0^t ds\int dn\,
        r^2\chi_\phi G^2,
\]

and define `F_phi` by the upstream unique-retarded-time spatial indicator,
integrating `|B|²` on `J*` and dividing by `I`. Both satisfy
`sum_phi G_phi<=C`, `sum_phi F_phi<=C`. They depend on the receiver, interval,
and upper length, and **not** on source species or on `p,theta,sigma,h`.

Proof. Backward-cone field energy and bounded angular overlap prove the first
bound. Conserved field energy and `|J*|<=CI` prove the second. Existence and
uniqueness of the retarded time follow solely from the timelike receiver.
The Jacobian `r²D` gives
`integral_bin r²phi²|B|²<=C(I+h)Fcal`, with `Fcal=F_phi` for `h<=I`, otherwise
`1`. These budgets are common to the entire ensemble before any source sum.

Let `N=integral_bin F dW`. The density cap, support area, and occupation give

\[
 N\le Cp^3\nu^2,\quad
 \int1\le CIh\phi^2,\quad
 \int N^2\le C\min(Ih\phi^2p^6\nu^4,
                   p^3\nu^2\mathsf M/(h^2\phi^2)).
\]

Consequently the near/far table in direct.tex:115--128 holds verbatim with
`F,N,mathsf M` and one fixed extra constant `Gamma`. This follows directly
by applying Cauchy--Schwarz to `rGN` or `r phi |B| N`; one must aggregate the
nonnegative source density **before** that step. In particular it is not
necessary to spend a separate field budget for every source species.

Substituting Lemma 1 and summing radial dyads yields

\[
 T_\perp:\ C\sqrt I\,Rp^{-1}\theta^{-3}\nu\phi\sqrt{k_1},
\]

\[
 S_g:\ CI^{3/4}R^{1/2}p\phi\nu^{3/2}\theta^{-2}k_1^{1/4}
                      \sqrt{\mathcal G_\phi},\qquad
 S_b(h\le I):\ CI^{3/4}R^{1/2}p\nu^{3/2}k_1^{1/4}\sqrt{\mathcal F_\phi}.
\]

For `h>I`, crude time occupation yields a radial sum at most
`C sqrt(I) p nu^(4/3) theta^(-2/3) phi^(1/3)`. The deficit exception uses
near bounds with `h<=C/P²`. Summing it gives at most `CI S(w)` for sufficiently
large `P`, independent of `M,A` because `M,A>=1` were used to weaken lambda.

The angular sums are identical scalar geometric sums to direct.tex:286--419,
now with the aggregate `E_{p,phi}`. The essential small-sector term is

\[
 \sum_{p,\phi}C\sqrt I Rp\phi
 \le CP\sqrt I+C(M+\sqrt A)IP^2L/w.
\]

Indeed, expanding `R-1` gives the `M` contribution
`CIM P sum (p/m) sqrt(E)` and the square-root-`A` contribution
`CI sqrt(AL) P sum (p/m) sqrt(phi E)`. Their Cauchy--Schwarz squared weights
are bounded respectively by `C[L²+L(P/w)²]` and `C[L+(P/w)²]`. The common
aggregate angular budget therefore prevents an extra angular logarithm.
Remaining-sector and magnetic terms use the displayed common field budgets
and the geometric factors specified in direct.tex:317--390. This gives

\[
 \int(T_r+T_\perp+S_b+S_g^{\rm remaining}+\text{data})
       \le C\mathcal B(I,w),
 \quad \mathcal B=P\sqrt I+(M+\sqrt A)IS(w),
\]

and including small-sector `S_g` gives
`integral_eligible |K_a|<=C sqrt(w) B(I,w)`. The constant is uniform in the
receiver species, since the finite maximum `Gamma` was fixed beforehand.

## Lemma 3: all species direction counts and enhanced occupation

For any receiver species, `w>=P^(3/5)`, an interval of length at most
`(w/P)²` with receiver energy in `[w/8,8w]`, and
`w^(-3/5)<=delta<=w^(-1/10)`, the first-exit direction partition has at most
`C(M,A)L^6/delta` intervals.

Proof. Momentum normalization and the simultaneous bootstrap make each
complete first exit last at least
`c min((w delta/(MP))²,w delta/(A S(w)))`. Insert an endpoint-zero weight on
each complete interval, retaining a signed direction increment at least
`w delta/2`. Apply the exact pairwise weighted identity to every source with
the **same** fixed index selection `theta<kappa phi, p theta sqrt(h)<=1`, then
sum over sources. Disjoint weights share one upper length `I=(w/P)²` for all
bulk estimates, by Lemmas 1--2. Projected receiver and moving-projector
coefficients are at most `CL²/w`; their cost is `C(M,A) sqrt(w)L³`.
Weight derivatives cost `CL² N_c`. All other bulk terms are bounded by
`C(M,A)wL^6`: they use baseline occupation `R=1+sqrt(I/lambda)` and
`sqrt(I) R p phi<=C(M,A)w sqrt(L)`, not enhanced occupation. Summing first
exits gives

\[
 N_cw\delta/2\le C(M,A)wL^6+CL^2N_c.
\]

For sufficiently large `P`, `w delta>=P^(6/25)` absorbs the last term. The
same uniform constant applies to every source species when that species is
itself used as a receiver. Thus there is no missing source direction bound.

In the window `p,w>=P^.7` and `j^(-.49)<=phi<=j^(-.16)` for `j=p,w`, the
enhanced occupation is

\[
 \mathsf M\le C(h/p)\phi^{-29/25}
               \max(1,I/I_m^0,h/I_m^0),\quad I_m^0=(m/P)^2,
\]

with `C` independent of `M,A`. To see this without losing uniformity, let
`Q0=C2(M²+AL)` and `lambda0=I_m^0/Q0`. For `h>lambda0`, crude energy suffices
once `phi^(-29/25)>=Q0`. For `h<=lambda0`, the simultaneous bootstrap keeps
source/receiver energies comparable on each source cell and its receiver
extension. Lemma 3, with `delta=c2 phi`, applies to all those trajectories.
Bad hits cross a receiver direction boundary, giving duration `O(h)` per
boundary. On each common source/receiver direction refinement interval,
good hits have same-time separation `O(h phi)` and projected relative speed
at least `c phi`, so duration `O(h)`. The refinement number is at most the
sum of partition counts. Each source component's hit labels have mass at
most `C/p` at a common time; summing the positive ensemble preserves this
bound. Thus occupation is at most

\[
 C(M,A)(h/p)\phi^{-1}L^7\max(1,I/I_m^0,h/I_m^0).
\]

The window gives `phi^(-4/25)>=P^(56/3125)`, which absorbs the fixed
`C(M,A)L^7` above the threshold `P_*(M,A)`. The remaining prefactor is
independent of `M,A`. There is no reversal of this dependency order.

## Lemma 4: selected coefficients and every derivative error

Define `mathsf M_*` by the upstream exact three-entry table, using baseline
and enhanced occupation above. Then `mathsf M<=C mathsf M_*`, with `C`
independent of bootstrap constants after the threshold. Choose
`epsilon=10^(-5)` and `W=(P theta)^(-epsilon)phi^epsilon h^epsilon`. The
indices satisfying

\[
 \min\{I\sqrt h p^2\phi^2,
          \sqrt I\sqrt{p\mathsf M_*}/(\theta h)\}>P\sqrt I W
\]

are fixed throughout the interval and used for **every** source species.
The representative coefficient

\[
 U=w^{-1}\min\{h^2(p\theta)^3,(p\theta h\phi^2)^{-1}\}
\]

satisfies `U<=w^(-1/2)W` on selected indices for `P>=P_*(M,A)`. The proof is
exactly the rational contradiction fully recorded in `SUPPLEMENT_OCCUPATION_AUDIT.md`; the executable
certificate verifies its strict final margin. Its hypotheses depend on
representative powers, not on species constants.

At a fixed receiver time, summing the paired receiver residuals and
receiver-cutoff derivatives is at most `C U |K_a|`. This follows from the
aggregate density estimate or aggregate positive cone-particle flux. Therefore
its selected sum is at most `C w^(-1/2)|K_a|`, since `sum W<=C`. Lemma 2 then
bounds its integrated cost by `C B(I,w)`. The factor `C` already contains every
`|c_a e_b|`; no contraction is required from charge size.

For source derivative errors, the derivative of a selected sum can be assigned
to overlapping unselected indicators separately for each species, because
`sum beta_j=1` is an identity in its own normalized state variables. The
physical multiplier `c_a e_b g_b D k0/(rd)` is common before cancellation and
is not differentiated. Source logarithmic rates are bounded by
`C|c_b| p^(-1)(G/theta+theta|B|)`. Thus, after summing source species, their
error majorants are at most `C` times the **same** direct good-field and
magnetic terms in Lemma 2, with aggregate density `F`. On unselected small
neighbors the good-field term costs `CP sqrt(I) W`; magnetic and structural
neighbors cost `C B(I,w)`.

Spatial derivative errors have near/far minimum
`C min(I h p³ theta phi³, R²/(p h theta phi))`, with `R` independent of
`theta,h`. The transition `h0` solving near equality gives
`n0 f*=I R²p²phi²`; sum over radius with the extra far-selection bound costs
`C D0 min(x^((1-2epsilon)/(1+2epsilon)),x^(-1))`, where
`D0=sqrt(I) R p phi`, `x=n0/D0` and `n0` is a strictly increasing geometric
power of `theta`. Both angular tails sum geometrically to `C D0`. Lemma 2's
shared angular budget then costs `C B(I,w)`. The exceptional deficit near
terms have `h<=C/P²` and fit `CI S(w)` directly. This treats the spatial
derivatives without spending a separate source budget or time-piece count.

The central residual has `F/r²` majorant and radius/angle balance
`C sqrt(I) R p theta`, summing to `C D0`; hence it has the same bound.
Time-weight derivatives for an endpoint ramp fraction `eta` have majorant
`C_eta F theta/(I r phi)`. For `h<=I` this is bounded by a constant times the
central residual. For `h>I`, selection bounds the normalized near cost by
`C_eta h(p/P)^5 phi³ W^(-4)`, whose theta sum has positive radial and angular
exponents `1-6epsilon/(1-epsilon)` and `3-4epsilon/(1-epsilon)`; all remaining
sums are geometric. Initial-cone terms cost `CI`; free data also cost `CI`.
Thus, for the endpoint-zero ramp weight,

\[
 \left|\int_J\psi K_a\right|
       \le C_\eta[P\sqrt I+(M+\sqrt A)IS(w)],
\]

where `C_eta` is independent of `M,A`, uniform in species, endpoints, and
`P` above the threshold. The potentially bootstrap-dependent constants from
Lemma 3 were removed by its positive-power absorption **before** this step.

## Lemma 5: simultaneous bootstrap removal and momentum doubling

Take `eta` with `2sqrt(eta),2eta<=1/8`, then
`M>=max(32,8C_eta)`, then `A>=max(1,16C_eta M,256C_eta²)`, finally one threshold
`P0` satisfying every preceding fixed-parameter threshold. This order makes
every choice independent of the compact endpoint `t*`.

If `B_w(I)=MP sqrt(I)+AI S(w)>=32w`, the receiver's endpoint momenta already
give `|Delta W_a|<=16w<=B_w(I)/2`. Otherwise `I<=(w/P)²`. Restore the two edge
weights using signed receiver increments, obtaining

\[
 |\Delta W_a|\le(C_\eta+2M\sqrt\eta)P\sqrt I+
    [C_\eta(M+\sqrt A)+2A\eta]IS(w)\le B_w(I)/2.
\]

This holds for all supported species receivers at once. Define `T` as the
set of endpoints where the simultaneous bootstrap holds on every eligible
interval. It contains zero, is an initial interval, and is closed by
truncation. On the fixed compact solution interval, the full forces `K_a`
are uniformly bounded across the finite species set and compact source
labels. This temporary bound makes all sufficiently short intervals obey
the bootstrap. At any endpoint in `T`, the strict half-bound on prefixes
leaves a uniform positive margin for every longer crossing interval; the
bounded short suffix fits that margin. Thus `T` is relatively open and
equals `[0,t*]`. The temporary compact force bound affects only the openness
argument, not `M,A,P0`.

The union of initial label supports is compact and finite, so
`Q(t)=max_{a,z} q(W_a(t,z))` is continuous. At its first hit `t_n` of `2^n`,
choose any attaining species-label and its last half-energy time `s_n`.
One has `s_n>=t_(n-1)` even when successive maxima are attained by different
species. Its energy stays in `[2^(n-1),2^n]` on `[s_n,t_n]`. Taking
`P=1024*2^n,w=2^n` gives

\[
 t_n-t_{n-1}\ge t_n-s_n\ge c/\log(2+1024\cdot2^n).
\]

The sum diverges. Therefore a classical solution meeting the exact input
cannot suffer finite-time momentum blowup. For fixed positive masses,
bounded normalized momentum and bounded physical momentum are equivalent.
Applying an independently verified matching continuation theorem then gives
global existence in its exact data class.

## Scope and outstanding input

Opposite charge signs, repeated species, and zero charges are included: signs
are retained in the exact pair formulas and bounded only after integration;
zero-charge receivers have constant normalized momentum and zero-charge
sources have zero field contribution. Every mass may be arbitrarily small
but positive and fixed; constants need not be uniform as a mass tends to zero.
No neutrality, tail, collision, curved-spacetime, or massless extension is used.

The proof above shows that a valid paired geometric identity/majorant package
does close the finite-species bootstrap; it does not replace that package with
the statement of the one-species theorem. The remaining independent input is
exact kernel and boundary verification, energy/constraints, and local/
continuation theory. Neither this file nor the arithmetic certificate is a
claim of full Lean formalization or a complete preprint-priority audit.
