# Research log — hostile exact-\(\delta=4\) umbrella audit

## 2026-07-26T06:45:57Z — audit opened

- Began a source-preserving audit of the candidate umbrella in the parent
  directory.
- Scope is the exact-\(\delta=4\) six-family statement only: reconcile the
  frozen \(19+6+1\) denominator and immutable fourteen-row taxonomy, verify
  every bridge alias, inspect arbitrary-lower-term coverage and
  pivot/boundary completeness in all six family packages, and test
  fail-closed wrapper behavior.
- No claim about the rest of the fixed-quadratic row, any global quartic
  row, or degree at least five is in scope.
- Best-guess completion: **10%**.

## 2026-07-26T06:53:00Z — first bridge defects found

- The initial bridge pointed to the superseded primary \(17+6+1\)
  denominator rather than the canonical blinded \(19+6+1\) denominator.
- Its verifier checked only membership in that old six-entry list.  It did
  not bind certificate labels, paths, or terminal markers, while the
  aggregate executed a separate hard-coded list.
- Reported the defects to the assembler.  They were repaired by adopting
  the canonical six IDs, hard-binding their certificates, and emitting the
  execution plan from the validated manifest.
- Best-guess completion: **35%**.

## 2026-07-26T06:59:00Z — family-wrapper scope audit

- Confirmed that all six family calculations parameterize the full
  six-dimensional \(E_7\) kernel and retain arbitrary lower terms.
- Found one exact wrapper/prose mismatch: the `D4-DN-1CC` wrapper did not
  yet run its hostile reconstruction or a required-failure mutation even
  though the umbrella said every family wrapper did.  The assembler
  repaired the wrapper by invoking the hostile replay and mutating the
  decisive \(E_4\) obstruction.
- No missing contact pivot was found in the two DN plane atlases, the two
  one-line atlases, or the two squarefree plane atlases.
- Best-guess completion: **60%**.

## 2026-07-26T07:04:00Z — second bridge mutation round

- Canonical-ID, certificate-label, family-path, and marker mutations were
  correctly rejected by the first repaired verifier.
- Two further mutations were initially accepted while the verifier still
  printed its canonical marker: replacing the canonical source by a
  duplicate alternate path, and changing the theorem scope to a
  row/global claim.  Mutating the advertised canonical count
  \(19\mapsto18\) was also accepted.
- The assembler hard-bound the source and scope strings and the canonical
  schema, status, scope, and exact \(19/6/1/26\) counts.
- A fresh isolated replay rejected all seven mutations with their intended
  diagnostics.
- Best-guess completion: **80%**.

## 2026-07-26T07:08:58Z — taxonomy and theorem synthesis

- The immutable fourteen-row taxonomy checksum verifier passed.
- Both the frozen taxonomy and current certification ledger still mark
  `Q2-E2-A1-B2-D1-N2` open.  The umbrella therefore changes no global
  status.
- Reconstructed the six-orbit count from the local valuation mechanism,
  the saturated squarefree rank-drop factors, and the doubled-root gcd
  signatures.  The six are exhaustive and pairwise disjoint.
- Completed `AUDIT.md` with a final PASS verdict conditional on the fresh
  aggregate reaching its terminal marker.
- Best-guess completion: **95%**.

## 2026-07-26T07:25:07Z — final strict PASS

- The revised dynamic aggregate completed with all six distinct
  family-terminal markers, the canonical reconciliation marker, and
  `EXACT_DELTA4_SIX_FAMILY_EXCLUSION_STRICT_PASS`.
- The standalone hostile wrapper then repeated the full aggregate, replayed
  the immutable global-taxonomy checksums, confirmed that the containing
  row remains open, and rejected all seven isolated bridge mutations.
- Final marker:
  `EXACT_DELTA4_HOSTILE_UMBRELLA_AUDIT_STRICT_PASS`.
- Final theorem-level verdict: **PASS** at the exact-\(\delta=4\) binary
  sublocus scope.  No row/global exclusion and no degree-\(\ge5\) inference.
- Best-guess completion: **100%**.
