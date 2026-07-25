# Blind independent taxonomy research log

All times are America/Los_Angeles (UTC-07:00). This effort was derived without
reading, listing, searching, or inspecting pre-existing files in the parent
project.

## 2026-07-25

- **12:27:28** — Began the blinded derivation. Fixed the object of study as a
  nonzero homogeneous quartic triple \(H_4\) with
  \(\det JH_4=0\), considered under linear source and target changes. Identified
  the first invariant as the generic Jacobian rank \(0,1,2\).
- **12:27:28** — Flagged the central theorem-risk: algebraic dependence gives a
  projective curve, but the requested polynomial pencil factorization
  \(H_4=hA(p,q)\) requires a careful descent from a rational Lüroth parameter
  to coprime equal-degree forms and a divisibility argument. The final taxonomy
  will state this as a hypothesis unless a complete proof is supplied.
- **12:44:43** — Completed the factorization proof. After removing the
  component gcd, lift the projective map to the normalization
  \(\mathbb P^1\), represent the lift by a coprime equal-degree pencil, and use
  primitivity in the UFD to show equality rather than mere projective
  proportionality. This proves existence and the degree formula. The remaining
  gap is uniqueness of a least-degree pencil, not existence.
- **12:44:43** — Enumerated the thirteen rank-two numerical rows from
  \(e+ab=4\) and \(b=\delta\nu\), then added rank one, rank zero, binary-gcd,
  pencil-gcd, composition, cover, singularity, incidence, and rank-drop
  boundaries.
- **12:44:43** — Corrected an initially tempting but invalid product-orbit
  shortcut: finite source and outer quotients need not give a finite combined
  quotient because the embedded pencil can mark the parameter line. Recast the
  outer datum intrinsically as \(V_A\subset\operatorname{Sym}^bU\) and
  distinguished the genuinely finite rows from coupled orbit problems.
- **12:49:29** — Added the explicit rank-one factor boundary, the full
  binary/source gcd transition ledger, Hurwitz collision codes through degree
  four, and the delta-invariant baskets for rational plane quartics. Verified
  mechanically that the master table contains exactly thirteen distinct
  rank-two numerical IDs and that the blind output directory contains only the
  taxonomy and this log.
- **12:55:34** — Blind phase ended. Read only the newly authorized
  `CANDIDATE_GLOBAL_TAXONOMY.md`, `CANDIDATE_INCIDENCE_MANIFEST.md`, and
  `candidate_manifest.json`. The thirteen candidate rank-two tuples agree
  exactly with the blind enumeration. Began a hostile audit separating:
  (i) canonical leading numerical rows, (ii) coarse incidence predicates, and
  (iii) orbit/moduli strata.
- **12:55:34** — Observed that the candidate's relative-algebraic-closure
  clause can close the blind uniqueness gap if it is defined as the relative
  algebraic closure of the projective ratio field inside
  \(\mathbb C(\mathbb P^2)\). This field is unique, and two generators differ
  by \(\mathrm{PGL}_2\). The integer enumeration alone does not prove this.
- **12:55:34** — Found a literal overlap in the 68-leaf prose:
  `Q2-E2-A2-B1-D1-N1/L02` allows \(h=\ell^2,p=\ell m\) with
  \(m=\ell\), hence \(p=h\), while `L04`--`L08` separately cover \(p=h\).
  No exclusion \(m\not\parallel\ell\) or priority rule is stated.
- **13:00:40** — Completed `../RECONCILIATION.md`. Proved that the canonical
  relative-closure pencil is not only unique: every other polynomial pencil
  presentation has degree \(ka\) for an integer \(k\ge1\). Thus the fourteen
  leading numerical rows can be certified under that precise principle.
- **13:00:40** — Final reconciliation verdict: the JSON and Markdown
  arithmetically agree on 68, but the incidence ambient space/equivalence and
  several predicates are undefined, key exhaustiveness assertions are
  unsupported in the authorized freeze files, one leaf overlap is explicit,
  and many leaves contain continuous moduli. Therefore 68 is not presently a
  certified exhaustive/disjoint/canonical denominator; it can at most become
  a conventionally frozen coarse bucket count after formal repairs. No finite
  orbit denominator exists.
- **13:14:22** — Completed the final hostile replay in
  `../HOSTILE_FREEZE_AUDIT_v1.md`, inspecting only the five authorized files.
  The revised fourteen-row mathematical core passed every counterexample
  attempt. In particular, the relative-closure curve is rational, the
  basepoint-free substitution is primitive, and UFD primitivity upgrades the
  projective factorization to the polynomial equality \(G=A(p,q)\).
- **13:14:22** — Verified independently that the JSON has 14 unique rows, the
  exact 13 rank-two tuples with correct ID mappings, 45 ordered chart IDs, 630
  row/chart intersections including empty ones, and a 7/7 status split. The
  45 pieces really are a complete disjoint locally closed coefficient-pivot
  partition, but not a Zariski-open atlas or a moduli classification.
- **13:14:22** — Marked the release artifact as fail-pending-correction because
  the nominally fail-closed verifier skips checksums when the checksum file is
  absent and overclaims semantic verification. Also requested that the frozen
  prose record the short rank-one/rationality/primitivity proofs, call the 45
  pieces locally closed pivot strata, and separate the meta-level coverage
  failure from the four mathematical boundary-routing rules. No fifteenth
  leaf is needed.
- **13:22:54** — Completed
  `../HOSTILE_FREEZE_REAUDIT_v1.md`. Every content blocker from the first
  hostile audit is corrected. The normalization, rank-one cone argument,
  relative-closure rationality, polynomial factorization, least-degree
  canonicity, fourteen-row completeness, locally closed pivot partition, and
  ordered routing all pass.
- **13:22:54** — Performed a content dry run of the corrected machine checks:
  exact ID/tuple mappings, the full thirteen-tuple set, exact monomial order,
  `C00`--`C44`, and Markdown/manifest row synchronization all pass. Static
  inspection confirms that the final verifier now requires a nonempty
  checksum file with an exact safe filename set and no longer claims to prove
  the geometry.
- **13:22:54** — Issued a content **PASS**. The manifest's pending status and
  absent checksum file are intentionally deferred mechanical gates. Once this
  re-audit is final, the authorized sequence is: mark the manifest frozen,
  generate mandatory hashes, run the verifier, then record the separate
  freeze certificate. Exclusion claims remain unaudited.
