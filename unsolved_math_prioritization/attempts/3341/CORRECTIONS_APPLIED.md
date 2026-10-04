# Corrections applied after independent audit

Date: 2026-10-04 UTC.

The original release and complete audit are preserved byte-for-byte. The corrected release differs only in PARTIAL_RESULTS.md and its regenerated SHA256SUMS:

1. C1 replaces the inaccurate all-zero-margins phrase with the precise statement that zero strips separate neighboring nonzero regions.
2. C2 distinguishes Gardy's exact-format definitions w=c h and w=P(h) from the uniform upper-bound domains B(C,d), without invoking its folding remark as a proved transfer theorem.
3. C3 supplies the one-way H/V-to-cyclic-successor interpretation needed to apply the cited recognizability theorem.

No mathematical claim, control implementation, recorded control output, novelty statement, remaining gap, or unsolved 5/5 classification changed. CORRECTION_PATCH.diff is the complete textual difference in the manuscript. The original audit remains an audit of the original freeze; the corrected packet implements its explicitly listed clarifications and correction.

Manifest hashes:

- Original release: f7b7257998fdaa783353f008e3364078176153416f2a264189932bfa885bb7ea
- Independent audit: 97ae24d8811eda55a2b751c84c7fbd622205a4f43aa89850a3a80ea81e836efd
- Corrected release: f8c482ed8a8cfdcebc6cb0b394d58afe8501d8af4d207dd01260edb53782382b

All three manifests are separately checked in the final repository layout. BUNDLE_SHA256SUMS additionally binds this publication's complete problem-specific payload, excluding only itself.
