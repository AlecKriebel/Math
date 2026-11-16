# Editorial INITIAL: exact semidefinite TSP complexity

Frozen source-based assessment, 2026-11-16T06:49:18Z. Record 23204250, catalogue row 139. Editorial completion estimate: 30% of the private page and its reviewable custody package. This is an editorial reconstruction, not a fresh scientific certification.

## Independence and exposure

The assignment disclosed that the scientific review had passed. I therefore do not claim status blindness. Before this INITIAL I did not open the current root scientific clearance, root proof, scientific peer findings, or adversarial findings. I personally read the entire controlling TeX (all 189 lines, 18,972 bytes), extracted and read the complete six-page actual PDF, and individually viewed six newly generated page rasters in this owned folder. The rasters were produced directly with installed Poppler, without running any native scientific program or campaign helper. I read the complete actual native record response and files response, including all three original record file objects and complete file entries, the distinct native description, and the rights notices in both ZIP payloads.

The source intake's unread false/null fields are past-state statements, not errors to normalize. Its `printed_fields_inspected: false`, `printed_date: null`, `printed_version: null`, and the analogous TeX/PDF unread fields remain literally untouched in the frozen originals. My later reading adds a new state here. The printed date is October 6, 2026. No printed version appears. The native record has no version field (absence, not an empty or invented version). Its publication date is 2026-10-06; creation is 2026-10-07T05:38:14.026094+00:00.

## Exact claim and mechanism reconstructed from the source

For the convex hull of undirected Hamiltonian-cycle edge incidence vectors in the complete graph on N cities, the note states that there are c > 0 and N0 such that every integer N >= N0 satisfies

`2^(cN) <= xc_psd,R(P_TSP(N)) <= 2(N-1)+(N-1)(N-2)2^(N-3)`.

The quantity is the minimum order r of one real symmetric PSD matrix in an exact affine lift `P = pi(L intersect S_+^r)`, with unrestricted affine equations and affine output map. Several blocks count by their total order. The result is thus `2^Theta(N)` in matrix order. It is not an approximate relaxation or an algorithm running-time claim. In particular, the manuscript excludes coefficient bit complexity, arbitrary TSP algorithms, P versus NP, particular SDP hierarchies, complex-cone extensions, and stable-set extensions.

The substantial new lower-bound ingredient is OpenAI's shifted matching PSD-rank theorem, manuscript dated October 5, pinned at `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Its form fixes 0 < rho < 1 and gives exponential real PSD rank for sufficiently large even n. The note appends one scalar block to unshifted factors to obtain shifted factors, losing only one in rank; it uses rho = 1/2. A finite evaluation-cone argument converts any exact affine PSD lift into factors for tight nonnegative slacks, including odd-cut matching slacks. The note attributes this to the general cone-factorization framework and checks the affine bridge without a strict-feasibility assumption. The endpoint rho = 1 is excluded and has a polynomial edge-diagonal factorization.

The TSP transfer uses faces and affine images without increasing order. Yannakakis's established 3n-city gadget has left/right cliques joined by n forced two-edge paths through middle vertices. Residual clique edges give two perfect matchings whose colored union must be connected. Completing any first matching cyclically supplies a tour, proving surjectivity, not injectivity. The 2n-city variant forces diagonal cross edges to one and other cross edges to zero. The one constraints are essential: removing them permits projected paths. Small n = 2 is explicitly addressed in both gadgets.

All-city-count padding forces a path through new cities and contracts it to an old vertex. Its endpoint projection adds the two endpoint incident coordinates. The m >= 3 restriction ensures distinct remaining neighbors. Choosing even `n = 2 floor(N/4)` yields an exponential lower bound for every sufficiently large integer N, rather than only a subsequence. The upper bound uses the acyclic subset-state permutation network, whose `2q+q(q-1)2^(q-2)` arc variables for q = N-1 embed diagonally in a PSD matrix. Unit-flow decomposition and edge labels give exactly the tour polytope.

## Editorial interpretation and scholarly credit

The accessible explanation should say that an exact representation can use extra coordinates and a PSD matrix, but even the best such real representation must grow exponentially with the number of cities. An exponential-sized construction gives the matching scale. It should make the definition of size and exactness visible near the theorem, rather than hide them in a disclaimer.

This is an explicit consequence note with constructions and verification, not an independent lower-bound method or a priority claim. The page must credit OpenAI's matching breakthrough prominently, retain Yannakakis, Rothvoss, Gouveia-Parrilo-Thomas, Lee-Raghavendra-Steurer, Lee-Prakash-de Wolf-Yuen, and Held-Karp. The older unrestricted TSP exponent is 1/13 in LRS; LPDWY corrects a computational estimate to a tilde-Omega exponent 1/11. The tilde suppresses logarithmic factors. The manuscript's literature search does not establish priority. No earlier-work claim should be strengthened by editorial phrasing.

The manuscript and native description affirm independent mathematical scrutiny of the exponential matching input. This must not be silently replaced with an unverified hypothetical condition. The review comparison still needs to confirm what current clearance supports. Lean is a different level of evidence: the actual statements described by the note concern superpolynomial n^C growth only. Neither the exponential matching theorem nor the TSP theorem is claimed Lean-verified; full Lean builds were not reproduced. Finite graph checks are supporting checks, not asymptotic proof. Conventional human peer review has not occurred. AI use was extensive.

## Record, page, and custody requirements

The entire manuscript abstract and complete distinct native record description should appear separately and accurately. Use the original title, Alec Kriebel, the supplied ORCID, October 6, 2026, and unrefereed preprint status. No version label should be invented. Native asset order is `paper.pdf` (89,174 bytes), `tsp-verification.zip` (71,399 bytes), `tsp-source.zip` (11,448 bytes). Both ZIPs together contain 35 regular payload occurrences; there is one controlling TeX and no embedded PDF. The page should embed the unchanged searchable standalone PDF, supply open/download controls and native asset links in that order, and include original Zenodo links and BibTeX.

New prose/documentation has CC BY 4.0 rights; new code has MIT rights. Original assets and third-party rights remain intact. No blanket mixed-archive license is justified. Native record license object is literally `{ "id": "cc-by-4.0" }`; that is record metadata, not permission to erase the package's separate code and third-party terms.

The private preview should use a plain white, Arial, blog-like site frame with semantic `main#main`, readable equations, unique title/description and citation/JSON-LD metadata, and noindex. Canonical URL, production base URL, publication authority, AA outcome, and follow-up stay null. A natural proposed slug may be recorded without assigning a production URL. No follow-up question is justified by this editorial source reading; use null. Passive interest in independent verification, substantive extension, or journal development is appropriate, with authorship only for actual contribution. No outreach is authorized.

## Source pins and remaining work

Actual PDF: SHA256 `9b1b56f516183c309b5510422c51b9b7050660384101f592251f1265c1d38a72`. Controlling TeX: `97917390b62c13412f4e5734c3e64e654033f5ca4b8ef05d683b9067ea7e17ea`. SOURCE_READY: `13d913127abab98d78c3758516884b09f7e4849b5e6c07a3e0fd44c502147ec9`. SOURCE_READY_SEAL: `94bd3bbf71c9fd618b6bf12616120aace2a6d3fe04707d6f73bb1bd787dd8ecf`.

Remaining work: receive root acknowledgement that this INITIAL is frozen; then read the root scientific authority and proof, compare them with this reconstruction, inspect the actual reference site frame, author and inspect the full private page, and close the exact owned file/directory manifest. No public copy has been authored at this checkpoint. No source, scientific, root, prior packet, website, Git, Sheet, network, deployment, redirect, or external-contact mutation has been made.
