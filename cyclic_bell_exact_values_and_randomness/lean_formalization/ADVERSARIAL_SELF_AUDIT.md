# Adversarial/source-Fourier continuation — self-audit

**One assistant wrote the source, arithmetic tests and this inspection. No
independent agent or Lean kernel checked this package.** The incoming archive
is preserved by its SHA-256 and a local baseline commit, not assumed correct.

## Source correspondence

The manuscript `sec:framework` defines finite tripartite strategies with Eve's
POVM, full-extended-correlation closure and three commuting party families.
`eq:gval-model` conditions the marginal Bell score on the model's actual optimum.
The new definitions implement those objects directly. Extended success is the
sum of r(a,b,g) along g=(a,b), not the largest unconditional AB probability.

The finite model allows arbitrary normalized mixed states on `(A x B) x E`,
zero AB PVM effects and arbitrary positive complete Eve effects. The sandwich
formula is proved equal to the product Born expression. The actual vectorized
positive density square root provides a complete three-party commuting
realization, preserving every complex/real probability component. No generic
Qqa-subset-Qqc theorem or assumed embedding is used.

The qa closure is taken before score equality, and contains only limits of full
finite extended behaviors. This prevents replacing the domain by all possible
extensions of a marginal, or by closure of the already saturated family.
Normalization and nonnegativity are closed pointwise conditions, so the success
is bounded by one on every relevant domain. Physical members prove nonemptiness
before the real sSup laws are applied.

For fixed finite Eve space, general POVMs are parameterized by square Gram
factors. Normalization bounds each entry using the exact Frobenius trace and
cardinality of the actual Eve space. The compactness proof has no qubit-specific
radius/ambient dimension. It yields an attained maximum and preserves the full
AB behavior when Eve is replaced. The finite-q nested-supremum theorem thus does
not rely only on an informal claim that maxima exist.

The d=4 literal all-dimensional estimate is 1/12, while the actual swapped table
supports 3/32. These were separated and tested rather than conflated. The new
entropy endpoints are upper bounds and do not claim exact worst-case entropy.
The concrete scalar Bell maxima still come from the earlier independent
bound/attainment chains, not from the new validity definitions.

The source appendix uses the integer triangular exponent k(k+1)/2. Both Fourier
sums and the negative qutrit term retain matrix order and complex phase. Their
proof candidates are explicitly not a complete source-polar strategy theorem.

## Defect found in the incoming source

`GeneralScalar` referenced `dimension_pos` at four locations without importing
its provider, `GeneralWitness`. Moving the unchanged lemma to `GeneralFourier`
repairs this source-order error without pulling a witness into the bound.
The original locations are recorded in `logs/adversarial_incoming_reference_error.json`.
The new lexical reference scanner detects a reconstruction of that error,
missing imports, same-file forward references and selected qualified-name errors.
It cannot verify Lean elaboration, local shadowing or arbitrary API spellings.

## Repairs during this pass

An initially drafted Gram-surjectivity statement attempted to refer to a proof
inside the second conjunct. It was replaced before delivery by the explicit
condition `exists L, EveGramValid L and forall g, eveGram(L_g)=Q_g`, so no
normalization proof is assumed by a tactic while forming the statement.
Source Fourier proofs now expose the natural-to-integer cast bridge and prove
sine denominators positive. A missing appendix import was caught by the new
reference checker and fixed in the new module.

These are source inspections, not a claim that all other errors are absent.
Offline repairs may involve substantive mathematical and API work.

## Test interpretation

New exact ABE tests use general nonprojective Eve POVMs, unequal local dimensions,
rank-deficient and full-rank states, actual partial traces, fixed-guess effects
and full lifted actions. A recorded uniform AB distribution with perfectly
correlated Eve detects the false uniformity-implies-privacy inference.

Source coefficient tests reconstruct sines in rational cyclotomic arithmetic,
verify the DFTs and qutrit expression and test wrong signs/normalizations. They
also check finite source matrix unitarity/order, but that finite evidence does
not fill the explicitly missing general source-polar identification.

A separate exact trine ensemble tests positive Gram factors, normalized general
POVMs, primal success and a positive dual gap. It is not a cyclic Bell maximizer
and is not imported as Lean evidence. The tests share retained arithmetic
implementations and are not independent-agent work.

The reporting tests use mocked subprocess outputs for axiom/negative-control
logic. No mocked success is described as a real compiler result. Current exact
counts and executed commands are recorded in `CONTINUATION_REPORT.json`.

## Unfinished verification and source

All Lean scripts require a pinned clean build, actual transitive axiom reports,
physical positive/negative controls and independent manuscript validation.
The generic Qqa-subset-Qqc/GNS argument, full source-polar identification and
standard/anchored probability-table asymptotics remain unwritten endpoints.
There is no worst-case adversarial optimization or full maximizing-face claim.
