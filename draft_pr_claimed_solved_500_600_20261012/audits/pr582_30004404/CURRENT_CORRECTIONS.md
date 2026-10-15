# Current corrections to the frozen PR582 evidence

All 22 original files and completed review seals remain unchanged. These notes
reconcile their historical wording with the current verification and presentation.

1. **Khoi locator.** Cite Section 3, the unnumbered figure-eight example, printed
   p. 524. The historical designation “Section 3.1” is not a printed subsection
   number. The page and torus-bundle fact are correct.
2. **Historical verifier R1.** The original `verify_release.py` checks its supplied
   outer manifest but does not externally bind that manifest. Its constant
   `source_files_included: false` field does not classify arbitrary payloads.
   Root independently reproduced acceptance of a benign source-like file after
   extending the outer manifest. The actual original inventory is clean. That
   field must not be used as an independent exclusion-policy guarantee.
3. **Current original-inventory gate.** `verify_original_snapshot.py` pins the
   acquisition snapshot's SHA256, the reviewed head, and all 22 permitted paths
   and file hashes, including the original outer and two nested manifests.
   The baseline passes; added manifested PDF/corpus files and a resealed snapshot
   are rejected. The publication driver must run this gate alongside the full
   mathematical replays and enforce its own exact outer inventory. This checks
   consistency with known authored files; it does not certify authenticity or
   semantically classify arbitrary contents.
4. **Scope and credit.** Rational fillings include zero and exclude the meridian
   at infinity. The result refutes a universal affirmative assertion. It does
   not decide whether some other hyperbolic knot has a persistent rank-two free
   subgroup. The topology and metabelian ingredients are credited classical
   facts. The current priority audit is pending; this reconciliation provides
   no firstness or continued-open certification.

See `root_reproduction/ORIGINAL_STRICT_REGRESSION.json` for the new gate's
controls and `ROOT_MATH_ACCEPTANCE.md` for mathematical acceptance. Earlier
dated receipts may retain the old locator or a pre-repair status; this document
states the current interpretation. Paper and publication-driver integration
remain pending the priority gate.
