# Coding repair research log

## 2026-10-06 21:24:11 America/Los_Angeles / 2026-10-07 04:24:11 UTC

- Inspected Hsieh–Wilde 0903.3920v1 Eq. (4): it retains the consumed secret key in the secrecy target. The source cannot be cited as proving the conventional consumed-resource corner under its literal stronger promise.
- Independently inspected preceding Hsieh–Luo–Brun 0806.3525v1 Eq. (11): it traces consumed-key registers and requires decoded-message/Eve decoupling. This supports the conventional interpretation, but does not cure the later printed condition.
- Derived finite-dimensional key-selected satellite coding directly. Conditional quantum soft covering uses spectral projectors and an explicit centered Hilbert–Schmidt variance estimate; packing uses Hayashi–Nagaoka Lemma 2. Averaging over consumed key gives generated-message secrecy even after public label disclosure.
- Derived cost admissibility by independence across codeword positions and bounded scalar concentration. Supplied expurgation preserving average cost under an energy margin. The photon cutoff stays fixed during the coding limit.
- Strongest result: a finite cq ensemble gives corner (I(X;B),I(Y;B|X),-I(Y;E|X)) under generated-message trace secrecy, with bounded average cost, pending independent audit. It does not prove joint residual secrecy of consumed key.
- Remaining gaps outside this lemma: bosonic Gaussian discretization/cutoff continuity, full resource-cancellation conventions, upstream entropy dependency, novelty/complete-package audits.
- Mathematical completion of assigned lemma: 95%; publication-package completion of assigned note: 20%. These percentages are best guesses, not evidence.
- Public arXiv version pages checked: Hsieh–Wilde v1 (2009-03-23), Hsieh–Luo–Brun v1 (2008-06-21), Devetak v6 (2004-10-21), Hayashi–Nagaoka v4 (2003-02-28); no later arXiv version appeared on the checked pages. Hashes of pinned retrieved PDFs were computed without storing PDFs or modifying source clones.

Exact note/source metadata hashes at this checkpoint:

```json
{
  "DIRECT_CODING.md": "48f64a4071ccb6d93e5ddda2b69c8d10354c3c50601fe2929aefc2df2ed15adf",
  "SOURCE_HASHES.json": "7c5a799733d772f02725340795644686c77aa4ad20ebd92a0b23bcff5fa33191"
}
```
