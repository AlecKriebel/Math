## Accepted restricted result

This authored prose edition proves a sufficient fixed-rank-block criterion
for simultaneous lower and upper matroid degree bounds. For block
incidence κ, one basis satisfies both sides within additive κ−1 and costs
at most L. When κ≤Δ, this gives the requested additive Δ−1 on the stated
restricted class. The same-basis complement reduction is proved fully.

L is the LP optimum AFTER ceiling/floor normalization of rational degree
bounds, not the weaker unrounded rational-bound LP. Original integral
feasibility gives L≤OPT. Finite rational costs can be negative.

Canonical exchange components are the finest fixed-rank blocks and are
pointwise incidence-minimal only in the stated indexed anchor-complement
model retaining every original upper row. This does not exclude pruning,
merging duplicates, linear combinations, face restriction, or other methods.

The tight-face extension uses a direct sum of successive matroid minors.
It returns an original basis costing at most a specified feasible LP point.
For a chosen optimal point with face incidence at most Δ, the desired
restricted guarantee follows. The complete polynomial tight-set preorder
and maximal-chain construction are included. There is no guarantee of
finding a favorable point by searching all LP optima.

## Complete proof and accepted dependencies

The complete upper-only Király–Lau–Singh argument is reproduced with
attribution, including the equality-case linear dependence and the
selected-cost-plus-residual-optimum invariant for negative costs. It needs
LP feasibility, not an exactly degree-feasible integral basis.

Standard polynomial submodular minimization, rank-polytope separation,
and rational LP optimization/basic-optimum extraction are accepted oracle
dependencies. They are neither re-proved nor implemented by this edition.
The general proofs are complete subject to those stated standard tools.
No substantive proof correction was required by the independent audit.

## Historical finite evidence and reproduction limit

The graphic K5 example was separately checked to show that a face can
satisfy the criterion when the original matroid does not. The KLS example
was separately checked as a stalled elementary-rounding instance with a
unique fractional optimum. A checked relaxed-basis convex decomposition
shows cost-preserving existence relative to that point for every linear
objective. The stalled vertex does not refute the target guarantee.

The independent historical audit checked all 125 graphic bases, all 64
specified face bases, all 1,024 graphic rank subsets, all 96 KLS bases,
and all 4,096 KLS rank subsets. Additional controls covered normalization,
LP-only feasibility, negative costs, equality dependence, and boundary
coordinates. Normal, -O, and -OO runs passed, including 36 negative and
6 positive controls. Candidate programs were not imported or executed
by the independent audit.

Numerical instance definitions, coordinates, explicit finite witness and
basis lists, matrices, detailed tables, raw certificates, executable code,
and copied source documents are omitted. The omitted augmented exemplars
are not self-contained or computationally reproducible from this edition
alone. They are supporting evidence, not premises of the general theorems.
Preparation performed editorial and byte-integrity checks only, without
new mathematical executions or scholarly-source inspection.

## Sources, status, and remaining question

Tamás Király, Lap Chi Lau, and Mohit Singh,
[*Degree Bounded Matroids and Submodular Flows*](https://doi.org/10.1007/s00493-012-2760-6),
Combinatorica 32(6), 703–720 (2012), supplies the established upper-only
rounding result and Remark 1 obstruction. Public author PDF:
https://cs.uwaterloo.ca/~lapchi/papers/submodular.pdf .

Kristóf Bérczi, André Berger, Matthias Mnich, and Roland Vincze,
[*Degree-Bounded Generalized Polymatroids and Approximating the Metric Many-Visits TSP*](https://arxiv.org/abs/1911.09890v2),
provides related two-sided 2Δ−1 and one-sided Δ−1 context. Egres Open's
[*Bounded degree matroid basis*](https://oldlemon.cs.elte.hu/egres/open/Bounded_degree_matroid_basis)
is the retained target formulation, not current-status certification.
SOURCES.json records retained source identities and historical inspection.

The unrestricted simultaneous additive Δ−1 guarantee remains unresolved
by this work when the criterion fails. No novelty, priority, exhaustive
literature survey, hardness theorem, or general counterexample is claimed.
This AI-assisted work is unrefereed. Acceptance means an independent
internal AI audit, not external human peer review, journal acceptance,
or formal proof-assistant certification.

Exactly eight authored proof/audit/acceptance/provenance/verification
files are added under unsolved_math_prioritization/attempts/3000008.
QUEUE.md and unrelated paths are unchanged. Private coordination and
private personal data are excluded.

Base commit: `4b27092a448d53b61408355ce44ec38d103a1ce4`.

## Exact public-file identities

- `ACCEPTANCE.json`: 3,233 bytes; SHA-256 `6b5762cd970f3bfe4f651594ab2c384c9e6dc781df5d8df92e336bfa4593bec7`.
- `ACCEPTANCE.md`: 4,213 bytes; SHA-256 `3108fdec1d5a6980311fbe248451bf427adff4232e6138a1c4ca93b6742991fd`.
- `AUDIT.md`: 16,693 bytes; SHA-256 `5865b2e0491097ebeaeb022a523ec0759afaad3126d4120362932bd0581eec4f`.
- `MANIFEST.json`: 1,346 bytes; SHA-256 `58d1d578128714eff0885b099faae1ff4278db926e271c005b232b108d37b5b0`.
- `PROOF.md`: 21,073 bytes; SHA-256 `c3357bea796c775cdff5003116536acbf97e015753746ee53c2625301a063b34`.
- `README.md`: 2,458 bytes; SHA-256 `dcbf21f4692e27c032d58359eec4d5a290c14e47c380925fa11b3a7777be4dd5`.
- `SOURCES.json`: 4,146 bytes; SHA-256 `f668ee7b4c2050dbf7462b073394555767593fa736663e232690b5076bb517f9`.
- `VERIFICATION.json`: 3,608 bytes; SHA-256 `d64eca9680bc1d0a98d290395634f2605fa24f4413470decfce9c9bd25b93bf1`.

MANIFEST.json lists all eight members and hashes the other seven; this body independently pins its digest.

