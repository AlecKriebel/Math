# High-genus triangulation distances: accepted scoped partial results

**Problem 30005926 / OWR-14298373-004, rank 956. Unsolved after five substantive approaches (5/5).**

The independent audit accepts all twelve numbered results without a mathematical correction. The diameter constant and conjectured ratio three for uniform high-genus type-I triangulations remain unresolved. The typical-distance theorem is credited to Tanguy Lions; logarithmic diameter bounds and the strict diameter-versus-typical gap are credited to Budzinski, Chapuy and Louf. No novelty, human peer-review, or proof-assistant certification is claimed.

## Read the mathematics

- [Frozen author report](author/MATHEMATICAL_REPORT.md): parameter elimination, typical-to-extreme bounds, genus-preserving nonuniform obstruction, specified-tube first moment and cutoff, and a conditional extreme-decoration theorem.
- [Full independent audit](audit/AUDIT_REPORT.md): all twelve results reviewed, including boundary identifications, certificate multiplicities, logarithmic-window precision and conditional slot selection.
- [Audit verdict](audit/AUDIT_VERDICT.json) and [five-approach ledger](author/TURN_LEDGER.json).

All author and audit bytes are preserved. Statements such as “audit pending” and “not published” in the frozen author files record the historical author-stage state; the acceptance above and in the audit is the later disposition. No correction patch is needed.

## Portable reproduction

Python 3.10+ and the standard library only. Supply the independently retained SHA-256 of PUBLIC_MANIFEST.json, recorded in the draft PR, as EXPECTED_SHA256:

    python verify_publication.py --manifest-sha256 EXPECTED_SHA256
    python -O verify_publication.py --manifest-sha256 EXPECTED_SHA256
    python mutation_tests.py --manifest-sha256 EXPECTED_SHA256

The wrapper checks the complete file and directory inventory, every byte count and SHA-256, both independently anchored inner manifests, and both frozen ZIP inventories and contents before running either checker. It reproduces the author and independent outputs in normal and optimized Python modes byte-for-byte. It can be invoked from an unrelated working directory, without source PDFs, network access or the original work folders. The negative controls test corruption, coherent manifest rewriting, omitted/extra files, an extra directory, symlinks and false disposition claims with optimization both enabled and disabled. Explicit exceptions protect the guards from python -O.

The author controls comprise 57,292 exact finite checks and 12 Decimal numerical diagnostics (57,304 total). The independent program adds 15,042 controls, including 1,500 permutation-map tube surgeries with repeated vertices and edges on the boundary. The Decimal diagnostics are not interval-certified inequalities. Finite checks do not prove asymptotic results or the imported theorems. The separate optional symbolic-series record is evidence only and is not a replay dependency.

## Claim boundaries and provenance

The nonuniform tube construction is not a counterexample to the uniform-model conjecture. The fixed-pattern cutoff does not cover all deep decorations. The conditional theorem does not establish its hypotheses for high-genus triangulations. The remaining sharp depth tails, joint estimates, core diameter and attachment decomposition are stated explicitly in the report.

Public source metadata, PDF hashes, byte counts and inspection limitations appear in [author sources](author/SOURCES.json) and [audit source verification](audit/AUDIT_SOURCE_VERIFICATION.json). No copied source documents, source extracts, dataset contents, private sources or private coordination files are included. The previously supplied full-corpus hashes are provenance metadata, not a fresh remote-dataset verification.

The original author archive is AUTHOR_FREEZE.zip, SHA-256 aefc84ee9e468a4c39bdf06a4938948f34e98c939365023bba30f903cd771a4f (19,670 bytes). The original audit archive is AUDIT_PACKET.zip, SHA-256 48960aa6f74cd82e7329283b17a3f48fa0a484080ab26d99d356069cc5a35043 (22,883 bytes). Both contain only the manifested, source-free files also provided here as loose files.

Public references: [Lions, arXiv:2606.27357v1](https://arxiv.org/abs/2606.27357v1); [Budzinski–Chapuy–Louf](https://doi.org/10.1214/24-AOP1746); [Oberwolfach target](https://doi.org/10.4171/OWR/2024/25). Literature findings are bounded by the dated source-inspection record and are not exhaustive status certification.
