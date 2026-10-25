# Source and scope review: Zenodo 23442760

Completed 2026-10-25T07:21:07.994006+00:00. Full List row95, *Quadratic convergence of SOS-density bounds on convex bodies*. Independent GPT-6.1 Sol Ultra lane; no publication or promotion authority.

**The complete original main theorem, C² extension and stated worst-case proposition pass this review; no central mathematical gap was identified.** The exact explicit bound holds for every integer order, using one global square normalized over the entire body. The primary comparison confirms substantial older ingredients and a complete consequence assembled from them. No firstness, new-method or current-worldwide-openness certification is supplied. No narrowed replacement or source repair was made.

## Exact source and custody

The [actual Zenodo record](https://zenodo.org/records/23442760) is version1.0, DOI10.5281/zenodo.23442760, concept23442759. Publication is declared17October2026; actual creation is17October2026 at22:06:29.417068UTC and update at22:06:29.913910UTC. Fresh ordinary requests authenticated the original record, latest, versions and **all** public file objects; latest remains23442760 and versions total one. Exact raw JSON, normalized complete metadata, original file objects, response headers and actual transport/checksum receipts are retained under `sources/`.

| Actual public file | Bytes | SHA256 |
|---|---:|---|
| Convex_Body_SOS_Density_Note_v1.0.pdf | 77950 | f8cbd7733bc63f4918df3b18007d3087ae5cd862a4318c6bddd6f75d58385240 |
| Convex_Body_SOS_Density_Verification_v1.0.zip | 413706 | 52d8ba4dd670ab77184ea6706aacaac0233997c44ad16b041c357f6b5070d38a |

Actual API MD5 values are `8c8f54f455aae1e160b8b56ea8047775` and `531923304284805cf91754391725e0b1`, respectively. Both agree with full downloaded bytes and advertised size. The exact queue row/local PDF candidate agrees with the fresh public PDF; the candidate was not substituted for a download. The actual PDF has five pages. The sole controlling TeX is `sources/published-source/manuscript/main.tex`,15887 bytes, SHA256 `5508a2a2bf9079573b29b4be8b5cdf638b2c2003e4536e5c0e1518c591db7c59`.

All152 ZIP members have unique canonical safe regular paths, no traversal/symlink/encryption, successful CRC/hash reads and bounded expansion1327270 bytes; no nested archive. Every original member was preserved verbatim. The sole public version is distinct from internal `original_submitted` and `current_edition` historical snapshots. Their old status prose and absolute paths were not converted into current publication authority or aliases.

`SOURCE_READY.json` was promptly frozen and sent to root before manuscript/history reading, SHA256 `b3b01936d1b1ce7ce7ab88b0082b92399ebf663d2dcddc81fc50aa72250db8b2`. Its161-file manifest is `445d0532cc31dfca48ade7cf207d5439d83a0da13dc66f4c0451a12db3912c79`; early source seal is `002b8324c97eb11428fa6b747f7b749ea4a1301c953acdb425f19dc168b87da5`. These originals remain unchanged. Final source manifest/seal are additive only.

## Independence and complete proof

The actual complete five pages, every raw page render and full controlling TeX were read. Exact literal assumptions, complete original abstract, explicit constant, derivation, boundary cases and dependency questions were sealed in `INITIAL_INDEPENDENT_RECONSTRUCTION.json` before target primary passages, historical audits or current sibling/root scientific opinions. Early scope seal SHA256 is `f3843a20b67cced9c048c3560725e08e69482e0f5a42c22e536ddf5576a223ed`. The prior OWR file already existed from the immediately preceding unrelated Kaibel review; Laurent's target contribution was first read after this seal. Current sibling verdicts were not read. Both math lanes received only raw primary paths/hashes/provenance after their own early seals.

`ANALYTIC_CHECK.md` supplies a complete checkable derivation. For fixed n>=1, compact convex K with nonempty interior and polynomial f, choose any minimizer a. With H=max Hessian norm, gamma=1+H/2, ell=grad f(a).(x-a), g=ell+gamma||x-a||² and G=max g, constrained first-order optimality gives ell>=0 and Taylor gives0<=f-f*<=g. The positive quadratic ensures0<G<infinity even for affine/constant f. No smooth or semialgebraic boundary or convexity of f is required.

For u=g/G and F(t)=vol{u<=t}, the contraction identity gives

    F(t)<=(t/s)^n F(s), 0<s<=t,

including t>1. The degree-m Dirichlet polynomial A_m has absolute envelope min(1,1/(N sqrt(t))), N=2m+1, and positive core A_m>=2/pi on0<=t<=h=N^-2. Its fixed power Q=A_m(u)^(2L), L=n+2, is a global square. The denominator is at least(2/pi)^(2L)F(h); the core/shell numerator is at most hF(h)(1+2^(n+2)). The **same** core mass cancels, before summing a convergent geometric series. No oscillatory tail mass or part of the body is discarded.

For r>=2L, choose m=floor(r/(2L)); the square-root polynomial has degree<=2mL<=r and N>=r/(2L). This proves the literal bound

    0<=H_r(f,K)-f*<=C_n G/r²,
    C_n=4L²(pi/2)^(2L)(1+2^(n+2)).

For1<=r<2L, constant density supplies the same coarse bound. The same derivative argument gives the stated extension to f of classC² on an open neighborhood of K. The normalized hierarchy is global SOS degree<=2r and integral_K q dx=1, with n-dimensional Lebesgue measure.

The interval proposition also checks: shifted Legendre polynomials give q(t)<=(r+1)² for every feasible SOS density, so at least half its mass lies above1/[2(r+1)²]. Therefore H_r(t,[0,1])>=1/[4(r+1)²]. Applying the polynomial estimate fiberwise gives the same marginal bound on the stated product body. This is a fixed worst-case instance in every dimension, not a positive matching lower rate for every f; constant objectives have zero error.

No arbitrary reference measure, lower-dimensional/nonconvex body, objective-only pushforward hierarchy for general nonconvex f, efficient minimizer-finding method, exact asymptotic coefficient or sharp dimension dependence is inferred. Cumulative endpoint growth is not silently promoted to full interval-centered doubling.

## Actual primary comparison and credit

The entire Laurent contribution, printed2991-2993/actualPDF23-25 of the [2018 OWR report](https://ems.press/content/serial-article-files/46772?nt=1), was read from the unchanged actual publisher PDF bound in the prior packet. It asks for the general convex-body convergence regime and motivates probability measures. Its displayed equations3-4 actually omit the normalization value; the present paper explicitly supplies unit mass. This scope choice is not treated as an OCR correction.

Actual [Slot-Laurent arXiv1905.08142v2](https://arxiv.org/pdf/1905.08142v2), Eq3, confirms the normalized hierarchy. Lemmas1/4 already contain the constrained-gradient/quadratic-proxy reductions. Theorem11 states O(log²r/r²); its complete convex-body proof/lemmas atPDF21-24 and concluding question atPDF29 were inspected. Actual [de Klerk-Laurent arXiv1703.00744v1](https://arxiv.org/pdf/1703.00744v1), Corollary4.3 and complete proof atPDF7-8, also uses the proxy. These mechanisms receive prior credit.

Actual [Totik-Varga2012](https://www.math.u-szeged.hu/pot/5fdp.pdf), Theorem2.1/full proof and relevant Christoffel upper proof, confirms the paper's positive older-ingredient deduction. With endpoint parameter0 and psi(v)=sqrt(v), its degree-m polynomials have P_m(0)=1, sup<=2 and tail A exp[-c(m²t)^(1/4)]. Markov gives a positive core of width1/(8m²); the relative homothety bound and a convergent exponentially decaying dyadic sum yield the same O(m^-2) ratio. Composition/squaring and small-order fallback yield the same upper-rate theorem. The actual Christoffel proof compares shell masses with local core mass. Thus substantial classical localization and broad relative-mass mechanisms are positively established; a newly assembled consequence is not documentary evidence of an earlier printed full-target theorem.

Actual [de Klerk-Laurent arXiv1804.05524v1](https://arxiv.org/pdf/1804.05524v1), Theorem3.1/Corollaries3.2-3.3 and proofs, already supplies interval/Jacobi and product-box worst-case lower rates. The present coarse1/4 bound is directly proved, not falsely attributed as their literal constant. The [final2026 overview](https://ir.cwi.nl/pub/36052/36052.pdf), actualPDF10-11/printed158-159, still records the logarithmic rate for general convex bodies and quadratic rates for special bodies. This confirms that source's contents, not current worldwide openness.

Seven current queries and exact reading scopes are recorded. No earlier explicit full-target theorem was located in the inspected passages; no absence/firstness inference follows. Other Kroo/Ivanov-Totik predecessors, exhaustive citation coverage and all unindexed literature were not freshly read. All six cited bodies were available; five actual primary PDFs were newly fetched and the unchanged OWR report reused without a redundant copy. The read/access ledgers distinguish selected full theorem/proof sections from complete papers and preprint versions from later journal texts.

## Support and actual replay

All152 textual support members were fully decoded, JSON parsed and Python syntax parsed where applicable. Mechanical readability is distinct from full semantic reading of every historical audit. The current proof/moment formulation, package guide, priority clarifications and complete wrapper plus its three replay programs were semantically read; explicit scopes are ledgered.

The exact queue candidate directory supplied an existing outside `BUILD_RECEIPT.json`. Its PDF/ZIP and three external verifier anchors agree with the fresh public bytes; this receipt was bound before use, not fabricated from an internal archive anchor. The unchanged portable verifier passed151 root payload bindings, original/current seven-file editions and nine explicitly registered nested authored manifests. Historical absolute host strings were relocated only through declared family roots, never followed into old host locations.

The verifier performed seven actual isolated finite executions: root exact checks normal/-O/-OO; source-question checker normal only with optimization unset; candidate-aware checker normal/-O/-OO in a reconstructed seven-file original layout. Declared exact output comparisons passed. Root controls cover8 kernel identities,832 rational envelope samples,264 core samples,24 beta moments,12 proxy examples, four exact pyramid matrix orders,16000 degree/floor cases and four rejected false controls. The source-question checker covers33 identities,20000 degree cases,20 cone moments and six nonconvex triangle examples. Candidate-aware checks include16 identities,60 full-mass shell cases,567 pyramid moments,15 exact positive-definite matrices and negative controls. These are finite consistency checks, not universal theorem or priority certificates. Historical floating-point spectral stress was not rerun or newly certified. No new environment or source modification was needed.

## Preservation and completion

All **938** files in the six previous complete owned source/scope trees, including ignored raw caches, remain byte-identical with unchanged file sets: FPS22983138, Hessian23409904, endpoint23131374, cylinder23387774, discotope23074543 and spanning-tree23181280. All **163** original current source-ready bindings, including its manifest/seal, remain unchanged: **1101** preservation checks pass. Stale references into mutable core inputs were not followed. Third-party complete bodies/extracts and all raw renders remain in an entirely ignored cache verified before fetching, with exact inventory.

The final report/verdict, original source custody, actual execution receipts, early reconstruction, read/derivation/search/access ledgers, preservation evidence and timestamped research log are bound by the final own manifest/seal. This lane is100% complete. No followup recommendation or publication/promotion action is supplied. No manuscript repair, page/config/shared core/site/nativeUI/Sheet/Git/deploy/redirect/release or outside individual communication occurred.
