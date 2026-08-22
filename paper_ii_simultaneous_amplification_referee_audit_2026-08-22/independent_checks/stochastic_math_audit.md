# Independent stochastic-mathematics audit

**Checkpoint:** 2026-08-22T12:41:10-07:00
**Assigned-scope completion:** **100%**
**Component assessment:** The load-bearing stochastic argument is supported **after one minor mathematical correction** to an unstopped pendant hitting-time display. I found no major gap, counterexample to the theorem, fitness-dependent choice, illicit limit exchange, or independent-lineage substitution in the assigned scope.

## Scope and evidence standard

I read `main.tex` in full, treating its comments, prior logs, verifier claims, and conclusions as claims rather than evidence. I independently checked:

- the Bd and dB kernels and complete-graph baselines;
- the graph construction and effective weak-edge diagonal;
- arbitrary-size strong orbit lumping;
- the finite-state weak-cut Schur complement, its orientation, and compact-uniform convergence;
- all center intensity tables, establishment and confinement scales, Bd and dB cleanup, and pendant initialization;
- the reciprocal killed-Green and hub-excursion arguments;
- the four module-introduction rates, adverse center reversals, and global sweep;
- the interface from those results to the response functions and the final pointwise-in-fitness diagonal.

The independent script `independent_checks/stochastic_math/audit_small_chains.py` imports no manuscript or certificate code. It constructs labelled chains directly from the update rules using only the Python standard library. Its final run, command label `agent-stoch-rerun-small-chains`, exited 0. The finite checks are corroboration only; the arbitrary-size and asymptotic conclusions below rest on re-derivation.

## Finding

### S-M1 — Minor mathematical correction: two pendant waiting-time expectations omit the necessary core-exit stop

**Location.** Lemma 6 (`lem:pendant-cleanup`), `main.tex` lines 728–755, especially

- the claimed conditional bound on successive pendant-count changes at lines 743–747 (`eq:leaf-wait`), and
- the unconditional display
  `sup_{R<=2 delta c} E tau_{ell=m}=O(Cm)` at lines 749–755 (`eq:leaf-hitting-time`, equation (26) in the PDF).

**Exact defect.** With the usual convention `inf(empty set)=infinity`, these expectations are not finite as written. From a nonabsorbing high-core state there is a strictly positive finite-`C` probability that the core exits the strip and the process subsequently reaches global extinction before another pendant gain, or before ever reaching `ell=m`. At global extinction no later pendant-count change occurs and `ell=m` is never hit. For example, take `R=1`, resident hub, and `ell=0`; a finite sequence of resident replacement events leading to extinction has positive probability under either finite positive-fitness chain. Thus `tau_{ell=m}=infinity` on a positive-probability event and its unconditional expectation is infinite. The same issue can make `sigma_{j+1}-sigma_j` infinite once the embedded pendant trace is at `ell=0`.

**Minimal rigorous repair.** Let

\[
 \tau_\uparrow=\inf\{s:R_s\ge 2\delta c\},\qquad
 \Sigma=\inf\{s:(h_s,\ell_s)=(1,m)\text{ or }R_s\ge2\delta c\}.
\]

Replace `eq:leaf-wait` by the conditional mean time to the next pendant-count change **or** `tau_up`, and replace equation (26) by

\[
 \sup_{R\le\delta c}\mathbb E\Sigma=O(Cm)
\]

(the same estimate is valid from any state with `R<2 delta c`, with constants adjusted at the strip edge).

Here is a direct proof using the manuscript's preceding calculations.

1. For `1<=ell<m`, retain the worst-rate two-state committor at lines 694–715, but assign value one to an upper-strip exit. A core jump that exits then contributes `rate*(1-p_h)>=0` to the generator, so the same subharmonic argument gives
   \[
   \frac{\Pr(\text{leaf up or exit before leaf down})}
        {\Pr(\text{leaf down first})}\ge\beta>1.
   \]
   At `ell=0`, a down change is impossible.
2. At each resulting outcome, set the level equal to `m` if an exit occurs. Before absorption, the conditional expected level increment is at least
   `delta_beta=(beta-1)/(beta+1)>0`. Optional stopping of the truncated adapted walk therefore gives at most `m/delta_beta=O(m)` actual pendant-count changes before reaching `ell=m` or exiting. No Markov or independence assumption for the hidden core coordinates is needed.
3. Stop each hub phase also at `tau_up`. Adding exit as a terminal outcome can only shorten a phase. The rate bounds at lines 728–742 still give a compact-uniform `O(C)` conditional mean time to the next pendant change or exit: each phase has bounded mean duration and has probability at least `c_0/C` of a pendant outcome (with exit counted as terminal).
4. If a block starts at `(h,ell)=(0,m)`, which is the only case not captured by “first hit of `ell=m`,” activation, pendant loss, or exit occurs in bounded mean time. Activation or exit terminates `Sigma`; a loss restarts the preceding estimate from `m-1`. If `ell` reaches `m` through an upward pendant event, the hub is mutant at that same event, so the target is automatically `(h,ell)=(1,m)`. Consequently the stronger `E(Sigma-S_j | F_{S_j})=O(Cm)` asserted later at lines 802–809 is valid.

**Propagation audit.** Every later use needs only this stopped form:

- Lines 782–785: Markov gives `Pr(Sigma>C^2)=O(m/C)=o(1)` because `m=o(C)`; a hit of the upper strip is separately charged using `eq:core-confinement`.
- Lines 802–809: `Sigma_j` is already defined as the hit of `(1,m)` **or** `R>=2 delta c`; the repaired estimate proves exactly the stated conditional mean.
- Lines 824–838: the block success, escape, and duration inequalities already charge upper-strip escape separately.
- Lines 840–854: the conditional `O(Cm)` synchronization mean and the geometric strong-Markov recursion remain unchanged.

The correction changes neither an asymptotic rate nor the theorem. It is a genuine mathematical correction, not merely stylistic, because the two original expectations can equal infinity.

**Adversarial search for analogous defects.** I searched every occurrence of an expectation, mean duration, and hitting time in the stochastic proof. The other displayed expectations are already stopped at finite boundaries or horizons: the early walk at `{0,K}` (lines 527–542), the deficit excursions (lines 617–658 and 766–780), the Bd trial at `{0,K}` (lines 911–918), the killed-Green chain at `{0,ceil(delta c)}` (lines 934–995), and the finite-horizon/pure-death integrals (lines 1049–1088). I found no second independent unstopped-hitting defect; the phase statement and equations at lines 728–755 are one local stopping-omission family.

## Verification ledger

### 1. Model transitions and complete-graph baselines — verified

**References.** `main.tex` lines 141–189; transition equations at lines 154–170.

For Bd, after suppressing the common factor `F(S)`, a labelled mutant parent `u` replaces resident `v` at rate `r w_uv/d_u`; the reverse event has rate `w_uv/d_u`. Summing labelled events gives exactly the two displayed formulas. For dB, conditioning on the uniformly selected target `v` gives mutant-parent weight

\[
 \frac{r\sum_{u\in S}w_{uv}}
 {r\sum_{u\in S}w_{uv}+\sum_{u\notin S}w_{uv}},
\]

and its resident analogue, again exactly as displayed. Denominators are positive because each vertex has positive weighted degree and `r>0`.

On `K_n`, the Bd count-chain down/up ratio is `1/r`, giving
`(1-r^{-1})/(1-r^{-n})`. For dB, if the mutant count is `i`,

\[
 q_i^+=\frac{n-i}{n}\frac{ri}{ri+n-i-1},\qquad
 q_i^-=\frac{i}{n}\frac{n-i}{r(i-1)+n-i},
\]

so

\[
 \frac{q_i^-}{q_i^+}
 =\frac1r\frac{n-1+(r-1)i}{n-r+(r-1)i}.
\]

The product telescopes through the adjacent affine factors and the standard birth–death product formula gives

\[
 \rho_{\rm dB}(K_n,r)=\frac{n-1}{n}
 \frac{1-r^{-1}}{1-r^{-(n-1)}}.
\]

The independent labelled solver reproduced both formulas for `n=2,...,7` at `r=3/2`. The special boundary case `n=2` correctly gives dB singleton fixation `1/2`, independent of fitness.

### 2. Quantifiers and graph construction — verified

**References.** Definition 1, lines 191–199; construction, lines 201–299; effective diagonal Lemma 2, lines 294–322; main theorem, lines 324–336.

For every `t>=2`, the graph is finite and loopless. Unit clique and pendant edges, pair weight `W_t=C_t/sigma_*`, and weak weight `2^{-e_t}` are all strictly positive; symmetry makes the graph undirected, and the complete satellite–clique weak cut makes it connected. The scales are

\[
 C=t^4,\quad q=t=C^{1/4},\quad m=\lfloor\lambda_*t\rfloor,
 \quad q/C=C^{-3/4}.
\]

`sigma_*` and `lambda_*` are fixed algebraic constants; no weight uses subsequently quantified fitness.

For fixed `t`, all first-step systems are finite with entries in `K(r)`, `K=Q(R_hyb)`. On `I_t`, transient blocks are substochastic with spectral radius below one, hence `I-Q` is a nonsingular M-matrix with positive determinant. After clearing positive event and harmonic-system denominators, the absolute-value condition is a finite universal real-algebraic statement on an algebraic compact interval, so exact real quantifier elimination decides each candidate exponent. Fixed-`t` weak-cut convergence guarantees that some dyadic candidate works; sequential testing therefore terminates.

There is no hidden uniform-in-`t` claim here: uniformity is needed only over `r in I_t` for each fixed finite `t`. The later population limit fixes `r>1` first. This distinction makes the diagonal valid even though `I_t` expands toward `r=1`.

### 3. Arbitrary-size strong lumpability — verified

**References.** Lemma 4, lines 341–366.

The action
`S_{C-1} x (S_2 wr S_q) x S_m` consists of graph automorphisms: it permutes ordinary clique vertices, permutes pairs and swaps endpoints within each pair, and permutes leaves. It is transitive on every fibre `(h,i,u,v,ell)`. Both update kernels are equivariant under this action because an automorphism preserves edge weights, degrees, mutant count, and type-dependent fitness. Therefore, for configurations `S,S'` in one fibre and any target fibre `F`, choose an automorphism `g` with `gS=S'`; then

\[
 \sum_{T\in F}P(S,T)
 =\sum_{T\in F}P(gS,gT)
 =\sum_{T\in F}P(S',T).
\]

This proves strong lumpability for every finite `C,m,q`, every positive weak weight, and both updates. The independent exact-rational enumeration also found identical aggregated generator rows on all 108 fibres of a 512-state instance for Bd and dB; that finite test corroborates but is not used to generalize the proof.

### 4. Zero-cut fast states and Schur complement — verified

**References.** Proposition 5, lines 368–440; `eq:finite-trace` and `eq:schur-trace`.

At zero cut, the connected center and each positive-weight pair evolve internally. A mixed finite module reaches one of its two homogeneous states almost surely. Thus the only closed fast classes are states with homogeneous center and homogeneous pairs, while every state in `F` is transient; in particular `rho(Q_0)<1`.

With row-oriented first-step matrices and state order `(M,F)`, the harmonic equations give

\[
 h_F=(I-P_{FF})^{-1}P_{FM}h_M,
\]

and hence

\[
 [I-P_{MM}-P_{MF}(I-P_{FF})^{-1}P_{FM}]h_M=0.
\]

Using
`P_MM=I+eps A+O(eps^2)`, `P_MF=eps B+O(eps^2)`,
`P_FM=C_0+O(eps)`, and `P_FF=Q_0+O(eps)` and dividing by `-eps` gives exactly

\[
 [A+B(I-Q_0)^{-1}C_0]h_M=0.
\]

Thus the sign and orientation in `eq:schur-trace` are correct. The inverse is the exact distribution of the first monomorphic return after one introduction; it does not assume independent descendants or replace local absorption with a branching probability.

For fixed `C,m,q`, all matrices depend continuously and rationally on `(eps,r)`. On a compact positive-fitness interval, the spectral gap of `Q_0`, the inverse of the interior macro generator, and nearby absorbing inverses have finite uniform bounds. This proves compact-uniform convergence. A direct six-vertex calculation independently showed convergence of the positive-cut fixation probability to the separated trace under both rules; at weak weights `10^{-1},...,10^{-4}`, the final absolute errors were `4.77e-6` (Bd) and `5.99e-7` (dB).

### 5. Center intensity tables and early establishment — verified

**References.** Proposition 6, lines 443–466; tables at lines 473–494; Lemma 7, lines 499–543.

Direct labelled-event summation reproduces all twelve changing intensities. Representative checks are:

- Bd ordinary gain: `r(c-i){h/d+i/c}` for each resident ordinary target, summed over `c-i` targets;
- Bd hub activation: `r(i/c+ell)` from ordinary and leaf parents;
- dB ordinary loss: after an ordinary mutant dies, resident neighbor weight is `c-i+1-h` and total fitness-weighted neighbor weight is `c+(r-1)(i-1+h)`;
- dB leaves copy their sole hub neighbor, yielding rates `h(m-ell)` and `(1-h)ell` in the death-clock scaling.

The independent exact-rational enumeration matched every aggregate table entry on all 256 states of a `C=5,m=3` center for both updates.

Before a hub change, `h=ell=0`. The displayed ordinary up/down odds follow exactly. For `i<K=A_0 log C`, inverse odds satisfy

\[
 \lambda_i=r^{-1}(1+O(K/C)).
\]

The embedded walk has compact-uniform positive drift, so its expected number of changes before `{0,K}` is `O(K)`. The hub hazard relative to ordinary-changing hazard is `O(K/C)` on this range; the manuscript's `O(K^2/C)` union bound is conservative and valid. The product-odds formula then gives

\[
 \Pr_1(\tau_K<\tau_0)=1-r^{-1}+O(K^2/C)+O(r^{-K}).
\]

Choosing `A_0` from the lower endpoint of a fixed fitness compact makes both exponential-in-`K` errors `o(C^{-3/4})`, while `K^2/C=o(C^{-3/4})`.

### 6. Core completion and confinement — verified

**References.** Lemma 8, lines 544–660; `eq:core-confinement`, `eq:deficit-return`.

For `K<=i<=(1-delta)c`, the conditional ordinary up/down odds have a compact-uniform lower bound `r_0>1`, even after conditioning on the complete hidden-coordinate history. Applying the bound at ordinary-count change epochs makes `r_0^{-i_n}` a supermartingale and yields the stated `O(r_0^{-K})` failure scale.

In the high-core strip, the inward/outward deficit odds dominate `alpha R/(R+1)`. Above the fixed boundary layer `R_0`, an exponential function of the stopped deficit is a supermartingale. Starting below `delta c`, the probability of an excursion to `2 delta c` before returning to the boundary layer is `exp(-Theta(C))`. The total deficit-changing compensator through time `C^M` is `O(C^{M+1})`, so the union/strong-Markov estimate in `eq:core-confinement` has exactly the displayed polynomial prefactor.

The continuous-time generator satisfies `G R<=-kappa R` between the fixed boundary layer and the upper strip. Stopping at the two boundaries makes `exp(kappa t)R_t` a supermartingale and gives the exponential return-time tail. No assertion is required inside `R<=R_0`, and the proof correctly says so.

### 7. Cleanup and pendant initialization — verified after S-M1

**References.** Lemma 9, lines 662–932; Bd cleanup lines 680–859; dB cleanup lines 861–895; initialization lines 897–931.

For Bd, solving the two hub-phase renewal equations gives the displayed `p_0,p_1`. Both increase in activation and leaf-gain rates and decrease in hub-loss rate, so substituting the worst rates is a valid subharmonic comparison even with adapted core interruptions. The effective next-leaf up/down odds are bounded below by

\[
 \frac{r_-^2}{1+2\delta}(1-o(1))>1.
\]

After applying the stopped-time repair S-M1, synchronization has conditional mean `O(Cm)`. At `(h,ell)=(1,m)`, suppressing hub loss gives the exact Bd deficit drift

\[
 \mathcal G R=-R\left[\frac r{c+m}+(r-1)(1-R/c)\right].
\]

The integrated expected deficit before `{0,3 delta c}` is at most `2 delta c/kappa`; conditioning on the suppressed path makes hub survival exactly `exp[-int R_s/c ds]`. Jensen plus the exponentially unlikely upper exit therefore gives a compact-uniform positive cleanup probability. The nested-strip return and the explicit stopping times `S_j,T_j` make each block's success and bad-event estimates conditional on the past. Hence the recursion `(1-s_*)^{N_C}` uses only the strong Markov property, not independence.

For dB, with `T=beta_0 log C` and `m=O(C^{1/4})`,

\[
 me^{-T}=O(C^{1/4-\beta_0}),\qquad
 R_0e^{-\kappa T}=O(C^{-\kappa\beta_0}).
\]

The two displayed choices
`beta_0-1/4>=B_0+2` and `kappa beta_0>=B_0+2` make both errors `O(C^{-B_0-2})`. Suppressing deactivation makes resident leaves a pure-death population and gives `E int(m-ell_s)ds<=m`; the core drift gives `E int R_s ds<=R_0/kappa`. Therefore the hub-deactivation probability is

\[
 O((R_0/\kappa+m)/C)=O(C^{-3/4})=o(1),
\]

with no factor `T`. Enlarging `beta_0` does not spoil this estimate. Repeated activated attempts use conditional success at least `1/2` and the strong Markov property.

For Bd pendant initialization, the base-plus-extra-clock construction is attractive: deleting mutants and suppressing mutant arrows can only lower the mutant set. In the adverse regeneration state, pendant loss before hub activation is `O(C^{-1})`, a seed precedes hub loss with probability `Theta(1/m)`, and a stopped supercritical seed reaches `K` with probability bounded below. Per trial, loss is `O((1+K)/C)` and success is `Omega(1/m)`, so loss before success is `O(m(1+K)/C)=o(1)`. Under dB, a sole mutant leaf dies at rate one while hub activation is `O(C^{-1})`; activation is necessary for fixation, giving the claimed `O(C^{-1})` upper bound.

### 8. Reciprocal invasion — verified

**References.** Lemmas 10–11, lines 934–1119; `eq:green-macro` through `eq:renewal-refined`.

At reciprocal fitness `s=1/r<1`, choose `delta` so the ordinary birth/death ratio below `delta c` is uniformly at most `vartheta<1`, and the drift is at most `-kappa_0 i`. Product odds give exponentially small probability to reach the macroscopic boundary; Dynkin gives bounded particle-time. Hitting a level `L'+1` first costs `O(vartheta^{L'-L})`, after which the remaining expected particle-time is `O(L')`, yielding the exponential Green tail. Since hub-change hazard is `O(I/C)`, the first hub change is `O_L(C^{-1})` and its count has the stated hazard-weighted exponential tail.

For a Bd mutant-hub excursion from a fixed cloud, hub loss is rate at least `m`, versus `O_L(1)` ordinary activity and `O(m/C)` pendant seeding, so the post-excursion fixation bound is `x_{C,L}+O_L(m^{-1})+O(C^{-1})=o(1)`.

For dB, the ordinary cloud is dominated until hub loss by immigration–death rates `b(i+1)` and `d_0 i`, with `b<d_0`. For `1<z<d_0/b`, the exponential Lyapunov function satisfies `G z^i<=K_z-alpha_z z^i`; stopping at level `M` gives

\[
 \Pr(\max_{s\le T}\bar I_s\ge M)
 \le (z^L+K_zT)z^{-M}.
\]

The manuscript then uses the correct finite-horizon order: after the population limit, send the post-loss truncation `L_2` to infinity, then cloud cutoff `L_1` to infinity for fixed `T`, and only then `T` to infinity. There is no unsupported infinite-horizon maximum estimate. After hub loss, the reactivation probability is at most `K(m+a_{L_1})/C=o(1)` for fixed `L_1`.

Finally,

\[
 x_{C,1}\le ae^{-\kappa C}+\frac aC(y_{C,L}+e^{-\theta L})
\]

first yields `limsup C x_{C,1}<=a e^{-theta L}` and then, after `L->infinity`, the required little-`o(C^{-1})`. The hub-start term is `o(1)` and is divided by a degree of order `C`. Thus both
`u_core^Bd(1/r)=o(C^{-1})` and `J_H(1/r)=o(C^{-1})` are established, not merely big-O bounds.

### 9. Portal rates, adverse reversals, and global sweep — verified

**References.** Proposition 12, lines 1142–1247; rate table at lines 1193–1205.

The portal sums are correctly normalized:

\[
 I_H=1+\frac1{C-1+m},\quad I_P=\frac{2\sigma}{C},
 \quad J_P=\frac\sigma C,
\]

where `J_P` already includes the two dB singleton committors `1/2`. Direct event summation gives the four rates in the displayed directions. Their leading values are

| update | pair invades resident center `A` | center recovers pair `D` | mutant center invades pair `B` | pair recovers center `C'` |
|---|---:|---:|---:|---:|
| Bd | `2 sigma (r-1)+o(1)` | `2/(r+1)+o(1)` | `2r^2/(r+1)+o(1)` | `o(C^{-1})` |
| dB | `2(r-1)+o(1)` | `sigma/r` | `r sigma` | `o(C^{-1})` |

Consequently

\[
 A/D\to Z_B=\sigma(r^2-1),\qquad
 A/D\to Z_D=\frac{2r(r-1)}\sigma.
\]

In macro state `(1,k)`, all `q-k` resident pairs expose conversion rate `B` and adverse center-recovery rate `C'`. The chance of a reversal before the next conversion is exactly `C'/(B+C')`; retaining it and union-bounding over at most `q` conversions gives

\[
 1-P_U^H\le q\frac{C'}{B+C'}=o(q/C).
\]

From `(0,1)`, the first successful macro transition is center invasion at rate `A` or pair loss at rate `D`, so `P_U^P=[A/(A+D)]p_{1,1}`. The same retained-reversal sweep gives `p_{1,1}->1`. This is the exact macro chain, not a branching or independent-lineage approximation.

### 10. Response/diagonal interface — verified

**References.** Proposition 13, lines 1251–1290; theorem proof, lines 1348–1357.

Writing `eta=q/C`, expansion of `N=C+m+2q` shows that the center supplies the baseline plus a leaf correction: `lambda/(r-1)` for Bd and `-lambda` for dB. The locally fixed pair contributes its singleton factor, gate probability `Z/(1+Z)`, and multiplicity `2q`. Exact simplification yields

\[
 B(r;\sigma,\lambda)=
 \frac{2(\sigma-1)}{1+\sigma(r^2-1)}+\frac\lambda{r-1},
\]

\[
 D(r;\sigma,\lambda)=
 \frac{2\{r(2-r)-\sigma\}}{\sigma+2r(r-1)}-\lambda.
\]

The complete Bd baseline error is exponentially small and the dB error is `O(C^{-1})`, both `o(eta)`. The independent rational calculation reproduced both identities and, at `(r,sigma,lambda)=(3/2,19/137,20/27)`, the exact margins `232/17361` and `65/12123`.

For the final theorem, fix `1<r<R_hyb`. Compact-uniform response asymptotics may be applied on a fixed compact neighborhood of this `r`; eventually `r in I_t`. The preselected dyadic inequality changes the gain after scaling by `n_t/q_t` by at most `1/t`, while the two separated scaled gains converge to strictly positive constants. Hence the actual gains are eventually positive. The graph sequence and every weight were selected before this fixed `r`; the threshold `t_0` may depend on `r`, exactly as Definition 1 permits.

## Boundary cases and unresolved items

- `r=1` is excluded. Drift and bias constants need not remain uniform as `r downarrow 1`; the proof does not use such uniformity.
- The endpoint `r=R_hyb` is not claimed: both first-order responses vanish there.
- `eps=0` is used only for the separated limiting trace. Every constructed graph has `eps_t>0` and is connected.
- Reciprocal fitness lies in a compact subset of `(0,1)` once the beneficial fitness lies in a fixed compact subset of `(1,infinity)`.
- The exact sextic root isolation and global optimization were assigned to the response/algebra audit; I checked only the stochastic input and response identities needed at that interface.
- Apart from S-M1, I have no unresolved stochastic assumption or unperformed check in the assigned scope.

## Final component conclusion

The arbitrary-size lumping, finite weak-cut trace, gain-scale center estimates, reciprocal little-`o` bounds, and adverse-reversal macro sweep are mathematically coherent and mutually consistent. The only defect found is the missing upper-strip stop in the Bd pendant waiting/hitting expectations. The stopped estimate already used by the later block construction follows from the immediately preceding comparison, including the stronger target `(h,ell)=(1,m)`, so the main theorem's stochastic foundation survives unchanged after a localized correction.
