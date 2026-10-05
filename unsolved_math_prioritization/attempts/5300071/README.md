# Relaxed Newton common-arc problem: audited partial results

**Problem 5300071 / AMR-052-0071, source rank 650: unsolved; five of five
approach families used.** The independent audit passes the packet only at this
partial-result scope. There is no complete candidate or verified prior resolution.
The general degree-uniform common arc in the intersection of immediate basins
over every real 0 < h <= m remains unproved. Estimated completion remains 10%.

The verified partial results are a common local trapping disk, the one-root case,
the full target for equal-multiplicity two-root polynomials, and an exact
obstruction to one proposed direction of basin nesting. Finite controls support
these arguments but do not resolve the full parameter continuum or general
exterior-arc estimate. The literature search is bounded; no universal claim about
current literature status is made.

## Files and historical records

- `submission/` contains all 13 frozen author files unchanged.
- `audit-independent/` contains the full 11-file independent audit unchanged.
- The two ZIP files preserve exactly those two frozen inputs.
- `RELEASE_CLARIFICATION.md` implements the audit's minor Blaschke-hypothesis
  clarification separately, without rewriting frozen author history.
- `RELEASE_STATUS.json` records the current, narrowly scoped verdict and bindings.
- `SHA256SUMS.json` and `verify_release.py` bind the complete publication packet.

The author's original status says that independent review was pending, and the
audit states that the reviewer performed no publication. These are preserved
historical statements. The later independent verdict is in
`audit-independent/AUDIT_STATUS.json`; the publication scope is recorded here and
in `RELEASE_STATUS.json`. The clarification does not reopen the exhausted search.

## Portable checks

Python 3.10 or newer and its standard library suffice. No network, external
packages, scholarly PDFs, source text, corpus contents, or private files are
needed. From this directory run:

    python verify_release.py
    python submission/verify_manifest.py
    python audit-independent/audit_verify.py submission rank650-5300071-author-freeze.zip
    python audit-independent/integrity_negative_controls.py submission

To replay the author outputs, write outside this frozen directory:

    python submission/verify.py > /tmp/relaxed-newton-replay.json
    python -c "import json; assert json.load(open('/tmp/relaxed-newton-replay.json')) == json.load(open('submission/CONTROL_RESULTS.json'))"

Only public-source verification metadata is included: titles, URLs, hashes, byte
counts, inspection/retrieval history and publicly stated manuscript status.
No scholarly PDFs, extracted source text, dataset contents, source-page images or
private coordination files are redistributed. This draft proposes no merge,
release or DOI, and does not run the queue manager or alter Findings.
