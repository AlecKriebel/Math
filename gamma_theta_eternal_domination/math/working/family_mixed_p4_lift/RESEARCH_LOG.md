# Research log: lifting the mixed \(P_4\) exclusion from static to family lists

Date: 2026-07-28 (PDT)

## Scope

Work under

\[
\gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\]

with an arbitrary eternal family \(\mathcal F\), an independent retained
state \(S=\{a,b,c\}\), and an induced path
\(x_0x_1x_2x_3\) in \(\overline G\) having exact **family** lists

\[
\{a\},\quad\{a,c\},\quad\{b,c\},\quad\{b\}.
\]

Do not infer graph nonedges or failed domination from omitted family
responses.

## 2026-07-28 — input audit

- Read accepted C-148 and its hostile review in full.
- Read accepted C-121 and C-070 source notes in full, together with the
  original C-067 note and the `FDzro` hostile audit.
- The C-148 local calculation actually needs only the exact family lists,
  C-070 endpoint saturation, and one genuine endpoint domination defect.
  It does not need exact static lists at the other three path vertices.
- Therefore any equality realization of the family-list pattern must make
  both omitted middle-color endpoint swaps
  \(\{a,b,x_0\}\) and \(\{a,b,x_3\}\) dominating.  Otherwise the same
  eight-vertex, 32-completion local kernel from C-148 applies (after
  reflection at the right endpoint).
- This is a rigorous immediate reduction, not yet the requested dynamic
  elimination.  It pins the unresolved case to two dominating states
  intentionally omitted from \(\mathcal F\).

## Guardrail

The graph `FDzro` realizes the exact family lists in a proper eternal
family while both endpoint middle-color swaps dominate.  Hence no
equality-free argument may turn either omission into a graph nonedge,
static defect, or finite deletion rank in the unrestricted greatest
kernel.

## 2026-07-28 — exact checkpoint

- Wrote the self-contained endpoint-domination reduction in `NOTE.md`.
  If either omitted \(c\)-swap fails domination, the accepted C-148
  one-defect kernel applies verbatim: its other three negative static
  lists were not used.  Reflection handles the second endpoint.
- Recorded the exact greatest-kernel normal form.  Each endpoint state is
  either a survivor or has positive finite deletion rank.  Exact lists in
  the literal greatest family force the second alternative and a deleting
  attack whose every legal successor has strictly lower rank.  For a
  proper family, survival in the unrestricted greatest kernel remains
  possible and cannot be treated as rank failure.
- Built a direct SAT discovery model for an unknown graph and an arbitrary
  proper eternal family.  CaDiCaL 3.0.1 reported UNSAT at every tested
  order \(12\) through \(22\).  These runs are deliberately labeled
  `OBSERVED`: there are no proof logs or independent encoding/coverage
  audit.
- A diagnostic order-12 run remained UNSAT after deleting the explicit
  \(\alpha\le3\) clauses, consistent with
  \(\alpha\le\gamma^\infty=3\).  This is not promoted.
- The exact next recurrence is now finite-rank rather than static:
  descend from the deleting rows of the two dominating endpoint swaps to
  a lower-rank endpoint row, a C-148 domination-defect core, or a
  dominating pair.  A deleting attack cannot itself be relabeled as the
  old missed vertex because it must be adjacent to at least one occupied
  guard.
