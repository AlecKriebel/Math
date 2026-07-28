# Evidence for the parameter-lifting hostile review

Date: 2026-07-28 (PDT)

## Frozen candidate

The review audited these exact candidate bytes:

```text
3af7934f2aa504943fa7e5c792689712c90afbc3cab4fca49bbdce9ea936f268  math/working/parameter_lifting_audit/NOTE.md
fb3bafb723621a47ee602e16da2d4e0086e47ffba110e5a66659530e892480c6  math/working/parameter_lifting_audit/RESEARCH_LOG.md
213b9d73090f52124f5189ee4b939ce5a3326bdb8428fec371b758a735e2d70d  math/working/parameter_lifting_audit/verify_abstract_countermodel.py
163cfe56c205cd55b4e3e65efd9d6221cd259cde1b427387d4de3ebb26760219  math/working/parameter_lifting_audit/checker_output.txt
d398b4c2ead725ab332fd16a5b8fbcb36d70b6a8f3092dfa6f413b33225e071e  math/working/parameter_lifting_audit/MANIFEST.json
```

The hashes recorded inside the candidate manifest match its four payload
files.

## Candidate-checker replay

From `gamma_theta_eternal_domination/`:

```text
python3 -I -B -W error \
  math/working/parameter_lifting_audit/verify_abstract_countermodel.py
```

The replayed stdout has SHA-256

```text
163cfe56c205cd55b4e3e65efd9d6221cd259cde1b427387d4de3ebb26760219
```

and exactly matches the frozen `checker_output.txt`.

## Independent checker

Run:

```text
python3 -I -B -W error \
  reviews/parameter_lifting_hostile/independent_check.py
```

Exact stdout:

```text
PASS: independent parameter-lifting hostile controls
small equality_graphs=375 eternal_families=663 frozen_projections=12960 gl_controls=2129 global_list_checks=2129 inactive_suspensions=6710 labelled_graphs=1099 reference_states=2129 restoration_checks=12347 static_palette_colorings=6480
abstract k=3 n=4 m=3 slices=7 cliques=7 omega=2
abstract k=4 n=5 m=7 slices=15 cliques=15 omega=3
abstract k=5 n=6 m=12 slices=31 cliques=31 omega=4
abstract k=6 n=7 m=18 slices=63 cliques=63 omega=5
abstract k=7 n=8 m=25 slices=127 cliques=127 omega=6
abstract k=8 n=9 m=33 slices=255 cliques=255 omega=7
abstract k=9 n=10 m=42 slices=511 cliques=511 omega=8
abstract k=10 n=11 m=52 slices=1023 cliques=1023 omega=9
abstract k=11 n=12 m=63 slices=2047 cliques=2047 omega=10
```

The stdout SHA-256 is recorded in `MANIFEST.sha256`.

## What the bounded checker reconstructs

For every labelled graph through order five it independently computes:

- domination number by exhaustive subsets;
- independence number by exhaustive subsets;
- clique-cover number by exact clique-partition dynamic programming;
- the greatest one-guard eternal kernel by greatest-fixed-point deletion;
  and
- every nonempty optimal eternal subfamily by exhaustive subset testing.

For every equality graph, every optimal eternal family, and every independent
maximum state, it checks the restoration inclusion directly.  For every
nonempty proper anchor face it reconstructs both projected vertex sets and
both restricted families from the definitions, then checks domination,
one-guard closure, \(\gamma\), \(\alpha\), \(\gamma^\infty\), and
\(\theta\).  Static list colorings are found by a separate exact
complement-coloring backtracker.

For every target outside the reference state and every jointly inactive
anchor face, it computes the common open neighborhood in the complement and
checks both
\[
\omega\bigl(H[\{x\}\cup N_H(A)]\bigr)
\quad\text{and}\quad
\chi\bigl(H[\{x\}\cup N_H(A)]\bigr)
\]
exactly.

The abstract-list branch constructs \(K_{k-3}\vee P_4\) without calling the
candidate generator.  It exhausts every proper palette, every clique, every
single-vertex deletion, and every edge/common-color collision.

These bounded computations are adversarial controls only.  The uniform
claims are accepted because of the proof audit in `REVIEW.md`, not by
extrapolation from the finite checks.

