# Adversarial mathematical-scope review of v1.1.2

## Scope examined

I reviewed only the current canonical
`source/paper/main.tex`, `source/supplement/supplement.tex`,
`reviews/v1_1_2_release_hardening/REVIEW_DISPOSITION.md`, and the changes to
those materials relative to commit `888d9059`. I did not replay the finite
atlas or reassess unchanged theorem dependencies.

## Mathematical verdict

I found no theorem-level expansion, weakening, convention drift, parameter-
domain change, or altered Omega/Theta claim in the v1.1.2 edits.

The Section 10 change from “exact infinite-data JC observations” to “generic
exact infinite-data JC observations” is mandatory and correct. It brings the
informal biological-consequence sentence into literal agreement with
Corollary 1.2, which excludes a proper algebraic exceptional subset. It does
not weaken the formal theorem; it repairs an overbroad exposition sentence.
The immediately following “Away from the stated proper algebraic exceptional
set” paragraph remains consistent with this wording.

The change from “independently implemented replay” to “separately implemented
replay” is also correct. The disclosure explicitly defines the phrase as a
code-independent implementation and expressly disclaims independent human
review. The abstract, supplement, reproducibility discussion, and disclosure
therefore no longer invite the stronger human-independence reading. This
terminology does not alter the mathematical role of the replay certificates.

The reproduction-command edit in the supplement changes no mathematical
claim. It correctly treats the linked repository as a monorepository and uses
the project-directory prefix. The version-link change likewise has no effect
on the theorem, provided the referenced release actually exists when the
manuscript is released.

I specifically found no changed text that:

- broadens the fixed-mixed-graph, already-simple, reticulation-preserving
  convention;
- moves Theta or Omega into the strong class;
- changes the open JC domain (0<x_e<1), (0<\lambda_r<1);
- upgrades a common regular germ to equality of complete stochastic images;
- asserts physical bridge-parameter recovery;
- converts generic identifiability into pointwise identifiability; or
- recasts separately implemented code as external human review.

## Submission-blocking release-status inconsistency

The current bytes nevertheless contain one falsifiable status claim that is
not yet true. `REVIEW_DISPOSITION.md` says that the v1.1.2 archive, envelope,
manifests, and clean transcripts “are published as assets of the v1.1.2
GitHub Release.” The paper's data-and-code statement also points to the
`stc-jc-sharp-boundary-v1.1.2` tag. A direct public check found neither that
GitHub Release nor that remote tag. Thus the mathematical source currently
contains a broken public data/code link, and the disposition describes a
future release-engineering step as completed.

This is not a defect in the classification, genericity argument, Omega
family, Theta family, or parameter domain. It is, however, a submission-
blocking provenance inconsistency in the exact files under review.

## Mandatory corrections

1. Before freezing or submitting the PDFs, publish the exact v1.1.2 tag and
   GitHub Release with the archive, envelope, manifests, and clean replay
   transcripts named in the release documentation; verify the manuscript URL
   resolves and the published asset hashes match the active metadata.
2. If publication has not yet happened when `REVIEW_DISPOSITION.md` is
   committed, change its present-tense statement to an explicit pending
   requirement. Restore the present tense only after the public release check
   passes.

No mathematical-scope correction is otherwise required.

HOLD

## Dated re-review — 2026-08-16

### Scope and method

I re-reviewed the current working tree after addition of the bioRxiv,
Systematic Biology, and Journal of Mathematical Biology packages, including
the JMB-specific manuscript and Online Resource~1, the revised v1.1.2
disposition, and the split offline/public release gates. I did not recompute
the unchanged finite atlas or reassess its exhaustiveness.

I compared the article sources embedded in all three source ZIPs against the
canonical article. The Systematic Biology variant changes only review
formatting, one display's line breaking, and figure alt text. The JMB variant
adds the Online Resource~1 citation and groups unchanged declarations under
the journal's heading. Its Online Resource~1 changes only the identifying
title block. None of those transformations changes a theorem, hypothesis,
network convention, parameter domain, observational relation, Omega/Theta
statement, or genericity qualifier.

I also ran the bounded relevant checks:

- `verify_release_hardening.py` returned
  `PACKAGE_CANDIDATE_VERIFIED`, explicitly with
  `REQUIRES_POST_UPLOAD_EXTERNAL_GATE`, and rejected its eight targeted
  mutations;
- `verify_submission_source_archives.py` extracted all three source ZIPs,
  executed their documented commands literally, and reproduced all six
  packaged article/supplement PDFs byte for byte;
- `verify_public_release.py` failed because the public v1.1.2 release does
  not yet exist, which is the required fail-closed behavior; and
- `verify_active_release.py` failed because the active artifact inventory and
  hashes have not yet been core-sealed to the current package bytes, again
  showing that the working tree is a candidate rather than a completed
  release.

### Mathematical-scope result

The mathematical source remains sound relative to the previously audited
v1.1.1 theorem. The v1.1.2 wording still makes the correct distinctions:

- generic rather than pointwise identifiability;
- the fixed, already-simple, reticulation-preserving mixed-graph convention;
- the open JC domain only;
- projective local tensors rather than physical bridge multipliers;
- a common regular triangle germ rather than equality of complete stochastic
  images;
- Omega and Theta only as weak-but-not-strong sharpness families; and
- separately implemented code replay rather than external human specialist
  review.

The journal cover letters and metadata do not broaden the class beyond the
manuscript when read with their express reference to the convention stated
there. The JMB Online Resource~1 is correctly identified and introduces no
new mathematical claim.

One minor journal-facing sentence should nevertheless be narrowed before
freeze: the JMB cover letter says that exact certificates support “every
finite computation.” The article makes the defensible, enumerated claim that
the load-bearing finite-atlas, membership, Fourier, sign, and Jacobian claims
are certified. “Every finite computation” could encompass exploratory or
incidental calculations not claimed by the theorem. Replace it with “the
load-bearing finite computations” or the article's enumerated formulation.

### Remaining truthfulness defect in the active release surface

The new two-stage verifier architecture is correctly fail-closed, and
`REVIEW_DISPOSITION.md` now truthfully says that publication is conditional
on the post-upload gate. Several other active files still contradict that
status:

1. `STATUS.md` says v1.1.2 “publishes hash-bound current replay assets.”
2. `CLAIM_DEPENDENCY_GRAPH.md` and
   `THEOREM_CERTIFICATE_CROSSWALK.md` describe the envelope as already
   attached to the public v1.1.2 release and classify the publication portion
   of `V112` as verified.
3. `README.md` describes the sealed evidence as recorded in the public
   release and opens with the unqualified phrase “independently verified,”
   despite the submission disclosure's careful distinction between
   separately implemented code and independent human review.
4. `PERSISTENT_ARCHIVE_CHECKLIST.md` says the first eight files “are also”
   the exact public assets although the public release is not yet present.
5. The current `RELEASE_METADATA.json` still contains the preceding PDF,
   source-ZIP, and source hashes and lacks the complete v1.1.2 artifact
   inventory; this is why the active-release verifier correctly rejects it.

The manuscript's future release URL and the machine-readable target envelope
URL are acceptable in a candidate only because submission is explicitly
blocked until the post-upload verifier succeeds. The present-tense status
claims above are not similarly conditional. As written, they make the active
repository internally inconsistent: the disposition and executable gate say
“candidate pending upload,” while the status and crosswalk say “published and
verified.”

### Mandatory corrections before PASS

1. Conditionalize the cited present-tense publication statements, or update
   them only after the public tag and eight assets exist and
   `verify_public_release.py` returns `PUBLIC_RELEASE_VERIFIED`. Until then,
   `V112` should distinguish package-candidate verification from publication
   verification.
2. Core-seal `RELEASE_METADATA.json` to the final immutable source and all
   current bioRxiv/journal bytes; then create clean-checkout transcripts,
   archive and envelope, publish the tag and assets, and run the external
   gate. Do not call the exact package final before both the active-release
   and public-release gates pass.
3. Replace the README's unqualified “independently verified” wording with
   language consistent with the manuscript disclosure, such as “checked by
   exact primary and separately implemented replay certificates.”
4. Narrow “every finite computation” in the JMB cover letter as described
   above.

No mathematical theorem correction or de-scoping is required. The hold is
entirely for truthful release-state wording and completion of the already
designed post-upload seal.

HOLD

## Final disposition after mandatory corrections — 2026-08-16

I re-read `STATUS.md`, `CLAIM_DEPENDENCY_GRAPH.md`,
`THEOREM_CERTIFICATE_CROSSWALK.md`, `README.md`,
`PERSISTENT_ARCHIVE_CHECKLIST.md`, the JMB cover-letter source and rendered
PDF, and `REVIEW_DISPOSITION.md`.

The four mandatory corrections from the preceding re-review are complete.
Publication language now distinguishes a verified source/package candidate
from public evidence accepted only after `verify_public_release.py` returns
`PUBLIC_RELEASE_VERIFIED`; the README no longer implies independent human
verification; the JMB cover refers only to the load-bearing finite
computations; and core sealing, clean transcripts, upload, and public
download verification remain explicit subsequent gates. The offline
hardening check still reports only `PACKAGE_CANDIDATE_VERIFIED` with a
required external gate.

These changes introduce no theorem-scope drift, convention change,
parameter-domain change, genericity overclaim, or alteration of the Omega,
Theta, bridge, containment, or triangle statements. The present PASS applies
to the mathematically sound and truthful source candidate; it does not assert
that the still-separate public upload gate has already passed.

PASS
