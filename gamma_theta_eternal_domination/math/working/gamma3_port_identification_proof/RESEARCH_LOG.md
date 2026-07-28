# Research log

## 2026-07-27 20:55--21:35 PDT

- Read the accepted full-list, 2-SAT bicycle, odd connector, deletion
  dichotomy, and separated-port integration notes.
- Reconstructed the exact `HFzvvn{` response geometry without treating a
  missing family response as a graph nonedge.
- Proved the dynamic connector-cap lemma: \(\gamma=3\) supplies a common
  complement-neighbor, the dead-state lemmas force the omitted response
  color onto that cap, and \(\alpha=3\) makes the cap set a \(G\)-clique.
- Combined the cap lemma with C079 at path length one to prove positive
  completeness of every cap.
- Derived the exact cap-and-escape ladder for the separated-port core.
  The forced escape lies in the full vertex's complement link, omits the
  connector color, and cannot see both connector endpoints because that
  would create a complement \(K_4\).  The two forced new vertices give an
  eleven-vertex floor for this exact pattern.
- Exhausted all \(524{,}288\) exact induced two-vertex extensions.  Six
  passed the static \(\gamma=\alpha=3\) conditions; all six had empty
  eternal triple-kernel.  A clean-room implementation replayed the entire
  scope and conclusion; the deliberately local diagnostic remains
  `OBSERVED`.
- Built a direct exploratory SAT encoding with a positive `HFzvvn{`
  control.  Stopped the search lane without promoting any unlogged UNSAT
  output; the human cap results do not depend on it.
- Exact remaining obstruction: global iteration of alternating
  positive-cap and omitted-color link vertices.  Immediate physical port
  recurrence is not forced by the first \(\gamma=3\) completion.
