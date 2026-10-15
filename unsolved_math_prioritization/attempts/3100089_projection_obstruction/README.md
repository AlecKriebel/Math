# Unbounded recovery distance after one-vector augmentation

This symbolic appendix to [draft PR #1313](https://github.com/AlecKriebel/Math/pull/1313) concerns database problem 3100089 (AMR-030-0089). It gives a complete elementary proof and independent mathematical audit of a limitation on a possible saturation-based proof strategy. The original general pressing-connectivity conjecture is unresolved by this work. No novelty claim is made.

## The exact result

For every integer r≥2, start with a path on r vertices with one endpoint black. Its Gram matrix over F₂ has rank r and exactly one successful pressing word S=(0,1,…,r−1). One additional norm-one coordinate gives a rank-r path on r+1 vertices with both endpoints black.

In the augmented successful-word graph, with edges LCS≥r−4, a specified complete two-word reverse fiber has exact minimum distance

ceil((r−1)/4)

to the original word set {S}. The same exact distance holds from its full-matrix trajectory to the old-realized trajectory in the full augmented trajectory quotient, where changing representatives within fibers is free.

This quotient claim explicitly includes both representatives of the old trajectory: S and (0,1,…,r−2,r). It does not confuse the old-word subset with the old trajectory's full augmented fiber. The word-distance assertion is the minimum from the whole reverse fiber; no equality for each individual representative is asserted.

The augmented graph is nevertheless connected under the stronger threshold LCS≥r−1. Thus the result rules out a uniformly bounded recovery radius, including nearest-neighbor recovery, without producing a disconnected original or augmented word graph. Unrestricted nonlocal retractions, component preservation, and path rerouting remain outside the negative result.

## Definitions and normalization

For a symmetric matrix M over F₂, a legal press at v requires M_vv=1 and replaces M by M+(Me_v)(Me_v)ᵀ. A successful word is a sequence of legal presses ending at the zero matrix. A full trajectory records all intermediate matrices on the fixed full label set. A fiber contains every successful word with precisely that trajectory. The quotient graph joins distinct trajectories when some pair of their representatives is adjacent.

Here every successful word has length r. The original Bixby–Flint–Miklós threshold LCS≥r−4 permits at most four deletions and four insertions, or eight insertion/deletion edits in total. It is not a combined four-edit budget. The primary normalization source is [Bixby, Flint and Miklós, “Proving the pressing game conjecture on linear graphs,” Involve 9:1 (2016), 41–56, Conjecture 6 on p. 47](https://msp.org/involve/2016/9-1/involve-v9-n1-p03-s.pdf). The proof below does not invoke an external theorem.

## Contents

- [Complete symbolic proof](UNBOUNDED_PATH_PROJECTION.md), preserved byte-for-byte
- [Independent symbolic audit](AUDIT_REPORT.md), including the complete unchanged reconstruction and bounded-check scope
- [Acceptance and exact limitations](ACCEPTANCE.json)
- [Aggregate verification metadata and integrity pins](VERIFICATION.json)
- [Public primary citation and inspection history](SOURCE_METADATA.json)
- [Edition changes](EDITORIAL_MAP.json), [scope review](SCOPE_REVIEW.md), and [closed manifest](MANIFEST.json)

The audit is AI-assisted and unrefereed; it is not external human peer review or proof-assistant certification. Finite checks on ranks 2–10 corroborate the complete symbolic argument. No code, raw matrix certificates, enumerated datasets, copied source documents, or separate finite witnesses are included, so the packet is not a self-contained executable reproduction bundle.

This is a separate sibling of the normalization report and the positive-connectivity appendix. It adds nothing within either previously closed directory and requires no edits to their manifests. The complete proof does not depend on the earlier finite witnesses or on the separate residual-equivalence note.
