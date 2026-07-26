# The γ–θ Conjecture in One-Guard Eternal Domination

This directory contains a 27-day, laptop-only research campaign on the
conjecture

> If \(\gamma(G)=\gamma^\infty(G)\), then \(\gamma(G)=\theta(G)\).

Here \(\gamma^\infty\) always means the standard **one-guard-moves** eternal
domination number: attacks occur only at unoccupied vertices and exactly one
guard traverses one edge to the attacked vertex.

## Campaign dates

- Day 1: 2026-07-25
- Day 3 review: 2026-07-27
- Day 7 review: 2026-07-31
- Day 14 review: 2026-08-07
- Day 21 review: 2026-08-14
- Day 27/final package: 2026-08-20

Finite verification or a graph-class theorem is a partial result, not a
resolution. A resolution requires a universal proof, a fully certified
counterexample, or a verified prior resolution.

## Trust architecture

- `src/verifier_a/`: bitset greatest-fixed-point implementation.
- `src/verifier_b/`: structurally independent colored configuration-digraph
  implementation.
- `src/search/`: exploratory and synthesis programs, kept separate from
  decisive checking.
- `math/`: self-contained proofs and adversarial reviews.
- `literature/`: source audit with an explicit model/variant ledger.
- `instances/`, `certificates/`, `results/`: immutable inputs, checkable
  evidence, manifests, and run logs.

No external person may be contacted on behalf of this project. If independent
outside verification would help, that need is recorded only as a research
note.

## Reproducibility status

The repository is under active construction. Consult `STATE.md` for the exact
verified frontier and `CLAIMS.md` for the status of every claim. The current
standard-library test suite is run from this directory with:

```text
python3 -m unittest discover -s tests -v
```

The pinned graph generator is installed locally with:

```text
tools/bootstrap_nauty.sh
```

The published 2022 catalog and its independent clique-cover certificates are
reproduced with:

```text
PYTHONPATH=src python3 -m search.validate_mmv2022 \
  --catalog instances/mmv2022_table9.csv \
  --parameters results/mmv2022_parameters.csv \
  --log results/logs/mmv2022-validation.json

PYTHONPATH=src python3 -m search.certify_mmv2022_theta \
  --catalog instances/mmv2022_table9.csv \
  --certificate-dir certificates/mmv2022_theta_k3 \
  --manifest results/mmv2022_theta_certificates.csv \
  --log results/logs/mmv2022-theta-certificates.json
```

The second command independently replays every saved proof when the
certificates already exist. It never silently replaces an invalid or
mismatched certificate.

The certified one-vertex-extension result (claim C-018) can be replayed
without rerunning or modifying the frozen search.  The first, read-only
command reconstructs all 110,537 labeled extensions and checks their 54,216
canonical-class receipts; the second checks every saved domination,
independence, and one-guard fixed-point certificate using the separately
written mathematical verifier:

```text
PYTHONWARNINGS=error python3 reviews/extension_coverage_hostile_probe.py

PYTHONPATH=src PYTHONWARNINGS=error python3 -m evaluation_checker \
  --verify-only
```

To regenerate that bounded search from the pinned 55-graph input catalog,
use:

```text
PYTHONPATH=src PYTHONWARNINGS=error python3 -m search.extension_killtest \
  --validation-gate-open \
  --batch-size 256 \
  --wall-limit-seconds 2700 \
  --memory-limit-mib 1024
```

The production search is transactionally resumable.  The replay commands are
read-only and check the installed artifacts against their recorded hashes
rather than replacing them.

Claim C-019, the complete one-edge-toggle search around the 391 closest
extensions, has the same two-layer replay:

```text
PYTHONWARNINGS=error python3 reviews/edge_toggle_coverage_hostile_probe.py

PYTHONPATH=src PYTHONWARNINGS=error \
  python3 -m edge_toggle_evaluation_checker --verify-only
```

The first command reconstructs all 25,641 labeled toggles and verifies their
19,136 canonical-class mappings.  The second independently proves
`gamma < gamma-infinity` for every class from the installed domination and
one-guard fixed-point certificates.

Claim C-020 gives a stronger local obstruction: when
`alpha=gamma-infinity=k`, every maximum independent set must survive two
adaptive attacks, not merely one.  Its compact private-region certificate
and the C-021 pruning measurements can be independently replayed with:

```text
PYTHONWARNINGS=error python3 reviews/two_step_transition_hostile_probe.py
```

That read-only probe imports no campaign evaluator.  It reconstructs the
8,587 selected edge-toggle rows and streams the complete connected-unlabeled
orders 5 through 9.  The resulting counts are labeled `OBSERVED`; they do
not exclude all graphs of order 10 or higher.

Claims C-022 and C-023 extend this to arbitrary finite online horizons and
to direct recursive third-ply certificates.  The independent replay below
imports no campaign module, checks all 518 failure trees, recomputes all
8,587 source profiles, and verifies the strict \(K_2/K_3\) witness on
\(C_{15}\):

```text
PYTHONWARNINGS=error python3 reviews/three_step_kernel_hostile_probe.py
```

To regenerate the source-bound measurement, the 518-tree stream, and the
\(C_{15}\) witness into their default paths, use:

```text
PYTHONPATH=src PYTHONWARNINGS=error \
  python3 -m search.three_step_kernel
```

These claims concern a precisely delimited edge-toggle-derived population.
They are not an exhaustive order-11 or order-12 nonexistence result.

The separate C-024 robustness observation exhausts the edge-toggle ball of
radius at most two around `Kun_w{vRrblV`.  Its read-only deep replay reruns
the pinned canonicalizer and both exact evaluator stacks on all 1,076
canonical classes:

```text
PYTHONPATH=src PYTHONWARNINGS=error \
  python3 -m search.deep_survivor_radius2 \
  --audit-result results/deep_survivor_radius2_measurement.json \
  --deep --labelg tools/nauty2_9_3/labelg
```

The result is intentionally labeled `OBSERVED`: the generator and coverage
audit are source-bound but not independently implemented, and the coloring
conclusions do not have SAT proof logs.

Claims C-025--C-027 package two small induced one-guard failure cores and
their exact role in the 526-row deep population.  The installed
certificate, result, and one-vertex-extension table are checked with:

```text
PYTHONPATH=src PYTHONWARNINGS=error \
  python3 -m search.portable_failure_core audit

PYTHONPATH=src PYTHONWARNINGS=error \
  python3 -m unittest -v tests.test_portable_failure_core
```

The two core profiles, ranked attack DAGs, six embeddings, and exact
37-of-526 occurrence statement are `CERTIFIED-FINITE`.  The broader
623-key one-vertex-extension classification remains `OBSERVED` because its
distinct canonical keys were not independently proved nonisomorphic.

The direct order-12, parameter-three CEGAR runner is frozen and
hostile-review accepted for bounded production.  Its engineering audit is
replayed with:

```text
PYTHONPATH=src PYTHONWARNINGS=error \
  python3 reviews/synthesis_k3_cegar_hostile_probe.py
```

Claim C-028 now certifies that the `hole9` branch is empty.  The production
runner failed closed before writing a terminal marker, so this is explicitly
a recovered exact-CNF certificate rather than a retroactive CEGAR terminal.
The installed package and the independently written standard-library RUP
checker are replayed with:

```text
python3 \
  certificates/synthesis_k3_hole9_orphan_000170_recovery/repro/hole9_orphan_recovery.py \
  audit \
  --package certificates/synthesis_k3_hole9_orphan_000170_recovery \
  --drat-trim tools/drat_trim_2023_05_22/drat-trim

python3 -I reviews/hole9_orphan_recovery_hostile/probe.py --compact
```

The accepted result binds two non-destructive documentation errata, the
sealed 23-file package, the outer certificate, and the hostile review in
`results/synthesis_k3_hole9_orphan_recovery_acceptance.json`.  The original
170-cut checkpoint remains `running` and byte-identical.

Claims C-030 and C-034 now certify that the `hole7` and `hole5` branches are
empty; together with C-017 and C-028, this proves C-035:

```text
No graph G on 12 vertices satisfies
gamma(G) = gamma-infinity(G) = 3 < theta(G).
```

The exact `hole5` run is frozen at commit `dff45f42`.  Its clean-room
post-run audit imports neither the production runner nor the synthesis core,
reconstructs the strengthened CNF, parses both binary proofs, strips
deletions byte-for-byte, and freshly invokes the pinned warning-fatal,
forward, RUP-only checker:

```text
PYTHONWARNINGS=error \
  python3 reviews/hole5_binary_production_postrun_hostile_probe.py \
  | shasum -a 256

# Expected canonical-output SHA-256:
# bd7693fdad225f733c0d2e704c4de45186324cc62ffdec09a112836ceec014e5
```

A separate package audit binds all 12 run files, the 23 runtime sources at
commit `6f3ef0a0`, both pinned tools and source archives, and the immutable
Git subtree:

```text
PYTHONWARNINGS=error \
  python3 reviews/hole5_binary_run_package_auditor.py \
  | shasum -a 256

# Expected canonical-output SHA-256:
# 470f58bf532ae8ff68ac3b8f096ba20166e6bcd91bee4924c1f924e276fea2cb
```

The complete implication from the three branch certificates to C-035 is in
`math/lemmas/order12_k3_exclusion.md` and received two independent
mathematical reviews.  This is a `CERTIFIED-FINITE` parameter slice.  It
does not exclude order-12 counterexamples with common parameter at least
four and does not resolve the universal conjecture.

The claim-level replay wrapper checks all accepted C5/C7/C9 bindings and,
when the live resource gates permit, freshly replays all three proof
branches:

```text
python3 -I -B repro/c035/replay.py --mode fast

python3 -I -B repro/c035/replay.py --mode full \
  --output /fresh/path/c035-full-replay.json
```

Fast mode is metadata-only and explicitly returns
`NO_MATHEMATICAL_CLAIM`.  Full mode promotes C-035 only after four exact
independent audit children succeed.  It refuses to launch under excessive
CPU load, low memory, or low disk space.

Claim C-036 gives the classical half-order reduction
\(n\geq2k+1\) for a connected counterexample.  Thus, after C-035, only
connected \(k=4,5\) remain at order 12.  Claim C-037 supplies the exact
connected \(k=4\) parent formula:

```text
PYTHONPATH=src python3 -B -m synthesis_k4.generate \
  --mode full \
  --output instances/order12_k4_connected_parent/instance.cnf \
  --manifest instances/order12_k4_connected_parent/manifest.json

python3 -B reviews/order12_k4_synthesis_target_hostile_probe.py
```

The retained full CNF has 18,381 variables, 114,742 clauses, and SHA-256
`adbe0c01614bae6cd3aed4ccdcd45a757ca56e7ef9c4f2f280f2d8ef200e40ac`.
It is accepted exact formula infrastructure.  The full parent remains open;
one of its 16 Boolean-cube leaves is now certified UNSAT as C-042 below.

Claim C-038 sharpens the order-12 parameter-four structural frontier.
If \(H=\overline G\) contains an induced hole, at least four vertices lie
outside that hole.  Together with the Strong Perfect Graph Theorem and the
accepted one-guard cycle values, every surviving \(H\) therefore contains
an induced \(C_5\), \(C_7\), or \(\overline{C_7}\).  The independent
boundary and one-guard probe is:

```text
python3 reviews/order12_k4_structural_split_hostile_probe.py
```

Claim C-039 adds necessary hub constraints to those three templates.  Hubs
of an induced odd hole are independent in \(H\); with \(r\ge2\) outside
vertices, at most \(r-2\) are hubs.  An induced
\(\overline{C_7}\) has no outside hub at all.  Thus the order-12
\(C_5,C_7,\overline{C_7}\) templates permit respectively at most five,
at most three, and zero hubs.  These statements do not exclude a template.
Their clean-room regression is:

```text
python3 reviews/order12_k4_hub_constraints_hostile_probe.py
```

Claim C-041 resolves the next incidence layer in the
\(\overline{C_7}\) template.  Outside vertices adjacent in \(H\) to exactly
six antihole vertices are pairwise nonadjacent in \(H\), all miss the same
rim vertex, and there are at most three of them.  Hence the subbranch with
four or five such near-hubs is empty, although the full
\(\overline{C_7}\) template remains open.  An independent
configuration-digraph implementation checks all local cases:

```text
python3 reviews/order12_k4_antihole_near_hubs_hostile_probe.py
```

The standalone decoded-candidate verifier is also accepted.  It imports no
synthesis or prior verifier core and conditionally proves
\(\gamma=\gamma^\infty=4<\theta\) from an explicit graph, literal eternal
family, and complete 65,536-row complement-coloring trace:

```text
PYTHONPATH=src python3 -m unittest -v \
  tests.test_verifier_k4_candidate

python3 reviews/order12_k4_candidate_verifier_hostile_probe.py
```

No candidate currently exists.

The proof-producing runner's exact 16-cube partition covers the anchored
parent.  Its accepted version-three implementation uses six separately
bounded processes: CaDiCaL binary-DRAT production, raw forward verification,
strict addition-only normalization, normalized RUP-only forward
verification, RUP-only backward LRAT conversion, and fresh `lrat-check`
replay.  The normalization step makes no proof claim; the two fresh RUP-only
checks and LRAT replay are mandatory.  The runner preserves interrupted or
rejected attempts as retryable nonclaims and aggregates even sixteen locally
verified leaves only as
`ALL_LEAVES_VERIFIED_PENDING_INDEPENDENT_COVERAGE_AUDIT`.

```text
PYTHONPATH=src python3 -m unittest -v tests.test_k4_production

python3 reviews/order12_k4_production_hostile_probe.py
```

The four pre-launch defects and a fifth campaign-subdirectory Git-binding
defect found by the first real initializer are documented in
`reviews/order12_k4_production_hostile_review.md`.  The latter initializer
failed before creating a run directory or starting a solver; both Git lookup
sites and an unmocked regression are accepted.

The historical v2 smoke test of leaf `1111` found a sixth protocol defect and
failed closed.  It remains frozen at
`results/order12_k4_production_seed0` with status
`LRAT_CONVERSION_REJECTED_NONCLAIM`; it was neither rewritten nor promoted.

The v3 runner deliberately rejects every v2 run manifest before acquiring a
run lock, including through its ordinary read-only audit command.  Historical
v2 attempt 1 remains auditable with the source-bound v2 verifier at commit
`9b24d9ff74b2bf9278d45f9bfdf08fcb7a31c800`; v3 never interprets a v2
attempt, outcome, or certificate under its newer schemas.

Claim C-042 certifies exactly the new v3 `1111` leaf, with cube units
`4,14,23,31`, and nothing larger.  Its 18,381-variable, 114,746-clause CNF
has SHA-256
`aafc85341993ed030fe72ba222a4efaa5a02f6ea6fa95519a9dd2ed755b94d1f`.
The retained raw proof was normalized to an addition-only RUP stream and
converted to LRAT; an independent postrun review reconstructed the leaf CNF
byte-for-byte and freshly replayed the LRAT on private copies.  The preserved
package is commit `92f5ed2b6db1e88ac5776bdb60ebcb6490b85c8d`.

The current exact histogram is one `UNSAT_LRAT_VERIFIED` leaf and fifteen
`PENDING` leaves, so the aggregate status is `INCOMPLETE_NONCLAIM`.  This is
not an exclusion of the connected \((12,4)\) parent, the order-12
parameter-four slice, or the universal conjecture.

The independent v3 aggregate verifier is now accepted for that exact
incomplete scope.  It imports no search, synthesis, runner, or earlier
transition core; reconstructs the 3,992,947-byte parent and all 16 leaves;
checks the 16 coverage rows and 120 pairwise conflicts; validates the exact
v3 schemas and retained proof chain; and freshly replays each completed LRAT
from private copies under an external append-only ledger.  Both author and
hostile ledgers return exactly
`INCOMPLETE_1_OF_16_VERIFIED_NONCLAIM`.  The hostile replay used the current
source set, launched one bounded `lrat-check` child and no CaDiCaL process,
then resumed without launching another child.

```text
PYTHONPATH=src python3 -m unittest -v \
  tests.test_verifier_k4_aggregate

PYTHONPATH=src python3 -B -m verifier_k4_aggregate \
  --run-dir results/order12_k4_production_v3_seed0 \
  --replay-dir /fresh/external/replay-ledger \
  --memory-mib 512 \
  --memory-reserve-mib 512
```

An incomplete audit deliberately exits with status 3.  Only a future
16-of-16 current-bound replay may return aggregate success, and the
mathematical parent-encoding theorem remains a separate obligation even
then.

Claims C-043 and C-044 give two independent hand reductions of that same
parent without rewriting the immutable production record.  Connectedness
and the accepted outer-signature order force \(e_{0,4}=0\), so all eight
`1***` leaves are logically impossible.  The full anchor \(S_4\) action,
including the matching color-name action on the complete coloring bank,
then shows that every remaining orbit has a sorted representative whose
first signature is one of

```text
0000  0001  0011  0111
```

The exact coloring-bank covariance was checked for all
\(24\cdot65,536=1,572,864\) anchor/color actions, and an independent probe
checked all 319,770 admissible eight-signature multisets.  Thus the parent is
satisfiable iff at least one of those four canonical cube leaves is
satisfiable.  The other four `0***` leaves are orbit-redundant rather than
individually certified UNSAT.  None of the four canonical leaves has yet
received a SAT or UNSAT certificate.

```text
python3 reviews/order12_k4_minimum_signature_hostile_probe.py

python3 reviews/order12_k4_anchor_signature_symmetry_hostile_probe.py
```

Claim C-045 strengthens that orbit reduction with a compact DoubleLex
breaker.  View the eight outer signatures as an \(8\times4\) binary matrix.
A row-major least representative of its \(S_8\times S_4\) orbit has both
nondecreasing rows and nondecreasing columns.  Sorting the four eight-bit
columns therefore preserves satisfiability of the exact parent.

The three auxiliary-free column comparators add 765 clauses and 10,758
literals, with no variables.  The independently reconstructed exact formula
has 18,381 variables, 115,507 clauses, 1,190,774 literals, and SHA-256
`14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7`.
The hostile audit checked all ten adjacent \(S_8\times S_4\) generators
against every one of the 114,637 pre-sort clauses, all 65,536 comparator
assignments, and the exact generated bytes.

```text
PYTHONPATH=src python3 -m unittest -v tests.test_k4_doublelex

python3 reviews/order12_k4_doublelex_hostile_probe.py
```

This is accepted equisatisfiable formula infrastructure.  By itself it is
not a SAT/UNSAT result and does not exclude the \((12,4)\) slice.
