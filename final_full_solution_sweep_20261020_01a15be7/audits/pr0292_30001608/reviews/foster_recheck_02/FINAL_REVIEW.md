# Foster recheck 02 — final independent mathematical review

Recorded: 2026-10-21T03:28:10.337261+00:00. Review task: **100% complete**.

**Verdict: no mathematical gap found in TURN_4 for the stated six-rate CTMC at every fixed real lambda > 0.** The displayed global certificate establishes positive recurrence, subject to the exact model assumptions stated below. No repair to the original proof was required. This is mathematical review only; source identification/priority, literature novelty, and publication clearance are not assessed.

## Exact claim checked

On nonnegative integer (a,b,x,y), let D=x+y+1. Arrivals increase a or b, each at rate lambda/2. First downloads move (a,x) to (a-1,x+1) at a(x+1)/D and (b,y) to (b-1,y+1) at b(y+1)/D. Final downloads/departures decrease x at x(y+1)/D and y at y(x+1)/D. Coordinates that would be decremented from zero have zero rate. The permanent seed and exclusion of a,b from D are retained. The conclusion is irreducible, nonexplosive, positive recurrent for every fixed real lambda>0, and hence a unique stationary probability law. No uniform quantitative bound as lambda tends to infinity is claimed.

## Independence and strongest verified result

The initial timestamped checkpoint and population-generator derivation were written at 2026-10-21T03:19:30Z before reading TURN_4 or existing mathematical verdicts/checkers. The proof's rounded and Poisson terms were then independently rederived and recorded before author-checker inspection. Every later proof step was algebraically checked in ANALYTIC_RECHECK.md. The new executable diagnostics import no author or earlier review code and construct g by a killed tridiagonal linear solve rather than either existing corrector implementation. The old extensive audit and inherited review verdicts were not used to reach the mathematical verdict. Existing checkers were subsequently replayed as labeled reuse, providing supplementary controls.

The strongest verified result is the proposed all-state inequality LV<=-1 off a finite set F for the exact model, together with legitimate CTMC nonexplosion, irreducibility, and localization. Finite computational evidence supplements this deduction; it is not its proof.

## Analytic falsification attempts

- **Rounded h:** its derivative is clipped z/m and globally 1/m-Lipschitz. The quadratic remainder survives both +/-m crossings, including noninteger m. Z-changing rate is exactly lambda+d, yielding beta=17lambda/8 and q=7/8 with the correct signs.
- **Finite Poisson g, including R:** the invariant weights gamma^k are correct, the finite means increase to theta+1, and the prefix increments are negative. The terminal identity is -R t_(R-1)=R-mu. The zero extension has zero increments at R+1, while births from R contribute zero. The comparison to the actual chain has the correct rate/monotonicity directions.
- **Signed interfaces:** the exact identity uses the post-jump g. Both first-download cutoff ratios decrease, and g is nonnegative, so those interface errors are nonpositive even with unbounded a,b. Each departure has a positive interface cost bounded by 4ell G/D in total; arrivals cost lambda ell G/D. The separate coarse estimate LJ<=G(lambda+2d) handles small D.
- **All states and strict boundaries:** min(x,y)>=R+1 makes all current and successor corrections vanish, because g(R)=0. One-small/one-large states have d<=2R+1, qd>=y (or x symmetrically), and interface remainder at most one. The saturated and unsaturated cutoffs give LV<-3 and LV<=-3 respectively. Remaining visible counts are bounded and u controls a+b, giving LV<-1 past B. Equalities at R, R+1, N, gamma, eta, and B are assigned consistently.
- **All real fixed loads:** all constants are finite for every real lambda>0; R exists because the limiting mean exceeds theta by one. Integer rounding of R,N introduces no missing interval. The lambda=0 irreducibility endpoint is excluded; no uniformity or exchange of limits at infinity is required. Rational finite tests are explicitly not used to infer this universal statement.
- **True CTMC conclusion:** initial/arriving peers permit at most two later download transitions, giving at most 2*initial population+3*arrival count jumps on a finite interval. Seed-supported finite paths prove irreducibility. Localizing Dynkin at tau_F, time t, and population level M is valid on a finite set; discard nonnegative terminal V before Fatou, then take t to infinity. This yields E tau_F<=V(s). Local finiteness and bounded V on exit neighbors of finite F justify the continuous-time finite-set Foster conclusion.

The exact remaining mathematical gap found is **none**. This does not assert that an independent review can exclude every possible error; the full derivations and executable witnesses remain available for further checking.

## New finite exact evidence

`exact_falsification.py` and `exact_falsification_output.json` record **315,600 exact rational assertions**, 11,330 state evaluations, and 20 expected-failure diagnostics. Loads are 1/1,000,000 (R=54), 3/17 (R=60), 11/4 (R=157), and 55/8 (R=333). States include both orientations, support/region endpoints, exact ratio contacts and neighboring integer ratios, rounded interfaces, huge waiting rooms, and a+b immediately below/at/above B. The tests separately check the killed-system solution's terminal Poisson equation, the zero extension, every product identity, signed interfaces, generator upper bounds, coercivity, linear growth, and all applicable negative-drift cases.

The expected-failure controls expose these specific invalid replacements: unsmoothed absolute value with the same remainder; an absorbing top instead of the terminal death equation; extending a negative corrector slope past R; dropping departure interface cost (with an actual six-rate departure witness); and beginning the exact-zero region at min(x,y)=R. They verify diagnostic sensitivity and are not counterexamples to TURN_4. All mathematical assertions use exact fractions, including the very large N,B values.

## Fresh replays and frozen provenance

Every listed subprocess completed with exit code 0; no preexisting process or unsaved earlier result was assumed.

| Frozen control | Assertions/checks | Result |
|---|---:|---|
| turn1_checks.py | 48,049 | PASS |
| turn2_checks.py | 15,863 | PASS |
| turn3_checks.py | 6,032 | PASS |
| turn4_checks.py | 71,165 | PASS |
| independent_review_portable.py | 36,709 | PASS |
| verify_package.py | 72 | PASS |

The four author replay outputs equal their frozen saved outputs exactly. REPLAY_AND_SOURCE_INTEGRITY.json records every source SHA-256 and replay output hash. The 40 original files remain byte-identical to SOURCE_SNAPSHOT.json at PR head `1198534928f4c2bf8bf758c9ceb16edaa3a496e8`. TURN_4.md SHA-256 is `34e043b456ddc25cc37d86d3e5a39d10243de91c6a5d5002952252d2eab1b0fa`.

All new files are confined to this review folder. No Git, PR, spreadsheet, Zenodo, installed package, external communication, or unrelated-chat mutation occurred.
