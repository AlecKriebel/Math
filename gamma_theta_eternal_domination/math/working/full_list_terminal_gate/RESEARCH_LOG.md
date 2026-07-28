# Research log: full-list terminal gates

## 2026-07-28 12:41 PDT

- Opened the C-141/C-142 source note and hostile review and the revised
  C-149 source note and hostile review.
- Replayed the C-149 catalog-shape probe and inspected its exact
  deletion-rank and terminal-gate definitions.
- Initial boundary: the order-12 equality control
  ``Ksv`f\knJVis`` already has two annihilated colors whose selected
  starts reach only corridor terminals, so no one-color or two-color
  exclusion of corridor-only descent is possible.
- Candidate exact class to test: three annihilated colors whose retained
  terminal ban states all have singleton greatest-family root palettes.
  C-149 turns each trace endpoint into a positive palette incidence, while
  the accepted rainbow-singleton attack forbids three such incidences.
  This must be restated and checked without treating a missing family
  response as a graph nonedge.

## 2026-07-28 12:48 PDT

- **PROVED:** the palette-thin three-trace class is empty.  If each
  restricted kernel is annihilated and one decreasing-rank trace per color
  ends at \(S-u+r_u\), the three terminal palettes cannot be
  \(P(r_u)=\{u\}\).  The proof is a self-contained two-case one-guard
  attack tree.  Its only graph nonedges are anchor independence and
  \(r_u\in N_{\overline G}(x)\); missing palette entries exclude family
  states only.
- **PROVED exact finite control:** a new independent packed-mask checker
  reconstructs ``Ksv`f\knJVis`` with
  \((\gamma,\alpha,\gamma^\infty,\theta)=(3,3,3,3)\).  Colors 1 and 2
  have empty kernels, selected-start ranks one, and exactly two reachable
  terminal entries each.  All four entries are nonroot corridors and
  their terminal palettes have size two.  Color 3 leaves 64 states.
- **CANDIDATE/open:** an all-three non-singleton corridor-only pattern.
  The equality control realizes two colors, so no one-color or pairwise
  corridor exclusion can prove survival.
- Strict replay passed:
  `python3 -I -B -W error
  math/working/full_list_terminal_gate/verify_equality_control.py`.
