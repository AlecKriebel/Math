# Verification scope

`verify.py` is a finite arithmetic, graph-partition example and identity checker, not a formal or exhaustive proof checker. Normal and optimized runs use explicit exceptions, so Python's `-O` does not remove the checks.

The full-input receipt was generated with separately supplied complete corpus files and the inspected source PDF. The standalone optimized receipt correctly reports those optional checks NOT_RUN. The complete pair was recomputed from all fields with the recorded serialization; no projected record was used.

The program checks 5,000 exact successive differences, 156,384 exact square-completion instances, 1,629 integer quadratic maxima, 1,001 positive palette-slack instances and 680 explicit edge partitions of the attaining-family examples. Three malformed partitions are rejected (missing edge, duplicated edge, and a nonedge inside a part); a fourth negative control detects that omitting the linear term changes the claimed extremal expression.

These computations do not certify the proof, the general extremal theorem, scholarly publication status, completeness of the search, or novelty. They do not prove that every public URL will remain accessible or every future download will have identical bytes.

The standalone checker does not hash all prose files. An edited report, or coherently rewritten checker and metadata, can pass a standalone run. Integrity of the entire accepted snapshot therefore requires the externally pinned archive SHA-256 and external member manifest, checked by a trusted process outside the mutable packet. No cryptographic signature or tamper-proof filesystem is claimed; read-only modes merely discourage accidental edits.
