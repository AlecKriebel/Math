# Publication boundary and explicit skips

The original authored folders contain mathematical reports, author-created check scripts/results, acceptance reports, and public bibliographic/integrity/inspection metadata. Only those allowlisted files and the new publication guide, research log, manifest and source-free driver are included.

Excluded: source PDFs, copied/extracted source text, HTML source pages, screenshots and page renderings, dataset contents, private sources, private personal data, correspondence, and coordination material. Public manifests may retain a retrieved filename, hash, byte count, public URL and inspection history for an excluded source document; those are metadata, not the document.

Reproducibility distinctions:

- Nine unchanged historical scripts use only authored inputs and available mathematical Python libraries. The driver supplies their original relative layout in a temporary directory, with the packet root as the working directory. They should not be assumed to work from an arbitrary working directory when invoked directly.
- `theta_cusp_growth_audit/authored/verify_cusp_audit.py` additionally reads the excluded source PDFs named in `PUBLIC_CUSP_AUDIT_SOURCE_MANIFEST.json`. The source-free driver skips this complete historical script and reports the reason. Its separate elementary cusp checks do not claim to rerun the PDF checks.
- Original generated JSON outputs are preserved byte-for-byte as historical records. A `true` source-inspection or source-hash field in such a record is a historical claim supported by the original audit, not a new source-free verification.
- Public-source PDFs have not been re-fetched or re-inspected for publication packaging. Their bibliographic status and inspection metadata are dated records from the 7 October 2026 audits. A source-free reader can retrieve the public sources separately and compare the published pins.
- No numerical hyperbolic uniformization, actual torsion-connection comparison, full geometric recursion, or formal verification is performed by `verify.py`.

No release, DOI, merge, auto-merge, or outside-author contact is part of this publication.
