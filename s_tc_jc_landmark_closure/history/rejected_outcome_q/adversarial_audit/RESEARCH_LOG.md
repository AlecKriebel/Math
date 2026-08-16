# Outcome Q audit log

## 2026-08-13 — package frozen and audit opened

- Created branch `codex/stc-jc-outcome-q-audit` from verified Outcome P
  packaging commit `1478af79fa51b1e139361cd73ab7188f216172e4`.
- Froze the supplied archive and integration directive byte-for-byte.  The
  archive SHA-256 is
  `abb83eff03996b7b95520ace2491c233daa4a9634ef1a771d51dc703dbf97f14`.
- The ZIP integrity test, outer `SHA256SUMS.txt`, and inner release-tree
  manifest all pass.  This establishes byte consistency only, not theorem
  validity.
- Opened independent structural, JC-algebra, convention/literature, and
  certificate-sensitivity reviews.  Integration remains prohibited pending
  their verdicts and the main clean-room replay.

## 2026-08-13T21:03:20-07:00 — first load-bearing failure found

- Independently verified the one-step tree-child zipper formula
  \(\kappa=uv[\lambda\alpha\beta+(1-\lambda)\gamma]\), its strict analytic
  section, and its everywhere-rank-one effective-parameter map.  This narrow
  local lemma appears sound.
- Found that the package attributes the 2025 Englander convention from the
  obsolete v1 text to the cited v4 paper.  In v4, Definition 2.2 only
  deorients nonreticulation edges and suppresses the former root; parallel
  outputs are disallowed.  Exhaustive degree-two/parallel/2-blob cleanup is
  the induced-subnetwork operation in Definition 2.4, not the full-topology
  operation.  Thus the baseline `sd0` convention is already the relevant
  Englander convention, while Brits-style cleanup is a distinct convention.
- Constructed an explicit two-stage root zipper over the ordinary labelled
  three-leaf tree.  It is a binary, acyclic, LSA-valid rooted level-2 network
  with no parallel directed arcs, but is not tree-child because one
  reticulation has a reticulation child.  Exhaustive Brits-style cleanup
  removes both zipper layers and returns the ordinary three-leaf tree.
- Consequently, under Outcome Q's stated **complete unrestricted cleanup
  rooting fibre**, even the ordinary three-leaf tree has a non-tree-child
  cleanup rooting.  More generally, a double zipper can be placed above any
  already-simple rooting if the rooting fibre is not independently bounded.
  The claimed nonempty class `S_TC(clean)` and its class-relation census are
  therefore not established; under the literal definition the strong class
  is empty on the already-simple topology domain.
- The independent exact checker is
  `independent/double_zipper_counterexample.py`.  It reconstructs the typed
  cleanup trace from the primitive DAG and imports no Outcome Q code.
- Release replay is also not clean as supplied: `verify_quick.sh` fails because
  `pdftotext` is invoked but Poppler is absent from the declared environment.
  With a temporary audit-only shim, quick and full pass, but regenerate-all
  fails because `dependency_audit.json` embeds and byte-compares one exact
  Python build string.
- Outcome Q remains quarantined.  No change has been made to the verified
  Outcome P baseline.
