# Exchangeable multiportal protected-pair trace: research log

## 2026-08-02 09:10 PDT — program opened

- Scope: replace the two active portals by `q` exchangeable portals, retain
  every portal-count state `0,1,...,q`, and couple all portals symmetrically
  to a diffuse collection of strong-pair blades.
- Goal: derive the exact Bd and dB rare-mutant establishment transforms,
  search for a `q`-uniform tradeoff certificate, and audit the later
  blade-density sweep separately.
- The portal graph is initially the complete graph with equal portal-edge
  weights; no literature search or external contact will be used.

## 2026-08-02 09:35 PDT — full portal-count traces derived

- For `Q` portals, retained every episode state `0,1,...,Q`.  Derived the
  exact Bd rates
  `d_k=k[2c+(Q-k)g/(Q-1)]`,
  `u_k=r k(Q-k)g/(Q-1)`, and
  `b_k=k r^2(1-g)/(r+1)`.
- Derived the exact dB rates
  `d_k=k[Q-1-g(k-1)]/[Q-1+g(r-1)(k-1)]`,
  `u_k=r k(Q-k)g/[Q-1+g(r-1)k]`, and `b_k=krc`.
- Parent episode/death ratios remain independent of `Q`:
  `kappa_B=2r(r+1)c/(1-g)` and `kappa_D=r^2(1-g)/c`.
- Numerical reconnaissance for `Q` through 100 found no simultaneous
  establishment point and suggested a bound uniform in `Q`.

## 2026-08-02 09:45 PDT — `Q`-uniform exact obstruction

- Put `x=2c/(1-g)`.  At the Bd comparison point `z=1/r^2`, the exponential
  barrier `phi_k=[x/(x+r-1)]^k` has killed-generator residual with the sign
  of `1-x`.  The `M`-matrix comparison proves exactly that Bd establishment
  amplifies iff `x>1`, for every `Q`.
- At the dB boundary `x=1`, introduced backward ratios
  `R_k=F_{k-1}/F_k`.  The envelope
  `T_k=1+(r-1)[Q-1+g(r-1)(k-1)]/(Q-1)` is exact at `k=Q`; its backward
  recurrence gap factors into a product of positive terms proportional to
  `g^2 k(Q-k)(r-1)^3`.  Hence `R_1<=r` and the episode marked probability is
  at most `1-1/r`.
- Since the marked probability divided by `c` decreases with `c`, every
  Bd-amplifying load forces strict dB suppression for `1<r<=2`; the dB
  entrance factor handles `r>2`.

## 2026-08-02 10:00 PDT — singular and sweep audits completed

- Derived a parameter- and `Q`-uniform strict-gap dichotomy using the split
  `x_m=[1+r(2-r)]/2`.  This supports a growing-portal graph corollary when
  `Q_s=o(s)` and `x_s` stays in a positive compact interval, even when
  `g_s->1` arbitrarily fast.  A stopped branching martingale supplies the
  uniform `1/K` establishment-tail error.
- The `Q->infinity` boundary episode tends to a linear birth--death--mark
  process with no-mark root exactly `1/r`.  Thus the dB envelope becomes
  sharp, but its amplification threshold retains the strict factor
  `1/[r(2-r)]`.
- At arbitrary mutant-blade density, both portal-count stationary laws have
  the same adjacent-ratio form.  Stationary flow gives blade forward/backward
  ratio at least `r^3` for both rules, so the obstruction is entirely at
  establishment.
- `verify_multiportal_tradeoff.py` passes all symbolic-`Q,k` identities and
  independent exact tridiagonal checks for `Q=2,...,7`.
- An independent finite atomic-update lumping passed `Q=3` and `Q=4`
  convergence audits.  At `Q=3,r=1.6,c=0.35,g=0.4`, the predicted limits
  are `Bd=0.387948202767` and `dB=0.306411032031`; the `s=48` exact averages
  numerically obtained from the exact finite chain are `0.385447019575` and
  `0.309889503147`.
- Full theorem and scope written in `EXCHANGEABLE_MULTIPORTAL_NO_GO.md`.
  No commit or push made.

## 2026-08-02 10:19 PDT — independent labelled-state audit

- Rechecked every displayed finite transition directly against the atomic
  Bd and dB rules.
- Added a separate exact-fraction verifier that enumerates all 512 mutant
  subsets of a rational nine-vertex instance with three portals and three
  blades.  It checks strong lumpability and every orbit-generator entry
  without importing the finite numerical solver.
- The theorem package is ready for repository-level integration after this
  final verifier passes.
