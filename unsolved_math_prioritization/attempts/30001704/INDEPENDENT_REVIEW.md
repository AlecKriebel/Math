# Independent source and normalization review: 30001704

Reviewed 2026-10-01 UTC. Frozen author commit: `959430eaeec605e42320940ce61cf2707ab40b34` (`origin/dot/math-30001704`). The 12-file package was independently inspected at the fixed commit. This review covers source attribution, hypotheses, normalization, and diagnostic checks; it is not a fresh proof search.

## Verdict

**Mathematical/source-scope review PASS; one mandatory provenance-only correction before publication.** Retain **source/proof-validation hold, zero fresh proof-search approaches (0/5)**. The package correctly credits Swartz's prior affirmative theorem announcement and does not supply or claim an independently verified proof of the boundary finiteness theorem. This verdict neither declares the published theorem false nor declares the problem historically open.

## Exact source and scope

The original [OWR 8/2011 report](https://ems.press/content/serial-article-files/46323), Swartz contribution pp. 409–412, gives the three-dimensional boundary statement in Theorem 8(2), then asks for the higher-dimensional extension on p. 412. The extracted invariant and question agree with the recovered record. The original contribution distinguishes simplicial-complex triangulations from the nonsimplicial triangulations used for Matveev complexity.

The later [OWR 24/2012 report](https://ems.press/content/serial-article-files/46393), pp. 1427–1429, expressly assumes connected (d−1)-dimensional manifolds. Its complexity minimum is over the simplicial-complex category indicated by the subscript c. On p. 1429, Theorem 7 asserts finiteness of PL-homeomorphism types for fixed d and bounded Γ. The section requires d≥4, so geometric dimension is at least three. No orientability restriction occurs in this theorem. The formula, hypotheses, and theorem were checked in extracted text and rendered pages. No proof follows the theorem in this contribution.

The raw database sentence omits connectedness and category. Therefore every “exact match” or resolution statement must retain the package's qualification: **the intended connected simplicial/PL interpretation**. It must not be silently expanded to disconnected unions, arbitrary non-PL triangulations, or semi-simplicial complexes.

## Arithmetic and logical implication

For geometric dimension D and d=D+1, coefficient extraction gives

`h2 = f1 − D f0 + binomial(D+1,2)`.

Consequently the question's quantity q is exactly h2−v_int, and Γ(M)≤q for every eligible triangulation. A q≤N triangulation therefore places M among the types in the announced theorem with G=max(0,N). PL-homeomorphism finiteness implies ordinary-homeomorphism finiteness. The converse existence assertion uses the nonempty, integer-valued, bounded-below set of complexities, hence its minimum is attained. None of these deductions constitutes a proof of the announced theorem itself.

The cone-completion identity g2(completion)=q, boundary-facet stacking invariance, disconnected-union offset, and closed-normalization offset are correct. A cone vertex has link equal to the original boundary, so a solid-torus boundary produces a nonspherical link. The closed theorem cannot be transferred through this construction without new arguments.

The [2007 author manuscript of the 2008 closed theorem](https://pi.math.cornell.edu/~ebs/Edges.pdf), Theorem 2.1, explicitly excludes boundary. Its metadata correction to *Advances in Mathematics* 219(5) (2008), 1722–1728, DOI 10.1016/j.aim.2008.07.010 is corroborated by the recovered author publication list and Crossref JSON. The 2014 survey's boundary section and the 2020 boundary paper support the invariant/construction discussion; this review does not convert those related statements into a missing general proof.

## Independent diagnostics

The recovered `verify.py` was inspected as text but not executed. A separately authored standard-library checker, `independent_check.py`, passes **1,248 exact assertions**, saved in `independent_receipt.json`.

Coverage includes coefficient-basis polynomial checks; actual simplicial complexes; stacking face increments; cone counts and links; disconnected and closed offsets; the four recorded product-prism solid-torus examples; and nonzero interior-vertex controls from stellar subdivision of a simplex. Independent mod-2 homology yields [1,1,0,0] for the solid tori and [1,2,1] for their boundaries, with boundary vertex links verified to be cycles. All four author-receipt f-vectors and q=6 values match. The author's category counts sum consistently to 4,310, but no rerun of the original executable is claimed. These diagnostics are finite controls, not a topological finiteness proof.

All four hashes in `provenance.json` for the source record, mathematical report, verifier, and verification receipt match the recovered files. In particular:

- `SOURCE_STATUS.md`: `79bb15f7127d4bb41bf476582f41e582a5c08919294d65cb5503f5bf351e6feb`
- `verify.py`: `79ca8943c26ffa944ffd26811c763336f5f0384832b653dfb200b1b3672a6dca`

## Mandatory provenance-only correction

The first two entries of `source_manifest.json` pair EMS URLs with hashes/byte counts of the **MFO mirror PDFs**. Fresh retrieval independently recovered those exact historical bytes at the MFO URLs already cited in `SOURCES.md`:

1. For `owr2011.pdf`, replace only its `url` with `https://publications.mfo.de/bitstream/handle/mfo/3223/OWR_2011_08.pdf?isAllowed=y&sequence=1`. Preserve SHA-256 `41d86a57f750fb9c25a6e45fbd233454fda2afc00e9d92880ba8c40f7eef927f` and byte count 635326.
2. For `owr2012.pdf`, replace only its `url` with `https://publications.mfo.de/bitstream/handle/mfo/3295/OWR_2012_24.pdf?isAllowed=y&sequence=1`. Preserve SHA-256 `1b8092956b71893fb89a91645473247aaf25263588394cc814c98bac00b47a4d` and byte count 691091.

The EMS copies differ in binary representation. The decisive p. 412 (2011) and p. 1429 (2012) extracted text is identical between mirrors; the surrounding observed differences are formula-layout extraction differences. This is a URL-to-byte attribution correction, not a mathematical or source-statement discrepancy. All six other source-manifest entries were freshly downloaded from their recorded URLs and match both hash and byte count exactly. Details are in `source_retrieval_receipt.json`.

The correction does not change mathematical scope, the mathematical report, source-record hash, attempt accounting, or validation status. See the correction addendum for its verification. The historical pinned-corpus/prior-PR absence checks were not independently rerun; this review verifies their preserved record and directly checks the primary mathematical sources.

## Completion and stopping condition

Independent source/normalization review: **100% complete**. The provenance correction is verified in the accompanying `REVIEW_ADDENDUM.md`. Full boundary-proof validation remains on hold; no percentage toward a new discovery is claimed. No additional proof-search approach was consumed.
