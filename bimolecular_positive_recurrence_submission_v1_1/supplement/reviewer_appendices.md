# Reviewer supplement: trace-chain, physical-time, and computational interfaces

This supplement retains technical details moved from the Version 1.1 main
paper during compression. The substantive finite-trace and
embedded-chain-to-CTMC propositions, including their proofs, remain in the
manuscript. The material below records edge-case and reproducibility
interfaces that may be useful during review.

## 1. Trace-chain and physical-time details

### Labelled-channel marking

The augmented state records the target of the actual labelled channel that
fired. If two channels have the same population displacement but different
sources or targets, their post-jump populations can agree while their carried
targets or transition probabilities differ. They therefore remain separate.
Only channels with identical source and target may be aggregated.

### Nonemptiness of the Foster set

The finite set $K$ in the episode-drift construction is nonempty, not merely
finite. The global-minimum argument is pathwise: the residual log-factorial
potential has a global minimum, and every possible episode endpoint has
potential at least that minimum. No optional-stopping or integrability claim
is needed at this step because every episode has uniformly bounded finite
length.

### Hitting versus positive return

The trace-chain proof distinguishes first hitting from positive return. From
$k\in K$, one ordinary jump is taken before the next hit of $K$, so the
resulting return time is positive. There are only finitely many successors of
states in $K$, and the endpoint-chain drift estimate gives finite expected
hitting of $K$ from each successor. The finite trace chain is considered
only after this step. A uniform finite-block chance of reaching one selected
trace state gives finite expected positive trace return; the random trace
excursions are then expanded into ordinary embedded jumps using the strong
Markov property and Tonelli's theorem.

### Nonexplosion in physical time

The population embedded chain is constructed before nonexplosion is known.
Positive recurrence supplies a population state $x_*$ visited infinitely
often. At each visit, the following holding time has the same exponential law
with one fixed finite rate. The strong Markov construction makes these
holding times independent copies, and their infinite sum diverges almost
surely. Total physical time dominates this subseries, so jump times cannot
accumulate at a finite time. This recovers nonexplosion for the present
subclass; broader bimolecular weakly reversible nonexplosion is already known.

### Absorbing singletons

Absorbing singleton reachability classes are handled before channel
augmentation and carry their point-mass stationary laws. In a nonabsorbing
irreducible class every population state enables a genuine channel; otherwise
that state would itself be absorbing, and symmetry of accessibility would
force its reachability class to be the singleton.

## 2. Computational verification boundary

The accompanying dependency-free Python package performs deterministic,
exact-arithmetic checks of the falling-factorial identity and
source-probability rewrite. It also tests state-cycle lifting and accessibility
symmetry on finite calibration networks, scalar-envelope branch conditions
and monotonicity, the bimolecular top-complex classification with independently
validated witnesses, absorbing-singleton handling, the corrected
$\kappa_2\downarrow0$ rate-example limit, the exact logarithmic coefficient,
the exact ACK Example 4.1 comparison when retained in the paper, and
stationary return-cycle normalization on a finite chain.

The reproducer runs the complete test suite, emits the canonical report twice,
requires those reports to be byte-identical, and compares the result with the
committed report. Environment information is recorded separately so that it
does not destabilize the canonical JSON.

These computations are falsification and regression aids. No finite atlas
proves the universal theorem, no random test proves recurrence, and no
computation enumerates the analytic Foster set $K$ or certifies a useful
bound on its cardinality, location, or diameter. Those universal conclusions
come only from the manuscript's analytic argument.

## 3. Reproduction pointers

Run the complete verifier from the release directory with:

```bash
cd code
./reproduce.sh
```

The canonical output is `code/verification_report.json`; an identical durable
copy is retained as `supplement/verification_report.json`. The clean-clone
console transcript and environment record are under `validation/`, and the
release manifest is `supplement/MANIFEST.sha256`.
