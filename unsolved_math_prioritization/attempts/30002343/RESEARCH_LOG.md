# Research and publication record

Problem 30002343; five substantive mathematical approaches are preserved in public/TURN_LEDGER.md. Publication and audit add no proof-search turns.

The original packet was frozen at manifest SHA-256 fe1428032c46c505cfa5e60dc7dd7a13b64535c2b90da8c00c83c85d95db53d8. The complete independent audit was frozen at b3a863367d03b38370e7f119fee86bb392e937b5d7cefec82f0a891ae646ca9c. The audit accepts the partial results unchanged. No correction patch or replacement proof is needed.

Source provenance and inspection scope are preserved in public/SOURCE_AUDIT.md, public/SOURCE_METADATA.json, and independent_audit/INDEPENDENT_AUDIT.md. The six historical PDF checks compared supplied local bytes, with independent online inspection of primary versions and publisher records; not every PDF was separately downloaded byte for byte by the reviewer. The source-free replay compares the historical public metadata and all remaining independent-check fields, while explicitly reporting that source_pdf_checks are not rerun.

The portable publication verifier authenticates a closed file/directory inventory against an externally supplied manifest hash, separately enforces the frozen author and audit manifest hashes and their complete inventories, then runs actual normal and optimized child interpreters. The audit's own legacy nested author commands omit optimization and isolation flags and are not separately probed; the publication verifier removes inherited PYTHON environment variables and additionally runs the author directly at the selected optimization level. No run is passed off as optimized merely because its parent was optimized.

Corruption tests execute a trusted separate verifier on disposable copies: altered or missing payloads, extra hidden files and directories, symbolic links, wrong anchors, malformed inventories, duplicate JSON keys, and attempted laundering of the frozen evidence are rejected. These tests assume a trusted interpreter and operating system, and are not a hostile-code sandbox or a formal mathematical proof.

Publication preparation checkpoint, 2026-10-07 UTC: 100% of the planned authored partial packet and source-free verification package assembled; remote publication is a separate verification step. This is completion of the scoped deliverable, not a percentage toward resolving the unrestricted mathematical problem.
