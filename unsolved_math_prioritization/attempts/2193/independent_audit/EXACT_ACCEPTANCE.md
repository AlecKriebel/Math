# Exact acceptance of the scoped literal negative

Decision: ACCEPT_SCOPED_PRIOR_NEGATIVE, ID 2193 / EP-584 / rank 898.

The accepted result is the already documented refutation of the unrestricted H2 density-power claim, and hence of the joint unrestricted H1/H2 claim. The proof applies even if witness cycles may leave H2. It depends explicitly on the published LUW girth theorem. It is not a new discovery and does not resolve the intended sparsity-qualified internal strong-C6 problem.

Accepted original: DENSE_CYCLES_2193_VERIFIED_PRIOR_SAFE.zip, 6084 bytes, SHA-256 0d9ca1f554cab84136aa76a88ace9c8c6864d1d5786724ab51d3531fa56c95b7.

Preferred scope-clarified derivative: DENSE_CYCLES_2193_CLARIFIED_SAFE.zip, 6548 bytes, SHA-256 ebab33c6fba460c05265df0c79e8a711fe8a36650026578fcbd46b52a89a60b7. Its five exact member pins are listed in EXACT_ACCEPTANCE.json and the clarified external manifest. The actual patch changes only PROOF_SCOPE.md, README.md and VERIFICATION_LOG.md. It was replayed on a fresh extraction, reproducing every derivative member byte for byte. The mathematical counterexample is unchanged. Original author-stage status metadata is retained; this document records the subsequent independent acceptance.

The statement digest is b28737a9849838c6181d10b15f85a2d8e4eadce8040f8c437d8dbd8b06db485b. The complete record/report-pair digest is e1601693f7c82888489d082791d70f661cbeb1cdb3bf38c03ebc0927279b48d7. Both were recomputed from the complete supplied corpus files; the EP-584 report key is absent and its prescribed fallback is an empty object. The inherited background was read in full and is explicitly distinguished from the unqualified statement field.

The counterexample is D(5,q): n=2q^5, m=q^6, delta=1/(4q^4), girth at least 10, and delta^2 n^2=q^2/4. Every qualifying H2 has at most one edge, while the target tends to infinity. For every proposed absolute c2>0 choose a prime q>2/sqrt(c2). This is an infinite-family proof reduction, not a computation over finitely many graphs. Because delta^3 n^2=1/(16q^2), this family alone gives no H1-only refutation.

The acceptance excludes fixed-density conclusions with density-dependent thresholds, certification of the June 2026 Eric Li manuscript, certification of the prior note's Proposition 4, current live-page status, exhaustive prior-work absence, originality, human peer review and formal proof certification. Both exact live-page read attempts failed without content. Five public source PDFs were freshly downloaded and matched byte for byte to their prior pins. No publication, repository edit or queue change was performed.

INDEPENDENT_AUDIT.md contains the mathematical and source-scope review. SOURCE_AUDIT.json records fresh retrievals and inspection limits. REPLAY_RESULTS.json records successful archive/member checks, patch replay, all complete corpus pins, the exact record/report hash and all five source-PDF pins. replay_audit.py reproduces these checks when supplied the nonbundled corpus/source files; without them it explicitly skips those input checks. No raw source files, dataset contents or private coordination material are included.
