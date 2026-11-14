# Complete independent adversarial review — Zenodo 23383952

**The full original finite theorem is supported. No central mathematical gap, counterexample to the theorem or required source correction was identified.** The literature/version access limits below remain explicit. This is an AI review; publication authority is retained by root. The complete custom disposition is `VERDICT.json`, with no generic-PASS normalization of this or any original object.

The paper is *A finite counterexample to the weighted Yamabe heat trace comparison*, Alec Kriebel, actual four-page manuscript and complete 13,427-byte controlling `note.tex`. Both reader and API say version 1.0.0 and 13 October 2026. API creation is 15 October 2026, 04:00:37.039113 UTC; this is not relabelled as the declared manuscript date.

## Literal result and exact original target

The theorem specifies one finite smooth positive conformal weight W on the unit round S³ with integral W^(3/2)=2pi², and t*>0, such that

    t*^(3/2) Tr exp(-t*Y_W) >1106714561/1700054750>13/20,
    max(t>0) t^(3/2) Tr exp(-tY0)<321/500.

Here Y0=Delta+3/4 with positive Laplacian, and Y_W=W^(-1/2)Y0W^(-1/2) acts on the round L² space. Both time maxima are attained at positive finite times. The actual [original OWR item(16)](https://ems.press/content/serial-article-files/46205), printed 421–422, defines precisely this operator, normalization and universal n≥3 maximum comparison. Its separate monotonicity conjecture concerns n≥4. The n=3 example refutes the universal comparison; the restricted n≥4 comparison and separate monotonicity statement remain unaddressed.

## Independence and universal derivation

The complete actual four pages and all 317 TeX lines were read before inventory triage, foreign bodies, mathematical source code or historical/current opinions. The substantial initial mechanism and falsification plan were sealed at `EARLY_SEAL.json`, SHA256 `3f4ddfe9b8e1d241cfa6923f2b8cb821a92e2467d45bdabd3e929bf7f61dc68c`. No current/root final report, sibling verdict or archived audit conclusion was read to reach this disposition. The full proof is checkable in `DERIVATION.md`; `PROOF_BOUNDARIES.md` records the attempted failure mechanisms.

The construction is genuinely finite. On the cylinder coordinate s, the flat cutoff yields an exact product cylinder of length L=10000 and explicit sech tails. Pole coordinates turn the metric coefficient and weight into positive smooth rational functions of the squared Cartesian radius and finite E=exp(10000). The apparent absolute-value corner is inside a region where the cutoff is constant. No numerical evaluation of E or passage to a singular limiting metric is used. The exact cap estimate gives 4piL≤VL<4pi(L+4).

Set a=(2pi²/VL)^(2/3), h=a gL, W=a WL and t*=4a. This gives the required integral normalization. Conformal covariance and the unitary multiplier W^(3/4) identify the geometric Yamabe operator on h with the exact historical weighted operator. Its quadratic form gives a strictly positive spectral bottom, even if transition scalar curvature has negative values. Smooth compact ellipticity gives finite positive-time traces.

The zero-extended cylinder Dirichlet sine modes are legitimate global H¹ trial functions because their boundary traces vanish. They are not claimed to be global smooth eigenfunctions. Their k-dimensional spans give the kth full eigenvalue bound, with multiplicities included. Finite partial heat sums followed by a monotone limit and a Gaussian integral yield the trace lower estimate. Constant rescaling, including the time and its prefactor, gives exactly 16pi²/VL times the time-four unscaled trace. The strict cap-volume bound then produces the literal lower fraction and margin 3357947/3400109500 above 13/20.

For the round sphere, eigenvalues are j²-1/4 with multiplicities j². Differentiated Gaussian Poisson summation controls all small times 0<t≤7/5. Monotonicity of the first mode and all remaining modes gives universal endpoint bounds on six closed intervals covering [7/5,2], with an explicit infinite geometric-tail estimate. All spectral summands decrease for t≥2, controlling the entire remaining half-line. Thus the global bound does not come from sampled time values or a truncated numerical trace.

Finally, normalized leading heat coefficients give the zero-time limit sqrt(pi)/4, while positivity gives exponential decay at infinity. The weighted finite lower value and a round first-mode value at t=2 both exceed that zero-time limit. Continuity then puts each supremum in a compact positive-time interval, where it is attained. This checks the theorem's two maximum claims, not just its numerical separation.

## Own exact certificate and controls

Before opening the supplied checkers, `independent_rational.py` was independently authored from the sealed plan. It encloses pi using the Machin identity and alternating arctangent remainders; encloses exp(-x) with alternating degree 12/13 sums at x/32 raised to the 32nd power; and brackets square roots with integer calculations on a 2^40 lattice. This differs from the manuscript's P50 positive-series reciprocal implementation. Every decision uses exact integers/Fractions and explicit guards.

It independently verifies all seven literal time-region ceilings, the finite lower fraction, its stated margin, strict constant bounds, cap estimate, rescaling exponents, valid tail factor and maximum-attainment inequalities. Its rational upper fractions are displayed in `DERIVATION.md` and retained in `EXACT_RESULTS.json`. The exact weighted-lower-minus-coarse-round-upper margin is 33272110381/3400109500000>0. The strengthened 321/500 round conclusion is verified, together with the older weaker 129/200 threshold.

Two pristine runs, ordinary and optimized Python, passed. Seven changed formulas/assumptions reject in each mode: wrong unitary exponent, normalization exponent, time rescaling, weighted threshold, small-time Poisson sign range, tail factor and round table ceiling. These fourteen intended rejections are retained. The checks are controls on exact arithmetic and exponent algebra; smoothness, form domains, min–max, Poisson summation and heat asymptotics are supplied by the written proof with their hypotheses.

The complete 119-line supplied trace checker and 149-line geometry checker were inspected after our first independent certificate. Only the readonly trace checker was executed once, successfully. The geometry checker writes its result beside its source, so it was not executed. No source builder, finalizer, publication verifier, archive program, historic harness, copied fixture, new environment or compiler was used.

## Primary credit, exact editions and remaining access limits

`PRIMARY_LEDGER.md` gives exact interfaces and coordinates. Actual OWR PDF 67–68 and pixels authenticate the original comparison. Actual AJ v1 pages 1–6 and the exact December 8, 2008 author manuscript pages 1–10 were read. The latter is an authenticated existing ignored 15-page body, not a new HTTP acquisition. The v1 body has an actual 3 August 2007 header and internal 14 May 2019 typesetting date; these remain distinct from the 2008 edition. [Official Cambridge metadata](https://www.cambridge.org/core/books/abs/variational-problems-in-differential-geometry/supremum-of-first-eigenvalues-of-conformally-covariant-operators-in-a-conformal-class/A744D3E0755DF6EAF2201702FBDA4D6D) confirms the cited 2011 chapter identity, pp. 1–23 and DOI. A complete publisher-chapter body was not inspected.

The long-cylinder/Pinocchio conformal geometry, its predecessors, Dirichlet subspaces and spectral mechanism are established prior ingredients. The assessed contribution is a specified finite quantitative application to the exact historical heat-trace question. Our proof does not depend on importing the full AJ asymptotic spectral theorem.

The ordinary final-Morpurgo request returned 200 with non-PDF bytes, and ordinary ResearchGate access returned 403 HTML. The web reader exposed selected [author-uploaded transformed-trace interfaces](https://www.researchgate.net/publication/38337286_Sharp_inequalities_for_functional_integrals_and_traces_of_conformally_invariant_operators): its continuous convex test functions/integrability requirements and transformed-trace/zeta statements were directly read. A point-time Laplace delta is outside that stated continuous test class, so these interfaces do not directly assert the time-maximum comparison. This is a bounded interface inference, not a complete authenticated final-Duke-body audit. No failed response is counted as a PDF, and no unavailable edition is asserted.

Six actual focused queries, direct-open failures and selected interface reads are recorded in `READ_SEARCH_LEDGER.md`. They certify neither historical priority, firstness nor current openness. No historical search/review count or release-acceptance narrative was adopted. Extensive AI use and unrefereed status remain explicit; human peer review and formal proof-assistant certification are false.

## Custody and final handoff

The actual reader is 98,620 bytes, SHA256 `05ab26248c64b1e8dc7aa9c89e1eabd03142226dcefd32a622f78283af839de1`. The controlling TeX is 13,427 bytes, SHA256 `fffd5eea1ed89e06e2e987bea4323ad63768b1a4fd8ed0a11c52e8e25b976a43`. The source-ready seal is `bd759f183997313109e614402cdd3a40fc155fe3e0148d3e7579a899d779d5bf`.

All 151 original ready-manifest files plus its manifest/seal were rehashed. All four ZIP containers and 142 regular payload occurrences, including three nested original evidence ZIPs, were independently CRC-read and hash/extraction checked; total expanded bytes 928,042. The embedded `note.pdf` equals the selected standalone four-page reader. There is one controlling TeX candidate. Payload hashing does not mean archived opinions were read or endorsed.

The complete native source schema `all_assets_in_original_order`/`original_api_file_object`, PDF-before-ZIP order, original checksumcase, paths, raw metadata, full API objects and actual ordered transport headers are preserved unchanged. No aliases, invented transport fields, receipt rewrites or generic-PASS objects were created. `INPUT_BINDINGS.json` additionally binds three actual primary bodies, two raw custody receipts and seven ignored derived cache files. Web-only metadata/transcription access is labelled separately and has no fabricated PDF hash.

`verify_review.py` is read-only, checks the sealed bytes/native contracts/actual reader and all recursive payloads, and rejects seven in-memory changed custody cases in ordinary and optimized Python. It does not execute source programs or prove the mathematics. `SOURCE_PRESERVATION.json` preserves exact receipts and ignore boundaries. Future additive source envelopes can be separately authenticated without changing this packet.

This bounded adversarial assignment is complete at 100%. Original sources, early objects, previous 107 and other packets, siblings, shared/core/site/config/native/UI/Git state were not modified by this lane. No outreach was prepared or initiated. Publication clearance remains false, root authority is retained, all 203 papers remain ongoing, and no follow-up is scheduled.
