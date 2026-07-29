# Research log: higher-rank completion-fan descent

## 2026-07-28 PDT

- Reconstructed C-173--C-175 and the hostile-passed rank-one
  anchor-restoration reduction.  Fixed the open slice at a minimum
  second-fan state \(K_e=\{r,y,e\}\) with source rank \(h\ge2\).
- Tested and rejected the tempting inference that a reciprocal
  configuration two-cycle forces kernel survival.  Synchronous ranks are
  directional: a deleting response can descend from \(h\) to \(j<h\),
  while the unique reverse response legally rises from \(j\) back to
  \(h\).
- Proved the descending-petal lemma.  Every retained deletion response
  has lower rank and a unique reverse to the independent source.  A
  one-neighbor exit is a lower-rank exchange in a neighboring completion
  fan; a multi-neighbor exit supports one or two full repair fans.
- Derived the exact Johnson-distance formula for every endpoint.  At
  rank two, a retained endpoint must contain a ban anchor or a vertex of
  the target-ban set.
- Applied the minimum-fan property to exclude the lone neighbor set
  \(\{e\}\).  The six remaining physical neighbor sets and their
  nonempty retained-mover subsets give a list of 18 formal labeled
  \((A,M)\) patterns; no claim is made that all are realizable.
- Proved the exact target specialization.  A trapped completion fan
  forces all target petals \(X_e\).  A completely crossing fan either
  retains one common hub \(R_x\) or forces all target petals.  Every
  retained target endpoint has a unique reverse; it is lower-rank only
  when the target is the selected deleting attack.
- Built `verify_normal_form.py`.  It exhausts all 33,864 labeled graphs
  through order six, 2,162 equality graphs, 469,486 source-form bans,
  33,660 higher-rank state incidences, and 100,980 deletion exits.  All
  checks pass.  The exact 13-vertex gamma-two boundary realizes the
  multi-neighbor petals but keeps all restricted kernels empty.
- Best-guess completion: this higher-rank finite-normal-form subgate
  **100%**; elimination of higher-rank fan exits **35%**; complete
  \(k=3\) proof lane **about 59%**; universal conjecture resolution
  **about 20%**.  These are workload estimates, not probabilities.
