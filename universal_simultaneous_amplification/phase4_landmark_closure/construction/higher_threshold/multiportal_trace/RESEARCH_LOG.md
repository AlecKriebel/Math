# Two-portal protected-pair trace: research log

## 2026-08-02 08:35 PDT — program opened

- Scope: one symmetric module with two active portals, an optional portal--portal edge, and a growing collection of strong-pair blades.
- Goal: derive the rare-mutant trace for Bd and dB without discarding the simultaneous-two-portal state; separately audit the post-establishment density drift.
- First checkpoint will scan the homogeneous balanced scaling at `r=8/5` before attempting an exact class theorem.
- No literature search or external contact.

## 2026-08-02 09:05 PDT — rare-mutant portal trace derived

- Chosen architecture: two exchangeable portals, a portal edge of weight
  `2*c*theta`, and `s` pair blades with internal weight one and all four
  portal--blade incidences of weight `c/s`.
- Retained portal-count states `1` and `2` during an episode.  The Bd episode
  has `1->0` rate `2c+g`, `1->2` rate `rg`, `2->1` rate `4c`, and child rate
  `k*r^2*(1-g)/(r+1)`.  The dB episode has `1->0` rate one, `1->2` rate
  `rg/[1+(r-1)g]`, `2->1` rate `2(1-g)/[1+(r-1)g]`, and child rate `k*r*c`.
- Derived exact phase-type offspring PGFs and the lifetime-offspring fixed
  point for each rule.  Establishment is kept distinct from fixation.

## 2026-08-02 09:20 PDT — `r=8/5` reconnaissance

- Scanned 241 logarithmically spaced `c` values in `[0.02,20]` and 242
  portal-coupling values (`theta=0` plus 241 logarithmically spaced values in
  `[10^-4,100]`): 58,322 parameter pairs total.
- No pair beat `p=3/8` under both limiting establishment laws.
- Best coarse maximin point:
  `c=0.2591373395034`, `theta=0.2818382931264`,
  `alpha_B=0.3375562112857`, `alpha_D=0.3376994761266`; the common margin was
  `-0.0374437887143`.
- This is labeled numerical reconnaissance only; the exact certificate below
  supersedes it.

## 2026-08-02 09:28 PDT — exact all-fitness class no-go

- Exact Bd amplification criterion:
  `alpha_B > 1-1/r` iff `2c+g>1`.
- With `x=c-(1-g)/2`, the sign polynomial for dB amplification is

  ```text
  E = -(1-g)(r-1)[r^2+g^2+r(r-1)^2 g(1-g)]
      -2[1+(r-1)g][r((r-1)^2+1)(1-g)+2g] x
      -4(r-1)[1+(r-1)g] x^2.
  ```

  Hence the Bd condition `x>0` makes `E<0` for every `r>1`.  For `r>=2`,
  dB already fails through its one-half entrance factor.  Therefore this
  fixed-parameter symmetric two-portal class cannot simultaneously amplify at
  any beneficial fitness.
- At the requested `r=8/5`, all three coefficients of the shifted quadratic
  are manifestly negative on `0<=g<1`.

## 2026-08-02 09:35 PDT — post-establishment and finite-chain audits

- Derived the full fast portal-count chains at arbitrary mutant-blade density
  `y`, including count two.  Their exact averaged forward/backward blade
  ratios are
  `r^3[2c(1+(r-1)y)+gr]/[2c(1+(r-1)y)+g]` for Bd and
  `r^3[1+(r-1)(y+g(1-y))]/[1+(r-1)y(1-g)]` for dB.  Both exceed one, so the
  obstruction is at establishment rather than the sweep.
- `verify_two_portal_tradeoff.py`: all exact symbolic certificates pass.
- Independent finite exact lumping uses portal count plus resident,
  heterotypic, and mutant blade counts.  At `r=1.6,c=0.4,g=0.3`, the predicted
  limits are `Bd=0.385617963410`, `dB=0.307797052278`; at `s=64`, the exact
  finite averages are `Bd=0.384306832858`, `dB=0.309417002117`, consistent
  with the trace.  The corresponding complete baselines are `0.375` and
  `0.372115384615`.
- Deliverables written in `TWO_PORTAL_PAIR_NO_GO.md`; no commit or push made.

## 2026-08-02 09:40 PDT — independent root audit

- Re-derived every episode rate from the atomic Bd and dB rules and checked
  the fixed-point sign orientation.  No discrepancy was found.
- Strengthened the finite-cutoff argument to an explicit stopped-process
  convergence lemma.  The theorem uses branching survival only as a fixation
  upper bound and therefore does not invoke the invalid independent-genealogy
  domination rejected elsewhere in this program.
- Added a fully independent exact-fraction verifier.  It enumerates all 256
  labelled subsets for `s=3`, proves strong lumpability into 30 count states,
  and matches every aggregate generator rate under both rules.
