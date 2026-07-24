# Round 11: X=12 profile challenge and unrestricted controls

Status: **NUMERICAL EVIDENCE ONLY — no 41–44 point kissing
configuration was found.**

## Question tested

The centered quarter-grid count relaxation has an exact strict-interior
shadow with
\[
E=(6,72,102,174,181,34,251),\quad X=40V=12,\quad Y=800D=-51.
\]
This experiment asked whether that shadow points toward a previously
missed rank-five geometric basin.

For every \(N=41,42,43,44\), two six-replica populations were run:

- a profile-guided population first matched a differentiable seven-bin
  edge histogram and the shadow's sorted row-square-energy profile, then
  removed **all** profile, row, and centering penalties for its final
  1,800 iterations;
- an unrestricted population minimized only a smooth maximum-inner-product
  objective.

Both populations included asymmetric Gaussian starts, perturbations of the
best stored unrestricted configuration, and a topology-changing start that
deleted the most crowded point and selected a new insertion from 4,000
asymmetric random candidates.  Adjacent-temperature replicas attempted 776
exchanges, of which 500 were accepted.  A zero-temperature release and a
separate direct minimax epigraph polish followed.

All coordinates in the artifacts are binary64 numerical data.  A maximum
below \(1/2\) would require a new exact or interval certificate; none was
found.

## Outcome

The best independently recomputed values are:

| \(N\) | previous benchmark | round-11 best | result |
|---:|---:|---:|---|
| 41 | 0.5149946525121660 | 0.5149946525121660 | unchanged |
| 42 | 0.5182411558622624 | 0.5182411558622624 | unchanged |
| 43 | 0.5247244770145227 | 0.5247244770145227 | unchanged |
| 44 | 0.5274711925359574 | **0.5274577123235293** | numerical improvement \(1.3480\cdot10^{-5}\) |

The 44-point maximum was also recomputed with 90-digit `Decimal` arithmetic
directly from the stored binary64 coordinates:

```text
0.527457712323529339161270992458020245620952789628301122292549495969944325923783878806716529
```

The maximizing pair is `(16, 20)`.  The coordinate SHA-256 is
`d862f8be8e94cbb9fb6923f5f3fe2e9518dadcd87375741de270116f25627612`.
This remains about `0.02746` above the kissing threshold.

## Basin analysis

At \(N=41\), the profile-lock phase reached a substantially closer shadow
descriptor but a poor maximum: its selected profile-blend representative
had maximum `0.5683832844788013`.  Once every profile penalty was released,
the best guided descendant reached `0.5161693537285631`; direct epigraph
polish then returned to `0.5149946525121685`.

That polished configuration has the same 153-edge near-maximum graph,
component sizes `35,1,1,1,1,1,1`, and degree histogram as the inherited
best basin.  Its sorted pair multiset differs only through the movable
tail.  Thus this run gives no evidence that the X=12 pseudomarginal
corresponds to a new competitive 41-point geometric basin.

At \(N=44\), both a profile-guided descendant and an unrestricted descendant
slightly improved the old benchmark.  The unrestricted value
`0.5274577123235293` is lower than the profile-guided value
`0.5274590715832641`; the improvement is therefore not evidence for an
X=12-specific basin.

## Minimum-tight-edge-cover block reinsertion

A second, materially different search deleted a **minimum vertex cover** of
every edge within \(5\cdot10^{-4}\) of the current maximum.  Thus no retained
complement pair belonged to the original near-contact graph.  Each deleted
vertex was reinserted from a separate asymmetric random cap, the whole
deleted block was optimized while its complement was frozen, all vertices
were released, and a direct minimax polish followed.  Four deterministic
restarts were run for each \(N\).

For the source tight graphs, exact finite graph searches independently
certify:

| \(N\) | tight edges | maximum independent set | minimum vertex cover | stress residual |
|---:|---:|---:|---:|---:|
| 41 | 153 | 15 | 26 | \(2.32\cdot10^{-16}\) |
| 42 | 175 | 15 | 27 | \(4.00\cdot10^{-16}\) |
| 43 | 172 | 15 | 28 | \(2.30\cdot10^{-8}\) |
| 44 | 190 | 16 | 28 | \(1.63\cdot10^{-16}\) |

The stresses are nonnegative least-squares tangent-equilibrium fits, not
exact stresses.  In particular, the \(N=43\) residual is visibly weaker and
none of these numbers proves a geometric obstruction.

No restart improved its source at the declared \(10^{-12}\) comparison
scale, and none reached \(1/2\).  Fourteen of sixteen retained tight graphs
are nonisomorphic to their source graph; in every such case a different edge
count is already an exact finite-graph witness.  The cutoff classification
has minimum binary64 clearance `1.2168715028737509e-05`.

Two features are worth retaining as numerical construction evidence:

- three \(N=42\) restarts returned to the source maximum within
  \(1.3\cdot10^{-15}\), while their 176- or 177-edge tight graphs are
  nonisomorphic to the 175-edge source graph;
- the best \(N=44\) restart recovered a tight graph isomorphic to the record
  source and a Gram matrix agreeing after relabeling within
  `8.44e-15`.  It did not beat the record.

At \(N=41\), one restart also recovered an isomorphic 153-edge graph at the
same numerical maximum, but its mapped Gram matrix differs by `0.0132`.
This indicates flexibility or nonuniqueness inside that near-contact
topology, not a better configuration.

## Global rigidity-mode topology escape

A third construction mechanism made no deletion or pointwise reinsertion.
For each source tight graph, its infinitesimal edge-rigidity matrix was
formed in \(4N\) tangent coordinates.  The ten global rotation directions
were removed, and 28 lowest-singular nonrotational directions supplied
coherent geodesic kicks to all points.  During the first 900 iterations,
an auxiliary penalty pushed the old tight edges below their previous
level.  The penalty was then set identically to zero for 1,400 iterations
before direct minimax polish.

At the declared \(10^{-9}\) singular-value threshold, an independent
calculation using different tangent bases gives:

| \(N\) | nonrotation dimension | numerical rank | numerical nullity | smallest singular value |
|---:|---:|---:|---:|---:|
| 41 | 154 | 130 | 24 | \(0\) to binary64 precision |
| 42 | 158 | 150 | 8 | \(1.61\cdot10^{-16}\) |
| 43 | 162 | 162 | 0 | \(4.23\cdot10^{-8}\) |
| 44 | 166 | 166 | 0 | \(1.9859\cdot10^{-2}\) |

These are numerical rigidity diagnostics, not exact rank certificates.  In
particular, the \(N=43\) graph has three very small singular values between
`4.23e-8` and `2.87e-7`; declaring it exactly rigid would be unjustified.
The \(N=44\) source is much better separated numerically from a
nonrotational flex.

Again, no restart improved its source or reached \(1/2\).  Nine of sixteen
retained tight graphs are nonisomorphic to their source, each witnessed by
a changed edge count.  Small \(N=41\) kicks returned to the flexible
153-edge topology and the same numerical objective; small \(N=43\) kicks
returned within about `6e-7` in mapped Gram distance; and small \(N=44\)
kicks recovered the record orbit within `1.1e-14`.  Larger kicks changed
topology but worsened the objective.

## Reproduction

The recorded environment used Python 3.14.6, NumPy 2.5.1, and SciPy 1.18.0.
From the repository root:

```sh
./.venv/bin/python \
  experiments/construction_round11_x12_profile/search.py \
  --n 41 42 43 44 \
  --replicas 6 \
  --scale 1.0 \
  --seed-base 2026072400 \
  --output \
  experiments/construction_round11_x12_profile/results/portfolio.json

./.venv/bin/python \
  experiments/construction_round11_x12_profile/epigraph_polish.py \
  --maxiter 900

./.venv/bin/python \
  experiments/construction_round11_x12_profile/verify.py

./.venv/bin/python \
  experiments/construction_round11_x12_profile/verify_polished.py

./.venv/bin/python \
  experiments/construction_round11_x12_profile/block_reinsertion.py

./.venv/bin/python \
  experiments/construction_round11_x12_profile/block_topology.py

./.venv/bin/python \
  experiments/construction_round11_x12_profile/verify_block_reinsertion.py

./.venv/bin/python \
  experiments/construction_round11_x12_profile/test_block_reinsertion.py

./.venv/bin/python \
  experiments/construction_round11_x12_profile/flex_topology_escape.py

./.venv/bin/python \
  experiments/construction_round11_x12_profile/flex_topology.py

./.venv/bin/python \
  experiments/construction_round11_x12_profile/verify_flex_topology_escape.py

./.venv/bin/python -m unittest \
  experiments/construction_round11_x12_profile/test_flex_topology_escape.py -v

./.venv/bin/python -m unittest discover \
  -s experiments/construction_round11_x12_profile \
  -p 'test_*.py' -v
```

The first search uses deterministic seeds
\[
2026072400+100(N-41)+b,
\]
where \(b=0\) is profile-guided and \(b=1\) is unrestricted.

The independent verifier does not import the optimizer.  It recomputes 56
stored phase representatives and all 12 epigraph-polish records, checks
unit norms, frame spectra, every pairwise product, profile descriptors,
provenance hashes, schedules, seeds, deletion/insertion records, and replica
exchange activity.  Every maximum is computed both by a Gram matrix and by
an explicit scalar dot-product loop.  Five baseline/tamper tests pass under
normal Python, and both verifiers also pass under `python -O`.

The block verifier additionally recomputes exact maximum independent-set
sizes with a second Bron--Kerbosch implementation, checks every tangent
stress equation directly, verifies graph-isomorphism mappings, uses
edge-count witnesses for every nonisomorphism claim, and recomputes the best
stored binary64 dot products as exact rational numbers.  Its exact graph
search is tested against brute force on 270 small random graphs.  Five
tamper cases are rejected, and a separate test confirms that changing a
solver-success flag does not affect verification.

Artifact SHA-256 values:

```text
38860d86b4df9eacf0c2c27c18a76cfa0a8012df6f83e6d53c4ef0328ca86c76  results/portfolio.json
091c451b30a733123c5ebcda9da9ed80bd910b640aa1a6b0d1cd0eabad788b72  results/epigraph_polished.json
56cd11c284f9471df75af2cb77e8a6cb8cfe13372ad570f71d233149cda5f38c  results/block_reinsertion.json
962a03d83a10f39a938d7693145bc96a71eabee138ae5108db487560226420e4  results/block_topology.json
99ced8d38911388276d9c534b254f751ca6498d3c05e60626357bde7615902cc  results/flex_topology_escape.json
54f87082ccd5633435c7bde5c9daa79a29e7c02ed029e1cc5cf5839ca825ce03  results/flex_topology.json
```

Failure to improve \(N=41,42,43\), or failure to cross \(1/2\), proves no
upper bound.
