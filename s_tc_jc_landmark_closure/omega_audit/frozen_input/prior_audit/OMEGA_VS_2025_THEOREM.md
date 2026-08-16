# Omega versus the 2025 level-2 identifiability theorem

Overall status: **VERIFIED AFTER CORRECTION**

## Conclusion

Status: **VERIFIED AFTER CORRECTION**

The correct Gate-A outcome is `OMEGA-B`:

> The Omega source and target are nonisomorphic, binary, triangle-free,
> level-2 standard semi-directed networks, and their exact JC overlap
> certificate is valid.  They are not, however, *strongly tree-child* in the
> standard semi-directed sense used by Englander et al.  They are only weakly
> tree-child because the displayed rooted presentations are tree-child while
> some other admissible rootings are not.

Consequently Omega is not a counterexample to Theorem 3.2 of Englander et
al. and cannot appear in a theorem about the standard classes
`L_1`, `L_*`, or `S_2` locked for this audit.

## Literal comparison with Theorem 3.2

Status: **VERIFIED**

The July 4, 2026 revision of Englander et al. defines a semi-directed network
to be strongly tree-child when **every** directed network from which it can
be obtained is tree-child.  It records the equivalent local criterion that
each node with an outgoing retained edge has two incident undirected edges.
Theorem 3.2 applies to binary, triangle-free, strongly tree-child, level-2
semi-directed networks.

The independently reduced Omega networks satisfy all these hypotheses except
strong tree-childness:

| Hypothesis | Omega source | Omega target |
|---|---:|---:|
| Valid binary rooted presentation | yes | yes |
| Standard semi-directed reduction valid | yes | yes |
| Triangle-free | yes | yes |
| Level 2 | yes | yes |
| Labelled mixed graphs nonisomorphic | yes | yes |
| Chosen rooting tree-child | yes | yes |
| Every admissible rooting tree-child | **no** | **no** |
| Local strong-tree-child criterion | **fails at `U`** | **fails at `U`** |

At `U`, two retained edges point from `U` into reticulations, while only one
incident edge is undirected.  This is precisely the configuration excluded
in the paper's introductory paraphrase: a node with two reticulation nodes as
direct descendants.

## Independent graph computation

Status: **EXACTLY COMPUTED**

The implementation in
[`audit_omega_graphs.py`](INDEPENDENT_IMPLEMENTATION/audit_omega_graphs.py)
uses only the Python standard library.  It does not import the discovery
generator, canonicalizer, or Fourier engine.  From the final machine-readable
arcs it independently performs rooted validation, standard mixed-graph
reduction, exhaustive degree-two and parallel-artifact suppression, labelled
mixed-graph canonicalization, blob/cycle analysis, and admissible-rooting
enumeration.

For each of the two standard Omega topologies it finds seven admissible
rootings, of which exactly two are tree-child.  The source and target
canonical mixed-graph encodings differ.  Neither discrepancy is caused by a
root-created degree-two vertex, a parallel-edge artifact, or a hidden
2-sub-blob in the reduction used for Theorem 3.2.

Replay:

```sh
python3 AUDIT/INDEPENDENT_IMPLEMENTATION/audit_omega_graphs.py \
  certificates/jc_omega_move.json \
  --output AUDIT/INDEPENDENT_IMPLEMENTATION/omega_graph_audit.json
```

## Independent algebra computation

Status: **EXACTLY COMPUTED**

[`audit_omega_algebra.py`](INDEPENDENT_IMPLEMENTATION/audit_omega_algebra.py)
independently enumerates displayed trees and computes all zero-sum JC Fourier
coordinates.  It verifies:

- all 64 rational-function identities in the proposed parameter map;
- strict `Theta_0` membership at all four supplied source/target points;
- exact equality of all 64 complete Fourier coordinates at those points;
- the four advertised nonzero rank-nine minors; and
- generic rank exactly nine, with an independent upper certificate from the
  exact rank-six core and pendant-torus Euler dependencies.

The exact minors are

```text
N16 source  -171/2305843009213693952000000
N16 target  -513/9223372036854775808000000
N26 source    57/576460752303423488000000
N26 target   189/2305843009213693952000000
```

Replay:

```sh
python3 AUDIT/INDEPENDENT_IMPLEMENTATION/audit_omega_algebra.py \
  certificates/jc_omega_move.json \
  --output AUDIT/INDEPENDENT_IMPLEMENTATION/omega_algebra_audit.json
```

Thus the mathematical collision survives, but only as a theorem for the
larger weakly tree-child class.

## The inherited Theta pair has the same convention defect

Status: **EXACTLY COMPUTED**

The independent reduction of the inherited Theta pair finds standard
semi-directed graphs with cycle lengths `3,5,6`, two reticulations, and one
triangle.  The source and target are nonisomorphic.  Nevertheless, vertex
`A` has two outgoing reticulation edges and only one incident undirected
edge.  Each standard topology has five admissible rootings, only two of which
are tree-child.  Hence the inherited Theta pair is also outside the standard
strongly-tree-child `L_1` and `L_*` classes.

Replay:

```sh
python3 AUDIT/INDEPENDENT_IMPLEMENTATION/audit_theta_graphs.py \
  certificates/theta_pair_networks.json \
  --output AUDIT/INDEPENDENT_IMPLEMENTATION/theta_graph_audit.json
```

This does not refute the inherited algebraic/stochastic Theta certificate;
it corrects only its class-membership and biological-topology interpretation.

## Hashes

Status: **EXACTLY COMPUTED**

```text
c0b8f907d557d23169a2e132d7a85b789d6fa3fe03d4d90bab286eec206e960f  certificates/jc_omega_move.json
f38577ad38a7d5ae858ac7804f2449bc0523573a412e5bf5a6d9c6a55344af35  certificates/theta_pair_networks.json
ea6c821d47b4a40dd6d09945295af2d0d95557906f8efb31edf766e311ef0bf5  AUDIT/INDEPENDENT_IMPLEMENTATION/audit_omega_graphs.py
3aadbfadb0a67b52873dda706ac60487a07d61352da5ba191d24a499f1690633  AUDIT/INDEPENDENT_IMPLEMENTATION/audit_omega_algebra.py
75971146d0c7918e09c19a223db18c6d6d92e55276f0902f7c40ee928bc013f2  AUDIT/INDEPENDENT_IMPLEMENTATION/audit_theta_graphs.py
260a977d9629eeb1b9ea0b7afa6d8179625609748ce20a2007927df5aa6e874f  AUDIT/PRIOR_WORK/englander_level2_v4.pdf
```

## Dependency consequence

Status: **VERIFIED AFTER CORRECTION**

All standard-strong conclusions whose only non-triangle move is Omega,
`Omega_chain`, or Theta must be withdrawn or re-proved without those moves.
Their exact Fourier identities remain reusable only for explicitly named
weakly tree-child classes.  In particular, removing Omega alone is
insufficient: the flagship standard `L_1/L_*` theorem also loses Theta.

## Adversarial reviewer gate

Status: **VERIFIED**

An adversarial reviewer wrote a third implementation importing neither the
discovery code nor the first independent audit.  It reproduced the complete
graph, rooting, Fourier, `Theta_0`, rank, and Theta-invariant calculations and
attempted explicitly to falsify `OMEGA-B`.  It found no mathematical
discrepancy.  The only correction was a stale requested filename:
`jc_omega_exact_isomorphism.json` does not exist; the operative certificate
is `jc_omega_move.json`, already used above.

Artifacts:

- [`GATE_A_ADVERSARIAL_REVIEW.md`](REVIEWS/GATE_A_ADVERSARIAL_REVIEW.md)
- [`gate_a_crosscheck.py`](REVIEWS/gate_a_crosscheck.py)
- [`gate_a_crosscheck_output.json`](REVIEWS/gate_a_crosscheck_output.json)

```text
d4472d231495cb58bd39062dcf95de3c93db6b6eaf9d57ea9bacdf2f93117f2d  AUDIT/REVIEWS/GATE_A_ADVERSARIAL_REVIEW.md
fce241c14c45cba9a95f8bc92cd38df68d80ebc602a38c6f8e46a9efda1aff80  AUDIT/REVIEWS/gate_a_crosscheck.py
651b42e2c777b745711147f3a18b2435f4100eb5b1f51f93c24210a8f2272f02  AUDIT/REVIEWS/gate_a_crosscheck_output.json
```
