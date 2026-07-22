# Discovery 07 manifest

## Human-readable artifacts

| File | Purpose |
|---|---|
| `README.md` | Entry point, reproduction commands, scope, and warning |
| `NOTE.md` | Concise statement of the unifying thesis and stopping rule |
| `unified_consequences.tex` | Complete self-contained manuscript |
| `output/pdf/unified_consequences.pdf` | Rendered eleven-page paper |
| `PRIORITY_AUDIT.md` | Source-bounded literature and claim-scope audit |
| `RESEARCH_LOG.md` | Derivation, audit, and verification chronology |

## Exact construction and verification

| File | Purpose |
|---|---|
| `construction.py` | Loads the exact precursor constructions and defines both inverse coefficient families and symmetric companions |
| `verify_symbolic.py` | Primary bounded-memory exact proof-side checker |
| `export_certificate.py` | Deterministic exporter for the unified sparse certificate |
| `verify_exported_stdlib.py` | Dependency-free Python checker |
| `verify_exported_node.mjs` | Independent Node.js/BigInt checker |
| `output/unified_every_order.json` | Expanded 28D/30D potentials, targets, formulas, fiber basis, and precursor hashes |
| `render_paper.py` | Reproducible Tectonic build |
| `requirements.txt` | Pinned SymPy dependency |

## Claim-to-check map

| Claim | Exact guard |
|---|---|
| Three-point fiber is exact and reduced | `verify_symbolic.py` check 1; JSON fiber basis; both dependency-free checkers |
| 14D and 22D determinant-pencil block identities | `verify_symbolic.py` check 2; displayed stable operations certify `det J Psi=1` structurally |
| Weighted conjugacy and distinct integral normal forms | `verify_symbolic.py` check 3 |
| Homogeneous 15D companion has exact Jordan type `(14,1)` | `verify_symbolic.py` check 4, including `(Jg)^13 g = 0` |
| All `q_m` and `r_m` are nonzero | Closed formulas in the manuscript; `verify_symbolic.py` check 5; independent checks through index 999 |
| Source ray and 22D inverse target are exact | `verify_symbolic.py` check 6 |
| Term counts 178, 608, and 538 | `verify_symbolic.py` check 7; exported sparse certificate for 28D/30D; hashed 44D precursor |
| Symmetrization and inverse projection have the stated signs | `verify_symbolic.py` check 8 |
| Zhao index shift and factorial are correct | Manuscript equation (15); `verify_symbolic.py` check 9 |

## SHA-256

```text
deb01a83cea8543b17c13e8849cead0159d5d8feac07ae18034fd880a274495c  output/unified_every_order.json
b0c5cba5ebdfaa642cf2f02059e35b592dbcb0f5fbe6c36e3399034eb541256b  output/pdf/unified_consequences.pdf
2a912728161888849e77d607ea1f635233576543ed12d5fe8b2a65e0751789f4  ../discovery_03_small_vanishing_counterexample/output/potential_sparse.json
ce6ca33b38c808a973b18da3d5f4a1f5a647c7836c2fbd78889fa7ffb3ba746c  ../discovery_06_unipotent_three_point/output/unipotent14_sparse.json
```

The JSON's precursor paths are resolved relative to the Discovery 07 package
root by both independent checkers. They are repository-bundled dependencies,
not network fetches. The reference environment used Python 3, SymPy 1.14.0,
and Node.js; the primary symbolic run peaked at approximately 74 MiB RSS.

The certificate in turn pins the exact precursor certificates by SHA-256, so
the consolidated paper cannot silently drift away from the archived 14D and
44D formulas.
