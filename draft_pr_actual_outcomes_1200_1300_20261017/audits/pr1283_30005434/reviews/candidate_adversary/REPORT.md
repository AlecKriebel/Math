# Candidate adversary audit: PR 1283, Problem 30005434

## Decision and exact scope

The full submitted existence classification is mathematically correct under the displayed workshop axioms, and under the separately inspected monoid convention with its stated qualification. No actionable mathematical counterexample or missing branch was found. The strongest verified theorem is: every nonempty meet-semilattice admits the printed semibrace equations; it admits these equations and the L-algebra axioms exactly when it has a greatest element; in every joint realization the point is greatest and the logical and meet orders agree. Under the added meet-identity convention both existence questions require a greatest element. The complete independently checked derivation is PROOF.md.

This decision is confined to theorem validity and source-statement correspondence. It is not approval to merge, a historical novelty finding, human peer review, or proof-assistant certification. Historical PASS language in the captured packet was treated as a hypothesis, never as evidence that replaced a fresh check. The audit is candidate-informed: the submitted proof, formula, and prior audit were read before this reconstruction. No other family's outputs or parent derivations were read before sealing, and no external individuals were contacted.

## Authentication and inspected sources

The exact original-head snapshot is SHA-256 da2152816bbcd548e4db411ab57992c121009d935e2de59b3f6de93ae304a1d6, head 4624244af725a80a2b7faf111f6b1ca62aaefe37, single parent a72180cf68ed6c9c54360cfd61b7a6567f5a0a5f. All eight captured files, totaling 43,768 bytes, match their snapshot SHA-256, byte counts, and Git blob SHA-1. All eight were read in full. INPUT_RECEIPTS.json is a receipt inventory, not a declaration of authored manifest membership. verify_inputs.py reproduces current authentication and public-side preservation-ledger checks.

The locally available [official workshop source](https://ems.press/content/serial-article-files/47003) is 286,244 bytes, SHA-256 0ba13c573755289bb62e119df381d19e03a31cb3fff8e1ff3e240dce8dfeeefc. I read the contribution on printed pages 544-547 in supplied extracted text, inspected the supplied page images, then independently rendered PDF pages 8-11 and inspected all four fresh renders. Definition 1, the semilattice footnote, Definition 2, both Problem 3 questions, Problem 10, and surrounding context were checked visually. The footprint of the surrounding self-similarity discussion does not impose an extra axiom on Definition 2.

The footnote gives only associativity, commutativity, and idempotence for meet. Definition 2 uses this semilattice and a point e, then gives exactly S1-S4 in PROOF.md. It does not display the meet-identity equation e∧x=x. Problem 3 asks the two existence questions separately. No finiteness, distributivity, joins, bottom, nontriviality, cancellation, or self-similarity restriction is stated in these definitions/questions. The prose expressing surprise at the absence of an obvious trivial construction does not supply a further equation. This report makes no inference about an author's unstated intent.

The local [enumeration-paper v4 source](https://arxiv.org/pdf/2206.04955v4) is 429,694 bytes, SHA-256 cd5551caffcc3c69959fbc72bbcdc1b0d2d736aa14569fd5df34a257dd435ea6. Definition 3.1 was read in extracted text and on an independently rendered full page 5. It explicitly requires a commutative monoid with neutral e before giving the same four equations. On meet-semilattices, this is exactly the additional greatest-element requirement. The paper's definition itself permits a general commutative monoid; the theorem concerns the stated restriction to semilattices, not all monoids.

Both PDF pins were recomputed from the available local copies. No independent network redownload was performed. Raw PDFs, extracts, and images are private, read-only source inputs and are excluded from this authored bundle. Source version chronology, prior literature, and priority are not independently assessed here. The captured metadata's AIMS 2024 source and the workshop's cited Rump 2008 article were not inspected; no exact wording, access status, or priority assertion about them is newly certified by this report.

## Symbolic adversarial audit

I tried materially different symbolic mechanisms as well as checking every submitted branch. PROOF.md proves necessity by local S1/S3 substitutions and L3, rather than repeating the candidate's translation argument. It proves sufficiency through principal-ideal meet homomorphisms and the absorption law F_a∘F_x=F_a for a≤x. This derivation independently covers the same formula without relying on finite checks, joins, distributivity, or completeness.

| Submitted issue | Adversarial check | Outcome |
| --- | --- | --- |
| Right projection and empty/singleton boundary | Substitute all four equations; inspect diagonal | Correct for every prescribed e on nonempty X; joint only on singleton |
| Equality of translations implies equal points | Evaluate at each of the two points and use L3 | Correct; distinct from injectivity of individual translations |
| Necessity of top and order equality | New local-substitution proof; examine separation deletion | Correct; separation is essential |
| Totality and e branch | Check e itself, diagonal, top column, and impossible meet=e in other branch | Correct |
| S1 all branch patterns | Principal-ideal factorization; independently all finite triples | Correct, including incomparable arguments |
| S3 nested comparisons | Absorption lemma including a=x, x≤z and x≰z | Correct; no omitted equality branch |
| L2 | Derive from S3 and commutativity alone; check tables explicitly | Correct and redundant in a joint verification |
| Infinite, bottomless and no-join scope | Complete symbolic proof and explicit order constructions | Correct; sampled finite checks do not certify infinity |
| Nondistributivity | M3/N5 explicit checks and structural proof | Correct |
| Problem 10 negative control | Read exact y-valued branch; Boolean-lattice witness | Correct failure of S1, with no claim to refute Problem 10's L-algebra assertion |
| Product discussion | Coordinate separation and distinct B2 product formulas | Correct |
| Added monoid convention | Meet identity iff greatest element | Correct after restricting to semilattices |

No axiom of choice for an indexed family, bottom, arbitrary meet, join, order decision algorithm, or lattice distributivity is used. The sufficiency definition makes an ordinary classical case distinction. The one arbitrary selected point for the first question is one existential witness, not a choice function. If the two structures were initially assigned different distinguished elements, their diagonal identities force those points to coincide.

## Independent finite mechanism and countermodels

verify_algebra.py enumerates every labelled commutative idempotent binary operation table for n=1,2,3,4, then retains the associative tables. This is independent of the candidate's reported generation of naturally labelled posets. The table search covers 4,126 candidate meet tables, yielding 88 labelled meet-semilattices, 45 with a greatest element. It checks projection for every e (336 structures) and the new construction for each top (45 structures). It exhausts every L1-constrained multiplication table for each retained meet and every e, totaling 1,245,432 tables, and independently checks every defining identity and equality of orders on all 243 qualifying joint structures. These are labelled counts, not isomorphism-class counts.

| n | Labelled meet tables | With top | Projection checks | L1 tables | Joint structures |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 1 | 1 | 1 | 1 | 1 |
| 2 | 2 | 2 | 4 | 4 | 2 |
| 3 | 9 | 6 | 27 | 243 | 12 |
| 4 | 76 | 36 | 304 | 1,245,184 | 228 |

Additional controls check M3, N5, and an exact finite operation sample of the nonpositive-integer chain. The wrong Problem 10 branch fails S1 at (a,a,b) on the Boolean lattice. Reversing the inequality is also rejected. A three-element no-top model satisfies all four semibrace equations and L1/L2 when separation is omitted; its explicit tables in PROOF.md demonstrate why the necessity proof cannot drop L3.

Normal, -O, and -OO execution gives byte-identical deterministic outputs for both durable validators. Two deliberately bad algebra inputs are rejected with exit code 2 in all three modes. There are no assert statements whose disappearance could disable validation. CHECK_RESULTS.json, BYTE_AUDIT.json, and CHECK_EXECUTION.json preserve the results and receipts. Finite tests are consistency evidence, never the universal proof or formal certification.

## Historical evidence and actionable repair

Current public files and the submitted manifest match the snapshot. Every recorded public-side changed or unchanged segment of BYTE_PRESERVATION.json matches its stated hash, byte ranges partition both length coordinates arithmetically, and all four named public unchanged regions match their stated hashes. The old frozen original files are not included. Therefore original-side content identity, prior auditor independence, prior script execution, and reported original-to-public reconstruction are not newly verified. Validating hashes of existing public slices cannot authenticate absent historical bytes. verify_inputs.py and BYTE_AUDIT.json state this limit explicitly.

The earlier natural-label counts through six elements, 2,152 pointed structures, 51 top constructions, 114,745 L1 tables, and old normal/-O comparison hash are historical declarations in the eight-file packet. This audit does not claim to have reproduced them. The fresh table enumeration above has a different, explicitly documented scope and provides its own durable program. No discrepancy follows from different label multiplicities.

No mathematical repair to PROOF_CLASSIFICATION.md is required. For any newly promoted package, the actionable evidence repair is to attach the fresh durable verification code/results or label earlier unprovided computations as historical, and keep current theorem validation distinct from original-byte reconstruction, novelty, and intended-authorial-scope claims. If the old preservation claim itself is to be newly certified, supply the exact earlier proof/audit bytes or a genuinely available immutable source. Do not substitute current public hashes for those missing inputs.

## Strongest result, remaining gap, and seal boundary

The whole stated two-part existence theorem, prescribed-point/order consequences, and monoid qualification are established by a complete proof in PROOF.md and the inspected source text. No mathematical gap remains in that scope. Priority and historical input provenance are separate unverified matters. No Git/index/ref/PR/sheet/Zenodo mutation or external contact was performed. Only this review directory and its private scratch were written. Authored manifest membership is exclusively the literal files list in MANIFEST.json, whose rows have relative_path, bytes, and sha256; receipts that mention absolute source paths never become members. The manifest excludes itself and SEAL.json, which binds the manifest separately.
