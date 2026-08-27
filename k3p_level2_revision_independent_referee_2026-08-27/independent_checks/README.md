# Fresh independent spot checks

These scripts are referee-authored checks for the revised package dated
2026-08-27. They were written without importing any package producer,
verifier, atlas module, or prior referee output. They are deterministic,
reject optimized Python (`-O`), stop at the first failed assertion, read the
package only through `--package-root`, and write only beneath the supplied
`--output-dir`.

The scripts use only the pinned package environment's standard library,
SymPy, and NetworkX. Run them inside the referee's credential-free, offline
sandbox against the copied package, not the author's working tree.

## Coverage and independence boundaries

| Script | Fresh check | Package inputs retained | Exact boundary |
|---|---|---|---|
| `check_three_leaf_geometry.py` | Inverse Fourier round trip; principal versus CT domains; all six literal tree/sunlet circuits; H14 pullback under six leaf permutations; primitive-linear irreducibility argument; three-orientation common point, rank 14 and smoothness; exact six-dimensional cherry map, positive inverse, Jacobian and physical point | None | Symbolic formulas are independently transcribed from the article. |
| `check_bridge_gluing.py` | Marked and unmarked bridge-fibre exponent ranks, positive pair-anchor inverse, excluded degree-two stabilizer, sectorwise gauge cancellation, and 2,000 exact-rational capped-gluing trials with the symbolic CT lower bound | None | Freeness is conditional on the manuscript's marked-or-degree-at-least-three topological dichotomy. |
| `check_jc_endpoint_certificate.py` | Independently expands the JC inheritance mixture from every corrected switching-signature record; reconstructs all 77 normalized three-port tensors and their Delta/Gamma cases with exact sparse, factor, and Bernstein checks; rebuilds the two-active minors and identities | The 77 corrected signature records and their claimed normalization/case labels | Does not reconstruct witness graphs, primitive graph/completion completeness, or the 808,642-case unreduced binary-word census. It rederives each sign instead of replaying stored factor strings and Bernstein summary fields. |
| `check_four_port_witnesses.py` | Local switching compiler from literal DAGs; three exact quartic pullbacks; three fresh directional-rank witnesses; H21 saturation identities; two sunlet upper factorizations; independent quotient of the flat final residue into `40=38+2` and fourteen root-suppressed, arrowhead-preserving mixed-graph double cosets, including displayed-frame conjugation | Frozen literal graphs, the flat post-quadratic residue registry, and the final quotient only for a post-check comparison | Recomputes the final residue quotient, but does not repeat the preceding 405,216-to-40 exhaustive filtering. |
| `check_restoration_probe_census.py` | Streams every restoration and probe row; binds active restoration rows to the frozen forest (including legacy parentage, active/legacy statuses, and the exact 32-by-8 depth-two fanout); recomputes file/record hashes, ordered roots, registry usage, exact one-to-two-port parent/profile links, Cartesian two-port coverage, endpoint-map compatibility, and strict witness margins | Frozen restoration forest plus stored ledgers, registries, and manifests | Does not regenerate the restoration forest or reconstruct every restoration/probe graph; it is an all-row binding/census audit. |
| `check_probe_semantic_samples.py` | Rebuilds rooted and mixed graphs from public profiles for isomorphic, ordinary-triangle, displayed-quartet, and six-circuit tree/sunlet one-port rows plus a two-port equality/restriction row | Public candidate profiles and the selected stored row IDs/witness records | Five representative semantic rows, not an independent replay of all 574,535 rows. |
| `check_krawczyk_box.py` | Rebuilds both literal Fourier maps, point and interval Jacobians, Krawczyk self-inclusion, contraction, both rank-15 Neumann certificates, and physical margins | Rational center, frozen coordinates, pivot scales, radius, selected rank columns, and literal DAGs | Uniqueness is certified only in the supplied 15-dimensional pivot-coordinate slice box. |

`check_jc_endpoint_certificate.py` was authored in a no-execution follow-up.
No passing result is claimed for it unless and until the command below is run.

The exact cherry calculation in `check_three_leaf_geometry.py` is the local
all-n extension step: for each K3P sector it checks
`(u_h,v_h) -> (u_h/v_h,u_h v_h)`, its positive square-root inverse, and the
full six-dimensional Jacobian determinant.

## Exact commands

The commands below use the current copied package, its pinned interpreter, and
an output directory inside the allowed referee runtime area. Each command may
be run separately; no script calls another script.

```sh
/Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27/package_copy/.venv/bin/python /Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27/independent_checks/check_three_leaf_geometry.py --output-dir /Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27/package_copy/review_runs/independent_spot_checks
```

```sh
/Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27/package_copy/.venv/bin/python /Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27/independent_checks/check_bridge_gluing.py --output-dir /Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27/package_copy/review_runs/independent_spot_checks
```

```sh
/Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27/package_copy/.venv/bin/python /Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27/independent_checks/check_jc_endpoint_certificate.py --package-root /Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27/package_copy --output-dir /Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27/package_copy/review_runs/independent_spot_checks
```

```sh
/Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27/package_copy/.venv/bin/python /Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27/independent_checks/check_four_port_witnesses.py --package-root /Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27/package_copy --output-dir /Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27/package_copy/review_runs/independent_spot_checks
```

```sh
/Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27/package_copy/.venv/bin/python /Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27/independent_checks/check_restoration_probe_census.py --package-root /Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27/package_copy --output-dir /Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27/package_copy/review_runs/independent_spot_checks
```

```sh
/Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27/package_copy/.venv/bin/python /Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27/independent_checks/check_probe_semantic_samples.py --package-root /Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27/package_copy --output-dir /Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27/package_copy/review_runs/independent_spot_checks
```

```sh
/Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27/package_copy/.venv/bin/python /Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27/independent_checks/check_krawczyk_box.py --package-root /Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27/package_copy --output-dir /Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27/package_copy/review_runs/independent_spot_checks
```

Successful runs emit one JSON document to standard output and the same
document to, respectively:

- `three_leaf_geometry.json`
- `bridge_gluing.json`
- `jc_endpoint_certificate.json`
- `four_port_witnesses.json`
- `restoration_probe_census.json`
- `probe_semantic_samples.json`
- `krawczyk_box.json`

Any missing input, schema drift, failed identity, count mismatch, nonphysical
margin, failed rank bound, or failed semantic reconstruction terminates with a
nonzero exit before a success document is written.
