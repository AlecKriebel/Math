# KP-3.41: large positive contact-surgery partials

Problem **2839 / KP-3.41**, rank **913**, remains **unsolved, 5/5**. The exact unchanged author freeze is independently accepted as stalled partial. No correction patch is required.

## Accepted scope and remaining gap

- Stabilization preserves a positive sharpness deficit for a fixed oriented representative; this does not exclude other representatives.
- Mirroring negative surgery preserves tightness but loses the required positive contact orientation. Nonzero rescaling cannot repair the sign.
- The admissible nonzero-LOSS tb barrier is **conditional on Li-Wan-Zhou arXiv:2510.05294v1**, Theorems 1.6(2) and 3.3. The external theorem proofs are not independently certified.
- The minimum **integer** threshold is the known value **2m** for positive **T(2,2m+1), m >= 1**. It rules out a uniform threshold, without refuting knot-dependent thresholds.

**Golla's iff criterion is for nonvanishing of the specified contact invariant, not for tightness.** The original problem asks for an entire tail of rational slopes with a knot-dependent integer threshold. Orientation, stabilization, knot-class and quantifier gaps remain. These partial deductions do not resolve or refute the arbitrary-knot problem and carry no novelty claim.

Read the [original analysis](author_original/REPORT.md), [five approaches](author_original/APPROACHES.md), [complete independent audit](independent_audit/AUDIT_REPORT.md), and [exact acceptance](independent_audit/ACCEPTANCE.json). Original pending-audit and not-published fields are historical, frozen bytes. [Publication metadata](PUBLICATION_METADATA.json) records this checkpoint. The canonical queue change is only Status = unsolved and Turns = 5/5; Findings and all unrelated bytes are preserved.

## Verification and trust boundary

Both original and audit ZIPs, their external manifests, every extracted member, the exact acceptance, and the final audit receipt are preserved unchanged. The frozen audit receipt reports 9 positive and 79 negative acceptance checks, with normal, -O, -OO and relocation coverage. The original checker trusts its supplied manifest: altered prose with updated hashes can pass. Those passes are trust-boundary diagnostics, never accepted revisions. The externally pinned acceptance wrapper authenticates the accepted bytes before executing the original checker.

The publication wrapper uses explicit fail-closed guards under normal and optimized Python. It verifies exact inventories, all archive/member equality and acceptance pins, then replays the authenticated acceptance verifier. Optional corpus and source inputs rehash all three complete corpus files, the complete target-record/report pair, and all seven supplied PDF pins. Omitted inputs are explicitly reported as not rechecked. Hash identity does not prove mathematical truth, provenance, novelty or completeness of literature search. This checkpoint reuses retained inputs; it makes no new source retrieval or visual-inspection claim.

No copied source PDFs, source extracts, dataset contents or private coordination files are included. Source titles, public URLs, hashes, sizes and inspection history are verification metadata only.

## Reproduce

Python 3.9+ and the standard library. Independently authenticate the publication manifest and verifier before executing package code. A modified verifier cannot authenticate itself. The trusted publication manifest SHA-256 is provided in the draft PR description.

    python3 -B verify_publication.py . --manifest-sha256 HASH
    python3 -B -O verify_publication.py . --manifest-sha256 HASH
    python3 -B -OO verify_publication.py . --manifest-sha256 HASH

Optional --base-queue and --queue must be supplied together. Optional --catalog, --problems and --reports must be supplied together. Optional --source-dir uses the seven filenames in independent_audit/SOURCE_CHECKS.json. See PUBLICATION_TEST_RESULTS.json for publication controls; the immutable audit receipt retains the prior audit tests.

Local verification is separate from GitHub CI. This is a draft research PR, with no merge, auto-merge, release, DOI or outside outreach.
