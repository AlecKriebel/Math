# Discovery 04 artifact manifest

Status: research draft, not peer reviewed.

## Main artifacts

| Path | Role |
|---|---|
| `NOTE.md` | Full readable proof and exact displayed certificate |
| `wreath_monodromy.tex` | Typeset paper source |
| `output/pdf/wreath_monodromy.pdf` | Rendered six-page paper |
| `PRIORITY_AUDIT.md` | Timestamped 23-repository, web, arXiv, and MathOverflow audit |
| `RESEARCH_LOG.md` | Chronological decisions, rejected targets, and proof development |
| `README.md` | Entry point and reproduction commands |

## Exact verification

| Path | Independence and scope |
|---|---|
| `verify_symbolic.py` | SymPy derivation from the map: Jacobian, collisions, inverse resolvent, eliminant, Newton edge, discriminant, and coprimality |
| `verify_modular.py` | Python-standard-library polynomial arithmetic and Rabin irreducibility certificates; no CAS |
| `verify_iterate_inertia.py` | Python-standard-library check of the all-iterate integer recurrence |
| `verify_pari.gp` | PARI/GP re-entry of the displayed polynomials and independent discriminant, modular, and Galois checks |
| `verify_group.g` | GAP construction of `S_3 wr S_3` and exhaustive subgroup exclusion |
| `verify_level3_newton.py` | SymPy-generated level-three equations with nested resultants delegated to PARI |
| `search_wreath.py` | Exploratory exact arithmetic at five unrelated rational fibers |
| `requirements.txt` | Pinned SymPy requirement |
| `render_paper.py` | Reproducible Tectonic PDF build |

## Verified environment

```text
Python 3.9.6
SymPy 1.14.0
PARI/GP 2.17.4
GAP 4.14.0
Tectonic 0.16.9
```

No numerical approximation is used in a theorem certificate. The PDF was
rendered to page images and visually inspected; the TeX log contains no
overfull boxes, undefined references, or other layout warnings.

## Claim boundary

Proved in the draft:

- `Mon(F o F)=S_3 wr S_3` geometrically;
- order `1296` and generic degree nine;
- a unit-Jacobian noninjective normalization in `C^3`;
- full `3^m`-cycle inertia for every iterate `F^m`.

Not proved:

- full iterated-wreath monodromy for every `m`;
- first-ever imprimitive or non-symmetric Keller monodromy;
- guaranteed worldwide priority;
- peer-reviewed correctness.
