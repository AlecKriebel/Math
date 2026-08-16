# Gate A adversarial review: Omega, Theta, and the 2025 theorem

Timestamp: `2026-08-02T10:57:33-07:00`

Reviewer role: independently try to falsify the proposed Gate A correction.
The review used exact graph enumeration and exact rational/quadratic-field
arithmetic. No numerical sampling is used as evidence.

## Executive verdict

| Claim | Verdict | Finding |
|---|---|---|
| Omega is an exact full-dimensional JC ambiguity on the encoded networks. | **VERIFIED** | All 64 zero-sum Fourier coordinates, the rational correspondence, strict JC `Theta_0` membership, rank-nine lower certificates, and the rank-nine upper bound replay exactly. |
| The Omega source and target are distinct standard labelled semi-directed topologies. | **VERIFIED** | The two source rootings reduce to one mixed graph, the two targets reduce to another, and the source and target mixed graphs are nonisomorphic. |
| Omega is binary, level 2, and triangle-free after standard reduction. | **VERIFIED** | Each reduced graph has six degree-three internal vertices, one nontrivial blob containing the two reticulations, and simple-cycle lengths `4,4,6`. |
| Omega belongs to the 2025 paper's strongly tree-child semi-directed class. | **FALSE** | Vertex `U` is the tail of two retained reticulation arrows and has only one incident undirected edge. Each reduced graph has seven admissible rootings, only two tree-child. |
| Omega contradicts Theorem 3.2 of Englander et al. | **FALSE** | The exact failed hypothesis is **strongly tree-child**. Omega otherwise meets the binary, triangle-free, and level-2 hypotheses. The correct Gate A outcome is `OMEGA-B`. |
| The inherited Theta pair is an exact full-dimensional JC ambiguity. | **VERIFIED** | A second direct engine checks all 64 coordinates at the quadratic common point, strict JC `Theta_0`, nonzero rank-eight minors, and all six generic invariant pullbacks on both sides. |
| The Theta source and target are distinct standard labelled semi-directed topologies. | **VERIFIED** | They are nonisomorphic even as labelled underlying graphs. |
| The inherited Theta pair belongs to standard strongly tree-child `L_1` or `L_*`. | **FALSE** | Vertex `A` is the tail of arrows to reticulations `C,F` and has only one undirected incident edge. Each topology has five admissible rootings, only two tree-child. |
| The Gate A correction is valid as written. | **VERIFIED AFTER CORRECTION** | Its mathematics is correct. One requested artifact name was absent and had to be replaced by the actual certificate path documented below. |

The attempted falsification found no mathematical counterexample to the Gate A
correction. It did find the artifact-name discrepancy and a harmless wording
difference between the 2025 and 2026 semi-directed reduction definitions.

## 1. Artifact identity and independence

**VERIFIED AFTER CORRECTION.** The requested file
`certificates/jc_omega_exact_isomorphism.json` does not exist in the repository.
The audit scripts and detailed Omega certificate use:

```text
certificates/jc_omega_move.json
sha256 c0b8f907d557d23169a2e132d7a85b789d6fa3fe03d4d90bab286eec206e960f
```

The inherited Theta encoding is:

```text
certificates/theta_pair_networks.json
sha256 f38577ad38a7d5ae858ac7804f2449bc0523573a412e5bf5a6d9c6a55344af35
```

I inspected the existing independent scripts, then wrote a separate
cross-check that imports none of the original discovery code and none of
`AUDIT/INDEPENDENT_IMPLEMENTATION`. It independently implements:

- rooted bidegree, DAG, reachability, and lowest-stable-ancestor validation;
- mixed-edge construction and exhaustive standard suppression;
- labelled mixed-graph isomorphism by direct internal-vertex permutations;
- admissible rooting enumeration and rooted tree-child testing;
- direct displayed-tree JC Fourier evaluation;
- exact Jacobian determinants by multilinearity;
- exact arithmetic in `Q(beta)`; and
- generic pullbacks of the six inherited Theta invariants.

The reviewer implementation and deterministic output are:

```text
AUDIT/REVIEWS/gate_a_crosscheck.py
sha256 fce241c14c45cba9a95f8bc92cd38df68d80ebc602a38c6f8e46a9efda1aff80

AUDIT/REVIEWS/gate_a_crosscheck_output.json
sha256 651b42e2c777b745711147f3a18b2435f4100eb5b1f51f93c24210a8f2272f02
```

Environment: Python `3.14.6`, SymPy `1.14.0`. The graph, rational Fourier,
quadratic-field Fourier, and determinant routines themselves use only exact
arithmetic.

## 2. Standard-definition check

**VERIFIED.** Definition 2.3 of the local snapshot
`AUDIT/PRIOR_WORK/englander_level2_v4.clean.txt` defines a semi-directed
network to be strongly tree-child when **every** directed network producing it
under Definition 2.2 is tree-child. The same paragraph states the equivalent
local characterization:

> every node with an outgoing edge has two incident undirected edges.

Theorem 3.2 then assumes an `n`-leaf, binary, triangle-free, strongly
tree-child, level-2 **semi-directed** network. The relevant source hashes are:

```text
englander_level2_v4.pdf
sha256 260a977d9629eeb1b9ea0b7afa6d8179625609748ce20a2007927df5aa6e874f

englander_level2_v4.clean.txt
sha256 6131867408b2f0067b9f78729d05781090aad75d5dac5053be2cd4858fe9e41c
```

**VERIFIED AFTER CORRECTION.** Englander et al.'s Definition 2.2 says to
undirect non-reticulation edges, retain reticulation directions, and suppress
the former root; the later standard definition in
`brits_full_identifiability_v2.clean.txt` additionally says to exhaustively
suppress resulting parallel edges and degree-two vertices. This wording
difference cannot affect either pair: after root suppression neither Omega nor
Theta has a parallel edge or any remaining unlabelled degree-two vertex. Thus
both definitions produce exactly the mixed graphs reported below.

## 3. Omega graph audit

### 3.1 Reduction and topology

**VERIFIED.** For census entry 16, suppressing root `S`, whose children are
`U` and reticulation `X0`, creates the retained arrow `U -> X0`. The other
reticulation arrows include `U -> V`. For entry 26, suppressing `S`, whose
children are `U` and reticulation `V`, creates `U -> V`, while `U -> X0`
already exists. The two reductions are isomorphic for a fixed source
labelling and likewise for a fixed target labelling:

```text
N16_source  ~= N26_source
N16_target  ~= N26_target
```

The source is not isomorphic to the target in either presentation.

**VERIFIED.** A human-readable nonisomorphism certificate is available in
addition to exhaustive canonicalization. Leaf labels force the source
attachment vertices

```text
P1_0, P1_1, P4_0, X0
```

to map respectively to target attachment vertices

```text
P1_1, P1_0, X0, P4_0.
```

Adjacency then forces the underlying-theta endpoint reflection `U <-> V`.
That reflection maps source reticulations `{V,X0}` to `{U,P4_0}`, not to the
target reticulation set `{V,X0}`. It therefore cannot preserve arrowheads.

### 3.2 Binary, level, and cycles

**VERIFIED.** Each standard reduction has:

```text
internal degrees: all 3
reticulations: V, X0
nontrivial blobs: 1
reticulations in that blob: 2
simple-cycle lengths: 4, 4, 6
triangle count: 0
```

Every core edge lies on a cycle, while the four pendant edges are cut edges.
Thus the unique nontrivial blob contains exactly the two reticulations and the
network is level 2. No two-sub-blob or suppression artifact is needed to reach
the Gate A conclusion.

### 3.3 Strong versus weak tree-childness

**VERIFIED.** The selected rooted presentations are tree-child. This only
proves weak tree-childness of their standard semi-directed reductions.

At `U`, the reduced mixed graph has:

```text
outgoing retained arrows: U -> V, U -> X0
incident undirected edges: U -- P1_0       (entry 16)
                           U -- P0_0       (entry 26)
```

Therefore `U` violates the 2025 local criterion `(2 outgoing, 1 undirected)`.

The exhaustive rooting calculation independently finds, for each of all four
labelled presentations:

```text
admissible rootings: 7
tree-child rootings: 2
all rootings tree-child: false
```

The count is not load-bearing. An explicit accepted non-tree-child witness is
obtained by inserting the root in the pendant edge at `L0`. The resulting
rooted DAG is binary, acyclic, has the root as lowest stable ancestor, and has
`U` with the two reticulation children `V,X0`. Hence one valid witness alone
already disproves strong tree-childness.

### 3.4 Exact JC ambiguity

**VERIFIED.** The existing independent algebra replay and the reviewer engine
both directly enumerate displayed trees. At the certified point:

- all fourteen parameters of every presentation lie strictly in `(0,1)`, so
  the points are in standard JC `Theta_0`;
- all 64 zero-sum Fourier coordinates agree exactly; and
- the independent rank-nine minors are

```text
N16_source  -171/2305843009213693952000000
N16_target  -513/9223372036854775808000000
N26_source    57/576460752303423488000000
N26_target   189/2305843009213693952000000.
```

**VERIFIED.** `audit_omega_algebra.py` additionally checks 64 symbolic
identities for a nine-free-parameter rational correspondence. Its exact core
Jacobian rank is six. Four pendant-torus directions add at most four ranks,
and the checked Euler identity makes one of those directions dependent, so
the complete rank is at most nine. The minors above make it at least nine.
The common correspondence has rank nine at the interior point, establishing
a common regular relatively open subset of full model dimension.

## 4. Theta graph and model audit

### 4.1 Reduction and topology

**VERIFIED.** Suppressing `rho`, whose children are tree vertex `A` and
reticulation `C`, creates the retained arrow `A -> C`. The other retained
arrow from `A` is `A -> F`. The reduced core has internal degrees all three,
reticulations `{C,F}`, one nontrivial level-2 blob, cycle lengths `3,5,6`, and
exactly one triangle.

**VERIFIED.** The source and target are nonisomorphic even after all tree-edge
directions are discarded. A label-fixing isomorphism would have to fix `D`
(adjacent to leaf 2) and `F` (adjacent to leaf 3), while sending source `B` to
target `E` (leaf 1) and source `E` to target `B` (leaf 4). The source edge
`D--E` would then map to `D--B`, which does not exist.

### 4.2 Strong versus weak tree-childness

**VERIFIED.** The chosen rooted Theta presentation is tree-child, but its
standard reduction is not strongly tree-child. At `A`:

```text
outgoing retained arrows: A -> C, A -> F
incident undirected edges: A -- B
```

Thus `A` violates the local criterion. The independent rooting census gives:

```text
admissible rootings: 5
tree-child rootings: 2
all rootings tree-child: false
```

Again, an explicit witness is simpler than the census: insert the root in
`A--B`, orient it toward `A` and `B`, and retain the arrows into `C,F`. This is
a valid binary rooted DAG, but `A` has only reticulation children. Therefore
Theta is outside standard strongly tree-child `L_1` and `L_*`.

### 4.3 Exact JC ambiguity

**VERIFIED.** The reviewer engine reconstructed the inherited quadratic point
directly on `theta_pair_networks.json`. For the unique root `beta` in

```text
441/1250 < beta < 3529/10000
```

of

```text
43337075 beta^2 - 36083110 beta + 7336259 = 0,
```

it checked all 64 zero-sum Fourier coordinates in `Q(beta)`. The polynomial
has nonsquare discriminant, and rational interval inequalities certify every
edge multiplier and inheritance parameter strictly in `(0,1)`.

The selected rank-eight minors are nonzero:

```text
source  531441/16384000000000000000

target  97608431685933/382537302016000000000000000
      - (46892453833449/76507460403200000000000000) beta.
```

The target expression cannot vanish because that would make `beta` rational,
contrary to irreducibility of its quadratic polynomial.

**VERIFIED.** Independently generated generic JC parameterizations for both
labellings annihilate all six inherited equations. On the positive locus
`B*E != 0`, five coordinates reconstruct rationally and the only remaining
relation is `L^2=B*E*H`, giving local dimension at most eight. The nonzero
minors give dimension at least eight. The common point is smooth because the
derivative with respect to `H` is `-B*E != 0`. Each regular model image is
therefore locally open in the same smooth eight-dimensional sheet, proving a
full-dimensional regular stochastic overlap rather than merely one matching
point or equality of closures.

## 5. Literal reconciliation with Theorem 3.2

**VERIFIED.** Omega maps to the hypotheses of Englander et al. as follows:

| Theorem 3.2 hypothesis | Omega |
|---|---|
| same finite labelled leaf set | yes, four leaves |
| standard semi-directed phylogenetic network | yes |
| binary | yes |
| triangle-free | yes |
| level 2 | yes |
| strongly tree-child | **no** |

Consequently the unique Gate A conclusion is:

```text
OMEGA-B:
At least one network violates a stated hypothesis of the 2025 theorem.
In fact every encoded Omega source/target reduction violates the same
strongly-tree-child hypothesis at U.
```

**VERIFIED.** The 2025 theorem is not contradicted by Omega. No public-code
replay or extraordinary `OMEGA-D` protocol is required after the literal
hypothesis failure is proved.

**VERIFIED AFTER CORRECTION.** The inherited Theta ambiguity remains a valid
and exactly certified JC phenomenon for its standard semi-directed graphs,
but it cannot be used as a move *inside standard strongly tree-child*
`L_1/L_*`. Any downstream theorem that counts Theta as such a move must be
withdrawn or restated for a weaker “has a tree-child rooting” class.

## 6. Implementation stress checks and residual concerns

**VERIFIED.** I specifically checked the following possible failure modes:

1. Suppressing a root incident to a reticulation edge retains the arrowhead at
   the reticulation. Applying the opposite convention would not be the
   standard semi-directed reduction.
2. No later degree-two or parallel-edge suppression changes either example.
3. The existing rooting validator's lowest-stable-ancestor test is logically
   correct: it rejects an internal vertex whose deletion leaves no labelled
   leaf reachable from the root.
4. Splitting a retained reticulation edge as a candidate root location does
   not create false accepted witnesses; every accepted orientation is checked
   for binary bidegrees, acyclicity, reachability, and lowest stable ancestry.
5. Even if a different convention changed the total rooting count, the
   explicit non-tree-child rootings and local criterion already settle the
   strong-tree-child verdict.
6. Labelled isomorphism was tested by exhaustive internal-vertex bijections,
   with leaf labels and arrowheads fixed, and also has the manual obstructions
   above.

**UNRESOLVED.** This review does not determine what complete observational
move system survives *within* the standard strongly tree-child class. Its
scope is the Gate A correction only. It establishes that neither Omega nor
the inherited Theta pair supplies a non-triangle move in that class.

## 7. Exact replay commands

From the repository root:

```bash
cd /Users/alec/Documents/Math/strong_level2_phylo_identifiability

.venv/bin/python AUDIT/REVIEWS/gate_a_crosscheck.py \
  > AUDIT/REVIEWS/gate_a_crosscheck_output.json

.venv/bin/python AUDIT/INDEPENDENT_IMPLEMENTATION/audit_omega_graphs.py \
  certificates/jc_omega_move.json \
  > /tmp/reviewer_a_omega_graph.json

.venv/bin/python AUDIT/INDEPENDENT_IMPLEMENTATION/audit_theta_graphs.py \
  certificates/theta_pair_networks.json \
  > /tmp/reviewer_a_theta_graph.json

.venv/bin/python AUDIT/INDEPENDENT_IMPLEMENTATION/audit_omega_algebra.py \
  certificates/jc_omega_move.json \
  > /tmp/reviewer_a_omega_algebra.json

cmp /tmp/reviewer_a_omega_graph.json \
  AUDIT/INDEPENDENT_IMPLEMENTATION/omega_graph_audit.json
cmp /tmp/reviewer_a_theta_graph.json \
  AUDIT/INDEPENDENT_IMPLEMENTATION/theta_graph_audit.json
cmp /tmp/reviewer_a_omega_algebra.json \
  AUDIT/INDEPENDENT_IMPLEMENTATION/omega_algebra_audit.json
```

All commands completed successfully and all three `cmp` checks were byte-for-byte
identical.

## 8. Files added by this review

```text
AUDIT/REVIEWS/GATE_A_ADVERSARIAL_REVIEW.md
AUDIT/REVIEWS/gate_a_crosscheck.py
AUDIT/REVIEWS/gate_a_crosscheck_output.json
```

No other audit or discovery file was edited.
