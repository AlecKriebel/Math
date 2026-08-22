# Independent exact cross-checks and adversarial synthesis

Date: 2026-08-22  
Scope: frozen disposable referee package in `work/package`  
Implementation: `records/independent_crosschecks.py`  
Transcript: `records/independent_crosschecks.log`

## Bottom line

The independently written exact checker found **no mathematical mismatch or
counterexample**. It reproduces the manuscript's target-by-source orientation,
incoming-column gauge, fitness-two active collision identity, all eight displayed
Frobenius-normalized Hessian eigenvalues at `n=3,4,5`, the directed
strong-selection coefficient on four nonsymmetric kernels, and representative
triangle and symmetric-`K4` equality/strictness/boundary behavior.

The strongest adverse finding is instead a certification defect in the delivered
replay: 406 leading bare `assert` statements occur across 20 delivered Python
files, while neither bootstrap nor replay rejects `PYTHONOPTIMIZE`. Under
optimization those checks disappear and unconditional PASS/PROVED messages can
remain reachable. The clean, sanitized, unoptimized official replay did pass, so
this does not contradict the mathematical results; it does mean the launcher is
not a fail-closed verifier in an arbitrary inherited environment.

My overall recommendation from this route is **valid after minor corrections**:
no theorem or proof correction was found, but the replay should explicitly reject
optimized mode (and preferably replace theorem-bearing asserts with explicit
exceptions) before it is described as a robust certificate. The impact of this
software defect is high even though the remediation is small.

## Independence and method

I first read the defining manuscript equations, without reading a delivered
implementation for the computations below:

- target-by-source normalization and the dB transition rule, (2.1)--(2.2);
- active spaces, moves, and collision law, (3.10)--(3.12);
- active-kernel perturbation and Hessian resolvent, (4.1)--(4.6);
- sector embeddings and displayed values, (4.8)--(4.12);
- strong-selection expansion, (5.4)--(5.16);
- triangle equations/certificate, (6.1)--(6.8); and
- the definitions of `G13` and `G22` and their literal dB quotient, (B.1).

The new checker imports only `fractions.Fraction`, `itertools`, `platform`,
`sys`, and `__future__`. It does not import a delivered module, SymPy, FLINT, or
a package expected-answer implementation. It enumerates every transient subset
state and solves rational systems by a separately written pivoted Gaussian
eliminator. Its SHA-256 is
`019a599899fa223995ea61ca476e5e841e55bcea3605203f81b593d67f92d578`.

The first run stopped with a `KeyError` because the new active-chain builder
attempted to look up an invalid state attached to a zero-probability diagonal
source. I corrected it to omit exactly-zero contributions, then reran every
calculation from the start. This was an error in the new audit code, not in the
delivered package; it produced no accepted scientific result before correction.
The final run exited 0 under Python 3.14.6 with `sys.flags.optimize=0`. A second
run at `optimize=1` also exited 0 with identical results because this checker
uses explicit `require(...)/RuntimeError`, not bare asserts.

## Exact independent results

### 1. Orientation and column scaling

Raw directed weights were stored as `W[source][target]` and normalized as
`P[target][source]`, exactly as in (2.1). Multiplying the four incoming columns
by `2,3,5,7` left both `P` and exact fitness-two fixation unchanged:

`rho2 = 1994823874198812044599989615561 /
        4995392136150338282032947317056`.

A deliberately wrong source-row normalization of the same nonsymmetric raw
matrix gave

`16710880084112087651066519475395 /
 41940651071234278761027035179184`,

which is different. Thus the test is orientation-sensitive rather than a
symmetric control on which the two conventions accidentally coincide.

### 2. Literal subset chain versus literal active chain

For each positive nonsymmetric kernel, the checker independently built:

1. the `2^n-2` transient forward dB subset equations at `r=2`; and
2. all `n(2^(n-1)-1)` active states `(B,v)`, the two one-sample moves, the exact
   stationary law, and `H(B,v)=1/|B|`.

Every case satisfied `n*rho2*(nu H)=1` exactly.

| Kernel | `n` | Active states | Exact `rho2` | Exact `nu H` |
|---|---:|---:|---|---|
| P3-A | 3 | 9 | `179596/416271` | `138757/179596` |
| P3-B | 3 | 9 | `1178267/2900142` | `966714/1178267` |
| P4-A | 4 | 28 | `196796111507759984517/473683767269978727580` | `118420941817494681895/196796111507759984517` |
| P4-B | 4 | 28 | `87150802243189417565223/209118271071676443599852` | `52279567767919110899963/87150802243189417565223` |

This catches the rectangular phase order and normalization on genuinely
nonreversible examples. No row/source reversal, factor two, or `n` factor was
found.

### 3. Literal active-resolvent Hessian

At each `n`, the checker constructed `K0` and its directional derivative
`Delta` directly from the two active moves. It verified the displayed complete
stationary law entry-by-entry, formed

`G=(I-K0+1 nu0)^(-1)`,

checked `nu0 Delta Gq=0`, and computed

`R2(delta)=nu0 Delta G Delta Gq`.

The representatives were: `E(e0-e1)` for the standard sector; a four-edge
symmetric row/column-balanced square for the symmetric sector; and a directed
cycle circulation for the antisymmetric sector. Exact division by the
Frobenius norm squared gives:

| `n` | Sector | `R2(delta)` | `||delta||_F^2` | Computed normalized value | Manuscript |
|---:|---|---|---|---|---|
| 3 | standard | `4/33` | `4/3` | `1/11` | `1/11` |
| 3 | antisymmetric | `2/3` | `6` | `1/9` | `1/9` |
| 4 | standard | `261/2560` | `3/4` | `87/640` | `87/640` |
| 4 | symmetric | `3/26` | `8` | `3/208` | `3/208` |
| 4 | antisymmetric | `57/80` | `8` | `57/640` | `57/640` |
| 5 | standard | `6868/85971` | `8/15` | `8585/57314` | `8585/57314` |
| 5 | symmetric | `718/6665` | `8` | `359/26660` | `359/26660` |
| 5 | antisymmetric | `143/210` | `10` | `143/2100` | `143/2100` |

The symmetric dimension `n(n-3)/2` is zero at `n=3`, so no missing `n=3`
symmetric test exists.

### 4. Strong-selection coefficient

Rather than evaluate at merely large finite fitness, the checker differentiated
the literal subset absorption equations exactly at `epsilon=1/r=0`. In all
four nonsymmetric complete-support cases,

`[-(n-1)/n - rho'(0)] = E_dir/[n^2(n-2)]`.

| Kernel | `rho(0)` | `rho'(0)` | `E_dir` | Gap coefficient |
|---|---|---|---|---|
| P3-A | `2/3` | `-8/9` | `2` | `2/9` |
| P3-B | `2/3` | `-1853/1260` | `1013/140` | `1013/1260` |
| P4-A | `3/4` | `-43/48` | `14/3` | `7/48` |
| P4-B | `3/4` | `-123/128` | `27/4` | `27/128` |

This is an exact orientation-sensitive spot check of the coefficient, not a
floating extrapolation in `r`.

### 5. Triangle and symmetric-`K4` slices

All examples below used the full transient subset chain; the checker did not
use the manuscript's six-state triangle system or the delivered `K4` lumpings.

For triangles, uniform weights tied exactly; weights `(1,2,3)` at `r=2` had
gap `4016/389007`; `(2,5,7)` at `r=7/3` had gap
`43544/3022245`; and the near-boundary `(1/1000,2,3)` at `r=3/2` was strictly
suppressing. At the excluded support boundary `(0,2,3)`, suppression persisted
with gap `5/126`. At the neutral endpoint `r=1`, a nonuniform positive triangle
tied `1/3`, as it should.

For `G13`, `x=1` tied at `r=2`; `x=1/3` had gap `41/1827`; and
`x=1/1000,r=7/3` was strictly suppressing. The support boundary `x=0` was also
strictly suppressing. For `G22`, `(x,y)=(1,1)` tied; `(2,2),r=3/2` had gap
`27/47728`; `(1/10,10),r=2` was strictly suppressing; and the bipartite
boundary `(0,0),r=2` had gap `1/133`. The nonuniform neutral endpoint tied
`1/4`.

The exact endpoint checks also found that every tested positive two-vertex raw
weight ties the `n=2` baseline and that fixation increased strictly from
`r=1` to `2` to `3` on all four nonsymmetric kernels. The latter is only a
spot check; the manuscript's monotone-coupling proof supplies the universal
statement.

## Adversarial synthesis across proof, package, and replay

### A. Attempts to falsify the mathematics

No counterexample survived exact calculation, and no endpoint gap was found.

- **Local theorem ranges.** With `N=n-1`, the standard proof uses exact values
  for `2<=N<=9` and a strict analytic bound for `N>=10`. The antisymmetric
  coupling begins at `N=2`. The symmetric proof uses exact solves for
  `3<=N<=39`, every one of the 248 integers `40<=N<=287`, and an analytic
  certificate for `N>=288`. These ranges are contiguous. The separate local
  audit independently recomputed the exact `N=40` minimum and checked the
  large-order discriminant arguments, including positive leading coefficient
  and positive value at zero; no finite computation is extrapolated to an
  infinite range.
- **Strictness and conversion.** The independent active calculation found zero
  first variation and positive inverse-mean curvature in each existing sector.
  The manuscript's differentiation then gives negative fixation curvature with
  the factor `-2m_n^2/n`; there is no sign reversal or missing factor.
- **Strong selection.** The exact epsilon differentiation agrees with the
  incoming-column sum of squares on four directed examples. The independent
  strong-selection audit rederived the general singleton/pair expansion and
  checked that the cited noncomplete-support theorem uses the same dB model and
  hypotheses. The result is for each fixed finite structure; no uniformity in a
  growing graph sequence is asserted.
- **Low order.** Full-chain examples hit the equality classes, highly
  nonuniform interiors, neutral-fitness endpoint, near-zero weights, and
  connected zero-support boundaries. The separate low-order audit also
  regenerated the symbolic triangle and both `K4` factorizations; the samples
  here therefore serve as implementation-independent controls rather than the
  proof of the universal parameter statements.
- **Scope.** The `OPEN` notices in the replay concern global fitness-two
  maximality and stronger stochastic/forest routes. The manuscript explicitly
  leaves global `r=2` maximality open, gives no explicit or population-uniform
  local radius, and does not exclude singular growing amplifying families.
  None of those notices is a failed premise of a stated theorem.

### B. Proof/code alignment

The clean official replay, run from the frozen package under a credential-free
sanitized environment with Python 3.14.6 and optimization disabled, exited 0.
It installed the three pinned package versions, ran the full unit/replay suite,
reported the stated finite ranges, rebuilt the 30-page PDF, reproduced SHA-256
`a6bda621b764ca8ee86658f6b68de0245790b84315eb77a6cc7ca45f7953bd2d`,
and ended with the package PASS line.

The software and proof have different legitimate roles:

- the exact programs discharge the finite symbolic/rational cases and check
  algebraic identities;
- the standard/antisymmetric/symmetric tail arguments in Appendix A carry the
  infinite quantifiers; and
- the literal small-chain programs and this checker test phase order,
  orientation, and physical normalizations.

Consequently, a program line such as `PROVED ANALYTICALLY ... every n>=3`
must not be read as an exhaustive program loop. Static inspection found the
antisymmetric verifier evaluates its recurrence only through `n=40` and full
active chains only through `n=7`; the all-order claim is supported by the
manuscript coupling proof. This is correctly disclosed in the manuscript, but
the terminal wording is broader than the executable assertion alone.

### C. Findings and severity

#### C1. High-impact reproducibility/code defect: assertions can be erased

`submission/bootstrap_replay.sh` uses assertions for the Python and dependency
version gates, and most scientific programs use bare assertions for their
theorem-bearing checks. Static counting found 406 leading asserts across 20
delivered Python files. The wrappers do not clear `PYTHONOPTIMIZE` and do not
check `sys.flags.optimize`.

Exact reproduction already recorded in `records/COMMANDS.log`:

`PYTHONOPTIMIZE=1 /opt/homebrew/bin/python3 -c 'assert False; print("PASS_AFTER_ERASED_ASSERT")'`

prints `PASS_AFTER_ERASED_ASSERT` and exits 0. Thus a user can receive PASS
language after the certification conditions were compiled away. The audited
clean run explicitly verified `optimize=0`, so its scientific evidence remains
usable.

Required correction: make bootstrap reject `sys.flags.optimize != 0`, unset or
reject `PYTHONOPTIMIZE`, and convert load-bearing assertions to explicit checks
that raise or exit nonzero. This finding changes the package verdict but not the
mathematical verdict.

#### C2. Medium/low coverage-description issue: imported audit mains are inert

The claim map accurately says three modules are *reached as imported helpers*,
but that does not mean their guarded audit suites execute. Replay uses
`verify_resolvent_identities.solve` and
`verify_direct_flow_screen.matrix_from_edges`; it does not call the
direct-flow screen's `main`, the Fisher/witness suite in
`verify_fisher_route`, or the resolvent module's standalone examples. The
Fisher functions are only imported transitively.

No stated theorem was found to depend on those inert standalone diagnostics,
and the claim map warns that reachability is not proof. The correction is to
label the exact used symbols and separately mark the guarded audit mains as not
executed, preventing readers from counting them as independent evidence.

#### C3. Medium/low environment and supply-chain robustness

Versions are pinned but distributions are not hash-pinned or vendored, and a
fresh PDF build may download Tectonic resources. `PYTHONPATH` and `MAKEFLAGS`
are also inherited by the package scripts. The referee run mitigated this with
an empty environment, a declared package index, isolated HOME/cache/TMP paths,
and explicit absence of credential/build override variables. The byte-identical
PDF comparison and exact installed-version check validate this run, but the
launcher itself should sanitize or reject those variables and preferably use
hash-pinned artifacts for stronger reproduction.

#### C4. Low/non-load-bearing maintenance issue

The unused legacy `make paper1` target points to a tree omitted from the
standalone archive. The mandatory replay deliberately does not call it and the
document has a separate working build path. Remove or label the target to avoid
confusion; no theorem or executed check depends on it.

## Exact remaining limitations

1. This checker independently reconstructs the displayed active chains only at
   `n=3,4,5`; the all-order claim rests on the separately audited Appendix A
   proof and its finite exact certificates.
2. The `3<=N<=39` symmetric range ultimately relies on exact FLINT solves in
   the delivered verifier. Independent active/orbit calculations agree through
   the displayed small orders, but this route did not write a second solver for
   all 37 small symmetric orders.
3. Exact arithmetic still assumes the correctness of CPython integer/Fraction
   operations and, for the delivered finite certificates, SymPy/python-flint.
4. Global fitness-two maximality, an explicit or uniform local radius, and
   growing-family classification remain open by design, not failed checks.
5. No external person was contacted and no artifact was uploaded. The process
   used no empirical data.

Subject to the replay hardening in C1, the proof and software independently
support the same stated mathematical claims.
