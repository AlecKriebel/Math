# Independent adversarial audit of the T3-2 positive-recurrence manuscript

**Audit date:** 8 August 2026  
**Audited release:** `bimolecular_positive_recurrence_three_species_two_linkage.zip`  
**Claim:** positive recurrence for every finite bimolecular weakly reversible stochastic mass-action network with at most three dynamically active species and at most two active linkage classes, for every positive rate vector and every closed communicating class.

## Executive verdict

**The theorem is not yet certified.**

The finite combinatorial core reproduces and survives a clean-room third implementation. The deficiency-zero branch is mathematically standard and sound. The two exceptional service topologies appear sound after a minor endpoint correction.

However, the manuscript leaves several load-bearing infinite-state stochastic interfaces asserted rather than proved. The most serious are:

1. construction and normalization of escaping physical channel fluxes from killed Green occupations;
2. promotion to a terminal active-set/source-rate chart;
3. conversion of conditional same-linkage terminal drift into an unconditional negative shell episode after waiting for that linkage to fire;
4. construction of the finite effective process and uniform estimates in the one-active-coordinate case;
5. assembly of shell-dependent Dirichlet corrections into a proper global or Green-dual recurrence certificate.

These are substantive proof gaps, not stylistic omissions. I found no exact physical counterexample to the theorem, but the submitted proof does not currently establish it.

## Reproduction results

### T3-2 release

- Manifest: passed.
- Unit tests: `6 passed`.
- Direct C++ atlas: passed.
- Independent Python atlas: passed.
- PDF rebuild: passed.
- Reported PDF and verification hashes: matched.

### Clean-room third atlas implementation

A new implementation importing none of the release code independently reproduced:

- workload assignments: `187488`;
- shielded assignments: `446`;
- common-invariant assignments: `382`;
- deficiency-zero assignments: `60`;
- service assignments: `4`;
- unclassified assignments: `0`.

Files:

- `t3_2_audit/cleanroom_atlas_check.py`
- `t3_2_audit/cleanroom_atlas_check.out`

### Inherited two-species release

Its manifest and four Python tests passed, but `run_all.sh` then failed because the archive omits `src/exhaustive_boundary_supports.cpp`, which the script attempts to compile. This is a reproducibility defect in an inherited module. The T3-2 theorem should either remove this dependency and prove the lower-dimensional cases directly, or include a repaired and independently audited two-species package.

## Gate table

| Gate | Result | Assessment |
|---|---|---|
| Archive integrity and deterministic T3-2 replay | Pass | Certified |
| Four workload chambers/walls | Pass | Exact |
| Exhaustive `3^10` two-linkage assignment atlas | Pass | Independently reproduced three ways |
| Common affine-invariant feasibility | Pass | Exact rational linear algebra |
| Deficiency-zero product-form branch | Pass | Mathematically sound |
| Identification of two service architectures | Pass | Exact finite atlas |
| Strong-connectivity path enumeration for service systems | Pass | Exact finite enumeration |
| Service descent endpoint | Minor repair | Replace exact `-1` by `<= -1` where `0 -> 2C` may be the first positive path |
| Escaping Green occupation theorem | Not proved | Major load-bearing gap |
| Terminal chart compactification | Not proved | Major load-bearing gap |
| Fully active strict-flux contradiction | Conditional | Sound once the Green/chart theorem is supplied |
| Finite-shell linkage activation | Not proved | Major load-bearing gap |
| One-active-coordinate hierarchy | Not proved | Major load-bearing gap |
| Shell-dependent correction/Foster gluing | Not supplied | Major load-bearing gap |
| Final recurrence theorem | Conditional | Cannot be certified yet |

## Detailed findings

### 1. Green-flux construction is underdefined

The manuscript starts with normalized killed time-occupation measures and then asserts finite limiting physical channel fluxes satisfying

\[
\sum_e J_e(y'_e-y_e)=q,\qquad h\cdot q\ge 0.
\]

For unbounded mass-action rates, the integrated channel intensities need not be bounded under the time normalization. A second normalization by a channel/source-layer scale may be required. The proof must define that normalization, prove compactness of the normalized flux vector, retain the correct shell boundary terms, and show compatibility with the workload/source-rate chart. The current text does not do so.

### 2. A Green occupation is a measure, not a single divergent sequence

The proof repeatedly applies source-rate flags and active-coordinate language as though the escaping object were one state sequence. A normalized Green occupation may spread among multiple faces and rate-ratio regimes. A rigorous theorem must disintegrate or localize the occupation by capped phase and source-ratio chart, prove that a terminal component carries positive normalized flux, and show that transitions between omitted regimes appear as retained exit flux.

The current definitions of “active,” “promotion,” “terminal chart,” and “smaller rank” are descriptive rather than formal.

### 3. The finite-shell activation lemma loses the activation probability

After waiting for a reaction from linkage `L`, the conditional target-following episode may have expected reward tending to `-infinity`. But the full shell episode has reward approximately

\[
P(\text{activation before exit})\times
E[\text{terminal reward}\mid\text{activation}],
\]

plus the corrected exit terms.

The finite Dirichlet correction cancels the expected waiting reward; it does not by itself prove that the product above is bounded above by a fixed negative number. The activation probability may vanish with the shell. A rigorous proof needs either:

- a lower bound on activation probability relative to terminal rarity;
- a Green-flux argument showing that vanishing activation forces positive structural-exit flux;
- or a combined Dirichlet problem whose boundary values include the terminal reward and yield a uniform negative solution.

The submitted lemma proves only conditional negativity of the activation branch.

### 4. Shell corrections are not globally assembled

For each shell the finite function

\[
H_N(z)=E_z[F(Z_\sigma)-F(z)]
\]

is bounded. Boundedness on each finite shell is not enough. The paper invokes an inherited “shell-adapted Foster construction,” but supplies no theorem showing how the shell-dependent corrections, their oscillations, chart seams, and endpoint overshoots combine into one proper potential or an equivalent Green-dual contradiction.

This module must be stated precisely and its hypotheses verified.

### 5. The one-active-coordinate proof skips the effective-chain construction

The degree argument is promising and likely repairable:

- `2A` gives quadratic descent;
- without `2A`, linear sources do not increase `A`;
- bounded-rate births create an actual one-`A` carrier whose creator-linkage return path contains linear service.

But the proof does not construct the claimed finite generator, identify its recurrent and transient blocks, or prove the uniform `O(1/A)` interruption estimates. It also does not justify the claim that all unresolved failures live in a finite phase rather than an unbounded obligation count. The supplied verifier checks only elementary source-degree facts, not this stochastic hierarchy.

### 6. Service-system correction

For the linkage `{0,C,2C}`, a path from `0` to a positive complex may first reach `2C`. The resulting workload change is at most `-1`, not necessarily exactly `-1`. The descent conclusion survives after changing

\[
W_\tau=W_0-1
\]

to

\[
W_\tau\le W_0-1.
\]

### 7. The finite atlas is not the weak point

The four workload representatives are exhaustive for two active species with the third bounded. The exact assignment atlas, nullspace test, deficiency count, and service-template classification all replay correctly. Further enlargement of the atlas will not repair the stochastic gaps above.

## Required repair gates

Before theorem status can be restored, a revised proof should supply these explicit modules.

### Gate G1 — Green channel-flux compactness

State and prove a theorem deriving a finite normalized channel-flux object from infinite mean return, including:

- the exact finite volumes and workload bands;
- time and channel-flux normalizations;
- lower- and upper-cut flux estimates;
- compactness of all channel and chart fluxes;
- the vector balance equation;
- treatment of unbounded rates.

### Gate G2 — occupation-to-terminal-chart localization

Prove that the Green flux can be localized to a finite capped/support/source-rate chart with positive normalized flux, and that every omitted transition appears as lower-rank, support-promotion, or shell-exit flux.

### Gate G3 — unconditional linkage activation

Replace the conditional activation lemma by an exact killed-shell Dirichlet/Green theorem controlling activation probability, terminal reward, and exit reward together.

### Gate G4 — one-active finite-phase theorem

Write the exact finite phase, generator blocks, reward vector, Poisson corrector, interruption bounds, and zero-class invariant lift. Verify it for all two-linkage complex assignments or prove the general structural theorem.

### Gate G5 — shell correction and global closure

State a self-contained shell-adapted random-time Foster or Green-dual theorem and verify every hypothesis, including properness, seams, endpoint overshoot, physical duration, and trace-chain return.

### Gate G6 — inherited two-species dependency

Repair the missing C++ source and re-audit the two-species theorem, or remove the dependency from the T3-2 manuscript and prove all lower-dimensional cases inside the new paper.

## Recommended current status language

Use:

> **Candidate T3-2 theorem; finite workload atlas certified, analytic recurrence proof under revision.**

Do not use:

> **Outcome T3-2 established**

or submit the current manuscript as a proved theorem.

## Final conclusion

The release contains a strong and apparently correct finite structural classification. It does not yet contain a complete proof of positive recurrence. The theorem may still be true, and the remaining gaps appear targeted rather than diffuse, but they require new rigorous arguments rather than editorial expansion.
