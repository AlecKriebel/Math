# Final readiness verdict — version 1.2.0

**Assessment date:** 2026-08-11

**Release type:** author-ready, non-destructive revision package

**Prohibited publication or communication actions performed:** none

## Verdict

The scholarly files are ready for author inspection and for creation of five
Zenodo **New version** drafts. They are mathematically and computationally
frozen. The Physical Review A Regular Article package is complete except for
the new version-specific DOI insertion and the author's private conflict and
account checks.

The package must not yet be described as published version 1.2.0 or submitted
to PRA. Five new version-specific DOI values do not exist locally and have not
been fabricated.

## Acceptance gates

| Gate | Result | Evidence |
|---|---|---|
| A — ZCW accuracy | **PASS** | Latest public arXiv v1 and its public repository/formalization were checked directly; `zcw_claim_comparison.md` records the boundaries. |
| B — claim boundary | **PASS** | The paper distinguishes fixed-qubit separation, unrestricted optimization, convexified equality, raw-set equality, setting minimality, exact symbolic checks, and formal proof-assistant verification. |
| C — priority restraint | **PASS** | July 30/August 2 public chronology appears once and is explicitly not a claim about private development, correctness, or misconduct. |
| D — main-theorem emphasis | **PASS** | Abstract, introduction, contributions, cover letter, and website draft foreground universal two-input convexified equality and the resulting 3-by-2 minimum. |
| E — mathematical freeze | **PASS** | The 21 frozen Main/Theorem/Lemma/Proposition/Corollary blocks have the same digest as v1.1.0; `paper/appendices.tex` and all exact artifact sources are unchanged. A new contextual Remark does not modify a dependency or conclusion. |
| F — build and verification | **PASS** | Both 36-page manuscript PDFs and both auxiliary PDFs build warning-free; every exact check and every applicable manifest check passes; all pages were rendered and inspected. |
| G — Zenodo readiness | **CONDITIONAL PASS** | Five clean payloads, metadata sheets, history, changelog, checksums, and upload instructions exist. The author must create five New version drafts and insert the returned DOI values before publishing. |
| H — PRA readiness | **CONDITIONAL PASS** | Regular Article PDF/source, cover letter, supplement, verifier, dossier, data statement, AI disclosure, and referee report exist. Insert new DOI values and complete private author checks before submission. |
| I — correspondence readiness | **CONDITIONAL PASS** | The email is accurate and restrained; insert live new-version links and send only after the Zenodo release. |

## Mathematical status

- No pre-existing theorem statement, proof, Bell functional, exact witness,
  displayed constant, or conclusion changed from the July 30 release. One
  new contextual remark records that either independent exact 3-by-2 witness
  supplies the existence half of the unchanged minimum-setting corollary.
- The 3-by-2 result remains an exact attained POVM lower bound above a global
  analytic fixed-qubit PVM upper bound; neither is relabeled as an exact
  optimum.
- The universal theorem remains equality of shared-randomness convex hulls,
  not equality of raw strategy images and not same-state or operator-level
  simulation.
- The universal convexity/extremality/reconstruction/rank-exhaustion proof is
  a manuscript proof. The programs check finite exact identities and explicit
  constructions; they are not a formal proof assistant for the universal
  theorem.

## Integrity status

- Frozen v1.1.0 directory: unchanged and manifest-verified.
- Immutable exact source artifacts: unchanged and manifest-verified.
- Version 1.2.0 core manifest: generated from the final tracked/public file
  set, excluding temporary and private material.
- New archives: assembled from explicit allowlists; ignored `tmp/`, virtual
  environments, editor state, build logs, and private submission planning are
  absent.

## DOI tokens requiring replacement

The post-upload checklist tracks exactly five values:

1. new standard-PDF version DOI;
2. new line-numbered-PDF version DOI;
3. new source-archive version DOI;
4. new checksum-object version DOI; and
5. new software-archive version DOI.

These tokens occur only in the intended author-action documents, draft site,
PRA availability materials, and post-release correspondence. The canonical
version 1.2.0 manuscript uses the already public July 30 paper and software
records rather than a fictitious future DOI.

## External-state statement

No Zenodo record was created or modified; no journal or arXiv submission was
made; no website was deployed; no email or other external communication was
sent; and no Git tag or hosted release was created. A review-branch push, if
performed after this report is frozen, is repository synchronization rather
than a Zenodo/journal/site/email publication action and must be disclosed in
the handoff.
