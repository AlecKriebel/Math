# Discovery 04 artifact manifest

Status: public research draft, not peer reviewed.

## Main artifacts

| Path | Role |
|---|---|
| `NOTE.md` | Full readable proof and exact displayed certificate |
| `wreath_monodromy.tex` | Typeset paper source |
| `output/pdf/wreath_monodromy.pdf` | Rendered paper |
| `PRIORITY_AUDIT.md` | Timestamped 23-repository, web, arXiv, and MathOverflow audit |
| `RESEARCH_LOG.md` | Chronological decisions, rejected targets, and proof development |
| `README.md` | Entry point and reproduction commands |

## Exact verification

| Path | Independence and scope |
|---|---|
| `verify_symbolic.py` | SymPy derivation from the map: Jacobian, collisions, inverse resolvent, eliminant, subresultant/function-field certificate, Newton edge, discriminant, and coprimality |
| `verify_modular.py` | Python-standard-library polynomial arithmetic and Rabin irreducibility certificates; no CAS |
| `verify_iterate_inertia.py` | Python-standard-library check of the all-iterate recurrence, Newton edges, and reconstruction dominance inequalities |
| `verify_pari.gp` | PARI/GP re-entry of the displayed polynomials and independent discriminant, modular, and Galois checks |
| `verify_group.g` | GAP construction of `S_3 wr S_3` and exhaustive subgroup exclusion |
| `verify_level3_newton.py` | SymPy-generated level-three equations with nested resultants delegated to PARI |
| `verify_level3_wreath.py` | Exact primitive degree-27 eliminant, discriminant simple-divisor and denominator guards, plus the structural `W_3` kernel lemma |
| `w4_search/RESULT.md` | Separate good-reduction, norm-to-inertia, and group proof of `Mon(F^4)=W_4` |
| `w4_search/finite_field_norm.py` | Bounded-memory quotient-tower evaluator over a prime or prime-square coefficient ring |
| `w4_search/verify_w4_modular.py` | Recomputes the level-four modular certificate, direct sheet derivative, scan digest, and `S_3^27` kernel lemma |
| `w4_search/test_finite_field_norm.py` | Dependency-free quotient-algebra and prime-square determinant tests |
| `w5_search/RESULT.md` | Separate good-reduction, norm-to-inertia, and group proof of `Mon(F^5)=W_5` |
| `w5_search/finite_field_norm_depth4.py` | Rank-81 depth-agnostic quotient-tower evaluator and prime-square Hensel profile |
| `w5_search/verify_w5_modular.py` | Recomputes the level-five profile, direct sheet derivative, final double root, and `S_3^81` kernel lemma |
| `w5_search/audit_w5_hostile/verify_w5_matrix_tower.py` | Independent block regular-representation replay, with no imports from the W4/W5 quotient-vector arithmetic |
| `w5_search/verify_all_strict.sh` | Runs the primary, regression, hostile, and fault-injection level-five suites |
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
- `Mon(F^3)=S_3 wr S_3 wr S_3` geometrically;
- order `13,060,694,016` and generic degree 27;
- a unit-Jacobian noninjective normalization in `C^3`;
- full `3^m`-cycle inertia for every iterate `F^m`.
- in the separate `w4_search` proof artifact, `Mon(F^4)=W_4` geometrically,
  of order `6^40=13,367,494,538,843,734,067,838,845,976,576`.
- in the separately audited `w5_search` proof artifact,
  `Mon(F^5)=W_5` geometrically, of degree 243 and order `6^121`.

Not proved:

- full iterated-wreath monodromy for every `m`;
- first-ever imprimitive or non-symmetric Keller monodromy;
- guaranteed worldwide priority;
- peer-reviewed correctness.
