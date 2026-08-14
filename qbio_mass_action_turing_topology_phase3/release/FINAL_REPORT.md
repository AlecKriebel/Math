# Phase III final report

## OUTCOME

**VALIDATED-TALG**

Every central theorem survived an independent reconstruction, exact and adversarial software testing, clean replay, and a current good-faith priority audit. No strengthening route reached an exact publication-significant theorem, so the result is not labeled STRENGTHENED-TALG. This outcome is an internal mathematical validation, not external peer review.

## CORE CHARACTERIZATION

Let an indexed finite classical mass-action network have source-complex matrix `Y`, stoichiometric matrix `Gamma`, and stoichiometric subspace `S = im Gamma`. It is weakly all-mobile stationary-Turing-admissible exactly when there exist

```text
v > 0,     Gamma v = 0,     h > 0
```

such that

```text
J(v,h) = Gamma diag(v) Y^T diag(h)
```

is Hurwitz on `S` and has a negative signed principal minor:

```text
(-1)^|I| det J(v,h)[I,I] < 0
```

for some nonempty species set `I`. The converse mass-action realization is `x_i* = 1/h_i` and `k_r = v_r/(x*)^{y_r}`. A positive diagonal-damping theorem converts the negative signed minor into strictly positive all-species diffusion with a positive real nonzero-mode eigenvalue. Necessity follows from the same determinant expansion.

The independent audit verified conservation-law splitting, basis invariance of the reduced Jacobian, direct mass-action differentiation, the principal-minor scaling identity, Routh-Hurwitz conditions, and both directions of the stationary-Turing equivalence.

A Boolean diagonal selector gives a polynomial-size existential-real encoding. This proves membership in the existential theory of the reals, not hardness or completeness for that class.

## NP-HARDNESS

Source problem: binary-encoded `PARTITION`.

For a padded input vector `a`, with `m=k^2`, the reduction starts from the open-cube family

```text
B(x,y) = [ -k(I+aa^T)    y   ]
         [     x^T       k beta]
```

and proves that it contains a Hurwitz matrix exactly for YES `PARTITION` instances. A one-parameter-per-row similarity lift preserves stability. A separate scaling-elimination theorem proves that arbitrary positive right diagonal scalings of the lifted family cannot create a stable realization for a NO instance. An exact row-segment mass-action construction realizes the entire positive steady-flux image as `R L(q)` with independent positive row scales. Every mass-action Jacobian is therefore similar to `L(q)D`, and a fixed positive diagonal entry supplies the negative singleton minor whenever a stable realization exists.

The reduction is polynomial-time, many-one, uses `3m+1` species and `8m+2` reactions, retains strictly positive rates and equilibrium coordinates, and has stoichiometric columns `+e_i` or `-e_i`. The audit independently checked all algebraic identities, both inclusions of the row-image theorem, exhaustive small `PARTITION` instances, and numerical attacks on exact NO instances.

The hardness is weak NP-hardness. The constructed source complexes have unbounded molecularity.

## FIXED-SPECIES THEOREM

For every fixed species count `n`, the decision problem is solvable in polynomial bit complexity in the reaction count and rational input length.

The proof uses the cone

```text
K = {v >= 0 : Gamma v = 0}
```

and its linear image in the fixed `n^2`-dimensional space of Jacobian factors. When `K` contains a strictly positive vector, positive fluxes project exactly to the relative interior of that image. Every extreme ray of `K` is a positive circuit supported on at most `rank Gamma + 1 <= n+1` reactions, so all rays have polynomial enumeration count and polynomial bit length for fixed `n`. Fixed-dimensional exact polyhedral conversion produces a relative-facet description, after which fixed-variable real-algebraic decision is polynomial in the input bit length.

Two independent circuit enumerators agreed across the full campaign, and exact decomposition tests covered zero and repeated columns, lower-dimensional and zero images, conservation laws, parallel reactions, and nonpointed image behavior. The theorem is an exact algorithmic result, not a finite topology classification.

## CERTIFICATES

- **YES existence:** a sample point with coordinates in an explicitly isolated real algebraic number field, checked against a network-bound polynomial system.
- **NO existence:** a Real Nullstellensatz identity for every principal branch, or for the selector-encoded system.
- **Verification:** finite exact arithmetic and polynomial identity checking.
- **Generation:** computable in principle by exact real-algebraic algorithms or exhaustive enumeration.
- **Size:** no polynomial certificate-size bound is claimed.
- **Practical release:** no complete arbitrary-network certificate generator is bundled, and raw instances may remain `UNRESOLVED` in software.

## PRIORITY

The closest prior families are:

1. fixed-J unstable-subsystem and additive-diagonal-stability results;
2. signed interaction-topology and network-atlas studies;
3. mass-action graph-theoretic necessary conditions for zero-eigenvalue Turing instability;
4. unstable cores and child-selection methods for parameter-rich kinetics;
5. fixed three-species stationary and Turing-Hopf inequalities;
6. sufficient spatial-instability conditions for networks with monomial steady-state parameterizations;
7. interval-matrix stability NP-hardness, which supplies the source family but not the mass-action realization or scaling-elimination steps.

The dated audit found no earlier theorem combining indexed arbitrary classical mass action, existential positive rates/equilibrium/diffusion, conservation-correct weak stationary scope, an exact iff formula, NP-hardness, fixed-species polynomial algorithms, and finite exact two-sided certificates. This remains a good-faith search conclusion rather than a guarantee. Direct complete access to MathSciNet and zbMATH records was incomplete, and the prepared specialist inquiries were not sent.

## STRENGTHENING

Reconnaissance was conducted on bounded molecularity, strong NP-hardness, existential-real hardness, robust primary stationary crossing, and a practical complete fixed-`n` solver. None produced an exact accepted strengthening.

- Bounded molecularity: no exact finite-rate gadget preserved the whole Jacobian family.
- Strong NP-hardness: no 3-PARTITION replacement closed the strict cube-gap proof.
- Existential-real hardness: no exact multiplication gadget was obtained.
- Robust crossing: numerical searches found no counterexample, but no theorem was proved.
- Practical fixed-`n`: exact cone preprocessing was implemented, but no complete bundled CAD backend was added.

## BIOLOGICAL SCOPE

- Classical mass-action kinetics only.
- All species diffuse with strictly positive coefficients in the central theorem.
- A designated-mobile extension is proved using a positive spectral parameter; the determinant-at-zero substitute is false.
- Conservation laws are handled by homogeneous stability on `im Gamma`, while nonzero spatial modes act on the full species-amplitude space.
- The result concerns weak stationary linear instability: a positive real eigenvalue for some nonzero mode.
- It does not require the stationary crossing to occur first, be simple, or be transverse.
- It does not exclude an earlier Turing-Hopf instability.
- It does not prove a nonlinear patterned state.
- It does not give a finite motif characterization.
- The NP-hardness construction uses unbounded molecularity.

## MANUSCRIPT

**Title:** *The Complexity of Stationary Diffusion-Driven Instability in Mass-Action Reaction Networks: Exact Semialgebraic Characterization, NP-Hardness, and Fixed-Species Algorithms*

- Main manuscript: 10 pages, `manuscript/main.pdf`.
- Supplement: 16 pages, `manuscript/supplement.pdf`.
- External theorem summary: exactly 2 pages.
- External proof skeleton: exactly 5 pages.

The manuscript uses “polynomial-time exact decision algorithms” rather than “finite classifications,” states the Level-5 conclusion only among the six representations considered, distinguishes complexity from criterion compactness, separates certificate existence from practical generation, and foregrounds the unbounded-molecularity limitation.

## SOFTWARE

Replay command:

```bash
cd /mnt/data/qbio_mass_action_turing_topology_phase3
bash release/one_command_replay.sh 2>&1 | tee release/replay.log
```

The independent verifier imports no inherited implementation. The final replay verifies frozen archive hashes, runs exact unit and mutation tests, executes all falsifier campaigns, checks compact YES/NO examples, rebuilds every PDF, audits references and page counts, checks the mandatory tree, and regenerates a SHA-256 manifest.

The inherited candidate package also replays successfully, but that agreement was treated only as a regression check.

## REMAINING RISKS

1. No external human specialist or peer reviewer has yet verified the proof.
2. The current priority audit may miss inaccessible, unpublished, differently indexed, or differently worded work.
3. The NP-hardness result is weak and uses high-molecularity complexes.
4. The software does not provide practical complete quantifier elimination or general Nullstellensatz generation.
5. The fixed-species theorem relies on standard fixed-dimensional polyhedral and real-algebraic bit-complexity results; specialists should scrutinize that interface.
6. The three most delicate original steps remain the open-cube strict gap, arbitrary-right-scaling elimination, and complete positive-flux row-image equality, even though each now has an independent proof and implementation.
