# Adversarial reconciliation and final hostile-referee check

**Checkpoint:** 2026-08-22 (America/Los_Angeles)
**Assigned-scope completion:** **100%**
**Recommended categorical verdict:** **valid after minor corrections**
**Theorem status:** The main theorem survives. The manuscript contains a genuine false unstopped expectation in the Bd pendant-cleanup proof, but the stop already built into the later block construction yields the needed conditional `O(Cm)` estimate by a local, noncircular argument. I found no second mathematical defect and no reason to escalate the mathematical verdict to major correction, invalid, or inconclusive. The `PYTHONOPTIMIZE` issue is high severity for verifier soundness but is a mechanical software repair and does not undermine the independently checked mathematics.

## Materials and independence

I read the full 1,615-line `main.tex`, `work/THEOREM_LEDGER.md`, and the completed independent reports `stochastic_math_audit.md`, `response_quantifier_audit.md`, and `package_code_audit.md`. I treated every conclusion in them as a claim and rechecked the load-bearing interfaces, with particular attention to `main.tex:728-755`, `784`, `802-842`, the reciprocal little-`o` estimates, and the diagonal quantifiers. The working manuscript and delivered extracted source are byte-identical (SHA-256 `bdc026e1dd8f9de1f9889d85ea9bff5342fb570d8487d636b1ee4758f49b7ebe`). I did not modify `delivered_copy`, use the network, contact anyone, upload, commit, or push.

## ADV-MATH-01 — Genuine but local stopped-time omission

**Severity:** minor mathematical correction; mandatory, not stylistic.
**Location:** Lemma 9 (`lem:pendant-cleanup`), `main.tex:728-755`, especially `eq:leaf-wait` at `743-747` and `eq:leaf-hitting-time` at `749-755`; propagated citations at `784`, `807-808`, `825`, and `840-842`.

### Counterexample to the displays as written

The manuscript defines `sigma_j` as successive pendant-count changes and then claims

\[
 \mathbb E(\sigma_{j+1}-\sigma_j\mid\mathcal F_{\sigma_j})\le K_0C,
 \qquad
 \sup_{R\le2\delta c}\mathbb E\tau_{\{\ell=m\}}=O(Cm).
\]

Both can be infinite. Take a high-core state with resident hub and `ell=0` (for example `R=0`, so every ordinary clique vertex is mutant). Under either update rule there is a finite sequence of positive-rate resident replacement events that keeps the hub resident, decreases the ordinary mutant count to zero, and never changes a pendant. That path has strictly positive probability. At global extinction there is no later pendant change and `ell=m` is never reached, so `sigma_{j+1}=infinity` and `tau_{ell=m}=infinity` on a positive-probability event. This directly falsifies both unconditional expectations.

### Rigorous repair

For a block start `S`, define

\[
 \zeta_S=\inf\{s\ge S:R_s\ge2\delta c\},\qquad
 \Sigma_S=\inf\{s\ge S:(h_s,\ell_s)=(1,m)
                         \text{ or }R_s\ge2\delta c\}.
\]

The required statement is

\[
 \mathbb E(\Sigma_S-S\mid\mathcal F_S)\le K C m
 \quad\text{whenever }R_S\le\delta c,
\]

uniformly on the fixed fitness compact. This follows from the manuscript's preceding rates as follows.

1. For `1<=ell<m`, use the worst-rate two-hub-state committor from `main.tex:694-715`, but assign value one to an exit at `R>=2 delta c`. Interior core jumps still leave the committor unchanged, while an exit jump adds `rate*(1-p_h)>=0` to its generator. Therefore the same subharmonic calculation proves

   \[
   \frac{\Pr(\text{pendant up or strip exit before pendant down})}
        {\Pr(\text{pendant down first})}\ge\beta>1.
   \]

   This disposes of the most dangerous counterexample attempt: state-dependent strip-exit hazards cannot reverse the pendant bias when exit is made a favorable absorbing outcome.

2. At successive pendant-change-or-exit epochs, send the artificial level to `m` on exit. For levels below `m`, its conditional drift is at least

   \[
   d_\beta=\frac{\beta-1}{\beta+1}>0;
   \]

   at `ell=0` a downward change is impossible. Optional stopping first at a bounded number of epochs and then by monotone convergence gives at most `m/d_beta=O(m)` epochs before `ell=m` or exit. This uses conditional drift with the full hidden-coordinate history; it uses neither a Markov assumption for the pendant marginal nor independence.

3. Stop each hub phase at exit as well. Before exit, an `h=0` phase has activation-or-loss intensity bounded below by a positive constant, and an `h=1`, `ell<m` phase has deactivation-or-gain intensity at least one (`main.tex:728-742`). Each phase has bounded conditional mean length. Every one or two phases have conditional probability at least `c_0/C` of a pendant change; exit can only shorten the wait. Hence the conditional mean time to the next pendant change or exit is `O(C)`. Summing over the `O(m)` expected epochs gives `O(Cm)`.

4. The only extra case is `(h,ell)=(0,m)`. Activation, loss, or exit has bounded mean waiting time. Loss before activation has probability `O(C^{-1})` (`main.tex:757-758`) and restarts the stopped estimate at `m-1`; activation or exit terminates. Thus, if `M` is the worst target-or-exit mean,

   \[
   M\le K C m+K+O(C^{-1})M,
   \]

   and therefore `M=O(Cm)`. If `ell` first reaches `m` by a gain, the hub is mutant at that same event, so the target is already `(1,m)`.

This is precisely the conditional estimate claimed for `Sigma_j` at `main.tex:802-809` after the missing stop is supplied.

### No circularity and no transferred central difficulty

The repaired mean is proved **before** invoking confinement and is stopped at the strip exit, so it assumes no confinement event. Escape is then controlled on a deterministic horizon:

- From `R_{S_j}<=delta c`, Markov's inequality gives
  `Pr(Sigma_j-S_j>C^2)=O(Cm/C^2)=O(m/C)=o(1)`; separately, Lemma 8 bounds a hit of `2 delta c` by time `C^2` by a polynomial times `exp(-gamma C)`. Thus `main.tex:782-785` remains valid.
- For the block-duration estimate, stopped synchronization has mean `O(Cm)` and the stopped cleanup/return pieces have mean `O(C^2)`. With `D_*=B_0+4`, Markov gives `O(C^{-B_0-2})` as required at `main.tex:836-844`.
- Conditional on duration at most `C^{D_*}`, Lemma 8 controls synchronization escape; the nested `3 delta c` and `4 delta c` estimates control the later attempt and return. These are exactly the separately charged events at `main.tex:809-838`.

The logical order is therefore: stopped mean, deterministic truncation, confinement probability, strong-Markov regeneration. There is no use of the desired block conclusion to prove its own duration bound. The repair changes no asymptotic scale and introduces no claim equivalent to the theorem.

## Other hostile checks

### Reciprocal little-`o(C^{-1})` — survives

At `main.tex:1007-1094`, the coarse `x^U_{C,L}=O_L(C^{-1})` bound is not the final claim. The hub-excursion decompositions give `y^U_{C,L}=o(1)` for each fixed `L`, using the stated order `C -> infinity`, then `L_2`, `L_1`, and the finite horizon `T`. Substitution into `main.tex:1096-1106` gives

\[
 \limsup_{C\to\infty} Cx^U_{C,1}\le a e^{-\theta L},
\]

and only then `L -> infinity`, proving `x^U_{C,1}=o(C^{-1})`. The hub-start term is `o(1)` and is divided by a degree of order `C` at `main.tex:1109-1118`. Thus both `u_core^Bd(1/r)=o(C^{-1})` and `J_H(1/r)=o(C^{-1})` are genuinely little-`o`, and the gate estimate `qC'/B=o(q/C)` at `main.tex:1226-1228` is supported.

### Compact-uniform diagonal and quantifiers — survives

There are two different uniformities and the proof does not conflate them:

- For each fixed finite `t`, Proposition 5 is uniform on the one compact algebraic interval `I_t`; this is enough to make at least one dyadic exponent admissible and the least admissible exponent exactly decidable (`main.tex:276-322`). No rate uniform in `t` is required.
- For the population limit, one fixes an interior fitness `r` and applies Propositions 6, 12, and 13 on a fixed compact neighborhood of that `r`. Eventually `r in I_t`. The preselected diagonal changes the scaled normalized gain by at most `1/t` (`main.tex:1348-1356`).

Hence the order remains

\[
 \exists\{G_t\}\;\forall r\in(1,R_{\rm hyb})\;
 \exists t_0(r)\;\forall t\ge t_0(r),
\]

with no fitness-dependent graph choice and no exchange of the weak-cut and population limits.

### Weak-cut, gate, response, and algebra interfaces — survive

I found no sign/orientation mismatch in the row-oriented Schur complement `A+B(I-Q_0)^{-1}C_0` (`main.tex:396-440`), no use of a branching survival probability in place of exact local absorption, and no omitted adverse-reversal term in the macro chain (`main.tex:1214-1246`). The four portal rates give the stated `Z_B` and `Z_D`; the response and quantifier report independently reconstructs the first-order functions, tangency, sextic isolation, rational specialization, and endpoint strictness. These conclusions depend on the center estimates, but ADV-MATH-01's stopped repair restores that dependency rather than assuming it.

### Proof/code consistency — bounded correctly, except for false-pass behavior

The manuscript accurately says that the programs check finite transition aggregation and exact encoded algebra, not the weak-cut or stochastic asymptotics (`main.tex:1484-1489`). The finite nine-vertex lumping program is corroboration only; arbitrary-size lumpability comes from the automorphism proof. `verify_paper_claims.py` is a marker/integration audit, not a theorem checker. Thus I found no mathematical overclaim across the proof/code boundary.

## ADV-CODE-01 — Optimized Python can erase the verifier

**Severity:** high for software verifier soundness; no mathematical propagation.
**Locations:** `bootstrap_replay.sh:9-12,23-29`; `verify_leading_algebra.py:15-66`; `verify_hybrid_lumping.py:159`; `verify_hybrid_coefficients.py:16-106`; `verify_paper_claims.py:32-154`.

All verification conditions in the four mathematical programs, and the bootstrap's version conditions, are bare Python `assert` statements. `PYTHONOPTIMIZE=1` removes them. The retained disposable fixture injects an impossible `assert False` into `verify_leading_algebra.py`: normal execution exits 1, whereas optimized execution exits 0 and prints the numerical diagnostics and final `PASS`. This reproduces a real false pass, not merely a theoretical concern. The canonical completed run had `PYTHONOPTIMIZE` unset, so this does not cast doubt on the values observed in that run or on the independent derivations.

Required repair: replace every verification-critical assertion with an explicit conditional that raises, and explicitly reject `sys.flags.optimize != 0`. Sanitizing the inherited environment is additional hardening. This is high severity within the supplementary tool, but it is mechanical and does not supply or remove any step of the analytic proof; it does not justify escalating the scientific verdict to major correction.

## Reconciled result status

| Claim | Adversarial status |
|---|---|
| Effective dyadic diagonal (Lemma 2) | Survives; exact finite-`t` compact decision and final quantifier order are sound. |
| Weak-cut trace and strong lumping (Lemma 4 / Proposition 5) | Survive; orientation, fast-state transience, compact inverse, and certificate boundary are consistent. |
| Center module (Proposition 6) | Survives after ADV-MATH-01. |
| Pendant cleanup (Lemma 9) | False at the two unstopped expectation displays as written; valid with the explicit target-or-strip-exit stop. |
| Reciprocal renewal (Lemmas 10-11) | Survives; the final refinement proves little-`o(C^{-1})`. |
| Gate and global sweep (Proposition 12) | Survives; adverse reversals are retained and accumulated error is `o(q/C)`. |
| Responses, tangency, and theorem (Proposition 13, Lemma 14, Theorem 3) | Survive once the stopped cleanup statement replaces the false display. |
| Fixed-response optimality and rational family (Proposition 15 / Corollary 16) | Survive within their explicitly limited scope. |
| Supplementary verifier | Standard run supports its bounded claims, but fail-closed behavior is false under optimized Python until ADV-CODE-01 is fixed. |

## Final recommendation

The manuscript is not fully validated in its delivered wording because equations (25)-(26) assert infinite expectations are finite, and the supplementary certifiers are not fail-closed under optimized Python. Nevertheless, the stopped-time correction is explicit, local, and rigorous; it proves exactly the conditional `Sigma_j` estimate later required, without circularity or a new central lemma. All attempts to break the reciprocal rate, compact-uniform diagonal, gate scale, or proof/code interface failed.

Accordingly, the categorical recommendation is **valid after minor corrections**. Required corrections are: (i) rewrite `main.tex:728-755` throughout in target-or-upper-strip-exit form and update every later citation to that stopped statement; and (ii) replace assertion-based verifier checks by explicit fail-closed checks. No second mathematical defect or unresolved verification gap warrants a more severe verdict.

**Best-guess completion:** **100% of the assigned adversarial reconciliation.**
