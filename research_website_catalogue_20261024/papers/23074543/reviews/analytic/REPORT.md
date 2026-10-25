# COMPLETE analytic-family review: Zenodo 23074543

The actual four-page manuscript supports both stated mathematical theorems. No central proof defect, counterexample to either stated theorem, or necessary mathematical source correction was found. This is the conclusion of one bounded independent analytic family, with written derivations and exact diagnostics; it is neither human peer review nor formal certification. Publication clearance remains with the root review. The 203-paper catalogue remains ongoing.

The reviewed object is **Irreducibility of exposed-point varieties of discotopes**, declared September 30, 2026, version 1.0, Full List row 91, DOI [10.5281/zenodo.23074543](https://doi.org/10.5281/zenodo.23074543). The complete actual PDF and controlling `sources/published-source/paper.tex` were read before any primary reference body or other review. All four PDF pages were rendered and visually inspected. The historical `verification/source_snapshot/proof.tex` was not used as the controlling manuscript and was never read for its argument.

## Strongest verified mathematical result

For any positive finite number of centered ellipsoidal balls D_i, each of rank at least two in a finite real ambient space, the complex Zariski closure E(D) of the exposed points of their Minkowski sum is irreducible. The ambient sum may be lower-dimensional, and the spans, radicals and discs may be dependent or repeated.

The proof is complete for these hypotheses. The supporting face is a singleton exactly when every projected normal A_i^T u is nonzero. Hence the exposed set is exactly the image of the support map

`F(u) = sum_i A_i A_i^T u / ||A_i^T u||`

on U, the complement of finitely many kernels of codimension at least two. A two-segment avoidance construction makes U path connected. The real positive square-root branch makes F analytic on all U. If a product of two complex polynomials vanishes on F(U), a nonzero value of the first factor leaves an open domain where the second composition vanishes; analytic uniqueness propagates that vanishing throughout U. The vanishing ideal is therefore prime. This is the explicit real-analytic-to-complex-algebraic bridge, not an inference from topological connectedness alone. See the immutable `EARLY_DERIVATION.md`, sealed before reference reading.

For the second theorem, assume full dimension and the written condition (GP): every concatenation of summand bases has the largest possible rank. A boundary sum of relative summand boundary points has a supporting normal u. The summands killed by u must, under (GP), have independent concatenated columns of total rank at most d-1. The transpose is onto, so one perturbing vector w can prescribe all their unit parameter vectors simultaneously. The perturbed regular support points converge to the original boundary sum, proving S(D) is contained in E(D). The reverse containment follows directly from regular support points. This establishes S(D)=E(D). The supplied Vandermonde construction proves that (GP) is a nonempty Zariski-open condition in the stated bases parameter space; reducing to the actual ambient span handles the original full-dimensional convention.

## Proof boundaries and independent diagnostics

Rank one cannot be included without qualification: an interval has two exposed points, and a planar disc plus a horizontal segment has two distinct conic components in its exposed-point closure. The theorem makes no universal claim about configurations containing rank-one summands. A global complex square-root branch, injectivity or maximal differential rank of F, independence of radicals, and strict convexity of the full sum are not used.

The manuscript's nongeneric distinction is exact. For two xy unit discs and one xz unit disc, its polynomial P vanishes on all regular support points, whereas P(e_3)=16 and e_3 belongs to the set generating S. Thus S can strictly contain E. This prevents replacing the second theorem by an unsupported nongeneric identification.

The independently written `independent_checks.py`, run with the existing Python 3.12.14 / SymPy 1.14.0 runtime, passed four exact diagnostic groups: polynomial division for this separation; a rank-(2,2,2) Vandermonde example in R^5 with two simultaneously vanishing nonorthonormal summands and an exact remaining support limit; a lower-dimensional nonround ellipsoid; and the translated-conic rank-one boundary. These diagnostics check formulas and difficult interfaces. The universal proofs are the preceding written deductions, not finite samples. An initial diagnostic run hit a SymPy matrix API mismatch; the calculation was corrected to componentwise limits before the successful receipt was produced. No manuscript or archive code was executed.

## Primary interfaces, credit and limits

The primary checks were performed only after the early seal. Gesmundo--Meroni's actual arXiv v2 body was checked at its Section 2, Definition 3.3, Theorems 4.3 and 6.1, Section 5, and Conjecture 8.2. Its S-definition and bases genericity match the manuscript; the acknowledged prior special cases and gradient mechanism are present. The general theorem and (GP) identification address the specified conjecture rather than degrees, birationality or the full complex critical locus. The arXiv record labels v2 a journal version; this lane could not fetch the publisher PDF/DOI successfully and does not assert byte equivalence with the 29-page publisher edition. See [the versioned primary record](https://arxiv.org/abs/2111.01241v2).

Meroni's actual EMS report, printed p.830, defines the exposed-point closure E and states the generic rank-at-least-two irreducibility claim. The first theorem therefore proves that precisely formulated conjecture with genericity removed. See [the primary EMS report](https://ems.press/content/serial-article-files/47009?nt=1).

Kucharz--Kurdyka's actual institutional PDF, printed p.95, proof of Proposition 4.3, records irreducibility of the real Zariski closure of an analytic image of a connected real analytic manifold. The manuscript properly treats that as a standard real precursor and supplies its own complex-coefficient primeness proof. See [the institutional primary record](https://dspace.uni.lodz.pl/xmlui/handle/11089/23776).

The bounded searches are documented in `READ_SEARCH_LEDGER.json`. Search silence is not novelty evidence. Historical first priority, exhaustion of all earlier work, and absence of later independent resolutions are **not certified**. The claimed contribution relative to the checked primary interfaces is mathematically supported; global novelty remains a separate attribution question.

## Source custody and timing

The frozen actual PDF is 79,805 bytes, SHA256 `c13dc861e8e5b5c1d980bdd78d14aff8e4b1a130800c4f942b3bedafbc5f6b2a`. The controlling TeX SHA256 is `3576dcc78bf1a9188ee8a8b5c56f5914357d90d437767e29dc42e3a85ceedab4`. The 692,895-byte original archive SHA256 is `55941d26dbadc3b244a6ba191e9e4503201c0deb3e2cde43178d5f0799564027`. Its 87 members pass CRC and path-safety checks; archived `paper.tex` equals the extracted controlling source. Every one of the 97 frozen source bindings was rehashed and preserved.

The authenticated record declares September 30, 2026 and version 1.0. Its record-created timestamp is October 1, 2026, 04:23:09.001448 UTC, equivalent to September 30, 21:23:09.001448 in America/Los_Angeles. These date labels are compatible across timezones. Neither record creation nor the October 25 retrieval establishes the exact first public availability time of the current file bytes; the record was updated October 10. No first-priority date is inferred.

All third-party fulltexts, extracts and renders remain in ignored caches; ignore status and primary byte hashes were verified before reading. Public review outputs contain short source-specific interface summaries, original derivations and receipts, not borrowed fulltexts. Original source files and early sealed artifacts were not changed. This family made no Git, source, site, configuration, shared-core, Sheet, UI, deployment, release or external-contact changes.

Final bounded-review completion estimate: **100%**. Discovery completion and catalogue completion are separate and are not claimed.
