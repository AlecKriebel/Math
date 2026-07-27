# Research log: \(k=3\) 2-SAT bicycle dynamics

## 2026-07-26 18:56 PDT

- Read the projection-gluing, universal shared-response-core, cross-state
  exchange/base-orderability, mixed-\(P_4\), mixed-witness, and concurrent
  forced-\(C_5\) notes in full, together with the relevant hostile reviews.
- Proved the normalized inclusion-minimal 2-CNF terminal trichotomy:
  two-unit chain, one-unit lollipop, or unit-free bicycle.
- Derived the exact port-connector parity law translating implication paths
  back into paths inside frozen projection components.
- Found and proved a named-attack exclusion of the canonical one-unit
  tail-triangle realization.  The proof applies to an arbitrary specified
  eternal family and needs no domination equality.
- Found and proved a named-attack exclusion of the canonical unit-free
  two-variable bicycle.  Again the proof is arbitrary-family and
  equality-free.
- Constructed and directly verified `GFznc{`: a 35-state eternal family
  with parameters \((2,3,3,3)\), an unsatisfiable no-full-list response
  formula at both ends of the ridge \(012\)--\(127\), and exact covariance
  under \((0\ 7)\).  This is the first local countermodel in this lane where
  covariance acts nonvacuously on the unsatisfiable formula itself.
- Exhausted all ordinary 2-CNFs through three variables as a falsifier for
  the trichotomy.
- Scanned all 11,117 connected order-eight graphs.  In the
  \(\alpha=\gamma^\infty=3\), \(\gamma\in\{2,3\}\) slice, all 18,985
  eligible exact two-list restrictions produced zero uncolorable retained
  family instances.  This remains `OBSERVED`, not a certified frontier
  result.
- Reconciled the classification with the concurrent mixed-path theorem:
  a general minimal bicycle does not force end-witness overlap, and in the
  exact mixed-\(P_4\) geometry the proved conclusion is
  \(P_L\cap P_R=\varnothing\).

Frozen hashes at this checkpoint:

| artifact | SHA-256 |
|---|---|
| `NOTE.md` | `6d088edf77d6e0eee3491d2631db8ea0cebf614d112776ef8e719ffc90e6639a` |
| `evidence.py` | `052f7d55602b702935afa7dffb25f056b61d70d868606f5c4e91d1dce1b0f97c` |
| `evidence.json` | `f2025f12a1455e3cf44643ecf3e57324d9b5b2c1a183506a34299c04e63a4307` |
| concurrent forced-\(C_5\) note read | `0c6a3de00f8e4daa53f4602c437ed51a22da911cfdff3f42445550b07e3430bb` |

Exact boundary:

- `PROVED`: trichotomy, connector parity, and the two canonical closure
  exclusions.
- `EXACT CHECK`: `GFznc{`, its 35-state family, 175 obligations, parameters,
  two unsatisfiable ridge-end formulas, and covariance identities.
- `OBSERVED`: the bounded order-eight zero-unit scan.
- `OPEN`: subdivisions and larger bicycles, reduction to the mixed
  \(P_4\), the full-list slice, the \(k=3\) slice, and the universal
  conjecture.
