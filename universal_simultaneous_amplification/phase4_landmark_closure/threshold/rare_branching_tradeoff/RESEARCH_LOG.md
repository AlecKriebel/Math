# Rare-branching tradeoff research log

Date: 2026-08-08 (America/Los_Angeles)

No literature search or external contact was used.

## Starting target

Audit the conjecture, at `r=3/2`,

\[
 \overline x+\overline y
 \le {1\over3}+{1\over3}{n-2\over n-1}
\]

for the Bd and dB rare-mutant branching survival vectors on reversible
replacement matrices.  Only if proved was the route to be upgraded to
finite fixation.

## Exact outcome

- [FALSIFIED] A three-class search exposed a core--pendant separation
  mechanism.  It simplifies all the way to an unweighted graph: a clique on
  `3m+1` vertices with `m` pendant leaves attached to one clique hub.
- [EXACTLY CERTIFIED] At `m=25` (`n=101`), explicit positive rational
  subsolutions for the exact three-type branching maps have combined
  uniform mean above the conjectured bound by `4207/303000`.
- [PROVED] Along the full family, the Bd pendant survival converges to
  `(sqrt(85)-2)/9`, both dense-core survivals converge to `1/3`, and the dB
  pendant contribution vanishes.  The survival-sum excess converges to the
  exact positive constant `(sqrt(85)-8)/36`.
- [MECHANISM] Bd gain is carried by a positive-proportion low-temperature
  pendant class, while dB survival is retained by a disjoint
  positive-proportion dense clique class.  Separate Jensen bounds do not
  control this spatial separation.
- [FINITE-FIXATION STATUS] No correction theorem was obtained.  Since the
  branching upper target is already violated by a constant, no vanishing
  two-lineage correction can turn this premise into an asymptotic endpoint
  obstruction.  The branching counterexample is not claimed to be a finite
  fixation counterexample.

See `RARE_BRANCHING_COUNTEREXAMPLE.md` and
`verify_rare_branching_counterexample.py`.

